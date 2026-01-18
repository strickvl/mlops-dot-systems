---
author: Alex Strick van Linschoten
categories:
  - zenml
  - python
  - softwareengineering
date: "2025-12-23"
description: "Anatomy of a PR"
layout: post
title: "Anatomy of a PR"
toc: true
draft: true
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/posts/2025-12-23-anatomy-of-a-pr.html"
---

In [ZenML](https://github.com/zenml-io/zenml) we have a CLI command that helps you clean up the artifacts from old pipeline runs. People use ZenML for automating their ML pipelines, so between experimentation as well as just ordinary production usage, you can probably imagine that people might want to clean up from time to time. We automatically version the inputs and outputs of steps within each pipeline run, so for certain types of workflows this can add up over time.

At a certain point we added in a `zenml artifact prune` command which allowed users to clean up artifacts from pipeline runs which have already been deleted. The way ZenML works is that we connect to your pre-existing infrastructure (think: an S3 bucket, a GCS bucket, etc.) and store the artifacts there; ZenML doesn't own the storage, it just points to it and stores related metadata.

So the pre-existing CLI command allowed the user to clean these orphaned artifacts from both their storage as well as from ZenML's metadata store. We had some CLI options that allowed you to pick how you wanted this to happen:

| Option | Short | Description |
| --- | --- | --- |
| `--only-artifact` | `-a` | Only delete artifact data from artifact store, keep metadata in DB |
| `--only-metadata` | `-m` | Only delete metadata from DB, keep artifact data in store |
| `--yes` | `-y` | Skip confirmation prompt |
| `--ignore-errors` | `-i` | Continue to next artifact if deletion fails |

## Current implementation

This command was implemented back in 2022, so as far as ZenML's concerned it's a pretty old bit of the codebase and hasn't really been modified much over past three years. I had occasion to use this command while testing out some new different feature and I noticed it was running much slower than I expected. Looking at the code, it was clear why this was happening.

The current implementation goes like this:

1. We get a `List` of all the unused artifacts. ('Unused' here meaning that it isn't referenced in some existing pipeline run, either as the input to a step or an output of a step.)
2. We loop over this list and (depending on which options the user passed into the CLI invocation):
  - delete the artifact version
  - delete the artifact itself if there are no more versions of that artifact version that still exist
  - delete the metadata / references to that artifact from the (ZenML) database

The issue with this implementation is that it's not very efficient. Even from this prose explanation of how the code works, you'll have already noticed that we're looping over the artifacts one by one, and each step of the loop is itself already potentially a multi-step process.

I thought I'd make some improvements to this CLI command and so this blog is just my attempt to take you along for the ride.

## Initial improvement ideas

Based on what I know of the current implementation so far, my initial thoughts were to firstly try to make this more efficient by running the deletion of artifacts in parallel. So instead of iterating over the items one by one, we can have a pool of workers that each handle the deletion of a single artifact.

This seemed easy enough to implement, but I thought a bit more about how this command might otherwise have been improved:

- we already check to see whether the artifact is a step input or output, but we don't check to see whether it's referenced by a `Model` (ZenML has this concept of a 'Model' which is a bit different than just an ML model, but it includes things like data / metadata etc...). I'm not fully sure about the tradeoffs about including this check to see if there's a reference inside a `Model`. Models were implemented much later than this CLI command, so it's possible that we just forgot to include the check here, but it's also possible that the check is redundant. I'll have to think about this more.
- there's relatively little feedback given to the user about what's happening, or at least it could be much improved
- for a destructive operation like this, it would be nice to have a `--dry-run` option which shows which artifacts / versions / files would be deleted
- there are probably some improvements around filtering we could add in, like having an `--older-than` option where artifact versions would need to be older than some duration (e.g. 7 days, 1 year etc)
- we could set a `--keep-latest N` option where the user would mean that we keep the N most recent artifact versions
- we could add a `--show-size` option which would display the total storage that would be freed (or that was freed) by running the command
- possibly we could have a `--project` and/or `--workspace` scoping that would only delete artifacts from a specific project / workspace

There were some other more technical improvements that seemed useful to make:

- no need for multiple `Client()` instantiations. We can just reuse the one that has been made earlier in the code.
- there's a pre-existing `client.prune_artifacts()` method that uses a more efficient batch SQL deletion operation so we might want to use that directly?
- it seems like there's a stale data bug whereby we're checking for the state artifact versions for an artifact but it's not updated since we originally fetched it. For this reason as well, if multiple versions belong to the same parent artifact, we'll try to delete the parent artifact multiple times.

## Thinking through whether to include a `Model` check

In the current implementation we check to see whether an artifact is a step input or output in the following way:

```python
unused_filter = and_(
    ArtifactVersionSchema.id.notin_(
        select(StepRunOutputArtifactSchema.artifact_id)
    ),
    ArtifactVersionSchema.id.notin_(
        select(StepRunInputArtifactSchema.artifact_id)
    ),
)
```

That `and_` is a `sqlmodel` construct that returns a boolean expression that is true if both conditions are true. So we just are making sure that the artifact is not a step input or output. It does not check to see whether the artifact is a `Model` or not.

At this point we can ask: can an artifact be linked to a `Model` without being linked to a `Step`? Absolutely! In code it might look something like this:

```python
# Outside any step context (e.g., in a script or notebook)
from zenml import save_artifact, link_artifact_to_model, Model

# 1. Create artifact outside step - no step link is created
artifact = save_artifact(my_data, name="training_data")

# 2. Link it to a model version
model = Model(name="fraud_detector", version="production")
link_artifact_to_model(artifact, model=model)
```

So if we did this, we'd have an artifact that is linked to a model but not to a step. When we did `zenml artifact prune`, this artifact would be deleted because we didn't check to see whether it was linked to a `Model`.

I think when a user runs `zenml artifact prune`, they would expect to delete artifacts that are truly orphaned, not referenced by anything meaningful, and that would include artifacts that are linked to a `Model` but not to a `Step`.

Based on all of this, and looking at the `git` history a bit, I think we probably just forgot to add this check when the Model Control Plane feature and the `Model` data model (yes I can hear how this sounds!) was added.

The fix is fairly straightforward: we add the missing check to see whether the artifact is linked to a `Model`:

```python
unused_filter = and_(
    ArtifactVersionSchema.id.notin_(
        select(StepRunOutputArtifactSchema.artifact_id)
    ),
    ArtifactVersionSchema.id.notin_(
        select(StepRunInputArtifactSchema.artifact_id)
    ),
    # Missing check - should be added:
    ArtifactVersionSchema.id.notin_(
        select(ModelVersionArtifactSchema.artifact_version_id)
    ),
)
```

I think there will be some tests that need updating to account for this change, and I think we might want also to consider an update to the `zenml artifact prune` command to add a `--models` option that would allow users to prune artifacts that are linked to a `Model` but not to a `Step`.
