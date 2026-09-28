#!/usr/bin/env python3
"""WKB sensitivity (two conventions, argv[3] = fixedR or scaledH):
  fixedR : point residual R(P) held fixed while the operator k = f/r varies (a convention);
  scaledH: Hessian-type residual terms scaled by f with k (a plane-wave Hessian is ik x gradient).
Diagnostic: par -> fractional change of |S|; perp -> gauge-invariant rotation of S.
Usage: wind_correction_ksens.py [par|perp] [75|750000] [fixedR|scaledH]"""
import sys
from wind_cli import pick_dir, pick_k2
from wind_correction_solve import setup

a3 = sys.argv[3] if len(sys.argv) > 3 else "fixedR"
MODE = "scaledH" if a3 == "scaledH" else "fixedR"
S = setup(pick_dir(), pick_k2()); mp = S.mp
fs = [("1/3", mp.mpf(1) / 3), ("1/2", mp.mpf(1) / 2), ("1", mp.mpf(1)), ("2", mp.mpf(2)), ("3", mp.mpf(3))]
print(f"{S.DIR}, K2={S.K2v}, mode={MODE}: |dS_par|/|S| (par) or |rot| (perp); operator at k = f/r")
print(f"{'v [km/s]':>9s} " + " ".join(f"{'f='+lab:>10s}" for lab, _ in fs))
for vk in ["1", "3", "10", "30", "100", "300", "600"]:
    vv = mp.mpf(vk) / S.c_kms; row = []
    R = S.residual_vector(vv, "real") if MODE == "fixedR" else None
    for lab, f in fs:
        kk = S.kv * f
        Rk = R if MODE == "fixedR" else S.residual_vector(vv, f)
        dX = mp.lu_solve(mp.matrix(S.fM(S.qv, S.Jpv, S.Jlv, S.gval, kk, 0, vv)), -Rk)
        row.append(S.diag(dX, S.qv, kk, vv))
    print(f"{float(vk):9.0f} " + " ".join(f"{float(x):10.3e}" for x in row), flush=True)
