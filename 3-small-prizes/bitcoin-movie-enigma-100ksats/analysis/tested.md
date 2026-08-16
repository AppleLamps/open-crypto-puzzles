# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row. All
counts below were re-read from my own private research notes before writing this
folder.

## Both published image sets are identical

The rules page mentions "an alternative release, as a single image." I compared
every one of the 34 individual panel images against the corresponding region of the
combined alternative-release image, byte for byte (MD5).

Result: 34 of 34 panels match exactly. This channel is closed: the alternative
release carries no additional or different information, it is the same 34 stills
republished as one file. Date: 2026-08-03.

## Intruder criterion: MPAA rating equals R

Hypothesis: the 10 "intruder" films are exactly the ones rated R by the MPAA, and
the IMDb page field the rules point to is the certificate rating.

Method: count the films confirmed R-rated as more panels were identified.

Result: this criterion looked correct early, when only a partial set of films was
identified (10 of 18 identified films rated R at one point). It broke as soon as 2
more films were confirmed: with panel #4 (Mad Max, R) and panel #34 (rated R under
either of its 2 disputed identifications) added, the R-rated count reached 16 to 18
out of the identified films, well past 10. Refuted. Witness: this is a direct count
over the film corpus, not a search that could produce a false negative; re-counting
is immediate from `data/films.csv`. Date: 2026-08-04.

## Intruder criterion: won at least one Oscar

Hypothesis: the 10 intruders are the films that won at least one Academy Award.

Method: same approach, counting Oscar-winning films as identifications accumulated.

Result: looked correct at 10 of 21 identified films early on, refuted once panel
#24 (Ordinary People, a 4-Oscar winner including Best Picture) was confirmed
through a route independent of the reverse-image search used for most other
panels, pushing the count to 11 of 34. Date: 2026-08-04.

## Intruder criterion: adapted from a novel

Hypothesis: the 10 intruders are the films adapted from a published novel.

Method: same approach.

Result: looked correct at 10 of 31 identified films, refuted at 12 of 34 once
further identifications landed. Date: 2026-08-04.

## About 25 further intruder criteria

Method: the same accumulate-and-recount approach applied to about 25 further
candidate IMDb fields and binary properties (examples: country of origin,
decade of release, director's other Bitcoin-relevant work, runtime bracket, color
versus black and white, single-word versus multi-word title).

Result: none produced an exact 24-versus-10 split against the identified film set,
either from the start or after refutation by a later identification. Witness: each
criterion is a direct count over the film corpus and is immediately re-checkable;
no witness protocol beyond re-counting applies here. Date: 2026-08-04.

Methodological note, kept because it explains why no criterion is locked in below:
3 different criteria (MPAA=R, Oscar win, novel adaptation) each looked like the
answer while the film corpus was still incomplete, and each was broken by the very
next identification. With about 25 to 30 criteria tried against a set of only 34
films, landing on an exact 10-film split by chance is not strong evidence on its
own. My working rule is to not treat any criterion as confirmed before all 34
panels are identified with confidence.

## Title-to-word rule: base rate measurement

This is a measurement, not a hypothesis test with a pass or fail result: of the 33
titles identified as of 2026-08-04, 29 contain at least one English BIP39 word as a
literal substring of the title (for example, "Die Hard" contains "hard"; "A
Clockwork Orange" contains 4 candidates: "clock," "orange," "range," "work"). Four
titles contain none: The Goonies, Barry Lyndon, Sharknado, and Raiders of the Lost
Ark. The literal-substring rate across the 33 identified titles is about 14%,
counted per candidate word against the full BIP39 wordlist. This measurement rules
out "every title contains exactly one obvious word" as the full rule (4 titles have
none, several have more than one), but does not by itself say which of several
candidate words is the intended one, or what the rule is for the 4 titles with none.
