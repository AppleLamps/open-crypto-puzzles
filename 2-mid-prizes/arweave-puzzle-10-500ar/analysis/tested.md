# Negatives ledger, Arweave Puzzle #10

Every run used the certified oracle (SHA-512 x11513, AES-OpenSSL decrypt, `"kty":"RSA"`
gate). None of these runs carries a planted witness inside its own candidate space, since
the correct answer is unknown; the oracle itself is certified separately against the
solved sibling Arweave #8 (see the README's "Certified against" section). All dated
2026-07-25 unless noted otherwise.

| Family | Candidates | Notes |
|---|---|---|
| Curated left-to-right literal-token battery | 412 | reads the 5 keys as their obvious literal tokens, joined in image order |
| Grammar-calibrated pass | 1,798 | same reading style, expanded with the solved-siblings' answer grammar |
| 20-character hard-length reading of `[0-19]` | 6,492 | treats the bracket as a literal length specifier |
| "Paradise"-centric candidates across all lengths | 4,480 | follows a community reading of the dice/silhouette pair |
| Corrected structure: Palpatine not Vader, genesis key kept separate | 4,122 | |
| Corrected structure: slice-first-20 reading | 8,558 | |
| GPU sweep: image-order concatenation | 1,200,000 | rented GPU, certified exact-match gate |
| GPU sweep: separator concatenation | 800,000 | |
| GPU sweep: no-separator slice-to-20 over 6 orders | 640,000 | |
| GPU sweep: special-character connector variants | 660,000 | |
| GPU sweep: "Paradise"-pun forms | 40,000 | |
| Genesis-block message family | 9,187 | 314 genesis-block messages, 9 normalizations each |
| Pun/anagram/re-reading sweep, order A (genesis is the whole answer) | 660 | |
| Pun/anagram/re-reading sweep, pun image-order | 350,064 | |
| Pun/anagram/re-reading sweep, 2 extra orders | 230,400 each (460,800 total) | |
| Pun/anagram/re-reading sweep, Bible/Genesis-28-as-scripture axis | 35,910 + 532 | includes Hebrew transliterations |
| Curated 5-slot product with empty slots and slice-to-20 | 3,787,175 | |

One generator (a roughly 70,000-candidate literal `0..19` reading) was started and killed
before completion; it is not counted as a negative, since it never finished. Two further
candidate sets, an "on paper = on computer" notation reading (255,365 candidates) and a
wider exact-length-20 vocabulary set (2,196,517 candidates), were generated but not
confirmed run to exhaustion; they are not counted here either.

Also refuted, not a candidate sweep: forensic steganalysis of the puzzle image
(exiftool, binwalk, `zsteg -a`) found no LSB payload, no appended bytes, and no metadata
payload. A visually suspected "watermark strip" in a community-assembled composite image
was measured (cross-correlation against the authoritative on-chain PNG, peak correlation
0.41) and judged an upscaling artifact rather than a real signal, since that composite is
larger than every known authentic source of the image.

Cumulative: on the order of 8,010,190 candidates tested to completion across every
literal, pun, notation, and genesis-block reading found so far, 0 matches.
