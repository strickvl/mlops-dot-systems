---
author: Alex Strick van Linschoten
categories:
  - science
  - deep-learning
  - statistics
  - machinelearning
  - technology
  - deeplearning
date: "2021-05-26"
description: "How machine learning as we know it today traces back to Arthur Samuel's 1962 essay on automating computers to learn from their experience."
layout: post
title: "Arthur Samuel and the 'Frontier of Automation'"
toc: true
aliases:
  - "/blog/arthur-samuel-and-the-frontier-of-automation.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

The use of neural networks / architectures is a powerful pattern, but it's worth remembering that this pattern is part of the broader category of machine learning. (You can think of 'deep learning' as a rebranding of neural networks or what was once more commonly referred to as connectionism).

In a [classic essay](https://journals.sagepub.com/doi/abs/10.1177/000271626234000103) published in 1962, an IBM researcher called Arthur Samuel proposed a way to have computers 'learn', a different process from how we normally code things up imperatively (see [my previous post](https://www.alexstrick.com/blog/telling-cats-from-dogs) for more on this):

> "Suppose we arrange for some automatic means of testing the effectiveness of any current weight assignment in terms of actual performance and provide a mechanism for altering the weight assignment so as to maximise the performance. We need not go into the details of such a procedure to see that it could be made entirely automatic and to see that a machine so programmed would "learn" from its experience"

Within this essay and this quote specifically, we can find some of the key building blocks of machine learning:

![](images/2021-05-26-arthur-samuel-and-the-frontier-of-automation/a5d2ca1f4554_ScreenShot_2021-05-26_at_10.41.29.avif)

We have our inputs (our data) and our weights. Our weights (or the weight assignments) are variables that allow for different configurations and behaviours of our model. Our results are what the computer has assumed based on the weights and the model, and we have some kind of a metric (our performance) to judge whether this model was accurate or not. The computer then updates the weights based on that performance, tweaking it such that it tries to get better performance.

This is a slightly amended version which language or jargon that are more commonly found today. As you might expect would happen, the language used in the 1960s is in many cases different from what gets used today:

![](images/2021-05-26-arthur-samuel-and-the-frontier-of-automation/67a0c320e0d2_ScreenShot_2021-05-26_at_10.41.37.avif)

The main difference here is that we have some labels which are used to know whether the predictions are correct or not. The loss is a way of measuring the performance of our model that is suited for updating our parameters (that used to be referred to as weights).
