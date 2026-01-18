# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Quarto-based static blog combining technical content (mlops.systems) and personal content (migrated from Squarespace). The site is hosted on GitHub Pages. Content is written in Markdown (.md) and Jupyter notebooks (.ipynb).

The site has **two content sections** with separate RSS feeds:
- **Technical** (`/index.xml`) - MLOps, software engineering, AI/ML content
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
- `index.qmd` - Technical blog listing page
- `personal.qmd` - Personal blog listing page
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
include-before-body: '<script defer data-domain="mlops.systems" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/blog/YYYY/MM/old-slug.html"  # Optional: for SEO redirects from old URLs
---
```

**Note**: Personal posts use `data-domain="alexstrick.com"` in the analytics script.

## Important Notes

- **Image handling**: Do NOT manually save images into `posts/copied_from_nb/`. GitHub Actions automatically manages images there and may delete manually added files at build time.
- **Image compression**: A GitHub Action automatically compresses images on PRs using calibreapp/image-actions.
- **Build outputs**: `_site/` and `.quarto/` are gitignored and regenerated on build.
- **URL Redirects**: Personal posts have `aliases` in frontmatter to redirect old Squarespace URLs (`/blog/YYYY/MM/slug`) to new locations. These are client-side JS redirects.
- **Design docs**: The `design/` folder contains migration notes and planning docs (gitignored, not committed).
