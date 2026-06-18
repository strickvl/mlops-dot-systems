---
author: Alex Strick van Linschoten
categories:
  - agents
  - llms
  - reinforcement-learning
  - agentic-rl
date: "2026-06-13"
description: "Why and when you'd train your own model instead of paying for a frontier API: a practitioner's primer on distillation, graded SFT, and reinforcement learning for agents. I also get into some of the costs of this approach."
layout: post
title: "Off the frontier API: distillation, graded SFT, and RL for agents"
toc: true
draft: false
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I’ve been reading about reinforcement learning around the edges for a long while, and recently it seems to be something that you can find people doing in production systems more and more. I thought I’d attempt a bit of directed study and focus on the topic, so what follows is the first in a series of blogs where I capture what I’m learning and how I think about it. As always, these are mostly for myself, but they might serve some purpose for others so I will publish them here as I progress.

## Motivation

There are quite a few reasons why reinforcement learning (especially the parts of this that tie into agents / agent systems) is more on my mind (and that of others) these days:

- an obvious one: [Claude Fable got taken down](https://www.anthropic.com/news/fable-mythos-access) overnight which is a very nice example of a potential risk to a system which depends on frontier models. They might be taken away from you, or they might degrade in ways you can’t control. Also in general, most people would prefer not to be locked in to one single provider or model, even if it does give them superpowers.
- cost: most companies and even individuals who have substantial agent / LLM-driven use cases are finding that costs are rising. Part of this is that they’re just using things more. (I think actually overall, LLM per-token costs are trending downwards, especially when you take into account increased capability and so on). Even if that’s the case, people are still spending more money on these frontier models via the API and these costs are really starting to mount up. Frontier Labs want you to have more and more ambition so you can keep using their services, but it doesn’t always make economic sense to do so.
- privacy: there are some use cases where you just can’t allow your data to travel over the network to OpenAI, Anthropic, z.ai or any other external provider. Think medicine, law or research where you want to be able to guarantee that a third-party doesn’t have access to the data.

In general I just see the interest in this continuing and so it’s worth me investing a bit of time and effort to deepen my experience with it. Having a better sense of the fundamentals will also help me interpret and filter out all the releases, launches and general *noise* that you find these days.

I’ve continue to work on [hinbox](https://github.com/strickvl/hinbox/), which I’ve written about previously [here](https://alexstrick.com/technical.html#category=hinbox), a system that extracts data and builds up a knowledge database around certain domains. I specifically have the example of someone who wants this system to work on private data in mind when I’m building it out. I don’t know yet, but I could imagine that some RL work might help how hinbox works in some way. I hope to explore this over time.

## Starting sources

I’ve read a bunch of things in recent months, but some good ones that stood out to me were:

- [“How to train your goblin”](https://goblins.mchen.workers.dev/) by [Michelle Chen](https://x.com/michellechen) and [Will Brown](https://x.com/willccbb) is a good starting point.
- [“The ultimate guide to RL environments: building and scaling them in the LLM era”](https://huggingface.co/spaces/AdithyaSK/rl-environments-guide) by Adithya S Kolavi, Lewis Tunstall, Leandro von Werra, Quentin Gallouédec, Amine Dirhoussi, Ben Burtenshaw, and Sergio Paniego is also a really great primer in some of the frameworks / environments and tech stack that is used out in the world in May 2026.
- I maintain and curate the [LLMOps Database](https://www.zenml.io/llmops-database) and we have a bunch of case studies where RL is being used in production scenarios. I’ll hopefully get to review some of those as I go and show how the techniques are actually found out in the real world.

## Supervised Fine Tuning (SFT)

Let’s start with finetuning, since it’s [something I’ve written about](https://alexstrick.com/technical.html#category=finetuning) a bunch in the past, notably around the time I took the Maven finetuning course with Hamel and Dan. Back then, the example I worked on throughout the course was a pretty standard structured data extraction task. I even [managed to get my fine-tuned models to beat GPT-4](https://alexstrick.com/posts/2024-07-01-full-finetuned-model-evaluation.html) which I was very happy about at the time.

Structured data extraction -- where we have some unstructured data (a PDF, let’s say, or a newspaper article) and where we want to extract some specific items from a big stack of these PDFs or articles -- is a great use of supervised fine tuning. I chose it because I happened to have manually [annotated a dataset](https://huggingface.co/datasets/strickvl/isafpressreleases) which was quite nice for this purpose. But the process of annotation took me weeks and probably wasn’t even perfect (i.e. mistakes crept in). At a large scale, this approach might not be feasible with human annotators, either because of the time it takes or because of cost.

So supervised fine tuning can seem like a worthwhile choice if:

- you have a narrow use case
- you have lots of labelled data (or an easy way to get it / label it)
- you have suitable pre-trained models that make sense for your specific domain or use case
- you are willing to make the investment in expertise and maintenance (see below for more on this)

## Advanced Structured Data Extraction

But let's think of an advanced case of this. Let's say instead of using SFT to extract the data, you actually now have an agent that reads documents, has some either loosely defined task definition or slightly more structured workflow that it follows to extract the data you need. Usually this kind of thing would be for complex documents like PDFs, or perhaps very long documents. In these cases, your agent might sometimes call out to some database to check facts or spellings or carry out any number of domain-specific behaviours. At this point, SFT is going to be more complex to pull off since there is a lot going on and we might not even be talking about single-model systems any more.

At the same time, your agent-driven data extractor is probably costing you a ton of money. In May 2026, you can probably solve many of your data extraction problems, but can you solve them at scale with millions of documents while not bankrupting your company? That's the real question. The data extraction might not even be core to your business (or research or whatever), and you'd only keep doing it if it is cheap or easy to do so. 

So let's say it's important to the business, you need to keep this same level of complexity of extraction at a similar quality, *but* you are currently paying a ton of money to do it. The use case or need isn't going away, and you may even have an assumption that the scale will grow and you'll have even more demand.

At that point you have a few options to you, but some that I'd like to highlight as credible options would be:

1. You distil a powerful teacher model
2. You take your agent's own production traces, grade them, and use SFT to fine-tune on only the best ones
3. You use reinforcement learning with some scoring mechanism

I think in these blog posts that follow, I'll be exploring exactly what these different options involve, what tradeoffs are associated with them and maybe even practically how you do them.

Let's walk through one by one first, so at least at a high level we know what we're talking about.

### Distillation of a smart teacher

I actually wrote about this in [a book about Deepseek](https://www.packtpub.com/en-lu/product/deepseek-in-practice-9781806020843) which I co-authored. In chapter 10, I show how you can use a powerful so-called 'teacher' model (in this case, Deepseek) to fine-tune a student model (you can use Gemma or one of the Llama models or whatever). Distillation is basically about using a powerful model to label a whole bunch of data that you can use to further fine-tune a smaller model.

So in the example I mentioned above, where you have structured data extraction, you could take a bunch of cases where you didn't have any labelled data and then use the powerful teacher model to give you the labels for that data. The labels that you generate (i.e. the structured data) from the teacher model you then use as extra data with which you can fine-tune a better / stronger model.

To make that concrete, a single training example would look like this. You take a messy document that nobody ever wrote an answer for:

```
INVOICE — Acme Ltd
Date: 02/04/2026
3x widget @ £40.00 ............ £120.00
Delivery ...................... £8.50
Total due: £128.50
```

...hand it to the teacher, and keep whatever structured output it gives back:

```json
{ "vendor": "Acme Ltd", "date": "2026-04-02", "total": 128.50 }
```

That `(document, JSON)` pair is now one row of training data — exactly the same shape as the hand-labelled examples in ordinary SFT, except a model wrote the answer instead of a person. Do this across thousands of documents and you've got a dataset to fine-tune the smaller student on.

The obvious shortcoming of this approach is that you are not actually checking whether the data that gets generated by the powerful teacher model is correct. I suppose you might assume so, but for difficult problems this isn't necessarily the case. Another thing you might notice is that with this approach, even if you had perfectly labelled data being generated (i.e. no mistakes), you'd never be able to surpass the abilities of the teacher model this way.

Note also that it's often against the terms and conditions of frontier model providers to distil their models in this way, so if you get caught doing it you might be banned or have your access removed.

In pseudocode, we can boil down the training loop to something like this:

```python
def training(unlabelled_data, teacher_model) -> Model:
	teacher_labels = label_data(unlabelled_data, teacher_model)
	model = train_model(teacher_labels, pretrained_model)
	return model
```

### Graded answers with SFT

Another option is to use the real traces from your agent (which is running in production with frontier models, let's say) and then to grade the answers. Basically you do some annotation and you pick only the best examples. For structured data extraction it might be fairly easy to arrive at a decision about what constitutes a good answer, but for something like 'writing email replies to angry customers' or something then there might be lots of theoretically ok responses.

So you use your pre-existing traces and you use those as the basis of supervised fine-tuning. This has the advantage of not costing any extra money (the work has already been done) but it does require you to annotate some data, and it also is only going to be as good as the best examples of whatever your current setup allows.

Is this better than distillation? It depends on who's stronger. If your own agent (running on a frontier model) is better than whatever teacher you'd otherwise distil from, then keeping only your best traces wins. But if the teacher is stronger, its outputs can beat your agent's best, so distillation isn't automatically the worse option. And filtering isn't special to this approach: you could just as easily grade a teacher's outputs and keep only the good ones too. The real limitation here is that you're capped at the best your *current* setup already produces, and you might not have enough strong traces to fine-tune on.

In pseudocode, we can boil down the training loop to something like this:

```python
def training(existing_traces) -> Model:
	best_traces = grade_traces(existing_traces)
	model = train_model(best_traces, pretrained_model)
	return model
```

### Reinforcement Learning

Let's maybe start with the pseudocode to understand what happens with RL:

```python
def training(inputs, grading_function) -> Model:
	model = rl_trainer(inputs, grading_function)
	return model
```

So with RL, you have some kind of scoring mechanism or grader which is an unsupervised way of getting some signal out of what a system is doing. Let's make it more specific. In the case of structured data extraction, things we can use to compose together to help score the outputs:

- is the JSON formatted correctly?
- are the outputs within the realm of what is possible?
- let's say two columns need to add up together and be equal to some value.. is this the case?
- do we use strange characters or symbols?
- does the extracted data use words which are not present in the original document?
- and so on...

We can turn those checks into an actual grading function. It takes a document and an attempt, and hands back a score between 0 and 1:

```python
def score(document, attempt) -> float:
	checks = [
		is_valid_json(attempt),  # does it parse at all?
		has_required_fields(attempt),  # vendor, date, total present?
		totals_add_up(attempt),  # do the columns reconcile?
		only_uses_source_text(document, attempt),  # nothing invented?
	]
	return sum(checks) / len(checks)  # 0.0 -> 1.0
```

The thing worth noticing is what `rl_trainer` actually *does* with that function. In the graded-SFT approach above, we graded a *fixed* pile of traces we already had, just once. Here, the trainer scores the model's *own fresh attempts*, generated during training, over and over, and nudges the weights toward the higher-scoring ones:

```python
def rl_trainer(inputs, grading_function) -> Model:
	model = pretrained_model
	for document in inputs:  # no labels, just documents
		attempt = model(document)  # the model's own fresh try
		reward = grading_function(document, attempt)  # score it live
		nudge(model, attempt, reward)  # push toward higher reward
	return model
```

That loop is the whole difference: there are no fixed answers to be capped by, just a score to climb.

So we can get a decent amount of signal from the data even without having a 'golden' or perfectly annotated sample. This signal which we can pass into the reinforcement learning trainer can be enough to incrementally improve results, and can even exceed the frontier model results because of the RL training algorithm/process. (These are details that I don't understand fully yet, but I see this mentioned a lot so I am tentatively assuming that this is the case, proving you set things up in the right way.)

## Costs and benefits

Let's talk about costs, however. The short explanations above may make you think that this is all going to be easy and we should all use reinforcement learning. But there are some real considerations you have to bear in mind:

- it takes time (effectively: money) to develop the expertise to do this reliably well. There are lots of footguns here and you might need several people to manage it.
- there are maintenance costs. No model stays fresh. The moment you stop training it it usually starts degrading (since the world doesn't stop) so if you train it once then usually you have to keep training it (unless it's being used for historical data or something that truly doesn't change).
- there are testing / evaluation costs. This takes time and expertise again to know whether your model or new system is actually as good as your current frontier-model-driven solution.
- you'll probably end up serving your model yourself in-house, which also needs expertise as well as infrastructure costs. At scale, you will need to work to keep costs down and to serve your models efficiently.

You'll also want to consider how large a load you currently have and how consistently large it will remain. Also how stable is the use case. If the load fluctuates a lot and might not exist in a few months, then it might not be worth investing the time and effort to RL your own.

## Comparing the approaches

| Approach | Where the training data comes from | Setup effort & expertise | Cost shape | Ceiling: how good can it get? |
|---|---|---|---|---|
| **Plain SFT** (the baseline) | Humans hand-label every example | Low method, but hand-labelling is the real bottleneck (slow, costly at scale) | High up-front *human* cost; cheap to serve once trained | As good as your labels |
| **Distillation** | A stronger *teacher* model writes the labels | Low–medium: mostly "generate with the teacher, then SFT" | Pay the teacher once to label; cheap to serve. Mind the teacher's ToS | **The teacher** — you approach it, never beat it |
| **Graded / filtered SFT** | Your *own* agent's production traces, keeping only the best | Medium: you need a grader and an explicit quality bar | Data is near-free (already logged); cost is grading + training | Your agent's **best existing** behaviour, concentrated |
| **Reinforcement learning** | Your inputs + a scoring function — no fixed answers | High: an environment, a trainer (e.g. GRPO), and real footguns | Highest up-front *and* ongoing (serving, retraining); pays off at scale | **Can exceed any single model** — but only as far as your reward function is honest |

## Questions

Since this was meant to be an overview, I'd pass right now to just surface the questions which are at the top of my mind:

- What are the tradeoffs when choosing reinforcement learning (beyond what I mentioned above). Are there other things that I haven't thought of that might be great benefits or disadvantages?
- What is the threshold at which point it makes sense to choose RL? Is it purely a cost thing? Or even in a case where you cannot use frontier models (on account of data privacy restrictions, for example), are there cases or moments where / when you might want to still not do RL because it's not a great use case? What are those decisions? (Might be a good case for a flowchart next time!)
- Which parts of RL training are experimental and we don't know how well they work, and which parts are solid choices, dependable etc?
- Which RL paths are ones which are very simple and straightforward to do, and which ones require real expertise (whether engineering expertise or math / hard science expertise)? In other words, if you're a team that doesn't have a big research team then you're probably going to want to choose something as risk-free as possible.
- In the above I mostly was talking about offline RL, but what about online RL? How is this different? Why would one do one vs the other and what are the tradeoffs?
- What are the data thresholds for some common use cases? i.e. for an email support agent or something, how many traces of successful conversations would you need to get good results?
- Are there special ways of evaluating RL-ed models?
- Are there special flavours of RL out in the world that people are experimenting with?
- Is RL the main thing people are putting money and energy into at the moment for these kinds of use cases, or are there other options I haven't mentioned which are promising?
