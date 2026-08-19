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

## 9. The small-blob pipeline, first sweeps

The rows above test the 256-symbol object and the large blob. None of them tests the
small-blob pipeline `tools/oracle.py` implements (candidate answer to sha256 password to
AES decrypt to 32-byte key to address). These rows are the first sweeps of it.

Every sweep below was first run against the shipped oracle, which derived the AES key with
EVP_BytesToKey/MD5. That derivation is wrong for this puzzle (see section 10). The counts
and results here are from the re-run under EVP_BytesToKey/SHA-256; the earlier results are
void rather than negative, and are not reported.

Method: candidates pushed through the corrected oracle with no filter ahead of the address
comparison. PKCS7 padding rejects about 255 of every 256 wrong passwords before any
elliptic-curve work, measured at 0.35 percent of random passwords producing valid padding
against 0.39 percent expected, which is what makes this pipeline cheap to sweep. Measured
rate 76,803 candidates per second per core.

| Configuration | Candidates | Result |
|---|---|---|
| Puzzle vocabulary and stage names, each in four cases and reversed | 273 | 0 match |
| Ordered pairs of that vocabulary | 74,256 | 0 match |
| Suffixes and prefixes of the Architect message | 4,174 | 0 match |
| Every contiguous word window up to 14 words of the Architect message, the VIC plaintext, and the phase-2 and phase-3 decryptions | 49,808 | 0 match |
| Last-N-word readings of every stage text, in the conventions the pages state | 5,608 | 0 match |
| Live-page prose re-fetched from the site, SalPhaseIon and Cosmic Duality terms | 17,125 | 0 match |
| The system word list, each entry in four cases and reversed | 1,194,789 | 0 match |
| Confirmed stage passwords and their pairwise concatenations, including the phase-1 form password recovered from the hidden POST form on the theseedisplanted page | 12,544 | 0 match |

Result: 1,358,577 submissions, 0 match. Witness: yes, the corrected oracle reproduces two
real puzzle blobs from their known passwords (section 10). Date: 2026-08-19.

## 10. Key derivation: the shipped oracle used the wrong digest

Not a candidate sweep. `tools/oracle.py` derived the AES key with EVP_BytesToKey/MD5, and
its docstring described MD5 as "the scheme used throughout this puzzle's earlier stages".
That is false, and it is checkable against the puzzle's own material.

Method: the phase-2 and phase-3 blobs were re-fetched from the live page and decrypted
with their known stage passwords under both digests.

| blob | password | MD5 | SHA-256 |
|---|---|---|---|
| phase 2 | sha256 of the stage answer | padding invalid, 35 percent printable | padding valid, 100 percent printable, known plaintext |
| phase 3 | sha256 of the concatenated parts 1 to 7 | padding invalid, 38 percent printable | padding valid, 100 percent printable, known plaintext |

The phase-3 password digest was recomputed independently and reproduces the digest the
community published, which confirms the password string as well as the digest choice.

Why the old selftest passed anyway: its part 2 encrypted a self-made blob with the same
derivation it then decrypted with. A round trip certifies self-consistency, not the digest
choice, and cannot fail on a wrong constant used on both sides. `tools/oracle.py` now
certifies against the phase-2 blob instead, and asserts that MD5 fails on it.

Scope, corrected 2026-08-19: it is proven that MD5 fails on the phase-2 and phase-3
blobs, which is enough to establish that the shipped oracle's hardcoded MD5 was wrong.
It is NOT true that MD5 is unused in this puzzle. The Cosmic Duality blob decrypts only
under EVP_BytesToKey with MD5, verified by reproducing its published plaintext hash
4f7a1e4e...c081 at 1327 bytes from the live page (see section 11). The author therefore
used both digests on different blobs, and nothing determines which the small blob uses,
because its password is unknown. Hardcoding either digest is an error; `tools/oracle.py`
now tries both.

Consequence: any negative previously obtained through the shipped oracle is uncertified
and needs re-running. Date: 2026-08-19.


## 11. Cosmic Duality is decryptable, and it uses MD5

Not a candidate sweep, and a correction to this folder's account of the large blob. Row 6
and the README describe the "Dualite" / Cosmic Duality blob as never successfully
decrypted under any tested password. It has been decrypted, publicly, and the result
reproduces here from primary sources.

Method: the key is the XOR chain of the SHA-256 digests of seven tokens, in order --
matrixsumlist, enter, lastwordsbeforearchichoice, thispassword, matrixsumlist,
yourlastcommand, secondanswer -- giving
a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735. Those 32 raw bytes are
then used as the password to EVP_BytesToKey with MD5 against the blob published on the
SalPhaseIon page.

Result: 1327 bytes of high-entropy output, SHA-256
4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081. Both the key and the
plaintext hash were reproduced independently here from the live page, matching the
published values exactly. Witness: yes, the reproduction is the witness. Date: 2026-08-19.

Note that four of the seven tokens are the strings this folder already documents from the
SalPhaseIon page. They are ingredients in a key derivation, not the answer string the
small blob's password is built from; reading `lastwordsbeforearchichoice` and
`thispassword` as an instruction naming the small blob's password (section 9's last-words
sweeps) is therefore probably the wrong reading of them.

Consequence for the small blob: since the puzzle demonstrably mixes digests, sweeps that
assume one digest cover only half the space. Section 9's sweeps assumed SHA-256 and are
negative only for SHA-256.


## Cumulative

Across the 7 completed hypothesis families above (rows 1 to 7), 335,724,615
candidate submissions were made against the real address-comparison logic used in
the private research, all negative. Row 8's 116,043 submissions are reported
separately because that replay is explicitly partial. Section 9's 1,358,577 submissions
are reported separately again, because they sweep a different half of the final gate (the
small blob) and because they postdate the key-derivation correction in section 10. Rows 1 to 5 test the
hypothesis that the 256-symbol object reduces directly to a 32-byte key, bypassing
the AES blob entirely; row 6 tests the large blob without a password. Rows 1 to 8 do not
test the small-blob pipeline that `tools/oracle.py` in this folder implements
(candidate answer to sha256 password to AES decrypt); as of the private research's last
update that publicly reproducible half of the final gate had not been isolated and swept
on its own. Section 9 is the first sweep of it, and section 10 records why every result
obtained through the shipped oracle before that point has to be discarded.
