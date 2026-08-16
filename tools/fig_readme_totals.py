#!/usr/bin/env python3
"""
fig_readme_totals.py -- generates assets/prize-map.png for the root README.

A dark-theme donut of the biggest unsolved prizes (funded, open or watch), one distinct
colour per slice, with the grand total in the centre. Everything is read from puzzles.json,
so re-running this after an escrow moves keeps the picture honest.

Palette: the validated categorical dark theme (CVD-checked, ORD gates pass on surface
#0d1117). Usage: python3 tools/fig_readme_totals.py
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "puzzles.json"
OUT = ROOT / "assets" / "prize-map.png"

SURFACE = "#0d1117"      # GitHub dark, reads native to a crypto audience
INK = "#f0f6fc"          # primary text
MUTED = "#8b949e"        # secondary text
LEGEND_INK = "#c9d1d9"
# validated categorical dark theme, fixed order (blue, orange, aqua, yellow, magenta, green, violet, red)
PALETTE = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
OTHER = "#6e7681"

SHORT = {
    "gsmg-io-5btc-puzzle": "GSMG.io",
    "ballet-bobby-lee-2btc-cards": "Ballet cards",
    "bitaps-shamir-challenge-1btc": "Bitaps Shamir",
    "aoi-nakamoto-quizchain-0-854btc": "Aoi Quizchain",
    "peter-todd-hash-collision-bounties-0-59btc": "Peter Todd bounties",
    "guntis-vitolins-metamask-8-6eth": "Guntis Vitolins",
    "blm-brave-new-world-0-2btc": "BLM collage",
    "teikhos-bipedaljoe-solver-bounties-2eth": "TeikhosBounty",
    "arweave-puzzle-11-1eth": "Arweave #11",
}


def short_name(p):
    slug = (p.get("folder") or "").split("/")[-1]
    if slug in SHORT:
        return SHORT[slug]
    t = p["title"]
    for sep in (":", " - ", " / "):
        if sep in t:
            t = t.split(sep)[0]
    return t.strip()[:22]


def usd(v):
    return f"${v/1000:.0f}k" if v >= 1000 else f"${v:.0f}"


def main():
    doc = json.load(open(INDEX, encoding="utf-8"))
    funded = [p for p in doc["puzzles"] if p.get("status") in ("open", "watch")]
    total = sum((p["prize"].get("usd_estimate") or 0) for p in funded)

    items = [(short_name(p), p["prize"].get("usd_estimate") or 0)
             for p in funded if (p["prize"].get("usd_estimate") or 0) > 0]
    items.sort(key=lambda x: -x[1])
    top = items[:8]
    rest = items[8:]
    sizes = [v for _n, v in top]
    colors = [PALETTE[i] for i in range(len(top))]
    labels = [n for n, _v in top]
    if rest:
        sizes.append(sum(v for _n, v in rest))
        colors.append(OTHER)
        labels.append(f"{len(rest)} smaller puzzles")

    fig, ax = plt.subplots(figsize=(10.5, 6.0), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.02, right=0.60, top=0.86, bottom=0.06)

    wedges, _ = ax.pie(
        sizes, colors=colors, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.40, edgecolor=SURFACE, linewidth=2.2),
    )
    ax.set(aspect="equal")

    total_rounded = round(total, -3)
    ax.text(0, 0.13, f"${total_rounded:,.0f}", ha="center", va="center",
            fontsize=30, fontweight="bold", color=INK)
    ax.text(0, -0.17, f"{len(funded)} unsolved puzzles\non-chain right now",
            ha="center", va="center", fontsize=12.5, color=MUTED)

    fig.suptitle("Where the unsolved prize money sits", x=0.31, y=0.965,
                 fontsize=17, fontweight="bold", color=INK)

    legend_labels = [f"{n}   {usd(v)}" for n, v in top]
    if rest:
        legend_labels.append(f"{len(rest)} smaller puzzles   {usd(sum(v for _n, v in rest))}")
    leg = ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1.03, 0.5),
                    frameon=False, fontsize=12.5, handlelength=1.2, labelspacing=0.85)
    for txt in leg.get_texts():
        txt.set_color(LEGEND_INK)

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, format="png", facecolor=SURFACE)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
