# ONFO / Dr. J.R. Forsyth Bitcoin Treasure Hunt (1 BTC, [DEAD END])

Dr. John Forsyth, a Missouri physician and co-founder of the ONFO project, announced in June
2021 that he had hidden a Bitcoin private key "in plain sight" somewhere across a planned series
of 10 educational videos, and funded a wallet with 1 BTC as the prize. Only 5 of the 10 videos
were ever published, the last one in March 2022, and Forsyth, who said he was the only person
who knew where the key was hidden, died in 2023. The escrow remains intact and unspent. I did
not attempt any derivation: half the material needed to reconstruct the key was never released,
and the one person who could release it is no longer alive to do so.

## At a glance

| | |
|---|---|
| Author | Dr. John Forsyth, [Onfo LLC](https://www.youtube.com/channel/UCzphFzDxPwGFJ4jofoN30qg) (persona "Dr. J.R. Forsyth") |
| Published | 2021-06-25, press release ([Benzinga](https://www.benzinga.com/pressreleases/21/06/a21717862/onfo-announces-bitcoin-treasure-hunt)) |
| Prize | 1 BTC (about $63,000 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `157dpLJgAAKugukKz8UwBHapM4idyZvnLc` ([explorer](https://mempool.space/address/157dpLJgAAKugukKz8UwBHapM4idyZvnLc)) |
| Last on-chain check | 2026-08-16: funded and unspent, 1 BTC, single UTXO since the original 2021-06-04 deposit |
| Status | DEAD END |
| Puzzle type | raw-private-key, video-series |
| Target format | a Bitcoin private key, format not specified (WIF or hex), matching the escrow address |
| Certified oracle | no: no decoding method was ever specified, and the source material is incomplete |
| What remains | the missing video segments or the author's key material would need to surface |
| Series | none |

## Why this is a dead end

The announced mechanism requires all 10 video segments; only 5 were ever published, with a
6.5-month gap between segments 4 and 5 and nothing released after 2022-03-29. Forsyth stated
publicly, more than once, that he was "the only person on the planet" who knew where the key was
hidden. He died in 2023, and I have found no report, family statement, or on-chain event
indicating that his key material or the missing segments were ever released afterward. I
verified the escrow on-chain on 2026-08-16: still funded and unspent, unchanged from my previous
check. This would reopen if segments 6 to 10 surface, or if the author's key material is
released by someone with a legitimate claim to it. The lesson: an intact, well-funded escrow is
not by itself evidence that a puzzle is solvable; check whether the announced material was ever
completed before spending any effort on it.

## The puzzle as published

The 2021-06-25 press release, distributed through paid wire services and picked up by several
outlets, states the rule directly: "The private key is hidden somewhere in the videos, all 10
videos must be seen in order to find the private key." Forsyth repeated the same claim, nearly
word for word, in the description of each of the first four published segments. Only Segment
2's description restates the wallet address in clear text. No segment description, and no other
public statement I found, specifies a decoding method, cipher, or steganographic technique
beyond "in plain sight." Verbatim quotes with dates and links are in
[clues/author-posts.md](clues/author-posts.md).

## What is understood

### Mechanism

No mechanism has been established. The author's only description of the encoding is "in plain
sight" across unspecified visual or audio content of the videos; no oracle can be built against
an unknown encoding over an incomplete corpus.

### Derivation and oracle

No certified oracle in this folder: there is no decoding method to implement, and the video
corpus needed to test one is structurally incomplete. A solver can verify any candidate the same
way I would: check whether it is a valid Bitcoin private key (WIF or hex) whose address matches
`157dpLJgAAKugukKz8UwBHapM4idyZvnLc`, or simply watch whether the escrow balance changes at
[mempool.space](https://mempool.space/address/157dpLJgAAKugukKz8UwBHapM4idyZvnLc).

### Established facts

1. Only 5 of the 10 announced video segments exist on the channel, published 2021-06-22 through
   2022-03-29, with a 6.5-month gap between segments 4 and 5.
2. Segment 5's description no longer mentions the hunt, the 10-segment count, or the key, a
   break from the pattern in segments 1 through 4.
3. Comments are disabled on all 5 puzzle segments; no rule, hint, or solver write-up appears
   anywhere in the channel's public comments.
4. The escrow address has received exactly one deposit, 1 BTC on 2021-06-04, and has never been
   spent from, confirmed again on 2026-08-16.
5. Forsyth died in 2023, after stating publicly that he alone knew the key's location.

## What has been tested

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| A second Bitcoin address appears anywhere in the 19 channel videos' descriptions or subtitles | full text of all descriptions and available subtitles | text search | 0 addresses besides the target | uncertified | 2026-08-03 |
| The official site (onfocoin.com) or its Wayback captures name a decoding method | live site and archived captures | manual read plus text search of archived JavaScript | 0 hits; the domain is now an expired parking page | uncertified | 2026-08-03 |

I did not attempt any candidate derivation. With half the source material unpublished, a
negative would not be meaningful, so none is claimed here.

## Open leads, ranked

None while the reason above holds. This would reopen if the missing video segments (6 through
10) surface, or if the author's key material is released by someone with a legitimate claim to
it.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | verbatim quotes from the press release and video descriptions, with dates and links |

## Sources

- ONFO Announces Bitcoin Treasure Hunt (press release), Benzinga, 2021-06-25: https://www.benzinga.com/pressreleases/21/06/a21717862/onfo-announces-bitcoin-treasure-hunt
- SEGMENT 1 - Intro to Crypto, YouTube, 2021-06-22: https://www.youtube.com/watch?v=YMl3-AfBBvs
- SEGMENT 2 - Modern Slavery, YouTube, 2021-07-09: https://www.youtube.com/watch?v=40l9ukS7Nmg
- Segment 5 - Leveling the Playing Field (last segment published), YouTube, 2022-03-29: https://www.youtube.com/watch?v=LMbvquFBhoE
- Missing "Bitcoin Millionaire" and ONFO coin co-creator found dead: Report, Cointelegraph, 2023-06-01: https://cointelegraph.com/news/bitcoin-millionaire-onfo-coin-creator-dead
