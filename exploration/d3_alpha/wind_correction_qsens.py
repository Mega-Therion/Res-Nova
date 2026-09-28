#!/usr/bin/env python3
"""Sensitivity to the zero-mode lift stand-in: qbar = q_s * lap(phi)/(K2 Q0), q_s in {0.1, 0.3, 1, 3, 10}.
Diagnostic: par -> fractional change of |S|; perp -> gauge-invariant rotation of S.
Usage: wind_correction_qsens.py [par|perp] [75|750000]"""
from wind_cli import pick_dir, pick_k2
from wind_correction_solve import setup

S = setup(pick_dir(), pick_k2()); mp = S.mp
qs = ["0.1", "0.3", "1", "3", "10"]
print(f"{S.DIR}, K2={S.K2v}: |dS_par|/|S| (par) or |rot| (perp) vs lift strength qbar = q_s x (sec.26 value {float(S.qv):.3e}/Mpc)")
print(f"{'v [km/s]':>9s} " + " ".join(f"{'q_s='+q:>10s}" for q in qs))
for vk in ["1", "3", "10", "30", "100", "300", "600"]:
    vv = mp.mpf(vk) / S.c_kms; R = S.residual_vector(vv, "real"); row = []
    for q in qs:
        qq = S.qv * mp.mpf(q)
        dX = mp.lu_solve(mp.matrix(S.fM(qq, S.Jpv, S.Jlv, S.gval, S.kv, 0, vv)), -R)
        row.append(S.diag(dX, qq, S.kv, vv))
    print(f"{float(vk):9.0f} " + " ".join(f"{float(x):10.3e}" for x in row), flush=True)
