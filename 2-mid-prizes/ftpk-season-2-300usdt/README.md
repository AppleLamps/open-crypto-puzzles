# FTPK Season 2: Never-Ending (305.930218 USDT, [OPEN])

FTPKgame (@FTPKgame on X) launched the second season of this puzzle series on
2025-05-19: 12 mini-games, each worth one English BIP39 word, that together derive the
private key for an Ethereum wallet holding USDT. I mapped the entire site, certified the
derivation against the author's own worked example, and broke the page-naming scheme,
which turned out to hide a 13th page holding a 12th game. None of the 12 words is
confirmed via the on-chain oracle yet. Two players the author named left page
transcriptions of games 1, 4, 6, 7, 9, and 11; the live pages themselves sit behind
Vercel Attack Challenge Mode as of 2026-08-27.

## At a glance

| | |
|---|---|
| Author | FTPKgame, [@FTPKgame on X](https://x.com/FTPKgame) |
| Published | 2025-05-19, X ([announcement](https://x.com/FTPKgame/status/1924450289311961483)) |
| Prize | 305.930218 USDT (about $306, stablecoin, 2026-08-16) |
| Chain | ethereum |
| Escrow | `0xb5fe4f1b6cb2bbe6a327f8c68f370da7df18b2dc` ([explorer](https://etherscan.io/address/0xb5fe4f1b6cb2bbe6a327f8c68f370da7df18b2dc)) |
| Last on-chain check | 2026-08-27: USDT balance 305.930218, native ETH 0, 0 outgoing transactions ever |
| Status | OPEN |
| Puzzle type | bip39-seed, word-selection |
| Target format | 12 English BIP39 words, BIP44 `m/44'/60'/0'/0/0`, no passphrase |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the author's own Game 11 worked example) |
| What remains | apply the player page transcriptions and the 2025 X clues once a residential browser can read the twelve games; 0 words confirmed via the oracle so far |
| Series | FTPK (this folder covers Season 2 only) |

## The puzzle as published

The site (`findtheprivatekeys2.vercel.app`, reached through a hub at
`findtheprivatekeys.vercel.app`) lists 12 numbered games, a word-order helper page, and a
manual, paid answer checker the site itself does not require, since the escrow address is
a free and exact offline oracle. Each game page is named `sha256(word).html`, where
`word` is that game's own answer; reading the 11 known page names in order spells "the
last game has for url this sentence that is hashed", which names the URL of a 12th,
otherwise unlisted game. The word-order helper states that once all 12 words are known,
visiting a page named by their literal concatenation (no spaces) confirms the correct
order. On a page the author built for Season 4 to cross-reference Season 2, found by
breaking the same naming scheme, the author wrote: "game number 7 is the weakest game,
it's really too vague and poorly designed. If you had to bruteforce one or a few words,
this one is a good candidate."

## What is understood

### Mechanism

Twelve independent mini-games (ciphers, image puzzles, an audio track) each resolve to
one BIP39 word. The 12 words, in the correct order, form a standard mnemonic; its BIP44
Ethereum address at `m/44'/60'/0'/0/0` must equal the escrow exactly. The page-naming
scheme is not itself an oracle on the seed words: it is a meta-puzzle whose only function
is to reveal the hidden 12th game.

### Derivation and oracle

```
python3 tools/oracle.py --selftest                              # author's own example
python3 tools/oracle.py "twelve english words in a guessed order"
python3 tools/oracle.py --stdin                                  # one candidate per line
```

`MATCH <address>` on a hit, `NO MATCH` otherwise; a candidate with an invalid BIP39
checksum is reported as a checksum failure rather than derived. A second, free,
zero-computation oracle exists on the live site itself: the page named by the 12 words
concatenated without spaces confirms both the word set and the order at once.

### Certified against

`tools/oracle.py --selftest` reproduces the author's own published worked example (a
teaching page for Game 11): mnemonic `claim cycle staff clump domain judge boy session
razor tiny shoulder coconut` derives to `0x50D7e097e61121140c19871F06eA6FeB6d14105b`,
reproduced exactly.

### Established facts

1. The escrow holds 305.930218 USDT and 0 native ETH, with 0 outgoing transactions ever,
   checked via `eth_call` to the USDT contract and `eth_getTransactionCount` on
   2026-08-27.
2. The BIP44 derivation is certified against the author's own published example.
3. The page-naming scheme, `sha256(word)`, is broken: the 11 known preimages spell a
   sentence that names the URL of a 12th, hidden game page, confirmed live (HTTP 200).
4. A second, free, offline-equivalent oracle exists: probing the page named by the 12
   words concatenated without spaces confirms both the words and their order.
5. Game 1's 2 hidden decoy channels (a steganographic image layer and an invisible link
   to an unrelated image) both decode, once the game's own cipher is solved, to a message
   from the author explicitly naming themselves as decoys.
6. No public code repository for the author or this puzzle series exists.
7. On 2025-06-06 the author named @N4Khjir and @thedragon8383 as having left comments
   worth reading. N4's 2025-05-28 to 2025-06-06 replies transcribe live titles and body
   text for games 1, 4, 6, 7, 9, and 11, plus three extra hosted paths. Those strings
   are in [analysis/leads.md](analysis/leads.md). None of them is a 12-word MATCH.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Page-naming scheme as a direct oracle on BIP39 words (2048 words, 7 case/format variants, 5 hash functions, plus a large dictionary) | tens of thousands of hash checks | recompute page names, compare to the 11 known ones | refuted as a word oracle | yes: a full dictionary correctly reproduces all 11 known page names | 2026-07-26 |
| Game 1 candidate matching the decoy Cold War barrier image | 1 candidate | certified oracle | refuted: the puzzle's own decoded text names the image a decoy | uncertified | 2026-07-26 |
| Game 12 audio steganalysis (3-channel spectrogram) | full file | spectrogram analysis | refuted: no hidden image, genuine music | yes | 2026-07-26 |
| Game 10 sub-poem acrostics | 2 sub-pages | read first letters of each line | refuted: no word spelled | uncertified | 2026-07-26 |
| Image LSB steganalysis on Game 1's second decoy image | 30 layout variants | LSB extraction | refuted: nothing found | uncertified | 2026-07-26 |
| Public code repository search for the author | n/a | GitHub search API | refuted: does not exist | yes | 2026-07-26 |
| Solid-red X clue image as a hidden-payload carrier | 1 file, 250848 pixels | unique-colour count and EXIF/XMP | uniform #FF0000, no yellow, no metadata | uncertified | 2026-08-27 |
| Extra 50-letter page names as the 12-word concatenation oracle | 2 strings, 50 letters | DP word-break vs English BIP39 | 0 reconstructions | yes: teaching mnemonic concat re-found as 12 words | 2026-08-27 |
| Game 9 title/body as a single BIP39 index | 2 numbers | range check against 0..2047 / 1..2048 | both out of range | yes: bounds of the published list | 2026-08-27 |
| Game 9 title as A1Z26 of the whole digit string | 8 partitions | A1Z26 then BIP39 membership | 0 list words | yes: 12,1,19,20 reproduces the Game 2 page-name preimage | 2026-08-27 |

## Open leads, ranked

1. **Read the 12 game pages from a residential browser that passes Vercel's Attack
   Challenge Mode** (hours). The author enabled that mode on 2025-06-05 after page-name
   probing ran up the request bill; as of 2026-08-27 both a datacenter fetch and a
   headed browser on this host get a checkpoint (the browser failed with Code 11),
   while the hub and Season 1 still load. Confirmed by a full transcription of every
   game; killed only by an on-chain sweep.
2. **Apply the harvested 2025 X clues and the player page transcriptions** (hours).
   Catalogued in [analysis/leads.md](analysis/leads.md): Game 7 titled "Zero-based
   indexing" (the Season 4 page's weakest game), Game 11 titled `+33` with a Braille
   heading and a five-line French poem whose first letters are a city name, Game 9 as
   the digit strings `1211920` / `3114`, Game 6 as "Simplicity Must Be Rewarded I" on
   an extra letter-named page (those 50-letter names are not the 12-word
   concatenation oracle), ten hidden cities and "4 cities 1 word", French useful
   twice, Game 12 as a Drive file plus "F12" plus Photopea for the Game 1 `.psd`.
   The Season 4 hidden page remains the author's own S2 hint map once a browser can
   reach it. Confirmed by a 12-word MATCH on the certified oracle; killed only by
   exhausting every game's candidate readings.
3. **Transcribe the Game 12 audio track as notes to digits** (hours), the same method a
   Season 1 page from this author uses for a similar audio puzzle, rather than treating
   it as a song to identify. A player who had found the game called the track "the
   Jungle" and had not yet read the sound. Confirmed by a digit sequence that reads as
   a valid BIP39 word or index; killed by exhausting the plausible note-to-digit
   mappings.

## Files in this folder

| Path | What it is |
|---|---|
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | ranked leads, the 2025-05-19 to 2025-06-15 X clue harvest, and the player page transcriptions |
| `tools/oracle.py` | candidate checker: 12-word mnemonic to Ethereum address, certified against the author's own example |

## Sources

- "Here we go for a new game, 300 USDT to win", X, 2025-05-19: https://x.com/FTPKgame/status/1924450289311961483
- FTPK hub page: https://findtheprivatekeys.vercel.app/
- Season 2 puzzle site: https://findtheprivatekeys2.vercel.app/
- Season 4 hidden page cross-referencing Season 2 clues, including the game 7 admission: https://findtheprivatekeys4.vercel.app/servicecricketgloomattendsupremejumpannualeagerpulpprojectdiseaseround.html
- Author, Attack Challenge Mode and the request-bill posts, X, 2025-06-05: https://x.com/FTPKgame/status/1930610344247906356
- Author, "last clue from me" (black knight), X, 2025-06-15: https://x.com/FTPKgame/status/1934183762079666297
- Author, naming @N4Khjir and @thedragon8383, X, 2025-06-06: https://x.com/FTPKgame/status/1931006963740979489
- N4Khjir, Game 7 title "Zero-based indexing", X, 2025-05-28: https://x.com/N4Khjir/status/1927621189503005053
- N4Khjir, Game 11 Braille / +33 / French poem, X, 2025-05-28: https://x.com/N4Khjir/status/1927623047076282678
- Author, image2.jpg is a development error, X, 2025-06-06: https://x.com/FTPKgame/status/1931024956046909798
- Escrow wallet, etherscan.io: https://etherscan.io/address/0xb5fe4f1b6cb2bbe6a327f8c68f370da7df18b2dc
