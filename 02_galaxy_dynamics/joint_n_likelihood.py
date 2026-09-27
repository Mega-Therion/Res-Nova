#!/usr/bin/env python3
"""Where do galaxies + the solar system jointly put the transition, within the l^n family
mu_n = x/(1+x^n)^(1/n) at the DERIVED a0? Route 3 of the kappa-transition question.

-2 lnL(n) = chi2_SPARC(n) / s  +  ((Q2(n) - 1.6e-27) / 1.8e-27)^2
s = SPARC tier-1 best reduced chi2 (errors are underestimated by that factor; rescaling makes the
SPARC term a likelihood, not an over-confident one). Reported for s = best chi2_red and s = 1.
Q2 at g_e = 1.9e-10 and 2.4e-10 separately (the external field is the main systematic).
Transition value mu(1) = 2^(-1/n); canonical references: theta 0.7071, kappa 0.9539.
"""
import json
import numpy as np
from efe_quadrupole_q2 import Q2, A0_DERIVED
from cassini_sparc_joint import fit, gals, n as NPTS, nu_n

grid = np.round(np.concatenate([np.arange(2, 6.01, 0.25), np.arange(6.5, 16.01, 0.5)]), 3)
rows = []
for nn in grid:
    nu = nu_n(nn)
    c, k = zip(*[fit(g, nu, A0_DERIVED, 1) for g in gals])
    rows.append({"n": float(nn), "mu1": 2 ** (-1 / nn), "chi2": float(sum(c)), "dof": int(sum(NPTS) - sum(k)),
                 "Q2_19": Q2(nu, A0_DERIVED, 1.9e-10)[0], "Q2_24": Q2(nu, A0_DERIVED, 2.4e-10)[0]})
    print(f"n={nn:5.2f} mu1={2**(-1/nn):.4f} chi2={sum(c):9.1f} Q2 {rows[-1]['Q2_19']*1e27:5.2f}/{rows[-1]['Q2_24']*1e27:5.2f}", flush=True)
chi = np.array([r["chi2"] for r in rows]); s_best = chi.min() / rows[int(chi.argmin())]["dof"]
out = {"grid": rows, "s_best": s_best, "joint": {}}
for sname, s in (("rescaled", s_best), ("raw", 1.0)):
    for ge in ("Q2_19", "Q2_24"):
        m2 = chi / s + ((np.array([r[ge] for r in rows]) - 1.6e-27) / 1.8e-27) ** 2
        i = int(m2.argmin())
        # 1-sigma interval: m2 <= min + 1
        ok = [rows[j]["n"] for j in range(len(rows)) if m2[j] <= m2[i] + 1]
        out["joint"][f"{sname}_{ge}"] = {"n_best": rows[i]["n"], "mu1_best": rows[i]["mu1"], "n_1sigma": [min(ok), max(ok)],
                                         "mu1_1sigma": [2 ** (-1 / min(ok)), 2 ** (-1 / max(ok))]}
        print(f"{sname:9s} {ge}: n_best {rows[i]['n']:.2f}  mu(1) {rows[i]['mu1']:.4f}  1σ n in [{min(ok)}, {max(ok)}] -> mu(1) in [{2**(-1/min(ok)):.4f}, {2**(-1/max(ok)):.4f}]")
print(f"SPARC rescale s = {s_best:.2f}")
json.dump(out, open("JOINT_N_LIKELIHOOD.json", "w"), indent=1)
