#!/usr/bin/env python3
"""Parameter-accounting ledger: like-for-like at matched parameter counts.

The corpus has always compared fit quality. That concedes the wrong scoreboard.
The question that actually discriminates is: how many numbers does each
framework have to be TOLD, and where do they come from?

The prior comparison was also not like-for-like. strict_MOND existed, but no one
ever ran MOND or an NFW halo under the SAME per-galaxy nuisance treatment that
produced the 2.88 headline. Comparing a 0-parameter version of one model to a
382-parameter version of another is not a comparison.

Frameworks, at two matched parameter budgets:

  TIER 0 - no per-galaxy freedom (M/L fixed at 0.5, distance fixed, a0 fixed)
    GOD   mu(x) = x/(1+x),  a0 = cH0/2pi        DERIVED       0 params
    MOND  mu(x) = x/(1+x),  a0 = 1.2e-10        FITTED (lit)  0 params here
    (NFW cannot run at tier 0 - a halo without parameters is not a halo. That
     absence is itself a ledger entry.)

  TIER 1 - per-galaxy nuisance (Yd, Yb if bulge, fd), Gaussian priors
    GOD   + 0 shape params
    MOND  + 0 shape params (a0 still from literature)
    NFW   + 2 shape params per galaxy (c, V200)

Usage:
    python3 parameter_ledger.py [--out PARAMETER_LEDGER.json]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from sparc_paths import resolve_sparc_dir

C_LIGHT = 2.998e8
H0_SI = 67.4 * 1000 / 3.086e22
A0_HORIZON = C_LIGHT * H0_SI / (2 * math.pi)
A0_MOND = 1.2e-10

KPC_TO_M = 3.086e19
KM_TO_M = 1000.0
G_SI = 6.674e-11
MSUN = 1.989e30

try:
    SPARC_DIR = resolve_sparc_dir()
except FileNotFoundError:
    SPARC_DIR = Path("sparc_data")

YD_MEAN, YD_STD = 0.5, 0.125
YB_MEAN, YB_STD = 0.7, 0.175
FD_STD = 0.10


def load(d: Path):
    out = []
    for p in sorted(d.glob("*_rotmod.dat")):
        rows = []
        for line in p.read_text().splitlines():
            if line.startswith("#") or not line.strip():
                continue
            q = line.split()
            if len(q) < 6:
                continue
            try:
                rows.append([float(x) for x in q[:6]])
            except ValueError:
                continue
        if len(rows) < 5:
            continue
        a = np.asarray(rows, float)
        r, vobs, verr, vgas, vdisk, vbul = a.T
        k = (r > 0) & (verr > 0) & (vobs > 0)
        if k.sum() < 5:
            continue
        out.append(
            dict(
                name=p.name.replace("_rotmod.dat", ""),
                r=r[k],
                vobs=vobs[k],
                verr=verr[k],
                vgas=vgas[k],
                vdisk=vdisk[k],
                vbul=vbul[k],
                has_bulge=bool(np.any(np.abs(vbul[k]) > 0)),
            )
        )
    return out


def v_bary_sq(g, yd, yb, fd):
    s = math.sqrt(fd)
    vg, vd, vb = g["vgas"] * s, g["vdisk"] * s, g["vbul"] * s
    return np.maximum(vg * np.abs(vg) + yd * vd**2 + yb * vb**2, 1e-12)


def v_mond_like(g, a0, yd, yb, fd):
    """Shared functional form: tau = 1/2 + sqrt(1/4 + a0/g_bary).

    This is the dual-channel mu(x)=x/(1+x) branch. GOD and MOND differ here ONLY
    in where a0 comes from - derived vs fitted - which is the entire point."""
    vb2 = v_bary_sq(g, yd, yb, fd)
    r = g["r"] * fd
    gb = (vb2 * KM_TO_M**2) / (r * KPC_TO_M)
    return np.sqrt(vb2 * (0.5 + np.sqrt(0.25 + a0 / gb)))


def v_nfw(g, yd, yb, fd, c, v200):
    """Newtonian baryons + NFW halo. c = concentration, v200 in km/s."""
    vb2 = v_bary_sq(g, yd, yb, fd)
    r = g["r"] * fd
    # r200 from v200 (H0 = 67.4): r200 [kpc] = v200 / (10 h) with h=0.674
    r200 = v200 / (10 * 0.674)
    x = np.maximum(r / r200, 1e-6)
    mu = lambda t: np.log(1 + t) - t / (1 + t)
    vh2 = v200**2 * (mu(c * x) / x) / mu(c)
    return np.sqrt(np.maximum(vb2 + vh2, 1e-12))


def chi2(g, vpred, extra_prior=0.0):
    return float(np.sum(((g["vobs"] - vpred) / g["verr"]) ** 2) + extra_prior)


def fit_galaxy(g, model, a0=None, tier=1):
    """Return (chi2, n_free, n_points)."""
    npts = len(g["r"])

    if tier == 0:
        v = v_mond_like(g, a0, YD_MEAN, YB_MEAN if g["has_bulge"] else 0.0, 1.0)
        return chi2(g, v), 0, npts

    nb = 1 + (1 if g["has_bulge"] else 0)  # Yd (+Yb)

    if model in ("GOD", "MOND"):

        def f(t):
            yd, fd = t[0], t[-1]
            yb = t[1] if g["has_bulge"] else 0.0
            pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2
            if g["has_bulge"]:
                pr += ((yb - YB_MEAN) / YB_STD) ** 2
            return chi2(g, v_mond_like(g, a0, yd, yb, fd), pr)

        x0 = [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0]
        b = [(0.01, 5)] * nb + [(0.5, 2.0)]
        r = minimize(f, x0, bounds=b, method="L-BFGS-B")
        return float(r.fun), nb + 1, npts

    # NFW: same nuisance + 2 halo shape parameters
    def f(t):
        yd = t[0]
        yb = t[1] if g["has_bulge"] else 0.0
        fd, c, v200 = t[-3], t[-2], t[-1]
        pr = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - 1) / FD_STD) ** 2
        if g["has_bulge"]:
            pr += ((yb - YB_MEAN) / YB_STD) ** 2
        return chi2(g, v_nfw(g, yd, yb, fd, c, v200), pr)

    best = None
    for c0, v0 in ((10.0, 100.0), (5.0, 200.0), (15.0, 50.0)):
        x0 = [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0, c0, v0]
        b = [(0.01, 5)] * nb + [(0.5, 2.0), (1.0, 100.0), (10.0, 500.0)]
        r = minimize(f, x0, bounds=b, method="L-BFGS-B")
        if best is None or r.fun < best:
            best = float(r.fun)
    return best, nb + 3, npts


def run(gals, model, a0, tier):
    per, tot_chi2, tot_free, tot_pts = [], 0.0, 0, 0
    for g in gals:
        c, nf, npts = fit_galaxy(g, model, a0=a0, tier=tier)
        dof = max(npts - nf, 1)
        per.append(c / dof)
        tot_chi2 += c
        tot_free += nf
        tot_pts += npts
    per = np.array(per)
    return {
        "median_reduced_chi2": float(np.median(per)),
        "mean_reduced_chi2": float(np.mean(per)),
        "frac_under_1": int(np.sum(per < 1)),
        "frac_under_2": int(np.sum(per < 2)),
        "total_free_params": int(tot_free),
        "total_points": int(tot_pts),
        "aggregate_chi2_per_dof": float(tot_chi2 / max(tot_pts - tot_free, 1)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=None, help="Path to SPARC rotmod directory")
    ap.add_argument("--out", default="PARAMETER_LEDGER.json")
    args = ap.parse_args()

    sparc_dir = resolve_sparc_dir(args.data_dir)
    gals = load(sparc_dir)
    print(f"{len(gals)} galaxies, {sum(len(g['r']) for g in gals)} points\n")

    res = {}
    print("TIER 0 - zero per-galaxy freedom")
    for name, a0 in (("GOD", A0_HORIZON), ("MOND", A0_MOND)):
        r = run(gals, name, a0, tier=0)
        res[f"tier0_{name}"] = r
        print(
            f"  {name:5s} a0={a0:.3e}  median={r['median_reduced_chi2']:7.2f}  "
            f"free={r['total_free_params']:4d}  <1:{r['frac_under_1']:3d}"
        )

    print("\nTIER 1 - per-galaxy nuisance (Yd, Yb, fd), matched")
    for name, a0 in (("GOD", A0_HORIZON), ("MOND", A0_MOND), ("NFW", None)):
        r = run(gals, name, a0, tier=1)
        res[f"tier1_{name}"] = r
        print(
            f"  {name:5s} median={r['median_reduced_chi2']:7.2f}  "
            f"free={r['total_free_params']:4d}  <1:{r['frac_under_1']:3d}  "
            f"agg={r['aggregate_chi2_per_dof']:.2f}"
        )

    res["provenance"] = {
        "GOD_a0": "DERIVED, cH0/2pi (horizon argument), epistemic tag [O]",
        "MOND_a0": "FITTED to rotation curves in the literature (1.2e-10)",
        "GOD_interpolation": "DERIVED, Thm 8.7 dual-channel mu(x)=x/(1+x)",
        "MOND_interpolation": "CHOSEN by hand; several variants in use",
        "NFW_halo": "2 FITTED shape params per galaxy (c, V200)",
        "shared_nuisance": "Yd, Yb, fd - observational unknowns, not model params; identical across all three",
    }
    Path(args.out).write_text(json.dumps(res, indent=2))
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
