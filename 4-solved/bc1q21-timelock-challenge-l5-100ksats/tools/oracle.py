#!/usr/bin/env python3
"""Oracle for the bc1q21 Time-Lock Challenge, Level 5.

Checks a 12-word BIP39 mnemonic against the funding address of the puzzle: the
operator never published a recovery phrase, but the address that received the
100,000-sat prize (BIP84, account 0, external chain, index 0) is itself the proof
of a correct answer. This covers the word-recovery half of the puzzle only; the
second half (reconstructing the CLTV redeem script and locktime that actually
unlocked the funds) is described in the README and is not a candidate-checking
oracle in the same sense.

Usage:
  python3 oracle.py --selftest              # BIP84 test vector + the solved mnemonic
  python3 oracle.py "word1 word2 ... word12" # MATCH / NO MATCH, exit 0 / 1
  python3 oracle.py --stdin                  # one candidate mnemonic per line

Requires: bip_utils (pip install bip_utils). Stdlib otherwise.
"""
import sys

from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip84, Bip84Coins, Bip44Changes,
)

# The address that received the 100,000-sat Level 5 prize, BIP84 m/84'/0'/0'/0/0.
# Public since the funding transaction; the recovery phrase itself was never
# published by the operator.
TARGET_ADDRESS = "bc1q3pwpgp7dkhtzj6qya39l8tu6dgdarv9gr9kx0r"

SOLVED_MNEMONIC = "can large cool deny mean quick wish spare argue body ski spot"

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


def derive_address(mnemonic: str, passphrase: str = "") -> str:
    seed = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    ctx = Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
    node = ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    return node.PublicKey().ToAddress()


def check_candidate(mnemonic: str) -> bool:
    mnemonic = " ".join(mnemonic.split())
    if not is_valid_checksum(mnemonic):
        return False
    return derive_address(mnemonic) == TARGET_ADDRESS


def selftest() -> None:
    got = derive_address(BIP84_TV_MNEMONIC)
    assert got == BIP84_TV_ADDRESS, f"BIP84 test vector broken: {got} != {BIP84_TV_ADDRESS}"
    assert is_valid_checksum(BIP84_TV_MNEMONIC), "test vector checksum rejected"

    assert check_candidate(SOLVED_MNEMONIC), "solved mnemonic did not reproduce the funding address"

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
            if check_candidate(line):
                any_match = True
                print(f"MATCH {TARGET_ADDRESS} <- {line}")
        return 0 if any_match else 1

    candidate = sys.argv[1]
    if check_candidate(candidate):
        print(f"MATCH {TARGET_ADDRESS}")
        return 0
    print("NO MATCH")
    return 1


if __name__ == "__main__":
    sys.exit(main())
