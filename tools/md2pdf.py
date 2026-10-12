#!/usr/bin/env python3
"""
md2pdf.py — convert a course deliverable (Markdown) into a print-ready PDF.

Pipeline:  Markdown --(python-markdown)--> styled HTML --(headless Chrome)--> PDF

Why not pandoc/wkhtmltopdf? Neither is installed on this machine. Chrome is, and
its headless `--print-to-pdf` renders the same CSS @page rules a browser would,
so the PDF matches the on-screen design.

Usage:
    python tools/md2pdf.py docs/tugas-2-srs.md
    python tools/md2pdf.py docs/*.md                 # all deliverables
    python tools/md2pdf.py docs/tugas-2-srs.md --html  # keep the intermediate HTML

The document may start with a small YAML-ish front matter block delimited by
`---` lines; recognised keys become the cover page. Example:

    ---
    title: Software Requirements Specification
    subtitle: Aplikasi Kontrol Mobil RC IoT
    kicker: Tugas 2 — Praktik
    course: Application Project II
    lecturer: Jozua Ferjanus Palandi
    team: Ecayci Lover
    author: Faiz Ramadhan (241111011), Dico Havianto (241111017)
    date: 2026
    repo: https://github.com/Faeest/rc-iot-car
    ---
"""

from __future__ import annotations

import argparse
import html
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "tools" / "style" / "print.css"

# Candidate Chrome/Edge executables (Windows + POSIX).
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

FRONT_MATTER_KEYS = [
    "title", "subtitle", "kicker", "course", "lecturer",
    "team", "author", "date", "repo", "nim",
]


def find_chrome() -> str:
    for cand in CHROME_CANDIDATES:
        if Path(cand).exists():
            return cand
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit(
        "ERROR: no Chrome/Edge/Chromium found. Install one, or print the "
        "intermediate HTML from a browser manually (--html)."
    )


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Return (metadata, body). Front matter is optional."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    meta: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return meta, "\n".join(lines[i + 1:]).lstrip("\n")
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip().lower()] = val.strip()
    return {}, text  # unterminated -> treat whole thing as body


def cover_html(meta: dict[str, str]) -> str:
    if not meta:
        return ""

    def row(label: str, key: str) -> str:
        val = meta.get(key, "")
        return f"<dt>{html.escape(label)}</dt><dd>{html.escape(val)}</dd>" if val else ""

    title = html.escape(meta.get("title", ""))
    subtitle = html.escape(meta.get("subtitle", ""))
    kicker = html.escape(meta.get("kicker", ""))

    # Repo link is rendered as a real anchor.
    repo = meta.get("repo", "")
    repo_row = (
        f'<dt>Repositori</dt><dd><a href="{html.escape(repo)}">'
        f"{html.escape(repo)}</a></dd>"
        if repo
        else ""
    )

    rows = "".join([
        row("Mata Kuliah", "course"),
        row("Dosen Pengampu", "lecturer"),
        row("Nama Tim", "team"),
        row("Anggota", "author"),
        repo_row,
        row("Tanggal", "date"),
    ])

    return f"""<section class="cover">
  <div class="kicker">{kicker}</div>
  <h1>{title}</h1>
  <div class="subtitle">{subtitle}</div>
  <div class="rule"></div>
  <dl>{rows}</dl>
  <div class="foot">Dokumen ini disusun untuk memenuhi tugas mata kuliah
  Application Project II — Program Studi Teknik Informatika.</div>
</section>"""


def tighten_code_columns(content: str) -> str:
    """Add `nowrap` to a table's first column when its cells are short codes.

    Requirement tables start with codes like FR-01 / NFR-01 / UC-01 that look
    bad when wrapped ("FR-" / "01"). Long label columns must still wrap, so the
    rule is applied only when every first-column cell is short.
    """
    import re

    def fix(match: re.Match[str]) -> str:
        table = match.group(0)
        first_cells = re.findall(r"<tr>\s*<t[hd][^>]*>(.*?)</t[hd]>", table, re.S)
        texts = [re.sub(r"<[^>]+>", "", c).strip() for c in first_cells]
        if texts and all(len(t) <= 12 for t in texts if t):
            return table.replace("<table>", '<table class="codes">', 1)
        return table

    return re.sub(r"<table>.*?</table>", fix, content, flags=re.S)


def build_html(body_md: str, meta: dict[str, str]) -> str:
    md = markdown.Markdown(
        extensions=[
            "extra",          # tables, fenced_code, attr_list, def_list, ...
            "sane_lists",
            "toc",
            "admonition",
            "md_in_html",
            "pymdownx.tilde",
            "pymdownx.caret",
            "pymdownx.mark",
            "pymdownx.smartsymbols",
            "pymdownx.tasklist",
            "pymdownx.superfences",
        ],
        extension_configs={"toc": {"permalink": False, "toc_depth": "1-3"}},
    )
    content = md.convert(body_md)
    content = tighten_code_columns(content)

    # python-markdown's toc extension returns a <div class="toc"> wrapper; we
    # supply our own wrapper (with the "Daftar Isi" label via CSS ::before), so
    # unwrap the inner <ul> to avoid a doubled heading.
    toc = md.toc
    if toc:
        start, end = toc.find("<ul"), toc.rfind("</ul>")
        if start != -1 and end != -1:
            toc = toc[start:end + len("</ul>")]

    # Place the TOC at the very top of the body (before the first heading), so
    # the running order is: cover -> daftar isi -> content.
    toc_block = f'<nav class="toc">{toc}</nav>\n'
    if "[[TOC]]" in body_md:
        content = content.replace("[[TOC]]", toc_block)
    elif toc:
        content = toc_block + content

    css = CSS.read_text(encoding="utf-8")
    title = html.escape(meta.get("title", "Dokumen"))
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
{cover_html(meta)}
<main>
{content}
</main>
</body>
</html>"""


def html_to_pdf(chrome: str, html_path: Path, pdf_path: Path) -> None:
    html_path = html_path.resolve()
    pdf_path = pdf_path.resolve()
    with tempfile.TemporaryDirectory(prefix="chrome-pdf-") as profile:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--no-pdf-header-footer",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if not pdf_path.exists():
            sys.stderr.write(res.stdout + res.stderr)
            sys.exit(f"ERROR: Chrome failed to produce {pdf_path}")


def convert(src: Path, keep_html: bool = False, open_pdf: bool = False) -> Path:
    if not src.exists():
        sys.exit(f"ERROR: {src} not found")
    raw = src.read_text(encoding="utf-8")
    meta, body = split_front_matter(raw)
    if "title" not in meta:
        meta["title"] = src.stem.replace("-", " ").title()

    out_html = src.with_suffix(".html")
    out_html.write_text(build_html(body, meta), encoding="utf-8")

    pdf = src.with_suffix(".pdf")
    html_to_pdf(find_chrome(), out_html, pdf)

    if not keep_html:
        out_html.unlink()

    size_kb = pdf.stat().st_size / 1024
    print(f"  {src.name}  ->  {pdf.name}  ({size_kb:.0f} KB)")
    if open_pdf:
        os.startfile(pdf)  # type: ignore[attr-defined]  # Windows only
    return pdf


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="Markdown file(s) to convert")
    ap.add_argument("--html", action="store_true",
                    help="keep the intermediate HTML next to the PDF")
    ap.add_argument("--open", action="store_true", help="open the PDF when done")
    args = ap.parse_args()

    print("Converting Markdown -> PDF ...")
    for pattern in args.sources:
        for src in sorted(Path().glob(pattern)) if any(
            ch in pattern for ch in "*?["
        ) else [Path(pattern)]:
            convert(src, keep_html=args.html, open_pdf=args.open)
    print("Done.")


if __name__ == "__main__":
    main()
