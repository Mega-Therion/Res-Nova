#!/usr/bin/env python3
"""Joint test at the DERIVED a0 = cH0/2pi: which interpolating functions pass the Cassini EFE
quadrupole AND fit SPARC? Families from Hees et al. 2016 eq. 5 (nu_n, nu-bar_alpha).
nu_2 = mu_std, nu-bar_0.5 = McGaugh RAR, nu_1 = simple/mu_dual.
SPARC: ledger loader + nuisance treatment (tier 0 fixed, tier 1 priors)."""
import json
import numpy as np
from math import pi
from scipy.optimize import minimize
from efe_quadrupole_q2 import Q2, A0_DERIVED
from parameter_ledger import (FD_STD, KM_TO_M, KPC_TO_M, YB_MEAN, YB_STD, YD_MEAN, YD_STD,
                              chi2, load, v_bary_sq)
from sparc_paths import resolve_sparc_dir

def nu_n(n):      return lambda y: (0.5 * (1 + np.sqrt(1 + 4 * y**(-n))))**(1 / n)
def nubar(a):     return lambda y: (-np.expm1(-y**a))**(-1 / (2 * a)) + (1 - 1 / (2 * a)) * np.exp(-y**a)
FUN = {f"nu_{n}": nu_n(n) for n in (1, 2, 3, 4, 6, 8)}
FUN.update({f"nubar_{a}": nubar(a) for a in (0.5, 1, 1.5, 2, 3, 4, 6)})

def v_nu(g, nu, a0, yd, yb, fd):
    vb2 = v_bary_sq(g, yd, yb, fd); r = g["r"] * fd
    gN = vb2 * KM_TO_M**2 / (r * KPC_TO_M)
    return np.sqrt(vb2 * nu(np.maximum(gN / a0, 1e-12)))

def fit(g, nu, a0, tier):
    if tier == 0:
        return chi2(g, v_nu(g, nu, a0, YD_MEAN, YB_MEAN if g["has_bulge"] else 0.0, 1.0)), 0
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
        p = ((yd - YD_MEAN) / YD_STD)**2 + ((fd - 1) / FD_STD)**2 + (((yb - YB_MEAN) / YB_STD)**2 if g["has_bulge"] else 0)
        return chi2(g, v_nu(g, nu, a0, yd, yb, fd), p)
    r = minimize(f, [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0],
                 bounds=[(0.01, 5)] * nb + [(0.5, 2.0)], method="L-BFGS-B")
    return float(r.fun), nb + 1

def summ(c, k, n):
    red = np.array([ci / max(ni - ki, 1) for ci, ki, ni in zip(c, k, n)])
    return {"median": float(np.median(red)), "agg": float(sum(c) / max(sum(n) - sum(k), 1)), "under2": int((red < 2).sum())}

gals = load(resolve_sparc_dir(None)); n = [len(g["r"]) for g in gals]


def main():
    res = {}
    print(f"derived a0 {A0_DERIVED:.4e}; Cassini 1-sigma window Q2 in [0, 6]e-27 s^-2; g_e = 1.9e-10 / 2.4e-10")
    print(f"{'function':10s} {'Q2(1.9)':>8s} {'Q2(2.4)':>8s} {'Cassini':>8s} | {'t0 med':>7s} {'t0 agg':>7s} | {'t1 med':>7s} {'t1 agg':>7s}")
    for name, nu in FUN.items():
        q19, _ = Q2(nu, A0_DERIVED, 1.9e-10); q24, _ = Q2(nu, A0_DERIVED, 2.4e-10)
        ok = "PASS" if max(q19, q24) <= 6e-27 else ("edge" if min(q19, q24) <= 6e-27 else "FAIL")
        row = {"Q2_ge1.9": q19, "Q2_ge2.4": q24, "cassini": ok}
        for tier in (0, 1):
            c, k = zip(*[fit(g, nu, A0_DERIVED, tier) for g in gals]); row[f"tier{tier}"] = summ(c, k, n)
        res[name] = row
        print(f"{name:10s} {q19*1e27:8.2f} {q24*1e27:8.2f} {ok:>8s} | {row['tier0']['median']:7.2f} {row['tier0']['agg']:7.2f} | {row['tier1']['median']:7.2f} {row['tier1']['agg']:7.2f}", flush=True)
    json.dump(res, open("CASSINI_SPARC_JOINT.json", "w"), indent=1)


if __name__ == "__main__":
    main()
