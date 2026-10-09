#!/usr/bin/env python3
"""Reproduce SPARC rotation-curve fits for the Law of G.O.D. master manuscript.

Data: SPARC Rotmod_LTG (Lelli+2016c) *_rotmod.dat files.
Model: mu_std(x) = x/sqrt(1+x^2) (the live interpolating function since 2026-09-12; the
  tau(g) = 1/2 + sqrt(1/4 + a0/g) form this header described until 2026-10-09 is the inverse of the
  retired mu_dual and is not what the code computes).
Baryons (SPARC convention, Lelli+2016, and parameter_ledger.py):
  V_bar^2 = V_gas|V_gas| + Yd V_disk^2 + Yb V_bul^2   (Y multiplies V^2; negative V_gas subtracts)
  distance factor fd: V_bar^2 -> fd V_bar^2, R -> fd R, so g_bar = V_bar^2/R is distance-independent.
Strict mode: fixed a0, unit M/L (Yd = Yb = 1), fd = 1: no per-galaxy parameters. The model still
  carries the theory's two irreducible inputs: the a0 scale and the mu choice.
Nuisance mode: per-galaxy fit of Yd, Yb (if bulge) and fd with Gaussian priors N(0.5, 0.125),
  N(0.7, 0.175), N(1, 0.10) (standard SPARC practice).
Controls: baryons only (Newtonian), Yd = Yb = 1, fd = 1.

Usage:
  python3 sparc_reproduce.py
  python3 sparc_reproduce.py --data-dir /path/to/sparc_data --out-dir .
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
from pathlib import Path

import numpy as np

C_LIGHT = 2.998e8  # m/s
H0_KMS_MPC = 67.4
H0_SI = H0_KMS_MPC * 1000 / 3.086e22
KPC_TO_M = 3.086e19
KM_TO_M = 1000
A0_HORIZON = C_LIGHT * H0_SI / (2 * math.pi)
A0_MOND = 1.2e-10

from sparc_paths import resolve_sparc_dir

SCRIPT_DIR = Path(__file__).resolve().parent


def _resolve_sparc_data() -> Path:
    try:
        return resolve_sparc_dir()
    except FileNotFoundError:
        return SCRIPT_DIR / "sparc_data"


DEFAULT_DATA = _resolve_sparc_data()


def load_rotmod(path: Path) -> dict | None:
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        nums = re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", line)
        if len(nums) < 6:
            continue
        r, vobs, verr, vgas, vdisk, vbul = map(float, nums[:6])
        rows.append((r, vobs, verr, vgas, vdisk, vbul))
    if len(rows) < 3:
        return None
    arr = np.array(rows)
    r, vobs, verr, vgas, vdisk, vbul = arr.T
    mask = (r > 0) & (vobs > 0) & (verr > 0)
    vgas, vdisk, vbul = vgas[mask], vdisk[mask], vbul[mask]
    r, vobs, verr = r[mask], vobs[mask], verr[mask]
    if len(r) < 3:
        return None
    has_bulge = np.any(vbul > 0.5)
    gid = path.stem.replace("_rotmod", "")
    return {
        "id": gid,
        "r": r,
        "v_obs": vobs,
        "v_err": np.maximum(verr, 1.0),
        "v_gas": vgas,
        "v_disk": vdisk,
        "v_bulge": vbul,
        "has_bulge": bool(has_bulge),
        "n_points": int(len(r)),
    }


def v_baryon(v_gas, v_disk, v_bulge, yd: float, yb: float) -> np.ndarray:
    """V_bar at fd = 1. Y multiplies V^2 (mass-to-light scales the mass, so V^2), and a
    negative SPARC V_gas (net outward gas force) subtracts: V_gas|V_gas|. Same form as
    parameter_ledger.v_bary_sq. Until 2026-10-09 this squared (Y V)^2, which is Y^2 V^2."""
    vb_sq = np.maximum(v_gas * np.abs(v_gas) + yd * v_disk**2 + yb * v_bulge**2, 1e-12)
    return np.sqrt(vb_sq)


def predict_velocity(
    v_bary: np.ndarray, r_kpc: np.ndarray, a0: float, fd: float = 1.0
) -> np.ndarray:
    """GOD prediction using mu_std(x) = x/sqrt(1+x^2) (corrected 2026-09-12 from
    mu_dual(x)=x/(1+x), which was falsified: it leaks a constant, unscreened
    acceleration offset at every radius, not just deep-MOND, violating
    solar-system bounds by ~5.7e5x. See TARGET_D7_COVARIANT_COMPLETION.md Sec 4
    and 02_galaxy_dynamics/SPARC_MU_STD_RECOMPUTE_2026-09-12.md.

    Distance factor fd (parameter_ledger.v_mond_like): V_bar^2 -> fd V_bar^2 and R -> fd R.
    Until 2026-10-09 this divided R by fd and left V_bar unscaled. The parser sign bug noted
    here before is fixed in load_rotmod.
    """
    vb2_m = fd * (v_bary * KM_TO_M) ** 2
    r_m = r_kpc * KPC_TO_M * fd
    a_bary = vb2_m / np.maximum(r_m, 1e-6)
    g_std = np.sqrt(0.5 * a_bary**2 + np.sqrt(0.25 * a_bary**4 + (a_bary**2) * (a0**2)))
    return np.sqrt(vb2_m * np.maximum(g_std / np.maximum(a_bary, 1e-30), 0.0)) / KM_TO_M


def chi2_data(v_obs, v_model, v_err) -> float:
    return float(np.sum(((v_obs - v_model) / v_err) ** 2))


def newtonian_chi2(g: dict, yd: float = 1.0, yb: float = 1.0) -> float:
    """Baryons-only control: V_pred = V_bar at fixed M/L, fd = 1. Returns chi2_data."""
    vb = v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], yd, yb)
    return chi2_data(g["v_obs"], vb, g["v_err"])


def strict_chi2_reduced(g: dict, a0: float) -> float:
    """Strict tier: unit M/L (Yd=Yb=1), fd=1, fixed a0. No per-galaxy freedom."""
    vb = v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], 1.0, 1.0)
    vp = predict_velocity(vb, g["r"], a0)
    return chi2_data(g["v_obs"], vp, g["v_err"]) / g["n_points"]


def nuisance_chi2_total(g: dict, a0: float, yd: float, yb: float, fd: float) -> float:
    vb = v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], yd, yb)
    vp = predict_velocity(vb, g["r"], a0, fd)
    chi2 = chi2_data(g["v_obs"], vp, g["v_err"])
    # Gaussian priors (SPARC standard)
    chi2 += ((yd - 0.5) / 0.125) ** 2
    if g["has_bulge"]:
        chi2 += ((yb - 0.7) / 0.175) ** 2
    chi2 += ((fd - 1.0) / 0.10) ** 2
    return chi2


def fit_nuisance(g: dict, a0: float) -> dict:
    yd_grid = np.linspace(0.25, 1.75, 16)
    yb_grid = np.linspace(0.25, 1.75, 16) if g["has_bulge"] else [0.7]
    fd_grid = np.linspace(0.85, 1.15, 13)
    best = (1e99, 0.5, 0.7, 1.0)
    for yd in yd_grid:
        for yb in yb_grid:
            for fd in fd_grid:
                total = nuisance_chi2_total(g, a0, float(yd), float(yb), float(fd))
                if total < best[0]:
                    best = (total, float(yd), float(yb), float(fd))
    chi2_tot, yd, yb, fd = best
    nfree = 3 if g["has_bulge"] else 2
    vb = v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], yd, yb)
    vp = predict_velocity(vb, g["r"], a0, fd)
    chi2_d = chi2_data(g["v_obs"], vp, g["v_err"])
    reduced = chi2_d / max(g["n_points"] - nfree, 1)
    return {
        "yd": yd,
        "yb": yb,
        "fd": fd,
        "chi2_data": chi2_d,
        "chi2_reduced": reduced,
        "n_free": nfree,
        "v_flat_pred": float(np.nanmax(vp)),
    }


def point_rms_pct(g: dict, v_pred: np.ndarray) -> float:
    rel = (g["v_obs"] - v_pred) / np.maximum(v_pred, 1e-6)
    return float(np.sqrt(np.mean(rel**2)) * 100)


def load_galaxies(data_dir: Path) -> list[dict]:
    galaxies = []
    for path in sorted(data_dir.glob("*_rotmod.dat")):
        g = load_rotmod(path)
        if g:
            galaxies.append(g)
    return galaxies


def summarize(reduced: list[float]) -> dict:
    return {
        "n": len(reduced),
        "median": float(statistics.median(reduced)),
        "mean": float(statistics.mean(reduced)),
        "max": float(max(reduced)),
        "frac_lt_1": int(sum(r < 1 for r in reduced)),
        "frac_lt_2": int(sum(r < 2 for r in reduced)),
        "frac_lt_5": int(sum(r < 5 for r in reduced)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    ap.add_argument("--out-dir", type=Path, default=SCRIPT_DIR)
    args = ap.parse_args()

    if not args.data_dir.is_dir():
        raise SystemExit(f"SPARC data not found: {args.data_dir}")

    galaxies = load_galaxies(args.data_dir)
    if not galaxies:
        raise SystemExit("No galaxies loaded")

    rows = []
    strict_god = []
    strict_mond = []
    nuisance_god = []
    newton = []
    newton_pm = []
    agg = {"strict_GOD": [0.0, 0], "strict_MOND": [0.0, 0], "nuisance_GOD": [0.0, 0], "newtonian": [0.0, 0],
           "newtonian_prior_mean_ML": [0.0, 0]}

    for g in galaxies:
        s_god = strict_chi2_reduced(g, A0_HORIZON)
        s_mond = strict_chi2_reduced(g, A0_MOND)
        strict_god.append(s_god)
        strict_mond.append(s_mond)
        fit = fit_nuisance(g, A0_HORIZON)
        nuisance_god.append(fit["chi2_reduced"])
        n_chi2 = newtonian_chi2(g)
        newton.append(n_chi2 / g["n_points"])
        npm_chi2 = newtonian_chi2(g, 0.5, 0.7 if g["has_bulge"] else 0.0)
        newton_pm.append(npm_chi2 / g["n_points"])
        for key, c2, dof in (("strict_GOD", s_god * g["n_points"], g["n_points"]),
                             ("strict_MOND", s_mond * g["n_points"], g["n_points"]),
                             ("nuisance_GOD", fit["chi2_data"], max(g["n_points"] - fit["n_free"], 1)),
                             ("newtonian", n_chi2, g["n_points"]),
                             ("newtonian_prior_mean_ML", npm_chi2, g["n_points"])):
            agg[key][0] += c2
            agg[key][1] += dof
        vb = v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], 1.0, 1.0)
        vp = predict_velocity(vb, g["r"], A0_HORIZON)
        rows.append(
            {
                "Galaxy_ID": g["id"],
                "N_points": g["n_points"],
                "Has_bulge": int(g["has_bulge"]),
                "chi2_reduced_strict_GOD": round(s_god, 4),
                "chi2_reduced_strict_MOND": round(s_mond, 4),
                "chi2_reduced_nuisance_GOD": round(fit["chi2_reduced"], 4),
                "chi2_reduced_newtonian": round(n_chi2 / g["n_points"], 4),
                "Yd_fit": round(fit["yd"], 3),
                "Yb_fit": round(fit["yb"], 3),
                "fd_fit": round(fit["fd"], 3),
                "RMS_pct_strict": round(point_rms_pct(g, vp), 2),
                "a0_m_s2": f"{A0_HORIZON:.6e}",
            }
        )

    from datetime import date

    import hashlib

    files = sorted(args.data_dir.glob("*_rotmod.dat"))
    # Same definition as `sha256sum *_rotmod.dat | sha256sum`, which is the SHA-256 of the
    # committed VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256.
    listing = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in files)
    summary = {
        "generated": date.today().isoformat(),
        # A content digest, not the local path: the path is machine-specific (2026-10-09).
        "data": {"files": "SPARC Rotmod_LTG *_rotmod.dat (scripts/fetch_sparc.sh)",
                 "n_files": len(files),
                 "sha256_of_manifest": hashlib.sha256(listing.encode()).hexdigest()},
        "n_galaxies": len(galaxies),
        "n_points": int(sum(g["n_points"] for g in galaxies)),
        "a0_horizon_m_s2": A0_HORIZON,
        "a0_mond_empirical_m_s2": A0_MOND,
        "strict_GOD": summarize(strict_god),
        "strict_MOND": summarize(strict_mond),
        "nuisance_GOD": summarize(nuisance_god),
        "newtonian": summarize(newton),
        "newtonian_prior_mean_ML": summarize(newton_pm),
        "aggregate_chi2_per_dof": {k: v[0] / v[1] for k, v in agg.items()},
        "total_dof": {k: v[1] for k, v in agg.items()},
        "note": (
            "Strict: fixed a0, unit M/L, no distance rescaling. "
            "Nuisance: per-galaxy Yd, Yb (if bulge), fd with Gaussian priors; "
            "reduced chi2 = chi2_data/(N - Nfree). Newtonian: baryons only, unit M/L; "
            "newtonian_prior_mean_ML: baryons only at Yd = 0.5, Yb = 0.7 (0 if no bulge). "
            "V_bar^2 = V_gas|V_gas| + Yd V_disk^2 + Yb V_bul^2; fd scales V_bar^2 and R."
        ),
    }

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "SPARC_175_GOD_fits.csv"
    json_path = out_dir / "SPARC_175_summary.json"

    fieldnames = list(rows[0].keys())
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    json_path.write_text(json.dumps(summary, indent=2))

    print(json.dumps(summary, indent=2))
    print(f"\nWrote {csv_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
