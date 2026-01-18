---
author: Alex Strick van Linschoten
categories:
  - afghanistan
  - coding
  - python
  - research
date: "2018-01-31"
description: "How I tackled fuzzy searching and name matching across multiple spellings, particularly for transliterated Afghan names, using approaches like Levenshtein distance and the FuzzyWuzzy library."
layout: post
title: "Fuzzy Searching and Foreign Name Recognition"
toc: true
aliases:
  - "/blog/fuzzy-search.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Here's something that happens fairly often: I'll be reading something in a book and someone's name is mentioned. I'll think to myself that it'd be useful at this point to get a bit of extra information before I continue reading. I hop over to [DevonThink](http://www.devontechnologies.com/products/devonthink/devonthink-pro-office.html) to do a full-text search over all my databases. I let the search compute for a short while, but nothing comes up. I tweak the name slightly to see if a slightly different spelling brings more results. That works a bit better, but I have to tweak the spelling several times until I can really claim the search has been exhaustively performed.

Anyone who's done work in and on a place where a lot of material is generated without fixed spellings for transliteration. In Afghanistan, this ranges from people's names -- Muhammad, Mohammad, Muhammed, Mohammed etc -- to place and province names -- Kunduz, Konduz, Kondoz, Qonduz, Qhunduz etc.

DevonThink actually has a ['fuzzy search' option](http://www.myproductivemac.com/blog/devonthink-part-6-searching27102015) that you can toggle but it isn't clear to me how it works or whether it's reliable as a replacement for a more systematic approach.

As I'm currently doing more and more work using Python, I was considering what my options would be for making my own fuzzy search emulator.

My first thought was to be prescriptive about the various rules and transformations that happen when people make different spelling choices. The Kunduz example from above reveals that vowels are a key point of contention: the 'u' can also be spelt 'o'. The 'K' at the beginning could also, in certain circumstances, become 'Q' or 'Qh'. These various rules could then be coded in a system that would collect all the possible spelling variations of a particular string and then search the database for all the different variations.

Following a bit of [duckduckgo-ing](https://duckduckgo.com/) around, I've since learnt that there are quite extensive discussions of this problem as well as approaches to solution that have been proposed. One, commonly referenced, is a Python package called '[FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy)'; it uses a mathematical metric called the Levenshtein distance to measure how similar or not two strings are. I imagine that there are many other possible metrics that one could use to detect how much two strings resemble one another.

I imagine the most accurate solution is a mixture of both approaches. You want something that is agnostic about content in the case of situations where you don't have domain knowledge. (I happen to have read a lot of the materials relating to Afghanistan, so I know that these variations of names exist and that there is a single entity that unites the various spellings of Kunduz, for example). But you probably want to code in some common rules for things which come up often. (See [this article](https://www.dawn.com/news/76087), for example, on the confusion over spellings of Muslim names and how this leads to law enforcement mistakes).

I may end up coding up a version that has high accuracy on Afghan names because it's a scenario in which I often find myself, but I'll have to explore the other more mathematically-driven options to see if I can find a happy medium.
