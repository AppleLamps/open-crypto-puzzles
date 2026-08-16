#!/usr/bin/env python3
"""Oracle for the Zodomo 11x11 pixel puzzles (networked.art).

Checks a BIP39 mnemonic (12 or 24 words) against the known escrow addresses of the
artist's first three 11x11 puzzle pieces. Two of the three encoding schemes used to
turn a pixel grid into this mnemonic have been fully reconstructed and are
certified below; the active (fourth) puzzle currently has no known funded address
to check against (see the README), so a candidate for it cannot be confirmed by
balance alone.

Usage:
  python3 oracle.py --selftest              # reproduces the known #993 mnemonic
  python3 oracle.py "word1 word2 ... wordN"  # MATCH / NO MATCH, exit 0 / 1
  python3 oracle.py --stdin                  # one candidate mnemonic per line

Requires: bip_utils, pycryptodome. Stdlib otherwise.
"""
import sys

from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1, Bip39MnemonicValidator
from Crypto.Hash import keccak

# Escrow addresses funded by zodomo.eth on 2026-07-30 for pieces #869, #930 and #993.
# #869 and #930 were swept by a third party; #993 was reclaimed by the artist himself.
# None of these is the active (fourth) puzzle.
KNOWN_ESCROWS = {
    "0x60a5431a138b0320641408694562f624f3c977a8": "869",
    "0x9cc846fe9b75a4cee897f605b240dd0030fcd5a2": "930",
    "0xf5d45c9d798aedb754b1ed8660af3ea79178b765": "993",
}

DERIVATION_PATHS = [
    "m/44'/60'/0'/0/0",
    "m/44'/60'/0'/0/1",
    "m/44'/60'/1'/0/0",
]

# #993's mnemonic, reconstructed by this research from the color-partition reading of
# the piece's pixel grid (see the README "Mechanism" section). Its escrow was
# reclaimed by the artist, not a live prize, so publishing it risks no front-running.
SOLVED_993_MNEMONIC = (
    "tourist basic valid turn fit velvet weird sniff domain control comfort catch "
    "scare gallery meadow naive alarm daughter tone material rice note hawk struggle"
)


def is_valid_mnemonic(mnemonic: str) -> bool:
    try:
        return Bip39MnemonicValidator().IsValid(mnemonic)
    except Exception:
        return False


def eth_address(mnemonic: str, path: str, passphrase: str = "") -> str:
    seed = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    root = Bip32Slip10Secp256k1.FromSeed(seed)
    node = root.DerivePath(path)
    pub_uncompressed = node.PublicKey().RawUncompressed().ToBytes()  # 65 bytes, 0x04 prefix
    k = keccak.new(digest_bits=256)
    k.update(pub_uncompressed[1:])
    return "0x" + k.digest()[-20:].hex()


def check_candidate(mnemonic: str):
    """Returns (address, piece_number, path) on an exact match, else None."""
    mnemonic = " ".join(mnemonic.split())
    if not is_valid_mnemonic(mnemonic):
        return None
    for path in DERIVATION_PATHS:
        addr = eth_address(mnemonic, path).lower()
        if addr in KNOWN_ESCROWS:
            return addr, KNOWN_ESCROWS[addr], path
    return None


def selftest() -> None:
    assert is_valid_mnemonic(SOLVED_993_MNEMONIC), "known #993 mnemonic failed BIP39 checksum"
    got = eth_address(SOLVED_993_MNEMONIC, "m/44'/60'/0'/0/0")
    expected = "0xf5d45c9d798aedb754b1ed8660af3ea79178b765"
    assert got.lower() == expected, f"#993 derivation broken: {got} != {expected}"
    hit = check_candidate(SOLVED_993_MNEMONIC)
    assert hit is not None and hit[1] == "993", "candidate checker did not confirm #993"
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
                addr, piece, path = hit
                print(f"MATCH piece #{piece} {addr} via {path} <- {line}")
        return 0 if any_match else 1

    candidate = sys.argv[1]
    hit = check_candidate(candidate)
    if hit:
        addr, piece, path = hit
        print(f"MATCH piece #{piece} {addr} via {path}")
        return 0
    print("NO MATCH")
    return 1


if __name__ == "__main__":
    sys.exit(main())
