import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clues", "spiral.png")
import numpy as np, json, os, re, collections
from PIL import Image
from scipy import ndimage as ndi
REF = os.environ["APPLE_EMOJI_64"]
names = [f[:-4] for f in os.listdir(REF)]
TONE = re.compile(r"-?1f3f[b-f]")
fam = collections.defaultdict(dict)
for n in names:
    ts = re.findall(r"1f3f([b-f])", n)
    if len(ts) <= 1: fam[TONE.sub("", n)]["0" if not ts else ts[0]] = n
T = json.load(open("emoji_table2.json"))
img = np.asarray(Image.open(IMG).convert("RGBA")).astype(float)
d = json.load(open("centres.json")); C = np.array(d["centres"]); allc = np.vstack([C, d["coin"]])
H, W = img.shape[:2]; yy, xx = np.mgrid[0:H, 0:W]
L = lambda p: p[...,0]*0.2126 + p[...,1]*0.7152 + p[...,2]*0.0722
def tightbox(alpha): ys, xs = np.nonzero(alpha > 12); return ys.min(), ys.max()+1, xs.min(), xs.max()+1
def rs(arr, w, h, mode=Image.LANCZOS):
    return np.asarray(Image.fromarray(arr.astype(np.float32), "F").resize((w, h), mode))
rows = []
for t in T:
    base = TONE.sub("", t["glyph"]); v = fam.get(base)
    if not v or len(v) < 6 or len(re.findall(r"1f3f", t["glyph"])) > 1: continue
    i = t["i"]; x0, y0 = int(t["x"]-50), int(t["y"]-50)
    win = img[y0:y0+100, x0:x0+100].copy()
    dd = (xx[y0:y0+100, x0:x0+100][...,None]-allc[:,0])**2 + (yy[y0:y0+100, x0:x0+100][...,None]-allc[:,1])**2
    win[dd.argmin(-1) != i] = 0
    a0, a1, b0, b1 = tightbox(win[..., 3]); pz = win[a0:a1, b0:b1]; h, w = pz.shape[:2]
    refs = {k: np.asarray(Image.open(os.path.join(REF, n + ".png")).convert("RGBA")).astype(float) for k, n in v.items()}
    if t["mirror_margin"] > 0.3: refs = {k: r[:, ::-1] for k, r in refs.items()}
    r0, r1, c0, c1 = tightbox(refs["0"][..., 3])
    stack = np.stack([refs[k][r0:r1, c0:c1, :3] for k in "0bcdef"])
    op = np.stack([refs[k][r0:r1, c0:c1, 3] for k in "0bcdef"]).min(0) > 250
    skin = op & ((stack.max(0) - stack.min(0)).max(-1) > 40)
    skin = ndi.binary_erosion(skin, iterations=2)
    if skin.sum() < 20: continue
    m = rs(skin.astype(float), w, h, Image.BILINEAR) > 0.95
    m &= pz[..., 3] > 250
    if m.sum() < 15: continue
    pmean = float(pz[..., 0][m].mean())
    lv = {k: float(rs(L(refs[k][r0:r1, c0:c1]), w, h)[m].mean()) for k in "0bcdef"}
    order = sorted(lv, key=lambda k: abs(lv[k] - pmean))
    rows.append({"i": i, "base": base, "pmean": round(pmean, 1), "levels": {k: round(x, 1) for k, x in lv.items()},
                 "tone": order[0], "second": order[1], "gap": round(abs(lv[order[1]]-pmean) - abs(lv[order[0]]-pmean), 1),
                 "sep": round(abs(lv[order[1]] - lv[order[0]]), 1), "npx": int(m.sum()),
                 "prev": (re.findall(r"1f3f([b-f])", t["glyph"]) or ["0"])[0]})
json.dump(rows, open("skin_calls.json", "w"), indent=1)
print("measured:", len(rows))
res = np.array([abs(r["pmean"] - r["levels"][r["tone"]]) for r in rows])
print("residual |puzzle - best level|: median %.1f, 90%% %.1f, max %.1f" % (np.median(res), np.quantile(res, .9), res.max()))
weak = [r for r in rows if r["gap"] < 0.25 * r["sep"]]
print("calls where the margin is under a quarter of the separation:", len(weak))
print("changed vs previous call:", sum(r["tone"] != r["prev"] for r in rows))
c = collections.Counter(tuple(sorted((r["tone"], r["second"]))) for r in weak); print("weak pairs:", c.most_common())
