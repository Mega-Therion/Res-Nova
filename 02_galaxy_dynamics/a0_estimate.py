#!/usr/bin/env python3
"""What a0 does the SPARC data actually prefer?

Three prior answers existed in the corpus and disagreed:
  claimed  a0 = cH0/2pi = 1.042e-10 m/s^2
  CV report               1.455e-10
  run manifest            0.950e-10  (+/- 3.7e-13, quoted as 24.8 sigma tension)

The manifest's error bar implies 0.4% precision on a0 from 3,391 rotation-curve
points. That is not credible: SPARC points within a galaxy share distance,
inclination, and M/L systematics, so they are nowhere near independent. Treating
them as independent is what manufactures a 24.8 sigma result.

This script fixes three things:
  1. Per-galaxy nuisance parameters (Yd, Yb, fd) are profiled out at every a0,
     rather than fixed at values fit under a different a0.
  2. The error bar comes from bootstrapping over GALAXIES, not points. A galaxy
     is the independent unit here; a point is not.
  3. The 5-fold cross-validation retrains a0 inside each fold. The prior CV
     reported an identical a0 to 16 significant figures across all five folds,
     which means it was fit once on everything and reused - the parameter under
     test leaked into every test set.

Model (unchanged, Thm 8.7 dual-channel):
    tau(g) = 1/2 + sqrt(1/4 + a0/g)
    v_pred = v_bary * sqrt(tau)

Usage:
    python3 a0_estimate.py [--data-dir DIR] [--out PATH] [--boot N]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

C_LIGHT = 2.998e8
H0_KMS_MPC = 67.4
H0_SI = H0_KMS_MPC * 1000 / 3.086e22
A0_HORIZON = C_LIGHT * H0_SI / (2 * math.pi)

KPC_TO_M = 3.086e19
KM_TO_M = 1000.0

# Standard SPARC priors (Lelli+2016, McGaugh+2016 conventions).
YD_MEAN, YD_STD = 0.5, 0.125
YB_MEAN, YB_STD = 0.7, 0.175
FD_MEAN, FD_STD = 1.0, 0.10


def load_galaxies(data_dir: Path):
    """Read *_rotmod.dat into per-galaxy arrays. Vgas may be negative (inflow
    convention); square it signed, as standard SPARC practice does."""
    out = []
    for path in sorted(data_dir.glob("*_rotmod.dat")):
        rows = []
        for line in path.read_text().splitlines():
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            try:
                rows.append([float(x) for x in parts[:6]])
            except ValueError:
                continue
        if len(rows) < 4:  # need enough points to constrain 2-3 nuisance params
            continue
        a = np.asarray(rows, dtype=float)
        r, vobs, verr, vgas, vdisk, vbul = a.T
        keep = (r > 0) & (verr > 0) & (vobs > 0)
        if keep.sum() < 4:
            continue
        out.append(
            {
                "name": path.name.replace("_rotmod.dat", ""),
                "r": r[keep],
                "vobs": vobs[keep],
                "verr": verr[keep],
                "vgas": vgas[keep],
                "vdisk": vdisk[keep],
                "vbul": vbul[keep],
                "has_bulge": bool(np.any(np.abs(vbul[keep]) > 0)),
            }
        )
    return out


def chi2_galaxy(g, a0, theta):
    """chi2 for one galaxy at given a0 and nuisance vector theta.

    fd rescales distance: radii scale as fd, velocities as sqrt(fd)."""
    yd = theta[0]
    yb = theta[1] if g["has_bulge"] else 0.0
    fd = theta[-1]

    r = g["r"] * fd
    scale = math.sqrt(fd)
    vgas = g["vgas"] * scale
    vdisk = g["vdisk"] * scale
    vbul = g["vbul"] * scale

    v_bary_sq = vgas * np.abs(vgas) + yd * vdisk**2 + yb * vbul**2
    v_bary_sq = np.maximum(v_bary_sq, 1e-12)

    # g_bary in SI
    g_bary = (v_bary_sq * KM_TO_M**2) / (r * KPC_TO_M)
    tau = 0.5 + np.sqrt(0.25 + a0 / g_bary)
    v_pred = np.sqrt(v_bary_sq * tau)

    chi2 = np.sum(((g["vobs"] - v_pred) / g["verr"]) ** 2)

    prior = ((yd - YD_MEAN) / YD_STD) ** 2 + ((fd - FD_MEAN) / FD_STD) ** 2
    if g["has_bulge"]:
        prior += ((yb - YB_MEAN) / YB_STD) ** 2
    return chi2 + prior


def profile_galaxy(g, a0):
    """Minimise over this galaxy's nuisance parameters at fixed a0."""
    if g["has_bulge"]:
        x0, bounds = [YD_MEAN, YB_MEAN, FD_MEAN], [(0.01, 5), (0.01, 5), (0.5, 2.0)]
    else:
        x0, bounds = [YD_MEAN, FD_MEAN], [(0.01, 5), (0.5, 2.0)]
    res = minimize(
        lambda t: chi2_galaxy(g, a0, t), x0, bounds=bounds, method="L-BFGS-B"
    )
    return float(res.fun)


def chi2_curves(galaxies, grid):
    """chi2_g(a0) for every galaxy on the a0 grid.

    Computed once. Bootstrapping then just resamples rows of this matrix, which
    is what makes 2000 resamples affordable."""
    m = np.empty((len(galaxies), len(grid)))
    for i, g in enumerate(galaxies):
        for j, a0 in enumerate(grid):
            m[i, j] = profile_galaxy(g, a0)
    return m


def argmin_a0(curves, grid, idx=None):
    tot = curves.sum(axis=0) if idx is None else curves[idx].sum(axis=0)
    k = int(np.argmin(tot))
    # Parabolic refinement between neighbouring grid points.
    if 0 < k < len(grid) - 1:
        y0, y1, y2 = tot[k - 1], tot[k], tot[k + 1]
        denom = y0 - 2 * y1 + y2
        if denom > 0:
            shift = 0.5 * (y0 - y2) / denom
            lg = np.log10(grid)
            step = lg[k + 1] - lg[k]
            return float(10 ** (lg[k] + shift * step))
    return float(grid[k])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--data-dir",
        default="/home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data",
    )
    ap.add_argument("--out", default="A0_ESTIMATE.json")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--grid", type=int, default=60)
    args = ap.parse_args()

    galaxies = load_galaxies(Path(args.data_dir))
    print(
        f"loaded {len(galaxies)} galaxies, {sum(len(g['r']) for g in galaxies)} points"
    )

    grid = np.logspace(np.log10(3e-11), np.log10(6e-10), args.grid)
    print(f"profiling nuisance params over {args.grid}-point a0 grid ...")
    curves = chi2_curves(galaxies, grid)

    a0_hat = argmin_a0(curves, grid)
    print(f"global best-fit a0 = {a0_hat:.4e}")

    # Bootstrap over galaxies - the independent unit.
    rng = np.random.default_rng(20260815)
    n = len(galaxies)
    boots = np.empty(args.boot)
    for b in range(args.boot):
        boots[b] = argmin_a0(curves, grid, rng.integers(0, n, n))
    lo, hi = np.percentile(boots, [16, 84])
    sigma = float((hi - lo) / 2)
    print(f"bootstrap a0 = {np.median(boots):.4e}  68% CI [{lo:.4e}, {hi:.4e}]")

    # Honest 5-fold CV: a0 retrained on each training split.
    order = rng.permutation(n)
    folds = np.array_split(order, 5)
    cv = []
    for i, test in enumerate(folds):
        train = np.concatenate([f for j, f in enumerate(folds) if j != i])
        a0_tr = argmin_a0(curves, grid, train)
        # Test chi2 per point at the training-set a0.
        tot_chi2 = tot_pts = 0.0
        per_gal = []
        for gi in test:
            c = profile_galaxy(galaxies[gi], a0_tr)
            npts = len(galaxies[gi]["r"])
            per_gal.append(c / npts)
            tot_chi2 += c
            tot_pts += npts
        cv.append(
            {
                "fold": i + 1,
                "trained_a0": a0_tr,
                "test_median_chi2_per_point": float(np.median(per_gal)),
                "test_aggregate_chi2_per_point": float(tot_chi2 / tot_pts),
            }
        )
        print(
            f"  fold {i+1}: a0={a0_tr:.4e}  test median chi2/pt={np.median(per_gal):.2f}"
        )

    tension = abs(a0_hat - A0_HORIZON) / sigma if sigma > 0 else float("nan")

    result = {
        "generated": "2026-08-15",
        "n_galaxies": len(galaxies),
        "n_points": int(sum(len(g["r"]) for g in galaxies)),
        "model": "tau(g) = 1/2 + sqrt(1/4 + a0/g), v = v_bary*sqrt(tau)",
        "method": (
            "Per-galaxy Yd/Yb/fd profiled at every a0; a0 from total chi2 minimum; "
            "uncertainty from 68% bootstrap over galaxies (not points); "
            "5-fold CV with a0 retrained per fold."
        ),
        "a0_claimed_cH0_over_2pi": A0_HORIZON,
        "a0_mond_empirical": 1.2e-10,
        "a0_best_fit": a0_hat,
        "a0_bootstrap_median": float(np.median(boots)),
        "a0_68CI": [float(lo), float(hi)],
        "a0_sigma": sigma,
        "tension_with_claim_sigma": float(tension),
        "cross_validation": cv,
        "cv_trained_a0_distinct": len({round(c["trained_a0"], 18) for c in cv}),
    }
    Path(args.out).write_text(json.dumps(result, indent=2))
    print(f"\na0 = {a0_hat:.4e}  +/- {sigma:.3e}   ({tension:.1f} sigma from cH0/2pi)")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
