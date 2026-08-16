#!/usr/bin/env python3
"""
oracle.py -- P2SH multisig checker for the Objective Thune "Le secret de la Licorne"
puzzle.

Purpose:
    The escrow address is P2SH, and the puzzle's own announcement image states the
    mechanism: 3 private keys, physically hidden in 3 of 210 numbered collector
    copies of the book, whose public keys form a Bitcoin Core 0.18.1-style
    multisig redeem script (OP_M <pk1> <pk2> <pk3> OP_N OP_CHECKMULTISIG, keys
    NOT sorted, since Core 0.18.x does not apply BIP67 by default). Given
    candidate public keys, this script rebuilds the redeem script under every
    key order and every M from 2 to N, hashes it, and compares the resulting
    P2SH address to the escrow.

    This is a verifier, not a search tool: it needs real candidate public keys,
    extracted from physical books, to test. There is no cryptanalytic route to
    the 3 private keys; see the README.

Usage:
    python3 tools/oracle.py --selftest
    python3 tools/oracle.py "<pk1_hex> <pk2_hex> <pk3_hex>"
    python3 tools/oracle.py --stdin

Input:
    2 or 3 space-separated compressed public keys (33-byte hex, 66 hex chars
    each) on the command line, or one such line per line on stdin.

Output:
    "MATCH <m>-of-<n> <redeem_script_hex>" on a hit, "NO MATCH" otherwise. Exit
    0 on any match, 1 if none.

Dependencies:
    stdlib, base58.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from itertools import permutations

import base58

TARGET_ADDRESS = "3Jf995GANG4EmFBK89byNNyZdtB3ELXJsZ"
OP_CHECKMULTISIG = 0xAE

# A real, already-spent 2-of-3 P2SH multisig, found by scanning historical blocks
# and decoding the scriptSig that spends it: transaction
# de5af572e195ecbd7ce715be0464f79cd720b1c540c23c07a9d4e23dd24f8e47, block 360000
# (2015-06-08), spending 3MirgPA7x9hAmRzFcERXwj1nNnBjy894sT. Confirmed on
# mempool.space, 2026-08-16: 1 of 1 output spent, scriptSig carries this exact
# redeem script.
WITNESS_PUBKEYS_HEX = [
    "022fbc50c896d4ccec757c7032d4b8a755dad98e84816b4113e818451160bbfed1",
    "02ee70f4b0cbe4691e8104b5b18e03d62a716f1d8239657df2a14a697fce239e7f",
    "039a6ef848d2086703092029efc8ee8fded2c22776fc5786633bbbe08a18960504",
]
WITNESS_M = 2
WITNESS_ADDRESS = "3MirgPA7x9hAmRzFcERXwj1nNnBjy894sT"


def h160(data: bytes) -> bytes:
    return hashlib.new("ripemd160", hashlib.sha256(data).digest()).digest()


def _push(data: bytes) -> bytes:
    n = len(data)
    if n <= 0x4B:
        return bytes([n]) + data
    if n <= 0xFF:
        return bytes([0x4C, n]) + data
    if n <= 0xFFFF:
        return bytes([0x4D]) + n.to_bytes(2, "little") + data
    return bytes([0x4E]) + n.to_bytes(4, "little") + data


def build_multisig_redeem_script(m: int, pubkeys: list[bytes]) -> bytes:
    """OP_m <pk1> ... <pkN> OP_n OP_CHECKMULTISIG, keys in the given order (no
    BIP67 sort: matches createmultisig/addmultisigaddress in Bitcoin Core
    0.18.x, which does not sort keys by default)."""
    n = len(pubkeys)
    assert 1 <= m <= n <= 16
    script = bytes([0x50 + m])
    for pk in pubkeys:
        script += _push(pk)
    script += bytes([0x50 + n, OP_CHECKMULTISIG])
    return script


def p2sh_address(redeem_script: bytes, version_byte: bytes = b"\x05") -> str:
    payload = version_byte + h160(redeem_script)
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()


def check_one(pubkeys_hex: list[str], m: int, target_address: str) -> tuple[bool, str, str]:
    pubkeys = [bytes.fromhex(pk) for pk in pubkeys_hex]
    rs = build_multisig_redeem_script(m, pubkeys)
    addr = p2sh_address(rs)
    return addr == target_address, addr, rs.hex()


def check(candidate: str, target_address: str = TARGET_ADDRESS) -> tuple[bool, str | None, str | None]:
    """Try every key order and every M from 2 to N against target_address.
    Returns (match, "m-of-n", redeem_script_hex) for the first hit, or (False,
    None, None). This is a cheap, exhaustive check over public keys already in
    hand (N! * (N-1) tries for N=3: 12), not a search for private keys.
    target_address defaults to the puzzle escrow; the self-test overrides it to
    check against a known-good witness address instead."""
    pubkeys_hex = candidate.split()
    if not (2 <= len(pubkeys_hex) <= 16):
        return False, None, None
    try:
        for pk in pubkeys_hex:
            bytes.fromhex(pk)
    except ValueError:
        return False, None, None

    for m in range(2, len(pubkeys_hex) + 1):
        for perm in permutations(pubkeys_hex):
            matched, _addr, rs_hex = check_one(list(perm), m, target_address)
            if matched:
                return True, f"{m}-of-{len(pubkeys_hex)}", rs_hex
    return False, None, None


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def selftest() -> bool:
    ok = True

    matched, addr, rs_hex = check_one(WITNESS_PUBKEYS_HEX, WITNESS_M, WITNESS_ADDRESS)
    print(f"real 2-of-3 P2SH multisig, block 360000, spent 2015-06-08 -> {WITNESS_ADDRESS}: {'OK' if matched else 'FAIL'}")
    ok = ok and matched

    reordered = list(reversed(WITNESS_PUBKEYS_HEX))
    matched_wrong_order, _addr2, _rs2 = check_one(reordered, WITNESS_M, WITNESS_ADDRESS)
    order_matters = not matched_wrong_order
    print(f"the same 3 keys in a different order do NOT match (Core 0.18.x does not sort keys): {'OK' if order_matters else 'FAIL'}")
    ok = ok and order_matters

    found, mn, rs_hex2 = check(" ".join(WITNESS_PUBKEYS_HEX), target_address=WITNESS_ADDRESS)
    full_search_ok = found and mn == "2-of-3" and rs_hex2 == rs_hex
    print(f"the general checker finds the correct order and M among all 12 tries: {'OK' if full_search_ok else 'FAIL'}")
    ok = ok and full_search_ok

    no_match_on_target = not check_one(WITNESS_PUBKEYS_HEX, WITNESS_M, TARGET_ADDRESS)[0]
    print(f"negative control: the witness keys do not derive the licorne target address: {'OK' if no_match_on_target else 'FAIL'}")
    ok = ok and no_match_on_target

    if ok:
        print("SELFTEST OK")
    return ok


def _print_result(candidate: str) -> bool:
    matched, mn, rs_hex = check(candidate)
    if matched:
        print(f"MATCH {mn} {rs_hex}")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help='"<pk1_hex> <pk2_hex> <pk3_hex>"')
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification vector")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            any_hit = _print_result(line) or any_hit
        return 0 if any_hit else 1

    if not args.candidate:
        parser.print_help()
        return 0

    return 0 if _print_result(args.candidate) else 1


if __name__ == "__main__":
    sys.exit(main())
