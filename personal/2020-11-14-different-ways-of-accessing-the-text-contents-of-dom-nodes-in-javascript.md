---
author: Alex Strick van Linschoten
categories:
  - coding
  - web
  - launchschool
  - javascript
date: "2020-11-14"
description: "I spent some time unpacking the different properties available on DOM nodes for accessing their text contents, and here's what I learned about how `.textContent`, `.data`, `.nodeValue`, `.value`, `.innerText`, and `.innerHTML` each work."
layout: post
title: "Different ways of accessing the text contents of DOM nodes in JavaScript"
toc: true
aliases:
  - "/blog/different-ways-of-accessing-the-text-contents-of-dom-nodes-in-javascript.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

For a while now while studying the DOM and JavaScript's interaction with the web browser, I've been wondering about various properties available on nodes that relate to their contents or text values.

I spent a bit of time the other day unpacking what each of those do. This is a bit of code you can play around with to evaluate how they all work:

```
<!doctype html>
<html lang="en-US">
  <head>
    <title>title</title>
    <meta charset="UTF-8">
  </head>

  <body>
    <div>
      <h1>First bit of text.</h1>
      <p>Some <span>old</span> text</p>
      <textArea>pre-written</textArea>
    </div>
  <script>
    console.log(document.querySelector('div').innerHTML);
  </script>
  </body>
</html>
```

- `.textContent`

This property concatenates the text of the element plus all child elements including any whitespace (from the HTML markup itself).

- `.data`

This is the text content of a text node.

- `.nodeValue`

For text nodes, this is the text content of that text node (i.e the same as `.data`). For comments, it is the comment content. For element nodes (and most other types), it is `null`.

- `.value`

This is either an attribute property on an element (in which case the value is whatever was assigned to that property), or it is the contents of a `textArea` element.

- `.innerText`

This is the rendered text (i.e. as displayed on the browser page) of the node and child nodes. Note, if it is not being rendered, then this will be identical to the `.textContent` property.

- `.innerHTML`

This is all the HTML markup contained within the element (including nested elements and text (and whitespace). Note that sometimes this will just be plain text. Note too, that this can be used to create HTML inside an element as well.
