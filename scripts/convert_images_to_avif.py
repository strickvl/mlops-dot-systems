#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Convert images in personal/images to AVIF format and update markdown references.

Uses ffmpeg with libsvtav1 encoder, which can handle WebP, PNG, JPEG input formats.

Usage:
    uv run scripts/convert_images_to_avif.py --dry-run  # Preview changes
    uv run scripts/convert_images_to_avif.py            # Convert and update
    uv run scripts/convert_images_to_avif.py --delete   # Also delete originals
    uv run scripts/convert_images_to_avif.py --quality 25  # Higher quality (lower CRF)
"""

import argparse
import subprocess
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def find_images(images_dir: Path) -> list[Path]:
    """Find all convertible images in the directory."""
    images = []
    for ext in IMAGE_EXTENSIONS:
        images.extend(images_dir.rglob(f"*{ext}"))
        images.extend(images_dir.rglob(f"*{ext.upper()}"))
    return sorted(set(images))


def convert_image(image_path: Path, dry_run: bool = False, quality: int = 30) -> tuple[Path, bool, str]:
    """
    Convert a single image to AVIF using ffmpeg with libsvtav1 encoder.

    Quality (CRF): 0-63 where 0 is lossless, higher = more compression.
    For web images, 28-35 is a good balance (comparable to JPEG quality 70-80).
    Default is 30 which gives good quality with significant size reduction.

    Note: ffmpeg can handle WebP, PNG, JPEG, and other formats as input.
    """
    avif_path = image_path.with_suffix(".avif")

    if avif_path.exists():
        return image_path, False, "AVIF already exists"

    if dry_run:
        return image_path, True, f"Would convert to {avif_path.name}"

    try:
        # Use ffmpeg with libsvtav1 encoder (fast and good quality)
        # -crf: Constant Rate Factor (0-63, lower = better quality)
        # -preset: Speed/quality tradeoff (0-13, higher = faster)
        # -pix_fmt: Use yuv420p for broad compatibility
        result = subprocess.run(
            [
                "ffmpeg", "-y",  # Overwrite output
                "-i", str(image_path),  # Input file
                "-c:v", "libsvtav1",  # Use SVT-AV1 encoder
                "-crf", str(quality),  # Quality level
                "-preset", "6",  # Balanced speed/quality
                "-pix_fmt", "yuv420p",  # Broad compatibility
                "-an",  # No audio (images don't have audio anyway)
                str(avif_path)
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0 and avif_path.exists():
            # Calculate size reduction
            orig_size = image_path.stat().st_size
            new_size = avif_path.stat().st_size
            if orig_size > 0:
                reduction = (1 - new_size / orig_size) * 100
                ratio = orig_size / new_size if new_size > 0 else 0
                return image_path, True, f"Reduction: {reduction:.1f}% ({ratio:.1f}x smaller)"
            return image_path, True, "Converted successfully"
        else:
            error = result.stderr[:200] if result.stderr else "Unknown error"
            return image_path, False, f"Failed: {error}"
    except subprocess.TimeoutExpired:
        return image_path, False, "Timeout"
    except Exception as e:
        return image_path, False, str(e)


def update_markdown_references(md_dir: Path, dry_run: bool = False) -> dict[str, int]:
    """Update image references in markdown files from old extensions to .avif."""
    stats = {"files_updated": 0, "references_updated": 0}

    # Pattern to match local image references with common extensions
    pattern = re.compile(
        r'(images/[^\s\)\]"\']+)\.(png|jpg|jpeg|webp|gif)',
        re.IGNORECASE
    )

    for md_file in md_dir.glob("*.md"):
        content = md_file.read_text()

        matches = pattern.findall(content)
        if not matches:
            continue

        new_content = pattern.sub(r'\1.avif', content)

        if new_content != content:
            stats["files_updated"] += 1
            stats["references_updated"] += len(matches)

            if dry_run:
                print(f"  Would update {md_file.name}: {len(matches)} references")
            else:
                md_file.write_text(new_content)
                print(f"  Updated {md_file.name}: {len(matches)} references")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Convert images to AVIF and update references")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    parser.add_argument("--delete", action="store_true", help="Delete original images after conversion")
    parser.add_argument("--quality", type=int, default=30, help="CRF quality 0-63 (0=lossless, higher=more compression, default: 30)")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers (default: 4)")
    parser.add_argument("--images-dir", default="personal/images", help="Images directory")
    parser.add_argument("--md-dir", default="personal", help="Markdown directory")
    parser.add_argument("--convert-only", action="store_true", help="Only convert images, don't update markdown")
    parser.add_argument("--update-only", action="store_true", help="Only update markdown, don't convert images")
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    md_dir = Path(args.md_dir)

    if not images_dir.exists():
        print(f"Error: Images directory not found: {images_dir}")
        return 1

    # Convert images (unless --update-only)
    if not args.update_only:
        images = find_images(images_dir)
        print(f"Found {len(images)} images to convert\n")

        if images:
            print("Converting images to AVIF...")
            converted = 0
            failed = 0
            skipped = 0

            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {
                    executor.submit(convert_image, img, args.dry_run, args.quality): img
                    for img in images
                }

                for future in as_completed(futures):
                    img_path, success, message = future.result()
                    if success:
                        converted += 1
                        if not args.dry_run:
                            print(f"  ✓ {img_path.name}: {message}")
                    elif "already exists" in message:
                        skipped += 1
                    else:
                        failed += 1
                        print(f"  ✗ {img_path.name}: {message}")

            print(f"\nConversion: {converted} converted, {skipped} skipped, {failed} failed")

            # Delete originals if requested
            if args.delete and not args.dry_run and converted > 0:
                print("\nDeleting original images...")
                deleted = 0
                for img in images:
                    avif_path = img.with_suffix(".avif")
                    if avif_path.exists() and img.exists():
                        img.unlink()
                        deleted += 1
                print(f"Deleted {deleted} original images")

    # Update markdown references (unless --convert-only)
    if not args.convert_only:
        print("\nUpdating markdown references...")
        stats = update_markdown_references(md_dir, args.dry_run)
        print(f"Markdown: {stats['files_updated']} files, {stats['references_updated']} references updated")

    return 0


if __name__ == "__main__":
    exit(main())
