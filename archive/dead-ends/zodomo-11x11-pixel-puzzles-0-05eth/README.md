# Zodomo 11x11 Pixel Puzzles (0.05 ETH nominal, [DEAD END])

Generative artist Zodomo minted a series of 11x11-pixel artworks on networked.art for
Ethereum's 11th anniversary, encoding a BIP39 seed phrase in the pixels of 4 of them and
funding each with 0.05 ETH. I reconstructed two of the four encoding schemes from scratch and
confirmed both against their escrow addresses exactly. Three of the four puzzles have already
been claimed, two by a third party and one reclaimed by the artist himself. The fourth, the one
still described as active, has no funded escrow address anywhere I can find on Ethereum
mainnet, so there is currently nothing to claim even for a solver who cracks its encoding.

## At a glance

| | |
|---|---|
| Author | Zodomo, [networked.art/11x11](https://networked.art/11x11) |
| Published | 2026-07-30, first 3 puzzle pieces minted |
| Prize | 0.05 ETH nominal per piece (about $94 at ETH = $1,880, 2026-08-16); the active piece has no known funded address |
| Chain | ethereum |
| Escrow | 3 addresses for the solved/claimed pieces below; no address known yet for the active piece |
| Last on-chain check | 2026-08-16: all 3 known escrows spent; no funded address found for the active puzzle |
| Status | DEAD END |
| Puzzle type | bip39-seed, pixel-code |
| Target format | BIP39 12 or 24 words, English, 11x11 pixel grid, 11-color base-11 palette, BIP44 `m/44'/60'/0'/0/0` |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against piece #993) |
| What remains | a funded escrow for the active piece, and its encoding scheme |
| Series | none |

## Why this is a dead end

Zodomo funded 4 puzzle escrows with 0.05 ETH each on 2026-07-30. Three are accounted for:
pieces #869 and #930 were swept by a third party the same evening, and piece #993 was reclaimed
by Zodomo himself half an hour later. The fourth puzzle, which the artist's own 2026-08-01 post
describes as "still active," has never received a matching 0.05 ETH transfer on Ethereum
mainnet, on Base, or in any ERC-20 token from any of Zodomo's known wallets, as of my check
today. This is not a swept or emptied escrow; it is a puzzle whose prize, as far as public
on-chain evidence shows, was never placed on-chain in the first place, or is held off-chain by
the author. I verified this again on 2026-08-16: unchanged from my previous check. This would
reopen the moment a matching escrow appears on-chain. The lesson: for a puzzle series with
per-piece escrows, check the specific piece's own address, not just the artist's general
activity or an announcement's stated amount.

## The puzzle as published

The entirety of what Zodomo has said publicly about the puzzle is 5 posts on X between
2026-07-30 and 2026-08-01, with no attached media or links: "I will post 1 more puzzle... this
one is meant for AI too," followed by "both puzzle images are for the same seed," and finally
"4 seed phrases... Three were claimed. One is still active!" Verbatim quotes with dates are in
[clues/author-posts.md](clues/author-posts.md). The active puzzle is represented by two pieces,
#34886 and #35198, both declared by the artist to encode the same seed.

## What is understood

### Mechanism

Each piece is an 11x11 grid; its palette of 11 colors maps to base-11 digits. Two full schemes
are reconstructed and certified by exact address match: piece #869 reads the grid in
boustrophedon order, discards its 4 corner pixels as padding, and repeats a 39-digit block
(132 bits, 12 BIP39 words) three times over the remaining 117 cells; piece #993 splits the grid
by color range into a data region and a padding region, then reads the data region the same way
for a 264-bit, 24-word result. Both derive at BIP44 `m/44'/60'/0'/0/0`. Piece #930, swept by the
same third party, uses neither scheme; its encoding remains unknown, and so does the active
puzzle's.

### Derivation and oracle

```
python3 tools/oracle.py --selftest                    # reproduces the known #993 mnemonic
python3 tools/oracle.py "candidate mnemonic"           # MATCH / NO MATCH against the 3 known escrows
python3 tools/oracle.py --stdin                        # one candidate per line
```

A candidate mnemonic is validated against the BIP39 checksum, then its Ethereum address at 3
standard derivation paths is compared to the known escrow addresses. It cannot, by itself,
confirm a candidate for the active puzzle, since no funded address exists yet to compare against.

### Certified against

`tools/oracle.py --selftest` reproduces the reconstructed mnemonic for piece #993, which derives
`0xf5d45c9d798aedb754b1ed8660af3ea79178b765` exactly. This piece's escrow has already been
reclaimed by the artist, so publishing the mnemonic here creates no front-running risk.
Reproduced 2026-08-16.

### Established facts

1. All 4 known 0.05 ETH transfers from `zodomo.eth` occurred on 2026-07-30:

   | Piece | Address | Funded at | State |
   |---|---|---|---|
   | #869 | [`0x60a5431a138b0320641408694562f624f3c977a8`](https://etherscan.io/address/0x60a5431a138b0320641408694562f624f3c977a8) | 18:58:59 | spent (third party) |
   | #930 | [`0x9cc846fe9b75a4cee897f605b240dd0030fcd5a2`](https://etherscan.io/address/0x9cc846fe9b75a4cee897f605b240dd0030fcd5a2) | 18:59:23 | spent (third party) |
   | #993 | [`0xf5d45c9d798aedb754b1ed8660af3ea79178b765`](https://etherscan.io/address/0xf5d45c9d798aedb754b1ed8660af3ea79178b765) | 18:59:47 | spent (reclaimed by Zodomo) |
   | paid by hand | [`0xa15585918e6ef74239246f4e1538acdf70b4743e`](https://etherscan.io/address/0xa15585918e6ef74239246f4e1538acdf70b4743e) | 22:02:23 | active wallet, unrelated NFTs |

2. `0xa15585918e6ef74239246f4e1538acdf70b4743e` (`queengarden.eth`), the recipient of the fourth
   transfer, holds 17 unrelated NFTs and had 168 transactions since 2023 at the time it was
   checked; this is a real, pre-existing personal wallet, not a fresh puzzle escrow, and it was
   paid by hand rather than solved.
3. Pieces #34886 and #35198 (the active puzzle) were minted a day later, 2026-07-31, and their
   on-chain mint calldata contains only the 121 raw pixel bytes, no hidden message.

## What has been tested

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| The #869 boustrophedon triple-repetition scheme, applied to #930 and to the active pieces | full transform space (8 rotations times 8 traversal orders times padding options) | pattern statistics against the known #869 structure | fails to reproduce the pattern | yes: #869 itself is the positive control | 2026-08-01 |
| The #993 color-partition scheme, applied to #930 | all row and column splits | structural check | no block has 8 or fewer distinct colors, scheme does not apply | yes: #993 itself is the positive control | 2026-08-01 |
| General windowed sweep on #930 (rotations, traversal orders, lengths, bit order) | 48,256 windows | BIP39 checksum plus address compare | 0 match | uncertified | 2026-08-01 |
| Intersection of candidates from both active-puzzle images (declared to share one seed) | 14,997 times 15,043 candidates | BIP39 checksum, intersect the two sets | 0 candidates in common | uncertified | 2026-08-01 |
| Global on-chain balance sweep of generated candidates | about 10,600 addresses | balance and nonce check | 0 funded | not applicable, no funded escrow exists to find | 2026-08-01 |

## Open leads, ranked

None while the reason above holds. This would reopen if a funded escrow address for the active
puzzle (pieces #34886 and #35198) appears on Ethereum mainnet.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | the artist's 5 public posts about the puzzle, verbatim, with dates |
| `tools/oracle.py` | candidate checker: BIP39 checksum plus Ethereum address match against the 3 known escrows, self-tested |

## Sources

- Zodomo, piece collection: https://networked.art/11x11
- Zodomo, X post announcing the active puzzle, 2026-08-01: https://x.com/Zodomo/status/2083364549697155550
- Zodomo, X post naming the intended difficulty, 2026-07-30: https://x.com/Zodomo/status/2082949091244327366
