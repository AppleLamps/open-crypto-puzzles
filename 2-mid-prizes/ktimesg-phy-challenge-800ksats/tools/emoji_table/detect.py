import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clues", "spiral.png")
import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
from scipy.cluster.vq import kmeans2
a = np.array(Image.open(IMG)).astype(int)
al = a[...,3]; rgb=a[...,:3]; sat = rgb.max(-1)-rgb.min(-1); fg = al>0
lab,n = ndi.label(ndi.binary_dilation(fg, iterations=6)); lab = lab*fg
sl = ndi.find_objects(lab)
cents=[]; frags=[]
np.random.seed(1)
for i,s in enumerate(sl):
    w=s[1].stop-s[1].start-12; h=s[0].stop-s[0].start-12
    ys,xs = np.nonzero(lab[s]==i+1); ys=ys+s[0].start; xs=xs+s[1].start
    wts = al[ys,xs]
    if max(w,h) < 40: frags.append((xs.mean(), ys.mean())); continue
    if max(w,h) <= 70: cents.append(((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)); continue
    colored = sat[ys,xs] > 40
    if colored.sum() > 1000:   # coin cluster: coin = colored disc region
        cx, cy = xs[colored].mean(), ys[colored].mean()
        coin = (cx,cy)
        rest = ((xs-cx)**2+(ys-cy)**2 > 112**2) & (al[ys,xs] > 80)
        sub = np.zeros_like(fg); sub[ys[rest], xs[rest]] = True
        sl2, k2 = ndi.label(ndi.binary_dilation(sub, iterations=6)); sl2 = sl2*sub
        print('coin cluster neighbours:', k2)
        for j in range(1, k2+1):
            yy2, xx2 = np.nonzero(sl2 == j)
            if len(xx2) > 150: cents.append(((xx2.min()+xx2.max())/2, (yy2.min()+yy2.max())/2))
        continue
    else:
        pts = np.c_[xs,ys].astype(float); k=2
    c,l = kmeans2(pts, k, minit='++', seed=1)
    for j in range(k):
        p = pts[l==j]; cents.append(((p[:,0].min()+p[:,0].max())/2,(p[:,1].min()+p[:,1].max())/2))
cents=np.array(cents)
print("emoji centres:", len(cents), "fragments:", len(frags), "coin:", np.round(coin,1))
for f in frags:
    d = np.hypot(*(cents - f).T); 
    if d.min() > 70: print("fragment far from any emoji:", np.round(f), round(d.min()))
json.dump({"coin": coin, "centres": cents.tolist()}, open("centres.json","w"))
# fragments: belong to an emoji if within its 64-px box (+margin), otherwise group into new emojis
fr = np.array(frags); own = []
for f in fr:
    dx, dy = np.abs(cents - f).T
    own.append(((dx < 40) & (dy < 40)).any())
orph = fr[~np.array(own)]
groups = []
for f in orph:
    for g in groups:
        if np.hypot(*(np.mean(g,0)-f)) < 60: g.append(f); break
    else: groups.append([f])
print("orphan fragments:", len(orph), "-> new emojis:", len(groups))
new = []
for g in groups:
    # bbox of all fg pixels within 40 px of the group's mean
    gx, gy = np.mean(g,0)
    y0,y1,x0,x1 = int(gy-45),int(gy+45),int(gx-45),int(gx+45)
    ys,xs = np.nonzero(fg[y0:y1,x0:x1]); new.append(((xs.min()+xs.max())/2+x0,(ys.min()+ys.max())/2+y0))
    print("  new emoji at", np.round(new[-1]))
cents = np.vstack([cents, new]) if new else cents
print("total emojis:", len(cents))
json.dump({"coin": coin, "centres": cents.tolist()}, open("centres.json","w"))
