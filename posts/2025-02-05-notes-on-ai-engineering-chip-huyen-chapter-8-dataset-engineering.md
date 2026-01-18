---
author: Alex Strick van Linschoten
categories:
  - books-i-read
  - datasets
  - datalabelling
  - llm
  - llms
  - finetuning
date: "2025-02-05"
description: "Explores Chapter 8 of Chip Huyen's 'AI Engineering,' examining the intricate landscape of dataset engineering through the lenses of curation, augmentation, and processing."
layout: post
title: "Dataset Engineering: The Art and Science of Data Preparation"
toc: true
image: images/ch8-proportions.png
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/posts/2025-02-05-notes-on-ai-engineering-chip-huyen-chapter-8-dataset-engineering.html"
---

Finally back on track and reading the next chapter of Chip Huyen's book, 'AI Engineering'. Here are my notes on the chapter.

## Overview and Core Philosophy

> "Data will be mostly just toil, tears and sweat."

This is how we start the chapter :) This candid assessment frames dataset engineering as a discipline that requires both technical sophistication and pragmatic persistence. While the chapter's placement might have been suitable earlier in the book, its position allows it to build effectively on previously established concepts.

## Data Curation: The Foundation

Data curation addresses various use cases including fine-tuning, pre-training, and training from scratch, with specific considerations for chain of thought reasoning and tool use. The process addresses three fundamental aspects:

> **Data Quality**: The equivalent of ingredient quality in cooking
> 
> **Data Coverage**: Analogous to having the right mix of ingredients
> 
> **Data Quantity**: Determining the optimal volume of ingredients

### Quality Criteria
Data quality encompasses multiple dimensions:

- Relevance to task requirements
- Consistency in format and structure
- Sufficient uniqueness
- Regulatory compliance (especially critical in regulated industries)

### Coverage Considerations
Coverage involves strategic decisions about data proportions:

- Large language models often utilize significant code data (up to 50%) in training, which appears to enhance logical reasoning capabilities beyond just coding
- Language distribution can be surprisingly efficient (even 1% representation of a language can enable meaningful capabilities)
- Training proportions may vary across different stages of the training process

### Quantity and Optimization

A key phenomenon discussed is **ossification**, where extensive pre-training can effectively freeze model weights, potentially hampering fine-tuning adaptability. This effect is particularly pronounced in smaller models.

Key quantity considerations include:

- Task complexity correlation with data requirements
- Base model performance implications
- Model size considerations (OpenAI notes that with ~100 examples, more advanced models show superior fine-tuning performance)
- Potential for using lower quality or less relevant data for initial fine-tuning to reduce high-quality data requirements
- Recognition of performance plateaus where additional data yields diminishing returns

### Data Acquisition Process
The chapter provides a detailed example workflow for creating an instruction-response dataset:

1. Initial dataset identification (~10,000 examples)
2. Low-quality instruction removal (reducing to ~9,000)
3. Low-quality response filtering (removing 3,000)
4. Manual response writing for remaining high-quality instructions
5. Topic gap identification and template creation (100 templates)
6. AI synthesis of 2,000 new instructions
7. Manual annotation of synthetic instructions

Final result: 11,000 high-quality examples

## Data Augmentation and Synthesis

### Synthesis Objectives

1. Increasing data quantity
2. Expanding coverage
3. Enhancing quality
4. Addressing privacy concerns
5. Enabling model distillation

> **Notable Research**: An Anthropic paper (2022) found that language model-generated datasets can match or exceed human-written ones in quality for certain tasks.

Note that some teams actually prefer AI-generated preference data due to human fatigue and inconsistency factors.

### Synthesis Applications
The chapter distinguishes between pre-training and post-training synthesis:

- Synthetic data appears more frequently in post-training
- Pre-training limitation: AI can reshape existing knowledge but struggles to synthesize new knowledge

### LLaMA 3 Synthesis Pipeline
A comprehensive workflow example:

1. AI generation of problem descriptions
2. Solution generation in multiple programming languages
3. Unit test generation
4. Error correction
5. Cross-language translation with test verification
6. Conversation and documentation generation with back-translation verification

This pipeline generated 2.7 million synthetic coding examples for LLaMA 3.1's supervised fine-tuning.

### Model Collapse Considerations
The chapter addresses the risk of **model collapse** in synthetic data usage:

- Potential loss of training signal through repeated synthetic data use
- Current research suggests proper implementation can avoid collapse
- Importance of quality control in synthetic data generation

### Model Distillation
Notable example: BuzzFeed's fine-tuning of Flan T5 using LoRa and OpenAI's `text-davinci-003` generated examples, achieving 80% inference cost reduction.

## Data Processing Best Practices

> **Expert Tip**: "Manual inspection of data has probably the highest value to prestige ratio of any activity in machine learning." - Greg Brockman, OpenAI co-founder

### Processing Guidelines
The chapter emphasizes efficiency optimization:

1. Order optimization (e.g., deduplication before cleaning if computationally advantageous)
2. Trial run validation before full dataset processing
3. Data preservation (avoid in-place modifications)
4. Original data retention for:

   - Alternative processing needs
   - Team requirements
   - Error recovery

### Technical Processing Approaches
Deduplication strategies include:

- Pairwise comparison
- Hashing methods
- Dimensionality reduction techniques

Multiple libraries are referenced (page 400) for implementation.

### Data Cleaning and Formatting

- HTML tag removal for signal enhancement
- Careful prompt template formatting, crucial for:
  - Fine-tuning operations
  - Instruction tuning
  - Model performance optimization

### Data Inspection
The chapter emphasizes the importance of manual data inspection:

- Utilize various data exploration tools
- Dedicate time to direct data examination (recommended: 15 minutes of direct observation)
- Consider this step non-optional in the process
