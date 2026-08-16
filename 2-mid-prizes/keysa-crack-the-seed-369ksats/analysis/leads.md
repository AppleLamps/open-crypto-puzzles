# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Write to the author

Keysa is active (her most recent Nostr event at the time of my last check was
2026-08-01) and has twice invited exactly this kind of contact in her own posts:
"I would love to know if this method is solid" and "Open to comments." Her stated
interest is in an audit of her method, not in protecting a secret. This is a near
zero cost action with the highest plausible payoff, since the selection rule is, by
her own description, short, memorable, and meant to be spoken aloud to a trusted
person, which is exactly the kind of fact that a mechanical sweep cannot recover but
a direct question can.

What would confirm it: a reply describing the selection rule, or enough of it to
narrow the remaining candidates to something `tools/oracle.py` can check directly.
What would kill it: no reply, or a reply that does not narrow anything (she has
stated before that she does not want to spoil the puzzle for others).
Cost: needs a person; no compute cost.

## 2. Submit argued candidate 12-word orderings (the "order, not selection" reading)

Under the original announcement, a reader frames the puzzle's difficulty in terms of
knowing the 12 words but not their order ("620 quintillion guesses even if they knew
the exact 24 words, but not the correct order"). Keysa's own reply engages with
counting permutations for a 12-word case rather than correcting the framing to
"you would first need to know which 12 words." Read together with her stated design
goal (a rule short enough to say out loud), this suggests her own mental model may
treat the selection as easier to work out than the order.

The practical consequence: for any well-argued candidate set of 12 tokens, checking
every one of its 12! = 479,001,600 orderings costs about 38 seconds on a rented GPU
(measured at about 0.79 million derivations per second), against 36.8 minutes on a
CPU for the one set already tried in full (L-001, `analysis/tested.md`). The
bottleneck for this lead is producing a well-reasoned candidate set of 12 tokens,
not the permutation search itself.

What would confirm it: any 12-token candidate set whose full 12! ordering sweep,
run through `tools/oracle.py --stdin`, returns a MATCH.
What would kill it: exhausting every argued candidate set without a match; this
lead does not have a natural end state the way a bounded space does, since new
candidate sets can always be proposed.
Cost: minutes per candidate set on a rented GPU; the cost driver is generating
candidates, not derivation.

## 3. The "two tokens per row" bounded sweep

The 6 rows are confirmed to be typed line breaks rather than a display artifact
(see the row-structure measurement in `analysis/tested.md`), which makes any rule
defined per row a legitimate candidate family. One specific rule not yet fully
covered by the positional sweep in L-002 is: pick exactly 2 of the tokens from each
row, in some order, giving 12 tokens total. The space is C(12,2)^4 times C(11,2)^2,
about 5.7e10 raw combinations of token pairs (rows of 12 tokens each contribute 66
ways to choose 2, rows of 11 contribute 55), narrowing to about 3.6e9 after the
BIP39 checksum filter (1 in 16). At the measured rate of about 790,000 derivations
per second on one GPU, checking the checksum-valid subset costs about 76 minutes.

What would confirm it: a MATCH from `tools/oracle.py` on any candidate drawn from
this space.
What would kill it: running the full checksum-filtered space to completion with 0
matches, with a witness planted at the head, middle, and tail of the search order.
Cost: about 76 minutes on one rented GPU; this is the best remaining
information-to-cost ratio once leads 1 and 2 are exhausted.

## 4. The double-width gap after "mad", and the "369 clock" theme

Two weaker, unresolved observations, neither of which is itself an actionable next
step:

- The gap after the first token, `mad`, measures about 20 pixels, against 9 to 13
  pixels for every other inter-word gap on the card (`analysis/tested.md`). This is
  the only typographic anomaly on the card. It may mark a deliberate starting point,
  or it may be an unrelated formatting choice; I have not derived a selection rule
  from it to test.
- Keysa's own book anchors the 369 theme in a real, author-owned passage (pages 126
  to 127, "Satoshi's Numbers: 369 Clock"), which rules out the amount being purely
  decorative, but no digital-root or modulo-9 based selector derived from this theme
  has produced a match (L-004, L-005 in `analysis/tested.md`).

What would confirm either: a specific selection rule derived from one of these
observations that `tools/oracle.py` confirms.
What would kill either: this is not a bounded space to exhaust; both stay open until
a rule is proposed and tested, or until new information (most likely from lead 1)
explains them.
Cost: needs a new insight; no compute action is available on either today.
