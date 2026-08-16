#!/usr/bin/env python3
"""Are the fitted dark-matter halo parameters independent of the visible matter?

The parameter ledger showed NFW buying a better fit with 342 extra numbers -
concentration c and V200, two per galaxy. A parameter count alone is a weak
argument: more knobs fit better, everyone knows that.

The sharper question is whether those knobs behave like what they are supposed
to be. Under LCDM the halo collapsed first, from its own merger history, and the
baryons fell in afterwards. So c and V200 should be set by that history - only
loosely related to how much visible matter ended up inside.

This measures that directly. For each galaxy we take the fitted (c, V200) and
ask how well they are predicted by purely baryonic observables: total baryonic
mass, disk scale, and the baryonic velocity at the outermost measured radius.

Reported as Spearman rank correlations (monotonic, outlier-robust) with
permutation p-values, plus the scatter of the baryonic mass -> V200 relation.

If the correlations are tight, the halo parameters are not free in practice -
they are a function of the visible matter, which is the conspiracy the radial
acceleration relation describes.

This is a known tension in the literature (McGaugh+2016, Lelli+2017); the point
here is to confirm it holds in THIS dataset with THESE fits, rather than cite it.

Usage:
    python3 halo_conspiracy.py
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.stats import spearmanr

from parameter_ledger import (
    FD_STD,
    YB_MEAN,
    YB_STD,
    YD_MEAN,
    YD_STD,
    chi2,
    load,
    v_bary_sq,
    v_nfw,
)
from sparc_paths import resolve_sparc_dir

KPC_TO_M = 3.086e19
KM_TO_M = 1000.0
G_SI = 6.674e-11
MSUN = 1.989e30


def fit_nfw(g):
    nb = 1 + (1 if g["has_bulge"] else 0)

    def f(t):
        yd = t[0]
        yb = t[1] if g["has_bulge"] else 0.0
        fd, c, v200 = t[-3], t[-2], t[-1]
        pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2
        if g["has_bulge"]:
            pr += ((yb - YB_MEAN) / YB_STD) ** 2
        return chi2(g, v_nfw(g, yd, yb, fd, c, v200), pr)

    best, bx = None, None
    for c0, v0 in ((10.0, 100.0), (5.0, 200.0), (15.0, 50.0), (8.0, 300.0)):
        x0 = [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0, c0, v0]
        b = [(0.01, 5)] * nb + [(0.5, 2.0), (1.0, 100.0), (10.0, 500.0)]
        r = minimize(f, x0, bounds=b, method="L-BFGS-B")
        if best is None or r.fun < best:
            best, bx = float(r.fun), r.x
    yd = bx[0]
    yb = bx[1] if g["has_bulge"] else 0.0
    fd, c, v200 = bx[-3], bx[-2], bx[-1]
    return dict(chi2=best, yd=yd, yb=yb, fd=fd, c=c, v200=v200)


def baryonic_observables(g, fit):
    """Purely visible-matter quantities - no halo information used."""
    vb2 = v_bary_sq(g, fit["yd"], fit["yb"], fit["fd"])
    r = g["r"] * fit["fd"]
    # Enclosed baryonic mass at the outermost measured radius: M = v^2 r / G
    m_bary = (vb2[-1] * KM_TO_M**2) * (r[-1] * KPC_TO_M) / G_SI / MSUN
    return {
        "v_bary_outer": float(math.sqrt(vb2[-1])),
        "log_m_bary": float(math.log10(max(m_bary, 1.0))),
        "r_outer": float(r[-1]),
        "v_bary_max": float(math.sqrt(np.max(vb2))),
    }


def perm_p(x, y, rho, n=20000, seed=7):
    rng = np.random.default_rng(seed)
    y = np.asarray(y)
    cnt = sum(
        abs(spearmanr(x, rng.permutation(y)).statistic) >= abs(rho) for _ in range(n)
    )
    return (cnt + 1) / (n + 1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Evaluate baryonic vs NFW halo parameters.")
    ap.add_argument("--data-dir", default=None, help="Path to SPARC rotmod directory")
    ap.add_argument("--out", default="HALO_CONSPIRACY.json", help="Output JSON filename")
    args = ap.parse_args()

    sparc_dir = resolve_sparc_dir(args.data_dir)
    gals = load(sparc_dir)
    rows = []
    for g in gals:
        fit = fit_nfw(g)
        if not (1.01 < fit["c"] < 99) or not (11 < fit["v200"] < 499):
            continue  # railed against a bound - the fit did not converge
        rows.append({**baryonic_observables(g, fit), **fit, "name": g["name"]})

    print(f"{len(rows)} galaxies with converged NFW fits\n")

    out = {"n": len(rows), "correlations": {}}
    print("How well do PURELY BARYONIC observables predict the halo knobs?")
    print(f"{'halo knob':>8}  {'baryonic predictor':<18} {'rho':>7} {'p':>10}")
    for knob in ("v200", "c"):
        for pred in ("log_m_bary", "v_bary_outer", "v_bary_max", "r_outer"):
            x = [r[pred] for r in rows]
            y = [r[knob] for r in rows]
            rho = spearmanr(x, y).statistic
            p = perm_p(x, y, rho)
            out["correlations"][f"{knob}~{pred}"] = {"rho": float(rho), "p": float(p)}
            print(f"{knob:>8}  {pred:<18} {rho:>7.3f} {p:>10.5f}")

    # Scatter of the baryonic-mass -> V200 relation.
    x = np.array([r["log_m_bary"] for r in rows])
    y = np.log10([r["v200"] for r in rows])
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    out["log_v200_vs_log_mbary"] = {
        "slope": float(coef[0]),
        "intercept": float(coef[1]),
        "scatter_dex": float(np.std(resid)),
    }
    print(
        f"\nlog V200 = {coef[0]:.3f} * log M_bary + {coef[1]:.2f}"
        f"   scatter {np.std(resid):.3f} dex"
    )

    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

