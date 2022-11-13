---
aliases:
- /jupyter/2021/09/09/auto-reload-external-libraries
author: Alex Strick van Linschoten
categories:
- jupyter
date: '2021-09-09'
description: A small bit of Jupyter notebook magic
layout: post
title: How to set a Jupyter notebook to auto-reload external libraries
toc: false

---

The code to insert somewhere into your Jupyter notebook is pretty simple:

```python
%load_ext autoreload
%autoreload 2
```

When you're working on an external library or piece of Python code outside the contents of your notebook, this snippet will make sure that the updated functions and constants will always be available in their most-recently edited state.