# Negatives ledger, FTPK Season 2

Dated 2026-07-26 unless noted otherwise.

## Page-naming scheme as a direct word oracle

Tested whether a game's page name, `sha256(word).html`, could be recomputed directly
from a BIP39 word to search for the right one without solving the game itself: all 2048
BIP39 words, 7 case and format variants each, against MD5, SHA1, SHA256, SHA512, and
SHA3-256, plus double-hashing, plus template variants ("game1", "jeu1", "level1" and
similar, with several salts), plus a 104,334-word system dictionary. 0 hits against the
11 known page names. Refuted as a word oracle: a positive control (recomputing
`sha256("game")`-style names against the dictionary) correctly reproduces all 11 known
page names, proving the negative is real and not a harness bug. The naming scheme's real
function is the meta-puzzle: the 11 known preimages, in game order, spell "the last game
has for url this sentence that is hashed", which names the URL of a 12th, hidden game.

## Per-game structural checks

- Game 1 candidate matching a famous Cold War barrier: an image of it sits behind an invisible link on the
  page. Decrypting Game 1's own cipher (a Vigenere cipher keyed to a well-known 2012-14
  puzzle series) reveals the author's own text naming both this image and a second
  hidden image layer as decoys. Refuted directly by the puzzle's own plaintext, not by a
  candidate sweep.
- Game 5: an early reading of a digit grid, taken as a matrix-diagonal transcription,
  produced a number that returned HTTP 404 when probed as a page name. A corrected
  reading, taken as a plain visual diagonal of the same rendered block, returned HTTP
  200, confirming the corrected transcription rule advances to a further step; the word
  itself is not yet fixed.
- Game 12 audio track: spectrogram analysis of the left, right, and left-minus-right
  channels (window size 16384) found no hidden image encoded in the spectrum. The track
  is genuine music, meaning the intended reading is a note-to-digit transcription (the
  method a Season 1 page by the same author uses), not identifying the recording itself.
- Game 10: 2 short sub-poems on the page were checked for an acrostic (first letter of
  each line spelling a word). Neither does.
- Image steganalysis: the second decoy image from Game 1 was checked for an LSB payload
  across 30 channel and bit-order layouts. Nothing found; no appended bytes past the file
  end either.
- No HTML comments or `data-*` attributes exist anywhere on the mirrored site.
- A public code repository for the author or any variant of the puzzle's name does not
  exist (checked via the GitHub search API, 0 results).
- `robots.txt`, `sitemap.xml`, and `sitemap-index.xml` all return HTTP 404 on the puzzle
  site: they do not exist and hide nothing.

None of these checks carries a planted witness proving a full 12-word sweep would find a
real answer if one were in scope, since 0 of the 12 words are confirmed yet; each row's
witness column reflects only whether that specific check's own harness was proven to
work (a positive control), not whether the derivation oracle has been exercised on a
real solution.
