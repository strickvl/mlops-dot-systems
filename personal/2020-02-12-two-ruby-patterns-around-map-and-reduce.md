---
author: Alex Strick van Linschoten
categories:
  - coding
  - ruby
  - launchschool
date: "2020-02-12"
description: "Two fundamental patterns for transforming data in Ruby: using map to convert arrays into transformed arrays, and using reduce to combine multiple values into a single result."
layout: post
title: "Two Ruby patterns around map and reduce"
toc: true
aliases:
  - "/blog/two-ruby-patterns-around-map-and-reduce.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

When you're going to choose a method to work to transform a group of `n` things in Ruby, there are two broad patterns you can choose: work with a `map` function or work with a `reduce` / `inject` function.

This pattern choice was recently explained to me as part of my Ruby education at [Launch School](https://launchschool.com/). I hadn't fully grokked that the choice around how you transform a bundle of things (an `Array`, perhaps) really can be summarised by those two options.

You use a `map` method when you want to transfer your array into another array of (transformed) things. (For example, you wanted to transform an array of lowercase names into an array of uppercase names).

```
example_array = ['alex', 'john', 'terry', 'gill']
transformed_array = example_array.map(&:upcase) # => ["ALEX", "JOHN", "TERRY", "GILL"]
```

You use a `reduce` method when you want to transform `n` number of things (inside your array) into a single thing. (For example, you wanted to sum up the values of an array).

```
example_array = [1, 3, 5, 7, 9]
transformed_array = example_array.reduce(:+) # => 25
```
