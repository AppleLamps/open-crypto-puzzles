# FTPK Season 4: Something in Common (166.000000 USDC, [OPEN])

FTPKgame (@FTPKgame on X), the same author behind the Season 2 puzzle in this repository,
launched a fourth season on 2026-07-16: 12 independent mini-games, each worth one English
BIP39 word, unlocking an Ethereum wallet holding USDC. The author funded the escrow before
announcing it and has topped it up more than once since, most recently confirmed by a
tweet about an extra dollar added after someone used the paid checker. I mirrored the
full site, certified the BIP44 derivation, and established one word with confidence and a
second as a strong candidate. The author's own hint says most of the 12 games share one
common mechanic; the leading reading is that each produces a number usable as a BIP39
wordlist index.

## At a glance

| | |
|---|---|
| Author | FTPKgame, [@FTPKgame on X](https://x.com/FTPKgame) |
| Published | 2026-07-16, X ([announcement](https://x.com/FTPKgame/status/2077755138668671313)) |
| Prize | 166.000000 USDC (about $166, stablecoin, 2026-08-16) |
| Chain | ethereum |
| Escrow | `0xa468335485cE853F21A44451755bd88364e9d618` ([explorer](https://etherscan.io/address/0xa468335485cE853F21A44451755bd88364e9d618)) |
| Last on-chain check | 2026-08-16: USDC balance 166.000000, native ETH 0.00053941261264344 (gas preload for the winner), 0 outgoing transactions ever |
| Status | OPEN |
| Puzzle type | bip39-seed, word-selection |
| Target format | 12 English BIP39 words, BIP44 `m/44'/60'/0'/0/0`, no passphrase |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the public BIP39/BIP44 test mnemonic; no author-published worked example exists for this season) |
| What remains | solve enough of the 12 mini-games and identify their common mechanic; 1 word established, 1 more a strong candidate |
| Series | FTPK (this folder covers Season 4 only) |

## The puzzle as published

The site (`findtheprivatekeys4.vercel.app`) lists 12 games described by the author as
"pretty much all independent": a hangman-style word, a grid of dice, a subtraction
problem in colored dots, letter grids, a darts scoreboard, poker hands, tic-tac-toe
boards, an alphabet spiral, a repeated phrase, a list of characters from a game, and a
board game. Each page is named `md5(N).html` for a decimal integer `N`, all 12 pages
using N of 2200 or less. On 2026-07-23 the author confirmed,
["all the words are necessarily part of the BIP-39 list"](https://x.com/FTPKgame/status/2080258068529492034),
and on 2026-07-25 gave the season's one hint:
["There is something that almost all the games have in common. Sometimes it won't really
help you, but at other times, you will absolutely need to keep that common element in
mind."](https://x.com/FTPKgame/status/2080976765401387082)
On 2026-07-22 the author said,
["In Season 4, there is a hidden page to help you with Season 2. This page is hidden in a
way that's a bit similar to Game 12 from Season 2."](https://x.com/FTPKgame/status/2079947035357102350)
That page is the same `md5()` naming scheme applied to the 12 Season 4 answer words
concatenated in game order.

## What is understood

### Mechanism

Twelve independent mini-games each resolve to one BIP39 word. The 12 words, in the
correct order, form a standard mnemonic; its BIP44 Ethereum address at
`m/44'/60'/0'/0/0` must equal the escrow exactly. The word order is a minor convenience
rather than a real lock: only 1 in 16 of the 12-factorial orderings of any given 12-word
set passes the BIP39 checksum, about 30 million candidates, searchable offline in about
30 minutes on 16 cores once the word set itself is known. The author confirmed as much
directly, describing the order-helper page as providing "the exact word order so you can
withdraw funds from the wallet" rather than being a puzzle in its own right.

### Derivation and oracle

```
python3 tools/oracle.py --selftest                              # public BIP39/BIP44 vector
python3 tools/oracle.py "twelve english words in a guessed order"
python3 tools/oracle.py --stdin                                  # one candidate per line
```

`MATCH <address>` on a hit, `NO MATCH` otherwise; a candidate with an invalid BIP39
checksum is reported as a checksum failure rather than derived.

### Certified against

`tools/oracle.py --selftest` reproduces the standard public BIP39 test mnemonic, 12
repetitions of "abandon" followed by "about", deriving to
`0x9858EfFD232B4033E47d90003D41EC34EcaEda94` under `m/44'/60'/0'/0/0`. No worked example
specific to this season has been published by the author, unlike Season 2's Game 11.

### Established facts

1. The escrow holds 166.000000 USDC and a 0.00053941261264344 ETH gas preload, with 0
   outgoing transactions ever, checked via `eth_call` to the USDC contract and
   `eth_getTransactionCount` on 2026-08-16.
2. The prize has grown since the season launched: recorded at 153.000000 USDC in earlier
   research and at 166.000000 USDC on 2026-08-16, with the author confirming on X that a
   solver's use of the paid word checker added an extra dollar to the pool.
3. The author confirmed all 12 words are drawn from the standard BIP39 English wordlist.
4. The page-naming scheme, `md5(N).html` for a decimal integer `N`, is confirmed for all
   12 games (every N is 2200 or less) but is not itself a mapping from N to the answer
   word.
5. Game 1, a hangman puzzle with the pattern `??o?` and corner tags reading "1st" and
   "dance", establishes the word `frog` with confidence through the hangman mechanics
   themselves, not through the page-naming integer.
6. Game 10, a repeated phrase reading "again and again", is a strong candidate for the
   word `repeat`, pending confirmation alongside the other 11 words.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Page-naming integer N as a direct BIP39 wordlist index | 1 candidate per game, checked against game 1's pattern | compare index N to the BIP39 word at that position | refuted: neither word at index 1570 fits game 1's hangman pattern | uncertified | 2026-07-26 |
| 13th hidden page search (N up to 2200, thematic words, N up to 36,000) | approximately 34,000 URLs | HTTP probe, 200/404 signature | refuted: no extra page beyond the Season 2 hint page | uncertified | 2026-07-26 |
| Letter grids (games 4, 6, 9) as plain word searches | full BIP39 wordlist and a 75,145-word English dictionary, all 8 directions, length 4 or more | grid search | refuted as a classic word search: 2 incidental matches in game 4, 0 in games 6 and 9 | uncertified | 2026-07-26 |
| Hidden links in the page markup | full site mirror | grep for anchors and `data-*` attributes | refuted: none found | yes | 2026-07-26 |

## Open leads, ranked

1. **Identify the common mechanic across the 12 games** (hours). The leading reading,
   from the author's own hint and the games built around dice, darts, and a board game,
   is that each game yields a number usable as a 1-to-2048 index into the BIP39 wordlist.
   Confirmed by a reading that correctly derives 2 or more of the already-established
   words from their games' own numbers; killed by a full 12-word attempt that fails under
   every indexing convention tried.
2. **Solve the remaining games directly** (hours), since the word order is not a real
   lock once the set of 12 words is known. Confirmed by a full 12-word candidate matching
   the escrow; killed only by exhausting every game's plausible readings.

## Files in this folder

| Path | What it is |
|---|---|
| `analysis/tested.md` | the complete negatives ledger |
| `tools/oracle.py` | candidate checker: 12-word mnemonic to Ethereum address, certified against a public BIP39/BIP44 test vector |

## Sources

- "A new treasure hunt is live! (Something in common), 12 hidden words, 150 USDC to be won", X, 2026-07-16: https://x.com/FTPKgame/status/2077755138668671313
- "Yes, all the words are necessarily part of the BIP-39 list", X, 2026-07-23: https://x.com/FTPKgame/status/2080258068529492034
- "There is something that almost all the games have in common", X, 2026-07-25: https://x.com/FTPKgame/status/2080976765401387082
- "In Season 4, there is a hidden page to help you with Season 2", X, 2026-07-22: https://x.com/FTPKgame/status/2079947035357102350
- FTPK hub page: https://findtheprivatekeys.vercel.app/
- Season 4 puzzle site: https://findtheprivatekeys4.vercel.app/
- Escrow wallet, etherscan.io: https://etherscan.io/address/0xa468335485cE853F21A44451755bd88364e9d618
