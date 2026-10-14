#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastembed",
#     "numpy",
#     "pyyaml",
# ]
# ///
"""
Find the most similar posts for every post, across technical, personal and TIL.

A local embedding model turns each post's text into a vector (a list of
numbers capturing what the post is about). Posts whose vectors point the same
way are about similar things. For each post we keep the closest few, skipping
posts from the same series (the series box already links those), and write
them to `_related.json` for `filters/related-posts.lua`.

Vectors are cached in `_cache/related_embeddings.npz` next to a hash of the
text that produced them, so only new or edited posts go through the model.

Runs automatically as a Quarto `pre-render` step. To run it by hand:
    uv run scripts/build_related.py
"""

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIRS = {"posts": "Technical", "personal": "Personal", "til": "TIL"}
MODEL = "nomic-ai/nomic-embed-text-v1.5"
PREFIX = "clustering: "  # nomic models expect a task prefix
MIN_WORDS = 150  # shorter posts (link posts, image-only posts) neither get nor give suggestions
TOP_K = 5
MAX_WORDS = 1500  # the model's cost grows with the square of length; a post's opening says what it's about
CACHE = ROOT / "_cache" / "related_embeddings.npz"
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.S | re.M)


def split_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".ipynb":
        cells = json.loads(text).get("cells") or []
        text = "\n\n".join("".join(c.get("source", [])) for c in cells if c.get("cell_type") in ("raw", "markdown"))
    if not (m := FRONTMATTER.match(text)):
        return {}, text
    meta = yaml.safe_load(m.group(1))
    return (meta if isinstance(meta, dict) else {}), text[m.end():]


def clean(body: str) -> str:
    body = re.sub(r"```.*?```", " ", body, flags=re.S)  # code says little about the topic
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)  # images
    body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)  # keep link text, drop URL
    body = re.sub(r"<[^>]+>|\{[.#][^}]*\}", " ", body)  # HTML tags, Quarto attributes
    return re.sub(r"\s+", " ", body).strip()


def output_url(path: Path, meta: dict) -> str:
    rel = path.relative_to(ROOT)
    return "/" + (rel.parent / (meta.get("output-file") or rel.with_suffix(".html").name)).as_posix()


def as_set(value) -> set[str]:
    if value is None:
        return set()
    return {str(v) for v in value} if isinstance(value, list) else {str(value)}


def collect_posts() -> list[dict]:
    posts = []
    for d, section in CONTENT_DIRS.items():
        for f in sorted([*(ROOT / d).rglob("*.md"), *(ROOT / d).rglob("*.ipynb")]):
            meta, body = split_post(f)
            body = clean(body)
            if not meta or meta.get("draft") or len(body.split()) < MIN_WORDS:
                continue
            title = str(meta.get("title", f.stem))
            words = f"{title}. {meta.get('description') or ''}\n\n{body}".split()
            text = PREFIX + " ".join(words[:MAX_WORDS])
            posts.append({"src": f.relative_to(ROOT).as_posix(), "url": output_url(f, meta), "title": title,
                          "date": str(meta.get("date", ""))[:10], "section": section,
                          "series": as_set(meta.get("series")), "text": text,
                          "hash": hashlib.sha256(f"{MODEL}\n{text}".encode()).hexdigest()})
    return posts


def save_cache(cached: dict) -> None:
    CACHE.parent.mkdir(exist_ok=True)
    np.savez_compressed(CACHE, hashes=np.array(list(cached)), vectors=np.stack(list(cached.values())))


def embed(posts: list[dict]) -> np.ndarray:
    cached = {}
    if CACHE.exists():
        data = np.load(CACHE)
        cached = dict(zip(data["hashes"].tolist(), data["vectors"]))
    todo = [p for p in posts if p["hash"] not in cached]
    if todo:
        from fastembed import TextEmbedding  # imported lazily: only needed when something changed

        model = TextEmbedding(MODEL)
        # batch_size=1: batching pads every post to the longest one in the batch, which wastes work
        for n, (p, vec) in enumerate(zip(todo, model.embed([p["text"] for p in todo], batch_size=1)), 1):
            cached[p["hash"]] = vec.astype(np.float32)
            if n % 25 == 0 or n == len(todo):
                print(f"build_related: embedded {n}/{len(todo)} new or changed post(s)", flush=True)
                save_cache(cached)  # keep progress if the run is interrupted
    current = {p["hash"] for p in posts}
    cached = {h: v for h, v in cached.items() if h in current}  # drop vectors for edited or deleted posts
    save_cache(cached)
    vectors = np.stack([cached[p["hash"]] for p in posts])
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def nearest(posts: list[dict], vectors: np.ndarray) -> dict:
    similarity = vectors @ vectors.T
    related = {}
    for i, p in enumerate(posts):
        picks = []
        for j in np.argsort(-similarity[i]):
            q = posts[j]
            if j == i or (p["series"] & q["series"]):
                continue
            picks.append({k: q[k] for k in ("url", "title", "date", "section")})
            if len(picks) == TOP_K:
                break
        related[p["src"]] = picks
    return related


def main() -> None:
    posts = collect_posts()
    related = nearest(posts, embed(posts))
    (ROOT / "_related.json").write_text(json.dumps(related, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"build_related: suggestions for {len(related)} posts")


if __name__ == "__main__":
    main()
