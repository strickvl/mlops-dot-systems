---
author: Alex Strick van Linschoten
categories:
  - rust
  - learning
  - TIL
date: "2024-09-16"
description: "A quick post on what the 'prelude' is and why it exists."
layout: post
title: "What is the Rust prelude?"
toc: false
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I'm studying Rust these days on the side and one thing that I keep hearing and seeing is the idea of the 'prelude'. I thought I'd write a quick blog to cement exactly what's going on here.

At a very high level, the prelude is a bunch of functions, methods and other things that are automatically available to you when you start working on your project without you having to manually or explicitly import them. As [the Rust docs](https://doc.rust-lang.org/std/prelude/) state:

> "The prelude is the list of things that Rust automatically imports into every Rust program. It’s kept as small as possible, and is focused on things, particularly traits, which are used in almost every single Rust program."

I thought maybe a good example of this is the classic 'Hello, World!' starter when you create a new project using `cargo new ...`:

```rust
fn main() {
    println!("Hello, World!")
}
```

So here we have `println!` which is actually a macro, and from what I read this is *not* part of the prelude, though it is available to us by default.

A better / actual list of some things that are made available would include some types like `Option`, `Result`, `String` and `Vec`, as well as some traits like `Copy`, `Clone`, `Eq` and so on. For a full list, refer to [the official prelude contents](https://doc.rust-lang.org/std/prelude/#prelude-contents) as listed in the docs. Note that there are several versions (2015, 2018, 2021 etc) of the prelude. My understanding is that each successive version only adds new things that are exported by default. If that wasn't the case, then I'm guessing it would be hard to provide those solid backwards-compatibility guarantees.

So basically, there are some symbols or imports that were deemed to be used so
often that they decided not to force you to have to import them explicitly every
time you want to get started writing code.
