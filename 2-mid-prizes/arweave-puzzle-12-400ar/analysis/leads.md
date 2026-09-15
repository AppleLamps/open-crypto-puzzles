# Open leads, ranked -- Arweave Puzzle Weave #12

Supersedes the README's "Open leads, ranked" and an earlier draft of this file, as of
2026-09-15. Piece 2 remains the blocker. Every length pairing that closes p1 + p2 = 46
with a source-material reading of both pieces is now dead.

## What is now settled

- **Piece 3 = `2111011`**, independently re-derived (square/diamond/rectangle fix the
  ascender-x-height-descender rule with no free parameter; hexagon follows).
- **Piece 4 is exactly five letters** -- five hatched squares at 88-89px, five orange
  glyphs, stable across thresholds. The six-letter-word idea is refuted. All 120 letter
  orders have been swept, not just the dictionary anagrams.
- **Piece 1's candidate orderings are measured, not guessed.** Three vertical pairs by
  flag x-position; twelve principled reading orders; 144 strings instead of 4,320.
- **The 28+18 split is dead** across all 24 block orders and all 144 orderings for
  `AndreessenHorowitz`, and across 35 further 18-character organisation / founder /
  whale+date / Forbes-date concatenations (rows 20, 23-25).

## 1. Piece 4's answer may not be the five letters -- WORKED OUT AND DEAD

The hatching on piece 4 is the Petra Sancta heraldic convention -- each square quartered,
each quadrant hatched in the direction that denotes a tincture (see tested.md). Two of
the four clues are therefore about colour, which is unlikely to be a coincidence.

Worked out 2026-08-19 and negative in every form tested (tested.md rows 18 and 19, and
the decoding notes there): as five ASCII bytes at two bits per quadrant, as eight
five-bit letters, and as a literal 20-character sub-answer against all four length
pairings that 58 - 7 - 20 = 31 admits.

The heraldic identification itself stands and is worth keeping -- the hatching is a
recognised colour notation drawn correctly in four directions, not decoration. But it has
no demonstrated role in the answer under any of the three readings now tested:
directional ordering (row 1), heraldic tincture (rows 18 and 19), or line count.

A warning for whoever picks this up: hatch-line counts are **not** reliably measurable
here. Three counting methods give three different answers, and one of them produces a
seductive run of five consecutive integers that is pure artifact.

## 2. Piece 2, without the proper-noun assumption

Every search so far, here and in the community, has assumed piece 2 is a name. Sibling
#5's confirmed sub-answers are `*`, `48`, `GCE` and `Eris`; sibling #3's are
four-character tokens including the chess move `e4d5`. This author uses bare symbols,
numbers and acronyms freely.

So piece 2 may be an acronym (`a16z`, `USV`, `AH`), a bare number, or a date string, at a
length that pairs with a different piece-1 reading. The length algebra in tested.md gives
the pairings. Swept as of 2026-09-15: 28+18 (including a new 18-character organisation /
whale+date / Forbes-date list, rows 20, 23-25), 12+34, 11+35, 9+37, 36+10 (date as drawn),
42+4 (`a16z`), 38+8 (`16032020` with hex codes plus `IQ`/`AR`, row 21), and 32+14
(Cerulean for the blank flag, row 22). Nothing cheap remains on this branch.

## 2. Piece 1 as something other than colour names -- AUDITED AND CLOSED

Done, 2026-08-18; see the assumption audit in tested.md. The attributes were measured
(ball on violet/red/green, none on gray/purple/blank; flag side opposing in all three
pairs) and turn out to be scaffolding: the blank flag's attributes are fully determined
by its partner, so they encode the pairing rather than a payload. Reading them as an
18-bit answer is refuted on that principle, no sweep required.

Every colour-derived encoding whose length pairs with a supported piece-2 reading is now
dead: six names (28) with `AndreessenHorowitz` and with 35 other 18-character strings,
three primary names (12) with AH+CoinbaseVentures, six bare hex codes (36) with the date
as drawn, six `#`-prefixed codes (42) with `a16z`, six hex codes plus `IQ`/`AR` (38) with
`16032020`, and Cerulean-for-Blue (32) with five 14-character piece-2 strings. The two
encodings left untested -- a single colour name (4) and one-letter abbreviations (6) --
are untested because nothing plausible sits at the 42- and 40-character piece-2 lengths
they force.

The audit's own conclusion is that piece 1 is not where the error is.

## 3. All four clues pointing at one answer -- TESTED AND DEAD

Swept 2026-08-19 (row 17): every ordered concatenation of the clue-implied vocabulary
totalling exactly 58 characters, 516,138 candidates, 0 match.

There is also an argument against the model that should have been weighed earlier. Piece
3's answer is a *digit string*, `2111011`, and that is certain: the puzzle prints codes on
three shapes and leaves the hexagon's blank. Four clues cannot jointly name a
natural-language phrase when one of them contributes digits. The concatenation model is
the right one, and it matches sibling #5, whose confirmed sub-answers were a symbol, a
number, an acronym and a name.

So the error is in a sub-answer, not in the model joining them.

## 4. Upstream the fast-reject oracle (tooling) -- SHIPPED 2026-09-15

`tools/oracle.py --fast` decrypts plaintext block 0 only; any hit is re-checked through
the full pipeline before MATCH. `--selftest` certifies that sibling #8's keyfile begins
with `{"kty":"RSA"` at offset 0, and that a case flip, a truncation, and #8's answer
against #12's ciphertext all reject. Scope limit unchanged: a gate at a non-zero offset
would be missed by `--fast` and caught by the default path.

## 5. What is left (2026-09-15)

The length algebra with p3 = 7 and p4 = 5 has no remaining source-material pairing.
Either piece 2 is an 18-character string with no public name attached (a private
nickname, a non-English word, a hash prefix), which is not insight-shaped, or one of
the "certain" pieces is still misread. The cheapest remaining structural doubts:

- Piece 4 is five letters but the intended string is not an anagram of IEALN. A sixth
  implied letter was already refuted by measurement; a non-letter reading (tincture
  initials) is dead in row 18.
- Piece 1 is not colour names and not hex. The audit priced the leftover encodings at
  4 and 6 characters, which force 42- and 40-character piece-2 strings. An Ethereum
  address is 42 characters, but the 16-03-2020 round was a private equity round, not
  an on-chain transfer.
- The whale is drawn as a blue whale. `BalaenopteraMusculus` is 20 characters and is
  already length-refuted against p3 = 7, p4 = 5.

I would rank "look at sibling #5's mix of symbol / number / acronym, not more
18-character English names" above another name sweep.

## Retired

- **"Confirm piece 1's blank flag as Blue by an oracle hit"** (README rank 2). Not
  independently testable: an oracle hit needs every block correct at once, so no sweep can
  confirm or refute Blue while piece 2 is unknown. The structural case for Blue is
  nonetheless strong -- one additive primary per measured pair -- and the lengths close
  exactly at 28.
- **Co-investor names as piece 2 at length 18.** Length-refuted:
  `UnionSquareVentures` is 19, `CoinbaseVentures` is 16. Both have now been swept in the
  two- and three-name concatenations where their lengths do close the budget.
- **Hatching as an ordering scheme.** Confirmed refuted a second time, by measurement:
  distinct hatch directions per square are 3,2,3,4,3, not a permutation of 1 to 5.
- **`--fast` oracle flag.** Shipped 2026-09-15.
- **New 18-character piece-2 outside the investor spelling** (Arweave Foundation,
  Permaweb Foundation, Grants+Boost, whale+date concatenations, Forbes-date concatenations).
  Dead, rows 20 and 23-25.
- **`16032020` with piece 1 at 38 as hex+IQ/AR.** Dead, row 21.
- **Blank flag as Cerulean from the whale fill `#20a0c8`.** Dead, row 22.
