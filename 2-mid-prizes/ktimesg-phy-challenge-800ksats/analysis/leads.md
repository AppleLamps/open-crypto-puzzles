# Leads (full notes): Phy Challenge

Ordered by cost to test, then by expected value.

## Thread state on 2026-10-07 (96 posts)

What the community has established since this folder was written, re-read from the thread:

- The 9 bytes of `s` (91, 137, 11, 41, 43, 161, 171, 217, 177) are emoji IDs in a forum
  member's numbering of the image, and the low bytes of those 9 emojis' Unicode code points
  spell `1dffd7ff0d400f0a...0d080f` (`0d 40 0f` is ZWJ, female sign, VS16; `fb` to `ff` are
  the skin tone modifiers). With a `03` prefix it is a valid compressed point. The numbering
  is not public (its author's GitHub repo is private), so this step is reported, not
  reproduced here.
- The meta-clue `gvonys fhelucrM kbZ`, ROT13 then each word reversed, reads `flabit Zephyrus
  Mox`: Latin, "soon the west wind will blow".
- The author, in the post after the meta-clue: the LLM-driven readings miss "the actual structural
  things that a human brain would instantly see and wonder about".

What it implies: for `s` to name emoji IDs, the author chose `s` and the nonce `k` and then
derived the key as `d = (s*k - z)/r mod n`. So `k` must be published in the image, and the
point `H` is either a decoy or a step towards `k`.

## Measured emoji table (2026-10-07)

`data/emoji-table.json` holds all 256 emojis measured from `clues/spiral.png` rather than read by
eye: centre, best-matching Apple glyph as a Unicode sequence, skin tone, and how much better
the mirrored glyph fits. Rebuild with `tools/emoji_table/`. What it established:

- The background is fully transparent (alpha 0); the only coloured object is the coin, centred
  at about (1023.5, 1030.1).
- The greyscale conversion is Rec.709 luminance: against 41 tone-free glyphs it fits with a
  mean quantile error of 7.0, against 9.7 for Rec.601 and 27.6 for a plain average.
- Shape match is strong: median correlation 0.981; 9 glyphs score below 0.93 and deserve a
  manual look (ballet dancer, woman feeding baby, and a few people glyphs).
- 205 asymmetric glyphs are drawn in Apple's normal orientation. The 9 that match mirrored are
  walking, running, kneeling, white-cane and wheelchair figures facing right, which is how the
  Unicode "facing right" sequences look, plus a backhand index. "Every emoji is mirrored", said
  in the thread, is not true.
- Skin tone is decided within each glyph family by luminance quantiles; 42 of 256 calls have a
  runner-up within 2 levels and are uncertain.
- Colour restoration (`tools/emoji_table/tone2.py`): every tone variant of each glyph is converted
  to Rec.709 grey, scaled to the puzzle glyph's box and compared pixel by pixel. Measured from the
  references, the skin grey levels are 227 (light), 204 (default yellow), 198 (medium-light),
  about 150 (medium), 114 (medium-dark) and 75 (dark). Default yellow and medium-light are 6
  levels apart, and that pair accounts for 24 of the 41 tone calls whose runner-up is within 25
  percent; medium-dark against dark accounts for 10 more. This is the most likely meaning of the
  author's remark that the image "was redrawn and requires to test the skin-tone to fix the
  image". Hearts and other coloured objects carry the same problem (a grey heart could be several
  colours) and were not resolved. A restored colour picture is easy to render from the table, but
  it is not stored here because it reproduces Apple's artwork.
- Calibrated skin tones (`tools/emoji_table/skin.py`, `calibrate.py`): measuring only each glyph's
  skin pixels (the pixels that change between its tone variants, eroded by 2) and fitting the
  puzzle's grey against the references gives **puzzle grey = 1.1225 x Rec.709 - 16.15**, a
  contrast stretch, with a median residual of 0.76 grey levels over 183 single-person glyphs.
  With that calibration only 5 tone calls stay uncertain (emojis 77, 114, 150, 180, 214), down
  from 41. This is most likely the "much easier and precise normalization" the author mentions.
  Tone counts among those 183: medium-dark 40, default yellow 36, light 29, medium-light 29,
  medium 25, dark 24. `data/emoji-table.json` now carries the calibration and these calls.
- Spiral geometry (`tools/emoji_table/geometry.py`, `data/spiral-geometry.json`). The layout is
  exactly point-symmetric: all 256 emojis form 128 mutual mirror pairs through a centre at about
  (1023.9, 1017.5), median mismatch 1.7 px against 44 px for random rotations. The centre sits
  about 12.5 px above the coin's measured centroid. Pair n (1 to 128) lies at radius
  76.045*sqrt(n) + 42.822 px and angle 319.72 + 130.2601*n degrees (image coordinates), its
  partner at the same radius plus 180 degrees; the fit leaves 1.2 px median error. The divergence
  angle is 130.26 degrees, not the golden 137.51. The offsets from this ideal carry no data (see
  `analysis/tested.md`). The geometric order agrees with the "in-out A,B" draw order posted in
  the thread, so that order is now confirmed from the image rather than assumed. The two
  emojis of a pair share no base glyph (0 of 128) and share a skin tone only 26 times out of 128,
  close to chance. Unexplained so far: why 130.26 degrees, and why the symmetry centre is offset
  from the coin.
- The divergence angle has no clean closed form: the nearest simple fraction of a turn is 55/152
  (130.263 degrees), and no golden-ratio or `e` expression matches. It was probably tuned for spacing.
- The emoji code points carry no visible relation within mirror pairs: the first code points of A and B
  differ by 119 distinct amounts over 128 pairs, and their sums and XORs show no repeat pattern.
- The coin sits at the exact image centre, (1023.5, 1023.5), radius 59.4 px, with 34 regular rim
  ticks (one due east) and an upright B. The thread's "34 divisions" is right; its "14 degree tilt"
  does not show on the coin. The spiral's symmetry centre is 5.9 px above the coin's centre. Apple's
  ink placement inside the glyph box explains only 0.6 px of that, and in the wrong direction, so
  the emojis were probably drawn as text from a baseline that sits slightly high. That is a rendering
  detail, not an obvious carrier, and the 34 ticks look like the stock coin art.
- The forum IDs behind the point `H` cannot be reproduced. The 9 emojis whose code points spell
  `H.x` decode as index up (dark), woman climbing (dark), raised fist (medium-light), running
  (medium), woman kneeling facing right (medium-light), grinning cat, frowning face, woman
  construction worker (dark) and man pilot (medium-dark). Matched to their positions, their IDs
  (91, 137, 11, 41, 43, 161, 171, 217, 177) follow none of: radius from the coin either way,
  a golden-angle spiral index either way, x order, y order. The IDs come from a forum member's
  private numbering, so the "s selects nine emojis" chain may be a pattern found after the
  fact; the author has not confirmed it.

## 1. Read the author's hints as one set

- **Cost**: minutes
- **What it is**: the author has posted a short list of hints over four months (quoted in
  `../clues/author-posts.md`): "inside-out", "ASCII 8 cat incident", "no loose ends, no
  hashing", "everything required to solve is in the first post", a skin-tone remark about the
  image, a meta-clue string, and a solution time of "4 milliseconds". Any hypothesis has to
  explain all of them, not one.
- **Why it ranks here**: it costs nothing, and the author states that the solution is short
  once seen. The author also says the solution needs no heavy compute.
- **What would confirm it**: a reading of the first post that produces a 64-hex candidate for
  which `python3 tools/oracle.py <candidate>` prints MATCH.
- **What would kill it**: nothing kills it as a whole. A single reading is killed when its
  candidate does not match.
- **Status**: open

## 2. Check the structure a forum user reported on 2026-07-29

- **Cost**: minutes to hours
- **What it is**: [NotATether's post](https://bitcointalk.org/index.php?topic=5584952.msg66990855#msg66990855)
  reports that the significant bytes of the signature's `s` value select nine emojis, that
  their Unicode bytes read "inside-out" give the hex string
  `031dffd7ff0d400f0afcc3fdcefc0d400f0da10f3a390f77ff0d400f68fe0d080f`, that a cat's
  eight-step path in the image reads as the ASCII digit 3, and that the image geometry points
  to an 80-bit interval discrete logarithm. The post itself states that the private key was
  not found.
- **Why it ranks here**: the poster published exact intermediate values, so each is cheap to
  reproduce. The reading is unverified here. The author wrote on 2026-07-29 that he does not
  know "where it was ever hinted anything about using Kangaroo", which argues against the
  interval-search reading.
- **What would confirm it**: reproducing the nine emoji selection and the hex string from the
  published signature and image alone, then finding that the result yields a key the oracle
  accepts.
- **What would kill it**: the hex string cannot be reproduced from the published material, or
  it is not the intermediate value of any key that leads to the escrow.
- **Status**: open

## 3. Ask the author a narrow question in the thread

- **Cost**: needs a person
- **What it is**: the author answers specific yes or no questions in the thread (2026-08-13,
  2026-09-07, 2026-09-15). A question that tests one reading costs the author one line.
- **Why it ranks here**: the answers have been the only source of new information since
  2026-07-29. It needs an account on the forum and it is bounded by the author's patience:
  on 2026-08-28 he asked readers to stop sending him direct messages and long essays about the puzzle.
- **What would confirm it**: an answer that fixes one element of the mechanism.
- **What would kill it**: no reply, or a reply that repeats an earlier hint.
- **Status**: open

## 4. Bounded interval search

- **Cost**: unknown, not started
- **What it is**: if a reading from lead 1 or 2 bounds the private key to an interval, the
  search is a discrete logarithm of the recovered public key
  `02425afdd1716149faf414b6fdb96d5e7afc8ce42496042f4df559c80a7c6650eb`.
- **Why it ranks here**: N and the rate D are not known, so t = N / D cannot be written down.
  Per the rules in `../../../AGENTS.md`, no compute is requested before N is known. The
  author's statements point away from this route.
- **What would confirm it**: a derived interval with a measured rate and t under two hours.
- **What would kill it**: no interval can be derived from the published material.
- **Status**: open
