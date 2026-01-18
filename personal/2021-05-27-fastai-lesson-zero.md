---
author: Alex Strick van Linschoten
categories:
  - productivity
  - deep-learning
  - study
  - fastai
  - deeplearning
date: "2021-05-27"
description: "My notes from Jeremy Howard's FastAI Lesson 0 video on how to approach learning deep learning effectively."
layout: post
title: "FastAI Lesson Zero: video notes"
toc: true
aliases:
  - "/blog/fastai-lesson-zero.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

[These are mainly notes for myself, based off Jeremy Howard’s ‘Lesson 0’ [video](https://youtu.be/gGxe2mN3kAg) that was recently posted. It doesn’t capture the entirety of what was said during the course, but it includes pieces that I felt are relevant to me now and that might be relevant to me in the future.]

- decide when you’re studying
  - be precise about how much time you’re going to spend
  - think about how it’s going to fit into your day or your life
  - give yourself deadlines and goals, perhaps, but also don’t worry if disruptions happen.
  - Mainly make sure that if something *does* come up, make sure you get back on the horse and keep going. (Tenacity counts for a lot)
- Finish. The. Course.
  - make a commitment to complete [the course](https://course.fast.ai), and make sure you actually do that.
  - If you’re attending the course and working through it, you should follow through on your original commitment and actually work through the course.
- Finish a Project
  - build a project and make it really great.
  - You’ll probably have several projects here and there that you work on during the course of the fastai course, but at a minimum make sure you pick one of those and make it really great.
  - (It doesn’t have to be unique or world-changing. Even replicating something that’s already in existence can still be worth it).
- Find good role models
  - Jeremy raises up the example of [Radek Osmulski](https://twitter.com/radekosmulski/) (who recently published an ebook called [Meta Learning](https://gumroad.com/l/learn_deep_learning)).
  - ([Jeremy](https://twitter.com/jeremyphoward/) himself is a good role model too).
- Learn by doing. Use what you learn and figure out the rest as you go. (Don’t get paralyzed by trying to learn ‘pre-requisites’ like complex mathematics topics, esp since most of them aren’t actually needed to become a practitioner).
- Share and communicate your work
  - (Jeremy doesn’t mention the book, but I’ll insert here that the book “[Show Your Work](https://www.amazon.com/Show-Your-Work-Austin-Kleon/dp/076117897X/ref=tmm_pap_swatch_0?qid=1621525599&sr=1-1&tag=soumet-20&_encoding=UTF8)” by Austin Kleon is a great starter on this point).
  - If you consistently blog during your studies, at the end of it you’ll likely have a huge collection of artefacts of that study, showing what you’ve learned and accomplished.
  - Alongside that, being a good citizen and contributing in the forums etc is also a really solid way to extend whatever knowledge you have to others, and quite possibly cement things in your own mind as you reply.
- How to do a lesson
  - watch the video / read the chapter
  - Run the notebook & experiment — play around with things + make sure you actually understand what’s happening
  - Reproduce the notebook from scratch — (and really start with nothing here, and try to reimplement whatever was done during the lesson. From previous experience, this work will be hard, but it’s super worth it. Recall learning is the best kind of learning)
  - Repeat with a different dataset — use the techniques you learned in the course on a dataset of your own / or solve some related problem using these techniques
- Using a notebook server vs a full linux server
  - the notebook server allows you to get going much faster
  - A full linux server is more ‘your own’ and you get to also practice a bunch of other not-specifically-deep-learning skills along the way
  - With the [fastsetup](https://github.com/fastai/fastsetup) library, Jeremy has made getting going with an EC2 instance pretty easy.
  - the video spends a fair amount of time showing how to do this with Colab Noteboks and a AWS EC2 instance. Refer to the FastAI website and the full video for more details.
- Get better as a developer
  - just doing the course, you’ll also work on your development skills along the way
  - Two important things to do to help with this:
    - Read a lot of code
    - Write a lot of code
- Start with a simple baseline & get a basic end-to-end solution up and running
  - When you’re working on a project, it’s a really good idea to start with a naive / super-basic baseline so that you know whether you’re making progress or whether you’re achieving anything with the work you’re doing.
  - Successful ML projects that Jeremy has seen start with the simplest possible end-to-end solution and then incrementally grow from there.
  - The work of getting your pipeline working / your data imported etc will take a bit of time, and if you get that all sorted upfront it’ll help you focus on the actual work you want to be focused on.
- (At some point during the course) join a [Kaggle](https://www.kaggle.com) competition and make a serious attempt to do your best
  - just getting a model on the leaderboard tests your knowledge and your skills
  - just work regularly on things, show up every day, try to make your model a little better each day
  - Do these things:

[![](images/2021-05-27-fastai-lesson-zero/ff44b78fb0ed_ScreenShot_2021-05-27_at_12.40.27.avif)](https://twitter.com/radekosmulski/status/1334490647986905089)

- For getting a job in the space
  - having a public-facing portfolio of writings and projects will take you a really long way
  - Some companies are more interested in people having the right credentials etc and will never choose you.
  - Startups are a great place where this matters less.
- Try to take the [second course](https://course19.fast.ai/part2)
  - The first course gets you going as a practitioner of deep learning, but the second course allows you to implement algorithms and models from scratch and digs far more into the depths of the subject.
  - Jeremy wishes more people would take part two + encourages them to do so.
- The [`fastsetup`](https://github.com/fastai/fastsetup) library is great for installing everything on a Ubuntu machine (like an AWS EC2 instance)
- Experiment tracking software
  - The two big players are [TensorBoard](https://www.tensorflow.org/tensorboard/) and [Weights & Biases](https://wandb.ai/).
  - Jeremy doesn’t use these. Finds it too tempting to spend your time watching your models train instead of doing something else that is probably more valuable.
  - There are some cases where it might help to use this software.
  - [Weights & Biases](https://wandb.ai/) seems like a good company to work for & they’ve hired FastAI grads in the past.
