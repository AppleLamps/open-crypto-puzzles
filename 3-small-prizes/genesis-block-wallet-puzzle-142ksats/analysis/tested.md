# Tested (full negatives ledger)

The summary table in the folder's `README.md` shows the highlights; this file is the
complete record. Add one row per hypothesis family tested, in the order tested. Never remove
a row; if a hypothesis is retested with a different method, add a new row rather than editing
the old one.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 1, families A to D: the literal readings of the two 2026-08-28 hints (raw keys from windows of the coinbase text, BIP32 seeds and BIP39 entropy from the same text along 214 paths including every BIP48 path with a genesis integer as account, the other genesis fields), every ordered pair of the union | 447,916 distinct public keys (447,922 records with 6 witness copies), 200,634,118,084 ordered pairs | keys generated on the CPU by `tools/candidates.py` (22 processes, 15 s), pairs formed and hashed on the GPU by `engines/p2wsh_2of2_pairs.cu`, exact 32-byte compare with the escrow program; every GPU hit re-derived on the CPU with `tools/oracle.py` | 0 match | yes: the 2-of-2 pair revealed in block 963,629 placed at head, middle and tail of the key file, all 9 ordered combinations re-found, engine reported `exhausted=yes` | 1.95e9 ordered pairs/s on one RTX 5080, 103 s | 2026-08-29 |

## Pass 1 in full

200,634,118,084 ordered pairs tested, 0 match. Method: 447,916 distinct public keys built on
the CPU from four families, then every ordered pair (i, j) rebuilt as
`OP_2 <Ki> <Kj> OP_2 OP_CHECKMULTISIG`, hashed with SHA-256 on the GPU and compared byte for
byte with the escrow's witness program. Witness: the real 2-of-2 pair spent in block 963,629
(transaction `47ded3504e855ce418e46eeca4694b55a623d1e23a8e3c83292abbcf9cee9f7a`) inserted at
the head, the middle and the tail of the key file with its own program as a second target; all
9 ordered head/middle/tail combinations were re-found and confirmed on the CPU, and no other
hit appeared. Rate: 1.95e9 ordered pairs/s on one RTX 5080, 103 s elapsed. Date: 2026-08-29.

Exact scope of the key set (labels in `labels.tsv` produced by `tools/candidates.py --write`):

- A, raw private keys: every 1 to 32-byte window of the 69-byte coinbase text T, the 47-byte
  headline J, the 77-byte scriptSig S and the lower and upper-case forms of T and J, read as a
  big-endian integer, a little-endian integer and right-padded to 32 bytes; windows longer
  than 32 bytes reduced modulo the curve order (big and little-endian); the 12 genesis
  integers {0, 1, 2, 3, 9, 50, 2009, 3012009, 20090103, 1231006505, 2083236893, 486604799};
  the other fields (D). Compressed keys, plus uncompressed keys for T, J, S, the integers and
  the fields. 36,816 integers, 54,264 keys before deduplication.
- B, BIP32 seeds: each whole text, its 16/20/24/28/32/64-byte windows, T[32:], T[22:] and the
  fields of at least 16 bytes (1,370 seeds), each derived along 214 paths: `m/48'/0'/a'`,
  `m/48'/0'/a'/s'`, `m/48'/0'/a'/s'/0/0`, `/0/1`, `/1/0` and `m/48/0/a/s/0/0` for every
  genesis integer a and script type s in {0, 1, 2}; `m`, `m/0`, `m/0/0`, `m/0/1`, `m/1/0`,
  `m/0'`, `m/0'/0`, `m/0'/0'`, `m/0'/0'/0'`, `m/44'/0'/0'/0/0`, `m/44'/0'/0'/0/1`,
  `m/44'/0'/0'`, `m/49'/0'/0'/0/0`, `m/84'/0'/0'/0/0`, `m/84'/0'/0'/0/1`, `m/86'/0'/0'/0/0`,
  `m/45'`, `m/45'/0/0`, `m/45'/0/0/0`, `m/45'/1/0/0`, `m/48'`, `m/48'/0'`. 293,180 keys.
- C, BIP39 entropy: the 16/20/24/28/32-byte windows of the same texts and the prefixes of the
  32-byte fields, English mnemonic, seed with an empty passphrase and with T as passphrase
  (2,730 seeds), same 214 paths. 584,220 keys.
- D, other fields as raw keys: merkle root (both byte orders), block hash (both), coinbase
  public key and its x and y coordinates, header, coinbase transaction, nonce, time, bits and
  version (both byte orders). 90 keys.

The union deduplicates to 447,916 keys because J is a suffix of T, T is a suffix of S, and the
case-changed forms share every window without a letter.

What this negative does not cover: a root built by a library step not modeled here (a raw
private key with a zero chain code, a raw extended key made of 32 key bytes plus 32 chain-code
bytes, BIP85, SLIP-39), hashed roots (the author said "no hash", but a SHA-256 of the text as
seed or key costs nothing to add), paths outside the list above, a passphrase other than empty
or T, and any witness script other than `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG` with 33-byte keys
(uncompressed keys were only tried for family A and D).
