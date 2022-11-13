---
aliases:
- /python/skillbuilding/2021/09/18/reading-python.html
author: Alex Strick van Linschoten
categories:
- python
- skillbuilding
date: '2021-09-18'
description: Some of the code libraries I plan on reading to improve my Pythonic style
image: python-code.jpeg
layout: post
title: Reading Python Code
toc: true

---

It's a truism of sorts that in order to improve your skills, you have to practice them. For coding, the stereotypical image is of someone typing, actually creating new things. But as often as not, you're going to be *reading* code instead. This code might be something you write yesterday or last year, or it might be something that someone else wrote.

One way or another, reading code is a great way to get increasing familiarity with stylistic, syntactic patterns and to get exposed to some best practices, especially if you get to pick the code you're reading.

I'll be doing the same as I ramp up my Python proficiency. I wanted to gather some lists of codebases and assorted resources in one place for myself, and I hope maybe it'll be useful for someone else as well.

## Good Quality Python Code

- [`jinja`](https://jinja.palletsprojects.com/en/3.0.x/) — a templating engine written in Python (and see the recommendations for supplemental reading and watching for `jinja` [here](https://death.andgravity.com/aosa))
- [`howdoi`](https://github.com/gleitz/howdoi) — a search tool for coding answers via the command line
- [`flask`](https://github.com/pallets/flask) — a micro-web framework for Python
- [`FastAPI`](https://fastapi.tiangolo.com) — another web framework that's a bit larger than flask
- [`diamond`](https://github.com/python-diamond/Diamond) — a Python daemon that collects and publishes system metrics
- [`werkzeug`](https://github.com/pallets/werkzeug) — a web server gateway library
- [`requests`](https://docs.python-requests.org/en/latest/) — an HTTP library, now part of the Python standard library
- [`tablib`](https://tablib.readthedocs.io/en/stable/) — library for Pythonic way to work with tabular datasets
- [`click`](https://click.palletsprojects.com/en/8.0.x/) — a Python package for creating command line interfaces
- [`pathlib`](https://docs.python.org/3/library/pathlib.html) — part of the Python standard library; a module to handle filesystem paths (also the corresponding [PEP proposal #428](https://www.python.org/dev/peps/pep-0428/))
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) — a module in the Python standard library; reduces boilerplate of writing classes (also the corresponding [PEP proposal #557](https://www.python.org/dev/peps/pep-0557/))
- [`joblib`](https://joblib.readthedocs.io/en/latest/) — a library to support lightweight pipelining in Python

## Other Resources

- [500 Lines or Less](http://aosabook.org/en/index.html) — a book in which specific small open-source projects are profiled to understand how they approached their particular challenge.
- [The Architecture of Open Source Applications: Elegance, Evolution and a Few Fearless Hacks](http://aosabook.org/en/index.html) — examination of the structure of the software of some open-source software applications.
- [The Architecture of Open Source Applications: Volume II: Structure, Scale and a Few More Fearless Hacks](http://aosabook.org/en/index.html) — the second volume in the series.
