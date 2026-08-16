#!/usr/bin/env python3
"""A proper measurement of a0 from SPARC, with a systematic error budget.

Every prior attempt in this corpus quoted a single number with a single error
bar, and the error bar was statistical only. That is what produced a claimed
0.4% precision and a spurious 24.8 sigma tension: points inside one galaxy were
treated as independent when they share a distance, an inclination and an M/L.

This script does three things differently.

1. REAL per-galaxy priors, not generic ones. Distance and inclination
   uncertainties come from the published SPARC values (Lelli+2016 Table 1, via
   the unified corpus, Zenodo 10.5281/zenodo.19563417) rather than a blanket
   10%. Inclination matters more than it looks: rotation curves are deprojected
   by sin(i), so a few degrees on a face-on galaxy moves every velocity.

2. STATISTICAL error from bootstrapping over GALAXIES. The galaxy is the
   independent unit; the radial point is not.

3. A SYSTEMATIC BUDGET, which is the part that was missing entirely. Shared
   assumptions are varied one at a time and the induced shift in a0 recorded.
   More galaxies cannot shrink these, which is the whole reason a0 is not
   already pinned down.

Model (Thm 8.7 dual-channel, unchanged):
    tau(g) = 1/2 + sqrt(1/4 + a0/g);  v_pred = v_bary * sqrt(tau)

Usage:
    python3 a0_measure.py [--boot 2000] [--grid 80]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

C_LIGHT = 2.998e8
H0_KMS_MPC = 67.4
A0_HORIZON = C_LIGHT * (H0_KMS_MPC * 1000 / 3.086e22) / (2 * math.pi)
A0_MOND = 1.2e-10

KPC_TO_M = 3.086e19
KM_TO_M = 1000.0

from sparc_paths import resolve_sparc_dir, resolve_sparc_meta


def load(sparc_dir: Path, corpus_csv: Path | None = None):
    """SPARC rotation curves joined to published distance/inclination errors."""
    meta = {}
    if corpus_csv is not None and corpus_csv.is_file():
        for row in csv.DictReader(corpus_csv.open()):
            if row.get("survey") != "SPARC":
                continue

            def f(k):
                try:
                    return float(row[k])
                except (TypeError, ValueError):
                    return None

            meta[row["galaxy"]] = {
                "dist": f("distance_mpc"),
                "e_dist": f("e_distance_mpc"),
                "inc": f("inc_deg"),
                "e_inc": f("e_inc_deg"),
            }

    out = []
    for path in sorted(sparc_dir.glob("*_rotmod.dat")):
        name = path.name.replace("_rotmod.dat", "")
        rows = []
        for line in path.read_text().splitlines():
            if line.startswith("#") or not line.strip():
                continue
            p = line.split()
            if len(p) < 6:
                continue
            try:
                rows.append([float(x) for x in p[:6]])
            except ValueError:
                continue
        if len(rows) < 5:
            continue
        a = np.asarray(rows, float)
        r, vobs, verr, vgas, vdisk, vbul = a.T
        keep = (r > 0) & (verr > 0) & (vobs > 0)
        if keep.sum() < 5:
            continue

        m = meta.get(name, {})
        dist, e_dist = m.get("dist"), m.get("e_dist")
        inc, e_inc = m.get("inc"), m.get("e_inc")
        # Fall back to a 10% distance / 5 deg inclination prior only if the
        # published value is missing, and record that we did.
        frac_d = (e_dist / dist) if (dist and e_dist and dist > 0) else 0.10
        frac_d = min(max(frac_d, 0.02), 0.50)

        out.append(
            {
                "name": name,
                "r": r[keep],
                "vobs": vobs[keep],
                "verr": verr[keep],
                "vgas": vgas[keep],
                "vdisk": vdisk[keep],
                "vbul": vbul[keep],
                "has_bulge": bool(np.any(np.abs(vbul[keep]) > 0)),
                "d_frac_sigma": frac_d,
                "inc": inc if inc else 60.0,
                "e_inc": e_inc if e_inc else 5.0,
                "has_meta": bool(m),
            }
        )
    return out


def chi2(g, a0, theta, cfg):
    """chi2 + priors for one galaxy.

    theta = [Yd, (Yb), fd, di]
      fd = distance scale factor; di = inclination offset in degrees.
    Rotation curves are deprojected by sin(i), so a shift di rescales Vobs by
    sin(i)/sin(i+di). The baryonic components are intrinsic circular speeds and
    are not affected by inclination, only by distance."""
    i = 0
    yd = theta[i]
    i += 1
    yb = theta[i] if g["has_bulge"] else 0.0
    i += 1 if g["has_bulge"] else 0
    fd = theta[i]
    i += 1
    di = theta[i] if cfg["fit_inc"] else 0.0

    r = g["r"] * fd
    s = math.sqrt(fd)
    vgas, vdisk, vbul = g["vgas"] * s, g["vdisk"] * s, g["vbul"] * s

    vobs = g["vobs"]
    verr = g["verr"]
    if cfg["fit_inc"] and di != 0.0:
        i0 = math.radians(g["inc"])
        i1 = math.radians(min(max(g["inc"] + di, 5.0), 90.0))
        ratio = math.sin(i0) / math.sin(i1)
        vobs = vobs * ratio
        verr = verr * ratio

    v_bary_sq = vgas * np.abs(vgas) + yd * vdisk**2 + yb * vbul**2
    v_bary_sq = np.maximum(v_bary_sq, 1e-12)

    g_bary = (v_bary_sq * KM_TO_M**2) / (r * KPC_TO_M)
    tau = 0.5 + np.sqrt(0.25 + a0 / g_bary)
    v_pred = np.sqrt(v_bary_sq * tau)

    c = np.sum(((vobs - v_pred) / verr) ** 2)
    c += ((yd - cfg["yd_mean"]) / cfg["yd_std"]) ** 2
    c += ((fd - 1.0) / (g["d_frac_sigma"] * cfg["dist_infl"])) ** 2
    if g["has_bulge"]:
        c += ((yb - cfg["yb_mean"]) / cfg["yb_std"]) ** 2
    if cfg["fit_inc"]:
        c += (di / g["e_inc"]) ** 2
    return c


def profile(g, a0, cfg):
    x0 = [cfg["yd_mean"]]
    b = [(0.01, 5.0)]
    if g["has_bulge"]:
        x0.append(cfg["yb_mean"])
        b.append((0.01, 5.0))
    x0.append(1.0)
    b.append((0.3, 3.0))
    if cfg["fit_inc"]:
        x0.append(0.0)
        b.append((-25.0, 25.0))
    res = minimize(lambda t: chi2(g, a0, t, cfg), x0, bounds=b, method="L-BFGS-B")
    return float(res.fun)


def curves(gals, grid, cfg):
    m = np.empty((len(gals), len(grid)))
    for i, g in enumerate(gals):
        for j, a0 in enumerate(grid):
            m[i, j] = profile(g, a0, cfg)
    return m


def best(curv, grid, idx=None):
    tot = curv.sum(axis=0) if idx is None else curv[idx].sum(axis=0)
    k = int(np.argmin(tot))
    if 0 < k < len(grid) - 1:
        y0, y1, y2 = tot[k - 1], tot[k], tot[k + 1]
        den = y0 - 2 * y1 + y2
        if den > 0:
            lg = np.log10(grid)
            return float(10 ** (lg[k] + 0.5 * (y0 - y2) / den * (lg[k + 1] - lg[k])))
    return float(grid[k])


BASE = dict(
    yd_mean=0.5, yd_std=0.125, yb_mean=0.7, yb_std=0.175, dist_infl=1.0, fit_inc=True
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=None, help="Path to SPARC rotmod directory")
    ap.add_argument("--meta", default=None, help="Path to SPARC metadata CSV (corpus_flat.csv)")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--grid", type=int, default=80)
    ap.add_argument("--out", default="A0_MEASUREMENT.json")
    args = ap.parse_args()

    sparc_dir = resolve_sparc_dir(args.data_dir)
    meta_csv = resolve_sparc_meta(args.meta)
    gals = load(sparc_dir, meta_csv)
    n_meta = sum(g["has_meta"] for g in gals)
    if n_meta == 0:
        print(
            "No external metadata CSV found (SPARC_META_CSV or --meta); "
            "running with standard default priors (10% D, 5 deg inc; has_meta=false)."
        )
    print(
        f"{len(gals)} galaxies, {sum(len(g['r']) for g in gals)} points; "
        f"published D/i errors for {n_meta}"
    )

    grid = np.logspace(np.log10(3e-11), np.log10(6e-10), args.grid)

    print("baseline fit (real D/i priors, inclination floated) ...")
    cv = curves(gals, grid, BASE)
    a0 = best(cv, grid)

    rng = np.random.default_rng(20260815)
    n = len(gals)
    boots = np.array([best(cv, grid, rng.integers(0, n, n)) for _ in range(args.boot)])
    lo, hi = np.percentile(boots, [16, 84])
    stat = float((hi - lo) / 2)
    print(f"  a0 = {a0:.4e}  stat +/- {stat:.3e}")

    # --- systematic budget -------------------------------------------------
    # Each variation perturbs an assumption SHARED by every galaxy. More data
    # cannot average these away.
    variants = {
        "distance_scale_-5%": ("dist", 0.95),
        "distance_scale_+5%": ("dist", 1.05),
        "M/L_prior_0.40": ("cfg", dict(BASE, yd_mean=0.40)),
        "M/L_prior_0.60": ("cfg", dict(BASE, yd_mean=0.60)),
        "inclination_fixed": ("cfg", dict(BASE, fit_inc=False)),
        "drop_face-on_i<30": ("cut", 30.0),
    }
    sysres = {}
    for label, (kind, val) in variants.items():
        if kind == "cfg":
            a = best(curves(gals, grid, val), grid)
        elif kind == "dist":
            g2 = [dict(x) for x in gals]
            for x in g2:
                x["r"] = x["r"] * val
                s = math.sqrt(val)
                x["vgas"], x["vdisk"], x["vbul"] = (
                    x["vgas"] * s,
                    x["vdisk"] * s,
                    x["vbul"] * s,
                )
            a = best(curves(g2, grid, BASE), grid)
        else:
            sub = [x for x in gals if x["inc"] >= val]
            a = best(curves(sub, grid, BASE), grid)
        sysres[label] = {"a0": a, "shift": a - a0, "shift_pct": 100 * (a - a0) / a0}
        print(f"  {label:22s} a0={a:.4e}  shift {100*(a-a0)/a0:+.1f}%")

    # Pair the +/- variations, take half-range; keep single-sided ones whole.
    def half(p, m):
        return abs(sysres[p]["shift"] - sysres[m]["shift"]) / 2

    comps = {
        "distance_scale": half("distance_scale_+5%", "distance_scale_-5%"),
        "M/L_prior": half("M/L_prior_0.60", "M/L_prior_0.40"),
        "inclination_treatment": abs(sysres["inclination_fixed"]["shift"]),
        "sample_selection": abs(sysres["drop_face-on_i<30"]["shift"]),
    }
    syst = float(math.sqrt(sum(v**2 for v in comps.values())))
    tot = float(math.hypot(stat, syst))

    res = {
        "generated": "2026-08-15",
        "n_galaxies": len(gals),
        "n_points": int(sum(len(g["r"]) for g in gals)),
        "model": "tau(g)=1/2+sqrt(1/4+a0/g), v=v_bary*sqrt(tau)",
        "priors": "per-galaxy published SPARC distance + inclination errors; Yd~N(0.5,0.125), Yb~N(0.7,0.175)",
        "a0_best_fit": a0,
        "stat_sigma": stat,
        "stat_68CI": [float(lo), float(hi)],
        "syst_components": comps,
        "syst_sigma": syst,
        "total_sigma": tot,
        "systematic_variations": sysres,
        "a0_claimed_cH0_over_2pi": A0_HORIZON,
        "a0_mond_empirical": A0_MOND,
        "tension_claim_sigma": abs(a0 - A0_HORIZON) / tot,
        "tension_mond_sigma": abs(a0 - A0_MOND) / tot,
    }
    Path(args.out).write_text(json.dumps(res, indent=2))

    print(f"\n  a0 = {a0:.4e}  +/- {stat:.3e}(stat) +/- {syst:.3e}(syst)")
    print(f"  total +/- {tot:.3e}  ({100*tot/a0:.1f}%)")
    print(f"  cH0/2pi  {abs(a0-A0_HORIZON)/tot:.2f} sigma")
    print(f"  MOND 1.2 {abs(a0-A0_MOND)/tot:.2f} sigma")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
