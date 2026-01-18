---
author: Alex Strick van Linschoten
categories:
  - science
  - tech
  - deep-learning
  - data
  - technology
  - deeplearning
date: "2021-05-28"
description: 'Some reflections on the "black box" problem in deep learning and why neural networks can be difficult to interpret.'
layout: post
title: "On the interpretability of models"
toc: true
aliases:
  - "/blog/on-the-interpretability-of-models.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

A [common](https://www.brightworkresearch.com/the-problematic-black-box-nature-of-neural-networks-and-deep-learning/) [criticism](https://www.datanami.com/2017/10/27/dealing-deep-learnings-big-black-box-problem/) of deep learning models is that they are 'black boxes'. You put data in one end as your inputs, the argument goes, and you get some predictions or results out the other end, but you have no idea *why* the model gave your those predictions.

![Ways of interpreting learning in computer vision models - credit https://thedatascientist.com/what-deep-learning-is-and-isnt/](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi0.wp.com%2Fwww.skampakis.com%2Fwp-content%2Fuploads%2F2018%2F03%2FDeep-Neural-Network-What-is-Deep-Learning-Edureka.png&f=1&nofb=1)

This has something to do with how neural networks work: you often have many layers that are busy with the 'learning', and each successive layer may be able to interpret or recognise more features or greater levels of abstraction. In the above image, you can get a sense of how the earlier layers (on the left) are learning basic contour features and then these get abstracted together in more general face features and so on.

Some of this also has to do with the fact that when you train your model, you do so assuming that the model will be used on data that the model hasn't seen. In this (common) use case, it becomes a bit harder to say exactly why a certain prediction was made, though there are a lot of ways we can start to open up the black box.
