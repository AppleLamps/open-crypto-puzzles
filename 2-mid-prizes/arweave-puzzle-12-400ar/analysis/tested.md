# Negatives ledger, Arweave Puzzle Weave #12

Every candidate sweep used the certified oracle (SHA-512 x11513, AES-OpenSSL decrypt,
`"kty":"RSA"` gate, exact 58-character length filter). None of these runs carries a
planted witness inside its own candidate space, since the correct answer is unknown; the
oracle itself is certified separately against the solved sibling Arweave #8 (see the
README's "Certified against" section). All dated 2026-07-25.

| # | Configuration | Candidates | Result |
|---|---|---|---|
| 1 | Piece 4 hatching read as an ordering scheme: all 4! direction-to-digit assignments across 6 quadrant reading orders | 144 | refuted exhaustively: no assignment produces a valid 1-to-5 permutation or a 5-letter word |
| 2 | Round-1 bounded assembly: 4 sub-answers, 24 orders, 3 cases, length-filtered to exactly 58 | 104,184 (858 seconds) | 0 match |
| 3 | Round-2: the 2 length partitions that survived round 1, 6 orders, 36 color names, Gray/Grey spelling, 2 cases | 46,688 (441 seconds) | 0 match |
| 4 | "BLUE" literal readings, 6 bounded runs: orders, spellings, cases, anagrams | 3,266 | 0 match |
| 5 | Literal `Hexagon`, `BalaenopteraMusculus` (20 characters), and 4-number reorderings | 1,824 | 0 match |
| 6 | Piece 1 read as RGB decimal or hex numbers instead of color words, 4 orders x 5 piece-2 candidates x anagrams x 2 block orders, exact-58 constrained | 768 | 0 match |

Also refuted, not a candidate sweep: steganography in the jigsaw JPEG and the page's
favicon (no EXIF or XMP metadata, 0 trailing bytes after the JPEG end marker, `zsteg -a`
returns noise only, the favicon's alpha channel is ordinary anti-aliasing). The author's
full transaction history was paged to exhaustion; the only asset near the funding or
publication window is a PNG image byte-identical to sibling puzzle #11's, not a hint
specific to #12.

Cumulative: 156,730 assembled 58-character candidates tested against the escrow, 0
matches. 3 of the 4 sub-answers have a strong-to-certain reading; the gap is piece 2's
exact 18-character string, plus an oracle-confirmed hit on piece 1.
