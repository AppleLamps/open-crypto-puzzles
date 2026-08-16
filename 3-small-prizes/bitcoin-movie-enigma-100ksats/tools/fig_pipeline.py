#!/usr/bin/env python3
"""
fig_pipeline.py -- generate images/01-pipeline-derivation.svg.

Purpose:
    Draw the derivation pipeline described in the puzzle's own published rules
    (bitcoinmovieenigma.com/rules): 34 movie panels to 34 titles to 34 BIP39 words,
    drop 10 intruders to get 24 words, then BIP39 to BIP84 to the P2WPKH address.

Usage:
    python3 tools/fig_pipeline.py

Input:
    data/pipeline-stages.json (stage labels and edge labels).

Output:
    images/01-pipeline-derivation.svg
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_PATH = os.path.join(ROOT, "data", "pipeline-stages.json")
OUT_PATH = os.path.join(ROOT, "images", "01-pipeline-derivation.svg")

BOX_W = 160
BOX_H = 66
GAP = 76
MARGIN = 30
FONT = "DejaVu Sans"

COLOR_BOX = "#1F5FBF"
COLOR_TEXT = "#FFFFFF"
COLOR_EDGE = "#333333"
COLOR_BG = "#FFFFFF"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    stages = data["stages"]

    n = len(stages)
    width = MARGIN * 2 + n * BOX_W + (n - 1) * GAP
    height = 280

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">'
    )
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="{COLOR_BG}"/>')

    y = height // 2 - BOX_H // 2
    x = MARGIN
    centers = []
    for stage in stages:
        cx = x + BOX_W / 2
        centers.append((x, cx))
        parts.append(
            f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="8" '
            f'fill="{COLOR_BOX}" stroke="#14406e" stroke-width="1.5"/>'
        )
        lines = stage["label"].split("\n")
        line_h = 14
        start_ty = y + BOX_H / 2 - (len(lines) - 1) * line_h / 2 + 5
        for li, line in enumerate(lines):
            parts.append(
                f'<text x="{cx}" y="{start_ty + li * line_h}" text-anchor="middle" '
                f'font-size="11" fill="{COLOR_TEXT}">{esc(line)}</text>'
            )
        x += BOX_W + GAP

    for i in range(1, n):
        prev_right = centers[i - 1][0] + BOX_W
        this_left = centers[i][0]
        mid_y = y + BOX_H / 2
        parts.append(
            f'<line x1="{prev_right}" y1="{mid_y}" x2="{this_left - 8}" y2="{mid_y}" '
            f'stroke="{COLOR_EDGE}" stroke-width="1.5" marker-end="url(#arrow)"/>'
        )
        edge_label = stages[i].get("edge")
        if edge_label:
            label_x = (prev_right + this_left) / 2
            edge_lines = edge_label.split("\n")
            line_h = 12
            base_y = mid_y - 18 - (len(edge_lines) - 1) * line_h
            for li, line in enumerate(edge_lines):
                parts.append(
                    f'<text x="{label_x}" y="{base_y + li * line_h}" text-anchor="middle" '
                    f'font-size="9" fill="{COLOR_EDGE}">{esc(line)}</text>'
                )

    parts.append(
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#333333"/></marker></defs>'
    )
    parts.append("</svg>")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    main()
