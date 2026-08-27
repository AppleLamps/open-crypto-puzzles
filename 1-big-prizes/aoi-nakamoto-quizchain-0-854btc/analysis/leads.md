# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Exact combination and transform of the four Finney-pattern groups

The "Second" chapter contains three planted paragraph-initial blocks that match
the Finney-post pattern (one sign paragraph plus four non-sign paragraphs whose
first letters are F, F, W, W), plus a direct quotation from the Finney post that
also matches the pattern. These are located at the start of each main section
(Section I, Section II, Section III/Finney quote).

The 2019-08-01 author post confirms the solution text has multiple paragraphs
and is separated by two CRLF sequences (ASCII 13 10 13 10, "hit enter twice").
A comprehensive search over permutations, subsets, whole vs non-sign-only,
first-only vs first+last case-flip, quote stripping, title prefixes, and
LF/CR/CRLF/double-CRLF separators produced no match (17,921 candidates,
`analysis/tested.md`, 2026-08-27). The remaining uncertainty is therefore not
the separator, but the exact group-combination and transform the author applied
before hashing.

What would confirm it: a defined selection rule (which groups, in which order,
which paragraphs per group, which flip mode, which quote/whitespace
normalization) that reproduces the escrow address through `tools/oracle.py`.
What would kill it: an exhaustive, witness-backed sweep of all plausible
combinations of these four groups with no match.
Cost: seconds per candidate; bounded by the number of plausibly distinct
selection/flip/serialization variants.

## 2. Reconstruct any remaining 2019 page-level copy behavior

The author typed the chapter with blank lines between paragraphs. The current
Wattpad API storage normalizes these away, and the current Chrome reader page
produces LF-separated innerText/selection strings. The 2019 reader page may have
included the title, author byline, section headings, or CSS-generated
characters (non-breaking spaces, quote marks) that are not in the API storage.
Current captures (API JSON, `innerText`, `selection.toString`, `textContent`) are
saved under `/tmp` but do not include a faithful 2019 render.

What would confirm it: a 2019-era Wattpad reader page or snapshot, or a
precise reconstruction of its paragraph text, applied to the same group/flip
rule and run through `tools/oracle.py`.
What would kill it: a faithful reconstruction of the four groups with the
known separator still not matching after all plausible page-level prefixes and
whitespace normalizations are exhausted.
Cost: hours if a 2019 render must be recovered; seconds per candidate once the
text is known.

## 3. Two-character edits on the strongest base texts

The single-character-edit sweep (266,038,400 candidates, `analysis/tested.md`)
covers every one-character difference from 40 base texts and is exhaustive for
that distance. It does not cover 2-character differences, which would catch a
base text that is off by, for example, one inserted invisible character AND one
capitalization slip. A 2-character sweep restricted to the small set of NBSP and
line-ending pairs (rather than all positions) is a bounded space, not a full
40-base x 2-character search.

What would confirm it: a match within the bounded 2-character space.
What would kill it: exhausting that bounded space with 0 match; the full,
unbounded 2-character space is not proposed here, since its cost is
disproportionate without a narrower reason to expect the answer lives there.
Cost: on the order of an hour on a rented GPU for the bounded version described
above; the private research folder priced this at roughly 45 minutes per base
text for a similarly scoped variant.

## 4. Identify what "76" indexes for Block 76

A method confirmed on 3 other blocks in the same series (56, 57, 58) uses the
block's own number as a position index into a specific corpus (a numbered post
by Satoshi Nakamoto or Hal Finney on bitcointalk, read in a specific order). The
same method, tried against every corpus and ordering available (Satoshi's and
Hal Finney's bitcointalk posts, Hal Finney's tweets), does not produce a post
containing "change" or "from" at position 76. The corpus this method should
index for block 76 has not been identified; candidates not yet tried include the
complete list of Hal Finney's tweets (only 58 were recovered through the
official API; a fuller archive may exist), Satoshi's SourceForge posts, the
Bitcoin whitepaper or v0.1 source code read as a sequence of numbered units, and
the author's own r/Grycoin posts read as their own numbered sequence.

What would confirm it: a position-76 item in the right corpus containing "change
to" or "from change to", tested through `tools/oracle.py --block76-filter` and
then a full derivation.
What would kill it: exhausting the remaining candidate corpora with no match at
position 76.
Cost: minutes per corpus once a candidate corpus is assembled.

## 5. A short, human-reasoned answer to "change to" / "from change to"

The author's own hint structure (a short, freeform-text question plus a short
TOMI expansion, confirmed on more than a dozen other blocks) argues for a short,
punchy answer rather than a long dictionary phrase. The scripted sweep in
`analysis/tested.md` covers dictionary and corpus vocabulary exhaustively within
its stated bounds, but a human-reasoned short answer with unusual capitalization
or punctuation (the author's own confirmed style on other blocks, for example
"NGD" for "net zero" or "JD6" for "QWERTY") is a different kind of hypothesis
than a word-list sweep can reach.

What would confirm it: any short candidate, tested through
`tools/oracle.py --block76-filter` first (a near-instant filter) and then
through a full derivation.
What would kill it, in the useful sense: nothing kills this lead outright; it
stays open as a standing invitation, same as any human-reasoned wordplay block
in the series.
Cost: minutes per candidate; no sweep implied.

## Resolved leads

### Author posts between the rehash and shutdown (was lead 2)

The Real Big Block Discussion thread contains 16 AoiNakamoto posts, not 27,
between 2019-07-25 and 2019-08-01. The relevant constraints extracted:

- 2019-07-25: extra line breaks were added between paragraphs.
- 2019-07-31: the rehashed solution has multiple paragraphs and two line breaks
  between each of them.
- 2019-08-01: "I mean the second one. Hit enter twice. This displays in Ascii as
  13 10 13 10, according to asciivalue.com."

This fixes the paragraph separator as CRLF+CRLF (13 10 13 10). No further
paragraph-selection constraints were found in the thread, so this lead is
resolved and its information is folded into lead 1 and lead 2 above.

## Stage One reproduction: the MD5 and two reimplementation gotchas (issue #1)

stakeados (issue #1) wrote down the exact Stage One value, which this folder reproduced during
research but never recorded as a number:

- source: bitcointalk topic 155054, first post, raw HTML (ISO-8859-1, ASCII body)
- md5: `9dd2efb9bc976c2095bd534d7b8d431c`
- derives to `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` at `m/44'/0'/0'/0/0`

Both reimplementation gotchas they flag are already handled in `tools/oracle.py`, but neither
was stated in prose: a paragraph break is `<br><br>`, so a single `<br>` (as in the
"[edited slightly]" line) does not start a new paragraph; and the byte encoding is ISO-8859-1,
not UTF-8. Recording the MD5 makes the Stage One reproduction checkable without re-deriving
from the post.
