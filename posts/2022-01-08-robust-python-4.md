---
aliases:
- /books-i-read/python/robustpython/2022/01/08/robust-python-4
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2022-01-08'
description: Reflections on the fourth chapter of Patrick Viafore's recent book, 'Robust
  Python'. We learn about the different options for combining types and constraining
  exactly which sets of types are permitted for a particular function or variable
  signature.
image: images/robust-python/robust-python-cover.jpeg
layout: post
title: Different ways to constrain types in Python
toc: true

---

The fourth chapter of ['Robust Python'](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?_encoding=UTF8&me=&tag=soumet-20&qid=) continues on from [where we left off](https://mlops.systems/robustpython/python/books-i-read/2022/01/03/robust-python-3.html) last time. We had previously learned about the benefits of type annotations in general terms, as well as started to understand how we might apply these annotations to simple code examples. But what if things are a bit more complicated? Then we have a few more options at our disposal.

Note that you can assign all of these type assignments to variables ('type aliases'), which might just make your code that much more readable.

## `Optional` to catch `None` references

`Optional` as a type annotation is where you want to allow a specific type or `None` to be passed in to a particular function:

```python
from typing import Optional

def some_function(value: Optional[int]) -> int:
	# your code goes here
```

Note that you'll probably want (and `mypy` will remind you if you forget) to handle what happens in both those cases inside your function. (You may need to specifically pass in the `—strict-optional` flag to catch this when using `mypy`.)

## `Union` to group types together

This is used when multiple different types can be used for the same variable:

```python
from typing import Union

def returns_the_input(input: Union[str, int]) -> Union[str, int]:
	return input
```

This function doesn't really do anything, but you get the idea. Note, too, that `Optional[int]` is really a version of `Union[int, None]`. (The book gets into exactly why we might care about reducing the number of possible options by way of a little detour into set theory.)

## `Literal` to include only specific values

A little like what I believe enumerations do, we also have the `Literal` type. It restricts you to whatever specific values are defined:

```python
from typing import Literal

def some_function(input: Literal[1, 2, 3]) -> int:
	return input
```

Here the function is restricted to inputs that are either 1, 2 or 3. Note that these are a feature that applies to Python 3.8 and above.

## `Annotated` for more complicated restrictions

These are available, but not really useful since they only function as a communication method. You can specify specific restrictions such as the following (example is taken from the book, p. 56:

```python
from typing import Annotated

x: Annotated[int, ValueRange(3,5)]
y: Annotated[str, MatchesRegex('[abc]{2}')
```

Read more about it [here](https://docs.python.org/3/library/typing.html?highlight=annotated#typing.Annotated). The book doesn't spend much time on it and it seems like it's probably best left alone for the moment.

## `NewType` to cover different contexts applied to the same type

`NewType`, on the other hand, is quite useful. You can create new types which are identical to some other type, and those new values made with the new type will have access to all the methods and properties as the original type.

```python
from typing import NewType

class Book:
	# you implement the class here
	
NewBook = NewType("NewBook", Book)

def process_new_book(book: NewBook):
	# here you handle what happens to the new book
```

You can achieve something like the same thing with classes and inheritance, I believe, but this is a lightweight version which might be useful to achieve the same end goal.

## `Final` to prevent reassignment / rebinding

You can specify that a particular variable should have a single value and that value only. (Note that mutations of an object etc are all still possible, but reassignment to a new memory address is not possible.

```python
from typing import Final

NAME: Final = "Alex"
```

If you tried to subsequently change this to a different name, `mypy` would catch that you'd tried to do this. This can be valuable across very large codebases, where the potential for someone to reassign a variable might be not insignificant.

So there you have it: a bunch of different ways to handle combinations of types and/or more complicated annotation scenarios. The next chapter will cover what happens when we throw collections into the mix, and what type annotation challenges are raised.