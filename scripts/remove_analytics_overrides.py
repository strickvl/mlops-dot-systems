#!/usr/bin/env python3
"""
Removes include-before-body analytics overrides from all posts.

After the Plausible domain rename (mlops.systems → alexstrick.com), the global
_quarto.yml config handles analytics for all pages. Individual post overrides
are no longer needed and should be removed.

This script removes lines like:
  include-before-body: '<script defer data-domain="..." src="..."></script>'

from the YAML frontmatter of markdown files.

Usage:
    uv run scripts/remove_analytics_overrides.py --dry-run  # Preview changes
    uv run scripts/remove_analytics_overrides.py            # Apply changes
"""

import re
from pathlib import Path
from typing import NamedTuple


class Result(NamedTuple):
    path: Path
    removed: bool
    error: str | None = None


def remove_analytics_override(filepath: Path, dry_run: bool = False) -> Result:
    """Remove include-before-body from a post's frontmatter."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return Result(filepath, False, str(e))

    if "include-before-body:" not in content:
        return Result(filepath, False)

    # Pattern matches include-before-body with single-line or multi-line values
    # Single-line: include-before-body: '<script...>'
    # Multi-line:  include-before-body:
    #                '<script...>'
    patterns = [
        # Single-line format
        r"include-before-body:\s*'[^']*'\n",
        r'include-before-body:\s*"[^"]*"\n',
        # Multi-line format (indented continuation)
        r"include-before-body:\s*\n\s+'[^']*'\n",
        r'include-before-body:\s*\n\s+"[^"]*"\n',
        # Multi-line with pipe or > continuation
        r"include-before-body:\s*\|\s*\n(?:\s+[^\n]+\n)+",
    ]

    new_content = content
    for pattern in patterns:
        new_content = re.sub(pattern, "", new_content)

    if new_content == content:
        # Pattern didn't match but include-before-body exists - try simpler approach
        lines = content.split("\n")
        new_lines = []
        skip_next_indented = False

        for i, line in enumerate(lines):
            if "include-before-body:" in line:
                # Check if value is on same line
                if "'" in line or '"' in line:
                    skip_next_indented = False
                    continue  # Skip this line
                else:
                    # Value is on next line(s)
                    skip_next_indented = True
                    continue
            elif skip_next_indented and line.startswith(("  ", "\t")):
                continue  # Skip indented continuation
            else:
                skip_next_indented = False
                new_lines.append(line)

        new_content = "\n".join(new_lines)

    if new_content == content:
        return Result(filepath, False)

    # Clean up any double blank lines created by removal
    new_content = re.sub(r"\n{3,}", "\n\n", new_content)

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")

    return Result(filepath, True)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Remove include-before-body analytics overrides from posts"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all files processed, not just modified ones",
    )
    args = parser.parse_args()

    directories = [Path("posts"), Path("personal"), Path("til")]
    results: list[Result] = []

    for directory in directories:
        if not directory.exists():
            continue
        for md_file in directory.rglob("*.md"):
            result = remove_analytics_override(md_file, dry_run=args.dry_run)
            results.append(result)

    # Also check root .qmd files (but probably don't have overrides)
    for qmd_file in Path(".").glob("*.qmd"):
        result = remove_analytics_override(qmd_file, dry_run=args.dry_run)
        results.append(result)

    # Summary
    modified = [r for r in results if r.removed]
    errors = [r for r in results if r.error]

    if args.dry_run:
        print("=== DRY RUN (no changes made) ===\n")

    if modified:
        print(f"{'Would modify' if args.dry_run else 'Modified'} {len(modified)} files:")
        for r in modified:
            print(f"  {r.path}")
    else:
        print("No files needed modification.")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for r in errors:
            print(f"  {r.path}: {r.error}")

    if args.verbose:
        skipped = [r for r in results if not r.removed and not r.error]
        print(f"\nSkipped {len(skipped)} files (no include-before-body found)")

    print(f"\nTotal files scanned: {len(results)}")


if __name__ == "__main__":
    main()
