# Q's donated BIP38 paper wallet (0.005297 BTC, [WATCH])

The person posting as q explicitly offers the remaining funds to anyone who recovers the forgotten BIP38 passphrase. Funding is verified, but the supplied memories do not establish a practical search.

## At a glance

| | |
|---|---|
| Author | [q](https://stacker.news/q) |
| Published | 2023-10-06; Dated public invitation on Stacker News. |
| Prize | 0.005297 BTC; about $334 at the 2026-08-16 price snapshot |
| Chain | bitcoin |
| Escrow | `1J7BVeP8JK4op2X3GN3Hy7xkTnGnQTMpou` ([explorer](https://mempool.space/address/1J7BVeP8JK4op2X3GN3Hy7xkTnGnQTMpou)) |
| Last on-chain check | 2026-10-01; partially-spent; exact retrieval time in [funding evidence](data/evidence-2026-10-01.json) |
| Status | WATCH |
| Puzzle type | bip38 |
| Target format | BIP38 encrypted private-key record published by q; recover the passphrase and match the named Bitcoin address. |
| Certified oracle | no; not established |
| What remains | uneconomic: The author recalls a likely sub-30-character passphrase and possibly combined passwords, but no small candidate space or feasible search cost is established. Ownership is the author's public claim. |
| Series | none |

## The puzzle as published

On 2023-10-06 q posted a forgotten-passphrase paper wallet, its encrypted BIP38 record and its public address, with an explicit invitation to recover it and keep the coins. I rely on that voluntary public donation statement, not on a generic list of lost wallets. The post and author's replies mention a likely length below 30 characters and possible combinations of three older passwords; those memories are uncertain.

529700 sats is the verified remainder, not the lifetime receipts. Historical spends do not by themselves prove the donated challenge has been solved.

## What is understood

The wallet has previous spends, and the author says it was used before the passphrase was forgotten. The balance is therefore partially-spent rather than lifetime-unspent. Recovering a BIP38 passphrase and reproducing the public address is the target; I have not decoded the record, certified a derivation or tested candidates. No recovered key material is reproduced here.

4865700 sats received, 4336000 sats historically spent, 529700 sats remain; 3 transactions, no pending activity. I requested the linked public source with cache reuse disabled.
The retrieval timestamp records when that response was available for review; explorer lag
or upstream caching cannot be excluded. Funding evidence is not a guarantee that a puzzle
remains solvable, or that a particular person owns the funds.

## What has been tested

I checked the public sources and funding summary only. No candidate, private key or seed
was tested, no search was run, and no new oracle certification is claimed. The zero counts
in the manifest record that scope; they are not a negative result about any candidate space.

## Open leads, ranked

1. Review only the hints intentionally published with the donation. A smaller public constraint would be needed before a measured, bounded search could be assessed. No personal-information search or leaked-password collection is supported by this entry.

## Files in this folder

| Path | What it is |
|---|---|
| [puzzle.json](puzzle.json) | Manifest, author attribution, balance scope and source links |
| [data/evidence-2026-10-01.json](data/evidence-2026-10-01.json) | Timestamped public balance observation |

Original puzzle materials remain on their authors' sites. No solution or recovered private
material is included.

## Sources

- [Author material, read 2026-10-01; publication timing explained above](https://stacker.news/items/275973) (2023-10-06).
- [Public funding evidence, read 2026-10-01](https://mempool.space/api/address/1J7BVeP8JK4op2X3GN3Hy7xkTnGnQTMpou) (2026-10-01).
