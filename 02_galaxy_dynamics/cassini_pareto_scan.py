#!/usr/bin/env python3
"""Pareto scan at the DERIVED a0: Cassini Q2 (2026 bound) vs SPARC fit, three Hees families.
Cassini 2026 (arXiv:2602.17884): Q2 = (1.6 +/- 1.8) x 10^-27 s^-2  -> 2-sigma upper 5.2e-27.
Q2 taken at g_e = 1.9e-10 and 2.4e-10; a function PASSES if both are <= 5.2e-27 (2 sigma)."""
import json
import numpy as np
from efe_quadrupole_q2 import Q2, A0_DERIVED
from cassini_sparc_joint import fit, summ, gals, n, nu_n, nubar

def nuhat(a): return lambda y: (-np.expm1(-y**(a / 2)))**(-1 / a)
FAM = {"nu_n": (nu_n, np.arange(2, 12.01, 1.0)), "nubar_a": (nubar, np.array([0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10])),
       "nuhat_a": (nuhat, np.array([1, 2, 3, 4, 5, 6, 7, 8, 10]))}
UP2 = 1.6e-27 + 2 * 1.8e-27
rows = []
for fam, (mk, grid) in FAM.items():
    for p in grid:
        nu = mk(p)
        q19, _ = Q2(nu, A0_DERIVED, 1.9e-10); q24, _ = Q2(nu, A0_DERIVED, 2.4e-10)
        r = {"family": fam, "p": float(p), "Q2_19": q19, "Q2_24": q24, "sigma_2026": (max(q19, q24) - 1.6e-27) / 1.8e-27,
             "pass_2sigma": bool(max(q19, q24) <= UP2)}
        for tier in (0, 1):
            c, k = zip(*[fit(g, nu, A0_DERIVED, tier) for g in gals]); r[f"t{tier}"] = summ(c, k, n)
        rows.append(r)
        print(f"{fam:8s} {p:5.1f}  Q2 {q19*1e27:6.2f}/{q24*1e27:6.2f}  {r['sigma_2026']:+6.1f}σ {'PASS' if r['pass_2sigma'] else '    '} | t0 {r['t0']['median']:6.2f}/{r['t0']['agg']:7.2f} | t1 {r['t1']['median']:5.2f}/{r['t1']['agg']:6.2f}", flush=True)
json.dump(rows, open("CASSINI_PARETO_SCAN.json", "w"), indent=1)
ok = [r for r in rows if r["pass_2sigma"]]
print("\nbest PASSING by tier-1 aggregate:", sorted([(r["family"], r["p"], round(r["t1"]["agg"], 2), round(r["t1"]["median"], 2)) for r in ok], key=lambda x: x[2])[:5])
print("best PASSING by tier-0 median:", sorted([(r["family"], r["p"], round(r["t0"]["median"], 2), round(r["t0"]["agg"], 1)) for r in ok], key=lambda x: x[2])[:5])
