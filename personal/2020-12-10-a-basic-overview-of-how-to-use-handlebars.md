---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - javascript
  - web
  - technology
  - launchschool
date: "2020-12-10"
description: "A basic overview of the Handlebars templating language and how to use it with JavaScript to separate HTML from your code."
layout: post
title: "A basic overview of how to use Handlebars"
toc: true
aliases:
  - "/blog/a-basic-overview-of-how-to-use-handlebars.html"
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

![](images/2020-12-10-a-basic-overview-of-how-to-use-handlebars/9e8ea59b7c0c_image-asset.avif)

[Handlebars](https://handlebarsjs.com/) is a simple templating language that you can use with your JavaScript code. It came somewhat late to the game; Python and Ruby and others had their own templating options for a while.

The problem it is trying to solve is the case where you have a lot of HTML code that you need to create in your JavaScript files, but you don't want to leave your `.js` files completely bursting to the seams with HTML.

An example is probably good at this point:

```
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/handlebars@latest/dist/handlebars.js"></script>
    <script src='handlebarsApp.js'></script>
  </head>
  <body>
    <h1>Hello, World</h1>
    <script id='handlebars1' type='text/x-handlebars'>
      <div>
        {{{name}}}
        <br>
        {{date}}
      </div>
    </script>
  </body>
</html>
```

and here's the associated JavaScript file:

```
document.addEventListener('DOMContentLoaded', () => {
  let script1 = document.querySelector('#handlebars1').innerHTML;

  let obj = {
    "name": "<h2>Henry</h2>",
    "date": "<i>2020-12-10</i>",
  };

  let templateScript = Handlebars.compile(script1); // returns a function
  document.body.innerHTML = templateScript(obj);
});
```

A few points to note from this (simple) example:

- you include the Handlebars functionality by adding a script that either links to a CDN (as I did above), or you download the file and host that yourself.
- in the main HTML file, prior to the JavaScript running, you have the `<h1>` text ('Hello World') which is displayed and you have this `<script>` block (our 'template') which is defined with an `id` of `handlebars1`. This just sits here until the JavaScript does something with it.
- The template uses both double curly braces (`{{something1}}`)and triple curly braces (`{{{something2}}}`). Double curly braces means that any HTML values are 'escaped' when we pass everything through handlebars for compilation. Triple curly braces means that we don't escape characters, so the `<h2>` tag is 'processed' and you can see the result of that tag being applied, whereas the `<i>` tag is not applied and it is just treated as plain text (so you see the markup).
- In our JavaScript code, the procedure is as follows:
  - (Make sure the DOM has loaded and is ready for things to start happening)
  - locate the template in the DOM and the html contained with in (you can either use the `.innerHTML` property or jQuery's `.html()` method on a jQuery object
  - create the context that you want to pass into this template. this will be an object with keys named as per whatever you used to define your template inside the HTML file.
  - use `Handlebars.compile()` (passing in the template's `innerHTML`) to get a function that can return HTML text depending on what context we pass into it.
  - use the returned function from the previous step to get that HTML text, and then do with that what we wish. (We might want to create a new node object and insert it into the DOM somewhere. We might want to replace one of the currently existing nodes and put our compiled HTML there instead).

Note also how we have managed to keep our JavaScript file mostly free of HTML code. This allows us to keep the layout and templating work to the HTML file, and our logic for our JavaScript file.

## Logic: Conditionals

Handlebars *does* allow us to include some logic in our templates, however. I can add a few lines to my template:

```
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/handlebars@latest/dist/handlebars.js"></script>
    <script src='handlebarsApp.js'></script>
  </head>
  <body>
    <h1>Hello, World</h1>
    <script id='handlebars1' type='text/x-handlebars'>
      <div>
        {{{name}}}
        <br>
        {{date}}
        <br></br>
        {{#if homework}}
        I love homework.
        {{else}}
        -- No homework today
        {{/if}}
      </div>
    </script>
  </body>
</html>
```

In this example I added a conditional if/else statement. I checked there was a `homework` key on the object that we compiled our HTML with. There wasn't, so the 'no homework today' string was output.

(A Handlebars conditional is false if the property value is `false`, `undefined`, `null`, `''`, `0` or an empty array.)

Note that we start the vast majority of these 'logic' parts of Handlebars with a `#` character. `{{else}}` is apparently an exception and you shouldn't include a `#` in front of that when using it.

## Logic: Iteration

We can also include iteration as part of our Handlebars templates using the `{{#each}}` keyword. Here's the HTML:

```
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/handlebars@latest/dist/handlebars.js"></script>
    <script src='handlebarsApp.js'></script>
  </head>
  <body>
    <h1>Hello, World</h1>
    <script id='handlebars1' type='text/x-handlebars'>
      <div>
        {{{name}}}
        <br>
        {{date}}
        <br></br>
        {{#if homework}}
        I love homework.
        {{else}}
        -- No homework today
        {{/if}}
        <br><br>
        <h3>List of people</h3>
        {{#each people}}
        <p>{{this}}</p>
        {{/each}}
      </div>
    </script>
  </body>
</html>
```

And here's the associated JavaScript file, updated to include an array as part of the context object:

```
document.addEventListener('DOMContentLoaded', () => {
  let script1 = document.querySelector('#handlebars1').innerHTML;

  let obj = {
    "name": "<h2>Henry</h2>",
    "date": "<i>2020-12-10</i>",
    "people": [
      "Alex Strick",
      "Hope Riley",
    ],
  };

  let templateScript = Handlebars.compile(script1); // returns a function
  document.body.innerHTML = templateScript(obj);
});
```

Things to note from this example:

- We start the iteration with `{{#each people}}`, passing in the name of the object property that is iterable
- We end the iteration with a closing `{{/each}}`
- the `this` *inside* our iteration refers to the individual element that we're currently on as part of our iteration.

If we want to deal with nested values, the `as` keyword along with `|` pipes allows us to do what we need. Our HTML runs as follows:

```
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/handlebars@latest/dist/handlebars.js"></script>
    <script src='handlebarsApp.js'></script>
  </head>
  <body>
    <h1>Hello, World</h1>
    <script id='handlebars1' type='text/x-handlebars'>
      <div>
        {{{name}}}
        <br>
        {{date}}
        <br></br>
        {{#if homework}}
        I love homework.
        {{else}}
        -- No homework today
        {{/if}}
        <br><br>

        <h3>List of people</h3>
        {{#each people}}
        <p>{{this}}</p>
        {{/each}}

        <h3>Agenda</h3>
        {{#each agenda as |agendaItem name|}}
        <p>{{name}}: {{agendaItem.hobby}} // {{agendaItem.work}}</p>
        {{/each}}

      </div>
    </script>
  </body>
</html>
```

And our updated JavaScript to include a nested object:

```
document.addEventListener('DOMContentLoaded', () => {
  let script1 = document.querySelector('#handlebars1').innerHTML;

  let obj = {
    "name": "<h2>Henry</h2>",
    "date": "<i>2020-12-10</i>",
    "people": [
      "Alex Strick",
      "Hope Riley",
    ],
    'agenda': {
      'alex': {
        'hobby': 'swimming',
        'work': 'reading',
      },
      'hope': {
        'hobby': 'dancing',
        'work': 'walking',
      },
    },
  };

  let templateScript = Handlebars.compile(script1); // returns a function
  document.body.innerHTML = templateScript(obj);
});
```

Note that after using the `as` keyword and the pipes operators, we specify first the variable name to denote the bottom-level object (`agendaItem`), and then a variable name to denote the two named keys (i.e. `alex` and `hope`). This allows us to use both in the pattern we code in our template.

## Logic: Iteration and the `with` keyword

We can use the `with` keyword to gain access to object properties. Instead of using the `as` syntax shown above, we can use `with` so we don't need the dot syntax to access those properties. The example is a bit contrived, but you get the idea. The relevant additional section of our HTML file would be:

```
<h3>Agenda 2</h3>
{{#each agenda as |__ name|}}
{{#with this}}
<p>{{name}}: {{hobby}} // {{work}}</p>
{{/with}}
{{/each}}
```

I use the `as` syntax here so that we can refer to each individual object's key, but we wouldn't always necessarily need to do this.

## Partials For More Complex Templating

We can use partials to include templates within templates. The syntax to include a partial inside a template is to use the `>` symbol inside a pair of curly braces. For example, our HTML might look like this in a simple case:

```
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/handlebars@latest/dist/handlebars.js"></script>
    <script src='handlebarsApp.js'></script>
  </head>
  <body>
    <h1>Title of our Page</h1>
    <script id='handlebars1' type='text/x-handlebars'>
      <div>
        {{> partialTemplate}}
        <ol>
        {{#each names}}
        <li>{{this}}</li>
        {{/each}}
        </ol>
      </div>
    </script>

    <script id='partial' type='text/x-handlebars'>
      <h2>Job: {{job}}</h2>
      <h2>Year: {{year}}</h2>
    </script>
  </body>
</html>
```

…and the associated JavaScript would look like this:

```
document.addEventListener('DOMContentLoaded', () => {
  let script1 = document.querySelector('#handlebars1').innerHTML;
  let script2 = document.querySelector('#partial').innerHTML;

  let obj = {
    "names": [
      "Alex Strick",
      "Hope Riley",
    ],
    'job': 'fencing',
    'year': 2021,
  };

  let templateScript1 = Handlebars.compile(script1);

  Handlebars.registerPartial('partialTemplate', script2);

  let newNode1 = document.createElement('div');
  newNode1.innerHTML = templateScript1(obj);

  document.body.appendChild(newNode1);
});
```

Some points worth mentioning here about the two chunks of code above:

- Our partial looks like any other template when we define it in our HTML file. We might want to distinguish it by giving it a certain `id`, but otherwise it looks like any other handlebars template, with the same `type` applied to it.
- In order for our partial to be usable as a template-within-a-template, it needs to have a variable name that we can use to reference it. We register this name by using `Handlebars.registerPartial()`. This method takes two arguments: the name that we'd like to register it under, and the template HTML.
- The rest of our code runs as in previous examples mentioned above, with the exception that when it reaches the line of code {{> partialTemplate}}`, this is then converted and passed in to replace the placeholder at this point.

You can also define partials in the JavaScript code itself. [This website](https://www.sitepoint.com/a-beginners-guide-to-handlebars/) offers an example of that:

```
Handlebars.registerPartial(
  'partialTemplate',
  '{{language}} is {{adjective}}. You are reading this article on {{website}}.'
);

var context={
  "language" : "Handlebars",
  "adjective": "awesome"
}
```

This is coupled with the following defined in the HTML file:

```
{{> partialTemplate website="sitepoint"}} <br>
{{> partialTemplate website="www.sitepoint.com"}}
```

You can play around with that example [on CodePen](http://codepen.io/SitePoint/pen/BNYZLK).

## Closing Thoughts

You can play around with Handlebars [here](http://tryhandlebarsjs.com/). I like how it gives you options as to where you want to house logic for a particular website. There are obviously tradeoffs to consider, particularly whether code should be running server-side or client-side and how that might affect speed and loading times.

I will need more practical experience to really unpack the implications of using Handlebars, but I am looking forward to getting to use it with a better sense of control now that I understand the fundamentals.
