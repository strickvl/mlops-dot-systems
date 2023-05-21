---
author: Alex Strick van Linschoten
categories:
  - balochi
  - nlp
  - balochi-language-model
  - deep-learning
date: "2023-05-21"
description: "The Balochi language is underrepresented in NLP. I'm interested in contributing to the field by building a language model for Balochi from scratch and contributing training resources and datasets along the way."
layout: post
title: "Low-resource language models: making a start with Balochi"
toc: false
image: images/starting-balochi-llm.png
include-before-body:
  '<script defer data-domain="mlops.systems"
  src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Large Language Models are all the rage, but what do you do when the language you want to model is essentially unrepresented in the public datasets used for training? I have a few months before the start of my next maths module and I'd like to use the time in part to dive into the ins and outs of training your own language models from scratch.

The language I'm working with is Balochi, in particular the dialect or subset of Balochi that is spoken in southeastern Iran. The parent subgroup of 'Balochi' is spoken by 8-10 million people, but those break down into a few varieties which is in turn driven to a large extent by geography. The kind of Balochi used in Pakistan is subject to different linguistic influences than the one I'm interested in, for example.

Despite the existence of millions of people speaking this language (family), it is more or less unrepresented in benchmarks and so-called breakthroughs in language modelling. Even the raw data to represent the language is absent. Common Crawl, one popular source of data for training language models, [doesn't even include Balochi](https://commoncrawl.github.io/cc-crawl-statistics/plots/languages) as one of the languages represented in its corpus. Moreover, there's no Balochi Wikipedia or anything really like it, so anyone hoping to work on language models in Balochi is first going to have to put together a corpus of data.

There's nothing particularly novel about this problem. Languages with very few resources are known as low-resource languages and there's a whole field of research (and some practice) busy trying to find ways to better serve these smaller language communities. I view the work as valuable, not only in that it seeks to preserve what might otherwise be lost, but also in terms of the disproportionately large (potential) impact it can have.

I have personally experienced this issue at a distance, for the most part, having studied and worked with languages for which there are few study materials. The two languages I was passed down by my parents — English and, to a lesser extent, Dutch — are well-represented in the work and time spent by researchers and practitioners thus far. I have learned languages from neighbouring families, both geographically and linguistically, and always wanted to study Balochi myself. My hope is that it will be a gateway for me into the language and its community of speakers.

I'm quite conscious of wanting to go about this project in a way that is ethical. Work of this kind is too often predicated on a principle of 'take now, ask later' so I'll be writing more about this as I go as well as (hopefully) working with Balochi speakers and researchers to augment the work that is already being done. My initial survey of what has been done so far leads me to think that there is much remaining in the way of low-hanging fruit. I haven't yet come across a Balochi tokenizer, for example, or embeddings or many other things that you would take for granted if you were working with the English language.

My somewhat distant goal — one for which I'm unsure how unrealistic I'm being —
for all of this would be develop models and materials that can aid non-native
speakers of Balochi to learn the language through what is known as
[comprehensible
input](https://www.cambridge.org/core/journals/journal-of-classics-teaching/article/comprehensible-input-and-krashens-theory/2308987050E8D31E3986B530D4B02F6F).
All of which is to say: I don't know much Balochi as I start this work, but I
hope to develop my fluency over time.
