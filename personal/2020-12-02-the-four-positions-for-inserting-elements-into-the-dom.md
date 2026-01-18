---
author: Alex Strick van Linschoten
categories:
  - coding
  - launchschool
  - javascript
date: "2020-12-02"
description: "How JavaScript's four position arguments work for inserting elements into the DOM."
layout: post
title: "The Four Positions for Inserting Elements into the DOM"
toc: true
aliases:
  - "/blog/the-four-positions-for-inserting-elements-into-the-dom.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

As part of my [Launch School studies](https://www.alexstrick.com/blog/tag/launchschool#show-archive), I'm revising the ways we can use JavaScript to insert nodes into the DOM. These can be simple text nodes, or they could be elements, but the difficult part I've found is recalling the arguments for `position`. This is an argument you add into your method call which states where the node, for example, should be inserted. It looks something like this in action:

```
let newNode = document.createElement('p');
document.body.insertAdjacentElement('beforebegin', newNode);
```

Where you see `beforebegin` is where you can include one of four different text strings:

- `beforebegin` — before the calling element
- `afterbegin` — immediately inside the element, before its first child
- `beforeend` — inside the element, just after its last child
- `afterend` — after the element itself

The words chosen for these position arguments never felt fully clear to me, so writing it out has been useful to clarify their meaning. This is also a useful code excerpt, [from the MDN docs](https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML):

```
<!-- beforebegin -->
<p>
  <!-- afterbegin -->
  foo
  <!-- beforeend -->
</p>
<!-- afterend -->
```
