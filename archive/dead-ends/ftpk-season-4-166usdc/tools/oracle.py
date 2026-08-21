#!/usr/bin/env python3
"""Oracle for FTPK Season 4 ("Something in Common").

Purpose: check whether a 12-word BIP39 mnemonic derives the escrow's Ethereum address
under the standard BIP44 path m/44'/60'/0'/0/0.

Usage:
  python3 oracle.py --selftest              # reproduces the public BIP39/BIP44 test mnemonic (no author-published worked example exists for this season)
  python3 oracle.py "word1 word2 ... word12" # MATCH / NO MATCH, exit 0 / 1
  python3 oracle.py --stdin                  # one 12-word candidate per line

Input: 12 space-separated English BIP39 words, in the order to derive with.
Expected output: "SELFTEST OK" (exit 0) or "SELFTEST FAILED" (exit 1) for --selftest;
"MATCH <address>" or "NO MATCH" per candidate otherwise. A checksum-invalid candidate is
reported as NO MATCH (mnemonics with a wrong BIP39 checksum cannot derive any seed).

Requires: mnemonic, bip_utils (both pure-Python, no network).
"""
import sys

from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicValidator

ESCROW = "0xa468335485cE853F21A44451755bd88364e9d618".lower()
DERIVATION_PATH = "m/44'/60'/0'/0/0"

SELFTEST_MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
SELFTEST_ADDRESS = "0x9858EfFD232B4033E47d90003D41EC34EcaEda94"

MNEMO = Mnemonic("english")
VALIDATOR = Bip39MnemonicValidator()


def derive_eth(mnemonic, passphrase=""):
    seed = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    acc = (Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
           .Purpose().Coin().Account(0)
           .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0))
    return acc.PublicKey().ToAddress()


def check(candidate):
    """Returns (ok, address_or_none, reason)."""
    words = candidate.split()
    if len(words) != 12:
        return False, None, "need exactly 12 words, got %d" % len(words)
    if not VALIDATOR.IsValid(" ".join(words)):
        return False, None, "invalid BIP39 checksum"
    addr = derive_eth(" ".join(words))
    if addr.lower() == ESCROW:
        return True, addr, "match"
    return False, None, "no match"


def selftest():
    got = derive_eth(SELFTEST_MNEMONIC)
    ok = got.lower() == SELFTEST_ADDRESS.lower()
    print("selftest mnemonic -> %s" % got)
    print("expected              %s" % SELFTEST_ADDRESS)
    print("SELFTEST %s: the public BIP39/BIP44 test mnemonic (no author-published worked example exists for this season)" % ("OK" if ok else "FAILED"))
    return ok


def main():
    if len(sys.argv) < 2:
        print('usage: oracle.py --selftest | "12 words" | --stdin', file=sys.stderr)
        sys.exit(2)
    if sys.argv[1] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if sys.argv[1] == "--stdin":
        found = False
        for line in sys.stdin:
            cand = line.strip()
            if not cand:
                continue
            ok, addr, reason = check(cand)
            if ok:
                print("MATCH %s <- %r" % (addr, cand))
                found = True
        sys.exit(0 if found else 1)
    ok, addr, reason = check(sys.argv[1])
    if ok:
        print("MATCH %s" % addr)
        sys.exit(0)
    print("NO MATCH (%s)" % reason)
    sys.exit(1)


if __name__ == "__main__":
    main()
