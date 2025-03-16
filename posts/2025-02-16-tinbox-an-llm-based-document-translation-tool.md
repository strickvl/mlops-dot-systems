---
author: Alex Strick van Linschoten
categories:
  - translation
  - llm
  - llms
  - languages
  - research
  - miniproject
  - python
  - tools
date: "2025-02-16"
description: "Explores an open-source tool I built that tackles the challenges of large-scale document translation using LLMs. Born from my experience as both a historian working with Afghan primary sources and a developer, it offers innovative solutions to common translation problems through smart chunking algorithms and local model support, making multilingual content more accessible for researchers and developers alike."
layout: post
title: "Tinbox: an LLM-based document translation tool"
toc: true
image: images/tinbox-gh-small.png
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Large Language Models have transformed how we interact with text, offering capabilities that seemed like science fiction just a few years ago. They can write poetry, generate code, and engage in sophisticated reasoning. Yet surprisingly, one seemingly straightforward task – document translation – remains a significant challenge. This is a challenge I understand intimately, both as a developer and as a historian who has spent years working with multilingual primary sources.

Before the era of LLMs, I spent years conducting historical research in Afghanistan, working extensively with documents in Dari, Pashto, and Arabic. This wasn't just casual reading – it was deep archival work that resulted in publications like ["Poetry of the Taliban"](https://www.amazon.com/Poetry-Taliban-Columbia-Strick-Linschoten/dp/0231704046?dib_tag=AUTHOR&ref_=ast_author_dp_rw&dib=eyJ2IjoiMSJ9.1mVaySVqbTMQoyHNw9jr729HdyTrJqF63q_dK--vp8ZIMJilxU2L9GFro0SDlAHwkLCNvm6uzLyUFyfhIMgnqHsy6OcH29oAJydmPZBO_nk.1ryRpL7upcac5fthUBd3TPVG15nuXehSARppPP0GLz8&tag=soumet-20) and ["The Taliban Reader"](https://www.amazon.com/Taliban-Reader-Islam-Politics-their-ebook/dp/B07F37SB8S?sr=1-1&qid=1739727492&keywords=taliban%2Breader&sprefix=taliban%2Breader%252Cdigital-text%252C182&tag=soumet-20&dib_tag=se&crid=1YY9Y6SJN9YLO&dib=eyJ2IjoiMSJ9.rJDPRcIzPe3NY83zHYXFevNXoERWWiJ6BTyj9SXHYfv_jixdQKUV27Qwh1NJYX0qMhAV02Z4r75o_tYUCysq_Obf_9wo3qk9AzLlZWyTWO-dSa88xUIQP3MCe9dgIUf2Okhj6DAyqjgHQDdgrivgTmN0eJNQ_IOp2MKhnWLbOpEcdZtxrI7VisVAITML4b4dwYyjKbfbKnsk1IHWtk_P0NU-XcV2ChEHBcbqlx3jh4OvKXYZ1h39-RJ7W5Tm1eo1R0T673keyXEstEi4j6msDfDu99000EMSNsvWmLIQAxPQKBsbMjEeDneokEA0-dM3.3Yy2jETrAfRcOZLuWM8Cc5f_sfS_RuVMsh0bpSCp6TA&s=digital-text), projects that required painstaking translation work with teams of skilled translators. The process was time-consuming and resource-intensive, but it was the only way to make these primary sources accessible to a broader audience.

As someone who has dedicated significant time to making historical sources more accessible, I've watched the rise of LLMs with great interest. These models promise to democratise access to multilingual content, potentially transforming how historians and researchers work with primary sources. However, the reality has proven more complex. Current models, while powerful, often struggle with or outright refuse to translate certain content. This is particularly problematic when working with historical documents about Afghanistan – for instance, a 1984 document discussing the Soviet-Afghan conflict might be flagged or refused translation simply because it contains the word "jihad", even in a purely historical context. The models' aggressive content filtering, while well-intentioned, can make them unreliable for serious academic work.

After repeatedly bumping into these limitations in my own work, I built [`tinbox`](https://github.com/strickvl/tinbox) (shortened from 'translation in a box'), a tool that approaches document translation through a different lens. What if we had a tool that could handle these sensitive historical texts without balking at their content? What if researchers could quickly get working translations of primary sources, even if they're not perfect, to accelerate their research process? As a historian, having access to even rough translations of primary source materials would have dramatically accelerated my research process. As a developer, I knew we could build something better than the current solutions.

The name "tinbox" is a nod to the simple yet effective nature of the tool – it's about taking the powerful capabilities of LLMs and packaging them in a way that actually works for real-world document translation needs. Whether you're a researcher working with historical documents, an academic handling multilingual sources, or anyone needing to translate documents at scale, [`tinbox`](https://github.com/strickvl/tinbox) aims to provide a more reliable and practical solution.

## The Hidden Complexity of Document Translation

The problem of document translation sits at an interesting intersection of challenges. On the surface, it might seem straightforward – after all, if an LLM can engage in complex dialogue, surely it can translate a document? It can, but there are some edge cases and limitations.

When working with real-world documents, particularly PDFs, we encounter a cascade of complications. First, there's the issue of model refusal. LLMs frequently decline to translate documents, citing copyright concerns or content sensitivity. This isn't just an occasional hiccup – it's a systematic limitation occurring regularly that makes these models unreliable for production use out of the box.

Then there's the scale problem. Most documents aren't just a few paragraphs; they're often dozens or hundreds of pages long. This runs headlong into the context window limitations of current models. Breaking documents into smaller chunks might seem like an obvious solution, but this introduces its own set of challenges. How do you maintain coherence across chunks? What happens when a sentence spans two pages? How do you handle formatting and structure?

The PDF format adds another layer of complexity. Most existing tools rely on Optical Character Recognition (OCR), which introduces its own set of problems. OCR can mangle formatting, struggle with complex layouts, and introduce errors that propagate through to the translation. Even when OCR works perfectly, you're still left with the challenge of maintaining the document's original structure and presentation.

## A Word About Translations, Fidelity and Accuracy

Having worked professionally as a translator and worked as an editor for teams of translators, I'm acutely aware of the challenges and limitations of LLM-provided translations. While these models have made remarkable strides, they face several significant hurdles that are worth examining in detail.

One of the most prominent issues is consistency. LLMs often struggle to maintain consistent terminology across multiple API calls, which becomes particularly evident in longer documents. Technical terms, product names, and industry-specific jargon might be translated differently each time they appear, creating confusion and reducing the professional quality of the output. This problem extends beyond mere terminology – the writing style and tone can drift significantly between chunks of text, especially when using the chunking approach necessary for longer documents. You might find yourself with a document that switches unexpectedly between formal and informal registers, or that handles technical depth inconsistently across sections.

Even formatting poses challenges. The way LLMs handle structural elements like bullet points, numbered lists, or text emphasis can vary dramatically across sections. What starts as a consistently formatted document can end up with a patchwork of different styling approaches, requiring additional cleanup work.

Perhaps more fundamentally, LLMs struggle to find the right balance between literal and fluent translation. Sometimes they produce awkwardly literal translations that technically convey the meaning but lose the natural flow of the target language. Other times, they swing too far in the opposite direction, producing fluid but unfaithful translations that lose important nuances from the source text. This challenge becomes particularly acute when dealing with idioms and cultural references, where literal translation would be meaningless but too free a translation risks losing the author's intent.

Cultural nuances present another significant challenge. LLMs often miss or mishandle culture-specific references, humour, and wordplay. They struggle with regional variations in language and historical context, potentially stripping away layers of meaning that a human translator would carefully preserve. This limitation becomes even more apparent in specialised fields – medical texts, legal documents, technical manuals, and academic writing all require domain expertise that LLMs don't consistently demonstrate.

The technical limitations of these models add another layer of complexity. The necessity of breaking longer texts into chunks means that broader document context can be lost, making it difficult to maintain coherence across section boundaries. While tools like `tinbox` attempt to address this through seam repair and sliding window approaches, it remains a significant challenge. Cross-references between different parts of the document might be missed, and maintaining a consistent voice across a long text can prove difficult.

Format-specific problems abound as well. Tables and figures might be misinterpreted, special characters can be mangled, and the connections between footnotes or endnotes and their references might be lost. Page layout elements can be corrupted in the translation process, requiring additional post-processing work.

Reliability and trust present another set of concerns. LLMs are prone to hallucination, sometimes adding content that wasn't present in the original text or filling in perceived gaps with invented information. They might create plausible but incorrect translations or embellish technical details. Moreover, they provide no indication of their confidence in different parts of the translation, no flags for potentially problematic passages, and no highlighting of ambiguous terms or phrases that might benefit from human review.

When it comes to handling source texts, LLMs show particular weakness with poor quality inputs. They struggle with grammatically incorrect text, informal or colloquial language, and dialectal variations. Their handling of abbreviations and acronyms can be inconsistent, potentially introducing errors into technical or specialised documents.

The ethical and professional implications of these limitations are significant. There's often a lack of transparency about the translation process, no clear audit trail for translation decisions, and limited ability to explain why particular choices were made. This raises concerns about professional displacement – not just in terms of jobs, but in terms of the valuable human judgment that professional translators bring to sensitive translations, the opportunity for cultural consultation, and the role of specialist translators in maintaining high standards in their fields.

These various limitations underscore an important point: while LLMs are powerful tools for translation, they should be seen as aids to human translators rather than replacements, especially in contexts requiring high accuracy, cultural sensitivity, technical precision, legal compliance, or creative fidelity. The future of translation likely lies in finding ways to combine the efficiency and broad capabilities of LLMs with the nuanced understanding and expertise of human translators.

So why build a tool like this given all these problems? I think there's still a use for something like this in fields where there are few translators and a huge backlog of materials where there's a benefit to reading them in your own mother tongue, even in a 'bad' translation. (That said, having done a decent amount of comparison of outputs for languages like Arabic, Dari and Pashto, I actually don't find the translations to be terrible, especially for domains like the news or political commentary.) For myself, I am working on a separate tool or system which takes in primary sources and incrementally populates a knowledge database. Having ways to ingest materials written in foreign languages is incredibly important for this, and having a way to do it that doesn't break the bang (i.e. by using local models) is similarly important.

## Engineering a Solution

`tinbox` takes a simple approach to solving these issues through two core algorithmic features. The first is what I call "page-by-page with seam repair." Instead of treating a document as one continuous piece of text, we acknowledge its natural segmentation into pages. Each page is translated independently, but – and this is crucial – we then apply a repair process to the seams between pages.

This seam repair is where things get interesting. When a sentence spans a page boundary, we identify the overlap and re-translate that specific section with full context from both pages. This ensures that the translation flows naturally, even across page boundaries. It's a bit like being a careful tailor, making sure the stitches between pieces of fabric are invisible in the final garment.

For continuous text documents (read: a `.txt` file containing multiple tens of thousands of words), we take a different approach using a sliding window algorithm. Think of it like moving a magnifying glass across the text, where the edges of the glass overlap with the previous and next positions. This overlap is crucial – it provides the context necessary for coherent translation across chunk boundaries.

The implementation details matter here. We need to carefully manage memory, handle errors gracefully, and provide progress tracking for long-running translations. The codebase is structured around clear separation of concerns, making it easy to add support for new document types or translation models.

Moreover, we need to ensure that in the case of failure we're able to resume without wasting what we spent translating earlier parts of the document.

## The Engineering Details

The architecture reflects these needs. At its core, `tinbox` uses a modular design that separates document processing from translation logic. This allows us to handle different document types (PDFs, Word documents, plain text) with specialised processors while maintaining a consistent interface for translation.

Error handling is particularly crucial. Translation is inherently error-prone, and when you're dealing with large documents, you need robust recovery mechanisms. We implement comprehensive retry logic with exponential backoff, ensuring that temporary failures (like rate limits) don't derail entire translation jobs.

For large documents, we provide checkpointing and progress tracking. This means you can resume interrupted translations and get detailed insights into the translation process. The progress tracking isn't just about displaying a percentage – it provides granular information about token usage, costs, and potential issues.

### Page-by-Page with Seam Repair

The page-by-page algorithm handles PDFs by treating each page as a separate unit while ensuring smooth transitions between pages. Pseudocode that can help you understand how this works goes something like this:

```python
def translate_with_seam_repair(document, overlap_size=200):
    translated_pages = []
    
    for page_num, page in enumerate(document.pages):
        # Translate current page
        current_translation = translate_page(page)
        
        if page_num > 0:
            # Extract and repair the seam between pages
            previous_end = translated_pages[-1][-overlap_size:]
            current_start = current_translation[:overlap_size]
            
            # Re-translate the overlapping section with full context
            repaired_seam = translate_with_context(
                text=current_start,
                previous_context=previous_end
            )
            
            # Update translations with repaired seam
            translated_pages[-1] = translated_pages[-1][:-overlap_size] + repaired_seam
            current_translation = repaired_seam + current_translation[overlap_size:]
        
        translated_pages.append(current_translation)
    
    return "\n\n".join(translated_pages)
```

### Sliding Window for Text Documents

For continuous text documents, we use a sliding window approach. Again, pseudocode to help understand how this works goes something like this, though the actual implementation is different:

```python
def translate_with_sliding_window(text, window_size=2000, overlap=200):
    chunks = []
    position = 0
    
    while position < len(text):
        # Create window with overlap
        end = min(len(text), position + window_size)
        window = text[position:end]
        
        # Translate window
        translation = translate_window(window)
        chunks.append(translation)
        
        # Slide window forward, accounting for overlap
        position = end - overlap
    
    return merge_chunks(chunks, overlap)
```

### CLI Usage Examples

The tool provides a simple command-line interface:

```bash
# Basic translation of a PDF to Spanish
tinbox --to es document.pdf

# Specify source language and model
tinbox --from zh --to en --model anthropic:claude-3-5-sonnet-latest chinese_doc.pdf

# Use local model via Ollama for sensitive content
tinbox --model ollama:mistral-small --to en sensitive_doc.pdf

# Advanced options for large documents
tinbox --to fr --algorithm sliding-window \
       --window-size 3000 --overlap 300 \
       large_document.txt
```

## Other notable features

The CLI interface for `tinbox` currently is built on top of `litellm` so it technically supports most models you might want to use with it, though I've only enabled OpenAI, Anthropic, Google/Gemini and Ollama as base providers for now.

The Ollama support was one I was keen to offer since translation is such a token-heavy task. I also really worry about the level of sensitivity / monitoring on the cloud APIs and have run into that in the past (particularly with regard to my previous work as a historian working on issues relating to Afghanistan). Ollama-provided local models should solve that issue, perhaps at the expense of access to the very latest and greatest models.

## Things still to be done

There's lots of improvements still to be made. I'm particularly interested in exploring semantic section detection, which could make the chunking process more intelligent. There's also work to be done on preserving more complex document formatting and supporting additional output formats.

Currently the tool is driven by whatever you tell it to do. Most decisions are in your hands. You have to choose the model to use for translation, notably. I am most interested in using this tool for some other side-projects and for low-resource languages so one of the important things I'll be doing is to pick sensible defaults depending on the language and input document type you choose.

For example, some vision language models like GPT-4o are able to handle translating directly from an image in Urdu to English, the open-source versions (like `llama3.2-vision`) struggle much more with these kinds of tasks so it's possible I might even need to insert an intermediary step of transcribe, then translate the transcribed text into English etc. In fact, for highest-fidelity of translation I almost certainly might want to enable that option.

The code is available at [GitHub](https://github.com/strickvl/tinbox), and I welcome contributions and feedback.