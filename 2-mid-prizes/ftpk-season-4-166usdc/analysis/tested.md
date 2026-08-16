# Negatives ledger, FTPK Season 4

Dated 2026-07-26 unless noted otherwise.

## Page-naming scheme

Every game page is named `md5(N).html` for a decimal integer `N`; probing roughly 34,000
URLs (every N from 0 to 2200, a set of thematic word hashes, and a wider sweep up to
36,000) found exactly the 12 known game pages plus 1 further page, the one the author
announced as a Season 2 hint (its input string is the 12 Season 4 answer words
concatenated in game order, matching the site's own naming convention). No other hidden
page exists in this range.

Testing whether N itself is a direct index into the BIP39 wordlist: game 1's own hangman
mechanics fix the answer as `frog` with confidence (pattern `??o?`, corner tags "1st" and
"dance" marking already-excluded letters and the first alphabetically surviving
candidate). Game 1's page-naming integer is 1570, which indexes to "service" or "session"
in the BIP39 list depending on 0- or 1-based counting; neither word fits the `??o?`
pattern. Refuted as a direct index scheme.

## Grid puzzles

Games 4 (8x8, corner tag "fall"), 6 (15x15), and 9 (11x11, corner tag "5:30") were
searched in all 8 directions, length 4 or more, against both the full BIP39 wordlist and
a 75,145-word English dictionary. Game 4 returned 2 incidental matches ("time" and
"evans"), neither fitting any established pattern; games 6 and 9 returned 0 matches.
Refuted as classic word-search puzzles.

Game 12 (a Ludo board with colored squares) and game 6 are both 15x15, which looked
intentional; overlaying the Ludo board's colored-square mask onto the letter grid in
row-major order produces unreadable sequences (for example the silver squares read
`AVEXRO`, the khaki squares `PVMIJT`). Refuted for the naive row-major alignment; other
alignments (rotations, reflections, or reading the board's own path order) were not
exhausted.

Game 3 (a subtraction problem rendered in colored dots): reading the full dot pattern as
a base-3 number under each of 6 color-to-digit assignments, then subtracting as the
puzzle's layout implies, produces 10 or 11-digit results under every assignment, none in
the 1 to 2048 range a BIP39 index would need. Refuted as stated; the puzzle's structure
is confirmed, its encoding is not yet solved.

## Oracle self-test

`tools/oracle.py --selftest` reproduces the public BIP39/BIP44 test mnemonic (12
repetitions of "abandon" followed by "about") deriving to
`0x9858EfFD232B4033E47d90003D41EC34EcaEda94`, and separately confirms the checksum filter
accepts that vector and rejects a corrupted variant of it. Measured on one CPU core: 956
mnemonic derivations per second, and 1.5 million BIP39 checksum checks per second with a
6.23 percent pass rate, matching the 1-in-16 rate BIP39's checksum design predicts.

None of the grid and page-naming checks above carries a planted witness proving a search
would find a real answer if one were in scope, since most of the 12 words are not yet
established; each row's witness reflects only whether that specific check's own method
was validated (a positive control), not whether the full derivation oracle has been
exercised on a real solution.
