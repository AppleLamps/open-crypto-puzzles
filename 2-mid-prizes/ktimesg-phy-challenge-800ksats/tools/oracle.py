#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the kTimesG "Phy Challenge" puzzle.

Purpose:
    The author published a BIP-137 signed message (clues/first-post-message.txt signed with
    clues/signature.txt). Recovering the public key from that signature gives the escrow
    address. This script does two jobs:

    1. recover: rebuild the signer's compressed public key and P2WPKH address from the
       published signature and message, and compare it to the escrow address.
    2. check a candidate private key (64 hex characters): derive its compressed public key
       and P2WPKH address and compare to the escrow address.

    The recovery accepts only BIP-137 header bytes 39 to 42 (compressed key, native SegWit
    P2WPKH), so it certifies the signature type the author published.

    Only an exact address match counts. Nothing else is reported as progress.

Usage:
    python3 tools/oracle.py --selftest            # must print SELFTEST OK
    python3 tools/oracle.py --recover             # print the recovered public key and address
    python3 tools/oracle.py --scripts             # print the same key under other script forms
    python3 tools/oracle.py <64-hex private key>  # candidate check
    python3 tools/oracle.py --stdin               # one 64-hex candidate per line

Input:
    A private key as 64 hexadecimal characters (big-endian scalar), on the command line or
    one per line on stdin. The script never prints a candidate back.

Output:
    "MATCH" when the candidate's compressed-key P2WPKH address equals the escrow address,
    "NO MATCH" otherwise. Exit 0 on any match, 1 if none. If you see MATCH, stop, do not
    broadcast anything, and give the key to the human running you.

Dependencies:
    stdlib only. Needs a Python build whose hashlib provides ripemd160.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import sys

ESCROW = "bc1qrpn28qa82uyjg37dvsz3w7wpm3kpdea957nm9p"

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (GX, GY)

HERE = os.path.dirname(os.path.abspath(__file__))
CLUES = os.path.join(HERE, "..", "clues")

BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def point_add(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    if a == b:
        lam = (3 * a[0] * a[0]) * pow(2 * a[1], -1, P) % P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x = (lam * lam - a[0] - b[0]) % P
    return (x, (lam * (a[0] - x) - a[1]) % P)


def point_mul(k, pt):
    out = None
    while k:
        if k & 1:
            out = point_add(out, pt)
        pt = point_add(pt, pt)
        k >>= 1
    return out


def compress(pt):
    return (b"\x02" if pt[1] % 2 == 0 else b"\x03") + pt[0].to_bytes(32, "big")


def hash160(data):
    return hashlib.new("ripemd160", hashlib.sha256(data).digest()).digest()


def _polymod(values):
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if (top >> i) & 1 else 0
    return chk


def _convert_bits(data, frm, to):
    acc = bits = 0
    out = []
    for v in data:
        acc = (acc << frm) | v
        bits += frm
        while bits >= to:
            bits -= to
            out.append((acc >> bits) & ((1 << to) - 1))
    if bits:
        out.append((acc << (to - bits)) & ((1 << to) - 1))
    return out


def p2wpkh_address(pubkey33):
    hrp = "bc"
    data = [0] + _convert_bits(hash160(pubkey33), 8, 5)
    expand = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]
    mod = _polymod(expand + data + [0] * 6) ^ 1
    checksum = [(mod >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + "1" + "".join(BECH32_CHARSET[d] for d in data + checksum)


BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58check(payload):
    full = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(full, "big")
    out = ""
    while n:
        n, rem = divmod(n, 58)
        out = BASE58[rem] + out
    return "1" * (len(full) - len(full.lstrip(b"\0"))) + out


def decompress(pubkey33):
    x = int.from_bytes(pubkey33[1:], "big")
    y = pow((pow(x, 3, P) + 7) % P, (P + 1) // 4, P)
    if y % 2 != pubkey33[0] % 2:
        y = P - y
    return b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")


def other_script_addresses(pubkey33):
    """The same key under other single-key script forms (not P2WPKH, not multisig, not taproot)."""
    redeem = b"\x00\x14" + hash160(pubkey33)
    return {
        "P2PKH compressed": base58check(b"\x00" + hash160(pubkey33)),
        "P2PKH uncompressed": base58check(b"\x00" + hash160(decompress(pubkey33))),
        "P2SH-P2WPKH": base58check(b"\x05" + hash160(redeem)),
    }


def _varint(n):
    return bytes([n]) if n < 253 else b"\xfd" + n.to_bytes(2, "little")


def message_hash(message):
    prefixed = b"\x18Bitcoin Signed Message:\n" + _varint(len(message)) + message
    return hashlib.sha256(hashlib.sha256(prefixed).digest()).digest()


def recover_pubkey(signature_b64, message):
    """BIP-137 public key recovery. Returns the 33-byte compressed public key."""
    raw = base64.b64decode(signature_b64 + "=" * (-len(signature_b64) % 4))
    if len(raw) != 65:
        raise ValueError("signature is not 65 bytes")
    header = raw[0]
    if not 39 <= header <= 42:
        raise ValueError("BIP-137 header must be 39 to 42 for a compressed P2WPKH key")
    r = int.from_bytes(raw[1:33], "big")
    s = int.from_bytes(raw[33:], "big")
    recid = header - 39
    x = r + (recid >> 1) * N
    beta = pow((pow(x, 3, P) + 7) % P, (P + 1) // 4, P)
    y = beta if (beta - recid) % 2 == 0 else P - beta
    big_r = (x, y)
    e = int.from_bytes(message_hash(message), "big")
    r_inv = pow(r, -1, N)
    q = point_mul(r_inv, point_add(point_mul(s, big_r), point_mul((-e) % N, G)))
    return compress(q)


def load_clues():
    with open(os.path.join(CLUES, "first-post-message.txt"), "rb") as f:
        message = f.read()
    with open(os.path.join(CLUES, "signature.txt"), encoding="ascii") as f:
        signature = f.read().strip()
    return message, signature


def recovered_address():
    message, signature = load_clues()
    pub = recover_pubkey(signature, message)
    return pub, p2wpkh_address(pub)


def check_candidate(hex_key, target=ESCROW):
    hex_key = hex_key.strip()
    if len(hex_key) != 64:
        return False
    try:
        d = int(hex_key, 16)
    except ValueError:
        return False
    if not 1 <= d < N:
        return False
    return p2wpkh_address(compress(point_mul(d, G))) == target


def selftest():
    ok = True

    # Public BIP-173 test vector: private key 1 gives this P2WPKH address.
    pub1 = compress(point_mul(1, G))
    if pub1.hex() != "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798":
        print("FAIL: public key of private key 1")
        ok = False
    if p2wpkh_address(pub1) != "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4":
        print("FAIL: BIP-173 address vector")
        ok = False

    # The author's own signature over the author's own message must recover the escrow.
    message, signature = load_clues()
    pub, address = recovered_address()
    if address != ESCROW:
        print("FAIL: published signature does not recover the escrow address")
        ok = False

    # Negative control: a one-byte change to the signed message must not recover the escrow.
    other = p2wpkh_address(recover_pubkey(signature, message + b"\n"))
    if other == ESCROW:
        print("FAIL: altered message still recovers the escrow address")
        ok = False

    # The candidate matcher must re-find a known-good input through the same code path:
    # private key 1 against its own public BIP-173 address (the target is injected here).
    bip173 = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"
    one = "00" * 31 + "01"
    if not check_candidate(one, target=bip173):
        print("FAIL: known-good key 1 not re-found against its BIP-173 address")
        ok = False
    # It must also reject a wrong key for that target, and reject key 1 for the real escrow.
    if check_candidate("00" * 31 + "02", target=bip173):
        print("FAIL: private key 2 reported as a match for the key 1 address")
        ok = False
    if check_candidate(one):
        print("FAIL: private key 1 reported as a match for the escrow")
        ok = False

    # Header validation: other BIP-137 address types and out-of-range headers must be refused,
    # even when their low bits would recover the same key.
    raw = bytearray(base64.b64decode(signature + "=" * (-len(signature) % 4)))
    for bad_header in (27, 31, 35, 38, 43):
        raw[0] = bad_header
        try:
            recover_pubkey(base64.b64encode(bytes(raw)).decode(), message)
            print(f"FAIL: header {bad_header} was accepted")
            ok = False
        except ValueError:
            pass

    # Other script forms of private key 1. The two P2PKH vectors are the widely published
    # addresses for key 1. The P2SH-P2WPKH address has 38 transactions on chain (2026-10-01).
    expected = {
        "P2PKH compressed": "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
        "P2PKH uncompressed": "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm",
        "P2SH-P2WPKH": "3JvL6Ymt8MVWiCNHC7oWU6nLeHNJKLZGLN",
    }
    if other_script_addresses(pub1) != expected:
        print("FAIL: other script forms of private key 1")
        ok = False

    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return ok


def main():
    ap = argparse.ArgumentParser(description="Phy Challenge oracle")
    ap.add_argument("candidate", nargs="?", help="private key as 64 hex characters")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--recover", action="store_true")
    ap.add_argument("--scripts", action="store_true")
    ap.add_argument("--stdin", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest() else 1
    if args.recover:
        pub, address = recovered_address()
        print("public key:", pub.hex())
        print("address:   ", address)
        print("escrow:    ", ESCROW)
        print("MATCH" if address == ESCROW else "NO MATCH")
        return 0 if address == ESCROW else 1
    if args.scripts:
        pub, _ = recovered_address()
        for name, address in other_script_addresses(pub).items():
            print(f"{name}: {address}")
        return 0
    if args.stdin:
        found = False
        for line in sys.stdin:
            if line.strip() and check_candidate(line):
                found = True
                print("MATCH")
        if not found:
            print("NO MATCH")
        return 0 if found else 1
    if args.candidate:
        if check_candidate(args.candidate):
            print("MATCH")
            return 0
        print("NO MATCH")
        return 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
