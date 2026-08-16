# Commander U Riddle for 8.5 BTC (8.50099081 BTC nominal, [DEAD END])

An anonymous GitHub Pages site by "Commander U," last edited in May 2019, offers 6 riddle
fragments that concatenate into a 51-character Bitcoin private key for an address that genuinely
holds 8.50099081 BTC. The nominal prize is real money sitting at a real, unspent address. I am
listing it as a dead end anyway: the address's public key was already exposed on-chain before
the puzzle was published, it appears associated with resold "wallets for sale," the author has
been unresponsive since 2019, and the fragments that remain unsolved do not match any standard
transform of any base58 string, an internal inconsistency a genuine puzzle would not have. I did
not attempt to assemble a candidate key or broadcast anything.

## At a glance

| | |
|---|---|
| Author | Commander U, [GitHub Pages site](https://commanderu.github.io/index.html) |
| Published | 2019-05-15 (earliest captured version; site unchanged since 2019-05-20) |
| Prize | 8.50099081 BTC nominal (about $535,562 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `1KDUcZh5Z6H1of4Pwoy5ojJtkQxcQBHhnH` ([explorer](https://mempool.space/address/1KDUcZh5Z6H1of4Pwoy5ojJtkQxcQBHhnH)) |
| Last on-chain check | 2026-08-16: 8.50099081 BTC total, fully unspent (see note on indexing below) |
| Status | DEAD END |
| Puzzle type | raw-private-key, text-cipher |
| Target format | 51-character uncompressed mainnet WIF, 6 base58 fragments (9+8+9+9+8+8 characters) |
| Certified oracle | no: no canonical checker script exists for this puzzle, and 4 of 6 fragments are unrecovered |
| What remains | the original 2019 channel with the sub-riddle answers, which I could not find |
| Series | none |

## Why this is a dead end

The nominal 8.5 BTC sits in a 2010-era P2PK output whose public key is already exposed on-chain,
which means anyone, not necessarily the private key's owner, can build a puzzle site pointing at
it. The GitHub repository's own issue tracker records two unanswered questions asking whether
the puzzle is still legitimate, and one commenter there notes the address has been used in
various wallet resale listings. A 2026 Bitcointalk repost of the puzzle drew a public challenge
to its legitimacy from another forum member. On top of that, my own exhaustive check of the 3
unsolved MD5-only fragments (see "What has been tested") found that none of them is the MD5 of
any base58 string under any of 28 standard transforms, while the 2 already-solved fragments are
both clean, direct MD5 matches. A real puzzle with one consistent scheme would not have 2 clean
fragments and 3 that never assemble. I verified the escrow on-chain on 2026-08-16: still
unspent, unchanged. This would reopen if a genuine 2019 "Commander U" channel with the original
sub-riddle statements surfaces, or if the author responds to the open GitHub issues. The lesson:
an intact, large balance at a P2PK address is not by itself evidence of a legitimate puzzle,
since a P2PK public key is public by construction.

## The puzzle as published

The site states, verbatim: "Hints (6 parts: 3-9, 3-8 Sigma 51): 3*9,3*8 =Sigma= privkey", six
fragments of length 9, 9, 9, 8, 8, 8 summing to 51 characters, the length of an uncompressed
mainnet WIF. Six QR codes on the page encode the six fragments. Fragment 1 decodes in clear from
a base64 string; fragment 4 was cracked by another community member and verified against its
published MD5 hash; fragment 2 is a text riddle with no published checksum; fragment 3 is
AES-encrypted with an unknown passphrase; fragments 5 and 6 are MD5 hashes with no further clue.
Full text in [clues/author-posts.md](clues/author-posts.md).

## What is understood

### Mechanism

The 6 fragments, once all recovered, concatenate in order into a 51-character uncompressed
mainnet WIF starting with "5." Decoding that WIF gives a private key whose uncompressed public
key must equal `041ebfac69910efb17ab697db5f2a4ff815e1d37c05e40d56977031a3a36b80464ea6782ad2913e2a5ec33e187f0fee50675bc78a25d657846e08e8425f2384b2a`
exactly, the same key already exposed by the 2010 P2PK output.

### Derivation and oracle

No certified oracle in this folder. Only 2 of 6 fragments are known, so there is no complete
candidate to check yet, and no canonical single-command checker exists in my working notes for
this puzzle. A solver can verify any completed candidate the same way I would: decode the
51-character string as a WIF, compute its uncompressed public key, and compare it byte for byte
to the public key above, or watch whether the escrow balance changes at
[mempool.space](https://mempool.space/address/1KDUcZh5Z6H1of4Pwoy5ojJtkQxcQBHhnH).

### Established facts

1. Fragment 1 decodes in clear: base64 `MS41SlJkNDJuVTE=` gives `5JRd42nU1`.
2. Fragment 4, `AhiF1tpuG`, matches its published MD5 hash exactly; it was found by a community
   member on Bitcointalk, not by me.
3. Fragments 3, 5 and 6 do not match the MD5 of any base58 string of length 7 to 9 under any of
   28 standard transforms (uppercase, lowercase, prefixed, suffixed, MD5 squared or cubed,
   MD5 of SHA1, MD4, NTLM, and others).
4. The 6 QR codes encode exactly the visible query-string data on the page; decoding them with
   no assumptions finds no hidden channel.

## What has been tested

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Fragment 3 AES passphrase, dictionary and contextual word lists | about 1.12 million candidates | AES decrypt attempt, check for valid plaintext | 0 match | uncertified | 2026-07-26 |
| Fragment 3 AES passphrase, full printable ASCII, length 5 or less | 7.4e9 candidates | AES decrypt attempt, sharded across 24 cores | 0 match | uncertified | 2026-07-26 |
| Fragments 3, 5, 6 as MD5 of base58 strings, length 7 | 58^7 candidates, 28 transforms | GPU exhaustive search | 0 match | yes: witness fragment 4 recovered each run | 2026-07-26 |
| Fragments 3, 5, 6 as MD5 of base58 strings, length 8 | 58^8 candidates, 28 transforms | GPU exhaustive search | 0 match | yes: witness fragment 4 recovered each run | 2026-07-26 |
| Fragments 3, 5, 6 as MD5 of base58 strings, length 9 | 58^9 candidates (about 7.43e15), 28 transforms | GPU exhaustive search on rented hardware | 0 match, search exhausted | yes: witness fragment 4 recovered at about 90 percent of the sweep | 2026-07-26 |

## Open leads, ranked

None while the reason above holds. This would reopen if a genuine 2019 "Commander U" channel
with the original sub-riddle statements surfaces, or if the author responds to the open GitHub
issues confirming ownership.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | the site's own hint text and fragment table, as published |

## Sources

- Commander U, puzzle site, 2026-07-26: https://commanderu.github.io/index.html
- Commander U repository issues, 2026-07-26: https://github.com/commanderu/commanderu.github.io/issues
- Bitcointalk repost, thread 5573629, 2026-02: https://bitcointalk.org/index.php?topic=5573629.0
- Funding transaction (2010 P2PK output), mempool.space, 2010-09-22: https://mempool.space/tx/80d8bc9856938d3dce012dfa2b2f93d6724bc046e10f4d0dde824ce3392eb774
