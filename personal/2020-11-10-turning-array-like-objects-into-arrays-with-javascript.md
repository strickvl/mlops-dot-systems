---
author: Alex Strick van Linschoten
categories:
  - coding
  - launchschool
  - javascript
date: "2020-11-10"
description: "How I figured out how to convert array-like objects into actual arrays using Array.prototype.slice.call()."
layout: post
title: "Turning array-like objects into arrays with JavaScript"
toc: true
aliases:
  - "/blog/turning-array-like-objects-into-arrays-with-javascript.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I've long been wondering how the following piece of code works:

```
// assuming a website with a bunch of elements with 'h1' tags
let liveCollection = document.querySelectorAll('h1');
let arrayVersion = Array.prototype.slice.call(liveCollection); // returns that live collection of elements in the form of an array
```

So I thought I'd write up a little on my understanding of how it works.

`Array.prototype.slice` is simple. The `slice()` function is stored inside the `prototype` object property on the `Array` constructor. That's all as you might expect given how JavaScript handles things with the prototypal chain.

But why are we using `call` here, and how does that work when you pass in `liveCollection` as the object within which you want to invoke `slice()`?

Normally when we have an array that we want to call `slice` on, we have to do that using `slice` as a method. Arrays have the `slice` method available to them through the prototypal chain (also in the `Array.prototype` object). But our array-like object (i.e. the live collection in the example above) don't have those methods available to them.

Under the hood, when the `slice` method is invoked, what it does is iterates over the array as part of its more special functionality (which I'll ignore for now). If we have an array-like object with a length and with elements that you can sequentially iterate over, then we can run something like `slice` on that array-like object.

So how do we bring these two pieces together? We use `call`. `call` is a way of using a function inside a different execution context. In our case, we want to use the execution context (i.e. what `this` is set to) of the live collection, but still have it use the functionality defined in `slice`. `call` and `apply` are both ways we can do this.

(For more on this, there are some very useful explanations in [this stackoverflow post](https://stackoverflow.com/questions/7056925/how-does-array-prototype-slice-call-work).)
