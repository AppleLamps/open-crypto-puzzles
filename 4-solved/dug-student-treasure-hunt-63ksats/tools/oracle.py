#!/usr/bin/env python3
"""Oracle for Dug's Student Treasure Hunt (2025 edition).

Checks a 12-word BIP39 mnemonic against the three funded receive addresses of the
puzzle wallet (BIP84, account 0, external chain, indices 0, 1 and 2). No private
address was ever published by the author; the funded-and-not-yet-swept address at
the time was itself the proof of a correct answer.

Usage:
  python3 oracle.py --selftest          # reproduces the official BIP84 test vector
                                          # and the solved mnemonic, exit 0
  python3 oracle.py "word1 word2 ... word12"   # MATCH / NO MATCH, exit 0 / 1
  python3 oracle.py --stdin             # one candidate mnemonic per line, prints matches only

Requires: bip_utils (pip install bip_utils). Stdlib otherwise.
"""
import sys

from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip84, Bip84Coins, Bip44Changes,
)

# The three receive addresses actually funded by the author (indices 0, 1, 2 of
# m/84'/0'/0'/0/i). All three are public now: index 0 and 2 were swept by a third
# party on 2026-07-08, index 1 was swept by me on 2026-08-02.
TARGETS = {
    "bc1qych2me6h85j38s3xmfwdkcvpqakpld3yr2y5ss": "m/84'/0'/0'/0/0",
    "bc1qphfklk568cf93267yetpngqsz0mthw4z4x2q69": "m/84'/0'/0'/0/1",
    "bc1qnclravnmv7vta9fhnp44hu3y85z3tfgz0n33wl": "m/84'/0'/0'/0/2",
}

SOLVED_MNEMONIC = (
    "profit general lava hover jar visa joy immense install first give kingdom"
)

BIP84_TV_MNEMONIC = (
    "abandon abandon abandon abandon abandon abandon "
    "abandon abandon abandon abandon abandon about"
)
BIP84_TV_ADDRESS = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"


def is_valid_checksum(mnemonic: str) -> bool:
    try:
        return Bip39MnemonicValidator().IsValid(mnemonic)
    except Exception:
        return False


def derive_address(mnemonic: str, index: int, passphrase: str = "") -> str:
    seed = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    ctx = Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
    node = ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)
    return node.PublicKey().ToAddress()


def check_candidate(mnemonic: str):
    """Returns (address, path) on an exact match against TARGETS, else None."""
    mnemonic = " ".join(mnemonic.split())
    if not is_valid_checksum(mnemonic):
        return None
    for index in range(3):
        addr = derive_address(mnemonic, index)
        if addr in TARGETS:
            return addr, TARGETS[addr]
    return None


def selftest() -> None:
    got = derive_address(BIP84_TV_MNEMONIC, 0)
    assert got == BIP84_TV_ADDRESS, f"BIP84 test vector broken: {got} != {BIP84_TV_ADDRESS}"
    assert is_valid_checksum(BIP84_TV_MNEMONIC), "test vector checksum rejected"

    hit = check_candidate(SOLVED_MNEMONIC)
    assert hit is not None, "solved mnemonic did not reproduce a known funded address"
    for addr, path in TARGETS.items():
        got = derive_address(SOLVED_MNEMONIC, int(path.rsplit("/", 1)[1]))
        assert got == addr, f"solved mnemonic does not reproduce {path}: {got} != {addr}"

    print("SELFTEST OK")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    if sys.argv[1] == "--selftest":
        selftest()
        return 0

    if sys.argv[1] == "--stdin":
        any_match = False
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            hit = check_candidate(line)
            if hit:
                any_match = True
                addr, path = hit
                print(f"MATCH {path} {addr} <- {line}")
        return 0 if any_match else 1

    candidate = sys.argv[1]
    hit = check_candidate(candidate)
    if hit:
        addr, path = hit
        print(f"MATCH {path} {addr}")
        return 0
    print("NO MATCH")
    return 1


if __name__ == "__main__":
    sys.exit(main())
