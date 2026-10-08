"""Fit puzzle grey = a * Rec.709 + b on confident skin calls, iterate to convergence, re-call every
measured skin tone with the calibrated levels, and write emoji_table3.json (skin.py output + emoji_table2.json)."""
import json, os, re, collections
import numpy as np
REF = os.environ["APPLE_EMOJI_64"]
TONE = re.compile(r"-?1f3f[b-f]")
R = json.load(open("skin_calls.json"))
a, b = 1.0, 0.0
for it in range(20):
    calls = []
    for r in R:
        cal = {k: a*v + b for k, v in r["levels"].items()}
        o = sorted(cal, key=lambda k: abs(cal[k]-r["pmean"]))
        calls.append((r, o[0], o[1], abs(cal[o[1]]-r["pmean"]) - abs(cal[o[0]]-r["pmean"]), abs(cal[o[1]]-cal[o[0]])))
    conf = [c for c in calls if c[3] >= 0.5*c[4]]
    x = np.array([c[0]["levels"][c[1]] for c in conf]); y = np.array([c[0]["pmean"] for c in conf])
    (na, nb), *_ = np.linalg.lstsq(np.vstack([x, np.ones_like(x)]).T, y, rcond=None)
    if abs(na-a) < 1e-4 and abs(nb-b) < 1e-3: break
    a, b = na, nb
res = np.array([abs(a*c[0]["levels"][c[1]]+b - c[0]["pmean"]) for c in calls])
print("puzzle = %.4f * rec709 + %.2f; residual median %.2f" % (a, b, np.median(res)))
fam = collections.defaultdict(dict)
for n in (f[:-4] for f in os.listdir(REF)):
    ts = re.findall(r"1f3f([b-f])", n)
    if len(ts) <= 1: fam[TONE.sub("", n)]["0" if not ts else ts[0]] = n
byi = {c[0]["i"]: c for c in calls}
T = json.load(open("emoji_table2.json"))
for t in T:
    c = byi.get(t["i"])
    if not c: t["tone_method"] = "aligned-glyph"; continue
    t["glyph"] = fam[TONE.sub("", t["glyph"])][c[1]]; t["tone_method"] = "skin-calibrated"
    t["skin_margin"] = round(float(c[3]), 2); t["skin_second"] = c[2]; t["skin_uncertain"] = bool(c[3] < 0.25 * c[4])
    for k in ("tone_rmse", "tone_runner_up", "tone_changed", "tone_err"): t.pop(k, None)
json.dump({"grey_calibration": {"formula": "puzzle = a * rec709 + b", "a": round(float(a), 4), "b": round(float(b), 2)},
           "emojis": T}, open("emoji_table3.json", "w"), indent=1)
