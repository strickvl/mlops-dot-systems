---
aliases:
- /fastai/jupyter/python/tools/2022/01/06/nbdev-early-impressions
author: Alex Strick van Linschoten
categories:
- python
- jupyter
- fastai
- tools
date: '2022-01-06'
description: Some early thoughts on the benefits and possible drawbacks of using fastai's
  'nbdev' literate programming tool which is a suite of tools that allows you to Python
  software packages from Jupyter notebooks.
image: images/nbdev-early-impressions/laura-ockel-UQ2Fw_9oApU-unsplash.jpg
layout: post
title: Learning about 'nbdev' while building a Python package for PDF machine learning
  datasets
toc: false

---

While working to
[develop a computer vision model](https://mlops.systems/categories/#redactionmodel)
that detects redactions in documents obtained as a result of
[FOIA requests](<https://en.wikipedia.org/wiki/Freedom_of_Information_Act_(United_States)>),
I have encountered some tasks that I end up repeating over and over again. Most
of the raw data in the problem domain exists in the form of PDFs. These PDF
files contain scanned images of various government documents. I use these images
as the training data for my model.

The things I have to do as part of the data acquisition and transformation
process include the following:

- downloading all the PDF files linked to from a particular website, or series
  of web pages
- converting and splitting all the downloaded PDF files into appropriately sized
  individual image files suitable for use in a computer vision model
- generating statistics on the data being downloaded and processed, as well as
  (further down the line) things like detecting data drift for incoming training
  data
- splitting up data as appropriate for train / validation / test data sets
- extracting text data from the images via an OCR process
- versioning, syncing and uploading those images to an S3 bucket or some other
  cloud equivalent for use in the overall workflow

It's not hard to see that many of these things likely apply to multiple machine
learning data acquisition scenarios. While writing the code to handle these
elements in my specific use case, I realised it might be worth gathering this
functionality together in an agnostic tool that can handle some of these
scenarios.

I had wanted to try out `nbdev` ever since
[it was announced](https://www.fast.ai/2019/12/02/nbdev/) back in 2019. The
concept was different to what I was used, but there were lots of benefits to be
had. I chose this small project to give it an initial trial run. I didn't
implement all of the above features. The two notable missing parts are text
extraction and data versioning and/or synchronisation.

[`pdfsplitter`](https://github.com/strickvl/pdfsplitter/tree/main/) is the
package I created to scratch that itch. It's still very much a work in progress,
but I think I did enough with `nbdev` to have an initial opinion.

I think I had postponed trying it out because I was worried about a steep
learning curve. It turned out that an hour or two was all it took before I was
basically up and running, with an understanding of all the relevant pieces that
you generally use during the development lifecycle.

Built in to `nbdev` in general is the ability to iterate quickly and driven by
short, small experiments. This is powered by Jupyter notebooks, which are sort
of the core of everything that `nbdev` is about. If you don't like notebooks,
you won't like `nbdev`. It's a few years since it first saw the light of day as
a tool, and as such it felt like a polished way of working, and most of the
pieces of a typical development workflow were well accounted for. In fact, a lot
of the advantages come from convenience helpers of various kinds. Automatic
parallelised testing, easy submission to
[Anaconda](https://anaconda.org/anaconda/repo) and [PyPi](https://pypi.org)
package repositories, automatic building of documentation and standardising
locations for making configuration changes. All these parts were great.

Perhaps the most sneakily pleasant part of using `nbdev` was how it encouraged
best practices. There's no concept of keeping test and documentation code in
separate silos away from the source notebooks. Following the best traditions of
[literate programming](http://literateprogramming.com), `nbdev` encourages you
to do that as you develop. Write a bit of code here, write some narrative
explanation and documentation there, and write some tests over there to confirm
that it's working in the way you expected. When Jeremy speaks of the significant
boost in productivity, I believe that a lot of it comes from the fact that so
much is happening in one place.

While working on `pdfsplitter`, I had the feeling that I could just focus on the
problem at hand, building something to help speed up the process of importing
and generating images from PDF data for machine learning projects.

Not everything was peaches and roses, however. I ran into a weird mismatch with
the documentation pages generated and my GitHub fork of `nbdev` since I was
using `main` as the default branch but `nbdev` still uses `master`. I will be
submitting an issue to their repository, and it was an easy fix, but it was
confusing to struggle with that early on in my process. I'm also not sure how
well `nbdev` will gel with large teams of developers, especially when they're
working on the same notebooks / modules. I know
[`reviewnb`](https://www.reviewnb.com) exists now and even is used within
`fastai` for code reviews, but I would imagine an uphill battle trying to
persuade a team to take a chance with that.

I've been using VSCode at work, supercharged with GitHub Copilot and various
other goodies, so it honestly felt like a bit of a step back to be forced to
develop inside the Jupyter notebook interface, absent all of my tools. I also
found the pre-made CLI functions a little fiddly to use — fiddly in the sense
that I wish I'd set up some aliases for them early on as you end up calling them
all the time. In fact, any time I made a change I would find myself making all
these calls to build the library and then the documentation, not forgetting to
run the tests and so on. That part felt a bit like busy work and I wish some of
those steps could be combined together. Maybe I'm using it wrong.

All in all, I enjoyed this first few hours of contact with `nbdev` and I will
continue to use it while developing
[`pdfsplitter`](https://github.com/strickvl/pdfsplitter/). The experience was
also useful to reflect back into my current development workflow and
environment, especially when it comes to keeping that close relationship between
the code, documentation and tests.

[Photo by <a
href="https://unsplash.com/@viazavier?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Laura
Ockel</a> on <a
href="https://unsplash.com/s/photos/cogs?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>]
