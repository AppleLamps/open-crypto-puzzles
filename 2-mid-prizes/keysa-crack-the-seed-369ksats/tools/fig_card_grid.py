#!/usr/bin/env python3
"""
fig_card_grid.py -- generate images/01-annotated-card-grid.png.

Purpose:
    Show the published ciphertext card next to a legend panel that renders the 70
    transcribed tokens, laid out in the same 6 rows of 12/12/11/12/12/11, with the 12
    tokens that carry no trailing dot on the card highlighted. This is the "12
    dotless tokens" set enumerated exhaustively in analysis/tested.md (L-001, 0
    match under all 479,001,600 orderings).

    The original card pixels are kept untouched; the legend is a separate panel
    below the image, not an overlay on it, since word-level pixel coordinates are
    not part of the transcription this folder ships.

Usage:
    python3 tools/fig_card_grid.py

Input:
    clues/L9rQ.jpg (the published card, untouched).
    data/card-tokens.txt (my transcription, dots mark tokens with a trailing period).

Output:
    images/01-annotated-card-grid.png
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CARD_PATH = os.path.join(ROOT, "clues", "L9rQ.jpg")
TOKENS_PATH = os.path.join(ROOT, "data", "card-tokens.txt")
OUT_PATH = os.path.join(ROOT, "images", "01-annotated-card-grid.png")

COLOR_DOTLESS = "#E07A1F"   # unknown / under test: the 12 dotless tokens
COLOR_TEXT = "#1a1a1a"
COLOR_BG = "#FFFFFF"

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_rows():
    rows = []
    with open(TOKENS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            row = [(t.rstrip("."), t.endswith(".")) for t in tokens]
            rows.append(row)
    return rows


def main():
    card = Image.open(CARD_PATH).convert("RGB")
    rows = load_rows()

    font = ImageFont.truetype(FONT_PATH, 15)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 15)
    font_small = ImageFont.truetype(FONT_PATH, 12)

    legend_h = 40 + len(rows) * 30 + 40
    width = max(card.width, 1100)
    height = card.height + legend_h

    canvas = Image.new("RGB", (width, height), COLOR_BG)
    canvas.paste(card, ((width - card.width) // 2, 0))

    draw = ImageDraw.Draw(canvas)
    y = card.height + 15
    draw.text(
        (20, y),
        "My transcription (data/card-tokens.txt), 70 tokens in 6 rows of 12/12/11/12/12/11:",
        font=font_bold,
        fill=COLOR_TEXT,
    )
    y += 25

    for row in rows:
        x = 20
        for word, dotted in row:
            color = COLOR_TEXT if dotted else COLOR_DOTLESS
            label = word if dotted else word
            bbox = draw.textbbox((x, y), label, font=font)
            w = bbox[2] - bbox[0]
            if not dotted:
                draw.rounded_rectangle(
                    [x - 3, y - 2, x + w + 3, y + 16], radius=4, outline=COLOR_DOTLESS, width=2
                )
            draw.text((x, y), label, font=font, fill=color)
            x += w + 14
        y += 30

    y += 10
    draw.rectangle([20, y, 34, y + 14], outline=COLOR_DOTLESS, width=2)
    draw.text(
        (40, y - 1),
        "outlined = the 12 tokens with no trailing dot on the card (L-001, exhausted: 479,001,600 orderings, 0 match)",
        font=font_small,
        fill=COLOR_TEXT,
    )

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    canvas.save(OUT_PATH, "PNG", optimize=True)
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes), size {canvas.size}")


if __name__ == "__main__":
    main()
