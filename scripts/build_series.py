#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
# ]
# ///
"""
Build the series index that the series page and the in-post series boxes read.

Quarto renders each page on its own, so a post can't know it is "part 4 of 8"
without someone looking at every post first. This script does that: it reads
`_series.yml` plus the `series:` frontmatter of every post, orders each series
by date, and writes `_series.json`. Two Lua files in `filters/` then read that
JSON during the render.

Runs automatically as a Quarto `pre-render` step. To run it by hand:
    uv run scripts/build_series.py
"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIRS = ["posts", "personal"]
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.S | re.M)


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".ipynb":
        cells = json.loads(text).get("cells") or [{}]
        text = "".join(cells[0].get("source", []))
    if not (m := FRONTMATTER.match(text)):
        return {}
    meta = yaml.safe_load(m.group(1))
    return meta if isinstance(meta, dict) else {}


def as_list(value) -> list[str]:
    if value is None:
        return []
    return [str(v) for v in value] if isinstance(value, list) else [str(value)]


def output_url(path: Path, meta: dict) -> str:
    rel = path.relative_to(ROOT)
    name = meta.get("output-file") or rel.with_suffix(".html").name
    return "/" + (rel.parent / name).as_posix()


def collect_posts() -> list[dict]:
    files = [f for d in CONTENT_DIRS for ext in ("*.md", "*.ipynb") for f in (ROOT / d).rglob(ext)]
    posts = []
    for f in files:
        meta = read_frontmatter(f)
        if not (ids := as_list(meta.get("series"))) or meta.get("draft"):
            continue
        posts.append({"src": f.relative_to(ROOT).as_posix(), "url": output_url(f, meta),
                      "title": str(meta.get("title", f.stem)), "date": str(meta.get("date", ""))[:10],
                      "series": ids})
    return posts


def build(registry: list[dict], posts: list[dict]) -> dict:
    known = {s["id"] for s in registry}
    if unknown := sorted({(p["src"], i) for p in posts for i in p["series"] if i not in known}):
        lines = "\n".join(f"  {src}: series '{i}' is not in _series.yml" for src, i in unknown)
        sys.exit(f"build_series: unknown series id(s):\n{lines}")

    series, by_post = [], {}
    for s in registry:
        members = sorted((p for p in posts if s["id"] in p["series"]), key=lambda p: (p["date"], p["src"]))
        if not members:
            print(f"build_series: warning: series '{s['id']}' has no posts yet", file=sys.stderr)
            continue
        series.append({"id": s["id"], "title": s["title"], "section": s.get("section", "technical"),
                       "description": s.get("description", ""), "ongoing": bool(s.get("ongoing")),
                       "start": members[0]["date"], "end": members[-1]["date"],
                       "posts": [{k: p[k] for k in ("src", "url", "title", "date")} for p in members]})
        for i, p in enumerate(members):
            by_post.setdefault(p["src"], []).append({"series": s["id"], "index": i})

    series.sort(key=lambda s: s["start"], reverse=True)
    return {"series": series, "posts": by_post}


def main() -> None:
    registry = yaml.safe_load((ROOT / "_series.yml").read_text(encoding="utf-8")) or []
    index = build(registry, collect_posts())
    (ROOT / "_series.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"build_series: {len(index['series'])} series, {len(index['posts'])} posts")


if __name__ == "__main__":
    main()
