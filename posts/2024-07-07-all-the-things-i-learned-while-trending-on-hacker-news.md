---
author: Alex Strick van Linschoten
categories:
  - llms
  - miniproject
  - finetuning
  - isafpr
  - evaluation
  - nlp
date: "2024-07-07"
description: "I was on the front page of Hacker News for my two last blog posts and I learned various things forom the discussion and scrutiny of my approach to evaluating my finetuned LLMs."
layout: post
title: "All the things I learned while trending on Hacker News"
toc: true
image: 'images/isafpr-hackernews.png'
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

My previous two blog posts — [here](https://mlops.systems/posts/2024-06-25-evaluation-finetuning-manual-dataset.html) and [here](https://mlops.systems/posts/2024-07-01-full-finetuned-model-evaluation.html) — were trending / on the front page of Hacker News, driving over 20,000 new visitors to this blog. Welcome! I learned a few new tricks (and some mistakes I'd made) during the ensuing discussion so I thought I'd share some of these here. Some of them might trigger some mini side-investigations into certain hypotheses, too, which is even more exciting. Let's dive in.

## Temperature = 0

Some commenters rightly pointed out that setting the temperature to 1 for some of the OpenAI inference meant that I was more likely to have less stable and less factually consistent responses. I also heard back from the OpenPipe team that there was maybe no hard and fast rule on this but that I should experiment around for my specific use case.

There was enough strongly-voiced opinions on this that I might see if I can rerun the evals using `0` as the temperature to see how much of a difference it makes.

## Function calling vs JSON mode vs prompt vs some schema-forcing library

In [a previous baseline eval for OpenAI's models](https://mlops.systems/posts/2024-06-03-isafpr-evaluating-baseline.html) I used `instructor` to coerce the output into Pydantic objects. [This time round](https://mlops.systems/posts/2024-07-01-full-finetuned-model-evaluation.html) I just used a strongly-worded request in the prompt to request a JSON response and turned on JSON mode (with the `response_format={"type": "json_object"}` passed into the `create` method). That was enough to ensure that [every response I got back was valid JSON](https://mlops.systems/posts/2024-07-01-full-finetuned-model-evaluation.html#json-validity-test).

I've since been reading about the performance differences between these different responses, and how certain models (like the OpenAI GPT class) do much better with function-calling than with just a prompt and/or JSON mode.

I'll be blogging about the differences between these options (and how exactly they work) but I think there's also enough potential here for me to try this as well in a separate round of reruns of the evals.

Specifically: what's the difference in performance between the prompt that I used (which effectively stuffed the schema into the prompt) and using a more formalised function-calling approach? Given what I've read, I suspect function-calling will prove superior, but by how much?

## Llama3 EOS and PAD tokens

I had some helpful comments suggesting there was maybe something untoward going on with these tokens during my Llama3 local finetune. I did set them in my `axolotl` config, but it's well possible that something went wrong there. I'm planning to return to some local finetunes (since my credits on the one-click providers is not infinite and I want to make the local setup work) so I will dive into this soon. Llama3 performed really well so it seems there's just some small bug here.

## The one-click finetuned models can be run locally

I found out that it **is** possible to download the adapters from places like Predibase and OpenPipe and just set things up to run them locally, but it's just buried a bit in the docs (or not documented at all.)

Part of the difficulty with documenting how users can do this is that (thanks to CUDA setup intricacies) there isn't really an easy one-approach-fits-all option. Docker is maybe the closest to this, but at the moment you have to do some of the legwork yourself.

## Others have had similar success with finetuned models

There were a few other links to successes that others had with finetuning models for structured data extraction posted in the HN thread. See [this doctoral dissertation](https://jacobsgill.es/phdobtained). Also [this article in Nature](https://www.nature.com/articles/s41467-024-45563-x). And of course the OG [LoRA Land paper](https://arxiv.org/abs/2405.00732).

## Controversial content means OpenAI tries less hard?

One commenter suggested that the nature of the content might be the reason why OpenAI's GPT performance wasn't as good as the finetuned models. My experience of this is that it's binary — either you get a real response or you get a canned 'this is too sensitive a topic' reply — but (s)he suggested that instead of getting rejected I might just get a degraded-in-quality response.

This would need some further testing to confirm or deny. A nice little experiment for someone.

## What about Anthropic's Claude models?

I should probably have done this as well, but I just hit up against the timebox I allocated for the evaluation work. I'll try to do some experiments with Haiku and the new Sonnet 3.5 to see if a mixture of tool use (aka function calling) and stuffing the prompt with more examples might be able to get us to feature parity with the finetuned models. Watch this space.

## Data labelling issues

One commenter found some inconsistencies in the data labelling around dates. I'll admit to not really having a good answer around this, but also I didn't dive into the issues raised too deeply. They showed some examples of where the 'ground truth' date assigned to a press release was wrong. There's of course the possibility I may have made mistakes while doing the labelling, and there might be some cases where press releases were emailed out earlier than when they were published on the website, but that's much harder to show. I'll dig into this a bit at some point, though this is lower priority on the 'next steps' list.

## You can't predict what people want to read!

The title I chose was clearly designed to be a bit provocative and/or draw readers in, but it wasn't hyperbolic. My evals did actually show my finetuned models 'beating' GPT-4o. That said, [the blog before it](https://mlops.systems/posts/2024-06-25-evaluation-finetuning-manual-dataset.html), setting up the evals I did, was written in a fairly general way and I was really surprised that people enjoyed reading that one so much. It just goes to show that you just need to keep showing up, writing and publishing and you don't know what people will like. Most of the time I'm writing just for me anyway, so anything on top is just a bonus.

Alongside this is the understanding that the things that a Hacker News audience enjoys are not necessarily the same things that the wider world and readership enjoys. That's worth bearing in mind.

## Github Pages hosting holds up!

My blog is [a Quarto blog](https://quarto.org/) hosted on [Github Pages](https://pages.github.com/). As such I don't pay anything for this hosting. I was pleasantly surprised that Github Pages did well in scaling up in response to the traffic. There was no slowness or downtime on the site. Good to know that just because you're using open-source software and free tools that you're not penalised.

## Next Steps

My next effort will be to dive into the deployment side of these finetuned LLMs along with some of the low-hanging fruit mentioned above.