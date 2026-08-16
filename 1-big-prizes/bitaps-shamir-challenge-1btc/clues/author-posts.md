# Author posts: Bitaps Shamir secret-sharing challenge

Verbatim short posts published by Bitaps (bitaps.com), the company running the challenge.
Chronological.

---

**2020-06-19, challenge page**, `bitaps.com/mnemonic/challenge`
(live page returns HTTP 403 as of 2026-08-16; archived copy:
[web.archive.org, 2023-03-28](https://web.archive.org/web/20230328022959/https://bitaps.com/mnemonic/challenge)):

> "The New Bug Bounty program for Shamir Secret Backup Scheme... if you can hack the scheme
> completely, then the main reward is already waiting for you at the bitcoin address."

> "The goal is to break the Shamir Secret Sharing scheme or break the implementation of
> software for SSSS. We publish 2 of 3 shares needed to restore."

The two published shares (12 words each, Shamir index embedded in the last 4 bits in place
of the BIP39 checksum):

```
session cigar grape merry useful churn fatal thought very any arm unaware
clock fresh security field caution effort gorilla speed plastic common tomato echo
```

**2020-06-19, announcement**: [x.com/bitaps_com/status/1274018817304379394](https://x.com/bitaps_com/status/1274018817304379394)
(not independently re-read today; X blocks automated reads without a session, see
[Sources](../README.md#sources)).

**2020-06-19, code of record**: [github.com/bitaps-com/mnemonic-offline-tool](https://github.com/bitaps-com/mnemonic-offline-tool),
commit [`5b6dd995`](https://github.com/bitaps-com/mnemonic-offline-tool/commit/5b6dd995478b49c489b95444fbb0dca4006746a2)
(2020-06-19T09:46:32Z, the same day the challenge address was funded), bundling the
`jsbtc` library that generated the two published shares.
