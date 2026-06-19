---
author: Alex Strick van Linschoten
categories:
  - agents
  - llms
  - reinforcement-learning
  - agentic-rl
date: "2026-06-19"
description: "The RL tooling space grows weekly. Rather than memorise frameworks, I read each one against a five-stage mental model — and stay skeptical of what its README claims to do."
layout: post
title: "How to read an RL framework without believing its README"
toc: true
draft: false
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---
I'm mostly through my first pass at understanding the world of agentic RL at a conceptual level. As [a little refresher](https://alexstrick.com/posts/2026-06-16-rl-stages.html), here are the five concepts you really have to have in mind:

1. Tasks – the problems or input that you attempt to solve / handle
2. Harness – the tools you use to attempt to solve the problems
3. Rollout – a recorded attempt of solving the problem (with the full ‘trajectory’ of traces captured)
4. Reward – a score for the attempt (how well did it solve it? which may or may not be whether it was a ‘correct’ answer)
5. Trainer – a way to nudge the model’s weights to achieve higher scores using some algorithm (as of June 2026, this is usually something called GRPO)

Today I want to shift gears to look at the universe of framework and libraries that exists to solve the five areas I just mentioned.

My first observation is that it's a very rich area. It's the kind of richness that people seem to be constantly writing blogs and explainers that help situate readers as to what each framework is doing and what they are concerned with.

As an aside, there are some really useful blog posts that I found helpful when learning about all this, but one of the most notable one is ["The ultimate guide to RL environments: building and scaling them in the LLM era"](https://huggingface.co/spaces/AdithyaSK/rl-environments-guide) (published on Hugging Face by Adithya S Kolavi, Lewis Tunstall, Leandro von Werra, Quentin Gallouédec, Amine Dirhoussi, Ben Burtenshaw and Sergio Paniego). It was written in May so it might even be a bit out of date by now, but it's still worth a read.

## Popular tools

I'm focused on a fairly specific chunk of the RL world, as well, so that narrows it down a little but obviously there is tremendous interest in these techniques at the moment so accordingly there is an explosion of tooling alongside. There's no point exhaustively listing things but some of the popular options include:

- [`verifiers`](https://github.com/PrimeIntellect-ai/verifiers) + [`prime-rl`](https://github.com/PrimeIntellect-ai/prime-rl) -- this is a popular combination of libraries from PrimeIntellect. It covers the full set of tasks from defining the environment to training your model.
- [OpenEnv](https://github.com/huggingface/OpenEnv) -- this was recently [in the news](https://huggingface.co/blog/openenv-agentic-rl) for being backed by Hugging Face and a number of other big names in the space. It is a server that helps glue together some of the components of RL though it is not an all-in-one solution. You still need to bring the actual environment and trainer and so on, but it does coordinate between those.
- [TRL](https://github.com/huggingface/trl) -- Hugging Face's trainer for RL / post-training. Quite popular.
- [Harbor](https://www.harborframework.com/) -- a very popular framework that handles defining the environment and rollout stages, with orchestration of how rollouts get executed on sandbox environments and so on.
- [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym) -- NVIDIA's library for RL environments that connects to the full ecosystem of RL frameworks. It plugs into other libraries (for environments, for training and even for the agent harnesses themselves) and allows you to compose what you need together. It also has an environment hub like that hosted by PrimeIntellect. (It's used by NVIDIA in training their own Nemotron 3 models.)

These are just the ones that seem prominent to me based on my readings, but there are many more. (Even libraries like Unsloth have [serious RL capabilities](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide).)

But how do you navigate all this tooling?

## How to parse the tooling explosion

So far the way I've been doing it so far is to use the mental model of the five stages (see above) and then just figuring out which parts of those are solved by whatever framework we're looking at.

As always, you have to be sceptical of vendor claims. Many of these frameworks will claim that they tackle all or most of the problem space, so you have to look at their SDK, API and docs and see exactly what they care about. Most maintainers don't have time to give equal attention to all of the pieces since there is a lot of complexity going on so you just have to figure out what their core is. Things to look at:

- are there parts of the codebase which receive much less attention and updates?
- who is maintaining or funding the project? (Perhaps if it's an infrastructure provider then they care about the trainer component most? Maybe they're a model builder themselves so they really care about getting good environments?)
- what are the kinds of things they post about online (twitter etc)?

All these things are just signals that allow you to understand where the centre of gravity is. Many of these projects are open-source so there is often activity in many places, but if you follow where the core team's attention lies then that will help you place them into a category.

## Placing NeMo Gym

Let's walk through this process on a framework which I have less experience of, because maybe that helps you understand the process better.

[NeMo Gym](https://github.com/NVIDIA-NeMo/Gym) is a library from NVIDIA that I mentioned earlier. Here's a diagram that's part of their README:

![NeMo Gym product overview diagram](images/nemo-gym-product-overview.avif)

If you take this at its word, you'd think maybe that everything is included. It has agents, models, environments and it's all connected. My first instinct was that this was basically another framework that defines the environment, runs the rollout, scores it like `verifiers`.

But when you think about where the attention actually is, you see that the thing they're talking about a lot is the whole connection ecosystem. So it plugs into other people's environment (Harbor etc), other people's trainers and even other people's agent harnesses like OpenCode. So NeMo Gym allows you to compose these things together, almost like a kind of orchestration for environments and trainers.

So if we place it inside the five categories, it's less that NeMo Gym is just a way to define environments, but rather it's more that it sits across all the stages and allows you to compose various tools together.

If you want to watch me run this same method across each of the popular frameworks, here's a short walk-through:

{{< video https://www.youtube.com/watch?v=qAtJrpsktJk >}}

## Where this leaves me

Now that I have the high level concepts and the critical chops to be able to see a new framework and situate it within my mental model, I'm in a place where I can pick the pieces that I need for what I'm trying to do. This whole project, after all, is focused on taking an agent's logged traces and turning them into a cheaper trained model. Probably my first step for this is going to be to reach for `verifiers` and `prime-rl` and then I'll experiment with other frameworks to have some experience of how they do things.

The bigger point to make, though, and the one I'd heartily endorse for anyone else drowning in the tooling explosion is that you shouldn't try to memorise the frameworks. New software is born every day it seems. Just learn the grid and bring some skepticism and you'll have enough to navigate the space.