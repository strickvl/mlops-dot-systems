#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""
Stamp the site's own stylesheet links with a hash of the file's contents,
e.g. `styles.css` -> `styles.css?v=3f9a1c2b7d`.

The server tells browsers to keep CSS for 4 hours. Without a stamp, a reader
who visited earlier gets the new HTML with their old cached CSS, and new
elements show up unstyled. A stamp that changes whenever the CSS changes makes
the browser fetch the new file; unchanged CSS keeps the same stamp and stays
cached. Quarto's own files in `site_libs/` already carry hashes in their names.

Runs automatically as a Quarto `post-render` step. To run it by hand after a
render:
    uv run scripts/cache_bust.py
"""

import hashlib
import os
import re
from functools import cache
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "_site"
LINK = re.compile(r'(<link\b[^>]*?\bhref=")((?:[^"?]*/)?styles(?:/[\w-]+)?\.css)(?:\?v=\w+)?(")')


@cache
def stamp(css: Path) -> str | None:
    return hashlib.sha256(css.read_bytes()).hexdigest()[:10] if css.is_file() else None


def bust(page: Path) -> bool:
    html = page.read_text(encoding="utf-8")

    def replace(m: re.Match) -> str:
        v = stamp((page.parent / m.group(2)).resolve())
        return f"{m.group(1)}{m.group(2)}?v={v}{m.group(3)}" if v else m.group(0)

    new = LINK.sub(replace, html)
    if new != html:
        page.write_text(new, encoding="utf-8")
    return new != html


def main() -> None:
    # Quarto lists the files it just rendered; a by-hand run covers the whole site
    listed = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES")
    pages = [Path(p).resolve() for p in listed.splitlines()] if listed else list(SITE.rglob("*.html"))
    pages = [p for p in pages if p.suffix == ".html" and p.is_file()]
    print(f"cache_bust: stamped stylesheet links in {sum(map(bust, pages))} of {len(pages)} pages")


if __name__ == "__main__":
    main()
