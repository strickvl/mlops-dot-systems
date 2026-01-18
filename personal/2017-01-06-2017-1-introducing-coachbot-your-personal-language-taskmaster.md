---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - tech
  - language
  - productivity
  - languages
  - pythonsideproject
  - coachbot
date: "2017-01-06"
description: "I built CoachBot to solve the choice paralysis I faced when studying intermediate languages—a tool that suggests randomized language-learning tasks based on your current situation and energy level."
layout: post
title: "Introducing CoachBot: Your Personal Language Taskmaster"
toc: true
aliases:
  - "/blog/2017/1/introducing-coachbot-your-personal-language-taskmaster.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2017-01-06-2017-1-introducing-coachbot-your-personal-language-taskmaster/2a7c6225242d_image-asset.avif)

For languages that aren’t new, I often feel like I’m stagnating and get bored when I reach the intermediate levels. This can reflect a lack of materials from which to study (as was the case with Pashto when I first started studying it) or — more commonly — a surfeit of materials. This creates a kind of choice paralysis where the number of options means I’m far less likely to sit down and pick one of them. (In a similar way, I'll sometimes choose not to watch any of the in-flight entertainment because there are too many choices to pick from.)

Studying a brand new language is (almost) always fun: you’re making quick progress, everything is new so you still have that nice-and-shiny feeling, and you feel like you’re really on your way to success. Continuing that study after two to four years of effort is a little harder. Like with any longer-term project, you start having to find ways to remind yourself of why you’re even working on it in the first place. It can often feel like you’ve lost that original magic somehow, even to the extent that you question whether you actually want to learn the language.

It is useful to address some of these issues ahead of time. That way, when you hit a period of less energy or motivation, you have a pre-formulated plan of action (made by you when you weren’t consumed by whatever mood is dominant). For me, this takes the form of making lists of suggestions to my future-self. I have pre-made task lists for:

- When I’m travelling
- When I’m feeling sick
- When I have no time to study
- When I have oodles of time to study
- When I have lots of energy and enthusiasm for learning
- When I have no enthusiasm for learning

Try to have at least 10 or 15 tasks in whatever lists you do end up creating. Maybe save a few pages at the back of your language notebook to list these tasks. This way, you always have them handy. It helps to have a good amount of variety in the tasks you pre-assign to yourself.

I keep lists as described above, but they weren’t as effective as I'd hoped. I’d glance at the tasks, feel only a limited enthusiasm for the options available and then put the list to one side. I needed a different solution.

I happened to be [teaching myself to program/code](https://www.alexstrick.com/blog/?category=Coding) at around the same time, so I thought this might make an interesting practice problem to try to solve. (I was studying [Python](https://www.python.org/) and so I found a way to make a web app that uses that to connect to [Flask](http://flask.pocoo.org/).)

[CoachBot](http://www.languagecoach.io/coachbot) is the free tool I designed to solve the problem of study choice paralysis for language-learners. It’s still only a prototype, but I'm soft-launching it here now since I imagine it might help those reading who are in similar situations.

[CoachBot](http://www.languagecoach.io/coachbot) gives you a task that you can complete within a specific time-frame. If you have only 5 minutes, it'll pick a random task from the database that I curated and wrote myself. Have an hour? It'll suggest a different kind of task. If you don't want to do a particular task that it suggests, just click a button to get a new one.

These are the kinds of tasks I suggest when [working with students one-on-one](http://languagecoach.io/coaching). They’re also the kinds of tasks I had written down in my lists. As of writing, there are 386 unique tasks in the database, which means that the suggestions are far more varied and creative than anything I was previously using.

I’d suggest you use it as follows: if you ever feel like you don’t know what to do to keep going with your language studies, open up [CoachBot](http://www.languagecoach.io/coachbot), pick a time corresponding to your needs and do whatever it tells you to do. When you’re done, make a note of what you did and how long it took in your learning log. Consider doing another session.

I’ve been using this for a few weeks already and can attest to its value. One of the key benefits I’ve found is just in getting started. Sometimes I’ll only need to do a five-minute task before I realise that there was something else that I wanted to read or study and then I’ll get busy working on that.

There are lots of features that I hope to build in for future versions. I want to include user accounts and tracking of how much time you spend on the different tasks. I want to sub-divide by language skill (i.e. which skill is being trained) and eventually to build in some kind of guidance and interactivity to how the tool functions. But for now, use it as it is: get some studying done by outsourcing the choice of what you’ll be studying.

There are more details on [the website itself](http://www.languagecoach.io/coachbot). You can click through to the [project’s roadmap](https://trello.com/b/RVjGqGnV) where you can see an updated version of features coming soon. You can also make suggestions for tasks that you’d like included in the Bot and/or specific features you’d like me to build as part of the project.

*[Special thanks to Alex, Ian, Kevin and Peter for patiently answering my questions while I was building this initial prototype].*
