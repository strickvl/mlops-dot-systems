# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Quarto-based static blog combining technical content and personal content (migrated from Squarespace). The site is built locally with Quarto and served from **GitHub Pages** (the `gh-pages` branch) at **alexstrick.com**, with **Cloudflare in front as DNS + CDN** (so responses show `server: cloudflare` even though GitHub Pages is the origin). `mlops.systems` redirects to `alexstrick.com`. Content is written in Markdown (.md) and Jupyter notebooks (.ipynb).

> **Domain Migration In Progress**: See `design/domain-migration-plan.md` for details. The canonical domain is `alexstrick.com`.

The site has **two content sections** with separate RSS feeds:
- **Technical** (`/technical.xml`) - MLOps, software engineering, AI/ML content
- **Personal** (`/personal.xml`) - Personal writing, language learning, books, Afghanistan, etc.

## Common Commands

```bash
# Preview site locally (hot-reloads on changes)
quarto preview

# Build static site to _site/ directory
quarto render

# Publish to GitHub Pages
quarto publish gh-pages

# Generate descriptions for posts missing them (uses Claude Haiku)
uv run scripts/generate_descriptions.py --directory personal --dry-run
```

## Content Structure

- `posts/` - Technical blog posts (Markdown and Jupyter notebooks)
- `personal/` - Personal blog posts (migrated from Squarespace, ~287 posts)
  - `personal/images/` - Images for personal posts, organized by post
- `til/` - "Today I Learned" short-form content
- `scripts/` - Utility scripts (migration, description generation, etc.)
- `_quarto.yml` - Site configuration (navbar, theme, analytics)
- `index.qmd` - Custom landing page (two cards linking to Technical/Personal); NOT a post listing
- `technical.qmd` - Technical blog listing page (lists `posts/`); shows the clickable category tag cloud
- `personal.qmd` - Personal blog listing page (lists `personal/`)
- `all.qmd` - Combined chronological archive (lists `posts/` + `personal/`)
- `styles.css` - Global CSS (e.g. tag-cloud styling); each listing page also loads its own `styles/<page>.css`
- `about.qmd`, `til.qmd` - Other main pages

## Blog Post Format

Posts use YAML frontmatter:

```yaml
---
author: Alex Strick van Linschoten
categories:
  - category1
  - category2
date: "YYYY-MM-DD"
description: "Brief description"
layout: post
title: "Post Title"
toc: true
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/blog/YYYY/MM/old-slug.html"  # Optional: for SEO redirects from old URLs
---
```

**Note on Analytics**: The global `_quarto.yml` config handles Plausible analytics (`data-domain="alexstrick.com"`). Do NOT add `include-before-body` to individual posts — legacy overrides are being removed.

**Category / tag links**: The listing pages use `categories: cloud`, which renders a clickable tag cloud and turns each post's category badges into filter links. When linking to a tag from post body text, point to `/technical.html#category=X` (or `/personal.html#category=X`) — NOT `index.html#category=X` (the landing page has no listing, so the filter silently does nothing) and NOT the old `mlops.systems/#category=X`.

## Important Notes

- **Publishing is manual**: After adding or editing blog posts, run `quarto publish gh-pages` to deploy changes to the live site. There is no automatic GitHub Actions workflow for publishing - only for image compression on PRs. (Committing/pushing to `main` does NOT deploy — only `quarto publish gh-pages` does.)
- **Cloudflare caching after publish**: A deploy takes a few minutes (GitHub Pages build), and Cloudflare may then serve a stale `styles.css`/assets. If CSS or asset changes don't show, hard-refresh (Cmd-Shift-R) or purge the Cloudflare cache. To confirm a deploy actually landed, check the branch directly (`git show origin/gh-pages:<file>`) rather than curling the live URL, which is subject to both delays.
- **One malformed-YAML post aborts the whole render**: `quarto render`/`publish` parses every post's frontmatter, so a single file with curly/smart quotes (`"` `"`) or an unquoted colon in a value kills the entire build. If a render fails on a YAML error, check recently-edited or draft posts' frontmatter first. For work-in-progress posts, set `draft: true`; with the configured `draft-mode: gone` they render to a tiny empty stub and stay out of all listings, the sitemap, and search.
- **DO NOT DELETE FILES without understanding what they are.** Only delete files that are clearly identified as build artifacts (`.html` files in source directories, `_files/` directories, `site_libs/`). If you see an unfamiliar file or directory in `git status`, ASK before deleting. The user may be working on new files in parallel.
- **Image handling**: Do NOT manually save images into `posts/copied_from_nb/`. GitHub Actions automatically manages images there and may delete manually added files at build time.
- **Image compression**: A GitHub Action automatically compresses images on PRs using calibreapp/image-actions.
- **Build outputs**: `_site/` and `.quarto/` are gitignored and regenerated on build.
- **URL Redirects**: Personal posts have `aliases` in frontmatter to redirect old Squarespace URLs (`/blog/YYYY/MM/slug`) to new locations. These are client-side JS redirects.
- **Design docs**: The `design/` folder contains migration notes and planning docs (gitignored, not committed).
