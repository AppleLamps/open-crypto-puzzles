# Open leads: Hunting Time

## 1. Certify the Electrum derivation branch (minutes to hours)

The author's own words name the wallet type: "a fresh electrum wallet." The BIP39-to-BIP84
branch in the oracle is certified against a public test vector, but Electrum's segwit seed
derivation has no known-good seed-and-address pair embedded to prove the code accepts a correct
answer. Without that, any "no match" result on the Electrum branch is uncertified, not a real
negative. A documented Electrum-generated seed and its resulting receiving address, taken from
Electrum's own software or documentation, would settle this before any further search is worth
running.

## 2. Re-run the numeric-index hypothesis after cleaning the candidate pools (minutes)

9 of the 12 clue images carry a visible number; if those numbers are BIP39 wordlist indices,
only the 3 unnumbered images (clues 2, 5, and 10) leave free positions. The previous attempt
crashed on a non-BIP39 word ("pay") in one candidate pool before testing anything. Purging the
pools of non-wordlist words and re-running would cover a space of a few million combinations in
well under an hour.

## 3. Recover the book's cover image (needs a person, minutes)

The opening post states the cover carries a code from the Bitcoin Genesis Block and hints at a
second hidden code, but no cover image has been brought into this research. Obtaining a
high-resolution copy of the cover (purchase or library access to the novel) is a cheap, direct
way to check whether it contributes a 13th data point or resolves ordering among the 12 clue
words.
