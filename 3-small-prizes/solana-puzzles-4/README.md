# Solana Puzzles #4 (0.834 SOL, [OPEN])

An image and twelve hints are intended to yield a 12-word seed phrase. The active page advertises 0.8 SOL; the named wallet currently holds 0.834 SOL.

## At a glance

| | |
|---|---|
| Author | [SolanaPuzzles](https://solanapuzzles.com/) |
| Published | Exact public date unknown; Funding and the page timer suggest approximately September 2025, but an exact public launch date is not verified. |
| Prize | 0.834 SOL; about $63 at the 2026-08-16 price snapshot |
| Chain | solana |
| Escrow | `DmDBmb7AEm6xRxkoBYq1mJYqsZP263gmXB53zA2dqjne` ([explorer](https://solscan.io/account/DmDBmb7AEm6xRxkoBYq1mJYqsZP263gmXB53zA2dqjne)) |
| Last on-chain check | 2026-10-01; funded-unspent; exact retrieval time in [funding evidence](data/evidence-2026-10-01.json) |
| Status | OPEN |
| Puzzle type | bip39-seed, image-stego, word-selection |
| Target format | 12-word seed phrase inferred from an image; the site names Phantom, but the exact derivation path and optional passphrase are not established. |
| Certified oracle | no; not established |
| What remains | insight: The public page is marked ACTIVE and supplies twelve hints. Address derivation is unverified; no candidate seeds or certified negatives are claimed. |
| Series | Solana Puzzles |

## The puzzle as published

The puzzle page is marked ACTIVE, gives twelve hints and names Phantom as the intended wallet. Its displayed prize is 0.8 SOL. I link the author's image and hints rather than copy them. The homepage has a deliberate decoy route before linking the actual numbered page; the page and exact escrow address are the identity used here.

The page advertises 0.8 SOL. The observed wallet contains 0.834 SOL. USD estimate uses the verified 2026-08-16 historical SOL quote of $75.27983398665542, rounded to the nearest dollar.

## What is understood

The fresh explorer page displays 0.834 SOL and two incoming transfers. An independent earlier finalized RPC observation on 2026-10-01 at slot 452162643 reported 834000000 lamports. The timer and first funding suggest approximately September 2025, but neither establishes an exact public launch date. Phantom's name alone does not certify a derivation path or optional passphrase.

834000000 lamports (0.834 SOL); explorer displays 2 incoming transfers of 0.417 SOL and no outgoing transfer. I requested the linked public source with cache reuse disabled.
The retrieval timestamp records when that response was available for review; explorer lag
or upstream caching cannot be excluded. Funding evidence is not a guarantee that a puzzle
remains solvable, or that a particular person owns the funds.

## What has been tested

I checked the public sources and funding summary only. No candidate, private key or seed
was tested, no search was run, and no new oracle certification is claimed. The zero counts
in the manifest record that scope; they are not a negative result about any candidate space.

## Open leads, ranked

1. Establish the exact address-derivation convention from public author material before interpreting any seed search. A self-test matching a known author example would be needed before a negative could count as certified.

## Files in this folder

| Path | What it is |
|---|---|
| [puzzle.json](puzzle.json) | Manifest, author attribution, balance scope and source links |
| [data/evidence-2026-10-01.json](data/evidence-2026-10-01.json) | Timestamped public balance observation and historical price evidence |

Original puzzle materials remain on their authors' sites. No solution or recovered private
material is included.

## Sources

- [Author material, read 2026-10-01; publication timing explained above](https://solanapuzzles.com/puzzle4.html) (2026-10-01).
- [Public funding evidence, read 2026-10-01](https://solscan.io/account/DmDBmb7AEm6xRxkoBYq1mJYqsZP263gmXB53zA2dqjne) (2026-10-01).
- [Historical SOL/USD quote for 2026-08-16, read 2026-10-01](https://api.coingecko.com/api/v3/coins/solana/history?date=16-08-2026) (2026-10-01).
