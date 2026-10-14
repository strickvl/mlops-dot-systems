#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pillow",
# ]
# ///
"""
Give every post a link-preview image (the picture shown when a link is shared
in Slack, LinkedIn, Mastodon, iMessage and so on).

Quarto picks a post's first image as its preview, if it has one. Posts with no
image get none, and posts whose image is AVIF (most migrated personal posts)
get one that the services drawing previews can't display. For both, this
script draws a 1200x630 title card and points the page's `og:image` and
`twitter:image` tags at it. Posts with a JPG/PNG/GIF preview are left alone.

Cards are cached in `_cache/cards/` by a hash of their text, so only new or
retitled posts are drawn again.

Runs automatically as a Quarto `post-render` step. To run it by hand after a
render:
    uv run scripts/preview_cards.py
"""

import hashlib
import html
import os
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
CACHE = ROOT / "_cache" / "cards"
FONT = ROOT / "assets" / "fonts" / "PlusJakartaSans[wght].ttf"
SITE_URL = "https://alexstrick.com"
SECTIONS = {"posts": ("Technical", "#2563EB"), "personal": ("Personal", "#C2593D"), "til": ("Today I Learned", "#2563EB")}
W, H, PAD = 1200, 630, 80
BG, INK, MUTED = "#FDFCFA", "#1F1F1F", "#6B6B70"
DESIGN = "v2"  # bump to redraw every card after changing the design

OG_IMAGE = re.compile(r'<meta property="og:image" content="([^"]*)"\s*/?>')
OG_TITLE = re.compile(r'<meta property="og:title" content="([^"]*)"')


def font(size: int, weight: str) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_name(weight)
    return f


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=f) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return [*lines, line]


def draw_card(title: str, section: str, colour: str, out: Path) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 14, W, H], fill=colour)
    d.text((PAD, PAD), section.upper(), font=font(26, "Bold"), fill=colour)

    # Largest title size (from 72px down) whose lines end well above the footer
    top, bottom = PAD + 70, H - PAD - 80
    for size in range(72, 34, -4):
        f, line_h = font(size, "Bold"), int(size * 1.2)
        lines = wrap(d, title, f, W - 2 * PAD)
        if top + len(lines) * line_h <= bottom:
            break
    y = top
    for line in lines:
        d.text((PAD, y), line, font=f, fill=INK)
        y += line_h

    d.text((PAD, H - PAD - 30), "Alex Strick van Linschoten", font=font(28, "SemiBold"), fill=INK)
    d.text((W - PAD, H - PAD - 30), "alexstrick.com", font=font(28, "Medium"), fill=MUTED, anchor="ra")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)


def needs_card(page: str) -> bool:
    m = OG_IMAGE.search(page)
    return m is None or m.group(1).lower().endswith(".avif") or f"{SITE_URL}/cards/" in m.group(1)


def set_preview(page: str, url: str) -> str:
    tags = (f'<meta property="og:image" content="{url}">\n'
            f'<meta property="og:image:width" content="{W}">\n<meta property="og:image:height" content="{H}">\n')
    page = re.sub(r'<meta property="og:image(?::\w+)?" content="[^"]*"\s*/?>\n?', "", page)
    page = re.sub(r'<meta name="twitter:image(?::\w+)?" content="[^"]*"\s*/?>\n?', "", page)
    page = re.sub(r'<meta name="twitter:card" content="[^"]*"\s*/?>',
                  '<meta name="twitter:card" content="summary_large_image">', page)
    tags += f'<meta name="twitter:image" content="{url}">\n'
    return page.replace("</head>", tags + "</head>", 1)


def process(page_path: Path) -> bool:
    rel = page_path.relative_to(SITE)
    if rel.parts[0] not in SECTIONS or len(rel.parts) != 2:
        return False
    page = page_path.read_text(encoding="utf-8")
    if not (m := OG_TITLE.search(page)) or not needs_card(page):
        return False  # redirect stubs have no og:title; posts with a usable image keep it
    title = html.unescape(m.group(1)).removesuffix(" – Alex Strick van Linschoten")
    section, colour = SECTIONS[rel.parts[0]]
    key = hashlib.sha256(f"{DESIGN}\n{section}\n{title}".encode()).hexdigest()[:16]
    cached = CACHE / f"{key}.png"
    if not cached.exists():
        draw_card(title, section, colour, cached)
    card_rel = Path("cards") / rel.parts[0] / f"{page_path.stem}.png"
    (SITE / card_rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(cached, SITE / card_rel)
    page_path.write_text(set_preview(page, f"{SITE_URL}/{card_rel.as_posix()}"), encoding="utf-8")
    return True


def main() -> None:
    listed = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES")
    pages = [Path(p).resolve() for p in listed.splitlines()] if listed else list(SITE.rglob("*.html"))
    pages = [p for p in pages if p.suffix == ".html" and p.is_file()]
    print(f"preview_cards: title cards for {sum(map(process, pages))} of {len(pages)} pages")


if __name__ == "__main__":
    main()
