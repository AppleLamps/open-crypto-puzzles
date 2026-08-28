# Tested: Bitaps Shamir secret-sharing challenge

Full negatives ledger. The README shows the summary table.

## 1. Wrong code base (rounds 1 and 2, superseded)

I first analyzed `pybtc`, a Python reimplementation of the same scheme, and found a
time-based coefficient bias in its `(a * i) % 255` construction, computing a residual of
119, 98, then 82 bits under 3 successive refinements. This turned out to be the wrong
target: `pybtc`'s Shamir index space is `x` in 1 to 5, and the real published share 2 has
index `x = 15`, which `pybtc` cannot produce. `pybtc` also only gained the embedded-index
feature it would need on 2020-07-11, three weeks after the challenge address was funded.
I dropped this line of analysis once the index mismatch was confirmed; it is kept in the
project history as a recorded wrong turn, not as a result.

## 2. Establishing the real code base

`bitaps-com/mnemonic-offline-tool`, commit `5b6dd995` (2020-06-19, the funding date),
bundles `jsbtc`, not `pybtc`. 3 checks confirm this: the trailing 4 bits of each share are
a data field (an index), not a checksum, since both published shares fail the BIP39
checksum in a way consistent with an embedded index rather than corruption; the observed
index values (3 and 15) fall inside `jsbtc`'s 4-bit index range (1 to 15) and outside
`pybtc`'s 3-bit range (1 to 5) as it existed on the funding date; and re-deriving from
both candidate implementations against the 2 published shares, only the `jsbtc` reading
produces internally consistent output. Method: source comparison plus the index-range
argument above. Witness: the public BIP84 test vector reproduces via `tools/oracle.py
--selftest`. Result: `jsbtc` established as the code of record. Date: 2026-08-03.

## 3. Residual entropy of the secret

See `data/entropy_measurements.csv` for the 3 measurements and their method. Summary: the
theoretical 128 bits narrows to 127.73 bits under the duplicate-value coefficient
rejection rule common to both `jsbtc` and `pybtc`, and to about 125 bits (124.90 to
125.19 across 3 independent measurements) once I added the effect of a real defect in the
deployed 2020 generator: its randomness self-check calls an undefined function
(`igam`, called from `igamc`), which throws and is silently caught, discarding a
disproportionate share of otherwise-valid random draws. None of this is small enough to
search; the point of measuring it is to state the true entropy accurately rather than by
assumption. Witness: the multiplication and interpolation tables underneath the
measurement were checked against an independent reference (65,536 GF(256) products, 0
discrepancies; 32,553 Lagrange evaluations, 0 discrepancies). Date: 2026-08-03.

## 4. Third-share search in the archives

14 archived captures of the challenge page and its regional mirrors (`bitaps.com`, plus
`ltc`, `tltc`, `tbtc`, `btc` subdomains), spanning 2020-07-04 to 2024-02-25 (Wayback CDX
and Common Crawl), all show the same 2 shares. Method: fetch every capture, extract any
12-word phrase, compare against the 2 known shares. Witness: the detector recovers both
known-good shares from every capture it reads, so an empty result is not a detector
failure. Result: 0 additional shares found across 14 captures. The interval between
2020-06-19 (funding) and 2020-07-04 (earliest capture), 15 days, is not covered by either
archive. Date: 2026-08-03.

## 5. Coefficient PRNG check

`bip39_mnemonic.js` in the bundled `jsbtc` uses `crypto.getRandomValues` or Node's
`randomBytes` for share coefficients, with no `Math.random` fallback path in the code I
read. Method: source review of the exact bundled file. Result: no exploitable seed bias
found in the coefficient generator itself (the bias found in section 1 was specific to
`pybtc`, the wrong code base). Date: 2026-08-03.

## 6. Degenerate coefficient case

The scheme's second coefficient can, with probability 1/255 per byte, be zero, which
would drop the polynomial's effective degree. This is not identifiable from only 2
shares; I enumerated the 16-byte space of this specific degenerate case and found no way
to test it without a 3rd share. Not pursued further as a standalone lead. Date:
2026-08-03.

## 7. The 15-day archive gap, rechecked

Hypothesis: a 3rd share, or a different page state, existed between funding (2020-06-19)
and the earliest Wayback/Common Crawl capture (2020-07-04) and was later removed.

Method: Wayback CDX for `bitaps.com/mnemonic/challenge` and the `www`, `ltc`, `tltc`,
`tbtc`, `btc` mirrors, window `from=20200619&to=20200704`; Common Crawl `CC-MAIN-2020-24`,
`CC-MAIN-2020-29`, `CC-MAIN-2020-34`; Arquivo.pt CDX for the same URL. Memento TimeTravel
(`timetravel.mementoweb.org`) did not resolve (DNS, 2026-08-28).

Result: 0 captures inside 2020-06-19 through 2020-07-03. The first Common Crawl hit is
`CC-MAIN-2020-29` timestamp `20200704182040`, which is the same 2020-07-04 capture already
logged in section 4. Arquivo.pt returned an empty CDX body (HTTP 200, 0 records).

Witness: the same Wayback CDX query without the gap window still returns later captures
of the known challenge URL (8 digest-collapsed rows for `bitaps.com/mnemonic/challenge`
across 2020-2024). An empty gap result is therefore not an API failure. Date: 2026-08-28.

## 8. archive.today

Hypothesis: archive.today holds a capture from the gap window, or a capture with a 3rd
share. The earlier attempt (2026-08-03) got HTTP 429 on the service's own witness page.

Method: fetched the archive.today listing for `https://bitaps.com/mnemonic/challenge`
and the one snapshot it named, `https://archive.is/8bNRM` (saved 2021-06-20 11:09:19 UTC).
Extracted every 12-word BIP39 English sequence and compared it to the 2 published shares.

Result: 1 snapshot, dated 2021-06-20, 0 additional shares. The page state is the same 2
shares plus the published zpub. Direct timemap URLs still returned HTTP 429 this session,
so this is one working read of the listing and of snapshot `8bNRM`, not a proof that the
service holds nothing else.

Witness: the extractor recovered both known-good shares from snapshot `8bNRM`. Date:
2026-08-28.

## 9. Same-day announcement copies (Reddit, Telegram, X)

Hypothesis: a 3rd share was posted on a channel other than the challenge page on or
near 2020-06-19.

Method: fetch each channel, extract every 12-word BIP39 English sequence, compare to
the 2 published shares, and pass any other 12-word sequence through `tools/oracle.py`.

- [r/Bitcoin post `hc4bfk`](https://www.reddit.com/r/Bitcoin/comments/hc4bfk/1_btc_cryptographic_challenge_with_splitted/)
  by u/bitaps, same day as funding. Body carries the 2 shares, the zpub, the escrow
  address, and the jsbtc pointer. Wayback capture
  `20230611002230` of the old.reddit thread includes all 26 comments. None of the
  comments contains a 12-word BIP39 sequence other than windows formed by joining the
  two published shares with the word "share".
- Telegram public preview [`t.me/s/bitapscom`](https://t.me/s/bitapscom), keyword
  searches for mnemonic, challenge, share, and Shamir, plus a page of older posts.
  The 2020-06-19 post is [`t.me/bitapscom/15`](https://t.me/bitapscom/15): a reprint of
  the X announcement (address and link, no share words). Later hits are the 2020-05-18
  offline-tool post and the 2021-06-09 ZeroNights bounty post. 0 extra shares.
- X status [1274018817304379394](https://x.com/bitaps_com/status/1274018817304379394),
  posted 2020-06-19T16:38:50Z: address and link, no share words. The 3 replies returned
  with the post include a 2025-05-14 request to "reveal 1 or 2 words from the third
  share"; no author reply among those 3.

Result: 1 Reddit submission + 26 comments + Telegram preview + 1 X post + 3 replies,
0 unpublished 12-word share, 0 oracle MATCH.

Witness: both known-good shares are recovered from the Reddit body. The Telegram and X
posts do not contain the share words; the witness there is recovery of the known
announcement URL, escrow address, and date. Overlap windows created by concatenating
the two published shares (13 sequences) were submitted to `tools/oracle.py --stdin`:
13 NO MATCH. Date: 2026-08-28.

## 10. GitHub forks of mnemonic-offline-tool

Hypothesis: a fork of `bitaps-com/mnemonic-offline-tool` carries a diverged 3rd share
or a modified challenge page.

Method: list forks via the GitHub API (reported `forks_count` 13), resolve each
reachable default-branch HEAD, compare to upstream commit `5b6dd995`. Also GitHub code
search for the first six words of each published share.

Result: 12 reachable heads equal `5b6dd995`. 1 reachable head
(`Stevenans985900/mnemonic-offline-tool`) equals the prior commit `91ea8b94`
(2020-05-22), which predates the challenge. Stale fork-list entries returned HTTP 404
and were not readable. Code search hits are copies of the 2 published shares (this
catalogue, and third-party notes that quote them). Pull request #8 on the upstream repo
(2026-07-20) retitles README.md with an unrelated 24-word phrase; that is not a 12-word
share and was not submitted to the 12-word oracle.

Witness: 12 forks reproduce the known-good commit hash `5b6dd995`. Date: 2026-08-28.

## 11. Live challenge pages, 2026-08-28

Hypothesis: a regional mirror still serves a 3rd share, or the live page has changed
since the 2023 Wayback copy.

Method: fetch `bitaps.com/mnemonic/challenge` (including `?language=ru`),
`tbtc.bitaps.com/mnemonic/challenge`, and `ltc.bitaps.com/mnemonic/challenge`. Extract
12-word BIP39 sequences. Derive BIP84 `m/84'/0'/0'/0/0` from the published zpub and
compare to the escrow.

Result: all 3 hosts still publish the same 2 shares. The published zpub
`zpub6qdEDkv51FpxX6g1rpFGckmiL46vV8ccmtEgPAkj3qj8N4ZZHyXDRA9RwpTiFK2Kb8vRaDmSmwgX6rfB4t2K8Ktdq8ExQ6fumKpn2ndJCqL`
derives `bc1qyjwa0tf0en4x09magpuwmt2smpsrlaxwn85lh6` at `m/84'/0'/0'/0/0`. The live
`bitaps.com` page, which returned HTTP 403 on 2026-08-16, returned the challenge body
on 2026-08-28.

Witness: both known-good shares recovered from each host; zpub-to-address is an exact
character match. Date: 2026-08-28.

## 12. Determined 2-share algebraic models

Hypothesis: extra structure on the per-byte degree-2 polynomial would make the secret
unique, or unique up to a 2-valued choice per byte, given only the 2 published shares
(indexes 3 and 15). The deployed splitter (`jsbtc` `__split_secret` / `__shamirFn` at
the 2020-05-19 merge of PR 12) draws `a1` and `a2` independently per byte, rejecting
duplicates of the secret byte. That does not by itself determine the secret. The models
below are the extra assumptions that *would* determine it, and that are small enough
to test (N/D well under two hours at about 650 derivations/s).

Method: reconstruct a 16-byte secret under each model, re-encode with a true BIP39
checksum, derive BIP84 `m/84'/0'/0'/0/0`, compare to the escrow. Constructed 3rd shares
go through `tools/oracle.py`. Code: `tools/structured_candidates.py`.

Families and counts:

- Unique models, 14 secrets: `a2=0` for every byte (the 2-point line, already in the
  oracle self-test), `a1=0` for every byte, `a1=a2`, `a1=s`, `a2=s`, secret equal to
  `y1`, `y2`, `y1 XOR y2`, SHA-256 prefixes of those, and the byte-reversals of the
  first three. 0 match.
- Same `(a1, a2)` for all 16 bytes: 65,536 pairs checked algebraically against both
  published points. 0 pairs consistent, so 0 secrets to derive.
- Global constant `a1` (256) or global constant `a2` (256), the other coefficient free
  per byte and then determined. 512 secrets, 0 match.
- Constructed 3rd-share `y` values (zeros, ones, 0xff, copy of `y1`/`y2`, XOR, SHA-256
  prefixes, the escrow hash160 prefix, and the five on-chain amount fingerprints as
  16-byte integers) at each of the 13 unused indexes. 273 candidates, 0 match.
- 2-point interpolation pretending the indexes are every pair from 1 to 15 instead of
  3 and 15. 105 pairs, 0 match.
- Per-byte 2-model mix (`a2=0` vs `a1=0`, vs `a1=a2`, vs `a1=s`; `a1=0` vs `a2=s`;
  `a2=0` vs `a2=1`; `a2=1` vs `a2=255`). 6 x 65,536 = 393,216 secrets, 0 match.
- Three BIP39 test-vector phrases from the 2020 `jsbtc` test file, as secrets and as
  3rd shares. 0 match. A 12-word phrase claimed in `pybtc` issue 53 as a 2-share
  recovery of this escrow fails the BIP39 checksum and is not a candidate.

Result: 394,125 address comparisons, 0 match, plus 65,536 algebraic pairs with 0
consistent. Rate: about 650 derivations/s. Witness: `tools/structured_candidates.py
--selftest` recovers a synthetic `a1=0` split, checks the mixed-mask enumerator at
head, bit 0 and tail, and round-trips share encode/decode; the scan uses the same
`derive_address` path as the certified oracle. Date: 2026-08-28.
