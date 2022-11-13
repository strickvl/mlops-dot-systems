---
aliases:
- /debugging/2021/10/25/debugging
author: Alex Strick van Linschoten
categories:
- debugging
date: '2021-10-25'
description: A few lessons I've learned about debugging at work in recent weeks
layout: post
title: Some things I learned about debugging
toc: true

---

I've had to deal with a whole bunch of bugs in the past few days and weeks. I thought it'd be useful to put down some thoughts about things that I've learned along the way.

## Logging & Printing

These are maybe the first things that everyone says you should do when you have a bug you need to fix: log things somewhere where you can see them.

There are some scenarios where simple `print` calls aren't enough. If you're running code through a series of tests, then the test harness will often consume all output to `stdout` so you won't see any of your print statements. Luckily, test environments can usually be configured to print debug statements of loggers.

Once you can see what's happening at a particular moment, you can see if what you expected to happen at that moment is actually happening.

## Breakpoint your way to infinity!

The `breakpoint()` function comes built-in with Python. It's a convenience wrapper around some [`pdb`](https://docs.python.org/3/library/pdb.html) magic, and practically speaking it means you can set a point where you can interrupt the Python execution. Your terminal will halt at that point, and you can inspect the variables or objects available at that particular moment.

I wish I had known about this earlier on. It's extremely useful for understanding exactly how a function or piece of code is being executed.

## Come with hypotheses

If you don't have a sense of what you expect to happen, it's going to be hard to determine if what you're doing is having any effect or not.

I've been lucky to do some pairing sessions with people as they work through bugs and problems, and I've had this 'come with a hypothesis' behaviour modelled really well for me.

It's not a panacea; there's still a lot of work to be done around this, but it's sort of the foundation, particularly for non-trivial bugs.

## Leave your assumptions at the door

Don't assume what's written is what's actually working. This applies to the code you're working on, the documentation, docstrings, everything. This is especially true when your codebase is rapidly changing growing, such as at a startup or a smaller company where not everything has been cemented into place.

The rapid pace of change means that things can get out of date, or people can make mistakes. This applies to packages or modules you're importing as well. Of course, it's probably more likely that you're misunderstanding something vs the Python standard library has got something wrong, but for many other open-source projects, you should at least be open to the possibility that weird things might show up.

## Follow the thread wherever it leads

This is something about updating your assumptions as you move through the process of testing your assumptions. If you rule out certain pathways, then you should be prepared to go down the remaining ones as far as you need.

## Be systematic

I've found a few times now, that there are certain moments where I notice I'm far _far_ down the road. I'll have kept making a bunch of decisions at the various crossroads that I passed. At a certain moment, though, I need to take stock and just note down all the decisions and assumptions I've made in order to reach this point.

I'll write a short note to myself (mainly), but also for teammates, where I explain all the different assumptions and pathways that I'm travelling down. I'll specifically write down all the conditions that need to be present for this bug to present (as far as I know them).

Quite often, just writing these assumptions down will help me solve the problem outright. Even when it doesn't, it's extremely useful in re-grounding myself and reminding me of why I'm going down rabbit hole x or y.

## Know when to stop

In an ideal world you'd get to follow every windy road and to figure out everything that doesn't make sense. But — and this is again especially true for fast-moving startups — you might not always have time to do that.

This is somehow connected to the Pareto Principle (also known as the 80/20 rule). At a certain point you should make sure to check in with how much time you'd planned on spending on a particular bug. If you're finding that it's taking far longer than expected, and you have other things you're committed to completing, then you should maybe take an opportunity to connect to your team. Alternatively, you can rescope and find a way to disable or flag a particular bug for the next sprint, or see if someone can help you with it.

## Remember: this is the work

Sometimes when I'm fixing bugs I have the feeling that I'm wasting my time somehow, or that I should be doing something more productive. It's often the case, though, that this **is** the work. I'm low on experience, but proxy experience that I've gained through reading books tells me that finding, fixing and triaging bugs is a lot of what we do as software engineers.

## Know when to ask for help

Sometimes there are bugs which turn out to be bigger than you're able to handle. It's certainly worth pushing back against that feeling the first few times you feel it. Early on it's often going to feel like the bug is unsolvable.

But some times there are pieces of context you don't have, which a quick overview of what you've done and tried might alert someone more season to the fact that you're going down the wrong alley. Or it might remind them of something they knew implicitly but had forgotten. The important things is to judge when is the right time to seek outside advice.
