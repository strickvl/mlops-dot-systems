---
author: Alex Strick van Linschoten
categories:
  - coding
  - python
  - lists
  - numpy
date: "2018-01-23"
description: "Quick reference for useful Numpy functions I discovered for creating and shuffling lists in Python."
layout: post
title: "Making and shuffling lists in Python"
toc: true
aliases:
  - "/blog/lists-shuffling-numpy.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I discovered some useful functions the other day while trying to solve one of the [Dataquest](https://www.dataquest.io) guided projects. These all relate somehow to lists and use [Numpy](http://www.numpy.org/). I'm listing them here mainly as a note for my future-self.

```
import numpy as np

# this code returns a list of n number of items starting at 0
np.arange(3)
---- returns [0,1,2]

# this code is a variation on the previous one
np.arange(3,7)
---- returns [3,4,5,6]

# this adds the functionality of steps in between values
np.arange(2,9,2)
---- returns [2,4,6,8]

# these are slightly different; they sort lists
# if you want to make list of numbers randomly sorted:

np.random.permutation(10)
---- returns the numbers 1-9 in a list, randomly sorted

# you can also pass non-numeric lists into the `permutation`
list = [a,b,c]
np.random.permutation(list)
---- returns something like [b,a,c]
```
