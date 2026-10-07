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
