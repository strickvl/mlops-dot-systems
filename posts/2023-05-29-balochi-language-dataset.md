---
author: Alex Strick van Linschoten
categories:
  - balochi
  - nlp
  - balochi-language-model
  - ethics
  - datasets
date: "2023-05-29"
description: "I share my journey of building language models for Balochi, a language with few digital resources. I discuss assembling a dataset of 2.6 million Balochi words."
layout: post
title: "Building a Balochi Language Dataset for NLP Applications"
toc: false
image: images/awesome-balochi-small.png
include-before-body:
  '<script defer data-domain="mlops.systems"
  src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I'm working on building out some language models and utilities for the Balochi language. (Read [previous posts](https://mlops.systems/#category=balochi) in this series for the full context.) Even though there are some 8-10 million estimated speakers, it certainly falls into the category of being a 'low-resource' language. Many (most?) things that you'd take for granted when working with English-language models are either non-existent or bare bones for Balochi.

The experimentation phase of a project like this rewards a fast iteration speed, so I'm looking for ways to keep moving forward. I don't need to spend days running a single experiment to validate my ideas; I'm sufficiently green that small datasets and these frequent tweaks to what I'm doing will hopefully reward me.

I did an initial survey of materials and resources that already exist, collecting a mix of more general language materials alongside some prior work that exists in the NLP space for Balochi. In particular, there are some small datasets on GitHub as well as some more targeted projects for Named Entity Recognition (NER). Since it's my repository, I also threw in some blog posts that inspired me to get started in the first place (from [Lj Miranda](https://ljvmiranda921.github.io) and [Kurian Benoy](https://kurianbenoy.com/blog.html#category=malayalamtextmodels), among others).

![](images/awesome-balochi.png "A screenshot of the `awesome-balochi-nlp` repository I put together.")

[The `awesome-balochi-nlp` repository](https://github.com/strickvl/awesome-balochi-nlp) is my first effort at gathering a list of resources. I'll be keeping it up to date as I continue.

For my work gathering the dataset together, I had my eyes on three potential sources of authentic Balochi texts:

- Sina Ahmadi's [PersoArabicLID project](https://github.com/sinaahmadi/PersoArabicLID) (language classification for a series of low-resource languages that share a common script) includes (labelled) datasets as part of the repository
- [Baask.com](http://baask.com/archive/) — a website that's been posting Balochi content for around a decade and that I had come across in the past
- [Kissah.org](https://kissah.org) — a project by [Junaid Qadir](https://github.com/JunaidQadirB) that collates Balochi stories

The mechanics of gathering the texts from these sources was straightforward (a few scripts using `beautifulsoup` and the `requests` module), but I'll admit that the experience felt a little uncomfortable. The content from these sources may technically be 'fair game' but I'll admit to a certain queasiness about how easy it was to put together my promo-dataset of Balochi language in an evening. (For that reason, I'm probably not going to open up the dataset until I've figured out a way to do that properly; the ideal end-goal is to have datasets like this available publicly on the Huggingface Hub and so on.)

So now I have a dataset containing some 2.6 million words of Balochi text. This
feels like it's enough to do some experiments at least, and we'll see how far I
get with it. The first order of business is to look into tokenisation or the
process of splitting those texts up into pieces that can be used and processed
by the machine learning machinery. Surprise surprise: there aren't any
pre-existing tokenisers for Balochi and while there are language-agnostic
tokenisation processes I want to understand the tradeoffs around the different
algorithms and approaches they take.
