import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clues", "spiral.png")
import numpy as np, json, os, re
from PIL import Image
REF = os.environ["APPLE_EMOJI_64"]
names = [f[:-4] for f in os.listdir(REF)]
TONE = re.compile(r"-?1f3f[b-f]")
fam = {}
for n in names: fam.setdefault(TONE.sub("", n), []).append(n)
M = json.load(open("matches.json"))
img = np.asarray(Image.open(IMG).convert("RGBA")).astype(float)
d = json.load(open("centres.json")); C = np.array(d["centres"]); allc = np.vstack([C, d["coin"]])
H, W = img.shape[:2]; yy, xx = np.mgrid[0:H, 0:W]
q = np.linspace(0.02, 0.98, 49)
def lum709(p): return p[...,0]*0.2126 + p[...,1]*0.7152 + p[...,2]*0.0722
cache = {}
def refq(n):
    if n not in cache:
        p = np.asarray(Image.open(os.path.join(REF, n + ".png")).convert("RGBA")).astype(float)
        cache[n] = np.quantile(lum709(p)[p[...,3] > 250], q) if (p[...,3] > 250).sum() > 50 else None
    return cache[n]
rows = []
for o in M:
    i = o["i"]; cx, cy = o["x"], o["y"]
    x0, y0 = int(cx-48), int(cy-48)
    win = img[y0:y0+96, x0:x0+96].copy()
    dd = (xx[y0:y0+96, x0:x0+96][...,None]-allc[:,0])**2 + (yy[y0:y0+96, x0:x0+96][...,None]-allc[:,1])**2
    win[dd.argmin(-1) != i] = 0
    pa = win[...,3] > 250
    pv = np.quantile(win[...,0][pa], q) if pa.sum() > 50 else None
    best = o["top"][0]; base = TONE.sub("", best[0])
    tones = []
    for n in fam.get(base, [best[0]]):
        rq = refq(n)
        if rq is None or pv is None: continue
        tones.append((float(np.abs(pv - rq).mean()), n))
    tones.sort()
    mir = best[2] - best[1]
    rows.append({"i": i, "x": round(cx, 1), "y": round(cy, 1), "glyph": tones[0][1] if tones else best[0],
                 "shape_score": round(max(best[1], best[2]), 3), "mirror_margin": round(mir, 3),
                 "tone_err": round(tones[0][0], 2) if tones else None,
                 "tone_runner_up": (tones[1][1], round(tones[1][0], 2)) if len(tones) > 1 else None})
json.dump(rows, open("emoji_table.json", "w"), indent=1)
te = [r["tone_err"] for r in rows if r["tone_err"] is not None]
print("rows", len(rows), "tone err median %.1f, 90%% %.1f" % (np.median(te), np.quantile(te, .9)))
amb = [r for r in rows if r["tone_runner_up"] and r["tone_runner_up"][1] - r["tone_err"] < 2]
print("tone calls with runner-up within 2 levels:", len(amb))
print("mirrored (margin > 0.01):", sum(r["mirror_margin"] > 0.01 for r in rows), " unmirrored (margin < -0.01):", sum(r["mirror_margin"] < -0.01 for r in rows))
print("low shape score (<0.93):", [(r["i"], r["glyph"], r["shape_score"]) for r in rows if r["shape_score"] < 0.93])
