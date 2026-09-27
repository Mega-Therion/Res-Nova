#!/usr/bin/env python3
"""Branch B, phenomenological test: keep mu_std (galaxies' choice), add a screening radius
r_scr(M) = r_sun * (M / M_sun)^(1/4)   (the M^(1/4) scaling of Babichev-Deffayet-Esposito-Farese
2011 extended-Vainshtein MOND), inside which the MOND boost (nu - 1) is suppressed by
s(u) = u^p / (1 + u^p),  u = r / r_scr.

Cassini: exact QUMOND quadrupole with a position-dependent nu,
  Q2 = (3/2) Int dr Int dtheta sin(theta) (nu - nu_e) s(r) (-3/r^2) [(GM/r^2 + g cos)P2 - g sin^2 cos]
(subtracting nu_e is exact because every theta-integral of the bracket vanishes at fixed r).
Validated at s = 1 against efe_quadrupole_q2.Q2 (Milgrom's formula).
SPARC: v^2 = r gN [1 + (nu - 1) s(r / r_scr,gal)], r_scr,gal from the galaxy's baryonic mass.
Scan r_sun; report the window where Cassini passes (2026, 2 sigma) AND SPARC is unchanged.
"""
import json
import numpy as np
from math import pi
from scipy.optimize import minimize
from efe_quadrupole_q2 import Q2 as Q2_milgrom, A0_DERIVED, GM
from parameter_ledger import (FD_STD, KM_TO_M, KPC_TO_M, YB_MEAN, YB_STD, YD_MEAN, YD_STD, chi2, load, v_bary_sq)
from sparc_paths import resolve_sparc_dir

PC = 3.0857e16; MSUN = 1.989e30; G_SI = 6.674e-11
nu_std = lambda y: np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y**2)))
UP2 = 1.6e-27 + 2 * 1.8e-27


def Q2_screened(nu, a0, ge, r_scr, p, nr=6000, nth=400):
    """Q2 = -(3/4pi) Int (nu_eff - 1) grad(Phi_N) . grad(P2/r^3) d^3x  (QUMOND, any scalar nu(x)).
    A subtraction c(r) that depends on r alone is exact (every theta-integral of the bracket
    vanishes); it is applied only beyond r_M/10, where the external field dominates, to avoid
    floating-point cancellation near the Sun. Validated at s = 1 against Milgrom's formula."""
    from scipy.optimize import brentq
    gNe = brentq(lambda g: g * nu(g / a0) - ge, 1e-14, ge)
    nue = nu(gNe / a0)
    r = np.logspace(12, 21, nr)
    x, w = np.polynomial.legendre.leggauss(nth)
    R, X = np.meshgrid(r, x, indexing="ij")
    gr = GM / R**2 + gNe * X; gt = -gNe * np.sqrt(1 - X**2)
    gmag = np.sqrt(gr**2 + gt**2); P2 = 0.5 * (3 * X**2 - 1)
    dot = (-3 / R**4) * gr * P2 + gt * (-3 * X * np.sqrt(1 - X**2)) / R**4
    s = np.ones_like(R) if r_scr is None else (R / r_scr) ** p / (1 + (R / r_scr) ** p)
    c = np.where(R > 0.1 * np.sqrt(GM / a0), (nue - 1) * s, 0.0)
    f = ((nu(gmag / a0) - 1) * s - c) * dot * 2 * np.pi * R**2
    return -(3 / (4 * np.pi)) * np.trapezoid(f @ w, r)


def v_screened(g, a0, yd, yb, fd, r_sun, p):
    vb2 = v_bary_sq(g, yd, yb, fd); r = g["r"] * fd
    gN = vb2 * KM_TO_M**2 / (r * KPC_TO_M)
    nu = nu_std(np.maximum(gN / a0, 1e-12))
    if r_sun is not None:
        M = (r[-1] * KPC_TO_M) * vb2[-1] * KM_TO_M**2 / G_SI / MSUN
        rs = r_sun * max(M, 1.0) ** 0.25 / 1e3                    # r_sun [pc] -> r_scr [kpc]
        u = r / rs
        nu = 1 + (nu - 1) * u**p / (1 + u**p)
    return np.sqrt(vb2 * nu)


def fit1(g, a0, r_sun, p):
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
        pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2 + (((yb - YB_MEAN) / YB_STD) ** 2 if g["has_bulge"] else 0)
        return chi2(g, v_screened(g, a0, yd, yb, fd, r_sun, p), pr)
    r = minimize(f, [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0], bounds=[(0.01, 5)] * nb + [(0.5, 2.0)], method="L-BFGS-B")
    return float(r.fun), nb + 1


if __name__ == "__main__":
    a0 = A0_DERIVED
    v0 = Q2_screened(nu_std, a0, 1.9e-10, None, 2); m0 = Q2_milgrom(nu_std, a0, 1.9e-10)[0]
    print(f"validation (no screening): direct {v0:.4e}  Milgrom {m0:.4e}  ratio {v0/m0:.4f}")
    gals = load(resolve_sparc_dir(None)); npts = sum(len(g["r"]) for g in gals)
    base = [fit1(g, a0, None, 2) for g in gals]; chi_base = sum(c for c, _ in base)
    red0 = np.median([c / max(len(g["r"]) - k, 1) for (c, k), g in zip(base, gals)])
    print(f"SPARC mu_std unscreened: total chi2 {chi_base:.1f}, tier-1 median {red0:.3f}")
    out = {"validation": [v0, m0], "rows": []}
    for p in (2, 4):
        for r_sun in (0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0):   # pc
            rs_m = r_sun * PC
            q19 = Q2_screened(nu_std, a0, 1.9e-10, rs_m, p); q24 = Q2_screened(nu_std, a0, 2.4e-10, rs_m, p)
            fits = [fit1(g, a0, r_sun, p) for g in gals]
            chi = sum(c for c, _ in fits)
            med = np.median([c / max(len(g["r"]) - k, 1) for (c, k), g in zip(fits, gals)])
            row = {"p": p, "r_scr_sun_pc": r_sun, "r_scr_1e10_pc": r_sun * 1e10 ** 0.25, "Q2_19": q19, "Q2_24": q24,
                   "cassini_pass": bool(max(q19, q24) <= UP2 and min(q19, q24) >= 1.6e-27 - 2 * 1.8e-27), "sparc_dchi2": chi - chi_base, "sparc_dchi2_over_s": (chi - chi_base) / 6.09, "t1_median": float(med)}
            out["rows"].append(row)
            print(f"p={p} r_sun={r_sun:6.3f} pc (1e10 Msun galaxy: {row['r_scr_1e10_pc']:7.1f} pc)  Q2 {q19*1e27:6.2f}/{q24*1e27:6.2f} {'PASS' if row['cassini_pass'] else 'FAIL'}  SPARC dchi2/s {row['sparc_dchi2_over_s']:+8.1f}  t1 med {med:.3f}", flush=True)
    json.dump(out, open("SCREENING_WINDOW.json", "w"), indent=1)
