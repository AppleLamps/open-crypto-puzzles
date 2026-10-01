# Negatives ledger: Phy Challenge

Every row names its count, method, witness, rate and date. No key search has been run on this
puzzle: 0 candidate private keys tested. The rows below are checks of the setup, so that the
next person does not repeat them.

Oracle: `tools/oracle.py`. Witness for all rows: `tools/oracle.py --selftest` prints
`SELFTEST OK`, which includes the public BIP-173 vector (private key 1 gives
`bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4`) and the recovery of the escrow address from the
author's own signature.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| The signed message is exactly the first code block of the first post, LF line endings, no trailing newline (959 bytes) | 1 reading | BIP-137 public key recovery with `tools/oracle.py --recover`, compare the hash160 address to the escrow | 1 match: recovers `bc1qrpn28qa82uyjg37dvsz3w7wpm3kpdea957nm9p` | yes: same code reproduces the BIP-173 vector | about 55 recoveries/s, pure Python on one CPU core | 2026-10-01 |
| Whitespace variants of the signed message: trailing LF added, CRLF line endings, CRLF with a trailing CRLF | 3 readings | same recovery | 0 match. They recover `bc1qpmpy8zy2reer2ext9cffwr6tdhwlm937dtwfvh`, `bc1qvjvyugkw3xwjnqeu5cld32xlss9kjvyd7csm98` and `bc1q3tazetwnw22jxmew9ptj34tyn6x53zg4a7qadr`, none of which is the escrow | yes: the exact reading in row 1 is re-found by the same code | about 55 recoveries/s, pure Python on one CPU core | 2026-10-01 |
| The funded address has spent an output and so revealed a signature on chain | 1 address | `curl https://mempool.space/api/address/<escrow>`, read `spent_txo_sum` and `tx_count` | `spent_txo_sum` 0, `tx_count` 1: no signature from this key is on chain | uncertified (one API read, not oracle-run) | not applicable | 2026-10-01 |
