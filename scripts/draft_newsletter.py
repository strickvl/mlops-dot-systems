#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "beautifulsoup4",
#     "pyyaml",
# ]
# ///
"""
Create a draft newsletter email in Buttondown for a published post.

The email has the post's title as its subject, then its description and the
whole post, taken from the built page in `_site/` (so render the post first). It is
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
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://alexstrick.com"
CONTENT_DIRS = ["posts", "personal", "til"]
API = "https://api.buttondown.com/v1/emails"
LOG = ROOT / "_cache" / "newsletter_drafts.json"
# site-only parts of the built page: title block, contents, series box, related posts, sign-up form, comments
SITE_ONLY = ("#title-block-header, #TOC, .series-box, .series-footer, .subscribe-box, #related-posts, #related-posts-home, "
             "#quarto-appendix, script, style, .anchorjs-link, .code-copy-button")
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


def built_page(path: Path, meta: dict) -> Path:
    rel = path.relative_to(ROOT)
    page = ROOT / "_site" / rel.parent / (meta.get("output-file") or rel.with_suffix(".html").name)
    if not page.exists():
        sys.exit(f"draft_newsletter: {page.relative_to(ROOT)} doesn't exist; run `quarto render {rel}` first")
    return page


def post_body(page: Path, url: str) -> str:
    """The post's text from the built page, without the parts that only make sense on the site, as markdown."""
    main = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser").select_one("main#quarto-document-content")
    for junk in main.select(SITE_ONLY):
        junk.decompose()
    for tag, attr in (("a", "href"), ("img", "src")):
        for el in main.find_all(tag, attrs={attr: True}):
            if not el[attr].startswith("#"):
                el[attr] = urljoin(url, el[attr])
    # pandoc rather than raw HTML: Buttondown reads the body as markdown, where blank lines inside HTML blocks break them
    md = subprocess.run(["quarto", "pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"],
                        input=str(main), capture_output=True, text=True, check=True).stdout
    return md.strip()


def build_email(path: Path) -> tuple[str, str]:
    meta, _ = read_post(path)
    url = post_url(path, meta)
    parts = [f"*{meta['description']}*"] if meta.get("description") else []
    parts += [f"[Read this on alexstrick.com]({url})", post_body(built_page(path, meta), url),
              f"**[Comment on this post at alexstrick.com →]({url})**"]
    return str(meta.get("title", path.stem)), "\n\n".join(parts)


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
