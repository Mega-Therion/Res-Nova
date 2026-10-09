#!/usr/bin/env python3
"""Independent reimplementation of SPARC rotation curve fitting and reproducibility verification.

Uses a direct line-splitting code path (without regex matching) over raw SPARC *_rotmod.dat files
to independently parse inputs, compute baryon velocities and predicted rotation curves under the GOD model,
and compare output numbers against sparc_reproduce.py.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import numpy as np

C_LIGHT = 2.998e8
H0_KMS_MPC = 67.4
H0_SI = H0_KMS_MPC * 1000 / 3.086e22
KPC_TO_M = 3.086e19
KM_TO_M = 1000
A0_HORIZON = C_LIGHT * H0_SI / (2 * math.pi)

SCRIPT_DIR = Path(__file__).resolve().parent
SPARC_DIR = SCRIPT_DIR / "sparc_data"

def load_rotmod_independent(path: Path) -> dict | None:
    """Independent parser using direct line split and float conversion."""
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tokens = line.split()
        if len(tokens) < 6:
            continue
        try:
            r, vobs, verr, vgas, vdisk, vbul = [float(t) for t in tokens[:6]]
        except ValueError:
            continue
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

def v_baryon_independent(v_gas, v_disk, v_bulge, yd: float = 1.0, yb: float = 1.0) -> np.ndarray:
    vb_sq = np.maximum(v_gas * np.abs(v_gas) + (yd * v_disk)**2 + (yb * v_bulge)**2, 1e-12)
    return np.sqrt(vb_sq)

def predict_velocity_independent(v_bary: np.ndarray, r_kpc: np.ndarray, a0: float) -> np.ndarray:
    r_m = r_kpc * KPC_TO_M
    v_m = v_bary * KM_TO_M
    a_bary = v_m**2 / np.maximum(r_m, 1e-6)
    g_std = np.sqrt(0.5 * a_bary**2 + np.sqrt(0.25 * a_bary**4 + (a_bary**2) * (a0**2)))
    return v_bary * np.sqrt(np.maximum(g_std / np.maximum(a_bary, 1e-30), 0.0))

def main():
    files = sorted(SPARC_DIR.glob("*_rotmod.dat"))
    indep_records = []
    for p in files:
        g = load_rotmod_independent(p)
        if g is None:
            continue
        vb = v_baryon_independent(g["v_gas"], g["v_disk"], g["v_bulge"])
        vp = predict_velocity_independent(vb, g["r"], A0_HORIZON)
        chi2 = float(np.sum(((g["v_obs"] - vp) / g["v_err"])**2))
        chi2_red = chi2 / g["n_points"]
        indep_records.append({
            "id": g["id"],
            "n_points": g["n_points"],
            "v_pred": vp,
            "chi2_red_god": chi2_red
        })
    
    # Load repo pipeline output
    import sparc_reproduce as sr
    repo_galaxies = sr.load_galaxies(SPARC_DIR)
    repo_records = []
    for g in repo_galaxies:
        vb = sr.v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], 1.0, 1.0)
        vp = sr.predict_velocity(vb, g["r"], A0_HORIZON)
        chi2_red = sr.strict_chi2_reduced(g, A0_HORIZON)
        repo_records.append({
            "id": g["id"],
            "n_points": g["n_points"],
            "v_pred": vp,
            "chi2_red_god": chi2_red
        })
    
    assert len(indep_records) == len(repo_records) == 175
    
    v_pred_indep = np.concatenate([r["v_pred"] for r in indep_records])
    v_pred_repo = np.concatenate([r["v_pred"] for r in repo_records])
    
    c2_indep = np.array([r["chi2_red_god"] for r in indep_records])
    c2_repo = np.array([r["chi2_red_god"] for r in repo_records])
    
    max_diff_vp = float(np.max(np.abs(v_pred_indep - v_pred_repo)))
    corr_vp = float(np.corrcoef(v_pred_indep, v_pred_repo)[0, 1])
    
    max_diff_c2 = float(np.max(np.abs(c2_indep - c2_repo)))
    corr_c2 = float(np.corrcoef(c2_indep, c2_repo)[0, 1])
    
    report = {
        "n_galaxies": len(indep_records),
        "n_total_points": int(len(v_pred_indep)),
        "max_abs_diff_v_pred_km_s": max_diff_vp,
        "pearson_corr_v_pred": corr_vp,
        "max_abs_diff_chi2_red": max_diff_c2,
        "pearson_corr_chi2_red": corr_c2,
        "agreement": max_diff_vp == 0 and max_diff_c2 == 0
    }
    
    out_file = SCRIPT_DIR / "SPARC_RECOMPUTE_VERIFICATION.json"
    out_file.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"Wrote verification report to {out_file}")

if __name__ == "__main__":
    main()
