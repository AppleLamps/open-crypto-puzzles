# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row. All
counts and witness claims below are re-read from the private research folder's own
established-facts register before being written here. A review on 2026-07-28 found
that an appearance-based acceptance filter used in about 46% of the folder's scripts
(98 of 213) had been silently rejecting the correct answer shape for years, because
it required decrypted plaintext to look like printable ASCII when the expected
plaintext is raw key material. The negatives below post-date that fix: nothing here
judges a candidate on how it looks, only on whether it reproduces the target address
exactly.

## 1. Letter-to-bit mask reduction of the 256-symbol object

The final odd-position stream of the puzzle's own Bifid decoding step reduces, after
removing the two Base58-ambiguous letters I and O, to exactly 256 symbols drawn from
a 23-letter alphabet. The most direct hypothesis is that each symbol maps to one bit
of a 256-bit key.

Method: every letter-to-bit mask, tested both in linear reading order and under 20
spatial reading orders (row-major, column-major, spiral, boustrophedon, and their
reverses).

Result: 335,000,000 submissions, 0 match. Witness: yes, two independent
implementations reproduced the same negative and an injected known-good object was
correctly flagged by both. Date: 2026-07-28.

## 2. 16+7 partitions of the 256-symbol object's alphabet

Hypothesis: the 23-letter alphabet splits into a 16-letter and a 7-letter group
(echoing "23 individuals, 16 female, 7 male" from the source text the final page's
prose is adapted from), each group indexing a different half of the key.

Method: all 245,157 possible 16+7 partitions of a 23-symbol alphabet, both
polarities.

Result: 490,314 submissions (245,157 x 2), 0 match. Witness: yes, autotest by
injecting a known-good partition into the same code path. Date: 2026-07-28.

## 3. The 32 target numbers as ASCII codes of a substring

Hypothesis: the 32 numbers the final gate expects are the ASCII codes of 32
consecutive characters taken from one of the puzzle's known decoded objects.

Method: 10 candidate source objects x 2 letter cases x 2 reading directions x every
window of 32 consecutive characters x 2 value conventions (direct ASCII, or the
letter's rank in the reduced alphabet).

Result: 34,000 candidates, 0 match. Witness: yes. Date: 2026-07-28.

## 4. The 256-symbol object read as a single Base58 number

Hypothesis: the object, or the string it derives from, is a private key written
directly in Base58 (matching the object's own alphabet, which happens to exclude
the two Base58-ambiguous letters I and O).

Method: windows of 43, 44 and 45 characters (the length of a Base58-encoded 32-byte
value), every position, both reading directions, 2 extraction conventions, plus the
object read whole.

Result: 17,304 candidates, 0 match. Witness: yes. Date: 2026-07-28.

## 5. A substring of the object is Base58 to decode

A related but distinct hypothesis: some substring of the 256-symbol object, or of
the 570-character string it derives from with I and O removed, is a Base58Check
string with a valid checksum, rather than a raw private key encoding.

Method: every substring of length 21 to 64 characters, both reading directions, on
both source objects.

Result: 123,728 submissions, 0 match, and separately: zero valid Base58Check
checksum found anywhere in this space. That checksum observation is reported as a
fact, not used as a filter ahead of the address-comparison step. Witness: yes.
Date: 2026-07-28.

## 6. Direct readings of the large "Dualite" blob without a password

Hypothesis: the second, larger OpenSSL-format blob on the final page (titled
"Dualite" in the page's own markup) might be plain bits to read directly, rather
than something requiring a password.

Method: every 256-bit window (step 1 bit) of the decoded blob, submitted directly
to the address comparison, no key involved.

Result: 59,269 submissions, 0 match. A companion entropy measurement (byte
histogram, autocorrelation) on the same blob shows it is indistinguishable from
well-formed AES-CBC ciphertext, not from noise or a decorative filler value.
Witness: yes, on both the submission sweep and the entropy measurement.
Date: 2026-07-30. This narrows the interpretation (it is encrypted data with an
unknown key, not noise to read directly) without narrowing the space of possible
passwords, which has not been swept for this blob: see the README's mechanism
section for why this repository does not ship an oracle for it.

## 7. Taijitu (yin-yang) antisymmetry reading of the 256-symbol object

Hypothesis: the object, read as a binary image under some letter-to-bit mask, forms
a taijitu (rotationally antisymmetric) pattern, echoing a creator hint about a
"ying yang".

Method: analytic check, not a search: for every one of the 128 possible letter
pairings needed to test 180-degree rotational antisymmetry under any mask, checked
whether at least one pair of positions is forced to carry the same letter twice.

Result: every one of the 128 pairings fails this check, so no letter-to-bit mask can
produce a taijitu from this object. Refuted analytically; no submissions needed.
Date: 2026-07-28.

## 8. A partial replay of literal candidate strings from the folder's own history

Hypothesis: among literal password guesses tried by scripts written over several
years, some were built correctly but never reached a real address comparison,
because of the appearance-based filter bug described above.

Method: 13,090 literal strings harvested from 1,017 archived scripts that contain
password-guessing logic, submitted directly to an address comparison with zero
rejection ahead of that comparison; separately, the single most-repeated candidate
family across the same archive (69,454 variants).

Result: 46,589 plus 69,454 submissions, 0 match. Witness: yes, head, middle and
tail witnesses recovered. Date: 2026-07-28. This is explicitly a partial replay,
not a completed one: it covers literal strings only, not the patterns those same
scripts constructed dynamically at run time (concatenations, permutations, chained
derivations). Those dynamic patterns are the subject of the open lead ranked first
in the README; this row is why that lead is ranked first rather than closed.

## Cumulative

Across the 7 completed hypothesis families above (rows 1 to 7), 335,724,615
candidate submissions were made against the real address-comparison logic used in
the private research, all negative. Row 8's 116,043 submissions are reported
separately because that replay is explicitly partial. Rows 1 to 5 test the
hypothesis that the 256-symbol object reduces directly to a 32-byte key, bypassing
the AES blob entirely; row 6 tests the large blob without a password. None of these
rows tested the small-blob pipeline that `tools/oracle.py` in this folder
implements (candidate answer to sha256 password to AES decrypt); that specific,
publicly reproducible half of the final gate had not been isolated and swept on its
own as of the private research's last update.
