#!/usr/bin/env python3
"""The l^n family mu_n(x) = x / (1 + x^n)^(1/n)  (Hees's nu_n is its inverse: nu_n = [(1+sqrt(1+4y^-n))/2]^(1/n)).

Facts checked here:
 (1) inversion: mu_n(x) x = y  <=>  x = nu_n(y) y          (numerically, all n)
 (2) duality: mu_n(x)^n + mu_n(1/x)^n = 1                 (the canon's MuStdDuality is n = 2)
 (3) transition value: mu_n(1) = 2^(-1/n).  n = 2 gives 1/sqrt2 = theta (the chiral floor).
     Setting mu_n(1) = kappa = 0.9539 gives n_kappa = ln2 / -ln(kappa).
Then Cassini Q2 (2026 bound) and SPARC fits at the derived a0 for n = 2, n_min(Cassini 2 sigma), n_kappa.
"""
import json
from math import log
import numpy as np
from scipy.optimize import brentq
from efe_quadrupole_q2 import Q2, A0_DERIVED
from cassini_sparc_joint import fit, summ, gals, n as NPTS, nu_n

THETA, KAPPA = 2 ** -0.5, 0.9539
mu = lambda nn: (lambda x: x / (1 + x**nn) ** (1 / nn))
x = np.logspace(-3, 3, 2001)
for nn in (1, 2, 5, 14.69):
    y = mu(nn)(x) * x
    inv = np.max(np.abs(nu_n(nn)(y) * y / x - 1))
    dual = np.max(np.abs(mu(nn)(x) ** nn + mu(nn)(1 / x) ** nn - 1))
    print(f"n={nn:6.2f}  inversion err {inv:.1e}  duality err {dual:.1e}  mu(1)={2**(-1/nn):.5f}")
n_kappa = log(2) / -log(KAPPA)
print(f"\nmu_n(1) = theta  -> n = 2 exactly;  mu_n(1) = kappa = {KAPPA} -> n_kappa = {n_kappa:.4f}")
UP2 = 1.6e-27 + 2 * 1.8e-27
qmax = lambda nn: max(Q2(nu_n(nn), A0_DERIVED, 1.9e-10)[0], Q2(nu_n(nn), A0_DERIVED, 2.4e-10)[0])
n_min = brentq(lambda nn: qmax(nn) - UP2, 3, 8, xtol=1e-3)
print(f"Cassini 2026 2-sigma needs n >= {n_min:.3f}  ->  mu(1) >= {2**(-1/n_min):.4f}")
res = {"n_kappa": n_kappa, "n_min_cassini_2sigma": n_min, "mu1_at_n_min": 2 ** (-1 / n_min), "rows": []}
for label, nn in (("theta (n=2, mu_std)", 2.0), ("Cassini edge", n_min), ("kappa", n_kappa)):
    q = qmax(nn); nu = nu_n(nn)
    t0 = summ(*zip(*[fit(g, nu, A0_DERIVED, 0) for g in gals]), NPTS)
    t1 = summ(*zip(*[fit(g, nu, A0_DERIVED, 1) for g in gals]), NPTS)
    res["rows"].append({"label": label, "n": nn, "mu1": 2 ** (-1 / nn), "Q2max": q, "sigma": (q - 1.6e-27) / 1.8e-27, "t0": t0, "t1": t1})
    print(f"{label:22s} n={nn:6.3f} mu(1)={2**(-1/nn):.4f}  Q2max {q*1e27:5.2f} ({(q-1.6e-27)/1.8e-27:+.1f}σ)  t0 {t0['median']:.2f}/{t0['agg']:.1f}  t1 {t1['median']:.2f}/{t1['agg']:.2f}", flush=True)
json.dump(res, open("MU_N_DUALITY_BAND.json", "w"), indent=1)
