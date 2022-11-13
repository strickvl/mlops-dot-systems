---
aliases:
- /books-i-read/python/robustpython/2022/01/18/robust-python-5
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2022-01-18'
description: Reflections on the fifth chapter of Patrick Viafore's book, 'Robust Python'.
  We learn about how to use type annotations when collections (lists, dictionaries
  and sets, primarily) are involved.
image: robust-python/robust-python-cover.jpeg
layout: post
title: Using type annotation with collections in Python
toc: true

---

The fifth chapter of
['Robust Python'](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?_encoding=UTF8&me=&tag=soumet-20&qid=)
continues on from
[where we left off](https://mlops.systems/robustpython/python/books-i-read/2022/01/08/robust-python-4.html)
last time. We saw how to apply type annotations when simple things like strings,
integers and floats were involved. This chapter deals with the different ways
you annotate your types when collections get involved.

We start with the context for why this is even something that requires a
separate chapter to deal with. This involves the difference between homogenous
and heterogeneous types. For a Python list, we could say it had homogenous types
if all the items were of the same type (strings, e.g.). If this list contains
multiple different types (a mix of strings and integers, e.g.) then we'd have to
say it contained heterogenous types. This is of importance given that the
presence of multiple types in a single list is going to require you to handle
the types differently. Even in the most trivial of examples (as with strings and
integers being together), the interfaces for both are different. Try adding a
string to an integer in Python and see what happens.

So it's actually not quite true to say that a collection of homogenous types
have to all be exactly the same type, but they must share common interfaces and
ideally be handled using the same logic. If you think about it, in the real
world heterogenous types are pretty common occurrences. There are often
situations where, for example, you have to handle the output of API calls or
data that doesn't derive from code that's in yous control and then you'll
perhaps be dealing with a dictionary that contains all sorts of types.

In Python we do have the `typing.Any` annotation, but it's pretty clear — and
the book emphasises this — that isn't really useful in the vast majority of
cases. You might as well not bother with type annotations if you're going to
liberally be using `Any`.

## The first of our collection type helpers: `TypedDict`

`TypedDict` was introduced in Python 3.8 and allows you to communicate intent
when it comes to the types that are being passed through your code. Note that,
as with a lot of what we're talking about here, this is all information that's
useful for a type checker and isn't something that is dynamically checked.

You can use `TypedDict` to define structures that specify the types of fields of
your dictionary in a way that is easier to parse as a human reader than just
using `dict`. See this example, adapted from one in the book:

```python
from typing import TypedDict

class Range(TypedDict):
    min: float
    max: float

class Stats(TypedDict):
	value: int
	unit: str
	confidenceRange: Range

our_stats = Stats(value=3, unit="some_name", confidenceRange=Range(min=1.3, max=5.5))
print(our_stats) # returns {'value': 3, 'unit': 'some_name', 'confidenceRange': {'min': 1.3, 'max': 5.5}}
```

If `TypedDict` doesn't do everything you need it to, we have some other options.

## Custom Collections with `TypeVar`

`TypeVar` in Python is how you can implement generics. Generics, as I learned
while reading, are ways of representing things that are the same, like when you
don't care what specific type is being used. Take this example from the book,
where you want to reverse items in a list, but only if the items are all of the
same type. You could write the following:

```python
from typing import TypeVar
T = TypeVar('T')
def reverse(coll: list[T]) -> list[T]:
	return coll[::-1]
```

You can use generics in other ways to create new kinds of collections or
groupings. For example, again this one is adapted from the book, if you were
writing a series of methods that returned either something useful or a
particular error message:

```python
def get_weather_data(location: str) -> Union[WeatherData, APIError]:
	# …

def get_financial_data(transaction: str) -> Union[FinancialData, APIError]:
	# …
```

…and so on, you could use generics as a way of simplifying how this gets
presented:

```python
T = TypeVar('T')
APIResponse = Union[T, APIError]

def get_weather_data(location: str) -> APIResponse[WeatherData]:
	# …

def get_financial_data(transaction: str) -> APIResponse[FinancialData]:
	# …
```

That looks and feels so much cleaner!

## Tweaking existing functionality with `collections`

If you're just making slight changes to the behaviour of collections, instead of
subclassing dictionaries or lists or whatever, it's better to override the
methods of `collections.UserDict`, `collections.UserString` and/or
`collections.UserList`.

You'll run into fewer problems when you actually implement this. Of course,
there is a slight performance cost to importing these collections, so it's worth
making sure this cost isn't too high.

You'll maybe have noticed that there isn't a `collections.UserSet` in the list
above. For sets we'll have to use abstract base classes which are found in
`collections.abc`. The big difference between the `User*` pattern of classes,
there is no built-in storage for the `abc` classes. You have to provide your own
storage if you need it. So for sets, we'd use `collections.abc.Set` and then
implement whatever group of methods are required for that particular class.

In the set example, we have to implement `__contains__`, `__iter__` and
`__len__`, and then the other set operations will automatically work. There are
currently (as of Python 3.10.2)
[25 different ABCs](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)
available to use. I definitely will be exploring those as they seem really
useful.

Even though this chapter got into the weeds of collections a little, I learned a
_lot_ and I'm already finding places in the ZenML codebase where all of this is
being used.

## Typeguard

Before I leave, since we're still thinking about types, I wanted to share this
little package I discovered the other day:
[`typeguard`](https://typeguard.readthedocs.io/en/latest/index.html). You can
use it in a bunch of different ways, but a
[useful short video from calmcode.io](https://calmcode.io/shorts/typeguard.py.html)
showed how a simple decorator can simplify code and catch type errors.

Consider the following example code:

```python
def calculate_risk(risk_factor: float) -> str:
	"""Calculates how much risk you took"""
	return risk_factor * 3 # arbitrary return value :)
```

What if someone passes in a wrong type into this function? It'll fail. So maybe
we want to handle that particular situation:

```python
def calculate_risk(risk_factor: float) -> str:
	"""Calculates how much risk you took"""
	if not isinstance(risk_factor, float):
		raise ValueError("Wrong type for risk_factor")
	return risk_factor * 3
```

If you have lots of parameters in your function and you have to handle them all,
this could get messy quite quickly. Instead, we can `pip install typeguard` and
do the following:

```python
from type guard import typechecked

@typechecked
def calculate_risk(risk_factor: float) -> str:
	"""Calculates how much risk you took"""
	return risk_factor * 3
```

Now that's a handy little decorator! It'll handle all the raising of appropriate
errors above based on whether you passed in the right type or not. It works for
classes as well. You're welcome, and thanks
[Vincent](https://twitter.com/fishnets88) for making the introductory video!
