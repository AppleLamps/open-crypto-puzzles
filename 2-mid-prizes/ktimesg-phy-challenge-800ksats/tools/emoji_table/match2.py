import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clues", "spiral.png")
import numpy as np, json
from PIL import Image
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "match.py")).read().split("# references")[0])
R = np.load("refs.npz"); names = R["names"]; RA, RL, RAR = R["A"], R["L"], R["AR"]
def z(x):
    x = x.reshape(len(x), -1); x = x - x.mean(1, keepdims=True)
    return x / (np.linalg.norm(x, axis=1, keepdims=True) + 1e-9)
RAz, RLz = z(RA), z(RL)
RAzm, RLzm = z(RA[:, :, ::-1]), z(RL[:, :, ::-1])
img = np.asarray(Image.open(IMG).convert("RGBA")).copy()
d = json.load(open("centres.json")); C = np.array(d["centres"]); coin = np.array(d["coin"])
allc = np.vstack([C, coin])
H, W = img.shape[:2]
yy, xx = np.mgrid[0:H, 0:W]
out = []
for i, (cx, cy) in enumerate(C):
    x0, x1, y0, y1 = int(cx-48), int(cx+48), int(cy-48), int(cy+48)
    win = img[y0:y1, x0:x1].copy()
    gx, gy = xx[y0:y1, x0:x1], yy[y0:y1, x0:x1]
    dd = (gx[..., None]-allc[:, 0])**2 + (gy[..., None]-allc[:, 1])**2
    win[dd.argmin(-1) != i] = 0          # keep only pixels nearest this emoji's centre
    v = norm(win)
    a, l, ar = v
    az, lz = z(a[None])[0], z(l[None])[0]
    sc = 0.5*(RAz @ az) + 0.5*(RLz @ lz)
    scm = 0.5*(RAzm @ az) + 0.5*(RLzm @ lz)
    best = np.argsort(-np.maximum(sc, scm))[:5]
    out.append({"i": i, "x": float(cx), "y": float(cy), "aspect": float(ar),
                "top": [(str(names[b]), round(float(sc[b]), 3), round(float(scm[b]), 3)) for b in best],
                "lum_mean": float((l.sum() / max(a.sum(), 1e-9)))})
json.dump(out, open("matches.json", "w"), indent=1)
import collections
mir = sum(1 for o in out if o["top"][0][2] > o["top"][0][1])
print("emojis:", len(out), "best match is the mirrored glyph for:", mir)
conf = sorted(o["top"][0][1:] and max(o["top"][0][1:]) for o in out)
print("best-score quantiles:", np.round(np.quantile(conf, [0, .05, .25, .5, .9]), 3))
