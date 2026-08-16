# Arweave Puzzle #3 (1000.165838006237 AR, [OPEN])

Tiamat (@ArweaveP), an Arweave project team member, posted this puzzle on the Arweave
permaweb on 2019-05-27: 8 hand-drawn rebus images, one per four-character answer, feeding
a client-side decryptor that unlocks an Arweave wallet keyfile holding 1000.17 AR. I
reversed the page's decrypt routine byte-for-byte and certified it against a solved
sibling puzzle in the same series. The mechanism and the oracle are both settled; what is
missing is 2 or more correct rebus readings. A diagnostic sweep freeing each of the 8
slots in turn, one at a time, found no rescue in any of them, so the block is specifically
in image interpretation, not in search. The author has called this the hardest puzzle in
the series and has said the puzzle was likely brute-forced once by an unknown solver who
never came forward with an answer.

## At a glance

| | |
|---|---|
| Author | Tiamat, [@ArweaveP on Twitter](https://twitter.com/arweavep) |
| Published | 2019-05-27, Twitter ([announcement](https://twitter.com/arweavep/status/1132936723162378240)) |
| Prize | 1000.165838006237 AR (about $1,810 at AR = $1.81, 2026-08-16) |
| Chain | arweave |
| Escrow | `wHP6OPG5GMF5dedo_CD8AAy6x8La-gfI5b5pk65Tx_0` ([explorer](https://viewblock.io/arweave/address/wHP6OPG5GMF5dedo_CD8AAy6x8La-gfI5b5pk65Tx_0)) |
| Last on-chain check | 2026-08-16: funded and unspent, 1000165838006237 winston |
| Status | OPEN |
| Puzzle type | word-selection, text-cipher |
| Target format | 8 four-character rebus answers, concatenated and lowercased, SHA-512 x11513, AES-decrypt to an Arweave JWK keyfile |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against solved sibling Arweave Puzzle Weave #8) |
| What remains | at least 2 of the 8 rebus readings are still wrong; needs a sharper visual/OSINT read, not more search |
| Series | Arweave Puzzles (this folder covers puzzle #3 only) |

## The puzzle as published

The live page (still up on the permaweb) shows one composite drawing split into 8 rebus
regions and 32 single-character input boxes grouped 4 at a time, one group per region.
Typing an answer into each group, concatenating in DOM order and lowercasing, and
clicking "proceed" runs the decrypt routine against the page's embedded ciphertext. The
author's only two per-image hints, both from his own tweet history: on the eighth image,
["Did anybody count the dots?"](https://twitter.com/arweavep/status/1152887601529073665)
(2019-07-21); on the third image,
["With N.1.7.0.0 release, third pic became obsolete"](https://twitter.com/arweavep/status/1177235139035836417)
(2019-09-26), a reference to an Arweave software release that replaced one mining
algorithm with another. On 2020-03-04 he
[ranked the series by difficulty](https://twitter.com/arweavep/status/1235199397371277315)
as "3, 9, 8, 5, 7", placing #3 first, meaning hardest.

## What is understood

### Mechanism

The page concatenates the 8 typed answers in DOM order, lowercases the result, stretches
it with SHA-512 applied 11,513 times, and uses the resulting 128-character hex digest as
an EvpKDF/AES-OpenSSL password to decrypt an embedded ciphertext. Success is declared
only if the decrypted plaintext contains the literal marker `"kty":"RSA"`, meaning it
decoded to a real Arweave wallet keyfile. This CryptoJS bundle carries a documented
library quirk (crypto-js issue #293): overriding the AES key size to 32 words turns the
cipher into a non-standard 1024-bit-key, 38-round Rijndael variant rather than textbook
AES-256. Forensic analysis of all 8 images (exiftool, binwalk, `zsteg -a`) found no
steganography: this is a pure visual rebus, not a data-hiding puzzle.

### Derivation and oracle

```
python3 tools/oracle.py --selftest       # reproduces the solved sibling Arweave #8
python3 tools/oracle.py "weve md12 a384 cash e4d5 root pull base"
python3 tools/oracle.py --stdin          # one candidate per line
```

A candidate is the 8 answers in image order (lowercased automatically). `MATCH <address>`
on a hit, `NO MATCH` otherwise. Since no dependency available to this repository
implements CryptoJS's non-standard Rijndael variant, the oracle reimplements it in pure
Python; the implementation was checked to reproduce a standard AES-256 library exactly at
the standard key size before being trusted at this puzzle's non-standard one.

### Certified against

`tools/oracle.py --selftest` decrypts the real ciphertext of the solved sibling Arweave
Puzzle Weave #8 with its published answer, `RasputinWilhelmAlekhine`, and recovers a JWK
whose derived address matches `ayJQH1S6Fi52OEokLVi2tl5kr_y39LSfhJcNV0z9Ny4` exactly, the
address baked into that puzzle's own success page. Puzzle #8's escrow is already spent
(checked 2026-08-16), so this is historical calibration data, not a live prize. The
oracle's raw decrypt output was also checked byte-for-byte against this puzzle's own
JavaScript decryptor running under Node, on both matching and non-matching passphrases.

### Established facts

1. The escrow is funded and unspent: 1000.165838006237 AR, checked via
   `arweave.net/wallet/<address>/balance` on 2026-08-16.
2. The decrypt mechanism is reproduced byte-for-byte from the live page's own script.
3. No steganography was found in any of the 8 rebus images or the page itself.
4. Freeing each of the 8 slots individually over the full 4-character charset, with the
   other 7 held at their current best-guess reading, produced 0 matches in all 8 runs,
   proving that at least 2 of the 8 current readings are wrong.
5. The series' 3 already-solved sibling puzzles (#5, #7, #8) show the author's answer
   grammar: the drawn object is never the literal answer; the answer is a specific proper
   noun, a notation, or a count. An earlier pass of this research over-fit puzzle #3's
   readings to Arweave-ecosystem jargon before recalibrating against this grammar.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Free-slot diagnostic (each of 8 slots freed alone, other 7 at best guess) | 13,440,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Curated top-N batteries under an Arweave-jargon reading (5 configurations) | 6,147,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Extended-charset and single-anchor-relaxation sweeps | approximately 102,000,000 to 126,000,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Top-8 and top-10 consolidated readings, all 8 slots | 133,400,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Word-order permutation sweeps, 3 different 8-word sets | 67,108,864 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Forensic steganalysis of all 8 images and the page | full file | exiftool, binwalk, zsteg -a | refuted: no hidden data | yes | 2026-06-22 |

Cumulative: on the order of 330,000,000 candidates tested against the current best-guess
readings, 0 matches.

## Open leads, ranked

1. **A sharper visual and OSINT reading of slots 1 and 7** (hours), the two most
   speculative images, plus arbitration between the leading candidates for slot 5 (a
   chess notation versus a year) and slot 8 (a service name versus a literal count). The
   3 already-solved siblings' answer grammar (proper nouns, notations, counts) is the
   filter to re-read the images through, rather than Arweave-ecosystem jargon. Confirmed
   by a full 8-slot candidate matching the escrow; killed only by exhausting every
   plausible reading of the remaining 2 images.
2. **Bounded 2-slot sweeps on the most-suspect slot pairs** (minutes once a reading is
   fixed), covering the case where exactly 2 of the current readings are wrong at once.
   Not yet run, since the readings to sweep around are still in flux.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/slot-1.png` ... `clues/slot-8.png` | the 8 official rebus images, one per answer slot, as published on the puzzle page |
| `clues/puzzle-composite.png` | the full composite drawing all 8 regions are cut from |
| `analysis/tested.md` | the complete negatives ledger, 16 configurations |
| `tools/oracle.py` | candidate checker: 8 answers to JWK address, certified against the solved sibling #8 |

## Sources

- Puzzle Weave 3 announcement, Twitter, 2019-05-27: https://twitter.com/arweavep/status/1132936723162378240
- Live puzzle page, Arweave permaweb: https://kszeqgxezf5quhzld4nhpasyilhxphclq2peqi5mrn7utxmqhwga.arweave.net/VLJIGuTJewofKx8ad4JYQs93nEuGnkgjrIt_Sd2QPYw
- "Did anybody count the dots?", Twitter, 2019-07-21: https://twitter.com/arweavep/status/1152887601529073665
- "With N.1.7.0.0 release, third pic became obsolete", Twitter, 2019-09-26: https://twitter.com/arweavep/status/1177235139035836417
- "The list of unsolved Arweave puzzles ordered by difficulty probably looks like: 3, 9, 8, 5, 7", Twitter, 2020-03-04: https://twitter.com/arweavep/status/1235199397371277315
- HomelessPhD/AR_Puzzles community repository, PZL3 entry: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL3
- Escrow wallet, viewblock.io: https://viewblock.io/arweave/address/wHP6OPG5GMF5dedo_CD8AAy6x8La-gfI5b5pk65Tx_0
