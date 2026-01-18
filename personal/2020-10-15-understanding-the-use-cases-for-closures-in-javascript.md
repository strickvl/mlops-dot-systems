---
author: Alex Strick van Linschoten
categories:
  - coding
  - launchschool
  - javascript
date: "2020-10-15"
description: "How I came to understand why closures are actually useful in JavaScript."
layout: post
title: "Understanding the use cases for Closures in JavaScript"
toc: true
aliases:
  - "/blog/understanding-the-use-cases-for-closures-in-javascript.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I spent today revising some of my [Launch School](https://launchschool.com/) JS225 topics. Among those was the idea of closures, or in other words how functions can capture and package away any variables or 'state' in scope at the point *of function definition*.

I hadn't fully realised just how useful that can be. Other languages have other ways of realising the same functionality. In JavaScript, it turns out this is a really useful feature because it effectively allows you to keep some variables, functions and whatever else available to our objects or functions, but we can control access to them. They are accessible via whatever interfaces we provide, but to an outsider trying to access those elements via our API or function calls, they are effectively private.

There are a bunch of ways that this is useful in things that I don't yet understand and haven't studied yet (async or promises seem high up that list) but closures play a role in those as well.

I write all of this mainly because it's useful from time to time to step out of the weeds and remind oneself *why* any or all of this is actually useful.
