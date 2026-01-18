---
author: Alex Strick van Linschoten
categories:
  - coding
  - javascript
  - internet
  - privacy
  - launchschool
date: "2020-12-03"
description: "How I learned to use events and the DOM to make web pages interactive without full page reloads, and some thoughts on the privacy implications of JavaScript event tracking."
layout: post
title: "How events drive programming for the web"
toc: true
aliases:
  - "/blog/how-events-drive-programming-for-the-web.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

As part of my studies for Launch School, last month I was introduced to the idea of 'events' and how we can use the DOM and JavaScript to cause things to happen without having to force a full reload of the page. This is sometimes known as AJAX requests, which stands for Asynchronous JavaScript And XML.

In this mental model, we can think of the HTML and CSS code loaded by the browser (when you visit a website, for example) as the part which we can interact with. Absent any JavaScript code we include, this is somewhat static.

If we add in some JavaScript, we can first make sure that the DOM is fully loaded. For this we add an event listener for the `DOMContentLoaded` event.

Then after that, the sky is the limit. We can add event listeners to basically anything in our document (or just the whole `document` object itself). [This is the list](https://developer.mozilla.org/en-US/docs/Web/Events) of events that we can watch for.

From reading outside the course, I know that companies' monitoring of user behaviour via JavaScript events triggering is a really big source of privacy violations or issues. I am not sure how the current model of how the web works serves to limit these violations. For instance, do people know that their mouse movements and clicks and patterns of mouse behaviour can all be monitored while they're on a site. So even if you don't click on an object, the website can still track that you're hovering over a particular element. That, to my mind, is a step too far, but it's the world we live in. You can disable JavaScript completely, but then you break a majority of sites that you're visiting.

Of course, if you're browsing in something like [emacs' eww](https://www.emacswiki.org/emacs/eww), or in [brow.sh](https://www.brow.sh/), then you bypass this problem somewhat.

Back to the JavaScript, though, the most interesting thing I found was the sheer amount of events that the browser was built to encounter. I'd love to see a chart showing how and when all these events were added to the browser's capabilities.
