---
author: Alex Strick van Linschoten
categories:
  - agentic-rl
  - isafpr
  - datasets
  - datavalidation
  - huggingface
date: "2026-06-28"
description: "Before trusting my ISAF press-release dataset to train and evaluate an RL model, I audited its gold labels and found misspelled provinces, ambiguous values where 'unknown' is the honest answer, and a subtle train/test leak. I cleaned it without overwriting the original."
layout: post
title: "Is this data actually good, or does it just look good?"
toc: true
draft: false
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I wanted to write a bit about the status of the underlying dataset we'll use for my first environment / RL training, since as I was getting that together I realised a few things that needed attention and (aside from the heatwave that's addled my brain this past week) that's what I've mostly been busy with since I last wrote.

I'll go through the problems I hit and how I addressed those in the data.

## The answer key is wrong

I noticed while looking at the data that some of the entries had misspelled province names. (As a quick recap, the data consists of press releases and then a bunch of extracted data points derived from the press releases.) So instead of using 'paktia' we saw 197 uses of 'paktya'. When I looked into the values for that 'province' column, I saw actually 38 distinct values and not the 34 I was expecting (i.e. the number of Afghanistan's provinces).

More about the fix for this below.

## Sorting the data by how fixable it is

I split our data quality issues into three tiers:

1. mechanical -- where there's a clear right answer and it's fixable. In the case of the 'paktia'/'paktya' misspelling, a simple lookup table can convert the misspelling into the correct version.
2. judgement -- this is where the dataset curator (i.e. me) brings some judgement and where there isn't necessarily a single right answer. Part of this is driven by what I see the dataset as being used for, and part of it is just my judgement about how I consider it best to represent things. An example of this is that in the 'province' column I found some region descriptions like 'southern Afghanistan'. In these cases, the original press release had *not* specified one province in particular, but it just vaguely referred to the cluster of provinces. One way round it would be to determine that for those cases, you could just assign them as 'Kandahar', or (which is what I chose) you could assign it as 'unknown' since we actually don't know the province in specific.
3. alarm / caution -- here there was no obvious single answer in the value. So as an example of this, some press releases were assigning incidents to multiple provinces (again in an unclear way, whether deliberately obscuring the reality or not is something for a separate discussion). So I had values in the 'province' column like "khost;paktya", and also "???" or "??".

Overall the takeaway here was that you need to separate out the status of fixes and your data so that you can make the right decisions. A blind 'replace-all' will likely result in errors otherwise.

## "Unknown" is a real answer

For some rows where there is either unknown values or ambiguity, it's totally fine to have 'Unknown' as a value. I mentioned above, but if the press releases specifically doesn't mention a province, then we shouldn't guess or assign some certainty to that value if it wasn't there in the original source. At worst this will lead to silent inflation of inaccuracy and also give you a misplaced sense of confidence in the data. It also will be confusing for a model seeking to learn from the data when the 'golden' data assigns some province to a press release where it wasn't warranted to do so.

Note that there's a really interesting (and I think well known?) study from [Northcutt et al (2021)](https://arxiv.org/abs/2103.14749) which looked at this problem and they found that correcting the gold labels of the datasets altered which model 'won' a benchmark.

## Remember to audit all your data

I did a full audit of the data and then remembered that actually this dataset had both a 'train' and a 'test' split in the Huggingface dataset. It turns out that most of the fixes I'd made for the 'train' split also applied to the 'test' set, but there were some other failure patterns which I needed to handle.

## Non-destructive cleaning

Huggingface datasets are just git repositories in the end, so I figured that when I change the dataset, I could just overwrite the 'province' column. After I thought about it a bit more, that seemed like it was needlessly aggressive.

So instead of touching the original `province` column, I've created two new columns which I added to the dataset:

- `province_clean` which contains the new value (post-clean)
- `province_status` which explains whether any transformations etc were applied to the province column during the process.

This way, the audit trail of the data is represented *in* the dataset itself and not just in the git log of changes.

I also added in a `v1` tag to the old dataset before I pushed my changes. I also updated the datacard for the dataset which explained what had changed and why.

## Some final leakage

One of the unique things about the dataset is that there are some press releases where a single text can represent 3 different incidents. So the text doesn't split up the incidents into separate sections, but rather it'll say something like "we made 3 separate attacks last night and we killed 3 people in kandahar and captured 2 in khost... etc". So we have multiple entries in the dataset (one for each entry) but the source text is the same.

This makes it maybe confusing for the model to learn from this, because there are multiple possible outputs for the same text.

This is known (I think?) as ['group leakage'](https://doi.org/10.1016/j.patter.2023.100804). What I did here was to audit cases where press releases existed on both sides of the train/test split. So I was willing to have the multiple outputs from one text, but it wouldn't have been so great to have a press release from one of the training data set to show up in the test set.

An even better solution going forward maybe would be to have the option for the model output to be *multiple* structured JSON objects for each press releases i.e. for multiple incidents, but then we're departing a bit from the original experiment so I would defer that for now.

We also hashed the input/output pairs now and so that gives us some honesty now to show that we're not changing our train/test split or anything like that in order to boost our scores.

=========================

Up next (I hope!) is moving on to finally setting up the reward function and rollout for doing this via a `verifiers` environment...