#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Adds URL aliases to technical posts to preserve old mlops.systems paths.

When mlops.systems redirects to alexstrick.com, these aliases ensure that
paths like /posts/2025-03-16-learnings-building-llms.html continue to work.

Usage:
    uv run scripts/add_technical_post_aliases.py
    uv run scripts/add_technical_post_aliases.py --dry-run
"""

import argparse
import json
import re
from pathlib import Path


def add_alias_to_markdown(filepath: Path, dry_run: bool = False) -> bool:
    """Add alias to a markdown post's frontmatter if not present."""
    content = filepath.read_text()

    # Extract filename to create alias
    # e.g., 2025-03-16-learnings-building-llms.md -> /posts/2025-03-16-learnings-building-llms.html
    stem = filepath.stem
    alias = f"/posts/{stem}.html"

    # Check if aliases already exist
    if "aliases:" in content:
        print(f"  Skipping {filepath.name} (already has aliases)")
        return False

    # Find the end of frontmatter and insert alias before the closing ---
    # Frontmatter is between --- markers
    match = re.match(r"(---\n)(.*?)(---)", content, re.DOTALL)
    if not match:
        print(f"  Skipping {filepath.name} (no frontmatter found)")
        return False

    frontmatter_start = match.group(1)  # "---\n"
    frontmatter_body = match.group(2)   # content between markers
    frontmatter_end = match.group(3)    # "---"

    # Add aliases at the end of frontmatter body
    new_frontmatter_body = frontmatter_body.rstrip() + f'\naliases:\n  - "{alias}"\n'
    new_content = frontmatter_start + new_frontmatter_body + frontmatter_end + content[match.end():]

    if dry_run:
        print(f"  Would add alias to {filepath.name}: {alias}")
    else:
        filepath.write_text(new_content)
        print(f"  Added alias to {filepath.name}: {alias}")

    return True


def add_alias_to_notebook(filepath: Path, dry_run: bool = False) -> bool:
    """Add alias to a Jupyter notebook's frontmatter if not present."""
    content = filepath.read_text()

    try:
        notebook = json.loads(content)
    except json.JSONDecodeError:
        print(f"  Skipping {filepath.name} (invalid JSON)")
        return False

    # Find the first cell with frontmatter (raw cell starting with ---)
    cells = notebook.get("cells", [])
    if not cells:
        print(f"  Skipping {filepath.name} (no cells)")
        return False

    # Look for frontmatter in first few cells
    frontmatter_cell_idx = None
    for idx, cell in enumerate(cells[:3]):
        source = "".join(cell.get("source", []))
        if source.strip().startswith("---") and "---" in source[3:]:
            frontmatter_cell_idx = idx
            break

    if frontmatter_cell_idx is None:
        print(f"  Skipping {filepath.name} (no frontmatter found)")
        return False

    cell = cells[frontmatter_cell_idx]
    source = "".join(cell.get("source", []))

    # Check if aliases already exist
    if "aliases:" in source:
        print(f"  Skipping {filepath.name} (already has aliases)")
        return False

    # Create alias from filename
    stem = filepath.stem
    alias = f"/posts/{stem}.html"

    # Insert alias before the closing ---
    # Find the last --- and insert before it
    lines = source.split("\n")

    # Find the closing --- (should be the last line or near it)
    closing_idx = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "---":
            closing_idx = i
            break

    if closing_idx is None:
        print(f"  Skipping {filepath.name} (no closing --- found)")
        return False

    # Insert alias lines before the closing ---
    alias_lines = [f'aliases:', f'  - "{alias}"']
    new_lines = lines[:closing_idx] + alias_lines + lines[closing_idx:]
    new_source = "\n".join(new_lines)

    if dry_run:
        print(f"  Would add alias to {filepath.name}: {alias}")
    else:
        # Update the cell source (notebooks store source as list of lines)
        cell["source"] = [line + "\n" if i < len(new_lines) - 1 else line
                         for i, line in enumerate(new_lines)]

        # Write back the notebook
        filepath.write_text(json.dumps(notebook, indent=1, ensure_ascii=False))
        print(f"  Added alias to {filepath.name}: {alias}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Add aliases to technical posts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--dir", default="posts", help="Directory containing posts (default: posts)")
    args = parser.parse_args()

    posts_dir = Path(args.dir)
    if not posts_dir.exists():
        print(f"Error: Directory {posts_dir} not found")
        return 1

    modified_md = 0
    modified_ipynb = 0
    skipped = 0

    print(f"Processing markdown files in {posts_dir}/...")
    for md_file in sorted(posts_dir.glob("*.md")):
        if md_file.name == "README.md":
            continue
        if add_alias_to_markdown(md_file, dry_run=args.dry_run):
            modified_md += 1
        else:
            skipped += 1

    print(f"\nProcessing Jupyter notebooks in {posts_dir}/...")
    for ipynb_file in sorted(posts_dir.glob("*.ipynb")):
        if add_alias_to_notebook(ipynb_file, dry_run=args.dry_run):
            modified_ipynb += 1
        else:
            skipped += 1

    print(f"\n{'Would modify' if args.dry_run else 'Modified'}: {modified_md} markdown files, {modified_ipynb} notebooks")
    print(f"Skipped: {skipped} files")

    return 0


if __name__ == "__main__":
    exit(main())
