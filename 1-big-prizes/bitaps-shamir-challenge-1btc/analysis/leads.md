# Open leads: Bitaps Shamir secret-sharing challenge

Full notes. The README shows the ranked summary.

## 1. The 15-day archive gap (2020-06-19 to 2020-07-04)

The earliest archived capture of the challenge page I found is dated 2020-07-04, 15 days
after the address was funded and the 2 shares were published. Neither the Wayback Machine
CDX index nor Common Crawl has anything from this window for `bitaps.com/mnemonic/challenge`
or its regional mirrors. If a 3rd share, or a clarifying comment, was ever posted and then
edited out, this is the only window where it could have existed and gone uncaptured.
What would confirm it: any archiver, forum mirror, or dated screenshot from this specific
window showing a different page state. What would close it: a systematic search of
smaller/regional archivers and search-engine caches turning up nothing across the same
window, the way the 14-capture, 4-year search already did for the rest of the timeline.
Cost: an afternoon of searching alternative archivers; no compute.

## 2. Uncertified channels

archive.today returned HTTP 429 on its own known-good witness page when I tried it
(2026-08-03), so I could not tell whether it holds anything for this challenge; Memento
TimeTravel was unreachable the same session; I found no verified anonymous read route for
X replies to `@bitaps_com`; the GitHub forks of `mnemonic-offline-tool` (13 as of
2026-08-03) have not been individually reviewed for a diverged share; and Telegram's
`t.me/s/bitapscom` public preview has not been read. None of these are established as
empty, only as not yet checked with a working method. What would confirm or kill each:
a working read of the channel that either surfaces a 3rd share or comes back clean with a
witness proving the read method works. Cost: minutes to hours per channel, no compute.

## 3. Direct computation

Not ranked as a lead. The residual entropy is about 125 bits (see
`data/entropy_measurements.csv`), which is not in range for search on any hardware I have
access to. This door is closed by the numbers, not by assumption.
