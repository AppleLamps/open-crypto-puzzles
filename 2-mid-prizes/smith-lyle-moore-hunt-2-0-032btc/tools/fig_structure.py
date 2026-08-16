#!/usr/bin/env python3
"""
fig_structure.py -- generate images/02-structure-branches.svg.

Purpose:
    Draw the Wix site as a tree: the shared entry chain (EXIF coordinates, then the
    compass page), fanning out into the 4 branches (North, West, East, South), each drawn
    as a vertical chain of pages colored by state (open, dead-end, locked).

Usage:
    python3 tools/fig_structure.py

Input:
    data/site-structure.csv (branch, step, page_id, state).

Output:
    images/02-structure-branches.svg
"""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_PATH = os.path.join(ROOT, "data", "site-structure.csv")
OUT_PATH = os.path.join(ROOT, "images", "02-structure-branches.svg")

COLOR_OPEN = "#1F5FBF"
COLOR_DEADEND = "#9A9A9A"
COLOR_LOCKED = "#E07A1F"
COLOR_ENTRY = "#1F5FBF"
COLOR_TEXT = "#FFFFFF"
COLOR_BG = "#FFFFFF"
FONT = "DejaVu Sans"

STATE_COLOR = {"open": COLOR_OPEN, "dead-end": COLOR_DEADEND, "locked": COLOR_LOCKED}
STATE_LABEL = {"open": "open", "dead-end": "dead end", "locked": "locked (insight gate)"}

BOX_W = 140
BOX_H = 44
COL_GAP = 30
ROW_GAP = 12
MARGIN = 30
TOP_H = 90


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(line for line in f if not line.startswith("#"))]

    branches = []
    seen = set()
    for r in rows:
        if r["branch"] not in seen:
            seen.add(r["branch"])
            branches.append(r["branch"])
    by_branch = {b: [r for r in rows if r["branch"] == b] for b in branches}

    n_cols = len(branches)
    max_rows = max(len(v) for v in by_branch.values())
    width = MARGIN * 2 + n_cols * BOX_W + (n_cols - 1) * COL_GAP
    height = MARGIN + TOP_H + max_rows * (BOX_H + ROW_GAP) + MARGIN + 30

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">'
    )
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="{COLOR_BG}"/>')

    entry_w = 260
    entry_x = width / 2 - entry_w / 2
    entry_y = MARGIN
    parts.append(
        f'<rect x="{entry_x}" y="{entry_y}" width="{entry_w}" height="{BOX_H}" rx="8" '
        f'fill="{COLOR_ENTRY}" stroke="#14406e" stroke-width="1.5"/>'
    )
    parts.append(
        f'<text x="{width/2}" y="{entry_y + BOX_H/2 - 4}" text-anchor="middle" font-size="12" '
        f'fill="{COLOR_TEXT}">entry: image EXIF -> compass</text>'
    )
    parts.append(
        f'<text x="{width/2}" y="{entry_y + BOX_H/2 + 12}" text-anchor="middle" font-size="10" '
        f'fill="{COLOR_TEXT}">3 pages, open, reveals 4 branch passwords</text>'
    )

    col_xs = []
    for ci in range(n_cols):
        cx = MARGIN + ci * (BOX_W + COL_GAP)
        col_xs.append(cx)

    branch_top_y = MARGIN + TOP_H
    for ci, branch in enumerate(branches):
        cx = col_xs[ci]
        parts.append(
            f'<text x="{cx + BOX_W/2}" y="{branch_top_y - 14}" text-anchor="middle" '
            f'font-size="13" font-weight="bold" fill="#111111">{esc(branch)}</text>'
        )
        parts.append(
            f'<line x1="{width/2}" y1="{entry_y + BOX_H}" x2="{cx + BOX_W/2}" '
            f'y2="{branch_top_y}" stroke="#666666" stroke-width="1.2"/>'
        )
        rows_b = by_branch[branch]
        prev_bottom = None
        for ri, r in enumerate(rows_b):
            by = branch_top_y + ri * (BOX_H + ROW_GAP)
            color = STATE_COLOR[r["state"]]
            parts.append(
                f'<rect x="{cx}" y="{by}" width="{BOX_W}" height="{BOX_H}" rx="6" '
                f'fill="{color}" stroke="#222222" stroke-width="1"/>'
            )
            parts.append(
                f'<text x="{cx + BOX_W/2}" y="{by + 18}" text-anchor="middle" '
                f'font-size="12" font-weight="bold" fill="{COLOR_TEXT}">{esc(r["page_id"])}</text>'
            )
            parts.append(
                f'<text x="{cx + BOX_W/2}" y="{by + 34}" text-anchor="middle" '
                f'font-size="9.5" fill="{COLOR_TEXT}">{esc(STATE_LABEL[r["state"]])}</text>'
            )
            if prev_bottom is not None:
                parts.append(
                    f'<line x1="{cx + BOX_W/2}" y1="{prev_bottom}" x2="{cx + BOX_W/2}" '
                    f'y2="{by}" stroke="#666666" stroke-width="1.2"/>'
                )
            prev_bottom = by + BOX_H

    legend_y = height - 22
    lx = MARGIN
    for label, color in [
        ("open", COLOR_OPEN), ("dead end", COLOR_DEADEND), ("locked (insight gate)", COLOR_LOCKED)
    ]:
        parts.append(f'<rect x="{lx}" y="{legend_y - 10}" width="14" height="14" fill="{color}"/>')
        parts.append(f'<text x="{lx + 20}" y="{legend_y + 1}" font-size="11" fill="#111111">{esc(label)}</text>')
        lx += 190

    parts.append("</svg>")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    main()
