---
aliases:
- /robustpython/python/books-i-read/2021/12/30/robust-python-2
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2021-12-30'
description: Reflections on the second chapter of Patrick Viafore's recent book, 'Robust
  Python'. We learn about types and how they fit into Python.
image: robust-python/robust-python-cover.jpeg
layout: post
title: What's special about types in Python?
toc: false

---

The first section of
[_Robust Python_](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?qid=&me=&tag=soumet-20&_encoding=UTF8)
dives into types. We begin by taking a step back to think about what exactly
types are being used for, and what they might bring us. Python was not
([until v3.5](https://stackoverflow.com/questions/32557920/what-are-type-hints-in-python-3-5))
a language with which you could easily use typing. I remember going to
[the Pylondinium conference](http://pylondinium.org/2018/) in London in 2018 and
going to
[a talk by Bernat Gabor](https://pylondinium.org/2018/talk.html?talk_id=24)
about type hints in Python. Back then I didn't have much of a sense of how new
they were to many people, but even now I don't get the feeling that they've been
universally adopted. Hence Patrick's book, I suppose…

A type is defined in the book as being "a communication method", both to / for
computers ("mechanical representation") as well as for humans ("semantic
representation"). For the computer, when a variable is of a certain type this
determines what methods can be called on that particular object. As such, though
I'm straying into territory I don't fully understand, I believe it also helps
with compilation efficiency. (Python is a dynamically-typed language so any
errors or type mismatches will only become apparent at runtime, however).

For humans, types can help signal intent. This connects with
[my previous chapter summary](https://mlops.systems/robustpython/python/books-i-read/2021/12/29/robust-python-1.html)
from this book where I stated that code should communicate intent well to be
considered 'robust'. Take the following simple code snippet:

```python
dates = [...]

def process_date(input):
  date = extract_date(input)
  dates.append(date)
  return date
```

We have an `extract_date` function (defined elsewhere in the code), but we have
no real sense of what this `input` parameter would be. Are we taking in strings
as input? Are we taking in `datetime.datetime` objects? Does the `extract_date`
function accept both, or do we need to ensure that we are only taking a specific
type? All these questions could be cleared up with a simple type hint as part of
the function definition, like so:

```python
dates = [...]

def process_date(input: datetime.datetime):
	date = extract_date(input)
  dates.append(date)
  return date
```

Now we know what the `input` should be, and we can also add a type hint to the
`extract_date` function as well which will help _communicate our intent_.

We also learn how Python is more towards the 'strongly-typed' side of things on
the language spectrum. If you try to concatenate a `list` with a `dict` in
Python using the `+` operator, Python will throw a `TypeError` and fail. If you
try to do the same in Javascript you get two different answers depending on the
order of the two operands:

```
>>> [] + {}
"[object Object]"

>>> {} + []
0
```

For our purposes, using Python, we can use the strong typing to our advantage.

Python is dynamically typed, though, which takes a bit more caution to handle in
a robust manner. Any type mismatches will only be found at runtime — at least
using just the vanilla install of the language without any extra imports or
modules.

The chapter ends with a brief discussion of duck typing, defined as "the ability
to use objects and entities in a programming language as long as they adhere to
some interface". We gain a lot in terms of increased composability, but if you
rely on this feature of the language too much then it can become a hindrance in
terms of communicating intent.

This chapter didn't add too many new concepts or skills to my current
understanding of the benefits of types, but it was useful to have this concept
of 'communicating intent' to be reiterated. When I think back to how I've heard
types mentioned in the past, they often get cast in a technical sense, whereas
thinking about communication between developers I think is a more motivating
framing.
