---
aliases:
- /tools/redactionmodel/computervision/mlops/2022/05/24/data-versioning-dvc.html
author: Alex Strick van Linschoten
categories:
- tools
- redactionmodel
- computervision
- mlops
date: '2022-05-24'
description: I show you why you probably want to be versioning your data alongside
  your code. I introduce the basic functionality of DVC, the industry-standard tool
  for data versioning. I also explain specifically how I'm using DVC for my computer
  vision project.
image: dvc/dvclogo.png
layout: post
title: 'More Data, More Problems: Using DVC to handle data versioning for a computer
  vision problem'
toc: true

---

_(This is part of a series of blog posts documenting my work to train a model that detects redactions in documents. To read other posts, check out [the `redactionmodel` taglist](https://mlops.systems/categories/#redactionmodel).)_

If you've been following along as I train an object detection model to detect redactions, you'll know that there have been a few iterations in how I go about doing this. For the most part, though, the dataset has remained relatively static. I downloaded a huge tranche of publicly-released government documents right at the beginning and aside from [my experiments](https://mlops.systems/tools/redactionmodel/computervision/2022/04/06/synthetic-data-results.html) in [synthetic data creation](https://mlops.systems/redactionmodel/computervision/python/tools/2022/02/10/synthetic-image-data.html) I haven't really been adding to this data.

When it comes to turning this model into something that can work *in production*, it won't be enough to have a big bucket of image files that I train on. I'll need to have a bit more control and fine-grained segmentation of the ways this data is being used. In short, if I want to be able to reproduce my workflows then I need some kind of data versioning.

## 🚦 TL;DR: Data Versioning for Computer Vision

- ⛽️ We version our data because it is the fuel for our model development and experimentation process.
- 💻 Data versioning tools like DVC allow you to apply the same mental model you have for `git` to your data.
- ⋔ The ability to 'branch' off your data gives you the flexibility to experiment just as the same is true for branching off your code to try out some new behaviour.
- [DVC](https://dvc.org/) is probably the leading tool that allows you to version your data and flexibly access all the previous 'commits' and checkpoints you make along the way.

## 🤔 Why do we need data versioning? Isn't `git` enough?

If the lifeblood of traditional software engineering is code then the equivalent for machine learning is data. We solve the problem of checkpointing what our code looked like at a particular moment with `git` and online hubs like Github. Until recently there weren't many equivalent options for data. We're trying to solve the problem that often occurs if you're asked to reproduce the data that was used to train a particular iteration of a model from some point in the past. Without some kind of data version control this is more or less impossible, particularly if your data is constantly changing.

Even in my case for this redaction project, I wasn't ingesting new data all the time but I *was* removing bad annotations or updating those annotations as I conducted error analysis or [used tools like FiftyOne](https://mlops.systems/redactionmodel/computervision/tools/debugging/jupyter/2022/03/12/fiftyone-computervision.html) to understand why my model wasn't performing as well as I'd have liked.

Luckily there's a pretty great tool in this space that seems to be more or less unchallenged for what it does in the data versioning domain: [Data Version Control](https://dvc.org) or [DVC](https://dvc.org).

## 👩‍💻 DVC Use Cases

DVC does many things, but for our purposes at this moment its core value is that it helps us version our data. It also handles the case where we have large files or a dataset that changes a lot and where we might end up having problems with storing all the versions of this data.

The core behaviour we want to use with a data versioning tool is to access our data at one particular moment. Just like you incrementally annotate your code updates using `git`, with sometimes atomic progressions as you do your work, so it is with DVC that you can checkpoint your data as you make changes.

At the beginning this was a slight mental adjustment for me. When working on a project it is now second nature to regularly make `git` commits along the way, but I wasn't in the habit of making regular data commits as a second step. In the long-run, this requires a bit of a mental shift but this is exactly what will enable the benefits that using a tool like DVC brings.

In particular, being able to experiment with data in a way that you can always roll-back from feels pretty liberating once you've covered your back with DVC. Just as you can use create `git` branches for your code, so you can create branches for your versioned data. [Checking out](https://dvc.org/doc/command-reference/checkout) the precise data used for some zany experiment you did is pretty painless. If you realise that the experiment is a dead-end and it's not helping you move forward, just rewind and reset your data back to a useable state from before you had that crazy idea to create a million synthetic images :)

One other thing: DVC is built on top of `git` and it follows many of the mental models you might have about how versioning works. In this way, DVC luckily is smart about how it allows you to make incremental changes to your data. When it calculates the `diff` of your dataset before and after, it really is able to do some atomic updates and logging of what changed rather than just storing all the files multiple times over. This helps prevent you building up a really huge data cache and it helps the whole process be efficient.

{% include info.html text="I've mentioned this for other tools like Evidently before so I should also note that the DVC online community (https://dvc.org/community) is a pretty friendly and helpful place to hang out and learn about data versioning or to troubleshoot your problems. Nobody will tell you to RTFM here and their community events are generally beginner-friendly in my experience. This makes a big difference so they should be commended for the efforts they take to foster this kind community atmosphere. ❤️" %}

## 🚀 How to get started with DVC

The basics are mostly similar to how you'd use a tool like `git`:

- You [`init`](https://dvc.org/doc/command-reference/init) your repository. This add some DVC superpowers on top of what you already have with `git`.
- You [specify which files](https://dvc.org/doc/command-reference/add) you want to have DVC manage and track. It would make a lot of sense, for example, to have DVC handle tracking your models, your image files and your data annotations (if those exist as separate files).
- You can optionally also [specify a `remote` location](https://dvc.org/doc/command-reference/remote) where you want these files to be stored. (DVC supports several types of remote storage: local file system, SSH, Amazon S3, Google Cloud Storage, HTTP, HDFS, among others.)

(To get a taste of the full workflow when using DVC for data tracking I'd recommend something like the basic tutorial they have [here](https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial). They also [recently added a three-part tutorial](https://dvc.org/blog/end-to-end-computer-vision-api-part-1-data-versioning-and-ml-pipelines) specific to computer vision that you might want to check out.)

If you want to use DVC programmatically using their Python API, you can get some information on this [in their docs here](https://dvc.org/doc/api-reference). Unfortunately, these docs are incomplete and you'll have to experiment a bit if you want to do anything beyond the simple functionality they themselves list. I'm told it behaves very similarly to how [a tool like GitPython](https://gitpython.readthedocs.io/en/stable/intro.html) works, where you can just use the equivalent `add()` or `checkout()` function call that corresponds to a DVC CLI command, but given the lack of documentation it's a bit harder to get a full sense of what is possible.

{% include alert.html text="DVC includes a lot of extra functionality around experiment tracking and pipelining of your code. You can safely ignore all that and just use DVC for data versioning. No shame in that :)" %}

## 🛠 When to use DVC

It probably is a good practice to use something like DVC from the start of most projects. If you know you're never going to need to update the data you use, or if you will only ever generate one model, then maybe you have no need for data versioning. But realistically, when are you going to do that? Generally speaking you'll be iterating a lot and you'll be trying things out, so perhaps just start using DVC at the start of any new project: a `git init` can just as easily be followed by a `dvc init`…

DVC will thrive in long-lived projects where you go down certain rabbit-holes, trying out different approaches and techniques. If you have a decent amount of data — and you probably do if you're bringing deep learning to the table — then you can leverage how DVC makes it easy to store your data in the remote infrastructure of your choice with [`dvc remote`](https://dvc.org/doc/command-reference/remote).

## 📄 How I'm using DVC in my redaction project

For my purposes, the things I'm tracking with DVC include:

- the models I train
- the PDF documents I downloaded from public sources that form the basis of the data in this project
- the images that I extracted from the PDF documents
- the annotations I make on the images using [the standard COCO Dataset format](https://cocodataset.org/).

This covers the core data that I expect to be working with for this project. I keep all this data synced to a remote Amazon S3 bucket which allows me to easily get set up on a new remote machine if needed.

I'll next be writing about how to move towards a 'production-ready' system in the coming weeks, but one thing I'll hope to be adding to the current way I do things is to add some kind of ['data cards'](https://github.com/PAIR-code/datacardsplaybook). I think a combination of manual comments and annotations alongside some auto-generated data profiles would be a useful thing to get a sense of for every checkpoint we make, particularly as the data grows and is augmented.

Let me know if you're using DVC to version your data for computer vision projects! I'm curious if there are any tricks I'm missing out…

## 🏃 Appendix: How to switch from `git-lfs` to DVC

When I first started this project, [`git-lfs`](https://git-lfs.github.com) or Git Large File Storage seemed the best option that didn't constrain my choices. It allowed me to store any large files I had inside my repository and allowed for some sort of versioning. Over time this ended up being less robust, especially in the context of an ML workflow, so I decided to switch to using DVC backed by an Amazon S3 bucket.

I didn't find any useful information on the DVC website or forums on how to make this switch so I'm including my notes on how I switched over myself.

{% include alert.html text="Lots of caution is advised when doing this for your own project or work. I hit some major roadblocks along the way while doing this owing to some quirks of how I'd set 'git-lfs' up in the beginning. Please take all necessary backups and snapshots of your data in case something goes wrong along the way!" %}

Some resources I consulted to understand how to do this:

- [This Stackoverflow thread](https://stackoverflow.com/questions/35011366/move-git-lfs-tracked-files-under-regular-git/54119191#54119191)
- [A Github issue](https://github.com/git-lfs/git-lfs/issues/3026) on the same topic
- [A super useful Gist](https://gist.github.com/everttrollip/198ed9a09bba45d2663ccac99e662201) I reached via the previous Github issue that ended up guiding me most of the way

This is what I did, step by step:

- Commit and push everything to Git / Github / `git-lfs`
- Create a branch, something like `fix/remove-lfs`
- Remove the hooks using `git las uninstall`
- Go into the `.gitattributes` file and delete whatever tracking you don't want `git-lfs` to handle from now on. For me, this involved removing lines referring to `.pth` (model) files and `.jpg` (image) files.
- Get a list of all the files that `git-lfs` currently is storing using the following command: `git lfs ls-files > files.txt`
- Modify the file to remove the beginnings of each line that we don't need. At the end we want our `files.txt` to contain just a series of paths to our files. I did it with a simple Python script:

```python
with open("filenames.txt", "w") as f:
    f.write("")

with open("files.txt", "r") as f2:
    for line in f2:
        with open("filenames.txt", "a") as f:
            f.write(line.split(" ")[-1])
```

- Run `run git rm --cached` for each file that `git-lfs` is storing. I did this with a simple bash command that uses the file I'd created in the previous step:

```shell
while read line; do git rm --cached "$line"; done < files.txt
```

- Initialise the DVC repository with `dvc init`
- Add whatever data sources you want tracked (`dvc add FOLDERNAME`)
- Allow for autostaging with DVC with the `dvc config core.autostage true` command
- Commit everything
- Check that no `git-lfs` files are left with the `git lfs ls-files` command. Whatever you uncached in previous steps should not show up any more.
- Remove any lfs with `rm -rf .git/lfs`
- Merge your branch into `main`
	- (if you're using `git-lfs` as a team, now is probably the time when other collaborators can uninstall git-lfs as specified above)
- If needed, add your DVC remote storage with `dvc remote add …` ([consult the docs](https://dvc.org/doc/command-reference/remote) for exactly how to set this up for your specific needs)
- `dvc push` to get your files synced with your remote storage

At this point you should be fully transitioned over. As I mentioned above, there are a ton of weird edge cases and quirks to this process and you probably shouldn't follow this list blindly. I'm mainly writing this up for my own records as much as anything else, so perhaps it's helpful for someone else seeking to transition but maybe it should be taken less as a direct list of instructions than an inspiration or general template. (I wish DVC would provide some official-ish guidance on this process through their documentation. I imagine that it's a fairly common path for someone to outgrow `git-lfs` and want to get going with DVC but currently there are no instructions for how to think this through.)

UPDATE: *I originally made reference to 'continuous training' in the title of this blogpost but I didn't actually get into this specific use case in what I covered, so I took that out of the title and we'll save the specifics for a subsequent post!*
