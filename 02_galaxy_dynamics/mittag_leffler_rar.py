#!/usr/bin/env python3
"""Mittag-Leffler generalization of the radial acceleration relation (RAR), a0 derived.

McGaugh-Lelli-Schombert (2016) RAR:   g = g_N / (1 - exp(-sqrt(g_N/a0)))
The exponential is the alpha = 1 member of the Mittag-Leffler family
    E_alpha(z) = sum_k z^k / Gamma(alpha k + 1),
the relaxation function of fractional calculus (the Gamma function sets the whole family).
Combination tested (new, to our knowledge): replace exp with E_alpha,
    g = g_N / (1 - E_alpha(-sqrt(g_N/a0))),   0 < alpha <= 1,
with a0 = cH0/2pi DERIVED. One order alpha replaces the hand choice of interpolating function.
Deep-MOND limit is kept for every alpha (E_alpha(-t) -> 1 - t/Gamma(1+alpha) as t -> 0, so
g -> Gamma(1+alpha) sqrt(g_N a0)): the effective deep-MOND constant becomes
a0_eff = Gamma(1+alpha)^2 a0. At alpha -> 1 it is the plain RAR.

E_alpha(-x) for 0 < alpha < 1 via its completely-monotone integral representation:
    E_alpha(-x) = (sin(alpha pi)/pi) Int_0^inf  e^{-u x^(1/alpha)} u^(alpha-1) / (u^(2alpha) + 2 u^alpha cos(alpha pi) + 1) du

    python3 mittag_leffler_rar.py   -> MITTAG_LEFFLER_RAR.json
"""
import json
from math import gamma, pi, sin, cos
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

from parameter_ledger import (A0_HORIZON, A0_MOND, FD_STD, KM_TO_M, KPC_TO_M, YB_MEAN,
                              YB_STD, YD_MEAN, YD_STD, chi2, load, v_bary_sq, v_mond_like)
from sparc_paths import resolve_sparc_dir


def ml_neg(alpha, x):
    """E_alpha(-x), x >= 0, 0 < alpha <= 1."""
    if alpha >= 0.9999:
        return np.exp(-x)
    out = np.empty_like(np.atleast_1d(x), dtype=float)
    sa, ca = sin(alpha * pi), cos(alpha * pi)
    for i, xi in enumerate(np.atleast_1d(x)):
        if xi == 0:
            out[i] = 1.0; continue
        if xi < 0.5:  # series converges fast here
            out[i] = sum((-xi) ** k / gamma(alpha * k + 1) for k in range(60)); continue
        X = xi ** (1 / alpha)
        f = lambda u: np.exp(-u * X) * u ** (alpha - 1) / (u ** (2 * alpha) + 2 * u**alpha * ca + 1)
        v1, _ = quad(f, 0, 1, limit=200); v2, _ = quad(f, 1, np.inf, limit=200)
        out[i] = sa / pi * (v1 + v2)
    return out


class MLTable:
    """Tabulate E_alpha(-t) on a log grid in t for speed."""
    def __init__(self, alpha):
        self.t = np.concatenate([[0.0], np.logspace(-4, 2.5, 500)])
        self.e = ml_neg(alpha, self.t)
    def __call__(self, t):
        return np.interp(t, self.t, self.e, right=0.0)


def v_ml(g, tab, a0, yd, yb, fd):
    vb2 = v_bary_sq(g, yd, yb, fd)
    r = g["r"] * fd
    gN = vb2 * KM_TO_M**2 / (r * KPC_TO_M)
    t = np.sqrt(gN / a0)
    denom = np.maximum(1 - tab(t), 1e-12)
    return np.sqrt(vb2 / denom)


def fit(g, vfun, tier):
    if tier == 0:
        return chi2(g, vfun(YD_MEAN, YB_MEAN if g["has_bulge"] else 0.0, 1.0)), 0
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]; yb = t[1] if g["has_bulge"] else 0.0
        p = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2 + (((yb - YB_MEAN) / YB_STD) ** 2 if g["has_bulge"] else 0)
        return chi2(g, vfun(yd, yb, fd), p)
    x0 = [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0]
    r = minimize(f, x0, bounds=[(0.01, 5)] * nb + [(0.5, 2.0)], method="L-BFGS-B")
    return float(r.fun), nb + 1


def summ(c, k, n):
    red = np.array([ci / max(ni - ki, 1) for ci, ki, ni in zip(c, k, n)])
    return {"median": float(np.median(red)), "mean": float(np.mean(red)), "under2": int((red < 2).sum()),
            "agg": float(sum(c) / max(sum(n) - sum(k), 1))}


def main():
    # self-check E_alpha against the series at moderate x and exp at alpha=1
    for a in (0.5, 0.8):
        s = sum((-1.0) ** k / gamma(a * k + 1) for k in range(80))
        print(f"check E_{a}(-1): integral {ml_neg(a, np.array([1.0]))[0]:.10f} series {s:.10f}")
    print(f"check E_0.5(-x) = exp(x^2) erfc(x) at x=2: {ml_neg(0.5, np.array([2.0]))[0]:.10f} vs",
          f"{float(np.exp(4) * __import__('scipy.special', fromlist=['erfc']).erfc(2)):.10f}")
    gals = load(resolve_sparc_dir(None)); n = [len(g["r"]) for g in gals]
    res = {}
    for tier in (0, 1):
        for name, vf in [("GOD_mu_std", lambda g: (lambda yd, yb, fd: v_mond_like(g, A0_HORIZON, yd, yb, fd)))]:
            c, k = zip(*[fit(g, vf(g), tier) for g in gals]); res[f"tier{tier}_{name}"] = summ(c, k, n)
            print(f"tier{tier} {name:14s} {res[f'tier{tier}_{name}']}")
        for alpha in (1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.5):
            tab = MLTable(alpha)
            for a0n, a0 in (("derived", A0_HORIZON), ("mond", A0_MOND)):
                c, k = zip(*[fit(g, (lambda yd, yb, fd, g=g: v_ml(g, tab, a0, yd, yb, fd)), tier) for g in gals])
                key = f"tier{tier}_ML_alpha{alpha}_a0{a0n}"; res[key] = summ(c, k, n)
                print(f"tier{tier} ML alpha={alpha:4.2f} a0={a0n:7s} {res[key]}", flush=True)
    Path("MITTAG_LEFFLER_RAR.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
