---
name: publish-blog
description: Take a newly written alexstrick.com post from draft to live, covering frontmatter checks, series, build, commit, push, `quarto publish`, and a newsletter draft. Use for /publish-blog, "publish this post", or "I've written a new post".
---

# Publish a blog post

Starting point: Alex has just written a new post (in `posts/`, `personal/` or `til/`). Invoking this skill authorizes every step below, including the commit, the push and the publish. Sending the newsletter stays with Alex: this skill only creates a draft.

## Steps

1. **Find the post.** Look at `git status` for new or changed `.md`/`.ipynb` files in `posts/`, `personal/` or `til/`, plus their images (`posts/images/<slug>/`, `personal/images/<slug>/`). Done when you have exactly one post and its image files. If there are several candidates, ask which one.

2. **Check the frontmatter.** One bad post stops the whole site from building, so check:
   - `title`, `date` (quoted `"YYYY-MM-DD"`), `description`, `categories`, `author: Alex Strick van Linschoten`, `layout: post`, and the `comments: utterances: repo: strickvl/mlops-dot-systems` block that sibling posts carry.
   - No curly quotes (`“ ” ‘ ’`) or unquoted colons inside YAML values.
   - `draft: true` is absent, or ask whether to remove it. With it, the post builds to an empty page.
   - **Categories reuse existing tags.** Compare each one with the tags already in use (count them across `posts/ personal/ til/`). If a tag is a near-duplicate of an existing one (plural, hyphen, capitals, synonym), switch to the existing one and say so.
   - **Series.** If the post continues an existing series in `_series.yml`, or Alex says it starts one, follow the `blog-series` skill.
   - If `description` is missing, write one sentence in Alex's plain voice from the post and show it to Alex.

   Done when every item above passes or has been fixed, and every fix is reported.

3. **Render the post.** Run `quarto render <post path>`. This also runs the pre-render steps (series index, related-posts embeddings) and the post-render steps (preview cards, stylesheet stamps). Done when it exits 0 and the built page `_site/<dir>/<slug>.html` contains:
   - `id="related-posts"` (only posts of 150+ words get related posts)
   - `subscribe-box`
   - `og:image`
   - `series-part` with the expected "Part N of M", if the post is in a series

   On a fresh clone, the first related-posts run downloads a ~0.5 GB model and embeds every post (about 2 minutes); later runs take seconds.

4. **Commit and push.** Stage only the post and its own images (and `_series.yml` if step 2 changed it). Commit with a subject like ``Add post: `<slug>` `` (code identifiers in backticks). Push. Never stage `_site/`, `_cache/`, `_series.json`, `_related.json`, `.env` or anything in `design/`. Done when `git status -sb` shows `main` level with `origin/main`.

5. **Publish.** Run `quarto publish gh-pages --no-prompt`. It re-renders the whole site, which takes a few minutes, and pushes `_site/` to the `gh-pages` branch. Done when it exits 0 and `git fetch -q origin gh-pages && git show origin/gh-pages:<dir>/<slug>.html` shows the post. Check the branch, not the live URL, which can lag by a few minutes behind GitHub Pages and Cloudflare.

6. **Draft the newsletter.** The email is the whole post. The script takes it from the built page in `_site/` (step 3 made it), cuts out the site-only parts (title block, contents, series box, related posts, sign-up form) and turns it into markdown with pandoc. Run `uv run scripts/draft_newsletter.py <post path> --dry-run` and check that:
   - links and images point to alexstrick.com, and links to other posts end in `.html`, not `.md` or `.ipynb`
   - none of the site-only parts are left, and there's no stray HTML or `:::` markup

   If the email reads badly, fix the script rather than the post. Then run it without `--dry-run`. Skip this step if Alex asked for no email. Done when the script reports the draft was created (or reports that one already exists for this post).

   **If the draft is already made and needs redoing** (the post changed, or the script was fixed), run it again with `--force` to make a new draft. Tell Alex to delete the old draft in Buttondown, so only one is left to send. The script never deletes or edits drafts.

7. **Report.** Give the live URL, the series part (if any), the five related posts, any fixes made in step 2, and remind Alex the email is a **draft** waiting at https://buttondown.com/emails for him to review and send.
