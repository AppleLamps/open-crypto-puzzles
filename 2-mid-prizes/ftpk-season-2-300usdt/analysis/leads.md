# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

I harvested the author's public X timeline covering the Season 2 clue window
(2025-05-19 launch through the author's own "last clue from me" on 2025-06-15,
plus the remaining promotional posts that month). The live game pages themselves
are a separate problem: on 2025-06-05 the author posted a screenshot of the
hosting dashboard's "Enable Attack Challenge Mode" button and said they were
turning it on because dictionary probing of page names was running up the
request bill. As of 2026-08-27, `findtheprivatekeys2.vercel.app` and the Season 4
hidden page both return a Vercel Security Checkpoint (HTTP 429/403) to a
datacenter fetch, and a headed browser session on the same host failed the
checkpoint with "Failed to verify your browser - Code 11". The hub at
`findtheprivatekeys.vercel.app` still returns 200. Wayback has only the Season 2
landing page (2025-05-19), not `home.html` or any hashed game URL. A residential
browser that Vercel will admit is still the way to read the twelve games; the X
posts are the part I can work with offline.

I am not treating any of the images below as a BIP39 word. Several of them
thematically neighbour words on the English list, and that is exactly the kind
of near-miss this catalogue refuses to print as a claim.

## 1. Read the twelve game pages from a residential browser

The derivation is certified and the page-naming scheme is already broken. What
is missing is the games themselves. The author's 2025-06-05 posts show why a
scripted fetch is no longer enough: Attack Challenge Mode was enabled on
purpose. A headed browser on this host also failed, with checkpoint Code 11, so
the bar is a client Vercel treats as a person on a normal ISP, not merely
"JavaScript on". The hub page still loads, Season 1 still loads, and the hashed
Season 2 URLs were HTTP 200 when I mapped them in 2026-07, so the content is
still hosted.

What would confirm it: a mirror of all 12 game pages (plus the word-order helper)
from a session that passed the checkpoint, with every visible string, corner
number, image URL, and audio URL transcribed.
What would kill it: an on-chain sweep, or the author taking the season down.
Cost: a residential browser that Vercel will admit; no compute.

Known hashed URLs, in the order the 11 listed-game preimages spell, with game 12
named by the whole sentence. Each path is
`https://findtheprivatekeys2.vercel.app/<hex>.html`.

| Game | Page-name preimage | sha256 |
|---|---|---|
| 1 | the | `b9776d7ddf459c9ad5b0e1d6ac61e27befb5e99fd62446677600d7cacef544d0` |
| 2 | last | `3547cb112ac4489af2310c0626cdba6f3097a2ad5a3b42ddd3b59c76c7a079a3` |
| 3 | game | `6ca5cab77e702c787b4c14b3d3bf26bad43da606be6eed04ab0b9720120ae081` |
| 4 | has | `9150c74c5f92d51a92857f4b9678105ba5a676d308339a353b20bd38cd669ce7` |
| 5 | for | `10c22bcf4c768b515be4e94bcafc71bf3e8fb5f70b2584bcc8c7533217f2e7f9` |
| 6 | url | `28e5ebabd9d8f6e237df63da2b503785093f0229241bc7021198f63c43b93269` |
| 7 | this | `1eb79602411ef02cf6fe117897015fff89f80face4eccd50425c45149b148408` |
| 8 | sentence | `821119d79af8b9fcf86d782863d55861708cc4040673f905f9e3b616cfb71199` |
| 9 | that | `8e7fc0236af43df9340685fc16f1efe36543cc1707051220a103ad99cf69a2df` |
| 10 | is | `fa51fd49abf67705d6a35d18218c115ff5633aec1f9ebfdc9d5d4956416f57f6` |
| 11 | hashed | `1a06df824ed741b53c785079a6347f00eec5af82f9850775409ca69dff4068a6` |
| 12 | the last game has for url this sentence that is hashed | `2d80326b034b1aa616625ecb0febf8e9f58b125c5c43bc65f5d8ab6bd6cc1d36` |

Extra hosted paths transcribed by @N4Khjir from the live site in May 2025, still
behind the same checkpoint. These are not `sha256` hex names.

| Path | What N4 reported | Tweet |
|---|---|---|
| `/image1.psd` | Photoshop file linked from Game 1 | https://x.com/N4Khjir/status/1927619197695082629 |
| `/gdjztvzuojmmsmuwrsudjhzdvvlkftfehnxxkbpilscjfljyyg.html` | second extra Game 1 page | https://x.com/N4Khjir/status/1927619197695082629 |
| `/hdvpvgyqxzplxefvngacfsdsljxajfhtweksvlkihugghszomf.html` | Game 6 page titled "Simplicity Must Be Rewarded I" | https://x.com/N4Khjir/status/1929061582220276150 |

Wayback has none of these three. A browser PSD editor is the reading the author
gave for at least one image file (lead 3).

## 2. Cross-reference the Season 4 hidden page

Still the author's own stated S2 hint map, including the line that game 7 is the
weakest and the best candidate to leave unconstrained. The page is named by the
md5 of Season 4's 12 answer words concatenated, and the live URL is in this
folder's sources. It is behind the same Vercel checkpoint as Season 2 as of
2026-08-27. The author announced the page on 2026-07-22
(https://x.com/FTPKgame/status/2079947035357102350) and said it is hidden "in a
way that's a bit similar to Game 12 from Season 2."

What would confirm it: the page text, quoted, tying specific S4 clues to
specific S2 games, then a 12-word candidate matching the escrow.
What would kill it: reading the page and finding it does not name any S2 word.
Cost: same browser session as lead 1.

## 3. Game 12 as notes-to-digits, not song identification

Already the second README lead; the X posts add two facts. On 2025-05-27 the
author posted "Screenshot of game 12" showing the Google Drive placeholder
"Click here to view the file", then replied to themselves "F12 of course". On
2025-06-03 they said someone had found an email address on that Drive link, that
the address is useless, and that they would not open the attachments. Season 1's
hidden `kplo.html` page ("M Prez can help you") is the grammar: keypad digits
play fixed notes (1=D4 293.66 Hz through 0=C4 261.63 Hz) and the instruction is
to visit `https://findtheprivatekey.vercel.app/(the number).html`. A spectrogram
of the S2 track as an image was already refuted (`analysis/tested.md`); the
remaining reading is note names or MIDI numbers to a digit string, then that
string as a BIP39 word or as a page name.

@thedragon8383 asked for a hint "through the Jungle" under the author's one-word
post "photopea"
(https://x.com/FTPKgame/status/1926763058266767552,
https://x.com/thedragon8383/status/1926814830620459249). Two days later the same
player identified "the Jungle" as Game 12's sound, with the game found and the
audio unread (https://x.com/thedragon8383/status/1927546235486871920). Photopea
is the browser editor for the Game 1 `.psd`; the Jungle is the Game 12 track.

What would confirm it: a digit string that is a BIP39 word or that names a page
whose body is the word, then the full 12-word mnemonic matching the escrow.
What would kill it: exhausting the note-to-digit maps against the oracle once
the other 11 words are held.
Cost: hours, once the audio file is downloaded through a browser session.

## 4. The cities cluster

Three posts in one week, none of them a picture:

- 2025-06-05: "In the entire game, there are 10 hidden cities (of course, this
  only applies to certain games)"
- 2025-06-10: "If I were a city I would be ?"
- 2025-06-12: "4 cities 1 word"

This is the largest explicit constraint the author published: ten city names
hidden across a subset of the twelve games, and one of the twelve words is
fixed by a set of four cities. It does not say the word is a city name. It
does not name the four cities.

One city is already sitting in a player transcription. Game 11's French poem
(lead 6) has first letters I, B, I, Z, A. That string is a city and is not an
English BIP39 word, so it is a city-clue, not a twelfth seed word. It is a
candidate member of the set of ten, and maybe of the set of four. I am not
treating it as a MATCH.

What would confirm it: identifying the four cities on the live pages and
reading the one BIP39 word they share, then matching the escrow.
What would kill it: a full reading of every game that contains no city names.
Cost: needs the pages; no compute until then.

## 5. The rest of the 2025-05-19 to 2025-06-15 clue posts

Posted in order, skipping pure advertisements. Each URL is the author's own
post; I am describing the attached image rather than reproducing it.

- 2025-05-27 "Screenshot of game 12" then "F12 of course": Drive file
  placeholder, see lead 3.
  https://x.com/FTPKgame/status/1927326950692941869
- 2025-05-28 "History": text only.
  https://x.com/FTPKgame/status/1927680981399457854
  A reply asking "Is this a hint?" got "It's up to you ;) For me, yes :)"
- 2025-05-29 a dark wood library interior, candles, herringbone floor, one
  open book on an armchair. https://x.com/FTPKgame/status/1928053987237925220
- 2025-05-30 a leaping white rabbit on a lavender ground.
  https://x.com/FTPKgame/status/1928392074086285478
- 2025-05-31 a Google Maps view of the Pacific with the International Date
  Line drawn as a dashed zig-zag. https://x.com/FTPKgame/status/1928791004858945750
- 2025-06-02 "In one of the games, there is an optional clue that doesn't have
  very good vibes". Text only.
- 2025-06-03 a uniform #FF0000 rectangle, then the reply "What could it make
  you think of? (several attempts will probably be necessary, but you will
  find)". Pixel check: 624x402, every pixel RGB(255,0,0), no yellow, no EXIF
  payload (`analysis/tested.md`). Three days later: "Just a little yellow in
  all this red will help you find the right one." The yellow is therefore not
  in this PNG; it is on a game page.
  https://x.com/FTPKgame/status/1929833486514278892
- 2025-06-04 "SHA256": names the page-naming scheme, already broken.
- 2025-06-05 "5" attached to a blue Tetris J-piece (four squares).
  https://x.com/FTPKgame/status/1930573400700833946
  Game 5 is independently a digit grid whose corrected diagonal already
  returned HTTP 200 as a number URL; this image may be that game's theme, or
  the number five, or both.
- 2025-06-06 screenshot of a player asking whether Game 6's contact-info
  section is meant to be empty, and the author answering that they removed
  a fake email to avoid contact with a fake address, that "collusion,
  false leads, human error can happen", and that the empty field is now
  part of the game. https://x.com/FTPKgame/status/1931005550558371927
  The same post tells readers to look at comments from @N4Khjir and
  @thedragon8383.
- 2025-06-07 an empty 15x15 Scrabble board, standard colouring, centre star,
  no tiles. https://x.com/FTPKgame/status/1931313249644859692
- 2025-06-08 "ccza". Four letters, no image. Unread.
- 2025-06-09 the Arabic word for date/history. Pairs with "History" and with
  the International Date Line map, but that is a grouping, not a word.
  https://x.com/FTPKgame/status/1931993663816548769
- 2025-06-09 a painter at an easel working a blocky colour canvas (posted as
  a wink, then "work of art" two days later).
  https://x.com/FTPKgame/status/1932181950292525147
  https://x.com/FTPKgame/status/1932844034503868830
- 2025-06-10 a Fall Guys bean in the Ninja skin, captioned "The fall guys
  level is very hard and normally requires two players". One of the twelve
  Season 2 games is a Fall Guys Creative level. This is weeks before Season 3
  ("Fall Guys") launched.
  https://x.com/FTPKgame/status/1932394053368238137
- 2025-06-12 "bip". Confirms the target is a BIP39 word, which the oracle
  already assumes.
- 2025-06-13 a Shure SM58, then the one-word post "standards".
  https://x.com/FTPKgame/status/1933439628868014452
- 2025-06-14 "2 times throughout the game, French will help you". The author
  is in Paris; Season 1 already used French song titles as hashtags. Two of
  the twelve games, not all twelve.
- 2025-06-15 "last clue from me": a black chess knight on a grey ground.
  https://x.com/FTPKgame/status/1934183762079666297

After 2025-06-15 the author said they would only promote, not clue. I have not
treated later posts as S2 clues.

What would confirm any one of these: the matching game page, a single BIP39
word, and a 12-word MATCH against the escrow.
What would kill any one of these: the matching game page showing the image was
flavour, plus the word coming from a different mechanic on that page.
Cost: insight against the live pages; I will not sweep the English wordlist
against the escrow on the strength of an image caption.

## 6. Player comments the author pointed at

On 2025-06-06 the author named @N4Khjir and @thedragon8383 as having left
comments "that could interest you", in the same thread as the Game 6 contact-info
answer (https://x.com/FTPKgame/status/1931006963740979489). I pulled both
timelines for the Season 2 clue window (2025-05-19 through the author's
2025-06-15 last clue). The threads are not social only. N4 pasted live page
text. The dragon posted progress reports the author answered. None of this is a
seed word. Every 12-word set still has to go through `tools/oracle.py`.

### @N4Khjir page transcriptions (2025-05-28 to 2025-06-06)

Posted as replies to the author, with the live titles and body text. I am
quoting the puzzle strings, not claiming a BIP39 word.

- Game 1 (https://x.com/N4Khjir/status/1927619197695082629): Vigenere block
  `ZROQV / JVVW EHFOZV TILV XDB. / OROLV LJNH ZRX DDQ'U VTFJR IRZ / UR GFW TIH
  MFVVAHH QVLFK`; Cicada 3301; the Cold War barrier image already named a decoy
  in `analysis/tested.md`; extra paths `/image1.psd` and
  `/gdjztvzuojmmsmuwrsudjhzdvvlkftfehnxxkbpilscjfljyyg.html`.
- Game 4 (https://x.com/N4Khjir/status/1927620248426913890): two photographs.
  The attached files are no longer served. No transcription of what they depict.
- Game 6 (https://x.com/N4Khjir/status/1929061582220276150): page
  `hdvpvgyqxzplxefvngacfsdsljxajfhtweksvlkihugghszomf.html`, title
  "Simplicity Must Be Rewarded I". Season 1 used the same sentence as a hashtag
  and as a clue, with a different final letter.
- Game 7 (https://x.com/N4Khjir/status/1927621189503005053): title
  "Zero-based indexing", plus a screenshot that is no longer served. This is
  the game the Season 4 hint page calls the weakest. The title names the
  convention for reading a number as a list position (0-based versus 1-based).
  I am not treating the title-word as a candidate.
- Game 9 (https://x.com/N4Khjir/status/1927621634828939664): title `1211920`,
  body `3114`. Digit strings. Plausible readings are A1Z26 groups or BIP39
  list indices; both are unconstrained until the live page shows how the
  digits are grouped. I am not printing a word from either split.
- Game 11, teaching pane (https://x.com/N4Khjir/status/1927616681964126429):
  title `44 . C`, plus the mnemonic and address that `tools/oracle.py
  --selftest` already reproduces. Teaching example, not the Season 2 seed.
- Game 11, second pane (https://x.com/N4Khjir/status/1927623047076282678):
  title `+33`, heading "Transcription from Braille", then a five-line French
  poem. `+33` is the calling code for France, which pairs with the author's
  "2 times throughout the game, French will help you". The live page may show
  Braille; this is N4's Latin transcription:

  > Infinie est la lumiere du matin.
  > Berce doucement, le vent dans le jardin.
  > Il murmurait des secrets aux fleurs endormies.
  > Zephyr danse, leger sur l'eau de la vie.
  > Au loin, l'horizon veille, plein de magie.

  English gloss: Infinite is the morning light. Gently rocked, the wind in the
  garden. It whispered secrets to the sleeping flowers. Zephyr dances, light
  on the water of life. In the distance, the horizon watches, full of magic.
  First letters: I, B, I, Z, A (lead 4). Accents omitted here; they do not
  change the first letters.
- Game 5 (https://x.com/N4Khjir/status/1931017991170183383): "Z = 2 ?". Pairs
  with the author's 2025-06-05 Tetris J-piece captioned "5" and with the digit
  grid already in `analysis/tested.md`.
- Game 1 follow-up (https://x.com/N4Khjir/status/1931020117774668115): "The
  file image2.jpg does not exist." The author confirmed it
  (https://x.com/FTPKgame/status/1931024956046909798): the file was a
  development error, and they said they would delete that part of the code.
  Not a puzzle step.
- White-rabbit clue (https://x.com/N4Khjir/status/1928535519022948673): N4
  read it as a wallet with no native ETH. The escrow's ETH balance is 0; the
  prize is the USDT token. I am not treating a thematically neighbouring
  BIP39 word as a candidate.

The author told N4 "you did some good research... nice to share it with
others" (https://x.com/FTPKgame/status/1927681391833051513). N4's later
2025-06-07 to 2025-06-15 posts in the Wayback capture are unrelated retweets,
except a no-text reply to the Shure SM58 clue.

### @thedragon8383 progress reports

- Game 11 teaching wallet empty?
  (https://x.com/thedragon8383/status/1925711495020560598). It is the
  teaching example, 0 ETH / 0 USDT, not the escrow.
- "not sure if I C what is going on"
  (https://x.com/thedragon8383/status/1925723116078080077). Author: "This
  game seems okay" (https://x.com/FTPKgame/status/1925716299876896917).
  Pairs with Game 11's `44 . C` title, or with the letter C, or with neither.
- "I think I got game 10"
  (https://x.com/thedragon8383/status/1926386081076826598). Unverified. Game
  10's two sub-poem acrostics already fail (`analysis/tested.md`); if the
  player was right, the word is not in those acrostics.
- Jungle / Photopea / Game 12 sound: see lead 3.
- "cold German cicada", stuck on Game 1 part 2
  (https://x.com/thedragon8383/status/1929260937292267742). Author: the
  optional bad-vibes clue is not required to reach Game 1
  (https://x.com/FTPKgame/status/1929299848991244698). Later recap: the
  player's first reply was cicada, the second a GPS coordinate site
  (https://x.com/FTPKgame/status/1929903388839350590). The GPS site the
  player linked was https://www.itilog.com/
  (https://x.com/thedragon8383/status/1929895434689941876).
- Solid-red PNG: "Game 2... but why?"
  (https://x.com/thedragon8383/status/1929885806606372961).
- Game 5: asked for a hint; author said a first one had already been posted,
  then the Tetris-J image. Player: "More of these two part puzzles"
  (https://x.com/thedragon8383/status/1930789907376594980).
- International Date Line map: "stuck in Colorado, USA"
  (https://x.com/thedragon8383/status/1930426198095515915).
- Empty Scrabble board: guessed Game 1 or Game 5, "did not seem to get me
  anywhere with either game"
  (https://x.com/thedragon8383/status/1931419058877968771).
- Arabic تاريخ: asked whether the word was Sindhi or Arabic
  (https://x.com/thedragon8383/status/1932077123491053972).

What would confirm any transcription: the matching live page, a single BIP39
word from that page's mechanic, and a 12-word MATCH against the escrow.
What would kill any transcription: the live page showing the pasted text was
flavour, plus the word coming from a different mechanic on that page.
Cost: the harvest itself is done. Applying it still needs the residential
browser in lead 1. I will not sweep the English wordlist against the escrow
on the strength of a title or an acrostic.
