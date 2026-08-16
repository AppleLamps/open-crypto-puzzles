#!/usr/bin/env python3
"""
fig_pipeline.py -- generates images/02-pipeline-derivation.svg

Purpose:
    Draw the confirmed derivation and authorization pipeline, from a 12-word BIP39
    candidate through to the withdraw() call on the Base pot contract. Every box
    label and the contract addresses come from data/pipeline-stages.json.

Usage:
    python3 tools/fig_pipeline.py

Input:
    data/pipeline-stages.json

Output:
    images/02-pipeline-derivation.svg
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "pipeline-stages.json"
OUT_FILE = ROOT / "images" / "02-pipeline-derivation.svg"

BLUE = "#1F5FBF"
GRAY = "#9A9A9A"
INK = "#222222"


def main() -> None:
    with open(DATA_FILE, encoding="utf-8") as f:
        spec = json.load(f)
    stages = spec["stages"]

    box_w, box_h = 180, 90
    gap = 50
    n = len(stages)
    width = n * box_w + (n - 1) * gap + 40
    height = 300

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="DejaVu Sans, sans-serif">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>',
        '<defs><marker id="arrow2" markerWidth="10" markerHeight="10" refX="6" refY="3" '
        f'orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{INK}"/></marker></defs>',
    ]

    y0 = 90
    for i, stage in enumerate(stages):
        x = 20 + i * (box_w + gap)
        parts.append(f'<rect x="{x}" y="{y0}" width="{box_w}" height="{box_h}" rx="8" '
                      f'fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
        lines = stage["label"].split("\n")
        ty = y0 + 30 - (len(lines) - 1) * 8
        for line in lines:
            parts.append(f'<text x="{x + box_w / 2}" y="{ty}" font-size="13" '
                          f'font-weight="bold" fill="{INK}" text-anchor="middle">{line}</text>')
            ty += 18
        note_lines = _wrap(stage.get("note", ""), 24)
        ny = y0 + box_h + 18
        for nl in note_lines:
            parts.append(f'<text x="{x + box_w / 2}" y="{ny}" font-size="11" fill="{GRAY}" '
                          f'text-anchor="middle">{nl}</text>')
            ny += 14
        if i < n - 1:
            ax = x + box_w
            ay = y0 + box_h / 2
            parts.append(f'<line x1="{ax}" y1="{ay}" x2="{ax + gap}" y2="{ay}" '
                          f'stroke="{INK}" stroke-width="2" marker-end="url(#arrow2)"/>')

    parts.append(f'<text x="20" y="30" font-size="16" font-weight="bold" fill="{INK}">'
                  f'12 words to withdraw() authorization</text>')
    parts.append(f'<text x="20" y="52" font-size="12" fill="{GRAY}">'
                  f'winner wallet {spec["winner_wallet"]} is the only address withdraw() accepts, '
                  f'selector {spec["withdraw_selector"]}</text>')

    parts.append("</svg>")
    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")


def _wrap(text, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


if __name__ == "__main__":
    main()
