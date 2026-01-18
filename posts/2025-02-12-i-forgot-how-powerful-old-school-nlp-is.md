---
author: Alex Strick van Linschoten
categories:
  - datalabelling
  - finetuning
  - miniproject
  - nlp
date: "2025-02-12"
description: ""
layout: post
title: "I forgot how powerful old-school NLP is"
toc: true
image: images/2025-02-12-i-forgot-how-powerful-old-school-nlp-is/someimage.png
draft: 'true'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/posts/2025-02-12-i-forgot-how-powerful-old-school-nlp-is.html"
---

[This is a long one. Sorry / not sorry. *TL;DR*: I automated the process of curating articles to be included in the a popular database I maintain by using Spacy to create a classifier that's only 2 MB in size!]

A few weeks back I created and launched [a big database](https://www.zenml.io/llmops-database) that curated implementations of GenAI use cases and LLMOps out in the wild. I'd been keeping a list of these interesting blogs for a while and it occurred to me that it might be useful for others to share the full list.

![](images/2025-02-12-i-forgot-how-powerful-old-school-nlp-is/someimage.png)

Each entry in the database has some metadata and tags attached to it (to help with search / discoverability) as well as a comprehensive summary of the key points of the link's contents. (Links were most often blogs, but sometimes YouTube videos where the task was then to grab the transcript and summarise that.)

## The Problem: it takes time to curate the database

The database has grown quite a bit since we launched and now is approaching 600 entries (!). At ZenML, we'll continue to maintain and update it but the process of finding new entries is non-trivial:

- **Finding good use cases**: where possible we try to meet some kind of technical depth standard where we're not just republishing some marketing press release. The gold standard is the engineering team of some company writing a deep dive into what they learned from implementing feature X or Y, ideally with code samples and/or architecture diagrams.
- **Staying fresh**: things change fast in the world of LLMOps, so we want to stay more or less up to date with whatever people are building *now* and not just the fresh trends of a year ago.
- **Not just the big names**: there are well-known and (rightfully) acclaimed engineering blogs from mega-companies but there are also smaller groups doing interesting work that is at least as worthy of inclusion in the database.

We have [a 'submit your case study' link](https://docs.google.com/forms/d/e/1FAIpQLSfrRC0_k3LrrHRBCjtxULmER1-RJgtt1lveyezMY98Li_5lWw/viewform) at the top of the database but to be honest so far it's been a flytrap for spammers rather than a go-to destination for the people writing their technical accounts. All of of the above means that, till now, my process for updating the database looks something like this:

- In general, I keep an eye out on social media (mostly Twitter, but occasionally LinkedIn and/or Bluesky) for new posts or videos that get shared. This is low-effort but also low-frequency.
- I have RSS subscriptions (yay [Newsblur](https://newsblur.com/)!) to some blogs and YouTube channels that consistently have good content and I group them together so I can process that queue every few days.
- As mentioned above, we have a link to submit technical write-ups which I check whenever someone makes a new submission.
- Search with exa.ai: this is the most high-value thing I do to populate the list. (Exa.ai is an embeddings-based search engine that excels at finding 'other articles like this one' and I'd guess that 70% of the blogs (i.e. non-YouTube links) in the database were found with it.)

For all of this, usually 'processing' means clicking through the URL, giving the article a quick skim read. For videos, it means a mix of skipping through the contents directly in video form or passing it off to an LLM using [my custom YouTube summarisation tool](https://gist.github.com/strickvl/ac2a6a6e6f642ed6be375bd1943bd65f). I have a 'I know it when I see it' set of criteria that determines whether an article is worthy of inclusion in the database. That mostly boils down to:

1. Does the article actually match up with the subjects we're trying to cover? i.e. GenAI uses *in production* and not just some experiment that someone tried locally or some pushing of some benchmark score forward by 0.2% etc. The focus is on production use cases, so how these things work as a system and how people are ensuring reliability and what are they learning along the way.
2. Does the article have some depth to it? There is a *lot* written about AI use cases these days and (aside from the content that's auto-generated purely for SEO) not all of it actually contains useful insights or implementation details. I'm not saying we need to see your code, but we're really looking for something more than just 'we made this amazing system and it uses these 3 tools'.

I haven't properly written down my acceptance criteria yet because so far it was only me working on the project and it's also a pretty hard one to summarise as a text spec. It seems like there's many edge cases, and when I'm checking the links I often have to stop, think and weigh the value of what I'm consuming.

Long story short: it takes up quite a bit of time to sift through the internet in the hope that someone's written a new technical blog describing how they built something or what lessons they learned along the way. So far it's been a pretty manual process taking a non-zero amount of time. (Not hours and hours, but perhaps 20 minutes every two or three days. 'It's not nothing' would be how I'd quantify it!)

## 💡 Let's train a model to pick the articles

I read [Daniel van Strien's article](https://danielvanstrien.xyz/posts/2025/deepseek/distil-deepseek-modernbert.html) on distilling DeepSeek down into a ModernBERT classifier with interest and I wondered whether I could also use a model to help process the incoming articles. This seems like an obvious next step in retrospect, but I think I also needed the months of drip-drip work on curating the articles till this point for me to have arrived at a solid collection of validated examples.

On the other hand, I hadn't been 
