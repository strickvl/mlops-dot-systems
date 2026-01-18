---
author: Alex Strick van Linschoten
categories:
  - tech
  - useful-tools
  - deep-learning
  - technology
  - deeplearning
date: "2021-05-23"
description: "Why GPUs are the small, powerful boxes powering everything from your screen to deep learning models—and why they've been impossible to find."
layout: post
title: "Small, unexpectedly powerful boxes"
toc: true
aliases:
  - "/blog/small-unexpectedly-powerful-boxes.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Graphics Processing Units or GPUs are what your computer uses to quickly display your screen. Most computers (desktop or laptop) have one of these, and they are used to good effect to keep the screen refreshed and display everything in effectively realtime speed. The world of gaming is also, perhaps unsurprisingly, quite dependent on fast GPU performance, with Nvidia as the lead provider of these hardware units.

![nvidia gpu](https://icdn.digitaltrends.com/image/digitaltrends/geforce-rtx-3080-product-gallery-full-screen-3840-3-1-720x720.jpg)

It was discovered a while back that GPUs are also pretty great at performing certain kinds of computation at incredible speed. Certain calculations which, if you would do them on a standard CPU, would take ages to complete are much faster when run on a GPU. For this reason, they're the hardware of choice for training deep learning models.

GPUs also happen to be heavily used (for similar reasons) for cryptocurrency mining and accordingly there has been a worldwide shortage for some time. Between the crypto bros and the deep learning practitioners, the price got inflated for a while. Nvidia has made [some attempts](https://www.digitaltrends.com/computing/nvidia-lite-hash-rate-ampere-cards-crypto-limiter/) to limit crypto miners from using their hardware, but to inconclusive effect.
