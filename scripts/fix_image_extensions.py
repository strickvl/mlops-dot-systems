#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Fix image file extensions based on actual file content.
Some Squarespace images are WebP files with .png or .jpg extensions.
"""

import os
import subprocess
from pathlib import Path


def get_true_extension(file_path: Path) -> str | None:
    """Use `file` command to detect actual image type."""
    try:
        result = subprocess.run(
            ["file", "--brief", str(file_path)],
            capture_output=True,
            text=True,
        )
        output = result.stdout.lower()

        if "web/p" in output or "webp" in output:
            return ".webp"
        elif "png" in output:
            return ".png"
        elif "jpeg" in output or "jpg" in output:
            return ".jpg"
        elif "gif" in output:
            return ".gif"
        return None
    except Exception:
        return None


def fix_extensions(images_dir: Path, dry_run: bool = False) -> dict:
    """Fix all misnamed image files."""
    stats = {"checked": 0, "renamed": 0, "errors": []}

    for root, _, files in os.walk(images_dir):
        for filename in files:
            file_path = Path(root) / filename
            if not file_path.is_file():
                continue

            stats["checked"] += 1
            current_ext = file_path.suffix.lower()
            true_ext = get_true_extension(file_path)

            if true_ext and true_ext != current_ext:
                new_path = file_path.with_suffix(true_ext)
                print(f"  Renaming: {file_path.name} -> {new_path.name}")

                if not dry_run:
                    file_path.rename(new_path)

                    # Update references in markdown files
                    update_markdown_references(
                        images_dir.parent,
                        file_path.name,
                        new_path.name,
                    )

                stats["renamed"] += 1

    return stats


def update_markdown_references(posts_dir: Path, old_name: str, new_name: str):
    """Update markdown files to reference the renamed image."""
    for md_file in posts_dir.glob("*.md"):
        try:
            content = md_file.read_text()
            if old_name in content:
                new_content = content.replace(old_name, new_name)
                md_file.write_text(new_content)
                print(f"    Updated reference in: {md_file.name}")
        except Exception as e:
            print(f"    Error updating {md_file.name}: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fix image extensions")
    parser.add_argument("--dir", default="personal/images", help="Images directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")

    args = parser.parse_args()
    images_dir = Path(args.dir)

    print(f"Scanning {images_dir} for misnamed images...")
    stats = fix_extensions(images_dir, dry_run=args.dry_run)

    print(f"\n--- Summary ---")
    print(f"Checked: {stats['checked']} files")
    print(f"Renamed: {stats['renamed']} files")

    if args.dry_run:
        print("\n(Dry run - no changes made)")


if __name__ == "__main__":
    main()
