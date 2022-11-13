---
aliases:
- /python/tools/2022/02/27/python-parsers
author: Alex Strick van Linschoten
categories:
- python
- tools
date: '2022-02-27'
description: The parse, yarl and datefinder packages are all ways in Python to help
  parse input data of different formats and types. Nothing essential here, but useful
  nonetheless.
image: python-parsers/parse.png
layout: post
title: Three Python Helpers for Parsing Inputs
toc: false

---

I continue to slowly work my way through the [calmcode](https://calmcode.io) back catalogue. This week I learned about three tiny utility packages that make certain parsing tasks less painful.

[`parse`](https://github.com/r1chardj0n3s/parse) (introduced [here](https://calmcode.io/parse/introduction.html)) is a way of turning simple text patterns into restructured data. Take the following example as an illustration:

```python
from parse import parse

url = "https://github.com/strickvl/some-repo/"

parse("https://github.com/{owner}/{repo}/", url).named

# returns {'owner': 'strickvl', 'repo': 'some-repo'}
```

As [Vincent explains](https://calmcode.io/parse/introduction.html), it's sort of the inverse or opposite operation to what happens with an f-string.

For URLs of various kinds that you want to decompose easily, [`yarl`](https://yarl.readthedocs.io/en/latest/) (introduced [here](https://calmcode.io/shorts/yarl.py.html)) is a great way to approach that in Python.

For dates stored in some kind of a string format, you might want to try [`datefinder`](https://datefinder.readthedocs.io) (introduced [here](https://calmcode.io/shorts/datefinder.py.html)), an elegant if not always perfect way for converting date strings into `datetime.datetime` objects.
