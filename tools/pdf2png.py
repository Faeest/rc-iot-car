#!/usr/bin/env python3
"""
pdf2png.py — rasterise PDF pages to PNG so the rendered result can be reviewed
(exactly what a grader sees), without needing a PDF viewer.

Usage:
    python tools/pdf2png.py docs/tugas-2-srs.pdf .scratch/srs --scale 1.4
    python tools/pdf2png.py docs/tugas-2-srs.pdf .scratch/srs --pages 1-3
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pypdfium2 as pdfium


def parse_pages(spec: str, total: int) -> list[int]:
    """'1-3,5' -> [0,1,2,4]  (0-based)."""
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a) - 1, int(b)))
        elif part:
            out.append(int(part) - 1)
    return [p for p in out if 0 <= p < total]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("prefix", help="output path prefix, e.g. .scratch/srs")
    ap.add_argument("--scale", type=float, default=1.5)
    ap.add_argument("--pages", default="", help="e.g. 1-3,5 (default: all)")
    args = ap.parse_args()

    doc = pdfium.PdfDocument(args.pdf)
    n = len(doc)
    idxs = parse_pages(args.pages, n) if args.pages else list(range(n))

    prefix = Path(args.prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)

    print(f"{args.pdf}: {n} page(s)")
    for i in idxs:
        page = doc[i]
        img = page.render(scale=args.scale).to_pil()
        out = prefix.parent / f"{prefix.name}-p{i+1}.png"
        img.save(out)
        print(f"  page {i+1} -> {out}  ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
