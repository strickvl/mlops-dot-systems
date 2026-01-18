#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "markdownify",
# ]
# ///
"""
Squarespace to Quarto Migration Script

Parses a Squarespace/WordPress XML export and converts posts to Quarto-compatible
Markdown files with proper frontmatter, image downloading, and URL alias generation.

Usage:
    python scripts/migrate_squarespace.py --xml squarespace_export/export.xml --output personal/
    python scripts/migrate_squarespace.py --xml squarespace_export/export.xml --dry-run  # Preview only
"""

import argparse
import hashlib
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse
import json

import httpx
from markdownify import markdownify as md, MarkdownConverter

# XML namespaces used in WordPress export format
NAMESPACES = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


@dataclass
class Post:
    """Represents a blog post extracted from the XML export."""

    title: str
    slug: str
    content_html: str
    pub_date: datetime
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    status: str = "publish"
    post_type: str = "post"
    original_url: str = ""
    excerpt: str = ""

    @property
    def filename(self) -> str:
        """Generate Quarto-compatible filename: YYYY-MM-DD-slug.md"""
        date_prefix = self.pub_date.strftime("%Y-%m-%d")
        # Clean slug: remove date prefix if present, keep alphanumeric and hyphens
        clean_slug = re.sub(r"^\d{4}/\d{2}/", "", self.slug)
        clean_slug = re.sub(r"[^a-z0-9-]", "-", clean_slug.lower())
        clean_slug = re.sub(r"-+", "-", clean_slug).strip("-")
        return f"{date_prefix}-{clean_slug}.md"

    @property
    def alias_path(self) -> str:
        """Generate alias path matching original Squarespace URL structure."""
        # Original URLs look like: /blog/2010/04/kandahar-chronology-...
        if self.original_url.startswith("/"):
            return self.original_url.rstrip("/") + ".html"
        return f"/blog/{self.slug}.html"


class CustomMarkdownConverter(MarkdownConverter):
    """Custom converter with better handling of Squarespace-specific HTML."""

    def convert_img(self, el, text, convert_as_inline):
        """Handle images, extracting src and alt text."""
        src = el.get("src", "")
        alt = el.get("alt", "")

        # Handle Squarespace image URLs
        if "squarespace" in src or "static.squarespace" in src:
            # Mark for later download
            return f"![{alt}]({src}){{.squarespace-image}}"

        return f"![{alt}]({src})"

    def convert_iframe(self, el, text, convert_as_inline):
        """Convert iframes (YouTube embeds, etc.) to a placeholder."""
        src = el.get("src", "")
        if "youtube" in src or "youtu.be" in src:
            # Extract video ID
            video_id = None
            if "youtube.com/embed/" in src:
                video_id = src.split("/embed/")[1].split("?")[0]
            elif "youtube.com/v/" in src:
                video_id = src.split("/v/")[1].split("&")[0]
            if video_id:
                return f"\n\n{{{{< video https://www.youtube.com/embed/{video_id} >}}}}\n\n"
        return f"\n\n[Embedded content: {src}]\n\n"

    def convert_object(self, el, text, convert_as_inline):
        """Handle old Flash embeds (often YouTube)."""
        # Look for YouTube video URL in params
        for param in el.find_all("param") if hasattr(el, "find_all") else []:
            value = param.get("value", "")
            if "youtube.com/v/" in value:
                video_id = value.split("/v/")[1].split("&")[0]
                return f"\n\n{{{{< video https://www.youtube.com/embed/{video_id} >}}}}\n\n"
        return ""


def parse_xml(xml_path: Path) -> tuple[list[Post], list[dict]]:
    """
    Parse WordPress XML export file and extract posts and pages.

    Returns:
        Tuple of (posts, pages) where each is a list of Post objects
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    channel = root.find("channel")

    posts = []
    pages = []

    for item in channel.findall("item"):
        # Extract post type
        post_type = item.find("wp:post_type", NAMESPACES)
        post_type_text = post_type.text if post_type is not None else "post"

        # Skip attachments
        if post_type_text == "attachment":
            continue

        # Extract status
        status = item.find("wp:status", NAMESPACES)
        status_text = status.text if status is not None else "publish"

        # Skip drafts unless you want them
        if status_text != "publish":
            continue

        # Extract title
        title_el = item.find("title")
        title = title_el.text if title_el is not None and title_el.text else "Untitled"

        # Extract content
        content_el = item.find("content:encoded", NAMESPACES)
        content_html = content_el.text if content_el is not None and content_el.text else ""

        # Extract link/URL
        link_el = item.find("link")
        original_url = link_el.text if link_el is not None and link_el.text else ""

        # Extract slug
        slug_el = item.find("wp:post_name", NAMESPACES)
        slug = slug_el.text if slug_el is not None and slug_el.text else ""

        # Extract publication date
        date_el = item.find("wp:post_date", NAMESPACES)
        if date_el is not None and date_el.text:
            try:
                pub_date = datetime.strptime(date_el.text, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pub_date = datetime.now()
        else:
            pub_date = datetime.now()

        # Extract categories and tags
        categories = []
        tags = []
        for cat in item.findall("category"):
            domain = cat.get("domain", "")
            if cat.text:
                if domain == "category":
                    categories.append(cat.text)
                elif domain == "post_tag":
                    tags.append(cat.text)

        # Deduplicate
        categories = list(set(categories))
        tags = list(set(tags))

        # Extract excerpt
        excerpt_el = item.find("excerpt:encoded", NAMESPACES)
        excerpt = excerpt_el.text if excerpt_el is not None and excerpt_el.text else ""

        post = Post(
            title=title,
            slug=slug,
            content_html=content_html,
            pub_date=pub_date,
            categories=categories,
            tags=tags,
            status=status_text,
            post_type=post_type_text,
            original_url=original_url,
            excerpt=excerpt,
        )

        if post_type_text == "page":
            pages.append(post)
        else:
            posts.append(post)

    return posts, pages


def html_to_markdown(html: str) -> str:
    """
    Convert HTML content to Markdown with custom handling.
    """
    if not html:
        return ""

    # Clean up Squarespace-specific wrapper divs
    html = re.sub(r'<div class="sqs-html-content"[^>]*>', '', html)
    html = html.replace("</div>", "")

    # Convert to markdown using custom converter
    markdown = md(
        html,
        heading_style="ATX",
        bullets="-",
        code_language_callback=lambda _: "",
    )

    # Clean up excessive whitespace
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.strip()

    return markdown


def extract_image_urls(html: str) -> list[str]:
    """Extract all Squarespace image URLs from HTML content."""
    patterns = [
        r'src="(https?://[^"]*squarespace[^"]*)"',
        r'src="(https?://static\.squarespace\.com[^"]*)"',
        r'src="(https?://images\.squarespace-cdn\.com[^"]*)"',
        r'src="(http://static\.squarespace\.com[^"]*)"',
    ]

    urls = []
    for pattern in patterns:
        urls.extend(re.findall(pattern, html))

    return list(set(urls))


def download_image(url: str, output_dir: Path, timeout: float = 30.0) -> Optional[str]:
    """
    Download an image and return the local path.

    Returns:
        Local filename if successful, None otherwise
    """
    try:
        # Create a stable filename based on URL hash
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

        # Try to extract original filename
        parsed = urlparse(url)
        path_parts = parsed.path.split("/")
        original_name = path_parts[-1] if path_parts else "image"

        # Clean up the filename
        original_name = re.sub(r"\?.*$", "", original_name)  # Remove query params
        original_name = re.sub(r"[^a-zA-Z0-9._-]", "_", original_name)

        # Add hash to ensure uniqueness
        ext = Path(original_name).suffix or ".jpg"
        local_filename = f"{url_hash}_{original_name}" if original_name != "image" else f"{url_hash}{ext}"
        local_path = output_dir / local_filename

        if local_path.exists():
            return local_filename

        # Download
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()

            output_dir.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(response.content)

            return local_filename

    except Exception as e:
        print(f"  Warning: Failed to download {url}: {e}")
        return None


def generate_frontmatter(post: Post, image_dir: str = "images") -> str:
    """Generate Quarto-compatible YAML frontmatter."""
    # Combine categories and tags, adding 'personal' to distinguish from technical
    all_categories = ["personal"] + post.categories + post.tags
    all_categories = [c.lower().replace(" ", "-") for c in all_categories]
    all_categories = list(dict.fromkeys(all_categories))  # Preserve order, remove dupes

    # Build frontmatter
    lines = [
        "---",
        f'author: Alex Strick van Linschoten',
        f'categories:',
    ]
    for cat in all_categories:
        lines.append(f'  - {cat}')

    lines.extend([
        f'date: "{post.pub_date.strftime("%Y-%m-%d")}"',
    ])

    # Add description if we have an excerpt
    if post.excerpt:
        # Clean and truncate excerpt
        desc = post.excerpt.strip()[:200]
        desc = desc.replace('"', '\\"')
        lines.append(f'description: "{desc}"')

    lines.extend([
        f'layout: post',
        f'title: "{post.title.replace(chr(34), chr(39))}"',
        f'toc: true',
    ])

    # Add alias for old URL redirect
    if post.alias_path:
        lines.extend([
            f'aliases:',
            f'  - "{post.alias_path}"',
        ])

    # Add Plausible analytics (for alexstrick.com domain)
    lines.append('include-before-body: \'<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>\'')

    # Add Utterances comments
    lines.extend([
        'comments:',
        '  utterances:',
        '    repo: strickvl/mlops-dot-systems',
    ])

    lines.append("---")

    return "\n".join(lines)


def process_post(
    post: Post,
    output_dir: Path,
    image_dir: Path,
    download_images: bool = True,
    dry_run: bool = False,
) -> dict:
    """
    Process a single post: convert to Markdown, download images, write file.

    Returns:
        Dict with processing results
    """
    result = {
        "filename": post.filename,
        "title": post.title,
        "date": post.pub_date.isoformat(),
        "images": [],
        "status": "success",
        "error": None,
    }

    # Extract and optionally download images
    image_urls = extract_image_urls(post.content_html)
    markdown_content = html_to_markdown(post.content_html)

    if download_images and image_urls:
        post_image_dir = image_dir / post.filename.replace(".md", "")

        for url in image_urls:
            if dry_run:
                result["images"].append({"url": url, "status": "would_download"})
            else:
                local_file = download_image(url, post_image_dir)
                if local_file:
                    # Update markdown to use local path
                    relative_path = f"images/{post.filename.replace('.md', '')}/{local_file}"
                    markdown_content = markdown_content.replace(url, relative_path)
                    result["images"].append({"url": url, "local": relative_path, "status": "downloaded"})
                else:
                    result["images"].append({"url": url, "status": "failed"})

    # Generate full post content
    frontmatter = generate_frontmatter(post)
    full_content = f"{frontmatter}\n\n{markdown_content}\n"

    # Write file
    if not dry_run:
        output_path = output_dir / post.filename
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_text(full_content)
        result["path"] = str(output_path)
    else:
        result["preview"] = full_content[:1000] + "..." if len(full_content) > 1000 else full_content

    return result


def main():
    parser = argparse.ArgumentParser(description="Migrate Squarespace export to Quarto")
    parser.add_argument("--xml", required=True, help="Path to Squarespace XML export")
    parser.add_argument("--output", default="personal", help="Output directory for posts")
    parser.add_argument("--images", default=None, help="Directory for downloaded images")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--limit", type=int, default=None, help="Process only N posts (for testing)")
    parser.add_argument("--skip-images", action="store_true", help="Skip image downloading")
    parser.add_argument("--stats", action="store_true", help="Show statistics only")

    args = parser.parse_args()

    xml_path = Path(args.xml)
    output_dir = Path(args.output)
    image_dir = Path(args.images) if args.images else output_dir / "images"

    print(f"Parsing {xml_path}...")
    posts, pages = parse_xml(xml_path)

    print(f"\nFound {len(posts)} posts and {len(pages)} pages")

    if args.stats:
        # Show statistics
        print("\n--- Post Statistics ---")
        years = {}
        categories = {}
        for post in posts:
            year = post.pub_date.year
            years[year] = years.get(year, 0) + 1
            for cat in post.categories:
                categories[cat] = categories.get(cat, 0) + 1

        print("\nPosts by year:")
        for year in sorted(years.keys()):
            print(f"  {year}: {years[year]}")

        print("\nTop categories:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:15]:
            print(f"  {cat}: {count}")

        print("\n--- Sample Posts ---")
        for post in posts[:3]:
            print(f"\n  Title: {post.title}")
            print(f"  Date: {post.pub_date}")
            print(f"  URL: {post.original_url}")
            print(f"  Categories: {post.categories}")
        return

    # Process posts
    if args.limit:
        posts = posts[:args.limit]

    print(f"\nProcessing {len(posts)} posts...")
    results = []

    for i, post in enumerate(posts, 1):
        print(f"  [{i}/{len(posts)}] {post.title[:50]}...")
        result = process_post(
            post,
            output_dir,
            image_dir,
            download_images=not args.skip_images,
            dry_run=args.dry_run,
        )
        results.append(result)

        if args.dry_run and i <= 2:
            print(f"\n    Preview:\n{result.get('preview', 'N/A')[:500]}\n")

    # Summary
    print("\n--- Summary ---")
    success = sum(1 for r in results if r["status"] == "success")
    print(f"Processed: {success}/{len(results)} posts")

    total_images = sum(len(r["images"]) for r in results)
    downloaded = sum(1 for r in results for img in r["images"] if img.get("status") == "downloaded")
    print(f"Images: {downloaded}/{total_images} downloaded")

    if args.dry_run:
        print("\n(Dry run - no files written)")
    else:
        print(f"\nPosts written to: {output_dir}")
        print(f"Images saved to: {image_dir}")


if __name__ == "__main__":
    main()
