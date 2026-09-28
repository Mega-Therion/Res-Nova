#!/usr/bin/env python3
"""WKB sensitivity: hold the point residual R(P) fixed and evaluate the operator at k = f/r, f in {1/3,1/2,1,2,3}.
The residual's Hessian amplitudes (H = g/r) are background facts; only the plane-wave k of the response is varied."""
import sys
DIR = sys.argv[1] if len(sys.argv) > 1 else "par"; K2v = sys.argv[2] if len(sys.argv) > 2 else "75"
sys.argv = ["wcs", DIR, K2v]
src = open("wind_correction_solve.py").read()
src = src[:src.index('ix = {nm: i for i, nm in enumerate(names)}')]
G = {}; exec(compile(src, "wcs", "exec"), G)
mp, names, fM, fY1d, fY0, frot = G["mp"], G["names"], G["fM"], G["fY1d"], G["fY0"], G["frot"]
# diagnostic: par -> fractional change of |S| (dY/2Y0); perp -> gauge-invariant rotation of S
diag = (lambda dX, qq, kk, vv: abs(fY1d(*[dX[i] for i in range(len(names))], qq, gval, kk, 0, vv)) / (2 * fY0(gval, vv))) if DIR == "par" else \
       (lambda dX, qq, kk, vv: abs(frot(*[dX[i] for i in range(len(names))], qq, gval, kk, 0, vv)) / mp.sqrt(fY0(gval, vv)))
qv, Jpv, Jlv, gval, kv, c_kms = G["qv"], G["Jpv"], G["Jlv"], G["gval"], G["kv"], G["c_kms"]
fs = ["1/3", "1/2", "1", "2", "3"]
print(f"{DIR}, K2={K2v}: |dS_par|/|S| (par) or |rot| (perp) with R(P) fixed, operator at k = f/r")
print(f"{'v [km/s]':>9s} " + " ".join(f"{'f='+f:>10s}" for f in fs))
for vk in ["1", "3", "10", "30", "100", "300", "600"]:
    vv = mp.mpf(vk) / c_kms; R = G["residual_vector"](vv, "real"); row = []
    for f in fs:
        kk = kv * mp.mpf(sp_f := eval(f.replace("/", "/mp.mpf(") + (")" if "/" in f else "")))
        Mn = mp.matrix(fM(qv, Jpv, Jlv, gval, kk, 0, vv)); dX = mp.lu_solve(Mn, -R)
        row.append(diag(dX, qv, kk, vv))
    print(f"{float(vk):9.0f} " + " ".join(f"{float(x):10.3e}" for x in row), flush=True)
