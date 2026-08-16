# bc1q21 Time-Lock Challenge, Level 5 (100,000 sats, [SOLVED])

bc1q21 is a Bitcoin time-locked gift service that ran a 12-day riddle challenge in July 2026,
posting one clue per day, each resolving to a BIP39 word under a wordlist-constrained reading.
The 100,000-sat prize sat behind a Bitcoin script (P2SH, CheckLockTimeVerify) that only becomes
spendable after a locktime the operator never announced directly. I recovered the 12-word phrase
from the daily clues, then found the exact locktime and spending key by treating the lock
address itself as an offline oracle, without ever decrypting the encrypted data the operator
attached to the puzzle. I claimed the prize the same day the lock expired.

## At a glance

| | |
|---|---|
| Author | bc1q21, [site](https://bc1q21.com) |
| Published | 2026-07-13, first daily clue (site: [bc1q21.com](https://bc1q21.com)) |
| Prize | 100,000 sats locked (about $63 at BTC = $63,000, 2026-08-16); I received 99,604 sats after fee |
| Chain | bitcoin |
| Escrow | P2SH `37xcRXcYRht9VZJeLYWegDRC2fjX5XVnAp` ([explorer](https://mempool.space/address/37xcRXcYRht9VZJeLYWegDRC2fjX5XVnAp)) holding the prize; `bc1q3pwpgp7dkhtzj6qya39l8tu6dgdarv9gr9kx0r` ([explorer](https://mempool.space/address/bc1q3pwpgp7dkhtzj6qya39l8tu6dgdarv9gr9kx0r)) as the word-recovery oracle |
| Last on-chain check | 2026-08-16: both addresses funded and fully spent |
| Status | SOLVED |
| Puzzle type | bip39-seed, timelock |
| Target format | BIP39 12 words, English, BIP84 `m/84'/0'/0'/0/0` for the oracle address; CLTV spend key at `m/44'/0'/0'/0/0`, no passphrase |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the official BIP84 test vector and the solved mnemonic) |
| What remains | nothing; solved and paid out |
| Series | none; this folder covers Level 5 only |

## The puzzle as published

Between 2026-07-13 and 2026-07-24, bc1q21 posted one riddle per day on X, Primal and YouTube
(not on the bc1q21.com site itself), each with a letter-count hint for one BIP39 word. Day 1:
"A Bitcoin time-locked gift isn't something you eat, but every gift still has a place where it
belongs. The gift ___ be yours." (3 letters, answer "can"). Day 6, the clue that revealed the
operator's writing constraint: "A Bitcoin transaction can be confirmed surprisingly _____
compared to traditional international banking." (5 letters; the natural word "fast" is not in
the BIP39 wordlist, so the operator wrote "quick" instead). The site's own public JavaScript
source documents the time-lock contract construction and its two derivation paths.

## What is understood

### Mechanism

The riddles were written under a hidden constraint: whenever the natural English answer is not
a BIP39 word, or is the wrong length, the operator substitutes the closest BIP39 word available.
This held for 7 of the 12 words and was the single most productive reading key. Separately, the
prize sits in a P2SH output whose redeem script encodes a CheckLockTimeVerify clause; the
address itself is the hash of that script, so a candidate (derivation path, locktime) pair can
be checked offline by hashing it and comparing to the known P2SH address, with no need to
decrypt anything the operator attached to the puzzle.

### Derivation and oracle

```
python3 tools/oracle.py --selftest                    # BIP84 test vector + solved mnemonic
python3 tools/oracle.py "twelve candidate words"       # MATCH / NO MATCH against the funding-oracle address
python3 tools/oracle.py --stdin                        # one candidate per line
```

A candidate is checked against the BIP39 checksum, then its BIP84 `m/84'/0'/0'/0/0` address is
compared exactly to the funding-oracle address. The redeem-script and locktime reconstruction is
a separate, one-off offline search (path times candidate midnight-UTC date), not part of this
uniform interface.

### Certified against

`tools/oracle.py --selftest` reproduces the official BIP84 test vector
(`abandon x11 about` to `bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu`) and the solved mnemonic,
which derives the funding-oracle address exactly. Reproduced 2026-08-16.

### Established facts

1. The BIP84 `m/84'/0'/0'/0/0` address of the solved mnemonic matches
   `bc1q3pwpgp7dkhtzj6qya39l8tu6dgdarv9gr9kx0r` exactly.
2. The BIP44 `m/44'/0'/0'/0/0` public key of the same mnemonic,
   `028d570df5e21b1ca0ef88c3c06f02acf516e673bc32d473a5484f685ce05f8875`, matches the pubkey
   embedded in the redeem script that actually spent the P2SH output, byte for byte.
3. Day 11's obvious reading, "joy" (as in "joyride"), is wrong; the correct word is "ski." This
   was a deliberate trap for anyone testing only the single most likely word per position.

## What has been tested

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Balanced candidate set, about 6 words per position across all 12 positions | 2,488,320,000 combinations | BIP39 checksum plus BIP84 address-oracle | 1 match, at 29 percent of the sweep | yes: oracle certified against the BIP84 test vector | 2026-07-24 |
| Narrower candidate set (3 per position) plus 1 rolling wildcard position | 900,000,000 combinations | same oracle | not needed, superseded by the balanced-set match | n/a | 2026-07-24 |
| CLTV redeem-script and locktime reconstruction | 380 derivation paths times about 1,100 candidate midnight-UTC dates | hash candidate script, compare to the P2SH address | 1 match | yes: reconstructed script spent the real output | 2026-07-24 |

## Open leads, ranked

None. Both addresses are spent; nothing remains open on Level 5.

## Solution

**Answer** (BIP39, 12 words):
```
can large cool deny mean quick wish spare argue body ski spot
```

**Derivation**: word recovery certified via BIP84 `m/84'/0'/0'/0/0` against the funding-oracle
address. The prize itself was unlocked with the CLTV spend key at BIP44 `m/44'/0'/0'/0/0`.

**Key material** (CLTV spend key, the one that actually signed the claim): private key hex
`172059895de77a7681ff170fea3d2cee09f7147571ae476aebb44fd154742def`, WIF
`KwzfZ3ey7EFT99vinHiwnxXivw33bEW6Mrju6oND53irRmvaZtfs`. Reconstructed redeem script (never
decrypted, only reconstructed by matching the P2SH hash):
`0400ab626ab17521028d570df5e21b1ca0ef88c3c06f02acf516e673bc32d473a5484f685ce05f8875ac`, locktime
`1784851200` (2026-07-24 00:00 UTC).

**Payout**: txid
[`73baf40f668fb221b6b9c934f199a51f7e0ab1f1bb585e07c18a7b3e88dfd7ed`](https://mempool.space/tx/73baf40f668fb221b6b9c934f199a51f7e0ab1f1bb585e07c18a7b3e88dfd7ed),
block 959447, confirmed 2026-07-24, 99,604 sats to
`bc1qax0hsnwnxl7393awtc3hsy0ftm6tg4tyk2nfja` (396 sat fee).

**What it teaches about the series**: a time-locked script's own address is a free, offline
oracle for its redeem script, as long as the derivation path and the locktime are both within a
searchable range. Any similar time-locked puzzle from this operator, or from another one using a
CLTV or CSV script, does not need its encrypted attachment decrypted at all: the lock consensus
itself, plus the address, is enough.

**How I got there**: I first treated the encrypted data the operator attached to the puzzle as
the path to the redeem script, and it was not needed at all. Once I recognized the P2SH address
as a hash I could match directly, the locktime search took seconds; the word-recovery side took
longer because the naive per-position best guess (for example "joy" on day 11) was wrong, and
only a balanced candidate set across all positions reached the correct combination.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | 3 representative daily clues, verbatim, with dates |
| `tools/oracle.py` | candidate checker: BIP39 checksum plus BIP84 address match against the funding-oracle address, self-tested |

## Sources

- bc1q21, official site: https://bc1q21.com
- Claim transaction, mempool.space, 2026-07-24: https://mempool.space/tx/73baf40f668fb221b6b9c934f199a51f7e0ab1f1bb585e07c18a7b3e88dfd7ed
- Time-lock creation transaction, mempool.space, 2026-07-03: https://mempool.space/tx/d2c8237bd6d107a4d08ab390c0bfa4f21f4e52a19d8672d66012bceaab881901
