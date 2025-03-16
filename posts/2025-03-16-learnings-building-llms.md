---
author: Alex Strick van Linschoten
categories:
  - claude
  - llm
  - llms
  - miniproject
  - openai
  - prompt-engineering
  - softwareengineering
  - tools
date: "2025-03-16"
description: "Insights from a week of building an LLM-based knowledge database, highlighting experiences with local models, prompt engineering patterns, development tools like Ollama and RepoPrompt, and software engineering principles that enhance AI-assisted development workflows."
layout: post
title: "Learnings from a week of building with local LLMs"
toc: true
image: "images/learnings-building-llms/cover.png"
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

I took the past week off to work on a little side project. More on that at some point, but at its heart it's an extension of what I worked on with my translation package [`tinbox`](https://mlops.systems/posts/2025-02-16-tinbox:-an-llm-based-document-translation-tool.html). (The new project uses translated sources to bootstrap a knowledge database.) Building in an environment which has less pressure / deadlines gives you space to experiment, so I both tried out a bunch of new tools and also experimented with different ways of using my tried-and-tested development tools/processes.

Along the way, there were a bunch of small insights which occurred to me so I thought I'd write them down. As usual with this blog, I'm mainly writing for my future self but I think there might be parts that are useful for others! Apologies for the somewhat rushed nature of these observations; better I get the blog finished and published than not at all!

## 🤖 Local Models

During this project, I experimented with several local models, which continue to impress me with their evolving capabilities. The recent launch of `gemma3` was particularly timely - I found myself regularly using the 27B version, which performed admirably across various tasks.

There are three or four models I keep returning to. `mistral-small` stands out
as an exceptional model that's been relatively recently updated and seems a bit
underrated / underappreciated. The original `mistral` model continues to hold up remarkably well, particularly for structured
extraction tasks and general writing needs like summarization.

One important realization when working with real-world use cases: benchmarks can be deceptive. While helpful as general indicators, each model has its own strengths and quirks. Many newer models are heavily optimized for structured data extraction, but their performance ultimately depends on whether their training documents align with your specific use case. It's crucial to test models against your actual requirements rather than relying solely on published benchmarks.

For robust results with local models, I've found that implementing a
"reflection, iterate and improve" pattern significantly enhances performance.
When you need a model to summarize or analyze content in a particular format,
having a secondary model (or even the same model!) review the output against the original prompt
requirements is incredibly valuable. This reviewer model can suggest
improvements to better fulfill the original request. Running this loop for 2-5
iterations (depending on complexity) can yield results approaching those of
proprietary models like Claude or GPT-4, which might achieve similar quality in
a single pass. For local deployments, this iterative improvement pattern is
essentially non-negotiable.

I also explored vision models, particularly `llava` and `llama-3.2-vision`. These were my primary tools for extracting context from images, generating captions, and analyzing visual content. Their effectiveness varies based on content type and language, but they represent impressive capabilities that can run entirely on local systems.

A significant portion of my work involved non-English languages, including some relatively rare ones. This is another area where benchmark claims about supporting "hundreds of languages" often don't align with real-world performance. Models might list impressive language coverage in their specifications, but actual proficiency varies dramatically. It reinforces my earlier point - always verify benchmark claims against your specific use case before committing to a particular model.

## 💬 Prompting & Instruction Following

Working extensively with various models during this project reinforced some fundamental insights about prompting that might seem basic, but prove critical in practical applications. These observations are particularly relevant when working with local models, though they apply to cloud-based systems as well.

Context matters significantly more than we might assume. While we've grown accustomed to proprietary models like Claude or GPT-4o performing admirably with minimal guidance, local models require more deliberate direction. The more relevant context you can provide (within reasonable token limits), the better your results will be. If you would naturally provide certain background information to a human performing the task, make sure to include it in your prompt to the model as well.

Another key insight: every model has its unique characteristics. Techniques that work brilliantly with one model might fall flat with another, especially in the local model ecosystem. They each require slightly different prompting approaches, specific phrasing patterns, and tailored guidance. This necessitates running small experiments to understand how different models respond to various prompting styles. It's still more art than science, but this experimentation phase is crucial when implementing local models effectively.

Perhaps the most valuable lesson I rediscovered is that breaking complex tasks into smaller components yields superior results compared to using a single comprehensive prompt. This is particularly true with local models. When performing extensive data extraction or when dealing with structured data where the extraction targets differ significantly from each other, don't expect the model to handle everything in one pass – even a human might struggle with such an approach.

Instead, break down the task into logical components, create targeted mini-prompts for each aspect, and then recombine the results once all the separate LLM calls are completed. Yes, this approach adds processing time and complexity, but the quality improvement is well worth the trade-off. When accuracy matters more than speed, this decomposition strategy consistently delivers better outcomes.

## 🧰 Process & Tools

My development environment during this project provided plenty of opportunities
to evaluate various tools and workflows. As context, I primarily work on a Mac
while maintaining access to a separate (local) machine with GPU capabilities for more
intensive tasks. This setup allows me to flexibly experiment with both local and
cloud-based models.

For managing local models, [Ollama](https://ollama.ai/) continues to be my go-to solution for downloading, running, and interfacing with these models. A recent discovery that significantly improved my workflow is [Bolt AI](https://boltai.com/), an excellent Mac interface that provides seamless switching between local Ollama models and cloud-based alternatives. If you're working in a hybrid model environment, Bolt AI is definitely worth exploring.

I've also recently integrated [OpenRouter](https://openrouter.ai/) into my
toolkit, which solves the problem of managing countless API keys across
different inference providers. OpenRouter not only offers native connections to
many cloud providers but also allows you to incorporate your own API keys,
streamlining access to a diverse model ecosystem through a unified interface. It
also helps with setting spend limits on various models or projects.

In terms of development insights, I was impressed by how rapidly front-end
development can progress with the assistance of models like Claude 3.7 and
OpenAI's O1-Pro. These models perform exceptionally well when supplemented with
documentation (such as an [`llms.txt` file](https://llmstxt.org)) alongside your
prompts. While I can't speak to their effectiveness with extremely complex
applications or massive frontend codebases, they demonstrate remarkable proficiency with
small to medium-sized projects.

A significant portion of my experimentation involved
[RepoPrompt](https://repoprompt.com), a tool that recently transitioned from
free beta to a paid license model. RepoPrompt addresses the challenge of getting
your codebase into an LLM-friendly format. Unlike standard CLI tools that simply
export code to clipboard or text files, RepoPrompt generates a structured XML
representation that, when modified by an LLM and pasted back, creates a
reviewable diff of the proposed changes. At least, that's one of the things it
allows you to do! It's actually a bit more powerful / flexible than that and
here's a video so you can see it in action:

[![RepoPrompt Demo Video](https://img.youtube.com/vi/8zIY0zxcafE/0.jpg)](https://www.youtube.com/watch?v=8zIY0zxcafE
"RepoPrompt Demo Video using O1 Pro")

While tools like Cursor and Windsurf offer similar functionality, they tend to become less reliable as project complexity increases. RepoPrompt shines when paired with an OpenAI Pro subscription, enabling effective integration of models like O1 Pro and `o3-mini-high` into your development lifecycle. In my testing, the RepoPrompt + O1 Pro/O3 Mini High combination consistently delivered superior results compared to using Cursor with Claude 3.7 (even with 'Thinking Mode' enabled). Despite the occasional pauses while these models process complex problems, the quality improvement justifies the wait.

Additionally, I continued working with [Claude Code](https://claude.ai/code) and [CodeBuff](https://codebuff.com/), both CLI-driven tools focused on code improvement. Of the two, CodeBuff has become my preferred option. Both tools require careful supervision—I typically keep Cursor open to monitor changes in real-time, occasionally needing to revert modifications or redirect the approach. These tools excel when you clearly articulate your objectives and maintain oversight of the implementation process. CodeBuff particularly impresses with larger codebases and demonstrates superior stability overall.

An interesting pattern emerged during development: whenever files approached 800-900 lines, it signaled the need to refactor into smaller submodules to maintain LLM comprehension, especially when using agent mode in Cursor. The modular approach significantly improved model performance.

I was genuinely surprised by the effectiveness of the RepoPrompt and O1 Pro
combination. For smaller, targeted modifications, CodeBuff continues to
demonstrate remarkable capability. While I didn't evaluate these tools in
conjunction with local models, I suspect such combinations would require more
iterative refinement to achieve comparable results.

## 🧑‍🔬 Software Engineering Patterns

Throughout this experimental project, several software engineering principles proved particularly valuable when working with LLM-assisted development. These patterns aren't revolutionary, but their importance amplifies in the context of AI-augmented workflows.

The principle of simplicity served as a cornerstone approach. Breaking development into the smallest logical next task repeatedly demonstrated its value, especially during the exploratory phases when project architecture was still taking shape. While some engineers might possess the cognitive bandwidth to fully conceptualize complex systems with perfect abstractions from the outset, I've found incremental development leads to more robust outcomes. This approach aligns naturally with how most developers actually think through problems and provides clear checkpoints for evaluating progress.

Data visibility emerged as another critical factor. When leveraging LLM-assisted coding, comprehensive logging becomes even more essential than in traditional development. Strategically placed log outputs create a diagnostic trail that proves invaluable when troubleshooting unexpected behaviors. This practice creates a feedback loop that strengthens both your understanding of the system and the LLM's ability to assist effectively.

A particularly underappreciated practice I haven't seen widely discussed is the importance of dead code detection. When working with LLM-assisted development, code cruft tends to accumulate more rapidly than in conventional programming. Tools like [`deadcode`](https://github.com/albertas/deadcode) and [`vulture`](https://github.com/jendrikseipp/vulture) provide static analysis of Python projects to identify unused functions and variables. Running these tools periodically helps maintain codebase clarity by flagging remnants that might otherwise cause confusion during review. I'm not certain whether newer tools like `ruff` from Astral include this functionality (particularly for function calls), but the capability is invaluable for maintaining a clean, navigable codebase.

Taking time to think offline—away from the keyboard—often yields surprising clarity. This deliberate pause creates space to articulate precisely what you need for the next development increment. When you can express your requirements with precision, the LLM's output improves proportionally. Ambiguous instructions inevitably produce suboptimal results, whereas clarity fosters efficiency.

A final observation worth emphasizing: having experience as an engineer in the pre-LLM era remains tremendously advantageous. When confronting complex workflows involving chained LLM calls with interdependencies and reflection patterns, traditional debugging skills become indispensable. Knowing when to step away from AI assistance and dive into manual debugging with tools like `pdb`, stepping through code execution and inspecting variables directly, represents a crucial judgment call.

LLMs and coding agents often demonstrate a bias toward generating new code
rather than methodically analyzing existing problems. Recognizing the moment
when direct human intervention becomes more efficient than continually prompting
an AI is a skill that comes with experience. Once you've manually identified the
underlying issue, you can return to the LLM with precisely targeted prompts that
yield superior results.

## 🌐 Appendix 1: FastHTML

As a practical addition to my experimentation, I implemented FastHTML for the first time to build a frontend for my knowledge base extraction assistant. The experience was remarkably frictionless, particularly when leveraging their `llms.txt` file—a markdown-formatted documentation set that integrates seamlessly with your frontend codebase when provided alongside prompts.

This approach works exceptionally well with models like O1 Pro or O3 Mini High, creating a development workflow that feels intuitive and responsive. Despite having substantial JavaScript experience from previous roles, I found FastHTML significantly more manageable than complex JavaScript frameworks that dominate the ecosystem today.

The reduced cognitive overhead and natural integration with Python-based workflows makes FastHTML a compelling choice for ML practitioners who prefer to minimize context-switching between languages and paradigms. The framework strikes an excellent balance between capability and simplicity that aligns perfectly with rapid prototyping and iterative development cycles common in ML projects. For those building interfaces to ML systems, it's definitely worth considering as your frontend solution.

## 📃 Appendix 2: OCR + Translation

Another interesting challenge I tackled involved OCR and translation of handwritten documents in non-English languages—a task that proved impossible to accomplish in a single pass with local models, particularly for less common languages.

The solution emerged through methodical problem decomposition:

1. Breaking down PDFs into individual page images
2. Segmenting each page into overlapping image chunks (critical for handwriting where text may slant across traditional line boundaries)
3. Applying OCR to extract text in the original source language from each image segment
4. Using translation models to convert the extracted text to English

This multi-stage pipeline allowed me to overcome the limitations of local models when confronted with the combined complexity of handwriting recognition and translation. Both `gemma3` and `llama-3.3` performed admirably within this decomposed workflow, demonstrating that even resource-constrained local deployments can achieve impressive results when problems are thoughtfully restructured.

This case exemplifies a core principle of effective ML implementation: when
dealing with complex, multi-faceted challenges, breaking them into targeted
sub-problems often yields better outcomes than attempting end-to-end
solutions—especially when working with constrained computational resources.
While this approach may increase processing time, the quality improvement
justifies the trade-off for many practical applications.
