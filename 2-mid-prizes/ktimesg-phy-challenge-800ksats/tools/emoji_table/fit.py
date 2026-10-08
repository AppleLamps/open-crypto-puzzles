import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clues", "spiral.png")
import numpy as np, json
from scipy.optimize import linear_sum_assignment, minimize
d = json.load(open("centres.json")); C = np.array(d["centres"]); cx, cy = d["coin"]
GA = np.pi*(3-np.sqrt(5))
def pred(p, N, sgn, n0):
    a, b, t0, ox, oy = p
    n = np.arange(n0, n0+N)
    rr = np.sqrt(np.maximum(a*n + b, 0)); th = t0 + sgn*n*GA
    return np.c_[cx+ox+rr*np.cos(th), cy+oy+rr*np.sin(th)]
def cost(p, N, sgn, n0, ret=False):
    P = pred(p, N, sgn, n0)
    D = np.hypot(*(P[:,None,:]-C[None,:,:]).transpose(2,0,1))
    ri, ci = linear_sum_assignment(D)
    return (D[ri,ci], ri, ci) if ret else np.mean(np.minimum(D[ri,ci], 60)**2)
best = None
for N in (256, 257):
  for n0 in (0, 1):
    for sgn in (1, -1):
        for t0 in np.linspace(0, 2*np.pi, 72, endpoint=False):
            p0 = [3120.4, 26599.2 - 3120.4*(n0-1), t0, 0, 0]
            c = cost(p0, N, sgn, n0)
            if best is None or c < best[0]: best = (c, N, n0, sgn, p0)
print("coarse best", best[:4])
c, N, n0, sgn, p0 = best
res = minimize(lambda p: cost(p, N, sgn, n0), p0, method="Nelder-Mead", options={"maxiter": 4000, "xatol":1e-3, "fatol":1e-3})
dd, ri, ci = cost(res.x, N, sgn, n0, ret=True)
print("refined params", np.round(res.x, 3), "N", N, "n0", n0, "sgn", sgn)
print("match dist: mean %.1f, max %.1f, >25px: %d" % (dd.mean(), dd.max(), (dd > 25).sum()))
unmatched = sorted(set(range(N)) - set(ri))
print("predicted indices with no detection:", [n0+i for i in unmatched])
P = pred(res.x, N, sgn, n0)
for i in unmatched: print("  missing index", n0+i, "predicted at", np.round(P[i]))
idx = np.full(len(C), -1); idx[ci] = ri + n0
json.dump({"params": res.x.tolist(), "N": N, "n0": n0, "sgn": sgn, "index": idx.tolist(), "dist": dict(zip(map(int,ci), map(float,dd)))}, open("fit.json","w"))
