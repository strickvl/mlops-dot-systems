---
aliases:
- /robustpython/python/books-i-read/2022/02/05/robust-python-9
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2022-02-05'
description: Chapter 9 of 'Robust Python' dives into the uses of data classes, a user-defined
  datatype in which you can store heterogenous data together. They help formalise
  implicit concepts within your code and as a result also improve code readability.
image: robust-python/robust-python-cover.jpeg
layout: post
title: Upgrade your Python dicts with data classes
toc: false

---

I've been curious about data classes since more or less my first day at work when someone mentioned to me that Pydantic was built on the shoulders of data classes. I hadn't taken the opportunity to dive into all the details of what data classes do until now, prompted by their being part of Patrick Viafore's book, '[Robust Python](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?_encoding=UTF8&me=&tag=soumet-20&qid=)', specifically chapter nine.

An example upfront might help ground the conversation. Here is a data class in action:

```python
import datetime
from dataclasses import dataclass
from typing import Literal

@dataclass
class CatPassport:
  name: str
  breed: CatBreed
  issue_date: datetime.date
  expiry_date: datetime.date
  gender: Literal['male', 'female']

aria = CatPassport("Aria", CatBreed('bengal'), datetime.date(2022, 01, 05), datetime.date(2025, 01, 04), 'female')
print(aria.name) # prints 'Aria'
```

From this you can see that it's an easy way to represent structured data made up of different types. Where it excels over simply using a `dict` or a class you write yourself is the fact that it auto-generates a number of `__` dunder helper methods. You get `__str__` and `__repr__` to handle what this object looks like when you try to `print()` it. It also creates an `__eq__` method which allows you to check for equality between two objects of the same type with the `==` comparison operator. 

(If you want to add a way to compare between your data class objects, you can add arguments to the `@dataclass` decorator like `@dataclass(eq=True, order=True)` which will handle the creation of the relevant dunder methods.

The fact that data classes are just classes at heart mean that you can also add behaviours to these collections of values, something that isn't possible with a plain `dict`.

You can specify that your data class should be frozen (`@dataclass(frozen=True)`) which effectively makes it an immutable data store, though taking note that objects stored as values on the data class' properties might themselves not be immutable (think lists and dicts).

After reading the chapter in 'Robust Python', I read around a little to get a sense of this concept. I read [the official docs](https://docs.python.org/3/library/dataclasses.html) which were fairly helpful, but in fact it was [the PEP document (557)](https://www.python.org/dev/peps/pep-0557/) that I found most interesting. I haven't previously taken the time to dive into the specifics of PEP specifications before, but I discovered that they are pretty readable and you get a real sense of what problem a particular feature or addition to the language was trying to solve.

[PEP 557](https://www.python.org/dev/peps/pep-0557/) explains some of the alternatives and why it might be useful to include this new feature. I also learned about the [`attrs`](https://github.com/python-attrs/attrs) package and how data classes are actually just a subset of what `attrs` offers. (As a side note, I was surprised that `attrs` seems to have been mentioned nowhere in 'Robust Python', even in the context of the upcoming Pydantic chapter. Perhaps it was just too confusing to have all these things alongside one another.)

Other options to consider alongside data classes when dealing with heterogenous data inside a single object or structure include `TypedDict` and `namedtuple`, but it seems like the default for this kind of scenario should probably just be a data class, though I should add that it is only part of the standard library for Python 3.7 and above.
