#!/usr/bin/env python3
"""Which residual rows drive the MOND-field correction? Linear response: dX = sum over rows of -M^-1 R_row.
Per-row contribution to dY/(2Y0) (signed, real phase variant), plus the aether tilt and the scalar part ik dP / g."""
import sys, runpy
DIR = sys.argv[1] if len(sys.argv) > 1 else "par"; K2v = sys.argv[2] if len(sys.argv) > 2 else "75"
sys.argv = ["wcs", DIR, K2v]
src = open("wind_correction_solve.py").read()
src = src[:src.index('ix = {nm: i for i, nm in enumerate(names)}')]
G = {}; exec(compile(src, "wcs", "exec"), G)
mp, names, fM, fY1d, fY0, frot = G["mp"], G["names"], G["fM"], G["fY1d"], G["fY0"], G["frot"]
qv, Jpv, Jlv, gval, kv, c_kms, Q0f = G["qv"], G["Jpv"], G["Jlv"], G["gval"], G["kv"], G["c_kms"], G["Q0f"]
ix = {nm: i for i, nm in enumerate(names)}
for vk in ["1", "10", "100", "600"]:
    vv = mp.mpf(vk) / c_kms
    Mn = mp.matrix(fM(qv, Jpv, Jlv, gval, kv, 0, vv)); R = G["residual_vector"](vv, "real")
    Y0v = 2 * fY0(gval, vv)
    tot = mp.lu_solve(Mn, -R)
    print(f"v = {vk} km/s: total dY/2Y0 = {mp.nstr(fY1d(*[tot[i] for i in range(len(names))], qv, gval, kv, 0, vv)/Y0v, 5)}"
          f"   ik dP/g = {mp.nstr(1j*kv*tot[ix['phi']]/gval, 4)}   Q0 du^z/g = {mp.nstr(Q0f*tot[ix['uz']]/gval, 4)}   Q0 h0z/g = {mp.nstr(Q0f*tot[ix['h0z']]/gval, 4)}")
    for j, nm in enumerate(names):
        if R[j] == 0: continue
        Rj = mp.matrix(len(names), 1); Rj[j] = R[j]
        dX = mp.lu_solve(Mn, -Rj)
        c = fY1d(*[dX[i] for i in range(len(names))], qv, gval, kv, 0, vv) / Y0v
        ro = frot(*[dX[i] for i in range(len(names))], qv, gval, kv, 0, vv) / mp.sqrt(fY0(gval, vv))
        print(f"    row {nm:4s}: R = {mp.nstr(R[j], 4):>12s}   dY/2Y0 = {mp.nstr(abs(c), 4):>10s}   |rot| = {mp.nstr(abs(ro), 4)}")
