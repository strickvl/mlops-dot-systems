---
author: Alex Strick van Linschoten
categories:
  - coding
  - javascript
  - web
  - technology
  - launchschool
date: "2020-11-12"
description: "How I learned to use CSS selectors with JavaScript DOM methods like querySelector and querySelectorAll."
layout: post
title: "Using CSS selectors with JavaScript DOM methods"
toc: true
aliases:
  - "/blog/using-css-selectors-with-javascript-dom-methods.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I've been using JavaScript methods that interact with the DOM all week as part of my [Launch School](https://launchschool.com/) course. Among them, `document.querySelector()` and `document.querySelectorAll()` seem really useful. I realised I didn't fully understand the selectors that you were supposed to pass in as an argument, so I'm writing up some of what I discovered about them here. (See [here](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector) for the documentation).

The simple part is when you have a single selector. Three important selectors are:

- id selectors (`#`) — so if the html contains an id attribute of 'some-id', then you could write `#some-id`.
- class selectors (`.`) — so if the class was 'special-style', then you can write `.special-style`.
- tag selectors — for these, you just write the page itself

When combining tags, there is a complex set of options depending on whether things are siblings or descendants or children. For the most part that is TMI. The important ones to remember are:

- descendant selector combinations — place a space between elements — so if you want to select all `<div>` tags that descend (however far down in the tree) from a `<p>` tag, then you can write `p div`.
- child selector — place a `>` between the elements — this allows you to find elements that are direct children (i.e. no intermediary levels) of other elements. `p > div` will find all div elements that are the direct children of paragraph elements.

(For a more complete exploration of this topic, specifically the combination of selectors, read [this blogpost](http://galjot.si/combining-css-selectors).)
