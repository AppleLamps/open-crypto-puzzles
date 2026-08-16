# Tested: Objective Thune, "Le secret de la Licorne"

Full negatives ledger. The README shows the summary.

## 1. Full-text search of the book

I searched the complete text of the book (133,416 characters, obtained for research
purposes, not reproduced here per the copyright note in the README) for the escrow
address, "licorne," "multisig," "0.18," "cle privee," "trois cles," and "exemplaire n."
Method: plain-text search of the extracted book text. Result: 0 occurrences anywhere in
the narrative. The mechanism lives only in the publisher's external posts, never in the
book itself; the author even winks at this directly, writing of a fortune-telling
character, "Devinerait-elle les cles privees? Nous ne le saurons jamais" ("Would she
guess the private keys? We will never know"). Date: 2026-08-03.

## 2. Cover hex bands

The hexadecimal-looking decoration on the collector cover decodes to the Bitcoin genesis
block hash, `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`, repeated.
Method: direct visual decode of the cover image. Result: a public constant, not a secret.
Closed. Date: 2026-08-03.

## 3. The drawn "private key" on page 10

A comic-book panel shows a character asking about "the private key of this wallet,"
drawn as a 52-character string starting `Kz`, the shape of a compressed WIF private key.
I transcribed it and tested every variant within edit distance 2 across all 52 positions
and 58 base58 symbols: 4,308,174 candidates, checked for a valid WIF checksum, in 11
seconds. Witness: a known-good WIF is accepted by the same checker, and the same WIF
with 1 character changed is correctly rejected, so the checker is not silently accepting
everything. Result: 0 valid checksums. This is a fictional prop, not a real key. Closed.
Date: 2026-08-03.

## 4. Bibliographic and marketplace search

I queried the Bibliotheque nationale de France (BnF, SRU protocol), OpenLibrary,
Delcampe, tintinomania.com, WorldCat, SUDOC, bedetheque.com, Vinted, eBay, Rakuten,
Leboncoin, and Catawiki for the book. Method: direct query or search, with a witness
query proven to succeed first. Result: the BnF query is legitimately empty (0 records),
not a search failure: the publisher is Swiss, so French legal deposit does not apply;
the Bibliotheque nationale suisse (Helveticat) does hold 1 catalogued copy, not confirmed
as one of the 3 marked copies. OpenLibrary, Delcampe, and tintinomania.com are
legitimately empty (witness queries succeeded). WorldCat, SUDOC, bedetheque.com, Vinted,
eBay, Rakuten, Leboncoin, and Catawiki returned no usable data (client-side rendering or
anti-bot blocks even on witness queries), so their result is unconfirmed, not negative.
1 standard (non-numbered) copy was found for sale on AbeBooks. Date: 2026-08-03.

## 5. Funding-transaction trace

I traced both funding transactions 2 hops back on-chain. Method: follow input addresses.
Result: every source and change address is single-use, no `OP_RETURN`, no exchange tag
identified. Diminishing returns; not pursued further. Date: 2026-08-03.

## 6. Publisher payout track record

I checked a different contest run by the same publisher on the same domain ("Utopie
p2p," announced on bitcoin.fr 2023-01-20, address
`bc1qnqpfydv9amqewthfjmskh03t2aunafv2wvpmm6`). Method: on-chain balance check. Result:
fully spent (funded = spent = 6,694,793 sats), confirmed again 2026-08-16. This shows
the publisher does pay real winners, and that the Licorne escrow staying intact for 6.5
years is not a bookkeeping artifact.

## 7. IPFS-hosted halving content

The publisher cites a video and text pinned to IPFS at launch
(`QmanqrvZMQnosDQJYD1evPSzkjdZxffYf1sJx7W3SnLfJW` and
`QmNX3FCBUuEBokY1QZNujNgpubV8umw2RuBY3X2cTwGbRC`). Method: fetch via `ipfs.io` and
`cloudflare-ipfs.com` gateways. Result: unreachable ("no providers found") on both
gateways, consistent with 6 years unpinned. Unverified, not confirmed empty or full.
Date: 2026-08-03.
