# Leads (full notes)

The "Open leads, ranked" section of the folder's `README.md` shows the ranked list; this file
carries the full notes behind each entry. Order leads by cost to test, then by expected
value.

Notation: T is the 69-byte coinbase text `The Times 03/Jan/2009 Chancellor on brink of second
bailout for banks`, J the 47-byte headline `Chancellor on brink of second bailout for banks`,
S the full 77-byte scriptSig, and G the set of genesis integers {nonce 2083236893, time
1231006505, bits 486604799, version 1, height 0, 2, 3, 2009, 50}, all under 2^31 and so valid
as hardened BIP32 indexes.

## 1. Bounded first pass over the coinbase text

- **Cost**: minutes (one CPU, no GPU needed)
- **What it is**: the literal readings of the two 2026-08-28 hints, enumerated. Four families:
  - A, raw private keys: every window of 1 to 32 bytes of T, J and S, read as a big-endian
    integer, as a little-endian integer, left-padded and right-padded to 32 bytes, with
    compressed and uncompressed public keys. About 15,000 distinct keys, 1.1e8 pairs, two
    key orders each, about 4 minutes at 1,200,000 pairs/s.
  - B, BIP32 root plus BIP48 path: seed in {T, J, S, T[:32], T[32:], J[:32], every 16 and
    32-byte window}, paths `m/48'/0'/a'/s'/0/i` with a in G, s in {0', 1', 2'}, i in {0, 1},
    plus `m`, `m/0`, `m/0/0`, `m/44'/0'/0'/0/0`, `m/84'/0'/0'/0/0`. About 60 seeds times 70
    paths, 4,000 keys, under a minute.
  - C, BIP39 entropy: windows of T, J and S of 16, 20, 24, 28 and 32 bytes as entropy, the
    resulting mnemonic with an empty passphrase and with T as passphrase, then the paths of
    B. About 35,000 keys, 6e8 pairs, about 10 minutes.
  - D, other fields: merkle root, block hash, public key and header, raw, byte-reversed and
    truncated, as raw keys, as seeds and as entropy, with accounts in G. About 500 keys,
    seconds.
  Pairs are also taken across families (A with B, B with C) while the total stays under 1e9
  hashes. Free filters: a raw key must lie in [1, n-1] (short windows right-padded overflow
  and are dropped); BIP39 entropy must be 16 to 32 bytes in steps of 4.
- **Why it ranks here**: cheapest possible test of what the author literally said. "Maybe
  both" to "32 bytes or smaller" fits one key on T[:32] (`The Times 03/Jan/2009 Chancellor`,
  exactly 32 bytes) and one on a shorter slice; "root -> multisig -> mainnet -> genesis_data
  -> script_type" is the BIP48 level order with a genesis value in the account slot.
- **What would confirm it**: a MATCH from `tools/oracle.py`.
- **What would kill it**: 0 match with the witness re-found at head, middle and tail of each
  family. That closes the literal readings and hands the problem to lead 2; it does not close
  the puzzle, since "root" may be built by a library step I have not modeled.
- **Status**: open

## 2. Ask the author one precise question on chain

- **Cost**: needs a person; about 5,000 to 10,000 sats plus fees; answer within hours (every
  paid question so far was answered in 1 to 10 hours)
- **What it is**: a transaction with one output to the escrow (or to the author's current
  change address, which the author then relays) and one OP_RETURN of at most 80 bytes with
  the question. Draft, 79 bytes:
  `Root = BIP32 seed from coinbase text directly? account = genesis nonce?`
  Shorter variant, 55 bytes: `Is root seeded by the 69-byte coinbase text, no BIP39?`
- **Why it ranks here**: the author sells hints and has answered every one; the two most
  useful hints cost 3,000 and 3,500 sats. One yes/no answer collapses families B and C to a
  few dozen candidates. It ranks second only because lead 1 is free and may make it moot.
- **What would confirm it**: any answer, checked against the oracle in seconds.
- **What would kill it**: the author stops answering (last answer 2026-08-28 23:50 UTC), or a
  spend of the escrow by someone else.
- **Status**: open

## 3. Watch the channel

- **Cost**: minutes
- **What it is**: before any work, re-read the escrow's transactions on an explorer. A new
  OP_RETURN spending the author's latest change output is a new constraint; a spend of the
  escrow ends the puzzle. The author's current change address is
  `bc1qktf2wdszlsg4fes6mlzjxkcnhp63wnhct6gkgh` (17,200 sats, unspent on 2026-08-29); it
  changes with every message, so follow the chain of inputs from the last author
  transaction rather than this fixed address.
- **Why it ranks here**: zero cost, and every hint so far reduced the space more than any
  computation could.
- **What would confirm it**: a new author message.
- **What would kill it**: a spend of the escrow.
- **Status**: open
