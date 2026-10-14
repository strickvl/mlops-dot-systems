---
name: blog-series
description: Add, start, finish, rename or remove blog series on alexstrick.com. Use when a post should join a series, a new series begins, a series ends, or the series page or "Part N of M" boxes look wrong.
---

# Blog series

A series is a run of posts listed on `/series.html` and marked in each member post with a "Part N of M" box at the top and previous/next links at the bottom.

Two places hold all the data; everything else is generated:

- `_series.yml`: one entry per series (`id`, `title`, `section: technical|personal`, `description`, optional `ongoing: true`). Its order doesn't matter; the page sorts series by start date, newest first.
- each post's frontmatter: `series: <id>`, or `series: [<id>, <other-id>]` for a post in two series.

Part numbers come from post dates (ties broken by filename). Never write a number by hand. Draft posts are left out until `draft: true` is removed.

## Steps

1. **Read `_series.yml`** and note the existing ids. Done when you know whether the series the user means already exists.

2. **Make the change** for the branch that applies:
   - **Post joins a series**: add the `series:` line as the last line of the frontmatter, just above the closing `---`. If the post already has a `series:` line, turn it into a list instead of adding a second line.
     In a `.ipynb` post the frontmatter is in the first (raw) cell, stored as JSON strings. Insert `"series: <id>\n",` as a new line directly above the closing `"---"` line, matching its indentation. Edit the text in place; re-saving the notebook through a JSON library reformats the whole file.
   - **New series**: add an entry to `_series.yml` with `ongoing: true`, then tag its posts as above. Use a short kebab-case id; it becomes the `/series.html#<id>` link. If the user gave no description, draft one sentence in their plain first-person voice from the posts' content and show it to them.
   - **Series finished**: delete its `ongoing: true` line.
   - **Rename an id**: change it in `_series.yml` and in every post (`grep -rln "series:.*<old-id>" posts personal`). Tell the user that old `/series.html#<old-id>` links will stop scrolling to the series.
   - **Post leaves a series**: remove that id from its `series:` value, or delete the line if it was the only one.

3. **Rebuild the index**: `uv run scripts/build_series.py`. Done when it prints `build_series: N series, M posts` with no error. An unknown id stops it with the post's path named; a series with no posts prints a warning and is left off the page.

4. **Render and check**: `quarto render series.qmd` plus each post you touched (`quarto render <path>`). Then `grep -o 'series-part">[^<]*' _site/<path>.html` for each touched post. Done when every touched post shows the "Part N of M" you expect, and the series page lists the series with the right number of parts.

5. **Report** what changed and the part numbers each touched post now has. Publishing is a separate manual step (`quarto publish gh-pages`, which does a full render). Only a full render updates every page, so other posts in the same series show the new total only after that.

## How the generated parts fit together

`scripts/build_series.py` runs as Quarto's `pre-render` step on every render. It reads `_series.yml` and every post's frontmatter and writes `_series.json` (gitignored). Then, during the render:

- `filters/series-box.lua` looks up the post being rendered in `_series.json` and adds the boxes.
- `filters/series-index.lua` is the `{{< series-index >}}` shortcode in `series.qmd`; it draws the timeline.

Styles live in `styles.css` (in-post box, under "Series box inside posts") and `styles/series.css` (series page).
