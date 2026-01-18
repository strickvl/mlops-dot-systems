---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - web
  - launchschool
  - javascript
date: "2020-12-10"
description: "A quick guide to including jQuery and Handlebars libraries in your HTML with script tags."
layout: post
title: "How to use jQuery and Handlebars in your website"
toc: true
aliases:
  - "/blog/how-to-use-jquery-and-handlebars-in-your-website.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

jQuery and Handlebars are both external to the core functionality of JavaScript. Both are libraries that we can use and include when making websites. Doing so is very simple. We include `<script>`s in the `head` of our HTML file, as in the following example:

```
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/handlebars@latest/dist/handlebars.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  </head>
  <body>
    <h1>Hello, World</h1>
  </body>
</html>
```

Note that jQuery is now modular, so you may want to consider whether you want to include the entire library. Above I chose to download it from Google's CDN, but there are other options listed [here](https://jquery.com/download/).
