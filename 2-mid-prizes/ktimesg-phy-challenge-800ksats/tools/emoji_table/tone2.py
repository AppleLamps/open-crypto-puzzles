import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clues", "spiral.png")
import numpy as np, json, os, re
from PIL import Image
REF = os.environ["APPLE_EMOJI_64"]
names = [f[:-4] for f in os.listdir(REF)]
TONE = re.compile(r"-?1f3f[b-f]")
fam = {}
for n in names: fam.setdefault(TONE.sub("", n), []).append(n)
T = json.load(open("emoji_table.json"))
img = np.asarray(Image.open(IMG).convert("RGBA")).astype(float)
d = json.load(open("centres.json")); C = np.array(d["centres"]); allc = np.vstack([C, d["coin"]])
H, W = img.shape[:2]; yy, xx = np.mgrid[0:H, 0:W]
def tight(p):
    ys, xs = np.nonzero(p[..., 3] > 12); return p[ys.min():ys.max()+1, xs.min():xs.max()+1]
def gray_pm(p):   # Rec.709 luminance, premultiplied by alpha, plus alpha
    a = p[..., 3] / 255; return (p[...,0]*0.2126 + p[...,1]*0.7152 + p[...,2]*0.0722) * a, a
out = []
for t in T:
    i = t["i"]; cx, cy = t["x"], t["y"]; x0, y0 = int(cx-50), int(cy-50)
    win = img[y0:y0+100, x0:x0+100].copy()
    dd = (xx[y0:y0+100, x0:x0+100][...,None]-allc[:,0])**2 + (yy[y0:y0+100, x0:x0+100][...,None]-allc[:,1])**2
    win[dd.argmin(-1) != i] = 0
    pz = tight(win); h, w = pz.shape[:2]
    pg, pa = gray_pm(pz)
    mirrored = t["mirror_margin"] > 0.3
    scores = []
    for n in fam.get(TONE.sub("", t["glyph"]), [t["glyph"]]):
        ref = np.asarray(Image.open(os.path.join(REF, n + ".png")).convert("RGBA"))
        if mirrored: ref = ref[:, ::-1]
        rr = np.asarray(Image.fromarray(np.ascontiguousarray(tight(ref.astype(float)).astype(np.uint8)), "RGBA").resize((w, h), Image.LANCZOS)).astype(float)
        rg, ra = gray_pm(rr)
        m = (pa > 0.9) & (ra > 0.9)
        scores.append((float(np.sqrt(np.mean((pg[m] - rg[m])**2))), n))
    scores.sort()
    t2 = dict(t); t2["glyph"] = scores[0][1]; t2["tone_rmse"] = round(scores[0][0], 2)
    t2["tone_runner_up"] = (scores[1][1], round(scores[1][0], 2)) if len(scores) > 1 else None
    t2["tone_changed"] = scores[0][1] != t["glyph"]
    out.append(t2)
json.dump(out, open("emoji_table2.json", "w"), indent=1)
amb = [o for o in out if o["tone_runner_up"] and o["tone_runner_up"][1] < 1.25 * o["tone_rmse"]]
print("emojis with tone variants:", sum(1 for o in out if o["tone_runner_up"]))
print("tone call changed vs quantile method:", sum(o["tone_changed"] for o in out))
print("ambiguous (runner-up within 25%):", len(amb))
print("rmse median %.1f" % np.median([o["tone_rmse"] for o in out]))
