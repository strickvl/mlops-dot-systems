---
author: Alex Strick van Linschoten
categories:
  - llm
  - prompt-engineering
  - books-i-read
  - evaluation
date: "2025-01-17"
description: "Detailed notes covering Chapters 10 and 11 of 'Prompt Engineering for LLMs' by Berryman and Ziegler, focusing on LLM application evaluation and future trends. Chapter 10 explores comprehensive testing frameworks including offline example suites and online AB testing, while Chapter 11 discusses multimodality, user interfaces, and core principles for effective prompt engineering. Includes personal insights on the book's emphasis on completion models versus chat models."
layout: post
title: "Final notes on 'Prompt Engineering for LLMs'"
toc: true
image: images/chapter-10-prompt-eng.png
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Here are the final notes from '[Prompt Engineering for LLMs](https://app.thestorygraph.com/books/8535f61d-1dcd-4610-9cd9-6bcaf774f392)', a book I've been reading over the past few days (and enjoying!).

## Chapter 10: Evaluating LLM Applications

The chapter begins with an interesting anecdote about GitHub Copilot - the first code written in their repository was the evaluation harness, highlighting the importance of testing in LLM applications. The authors, who worked on the project from its inception, emphasise this as a best practice.

### Evaluation Framework

When evaluating LLM applications, three main aspects can be assessed:

- The model itself - its capabilities and limitations
- Individual interactions with the model (prompts and responses)
- The integration of multiple interactions within the broader application

As a general rule of thumb, you should always track and record:

- Latency
- Token consumption statistics
- Overall system approach metrics

### Offline Evaluation

#### Example Suites
The foundation of offline evaluation is creating example suites - collections of 10-20 (minimum) input-output pairs that serve as test cases. These should be accompanied by scripts that apply your application's logic to each example and compare the results.

Example sources come from three main areas:

- Existing examples from your project
- Real-time user data collection
- Synthetic creation

When using synthetic data, it's crucial to use different LLMs for creation versus application/judging to avoid potential biases.

#### Evaluation Approaches

1. **Gold Standard Matching**
- Can be exact or partial matching
- Particularly effective for binary decisions or multi-label classification
- Can leverage "logical frogs" tricks from Chapter 7 to assess model confidence
- Free-form text requires more creative evaluation approaches
- Tool-use scenarios may be easier to evaluate, especially in agent-driven applications

2. **Functional Testing**
- A step up from unit tests but not full end-to-end testing
- Focuses on testing specific system components

3. **LLM as Judge**
- Currently trendy but requires careful implementation
- Should include human verification loop, preferably multiple humans
- Key insight: Always frame the evaluation as if the LLM is grading someone else's work, never its own
- Recommendations for quantitative measures:
	 - Use gradient and multi-aspect coverage (MA)
	 - Implement 1-5 scales with specific criteria
	 - Place all instructions and criteria before the content to be evaluated
	 - Break down "Goldilocks" questions (was it just right?) into separate questions about whether it was enough and whether it was too much

### Online Evaluation

The chapter transitions to discussing why we need online testing despite having offline evaluation capabilities. While offline testing is safer and more scalable, real human interactions are unpredictable and require live testing.

Key points about online evaluation:

- AB testing is the standard approach
- Existing solutions include Optimizely, VWO Consulting, and AB Tasty
- Applications need to support running in two modes (A and B)
- Consider rollout timing and users on older versions

Five main metrics for online evaluation (from most to least straightforward):

1. Direct feedback (user responses to suggestions)
2. Functional correctness
3. User acceptance (following suggestions)
4. Achieved impact (user benefit)
5. Incidental metrics (surrounding measurements)

Direct feedback data is particularly valuable as it can later be used for model fine-tuning. It's recommended to track more incidental metrics rather than fewer, both for quality indicators and investigating unexpected changes.

## Chapter 11: Looking Ahead

The final chapter covers several forward-looking topics:

- Multimodality in LLMs
- User experience and interface considerations
- Published artifacts from Anthropic
- Risks and rewards of custom interfaces
- Trends in model intelligence, cost, and speed

### Book-Level Conclusions

Two main lessons emerge from the book:

1. **LLMs as Text Completion Engines**
	- They fundamentally mimic training data
	- Success comes from aligning prompts with training data patterns
	- Particularly relevant for completion models

2. **Empathy with LLMs**
- Think of them as mechanical friends with internet knowledge
- Five key insights:
	- LLMs are easily distracted; keep prompts focused
	- If humans can't understand the prompt, LLMs will struggle
	- Provide clear instructions and examples
	- Include all necessary information (LLMs aren't psychic)
	- Give space for "thinking out loud" (chain of thought)

## Personal Reflections

The book, while not revolutionary, provides valuable insights and is a recommended read at 250 pages. It can be completed in about 10-11 days. The heavy focus on completion models versus chat models is interesting, likely due to the authors' experience with GitHub Copilot. While some points were novel, none were completely mind-blowing. The book's emphasis on completion models versus chat models is both intriguing and occasionally confusing, though this perspective is understandable given the authors' background with GitHub Copilot.