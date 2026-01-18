#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic",
#     "pyyaml",
# ]
# ///
"""
Generate SEO-friendly descriptions for blog posts using Claude Haiku.

Reads markdown files, extracts content, sends to Claude Haiku for a
one-sentence description, and updates the YAML frontmatter.

Usage:
    # Preview first 5 posts (dry run)
    uv run scripts/generate_descriptions.py --dir personal --limit 5 --dry-run

    # Process first 5 posts
    uv run scripts/generate_descriptions.py --dir personal --limit 5

    # Process all posts
    uv run scripts/generate_descriptions.py --dir personal

    # Skip posts that already have descriptions
    uv run scripts/generate_descriptions.py --dir personal --skip-existing

Environment:
    ANTHROPIC_API_KEY: Your Anthropic API key
"""

import argparse
import os
import re
import sys
from pathlib import Path

import anthropic
import yaml


# Claude Haiku model - cheapest and fastest option
MODEL = "claude-haiku-4-5-20251001"

# System prompt for generating descriptions
SYSTEM_PROMPT = """You are helping a blogger write descriptions for their posts. The blogger writes in a personal, first-person style.

Your task: Write a natural description that captures what the post is about.

Style guidelines (based on existing descriptions):
- Use first-person ("I built...", "I learned...", "How I trained...") when the post describes something the author did
- Use third-person or neutral phrasing for more abstract/educational content
- Keep it natural - can be a sentence fragment or a full sentence
- Be specific about what the post covers
- Don't pad with filler words or generic phrases
- Don't start with "This post..." or "In this article..."
- Don't use quotes in your response

Examples of good descriptions:
- "I published a dataset from my previous work as a researcher in Afghanistan."
- "How I used Prodigy to annotate my data ahead of training an object detection model."
- "A working setup for controlling your Python environment."
- "Some reflections on the idea of what it is that we do as software engineers."
- "Explores when and how to implement finetuning effectively."

Respond with ONLY the description, nothing else."""


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """
    Extract YAML frontmatter and body from markdown content.

    Returns:
        Tuple of (frontmatter_dict, body_content)
        frontmatter_dict is None if no valid frontmatter found
    """
    # Match YAML frontmatter between --- delimiters
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None, content

    try:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    except yaml.YAMLError as e:
        print(f"  Warning: Failed to parse YAML: {e}")
        return None, content


def update_frontmatter_with_description(content: str, description: str) -> str:
    """
    Add or update the description field in the YAML frontmatter.

    Preserves the original formatting as much as possible by doing
    a targeted insertion rather than re-serializing the whole YAML.
    """
    # Find the frontmatter section
    pattern = r'^(---\s*\n)(.*?)(\n---\s*\n)(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return content

    start_delimiter = match.group(1)
    frontmatter_text = match.group(2)
    end_delimiter = match.group(3)
    body = match.group(4)

    # Escape any special characters in description for YAML
    # Use single quotes if the description contains double quotes
    if '"' in description:
        escaped_desc = f"'{description}'"
    else:
        escaped_desc = f'"{description}"'

    # Check if description already exists
    if re.search(r'^description:', frontmatter_text, re.MULTILINE):
        # Replace existing description
        frontmatter_text = re.sub(
            r'^description:.*$',
            f'description: {escaped_desc}',
            frontmatter_text,
            flags=re.MULTILINE
        )
    else:
        # Insert description after date field (to maintain consistent ordering)
        # If date not found, insert after title
        if re.search(r'^date:', frontmatter_text, re.MULTILINE):
            frontmatter_text = re.sub(
                r'^(date:.*?)$',
                rf'\1\ndescription: {escaped_desc}',
                frontmatter_text,
                flags=re.MULTILINE
            )
        elif re.search(r'^title:', frontmatter_text, re.MULTILINE):
            frontmatter_text = re.sub(
                r'^(title:.*?)$',
                rf'\1\ndescription: {escaped_desc}',
                frontmatter_text,
                flags=re.MULTILINE
            )
        else:
            # Just append at the end of frontmatter
            frontmatter_text += f'\ndescription: {escaped_desc}'

    return f"{start_delimiter}{frontmatter_text}{end_delimiter}{body}"


def generate_description(client: anthropic.Anthropic, title: str, content: str) -> str:
    """
    Call Claude Haiku to generate a description for the blog post.
    """
    # Truncate content if too long (keep first ~3000 chars for efficiency)
    truncated_content = content[:3000]
    if len(content) > 3000:
        truncated_content += "\n\n[Content truncated...]"

    user_message = f"""Blog post title: {title}

Blog post content:
{truncated_content}

Write a description for this blog post:"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,  # Allow for longer, natural descriptions
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    # Extract the text from the response
    description = response.content[0].text.strip()

    # Clean up any stray quotes the model might have added
    description = description.strip('"\'')

    return description


def process_file(
    file_path: Path,
    client: anthropic.Anthropic | None,
    dry_run: bool = False,
    skip_existing: bool = False,
) -> dict:
    """
    Process a single markdown file.

    Returns:
        Dict with processing results
    """
    result = {
        "file": file_path.name,
        "status": "success",
        "description": None,
        "skipped_reason": None,
    }

    content = file_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        result["status"] = "skipped"
        result["skipped_reason"] = "no valid frontmatter"
        return result

    title = frontmatter.get("title", "Untitled")

    # Check if description already exists
    if skip_existing and frontmatter.get("description"):
        result["status"] = "skipped"
        result["skipped_reason"] = "already has description"
        result["description"] = frontmatter["description"]
        return result

    if dry_run:
        result["status"] = "would_process"
        result["title"] = title
        result["content_preview"] = body[:200] + "..." if len(body) > 200 else body
        return result

    # Generate description using Claude
    try:
        description = generate_description(client, title, body)
        result["description"] = description

        # Update the file
        updated_content = update_frontmatter_with_description(content, description)
        file_path.write_text(updated_content, encoding="utf-8")

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate descriptions for blog posts using Claude Haiku"
    )
    parser.add_argument(
        "--dir",
        default="personal",
        help="Directory containing markdown files (default: personal)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only N files (for testing)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without making API calls or writing files"
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip files that already have a description"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show more detail about each file"
    )

    args = parser.parse_args()

    # Check for API key (unless dry run)
    if not args.dry_run:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("Error: ANTHROPIC_API_KEY environment variable not set")
            print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
            sys.exit(1)
        client = anthropic.Anthropic()
    else:
        client = None

    # Find markdown files
    dir_path = Path(args.dir)
    if not dir_path.exists():
        print(f"Error: Directory '{args.dir}' not found")
        sys.exit(1)

    md_files = sorted(dir_path.glob("*.md"))

    if not md_files:
        print(f"No markdown files found in {args.dir}")
        sys.exit(0)

    print(f"Found {len(md_files)} markdown files in {args.dir}")

    if args.limit:
        md_files = md_files[:args.limit]
        print(f"Processing first {args.limit} files")

    if args.dry_run:
        print("(Dry run - no API calls or file writes)")

    print()

    # Process files
    results = []
    for i, file_path in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] {file_path.name}...", end=" ")

        result = process_file(
            file_path,
            client,
            dry_run=args.dry_run,
            skip_existing=args.skip_existing,
        )
        results.append(result)

        if result["status"] == "success":
            print(f"✓")
            if args.verbose and result["description"]:
                print(f"    → {result['description']}")
        elif result["status"] == "skipped":
            print(f"⊘ ({result['skipped_reason']})")
        elif result["status"] == "would_process":
            print(f"[dry run]")
            if args.verbose:
                print(f"    Title: {result.get('title', 'N/A')}")
        elif result["status"] == "error":
            print(f"✗ Error: {result.get('error', 'Unknown')}")

    # Summary
    print("\n--- Summary ---")
    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    errors = sum(1 for r in results if r["status"] == "error")
    would_process = sum(1 for r in results if r["status"] == "would_process")

    if args.dry_run:
        print(f"Would process: {would_process}")
        print(f"Would skip: {skipped}")
    else:
        print(f"Processed: {success}")
        print(f"Skipped: {skipped}")
        if errors:
            print(f"Errors: {errors}")

    # Show sample descriptions if verbose
    if args.verbose and not args.dry_run:
        print("\n--- Sample Descriptions ---")
        for r in results[:5]:
            if r["description"]:
                print(f"\n{r['file']}:")
                print(f"  {r['description']}")


if __name__ == "__main__":
    main()
