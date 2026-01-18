---
author: Alex Strick van Linschoten
categories:
  - coding
  - launchschool
  - javascript
date: "2020-10-12"
description: "Working through JavaScript's prototype-based object model and exploring OLOO patterns for encapsulation and private data."
layout: post
title: "Working with JavaScript's Object Prototype model"
toc: true
aliases:
  - "/blog/working-with-javascripts-object-prototype-model.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Today I worked on some more exercises relating to implementing object-oriented design patterns in JavaScript.

I'm taking the position that a lot of my difficulty in absorbing the materials is because JavaScript itself wasn't designed with this in mind. Any implementations that look or seem intuitive are probably going to be hacky, or hide complexity under some syntactical sugar.

The exercises revealed some models for how to work with OLOO code (see [this](https://medium.com/launch-school/javascript-design-patterns-building-a-mental-model-68c2d4356538) for an example), particularly when you want to conceal some kind of 'private' data along with your encapsulation of methods. For this latter implementation, [an IIFE](https://developer.mozilla.org/en-US/docs/Glossary/IIFE) seems to do the trick, though it also feels a bit of a hack.

Tomorrow I will try to complete the rest of my exercises for the module and then get some more practice of these paradigms / models in examples of my own creation.
