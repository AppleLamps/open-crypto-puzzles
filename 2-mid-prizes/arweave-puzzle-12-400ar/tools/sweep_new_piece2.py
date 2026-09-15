#!/usr/bin/env python3
"""Bounded sweep of NEW piece-2 strings for Arweave Puzzle Weave #12.

Does not repeat tested.md rows 1-19. Those already killed AndreessenHorowitz,
the 137 curated 18-character investor/Forbes/date/whale-species list, hex-code
pairings with 16-03-2020 and a16z, joint-naming, and tincture-length branches.

This run covers three cheap leftover families:

  A. 18-character piece-2 strings that are organisations, founder names,
     Forbes-article *initiatives* (Grants + Boost), or whale+date concatenations
     (the piece draws both), not the investor spelling already swept.
  B. piece 2 as an 8-character date (16032020 and close forms) with piece 1 =
     the six flag hex codes plus a 2-character suffix (IQ / AR), length 38.
  C. blank flag read as Cerulean (the sampled whale fill is #20a0c8) so piece 1
     is 32 characters, pairing with a 14-character piece-2.

Piece 3 is fixed at 2111011. Piece 4 is the five-letter anagram set plus a few
visual reading orders. Block order is 1-2-3-4.

Usage:
  python3 sweep_new_piece2.py           # full sweep
  python3 sweep_new_piece2.py --count   # print N and exit
  python3 sweep_new_piece2.py --rate    # 40-candidate timing probe, then exit
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle  # noqa: E402

P3 = "2111011"

# Five dictionary anagrams in the three cases used by row 14, plus four visual
# reading orders of the five letters as drawn (I top-left, E top-right, A centre,
# N bottom-left, L bottom-right).
P4 = [
    "Alien", "ALIEN", "alien",
    "Aline", "Anile", "Elain", "Liane",
    "IEANL", "IEALN", "IENAL",
]

# Geometry: three vertical pairs from measured centroids.
LEFT = ("red", "purple_dark")   # top, bottom
MID = ("gray", "green")
RIGHT = ("violet", "blank")

ORDERS = [
    # column-major, 4 directions
    (LEFT[0], LEFT[1], MID[0], MID[1], RIGHT[0], RIGHT[1]),
    (LEFT[1], LEFT[0], MID[1], MID[0], RIGHT[1], RIGHT[0]),
    (RIGHT[0], RIGHT[1], MID[0], MID[1], LEFT[0], LEFT[1]),
    (RIGHT[1], RIGHT[0], MID[1], MID[0], LEFT[1], LEFT[0]),
    # row-major tops-then-bottoms / bottoms-then-tops, LTR and RTL
    (LEFT[0], MID[0], RIGHT[0], LEFT[1], MID[1], RIGHT[1]),
    (RIGHT[0], MID[0], LEFT[0], RIGHT[1], MID[1], LEFT[1]),
    (LEFT[1], MID[1], RIGHT[1], LEFT[0], MID[0], RIGHT[0]),
    (RIGHT[1], MID[1], LEFT[1], RIGHT[0], MID[0], LEFT[0]),
    # y-scanline (down / up) and boustrophedon rows
    ("gray", "violet", "red", "green", "blank", "purple_dark"),
    ("purple_dark", "blank", "green", "red", "violet", "gray"),
    (LEFT[0], MID[0], RIGHT[0], RIGHT[1], MID[1], LEFT[1]),
    (RIGHT[0], MID[0], LEFT[0], LEFT[1], MID[1], RIGHT[1]),
]

PURPLE_NAMES = ("Purple", "Violet", "Indigo")
GRAY_NAMES = ("Gray", "Grey")

P2_18_PASCAL = [
    "PermawebFoundation",
    "ArweavesFoundation",
    "ThePermawebArweave",
    "BlockweaveProtocol",
    "PermanentDataStore",
    "MinimumEndowmentAR",
    "StorageEndowmentAR",
    "PermanentStorageAR",
    "CommunityEcosystem",
    "ArweaveGrantsBoost",
    "SamWilliamsFounder",
    "SamWilliamsArweave",
    "BlueWhale16March20",
    "BlueWhale16Mar2020",
    "BlueWhaleMarch2020",
    "TheBlueWhale160320",
    "SpermWhaleOrca2020",
    "OrcinusOrca16March",
    "CyanWhale16March20",
    "AndreessenA16zFund",
    "A16zCryptoPartners",
    "CoinbaseVenturesAH",
    "ArweaveSeedRound20",
    "MichaelHaleyForbes",
    "ArweaveNewsMarch20",
    "EightPoint3Million",
    "EmpowerThePermaweb",
    "LibraryAlexandriaA",
    "HaltCensorshipARWV",
    "ArweaveBoostGrants",
]

P2_8 = [
    "16032020",
    "20200316",
    "16-03-20",
    "16.03.20",
    "16/03/20",
    "16 03 20",
]

P2_14 = [
    "AndreessenA16z",
    "a16zCryptoFund",
    "SixteenMarch20",
    "A16zSixteenMar",
    "CoinbasePlusAH",
]

HEX = {
    "red": "c00000",
    "purple_dark": "410080",
    "gray": "808080",
    "green": "3f8000",
    "violet": "7f00ff",
}


def _colour_name(flag, gray, p_dark, p_light, blank):
    return {
        "red": "Red",
        "green": "Green",
        "gray": gray,
        "purple_dark": p_dark,
        "violet": p_light,
        "blank": blank,
    }[flag]


def piece1_colour_names(blank="Blue"):
    out = []
    for order, gray, p_dark, p_light in product(ORDERS, GRAY_NAMES, PURPLE_NAMES, PURPLE_NAMES):
        out.append("".join(_colour_name(f, gray, p_dark, p_light, blank) for f in order))
    return out


def piece1_hex_plus_suffix():
    out = []
    blanks = ("ffffff", "0000ff", "20a0c8")
    suffixes = ("IQ", "AR")
    for order, blank, suffix, upper in product(ORDERS, blanks, suffixes, (False, True)):
        parts = []
        for f in order:
            hx = HEX[f] if f != "blank" else blank
            parts.append(hx.upper() if upper else hx)
        out.append("".join(parts) + suffix)
    return out


def p2_18_all_cases():
    # Sibling #8 is PascalCase concatenated proper nouns. ALLCAPS / lowercase
    # of these new strings would triple N past the two-hour budget at the
    # measured single-core rate; they are not generated here.
    return list(P2_18_PASCAL)


def assemble():
    """Yield (family, candidate) 58-character strings."""
    p1_blue = piece1_colour_names("Blue")
    for p1, p2, p4 in product(p1_blue, p2_18_all_cases(), P4):
        yield "A", p1 + p2 + P3 + p4
    p1_hex = piece1_hex_plus_suffix()
    for p1, p2, p4 in product(p1_hex, P2_8, P4):
        yield "B", p1 + p2 + P3 + p4
    p1_cer = piece1_colour_names("Cerulean")
    for p1, p2, p4 in product(p1_cer, P2_14, P4):
        yield "C", p1 + p2 + P3 + p4


def _validate_lengths():
    for s in P2_18_PASCAL:
        if len(s) != 18:
            raise SystemExit("P2_18 length %d: %r" % (len(s), s))
    for s in P2_8:
        if len(s) != 8:
            raise SystemExit("P2_8 length %d: %r" % (len(s), s))
    for s in P2_14:
        if len(s) != 14:
            raise SystemExit("P2_14 length %d: %r" % (len(s), s))
    p1b = piece1_colour_names("Blue")
    if any(len(s) != 28 for s in p1b):
        raise SystemExit("piece-1 Blue names are not all 28")
    p1c = piece1_colour_names("Cerulean")
    if any(len(s) != 32 for s in p1c):
        raise SystemExit("piece-1 Cerulean names are not all 32")
    p1h = piece1_hex_plus_suffix()
    if any(len(s) != 38 for s in p1h):
        raise SystemExit("piece-1 hex+suffix are not all 38")
    n = {"A": 0, "B": 0, "C": 0}
    for fam, cand in assemble():
        if len(cand) != 58:
            raise SystemExit("assembled length %d in family %s" % (len(cand), fam))
        n[fam] += 1
    return n


def _probe_one(cand):
    head = oracle.decode_wallet(oracle.CIPHERTEXT_B64, cand, first_block_only=True)
    return oracle.GATE in head


def _worker(cands):
    hits = []
    n = 0
    for cand in cands:
        n += 1
        head = oracle.decode_wallet(oracle.CIPHERTEXT_B64, cand, first_block_only=True)
        if oracle.GATE in head:
            ok, addr = oracle.check(cand, fast=False)
            if ok:
                hits.append((cand, addr))
    return n, hits


def _chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--rate", action="store_true")
    ap.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = ap.parse_args()

    counts = _validate_lengths()
    n_total = sum(counts.values())
    print("N family A=%d B=%d C=%d total=%d" % (counts["A"], counts["B"], counts["C"], n_total),
          flush=True)
    if args.count:
        return 0

    # Witness the fast path through this same code before searching.
    if not oracle.selftest():
        return 1
    planted = "RasputinWilhelmAlekhine"
    if not (oracle.GATE in oracle.decode_wallet(
            oracle.PZL8_CIPHERTEXT_B64, planted, first_block_only=True)):
        print("WITNESS FAILED: planted sibling #8 answer not re-found on fast path")
        return 1
    print("WITNESS OK: sibling #8 answer re-found on the same fast path", flush=True)

    sample = [c for _, c in zip(range(24), (cand for _, cand in assemble()))]
    t0 = time.perf_counter()
    for cand in sample:
        _probe_one(cand)
    dt = time.perf_counter() - t0
    rate = len(sample) / dt if dt else 0
    t_est = n_total / rate if rate else float("inf")
    print("D=%.1f cand/s on %d-probe; t=N/D=%.0fs (%.1f min) workers=%d" % (
        rate, len(sample), t_est, t_est / 60, args.workers), flush=True)
    if args.rate:
        return 0
    if t_est > 7200 and args.workers == 1:
        print("abort: single-core t>2h; pass --workers", flush=True)
        return 2

    cands = [cand for _, cand in assemble()]
    workers = max(1, args.workers)
    chunk_size = max(32, len(cands) // (workers * 8) or 32)
    tested = 0
    hits = []
    t1 = time.perf_counter()
    if workers == 1:
        n, hits = _worker(cands)
        tested = n
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(_worker, ch) for ch in _chunks(cands, chunk_size)]
            for fut in as_completed(futs):
                n, h = fut.result()
                tested += n
                hits.extend(h)
                if tested % (chunk_size * workers) < chunk_size:
                    elapsed = time.perf_counter() - t1
                    print("progress %d/%d (%.1fs)" % (tested, n_total, elapsed), flush=True)
    elapsed = time.perf_counter() - t1
    print("tested=%d hits=%d elapsed=%.1fs rate=%.1f/s" % (
        tested, len(hits), elapsed, tested / elapsed if elapsed else 0), flush=True)
    for cand, addr in hits:
        print("MATCH %s" % addr)
        print("CANDIDATE_LEN %d" % len(cand))
        # Print the candidate to stdout for the operator; do not write a keyfile.
        print("CANDIDATE %s" % cand)
    return 0 if not hits else 0


if __name__ == "__main__":
    sys.exit(main())
