---
aliases:
- /books-i-read/python/robustpython/2022/01/22/robust-python-6
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2022-01-22'
description: Reflections on the sixth and seventh chapters of Patrick Viafore's book,
  'Robust Python'. We slowly wind down our discussion of type hints in Python code
  and think through using `mypy` and how to introduce type hints to a legacy codebase.
image: images/robust-python/robust-python-cover.jpeg
layout: post
title: Using mypy for Python type checking
toc: true

---

The final two chapters of part one of Patrick Viafore's '[Robust Python](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?qid=&me=&tag=soumet-20&_encoding=UTF8)' cover more practical advice on how to actually use and implement type checking in either a new project or a legacy codebase.

[`mypy`](http://www.mypy-lang.org) is the most commonly used option for type checking in Python and it does most of what you probably need it for. You can run it via the command line, inline as part of your IDE, or as part of a CI/CD pipeline. At work we do all three.

You can configure `mypy` to your heart's desire either with inline comments in your code, or via a configuration file. A configuration file is probably the way to go, particularly if you're versioning your code and sharing these kinds of settings across a team.

Chapter 6 goes into detail about some of the specific options or settings you can tweak to make `mypy` more or less sensitive to certain kinds of errors. For example, in [a previous post](https://mlops.systems/robustpython/python/books-i-read/2022/01/08/robust-python-4.html) we mentioned how you can implicitly accept `None` as a type with the `Optional` type annotation wrapper. But maybe you don't want to allow this behaviour because it's generally not a great idea: if so, you can use the `—strict-optional` flag to get notified whenever you're using that particular construction.

`mypy` also allows for the export of its results to html and xml, and you can run it in the background as a daemon which (particularly for large code bases) might speed it up.

We also learn about some alternatives to `mypy`, namely Pyre and Pyright. [Pyre](https://pyre-check.org) runs as a daemon in the background and allows you to run queries relating to type usage in your codebase. It also includes a static code analyser called [Pysa](https://pyre-check.org/docs/pysa-basics/) that runs a kind of security analysis on your code called 'taint analysis'. A quick summary of this would be to say that you can specify specific kinds of security flaws that you want to address and/or prevent being part of your codebase.

[Pyright](https://github.com/microsoft/pyright) is interesting since it has a useful VS Code integration (via the [Pylance extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)). You get all sorts of autocompletion and tooltip goodness by using Pyright/Pylance.

Finally, chapter 7 thinks through how you might want to approach actually using type checking and type hints in a larger codebase, perhaps one that already exists. It's useful this was included as I imagine these sorts of practicalities are much more of a blocker to adoption than any technical issues. After a brief discussion of tradeoffs, we learn about some different options for where you might want to start with introducing types to a legacy codebase.

- Focusing on the pain points — i.e. where the lack of type hints has already seen bugs emerge in the past
- or perhaps adding them to new code only
- or perhaps type annotating the pieces of the codebase that actually drive the product or business' profits
- or maybe whatever is complex to understand

All of these are options and it will definitely depend on your particular situation.

We also learn about two tools that might help get you started with type annotation: [MonkeyType](https://github.com/instagram/MonkeyType) and [Pytype](https://google.github.io/pytype/). Both auto-generate type hints for your codebase. MonkeyType does so dynamically, so it only generates type hints for parts of your code that it accesses while running the code. Pytype does so by static analysis. Both deliver some kind of output that you can then use (perhaps) as the basis of some annotations of your codebase. My instinct is that these two tools feel like they might lead to some faulty assumptions or errors if you rely on them too much and that in fact it would be better to just methodically go through your code and incrementally add type hints as suggested above.

This concludes the type hints part of the book. I feel like I really got a solid overview of why type hints are used in large or complex Python codebases as well as how to implement this practically. I will be writing separately about how we use `mypy` and type hinting at ZenML as I think it offers an interesting case study on some of the benefits and tradeoffs that we've observed on a day-to-day basis.

Next up in Robust Python: defining your own types with `Enums`, data classes, classes and how this fits into libraries like Pydantic.