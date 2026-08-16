# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the
ranking. All 3 leads below are priced and specified; none has been run.

## 1. Extend the swept word pool with connecting words (liaisons)

Every completed sweep (`analysis/tested.md`) draws its non-anchor words from
full words in the 5 planted sentences and confirmed metadata (tags, title,
hook line). None of them include short connecting words from the same
sentences: prepositions, articles, and conjunctions such as "there", "will",
"also", "you", "more", "can", "then" (video side) or "only", "because",
"there", "like" (post side). These words are cheap to add: the private
research's own P2 estimate, before the metadata extension, priced this
addition at 15/14 words per side, 1.36x10^10 derivations, about 3.8 hours on
one GPU. Extending the already-metadata-inclusive R1 pool the same way is a
comparable-sized addition.

What would confirm it: a match within the extended set.
What would kill it: exhausting the extended set with 0 match, the same witness
protocol as every prior sweep.
Cost: hours on one rented GPU.

## 2. Extend further to substrings of longer words

The author, asked directly whether a list word could be hidden inside a
longer written word, answered yes and gave "possible" inside its own
negation, formed with the prefix "im-", as his own example, though the
surrounding conversation suggests he may have
meant the paraphrase-hint mechanism rather than a substring mechanism (see
README, "What is understood"). This is confirmed as an open question, not a
confirmed mechanism. If it is real, plausible substrings already identified in
the source texts include "cat" (cattle), "ill" (will), "hen" (then), "like"
(likely), "cause" and "use" (because), "health" (healthy), "hunt" (hunter),
and "inner" (dinner). The private research's own P3 estimate for a
substring-inclusive sweep, before the metadata extension, was 21/20 words per
side, 2.78x10^11 derivations, about 77 hours on one GPU (later re-priced
downward once a faster kernel was validated at 792,000 derivations/second).

What would confirm it: a match within the substring-extended set.
What would kill it: exhausting it with 0 match.
Cost: on the order of a day on one rented GPU at the validated 792,000
derivations/second rate; re-price before running, since kernel throughput
changes this estimate directly.

## 3. Read the video and post one more time for a metadata-style hidden word

If leads 1 and 2 both return negative, the most likely remaining explanation
is that one word lives in a part of the source material not yet identified as
a metadata surface, the same way the blog post's tags were missed until
2026-08-15. The video's own metadata (its tags, description formatting, or
on-screen text) and the post's remaining unread surfaces (any HTML attribute
resembling `article:tag`, image alt text) have not been re-examined with the
same "check every metadata field" method that found `fork` in the post's tags.

What would confirm it: a new word found in an unexamined metadata field,
tested through `tools/oracle.py` after being combined with the already-mapped
words.
What would kill it: a full metadata re-read producing nothing new; there is no
natural exhaustion point for this lead beyond a careful, complete pass.
Cost: an hour of directed reading, not a sweep.
