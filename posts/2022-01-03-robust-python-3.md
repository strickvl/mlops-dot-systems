---
aliases:
- /books-i-read/python/robustpython/2022/01/03/robust-python-3
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2022-01-03'
description: Reflections on the third chapter of Patrick Viafore's recent book, 'Robust
  Python'. We get some quick practical examples of how to use type annotation and
  how to use tools like `mypy` to analyse how typed values pass through your code.
image: images/robust-python/robust-python-cover.jpeg
layout: post
title: Getting practical with type annotations and `mypy`
toc: false

---

The third chapter of ['Robust Python'](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?_encoding=UTF8&me=&tag=soumet-20&qid=) offers a quick introduction to the practicalities of type annotations in Python. We also see tools like `mypy` being used to catch places where the reality of your code doesn't necessarily match the type annotations that you've stated.

For the first, a quick example can suffice:

```python
name: str = "alex"

def some_function(some_number: int, some_text: str = "some text") -> str:
	# your code goes here
	return "" # returns a string
```

You can see the different places that type annotations might appear. You can annotate variables in your code. I've seen this one less often, but it's possible. Then you can have type annotations for the parameters when defining functions (some even with default values assigned). You can also have type annotations for the return value of those functions.\

Note that type hints are not used at runtime, so in that sense they are completely optional and don't affect how your code runs when it's passed through the Python interpreter. (Type hints were introduced in Python 3.5, though there is a way to achieve the same effect using comments and a standard way of listing type annotations that way if you are stuck with a 2.7 codebase, for example.)

With some type annotations added to our code, we can use a typechecker like `mypy` to see whether things are really as we imagine. In Viafore's own words:

> "type checkers are what allow the type annotations to transcend from communication method to a safety net. It is a form of static analysis."

If your codebase uses type annotations to communicate intent, and you're using `mypy` to catch any of those type errors, remember that typecheckers only catch this certain type of errors. You still need to be doing testing and all the other best practices to help catch the rest.

One forward-looking benefit covered by this chapter was how having code covered with type annotations and type checking could give you the confidence to change things in the codebase that otherwise you would have hesitated to even approach. There  are, of course, also some tradeoffs and disadvantages to adding this in: particularly around speed of iteration and possibly flexibility, but the book makes a strong case for why most large Python codebases could probably use type checking as part of their arsenal.