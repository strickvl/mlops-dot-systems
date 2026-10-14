---
author: Alex Strick van Linschoten
categories:
  - agentic-rl
  - swarms
  - observability
  - agents
  - useful-tools
  - linux
date: "2026-10-14"
description: "What people actually ask about their agent swarms, what evidence a recorder needs to capture to answer them, and some first ideas (FUSE, eBPF, Tetragon) for capturing it."
layout: post
title: "What Does a Swarm Recorder Need to Capture?"
toc: true
draft: false
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
series: agent-swarm-observability
---

[Yesterday](2026-10-13-agent-swarm-observability-tools.md) we covered the problem at a high level. Today I thought we could talk about:

- common questions that people ask of their swarms and their outputs
- the kinds of evidence that you'd expect to be captured by a swarm observability tool
- some options for capturing that evidence

For all of this I can't give a strong answer as to exactly what's going on inside the companies who actually have really large swarms operating at scale right now. We have some evidence from the few blog posts and vague comments on Twitter that some employees have made, but it's admittedly not extremely detailed. So for what follows I've used what's out there plus my own logical conclusions and imagination of the sorts of problems that people are facing.

## What questions do people have about their swarms?

Here's a collection of some of the questions that came up in the practitioner accounts I could find:

- Why did two planners produce incompatible designs for the same component? [Cursor]
- Why did one file become a shared dumping ground? [Cursor]
- Why did adding agents mostly add lock waiting rather than useful work? [Cursor]
- Why was the whole system waiting for its slowest worker? [Cursor]
- Why do these components work separately but fail together? [Anthropic C compiler]
- Did the agent's command kill the runner itself? [Anthropic C compiler]
- Did this session fail before the agent could do meaningful work? [Desplega]
- Why did this worker receive this task? [Desplega]
- Was the message actually delivered, or only attempted? [Claude Code agent teams]
- Is this worker idle, stalled or dead? [Gas Town]
- Why did the researcher miss obvious information: the query, the source choice, or a tool failure? [Anthropic Research]
- What happened inside the script that replaced many visible tool calls? [Desplega]
- Is this CPU or memory graph a real problem or a measurement error? [Desplega]
- Did the agent receive the missing information in the first place? [TraceElephant, MAST]
- What was the actual sequence of important actions? [METR]
- Did different instances collaborate, and through which channels? [METR]
- Did agents take steps to conceal what they did? [METR]
- What instructions were agents given, and how did their activity depart from them? [METR]
- Did a mid-run model change, rather than a coordination improvement, explain the change in results? [Extrapolated from OpenAI's Navier–Stokes run]
- Would the same starting state succeed under a different model or harness? [Extrapolated from AgenTracer and Who&When Pro]

## What kinds of evidence are needed?

These questions give hints at the kinds of evidence that are needed from whatever is recording the swarm's activity. We can then think about what kinds of information these questions need and come up with some rough guesses:

| Question | What the record needs to answer it |
|---|---|
| Why did two planners produce incompatible designs for the same component? | Model context, messages, harness decisions |
| Why did one file become a shared dumping ground? | File versions, merges, activity versus progress |
| Why did adding agents mostly add lock waiting rather than useful work? | Locks and claims, resources, ordering |
| Why was the whole system waiting for its slowest worker? | Harness decisions, background jobs, stop reasons |
| Why do these components work separately but fail together? | Transient file versions, environment, test results |
| Did the agent's command kill the runner itself? | Process execution, exits and signals |
| Did this session fail before the agent could do meaningful work? | Lifecycle, startup failures |
| Why did this worker receive this task? | Harness routing decisions |
| Was the message actually delivered, or only attempted? | Message delivery, capture health |
| Is this worker idle, stalled or dead? | Lifecycle, stop reasons |
| Why did the researcher miss obvious information: the query, the source choice, or a tool failure? | Model context, remote tools, memory retrieval |
| What happened inside the script that replaced many visible tool calls? | Execution inside code mode, remote calls |
| Is this CPU or memory graph a real problem or a measurement error? | Resources, capture health |
| Did the agent receive the missing information in the first place? | Model context, messages, compaction |
| What was the actual sequence of important actions? | Process execution, ordering, capture health |
| Did different instances collaborate, and through which channels? | Messages, outside world, follow-the-text links |
| Did agents take steps to conceal what they did? | Process execution versus transcript, off-agent store |
| What instructions were agents given, and how did their activity depart from them? | Model context, messages, human interventions |
| Did a mid-run model change, rather than a coordination improvement, explain the change in results? | Effective model, human interventions, ordering |
| Would the same starting state succeed under a different model or harness? | Environment, replay with stated guarantees |

## Clustering the evidence we need to collect

And then if we cluster all this together, we can start to put together a list of what needs capturing:

| Area | What to capture | What it lets you answer |
|---|---|---|
| Model context | Exact requests and responses; effective model and settings; context compaction and what it dropped | What did the agent actually see, which model was it really running on, and did it ever get the information it needed? |
| Identity and lifecycle | Run, agent, session, attempt, process, call; spawn, restart, exit, signal, out-of-memory kill | Which worker is this, is it alive, and why did it stop or never get started? |
| Execution | Every process that ran; calls made inside code-mode scripts; background jobs, retries, cache hits | What actually ran, including work hidden inside scripts or the background, and did it match what the agent claimed? |
| Files | Reads and writes with content hashes, byte ranges, temporary and half-written versions | What state was each file in at the moment someone read or tested it? |
| Coordination | Locks, claims and merges; message send, delivery and rejection; scheduler and approval decisions | Who owned what, who told whom what, did the message arrive, and why did the work get split up this way? |
| Outside world | Network calls and remote tools; package installs; databases and shared services; effective environment | Did something outside the agents change the result, or carry information between them? |
| Memory | Versions of memory entries; retrieval queries, filters and ranked results | What did an agent know at a given moment, and why did it find or miss something it had stored? |
| Time and order | Recorder sequence numbers; local order per machine; provable happened-before links | In what order did things really happen, and what could have caused what? |
| Evaluation and stopping | Test and verifier versions, inputs and raw results; stop, cancel and budget reasons | Did the work actually fail, was the test wrong, and did the agent finish or just run out of budget? |
| Integrity | Off-agent append-only store; transcript-versus-execution checks; capture-health and drop counters; recorder overhead | Can the record be trusted, and does a missing event mean nothing happened or only that nothing was captured? |
| Humans and resources | Human redirections and approvals; resource contention, throttling, queue waits | Was the outcome caused by the agents, by a person stepping in, or by the machine running short of something? |
| Replay | Historical playback, component re-execution and fresh runs, each with stated guarantees and side effects isolated | Would the same starting point succeed or fail again, under the same setup or a different one? |
| Live response | Alerts and the ability to pause or stop parts of a running swarm | Could anyone have noticed and stopped the problem while it was still happening? |

This list ends up being a sort of feature list for the kinds of tools that I have to imagine exist in some shape or form at the frontier labs and other places where people are doing research into agent swarms. After all, if you don't have ways of capturing all these kinds of data, how can you hope to understand what the swarm got up to?

## How to capture the data?

As for the precise technical means of capturing agent swarm behaviour, here we move into areas where I am less familiar with the solutions.

Some things are obvious. We can use pre-existing solutions for the traditional 'LLM tracing' that you are probably already familiar with. So here we already have a mental model for capturing the LLM calls (inputs, outputs, reasoning, tokens / cost etc) as well as tool calls, subagents and so on.

For the rest, it becomes a lot harder. We need to be doing things like:

- capturing **a log of all processes** that ran in the agent's machine / sandbox. (We need also to be capturing exit codes, stdout, stderr and things like this)
- **file reads + writes**. This can take various forms: snapshots of filesystems, content hashes for each version of a file, matching each read by a process to the file version it saw, and so on.

For the filesystem, we can use FUSE, which is a Linux feature that lets us wire in some custom logic (in our case, logging for the most part) to the actual filesystem. So instead of having the operating system kernel fully take charge of the logic around file handling, we can pass all these operations to some custom code that we write.

There are some other similar options -- [`fanotify`](https://man7.org/linux/man-pages/man7/fanotify.7.html) is one -- but my investigations and searches suggested that sometimes the notifications (i.e. notifications about file actions) can get dropped, especially when the system's under load. It's much harder for the FUSE actions to be bypassed or skipped.

For process logs, this is something we definitely need to keep track of because in the [Hugging Face incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/), agents built a way for them to show one command in the transcript of their activities but a different command actually being executed. When agents are running in [code mode](https://blog.cloudflare.com/code-mode/), you can have many commands being executed that are slightly more hidden away (depending on how you're logging things). The same applies to messages sent between agents. We need to track how and what they are communicating between themselves. (Prime Intellect's [blog on swarms](https://www.primeintellect.ai/blog/on-the-nature-of-the-swarm) suggested that these messages will only grow in volume.)

For watching processes, it seems like [Tetragon](https://tetragon.io/) is a good place to start. It tracks what programs ran, who started them and how they ended. It's an OSS tool from the Cilium project, and it's built on top of eBPF. (eBPF, as I learned this week, is a feature of Linux that allows you -- a little bit like we had with FUSE above -- to load small programs into the kernel and attach them to specific moments, like "a new program is about to start" etc. Each time one of those moments happens anywhere on the machine, the little program runs, notes the details, and passes them out to Tetragon, which turns them into a stream of JSON events.) This is great for capturing places where what the agent claims it ran vs what it actually ran (esp useful in cases of deception) are different.

(Interestingly, when I tried testing a POC version of this out, I was using Modal sandboxes, and it turns out that Modal's VM kernel didn't ship the BTF map needed for me to be able to use eBPF. A standard Ubuntu kernel (just a hosted machine in a different cloud provider) is what I ended up using instead.)

In some ideal world, we are also capturing all this data because it allows us to do things like:

a. Replay: rerun the swarm from a particular point with some small thing changed or tweaked. (Maybe change what model is used, or add some extra instruction or see if an extra bit of context might make a difference)
b. The whole universe of post-training / RL / finetuning / distillation and so on.

All this data should probably live in an append-only store that lives outside the swarm. It should be written by our recording/recorder logic and never directly by the agents. And all the obvious things like taking sandbox failure and respawning of agents into account (since this is a common occurrence). That means keeping track of the agent identities, each session, each attempt and connecting all of the data through explicit links.

I hadn't thought about it, but actually the clocks of all the agents might drift from one another, so instead of trying to fit all events on a global timeline, rather we probably should connect events together by whatever logically and provably makes sense. e.g. if a message was sent from one agent to another, and we track the sending and the receiving on both sides, and the message's hash remains unchanged in between, then this is probably good evidence to know which event happened first. Any events that we aren't able to connect or link then we have to rely on (possibly unreliable) clocks.

## Are we a tracing provider now?

There are even more details I started thinking through at this point, and it started to dawn on me that capturing all of this data was quite similar to what a provider like Langfuse or Braintrust is providing. In reality, we're doing a little bit more, both in terms of the types of events we're tracking as well as the volume. Ours is a bit easier in that we're append-only, but still it can be quite a large flood when the swarm is up and running. I did quite a bit of testing (more in subsequent posts) to ensure that the POC recorder I built could handle a reasonable volume. Specifically, I tested how it held up when 100,000 events were sent at it.

So by now we have a good idea of the kinds of evidence we want to save, as well as how to do it. I've been running some baby swarms over the past few days to test all this out and I'll be sharing some visual ideas for how you might think about representing answers to the questions listed above (or the process of discovering the answers). I also plan on sharing the actual swarm data (traces / process tracking and so on) on Hugging Face as a public dataset because I didn't have much joy so far in finding any other public data sources. More soon.

P.S. If you're working on swarm observability, please do reply to the thread or in the blog's comments. I'd love to hear whether my guesses resonate with your experience.