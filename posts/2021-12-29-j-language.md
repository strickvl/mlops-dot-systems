---
aliases:
- /j/2021/12/29/j-language.html
author: Alex Strick van Linschoten
categories:
- j
date: '2021-12-29'
description: What I have learned so far about why the J language exists and what problems
  it tries to solve.
image: j-language/jblue.png
layout: post
title: Exploring J, an array programming language
toc: false

---

I've long wanted to explore [the J programming language](https://www.jsoftware.com). I think I probably first heard about it from Jeremy Howard amidst one of the early iterations of the fastai course. He's since spoken about it [in other places](https://youtu.be/J6XcP4JOHmk?t=505).

It is part of the family of programming languages that includes [APL](https://en.wikipedia.org/wiki/APL_(programming_language)), [K](https://en.wikipedia.org/wiki/K_%28programming_language%29) and [Q](https://en.wikipedia.org/wiki/Q_(programming_language_from_Kx_Systems)). These can broadly be categorised as array-programming languages, where arrays are generally the core data structure and mental model to keep in mind. They used to be extremely popular in the 1970s and 1980s, particularly among institutions or businesses with a requirement for performant calculation / computation. One of these, Q, continues to live on (as a closed-source language) [in the world of finance and trading](https://www.efinancialcareers.se/news/2020/10/kdb-finance-jobs). (Q is popular alongside the proprietary database [kdb+](https://en.wikipedia.org/wiki/Kdb%2B)).

You're probably wondering why someone would want to use this fairly specialised and niche language. When you look at examples of J code — like the ones [here](https://code.jsoftware.com/wiki/Studio/IdiosyncraticIntroduction), for example — it's easy to simply dismiss it as an unreadable ('write-only') language. Indeed, many do dismiss it for this reason. Code is often compact, with single letters or symbols doing all the work. Defenders of J hold this up as a feature, not a problem. The compactness of the language means that you can fit the entirety of the solution (space) of a complex problem on a single screen, whereas in many (most?) other languages you would have to be scrolling up and down through dozens or even hundreds of lines of code.

The array languages seem to come at solving problems from a particular perspective. The symbols and letters that transform the arrays in J function as a pattern language. For a simple example, think of what you have to do when you want to find the count of a particular element from within an array/list. The array language paradigm argues that you don't want to waste your time and screen space writing out boilerplate code to carry out this calculation, when it's a common pattern that you can just use from the language itself. When problem-solving, therefore, spend your time thinking about the problem and not messing around with syntax or repeating yourself.

J and its cousins are extremely efficient. It is written in C, and I recently heard someone quote one of the early J pioneers as having said that "it is not theoretically possible to write J code that is more performant than C, but it often ends up being so". For some math- or statistics-heavy domains (think the world of finance), it is extremely helpful to have this highly abstracted language that works performantly on large datasets. Moreover, it seems to be even more helpful when you have a hard problem to work on that isn't fully understood.

Kenneth Iverson's wrote a paper (["Notation as a Tool of Thought"](https://www.jsoftware.com/papers/tot.htm)) that is a classic in computer science and gets into some of the above arguments. (It is written using APL, but [it also applies to J](https://www.hillelwayne.com/post/j-notation/)). I will probably return to that at a future date, because it often comes up and is recommended as a particularly rich document worth taking time to explore in depth.

Very much as a project to indulge my curiosity, I will be exploring J over the coming months. I have been listening to the back catalogue of [The Array Cast](https://www.arraycast.com) podcast, and I will be slowly working my way through [some of the resources](https://code.jsoftware.com/wiki/Main_Page) listed on the official J site. Let me know if you have experience working with J!
