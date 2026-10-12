#!/usr/bin/env python3
"""
montage.py — compose labelled sheets of screenshots for the deliverables.

Lays out the five phone screens side by side on one light sheet with captions,
so the PDF shows the whole flow in a single figure instead of one tall image
per page.

Usage:
    python tools/montage.py docs/tugas-3-prototype/screenshots
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# (file stem, caption, use-case tag)
SCREENS = [
    ("screen-connect",  "Hubungkan", "UC-01"),
    ("screen-control",  "Kontrol",   "UC-02/03/04"),
    ("screen-sensor",   "Sensor",    "UC-06"),
    ("screen-mode",     "Mode",      "UC-05"),
    ("screen-settings", "Setelan",   "—"),
]

BG = (244, 247, 251)
INK = (15, 44, 77)
MUTED = (91, 107, 127)
LINE = (213, 222, 232)
FONT = "segoeui.ttf"
FONT_B = "segoeuib.ttf"


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for base in (r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu"):
        p = Path(base) / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    # fall back to DejaVu names on Linux, else default
    for alt in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
        p = Path("/usr/share/fonts/truetype/dejavu") / alt
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def main() -> None:
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/tugas-3-prototype/screenshots")
    mode = sys.argv[2] if len(sys.argv) > 2 else "all"
    if mode == "detail":
        build_detail(folder)
    else:
        build_sheet(folder)
        build_detail(folder)


def build_sheet(folder: Path) -> None:
    f_title = load_font(FONT_B, 40)
    f_cap = load_font(FONT_B, 26)
    f_tag = load_font(FONT, 21)

    # target phone height on the sheet
    ph = 900
    pad = 54
    gap = 40
    header = 150
    footer = 70
    caption_h = 76

    tiles = []
    for stem, cap, tag in SCREENS:
        p = folder / f"{stem}.png"
        if not p.exists():
            sys.exit(f"missing {p}")
        im = Image.open(p).convert("RGB")
        w = round(im.width * ph / im.height)
        tiles.append((im.resize((w, ph), Image.LANCZOS), cap, tag))

    tile_w = tiles[0][0].width
    W = pad * 2 + len(tiles) * tile_w + (len(tiles) - 1) * gap
    H = header + caption_h + ph + footer

    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)

    # header
    d.text((pad, 40), "Prototype Hi-Fi — Aplikasi Kontrol Mobil RC IoT", font=f_title, fill=INK)
    d.text((pad, 96), "Tugas 3 · Tim Ecayci Lover · Application Project II · 390 × 844 px",
           font=f_tag, fill=MUTED)

    x = pad
    for im, cap, tag in tiles:
        # caption above the phone
        d.text((x, header), cap, font=f_cap, fill=INK)
        cw = d.textlength(cap, font=f_cap)
        d.text((x + cw + 12, header + 5), tag, font=f_tag, fill=MUTED)

        y = header + caption_h
        # drop shadow + phone
        d.rounded_rectangle([x + 6, y + 8, x + im.width + 6, y + im.height + 8],
                            radius=26, fill=(225, 231, 240))
        sheet.paste(im, (x, y))
        d.rounded_rectangle([x, y, x + im.width - 1, y + im.height - 1],
                            radius=24, outline=LINE, width=2)
        x += im.width + gap

    out = folder / "prototype-sheet.png"
    sheet.save(out, optimize=True)
    print(f"  -> {out}  ({sheet.width}x{sheet.height}, {out.stat().st_size/1024:.0f} KB)")


def build_detail(folder: Path) -> None:
    """Two-up detail sheet (Kontrol + Sensor) at a larger scale."""
    f_cap = load_font(FONT_B, 30)
    f_tag = load_font(FONT, 22)

    picks = [("screen-control", "Layar Kontrol", "UC-02 · UC-03 · UC-04"),
             ("screen-sensor",  "Layar Sensor",  "UC-06")]

    ph = 1180
    pad = 56
    gap = 56
    caption_h = 78
    footer = 56

    tiles = []
    for stem, cap, tag in picks:
        im = Image.open(folder / f"{stem}.png").convert("RGB")
        w = round(im.width * ph / im.height)
        tiles.append((im.resize((w, ph), Image.LANCZOS), cap, tag))

    W = pad * 2 + sum(t[0].width for t in tiles) + gap * (len(tiles) - 1)
    H = caption_h + ph + footer + 40

    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)

    x = pad
    for im, cap, tag in tiles:
        d.text((x, 34), cap, font=f_cap, fill=INK)
        cw = d.textlength(cap, font=f_cap)
        d.text((x + cw + 14, 42), tag, font=f_tag, fill=MUTED)

        y = caption_h
        d.rounded_rectangle([x + 6, y + 8, x + im.width + 6, y + im.height + 8],
                            radius=30, fill=(225, 231, 240))
        sheet.paste(im, (x, y))
        d.rounded_rectangle([x, y, x + im.width - 1, y + im.height - 1],
                            radius=28, outline=LINE, width=2)
        x += im.width + gap

    out = folder / "detail-sheet.png"
    sheet.save(out, optimize=True)
    print(f"  -> {out}  ({sheet.width}x{sheet.height}, {out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
