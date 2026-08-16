# Leads (full notes)

The "Open leads, ranked" section of `README.md` shows the ranked list; this file carries
the full notes behind each entry.

## 1. Buy the physical 2020 to 2021 printed EN and IT books

- **Cost**: needs a person and about $40 (two used books).
- **What it is**: every digitally accessible surface of both editions (ebook text, page
  scans, figure images) has been checked against every mechanism I could construct
  (see `tested.md`), with 0 matches on the 3 open lots. The author writes, of his own
  book copies: "you hold the source of each and every key in your hands... as long as
  you have a physical copy, that is" (print-only front matter, not present in any ebook
  capture I have). Separately, the IT_veryhard lot's likely clue pages (47 and 70, per
  the footnote cross-references) are absent from every digital capture I hold of the IT
  edition. A used copy from the original print run is preferable to a fresh
  print-on-demand reprint: on the IT side, a planted flaw is known to have moved between
  printings, so a POD copy printed today is not guaranteed to carry the same text as the
  puzzle-era edition.
- **Why it ranks here**: it is the only lead grounded directly in the author's own words
  about how the puzzles work, and it is the one lead not yet executed.
- **What would confirm it**: a distinctive detail on a physical page (pages 47 and 70 for
  IT_veryhard, or an equivalent gap for the two EN lots) that has no ebook counterpart.
- **What would kill it**: the physical text matches the ebook capture exactly on the
  relevant pages, with no new detail.
- **Status**: open, not yet executed (a purchase decision, not a compute task).

## 2. Crack IT_easy using its exposed public key as a free calibration oracle

- **Cost**: hours.
- **What it is**: IT_easy (`1MEstvLAzc5DzJtvx7uyvKNNUCPN3ofWMK`) was solved and swept by
  a community reader in 2022-02-18, which proves its answer is recoverable from the text
  alone, with no print gate. Because it was spent from, its public key is exposed
  on-chain. Deriving the IT_easy answer, even without the prize (already claimed), would
  reveal the Italian-edition answer style most likely to solve IT_veryhard, the
  remaining IT lot.
- **Why it ranks here**: it is bounded (a single known-solvable lot) and cheap relative
  to lead 1, but it depends on finding the right IT-only textual detail, which the
  ebook-mapping work has not yet located for IT_easy specifically (as opposed to
  IT_hard, which is solved).
- **What would confirm it**: a sha256x3 candidate string whose derived uncompressed
  P2PKH address matches `1MEstvLAzc5DzJtvx7uyvKNNUCPN3ofWMK`, or whose derived public key
  matches the one exposed by the spending transaction.
- **What would kill it**: exhausting the Italian front matter and body text (already
  mapped once, see `tested.md`) without a match; that would suggest IT_easy's answer
  also depends on print-only content.
- **Status**: open.
