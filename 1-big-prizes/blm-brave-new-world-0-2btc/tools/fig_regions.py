#!/usr/bin/env python3
"""
fig_regions.py -- generates images/01-annotated-regions.png

Purpose:
    Draw the 3 measured regions listed in data/candidate-regions.json (dial, monument,
    rune column) as boxes over the published puzzle collage, so a reader can see where
    on the image the candidate signal sits without hunting through the full 1600x1200
    original. Every box and label comes from the data file; nothing here is invented.

Usage:
    python3 tools/fig_regions.py

Input:
    clues/welcome-to-the-brave-new-world.png (the published puzzle image)
    data/candidate-regions.json (region boxes and labels)

Output:
    images/01-annotated-regions.png
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
REGIONS_FILE = ROOT / "data" / "candidate-regions.json"
OUT_FILE = ROOT / "images" / "01-annotated-regions.png"

ACCENT = (224, 122, 31)  # unknown/candidate orange, docs/illustrations.md palette


def main() -> None:
    with open(REGIONS_FILE, encoding="utf-8") as f:
        spec = json.load(f)

    im = Image.open(ROOT / spec["image"]).convert("RGB")

    # Downscale to keep the PNG under the 500 KB / 1600 px illustration cap while
    # keeping the boxes legible; original is already 1600 px on the long side.
    max_side = 900
    scale = min(1.0, max_side / max(im.size))
    if scale < 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)

    draw = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except OSError:
        font = ImageFont.load_default()

    for region in spec["regions"]:
        x0, y0, x1, y1 = [c * scale for c in region["box"]]
        draw.rectangle([x0, y0, x1, y1], outline=ACCENT, width=4)
        label = region["label"]
        text_y = max(0, y0 - 26)
        # White backing rectangle so the label reads over any part of the collage.
        text_w = draw.textlength(label, font=font)
        draw.rectangle([x0, text_y, x0 + text_w + 8, text_y + 24], fill=(255, 255, 255))
        draw.text((x0 + 4, text_y + 2), label, fill=ACCENT, font=font)

    OUT_FILE.parent.mkdir(exist_ok=True)
    quantized = im.quantize(colors=192, method=Image.MEDIANCUT)
    quantized.save(OUT_FILE, format="PNG", optimize=True)
    print(f"wrote {OUT_FILE} ({OUT_FILE.stat().st_size} bytes, {im.size})")


if __name__ == "__main__":
    main()
