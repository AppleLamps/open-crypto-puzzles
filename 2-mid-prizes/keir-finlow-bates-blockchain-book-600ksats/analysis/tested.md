# Tested (full negatives ledger)

The summary table in `README.md` shows the highlights; this file is the complete record
for the 3 open lots (EN_medium, EN_veryhard, IT_veryhard). All rows use the sha256x3
oracle in `tools/oracle.py`, certified against the solved lots EN_easy_1 ("221B Baker
Street") and IT_hard ("Genova Firenze Bologna Brindisi"): the same code that failed to
match any candidate below is proven, on those two lots, to match the correct answer
exactly. I never repeat a row; a hypothesis retested with a different method gets a new
row.

| Hypothesis | Space (N) | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Brainwallet family: SHA-256 applied 1 to 3 times over the raw book text (chapters, full text) | refuted by construction | tested the same transform directly against the solved-lot addresses first | fails to reproduce EN_easy_1 or IT_hard, so the whole family is dead, not just untested on the open lots | yes: tested against known answers, not just the open lots | 2026-07-10 |
| Systematic EN ebook mechanisms: planted numbers as signposts, flaw-and-fix to a corrected noun (10 sites), acrostic and positional reading at book scale, CHEST and discography letter extraction, section-heading to text-fragment crossings (about 120 pairs), reader-instruction sites (12 locations, the same class of clue as EN_easy_1) | approximately 5,500 candidates cumulative across these 6 mechanism classes (per-class split not separately recorded) | derived each candidate string with sha256x3, both key forms, checked against all 12 addresses | 0 match on the 3 open lots | yes: oracle certified against EN_easy_1 and IT_hard | 2026-07-18 |
| Late per-site closures: the "orange juice" flaw (Hoffman's canon is tomato juice, not orange), the EN Monopoly squares (Park Lane, Park Place, Mayfair, Boardwalk), the L606 pronoun slip | 33 candidates | same sha256x3 oracle | 0 match | yes: same certified oracle | 2026-07-18 |
| Discography reading order as a decoded site index (later refuted: the author's live Spotify playlist matches the printed order verbatim, so this was never a real signal); re-mined anyway on chapter 19 and "About the Author" | 111 candidates | same sha256x3 oracle | 0 match | yes: same certified oracle | 2026-07-14 |
| Erdos-number collaboration chain (Keir Finlow-Bates to Paul Erdos through 5 intermediate co-authors, printed only in the Italian edition's body text) | 30 candidate forms | same sha256x3 oracle | 0 match | yes: same certified oracle | 2026-07-14 |
| Pair-discipline sweep: crossing signposts (a planted detail plus a cultural reference, the same grammar that produced EN_easy_1) tested as pairs across 4 designated sites (an elephant parable, a Figure 7 caption, the Erdos back matter, a Figure 12 caption) | 146 candidate pairings | same sha256x3 oracle | 0 match | yes: same certified oracle | 2026-07-14 |

Cumulative across the 6 rows above: approximately 5,820 candidates tested against the 3
open lots, 0 matches.

## What this rules out and what it does not

Every mechanism I could construct from the EN and IT ebook text and figures is closed.
Four plants remain identified but unmapped to any natural-language answer: the Figure 8
DeLorean VIN that reads 26 in the prose and 27 in the figure, the number 74,638 printed
near a block explanation, an unattributed E. E. Cummings line in the preface ("the
deepest secret nobody knows"), and a chess note ("Bishop to a6"). Each was tried against
its obvious noun candidates as part of the 2026-07-18 row above; none matched. This does
not rule out a print-only answer for any of the 3 open lots: the physical 2020 to 2021
print runs have not been checked, since I have not yet compared a physical copy against
the ebook captures page by page.
