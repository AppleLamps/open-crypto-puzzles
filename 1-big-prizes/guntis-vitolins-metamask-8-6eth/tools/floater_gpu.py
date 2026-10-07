#!/usr/bin/env python3
"""
floater_gpu.py -- RO1 plus one free video word, over every on-screen and spoken
word of the challenge video not yet tested, on a GPU.

MODEL

Exactly the model of sweep_coins.py (anchors dutch 1, fog 5, parrot 12; fiber
and fork on the post side with 3 more post words in reading order; 3 video pool
words in reading order plus ONE floater in any of the 4 free video slots), with
the floater list widened from the 5 portfolio coin words to every word in
data/video-onscreen-words.json (on screen or spoken, in no written surface)
minus the 13 words already swept as floaters in analysis/tested.md.

  per floater word   85,350 video arrangements * 816 post sets * 5 fork slots
                     = 348,228,000 arrangements, about 21.76 million valid
  181 floater words  63,029,268,000 arrangements, about 3.94 billion valid

PIPELINE

  floater_gen.c      enumerates one unit (one post word set, 77,241,750 arrangements)
                     in the same loop order as sweep_coins.scan_unit and keeps
                     the checksum-valid rows
  engines/libbip39pass.so  check_mnemonics_eth_multi: PBKDF2-SHA512, BIP32
                     m/44'/60'/0'/0/0, keccak, compared to up to 16 targets

WITNESSES

Every unit carries 3 planted targets next to the escrow: the addresses of its
first, middle and last valid rows, derived on the CPU before the unit is sent.
A unit counts only if the GPU reports all 3 at exactly the expected row; any
miss aborts the run with exit 3 instead of reporting a negative.

ON A MATCH

The escrow hit is re-derived on the CPU, the phrase goes to --hit, and the log
prints only the unit and row number, never the words. The same unit and row
reproduce the phrase locally with floater_gen.

USAGE

  python3 tools/floater_gpu.py --size
  python3 tools/floater_gpu.py --crosscheck            # C generator == Python, no GPU
  python3 tools/floater_gpu.py --gpu-selftest          # engine known-answer test
  python3 tools/floater_gpu.py --run [--start-unit N]
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import ctypes
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(FOLDER))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "engines"))

import sweep_reading_order as ro  # noqa: E402
import sweep_coins as sc  # noqa: E402

ALREADY_SWEPT = {"atom", "link", "basic", "token", "dash", "build", "ready",
                 "donor", "stay", "until", "win", "hard", "minimum"}
PER_WORD = 85350 * 816 * 5
KAT_PHRASE = " ".join(["abandon"] * 11 + ["about"])
KAT_ADDR = "9858effd232b4033e47d90003d41ec34ecaeda94"


def floater_words(path, index_of):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    words = sorted((set(d["onscreen_not_in_pool"]) | set(d["spoken_not_in_pool"]))
                   - ALREADY_SWEPT)
    for w in words:
        if w not in index_of:
            sys.exit("floater word %s is not a BIP39 word" % w)
    return words


def write_plan(path, words, index_of, pool_path, floaters):
    pre, mid, free, order = ro.load_pool(pool_path)
    lays = sc.build_rows(pre, mid, index_of)
    units = list(__import__("itertools").combinations(free, 3))
    out = [" ".join(str(index_of[w]) for w in ("dutch", "fog", "parrot", "fork")),
           "%d %s" % (len(floaters), " ".join(str(index_of[w]) for w in floaters)),
           str(len(lays))]
    for vpos, coin, pool_slots, rows in lays:
        out.append("%d %d %s %d %s %d" % (coin, len(pool_slots),
                                          " ".join(map(str, pool_slots)), len(vpos),
                                          " ".join(map(str, vpos)), len(rows)))
        out.append(" ".join(str(x) for r in rows for x in r))
    out.append(str(len(units)))
    for bset in units:
        o4 = sorted(list(bset) + ["fiber"], key=lambda w: order[w])
        out.append(" ".join(str(index_of[w]) for w in o4))
    with open(path, "w") as fh:
        fh.write("\n".join(out) + "\n")
    return units


def gen_unit(gen, plan, unit, count=False):
    if count:
        r = subprocess.run([gen, plan, str(unit), "--count"], check=True,
                           capture_output=True, text=True)
        n, d = r.stdout.split()
        return int(n), int(d)
    r = subprocess.run([gen, plan, str(unit)], check=True, capture_output=True)
    return r.stdout


def rows_of(buf):
    import numpy as np
    return np.frombuffer(buf, dtype="<i4").reshape(-1, 12)


def setup(a):
    words, index_of = ro.load_wordlist(a.wordlist)
    floaters = floater_words(a.words, index_of)
    if a.limit_words:
        floaters = floaters[:a.limit_words]
    units = write_plan(a.plan, words, index_of, a.pool, floaters)
    return words, index_of, floaters, units


def cmd_size(a):
    _, _, floaters, units = setup(a)
    print("floater words  %d" % len(floaters))
    print("units          %d" % len(units))
    print("arrangements   %s" % format(PER_WORD * len(floaters), ","))
    print("expected valid about %s" % format(PER_WORD * len(floaters) // 16, ","))
    return 0


def cmd_crosscheck(a):
    """The C generator must emit exactly the valid candidates sweep_coins.py
    enumerates, in the same order, and the closed-form count per unit."""
    words, index_of, floaters, units = setup(a)
    ok = True
    pre, mid, free, order = ro.load_pool(a.pool)
    lays = sc.build_rows(pre, mid, index_of)
    sample = sorted({0, 1, len(units) // 2, len(units) - 1})
    sub = floaters[:3] + floaters[-2:]
    plan_small = a.plan + ".small"
    write_plan(plan_small, words, index_of, a.pool, sub)
    for u in sample:
        seen = []

        def grab(mn):
            seen.append(mn)
            return "0x" + "0" * 40
        n, d, _ = sc.scan_unit(units[u], index_of, words, lays,
                               [index_of[w] for w in sub], order, grab, "0x" + "f" * 40)
        crow = rows_of(gen_unit(a.gen, plan_small, u))
        cmn = [" ".join(words[i] for i in r) for r in crow]
        p = cmn == seen and n == 85350 * 5 * len(sub)
        print("unit %3d, %d floaters: python %d valid of %d, C %d valid, identical order: %s"
              % (u, len(sub), d, n, len(cmn), "OK" if p else "FAIL"))
        ok &= p
    for u in (0, len(units) - 1):
        n, d = gen_unit(a.gen, a.plan, u, count=True)
        p = n == 85350 * 5 * len(floaters) and abs(d / n - 1 / 16) < 0.002
        print("unit %3d, all %d floaters: %s arrangements, %s valid, rate %.5f: %s"
              % (u, len(floaters), format(n, ","), format(d, ","), d / n, "OK" if p else "FAIL"))
        ok &= p
    print("CROSSCHECK OK" if ok else "CROSSCHECK FAILED")
    return 0 if ok else 1


def load_engine():
    import bip39pass_eth as be
    lib = be.load()
    lib.bip39pass_set_eth_targets.restype = ctypes.c_int
    lib.bip39pass_set_eth_targets.argtypes = [ctypes.c_char_p, ctypes.c_int]
    lib.bip39pass_run_eth_batch_multi.restype = ctypes.c_int
    lib.bip39pass_run_eth_batch_multi.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                                  ctypes.POINTER(ctypes.c_int)]
    be.set_path(lib, be.parse_path("m/44'/60'/0'/0/0"))
    return be, lib


def gpu_batch(lib, rows, targets):
    import numpy as np
    lib.bip39pass_set_eth_targets(b"".join(targets), len(targets))
    out = (ctypes.c_int * 16)()
    arr = np.ascontiguousarray(rows, dtype=np.int32)
    e = lib.bip39pass_run_eth_batch_multi(arr.ctypes.data, len(arr), out)
    if e:
        sys.exit("CUDA error %d" % e)
    return list(out)[:len(targets)]


def cmd_gpu_selftest(a, be=None, lib=None):
    words, index_of = ro.load_wordlist(a.wordlist)
    if lib is None:
        be, lib = load_engine()
    be.load_wordlist(lib, words)
    kat = [index_of[w] for w in KAT_PHRASE.split()]
    p1 = be.cpu_eth_addr(KAT_PHRASE, be.parse_path("m/44'/60'/0'/0/0")).hex() == KAT_ADDR
    junk = [[(i * 7 + j * 131) % 2048 for j in range(12)] for i in range(255)]
    res = gpu_batch(lib, junk[:100] + [kat] + junk[100:], [bytes.fromhex(KAT_ADDR)])
    p2 = res[0] == 100
    print("CPU known-answer vector: %s" % ("OK" if p1 else "FAIL"))
    print("GPU known-answer vector found at row 100 of 256: %s" % ("OK" if p2 else "FAIL (%r)" % res))
    print("GPU SELFTEST OK" if p1 and p2 else "GPU SELFTEST FAILED")
    return 0 if p1 and p2 else 1


def cmd_run(a):
    words, index_of, floaters, units = setup(a)
    be, lib = load_engine()
    if cmd_gpu_selftest(a, be, lib):
        return 1
    path = be.parse_path("m/44'/60'/0'/0/0")
    escrow = bytes.fromhex(ro.TARGET_ADDRESS[2:])
    todo = list(range(a.start_unit, len(units)))
    print("RUN %d floater words, units %d..%d, batch %d, %d generator workers"
          % (len(floaters), todo[0], todo[-1], a.batch, a.workers), flush=True)
    rng = random.Random(20261007)
    t0 = time.time()
    tn = td = 0
    pool = cf.ThreadPoolExecutor(a.workers)
    window = {}
    nxt = 0

    def fill():
        nonlocal nxt
        while nxt < len(todo) and len(window) < a.workers + 2:
            window[todo[nxt]] = pool.submit(gen_unit, a.gen, a.plan, todo[nxt])
            nxt += 1
    fill()
    for k, u in enumerate(todo, 1):
        tu = time.time()
        rows = rows_of(window.pop(u).result())
        fill()
        nrow = len(rows)
        wi = [0, rng.randrange(1, nrow - 1), nrow - 1]
        waddr = [be.cpu_eth_addr(" ".join(words[i] for i in rows[j]), path) for j in wi]
        targets = [escrow] + waddr
        found = [-1, -1, -1, -1]
        for s in range(0, nrow, a.batch):
            res = gpu_batch(lib, rows[s:s + a.batch], targets)
            for t, r in enumerate(res):
                if r >= 0:
                    found[t] = s + r
        if found[0] >= 0:
            mn = " ".join(words[i] for i in rows[found[0]])
            if be.cpu_eth_addr(mn, path) == escrow:
                with open(a.hit, "w") as fh:
                    fh.write(mn + "\n")
                print("MATCH unit=%d row=%d, CPU re-derivation agrees. Phrase written to %s, "
                      "deliberately not printed." % (u, found[0], a.hit), flush=True)
                return 0
            print("GPU reported unit=%d row=%d but CPU disagrees; ignoring" % (u, found[0]))
        wok = found[1:] == wi
        n = 85350 * 5 * len(floaters)
        tn += n
        td += nrow
        el = time.time() - t0
        print("UNIT\t%d\t%d\t%d\twitness=%s\t%.1fs\t%.0f/s\teta %.0f min"
              % (u, n, nrow, "OK" if wok else "FAIL", time.time() - tu, td / el,
                 (len(todo) - k) * el / k / 60), flush=True)
        if not wok:
            print("WITNESS FAILURE in unit %d: expected rows %s, got %s. Aborting."
                  % (u, wi, found[1:]), flush=True)
            return 3
    print("FINISHED units %d..%d: %s arrangements, %s derivations, all witnesses OK, "
          "no match, %.1f min" % (todo[0], todo[-1], format(tn, ","), format(td, ","),
                                  (time.time() - t0) / 60), flush=True)
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wordlist", default=os.environ.get(
        "BIP39_WORDLIST", os.path.join(REPO, "engines", "lib", "bip39_english.txt")))
    ap.add_argument("--pool", default=os.path.join(FOLDER, "data", "reading-order-pool.json"))
    ap.add_argument("--words", default=os.path.join(FOLDER, "data", "video-onscreen-words.json"))
    ap.add_argument("--gen", default=os.path.join(HERE, "floater_gen"))
    ap.add_argument("--plan", default="floater_plan.txt")
    ap.add_argument("--hit", default="hit_floater.txt")
    ap.add_argument("--batch", type=int, default=1 << 20)
    ap.add_argument("--workers", type=int, default=min(8, max(1, (os.cpu_count() or 2) - 1)))
    ap.add_argument("--start-unit", type=int, default=0)
    ap.add_argument("--limit-words", type=int, default=0)
    for f in ("size", "crosscheck", "gpu_selftest", "run"):
        ap.add_argument("--" + f.replace("_", "-"), action="store_true")
    a = ap.parse_args()
    if a.size:
        return cmd_size(a)
    if a.crosscheck:
        return cmd_crosscheck(a)
    if a.gpu_selftest:
        return cmd_gpu_selftest(a)
    if a.run:
        return cmd_run(a)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
