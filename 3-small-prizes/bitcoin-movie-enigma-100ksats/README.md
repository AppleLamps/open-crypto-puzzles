# Bitcoin Movie Enigma (100,000 sats, [OPEN])

"klems" published this puzzle across Nostr, X, and Instagram in January 2024: 34
numbered panels, each a still from a different movie, that together encode a
24-word BIP39 seed phrase for a wallet funded with 100,000 sats. The rules, still
published on the author's own site, describe a two-step transform: turn each of the
34 movie titles into an English BIP39 word, then drop 10 "intruder" words using
information found on each film's IMDb page, leaving the real 24-word seed in panel
order. The derivation is fully understood and bounded once the inputs are known.
What is missing is entirely cultural: I have identified 32 of the 34 films with
confidence, 1 remains unidentified, and 1 has two different candidate
identifications from separate research passes that I have not reconciled, and I
have not yet found either the title-to-word rule or the IMDb field that splits the
24 keepers from the 10 intruders.

## At a glance

| | |
|---|---|
| Author | klems, [Nostr npub10q5dpm5p05a0g3vtgcl76wv0pc4t820f5fj8qmpfaa4umv6404xqvwzvp0](https://njump.me/npub10q5dpm5p05a0g3vtgcl76wv0pc4t820f5fj8qmpfaa4umv6404xqvwzvp0) |
| Published | 2024-01-03, Nostr, X and Instagram ([rules](https://bitcoinmovieenigma.com/rules)) |
| Prize | 100,000 sats (about $63 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6` ([explorer](https://mempool.space/address/bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6)) |
| Last on-chain check | 2026-08-16: funded and unspent (100,000 sats) |
| Status | OPEN |
| Puzzle type | bip39-seed, text-cipher, word-selection |
| Target format | BIP39 24 words (English), most likely BIP84 `m/84'/0'/0'/0/i` (script type `v0_p2wpkh`), no passphrase stated |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the public BIP39/BIP84 test vectors) |
| What remains | identifying 2 of the 34 films, then the title-to-word rule and the IMDb intruder field |
| Series | none |

## The puzzle as published

The rules page, still live at [bitcoinmovieenigma.com/rules](https://bitcoinmovieenigma.com/rules),
states the mechanism directly:

> "Guess all the 34 movie titles, from the provided movie frames."

> "Transform 'somehow' each movie title into an English BIP-0039 seed word."

> "The seedphrase you have is 34 words long, but we should have a 24 words
> seedphrase instead. Some movies should not be in the sequence, and should be
> considered intruders, but which ones? You will need additional informations
> about each movie to detect those intruders 'somehow'. Every information you need
> can be found on IMBD, on each movie's page."

> "Once you got rid of the intruders, you can restore the Bitcoin wallet using the
> 24 words passphrase with any compatible software."

The 34 panels were posted one per day (by their displayed date, 2024-01-03 through
2024-02-05) on the author's Nostr account and cross-posted to X and Instagram,
later mirrored to a dedicated site because, in the author's own words on the site's
about page, "some platforms compressed the movie frames poorly." Each panel is a
still from a different film; I do not reproduce them here, since they are
third-party film frames and the site hosting them is still live (see
[clues/author-posts.md](clues/author-posts.md) for direct links and further
quotes). A separate "alternative release" republishes the same 34 stills as a
single combined image; I confirmed byte for byte that all 34 match the individual
panels exactly, so it carries no extra information.

The escrow's wallet page names the address directly and lists the author's own
funding entry, "100000 | 4/08/2022," in a donation ledger, which matches the
escrow's on-chain funding date and resolves what would otherwise look like an
unexplained 21-month gap between funding and the January 2024 launch: the wallet
was pre-funded as a donation well before the puzzle was announced.

## What is understood

### Mechanism

Each of the 34 panels is one movie still, in a fixed panel order. Identifying the
34 titles and transforming each into an English BIP39 word gives a 34-word
sequence. Ten of those 34 words are "intruders" to be identified and dropped using
information on each film's IMDb page, leaving the real 24-word mnemonic in panel
order. The escrow's script type, `v0_p2wpkh`, points to BIP84 as the most likely
derivation, though the author never states the path directly, so the oracle also
checks BIP49, BIP44, and 3 raw derivation paths some simple wallets use.

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "w1 w2 ... w24"
```

The oracle validates a 24-word candidate as a BIP39 mnemonic, derives every
plausible address (BIP84, BIP49 and BIP44 across 2 accounts and 3 indices each,
plus 3 raw paths), and compares each to the escrow address. `MATCH <address> via
<path>` on a hit, `NO MATCH` otherwise. To check which 10 of 34 known words to
drop, generate the 24-word reductions yourself and pipe them through `--stdin`;
the puzzle's own arithmetic bounds this to C(34,10) = 131,128,140 raw combinations,
cut by the BIP39 checksum (1 in 256) to about 512,000 candidates, which costs on
the order of an hour end to end with this pure-Python, bip_utils-only oracle. That
bound only applies once all 34 words and their order are known, which is not yet
the case here.

### Certified against

No solved sibling exists for this puzzle, so `tools/oracle.py --selftest` certifies
the derivation path against the public BIP39/BIP84 test vectors: the 12-word
mnemonic "abandon" repeated 11 times plus "about" derives address
`bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu`, and the 24-word mnemonic "abandon"
repeated 23 times plus "art" is confirmed to be checksum-valid and to derive a
non-empty address; a 1-word-off variant is correctly rejected by the checksum.
Reproduced 2026-08-16.

### Established facts

1. The escrow is funded and unspent as of 2026-08-16 (checked via
   [mempool.space](https://mempool.space)); the single funding transaction
   confirmed 2022-04-08 at block 730990.
2. The escrow's own wallet page names the address and lists the author's funding
   entry with the same date, resolving the apparent gap between funding and launch.
3. Both published image sets (individual panels and the "alternative release") are
   byte-for-byte identical, 34 of 34, confirmed by MD5.
4. 32 of the 34 films are identified with confidence (24 confirmed, 7 probable, 1
   uncertain); panel 11 is unidentified; panel 34 has 2 competing identifications
   from different research passes that have not been reconciled
   (`data/films.csv`).
5. Of the 33 titles identified with any confidence, 29 contain at least one English
   BIP39 word as a literal substring of the title; 4 do not (The Goonies, Barry
   Lyndon, Sharknado, Raiders of the Lost Ark).
6. About 25 to 30 candidate IMDb-field criteria for the 10 intruders have been
   tried; none produces an exact 24-versus-10 split (`analysis/tested.md`).

![34 panel slots colored by identification confidence: confirmed, probable or uncertain or disputed, and unidentified](images/02-panel-grid-identification.svg)
*Figure 1. Identification status of the 34 panels, no film stills reproduced (source: data/films.csv, script tools/fig_panel_grid.py), 2026-08-16.*

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Both image sets carry different information | 34 panels compared | byte-for-byte MD5 comparison | identical, 34/34 | yes: direct comparison, independently reproducible | 2026-08-03 |
| Intruders = MPAA rated R | recount as films are identified | direct count over the film corpus | looked correct at 10/18, refuted at 16-18/34 | n/a: direct count, re-checkable from data/films.csv | 2026-08-04 |
| Intruders = won at least 1 Oscar | recount as films are identified | direct count | looked correct at 10/21, refuted at 11/34 | n/a: direct count | 2026-08-04 |
| Intruders = adapted from a novel | recount as films are identified | direct count | looked correct at 10/31, refuted at 12/34 | n/a: direct count | 2026-08-04 |
| About 25 further IMDb-field criteria | recount as films are identified | direct count | none reaches an exact 24/10 split | n/a: direct count | 2026-08-04 |

## Open leads, ranked

1. **Identify panel 11** (needs a person). The still shows "Bumble Bee" branded
   boxes buried in sand; a Nutrition Facts label dates the scene to after about
   1994. No film has been matched yet.
2. **Reconcile panel 34's identity** (needs a person, likely under an hour). Two
   research passes reached different conclusions, "Dead Ringers" (probable) and
   "The Human Centipede (First Sequence)" (2009, reached at higher confidence in a
   later, independent pass). I have not run both methods side by side to settle
   this, so I present it here as open rather than picking one.
3. **Find the title-to-word rule for the 4 titles with no literal BIP39 word**
   (needs new information). The Goonies, Barry Lyndon, Sharknado, and Raiders of
   the Lost Ark contain no BIP39 word as a literal substring; either the rule is
   not purely literal, or these 4 are themselves intruders.
4. **Find the IMDb field that splits 24 keepers from 10 intruders** (needs new
   information). About 25 to 30 criteria tried, all refuted; I am not testing new
   criteria until panels 11 and 34 are both settled, since a 10-of-34 split found
   against an incomplete film set has low statistical value on its own.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | verbatim quotes from the rules, about and wallet pages, with links; no film stills reproduced |
| `data/films.csv` | my identification state for all 34 panels: title, MPAA rating, confidence, candidate BIP39 words |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the 4 ranked leads |
| `images/02-panel-grid-identification.svg` | the 34-panel identification status grid |
| `tools/oracle.py` | candidate checker, certified against the public BIP39/BIP84 test vectors |
| `tools/fig_panel_grid.py` | generates images/02-panel-grid-identification.svg from data/films.csv |

## Sources

- Bitcoin Movie Enigma, rules page: https://bitcoinmovieenigma.com/rules
- Bitcoin Movie Enigma, about page: https://bitcoinmovieenigma.com/about
- Bitcoin Movie Enigma, wallet page: https://bitcoinmovieenigma.com/wallet
