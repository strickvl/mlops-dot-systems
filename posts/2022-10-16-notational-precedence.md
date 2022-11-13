---
aliases:
- /j/mathematics/mu123/q31/notation/2022/10/16/notational-precedence.html
author: Alex Strick van Linschoten
categories:
- j
- mathematics
- mu123
- q31
- notation
date: '2022-10-16'
description: I learned about prefix, postfix and infix notation, and how J evaluates
  mathematical expressions which makes the BIDMAS rules unnecessary.
image: notational-precedence/j-precedence.png
layout: post
title: Avoiding BIDMAS, or how J does notation
toc: false

---

One of the topics that comes up early on in Open University's [MU123 mathematics course](https://www.open.ac.uk/courses/modules/mu123) is precedence. Those who grew up in English-speaking countries will probably know this as [BODMAS or BIDMAS](https://www.bbc.co.uk/bitesize/topics/zxqnsk7/articles/znm8cmn). The order of precedence for execution of a mathematical expression gives us an idea for how to resolve expressions that don't make sense. For example, `3 + 1 x 4` can  either amount to 7 or 16, depending on how when you do the multiplication step.

Brackets are one way to make things more precise, and that's probably why they're the B in BIDMAS and that they go first. We could write `3 + (1 x 4)` to make it really clear that we wanted the `1 x 4` sub-expression to be evaluated first.

With the rules of precedence, we technically wouldn't need to add in any brackets because we could (likely) assume that people would follow the standard rules and they would know that we have to evaluate multiplications before we evaluate the additions. So we have a way, but it maybe feels a bit unsatisfactory.

Some languages or domains, however, have notational rules which don't rely on a meta-schema of precedence rules like BIDMAS to tell you which expressions should be evaluated first. Instead, the order is determined in other ways, with the option of brackets when needed.

Several of the languages in the APL family, like J, simply evaluate from right to left in the order that expressions are encountered. See this example in J:

```j
   3 + 1 * 4
7
   4 * 3 + 1
16
```

The order in which the expressions are evaluated determines the answer.

Thinking and reading a bit about these orders of precedence brought me to learn a bit about other traditions of mathematical notation. The one most used and that you'll be most familiar with is called *infix notation* i.e. `3 + 4`.

Prefix notation (AKA Polish notation) is when we write `+ 3 4` (to the same end) and postfix notation (AKA reverse Polish notation) is when we write `3 4 +`. (The Polish part relates back to [Jan Łukasiewicz](https://en.wikipedia.org/wiki/Jan_Łukasiewicz), who invented it in 1924.) These kinds of notation are used in Lisp and Clojure, for example.

Why would you want to use a notation style like this? Some possible reasons:

- the operands in the expressions can handle arbitrary numbers of arguments, making them more efficient to write
- they are consistent with the syntax used for functions in computer programming (which can be easier to get your mind round)
- they're clearer to read and (mostly) unambiguous, unlike infix notation which (see above) requires a whole order of precedence if you're not using brackets
- there's no confusion or need for precedence rules
- it's faster for a machine to evaluate, since the way expressions are formulated is much easier to translate into computer code.

So there you go. I'm unclear whether there are more fundamental benefits to living in the world of post-/prefix notation, and perhaps it's a little like the people who argue that [we'd all be better off](https://gizmodo.com/why-we-should-switch-to-a-base-12-counting-system-5977095) if we lived in a base-12 world instead of base-10, but that's beside the point for now.

I'll try to share some more diversions from my mathematics study along the way, hopefully powered by [J](https://www.jsoftware.com) which I'm trying to get back into.
