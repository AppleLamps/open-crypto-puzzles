#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Finlow-Bates blockchain-book puzzle series.

Purpose:
    Check a candidate answer against the 12 escrow addresses of the Finlow-Bates
    "Move Over Brokers, Here Comes The Blockchain" treasure hunt (8 EN lots, 4 IT lots).
    Two confirmed transform families are wired in, matching the two ways I have seen
    this author turn an answer into a key:

    1. sha256x3: a deduced text answer -> SHA-256 applied three times -> 32-byte
       private key -> P2PKH address (compressed and uncompressed both checked).
       This is the transform behind EN_easy_1, IT_hard, and my working hypothesis for
       the 3 lots still open (EN_medium, EN_veryhard, IT_veryhard).
    2. bip39: a 12-word mnemonic (English or Italian BIP39 wordlist), empty
       passphrase, BIP44 path m/44'/0'/0'/0/0, compressed address. This is the
       transform behind EN_hard_1 and IT_medium.

    This is a verifier, not a search tool: it checks the candidates you give it, it does
    not generate any.

Usage:
    python3 tools/oracle.py --selftest              # must print SELFTEST OK and exit 0
    python3 tools/oracle.py "221B Baker Street"      # sha256x3 mode (default), MATCH/NO MATCH
    python3 tools/oracle.py --bip39 "word1 word2 ... word12"   # BIP39 mode
    python3 tools/oracle.py --stdin                  # one candidate per line, sha256x3 mode,
                                                       # prints matches only

Input:
    A candidate answer string on the command line, or one per line on stdin.

Output:
    "MATCH <lot> <address> via <method>" for a hit, "NO MATCH" otherwise. Exit 0 on any
    match, 1 if none.

Dependencies:
    stdlib, ecdsa, base58, and (only for --bip39) bip_utils.
"""

from __future__ import annotations

import argparse
import hashlib
import sys

import base58
from ecdsa import SigningKey, SECP256k1

# ---------------------------------------------------------------------------
# The 12 lot addresses (public escrow addresses, all P2PKH). 3 are still open;
# 9 are already solved and swept, kept here only so --selftest has known-good
# vectors to reproduce.
# ---------------------------------------------------------------------------
LOTS = {
    "14aFhno96fkt7knLWMDQ4j8yh8v5hBF4n1": "EN_easy_1",
    "14utGQn5GdfPvUrHNLAwTmmP99QpXm9mg6": "EN_easy_2",
    "1QFafw3weoWTRQhiLafRw2eyWbVmES6wfJ": "EN_medium_s",
    "17Y9czcbcCz433QXsy1SGQjwLb27BBtLLZ": "EN_medium",
    "181rPpfdUGFg4fVEdhDZEfDbBSqgigtoZR": "EN_hard_1",
    "161YgNX2NrCzGunWvoV1hN3DuzWeuovBK3": "EN_hard_2",
    "1KZei2D5yz3UJ59LvXsC1Y9y4ktSgcnVwz": "EN_veryhard_s",
    "1DZ5NbUwDgxeJkKhQLgYcUUX36PtYso1pm": "EN_veryhard",
    "1MEstvLAzc5DzJtvx7uyvKNNUCPN3ofWMK": "IT_easy",
    "1Q78hDeaHXQbuCSQxG1uPAc4V3jsuVUG9r": "IT_medium",
    "1QExGvuieS9MvuKC3R1qjp6jGTVcqisTDj": "IT_hard",
    "19kkawFcg2U2s6vq368MXD7FJU9JZvRrjA": "IT_veryhard",
}


# ---------------------------------------------------------------------------
# Key derivation primitives
# ---------------------------------------------------------------------------

def ripemd160(data: bytes) -> bytes:
    try:
        h = hashlib.new("ripemd160")
        h.update(data)
        return h.digest()
    except ValueError:
        from Crypto.Hash import RIPEMD160
        h = RIPEMD160.new()
        h.update(data)
        return h.digest()


def hash160(data: bytes) -> bytes:
    return ripemd160(hashlib.sha256(data).digest())


def p2pkh_from_secret(secret: bytes) -> tuple[str, str]:
    """Return (compressed_address, uncompressed_address) for a 32-byte secret."""
    if len(secret) != 32:
        raise ValueError(f"private key must be 32 bytes, got {len(secret)}")
    sk = SigningKey.from_string(secret, curve=SECP256k1)
    vk = sk.verifying_key
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    uncompressed_pub = b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")
    prefix = b"\x02" if y % 2 == 0 else b"\x03"
    compressed_pub = prefix + x.to_bytes(32, "big")
    addr_compressed = base58.b58encode_check(b"\x00" + hash160(compressed_pub)).decode()
    addr_uncompressed = base58.b58encode_check(b"\x00" + hash160(uncompressed_pub)).decode()
    return addr_compressed, addr_uncompressed


def sha256_iter(text: str, depth: int) -> bytes:
    digest = text.encode("utf-8")
    for _ in range(depth):
        digest = hashlib.sha256(digest).digest()
    return digest


# ---------------------------------------------------------------------------
# Candidate checking
# ---------------------------------------------------------------------------

def check_sha256x3(candidate: str) -> list[dict]:
    """Check a text answer under SHA-256 applied 1, 2, and 3 times, both key forms."""
    hits = []
    text = candidate.strip()
    for depth in (1, 2, 3):
        secret = sha256_iter(text, depth)
        addr_c, addr_u = p2pkh_from_secret(secret)
        for key_form, addr in (("compressed", addr_c), ("uncompressed", addr_u)):
            if addr in LOTS:
                hits.append({
                    "lot": LOTS[addr],
                    "address": addr,
                    "method": f"sha256^{depth} ({key_form})",
                })
    return hits


def check_bip39(mnemonic: str) -> list[dict]:
    """Check a 12-word mnemonic (English or Italian wordlist), empty passphrase,
    BIP44 m/44'/0'/0'/0/0, compressed address."""
    from bip_utils import (
        Bip39SeedGenerator, Bip39Languages, Bip44, Bip44Coins, Bip44Changes,
    )
    hits = []
    for lang in (Bip39Languages.ENGLISH, Bip39Languages.ITALIAN):
        try:
            seed = Bip39SeedGenerator(mnemonic, lang).Generate("")
        except Exception:
            continue
        ctx = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
        node = ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        addr = node.PublicKey().ToAddress()
        if addr in LOTS:
            lang_name = "en" if lang == Bip39Languages.ENGLISH else "it"
            hits.append({
                "lot": LOTS[addr],
                "address": addr,
                "method": f"BIP39 ({lang_name}) -> BIP44 m/44'/0'/0'/0/0",
            })
    return hits


def selftest() -> bool:
    ok = True

    hits = check_sha256x3("221B Baker Street")
    found = any(h["lot"] == "EN_easy_1" and h["address"] == "14aFhno96fkt7knLWMDQ4j8yh8v5hBF4n1"
                and h["method"] == "sha256^3 (uncompressed)" for h in hits)
    print(f'sha256x3("221B Baker Street") -> EN_easy_1: {"OK" if found else "FAIL"}')
    ok = ok and found

    hits = check_sha256x3("Genova Firenze Bologna Brindisi")
    found = any(h["lot"] == "IT_hard" and h["address"] == "1QExGvuieS9MvuKC3R1qjp6jGTVcqisTDj"
                and h["method"] == "sha256^3 (uncompressed)" for h in hits)
    print(f'sha256x3("Genova Firenze Bologna Brindisi") -> IT_hard: {"OK" if found else "FAIL"}')
    ok = ok and found

    # negative control: an unrelated string must not match anything
    hits = check_sha256x3("this string is not an answer")
    clean = len(hits) == 0
    print(f"negative control (unrelated string) -> no match: {'OK' if clean else 'FAIL'}")
    ok = ok and clean

    if ok:
        print("SELFTEST OK")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="candidate answer string")
    parser.add_argument("--bip39", metavar="MNEMONIC", help="check a 12-word mnemonic instead")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line, sha256x3 mode")
    parser.add_argument("--selftest", action="store_true", help="run the certification vectors")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.bip39:
        hits = check_bip39(args.bip39)
        if hits:
            for h in hits:
                print(f"MATCH {h['lot']} {h['address']} via {h['method']}")
            return 0
        print("NO MATCH")
        return 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            cand = line.strip()
            if not cand:
                continue
            for h in check_sha256x3(cand):
                any_hit = True
                print(f"MATCH {h['lot']} {h['address']} via {h['method']}  candidate={cand!r}")
        return 0 if any_hit else 1

    if not args.candidate:
        parser.print_help()
        return 0

    hits = check_sha256x3(args.candidate)
    if hits:
        for h in hits:
            print(f"MATCH {h['lot']} {h['address']} via {h['method']}")
        return 0
    print("NO MATCH")
    return 1


if __name__ == "__main__":
    sys.exit(main())
