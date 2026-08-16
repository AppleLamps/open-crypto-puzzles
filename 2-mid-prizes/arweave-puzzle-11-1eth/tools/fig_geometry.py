#!/usr/bin/env python3
"""
fig_geometry.py -- generates images/01-annotated-geometry.png

Purpose:
    Draw the 12 measured building bounding boxes and the large sailboat bounding box
    over the published puzzle image, so a reader can see the geometry that was fed
    into the roughly 460 negative derivation candidates without re-running the
    measurement. Every box comes from data/geometry.json; nothing here is invented.

Usage:
    python3 tools/fig_geometry.py

Input:
    clues/arweave-puzzle-11.png (the published puzzle image)
    data/geometry.json (measured bounding boxes)

Output:
    images/01-annotated-geometry.png
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "geometry.json"
OUT_FILE = ROOT / "images" / "01-annotated-geometry.png"

CONFIRMED = (31, 95, 191)   # measured geometry, docs/illustrations.md "confirmed" blue
UNKNOWN = (224, 122, 31)    # decoy / unresolved, "unknown" orange


def main() -> None:
    with open(DATA_FILE, encoding="utf-8") as f:
        spec = json.load(f)

    im = Image.open(ROOT / spec["image"]).convert("L").convert("RGB")

    # Downscale to keep the PNG under the 500 KB illustration cap.
    max_side = 1100
    scale = min(1.0, max_side / max(im.size))
    if scale < 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)

    draw = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except OSError:
        font = ImageFont.load_default()

    for b in spec["buildings"]:
        box = [b["x0"] * scale, b["roof_y"] * scale, b["x1"] * scale, b["bottom_y"] * scale]
        draw.rectangle(box, outline=CONFIRMED, width=2)
        draw.text((box[0] + 2, box[1] - 16), f'B{b["id"]}', fill=CONFIRMED, font=font)

    sb = spec["large_sailboat"]
    sbox = [sb["x0"] * scale, sb["y0"] * scale, sb["x1"] * scale, sb["y1"] * scale]
    draw.rectangle(sbox, outline=CONFIRMED, width=3)
    draw.text((sbox[0] + 2, sbox[1] - 20), "large sailboat", fill=CONFIRMED, font=font)

    draw.text((10, 10), "12 buildings + 1 sailboat measured (blue); 5 small sail widths"
                         " measured but not positioned; tEXt-chunk address is a confirmed decoy",
              fill=UNKNOWN, font=font)

    OUT_FILE.parent.mkdir(exist_ok=True)
    quantized = im.quantize(colors=192, method=Image.MEDIANCUT)
    quantized.save(OUT_FILE, format="PNG", optimize=True)
    print(f"wrote {OUT_FILE} ({OUT_FILE.stat().st_size} bytes, {im.size})")


if __name__ == "__main__":
    main()
