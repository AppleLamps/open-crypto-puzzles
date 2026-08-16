#!/usr/bin/env python3
"""
oracle.py -- final-gate candidate checker for the GSMG.io puzzle.

Purpose:
    The puzzle's last published page names an OpenSSL AES blob and tells the solver
    to find the password. This script reproduces that specific, publicly documented
    half of the final gate: given a candidate answer string X, it computes
    password = sha256(X).hexdigest(), decrypts the blob printed on the last page
    (OpenSSL legacy "Salted__" format, AES-256-CBC, MD5 key derivation) with that
    password, reduces the resulting plaintext to a 32-byte value with a small set of
    standard readings, derives the uncompressed secp256k1 public key, and compares
    its HASH160 to the escrow address.

    This is NOT the puzzle's own sealed answer-checker (an unpublished tool some
    solvers reference informally); that tool is not public and this repository has
    no access to it, so it is not shipped here. What is shipped is the AES-blob
    pipeline itself, which is fully reproducible from the puzzle's own published
    material and the escrow's on-chain public key.

Usage:
    python3 tools/oracle.py --selftest              # see "Certified against" below
    python3 tools/oracle.py "<candidate answer>"     # try one candidate
    python3 tools/oracle.py --stdin                  # one candidate per line

Input:
    A candidate answer string X.

Output:
    "MATCH <address> reading=<name> priv_hex=<hex> wif=<wif>" on a hit,
    "NO MATCH" otherwise. Exit 0 on any match, 1 if none matched.

Dependencies: stdlib, pycryptodome, ecdsa, base58.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys

import base58
from Crypto.Cipher import AES
from ecdsa import SECP256k1, SigningKey

# The blob printed on the puzzle's last published page (128 base64 characters,
# decodes to 96 bytes: "Salted__" + 8-byte salt + 80 bytes of ciphertext).
BLOB_B64 = (
    "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
    "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
)

TARGET_ADDRESS = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# The escrow's public key, recovered from its 2024 spending transaction on chain
# (block 840725, txid 88cdb3cd...). Used only by the selftest, to certify the
# address-derivation half of the pipeline against a real, independently checkable
# fact: this pubkey's HASH160 must equal TARGET_ADDRESS.
KNOWN_PUBKEY_HEX = (
    "04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464"
    "9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559"
)


def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int) -> tuple[bytes, bytes]:
    """OpenSSL's legacy EVP_BytesToKey with MD5, the default for `openssl enc`
    without -md and the scheme used throughout this puzzle's earlier stages."""
    derived, prev = b"", b""
    while len(derived) < key_len + iv_len:
        prev = hashlib.md5(prev + password + salt).digest()
        derived += prev
    return derived[:key_len], derived[key_len:key_len + iv_len]


def unpad_pkcs7(data: bytes) -> bytes | None:
    if not data:
        return None
    n = data[-1]
    if n < 1 or n > 16 or n > len(data):
        return None
    if data[-n:] != bytes([n]) * n:
        return None
    return data[:-n]


def decrypt_blob(blob_b64: str, password: str) -> bytes | None:
    """Decrypt an OpenSSL "Salted__" AES-256-CBC blob. Returns the unpadded
    plaintext, or None if the header is malformed or padding does not validate."""
    raw = base64.b64decode(blob_b64)
    if raw[:8] != b"Salted__":
        return None
    salt, ciphertext = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(password.encode("utf-8"), salt, 32, 16)
    plain = AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext)
    return unpad_pkcs7(plain)


def readings(plain: bytes) -> list[tuple[str, bytes]]:
    """Standard ways to reduce a decrypted plaintext to a 32-byte private key
    candidate, with no judgment on how the bytes look (binary key material is
    expected, not printable text)."""
    out = [("sha256(plaintext)", sha256(plain))]
    if len(plain) >= 32:
        out.append(("first32", plain[:32]))
        out.append(("last32", plain[-32:]))
    if len(plain) >= 64:
        out.append(("sha256(first64)", sha256(plain[:64])))
    return out


def priv_to_address(priv_bytes: bytes) -> tuple[str, str]:
    """Uncompressed secp256k1 public key -> HASH160 -> P2PKH address. Returns
    (address, uncompressed_pubkey_hex)."""
    sk = SigningKey.from_string(priv_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()
    pub = b"\x04" + vk.to_string()
    h160 = hashlib.new("ripemd160", sha256(pub)).digest()
    address = base58.b58encode_check(b"\x00" + h160).decode()
    return address, pub.hex()


def wif_uncompressed(priv_bytes: bytes) -> str:
    return base58.b58encode_check(b"\x80" + priv_bytes).decode()


def attempt(candidate: str) -> tuple[bool, dict]:
    password = hashlib.sha256(candidate.encode("utf-8")).hexdigest()
    plain = decrypt_blob(BLOB_B64, password)
    if plain is None:
        return False, {"reason": "PKCS7 padding did not validate"}
    for name, key_bytes in readings(plain):
        if len(key_bytes) != 32:
            continue
        try:
            address, pub_hex = priv_to_address(key_bytes)
        except Exception:  # noqa: BLE001  out-of-range scalar, etc.
            continue
        if address == TARGET_ADDRESS:
            return True, {
                "reading": name,
                "address": address,
                "priv_hex": key_bytes.hex(),
                "wif": wif_uncompressed(key_bytes),
            }
    return False, {"reason": "padding valid, no reading matched the address"}


def selftest() -> bool:
    ok = True

    # Part 1: the address-derivation half of the pipeline, certified against a
    # real, independently checkable fact: the escrow's own on-chain public key
    # (recovered from its 2024 spending transaction) must hash to its address.
    pub = bytes.fromhex(KNOWN_PUBKEY_HEX)
    h160 = hashlib.new("ripemd160", sha256(pub)).digest()
    address_from_known_pubkey = base58.b58encode_check(b"\x00" + h160).decode()
    part1 = address_from_known_pubkey == TARGET_ADDRESS
    print(f"HASH160(known on-chain pubkey) -> {TARGET_ADDRESS}: {'OK' if part1 else 'FAIL'}")
    ok = ok and part1

    # Part 2: the AES decrypt implementation, certified against a self-made
    # OpenSSL-compatible vector (not from the puzzle: X is unsolved, so no real
    # password exists to test end to end). Proves evp_bytes_to_key + AES-256-CBC
    # + PKCS7 unpadding here reproduce `openssl enc -aes-256-cbc -d -a -salt`.
    test_password = "selftest password, not a puzzle answer"
    test_plaintext = b"0123456789abcdef" * 4  # 64 bytes, 5 AES blocks after padding
    salt = bytes.fromhex("00112233445566ff")
    key, iv = evp_bytes_to_key(test_password.encode("utf-8"), salt, 32, 16)
    pad_len = 16 - (len(test_plaintext) % 16)
    padded = test_plaintext + bytes([pad_len]) * pad_len
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(padded)
    made_blob = base64.b64encode(b"Salted__" + salt + ct).decode()
    recovered = decrypt_blob(made_blob, test_password)
    part2 = recovered == test_plaintext
    print(f"AES-256-CBC round trip (self-made vector): {'OK' if part2 else 'FAIL'}")
    ok = ok and part2

    # Part 2b: a wrong password must not validate (no false positive from a
    # coincidentally-valid PKCS7 padding byte).
    wrong = decrypt_blob(made_blob, "definitely the wrong password")
    part2b = wrong is None
    print(f"AES-256-CBC round trip, wrong password -> no valid padding: {'OK' if part2b else 'FAIL'}")
    ok = ok and part2b

    # Part 3: the real blob decodes to the documented shape (96 bytes total,
    # 8-byte salt, 80 bytes ciphertext = 5 AES blocks), independent of password.
    raw = base64.b64decode(BLOB_B64)
    part3 = raw[:8] == b"Salted__" and len(raw) == 96 and raw[8:16].hex() == "3ab585348552415d"
    print(f"published blob shape (96 bytes, salt 3ab585348552415d): {'OK' if part3 else 'FAIL'}")
    ok = ok and part3

    if ok:
        print("SELFTEST OK")
        print(
            "Note: parts 1, 2, 2b and 3 certify the pipeline's two halves "
            "independently. No end-to-end vector exists because X is unsolved."
        )
    return ok


def _print_result(candidate: str) -> bool:
    matched, info = attempt(candidate)
    if matched:
        print(f"MATCH {info['address']} reading={info['reading']} priv_hex={info['priv_hex']} wif={info['wif']}")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="candidate answer string X")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification checks")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            line = line.rstrip("\n")
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
