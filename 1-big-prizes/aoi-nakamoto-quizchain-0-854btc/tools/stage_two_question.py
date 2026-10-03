#!/usr/bin/env python3
"""
stage_two_question.py -- Stage One solution as the question for Real Big Block.

Purpose:
    She wrote that the complete Stage One solution "will in turn be the question
    for the Second stage". The published question is the Wattpad chapter
    "Second". This script tests the cheap remainder of that reading: concatenate
    the certified Stage One bytes with the chapter, apply the chapter's own
    leftover instructions (first-four and last-four words; last letters of
    paragraphs that fail the ITASM keep-test), and a one-paragraph extra case
    toggle on top of the keep-test. It does not rerun contiguous spans, 1-edit
    sweeps, or the paragraph-227 rule already in analysis/tested.md.

    Source texts are fetched at run time and never written to the repository:
    bitcointalk topic 155054 (Hal Finney, "Bitcoin and me") and Wattpad part
    720888559. --selftest reproduces Stage One (MD5
    9dd2efb9bc976c2095bd534d7b8d431c to address
    19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN at m/44'/0'/0'/0/0) before any search.

Usage:
    python3 tools/stage_two_question.py --selftest
    python3 tools/stage_two_question.py --size
    python3 tools/stage_two_question.py --scan

N is printed by --size before any derivation. At the measured CPU rate this
space is minutes, not hours.

Dependencies: stdlib, requests, bip_utils (via tools/oracle.py).
"""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import os
import re
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("oracle", os.path.join(HERE, "oracle.py"))
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)

FINNEY_URL = "https://bitcointalk.org/index.php?topic=155054.0"
WATTPAD_URL = "https://www.wattpad.com/apiv2/?m=storytext&id=720888559"
USER_AGENT = "open-crypto-puzzles/stage_two_question (escrow research)"

STAGE_ONE_MD5 = "9dd2efb9bc976c2095bd534d7b8d431c"
STAGE_ONE_ADDR = "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
CHAPTER_PARAS = 273
CHAPTER_LEN_LF = 45451

TARGETS = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "Real Big Block current",
    "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd": "Quizchain2 Block 76",
    "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "Real Big Block superseded 2019-07-24",
}

ITASM = oracle.STAGE_ONE_NO_FLIP_INITIALS
KEEP_MODES = ("none", "char", "letter", "skipquote")
JOINS = ("\n\n", "\r\n\r\n")
SEPS = ("\n\n", "\r\n\r\n", "\n", "\r\n", " ", "")
PLANT_TAG = "RBBPHASE2PLANTEDWITNESS"

# Instruction-like paragraph indices in the live Wattpad part (0-based).
# 227 is the ITASM rule already swept; the others name leftover operations.
HINT_PARAS = (221, 225, 227, 229, 235, 241, 242, 243, 244)


def fetch(url: str) -> bytes:
    last = None
    for _ in range(3):
        try:
            resp = requests.get(
                url, timeout=30, headers={"User-Agent": USER_AGENT}
            )
            resp.raise_for_status()
            return resp.content
        except requests.RequestException as exc:
            last = exc
    raise last


def first_letter(s: str) -> str:
    for c in s:
        if c.isalpha():
            return c
    return ""


def keep_paragraph(p: str, mode: str) -> bool:
    if mode == "none":
        return True
    if mode == "all":
        return False
    if not p:
        return True
    if mode == "char":
        return p[0] in ITASM
    if mode == "letter":
        return first_letter(p) in ITASM
    if mode == "skipquote":
        s = p
        if s[:1] in "'\"" + "\u201c\u201d":
            s = s[1:].lstrip()
        return first_letter(s) in ITASM
    raise ValueError(mode)


def apply_keep(paragraphs: list[str], mode: str, join: str) -> str:
    out = [
        p if keep_paragraph(p, mode) else oracle.flip_case(p) for p in paragraphs
    ]
    return join.join(out)


def toggle_letter(s: str, which: str) -> str:
    idx = [i for i, c in enumerate(s) if c.isalpha()]
    if not idx:
        return s
    i = idx[0] if which == "first" else idx[-1]
    chars = list(s)
    chars[i] = chars[i].lower() if chars[i].isupper() else chars[i].upper()
    return "".join(chars)


def words_of(p: str) -> list[str]:
    return p.split()


def first4_last4(p: str) -> str:
    w = words_of(p)
    if len(w) <= 8:
        return " ".join(w)
    return " ".join(w[:4] + w[-4:])


def load_stage_one_paragraphs() -> list[str]:
    raw = fetch(FINNEY_URL).decode("iso-8859-1")
    posts = re.findall(r'<div class="post">(.*?)</div>', raw, flags=re.S)
    if not posts:
        raise RuntimeError("no bitcointalk posts parsed")
    parts = re.split(r"<br\s*/?>\s*<br\s*/?>", posts[0], flags=re.I)
    paras = []
    for part in parts:
        t = re.sub(r"<br\s*/?>", "\n", part, flags=re.I)
        t = re.sub(r"<[^>]+>", "", t)
        t = html.unescape(t).strip()
        if t:
            paras.append(t)
    return paras


def load_chapter_paragraphs() -> list[str]:
    raw = fetch(WATTPAD_URL).decode("utf-8")
    blocks = re.findall(r"<p[^>]*>(.*?)</p>", raw, flags=re.S)
    paras = []
    for block in blocks:
        t = re.sub(r"<br\s*/?>", "\n", block, flags=re.I)
        t = re.sub(r"<[^>]+>", "", t)
        t = html.unescape(t)
        paras.append(t)
    return paras


def reconstruct_stage_one(paras: list[str]) -> str:
    return apply_keep(paras, "char", "\n\n")


def chapter_tokenizations(paras: list[str]) -> dict[str, list[str]]:
    """Named paragraph lists. Canonical LF join of 'all' plus trailing newline
    must be 45,451 characters."""
    bold_heads = {
        i
        for i, p in enumerate(paras)
        if i == 0 or re.match(r"^(I{1,3}|IV|V|\d+)\.", p)
    }
    out = {
        "all": list(paras),
        "drop_title": paras[1:],
        "drop_heads": [p for i, p in enumerate(paras) if i not in bold_heads],
        "no_internal_nl": [p.replace("\n", " ") for p in paras],
        "br_as_paras": [],
    }
    for p in paras:
        out["br_as_paras"].extend(p.split("\n") if "\n" in p else [p])
    return out


def add(bucket: dict[str, str], label: str, text: str) -> None:
    if text and text not in bucket:
        bucket[text] = label


def build_candidates(stage_paras: list[str], chap_paras: list[str]) -> dict[str, str]:
    bucket: dict[str, str] = {}
    stage_lf = reconstruct_stage_one(stage_paras)
    stage_crlf = apply_keep(stage_paras, "char", "\r\n\r\n")
    tokens = chapter_tokenizations(chap_paras)

    # Family A: Stage One bytes concatenated with a chapter serialization.
    for stage_name, stage in (("s1lf", stage_lf), ("s1crlf", stage_crlf)):
        for tok_name, tok in tokens.items():
            for keep in KEEP_MODES:
                for join in JOINS:
                    body = apply_keep(tok, keep, join)
                    for tail in ("", "\n", "\r\n"):
                        ch = body + tail
                        for order, left, right in (
                            ("s1+ch", stage, ch),
                            ("ch+s1", ch, stage),
                        ):
                            for sep in SEPS:
                                add(
                                    bucket,
                                    f"A|{stage_name}|{tok_name}|{keep}|{join.encode()!r}|tail={tail.encode()!r}|{order}|sep={sep.encode()!r}",
                                    left + sep + right,
                                )

    # Family B: first four and last four words, as the chapter states at 241.
    extracts = [first4_last4(chap_paras[i]) for i in HINT_PARAS if i < len(chap_paras)]
    all_extracts = [first4_last4(p) for p in chap_paras]
    for i, ext in zip(HINT_PARAS, extracts):
        add(bucket, f"B|hint{i}|words", ext)
        add(bucket, f"B|hint{i}|twolines", "\n\n".join(ext.split()[:4] + [" ".join(ext.split()[-4:])]) if len(ext.split()) >= 8 else ext)
    for join in JOINS:
        add(bucket, f"B|all_hints|{join.encode()!r}", join.join(extracts))
        add(bucket, f"B|every_para|{join.encode()!r}", join.join(all_extracts))
        flipped = apply_keep(all_extracts, "char", join)
        add(bucket, f"B|every_para_char|{join.encode()!r}", flipped)

    # Concatenate those extracts with the canonical chapter.
    canon = apply_keep(chap_paras, "char", "\n\n") + "\n"
    for i, ext in zip(HINT_PARAS, extracts):
        for sep in ("\n\n", "\r\n\r\n", " "):
            add(bucket, f"B|hint{i}+canon|{sep.encode()!r}", ext + sep + canon)
            add(bucket, f"B|canon+hint{i}|{sep.encode()!r}", canon + sep + ext)

    # Family C: last letters of paragraphs that fail the keep-test (STNM analog).
    for keep in ("char", "letter", "skipquote"):
        letters = []
        selected = []
        for p in chap_paras:
            if keep_paragraph(p, keep):
                continue
            selected.append(p)
            idx = [i for i, c in enumerate(p) if c.isalpha()]
            if idx:
                letters.append(p[idx[-1]])
        add(bucket, f"C|lastletters|{keep}", "".join(letters))
        for join in JOINS:
            add(bucket, f"C|selected|{keep}|{join.encode()!r}", apply_keep(selected, keep, join))
            add(bucket, f"C|selected|none|{keep}|{join.encode()!r}", join.join(selected))

    # Family D: short strings the Satoshi Code passage itself derives, plus the chapter.
    shorts = [
        "STNM",
        "I STNM",
        "I STNM.",
        "Today, I",
        "Today I",
        "Today, Satoshi's real identity",
        "I recognize the signs.",
        "Today, I recognize the signs.",
    ]
    for s in shorts:
        for sep in ("\n\n", "\r\n\r\n", " "):
            add(bucket, f"D|{s!r}+canon|{sep.encode()!r}", s + sep + canon)
            add(bucket, f"D|canon+{s!r}|{sep.encode()!r}", canon + sep + s)

    # Family E: stored markup, not inner text (small).
    html_src = fetch(WATTPAD_URL).decode("utf-8")
    add(bucket, "E|raw_html", html_src)
    inner = re.sub(r"</p>\s*<p[^>]*>", "\n\n", html_src)
    inner = re.sub(r"<[^>]+>", "", inner)
    add(bucket, "E|tags_stripped_keep_entities", inner)
    add(bucket, "E|tags_stripped_unescaped", html.unescape(inner))

    # Family F: one extra first/last-letter case toggle on a keep-tested chapter.
    for keep in KEEP_MODES:
        for join in JOINS:
            flipped_paras = [
                p if keep_paragraph(p, keep) else oracle.flip_case(p)
                for p in chap_paras
            ]
            for i in range(len(flipped_paras)):
                for which in ("first", "last"):
                    trial = list(flipped_paras)
                    trial[i] = toggle_letter(trial[i], which)
                    add(
                        bucket,
                        f"F|{keep}|{join.encode()!r}|p{i}|{which}",
                        join.join(trial),
                    )

    return bucket


def plants() -> list[str]:
    return [
        f"Head {PLANT_TAG} alpha\n\nsecond paragraph of plant.",
        f"Middle {PLANT_TAG} beta\n\nsecond paragraph of plant.",
        f"Tail {PLANT_TAG} gamma\n\nsecond paragraph of plant.",
    ]


def check_one(text: str) -> tuple[bool, dict]:
    entropy = oracle.md5_entropy(text)
    addresses = oracle.derive_addresses(entropy, n=6)
    for i, addr in enumerate(addresses):
        if addr in TARGETS:
            return True, {"address": addr, "label": TARGETS[addr], "index": i}
    return False, {}


def selftest() -> bool:
    ok = True
    stage_paras = load_stage_one_paragraphs()
    body = reconstruct_stage_one(stage_paras)
    md5 = hashlib.md5(body.encode("utf-8")).hexdigest()
    part = md5 == STAGE_ONE_MD5
    print(f"Stage One MD5 {md5} -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    addrs = oracle.derive_addresses(bytes.fromhex(md5), n=6)
    part = STAGE_ONE_ADDR in addrs and addrs.index(STAGE_ONE_ADDR) == 0
    print(f"Stage One address at index 0 -> {'OK' if part else 'FAIL'}")
    ok = ok and part

    chap = load_chapter_paragraphs()
    part = len(chap) == CHAPTER_PARAS
    print(f"chapter paragraphs {len(chap)} -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    canon = "\n\n".join(chap) + "\n"
    part = len(canon) == CHAPTER_LEN_LF
    print(f"canonical LF length {len(canon)} -> {'OK' if part else 'FAIL'}")
    ok = ok and part

    bucket = build_candidates(stage_paras, chap)
    planted = plants()
    # Insert without using add(), so duplicates of real candidates cannot hide them.
    ordered = list(bucket.keys())
    mid = len(ordered) // 2
    stream = [planted[0]] + ordered[:mid] + [planted[1]] + ordered[mid:] + [planted[2]]
    seen = {p: False for p in planted}
    for text in stream:
        if text in seen:
            seen[text] = True
    part = all(seen.values())
    print(f"three planted witnesses recovered in the generator stream -> {'OK' if part else 'FAIL'}")
    ok = ok and part
    return ok


def size() -> int:
    stage_paras = load_stage_one_paragraphs()
    chap = load_chapter_paragraphs()
    n = len(build_candidates(stage_paras, chap))
    print(f"N unique candidates = {n}")
    return n


def scan() -> int:
    if not selftest():
        print("SELFTEST FAIL; not scanning")
        return 1
    stage_paras = load_stage_one_paragraphs()
    chap = load_chapter_paragraphs()
    bucket = build_candidates(stage_paras, chap)
    planted = plants()
    ordered = list(bucket.items())
    mid = len(ordered) // 2
    stream = (
        [(planted[0], "plant-head")]
        + ordered[:mid]
        + [(planted[1], "plant-mid")]
        + ordered[mid:]
        + [(planted[2], "plant-tail")]
    )
    n = len(bucket)
    print(f"scanning {n} unique texts plus 3 plants")
    t0 = time.time()
    hits = 0
    plant_hits = 0
    match = None
    for i, (text, label) in enumerate(stream, start=1):
        if text in planted:
            plant_hits += 1
            continue
        hit, info = check_one(text)
        if hit:
            match = (label, info, len(text), hashlib.md5(text.encode("utf-8")).hexdigest())
            hits += 1
            break
        if i % 1000 == 0:
            elapsed = time.time() - t0
            rate = i / elapsed if elapsed else 0
            print(f"  {i}/{len(stream)} {rate:.0f}/s", flush=True)
    elapsed = time.time() - t0
    rate = len(stream) / elapsed if elapsed else 0
    print(
        f"done texts={n} plants_recovered={plant_hits}/3 hits={hits} "
        f"elapsed={elapsed:.1f}s rate={rate:.0f}/s"
    )
    if match:
        label, info, length, digest = match
        # Do not print the candidate bytes. Print enough to retrieve them from
        # the generator label and the MD5.
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
