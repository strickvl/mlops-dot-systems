---
author: Alex Strick van Linschoten
categories:
  - coding
  - ruby
  - launchschool
date: "2019-02-25"
description: "I discovered Ruby's .digits method and explored when it's actually worth using over simpler alternatives like .to_s.chars."
layout: post
title: "Using Ruby's .digits method"
toc: true
aliases:
  - "/blog/using-rubys-digits-method.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I discovered the `.digits` method in Ruby the other day. As a quick illustration, it extracts the digits of a method into an array, reverse sorted.

```
12345.digits #=> [5, 4, 3, 2, 1]
```

You can optionally specify what *base* you’d like it to use to calculate the digits using, i.e. the same calculation as above but in base 100 would give you the following:

```
12345.digits(100) #=> [45, 23, 1]
```

Reading around [a little bit](https://stackoverflow.com/questions/47953598/rubys-digits-method-performance), it seems that if you’re trying to get hold of the digits of a number, simply doing a `.digits.reverse` is perhaps an ok solution if the number is small, but at a certain point it starts to get slow. This is because `.digits` isn’t just ‘splitting’ the number.

For that reason, perhaps using `.to_s.chars` might be a better alternative. You can then use a `.map` function to convert the characters into integers:

```
12345.to_s.chars.map { |digit| digit.to_i }
```

I’m not entirely sure what `.digits` is actually used / useful for, given the speed issues.
