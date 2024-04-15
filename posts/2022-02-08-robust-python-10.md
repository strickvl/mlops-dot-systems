---
aliases:
- /robustpython/python/books-i-read/2022/02/08/robust-python-10.html
author: Alex Strick van Linschoten
categories:
- robustpython
- python
- books-i-read
date: '2022-02-08'
description: 'Chapter 10 covers the last of the user-defined types explored in ''Robust
  Python'': classes. We learn what an ''invariant'' is and how to decide whether to
  use a data class or a class when rolling your own types.'
image: robust-python/robust-python-cover.jpeg
layout: post
title: What are invariants and how can they help make your Python classes more robust?
toc: true

---

We've read [about enumerations](https://mlops.systems/robustpython/python/books-i-read/2022/01/30/robust-python-8.html) and we've read [about data classes](https://mlops.systems/robustpython/python/books-i-read/2022/02/05/robust-python-9.html). Now it's the turn of classes. Chapter 10 of Patrick Viafore's excellent book, '[Robust Python](https://www.amazon.com/Robust-Python-Patrick-Viafore-ebook-dp-B09982C9FX/dp/B09982C9FX/ref=mt_other?qid=&me=&tag=soumet-20&_encoding=UTF8)', is the last of the user-defined types to be covered. Early on he makes a good point that classes are often taught really early to those new to Python and/or programming, and that maybe the story is a bit more complicated. As I've mentioned before, things like enums and data classes are more or less unmentioned in such educational materials and as such I found this book really helped me fill in the conceptual gaps.

First off, for someone who has just learned about data classes, how would you explain what is new or distinct when it comes to classes? They're slightly different syntactically, with classes requiring you to write a bit more boilerplate. Compare the following:

```python
from dataclasses import dataclass
import datetime
from typing import Literal

# data class definition
@dataclass
class Cat:
	name: str
	breed: CatBreed
	birth_date: datetime.date
	gender: Literal['male', 'female']

# class definition
class Dog:
	def __init__(self, name: str, breed: CatBreed, birth_date: datetime.date, gender: Literal['male', 'female']):
		self.name = name
		self.breed = breed
		self.birth_date = birth_date
		self.gender = gender
```

You can note how it seems like the data class version is much more readable and involves less boilerplate to achieve the same effect, and for a simple example like this you're probably right. The difference, and where classes make sense and shine, is when you have a conceptual grouping or type that includes some notion of invariants.

## What is an invariant?

Most of this chapter is about invariants and how they relate to classes, and I'll admit I had never heard of the concept before reading in this book. An invariant is defined as "a property of an entity that remains unchanged throughout the lifetime of that entity." You can think of it as some kind of context or a property about that particular type that you need to encode and that won't change.

The book gives a pizza example (where a `Pizza` object could encode that in its list of toppings, the cheese could only be the final topping (i.e. on top) of the pizza). An alternative might be some kind of rule relating to an ID number, where either it must be unique to some kind of specification, or where the ID must conform to some kind of specification.

Even with this rudimentary definition, you can see how there might be some advantages to being able to account for these rules and properties of the object type. (With data classes, you don't have as much flexibility to specify all these nuances.) So what happens when you're instantiating a class and you hit one of those scenarios where your contextual rules dictate that something can't happen? (i.e. someone tries to create a `Pizza` object that has cheese as the bottom-layer topping) The book offers up two options:

1. Throw an exception — this will break you out of the code flow and prevent the object from being constructed
2. Do something to make the data fit — you can perform some kind of transformation which sees the cheese ingredient as being forced onto the top layer of the pizza toppings (or whatever is the equivalent for your specific scenario)

Note that the kinds of restrictions posed by these invariants are things that can't fully be captured by the typing system. [We've covered type hints](https://mlops.systems/#category=redactionmodel) and how they can help make your code more robust, but types don't help much when it comes to the order of a list, for example.

## Why code around invariants?

So why go to all of this trouble in the first place? How does it benefit to code with the invariants in mind? To start with, it'll probably help you think through edge cases and exceptions that you could do well to be wary of. The invariants alert you to the fact that arguments passed into functions and methods will not always be in the form that you would ideally like. (As a side note, this might also encourage you to add unit tests.)

It will help you keep the code that handles the invariants together instead of mixing it in with the code that instantiates the objects. In general, it will enhance your ability to reason about the code and the concepts that your code reflects. This is important not only for the implementation in code, but for how you think about any particular part and how it relates to the rest of your code base.

The goal for all of this: fewer bugs and a more robust system. Yes, it takes a bit more effort to think whether there are implicit or explicit invariants, but doing so makes your code and your system more reliable. In Viafore's words:

> "You're making an easier API for people to think about, and you reduce the risk of people using your objects incorrectly. […] You never want someone to be surprised when using your code." (p. 141)

## Invariants and class consumers

The rest of the chapter is about the implementation consequences of thinking about classes in this invariants-first way. For consumers of the class, how should you ensure that the invariants handled are clear? Aside from the implementation itself (in the constructor), docstrings and code comments are suggested as a means to this end. Of course, `README` files and documentation in general can serve the same purpose, but it's best if the context and information about invariants is as close to the code as possible.

## Invariants and class maintainers

For (future) maintainers of the class, unit tests are the way to go. Make sure that the relevant scenarios and invariants are covered by testing code and you will have extra confidence that your object instantiation really does do what you intend. Your code should already be doing the checking for invariants on the instantiation side, but unit tests are a way of ensuring that this is actually the case (and also that these invariants remain covered as the code base continues to evolve.

(The book offers one way of doing such tests for invariants with `contextlib.contextmanager` on page 145.)

## Encapsulation and classes

As the final chunk of the chapter, we learn about private, protected and public access to the properties and methods of a class, and how they relate to the maintenance of invariants.

This is an important part of the story. As users interface with your class and API, encapsulation is a way to ensure that they update and interact with the these properties in a way that is under your control. For example, even if at instantiation you enforce the `Pizza` object having cheese as the top-layer topping, what do we have in place to ensure that the user doesn't just amend the `toppings` property such that the cheese is the bottom-layer topping (i.e. AFTER instantiation)? Encapsulation — having an entity hide or restrict access to certain properties and actions — is how you handle that.

The book goes into a fair amount of detail on the uses of these different levels of access, and introduces the idea of 'accessors' and 'mutators' as an alternative to the more commonly-used 'getters' and 'setters'.

Remember, "you use invariants to allow users to reason about your objects and reduce cognitive load." (p. 151)

## So what am I supposed to use?

![]({{ site.baseurl
}}/images/robust-python-10/which-abstraction.png "A super helpful diagram from the book helping you choose which abstraction to pick.")

The end of the chapter offers this really helpful flowchart diagram which summarises the choices that we've covered during the previous three chapters. I really want to highlight that this chapter helped me think about classes in a way I hadn't, despite having been through courses, having read numerous articles and of course coded in this class-oriented fashion for several years.

The next few chapters continue onwards by thinking about how to design your interfaces such that they make sense for your users and allow your code base to grow with as few headaches as possible.
