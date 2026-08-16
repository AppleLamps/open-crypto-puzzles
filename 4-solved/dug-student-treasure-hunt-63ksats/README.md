# Dug's Student Treasure Hunt, 2025 edition (63,216 sats, [SOLVED])

Dug, a UK business-school lecturer who posts on Nostr, hides a 12-word BIP39 seed one word per
lecture slide across a final-year university module, then funds a wallet from the derived
address as the prize. This has run annually since 2023. For the 2025 edition, eleven of the
twelve words lived only in private lecture slides, but Dug also re-encoded the full phrase in
December 2025 as a public "Seed Cipher" puzzle. I decoded that cipher, derived the seed, and
swept the one funded address a third party had missed. The larger share of the prize had
already been claimed by someone else five weeks earlier.

## At a glance

| | |
|---|---|
| Author | Dug, [Nostr](https://njump.me/npub1zrmu0amjmkynxlxgmdsyrjmp8vhxdz8ch5vja9vh9ym4natg8k5s8ge9wx) |
| Published | 2025-06-26, prize wallet funded (module ran September to November 2025) |
| Prize | 63,216 sats, the portion I recovered (about $40 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | 3 addresses, BIP84 `m/84'/0'/0'/0/i`, i = 0, 1, 2; all 3 now spent, see table below |
| Last on-chain check | 2026-08-16: all 3 addresses funded and fully spent, 159,186 sats total ever received |
| Status | SOLVED |
| Puzzle type | bip39-seed, text-cipher |
| Target format | BIP39 12 words, English, BIP84 `m/84'/0'/0'/0/i`, no passphrase |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the official BIP84 test vector and the solved mnemonic) |
| What remains | nothing; solved and paid out |
| Series | none in this folder; the author runs the same format annually |

## The puzzle as published

Dug posted one BIP39 word per themed lecture slide through the module, revealed progressively
from September to October 2025. Only the twelfth and final word reached a public channel: a
2025-10-07 Nostr slide reading "Twelfth and Final Treasure Hunt Word: 12. Kingdom" over an image
of Bodiam castle. The other eleven words were shown only inside the module's private teaching
platform.

In February 2026, Dug posted a second, independent puzzle: a handwritten sheet titled "Seed
Cipher #888888" (2026-02-12), using a free public template from Stackchain Magazine (method
credited to Keysa and D++). He later wrote, of the unclaimed balance, "still 76k sats in a
wallet" and, on 2026-06-29, "Added some more cheap sats to the treasure hunt prize."

## What is understood

### Mechanism

The Seed Cipher pairs 96 glyph patterns between a canonical "Cipher Key" page and a scrambled
"Ciphertext" page to define a permutation. Applying that permutation to Dug's handwritten grid
recovers, for each of the 12 word slots, the first four letters of a BIP39 word. Combined with
the public "kingdom" slide for word 12, this gives 12 short prefixes; validating candidates
against the BIP39 checksum and against the funded wallet identifies the exact words.

### Derivation and oracle

```
python3 tools/oracle.py --selftest                    # BIP84 test vector + solved mnemonic
python3 tools/oracle.py "twelve candidate words"       # MATCH / NO MATCH against the 3 funded addresses
python3 tools/oracle.py --stdin                        # one candidate per line
```

A candidate is normalized, checked against the BIP39 checksum, and its BIP84 `m/84'/0'/0'/0/0`,
`/1` and `/2` addresses are compared exactly to the three addresses the author actually funded.

### Certified against

`tools/oracle.py --selftest` reproduces the official BIP84 test vector
(`abandon x11 about` to `bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu`) and the solved mnemonic
below, which derives all three funded addresses exactly. Reproduced 2026-08-16.

### Established facts

1. The transcribed cipher grid gave 11 of 12 four-letter groups correctly; one cell pair in word
   10 was misread ("first" read as "fist"), corrected by validating the full candidate against
   the BIP39 checksum and the funded wallet rather than trusting the raw transcription.
2. The correct 12-word phrase ranked 14th out of 1,935 checksum-valid candidates generated from
   the transcribed cipher output.
3. Index 0 received exactly 75,082 sats, matching Dug's own "75k sats out of my own pocket"; the
   funding dates of indices 1 and 2 (2026-06-26) fall three days before his 2026-06-29 post about
   topping up the prize.

## What has been tested

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Words 1 to 11 posted somewhere public on Nostr | full pulled timeline plus OCR of module-window media | text and image search | 0 occurrences | yes: same pipeline recovers the public word-12 slide | 2026-08-01 |
| Direct brute force of the 11 unknown words | about 2^121 combinations | infeasible, not attempted | not run | n/a | 2026-08-01 |
| Cipher-derived candidates, checksum-valid, ranked by transcription error budget | 1,935 candidates | BIP84 address-as-oracle | 1 match, at rank 14 | yes: oracle certified against the BIP84 test vector | 2026-08-02 |

## Open leads, ranked

None. All three funded addresses are now spent; nothing remains open on this edition.

## Solution

**Answer** (BIP39, 12 words):
```
profit general lava hover jar visa joy immense install first give kingdom
```

**Derivation**: BIP84, account 0, external chain, index 1 (`m/84'/0'/0'/0/1`), empty passphrase.

**Key material**: private key hex
`864ceb763bb9b9b3d3ce198d9a3ca8c60a45fd2e9c319de363c8fe454e1dd4b0`, WIF
`L1imp7K4txGdShFoVmo6zCpvUQQpwRN2kBhyxrd9hRc8kvxZrxXD`, address
`bc1qphfklk568cf93267yetpngqsz0mthw4z4x2q69`.

**Payout**: txid
[`ee70de514686588173b64fc31fc317ae15f1e903c742cc99140d2cf1bb2e8db1`](https://mempool.space/tx/ee70de514686588173b64fc31fc317ae15f1e903c742cc99140d2cf1bb2e8db1),
block 960728, confirmed 2026-08-02, 59,916 sats to
`bc1qax0hsnwnxl7393awtc3hsy0ftm6tg4tyk2nfja` (3,300 sat fee, no RBF signaled, to avoid giving
a third party who might also hold the phrase extra time to react).

**The full 3-address ledger**:

| Index | Address | Received | State | Claimed by | Date |
|---|---|---|---|---|---|
| 0 | [`bc1qych2me6h85j38s3xmfwdkcvpqakpld3yr2y5ss`](https://mempool.space/address/bc1qych2me6h85j38s3xmfwdkcvpqakpld3yr2y5ss) | 75,082 sats | spent | a third party | 2026-07-08 |
| 1 | [`bc1qphfklk568cf93267yetpngqsz0mthw4z4x2q69`](https://mempool.space/address/bc1qphfklk568cf93267yetpngqsz0mthw4z4x2q69) | 63,216 sats | spent | me | 2026-08-02 |
| 2 | [`bc1qnclravnmv7vta9fhnp44hu3y85z3tfgz0n33wl`](https://mempool.space/address/bc1qnclravnmv7vta9fhnp44hu3y85z3tfgz0n33wl) | 20,888 sats | spent | the same third party | 2026-07-08 |

A third party solved the same cipher (or ran a wallet scan) and consolidated indices 0 and 2,
95,792 sats total, into
[`bc1qup92dhjszq7m8e0raj685uje0pehkz4qt9dvqt`](https://mempool.space/address/bc1qup92dhjszq7m8e0raj685uje0pehkz4qt9dvqt)
on 2026-07-08, five weeks before I found index 1. I received the smaller remaining share, not
the whole prize; I state that plainly rather than implying otherwise. No winner announcement
ever appeared on Dug's Nostr feed for this edition, unlike 2023 and 2024, when he publicly
congratulated the winning student.

**What it teaches about the series**: this edition adds a second, independent puzzle (the Seed
Cipher) on top of the original lecture-slide format, and the cipher alone was sufficient to
recover the seed without ever reading the private slides. A gap-limit wallet scan that stops
after the first unused address in sequence, rather than checking every funded index
individually, will miss a later-funded index like this one.

**How I got there**: I transcribed the cipher grid, generated every checksum-valid candidate
consistent with the transcription's likely error range, and checked each one against the three
funded addresses in order of transcription confidence. The correct phrase was 14th in that
ordered list, not the first guess.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | short, dated quotes from the author's own Nostr posts, with a profile link |
| `tools/oracle.py` | candidate checker: BIP39 checksum plus BIP84 address match against the 3 funded addresses, self-tested |

## Sources

- Dug, Nostr profile: https://njump.me/npub1zrmu0amjmkynxlxgmdsyrjmp8vhxdz8ch5vja9vh9ym4natg8k5s8ge9wx
- Payout transaction, mempool.space, 2026-08-02: https://mempool.space/tx/ee70de514686588173b64fc31fc317ae15f1e903c742cc99140d2cf1bb2e8db1
- Third-party consolidation transaction, mempool.space, 2026-07-08: https://mempool.space/tx/bcc2154f4eb33c361973313b9fe81131568b2f4ee3ef5a2c3e98dc327afd8074
