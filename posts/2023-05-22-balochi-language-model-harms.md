---
author: Alex Strick van Linschoten
categories:
  - balochi
  - nlp
  - balochi-language-model
  - deep-learning
  - ethics
date: "2023-05-22"
description: "The dual-edged nature of developing a language model for the Balochi language, weighing potential benefits like improved communication, accessibility, and language preservation against serious risks such as misuse by state actors for surveillance and power consolidation, and the unintentional promotion of linguistic monoculture."
layout: post
title: "The Risks of Language Models in Minority Languages"
toc: false
image: images/balochi-llm-harms.png
include-before-body:
  '<script defer data-domain="mlops.systems"
  src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

In thinking about my work to put together a language model or some utilities relating to the Balochi language, I thought a fair bit about whether I should even start. At a very high level, we can look at general risks that comes from language models, as highlighted in [the 2022 Deepmind paper](https://dl.acm.org/doi/pdf/10.1145/3531146.3533088) entitled "Taxonomy of Risks posed by Language Models" which covers

> "six risk areas: I. Discrimination, Hate speech and Exclusion, II. Information Hazards, III. Misinformation Harms, IV. Malicious Uses, V. Human-Computer Interaction Harms, and VI. Environmental and Socioeconomic harms" (p.214)

I'll leave you to check out the paper if you wish. I can think of a number of specific risks and harms that could be connected to developing a language model for the Balochi language, most of which relate to state actors and their desire for more power and better surveillance capabilities.

The communities speaking Balochi have historically and currently been subject to more monitoring than many, either from central governments in Iran and Pakistan or from European and American intelligence agencies, for a variety of reasons. In this context, language models can potentially fit into a system which is geared towards maximising power and influence among the powerful, enhancing state control and surveillance. In the longer term — and I haven't seen to much by the way of research on this, but I'm going to take a leap — I can imagine that language models could well have the effect of creating a kind of linguistic monoculture. (Just think about the kind(s) of language that you read in default responses from ChatGPT and extrapolate from there.)

My assumption is that large, well-funded intelligence agencies already have strong capabilities for Balochi. Indeed, Balochi is [one of the language specified as qualifying](https://www.cia.gov/careers/language-opportunities/foreign-language-incentive-program/) for the CIA's 'Foreign Language Incentive Program' that offers cash bonuses for new and current employees with foreign language skills in Balochi. There is almost certainly a team working on — among other things — language models that allows for the better monitoring of communications in the Balochi language. (To get more of a sense of what such models and capabilities might be used for, check out [this article](https://consciousdigital.org/the-nsas-large-language-models/).)

What, then, are the positive uses of such technology? In no particular order, some things I thought of in the context of Balochi:

- disaster monitoring and outreach following natural disasters (NGOs and aid organisations (or even governments) are sometimes blocked by their inability to effectively communicate with those they are trying to help)
- translation and accessibility (heavily caveated, but there is the potential for positive action here as long as technology is responsibly deployed)
- equal access to technologies
- aggregation and summarisation tools
- language models as cultural artifacts (in a context of an incremental cultural erasure)
- enhancing the state of the art when it comes to training language models for low resource languages has the potential to support efforts being undertaken for many other languages
- work done to enhance datasets and the raw materials for language models might potentially be incorporated in bigger efforts by larger organisations (who generally would never think or make the effort to cover a language like Balochi)
- local and/or community ownership of the models (vs that of corporations)
- a way to reverse linguistic monoculture
- probably better results and performance for their specialised tasks than generalised mega-large language models
- (and finally, a cause close to my heart) language models can facilitate language learning by those learning it as a second language.

I don't believe that there's a simple calculation than can be made, putting
potential harm on one side and potential benefits on the other. Given that these
models surely do already exist or are being developed by state actors, I also
don't think it's a matter of staying away from the area entirely. That said, I
do think it's important to have these questions present when doing this kind of
work as well as to involve and work within the context of pre-existing community
efforts. I'll turn to other resources and previous work in my next post to give
a sense of what low-hanging fruit remains for the Balochi language.
