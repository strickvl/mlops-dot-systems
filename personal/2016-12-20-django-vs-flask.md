---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - plateau-ebook
  - thinking
date: "2016-12-20"
description: "Weighing Django vs Flask for building a language tool—comparing their tradeoffs in learning curve, built-in features, and speed to prototype."
layout: post
title: "Django vs Flask"
toc: true
aliases:
  - "/blog/django-vs-flask.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2016-12-20-django-vs-flask/f1549db0fbef_image-asset.avif)

I am diving back into the coding of my language-related web tool, [as I mentioned](https://www.alexstrick.com/blog/seeking-python-code-mentor) a few days back. In and of itself, the functionality is quite simple, but there are three parts that have to all work together, so it’s harder for me to put it all together than I had expected.

One of the decisions I’m currently mulling over is whether to use [Django](https://www.djangoproject.com/) or [Flask](http://flask.pocoo.org/) to allow my Python code to interact and get displayed on the website. For those of you who aren’t familiar with coding and how websites work, these two frameworks are what allows me to write the bulk of the tool in Python, but then use either Django or Flask to display it on the web and interact with the web server. (I realise I probably butchered that explanation.)

Django seems to be what most people recommend I use, in part because it comes with a number of useful things built-in. As a result, or maybe independently of that, it has a steeper learning curve and feels like a larger proposition than perhaps I need for my (somewhat small) project.

Flask is pretty basic and pared down. It doesn’t contain all the bells and whistles that Django offers, but as a result it’s easier to get your head round and make a working prototype sooner.

If I had a bit more time, I think I’d go with Django. The user community seems bigger and I’d probably end up using the built-in features, but Flask allows me to get a working prototype hosted somewhere much faster and thus seems like probably the option I’ll choose.

For now, I’m getting a bare-bones Python-only version of the tool ready, then I’ll hook that up to Flask and see how that interaction works.
