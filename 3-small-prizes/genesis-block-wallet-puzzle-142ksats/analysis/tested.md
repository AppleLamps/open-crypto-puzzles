# Tested (full negatives ledger)

The summary table in the folder's `README.md` shows the highlights; this file is the
complete record. Add one row per hypothesis family tested, in the order tested. Never remove
a row; if a hypothesis is retested with a different method, add a new row rather than editing
the old one.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 1, families A to D: the literal readings of the two 2026-08-28 hints (raw keys from windows of the coinbase text, BIP32 seeds and BIP39 entropy from the same text along 214 paths including every BIP48 path with a genesis integer as account, the other genesis fields), every ordered pair of the union | 447,916 distinct public keys (447,922 records with 6 witness copies), 200,634,118,084 ordered pairs | keys generated on the CPU by `tools/candidates.py` (22 processes, 15 s), pairs formed and hashed on the GPU by `engines/p2wsh_2of2_pairs.cu`, exact 32-byte compare with the escrow program; every GPU hit re-derived on the CPU with `tools/oracle.py` | 0 match | yes: the 2-of-2 pair revealed in block 963,629 placed at head, middle and tail of the key file, all 9 ordered combinations re-found, engine reported `exhausted=yes` | 1.95e9 ordered pairs/s on one RTX 5080, 103 s | 2026-08-29 |
| Pass 2, families A to D plus E (hashed roots: SHA-256, double SHA-256, hash160, SHA-512 of each text as raw key, BIP32 seed and BIP39 entropy), F (raw extended key: 32 key bytes plus 32 chain-code bytes taken from the text, swapped and reversed forms), G (raw key with a zero chain code for the 16 to 32-byte windows of the text, the texts modulo n, the genesis integers and the fields), all along the same 214 paths, every ordered pair of the union | 611,008 distinct public keys (611,014 records with 6 witness copies), 373,338,108,196 ordered pairs | same pipeline as pass 1 with `tools/candidates.py --pass 2` (22 processes, 17 s) | 0 match | yes: same witness pair at head, middle and tail, all 9 ordered combinations re-found, `exhausted=yes` | 4.18e9 ordered pairs/s on one RTX 5080, 89 s | 2026-08-29 |

## Pass 2 in full

373,338,108,196 ordered pairs tested, 0 match. Method: the pass 1 key set plus 165,064 keys
from three more families (16,548 E, 2,996 F, 145,306 G before deduplication), 611,008 distinct
public keys in total, every ordered pair rebuilt as the 2-of-2 witness script, hashed on the GPU
and compared byte for byte with the escrow's witness program. Witness: same protocol as pass 1,
9 of 9 ordered head/middle/tail combinations re-found and confirmed on the CPU, no other hit.
Rate: 4.18e9 ordered pairs/s on one RTX 5080, 89 s elapsed. Date: 2026-08-29.

Scope added by pass 2 (labels E:, F:, G: in `labels.tsv`):

- E, hashed roots despite "no hash": SHA-256, double SHA-256, hash160 and SHA-512 of each of
  the 7 texts, each used (1) as a raw private key (first 32 bytes big-endian and reversed; for
  SHA-512 also the second half and the whole digest modulo n), (2) as a BIP32 seed, (3) as
  BIP39 entropy of 32 and 16 bytes with an empty passphrase, then the 214 paths. 70 integers,
  77 seeds.
- F, raw extended key: master private key = X[:32] and chain code = X[32:64] for X in T, S,
  the lower and upper-case forms of T, and the byte-reversed T and S, plus the two halves
  swapped, plus T[:32] with T[37:69] and its swap, then the 214 paths. 14 roots.
- G, raw private key imported with a zero chain code: every 16/20/24/28/32-byte window of T
  read big-endian, little-endian and right-padded, T, J and S modulo n, the 12 genesis
  integers, and the fields of at most 32 bytes, then the 214 paths. 680 roots.

After pass 2 the mechanical readings of "root -> multisig -> mainnet -> genesis_data ->
script_type" with the coinbase text as the source are closed on this list of paths. Still not
covered: SLIP-39, BIP85, a passphrase other than empty or T, paths outside the 214, and a
witness script other than `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG` with compressed keys.

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
