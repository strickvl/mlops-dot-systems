---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - python
  - tools
  - food
date: "2016-12-29"
description: "I built a Python tool to solve my dinner party dilemma using weighted decision-making—and learned some valuable lessons about lists, dictionaries, and testing along the way."
layout: post
title: "Dinner Party Decision Matrix: A Python Tool"
toc: true
aliases:
  - "/blog/dinner-party-decision-matrix.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2016-12-29-dinner-party-decision-matrix/8212b6190e37_image-asset.avif)

Some friends were coming round for dinner this evening and I couldn’t decide what to cook. I couldn’t decide because there were too many variables floating around that would impact the decision.

So I decided to make an app.

I wanted something tasty but that also was relatively hassle-free. I wanted something that didn’t take too much time to prepare, but it still needed to be different from the kind of food I’d cook in a rush at the end of a long day.

I’d come across the idea of [weighted decision-making](http://www.ginaabudi.com/weighted-decision-making/) a while back, and really like its premise; you say how important various factors are to you and then rate all the different options according to those same factors. At the end, you’re left with a score that can be said to be more objective than just your gut feeling.

So yesterday morning I listed a bunch of the factors that were important to me in coming to a decision about what to cook. I figured I could get some coding practice by making a tool that would work to calculate the best option from any combination of choices.

I put the finishing touches on the decision-making tool this morning. You can check it out on [Github](https://github.com/strickvl/dinnerpartydecision), though you’ll need to know a little about how Python works to get it going for yourself. I’m fairly sure my code looks horrific to a seasoned professional. There are probably ways I could have standardised the flow of questions and improved the output, but for now, I’m satisfied.

The app ended up picking the following for dinner (photo below):

- Courgette, chickpea and feta filo pastry pie

- Roast beetroot and pistachio salad

- Kale, pomegranate and shredded chicken salad

- and a beetroot and chocolate cake

![](images/2016-12-29-dinner-party-decision-matrix/fc35d4f49cbd_dinner.avif)

I learnt a bunch of things about Python while coding the tool:

1. When you run a x= raw\_input(“Ask question here”) command, the information allocated to x will be in a string format. If you are collecting numbers, you’ll need to convert it to an integer format by using int().
2. Lists and dictionaries can be tricky, particularly when you’re looping over them or looping over certain keys etc.
3. It helps to test while you code. This particular function wasn’t too complex to understand, so I just pushed on without testing so much. At some point towards the end, I realised something in the middle was wrong: cue much debugging. I keep reading about the importance of having in-built tests. I’m not sure what that would mean / have meant in the context of this particular app, but I imagine I’ll find out in due course.
4. Coding is fun and appeals to the compulsive side of my brain. I rarely need to be urged back to the task at hand when I’m coding. This probably has something to do with the quick feedback loop that coding enables. In any case, I’m hooked (again).
