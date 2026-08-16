#!/usr/bin/env python3
"""
fig_readme_totals.py -- generates assets/prize-map.png for the root README.

A donut of the biggest unsolved prizes (funded, open or watch), each slice colored by its
blockchain, with the grand total in the center. Everything is read from puzzles.json, so
re-running this after an escrow moves keeps the picture honest.

Usage: python3 tools/fig_readme_totals.py
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "puzzles.json"
OUT = ROOT / "assets" / "prize-map.png"

CHAIN_COLOR = {
    "bitcoin": "#F7931A",
    "ethereum": "#627EEA",
    "base": "#3C6DF0",
    "arweave": "#222326",
    "solana": "#14F195",
}
ASSET_COLOR = {"USDT": "#26A17B", "USDC": "#2775CA"}
OTHER = "#B8BCC2"


SHORT = {
    "gsmg-io-5btc-puzzle": "GSMG.io",
    "ballet-bobby-lee-2btc-cards": "Ballet cards",
    "bitaps-shamir-challenge-1btc": "Bitaps Shamir",
    "aoi-nakamoto-quizchain-0-854btc": "Aoi Quizchain",
    "peter-todd-hash-collision-bounties-0-59btc": "Peter Todd bounties",
    "guntis-vitolins-metamask-8-6eth": "Guntis Vitolins",
    "objective-thune-licorne-0-21btc": "Objective Thune",
    "blm-brave-new-world-0-2btc": "BLM collage",
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


def fmt_usd(v):
    if v >= 1000:
        return f"${v/1000:.0f}k"
    return f"${v:.0f}"


def main():
    doc = json.load(open(INDEX, encoding="utf-8"))
    funded = [p for p in doc["puzzles"] if p.get("status") in ("open", "watch")]
    total = sum((p["prize"].get("usd_estimate") or 0) for p in funded)

    items = []
    for p in funded:
        usd = p["prize"].get("usd_estimate") or 0
        if usd <= 0:
            continue
        asset = p["prize"].get("asset")
        color = ASSET_COLOR.get(asset) or CHAIN_COLOR.get(p.get("chain"), OTHER)
        items.append((short_name(p), usd, color, p["prize"]))
    items.sort(key=lambda x: -x[1])

    TOP = 8
    top = items[:TOP]
    rest = items[TOP:]
    sizes = [i[1] for i in top]
    colors = [i[2] for i in top]
    labels = [i[0] for i in top]
    if rest:
        sizes.append(sum(i[1] for i in rest))
        colors.append(OTHER)
        labels.append(f"{len(rest)} smaller puzzles")

    fig, ax = plt.subplots(figsize=(10.5, 6.0), dpi=150)
    fig.subplots_adjust(left=0.01, right=0.60, top=0.86, bottom=0.14)

    wedges, _ = ax.pie(
        sizes, colors=colors, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
    )
    ax.set(aspect="equal")
    ax.text(0, 0.12, fmt_usd(total).replace("k", ",000") if total < 1e6 else f"${total/1e6:.2f}M",
            ha="center", va="center", fontsize=26, fontweight="bold", color="#111111")
    ax.text(0, -0.16, f"{len(funded)} unsolved puzzles\non-chain right now",
            ha="center", va="center", fontsize=12, color="#555555")
    fig.suptitle("Where the unsolved prize money sits", x=0.31, y=0.965, fontsize=17, fontweight="bold", color="#111111")

    # Side legend: name, value, and crypto amount.
    legend_labels = [f"{name}   {fmt_usd(usd)}" for name, usd, _c, _p in top]
    if rest:
        legend_labels.append(f"{len(rest)} smaller puzzles   {fmt_usd(sum(i[1] for i in rest))}")
    ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1.03, 0.5),
              frameon=False, fontsize=12, handlelength=1.2, labelspacing=0.85)

    # Chain-color key along the bottom, clear of the donut.
    key = [("Bitcoin", CHAIN_COLOR["bitcoin"]), ("Ethereum / Base", CHAIN_COLOR["ethereum"]),
           ("smaller puzzles grouped", OTHER)]
    x = 0.03
    for lab, col in key:
        fig.text(x, 0.05, "     ", backgroundcolor=col, fontsize=9)
        fig.text(x + 0.035, 0.045, lab, fontsize=10, color="#333333")
        x += 0.035 + 0.012 * len(lab) + 0.03

    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, format="png")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
