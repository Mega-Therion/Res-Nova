#!/usr/bin/env python3
"""Fractional-order gravity on SPARC-175, wired to the derived a0 = cH0/2pi.

Giusti (PRD 101, 124029, 2020) replaces Poisson's equation with a fractional one,
    (-Laplacian)^s Phi = -4 pi G l^(2-2s) rho ,   1 <= s <= 3/2,
whose point-mass force is  |grad Phi| = C_s (l/r)^(2-2s) G M / r^2,
    C_s = 4^(3/2-s) Gamma(5/2-s) / (sqrt(pi) Gamma(s)).
s = 1 is Newton; s = 3/2 gives a ~ 1/r (flat curves). Giusti ties l to a0 through
Tully-Fisher at s = 3/2: l = (2/pi) sqrt(G M / a0).

Combination tested here (new): fix l for EVERY order s by the same matching Giusti used,
generalized: the point-mass fractional force equals a0 at the MOND radius r_M = sqrt(GM/a0),
    l^(2-2s) = r_M^(2-2s) / C_s          (reduces to Giusti's l at s = 3/2)
with a0 = cH0/2pi DERIVED. Then the model has ONE global number, the order s, shared by
all 175 galaxies. If a single s fits, the order is a candidate for the functional-choice
parameter; if s scatters galaxy to galaxy, it is not.

At s = 3/2 with a0 = cH0/2pi this gives l = sqrt(r_s R_H) / Gamma(3/2) exactly
(r_s = 2GM/c^2, R_H = c/H0).

Geometry: spherical-equivalent baryons (M(<r) = r V^2 / G per component, gas signed),
exact shell average of the fractional Green function (no shell theorem for s > 1).
Newton limit checked to 1e-5 at s = 1. A thin disk is not a sphere: this is a like-for-like
comparison of ORDERS under one geometry, not a final disk solution.

Nuisance treatment is the ledger's (parameter_ledger.py): tier 0 fixed Yd=0.5, Yb=0.7, fd=1;
tier 1 Gaussian priors on Yd, Yb, fd.

Models:
  GOD        mu_std, a0 derived                        (ledger reference)
  FRAC(s)    universal order s, l from a0 derived      (one global number)
  FRAC_free  per-galaxy s and amplitude free           (diagnostic: where does each galaxy want s?)

    python3 fractional_gravity_sweep.py [--out FRACTIONAL_GRAVITY_SWEEP.json]
"""
from __future__ import annotations

import argparse
import json
import math
from math import gamma, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from parameter_ledger import (A0_HORIZON, FD_STD, KPC_TO_M, YB_MEAN, YB_STD,
                              YD_MEAN, YD_STD, chi2, load, v_mond_like)
from sparc_paths import resolve_sparc_dir

G_KPC = 4.30091e-6                       # kpc (km/s)^2 / Msun
A0_K = A0_HORIZON * KPC_TO_M / 1e6       # (km/s)^2 / kpc
S_GRID = [round(x, 3) for x in np.arange(1.0, 1.5001, 0.02)]


def C_s(s):
    return 4 ** (1.5 - s) * gamma(2.5 - s) / (sqrt(pi) * gamma(s))


def prim(x, s):
    """Antiderivative of phi(x) * x, phi = fractional Green function shape."""
    if abs(s - 1.5) < 1e-9:
        return (2 / pi) * (x**2 / 2 * np.log(x) - x**2 / 4)
    A = gamma(1.5 - s) / (4 ** (s - 1) * sqrt(pi) * gamma(s))
    q = 2 * s - 1
    return -A * x**q / q


def kernel(r, s, h=1e-4):
    """K[i, j] = d/dr of the shell-averaged Green function, point i, shell j (unit mass)."""
    rsh = r - 0.5 * np.diff(np.concatenate([[0.0], r]))
    def U(rr):
        lo = np.abs(rr[:, None] - rsh[None, :]) + 1e-12
        hi = rr[:, None] + rsh[None, :]
        return (prim(hi, s) - prim(lo, s)) / (2 * rr[:, None] * rsh[None, :])
    rp, rm = r * (1 + h), r * (1 - h)
    return (U(rp) - U(rm)) / (rp - rm)[:, None]


class Gal:
    def __init__(self, g):
        self.g = g
        self.K = {s: kernel(g["r"], s) for s in S_GRID}
        r = g["r"]
        def shells(v2):
            return np.diff(np.concatenate([[0.0], r * v2 / G_KPC]))
        self.dMg = shells(g["vgas"] * np.abs(g["vgas"]))
        self.dMd = shells(g["vdisk"] ** 2)
        self.dMb = shells(g["vbul"] ** 2)

    def v(self, s, yd, yb, fd, amp=None):
        """Fractional rotation curve. Distance factor fd: r -> fd r, masses -> fd^2 M,
        kernel homogeneous of degree 2s-4 in r."""
        dM = (self.dMg + yd * self.dMd + yb * self.dMb) * fd**2
        Mb = max(float(dM.sum()), 1e-3)
        if amp is None:
            if abs(s - 1.0) < 1e-9:
                amp = 1.0
            else:
                rM = sqrt(G_KPC * Mb / A0_K)
                amp = rM ** (2 - 2 * s) / C_s(s)
        gacc = G_KPC * amp * fd ** (2 * s - 4) * (self.K[s] @ dM)
        return np.sqrt(np.clip(gacc * self.g["r"] * fd, 1e-12, None))


def prior(g, yd, yb, fd):
    p = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2
    if g["has_bulge"]:
        p += ((yb - YB_MEAN) / YB_STD) ** 2
    return p


def fit_tier1(G, vfun):
    g = G.g
    nb = 1 + (1 if g["has_bulge"] else 0)
    def f(t):
        yd, fd = t[0], t[-1]
        yb = t[1] if g["has_bulge"] else 0.0
        return chi2(g, vfun(yd, yb, fd), prior(g, yd, yb, fd))
    x0 = [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0]
    b = [(0.01, 5)] * nb + [(0.5, 2.0)]
    r = minimize(f, x0, bounds=b, method="L-BFGS-B")
    return float(r.fun), nb + 1


def summarize(per_chi2, per_nf, per_n):
    red = np.array([c / max(n - k, 1) for c, k, n in zip(per_chi2, per_nf, per_n)])
    return {
        "median_reduced_chi2": float(np.median(red)),
        "mean_reduced_chi2": float(np.mean(red)),
        "frac_under_2": int(np.sum(red < 2)),
        "aggregate_chi2_per_dof": float(sum(per_chi2) / max(sum(per_n) - sum(per_nf), 1)),
        "total_free_params": int(sum(per_nf)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--out", default="FRACTIONAL_GRAVITY_SWEEP.json")
    a = ap.parse_args()
    gals = [Gal(g) for g in load(resolve_sparc_dir(a.data_dir))]
    npts = [len(G.g["r"]) for G in gals]
    print(f"{len(gals)} galaxies, {sum(npts)} points, a0 = {A0_HORIZON:.4e} m/s^2")
    res = {"a0_derived_SI": A0_HORIZON, "n_galaxies": len(gals), "n_points": sum(npts)}

    # Newton-limit self-check on the first galaxy
    G0 = gals[0]
    vN = np.sqrt(np.clip(G0.g["vgas"] * np.abs(G0.g["vgas"]) + 0.5 * G0.g["vdisk"] ** 2, 1e-12, None))
    vF = G0.v(1.0, 0.5, 0.0, 1.0)
    ok = np.abs(vN - vF) / vN
    res["newton_limit_max_rel_err_first_galaxy"] = float(ok[vN > 5].max())
    print(f"Newton-limit check (s=1): max rel err {res['newton_limit_max_rel_err_first_galaxy']:.2e}")

    for tier in (0, 1):
        print(f"\nTIER {tier}")
        # GOD reference
        c, k = [], []
        for G in gals:
            g = G.g
            if tier == 0:
                c.append(chi2(g, v_mond_like(g, A0_HORIZON, YD_MEAN, YB_MEAN if g["has_bulge"] else 0.0, 1.0))); k.append(0)
            else:
                cc, kk = fit_tier1(G, lambda yd, yb, fd, g=g: v_mond_like(g, A0_HORIZON, yd, yb, fd)); c.append(cc); k.append(kk)
        res[f"tier{tier}_GOD_mu_std"] = summarize(c, k, npts)
        print(f"  GOD mu_std       median {res[f'tier{tier}_GOD_mu_std']['median_reduced_chi2']:8.2f}  agg {res[f'tier{tier}_GOD_mu_std']['aggregate_chi2_per_dof']:8.2f}")
        # universal order scan
        scan = {}
        for s in S_GRID:
            c, k = [], []
            for G in gals:
                g = G.g
                if tier == 0:
                    c.append(chi2(g, G.v(s, YD_MEAN, YB_MEAN if g["has_bulge"] else 0.0, 1.0))); k.append(0)
                else:
                    cc, kk = fit_tier1(G, lambda yd, yb, fd, G=G, s=s: G.v(s, yd, yb, fd)); c.append(cc); k.append(kk)
            scan[str(s)] = summarize(c, k, npts)
            print(f"  FRAC s={s:4.2f}      median {scan[str(s)]['median_reduced_chi2']:8.2f}  agg {scan[str(s)]['aggregate_chi2_per_dof']:8.2f}", flush=True)
        res[f"tier{tier}_FRAC_universal_scan"] = scan
        best = min(scan, key=lambda s: scan[s]["median_reduced_chi2"])
        res[f"tier{tier}_FRAC_best_s_by_median"] = float(best)

    # per-galaxy free order (tier-1 nuisance + free s + free amplitude)
    print("\nPER-GALAXY FREE ORDER")
    rows = []
    for G in gals:
        g = G.g
        best = None
        for s in S_GRID:
            for la in np.linspace(-3, 3, 25):
                def vf(yd, yb, fd, s=s, la=la, G=G):
                    dM = (G.dMg + yd * G.dMd + yb * G.dMb) * fd**2
                    Mb = max(float(dM.sum()), 1e-3)
                    amp0 = 1.0 if abs(s - 1) < 1e-9 else sqrt(G_KPC * Mb / A0_K) ** (2 - 2 * s) / C_s(s)
                    return G.v(s, yd, yb, fd, amp=amp0 * 10**la)
                cc, kk = fit_tier1(G, vf)
                if best is None or cc < best[0]:
                    best = (cc, s, la, kk)
        rows.append({"name": g["name"], "chi2": best[0], "s": best[1], "log10_amp_over_derived": best[2],
                     "n": len(g["r"]), "k": best[3] + 2})
    s_arr = np.array([r["s"] for r in rows]); la_arr = np.array([r["log10_amp_over_derived"] for r in rows])
    res["per_galaxy_free"] = {
        "s_median": float(np.median(s_arr)), "s_p16": float(np.percentile(s_arr, 16)), "s_p84": float(np.percentile(s_arr, 84)),
        "s_hist": {str(s): int(np.sum(s_arr == s)) for s in S_GRID},
        "log10_amp_over_derived_median": float(np.median(la_arr)),
        "log10_amp_p16_p84": [float(np.percentile(la_arr, 16)), float(np.percentile(la_arr, 84))],
        "summary": summarize([r["chi2"] for r in rows], [r["k"] for r in rows], [r["n"] for r in rows]),
        "rows": rows,
    }
    pg = res["per_galaxy_free"]
    print(f"  s median {pg['s_median']:.2f}  [16-84%: {pg['s_p16']:.2f}, {pg['s_p84']:.2f}]  amp/derived median 10^{pg['log10_amp_over_derived_median']:.2f}")
    print(f"  median chi2_red {pg['summary']['median_reduced_chi2']:.2f}")
    Path(a.out).write_text(json.dumps(res, indent=1))
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
