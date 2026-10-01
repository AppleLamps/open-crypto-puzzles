# Bitcoin Puzzle Transaction family (verified lot 71) (7.1019168 BTC, [WATCH])

A single family of intentionally reduced private-key ranges. The 2017 account claimed creation and explained the difficulty masking; identity has not been cryptographically verified.

## At a glance

| | |
|---|---|
| Author | [Unknown creator; saatoshi_rising claims authorship](https://bitcointalk.org/index.php?action=profile;u=991321) |
| Published | 2017-04-27; Date of the creator-claim post, not the 2015 funding date or the first public discussion. |
| Prize | 7.1019168 BTC; about $447,421 at the 2026-08-16 price snapshot |
| Chain | bitcoin |
| Escrow | `1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU` ([explorer](https://mempool.space/address/1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU)) |
| Last on-chain check | 2026-10-01; funded-unspent; exact retrieval time in [funding evidence](data/evidence-2026-10-01.json) |
| Status | WATCH |
| Puzzle type | raw-private-key |
| Target format | Lot 71: scalar in [2^70, 2^71), compressed secp256k1 public key, Bitcoin P2PKH address. |
| Certified oracle | no; not established |
| What remains | bounded-compute: Finite 2^70-scalar range for the verified lot; no measured rate, affordable search or solve is established here. Other funded lots are not included in the amount. |
| Series | Bitcoin Puzzle Transaction |

## The puzzle as published

The funding transaction dates to January 2015. A public forum post on 2017-04-27 by saatoshi_rising claims creation, explains the intentionally reduced key sizes and describes a community cracking benchmark. I use that dated public explanation as the publication reference; it is not the first funding date. The author claim is unsigned identity evidence, not proof of ownership.

Only the current balance of lot 71 is counted. Initial lot allocations and later top-ups are different from this balance; no live whole-family aggregate is asserted.

## What is understood

For lot N the advertised private-key interval is [2^(N-1), 2^N). Lot 71 is therefore a finite range of 2^70 scalars. Deriving a compressed Bitcoin P2PKH address is the target mechanism. I have not certified a local oracle or established a feasible search rate. This is one numerical family; solved members and unsolved members are not independent discoveries.

Lot 71 only: 710191680 sats received over 69 transactions, 0 spent, no pending activity. I requested the linked public source with cache reuse disabled.
The retrieval timestamp records when that response was available for review; explorer lag
or upstream caching cannot be excluded. Funding evidence is not a guarantee that a puzzle
remains solvable, or that a particular person owns the funds.

## What has been tested

I checked the public sources and funding summary only. No candidate, private key or seed
was tested, no search was run, and no new oracle certification is claimed. The zero counts
in the manifest record that scope; they are not a negative result about any candidate space.

## Open leads, ranked

1. Track exact lot-level balances and verified payout transactions. A drained lot alone does not identify a solver; preserve the distinction between an individual lot and the whole series.

## Files in this folder

| Path | What it is |
|---|---|
| [puzzle.json](puzzle.json) | Manifest, author attribution, balance scope and source links |
| [data/evidence-2026-10-01.json](data/evidence-2026-10-01.json) | Timestamped public balance observation |

Original puzzle materials remain on their authors' sites. No solution or recovered private
material is included.

## Sources

- [Author material, read 2026-10-01; publication timing explained above](https://bitcointalk.org/index.php?topic=1306983.msg18765941#msg18765941) (2017-04-27).
- [Public funding evidence, read 2026-10-01](https://mempool.space/api/address/1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU) (2026-10-01).
- [Original January 2015 funding transaction (event evidence, not invitation date)](https://mempool.space/tx/08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15) (2015-01-15).
