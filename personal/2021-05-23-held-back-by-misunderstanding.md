---
author: Alex Strick van Linschoten
categories:
  - tech
  - deep-learning
  - academia
  - technology
  - deeplearning
date: "2021-05-23"
description: "How theoretical misunderstandings about neural networks held back the field of deep learning for decades."
layout: post
title: "Held back by misunderstanding"
toc: true
aliases:
  - "/blog/held-back-by-misunderstanding.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

The field of deep learning seems to have had a rough journey into public consciousness and adoption. In particular, two theoretical misunderstandings lead to funding being pulled and energy and attention moving away from the field:

1. Minsky/Papert's book [Perceptrons](https://www.amazon.com/Perceptrons-Introduction-Computational-Geometry-Expanded/dp/0262631113/ref=sr_1_1?dchild=1&qid=1621785922&keywords=minsky%252Bperceptron&tag=soumet-20&sr=8-1) showed how a neural network using only one layer was unable to learn some critical functions like `XOR`. Later in the same book, they show how using more layers addresses this problem completely, but for some reason the 'fix' to the problem was ignored and people fixated on the problem with using a single layer and its drawbacks.
2. By the 1980s, many people were using two layers in their neural networks, and while this did solve the problems identified in 'Perceptrons' and people were using neural networks to solve real problems, it was unwieldy in that form. Yes, you could theoretically approximate any mathematical function with two layers, but it was impractical and slow to do so. People thought that this meant that the principle was broken, whereas really the misunderstanding was that two layers were just not enough and that the number of layers could continue to increase.

These are two key misunderstandings identified by the Howard/Gugger [short introduction](https://www.amazon.com/Deep-Learning-Coders-fastai-PyTorch/dp/1492045527/ref=sr_1_1?tag=soumet-20&sr=8-1&keywords=deep%25252Blearning%25252Bfor%25252Bcoders&dchild=1&qid=1621784082) and I'm sure I'll read more of these in [Genius Makers](https://www.amazon.com/Genius-Makers-Mavericks-Brought-Facebook-ebook/dp/B08CD1M43L/ref=sr_1_1?dchild=1&qid=1621785566&keywords=genius%252Bmakers&tag=soumet-20&sr=8-1). It's amazing, but not entirely surprising, that a non-generous and unimaginative misreading of the literature could be responsible for such an effective trashing of a research path.
