# LuckyLurker Seed Riddles (80,000 sats, [OPEN])

The crypto-casino affiliate site luckylurker.com published a Bitcoin puzzle on
its own "Bitcoin Vault" page in March 2026: 12 hints, labeled "Word #1" through
"Word #12", each pointing at one word of a 12-word BIP39 seed in a fixed 1:1
position. Four hints send the reader to a specific review article on the same
site, where exactly one word is marked in italics; all four marked words are
valid BIP39 words, giving 4 of 12 words as ground truth. The other 8 hints are
one-line riddles with no such structural marker. I searched about 2 million
position-combinations of plausible synonyms for those 8 riddles against the
known 4 words, with zero exact match, which tells me the true words are not
inside the obvious synonym sets I tried. The lock here is interpretation, not
computation: once the 8 words are pinned, checking a full candidate takes a
fraction of a second.

## At a glance

| | |
|---|---|
| Author | unknown individual; published on luckylurker.com |
| Published | 2026-03-17, luckylurker.com/bitcoin-vault/, all 12 hints released at once |
| Prize | 80,000 sats (about $50 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `bc1q32e3dxcd0n2tlzdmchraf2057d0ax4xdwrk3jq` ([explorer](https://mempool.space/address/bc1q32e3dxcd0n2tlzdmchraf2057d0ax4xdwrk3jq)) |
| Last on-chain check | 2026-08-16: funded and unspent (80,000 sats, 2 transactions) |
| Status | OPEN |
| Puzzle type | bip39-seed, word-selection, text-cipher |
| Target format | BIP39 12 words (English), fixed 1:1 position mapping from the 12 hints, most likely BIP84 `m/84'/0'/0'/0/0` (script type v0_p2wpkh), no passphrase stated |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the public BIP39/BIP84 test vectors, since no solved sibling exists on this site) |
| What remains | pinning the exact intended word for 8 of 12 riddle-style hints; 4 of 12 are already fixed |
| Series | none |

## The puzzle as published

The vault page lists 12 hints labeled by position. Four point at a specific
article on the same site and are quoted here in full since they name the
mechanism directly: hint 3, "The word is hidden inside this article. It's
marked visually, so you can't miss it if you look closely," points to the
site's crypto-casinos guide; hint 5, "Find it inside the review of our #1 rated
CS2 gambling site for 2026," points to the Gamdom review; hint 8, "Just read N1
Casino review. The word is already there," points to the N1 review; hint 9,
"The quickest path still needs a second thought. Find the article on the site.
The word is there," points to a withdrawal-speed article. In each of the four
target articles, exactly one word is wrapped in an italic tag that is not part
of any icon, and that word is a valid BIP39 word. The other 8 hints are
one-line riddles with no comparable marker: for example, hint 1 reads
"Presence without permanence," hint 4 reads "Born twice, seen once," and hint
12 reads "A single mark on a map, or the act of finding it." Hint 2 describes a
domain ruled by a crown; hint 7 is a half-finished, self-referential line about
the hunt itself, cut off before it names anything. All 12 hints, captured
verbatim, are in [data/hints.csv](data/hints.csv).

## What is understood

### Mechanism

The page's own labeling fixes the order: hint N is seed word N, so word order is
not a separate unknown. Positions 3, 5, 8, and 9 are fixed by the italic-tag
device above: `unveil`, `deposit`, `grid`, `remind`. The other 8 positions (1, 2,
4, 6, 7, 10, 11, 12) are open. A full 12-word candidate is checked by BIP39
checksum, then derived under BIP84 with an empty passphrase; BIP49 and BIP44 are
checked as a fallback since the page never states the path.

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "w1 w2 ... w12"
```

### Certified against

No solved puzzle exists on this site to calibrate against, so
`tools/oracle.py --selftest` certifies the derivation path against the public
BIP39/BIP84 test vector: the mnemonic "abandon" repeated 11 times plus "about"
derives to `bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu` under
`m/84'/0'/0'/0/0`. Reproduced 2026-08-16.

### Established facts

1. The escrow is funded and unspent as of 2026-08-16 (checked via
   [mempool.space](https://mempool.space)); 2 funding transactions of 40,000
   sats each, none spent.
2. 4 of 12 words are fixed with high confidence: each of the 4 target articles
   contains exactly one non-icon italic word, and all 4 are valid BIP39 words.
3. Across 3 saved candidate pools and 3 derivation paths, about 2 million
   position-combinations were checked with the 4 known words fixed, yielding
   about 125,000 checksum-valid full mnemonics, none matching the address.

## What has been tested

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| The 8 riddle words are all inside plausible synonym pools | about 2,000,000 position-combinations across 3 pools and 3 derivation paths | BIP39 checksum filter, then BIP84/BIP49/BIP44 derivation and exact address match | about 125,000 checksum-valid mnemonics, 0 match | uncertified: no known-good candidate was planted in the pool to prove the sweep would have caught it | 2026-08-04 |

## Open leads, ranked

1. **Wait for or request the site's own canonical answer** (needs a person or
   external information). The vault page released all 12 hints at once and
   remains the only place a confirmation could come from at no cost. Once about
   7 of the 8 riddle words are confidently pinned, checksum plus the 4 known
   words reduce the rest to a sub-second exact-match check.
2. **Re-check the other 8 articles for the same italic-tag device** (minutes).
   The marker is confirmed on 4 of 12 target articles; whether it extends to
   any of the remaining riddle-linked pages has not been checked.

## Files in this folder

| Path | What it is |
|---|---|
| `data/hints.csv` | the 12 published hints, verbatim, with the 4 resolved words and their source articles |
| `tools/oracle.py` | BIP39 to BIP84/BIP49/BIP44 candidate checker, certified against the public BIP39 test vector |

## Sources

- Bitcoin Vault puzzle page: https://luckylurker.com/bitcoin-vault/
- Crypto casinos guide (hint 3 target): https://luckylurker.com/crypto-casinos-guide/
- Gamdom review (hint 5 target): https://luckylurker.com/casino/gamdom/
- N1 Casino review (hint 8 target): https://luckylurker.com/casino/n1/
- Fastest crypto casino withdrawals article (hint 9 target): https://luckylurker.com/fastest-crypto-casino-withdrawals-2026/
