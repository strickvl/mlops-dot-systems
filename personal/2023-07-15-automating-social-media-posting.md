---
author: Alex Strick van Linschoten
categories:
  - productivity
  - tech
  - useful-tools
  - automation
  - social-media
  - technology
date: "2023-07-15"
description: "How I set up automation to post my blog updates to social media using Zapier, Buffer, and ChatGPT."
layout: post
title: "Automating social media posting for my new blogposts"
toc: true
aliases:
  - "/blog/automating-social-media-posting.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I love blogging and I've benefitted a lot from what it's done for me ever since I started my first Geocities page in the mid 1990s. I maintain a technical blog at mlops.systems and a somewhat less technical blog at alexstrick.com/blog, though hope at some point to merge these together.

In the past I would have been content with ensuring that my blog published an RSS feed and known that anyone wanting to follow what I was writing could do so simply by connecting their feed reader and subscribing. I've become more conscious in recent years of a healthy brew of ambivalence, ignorance or even outright hostility to even the idea of RSS feeds and readers. It seems many people don't have RSS as an essential part of their informational hygiene any more. (I'll put my sadness / confusion about this to one side for now.)

And if I love blogging, I really dislike having to post my new blog posts to social media one by one, coming up with some catchy yet not overtly breathless summary of what I wrote, since this is apparently what many people use instead of RSS.

I've been grumbling under my breath about this situation for this for a few years now, but when ChatGPT came out it seemed like an obvious use: summarise my blogpost and repost to all my social media accounts taking into account their particular needs. (Mastodon uses hashtags more than the others, whereas LinkedIn posts can be a bit longer, vs Twitter which needs to be a bit shorter and so on.)

I held off, thinking I'd want to set up some system fully under my control involving serverless function calls and so on, but then I was reminded that I already use [Zapier](https://zapier.com/) for some other administrative tasks. So this afternoon I set up and turned on some automation for social media posting to my Mastodon, Twitter and LinkedIn accounts. Posting happens at one step removed since I queue my posts in [Buffer](https://buffer.com) so that they go out at a time when people are more likely to see them. I apologise / don't apologise for this. My blog writings remain wholly un-automated; it would completely remove the point of 'learning through writing' if I were to automate the things that I blog about. My social media postings (just one post per blogpost so as not to spam you all) are from now on automated. As an additional courtesy / discourtesy, I've tweaked the prompt such that the social media posts should always read just slightly 'off' and will be labelled with an `#automated` hashtag.
