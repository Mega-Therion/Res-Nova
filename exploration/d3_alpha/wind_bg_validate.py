#!/usr/bin/env python3
"""Validation of the wind-background builder (aest_wind_bg.py) before any solve uses it.
  1. Reduction: at v_w = 0 its matrix must equal the validated aest_mond_bg_fast.py matrix (random parameters).
  2. Boost: at g = 0, qbar = 0 (boosted vacuum + condensate) det M(k,w;v) / det M(k',w';0) must be constant in (k,w),
     with k' = gam (k + v w), w' = gam (w + v k)  (aether moving along -z in the dwarf frame).
  3. Conditioning at w = 0 on the dSph background (x = 0.05): singular values vs v.
Usage: wind_bg_validate.py [par|perp] [K2]"""

import sys, pickle, random, sympy as sp, mpmath as mp
from wind_cli import pick_dir, pick_k2

mp.mp.dps = int(sys.argv[3]) if len(sys.argv) > 3 else 60
DIR = pick_dir()
K2v = pick_k2()
Mw, names, (qb, Jp, Jl, g, k, w, vw), (KB, K2, Q0) = pickle.load(
    open(f"wind_bg_matrix_{DIR}_K2{K2v}.pkl", "rb")
)
fW = sp.lambdify((qb, Jp, Jl, g, k, w, vw), Mw, "mpmath")
ok = True
# ---- 1. reduction ----
if K2v == 75:
    Mf, (qb2, Jp2, Jl2, g2, k2, w2), _ = pickle.load(
        open(f"mond_bg_matrix_{DIR}_K275.pkl", "rb")
    )
    fF = sp.lambdify((qb2, Jp2, Jl2, g2, k2, w2), Mf, "mpmath")
    random.seed(1)
    worst = mp.mpf(0)
    for trial in range(5):
        p = [
            mp.mpf(random.uniform(1e-3, 1e-2)),
            mp.mpf(random.uniform(0.02, 0.9)),
            mp.mpf(random.uniform(0.02, 0.9)),
            mp.mpf(random.uniform(1e-4, 1e-2)),
            mp.mpf(random.uniform(50, 500)),
            mp.mpf(random.uniform(1, 400)),
        ]
        A = mp.matrix(fW(*p, 0))
        B = mp.matrix(fF(*p))
        scale = max(abs(B[i, j]) for i in range(B.rows) for j in range(B.cols))
        diff = (
            max(abs(A[i, j] - B[i, j]) for i in range(B.rows) for j in range(B.cols))
            / scale
        )
        worst = max(worst, diff)
    print(
        f"[1] reduction v_w=0 vs validated builder: max |dM|/max|M| over 5 random points = {mp.nstr(worst, 5)}"
    )
    Dsym = (Mw.subs(vw, 0) - Mf.subs({qb2: qb, Jp2: Jp, Jl2: Jl, g2: g, k2: k, w2: w})).applyfunc(sp.simplify)
    nnz = sum(1 for q in Dsym if q != 0)
    print(f"    symbolic difference at v_w = 0: {nnz} nonzero entries of 100")
    ok &= nnz == 0
# ---- 2. boost ----  exact rational arithmetic (Bareiss); Jl, g, qbar = 0 symbolically (avoids 0/0 in the
# unsimplified Y0 denominators). mpmath determinants showed a precision-independent ~6e-20 artefact; exact is decisive.
Mb = Mw.subs({Jl: 0, qb: 0}).subs(g, 0)
vbq = sp.Rational(3, 10); gbq = 1 / sp.sqrt(1 - vbq**2); ratios = []
for kk, ww in [(100, 30), (57, 400), (300, 5)]:
    kk, ww = sp.Integer(kk), sp.Integer(ww)
    kp, wp = sp.nsimplify(gbq * (kk + vbq * ww)), sp.nsimplify(gbq * (ww + vbq * kk))
    d1 = Mb.subs({Jp: sp.Rational(3, 10), k: kk, w: ww, vw: vbq}).det(method="bareiss")
    d0 = Mb.subs({Jp: sp.Rational(3, 10), k: kp, w: wp, vw: 0}).det(method="bareiss")
    ratios.append(sp.nsimplify(sp.simplify(d1 / d0)))
print(f"[2] boost test, exact (v=3/10, g=qbar=Jl=0): det M(k,w;v)/det M(k',w';0) = {ratios}  (1 - v^2 = {1 - vbq**2})")
ok &= len(set(ratios)) == 1
# ---- 3. conditioning at w = 0 on the dSph background ----
c_kms = mp.mpf(299792.458)
x = mp.mpf("0.05")
Jpv = x / mp.sqrt(1 + x * x)
Jlv = x * (1 + x * x) ** mp.mpf(-1.5)
gv = x * 2 * mp.mpf("3.577e-5")
vf = mp.mpf(10) / c_kms
r = mp.mpf("3e-4")
kv = 1 / r
qv = (vf / r) ** 2 / (mp.mpf(K2) * mp.mpf(Q0))
print(f"[3] conditioning of M(k=1/r, w=0; v), dSph x=0.05, K2={K2v}:")
for vk in ["0", "1", "10", "100", "600"]:
    Mn = mp.matrix(fW(qv, Jpv, Jlv, gv, kv, 0, mp.mpf(vk) / c_kms))
    sv = sorted([abs(sval) for sval in mp.svd_c(Mn, compute_uv=False)])
    print(
        f"    v={vk:>4s} km/s  s_min={mp.nstr(sv[0], 4)}  s_max={mp.nstr(sv[-1], 4)}  cond={mp.nstr(sv[-1]/sv[0], 4)}"
    )
print("VALIDATION", "PASS" if ok else "FAIL")
