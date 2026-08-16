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
