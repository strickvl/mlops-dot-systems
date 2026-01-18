---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - tech
  - afghanistan
  - productivity
  - data
  - software
  - technology
date: "2018-01-17"
description: "I discovered Tabula, a tool that extracts table data from PDFs and exports it to formats like CSV and JSON."
layout: post
title: "Tabula for extracting table data from PDFs"
toc: true
aliases:
  - "/blog/tabula-extracting-data-pdfs.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

Have you ever come across a PDF filled with useful data, but wanted to play around with that data yourself? In the past if I had that problem, I'd type the table out manually. This has some disadvantages:

- it is extremely boring
- it's likely that mistakes will get made, especially if the table is long and extends over several pages
- it takes a long time

I recently discovered a tool that solves this problem: [Tabula](http://tabula.technology/). It works on Windows and Mac and is *very* easy and intuitive to use. Simply take your page of data:

[caption id="" align="alignnone" width="2040"]![ A page listing Kandahar's provincial council election polling stations from a few years back. Note the use of English and Dari scripts. Tabula handles all this without problems. ](images/2018-01-17-tabula-extracting-data-pdfs/21ec1627605d_ScreenShot_2018-01-17_at_15.53.31.avif) A page listing Kandahar's provincial council election polling stations from a few years back. Note the use of English and Dari scripts. Tabula handles all this without problems. [/caption]

Then import the file into Tabula's web interface. It's surprisingly good at autodetecting where tables and table borders are, but you can do it manually if need be:

![](images/2018-01-17-tabula-extracting-data-pdfs/6b51f1eed600_ScreenShot_2018-01-17_at_15.56.25.avif)

Then check that the data has been correctly scraped, select formats for export (from CSV to JSON etc):

![](images/2018-01-17-tabula-extracting-data-pdfs/60892142ad64_ScreenShot_2018-01-17_at_15.57.19.avif)

And there you have it, all your data in a CSV file ready for use in R or Python or just a simple Excel spreadsheet:

![](images/2018-01-17-tabula-extracting-data-pdfs/53231595cfb4_ScreenShot_2018-01-17_at_15.57.50.avif)

Note that even though the interface runs through a browser, none of your data touches external servers. All the processing and stripping of data from PDFs is done on your computer, and isn't sent for processing to cloud servers. This is a really nice feature and I'm glad they wrote the software this way.

I haven't had any problems using Tabula so far. It's a great time saver. Highly recommended.
