---
author: Alex Strick van Linschoten
categories:
  - tech
  - deep-learning
  - history
  - technology
  - deeplearning
date: "2021-05-23"
description: "Looking back at the foundational PDP work from 1968 and how its eight core principles anticipate what we now call deep learning."
layout: post
title: "PDP: a precursor to modern neural networks?"
toc: true
aliases:
  - "/blog/pdp-a-precursor-to-modern-neural-networks.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

[Parallel Distributed Processing: Explorations in the Microstructure of Cognition](https://mitpress.mit.edu/books/parallel-distributed-processing-2-vol-set), a multi-volume publication by David Rumelhart, James McClelland and the PDP Research Group, was released in 1968 and is recognised as one of the most important works relating to neural networks.

![PDP (1968](https://mitpress.mit.edu/sites/default/files/styles/large_book_cover/http/mitp-content-server.mit.edu%3A18180/books/covers/cover/%3Fcollid%3Dbooks_covers_0%26isbn%3D9780262631129%26type%3D.jpg?itok=-zzHQP5T)

They lay out eight features necessary to perform what they called 'parallel distributed processing' (which I suppose you can think of as a sort of precursor to modern-day deep learning):

- processing units
- a state of activation
- an output function for each processing unit
- a pattern of connectivity among units
- a propagation rule (for propagating what is learned through the network)
- an activation rule
- a learning rule (where 'patterns of connectivity are modified by experience')
- an environment in which the system operates

I haven't read the book, and I don't fully understand all these different pieces, but it isn't particularly hard to see the pattern of what would later come to be handled by modern-day neural networks in these features. The vocabulary used to describe it is slightly different, but you have the connectivity between neurons, and you have a process through which you update the layers…

This feels like a book that would reward returning to for a proper in-depth read later on in my studies.
