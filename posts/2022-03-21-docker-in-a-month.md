---
aliases:
- /books-i-read/dockerinamonthoflunches/tools/2022/03/21/docker-in-a-month
author: Alex Strick van Linschoten
categories:
- tools
- dockerinamonthoflunches
- books-i-read
date: '2022-03-21'
description: I'm reading Elton Stoneman's 'Learn Docker in a Month of Lunches' and
  blogging as I learn along the way. In chapters 1-3 we learn about the context for
  Docker as well as some basic commands for running and building containers.
image: images/diamol/diamol-cover.jpg
layout: post
title: Starting Docker In A Month Of Lunches
toc: true

---

As far as software engineers go, I'm still barely a spring chicken, six months into my job with [ZenML](https://zenml.io/). Working at a startup is fairly fast-paced and the ability to get going quickly with any number of libraries and tools is a requirement of the work. The number of things I could study, learn or practice is vastly larger than the amount of time I have. Accordingly, it helps to try to pick things that will be long-lasting, teach a cross-cutting skill or that are somehow fundamental.

Two closely-connected technologies that I've realised I can no longer avoid are [Docker](https://www.docker.com/) and [Kubernetes](https://kubernetes.io/). I have some high-level knowledge of both, having worked with Docker images on Ekko and having encountered Kubernetes in recent months, but it's become clear in the last few weeks that they aren't going away. More than that, it seems that not having a better (practical) grasp of some of the ins and outs of both is holding me back from grasping more complex decisions that are being made at work.

[*Side-note: I'm very curious about [Podman](https://podman.io/) as a Docker-adjacent alternative, but I need to understand Docker better first before I can make comparisons. I'd also note that I'm pretty sure that there are lots of cases where Kubernetes is overkill, and where it doesn't make much sense to add all that complexity, particularly for smaller teams and projects. It's nevertheless a feature of life in the MLOps space, it seems, so I must understand it.*]

I've had my eye on two Manning books by [Elton Stoneman](https://blog.sixeyed.com/) for a while, and now seems the perfect time to dive in. [Learn Docker in a Month of Lunches](https://www.amazon.com/Learn-Docker-Month-Lunches-Stoneman-ebook/dp/B097824MVJ/ref=tmm_kin_swatch_0?qid=&sr=&tag=soumet-20&_encoding=UTF8) and [Learn Kubernetes in a Month of Lunches](https://www.amazon.com/gp/product/B0978175TP/ref=dbs_a_def_rwt_bibl_vppi_i1?tag=soumet-20) are very practical introductions to their subjects, come with good reviews and feedback and were published relatively recently. I'm especially happy that both books are extremely hands-on and even though I won't in any way be an expert in either technology by the end, I'll at least have some experience of having encountered the core use cases of both and maybe have a strong idea of what I do and don't know.

I'm not sure whether I'll complete each one in exactly a month, but I'll try to fast-track my reading. The chapters are written in such a way as to be digestible (including exercises) in around an hour. Stoneman says in the introduction to the Kubernetes book that it's best to start with the Docker one, which I suppose makes sense given that one builds on the other.

Just like [my posts as I read through Robust Python](https://mlops.systems/categories/#robustpython) (which I haven't stopped doing), I'll write up various things that I learn along the way, mainly as notes for myself but perhaps it will have value beyond this limited goal. So far I've read through the first three chapters of the Docker book, so what follows are some notes on the key points from that.

# Core Docker Commands

The book has you running a lot of examples. Two commands mentioned (specific to this book) to help clean up the images and containers that you were using:

```shell
# clean up containers and application packages
docker container rm -f $(docker container ls -aq)

# to reclaim disk space
docker image rm -f $(docker image ls -f reference='dial/*' -q)
```

Some core commands for interacting with a container:

```shell
# run a container
docker container run CONTAINERNAME

# run an interactive container with a connected terminal session
docker container run --interactive --tty CONTAINERNAME

# list running containers
docker container ls
# list all containers with any status
docker container ls --all 

# list processes running in a container
# CONTAINERNAME could be part of the container ID as well
docker container top CONTAINERNAME

# show logs for a container
docker container logs CONTAINERNAME

# view all details about a container
docker container inspect CONTAINERNAME

# get stats on a particular container
docker container stats CONTAINERNAME

# special flags
# --detach starts the container in the background
# --publish publishes a port from the container to the computer

# delete containers
# the force flag shuts it down if still running
docker container rm --force CONTAINERNAME

# the nuclear option
docker container rm --force $(docker container ls --all --quiet)
```

# Building your own images with Dockerfiles

Some commands which are useful for making your own images:

```shell
# gets the image from DockerHub registry
docker image pull IMAGENAME
```

Key mental models for Docker images:

- images are made up of 'layers'
- Docker images are stored as lots of small files, brought together as one image when you build with a `Dockerfile`.
- each layer of an image corresponds to a line in your `Dockerfile`
- layers are successively built on top of each other
- the order of the layers determines the cache invalidation. If something changes in a lower layer, then all subsequent layers are regenerated. It's for this reason that it pays to be careful about the order in which you write the commands that make up your `Dockerfile`.

It seems to be considered a good practice (at least where I am right now in the book) to pass in environment variables from the outside into your Docker image. This way you can keep configuration separate from how you actually run it. So you'd have a command something like this:

```shell
docker container run --env EPOCHS=30 SOMEUSER/CONTAINERNAME
```

which would pass the `EPOCHS` environment variable into the runtime of the Docker image if it had been set up with something like this as a line inside the `Dockerfile`:

```
ENV EPOCHS="1"
```

Note that only the environment variables that you specifically select to be passed into the container get passed in.

## Dockerfile layout

`Dockerfile`s seem to have some commonalities in terms of the structure:

- you start with a base image on which you're building. These seem usually or often to be a base image containing a runtime for whatever language your application uses
- Then there's often environment variables afterwards
- Then you can specify a `WORKDIR` which is the working directory for the application
- Then you can `COPY` files from your local filesystem into that working directory
- Then at the end you specify which `CMD` needs to be run in order to execute the application.

Once you're done with writing your `Dockerfile`, use the following command to build your image:

```shell
docker image build --tag SOMENAME .
```

Note that final `.` trailing that command. The `.` states that the current directory is the 'context' and thus is used for when you're copying in files using the `COPY` command.

You can view the layers of your Docker image with the `docker image history IMAGENAME` command (which will output them to the terminal).

To see how much disk space your containers and images are taking up, type `docker system df`.

When you rebuild an image, you can specify this with a `:v2` after the name, as in this command:

```shell
docker image build -t web-app:v2 .
```

When it comes to optimising your `Dockerfile`, bear the following in mind:

> "Any Dockerfile you write should be optimised so that the instructions are ordered by how frequently they change — with instructions that are unlikely to change at the start of the Dockerfile, and instructions most likely to change at the end. The goal is for most builds to only need to execute the last instruction, using the cache for everything else. That saves time, disk space, and network bandwidth when you start sharing your images." (pp. 42-43)

Some command tips and tricks:

- combine multiple commands onto the same line
- put the `CMD` instruction early on as it's unlikely to change