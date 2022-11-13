---
aliases:
- /books-i-read/python/robustpython/2022/01/30/robust-python-8
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2022-01-30'
description: The eight chapter of Patrick Viafore's book, 'Robust Python', gets into
  enums which you can use when you have a grouping of some constants that belong together.
image: robust-python/robust-python-cover.jpeg
layout: post
title: How and where to use enums in Python
toc: false

---

The second part of Viafore's ['Robust Python'](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?qid=&me=&tag=soumet-20&_encoding=UTF8) is all about user-created types. We start simple in chapter eight and consider the `Enum` type as a way of defining a particular restricted set of values. An example might help get us started:

```python
from enum import Enum

class TrafficLightsState(Enum):
  RED = "red"
  YELLOW = "yellow"
  GREEN = "green"
  OFF = "off"

current_state = TrafficLightsState.GREEN
print(current_state.value) # prints 'green'
```

We subclass off `Enum` and define the pairings of values that belong together. I hope you can see already that this is a readable way to define these values and show that they are part of the same semantic grouping.

If we're using these definitions not because we care about the values themselves but because we want to be able to evaluate whether the state of one particular traffic light is the same as a different traffic light, we can use `auto` to automatically assign values (ascending integers, by default) in the following way:

```python
from enum import Enum, auto

class TrafficLightsState(Enum):
  RED = auto()
  YELLOW = auto()
  GREEN = auto()
  OFF = auto()

current_state = TrafficLightsState.GREEN
print(current_state.value) # prints 3
```

You can iterate through your enums or get their length just as if it was a list, too.

While writing the above text, I realised that I was getting confused about the difference between types and classes in Python. It turns out that whatever differences once existed, they aren't much of a thing any more and [to all intents and purposes](https://stackoverflow.com/questions/4162578/python-terminology-class-vs-type) they're practically the same thing.

A lot of the enum-related definitions at work are defined in [this file](https://github.com/zenml-io/zenml/blob/0.6.0/src/zenml/enums.py). You can see that we tend not to use `auto`, though I'm not really sure why. (We don't ever seem to compare against actual values.)

If you want to make sure that the actual values assigned to these grouped constants are unique, you can add the `@unique` decorator which will enforce that you aren't duplicating values.

Better still for the readability of your code, you can use this collective type in your type annotations. For sure the difference between these two options should be clear:

```python
def get_status(some_input: str) -> str:
	# code goes here

def get_status(some_input: str) -> TrafficLightsState:
	# code goes here
```

In the first case, it is far less clear what's going on.

Note that if you're purely looking for a way to restrict the assignation to a particular variable, you can also use the `Literal` type, introduced in Python 3.8, though remember that it doesn't help with iteration, runtime checking or map values from name to value. For all that, you'll want to be using `Enum`."

If you want a way to combine Enums together, you can subclass from `enum.Flag`. Consider the case of when you have a list of enums for days of the week, but you want to represent the weekend as a pairing of Saturday and Sunday (if you were in Europe, e.g.). You could do the following:

```python
from enum import Flag, auto
class Weekday(Flag):
	MONDAY = auto()
	TUESDAY = auto()
	WEDNESDAY = auto()
	THURSDAY = auto()
	FRIDAY = auto()
	SATURDAY = auto()
	SUNDAY = auto()
	
weekend = Weekday.SATURDAY | Weekday.SUNDAY
```

You can perform bitwise operations on these combined groupings, but note that the values must support bitwise operations. (Strings don't support them, while integers do.)

Finally, the chapter covers the special case of `IntEnum` and `IntFlag` which allows for the conversion of integer values. This can be confusing and lead to non-robust behaviours, so the book discourages this particular usage.

Next up is Data Classes, something I'm extremely interested in getting to grips with as it comes up in our codebase at work a decent amount.
