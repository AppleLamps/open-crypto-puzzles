"""Spiral geometry of the 256 emojis (reads centres.json from detect.py, writes spiral-geometry.json).

1. Point symmetry: every emoji is paired with the emoji nearest its reflection through a centre,
   the centre chosen to minimise the median mismatch (Hungarian assignment).
2. Two-armed spiral: pair n (1..128) sits at radius A*sqrt(n) + B and angle theta0 + n*alpha, its
   partner at the same radius plus 180 degrees. Slots are assigned by Hungarian matching against a
   first sqrt(a*n + b) fit, then all six parameters are refitted by robust least squares.
3. Offsets: each emoji's radial and tangential distance from its ideal slot. The part shared by a
   pair is compared with the partner difference (pure measurement noise) by a Levene test, and the
   test's power is shown by injecting a +-1 px code into the pairs.
"""
import json
import numpy as np
from scipy.optimize import least_squares, linear_sum_assignment, minimize
from scipy.stats import levene

C = np.array(json.load(open("centres.json"))["centres"])
def pairing(c):
    D = np.hypot(*((2*c - C)[:, None, :] - C[None, :, :]).transpose(2, 0, 1)); np.fill_diagonal(D, 1e9)
    ri, ci = linear_sum_assignment(D); return D[ri, ci], ci
c = minimize(lambda c: np.median(pairing(c)[0]), C.mean(0), method="Nelder-Mead").x
pd, part = pairing(c)
assert all(part[part[i]] == i for i in range(len(C))), "pairing is not mutual"
def model(p, a_law):
    cx, cy, a, b, t0, al = p; n = np.arange(1, 129)
    r = a*np.sqrt(n) + b if a_law else np.sqrt(np.maximum(a*n + b, 1)); t = t0 + al*n
    return np.vstack([np.c_[cx + r*np.cos(t), cy + r*np.sin(t)], np.c_[cx - r*np.cos(t), cy - r*np.sin(t)]])
def assign(X):
    D = np.hypot(*(X[:, None, :] - C[None, :, :]).transpose(2, 0, 1)); return linear_sum_assignment(D)
# divergence angle from the doubled pair angles, radius law from the pair radii
pairs = sorted({tuple(sorted((i, int(part[i])))) for i in range(len(C))})
M = np.array([((C[i] - c) - (C[j] - c)) / 2 for i, j in pairs]); r = np.hypot(*M.T); th2 = 2*np.arctan2(M[:, 1], M[:, 0])
o = np.argsort(r); nn = np.arange(1, 129); (a, b) = np.linalg.lstsq(np.c_[nn, np.ones(128)], r[o]**2, rcond=None)[0]
al = max(np.linspace(0, np.pi, 18001), key=lambda x: abs(np.mean(np.exp(1j*(th2[o] - 2*x*nn)))))
p = np.array([c[0], c[1], a, b, 0.0, al])
p[4] = min(np.linspace(0, 2*np.pi, 720, endpoint=False),
           key=lambda t0: (lambda X: (lambda ri, ci: np.median(np.hypot(*(X[ri] - C[ci]).T)))(*assign(X)))(model([*p[:4], t0, p[5]], False)))
for _ in range(6):
    ri, ci = assign(model(p, False)); p = least_squares(lambda q: (model(q, False)[ri] - C[ci]).ravel(), p, loss="soft_l1", f_scale=5).x
slot = np.empty(len(C), int); slot[ci] = ri
n = slot % 128 + 1; arm = (slot >= 128).astype(int)
rr = np.hypot(C[:, 0] - p[0], C[:, 1] - p[1]); rn = np.array([rr[n == j].mean() for j in nn])
(A, B) = np.linalg.lstsq(np.c_[np.sqrt(nn), np.ones(128)], rn, rcond=None)[0]
def pred(q):
    r = q[2]*np.sqrt(n) + q[3]; t = q[4] + q[5]*n + np.pi*arm
    return np.c_[q[0] + r*np.cos(t), q[1] + r*np.sin(t)]
q = least_squares(lambda q: (pred(q) - C).ravel(), [p[0], p[1], A, B, p[4], p[5]], loss="soft_l1", f_scale=3).x
R = C - pred(q); t = q[4] + q[5]*n + np.pi*arm
rad = R[:, 0]*np.cos(t) + R[:, 1]*np.sin(t); tan = -R[:, 0]*np.sin(t) + R[:, 1]*np.cos(t)
def split(v):
    a_ = [np.where((n == j) & (arm == 0))[0][0] for j in nn]; b_ = [np.where((n == j) & (arm == 1))[0][0] for j in nn]
    return (v[a_] + v[b_]) / 2, (v[a_] - v[b_]) / 2
pr = levene(*split(rad)).pvalue; pt = levene(*split(tan)).pvalue
rng = np.random.default_rng(1)
power = np.mean([levene(*split(rad + rng.choice([-1.0, 1.0], 128)[n - 1])).pvalue < 0.01 for _ in range(200)])
out = {"symmetry_centre": [round(float(x), 2) for x in c], "partner_mismatch_px_median": round(float(np.median(pd)), 2),
       "spiral": {"centre": [round(float(q[0]), 2), round(float(q[1]), 2)], "radius": "%.3f*sqrt(n) + %.3f" % (q[2], q[3]),
                  "theta0_deg": round(float(np.degrees(q[4]) % 360), 3), "divergence_deg": round(float(np.degrees(q[5])), 4),
                  "angle_convention": "image coordinates, 0 = +x (east), positive = clockwise on screen"},
       "offset_test": {"levene_p_radial": round(float(pr), 3), "levene_p_tangential": round(float(pt), 3),
                       "power_at_1px_code": round(float(power), 3)},
       "emojis": [{"i": i, "n": int(n[i]), "arm": "AB"[arm[i]], "rad_px": round(float(rad[i]), 2), "tan_px": round(float(tan[i]), 2)} for i in range(len(C))]}
json.dump(out, open("spiral-geometry.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "emojis"}, indent=1))
