---
author: Alex Strick van Linschoten
categories:
  - deep-learning
  - software
  - technology
  - deeplearning
date: "2021-05-26"
description: "How neural networks learn to classify images differently than traditional programming, illustrated with a cat vs. dog classification example."
layout: post
title: "Telling Cats from Dogs"
toc: true
aliases:
  - "/blog/telling-cats-from-dogs.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

One of the main ways that using neural networks to train models is different from traditional (imperative) programming can be illustrated with a specific task: let's say you want to use a computer to tell you whether any particular photo you give it is a cat or a dog.

An imperative approach might be to make a mega list of certain kinds of features that cats and dogs have, and try to encode the differences into some kind of list of logical features. But even knowing how to tell the computer how it should recognise those features is a potentially massive project. How would you even go about that?

Instead, with neural network layers, we turn that pattern on its side. Instead of this:

![](images/2021-05-26-telling-cats-from-dogs/2e5999af6274_ScreenShot_2021-05-26_at_09.28.57.avif)

We have something closer to this:

![](images/2021-05-26-telling-cats-from-dogs/ea0a106d3a1e_ScreenShot_2021-05-26_at_09.29.07.avif)

So the neural networks are learning on the basis of data provided to it — you give it a bunch of images which you've pre-labelled to say 'this one is a cat and that one is a dog' and so on.

If you use transfer learning, too, you even can use a pretrained model (which is already pretty good at recognising features from images). You can then fine-tune that model to get really good at the specific task you need it to do. (Note, that's exactly what you do in the first chapter of Howard/Gugger's [Deep Learning for Coders](https://www.amazon.com/Deep-Learning-Coders-fastai-PyTorch/dp/1492045527/ref=sr_1_1?dchild=1&qid=1621784082&keywords=deep%2525252Blearning%2525252Bfor%2525252Bcoders&tag=soumet-20&sr=8-1)).
