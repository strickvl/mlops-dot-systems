---
author: Alex Strick van Linschoten
categories:
  - agents
  - llms
  - reinforcement-learning
  - isafpr
  - agentic-rl
date: "2026-06-17"
description: "Grounding RL vocabulary — trace, task, environment — and the three families of reward in a real structured-extraction task. With a dirty-gold-label gotcha that argues for looking at your data, composing rewards via gates and weights, and reward-hacking examples from Shopify's Sidekick."
layout: post
title: "Reward design for RL, grounded in a structured-extraction task"
toc: true
draft: false
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

It probably would help to ground our discussion of some of this RL terminology to look at an example. I mentioned that we could use the old ISAF press releases task (structured data extraction) as a starting point, so here is some data from that:

```json
trace = {
    "task_id": "isaf-pr-2011-0487",
    "task": {
        "document": "KABUL — An Afghan and coalition force detained three"
                    " suspected insurgents in Kandahar on 20 Feb 2011...",
        "fields": ["date", "province", "event_type", "detained_count"],
    },
    "steps": [                                  # one {action, observation} per turn
        {"action": {"tool": "emit_answer",
                    "args": {"date": "2011-02-20", "province": "Kandahar",
                             "event_type": "detention", "detained_count": 3}},
         "observation": None},               # nothing comes back; it just answers
    ],
    "output": {"date": "2011-02-20", "province": "Kandahar",
               "event_type": "detention", "detained_count": 3},
    "gold":   {"date": "2011-02-20", "province": "Kandahar",
               "event_type": "detention", "detained_count": 3},
    "reward": None,                          # filled in by score(), next session
}
```

So you can see a few things going on here:

- this is a 'trace', which is the record of what happened when we tried to run our system to extract the data from the press release.
- you can see the 'task' itself embedded within the trace
- you can see in the 'steps' what the system did in order to extract the data (it used the `emit_answer` tool, simply put)
- And you can see that we also have access to the golden annotation which will help us check whether this was correctly extracted.

So let's disambiguate these terms again, as well, for clarity:

- **task**: the input plus how the input will be graded ("extract date, province, event_type, detained_count from this press release" and "you're graded on how many fields match the golden annotation(s)")
- **trace**: a full record of an attempt at a task (including the tool calls used etc)
- **environment**: the task, the tools it's allowed or able to use, and the reward or grading function

RL, it seems, has a LOT of terminology so it's worth just walking through those to make sure we're all talking about the same things.

For our scoring function, a fairly simple version would look something like this:

```python
def score(trace: dict[str, Any]) -> float:
    """Reward for one ISAF trace: did it parse, and do fields match gold?"""
    out, gold = trace["output"], trace["gold"]
    if not isinstance(out, dict):          # didn't even produce a JSON object
        return 0.0
    fields = trace["task"]["fields"]
    hits = sum(1 for f in fields if out.get(f) == gold[f])
    return hits / len(fields)              # fraction of fields correct
```

Now it turns out that even with such a fairly simple way of grading outputs, there can be some interesting results. Here are four pairs of output vs the golden dataset equivalent:

```python
# 1 — clean hit
output = {province: "kandahar", eventtype: "detention", targetgroup: "taliban", minkilled: 0, mincaptured: 3}
gold   = {province: "kandahar", eventtype: "detention", targetgroup: "taliban", minkilled: 0, mincaptured: 3}

# 2 — partial
output = {province: "helmand", eventtype: "airstrike", targetgroup: "haqqani", minkilled: 1, mincaptured: 0}
gold   = {province: "helmand", eventtype: "airstrike", targetgroup: "taliban", minkilled: 2, mincaptured: 0}

# 3 — malformed
output = "I think this was a detention operation somewhere near Kabul."   # a string, not a dict
gold   = {province: "kabul", eventtype: "detention", targetgroup: "taliban", minkilled: 0, mincaptured: 2}

# 4 — dirty gold
output = {province: "paktia",  eventtype: "detention", targetgroup: "haqqani", minkilled: 0, mincaptured: 1}
gold   = {province: "paktya",  eventtype: "detention", targetgroup: "haqqani", minkilled: 0, mincaptured: 1}
```

So for group 1, we score a full 1.0 since everything was correct and it was correct JSON. For group 2, we scored a partial hit since the target group extracted was the wrong one (compared to the golden dataset). For group 3, we score 0.0 because the output was a string and not parseable as JSON. That's known as a 'gate', where we end early and return `0.0` because it doesn't even parse as JSON.

Group 4 is interesting, though, because here you can see that the only difference is the name of the province. Both are actually referring to the same place, only with alternative spellings. What's even more interesting is that the spelling in the golden dataset's version ('paktya') is itself an anomaly or outlier. Out of the 4822 items, 197 of them use 'paktya' as the spelling but the rest use 'paktia'. So actually somehow this is a problem with the original dataset, but probably you're not going to always be able to fix all these at the source, so you have to handle them within the reward.

The decision about how to handle it in the reward function will be made by what your needs are. If 'paktya' is just as legitimate a spelling as 'paktia' for your purposes, then you'd want to rate them equally. If you wanted to incentivise one spelling over another, then you could slightly penalise the agent for having used the spelling that you don't like.

This is a clear argument, by the way, for 'looking at your data'! These kinds of details are things that I imagine add up when you have a more complex agent, and it's quite important to understand exactly how tasks are being graded if you want to have control over how your system is going to be optimised through the RL training process.

## Three kinds of rewards

The `score()` function we used above is an example of the first and most basic kind of rewards, but there are two other categories that are commonly found. Let's walk through them all.

Firstly we have *verifiable / procedural* rewards. This is the same 'verifiable' as is used in the term RLVR ("reinforcement learning with verifiable rewards"). Think cheap functions that are quick to run and where there's an easy way to grade something. Did the JSON parse? Does the response match the correct one in the answer key? Does it pass a basic sanity count? These checks are hard to game or trick, though they still might lead to reward hacking and send your system in the direction of behaviours you don't want to incentivise.

Secondly we have *absolute LLM-as-a-judge*. For this, we pass the task and the response to an LLM and ask it to grade the response. It usually makes its assessment on the basis of a 'rubric' and is often used for things where it's harder to come up with cheap functional evaluations of like we had with as in the verifiable/procedural rewards above.

And thirdly, we have *relative / grouped judge* rewards. For this we aren't making an absolute assessment as in the LLM-as-judge example. Instead, we make multiple attempts (four, or ten, let's say) and then we use an LLM judge to just rank them or pick the best ones. This way we're not necessarily saying that the best ones are perfect, but we do give signal that these best ones were good so steer the model/policy in that direction, and that the bad ones were bad so steer the model *away* from those kinds of responses.

For our ISAF examples above, a simple procedural test could look like this:

```python
# The canonical 34 — the authoritative external reference, NOT derived from the gold column.
# (Deriving from gold would bless its dirt: the gold column carries junk values —
#  misspellings, regions like "southern afghanistan", multi-value cells — that aren't real provinces.)
KNOWN_PROVINCES = {"badakhshan", "badghis", "baghlan", "balkh", "kabul",
                   "kandahar", "khost", "kunar", "paktia", "paktika", ...}  # 34 total
ALIASES = {"paktya": "paktia", "nimroz": "nimruz",
           "dai kundi": "daikundi", "sar-e pul": "sar-e-pol"}

def _canon(p):                       # lower, strip, then de-alias
    p = p.strip().lower()
    return ALIASES.get(p, p)         # map a known misspelling, else leave it

def reward_field_match(pred, gold):   # does it match the gold answer?
    return 1.0 if _canon(pred) == _canon(gold) else 0.0

def reward_province_exists(pred):     # source criticism: is it a REAL province at all?
    return 1.0 if _canon(pred) in KNOWN_PROVINCES else 0.0
```

So here we have tests for whether we have a match *and* a sanity check for whether the province exists at all. Without the check for whether the province exists at all, we could conceivably start rewarding the model for producing provinces that don't exist but that seem plausible. So you actually need both tests to ensure that the model learns to emit real provinces as well as the right provinces (based on the logic that's part of the extraction task).

You can of course compose these together. You can use some checks as a simple gate. The JSON parsing one above is a good example of this. There's no point even using an LLM judge to check whether the extraction matched the input press release because improper JSON formatting makes the answer a non-starter.

You can also weight the parts of a reward function together. Maybe you assign 30% of the weight to procedural checks and 70% to whatever the value the LLM judge comes back with. In reality, these kinds of compound reward functions are what's found in production systems.

## Reward hacking side-quest

I also took a look at [a case study from Shopify](https://shopify.engineering/building-production-ready-agentic-systems) around their Sidekick agent system. (There's also [a video here](https://www.youtube.com/watch?v=xFW-oCpLa3w).) It has a few interesting examples of some reward hacking that they encountered when using RL on their agent traces:

```
The model found creative ways to game our reward system:

- Opt-out hacking: Instead of attempting difficult tasks, the model would explain why it couldn't help
- Tag hacking: Using customer tags as a catch-all instead of proper field mappings
- Schema violations: Hallucinating IDs or using incorrect enum values

For example, when asked to "segment customers with status enabled," the model learned to create filters like customer_tags CONTAINS 'enabled' instead of the correct customer_account_status = 'ENABLED'.
```

As you can see, some of these are fairly subtle and I'm curious how they caught these. It seems that they had some automations / evals to help understand what was going on, but I imagine that they must also have been looking at the data during the process.

## Catching half-errors

The examples above are fairly simplistic, but you can imagine that there are scenarios where you have to think carefully about exactly what behaviours you want to reward. For example, think about whether it's worse to miss a field in a response, or to invent one? If a completely hallucinated value is worse than missing a field, then you'd want your reward function to punish those false values more than missing fields. And then if "I don't know" is safe as an answer you can tolerate blank values.