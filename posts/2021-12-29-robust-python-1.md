---
aliases:
- /robustpython/python/books-i-read/2021/12/29/robust-python-1
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2021-12-29'
description: Reflections on the first chapter of Patrick Viafore's recent book, 'Robust
  Python'.
image: robust-python/robust-python-cover.jpeg
layout: post
title: What makes code robust?
toc: false

---

We use a lot of modern Python idioms, libraries and patterns at work, so I've been wanting to get up to speed on that and maybe even actively contribute to this general direction. A recently-published book, [Robust Python: Write Clean and Maintainable Code](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?qid=&me=&tag=soumet-20&_encoding=UTF8) by [Patrick Viafore](https://www.linkedin.com/in/patviafore/), seems like it answers many of the questions I have around this topic. It is quite dense in terms of the amount of new things per chapter, so I'll be working my way through it in the coming months and reflecting on things as I encounter them.

The first chapter is mainly about setting the scene for all the technical pieces that follow. Patrick asks the core questions: what is robust code and why do we even care? What problems does it solve to think about code in this way.

What I took away was that a robust codebase emphasises good communication as well as avoiding accidental complexity. A lot has been written about 'clean code' and how to achieve this, but it seems that 'Robust Python' is arguing for looking a bit further into the future, when you have to come back to refactor your code three months after you wrote it, or when your colleague needs to do the same.

> "Writing robust code means deliberately thinking about the future." (p. 3)

You write robust code, in other words, because you know that the codebase is going to be changing and shifting and that whatever you write today may need to be modified at a later date:

> "A robust codebase is resilient and error-free in spite of constant change." (p. 4)

We're trying to solve for the way that code is often hard to reason about or understand when you're outside the original moment when it was written. Accordingly, it pays dividends to take a bit of extra time upfront to write code such that it *does* communicate intent well, and that you haven't made things more complicated than they need to be. 

Moreover, the communication of intent needs to be done in a way that is asynchronous. The book goes into a bit more detail about why communication practices that require minimal cost and minimal proximity are to be preferred. These include: the code itself, in-code comments, tests, version control history, wikis, and in-project documentation.

The first part of the book is all about type annotation, using `mypy`, and how working with types helps makes your code more robust. We use a lot of this at work so I'm excited to take a deep dive into this.
