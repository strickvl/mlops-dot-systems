---
author: Alex Strick van Linschoten
categories:
  - tech
  - coding
  - languages
  - technology
  - pythonsideproject
date: "2016-11-05"
description: "How I'm structuring my Python side-project: building the core functionality as a standalone program first, then adding a web interface later."
layout: post
title: "Python Side-Project: Approach"
toc: true
aliases:
  - "/blog/python-side-project-approach.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2016-11-05-python-side-project-approach/d340fc318e99_image-asset.avif)

Since finishing the [Udacity IPND](https://www.alexstrick.com/blog/udacity-ipnd) I have been drawing up plans to start practical work on a specific side-project. I won’t go into too many of the details for now — it’ll be more fun to release it as a surprise — but I wanted to take a note of some of my evolving thinking on my approach.

I had wanted a project that combines the various skills I’d learned on the Udacity course. Thus: HTML, CSS, Python, SQL & databases. My idea is a website that will have a python/database back-end. I want to code it all from scratch. Much of my thinking about how to break it down into smaller chunks so far was focused on coming up with some sort of basic prototype that showcased the interactions between these various structures.

I’ve recently realised, however, that it makes a lot more sense to just code the entire project in Python as a standalone programme and to think about linking this functionality into a website once the Python prototype is done.

This simplifies my life a lot. Instead of looking around for frameworks or wrappers (I don’t even know if these are the right words to describe what I’m looking for) like [Django](https://www.djangoproject.com/) and [Flask](http://flask.pocoo.org/), I can focus on the core functionality of the service / programme.

Once that’s complete, I’ll figure out how to hook it up to a front-facing web interface, and then will work on the presentation as per my specifications.

I’m quite excited about this project. As a final clue I will add that it’s going to be a service that helps people learning languages.
