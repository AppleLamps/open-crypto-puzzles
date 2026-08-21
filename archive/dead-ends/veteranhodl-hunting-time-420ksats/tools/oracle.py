#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the VeteranHODL "Hunting Time" seed puzzle.

Purpose:
    The author states the seed is hidden across 12 weekly clue images (one word per
    image, in publication order) and that the funds sit in "a fresh electrum wallet."
    This script checks a candidate 12-word phrase against two derivation branches:

      - BIP39 -> BIP84, m/84'/0'/0'/0/i, empty passphrase, standard BIP39 checksum.
        This branch is CERTIFIED: it reproduces the public BIP39/BIP84 test vector.
      - Electrum segwit seed, salt "electrum", path m/0'/0/i, no BIP39 checksum.
        This branch is NOT CERTIFIED: no known-good (published seed plus published
        address) vector exists to prove the derivation accepts a correct answer, even
        though it is the wallet type the author explicitly named. A "NO MATCH" on this
        branch alone should not be read as a real negative.

Usage:
    python3 tools/oracle.py --selftest                 # must print SELFTEST OK
    python3 tools/oracle.py "w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12"
    python3 tools/oracle.py --stdin                     # one 12-word candidate per line

Input:
    A 12-word, space-separated candidate phrase, checked against both branches for
    address indexes 0 through 4.

Output:
    "MATCH <format> index=<i> <address>" on a hit, "NO MATCH" otherwise. Exit 0 on any
    match, 1 if none. The certified branch is tried first.

Dependencies:
    stdlib, bip_utils (checksum validation only; the derivation itself is hand-written
    so both branches share the same BIP32 and bech32 code).
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import struct
import sys
import unicodedata

from bip_utils import Bip39MnemonicValidator
from ecdsa import SigningKey, SECP256k1

TARGET = "bc1qhzy6j4amw26z7e694mgfr7kvzl7xteu54f0a85"

CURVE_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
HARDENED = 0x80000000

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


# ---------------------------------------------------------------------------
# bech32 (BIP173), written out so this file has no dependency beyond ecdsa
# ---------------------------------------------------------------------------

def _bech32_polymod(values):
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ v
        for i in range(5):
            chk ^= gen[i] if ((b >> i) & 1) else 0
    return chk


def _bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad and bits:
        ret.append((acc << (tobits - bits)) & maxv)
    return ret


def bech32_encode(hrp, witver, prog):
    data = [witver] + _convertbits(prog, 8, 5)
    polymod = _bech32_polymod(_bech32_hrp_expand(hrp) + data + [0, 0, 0, 0, 0, 0]) ^ 1
    checksum = [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + "1" + "".join(CHARSET[d] for d in data + checksum)


# ---------------------------------------------------------------------------
# BIP32 derivation (secp256k1, hardened and non-hardened steps)
# ---------------------------------------------------------------------------

def _pubkey_compressed(secret_int: int) -> bytes:
    sk = SigningKey.from_secret_exponent(secret_int, curve=SECP256k1)
    point = sk.verifying_key.pubkey.point
    prefix = b"\x02" if point.y() % 2 == 0 else b"\x03"
    return prefix + point.x().to_bytes(32, "big")


def _hash160(data: bytes) -> bytes:
    try:
        h = hashlib.new("ripemd160")
        h.update(hashlib.sha256(data).digest())
        return h.digest()
    except ValueError:
        from Crypto.Hash import RIPEMD160
        h = RIPEMD160.new()
        h.update(hashlib.sha256(data).digest())
        return h.digest()


def _master_key(seed: bytes):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return int.from_bytes(I[:32], "big"), I[32:]


def _child_key(k: int, c: bytes, n: int):
    if n >= HARDENED:
        data = b"\x00" + k.to_bytes(32, "big") + struct.pack(">I", n)
    else:
        data = _pubkey_compressed(k) + struct.pack(">I", n)
    I = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % CURVE_N, I[32:]


def _address_p2wpkh(k: int) -> str:
    return bech32_encode("bc", 0, _hash160(_pubkey_compressed(k)))


def address_bip39_bip84(phrase: str, index: int = 0) -> str:
    seed = hashlib.pbkdf2_hmac(
        "sha512", unicodedata.normalize("NFKD", phrase).encode(), b"mnemonic", 2048
    )
    k, c = _master_key(seed)
    for n in (84 + HARDENED, 0 + HARDENED, 0 + HARDENED, 0, index):
        k, c = _child_key(k, c, n)
    return _address_p2wpkh(k)


def address_electrum_segwit(phrase: str, index: int = 0) -> str:
    seed = hashlib.pbkdf2_hmac(
        "sha512", unicodedata.normalize("NFKD", phrase).encode(), b"electrum", 2048
    )
    k, c = _master_key(seed)
    for n in (0 + HARDENED, 0, index):
        k, c = _child_key(k, c, n)
    return _address_p2wpkh(k)


def electrum_seed_version_ok(phrase: str) -> bool:
    """A standard-type Electrum segwit seed has an HMAC-SHA512(key='Seed version', ...)
    hex digest starting with '100'. This checks well-formedness only; it does NOT prove
    the address derivation above is the one Electrum itself would produce (see the
    module docstring: this branch has no certified vector)."""
    x = hmac.new(
        b"Seed version", unicodedata.normalize("NFKD", phrase).encode(), hashlib.sha512
    ).hexdigest()
    return x.startswith("100")


# Public BIP39/BIP84 test vector (12 words, all-zero entropy), the standard vector used
# across the BIP39/BIP44/BIP84 test suites. Certifies the BIP39->BIP84 branch.
SELFTEST_VECTOR = " ".join(["abandon"] * 11 + ["about"])
SELFTEST_EXPECTED_ADDRESS = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"


def check(phrase: str, depth: int = 5) -> tuple[str, int, str] | None:
    words = phrase.split()
    if len(words) != 12:
        return None
    if Bip39MnemonicValidator().IsValid(phrase):
        for i in range(depth):
            addr = address_bip39_bip84(phrase, i)
            if addr == TARGET:
                return ("BIP39/BIP84", i, addr)
    if electrum_seed_version_ok(phrase):
        for i in range(depth):
            addr = address_electrum_segwit(phrase, i)
            if addr == TARGET:
                return ("Electrum segwit (uncertified)", i, addr)
    return None


def selftest() -> bool:
    ok = True

    print("-> BIP39 -> BIP84 (certified branch)")
    got = address_bip39_bip84(SELFTEST_VECTOR, 0)
    match = got == SELFTEST_EXPECTED_ADDRESS
    print(f"  {'OK' if match else 'FAIL'}  public BIP39/BIP84 test vector derives the known address")
    print(f"        {got}")
    ok = ok and match

    neighbor = " ".join(["abandon"] * 11 + ["abandon"])
    got_neighbor = address_bip39_bip84(neighbor, 0)
    distinct = got_neighbor != SELFTEST_EXPECTED_ADDRESS
    print(f"  {'OK' if distinct else 'FAIL'}  a one-word-different phrase does not collide")
    ok = ok and distinct

    not_target = check(SELFTEST_VECTOR) is None
    print(f"  {'OK' if not_target else 'FAIL'}  the test vector does not match the puzzle target")
    ok = ok and not_target

    print("-> Electrum segwit seed (uncertified branch, no known-good vector)")
    deterministic = electrum_seed_version_ok(SELFTEST_VECTOR) == electrum_seed_version_ok(SELFTEST_VECTOR)
    print(f"  {'OK' if deterministic else 'FAIL'}  the version check is deterministic")
    print("  NOTE  no known-good Electrum seed+address pair is embedded here: a NO MATCH")
    print("        on this branch alone is uncertified, not a proven negative")
    ok = ok and deterministic

    if ok:
        print("SELFTEST OK")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="candidate 12-word phrase")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification vector")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            cand = line.strip()
            if not cand:
                continue
            hit = check(cand)
            if hit:
                any_hit = True
                fmt, idx, addr = hit
                print(f"MATCH {fmt} index={idx} {addr}  candidate={cand!r}")
        return 0 if any_hit else 1

    if args.candidate is None:
        parser.print_help()
        return 0

    hit = check(args.candidate)
    if hit:
        fmt, idx, addr = hit
        print(f"MATCH {fmt} index={idx} {addr}")
        return 0
    print("NO MATCH")
    return 1


if __name__ == "__main__":
    sys.exit(main())
