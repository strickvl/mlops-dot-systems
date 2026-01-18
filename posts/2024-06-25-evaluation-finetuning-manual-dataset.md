---
author: Alex Strick van Linschoten
categories:
  - llms
  - finetuning
  - isafpr
  - afghanistan
  - datasets
  - evaluation
  - miniproject
date: "2024-06-25"
description: "I summarise the kinds of evaluations that are needed for a structured data generation task."
layout: post
title: "How to think about creating a dataset for LLM finetuning evaluation"
toc: true
image: images/eval-preview.png
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/posts/2024-06-25-evaluation-finetuning-manual-dataset.html"
---

I [previously](https://mlops.systems/posts/2024-06-17-one-click-finetuning.html) experimented with one-click LLM finetuning providers and now is a good time to return to the core of the matter: evaluating how well all these fine-tuned models and experiments are faring. I have a gut feeling that my fine-tuned models did pretty well, but we're not in the business of gut feeling so I'm hoping to be able to put some real numbers down to either prove or disprove this hypothesis.

As a quick reminder if you didn't read [any of the previous posts in the series](https://mlops.systems/#category=isafpr), I'm building a model that can take a press release text like this:

> "2011-11-S-011 ISAF Joint Command - Afghanistan For Immediate Release KABUL, Afghanistan (Nov. 7, 2011) — A combined Afghan and coalition security force conducted an operation in search of a Haqqani facilitator in Argo district, Badakshan province. The facilitator coordinates suicide attacks with other insurgent leaders in the area. During the operation, a local national male failed to comply with repeated verbal warnings and displayed hostile intent toward the security force. The security force engaged the individual, resulting in his death. The security force confiscated a shotgun and intelligence linking the local national to the Haqqani network. The security force also detained two suspected insurgents during the operation."

…and then turn it into structured data (i.e. a JSON object) like this:

```json
{
    'name': '1',
    'start_date': '2011-11-07',
    'event_type': ['captureandkill'],
    'province': ['badakhshan'],
    'target_group': ['haqqani'],
    'min_killed': 1,
    'min_captured': 2,
    'killq': True,
    'captureq': True,
    'killcaptureraid': True,
    'airstrike': False,
    'noshotsfired': False,
    'min_leaders_killed': 0,
    'min_leaders_captured': 0
}
```

I've now fine-tuned several models and I want to get a sense of how good these are. I showcased [some initial baseline evaluations](https://mlops.systems/posts/2024-06-03-isafpr-evaluating-baseline.html) using OpenAI's `gpt-4-turbo` but I want to pit model against model now.

I'm also interested in teasing out some of the edge cases where I know I struggled as a human annotator. (I [released the dataset](https://huggingface.co/datasets/strickvl/isafpressreleases) for this project publicly on the Hugging Face Hub and also was responsible for annotating every single item so I know the data intimately.) I can even consider using the hard examples to generate some synthetic data to boost performance on those edge cases, but that's a task for much later on.

This blogpost is a prose overview of some of the evaluations I'm adding to my suite of tests (and why I'm adding them). I learned a lot from [Hamel Husain's "Your AI Product Needs Evals" blogpost](https://hamel.dev/blog/posts/evals/) and if you're interested in this I'd recommend reading it and then actually implementing his suggestions.

## Core evaluations for accuracy

The most important measurement to start with is just a pure "did the LLM make a correct prediction or not?" If I was doing all these evaluations manually myself, I'd take a look at the example above, for example, and ask myself "was the start date of the event mentioned in the blogpost really '2011-11-07' as predicted by the model?" and "did the event take place in Badakhshan province?" and "were the Haqqanis the group targeted?"

It's fairly straightforward to make these determinations when comparing each property one by one. I can then repeat this over every example in my test slice of my dataset and take an average if I want a single aggregate figure, or I can get individual figures for dates, provinces, target groups and so on (to know if maybe there's one part of the prediction it struggles with most).

## Out of domain data

The ISAF mission has come to an end, so I don't have to worry too much about new data and having to adapt to a continuously changing world, but it is possible that some smaller groups weren't well represented in the training data (for predicting the target group, for example) so I want to know how well my model does with data it hasn't seen.

My prompt passes in the schema for the data and I encourage it to follow the schema in its response, but if there's a new group will it add the new group to the schema? I can write an evaluation to test this.

Another edge case is the possibility that a press release doesn't follow the standard format. Having read them all, I know that the vast majority are pretty formulaic, but sometimes there is a special event or incident which caused the author of the press release to depart from the standard formula. I want to know that my model will:

a. not just make something up so as to have *some* kind of JSON response even if the press release is about someone's birthday party
b. even better, produce some sort of error code or blank response when this happens.

I can use examples of this out of domain data to see what happens, and put a value to how often my model will just hallucinate something out of nothing. This will be important since the name of the game for this model is accuracy.

## Gradations of 'some', 'a few', 'many'

The press releases try to give some information without actually giving too much. Indeed, when I published [my report](https://www.afghanistan-analysts.org/en/special-reports/a-knock-on-the-door-22-months-of-isaf-press-releases/) on the press releases back in 2011, ISAF even [issued a press release](https://www.dvidshub.net/news/78455/isaf-responds-use-aan-news-releases-study) (!) in which they stated that:

> "Release of information in insurgent warfare is not always made public, so studies based on the use of press releases can be both incomplete and problematic. […] Authoritative research cannot be conducted through mere analysis of press releases, since the release of information through such releases is, by design, incomplete."

So reading the press releases is very much an exercise in reading between the lines. In the press release cited earlier, all the numbers are specific ("a facilitator", "a male", "two insurgents") so it's easy to put numbers to how many were killed or captured. In many of the press releases, particularly during times where raids were being conducted at a very high tempo, you have to just take assumptions about what their words mean and assign minimum values to those words.

So 'a couple' meant at least two, but 'a few' meant 3 or more. Similarly 'dozens' means multiple dozens so that meant a minimum value of at least 24. From the original report:

> "If a press release said that ‘insurgents’ were detained, without further details, we assigned that incident as having a minimum number of 2 detained (since we could not be sure of more). ‘A couple’ we took to mean 2. ‘Several’ we took to mean at least 3, even though on other occasions ‘several’ was used to refer to 7 or 8. Other terms we classified as denoting at least 3 included: ‘a few’, ‘some’, ‘a group’, ‘a small group’ and ‘multiple’; these terms sometimes were used to refer to far larger numbers but we chose the smaller number (if no other information was available in the press release) in order to come up with a minimally acceptable figure. ‘Numerous’ and ‘a handful’ we took to mean at least 4, and ‘a large number’ at least 5."

The reports mostly referred to events that had taken place that day or the day before, but occasionally they'd refer to events that took place "last Thursday" or "last week" and so then you'd have to know what day the press release was issued and then make calculations accordingly. For this backwards-referring time assignations, I'm particularly interested (read: concerned!) to know how well my LLMs did. Whatever score we get, it's probably fixable with a bit of manual parsing and logic, but we need to know if there's a problem or not first.

Generally speaking there were province names assigned to incidents (all but 23, to be precise) but when they weren't, then the LLM has to work back from a village name, potentially, or just specify that an incident took place in southern Afghanistan or Afghanistan as a whole. On a few occasions, the press release actually made an error, stating that village X or Y was in a particular province, when this was incorrect and it was in a different province. So for this, would we expect the LLM to assign the event to the correct province for that village, or just retain the error in the press release?

Sometimes a press release might refer to an event having taken place "in the provincial capital of X province" but without mentioning that city by name. So the LLM will have to have some knowledge of these things and I want to test how well it performs with this.

These might seem like tiny errors to get wrong, but for a project like this (where my report was making some strong accusations and drawing certain conclusions based on the data), it wouldn't do to get things factually wrong. For an internal-facing LLM-powered chatbot, the price of mistakes is minimal, but for a project like this, there are potentially far more serious consequences which is why I'm putting together such detailed evaluations.

## Spelling variation

Another issue with some of the press releases is that they use a variety of spellings for the same locations or names of individuals. For some things — province names, for example — it makes sense to standardise on a fixed naming convention but for others it's not always clear what to do. So our evaluation should ensure that common variations of certain provinces or designations or names are captured correctly by the LLM output.

## Complex stories

Some stories are very complicated and there may be no correct way to assign numbers, for example, to the text that was published. In those cases when annotating I often just left the minimum numbers at zero even though we know that *something* happened. Would the LLM also make the same call? What is the threshold for deciding not to take a chance on making a guess?

## Next step

The obvious next step is to actually code up these evaluation criteria and run those across our fine-tuned LLMs as well as the API-driven proprietary ones. I'll be working on that over the coming days. Luckily, I did most of the work to identify all of the above when I first wrote the report so there isn't much ground that needs to be broken so much as just sitting down and getting it done.