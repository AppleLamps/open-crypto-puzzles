# Arweave Puzzle Weave #12 (400.00248121 AR, [OPEN])

Tiamat (@ArweaveP) published this puzzle on the Arweave permaweb on 2020-04-29 and
announced it on Twitter on 2020-05-05: a single jigsaw image with 4 pieces (a row of
flags, a whale beside a date, geometric shapes carrying digit strings, and 5 hatched
letters), feeding one free-text field into the same decrypt routine used across this
author's series. The author confirmed the answer is exactly 58 characters and
case-sensitive. I reversed and certified the decrypt pipeline against a solved sibling
puzzle, and solved one of the 4 sub-answers with certainty from the page's own printed
numbers. A second sub-answer has a strong but unconfirmed reading, a third is refuted as
an ordering scheme, and the fourth, a company or investor named after a whale, has not
been identified. 3,148,564 assembled 58-character candidates have been tested with 0
matches.

## At a glance

| | |
|---|---|
| Author | Tiamat, [@ArweaveP on Twitter](https://twitter.com/arweavep) |
| Published | 2020-05-05, Twitter ([announcement](https://twitter.com/arweavep/status/1257613928185675776)), page live since 2020-04-29 |
| Prize | 400.00248121 AR (about $724 at AR = $1.81, 2026-08-16) |
| Chain | arweave |
| Escrow | `XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg` ([explorer](https://viewblock.io/arweave/address/XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg)) |
| Last on-chain check | 2026-09-15: funded and unspent, 400.00248121 AR, 0 outgoing transactions ever |
| Status | OPEN |
| Puzzle type | word-selection, geometry, text-cipher |
| Target format | one 58-character case-sensitive answer, 4 sub-answers concatenated with no separator, SHA-512 x11513, AES-decrypt to an Arweave JWK keyfile |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against solved sibling Arweave Puzzle Weave #8) |
| What remains | piece 2's exact string; every source-material pairing that closes the 58-character budget is now a negative |
| Series | Arweave Puzzles (this folder covers puzzle #12 only) |

## The puzzle as published

The live page shows one jigsaw JPEG cut into 4 pieces and a single free-text input field
wired to the decrypt routine. Piece 1 shows 6 flags in 3 vertical pairs; piece 2 shows a
whale beside the handwritten date "16-03-2020"; piece 3 shows geometric shapes each
carrying a printed digit string; piece 4 shows 5 letters rendered in a hatching pattern.
On 2020-05-23, replying to a question about the answer format, the author wrote,
["58 chars CS"](https://twitter.com/arweavep/status/1264211142714499072), confirming an
exact 58-character, case-sensitive answer. On 2020-04-14 he posted a series-wide status
update,
["1,2,4,8 = solved / 3,5,7,9 = not solved yet"](https://twitter.com/arweavep/status/1250036746802298885),
placing puzzle #12 among the unsolved half of the series at that time.

## What is understood

### Mechanism

The page reads the single free-text field verbatim (case-sensitive, no trimming),
stretches it with SHA-512 applied 11,513 times, and uses the resulting 128-character hex
digest as an EvpKDF/AES-OpenSSL password to decrypt an embedded ciphertext. Success is
declared only if the plaintext contains the literal marker `"kty":"RSA"`. This CryptoJS
block is byte-identical, script for script, to the ones in sibling puzzles #3 and #8,
including the same non-standard 1024-bit-key, 38-round Rijndael quirk (crypto-js issue
#293). The 58-character answer is the concatenation, in piece order, of the 4 jigsaw
sub-answers, with no separator between them.

### Derivation and oracle

```
python3 tools/oracle.py --selftest          # reproduces the solved sibling Arweave #8
python3 tools/oracle.py "BlueAndreessenHorowitz2111011Alien"
python3 tools/oracle.py --stdin             # one candidate per line
python3 tools/oracle.py --fast --stdin      # block-0 reject; hits re-checked in full
```

A candidate is passed through exactly as typed (case-sensitive, no trimming).
`MATCH <address>` on a hit, `NO MATCH` otherwise. Since no dependency available to this
repository implements CryptoJS's non-standard Rijndael variant, the oracle reimplements
it in pure Python; the implementation was checked to reproduce a standard AES-256 library
exactly at the standard key size before being trusted at this puzzle's non-standard one.

### Certified against

`tools/oracle.py --selftest` decrypts the real ciphertext of the solved sibling Arweave
Puzzle Weave #8 with its published answer, `RasputinWilhelmAlekhine`, and recovers a JWK
whose derived address matches `ayJQH1S6Fi52OEokLVi2tl5kr_y39LSfhJcNV0z9Ny4` exactly, the
address baked into that puzzle's own success page. Puzzle #8's escrow is already spent
(checked 2026-08-16), so this is historical calibration data, not a live prize. The
oracle's raw decrypt output was also checked byte-for-byte against this puzzle's own
JavaScript decryptor running under Node, on both matching and non-matching passphrases.

### Established facts

1. The escrow is funded and unspent: 400.00248121 AR, checked via
   `arweave.net/wallet/<address>/balance` on 2026-09-15; a GraphQL query for the wallet's
   own transaction history returns 0 outgoing transactions ever.
2. The author confirmed the answer is exactly 58 characters, case-sensitive.
3. Piece 3 is solved with certainty: the shapes read as `2111011` (spelling HEXAGON, one
   digit per letter, 0 for a descender, 1 for x-height, 2 for an ascender), a rule that
   reproduces all 3 printed numbers on the page with no free parameter.
4. Piece 4's hatching direction is not an ordering scheme: all 24 direction-to-digit
   assignments across 6 quadrant reading orders (144 combinations) fail to produce a
   1-to-5 permutation or a valid 5-letter word.
5. No steganography was found in the jigsaw image or the page's favicon (no EXIF or XMP
   data, no trailing bytes, `zsteg -a` returns noise only); the author's wallet history
   shows no companion transaction near the funding or publication window other than a PNG
   image identical to sibling puzzle #11's.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Piece 4 hatching as an ordering scheme | 144 combinations | exhaustive structural check | refuted: no valid permutation or word | yes | 2026-07-25 |
| Round-1 bounded assembly (4 sub-answers, 24 orders, 3 cases, length-filtered to 58) | 104,184 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Round-2, 2 surviving length partitions (6 orders, 36 color names, 2 cases) | 46,688 | certified oracle | 0 match | uncertified | 2026-07-25 |
| "BLUE" literal readings (6 bounded runs: orders, spellings, cases, anagrams) | 3,266 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Literal Hexagon / BalaenopteraMusculus / number-reordering partitions | 1,824 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Piece 1 as RGB decimal or hex numbers instead of color words | 768 | certified oracle | 0 match | uncertified | 2026-07-25 |
| New 18-character piece-2 (orgs, founder, whale+date, Grants+Boost) | 64,800 | certified oracle, `--fast` | 0 match | uncertified-space | 2026-09-15 |
| Length-8 date x hex+IQ/AR piece 1 | 8,640 | certified oracle, `--fast` | 0 match | uncertified-space | 2026-09-15 |
| Cerulean-for-Blue x 14-character piece 2 | 10,800 | certified oracle, `--fast` | 0 match | uncertified-space | 2026-09-15 |
| 24 block orders of the 6 strongest new piece-2 strings | 10,368 | certified oracle, `--fast` | 0 match | uncertified-space | 2026-09-15 |
| Forbes-date 18-character concatenations | 10,800 | certified oracle, `--fast` | 0 match | uncertified-space | 2026-09-15 |
| All 120 IEALN orders on the 10 strongest new piece-2 strings | 28,800 | certified oracle, `--fast` | 0 match | uncertified-space | 2026-09-15 |

Cumulative: 3,148,564 assembled 58-character candidates tested against the escrow, 0
matches. Rows 7-19 of the full ledger are in [analysis/tested.md](analysis/tested.md).

## Open leads, ranked

Ranked list in [analysis/leads.md](analysis/leads.md). Short version:

1. **Piece 2 as a non-name encoding** (hours). Every source-material pairing that closes
   p1 + p2 = 46 is now a negative, including `AndreessenHorowitz`, 35 other 18-character
   concatenations, `16032020` with hex+IQ/AR, and Cerulean-for-Blue. Sibling #5 used a
   symbol, a number, an acronym and a name; another English proper noun is the wrong
   shape of search.
2. **A leftover piece-1 encoding of length 4 or 6** (hours, weakly). Those force 42- and
   40-character piece-2 strings. An Ethereum address is 42 characters, but the drawn
   date's funding round was not an on-chain transfer.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/puzzle-image.jpg` | the published jigsaw puzzle image, byte-exact |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | ranked open and retired leads |
| `tools/oracle.py` | candidate checker, including `--fast` block-0 reject, certified against sibling #8 |
| `tools/sweep_new_piece2.py` | bounded sweep for rows 20-22 and 24 |

## Sources

- "Puzzle 12 is here", Twitter, 2020-05-05: https://twitter.com/arweavep/status/1257613928185675776
- Live puzzle page, Arweave permaweb, 2020-04-29: https://arweave.net/gymumAAsxGlzqPL5HzoEB8Xryu61o174j7vHwx21Qoo
- "58 chars CS", Twitter, 2020-05-23: https://twitter.com/arweavep/status/1264211142714499072
- "1,2,4,8 = solved / 3,5,7,9 = not solved yet", Twitter, 2020-04-14: https://twitter.com/arweavep/status/1250036746802298885
- HomelessPhD/AR_Puzzles community repository, PZL12 entry: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL12
- Escrow wallet, viewblock.io: https://viewblock.io/arweave/address/XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg
