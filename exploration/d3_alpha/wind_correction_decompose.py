#!/usr/bin/env python3
"""Which residual rows drive the MOND-field correction? Linear response: dX = sum over rows of -M^-1 R_row.
Per-row contribution to dY/(2Y0) and to the rotation (real phase variant), plus the aether tilt and ik dP / g.
Usage: wind_correction_decompose.py [par|perp] [75|750000]"""
from wind_cli import pick_dir, pick_k2
from wind_correction_solve import setup

S = setup(pick_dir(), pick_k2()); mp = S.mp; names = S.names
ix = {nm: i for i, nm in enumerate(names)}
for vk in ["1", "10", "100", "600"]:
    vv = mp.mpf(vk) / S.c_kms
    Mn = mp.matrix(S.fM(S.qv, S.Jpv, S.Jlv, S.gval, S.kv, 0, vv)); R = S.residual_vector(vv, "real")
    Y0v = 2 * S.fY0(S.gval, vv)
    tot = mp.lu_solve(Mn, -R)
    print(f"v = {vk} km/s: total dY/2Y0 = {mp.nstr(S.fY1d(*[tot[i] for i in range(len(names))], S.qv, S.gval, S.kv, 0, vv)/Y0v, 5)}"
          f"   ik dP/g = {mp.nstr(1j*S.kv*tot[ix['phi']]/S.gval, 4)}   Q0 du^z/g = {mp.nstr(S.Q0f*tot[ix['uz']]/S.gval, 4)}"
          f"   Q0 h0z/g = {mp.nstr(S.Q0f*tot[ix['h0z']]/S.gval, 4)}")
    for j, nm in enumerate(names):
        if R[j] == 0: continue
        Rj = mp.matrix(len(names), 1); Rj[j] = R[j]
        dX = mp.lu_solve(Mn, -Rj); amps = [dX[i] for i in range(len(names))]
        c = S.fY1d(*amps, S.qv, S.gval, S.kv, 0, vv) / Y0v
        ro = S.frot(*amps, S.qv, S.gval, S.kv, 0, vv) / mp.sqrt(S.fY0(S.gval, vv))
        print(f"    row {nm:4s}: R = {mp.nstr(R[j], 4):>12s}   dY/2Y0 = {mp.nstr(abs(c), 4):>10s}   |rot| = {mp.nstr(abs(ro), 4)}")
