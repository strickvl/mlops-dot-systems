---
aliases:
- /calmcode/debugging/testing/tools/2021/11/25/entr-reruns-tests
author: Alex Strick van Linschoten
categories:
- debugging
- testing
- tools
- calmcode
date: '2021-11-25'
description: entr is a useful tool to rerun things when watched files change. It's
  especially useful when testing.
layout: post
title: 'entr: a tool to run commands when files change'
toc: false

---

It's a fairly common pattern that you have some code that you're repeatedly running. Perhaps you're fixing a failing test, and you just have to keep running it every time you make a fix.

Enter [`entr`](http://eradman.com/entrproject/). This handy little tool reruns a particular command whenever changes are detected in a particular set of files.

Let's take the example I mentioned above: you have a failing test that you're debugging and you need to have it run every time you save a change to the file. Assuming your source code is stored in `src` and you're using `pytest`, then you could use something like the following:

```bash
ls src/*.py | entr -c pytest test.py::test_some_feature
```

So now, any time you change any Python file inside the `src` folder, it'll rerun your test. The `-c` flag will clear the terminal every time the test runs.

[Many thanks to [calmcode](https://calmcode.io/) for continuing to make these really useful videos.]