import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clues", "spiral.png")
import numpy as np, json, os
from PIL import Image
REF = os.environ["APPLE_EMOJI_64"]
S = 40
def norm(rgba):
    """tight alpha bbox, square-pad, resize to SxS; return alpha, luminance (Rec.601, premultiplied)"""
    a = rgba[..., 3].astype(float) / 255
    ys, xs = np.nonzero(a > 0.05)
    if len(xs) == 0: return None
    y0, y1, x0, x1 = ys.min(), ys.max()+1, xs.min(), xs.max()+1
    h, w = y1-y0, x1-x0; m = max(h, w)
    pad = np.zeros((m, m, 4), np.uint8)
    oy, ox = (m-h)//2, (m-w)//2
    pad[oy:oy+h, ox:ox+w] = rgba[y0:y1, x0:x1]
    im = Image.fromarray(pad, "RGBA").resize((S, S), Image.LANCZOS)
    p = np.asarray(im).astype(float)
    al = p[..., 3] / 255
    lum = (0.299*p[...,0] + 0.587*p[...,1] + 0.114*p[...,2]) / 255
    return al, lum * al, (w/h)
# references
names = sorted(os.listdir(REF))
RA, RL, RAR = [], [], []
keep = []
for f in names:
    v = norm(np.asarray(Image.open(os.path.join(REF, f)).convert("RGBA")))
    if v is None: continue
    keep.append(f[:-4]); RA.append(v[0]); RL.append(v[1]); RAR.append(v[2])
RA, RL, RAR = map(np.array, (RA, RL, RAR))
np.savez_compressed("refs.npz", names=np.array(keep), A=RA, L=RL, AR=RAR)
print("refs", len(keep))
