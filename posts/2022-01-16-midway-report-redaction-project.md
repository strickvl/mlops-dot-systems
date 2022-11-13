---
aliases:
- /fastai/python/redactionmodel/tools/2022/01/16/midway-report-redaction-project
author: Alex Strick van Linschoten
categories:
- python
- fastai
- tools
- redactionmodel
date: '2022-01-16'
description: A report midway through my computer vision project to detect the presence
  of redactions on government documents.
image: midway-report-redaction-project/midway-thumb.png
layout: post
title: A Midway Report on my Computer Vision Project
toc: false

---

(_This post is adapted from
[a twitter thread](https://twitter.com/strickvl/status/1482645800656281604), so
is a bit more terse than usual._)

I recently switched what I spend the majority of my professional life doing
(history -> software engineering). I'm currently working as an ML Engineer at
[ZenML](https://github.com/zenml-io/zenml) and really enjoying this new world of
MLOps, filled as it is with challenges and opportunities.

I wanted to get some context for the wider work of a data scientist to help me
appreciate the problem we are trying to address at
[ZenML](https://github.com/zenml-io/zenml), so looked around for a juicy machine
learning problem to work on as a longer project.

I was also encouraged by
[Jeremy Howard's advice](https://www.alexstrick.com/blog/fastai-lesson-zero) to
"build one project and make it great". This approach seems like it has really
paid off for those who've studied [the fastai course](https://course.fast.ai)
and I wanted to really go deep on something myself.

Following some previous success working with other mentors from
[SharpestMinds](https://www.sharpestminds.com) on a previous project, I settled
on Computer Vision and was lucky to find Farid AKA
[@ai_fast_track](https://twitter.com/ai_fast_track) to mentor me through the
work.

In the last 6 weeks, I've made what feels like good progress on the problem.
This image offers an overview of the pieces I've been working on, to the point
where the 'solution' to my original problem feels on the verge of being
practically within reach.

![]({{ site.baseurl
}}/images/midway-report-redaction-project/midway-presentation.jpeg "Some of the things
I worked on over the past six weeks.")

After just a few lessons of the FastAI course, I
[trained a classification model](https://mlops.systems/fastai/redactionmodel/computervision/datalabelling/2021/09/06/redaction-classification-chapter-2.html)
to ~95% accuracy to help me sort redacted images from unredacted images.

I used Explosion's Prodigy to
[annotate an initial round](https://mlops.systems/redactionmodel/computervision/datalabelling/2021/11/29/prodigy-object-detection-training.html)
of data to pass into the next step, enjoying how the labelling process brought
me into greater contact with the dataset along the way.

I switched to using [IceVision](https://airctic.com/) to help me with the more
complicated object detection problem, using MMDetection and VFNet
[to get pretty good results](https://mlops.systems/redactionmodel/computervision/progressreport/2021/12/11/redaction-progress-week-one.html)
early on.

I'm currently in the process of creating my own synthetic images to boost the
annotations I've manually made. (I'll be writing about this process soon as
well, as I'm learning a lot about why this is so important for these kinds of
computer vision problems.)

I've also been amazed at the effectiveness of self-training (i.e. using my
initial model in my annotation loop to generate an initial set of annotations
which I can easily amend as appropriate, then feeding those annotations in to
create a better model and so on). More to follow on that step, too.

I started using [Evidently](https://evidentlyai.com) to do some drift detection,
inspired by some work I was doing for ZenML on adding Evidently as an
integration to our own tool. This helped me think about how new data was
affecting the model and the training cycle. I feel like there's a lot of depth
here to understand, and am looking forward to diving in.

I made a tiny little demo on [HuggingFace Spaces](https://huggingface.co/spaces)
to show off the current inference capabilities and to see the model in a setting
that feels close to reality. This is a simple little
[Gradio](https://www.gradio.app) app but I liked how easy this was to put
together (a couple of hours, mainly involving some build issues and a dodgy
`requirements.txt` file)

Along the way, I found it sometimes quite painful or fiddly to handle the PDF
files that are the main data source for the project, so I built
[my own Python package](https://pypi.org/project/pdfsplitter/) to handle the
hard work. I used fastai's nbdev to
[very quickly get the starters](https://mlops.systems/python/jupyter/fastai/tools/2022/01/06/nbdev-early-impressions.html)
of what I'm hoping might be a useful tool for others using PDF data for ML
projects.

Throughout all this, [Farid](https://www.linkedin.com/in/farid-hassainia-ca/)
has been patiently helping guide me forward. He saved me from going down some
dark rabbit holes, from spending too long studying skills and parts of the
problem that needed relatively little mastery in order to get to where I am.

Farid has been a consistently enthusiastic and kind advocate for my work,
moreover, and this has really helped me stay the course for this project that
takes a decent chunk of my time (especially seeing as I do it completely aside /
separately from my day job).

I feel like I'm consistently making progress and learning the skills of a data
scientist working in computer vision, even though I have so much left to learn!
My project still has a ways to go before it's 'done', but I'm confident that
I'll get there with Farid's support. (Thank you!)
