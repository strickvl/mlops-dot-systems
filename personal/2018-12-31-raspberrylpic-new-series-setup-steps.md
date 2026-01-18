---
author: Alex Strick van Linschoten
categories:
  - raspberrylpic
  - tech
  - coding
  - raspberrypi
  - lpic
  - linux
  - technology
date: "2018-12-31"
description: "Starting a new series working through the LPIC-1 exam using a Raspberry Pi as my learning environment, and the setup steps I took to get it running."
layout: post
title: "RaspberryLPIC: A New Series &amp; Setup Steps"
toc: true
aliases:
  - "/blog/raspberrylpic-new-series-setup-steps.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2018-12-31-raspberrylpic-new-series-setup-steps/43c9501bc8f1_92690.avif)

I mentioned in my [last post](https://www.alexstrick.com/blog/linux-essentials-certification) that I hoped to move on to the LPIC-1 exam in the coming weeks. I’m going through a bit of flux in terms of my stable laptop setup at the moment and I wanted a bit of stability as I work my way through the course. The idea suggested itself to me: what if I work through the syllabus using a Raspberry Pi?

I have a few Raspberry Pi 3 and Zeros lying around the house, so I’ve chosen the latest model I have — a [model B version 1.2](https://en.wikipedia.org/wiki/Raspberry_Pi#Generations_of_released_models). I can SSH into the device over wifi regardless of whatever laptop I’m using at the time.

I’m choosing to use a Raspberry Pi for a few reasons:

- I want something that feels (and is) ‘disposable’ — if I make some mistake in my settings, I can install everything from scratch fairly trivially
- I didn’t want to do it on a virtual machine because sometimes this can behave idiosyncratically and I wanted something as close to an ‘authentic’ Linux experience as possible.
- I didn’t want to use a server from a cloud hosting provider since a dedicated server running online is probably overkill for what I need. You can get cheaper if you’re just using part of a server (via some virtualised service etc) but that seemed likely to provide non-standard output.
- I wanted to plug and play bits of hardware as part of my studies. That’s obviously not possible on a cloud server, and can provide non-standard responses when done through a virtual machine.
- I didn’t just want to install Linux on a spare laptop since I don’t have one of those lying around where I currently am. If I break anything, moreover, the installation / reformatting process and so on takes much longer than just flashing a SD card for a Raspberry Pi.

The hardware is pretty decent on the model I’m using, at least for the purposes of the LPIC-1 exam. This seems like an ideal use case.

Once again, I’m following through using the [Linux Academy’s video lectures](https://linuxacademy.com/linux/training/course/name/lpic1-exam-101-new). As far as I understand things, the LPIC-1 exam requires more than just passing familiarity with a few commands. For that reason, I’m using a few supplementary books. Once I’ve gone through both books and videos I’ll be testing myself with practice exams.

Yesterday I spent a few hours trying to get my base setup installed on the Raspberry Pi. I started with an ambitious plan to install [the version of Arch](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3) developed for use on a Raspberry Pi 3 (i.e. this version of an ARM chip) but it ended up being somewhat non-trivial. I ended up breaking Pacman (the Arch package installer) and unable to install any new software or update the system.

I realised that Arch probably wasn’t the ideal setup for this experiment in any case. The default Raspbian distro, based on Debian Wheezy, seemed a better option. Flashing that onto my SD card and getting a headless copy up and running was easy.

I might take a short detour before diving into the LPIC course proper by working my way through the [Linux From Scratch](http://www.linuxfromscratch.org/) series. I figure I’ll learn some useful things in that process of building my own custom kernel / distribution that I can then build on through the LPIC-1 syllabus. But I haven’t fully decided on that path yet.
