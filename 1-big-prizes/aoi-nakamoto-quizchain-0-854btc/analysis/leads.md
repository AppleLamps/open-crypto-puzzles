# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Reconstruct the 2019 Wattpad editor buffer, or a 2019 pre-wrap copy

The author states she typed the chapter with a blank line between paragraphs
and, on 2019-08-01, that "two line breaks" means hitting Enter twice, which
"displays in Ascii as 13 10 13 10" (CRLF CRLF). On 2019-07-28, before the
rehash, she said the hashed solution had only one line break, "one 13 and one
10". The chapter's current storage (fetched through Wattpad's API, `modifyDate`
2019-07-23, matching the 2019-07-30 funding of the current escrow) contains no
blank paragraphs at all: 273 `<p data-p-id>` nodes, 0 empty, 10 in-paragraph
`<br>`, 6 NBSP characters inside sentences. Wattpad's storage format
normalizes blank paragraphs away.

Live desktop CSS (fetched 2026-08-27) is:

- generic `pre { white-space: pre-wrap }`
- `.panel.panel-reading pre { white-space: inherit }` (so the reading panel
  inherits `normal` and collapses the 30-space SSR indent between `<p>` tags)
- first page is server-rendered inside `<pre>` as `id="sp720888559-pg1"` with
  36 paragraphs; pages 2 to 12 load from `apiv2/?m=storytext&id=...&page=N`

A 2026-08-27 search of 12,848 unique copy serializations built from those
facts (pages, prefixes, parts, title/byline, SSR indent, empty-paragraph NBSP
or space lines, `<br>` splits, LF/CRLF joins, Stage One flip) produced 0 match
against both listed addresses. Witness: 3 planted texts recovered at head,
middle and tail. Rate: 503/s.

What remains of this lead is a 2019 stylesheet that still applied `pre-wrap`
to the reading panel (no 2019 capture of this chapter exists), or a copy from
the write editor before save/normalize. A reader wrote on 2019-07-25 that
Wattpad did not let them copy the chapter directly, which argues the author
hashed an editor paste she then ran through asciivalue.com, not a reader
`selection.toString()`.

What would confirm it: a 2019 CSS or editor-buffer capture whose serialization,
with the certified case-flip rule, matches the current escrow.
What would kill it: that capture still not matching after the already-tested
paragraph-selection hypotheses are re-applied to it.
Cost: hours, mostly in getting a 2019 editor/CSS capture; the derivation itself
is seconds per candidate.

## 2. Two-character edits on the strongest base texts

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

## 3. Identify what "76" indexes for Block 76

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

## 4. A short, human-reasoned answer to "change to" / "from change to"

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

## Killed: the 27 posts between the rehash and the shutdown

Killed 2026-08-27. Full re-read of the author's Grycoin comments from
2019-07-30 to 2019-08-04 (arctic-shift archive of r/Grycoin, plus the Real Big
Block Discussion thread) produced no new paragraph group. It did pin down the
line-break bytes already used in the 2026-08-27 copy search: before the rehash,
one CRLF between paragraphs; after the rehash, Enter twice = `13 10 13 10`.
She also said, on Grycoin Block 2 (2019-08-03), to copy-paste and change only
capitalization. Those constraints are in `analysis/tested.md`; they did not
yield a match.

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
