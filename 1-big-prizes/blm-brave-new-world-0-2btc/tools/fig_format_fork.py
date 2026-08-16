#!/usr/bin/env python3
"""
fig_format_fork.py -- generates images/02-format-fork.svg

Purpose:
    Show the 3 coupled unknowns in the BLM derivation and the 2 candidate seed formats,
    each backed by a distinct set of words that appear only on that format's side of the
    fork. Every unknown, format name, path, and word list is read from
    data/format-fork.json, not hard-coded here.

Usage:
    python3 tools/fig_format_fork.py

Input:
    data/format-fork.json

Output:
    images/02-format-fork.svg
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "format-fork.json"
OUT_FILE = ROOT / "images" / "02-format-fork.svg"

ORANGE = "#E07A1F"   # unknown
BLUE = "#1F5FBF"     # confirmed structure (paths are confirmed derivation code, not answers)
GRAY = "#9A9A9A"
INK = "#222222"


def wrap_words(words, per_line=5):
    lines = []
    for i in range(0, len(words), per_line):
        lines.append(", ".join(words[i:i + per_line]))
    return lines


def main() -> None:
    with open(DATA_FILE, encoding="utf-8") as f:
        spec = json.load(f)

    unknowns = spec["unknowns"]
    formats = spec["formats"]

    width, height = 860, 560
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="DejaVu Sans, sans-serif">'
    )
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>')

    # Title
    parts.append(f'<text x="20" y="32" font-size="20" font-weight="bold" fill="{INK}">'
                  f'3 coupled unknowns, 2 candidate formats</text>')

    # Unknowns row
    parts.append(f'<text x="20" y="64" font-size="14" fill="{INK}">Unknown:</text>')
    ux = 110
    for i, unk in enumerate(unknowns):
        bw = 8 * len(unk) + 24
        parts.append(f'<rect x="{ux}" y="46" width="{bw}" height="28" rx="6" '
                      f'fill="none" stroke="{ORANGE}" stroke-width="2"/>')
        parts.append(f'<text x="{ux + bw / 2}" y="65" font-size="13" fill="{INK}" '
                      f'text-anchor="middle">{i + 1}. {unk}</text>')
        ux += bw + 16

    # Arrow down to the fork
    parts.append(f'<line x1="{width / 2}" y1="90" x2="{width / 2}" y2="130" '
                  f'stroke="{INK}" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append('<defs><marker id="arrow" markerWidth="10" markerHeight="10" '
                  'refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" '
                  f'fill="{INK}"/></marker></defs>')
    parts.append(f'<text x="{width / 2}" y="122" font-size="13" fill="{INK}" '
                  f'text-anchor="middle">which format?</text>')

    # Two format boxes
    box_w, box_h = 380, 340
    gap = 40
    total_w = box_w * 2 + gap
    x0 = (width - total_w) / 2
    y0 = 150
    for i, fmt in enumerate(formats):
        bx = x0 + i * (box_w + gap)
        parts.append(f'<rect x="{bx}" y="{y0}" width="{box_w}" height="{box_h}" rx="10" '
                      f'fill="none" stroke="{BLUE}" stroke-width="2"/>')
        parts.append(f'<text x="{bx + box_w / 2}" y="{y0 + 34}" font-size="17" '
                      f'font-weight="bold" fill="{INK}" text-anchor="middle">{fmt["name"]}</text>')
        parts.append(f'<text x="{bx + box_w / 2}" y="{y0 + 58}" font-size="13" fill="{INK}" '
                      f'text-anchor="middle">{fmt["path"]}</text>')
        parts.append(f'<text x="{bx + 16}" y="{y0 + 90}" font-size="13" fill="{INK}">'
                      f'Exclusive words on the image ({len(fmt["exclusive_words"])}):</text>')
        ty = y0 + 114
        for line in wrap_words(fmt["exclusive_words"], per_line=3):
            parts.append(f'<text x="{bx + 16}" y="{ty}" font-size="13" fill="{ORANGE}">{line}</text>')
            ty += 22
        parts.append(f'<text x="{bx + 16}" y="{y0 + box_h - 20}" font-size="12" fill="{GRAY}">'
                      f'settled if one of these words is confirmed as a real seed word</text>')

    parts.append('</svg>')

    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
