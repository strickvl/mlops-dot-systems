---
author: Alex Strick van Linschoten
categories:
  - nlp
  - balochi-language-model
  - tokenisation
  - links
date: "2023-06-04"
description: "Some links and random observations relating to tokenisation as gathered over the past week."
layout: post
title: "Tokenizer Links"
toc: false
image: images/link-odds-sods.png
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/posts/2023-06-04-token-odds-and-sods.html"
---

This is just a collection of various links and observations that I came across while learning about tokenisation during the past week that would otherwise have no other home.

- [NLTK](https://www.nltk.org) and [CLTK](http://cltk.org) are two other NLP libraries from the pre-deep learning era. CLTK has a focus on classical languages, but my sense of NLTK is that it maybe hasn't kept pace as much and I don't plan to delve too deeply into where it is strong.
- via [the ArabML community](https://github.com/ARBML) there is [tkseem](https://github.com/ARBML/tkseem) which offers tokenization for the Arabic language. Ideas to learn from in there, probably.
- I watched [this video](https://www.youtube.com/watch?v=X7c0T7uwtkM) from the MARI conference (about which more soon), and there was a really good example of the importance of tokenization mentioned (pointing to [this paper](https://aclanthology.org/2021.mrl-1.8/)) for negation in Swahili
- [Some interesting observations](https://blog.yenniejun.com/p/all-languages-are-not-created-tokenized) on how certain languages are disproportionately lossy when it comes to their text-to-token ratio. Feels like a useful area to research more.
- Apparently [GPU tokenization is a thing](https://developer.nvidia.com/blog/run-state-of-the-art-nlp-workloads-at-scale-with-rapids-huggingface-and-dask/), too, though unclear whether this is just NVIDIA making something so that they can sell more GPUs. (i.e. what is the need for this, given how fast it already runs)

## More Questions

And some other questions (beyond my larger questions around how to evaluate tokenisers):

- How useful (or not) is data augmentation when it comes to training a tokenizer?
- Is a list of dictionary words useful for training a tokenizer?
