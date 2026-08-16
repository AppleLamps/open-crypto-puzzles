# VeteranHODL: Hunting Time (420,000 sats, [OPEN])

VeteranHODL, on X, hid a real BIP39 seed phrase inside their novel "Hunting Time" and ran a
13-post clue campaign from 2026-06-15 to 2026-08-13, releasing one numbered photograph a week.
Each clue image gives one word of a 12-word phrase, in publication order. The author states the
funds sit in an Electrum wallet. I read every clue and built a candidate word pool for all 12
positions, but the search of that pool is only partly run, and the Electrum-format derivation the
author actually named has no certified test vector yet. The escrow, doubled by a second funding
just before the campaign closed, remains unclaimed.

## At a glance

| | |
|---|---|
| Author | VeteranHODL, [X](https://x.com/VeteranHODL) |
| Published | clue campaign 2026-06-15 to 2026-08-13 (13 posts); novel publication date not stated by the author |
| Prize | 420,000 sats (about $265 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `bc1qhzy6j4amw26z7e694mgfr7kvzl7xteu54f0a85` ([explorer](https://mempool.space/address/bc1qhzy6j4amw26z7e694mgfr7kvzl7xteu54f0a85)) |
| Last on-chain check | 2026-08-16: funded and unspent, 420,000 sats total across 2 funding transactions |
| Status | OPEN |
| Puzzle type | bip39-seed, book, word-selection |
| Target format | 12-word phrase, one word per clue image in publication order; author states an Electrum wallet |
| Certified oracle | yes, for the BIP39 to BIP84 branch only: `tools/oracle.py --selftest`; the Electrum-seed branch the author actually named is implemented but not certified (no known-good vector) |
| What remains | the full 12-word phrase; the semantic candidate-word sweep is about 20 percent run and not certified with a witness |
| Series | none |

## The puzzle as published

The campaign opened 2026-06-15: "Did you know that the code on the cover of Hunting Time is from
the Genesis Block? I wonder if anyone has found the other hidden code yet..."
([post](https://x.com/VeteranHODL/status/2066614083105738752)). On 2026-06-29 the author
announced the hunt directly: "Hidden within the pages of Hunting Time is a genuine Bitcoin seed
phrase. Over the coming weeks I'll release a series of clues to help readers uncover it. Find the
clues. Recover the wallet. Keep what's inside. The hunt starts now."
([post](https://x.com/VeteranHODL/status/2071632285951226106)). Eleven more numbered clue images
followed weekly through "FINAL CLUE" on 2026-08-13
([post](https://x.com/VeteranHODL/status/2087893684633141356)).

On 2026-08-01 the author named the wallet type and disclosed a second funding: "Three years ago,
when I started writing Hunting Time, I sent 210,000 sats to a fresh electrum wallet... A generous
stranger just topped it up with another 210,000 Satoshis, but has left the wallet unclaimed."
([post](https://x.com/VeteranHODL/status/2083486983142142452)). On 2026-08-03 the author
corrected a rumor that the puzzle had been solved: "The wallet containing 420,000 Satoshis
remains unclaimed." ([post](https://x.com/VeteranHODL/status/2084315859770872026)).

## What is understood

### Mechanism

Each of the 12 numbered clue images corresponds to one word of the phrase, in the order the
author posted them, so there is no ordering ambiguity once the words are known. 9 of the 12
images carry a visible painted, stamped, or displayed number; 3 carry no number and must be read
purely from their visual content. Each image reading yields a pool of 4 to 7 candidate BIP39
words.

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "w1 w2 ... w12"
```

The oracle checks a 12-word candidate against two branches: standard BIP39 to BIP84
(`m/84'/0'/0'/0/i`, empty passphrase, address indexes 0 to 4), and an Electrum segwit seed
(salt "electrum", path `m/0'/0/i`, no BIP39 checksum). Only the first branch is certified.

### Certified against

The BIP39/BIP84 branch reproduces the public 12-word BIP39 test vector (all-zero entropy) at
`m/84'/0'/0'/0/0`, reproduced 2026-08-16. The Electrum branch has no known-good seed-and-address
pair to certify against; it is included because it is the format the author explicitly named, but
a "no match" result on it alone proves nothing yet.

### Established facts

1. The escrow was funded twice, 210,000 sats on 2023-07-22 and 210,000 sats on 2026-07-31, and
   remains fully unspent as of 2026-08-16.
2. The address is a standard bech32 P2WPKH address with no reading trap: the two funding
   transactions are unambiguous and correctly typed.
3. The author states the wallet is Electrum, a detail with no certified oracle in this folder yet.
4. The visible numbers on 9 of the 12 clue images are not yet purged of non-BIP39 words in the
   candidate pool, which crashed one derivation attempt (see tested.md).

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Semantic candidate pool from the 12 image readings, combinatorial sweep | 393,750,000 combinations, stopped at about 20 percent | BIP39 checksum filter, then address comparison | 4,924,764 checksum-valid phrases found in the partial run; not run against the target address | none: no synthetic witness was planted in this run | 2026-08-15 |
| Visible numbers read as BIP39 wordlist indices | 22,118,400 combinations planned | direct index lookup | run crashed on a non-BIP39 word in one candidate pool; hypothesis never actually tested | uncertified (crashed before any comparison) | 2026-08-15 |

## Open leads, ranked

1. **Certify the Electrum derivation branch** (minutes to hours). This is the only wallet format
   the author has explicitly named, and precisely the branch with no known-good vector. A
   documented Electrum seed and its resulting address, from Electrum's own documentation or
   generated and read back by the software itself, would settle whether any negative on this
   branch means anything.
2. **Re-run the numeric-index hypothesis after cleaning the candidate pools** (minutes). With 9 of
   12 positions fixed by their visible numbers, only 3 positions remain free once the crash is
   fixed, dropping the space to a few million combinations.
3. **Recover the book's cover image**, referenced in the opening post as carrying a first code
   from the Genesis Block and hinting at a second hidden code, but never brought into this folder.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | the 13 X posts, verbatim, with dates and links |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the ranked leads |
| `tools/oracle.py` | candidate checker, BIP39/BIP84 branch certified, Electrum branch uncertified |

## Sources

- VeteranHODL on X: https://x.com/VeteranHODL
- Opening post: https://x.com/VeteranHODL/status/2066614083105738752
- Hunt announcement: https://x.com/VeteranHODL/status/2071632285951226106
- Wallet type and second funding: https://x.com/VeteranHODL/status/2083486983142142452
- Correction of the "solved" rumor: https://x.com/VeteranHODL/status/2084315859770872026
- Final clue: https://x.com/VeteranHODL/status/2087893684633141356
