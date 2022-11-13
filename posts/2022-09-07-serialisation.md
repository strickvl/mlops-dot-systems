---
aliases:
- /computervision/mlops/python/redactionmodel/tools/zenml/2022/09/07/serialisation
author: Alex Strick van Linschoten
categories:
- redactionmodel
- computervision
- mlops
- python
- tools
- zenml
date: '2022-09-07'
description: I explain the basics around data serialisation and deserialisation, why
  it's a commonly-encountered topic, and showcase where I had to implement some custom
  logic to serialise custom Python objects used in a computer vision project.
image: serialisation/fabio-oyXis2kALVg-unsplash.jpg
layout: post
title: 'Storing Bytes: what data serialisation is and why you need it for machine
  learning'
toc: true

---

_(This is part of a series of blog posts documenting my work to train a model that detects redactions in documents. To read other posts, check out [the `redactionmodel` taglist](https://mlops.systems/categories/#redactionmodel).)_

Serialisation and deserialisation. I ran headfirst into these two words on my first day in my new job. From the way my colleagues discussed them, it seemed like this was something I should have learned from a computer science degree; foundational concepts with practical applications throughout most places that computers touched.

A few months in, I've come to appreciate a little more about what the underlying concept is about as well as some of the reasons why it remains both relevant and something that pops up regularly. I'll begin by setting out some of this context before showing an example of where I encountered it recently in my own project. By the end, you'll understand why this is such an important (and practical) concept and why you'll encounter it a lot while doing machine learning.

## 🔢 The Basics

In the common definition, serialisation is the process by which you convert something into a sequence of bytes, and deserialisation is when you convert the other way (i.e. *from* bytes). In some domains it is also known as marshalling or pickling.

This commonly is encountered when you need to store some data on disk (i.e. *not* or no longer in memory). Perhaps you need some kind of permanent storage of that data, or you need to make the data available to another process. The process through which you transform the data (from something that is comprehensible to whatever environment or language you're working on) is serialisation.

To give another example, in a language like Python we often think in and deal through a series of 'objects': think dictionaries or even classes in an OOP context. In order to save this to disk, we have to convert it to some other format that firstly is in some format that is stable when saved as a file. We might want to send that data across the network, or have it opened by a different process or a programme running in a different language. Serialisation is the process by which something context and perhaps language-specific gets transformed into this universal substrate (i.e. a sequence of bytes).

## 🍏 Common ways to serialise data in Python

In the past, `pickle` was a commonly-used way of making this conversion. It has a lot of shortcomings, two of which sit at the top of the list:

- there isn't (as far as I'm aware) much interoperability for objects that are serialised with `pickle`. If you want to load an object that has been 'pickled', the entity doing the 'unpickling' will have to be running the exact same version of Python as the one that did the pickling. (If I'm not mistaken, there might even be some cross platform interoperability issues as well.)
- security concerns are serious when it comes to `pickle`: when you `load(...)` some pickled object, this will run whatever code is inside with the assumption that it is 'trusted'. As such, it is unsuitable for use with untrusted data and generally people tend to turn their nose at `pickle`. (If you *do* have to interact with some pickled data, [`pickletools`](https://docs.python.org/3/library/pickletools.html) is a handy tool that allows you to inspect and interact with the file **without** running the arbitrary code packaged inside. While we're at the library recommendations, it's also worth checking out [`fickling`](https://github.com/trailofbits/fickling) which overlaps in functionality somewhat.)

JSON has become a commonly-used format for serialising data (or its cousin [JSONL](https://jsonlines.org), for too-much-to-load-into-memory-at-once data). This is a common format with many uses, but it does come with a serious shortcoming which is that it only supports certain data types. If you're saving some custom object of your own creation, you'll first need to convert that into a format that can be transformed into a JSON object/file. If you don't, then your object will not be able to be rehydrated from the on-disk representation.

Note that the Python `pickle` module serialises data into a binary format, whereas the `json` module converts it into a text format (i.e. readable and comprehensible to someone browsing files or displaying their contents with something like `cat`). Moreover, `pickle` does handle many (most?) objects and types that you can throw at it, though with all the caveats mentioned above.

I haven't explored it at all, but while reading a bit about this area I was consistently pointed to Google's [Protobuf](https://developers.google.com/protocol-buffers) format / library which is another way to serialise structured data. I am unable to properly evaluate the extent to which this is an improvement on existing protocols.

## 🔐 Serialisation and deserialisation in Machine Learning

I mentioned earlier that this concept and operation was something that I confronted more or less on my first day working in my new job. (*We build [an open-source framework](https://zenml.io) that supports someone working to build and deploy machine learning models.*) In order to understand why this is so important, a small detour showing a basic example of a ZenML pipeline is necessary. What follows is an extremely simple example showcasing how pipelines are composed of steps, and how those are in turn run:

```python
from zenml.steps import step
from zenml.pipelines import pipeline

@step
def read_integer() -> int:
    return 3

@pipeline
def basic_pipeline(read_integer) -> None:
    read_integer()

basic_pipeline(read_integer=read_integer()).run()
```

Pipelines are constructed out of a series of steps. The steps are defined with an `@step` decorator, and pipeline definitions are composed in a similar way. Finally, at the end we specify which steps correspond to which parts of the pipeline definition and then call the `run()` method to execute our pipeline.

You'll also note the presence of some type annotations as part of how we define our step and pipeline. These are required, and while they may seem simplistic and unnecessary at the moment, later on they will make things much clearer.

Our pipeline isn't doing much at the moment, you might think. Behind the scenes, however, ZenML is doing a lot of legwork:

- storing the outputs (and inputs, though there aren't any in this basic example) of all steps
- caching those output values or objects, such that if the code doesn't change then we should just retrieve the cached value.
- validating and checking the types of values that get returned so that we can be sure our code is returning what we hope / think it should be returning.

Moreover, it does all this in a way that all this intermediary state is stored on disk and versioned. If you update your pipeline steps then rerun it, ZenML will save the new outputs such that you can go back and inspect where data came from and so on.

In order to save all these objects on disk, however, and to bring this story full-circle, ZenML serialises the data when saving the artifacts from pipeline runs, and deserialises that data when those artifacts are needed (by the cache, for example, or when you want to access a step output once your pipeline has completed its run). We call this part of the process 'materialisation'. (There's more [in our docs on materialisation here](https://docs.zenml.io/developer-guide/advanced-usage/materializer), and if you're searching, be sure to search with a 'z' and not an 's', coz America.)

## 🛠 A basic custom materializer

For most kinds of 'normal' Python objects, this is no problem at all. But as we saw above, if we're going to be able to reconstruct and rehydrate an object from a static sequence of bytes, we're going to need to do a bit more to make this happen. Within ZenML this means that if you have some special kind of object or type, you'll need to define a 'custom materialiser'; this is code that defines how ZenML should serialise and deserialise the objects that you want to be stored as state on disk.

To give you a sense of what this will look like, here's our code from above but updated a little to fit this new scenario:

```python
import os
from typing import Type

from zenml.artifacts import DataArtifact
from zenml.io import fileio
from zenml.materializers.base_materializer import BaseMaterializer
from zenml.pipelines import pipeline
from zenml.steps import step

class MyCustomObject:
    def __init__(self, name):
        self.name = name

class MyCustomMaterializer(BaseMaterializer):
    ASSOCIATED_TYPES = (MyCustomObject,)
    ASSOCIATED_ARTIFACT_TYPES = (DataArtifact,)

    def handle_input(self, data_type: Type[MyCustomObject]) -> MyCustomObject:
        """Read from artifact store"""
        super().handle_input(data_type)
        with fileio.open(os.path.join(self.artifact.uri, "data.txt"), "r") as f:
            name = f.read()
        return MyCustomObject(name=name)

    def handle_return(self, my_obj: MyCustomObject) -> None:
        """Write to artifact store"""
        super().handle_return(my_obj)
        with fileio.open(os.path.join(self.artifact.uri, "data.txt"), "w") as f:
            f.write(my_obj.name)

@step
def read_custom_object() -> MyCustomObject:
    return MyCustomObject("aria")

@pipeline
def basic_pipeline(read_custom_object) -> None:
    read_custom_object()

basic_pipeline(
    read_custom_object=read_custom_object().with_return_materializers(
        MyCustomMaterializer
    )
).run()
```

You'll notice a new piece of code which defines the `MyCustomMaterializer` class. This is subclassed off our `BaseMaterializer` class and we just have to define two methods, one that handles how to serialise or save the data to disk, and the other that handles how to deserialise or rehydrate the objects/data from disk. We add a special `.with_return_materializers` call when we run the pipeline; this lets ZenML that when we encounter a weird type of object, it can go ahead and use our custom defined materialiser to handle it.

I hope you'll agree that this stuff isn't *too* hard to grok, and while the precise steps of how you implement all this might take a bit of getting used to, it's conceptually not too hard once you understand the foundations of what you're doing. It took me longer than I'm proud to admit to really understand the elegance of this way of doing things, but all these little pieces add up and you can then go off and use them in your real-life projects.

## 🕵️ Materialisation in practice: IceVision and Custom Objects

Case in point: my object detection pipeline. I took a bit of a break over the summer, but now I'm back and working to get my pipeline production-ready. Defining the basic steps of my pipeline were fairly easy; I've already described that in [my last blog post](https://mlops.systems/tools/redactionmodel/computervision/mlops/2022/05/31/redaction-production-introduction.html).

The moment I started defining my pipeline in code, I immediately hit a whole array of non-standard objects. My data loading steps returned IceVision-specific parsers custom to COCO BBoxes and my training step returned a collection of various custom objects combining code with the trained model parameters. (*Note: for some common use cases like training with raw PyTorch or Tensorflow etc, ZenML has defined many standard materialisers already to get you going quickly.*) I realised that I'd have to define custom materialisers to handle these different inputs and outputs.

Some of this wasn't trivial to implement. Sometimes you might get lucky and the library you work with has implemented some handy features to help with serialisation and deserialisation. From what I can tell, this seems to be the case when saving models with PyTorch, for example. But for the rest it's often less clear what need to happen and why code works in the way it does. To save the IceVision `RecordCollection` object, for example, I had to jump through some hoops, converting several sub levels of custom objects along the way, to make sure that my objects were serialisable.

Here's the custom materialiser code responsible for handling those conversions and serialisation for the `RecordCollection`. (Think of `RecordCollection` just as a type of stored data, parsed and ready to use for model training.)

```python
import os
import pathlib
from typing import Any, Dict, List, Type

from icevision.all import *
import srsly
from zenml.artifacts import DataArtifact
from zenml.io import fileio
from zenml.materializers.base_materializer import BaseMaterializer

class COCOMaterializerParser(Parser):
    def __init__(self, template_record, records: List[Dict[str, Any]]):
        super().__init__(template_record=self.template_record())

        self.records = records
        self.class_map = ClassMap(records[0]["common"]["classes"])
        print(self.class_map)

    def __iter__(self) -> Any:
        yield from self.records

    def __len__(self) -> int:
        return len(self.records)

    def record_id(self, o: Any) -> Hashable:
        return o["common"]["filepath"]

    def template_record(self) -> BaseRecord:
        return BaseRecord(
            (
                FilepathRecordComponent(),
                InstancesLabelsRecordComponent(),
                AreasRecordComponent(),
                IsCrowdsRecordComponent(),
                BBoxesRecordComponent(),
            )
        )

    def filepath(self, o) -> Path:
        return pathlib.Path(o["common"]["filepath"])

    def img_size(self, o) -> ImgSize:
        return ImgSize(width=o["common"]["width"], height=o["common"]["height"])

    def labels_ids(self, o) -> List[Hashable]:
        return o["detection"]["label_ids"]

    def areas(self, o) -> List[float]:
        return o["detection"]["areas"]

    def iscrowds(self, o) -> List[bool]:
        return o["detection"]["iscrowds"]

    def bboxes(self, o) -> List[BBox]:
        boxes = []
        for bbox in o["detection"]["bboxes"]:
            a, b, c, d = bbox
            new_bbox = BBox.from_xyxy(a, b, c, d)
            boxes.append(new_bbox)
        return boxes

    def parse_fields(self, o: Any, record: BaseRecord, is_new: bool):
        if is_new:
            record.set_filepath(self.filepath(o))
            record.set_img_size(self.img_size(o))

        record.detection.set_class_map(self.class_map)
        record.detection.add_areas(self.areas(o))
        record.detection.add_iscrowds(self.iscrowds(o))
        record.detection.add_bboxes(self.bboxes(o))
        record.detection.add_labels(o["detection"]["labels"])


def detection_record_collection_to_json(rcoll: RecordCollection) -> str:
    indexes = list(rcoll._records)
    records = [rcoll._records[index] for index in indexes]
    classes = rcoll[0].detection.class_map.get_classes()
    dict_records = [record.as_dict() for record in records]
    for record in dict_records:
        record["common"]["filepath"] = str(record["common"]["filepath"])
        bboxes = record["detection"]["bboxes"]
        new_bboxes = []
        for bbox in bboxes:
            a, b, c, d = bbox.xyxy
            new_bbox = [a, b, c, d]
            new_bboxes.append(new_bbox)
        record["detection"]["bboxes"] = new_bboxes
        record["common"]["classes"] = classes
    return srsly.json_dumps(dict_records)


def detection_json_str_to_record_collection(records: str) -> RecordCollection:
    r = srsly.json_loads(records)
    template_record = ObjectDetectionRecord()
    parser = COCOMaterializerParser(template_record, r)
    parsed_records, *_ = parser.parse(data_splitter=SingleSplitSplitter())
    return parsed_records


class COCOBBoxRecordCollectionMaterializer(BaseMaterializer):
    ASSOCIATED_TYPES = (RecordCollection,)
    ASSOCIATED_ARTIFACT_TYPES = (DataArtifact,)

    def handle_input(self, data_type: Type[RecordCollection]) -> RecordCollection:
        """Read from artifact store"""
        super().handle_input(data_type)
        with fileio.open(
            os.path.join(self.artifact.uri, DEFAULT_RECORD_COLLECTION), "r"
        ) as f:
            return detection_json_str_to_record_collection(f.read())

    def handle_return(self, record_collection_obj: RecordCollection) -> None:
        """Write to artifact store"""
        super().handle_return(record_collection_obj)

        json_string = detection_record_collection_to_json(record_collection_obj)
        with fileio.open(
            os.path.join(self.artifact.uri, DEFAULT_RECORD_COLLECTION), "w"
        ) as f:
            f.write(json_string)
```

As you can see, there's a decent amount going on here. In my custom materialiser, I have a `detection_record_collection_to_json` method that constructs the JSON representation of my custom `RecordCollection` object. I use [Explosion's handy `srsly` package](https://github.com/explosion/srsly) for their forks + bundling together of various Python serialisation libraries. For the rest, that requires a bit more knowledge of how IceVision handles things like `BBox` objects and COCO Records under the hood, but you can get the idea that it's not completely trivial. 

## 🥳 Serialisation is for Everyone!

It's also not completely impossible to implement either, though, lest you feel like I'm leaving you without hope. My aim with this article was to guide you to the point where you feel you can understand why serialisation is important and to know why you might well encounter it during your data science journey. The moment you need to do something just slightly longer-lasting than an ephemeral training run that is tracked nowhere and just lives in a Colab notebook, that's when you'll hit serialisation.

Moreover, I showed how you can incrementally build up your pipelines with a tool like ZenML to handle lots of parts of the complexity that come with your modelling work.

[*Image credit*: Photo by <a href="https://unsplash.com/@fabioha?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">fabio</a> on <a href="https://unsplash.com/s/photos/data?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>]
