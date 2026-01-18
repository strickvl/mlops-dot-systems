---
author: Alex Strick van Linschoten
categories:
  - coding
  - golang
date: "2018-06-23"
description: "How I figured out structuring real-world Go projects with functions split across multiple files."
layout: post
title: "Real-World Go with Referenced Functions"
toc: true
aliases:
  - "/blog/real-world-go-with-referenced-functions.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2018-06-23-real-world-go-with-referenced-functions/4b6c1af93950_ScreenShot_2018-06-23_at_21.40.26.avif)

Writing small test scenarios and packages in the Go Playground, or in a single `main.go` file is all good and well, but in the real world things are more complex. (Or so I heard).

Today I wanted to get a brief sense of how that all works. I had some sense of how to make this all work when working through [the GreaterCommons course](https://greatercommons.com/learn/5098183625539584), but it proved harder when the training wheels were taken away.

[This](https://github.com/strickvl/golang_practice/tree/master/funcs-in-other-folders) is what I emerged with at the end of my experiments. It is a `main.go` file that references `extended.go`. This ended up being dependent on knowing a bunch of setup quirks and techniques that aren’t particularly well signposted for beginners. I ended up finding a tremendously helpful document on the main Go site entitled “[How to Write Go Code](https://golang.org/doc/code.html)”. They don’t signpost it much, especially when compared to ‘[Effective Go](https://golang.org/doc/effective_go.html)’ or the [general specification](https://golang.org/ref/spec).

I worked my way through the official examples. Luckily they were simple enough that I could follow all of the logic. Everything was incrementally constructed, slowly becoming more complex. I learnt the following:

- it’s best to setup your *workspace* in `$GOPATH/src/github.com/YOURUSERNAMEGOESHERE`
- every time I initialise a GitHub repository on my computer (rather than creating it at GitHub.com and then simply cloning it down to my computer) I have to relearn all the little commands relevant to making that work when pushing up to Github. (It’s sufficiently fiddly and reminiscent of using PGP. Lots of small moving parts and room for error. Big space for improving that user experience…).
- if you use the path listed above as your workspace, you can reference your other folders fairly easily. See my code for examples of that.
- The packages you’re referencing (i.e. not in the central `main.go` file) can be called anything you’d like, as can the file names. If you want to make the functions in those packages globally visible, however, make sure the functions start with a capital letter. (In my example, I have `extended.Extended`).

I am already demonstrating some sloppy habits with my documentation, tests, benchmarks and examples, I realise. For these kinds of toy demonstration examples it is less mission-critical, but there feels like a vague principle at stake.

My next Go exploration project will probably be the final version of an Exercism exercise I’ve been working on for a while.
