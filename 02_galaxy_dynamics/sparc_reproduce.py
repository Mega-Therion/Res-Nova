#!/usr/bin/env python3
"""Reproduce SPARC rotation-curve fits for the Law of G.O.D. master manuscript.

Data: SPARC Rotmod_LTG (Lelli+2016c) *_rotmod.dat files.
Strict mode: fixed a0 = c*H0/(2*pi), chirally-derived tau interpolation (Thm 8.7), zero per-galaxy params.
  tau(g) = 1/2 + sqrt(1/4 + a0/g); v_pred = v_bary * sqrt(tau). See DERIVATION_MU_INTERPOLATION__8_7.md.
Nuisance mode: per-galaxy fit of disk M/L (Yd), bulge M/L (Yb if bulge), distance scale (fd)
  with Gaussian priors matching standard SPARC practice (see script docstring in output JSON).

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

SCRIPT_DIR = Path(__file__).resolve().parent


def _resolve_sparc_data() -> Path:
    """Portable search: env, package-local, then monorepo-relative — no host-absolute default."""
    import os

    env = os.environ.get("SPARC_DATA") or os.environ.get("ARS_MAGNA_SPARC_DATA")
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p
    candidates = [
        SCRIPT_DIR / "sparc_data",
        SCRIPT_DIR.parent / "data" / "sparc_data",
        SCRIPT_DIR.parent.parent / "data" / "sparc_data",
        SCRIPT_DIR.parent.parent.parent / "data" / "sparc_data",
    ]
    for c in candidates:
        if c.is_dir() and any(c.glob("*_rotmod.dat")):
            return c
    # Last resort: empty path forces clear argparse error if missing
    return candidates[0]


DEFAULT_DATA = _resolve_sparc_data()


def load_rotmod(path: Path) -> dict | None:
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        nums = re.findall(r"\d+\.\d+", line)
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
    return np.sqrt(v_gas**2 + (yd * v_disk) ** 2 + (yb * v_bulge) ** 2)


def predict_velocity(v_bary: np.ndarray, r_kpc: np.ndarray, a0: float, fd: float = 1.0) -> np.ndarray:
    """GOD strict prediction: v_pred = v_bary * sqrt(tau), tau = 1/2 + sqrt(1/4 + a0/g_N).

    This is Theorem 8.7C (DERIVATION_MU_INTERPOLATION__8_7.md). Acceleration enters
    linearly in tau; velocity gets sqrt(tau). fd rescales radius only (nuisance tier).
    """
    r_m = r_kpc * KPC_TO_M / fd
    v_m = v_bary * KM_TO_M
    a_bary = v_m**2 / np.maximum(r_m, 1e-6)
    nu = 0.5 + np.sqrt(0.25 + a0 / np.maximum(a_bary, 1e-30))
    return v_bary * np.sqrt(np.maximum(nu, 0.0))


def chi2_data(v_obs, v_model, v_err) -> float:
    return float(np.sum(((v_obs - v_model) / v_err) ** 2))


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

    for g in galaxies:
        s_god = strict_chi2_reduced(g, A0_HORIZON)
        s_mond = strict_chi2_reduced(g, A0_MOND)
        strict_god.append(s_god)
        strict_mond.append(s_mond)
        fit = fit_nuisance(g, A0_HORIZON)
        nuisance_god.append(fit["chi2_reduced"])
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
                "Yd_fit": round(fit["yd"], 3),
                "Yb_fit": round(fit["yb"], 3),
                "fd_fit": round(fit["fd"], 3),
                "RMS_pct_strict": round(point_rms_pct(g, vp), 2),
                "a0_m_s2": f"{A0_HORIZON:.6e}",
            }
        )

    from datetime import date

    summary = {
        "generated": date.today().isoformat(),
        "data_dir": str(args.data_dir),
        "n_galaxies": len(galaxies),
        "a0_horizon_m_s2": A0_HORIZON,
        "a0_mond_empirical_m_s2": A0_MOND,
        "strict_GOD": summarize(strict_god),
        "strict_MOND": summarize(strict_mond),
        "nuisance_GOD": summarize(nuisance_god),
        "note": (
            "Strict: fixed a0, unit M/L, no distance rescaling. "
            "Nuisance: per-galaxy Yd, Yb (if bulge), fd with Gaussian priors; "
            "reduced chi2 = chi2_data/(N - Nfree)."
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