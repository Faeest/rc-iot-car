#!/usr/bin/env python3
"""
gen_diagrams.py — generate SVG diagrams for the course deliverables.

Everything is emitted as hand-built SVG (no Graphviz/Mermaid needed, neither of
which is installed here). Output goes to docs/assets/.

Usage:
    python tools/gen_diagrams.py            # writes all diagrams
    python tools/gen_diagrams.py usecase    # writes one
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets"

NAVY = "#0f2c4d"
NAVY2 = "#1b4b7a"
ACCENT = "#0ea5e9"
INK = "#1a2230"
LINE = "#8aa0b8"
SOFT = "#f4f7fb"
FONT = "Segoe UI, Inter, Helvetica Neue, Arial, sans-serif"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_open(w: int, h: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{FONT}">',
        "<defs>",
        # arrow head for association lines
        f'<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" '
        f'orient="auto" markerUnits="strokeWidth">'
        f'<path d="M0,0 L8,3 L0,6 z" fill="{LINE}"/></marker>',
        f'<marker id="arrowOpen" markerWidth="14" markerHeight="12" refX="11" refY="6" '
        f'orient="auto" markerUnits="strokeWidth">'
        f'<path d="M0,0 L11,6 L0,12" fill="none" stroke="{LINE}" stroke-width="1.4"/></marker>',
        "<style>",
        f".lbl {{ font-size: 15px; fill: {INK}; }}",
        f".uc {{ font-size: 15px; fill: {INK}; }}",
        f".rel {{ font-size: 12.5px; fill: {NAVY2}; font-style: italic; }}",
        f".actor {{ font-size: 14px; fill: {NAVY}; font-weight: 600; }}",
        f".title {{ font-size: 17px; fill: {NAVY}; font-weight: 700; }}",
        f".sub {{ font-size: 12px; fill: #5b6b7f; }}",
        "</style>",
        "</defs>",
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
    ]


def ellipse(cx: float, cy: float, rx: float, ry: float, lines: list[str]) -> list[str]:
    out = [
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{SOFT}" stroke="{NAVY2}" stroke-width="1.6"/>'
    ]
    n = len(lines)
    lh = 18
    y0 = cy - (n - 1) * lh / 2
    for i, ln in enumerate(lines):
        out.append(
            f'<text class="uc" x="{cx}" y="{y0 + i*lh + 5}" '
            f'text-anchor="middle">{esc(ln)}</text>'
        )
    return out


def actor(cx: float, ytop: float, label: str) -> list[str]:
    """Stick figure; returns svg parts. Figure spans ytop..ytop+150."""
    hx, hy, hr = cx, ytop + 20, 19
    body_top, body_bot = hy + hr, ytop + 100
    return [
        f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="none" stroke="{NAVY}" stroke-width="2"/>',
        f'<line x1="{hx}" y1="{body_top}" x2="{hx}" y2="{body_bot}" stroke="{NAVY}" stroke-width="2"/>',
        f'<line x1="{hx-30}" y1="{body_top+22}" x2="{hx+30}" y2="{body_top+22}" stroke="{NAVY}" stroke-width="2"/>',
        f'<line x1="{hx}" y1="{body_bot}" x2="{hx-26}" y2="{ytop+150}" stroke="{NAVY}" stroke-width="2"/>',
        f'<line x1="{hx}" y1="{body_bot}" x2="{hx+26}" y2="{ytop+150}" stroke="{NAVY}" stroke-width="2"/>',
        f'<text class="actor" x="{hx}" y="{ytop+178}" text-anchor="middle">{esc(label)}</text>',
    ]


def line(p1, p2, dashed=False, arrow=False) -> str:
    d = ' stroke-dasharray="7,5"' if dashed else ""
    m = ' marker-end="url(#arrow)"' if arrow else ""
    return (
        f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" '
        f'stroke="{LINE}" stroke-width="1.5"{d}{m}/>'
    )


def polyline(points, dashed=True, arrow=True) -> str:
    pts = " ".join(f"{x},{y}" for x, y in points)
    d = ' stroke-dasharray="7,5"' if dashed else ""
    m = ' marker-end="url(#arrowOpen)"' if arrow else ""
    return (
        f'<polyline points="{pts}" fill="none" stroke="{LINE}" '
        f'stroke-width="1.5"{d}{m}/>'
    )


def text(x, y, s, cls="lbl", anchor="middle") -> str:
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(s)}</text>'


def label_bg(x, y, s, cls="rel", anchor="middle", pad=5) -> list[str]:
    """Text with a white plate behind it so it stays readable over a line."""
    w = len(s) * 7.2 + pad * 2
    h = 20
    if anchor == "middle":
        x0 = x - w / 2
    elif anchor == "start":
        x0 = x - pad
    else:
        x0 = x - w + pad
    return [
        f'<rect x="{x0}" y="{y - 14}" width="{w}" height="{h}" fill="#ffffff" '
        f'opacity="0.92" rx="3"/>',
        f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(s)}</text>',
    ]


# --------------------------------------------------------------------------- #
# Diagram 1 — use case
# --------------------------------------------------------------------------- #
def use_case_diagram() -> str:
    W, H = 1160, 900
    bx, by, bw, bh = 275, 50, 570, 800
    cx, rx, ry = 560, 185, 38

    # use case centres (top -> bottom)
    ucs = {
        "UC1": (176, ["Menghubungkan ke Mobil"]),
        "UC2": (288, ["Mengendalikan Gerak Mobil"]),
        "UC3": (400, ["Mengatur Kecepatan"]),
        "UC4": (512, ["Menghentikan Mobil", "(E-Stop)"]),
        "UC5": (624, ["Mengaktifkan Mode", "Hindari Rintangan"]),
        "UC6": (742, ["Memantau Jarak Ultrasonik"]),
    }

    p: list[str] = svg_open(W, H)

    # system boundary
    p.append(
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" '
        f'fill="#fbfdff" stroke="{NAVY}" stroke-width="1.8" stroke-dasharray="9,5"/>'
    )
    p.append(text(cx, by + 32, "Sistem Kontrol Mobil RC IoT", "title"))
    p.append(text(cx, by + 54, "(firmware Arduino Uno + aplikasi kontrol)", "sub"))

    # use case ellipses
    for key, (yc, lines) in ucs.items():
        p += ellipse(cx, yc, rx, ry, lines)

    # actor: Pengguna (primary)
    peng_x, peng_top = 118, 320
    p += actor(peng_x, peng_top, "Pengguna")
    anchor = (peng_x + 30, peng_top + 42)  # right hand
    for key in ("UC1", "UC2", "UC3", "UC4", "UC5"):
        yc = ucs[key][0]
        p.append(line(anchor, (cx - rx, yc)))

    # actor: Sensor Ultrasonik (secondary / supporting)
    sen_x, sen_top = 1048, 660
    p += actor(sen_x, sen_top, "Sensor Ultrasonik")
    p.append(line((sen_x - 30, sen_top + 42), (cx + rx, ucs["UC6"][0])))

    # <<include>> UC5 -> UC6  (vertical, adjacent ellipses)
    y5, y6 = ucs["UC5"][0], ucs["UC6"][0]
    p.append(polyline([(cx, y5 + ry), (cx, y6 - ry)], dashed=True, arrow=True))
    p += label_bg(cx + 46, (y5 + ry + y6 - ry) / 2 + 5, "«include»", anchor="start")

    # <<extend>> UC4 -> UC2  (right-hand routing, clear of the ellipses)
    y2, y4 = ucs["UC2"][0], ucs["UC4"][0]
    xr = 848
    p.append(polyline(
        [(cx + rx, y4), (xr, y4), (xr, y2), (cx + rx, y2)], dashed=True, arrow=True
    ))
    p += label_bg(xr, (y2 + y4) / 2 + 5, "«extend»", anchor="middle")

    p.append("</svg>")
    return "\n".join(p)


DIAGRAMS = {"usecase": ("usecase-diagram.svg", use_case_diagram)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[1:] or list(DIAGRAMS)
    for name in wanted:
        if name not in DIAGRAMS:
            sys.exit(f"unknown diagram: {name} (have: {', '.join(DIAGRAMS)})")
        fname, fn = DIAGRAMS[name]
        path = OUT / fname
        path.write_text(fn(), encoding="utf-8")
        print(f"  {name} -> {path.relative_to(ROOT)}  ({path.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
