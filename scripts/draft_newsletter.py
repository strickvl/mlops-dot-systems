#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
# ]
# ///
"""
Create a draft newsletter email in Buttondown for a published post.

The email has the post's title as its subject, then its description, its
opening paragraphs, and a link to read the rest on alexstrick.com. It is
created as a DRAFT: nothing is sent until you open it in Buttondown and click
send. Each post is recorded in `_cache/newsletter_drafts.json`, so running the
script twice doesn't make a second draft (use --force to make one anyway).

Reads BUTTONDOWN_API_KEY from the environment or from `.env` (gitignored).

Usage (publish the post first, so the link works):
    uv run scripts/draft_newsletter.py                  # newest post
    uv run scripts/draft_newsletter.py posts/2026-10-13-agent-swarm-observability-tools.md
    uv run scripts/draft_newsletter.py --dry-run        # print the email, don't create it
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://alexstrick.com"
CONTENT_DIRS = ["posts", "personal", "til"]
API = "https://api.buttondown.com/v1/emails"
LOG = ROOT / "_cache" / "newsletter_drafts.json"
EXCERPT_WORDS = 180
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.S | re.M)


def read_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".ipynb":
        cells = json.loads(text)["cells"]
        text = "\n\n".join("".join(c["source"]) for c in cells if c["cell_type"] in ("raw", "markdown"))
    m = FRONTMATTER.match(text)
    return (yaml.safe_load(m.group(1)) or {}, text[m.end():]) if m else ({}, text)


def post_url(path: Path, meta: dict) -> str:
    rel = path.relative_to(ROOT)
    return f"{SITE_URL}/{(rel.parent / (meta.get('output-file') or rel.with_suffix('.html').name)).as_posix()}"


def newest_post() -> Path:
    candidates = []
    for d in CONTENT_DIRS:
        for f in [*(ROOT / d).glob("*.md"), *(ROOT / d).glob("*.ipynb")]:
            meta, _ = read_post(f)
            if meta.get("date") and not meta.get("draft"):
                candidates.append((str(meta["date"])[:10], f.name, f))
    return max(candidates)[2]


def absolute_links(paragraph: str, page_url: str) -> str:
    base = page_url.rsplit("/", 1)[0]

    def fix(m: re.Match) -> str:
        target = m.group(2)
        if re.match(r"^[a-z]+:|^#", target):  # already absolute, or a link within the page
            return m.group(0)
        return f"{m.group(1)}({SITE_URL + target if target.startswith('/') else f'{base}/{target}'})"

    return re.sub(r"(\[[^\]]*\])\(([^)\s]+)\)", fix, paragraph)


def excerpt(body: str, url: str) -> str:
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    keep, words = [], 0
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        # prose only: skip headings, images, HTML, Quarto divs/attributes, tables and list-heavy blocks
        if not p or p.startswith(("#", "!", "<", ":::", "|", "{", "- ", "* ", "1. ")):
            continue
        keep.append(absolute_links(p, url))
        words += len(p.split())
        if words >= EXCERPT_WORDS:
            break
    return "\n\n".join(keep)


def build_email(path: Path) -> tuple[str, str]:
    meta, body = read_post(path)
    url = post_url(path, meta)
    parts = [f"*{meta['description']}*"] if meta.get("description") else []
    parts += [excerpt(body, url), f"**[Read the full post on alexstrick.com →]({url})**"]
    return str(meta.get("title", path.stem)), "\n\n".join(p for p in parts if p)


def api_key() -> str:
    if key := os.environ.get("BUTTONDOWN_API_KEY"):
        return key
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("BUTTONDOWN_API_KEY="):
                return line.split("=", 1)[1].strip().strip("\"'")
    sys.exit("draft_newsletter: no BUTTONDOWN_API_KEY in the environment or .env")


def create_draft(subject: str, body: str) -> dict:
    req = urllib.request.Request(API, method="POST",
                                 data=json.dumps({"subject": subject, "body": body, "status": "draft"}).encode(),
                                 headers={"Authorization": f"Token {api_key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"draft_newsletter: Buttondown returned {e.code}: {e.read().decode(errors='replace')[:500]}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("post", nargs="?", help="path to the post (default: newest post)")
    ap.add_argument("--dry-run", action="store_true", help="print the email instead of creating a draft")
    ap.add_argument("--force", action="store_true", help="create a draft even if this post already has one")
    args = ap.parse_args()

    path = (ROOT / args.post).resolve() if args.post else newest_post()
    rel = path.relative_to(ROOT).as_posix()
    subject, body = build_email(path)
    if args.dry_run:
        print(f"Subject: {subject}\n\n{body}")
        return

    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    if rel in log and not args.force:
        sys.exit(f"draft_newsletter: {rel} already has a draft (created {log[rel]['created']}); use --force for another")
    email = create_draft(subject, body)
    LOG.parent.mkdir(exist_ok=True)
    log[rel] = {"id": email.get("id"), "created": email.get("creation_date", "")}
    LOG.write_text(json.dumps(log, indent=1))
    print(f"draft_newsletter: created a draft for {rel}: \"{subject}\"")
    print("Open https://buttondown.com/emails to review and send it.")


if __name__ == "__main__":
    main()
