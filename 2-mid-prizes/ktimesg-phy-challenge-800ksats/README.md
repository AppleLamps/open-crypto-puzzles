# kTimesG: Phy Challenge (800,000 sats, [OPEN])

kTimesG posted the Phy Challenge on bitcointalk on 2026-06-05: a base64 signed message, a
block of prose it signs, and a 2048x2048 grayscale emoji spiral with one colour Bitcoin emoji
at its centre. The author closes the post with "no loose ends, no hashing". The signature
recovers a native SegWit address that has held 800,000 sats, unspent, since 2026-06-21, and
the author confirmed on 2026-08-13 that this is the target. I confirmed the escrow state and
the link from signature to address. I tested no candidate key. The mechanism that turns the
post into a private key is not published, and no solver has claimed the funds as of
2026-09-24.

## At a glance

| | |
|---|---|
| Author | kTimesG, [bitcointalk](https://bitcointalk.org/index.php?action=profile;u=3610370) |
| Published | 2026-06-05, bitcointalk, Bitcoin Discussion board ([thread](https://bitcointalk.org/index.php?topic=5584952.0)) |
| Prize | 800,000 sats (about $504 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `bc1qrpn28qa82uyjg37dvsz3w7wpm3kpdea957nm9p` ([explorer](https://mempool.space/address/bc1qrpn28qa82uyjg37dvsz3w7wpm3kpdea957nm9p)) |
| Last on-chain check | 2026-10-01: funded and unspent, 800,000 sats, 1 transaction |
| Status | OPEN |
| Puzzle type | raw-private-key, image-stego, pixel-code (my classification; the mechanism is not confirmed) |
| Target format | one secp256k1 private key as 64 hex characters, compressed public key, P2WPKH address |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the BIP-173 vector and the recovery of the escrow from the author's own signature) |
| What remains | the whole mechanism: how the signature and the image give a private key |
| Series | none |

## The puzzle as published

The [first post](https://bitcointalk.org/index.php?topic=5584952.msg66802369#msg66802369)
(2026-06-05) has three parts, all saved in `clues/`:

1. A code block of 959 bytes, saved byte for byte in `clues/first-post-message.txt`. It opens
   with a rewritten version of the Bitcoin whitepaper abstract, then a line of equals signs,
   then a dated line and the sentence "here's a puzzle for everyone, no loose ends, no
   hashing."
2. A second code block holding a base64 string of 87 characters, saved in
   `clues/signature.txt`. The author edited it on 2026-07-29 to restore its first character,
   "J", which had been lost when the post was written.
3. One image, 2048x2048 pixels, saved unmodified in `clues/spiral.png`.

![The author's spiral image: grayscale emoji on a black background, arranged in a spiral, with one colour Bitcoin emoji at the centre](clues/spiral.png)

*Source: the author's first post, image hosted at
[talkimg.com](https://www.talkimg.com/images/2026/06/05/UrS0Mq.png), fetched 2026-10-01.*

The author added these statements in the thread. The full list with links is in
`clues/author-posts.md`.

- 2026-06-21: "there is a prize (as of today)", and a PGP message with the line "the
  password's already mentioned".
- 2026-07-23: "the hints are already inside-out", and a reference to "the ASCII 8 cat incident".
- 2026-08-13: "the signature verifies", in answer to a reader who doubted the address.
- 2026-08-28: "everything required to solve is in the first post".
- 2026-09-05: a meta-clue, `gvonys fhelucrM kbZ`.
- 2026-09-15: "The smart approach can find the correct solution in 4 milliseconds."

## What is understood

### Mechanism

Not established. The published material fixes the target: a private key whose public key is
the one recovered from the signature. How the prose, the signature bytes and the image
combine to give that key has not been published by the author or reproduced by me. A forum
user posted a reading on 2026-07-29 (see `analysis/leads.md`, lead 2); I did not reproduce it.

### Derivation and oracle

The target is fixed by the recovered public key
`02425afdd1716149faf414b6fdb96d5e7afc8ce42496042f4df559c80a7c6650eb`. A candidate is a 64-hex
private key. The oracle derives the compressed public key, hashes it, encodes a bech32 P2WPKH
address and compares it to the escrow. Only an exact address match counts.

```bash
python3 tools/oracle.py --selftest      # must print SELFTEST OK
python3 tools/oracle.py --recover       # rebuild the public key and address from the signature
python3 tools/oracle.py <64-hex key>    # candidate check, prints MATCH or NO MATCH
```

On a MATCH, stop, broadcast nothing, and hand the key to the human running you. See
[AGENTS.md](../../AGENTS.md).

### Certified against

1. The public BIP-173 vector: private key 1 has the compressed public key
   `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798` and the address
   `bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4`. The candidate matcher itself re-finds
   private key 1 against that address (the target is injected in the self-test), and a
   matcher that always returns false fails the self-test.
2. The author's own data: the published signature over the saved 959-byte message recovers
   `bc1qrpn28qa82uyjg37dvsz3w7wpm3kpdea957nm9p`. A message with one byte added recovers a
   different address, so the check can fail. The recovery accepts only BIP-137 header bytes
   39 to 42, which is the published signature type (compressed key, native SegWit), and the
   self-test refuses headers 27, 31, 35, 38 and 43.

### Established facts

1. The escrow `bc1qrpn28qa82uyjg37dvsz3w7wpm3kpdea957nm9p` holds 800,000 sats, unspent, in one
   transaction. Re-check: `curl -s https://mempool.space/api/address/bc1qrpn28qa82uyjg37dvsz3w7wpm3kpdea957nm9p`
   gives `funded_txo_sum` 800000, `spent_txo_sum` 0, `tx_count` 1. Checked 2026-10-01.
2. The funding transaction is
   [`2ba79d0b377ab2c41f3508e91e84d0b2aff771fd81b97b8e85c24788795964d3`](https://mempool.space/tx/2ba79d0b377ab2c41f3508e91e84d0b2aff771fd81b97b8e85c24788795964d3),
   confirmed in block 954728 at 2026-06-21 18:08:38 UTC. It pays 800,000 sats to the escrow and
   995,689 sats of change to `bc1qch9jj9rvdwnxwpvy9vjdv3alm69mqvp3j7vzqv` (input from
   `bc1qtu43kaxwtnzqcwmeg4jzrptyhg9j29c2yxtnqj`). Checked 2026-10-01.
3. The published signature over `clues/first-post-message.txt` recovers the escrow address.
   Re-check: `python3 tools/oracle.py --recover`. Checked 2026-10-01.
4. Three whitespace variants of the message (a trailing LF, CRLF line endings, CRLF with a
   trailing CRLF) each recover a different address. Of the four readings tested, only the
   959 bytes with LF line endings and no trailing newline recovers the escrow. Checked
   2026-10-01.
5. The signature is 65 bytes with header byte 39 (the BIP-137 value for a compressed key
   with a native SegWit address). Its `r` is 255 bits and its `s` is 71 bits,
   `0x5b890b292ba1abd9b1`. A signature from a random nonce has an `s` near 256 bits, so the
   small `s` is a property of how the author built this signature. Why it is small is not
   established. Re-check: decode `clues/signature.txt` from base64. Checked 2026-10-01.
6. The escrow address has never spent an output, so it has exposed no spending signature on
   chain. The same public key has 0 transactions as P2PKH (compressed and uncompressed) and
   as P2SH-P2WPKH (`python3 tools/oracle.py --scripts` prints the addresses). Multisig,
   taproot and bare-key uses of this key were not checked. Checked 2026-10-01.
7. The author said on 2026-08-13 that the signature verifies and the address is the target.
   Source: the thread, post linked in `clues/author-posts.md`. Reported by the author.
8. The thread has 94 posts, the last on 2026-09-24, and no post claims a solution. Read in
   full on 2026-10-01.

## What has been tested

No key search has been run: 0 candidate private keys tested. The three checks below are
checks of the setup. Full ledger in `analysis/tested.md`.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| The signed message is the first code block, LF endings, no trailing newline | 1 reading | BIP-137 recovery, compare address | 1 match: the escrow | yes: BIP-173 vector re-found by the same code | 2026-10-01 |
| Whitespace variants of that message | 3 readings | same recovery | 0 match | yes: exact reading re-found by the same code | 2026-10-01 |
| The escrow key has signed an on-chain input under another single-key script form | 4 addresses | `--scripts` plus mempool.space address stats | 0 transactions on the 3 other forms, 0 spent outputs on the escrow; multisig, taproot and bare-key uses not checked | yes: derivation reproduces key 1's P2PKH vectors; its P2SH-P2WPKH address has 38 transactions | 2026-10-01 |

## Open leads, ranked

1. **Read the author's hints as one set** (minutes). The author's posts in
   `clues/author-posts.md` carry the hints. A reading has to explain all of them. Confirm: a
   64-hex candidate that the oracle accepts.
2. **Check the structure a forum user reported on 2026-07-29** (hours). The post gives exact
   intermediate values, so each can be reproduced or refuted. The author's reply that day
   does not endorse an interval-search reading. Kill: the values cannot be reproduced from
   the published material.
3. **Ask the author a narrow question in the thread** (needs a person). He has answered
   single questions on 2026-08-13, 2026-09-07 and 2026-09-15.
4. **Bounded interval search** (not started). N and the rate are not known, so no run is
   sized. Start only after a reading bounds the key.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/first-post-message.txt` | the signed message: the first code block of the first post, 959 bytes, byte for byte |
| `clues/signature.txt` | the base64 signature from the first post, with the 2026-07-29 correction |
| `clues/spiral.png` | the author's image from the first post, unmodified, SHA-256 `baf3ed80ffd8d2a1c17cdc8e212910abffdda4ede0b5900d542f587ef346cdc9` |
| `clues/author-posts.md` | the author's short statements in the thread, with dates and links |
| `analysis/tested.md` | the negatives ledger |
| `analysis/leads.md` | the full lead notes |
| `tools/oracle.py` | recovery check and candidate checker, standard library only |

## Sources

- kTimesG, Phy Challenge, bitcointalk, 2026-06-05 to 2026-09-24 (read 2026-10-01): https://bitcointalk.org/index.php?topic=5584952.0 (archived: none found)
- kTimesG, bitcointalk profile (read 2026-10-01): https://bitcointalk.org/index.php?action=profile;u=3610370
- Funding transaction, mempool.space (read 2026-10-01): https://mempool.space/tx/2ba79d0b377ab2c41f3508e91e84d0b2aff771fd81b97b8e85c24788795964d3
- Author's puzzle image, talkimg.com, 2026-06-05 (fetched 2026-10-01): https://www.talkimg.com/images/2026/06/05/UrS0Mq.png
- BIP-137, signing messages with a P2WPKH key: https://github.com/bitcoin/bips/blob/master/bip-0137.mediawiki
- BIP-173, bech32 addresses and test vectors: https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
