# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Replay the dynamically-constructed candidates that a filter bug never reached

The 2026-07-28 review (see `analysis/tested.md`) found that an appearance-based
acceptance filter had been silently rejecting the correct answer shape in 98 of 213
historical scripts. A first replay already resubmitted 116,043 literal strings
harvested from those scripts directly to the real address comparison (0 match, see
`analysis/tested.md` row 8), but that replay covers literal strings only. The same
scripts also constructed candidates dynamically at run time: token concatenations,
permutations of decoded fragments, and chained transforms (for example, applying a
Vigenere step and then a substitution step in sequence). Those dynamic candidates
were generated, passed through the same broken filter, and discarded, but were
never logged as literal strings, so this first replay cannot reach them.

What would confirm it: re-running each script's own candidate-generation logic
(not just its final output) with the filter bug fixed, and finding a match.
What would kill it: exhausting the same generation logic with no match; since the
scripts number in the hundreds, this is judged in stages, not as one pass.
Cost: hours to days, since the generation logic differs script by script and each
needs re-reading before it can be replayed correctly.

## 2. Determine whether the 256-symbol object is the right object at all

Every hypothesis in `analysis/tested.md` rows 1 to 5 assumes the final key comes
directly from the 256-symbol, 23-letter object produced by the puzzle's Bifid
decoding step. That assumption has one point in its favor: of the 7 possible
letter-pairs that could be removed from the 285-letter pre-reduction stream to
leave exactly 256 symbols, exactly one (the pair I and O) yields a Base58-valid
alphabet, which is unlikely to be accidental. But the object itself is written
entirely in uppercase letters, and an all-uppercase Base58 encoding of 32 bytes has
a chance of about 1 in 10^17 of arising by coincidence, which argues against reading
it as a literal Base58 string (consistent with row 4 and row 5 both being negative).

What would confirm it: a reduction of the object to 32 bytes, other than the ones
already tried, that matches an address.
What would kill it, or redirect it: establishing that the final key instead comes
from the AES-blob route this folder's oracle implements (`tools/oracle.py`), or
from the still-unopened "Dualite" blob, making the 256-symbol object a waypoint
rather than the key's direct source.
Cost: an afternoon of directed reasoning, not a sweep; this lead is about which
object to target next, not about enumerating more of the current one.

## 3. Identify the tool the author says was used at every phase

An authenticated statement from the puzzle's author says the same software was used
to build every phase of the puzzle. Comparing the cipher conventions confirmed on
already-solved stages against one specific, publicly available cipher tool's source
code shows an exact match on non-obvious implementation details: the tool's Bifid
implementation takes no period parameter (it always uses a period equal to the full
message length, which is exactly the convention confirmed on this puzzle's own
Bifid step), and its available cipher list is short. If this identification is
right, it bounds every remaining cipher hypothesis to that tool's own menu, instead
of the space of all published ciphers.

What would confirm it: a cipher from that tool's menu, applied with its default
conventions, producing a match on a currently unexplained object (most plausibly
the "Dualite" blob's password, or the reduction step from the 256-symbol object).
What would kill it: the author naming a different tool, or every cipher on the
identified tool's menu being exhausted with no match.
Cost: the tool's menu is short (documented in the private research as fewer than a
dozen ciphers); testing all of them against the currently open objects is a matter
of hours.

## 4. Follow "esrever" the first published hint

The earliest hint attributed to the author reads "esrever" ("reverse" spelled
backwards) applied to a specific decoded object early in the puzzle. This hint
predates most of the puzzle's later stages and has not been exploited on the
current final-gate objects (the 256-symbol object, the small blob, or the
"Dualite" blob), only on the object it was originally paired with.

What would confirm it: applying a reversal (of reading order, of case, or of the
described object itself) to one of the current final-gate objects and getting a
match.
What would kill it: exhausting the small set of reasonable "reverse" readings
(string reversal, bit reversal, reading-order reversal) on all three current
objects with no match.
Cost: minutes to hours; this is a small, well-defined space, not a sweep.

## 5. Read the 29 symbols dropped during the object-256 reduction

Reducing the 285-letter pre-reduction stream to the 256-symbol object drops exactly
29 letters (the I's and O's removed to reach the Base58-safe alphabet). Every
hypothesis so far treats those 29 letters as discard. They have not been read as a
message in their own right, in their own extraction order.

What would confirm it: reading the 29 dropped letters (in order of removal) as
their own object and finding a match, or a legible fragment that leads to one.
What would kill it: reading them under the small set of reasonable orderings
(extraction order, position order) and finding neither a match nor a legible
fragment.
Cost: minutes; the space is small (29 letters, a handful of reading orders).

## Where the "Dualite" blob and the second address fit

The "Dualite" blob (see the README's mechanism section) is confirmed to be
well-formed AES-CBC ciphertext, not noise, and has never been successfully
decrypted under any tested password (`analysis/tested.md` row 6). No lead above
targets it directly with a password sweep, because no password-generation
hypothesis for it currently has more support than any other; leads 2 to 4 are the
routes most likely to produce one.
