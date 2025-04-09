---
author: Alex Strick van Linschoten
categories:
  - agents
  - google
  - tools
  - openai
  - research
date: "2025-04-09"
description: "Some initial fast impressions of Google Deepmind's new iteration of Gemini Deep Research that uses their 2.5 Pro model."
layout: post
title: "First impressions of the new Gemini Deep Research (with 2.5 Pro)"
toc: false
image: images/cover-gdr.png
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Google released an updated iteration of their Deep Research tool that uses the new 2.5 Pro model. This was taken from a post originally made on Twitter, so please excuse the terseness.

First impressions:

- a bit too eager to jump into a deep research task even when I just ask a clarifying question
- quite verbose, just like the OpenAI version. Not sure why both play this up a lot. It looks impressive but in practice I think we need more entry points into this. The 'Executive Summary' and other concluding headers are nice touches but I feel maybe there should be some more adherence to user requests for short reports. (I get that as UI it's maybe weird to think for 10 mins and then spit out a very concise version, but it might actually be more useful.)
- I continue to be annoyed about how these Gemini DR reports handle footnotes (i.e. as endnotes whacked on at the end of the report). Almost a deal-breaker IMO.
- It's almost like GDR tries to show how scholarly and serious it is by giving you these walls of prose (vs OpenAI DR which throws in a lot more bullet points). Not sure one is better than the other but would appreciate a bit more flexibility!
- The portability of these reports has always been *not great*. Yes you can export them to Google Docs but markdown (+ other options) would have been much better. In practice, this means that whenever I use GDR the report stays stuck there and I'm far less likely to share it with anyone, whereas the OpenAI DR reports I drop parts/all into a Github Gist etc.
- These reports *have* been getting better and better, all things considered. I've been following along and using GDR from the early days (even pre-OpenAI DR) and this latest version is the best version of it so far (as you'd hope!)
- (It's also a little bit annoying that GDR has removed any way to use the older versions of GDR with Gemini Pro 2.0 and 1.5 etc. Makes it harder to actually compare these things.)
- Please let's get an ipad version of the Gemini iPad app soon, too? Feels a bit regressive to have to use GDR on the web interface always.
- For serious research (as opposed to simply generating a nice report on some area where you don't know much about already), all these tools remain hamstrung by the quality of the sources. In areas where I am (or very recently used to be) a leading scholar / researcher, the difference between what I'd expect (in terms of taste / discernment for picking out these sources) is especially egregious. Make the models better, yes, but have better filters + retrieval.

So yeah, these tools are getting good! Kudos to the teams who are implementing this stuff. Hard to make it perform reproducibly well on so many open-ended uses. But more work to be done!

IMO the really great implementations of this 'deep research' pattern will all be in-house where you can have control over:

- source selection (i.e. high-quality inputs only, not just some random things on the internet)
- how long it spends thinking about a particular area / loop of the research (or decides to backtrack and dig deeper etc)
- output types / templates / length
- different modalities of Q&A (sometimes you want reports, other times you want a quick question answered, other times you want visual guides etc etc.)
- different models for different kinds of tasks
- possibly you have little sub-research agents / processes which will go off and work on some hypothesis, possibly involving actual datasets / analysis of tabular data etc, something clearly missing from the current versions we have

A few other things:

- GDR's 'clarification step' (which I've heard them discuss on podcasts etc) is not as good or useful as the OpenAI DR clarification questions. In practice, because it's buried under a concealment button that you have to click etc, and where the entire UI seems to be screaming at you to 'Start Research', you basically never update or amend the research plan. And when you do, it's really not clear what's changed because you don't get some feedback or diff that your comments were understood; you just get an entire new research plan (again buried under the concealment button)
- Going forward we're probably going to want / need ways of navigating the layers to this research. A global overview report will have subsections that (should you wish) can be expanded into their own more detailed or granular reports. This is how research works, after all. Not just endless new reports all trailed one after another pointed in the same direction.

The other thing that I think we're *really* going to need to work on is research taste. Like the LLMs that power them, GDR and OpenAI DR offer a level of research taste developed to the mean. (I know people are thinking about this since it came up on Dwarkesh's podcast with the AI 2027 guys, but they were focused on scientific research.) 

I think there's not a single answer for this which is, again, why I see the end result as people bringing these things in-house where they get to develop and refine what makes their particular flavour of research unique. (In the human-generated research world this is very much the case, where certain institutions (or even particular authors) are known for how deep they go, or what kinds of sources they prefer, or how they choose to feature or highlight the primary sources they access, and so on.) There are many possible variations of how this manifest, and I hope that we're headed into a world where all the AI 'deep researchers' will be unique and quirky in all the best senses of that word.