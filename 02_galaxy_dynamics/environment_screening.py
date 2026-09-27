#!/usr/bin/env python3
"""Parameter-free environmental screening: a system is only as MONDian as its surroundings.
    nu_eff = 1 + S(eta) (nu - 1),   S(eta) = 1 - mu_std(eta),   eta = g_ext / a0
No new length or constant: only a0 (derived) and mu_std (live). Pre-declared single form.
Sun: g_ext = 1.9-2.4e-10 (Galaxy) -> Q2_eff = S(eta) Q2 (g_ext uniform over the Sun's MOND region).
SPARC galaxies: external fields are small (field galaxies); tested at uniform eta = 0.01, 0.03, 0.1.
"""
import json
import numpy as np
from scipy.optimize import minimize
from efe_quadrupole_q2 import Q2, A0_DERIVED
from parameter_ledger import (FD_STD, KM_TO_M, KPC_TO_M, YB_MEAN, YB_STD, YD_MEAN, YD_STD, chi2, load, v_bary_sq)
from sparc_paths import resolve_sparc_dir

mu_std = lambda x: x / np.sqrt(1 + x**2)
nu_std = lambda y: np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y**2)))
S = lambda eta: 1 - mu_std(eta)
UP2 = 1.6e-27 + 2 * 1.8e-27

def v_env(g, a0, yd, yb, fd, eta):
    vb2 = v_bary_sq(g, yd, yb, fd); r = g["r"] * fd
    gN = vb2 * KM_TO_M**2 / (r * KPC_TO_M)
    return np.sqrt(vb2 * (1 + S(eta) * (nu_std(np.maximum(gN / a0, 1e-12)) - 1)))

def fit1(g, a0, eta):
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
        pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2 + (((yb - YB_MEAN) / YB_STD) ** 2 if g["has_bulge"] else 0)
        return chi2(g, v_env(g, a0, yd, yb, fd, eta), pr)
    r = minimize(f, [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0], bounds=[(0.01, 5)] * nb + [(0.5, 2.0)], method="L-BFGS-B")
    return float(r.fun), nb + 1

if __name__ == "__main__":
    a0 = A0_DERIVED; out = {"cassini": {}, "sparc": {}}
    for ge in (1.9e-10, 2.4e-10):
        eta = ge / a0; q = Q2(nu_std, a0, ge)[0]; qe = S(eta) * q
        out["cassini"][f"{ge:.1e}"] = {"eta": eta, "S": S(eta), "Q2_bare": q, "Q2_screened": qe, "sigma_2026": (qe - 1.6e-27) / 1.8e-27, "pass": bool(qe <= UP2)}
        print(f"Sun g_ext={ge:.1e}: eta={eta:.2f}  S={S(eta):.3f}  Q2 {q*1e27:.2f} -> {qe*1e27:.2f} e-27  ({(qe-1.6e-27)/1.8e-27:+.2f} sigma)  {'PASS' if qe <= UP2 else 'FAIL'}")
    gals = load(resolve_sparc_dir(None))
    base = [fit1(g, a0, 0.0) for g in gals]; cb = sum(c for c, _ in base)
    for eta in (0.01, 0.03, 0.1):
        fits = [fit1(g, a0, eta) for g in gals]; c = sum(x for x, _ in fits)
        med = float(np.median([x / max(len(g["r"]) - k, 1) for (x, k), g in zip(fits, gals)]))
        out["sparc"][str(eta)] = {"S": S(eta), "dchi2_over_s": (c - cb) / 6.09, "t1_median": med}
        print(f"SPARC eta={eta:.2f}: S={S(eta):.3f}  dchi2/s {(c-cb)/6.09:+.1f}  t1 median {med:.3f} (unscreened 3.360)")
    json.dump(out, open("ENVIRONMENT_SCREENING.json", "w"), indent=1)
