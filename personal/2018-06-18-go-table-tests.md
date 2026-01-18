---
author: Alex Strick van Linschoten
categories:
  - coding
  - testing
  - golang
date: "2018-06-18"
description: "How I learned to use table tests in Go to test multiple scenarios against the same function."
layout: post
title: "Table Tests in Go"
toc: true
aliases:
  - "/blog/go-table-tests.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2018-06-18-go-table-tests/54d26a29baf9_ScreenShot_2018-06-18_at_21.47.05.avif)

Today I wanted to stretch my use of test scenarios with Go. The example I [described a couple of days ago](https://www.alexstrick.com/blog/testing-workflow-golang) basically had me running individual tests for specific values. What I wanted was a way to test a bunch of different values for the same function. Enter: table tests.

You can see the code I ended up with partly in the image above but also on Github [here](https://github.com/strickvl/golang_greatercommons/blob/master/fmt-exercise/main_test.go). It took a while to get there.

I started with some notes I’d taken during [Todd McLeod’s](https://twitter.com/Todd_McLeod) excellent [GreaterCommons Go course](https://greatercommons.com/learn/5098183625539584). Those notes were enough to get a framework up and running. I understood the principle: you create a struct to store all the different values, loop over them all to check whether the test fails in any particular scenario.

When I ran *go fmt* at the end to format my code, it gave me an error as it refused to build:

![](images/2018-06-18-go-table-tests/2ec46b2e84d8_ScreenShot_2018-06-18_at_22.04.25.avif)

I could see that it wanted two ints and I was giving it a slice of ints. Basically this turned into a hunt for fixing my loop and which values I was spitting out at various iterations of the loop.

I ended up isolating the part of the code that was causing the problems, putting it [up on the Go Playground](https://play.golang.org/p/RtvQvSApaxh) so as to isolate exactly what was going wrong. Once I’d figured out exactly how to handle the loop, I could then bring that logic back into my *main\_test.go* file.

Now I know how implement table tests in Go. My next exploration will be around functions that aren’t located in the same file. So far I’ve been mainly using the same *main.go* file for all the code I’ve written, but a step up in the complexity will be to interact with different files.
