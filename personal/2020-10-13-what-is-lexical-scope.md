---
author: Alex Strick van Linschoten
categories:
  - coding
  - launchschool
  - javascript
date: "2020-10-13"
description: "Understanding lexical scope and how nested functions access variables in JavaScript."
layout: post
title: "What is Lexical Scope?"
toc: true
aliases:
  - "/blog/what-is-lexical-scope.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Scope defines what functions / variables and values are available at any point in a programme. Lexical scope is when you can derive the scope from looking at the code, or by looking at its position within the code. Lexical scope is also known as static scope.

The source code of our JavaScript code — in my example — defines the scope. It particularly relates to functions and nested functions. In those cases, we can create a hierarchy of scopes.

The inner functions have access to everything outside them, but the outer functions don't have access to everything from the inner functions.

Every function creates a new local variable scope. Every block also creates a new local variable scope. The code doesn't have to be executed for these scoping rules to be true, for these inner and outer scopes to exist.

This example below will log 'hello from inner scope' but will then give a `ReferenceError` since the variable `secret` is only available / accessible inside the inner scope function:

```
function outerScope() {
  function innerScope() {
    let secret = 'this is in inner scope';
    console.log('hello from inner scope'); 
  }

  innerScope();
  console.log(secret);
}

outerScope();
```
