#!/usr/bin/env python3
"""Sensitivity to the zero-mode lift stand-in: qbar = q_s * lap(phi)/(K2 Q0), q_s in {0.1, 0.3, 1, 3, 10}."""
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
qs = ["0.1", "0.3", "1", "3", "10"]
print(f"{DIR}, K2={K2v}: |dS_par|/|S| (par) or |rot| (perp) vs lift strength qbar = q_s x (sec.26 value {float(qv):.3e}/Mpc)")
print(f"{'v [km/s]':>9s} " + " ".join(f"{'q_s='+q:>10s}" for q in qs))
for vk in ["1", "3", "10", "30", "100", "300", "600"]:
    vv = mp.mpf(vk) / c_kms; R = G["residual_vector"](vv, "real"); row = []
    for q in qs:
        qq = qv * mp.mpf(q)
        Mn = mp.matrix(fM(qq, Jpv, Jlv, gval, kv, 0, vv)); dX = mp.lu_solve(Mn, -R)
        row.append(diag(dX, qq, kv, vv))
    print(f"{float(vk):9.0f} " + " ".join(f"{float(x):10.3e}" for x in row), flush=True)
