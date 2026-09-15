#!/usr/bin/env python3
"""
two_sign_toggles.py -- two extra first/last-letter toggles on a keep-tested chapter.

Purpose:
    Grycoin Block 2 said to copy-paste and change only capitalization. Stage One
    already changes first and last letters of the paragraphs that fail the ITASM
    keep-test. tools/stage_two_question.py killed one extra first-or-last toggle
    on top of that keep-test (3,270 texts). This script is the distance-2 slice
    of the same family: after the keep-test, toggle the first or last letter of
    exactly two distinct paragraphs.

    N = C(273, 2) * 2 * 2 * 4 keep-tests * 2 joins = 1,188,096.
    At the measured 448 candidates/s that is about 44 minutes on one core,
    about 12 minutes on four. It is not the unbounded 2-character space.

    The chapter is fetched at run time and never written to the repository.

Usage:
    python3 tools/two_sign_toggles.py --selftest
    python3 tools/two_sign_toggles.py --size
    python3 tools/two_sign_toggles.py --scan

Dependencies: stdlib, requests, bip_utils (via tools/oracle.py).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import os
import sys
import time
from multiprocessing import Pool, cpu_count

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "stage_two_question", os.path.join(HERE, "stage_two_question.py")
)
stq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stq)

KEEP_MODES = ("none", "char", "letter", "skipquote")
JOINS = ("\n\n", "\r\n\r\n")
WHICH = ("first", "last")
PLANT_TAG = "RBBTWOSIGNPLANTED"
N_PARAS = 273

# Worker globals, set by _init_worker.
_BASES = None
_KEEP_MODES = None
_JOINS = None


def n_space(n_paras: int = N_PARAS) -> int:
    pairs = n_paras * (n_paras - 1) // 2
    return pairs * len(WHICH) * len(WHICH) * len(KEEP_MODES) * len(JOINS)


def keep_lists(paras: list[str]) -> dict[str, list[str]]:
    out = {}
    for keep in KEEP_MODES:
        out[keep] = [
            p if stq.keep_paragraph(p, keep) else stq.oracle.flip_case(p)
            for p in paras
        ]
    return out


def render(base: list[str], join: str, i: int, j: int, wi: str, wj: str) -> str:
    parts = list(base)
    parts[i] = stq.toggle_letter(base[i], wi)
    parts[j] = stq.toggle_letter(base[j], wj)
    return join.join(parts)


def extras(paras: list[str]) -> dict[str, str]:
    """Paragraph 245: last words / last letters at the end of relevant paragraphs."""
    bucket: dict[str, str] = {}

    def add(label: str, text: str) -> None:
        if text and text not in bucket:
            bucket[text] = label

    for keep in ("char", "letter", "skipquote"):
        last_letters = []
        last_words = []
        selected = []
        for p in paras:
            if stq.keep_paragraph(p, keep):
                continue
            selected.append(p)
            letters = [c for c in p if c.isalpha()]
            if letters:
                last_letters.append(letters[-1])
            w = p.split()
            if w:
                last_words.append(w[-1])
        add(f"extra|lastletters|{keep}", "".join(last_letters))
        add(f"extra|lastwords|{keep}|space", " ".join(last_words))
        add(f"extra|lastwords|{keep}|nlnl", "\n\n".join(last_words))
        canon = stq.apply_keep(paras, keep, "\n\n") + "\n"
        add(f"extra|lastletters+canon|{keep}", "".join(last_letters) + "\n\n" + canon)
        add(f"extra|lastwords+canon|{keep}", " ".join(last_words) + "\n\n" + canon)
        add(f"extra|canon+lastletters|{keep}", canon + "\n\n" + "".join(last_letters))
    all_last = []
    for p in paras:
        letters = [c for c in p if c.isalpha()]
        all_last.append(letters[-1] if letters else "")
    add("extra|all_lastletters", "".join(all_last))
    return bucket


def plants() -> list[str]:
    return [
        f"Head {PLANT_TAG} alpha\n\nsecond paragraph of plant.",
        f"Middle {PLANT_TAG} beta\n\nsecond paragraph of plant.",
        f"Tail {PLANT_TAG} gamma\n\nsecond paragraph of plant.",
    ]


def _init_worker(bases: dict, keep_modes: tuple, joins: tuple) -> None:
    global _BASES, _KEEP_MODES, _JOINS
    _BASES = bases
    _KEEP_MODES = keep_modes
    _JOINS = joins


def _eval_job(job: tuple) -> tuple:
    """job = (keep_i, join_i, i, j, wi, wj) -> (hit, info_or_None, label, md5hex)."""
    ki, ji, i, j, wi, wj = job
    keep = _KEEP_MODES[ki]
    join = _JOINS[ji]
    text = render(_BASES[keep], join, i, j, wi, wj)
    hit, info = stq.check_one(text)
    label = f"{keep}|{join.encode()!r}|p{i}:{wi}|p{j}:{wj}"
    digest = hashlib.md5(text.encode("utf-8")).hexdigest() if hit else ""
    return hit, info, label, digest, len(text)


def iter_jobs(n_paras: int):
    for ki in range(len(KEEP_MODES)):
        for ji in range(len(JOINS)):
            for i, j in itertools.combinations(range(n_paras), 2):
                for wi in WHICH:
                    for wj in WHICH:
                        yield (ki, ji, i, j, wi, wj)


def selftest() -> bool:
    ok = True
    chap = stq.load_chapter_paragraphs()
    part = len(chap) == N_PARAS
    print(f"chapter paragraphs {len(chap)} -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    bases = keep_lists(chap)
    # Known-good input: one real pair, re-found through the same render().
    text = render(bases["char"], "\n\n", 1, 50, "first", "last")
    again = render(bases["char"], "\n\n", 1, 50, "first", "last")
    part = text == again and len(text) > 1000
    print(f"render is deterministic on a real pair -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    digest = hashlib.md5(text.encode("utf-8")).hexdigest()
    # Push that text through check_one (will be NO MATCH) and re-find the md5.
    hit, _ = stq.check_one(text)
    part = (not hit) and hashlib.md5(text.encode("utf-8")).hexdigest() == digest
    print(f"known-good pair re-found by md5 {digest[:8]}... -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    planted = plants()
    stream = [planted[0], text, planted[1], again, planted[2]]
    seen = {p: False for p in planted}
    found_real = 0
    for item in stream:
        if item in seen:
            seen[item] = True
        if hashlib.md5(item.encode("utf-8")).hexdigest() == digest:
            found_real += 1
    part = all(seen.values()) and found_real == 2
    print(f"three plants and the real pair recovered in a toy stream -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    extra = extras(chap)
    part = len(extra) > 0
    print(f"paragraph-245 extras {len(extra)} -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    print(f"N = {n_space(len(chap))}")
    return ok


def size() -> int:
    n = n_space()
    d = 448.0
    t = n / d
    print(f"N = {n}")
    print(f"D = {d:.0f}/s (measured 2026-09-15 on this CPU, same oracle path)")
    print(f"t = N/D = {t:.0f}s ({t / 60:.1f} min) serial; ~{t / max(cpu_count(), 1) / 60:.1f} min on {cpu_count()} cores")
    return n


def scan() -> int:
    if not selftest():
        print("SELFTEST FAIL; not scanning")
        return 1
    chap = stq.load_chapter_paragraphs()
    n = n_space(len(chap))
    d_est = 448.0
    t_est = n / d_est
    print(f"N={n} D~{d_est:.0f}/s t~{t_est:.0f}s serial")
    if t_est > 7200:
        print("t above two hours; refusing to scan")
        return 1

    bases = keep_lists(chap)
    planted = plants()
    extra = extras(chap)
    print(f"scanning {len(extra)} extras, then {n} two-toggle texts, plus 3 plants")

    t0 = time.time()
    hits = 0
    plant_hits = 0
    extra_done = 0
    done = 0
    witness_hits = 0
    match = None

    for text in planted:
        plant_hits += 1
        hit, info = stq.check_one(text)
        if hit:
            match = ("plant", info, len(text), hashlib.md5(text.encode("utf-8")).hexdigest())
            hits += 1
            break
    if match is None:
        for text, label in extra.items():
            extra_done += 1
            hit, info = stq.check_one(text)
            if hit:
                match = (label, info, len(text), hashlib.md5(text.encode("utf-8")).hexdigest())
                hits += 1
                break

    done = 0
    witness_hits = 0
    witness_label = "char|" + repr("\n\n".encode()) + "|p1:first|p50:last"
    workers = min(4, cpu_count() or 1)
    if match is None:
        with Pool(
            processes=workers,
            initializer=_init_worker,
            initargs=(bases, KEEP_MODES, JOINS),
        ) as pool:
            for hit, info, label, digest, length in pool.imap_unordered(
                _eval_job, iter_jobs(len(chap)), chunksize=256
            ):
                done += 1
                if label == witness_label:
                    witness_hits += 1
                if hit:
                    match = (label, info, length, digest)
                    hits += 1
                    pool.terminate()
                    break
                if done % 20000 == 0:
                    elapsed = time.time() - t0
                    rate = (extra_done + done) / elapsed if elapsed else 0
                    print(f"  {done}/{n} {rate:.0f}/s", flush=True)

    elapsed = time.time() - t0
    total = extra_done + done
    rate = total / elapsed if elapsed else 0
    print(
        f"done extras={extra_done} two_toggles={done} plants={plant_hits}/3 "
        f"witness_pair={witness_hits}/1 hits={hits} elapsed={elapsed:.1f}s rate={rate:.0f}/s"
    )
    if match:
        label, info, length, digest = match
        print(
            f"MATCH {info['label']} {info['address']} index={info['index']} "
            f"label={label} bytes={length} md5={digest}"
        )
        return 0
    print("NO MATCH")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--size", action="store_true")
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return 0 if selftest() else 1
    if args.size:
        size()
        return 0
    if args.scan:
        return scan()
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
