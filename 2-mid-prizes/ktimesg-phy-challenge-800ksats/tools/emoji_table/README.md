# Emoji table of the spiral image

Rebuilds `data/emoji-table.json`: the position, best-matching Apple glyph (Unicode sequence),
skin tone and mirror margin of each of the 256 emojis in `clues/spiral.png`.

The reference glyphs are not in this repository. Fetch them once into a scratch directory:

```bash
npm pack emoji-datasource-apple@16.0.0 && mkdir x && tar xzf emoji-datasource-apple-16.0.0.tgz -C x
export APPLE_EMOJI_64=$PWD/x/package/img/apple/64
```

Then, from a scratch working directory (the scripts write their JSON files to the current directory),
with `T` pointing at this folder:

```bash
T=/path/to/2-mid-prizes/ktimesg-phy-challenge-800ksats/tools/emoji_table
python3 $T/detect.py   # 256 emoji centres + the coin centre -> centres.json
python3 $T/match.py    # normalise the 3,793 reference glyphs -> refs.npz
python3 $T/match2.py   # shape + luminance correlation, plain and mirrored -> matches.json
python3 $T/tone.py     # skin tone by Rec.709 luminance quantiles within each glyph family -> emoji_table.json
python3 $T/tone2.py    # skin tone by aligned Rec.709 pixel comparison with every tone variant -> emoji_table2.json
python3 $T/skin.py     # mean grey over each glyph's skin pixels vs every tone's level -> skin_calls.json
python3 $T/calibrate.py  # fit puzzle grey = a*Rec.709 + b, re-call tones -> emoji_table3.json (= data/emoji-table.json)
python3 $T/geometry.py  # point symmetry, two-armed spiral fit, offset test -> spiral-geometry.json (= data/spiral-geometry.json)
python3 $T/fit.py      # optional: golden-angle spiral fit and index assignment -> fit.json
```

Needs numpy, scipy and pillow. Method notes and known limits are in `../../analysis/leads.md`.
