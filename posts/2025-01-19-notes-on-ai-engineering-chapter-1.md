---
author: Alex Strick van Linschoten
categories:
  - books-i-read
  - llm
  - llms
  - finetuning
  - prompt-engineering
date: "2025-01-19"
description: "A detailed analysis of Chapter 1 from Chip Huyen's 'AI Engineering' book, covering the transition from ML Engineering to AI Engineering, the three-layer AI stack, and modern development paradigms. Includes insights from a study group discussion on enterprise adoption challenges and emerging evaluation techniques."
layout: post
title: "Notes on 'AI Engineering' (Chip Huyen) chapter 1"
toc: true
image: images/aieng1-small.png
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/posts/2025-01-19-notes-on-ai-engineering-chapter-1.html"
---

Had the first of [a series of meet-ups](https://www.meetup.com/delft-fast-ai-study-group/) I'm organising in which we discuss Chip Huyen's new book. My notes from reading the chapter follow this, and then I'll try to summarise what we discussed in the group.

At a high-level, I *really* enjoyed the final part of the chapter where she got into how she was thinking about the practice of 'AI Engineering' and how it differs from ML engineering. Also the use of the term 'model adaptation' was an interesting way of encompassing all the different things that engineers are doing to get the LLM to better follow their instructions.

## Chapter 1 Notes

The chapter begins by establishing AI Engineering as the preferred term over alternatives like GenAI Ops or LLM Ops. This preference stems from a fundamental shift in the field, where application development has become increasingly central to working with AI models. The "ops" suffix inadequately captures the breadth and nature of work involved in modern AI applications.

### Foundation Models and Language Models

The text provides important technical context about different types of language models. A notable comparison shows that while Mistral 7B has a vocabulary of 32,000 tokens, GPT-4 possesses a much larger vocabulary of 100,256 tokens, highlighting the significant variation in model capabilities and design choices.

Two primary categories of language models are discussed:

1. Masked Language Models (like BERT and modern BERT variants)
2. Autoregressive Language Models (like those used in ChatGPT)

The term "foundation model" carries dual significance, referring both to these models' fundamental importance and their adaptability for various applications. This terminology also marks an important transition from task-specific models to general-purpose ones, especially relevant in the era of multimodal capabilities.

## AI Engineering vs Traditional Approaches

AI Engineering differs substantially from ML Engineering, warranting its distinct terminology. The key distinction lies in its focus on adapting and evaluating models rather than building them from scratch. Model adaptation techniques fall into two main categories:

1. Prompt-based techniques (prompt engineering) - These methods adapt models without updating weights
2. Fine-tuning techniques - These approaches require weight updates

The shift from ML Engineering to AI Engineering brings new challenges, particularly in handling open-ended outputs. While this flexibility enables a broader range of applications, it also introduces significant complexity in evaluation and implementation of guardrails.

## The AI Engineering Stack

The framework consists of three distinct layers:

### 1. Application Development Layer
- Focuses on prompt crafting and context provision
- Requires rigorous evaluation methods
- Emphasizes interface design and user experience
- Primary responsibilities include evaluation, prompt engineering, and AI interface development

### 2. Model Development Layer
- Provides tooling for model development
- Includes frameworks for training, functioning, and inference optimisation
- Requires systematic evaluation approaches

### 3. Infrastructure Layer
- Handles model serving
- Manages underlying technical requirements

## Planning AI Applications

The chapter outlines a modern approach to AI application development that differs significantly from traditional ML projects. Rather than beginning with data collection and model training, AI engineering often starts with product development, leveraging existing models. This approach allows teams to validate product concepts before investing heavily in data and model development.

Key planning considerations include:

- Setting appropriate expectations
- Determining user exposure levels
- Deciding between internal and external deployment
- Understanding maintenance requirements

A notable insight is the "80/20" development pattern: while reaching 80% functionality can be relatively quick, achieving the final 20% often requires equal or greater effort than the initial development phase.

## Evaluation and Implementation Challenges

The chapter emphasises that working with AI models presents unique evaluation challenges compared to traditional ML systems. This complexity stems from:

- The open-ended nature of outputs
- Difficulty in implementing strict guardrails
- Challenges in type enforcement
- The need for comprehensive evaluation strategies

## Data and Model Adaptation

The text discusses how data set engineering and inference optimisation, while still relevant, take on different forms in AI engineering compared to traditional ML engineering. The focus shifts from raw data collection and processing to effective model adaptation and deployment strategies.

## Modern Development Paradigm

A significant paradigm shift is highlighted in the development approach: unlike traditional ML engineering, which typically begins with data collection and model training, AI engineering enables a product-first approach. This allows teams to validate concepts using existing models before committing to extensive data collection or model development efforts.

## Discussion summary

The conversation started with a bit on how AI Engineering represents an interesting shift in the software engineering landscape, potentially opening new career paths for traditional software engineers. While developers may not need deep mathematical knowledge of derivatives and linear algebra upfront, there's a growing recognition that understanding how AI systems behave - their constraints and opportunities - is becoming increasingly valuable.

A key tension emerged in the discussion around enterprise adoption. While there's significant enthusiasm around AI applications, particularly on social media where developers showcase apps with substantial user bases, enterprise companies often maintain their traditional team structures. This creates an interesting dynamic where companies might maintain their existing ML engineering teams while simultaneously forming new "tiger teams" focused on generative AI initiatives, leading to organisational friction.

The group discussed how while it's now possible for software engineers to quickly build AI applications by calling APIs, they often hit limitations that require deeper understanding. This raises questions about whether the "shallow" approach of purely application-level development is sustainable, or whether engineers will inevitably need to develop deeper technical knowledge around model behaviour, evaluation, and fine-tuning.

A particularly notable challenge discussed was handling the non-deterministic nature of AI systems. Traditional software engineering practices, like unit testing, don't translate cleanly to systems where outputs can vary even with temperature set to zero. This highlights how AI Engineering requires new patterns and practices beyond traditional software engineering approaches.

The discussion also touched on evaluation techniques, including the use of log probabilities to understand model confidence and improve prompts. This represents an emerging area where traditional ML evaluation meets new challenges in assessing large language model outputs.