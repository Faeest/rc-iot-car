#!/usr/bin/env python3
"""
shot.py — screenshot a local HTML file (or a URL) with headless Chrome.

Usage:
    python tools/shot.py docs/tugas-2-srs.html out.png
    python tools/shot.py docs/tugas-2-srs.html out.png --width 1200 --full
    python tools/shot.py http://localhost:8080 out.png --full
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    for n in ("google-chrome", "chromium", "chrome"):
        if shutil.which(n):
            return shutil.which(n)  # type: ignore[return-value]
    sys.exit("ERROR: no Chrome/Chromium found")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="HTML file path or URL")
    ap.add_argument("out", help="output PNG path")
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--full", action="store_true", help="capture full page height")
    ap.add_argument("--scale", type=float, default=1.0)
    args = ap.parse_args()

    target = args.target
    if not target.startswith(("http://", "https://", "file://")):
        target = Path(target).resolve().as_uri()

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="chrome-shot-") as profile:
        cmd = [
            find_chrome(),
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--hide-scrollbars",
            f"--user-data-dir={profile}",
            f"--window-size={args.width},{args.height}",
            f"--screenshot={out}",
            f"--force-device-scale-factor={args.scale}",
        ]
        if args.full:
            cmd.append("--screenshot-full-page")
        cmd.append(target)
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not out.exists():
            sys.stderr.write(res.stdout + res.stderr)
            sys.exit(f"ERROR: screenshot failed -> {out}")
    print(f"  -> {out}  ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
