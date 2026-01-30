#!/usr/bin/env python3
"""
Render all .svg and .pdf files under:
  /Users/markokostiv/Downloads/Easy
  /Users/markokostiv/Downloads/Medium
into JPEGs (PDFs are rendered per-page).

Output goes to a sibling folder next to each source file:
  <source_file_parent>/rendered_jpegs/<relative_path_without_ext>/...

Requires:
  - poppler (for pdftoppm):  brew install poppler
  - for SVGs (pick one):
      A) cairosvg + pillow:  pip install cairosvg pillow
      B) OR inkscape:        brew install inkscape
      C) OR librsvg:         brew install librsvg
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOTS_DEFAULT = [
    Path("/Users/markokostiv/Downloads/Easy"),
    Path("/Users/markokostiv/Downloads/Medium"),
]


def run(cmd: list[str]) -> None:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): {' '.join(cmd)}\n"
            f"STDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}"
        )


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def which(name: str) -> str | None:
    return shutil.which(name)


def render_pdf_to_jpegs(pdf_path: Path, out_dir: Path, dpi: int, quality: int) -> list[Path]:
    """
    Uses pdftoppm to render each page:
      <prefix>-1.jpg, <prefix>-2.jpg, ...
    """
    pdftoppm = which("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm not found. Install poppler: brew install poppler")

    ensure_dir(out_dir)
    prefix = out_dir / pdf_path.stem  # pdftoppm adds -N and .jpg
    cmd = [
        pdftoppm,
        "-jpeg",
        "-r",
        str(dpi),
        "-jpegopt",
        f"quality={quality}",
        str(pdf_path),
        str(prefix),
    ]
    run(cmd)

    # Collect produced files (pdftoppm uses -1, -2, ...)
    produced = sorted(out_dir.glob(f"{pdf_path.stem}-*.jpg"))
    return produced


def render_svg_to_jpeg(svg_path: Path, out_path: Path, dpi: int, quality: int) -> None:
    """
    Tries, in order:
      1) cairosvg + pillow (pure python)
      2) inkscape (CLI)
      3) rsvg-convert + magick (fallback conversion)
    """
    ensure_dir(out_path.parent)

    # 1) cairosvg + pillow
    try:
        import cairosvg  # type: ignore
        from PIL import Image  # type: ignore

        # Render to PNG first (CairoSVG writes PNG well), then convert to JPEG with Pillow.
        tmp_png = out_path.with_suffix(".png")
        # CairoSVG takes "dpi" directly; higher dpi => higher resolution.
        cairosvg.svg2png(url=str(svg_path), write_to=str(tmp_png), dpi=dpi)

        im = Image.open(tmp_png).convert("RGB")
        im.save(out_path, format="JPEG", quality=quality, optimize=True)
        tmp_png.unlink(missing_ok=True)
        return
    except Exception:
        pass

    # 2) inkscape
    inkscape = which("inkscape")
    if inkscape:
        # Inkscape exports PNG; then convert to JPG (either with Pillow if available or sips).
        tmp_png = out_path.with_suffix(".png")
        run(
            [
                inkscape,
                str(svg_path),
                "--export-type=png",
                f"--export-filename={str(tmp_png)}",
                f"--export-dpi={dpi}",
            ]
        )
        # Convert PNG -> JPG via macOS sips (available by default)
        run(
            [
                "sips",
                "-s",
                "format",
                "jpeg",
                "-s",
                "formatOptions",
                str(quality),
                str(tmp_png),
                "--out",
                str(out_path),
            ]
        )
        tmp_png.unlink(missing_ok=True)
        return

    # 3) rsvg-convert (+ optional magick/sips)
    rsvg = which("rsvg-convert")
    if rsvg:
        tmp_png = out_path.with_suffix(".png")
        # librsvg doesn't use dpi directly; use zoom scaling as a proxy.
        # 96 dpi is baseline; scale = dpi/96.
        scale = max(dpi / 96.0, 0.1)
        run([rsvg, "-o", str(tmp_png), "-z", f"{scale}", str(svg_path)])
        run(
            [
                "sips",
                "-s",
                "format",
                "jpeg",
                "-s",
                "formatOptions",
                str(quality),
                str(tmp_png),
                "--out",
                str(out_path),
            ]
        )
        tmp_png.unlink(missing_ok=True)
        return

    raise RuntimeError(
        "No SVG renderer found.\n"
        "Install one of:\n"
        "  pip install cairosvg pillow\n"
        "  brew install inkscape\n"
        "  brew install librsvg\n"
    )


def output_base_for_root(root: Path) -> Path:
    return root / "rendered_jpegs"


def relative_bucket(root: Path, src: Path) -> Path:
    # Put each file into a folder mirroring the tree, without extension
    rel = src.relative_to(root)
    return rel.with_suffix("")


def process_root(root: Path, dpi: int, quality: int, dry_run: bool) -> None:
    if not root.exists():
        print(f"Skipping missing root: {root}", file=sys.stderr)
        return

    out_base = output_base_for_root(root)
    ensure_dir(out_base)

    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".pdf", ".svg"}]
    if not files:
        print(f"No .pdf/.svg files found under {root}")
        return

    for src in sorted(files):
        bucket = out_base / relative_bucket(root, src)
        try:
            if src.suffix.lower() == ".pdf":
                if dry_run:
                    print(f"[DRY] PDF  {src} -> {bucket}/<name>-N.jpg")
                    continue
                produced = render_pdf_to_jpegs(src, bucket, dpi=dpi, quality=quality)
                print(f"PDF  {src} -> {len(produced)} page(s) in {bucket}")
            else:
                out_jpg = bucket / f"{src.stem}.jpg"
                if dry_run:
                    print(f"[DRY] SVG  {src} -> {out_jpg}")
                    continue
                render_svg_to_jpeg(src, out_jpg, dpi=dpi, quality=quality)
                print(f"SVG  {src} -> {out_jpg}")
        except Exception as e:
            print(f"FAILED {src}: {e}", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--quality", type=int, default=92, help="JPEG quality 1-100")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--roots",
        nargs="*",
        default=[str(p) for p in ROOTS_DEFAULT],
        help="Override roots (space-separated paths).",
    )
    args = ap.parse_args()

    roots = [Path(r).expanduser() for r in args.roots]
    for r in roots:
        process_root(r, dpi=args.dpi, quality=args.quality, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
