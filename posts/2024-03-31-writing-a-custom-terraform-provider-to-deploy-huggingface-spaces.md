---
author: Alex Strick van Linschoten
categories:
  - devops
  - miniproject
  - terraform
  - go
  - skillbuilding
date: "2024-03-31"
description: "I worked on this short project to allow people to create/deploy Huggingface Spaces using Terraform (instead of via the API or using the website)"
layout: post
title: "Writing a custom Terraform provider to deploy Huggingface Spaces"
toc: true
image: images/tf-registry-docs.png
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

If you're reading this blog, you've probably visited [the Huggingface website](https://huggingface.co/) and you've almost certainly tried out one of [their 'Spaces'](https://huggingface.co/spaces). These are deployed mini-applications hosted on Huggingface infrastructure. I've created spaces of my own, and at work [I added](https://github.com/zenml-io/zenml/pull/1427) a way for people to quickly deploy a ZenML server as a 'Space'. I love browsing all the spaces that exist and they're really a testament to the creativity, smartness and elbow-grease contributed by the thriving open-source community that Huggingface facilitates through their platform.

I've been working on my Terraform skills [for a while](https://mlops.systems/#category=terraform) and recently I thought up a little project that I hope will help deepen my skill-building as well as be useful for others. My goals were to build something that would:

- allow people to deploy HF Spaces (using pre-build templates) using Terraform
- allow for all the templates and not just `zenml`
- facilitate the full range of CRUD functionality for spaces, including renaming and deleting the spaces
- make the provider a 'good' one that follows best practices as much as possible

This blogpost will describe my process and some of the things I learned along the way. A special thanks to Sean Kane at SuperOrbital for writing [an extremely useful blogpost](https://superorbital.io/blog/custom-terraform-providers/) that guided me on this journey (alongside [the official Hashicorp documentation](https://developer.hashicorp.com/terraform/tutorials/providers-plugin-framework/providers-plugin-framework-provider)). (TL;DR: [check out the finished provider here](https://registry.terraform.io/providers/strickvl/huggingface-spaces/latest/docs)!)

## The Terraform Golden Path

What I wanted to be able to do was define my resource in something like the following manner:

```hcl
terraform {
  required_providers {
    huggingface-spaces = {
      source = "strickvl/huggingface-spaces"
    }
  }
}

provider "huggingface-spaces" {
  apikey = var.huggingface_apikey
}

resource "huggingface-spaces_space" "zenml_server" {
	name     = "test-zenml-space"
	private  = false
	template = zenml/zenml
}
```

This really simple interface would allow people to spin up Huggingface spaces without needing to click through buttons on the Huggingface website. You can get a sense of how it works if you were to do it via that web interface here:

![Web interface to deploy Huggingface Spaces as of November 2023](images/hf_tf_provider/hf_web_interface.png)

## Using HTTP Request(s) to Deploy Spaces

Internally, this web interface will just be using API calls (through some layer of abstraction) to make the deployment, so we can take a look at the Huggingface documentation and experiment a bit to find out how we can make such deployments using the raw underlying HTTP.

It's important to have a sense of the HTTP API because this is what we're going to ultimately be using when we write the Terraform provider. For the provider, we'll have to use [Go](https://go.dev) to define how that works so in the interests of clarity I'll just show the HTTP requests on their own first.

There's [a useful Space](https://huggingface.co/spaces/enzostvs/hub-api-playground) by [Enzo](https://huggingface.co/enzostvs) that allows you to play around with the Hub API, and the [Huggingface docs](https://huggingface.co/docs/hub/api) cover the endpoints available for the Hub API.

For our purposes, we're interested in the `POST /api/repos/create` endpoint. Note that we're not making our query to the `api/spaces` endpoint, but rather to the `repos` endpoint. When you create a space, what you're actually doing is creating a repository with certain custom features that Huggingface then knows to instantiate and deploy as a 'Space'.

So as a simple HTTP request we can run the following in the terminal:

```bash
http POST "https://huggingface.co/api/repos/create" \
  Authorization:"Bearer YOUR_TOKEN_GOES_HERE" \
  type=space \
  name=test-hf-api \
  private=false sdk=docker template=zenml/zenml
```

You'll need to add in your authorisation token that you create on the Huggingface site and you can change the specific template you're creating and the name as you see fit. Running this command will do the same as clicking through the various buttons on the web interface. (I'm using [the `httpie` CLI tool](https://httpie.io/) to make the request, but you could just as well use something like `curl` if you prefer.)

Once we've confirmed that the basic creation of a Space based on the template works, we can try some other commands. If we wanted to rename the space, we can 'move' it. (Think how renaming folders in the UNIX terminal is also accomplished with the `mv` command.)

```bash
http POST "https://huggingface.co/api/repos/move" \
  Authorization:"Bearer YOUR_TOKEN_GOES_HERE" \
  fromRepo="strickvl/test-hf-api" toRepo="strickvl/my-renamed-space" type="space"
```

And then to delete the space we can do the following:

```bash
http DELETE "https://huggingface.co/api/repos/delete" \
  Authorization:"Bearer YOUR_TOKEN_GOES_HERE" \
  type=space \
  name=my-renamed-space \
  type=space
```

So the API allows us to interact with the Space without using the website as expected. So far so good!

## Terraform Provider Basics

At the end I want this provider to be available on the Terraform Registry for others to use, so in that case the repository needs to be named in the format `terraform-provider-THE_NAME_GOES_HERE`. I've chosen [`terraform-provider-huggingface-spaces`](https://github.com/strickvl/terraform-provider-huggingface-spaces).

Terraform [released a framework](https://github.com/hashicorp/terraform-plugin-framework) for creating these Terraform providers which is a new (v2) way of doing this. It's worth noting that it's fairly new and many (most?) of the community providers you see on the Terraform registry are using the old way. There's lots of support and even [a repository you can use as a template](https://github.com/hashicorp/terraform-provider-scaffolding-framework) scaffold for your own efforts. That's what we'll be using as well.

## Implementing the Provider

It's all implemented in Go, and while the template / framework got me started, there was a fair amount of boilerplate code to be written. Between Claude, GPT-4 (when Claude cut me off for making too many queries) and a bit of elbow grease, I got it all implemented and working. You can view the finished provider up [on the Terraform Registry here](https://registry.terraform.io/providers/strickvl/huggingface-spaces/).

![](images/tf-registry.png "A screenshot of the Terraform Registry page for the Hugging Face Spaces provider v0.0.2.")

![](images/tf-registry-docs.png "A screenshot of the Terraform Registry documentation for the Hugging Face Spaces provider v0.0.2.")

## Using the provider

So now you can use code like this:

```hcl
terraform {
  required_providers {
    huggingface-spaces = {
      source = "strickvl/huggingface-spaces"
    }
  }
}

provider "huggingface-spaces" {
  token = var.huggingface_token
}

variable "huggingface_token" {
  type        = string
  description = "The Hugging Face API token."
  sensitive   = true
}

resource "huggingface-spaces_space" "test_space" {
  name     = "test-hf-api-${formatdate("YYYYMMDD", timestamp())}"
  private  = true
  sdk      = "docker"
  template = "zenml/zenml"
}

data "huggingface-spaces_space" "test_space_data" {
  id = huggingface-spaces_space.test_space.id
}

output "test_space_id" {
  value = huggingface-spaces_space.test_space.id
}

output "test_space_name" {
  value = data.huggingface-spaces_space.test_space_data.name
}

output "test_space_author" {
  value = data.huggingface-spaces_space.test_space_data.author
}

output "test_space_last_modified" {
  value = data.huggingface-spaces_space.test_space_data.last_modified
}

output "test_space_likes" {
  value = data.huggingface-spaces_space.test_space_data.likes
}

output "test_space_private" {
  value = data.huggingface-spaces_space.test_space_data.private
}

output "test_space_sdk" {
  value = data.huggingface-spaces_space.test_space_data.sdk
}
```

And this will create a Hugging Face Space using the ZenML Docker template. You can even specific specific hardware that you want your space to be provisioned with, or state that you want persistent storage to be added, or add secrets and/or environment variables as part of the deployment. I would encourage you to visit and [read the documentation](https://registry.terraform.io/providers/strickvl/huggingface-spaces/latest/docs) for the provider for more information.

Unfortunately at some point towards the end of my development I seem to have triggered the Hugging Face API's rate limiter and now I'm in some purgatory where I can't do anything on the Hugging Face Hub for the next 23+ hours. Not sure what that means for my ability to test this functionality in our CI, but I'll be exploring this next.

## What this unlocks

I'm pretty excited that I finally got this working. This unlocks a few things for me.

Firstly, I'm one of the lead engineers responsible for maintaining [`mlstacks`](https://mlstacks.zenml.io/), a Python package and library that allows you to quickly spin up MLOps infrastructure. We started off with Kubernetes-based implementations of all of the possible infrastructure combinations you might need, but it's clear that for many use cases that's too heavy a footprint. With this provider, we can easily add in the ability to spin up an [Argilla annotation instance](https://huggingface.co/docs/hub/spaces-sdks-docker-argilla), for example, or any of the many other options.

![](images/docker-spaces.png "A screenshot of the GUI for setting up and deploying Docker spaces on Hugging Face.")

Hugging Face technically allow you to create any kind of repository, so potentially this opens up a way to deploy any kind of Docker-backed image to the Hugging Face Hub. Given how simply and easy these are to deploy and configure, I'm personally excited by this idea and how it makes various parts of MLOps more approachable and accessible to others.

I also think that this provider might be used by others. Technically you could use [the Python SDK for the `huggingface_hub`](https://github.com/huggingface/huggingface_hub), or perhaps raw HTTP requests using `curl`, but I find this interface useful and more maintainable. (I have a bit more work to do on the provider to add more robust testing and CI in that regard.) The newly-established [`mlinfra`](https://github.com/mlinfra-io/mlinfra) tool might also find this provider useful as part of its parallel attempt to allow for the deployment of MLOps infrastructure.

## What I learned

I've recently been reminded quite frequently that projects that seem daunting are often just a case of keeping moving forward, putting one step in front of another. I first thought of the idea for this provider a year ago, yet it only took me a weekend to implement the functionality that I've now released.

I found it quite hard to understand the precise endpoints of the Hugging Face API that were available. Some documentation can be found, but it's split [over](https://huggingface.co/docs/hub/api#hub-api-endpoints) [various](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/hf_api.py) [places](https://huggingface.co/spaces/enzostvs/hub-api-playground) and still is incomplete. The actual source code for the Hub's API is closed-source so it's not even possible just to go to the code implementation. Once I'm done with the testing for the provider I'll maybe see if I can go back and make a PR to improve the Hugging Face documentation.

Working with Go code is pretty pleasant. There were some new parts of Go I hadn't previously encountered, notably modules. Using the new Terraform provider plugin template / system means you have to use modules, but it wasn't too hard to figure out. Go is certainly easier to grok as a non-expert user than Rust.

A final 'as always' lesson was that my work was really helped by taking some time away from code to think through exactly how the provider would work, what pieces of information would be needed where and so on. I don't always remember this lesson — it's really easy to just start typing on a keyboard — but I appreciated having a game plan and some notes to keep me on track when I had choices to make.

So [give the provider a try](https://registry.terraform.io/providers/strickvl/huggingface-spaces/latest/docs) and let me know if you found it useful! (Also let me know if you'd like some other functionality adding and I'll see what I can do!)