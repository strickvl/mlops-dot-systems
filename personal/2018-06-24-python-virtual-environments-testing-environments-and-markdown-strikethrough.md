---
author: Alex Strick van Linschoten
categories:
  - coding
  - python
date: "2018-06-24"
description: "Setting up my Python project with virtual environments, testing considerations, and project structure decisions."
layout: post
title: "Python Virtual Environments, Testing Environments and Markdown Strikethrough"
toc: true
aliases:
  - "/blog/python-virtual-environments-testing-environments-and-markdown-strikethrough.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I spent part of this afternoon fixing things in my PDF splitter code.

- I learnt about virtual environments and the various choices available in Python. [This](http://docs.python-guide.org/en/latest/dev/virtualenvs/) was the most useful overview. I ended up choosing `pipenv` which is also outlined [here](https://realpython.com/pipenv-guide/). It installs a `Pipfile` in your directory which is an equivalent to the old `requirements.txt` that was previously used. This means that whenever you use `pip` to install a new package, it’ll remember and update the file accordingly.
- For testing, I ended up holding off for the moment. It wasn’t immediately apparent which of the various testing suites I should be using and the examples given in places like [this](https://realpython.com/python-cli-testing/) used strange syntax. I’ll have to tackle this later, but for now I’m putting it on hold.
- I learnt that you can make some text strikethrough (~~EXAMPLE~~) in Markdown by enclosing the text in two tildes (`~~`).
- I [read about application layouts / structures](https://realpython.com/python-application-layouts/) and made some initial decisions about what files to include in my project. Some of this is overkill for where I am currently, but soon enough this project will expand and I’ll need a standard structure format.

Tomorrow I want to start working on my regex search-and-rename function. I’ll start by figuring out the right regex string to use for my search, then I’ll figure out how to add in `re.search` into my script.
