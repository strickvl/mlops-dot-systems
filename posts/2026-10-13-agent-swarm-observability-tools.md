---
author: Alex Strick van Linschoten
categories:
  - agentic-rl
  - swarms
  - observability
  - agents
  - useful-tools
date: "2026-10-13"
description: "Why agent swarms need observability tools built for them: a 2,000-agent example, the historian's case for treating agent explanations as testimony rather than fact, and a look at what exists so far."
layout: post
title: "Reading the Swarm: Why Today's Agent Tracing Tools Fall Short"
toc: true
draft: false
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
series: agent-swarm-observability
---

Companies at the frontier of model and agent development keep posting about their work on 'agent swarms'. There was the [Hugging Face](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) / [OpenAI incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/), but also [Cursor has written](https://cursor.com/blog/agent-swarm-model-economics), as have [Prime Intellect](https://www.primeintellect.ai/blog/on-the-nature-of-the-swarm). Even Kevin Kelly recently [weighed in](https://kevinkelly.substack.com/p/swarm-intelligence).

I got to wondering a bit about what observability looks like for these agent swarms. You have to assume that the frontier labs doing testing and research work in this area have created their own tools to help them understand how the individual agents / subsystems behave and then also how this contributes to the overall output.

This article, and a few that might follow, are about some questions I asked while thinking through the problem of swarm observability. I'll talk through some UX ideas I had while imagining what the frontier labs have in-house in terms of tools to help them understand their own swarms.

## Why do we care?

Observability is about understanding what the agents are doing in real-time as well as once their activities have completed. The fact that we keep discovering new examples of message boards or other outbreaks by agents who escaped their training / experiment regimens suggests that the labs at least have not solved this problem.

Lots of work is being done on so-called mechanistic interpretability, i.e. the ability to understand why an individual LLM input resulted in a particular output, but it seems we also need an understanding at the agent and swarm level.

I used to be a professional historian, and ever since I read the first 'deep research' report back in early 2025 I've been thinking how much we need better ways of understanding the decisions that went into the outputs that we're reading. With humans, there are usually some conventions around this. For reports, citations help you follow evidence trails and sometimes you can just go ask the author directly. But for some agent-driven report, when understanding why the output maintains one particular claim or drives hard on a certain argument, then you want to be able to trace this back.

Even for a deep research report, it's perhaps within the realms of possibility to actually read through the full evidence trail. You can (sometimes) get a full list of all tool calls that took place, the web searches that were conducted and the URL summaries that were passed into the context for the agent conducting the research. In the past, I've always been surprised at the poor quality of the search results that go into feeding the output. If I was working with someone and I asked them to help write a chapter of a book, I'd be very disappointed if -- when asked about what research work they did -- they showed me the kinds of URLs that OpenAI or Gemini's deep research rely on.

So these multi-agent or highly parallelized research workflows are already hard to fully follow and trace, so how are we going to understand what an agent swarm is doing? We can expect extremely large volumes of text to be generated, more than can be reasonably assumed a human will be reading. So we'll need agents to help understand and parse the swarm's activities and intermediate outputs.

Which brings us to the next question...

## Why would they need special tools / don't they already exist?

Agent observability is a thriving field right now, both open-source and for paid SaaS products. From Braintrust to MLflow to Langsmith to Arize and more, there's hot competition and a blaze of activity. I've tried many of them and even the major players don't seem to have custom interfaces for agent swarms, it seems. Maybe this will come as their customers demand it, but it seems like this isn't on the immediate roadmap.

Swarm observability must be about more than just the LLM inputs and outputs, and the tool calls made. Swarms take place within the context of real infrastructure: filesystems and sandboxes and databases. So when the swarm has access to these things, we need to also have snapshots of how they changed over time as the agent interacted with the infrastructure. In an ideal world, you'd have recorded each atomic moment of change so you could rewind and replay each moment in the swarm's activity. Even better, you could switch out certain parts to see how those changes made a difference.

These interfaces are probably going to have to have strong visual elements to help with the explanations of agent/swarm behaviour. Most likely humans don't need an interface so they can read every single log and subagent output, but if they have questions then there should be ways to surface the most salient information.

Let's take a small imagined example to give you a sense of the complexity of what goes on with an agent swarm. Imagine that 2000 agents migrate a codebase, and at the end a test file is missing.

1. Agent #1412 deleted it. Its record says: "Coordinator told me to remove flaky tests."
2. The coordinator's record says: "Agent #87 reported test X as flaky."
3. Agent #87's record says it ran the test three times and it failed twice.
4. What really happened? Agent #303 was halfway through editing a shared config file at the same moment, so the test read a half-written file. The test was never flaky.

From this we can see how explanations sometimes are cross-agent. We can also -- especially if we used to be historians -- realise that the explanations given by agents should be treated as a kind of testimony or evidence but not fact. Its reasoning might be coherent and plausible, but that doesn't mean that it's not just a realistic story. Actually we're going to need to build the answers to 'why' questions out of evidence and not reports or claims by other agents. I hope it's also clear from even this simple example why humans are not going to be reading raw traces at this scale. They might ask questions (and perhaps not even that often), but they're going to need to rely on investigative agents and their evidence and reports gathering it together.

Now imagine you're looking at the cumulative traces of OpenAI's reported 10,000 agent swarm that [worked on the Navier-Stokes run](https://openai.com/index/navier-stokes-solution/). Not only is there a massive written output, but the output is already probably straining the limits of human comprehension because the topic is inherently complex.

## What are the current options available?

As far as I was able to discover, there are only a few options available as of mid-October 2026:

- LiteLLM recently launched [Lens](https://www.litellm.ai/blog?post=litellm-lens-launch), a product that helps launch investigations across your swarm traces. Built together with MindFort.
- [AgentProvenance](https://github.com/ByteYellow/AgentProvenance) is a layer that tracks "what the agent was asked to do, what its tools reported, and what happened in the operating system". You can then use agents to inspect the evidence graph.
- [AgentSight](https://github.com/eunomia-bpf/agentsight) offers similar capabilities, connecting the standard LLM + tool-call traces to what has happened on the underlying machine.

Most of these looked and felt like engines to power the recording of agent and swarm behaviour, but none of them looked like they offered much in the way of an interface or visual methods of interpreting and understanding.

In my next post I'll get into the kinds of evidence you'd expect to be captured by a swarm observability tool, and think through some of the options for capturing that evidence. I'll also run through some of the common questions that practitioners ask of their swarms and their outputs. These three things can help build up the outline of what a useful interface might contain.
