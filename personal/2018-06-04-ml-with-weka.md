---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - weka
  - golang
  - machinelearning
  - statistics
date: "2018-06-04"
description: "Getting started with machine learning using Weka's graphical interface, and working through the Titanic dataset from Kaggle to build a foundation in ML workflows before diving into code-based implementations."
layout: post
title: "Machine Learning with Weka"
toc: true
aliases:
  - "/blog/ml-with-weka.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2018-06-04-ml-with-weka/c70977cb3bba_weka-loader.avif)

Learning to program is an infinite process. The field is as open and wide as you can imagine, and you are mostly constrained by your imagination.

I spent much of May getting my mind around [Go](http://golang.org/). I took Todd McLeod's [Go course on Greater Commons](https://greatercommons.com/learn/golang) and learned a great deal. The course was somewhat short on practical implementation, however, and I'm eager to do things with what I learned. More on that in due course.

A parallel strand of my studies has been in statistics and more advanced applications of statistical methods i.e. machine learning. I had done a bit of this in the past, but my poor foundation in basic statistics didn't serve me well. I am now rectifying that through [Andy Field's excellent textbook](https://www.amazon.co.uk/Adventure-Statistics-Reality-Enigma/dp/1446210456/ref=sr_1_1?ie=UTF8&qid=1528122687&sr=8-1&keywords=adventure+statistics).

For machine learning I decided to take a step back from the programming and use a graphical interface to start with. There are great APIs / tools available for this in most languages you can think of but I wanted more of a solid foundation in workflows around machine learning and the kinds of analysis that get done.

I read through a good deal of Jason Brownlee's blog(<https://machinelearningmastery.com/>) as well as his [book on Weka](https://machinelearningmastery.com/machine-learning-mastery-weka/) and he made a good case for why [Weka](https://www.cs.waikato.ac.nz/ml/index.html) is a good place to start.

I have noted [a number of steps](https://workflowy.com/s/E4Ai.KVKD9PdnSl) to move through in sequence, at the same time recognising that data analysis is often unsequential. I expect this to expand and/or redefine this over time.

[Kaggle](https://www.kaggle.com/) is one of the major hubs for machine learning practice (and learning) and I wanted to reengage there. The first data set they usually have you work on [comes from the Titanic disaster](https://www.kaggle.com/c/titanic). You take the full roster of people who boarded, including data points like their economic class, where they were staying on board the ship and their age/gender etc and use anything and everything in terms of tools to predict who survived and who didn't. I had used this data set in the past when I was studying ML with Python.

My initial idea, therefore, was to take the `.csv` files from the Kagge competition and use them in Weka to come up with some predictions. Unfortunately, there are some idiosyncracies about the `.csv` file that make this difficult. Some of the attributes / columns in the data (like names) use punctuation marks which make parsing the csv data non-trivial. Weka uses ARFF files as standard but has the option to parse CSV data. It ran into quite a few errors when trying to crunch through the Titanic data, and no amount of basic fiddling would fix it.

Reading around a little, it seems that others have noted this problem in the past. One [blog post](http://www195.pair.com/mik3hall/weka_kaggle.html) tackled the problem head on but the solution didn't really help me much in the short term. I'm now somewhat stuck, knowing that the fix to the problem is to use another language (Python, perhaps) to range over the data and process it in a form that will be more palatable for Weka. Alternatively, I could use it as an opportunity to build a short Go programme that could perform the same function.

For the moment, i've decided to do neither. I'm going to find an alternative data set which doesn't require wrangling and fiddling. I know wrangling and fiddling is an important skill to master, but it's not the skill I'm trying to focus on right now. Luckily, between the [UCI Machine Learning repository](https://archive.ics.uci.edu/ml/index.php) and various other places, I'm not exactly lacking for examples / other data sets. Today I'll work with the Pima Indians Diabetes data set which came built-in with Weka.
