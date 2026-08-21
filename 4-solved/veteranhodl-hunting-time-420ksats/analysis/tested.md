# Negatives ledger: Hunting Time

Both entries below are marked uncertified: neither run planted a synthetic known-good candidate
to prove the search apparatus would have found a correct answer, so a "no hits" or "crashed"
result is INVALID as a proven negative under this repository's own convention, not a confirmed
absence.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Semantic candidate pool built from reading all 12 clue images (4 to 7 candidate BIP39 words per position), combinatorial sweep, BIP39 checksum filter then address comparison | 393,750,000 total combinations | 120 tasks across 8 processes | stopped at about 20 percent completion (19.0 minutes): 4,924,764 phrases passed the BIP39 checksum filter; the run log does not show these being compared against the target address | none: no synthetic witness was planted in this run | 2026-08-15 |
| Visible numbers on the clue images read as BIP39 wordlist indices (1 to 2048) | 22,118,400 combinations planned across 108 tasks | direct index lookup | run crashed with a KeyError on the word "pay," which is not a valid BIP39 word and was present in one candidate pool; the hypothesis was never actually tested to completion | uncertified: crashed before any address comparison | 2026-08-15 |

Both rows need to be redone: the first needs to be completed and its checksum-valid output
actually compared against the escrow address; the second needs the candidate pools purged of
non-BIP39 words before it can run at all.
