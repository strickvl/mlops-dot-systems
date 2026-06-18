---
author: Alex Strick van Linschoten
categories:
  - agents
  - llms
  - reinforcement-learning
  - isafpr
  - agentic-rl
date: "2026-06-18"
description: "A plain-language walk through Group Relative Policy Optimisation — baseline, advantage, and how a group of attempts becomes one weight update — with a runnable toy loop."
layout: post
title: "GRPO without the maths: how an RL trainer nudges the weights"
toc: true
draft: false
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

So far we've been looking at the high-level processes and components of reinforcement learning for agents, but I just finished learning about how the trainer / training process works and wanted to give some thoughts on that.

## GRPO Explained

Group Relative Policy Optimisation (GRPO) is the algorithm that's commonly used by the trainer component to nudge the model (aka 'policy') in the right direction during the training process. Last time I was [focused on how to put together a good reward function](https://alexstrick.com/posts/2026-06-17-rl-terms-rewards.html) but now we're interested on how you use those rewards to update the weights such that it improves the scores next time we attempt to answer the question / solve the problem.

With GRPO, the high-level idea is fairly easy to understand. We attempt the same problem a few times and then we compare between the results to see which ones did better than the others. Based on the best ones of the group, we can update the weights to behave a bit more like those ones. What does this mean in practice and what are the terms of art here?

- 'the baseline' -- this is the average score for all the attempts or rollouts that were attempted. So if this happened 8 times, then we'd add up all the scores and then divide by 8.
- 'the advantage' -- for each attempt, calculate the distance from the baseline value. For some of them we might be above the baseline so we'd have +0.5 advantage, for example. But for others, we might not have performed so well so we'd be below the baseline (`-0.3` e.g.).

During the training process we want to reward positive advantage. So we'd update the weights sufficiently (by some learning rate, just like in 'traditional' machine learning) a little bit such that we are hopefully more likely to see similar behaviours and performance.

Here's a simplified version of that training process in sort of pseudocode:

```python
def step(probs, scores):
    # 1. sample a GROUP of attempts from the current policy
    idxs = random_choices(range(3), weights=probs, k=8)
    # 2. score each attempt
    rewards = [scores[i] for i in idxs]
    # 3. baseline = the group average   ("good compared to what?")
    baseline = sum(rewards) / len(rewards)
    # 4 + 5. advantage = reward − baseline; nudge each sampled answer by it
    for i, r in zip(idxs, rewards):
        probs[i] += 0.15 * (r - baseline)   # >0 push up · <0 push down
    return normalize(probs)            # keep them a valid prob. distribution
```

I put a runnable version of this which you can use to [play around with the parameters here](https://gist.github.com/strickvl/fc7f1f209cbfb4f5fe4f54357dc02884). You can run it with `uv` easily and see how things change when you update various values.

I made a little video where I walk through how the scoring is calculated and how it works in the trainer (at a very high level):

{{< video https://www.youtube.com/watch?v=MGTbzOyUn7E >}}


## Credit Assignment

This is a term of art relating to how the trainer works. When you think about a relatively simple process, usually it might be clear where an agent did something well or when it did something bad. If we had an agent that was meant to review code, but somewhere in the middle it started reading recipes and fan fiction then we might be able to confidently state that  at step number `x` things started to go off the rails.

But when we have a long-running task where the result is much more qualitatively graded ("Write a good research report about some topic" or something like that...) then it's often going to be hard to specify when this happened.

For GRPO, the advantage is that the algorithm doesn't care. It grades you for the whole attempt and not the specific moments during the attempt. So if you got to the result but maybe you did some stupid reasoning or exploration at the beginning, GRPO doesn't care so much or doesn't necessarily make it less likely that we'll see the bad behaviours after training. This can make it less suitable for long-running agents or things with many steps in the trace / trajectory.

## PPO vs GRPO for long-running tasks

Actually there seems to be a really interesting fork developing around exactly this kind of agentic task. Yesterday saw the release of GLM-5.2, a new model from z.ai and they published a [blog about the training process](https://z.ai/blog/glm-5.2) that included the following observations:

> "For GLM-5.2, long-horizon tasks produce substantially longer execution traces, and once a super-long trajectory is split by compaction into multiple sub-traces, different rollouts under the same prompt yield different numbers of trainable traces with highly variable lengths. We therefore move from group-wise optimization to a critic-based PPO formulation that learns from individual rollouts, relying on a critic to estimate token-level advantages rather than group-relative comparisons. This single-rollout formulation fits compaction naturally, as it places no constraint on how many traces a prompt produces or on their relative lengths: we bring compaction into training by including all compacted sub-traces as trainable trajectories, and apply a token-level loss to address their length imbalance."

PPO is something we haven't talked about yet, but it's sort of the earlier algorithm used for training RL that was superseded by GRPO.

For PPO (Proximal Policy Optimization), we use a coach (model) which we ask to predict how well it thinks our agent will do. We actually have this coach or critic model do this at fine-grained intervals while it is working. So at the beginning maybe it might think that the agent has a good chance of solving it, but then after it sees it working a bit then it downgrades its chances and so on. And then the learning signal is basically what happens when the agent continues its work. So if the critic model predicts that it only has a 30% chance of success for our agent, but it actually gets a score of 60% or it outperforms somehow, then obviously we'd consider this to be a result worth updating the weights for. In other words, there is some behaviour in the attempt that just happened which we want to learn from.

The advantage of the PPO approach is that we get to learn from the whole journey of how an agent reached its answer (good parts and bad), whereas unfortunately the fact that we have to train and maintain a whole second critic model is obviously going to take time and experience and it's hard to get that right.

So it's really interesting after what I believe is a good amount of time (a little over a year?) where GRPO really ruled the waves, now we're finding that actually maybe PPO had some advantages that we want to use because many labs building models are interested in these long-horizon agentic tasks.

For my purposes, something like the work on [hinbox](https://github.com/strickvl/hinbox/) is also a long-horizon task with many parts to it, so it might be the kind of thing I'd consider when working on that.

I also saw that there's a paper from this year (["Learning Without Critics? Revisiting GRPO in Classical Reinforcement Learning Environments"](https://arxiv.org/pdf/2511.03527)) where some researchers seem to have shown that the critic model approach is actually *necessary* for long-horizon tasks. In other words, you can't just use GRPO if you have these tasks which require many steps to accomplish. This is obviously an important thing to understand about agentic RL. If your task is short enough, then maybe you can get away with GRPO, but as the horizon extends then in order to escape a performance ceiling you'll have to try other techniques and algorithms for updating the weights.

## GRPO and trainer algorithm intuitions

As you saw in the video above where I walk through some toy simulations, it seems clear that there are some things you have to watch out for when training with RL:

- how many steps are involved in the task? (This relates to the GRPO vs PPO debate. You might find you hit a ceiling with GRPO for long-horizon tasks.)
- how easy are the tasks? (If the tasks are too easy, then maybe all the attempts might give the same reward/score, and then there's no advantage which means there's no signal to update the weights. In the end, your model might just not learn anything.) This is also, I think, why you see people at the big labs tweet some version of "you'll be surprised by how good we made our new model! throw your hardest problems at it" whenever a new model drops. On the surface it's a boast ("our model is better than you think"), but it's also self-interested: the problems a model only sometimes solves are exactly the high-signal examples they need to keep training on for their next iteration. A task everyone's model already nails teaches nothing. It has no spread between the scores so that means there's no advantage; a task right at the edge of current ability is gold!
- Look at the traces! I think when you're doing RL it probably is really important to sample in the comparison between attempts on the same task. You might notice that either the scores don't match your intuition for what answers should be given, and you also might find out that there's some reward hacking going on or other strange behaviours. I'm really curious what people use to do this in real-world scenarios. Is it just `wandb`-type tools or do people have custom interfaces (for long agentic traces etc) or are they using agent-specific tracing tools?
- Are the scores too high? In general, if your agent is scoring 100% on every single answer as given by your reward function, then this might just mean you have a very simple task, but it also might be cause for concern as your reward function might be measuring the wrong thing and so on. So in general be suspicious of perfect scores always!

## Questions

As always, I have some questions at this point in my study!

- I may have written about this yesterday as well, but I'm really wondering when to use RL vs SFT? What are the calculations and thresholds? Is it when you have a certain kind of data? Or is it more the problem shape / type recommends it and you to RL? (Obviously the cost dimension also is part of the discussion.)
- How to handle systems with many models? RL helps you improve and iterate around one model, but what if an agent uses many models? (Or perhaps many models in some multi-agent scenario?) Do we just fix everything in place apart from one of the models and then we improve that one first?
- Are there other algorithms (aside from GRPO and PPO) being used out in the world? What are the tradeoffs or advantages of using those ones? I guess looking at what the frameworks support is an easy way to see what people are using! When would you use those other models?
- What's the timeline for all this? When was GRPO released, when was PPO released? When were they both popular and adopted into the mainstream? Were they being used (or ever used?) in the frontier labs? Are there other special tricks that the labs seem to have that aren't represented by things like GRPO and PPO?
- Is there any advantage to something like curriculum learning for RL? Where you start with either the hard tasks or the small ones, or you interleave the tasks or something like this?