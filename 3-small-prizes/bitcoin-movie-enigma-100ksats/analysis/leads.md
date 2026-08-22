# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.
The gate on this puzzle is entirely cultural (identifying films and an IMDb
field), not computational: once the 34 words and the intruder rule are both known,
checking a candidate is a single `tools/oracle.py` call, and searching every way to
drop 10 of 34 words is bounded (see the oracle's docstring for the timing).

## 1. Identify panel #11

Panel #11 remains unidentified. The still shows what appear to be "Bumble Bee"
branded boxes partly buried in sand; a Nutrition Facts label visible on the
packaging dates the scene to sometime after about 1994 (that label format was not
in use before then), which is the only anchor found so far.

What would confirm it: a film or scene search using the "Bumble Bee" branding and
the sand/beach setting, cross-checked against the post-1994 date constraint.
What would kill it: this lead has no natural end state; it stays open until a title
is identified with enough confidence to add to `data/films.csv`.
Cost: needs a person to search image and film databases; no compute cost.

## 2. Reconcile panel #34's identity

Two different identification sessions in my private research reached different
conclusions for panel #34, and I have not reconciled them. One pass concluded
"Dead Ringers" at probable confidence. A separate, later pass concluded "The Human
Centipede (First Sequence)" (2009) at a higher confidence, based on a reverse image
search on a tightly cropped region of the panel (avoiding whichever visual element
had caused the first pass's candidate to be rejected) returning a consistent
character-level tag across 2 independent crops of the same panel, plus an MPAA
certificate number matching a 2009 R-rated release. I am presenting this as an open
question rather than picking one, since the two sessions were not run against each
other side by side before this folder was written.

What would confirm either: re-running the reverse-image-search method documented in
this folder's mechanism notes on fresh crops of the panel, or any other independent
identification method, and checking whether it reproduces one candidate and not the
other.
What would kill either: a definitive identification ruling one candidate out
entirely (for instance, a visual element in the panel that cannot appear in one of
the two films).
Cost: needs a person, likely under an hour given the identification methods already
documented in this folder.

## 3. The title-to-word rule for titles with no literal BIP39 word

Four identified titles contain no English BIP39 word as a literal substring: The
Goonies, Barry Lyndon, Sharknado, and Raiders of the Lost Ark
(`analysis/tested.md`). If the rule is "the literal word in the title," these 4
titles have no answer, which means either the rule is not purely literal (a
synonym, a theme, or a different field of the title), or these 4 films are
themselves among the 10 intruders and never need a word at all.

What would confirm it: a title-to-word rule that produces exactly one BIP39 word
for every one of the 34 titles (or that explains why exactly these 4, or a
different set of 4, need none), checked against the escrow with
`tools/oracle.py` once the 24-word set is assembled.
What would kill it: this is not a bounded space to exhaust; it stays open until a
rule is proposed.
Cost: needs an insight; no compute action available today.

## 4. The IMDb metadata field that splits 24 keepers from 10 intruders

The rules state plainly that "every information you need can be found on IMDb, on
each movie's page," which means the intruder criterion is a specific IMDb field,
not general knowledge about the films. About 25 to 30 binary criteria have been
tried and refuted (`analysis/tested.md`), including the 3 that looked correct
until the next film identification broke them. My working rule, given how many
criteria have already failed against an incomplete film set, is not to lock in a
new criterion until panels #11 and #34 are both settled, since a 10-out-of-34 split
found against an incomplete corpus has low statistical value on its own.

What would confirm it: an IMDb field that splits the full 34-film set into exactly
24 and 10, tested against the escrow once combined with the word rule.
What would kill it: this is not a bounded space either; it stays open until all 34
films are identified and a field is proposed.
Cost: needs an insight, ideally after leads 1 and 2 are closed; no compute action
available today.


## Community identifications, 2026-08 (issues #9 and #3)

Two readers who watched the films posted panel identifications, one with per-scene
notes (issue #9, garrou), one confirming two panels after re-watching (issue #3,
CryptoBlueprint), plus a full 34-title list with IMDb ids in the issue #9 thread.

**They close the two panels this folder had left open.** Panel 11 is Godzilla (1998),
the footprint scene, and panel 34 is The Human Centipede (First Sequence), which
settles the Dead Ringers / Human Centipede dispute in favour of Human Centipede.
Both are now recorded in `data/films.csv`.

**They also disagree with the 2026-08-04 pass on several panels, and this is the more
important signal.** Each film maps to one BIP39 word, so a wrong title makes the seed
underivable; two independent viewers giving scene-specific descriptions outrank a
still-only pass. The full community list, with IMDb ids and the community's own
title-to-word reading, is now recorded verbatim in `data/films_community_issue9.csv`.

By 2026-08-22 the thread had converged on three panels that this table used to flag:
panel 4 is **Mad Max** (deviceio121's Going Places was corrected by SmallCakekoo against
IMDb, agreeing with this folder), panel 28 is **Scream 2**, and panel 30 is **Toy Story 2**
(couldes, tt0120363; the word is `story`/`toy` either way, so this changes no seed). Those
three are settled. The panels still genuinely unreconciled, community reading first:

| panel | community (viewer) | this folder's 2026-08-04 pass |
|---|---|---|
| 3 | Aliens (1986) | Alien |
| 5 | Alien (1979), leaving-the-ship scene | Star Trek: The Motion Picture |
| 9 | Spartacus (1960) | Duel in the Sun |
| 13 | Leon: The Professional (1994), apartment scene | Goodfellas |
| 14 | The Man in the Iron Mask (1998) | Eyes Wide Shut |
| 16 | The Visitors (1993), first five minutes | The 13th Warrior |
| 23 | Guardians of the Galaxy (2014) | Valerian |
| 24 | Close Encounters of the Third Kind (1977) | Ordinary People |
| 27 | Terminator 2 (1991), biker-bar scene | The Lost Boys |

Where the two lists point the search: under the community identifications, exactly three
titles yield no BIP39 word by any reading (substring, prefix, stem, or cross-token join):
**The Goonies, Leon: The Professional, and Sharknado.** timothy-barus reports running the
three IMDb-metadata intruder rules that leave at most two panels wordless (shares-a-year,
released-2000-or-later, ten-shortest-by-runtime) as exhaustive escrow sweeps, about 1.23
billion checksum-valid seeds in total with two-position wildcards, all empty (his numbers,
not reproduced here). If that holds, compute on the clean metadata rules is spent, and the
open problem is the single transform that turns those three titles into BIP39 words, which
would very likely reveal the rule for the rest.

Next step: reconcile the nine panels above against the actual stills, then recompute the
BIP39 word per title and rerun the C(34,10) reduction through `tools/oracle.py`. Ideas on
the three wordless titles are worth more right now than more compute. This is the
highest-value open work on this puzzle.
