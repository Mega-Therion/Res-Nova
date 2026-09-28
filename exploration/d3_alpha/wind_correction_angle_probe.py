#!/usr/bin/env python3
"""Probes that separate the two readings of the angled-k test (aest_wind_bg_angled.py operator, no rebuild).
The physical forcing R_z sits in the along-wind aether row, so it projects onto the along-k channel with cos(alpha).
  A. physical residual (all rows), alpha up to 89.5 deg: growth toward 90 deg = wake signature.
  B. aether forcing ALONG k: rows (ux, uz) = R_z (sin a, cos a).  flat -> isotropic balance; ~1/cos -> along-wind (k_z) balance.
  C. aether forcing TRANSVERSE to k: rows (ux, uz) = R_z (cos a, -sin a).  does it drive dP at all?
Diagnostic: |k dP|/g, the size of the scalar-gradient correction (it points along k); s_min(M) for conditioning.
Usage: wind_correction_angle_probe.py [par|perp] [75|750000]"""

import sympy as sp, mpmath as mp
from wind_cli import pick_dir, pick_k2
from sym_json import load_matrix
from wind_correction_solve import setup

mp.mp.dps = 80
DIR, K2v = pick_dir(), pick_k2()
MA, names, (qb, Jp, Jl, g, kx, kz, w, vw), _ = load_matrix(
    f"wind_bg_angled_{DIR}_K2{K2v}.json"
)
fM = sp.lambdify((qb, Jp, Jl, g, kx, kz, w, vw), MA, "mpmath")
S = setup(DIR, K2v)
ix = {nm: i for i, nm in enumerate(names)}


def solve(vv, a_deg, R):
    al = mp.radians(a_deg)
    kxv, kzv = S.kv * mp.sin(al), S.kv * mp.cos(al)
    Mn = mp.matrix(fM(S.qv, S.Jpv, S.Jlv, S.gval, kxv, kzv, 0, vv))
    dX = mp.lu_solve(Mn, -R)
    smin = min(abs(sv) for sv in mp.svd_c(Mn, compute_uv=False))
    return S.kv * abs(dX[ix["phi"]]) / S.gval, smin


def forcing(vv, a_deg, mode):
    R = S.residual_vector(vv, "real")
    if mode == "A":
        return R
    Rz = R[ix["uz"]]
    al = mp.radians(a_deg)
    out = mp.matrix(len(names), 1)
    if mode == "B":
        out[ix["ux"]], out[ix["uz"]] = Rz * mp.sin(al), Rz * mp.cos(al)
    else:
        out[ix["ux"]], out[ix["uz"]] = Rz * mp.cos(al), -Rz * mp.sin(al)
    return out


for mode, angles, title in [
    ("A", [0, 45, 75, 80, 85, 88, 89.5], "A. physical residual"),
    ("B", [0, 30, 45, 60, 75, 85], "B. aether forcing along k"),
    ("C", [0, 30, 45, 60, 75, 85], "C. aether forcing transverse to k"),
]:
    print(f"{DIR}, K2={K2v}: {title}; |k dP|/g  [s_min(M) in brackets]")
    print(f"{'v [km/s]':>9s} " + " ".join(f"{'a='+str(a):>19s}" for a in angles))
    for vk in ["1", "100", "600"]:
        vv = mp.mpf(vk) / S.c_kms
        cells = []
        for a in angles:
            val, smin = solve(vv, a, forcing(vv, a, mode))
            cells.append(f"{float(val):9.3e} [{float(smin):7.1e}]")
        print(f"{float(vk):9.0f} " + " ".join(f"{c:>19s}" for c in cells), flush=True)
