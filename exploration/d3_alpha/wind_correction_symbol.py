#!/usr/bin/env python3
"""The Fourier symbol of the high-speed response, K(k) = dP / R_uz for a unit along-wind aether forcing, and its real-space
reading. Measured: K * v * |k|^2 (complex) at several alpha and at alpha + 180 deg (k -> -k), on the validated angled operator.
If K*v*|k|^2 is real, even in k and alpha-independent, the linear correction solves a Poisson equation, lap(dphi) = kappa R_z / v,
and its sign says whether the phantom-density part of the forcing cancels (kappa > 0 with R_z/v = 8K_B lap(Phi) + ...: dphi ~ +Phi?)
or reinforces the MOND field. The sign convention is fixed by also measuring the static v -> 0 response to the same forcing.
Usage: wind_correction_symbol.py [par|perp] [75|750000]"""
import sympy as sp, mpmath as mp
from wind_cli import pick_dir, pick_k2
from sym_json import load_matrix
from wind_correction_solve import setup

mp.mp.dps = 80
DIR, K2v = pick_dir(), pick_k2()
MA, names, (qb, Jp, Jl, g, kx, kz, w, vw), _ = load_matrix(f"wind_bg_angled_{DIR}_K2{K2v}.json")
fM = sp.lambdify((qb, Jp, Jl, g, kx, kz, w, vw), MA, "mpmath")
S = setup(DIR, K2v)
ix = {nm: i for i, nm in enumerate(names)}
print(f"{DIR}, K2={K2v}: K v |k|^2 = dP v |k|^2 / R_uz for a unit along-wind aether forcing (|k| = 1/r)")
print(f"{'v [km/s]':>9s} {'alpha':>6s} {'K v |k|^2 (k)':>34s} {'K v |k|^2 (-k)':>34s}")
for vk in ["1", "100", "600"]:
    vv = mp.mpf(vk) / S.c_kms
    for a in [0, 30, 60, 85]:
        vals = []
        for a2 in (a, a + 180):
            al = mp.radians(a2); kxv, kzv = S.kv * mp.sin(al), S.kv * mp.cos(al)
            R = mp.matrix(len(names), 1); R[ix["uz"]] = 1
            dX = mp.lu_solve(mp.matrix(fM(S.qv, S.Jpv, S.Jlv, S.gval, kxv, kzv, 0, vv)), -R)
            vals.append(dX[ix["phi"]] * vv * S.kv**2)
        print(f"{float(vk):9.0f} {a:6d} {mp.nstr(vals[0], 8):>34s} {mp.nstr(vals[1], 8):>34s}", flush=True)
