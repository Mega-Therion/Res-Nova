#!/usr/bin/env python3
"""
Canonical 5-Fold Cross-Validation for Derived mu(x) = x / (1 + x)
Work Order D4 - Pre-Registered Execution
Author: Ryan W. Yett / Mega-Therion / Chyren Sovereign Intelligence
Date: 2026-08-14
"""

import json
import numpy as np
from pathlib import Path
from sparc_paths import resolve_sparc_dir

try:
    SPARC_DIR = resolve_sparc_dir()
except FileNotFoundError:
    SPARC_DIR = Path(__file__).resolve().parent / "sparc_data"

OUT_DIR = Path(__file__).resolve().parents[1] / "VERIFICATION_RUN_003" / "02_sparc"

def load_galaxy(fpath):
    data = []
    with open(fpath, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 6:
                try:
                    rad = float(parts[0])
                    vobs = float(parts[1])
                    verr = float(parts[2])
                    vgas = float(parts[3])
                    vdisk = float(parts[4])
                    vbulge = float(parts[5]) if len(parts) > 5 else 0.0
                    if verr > 0:
                        data.append((rad, vobs, verr, vgas, vdisk, vbulge))
                except ValueError:
                    continue
    return np.array(data)

def predict_v_derived(rad, vgas, vdisk, vbulge, a0, Yd, Yb=0.7, fd=1.0):
    kpc_to_m = 3.085677581491367e19
    km_to_m = 1000.0
    r_m = rad * kpc_to_m * fd
    v_bary_sq = np.abs(vgas)*vgas + Yd * np.abs(vdisk)*vdisk + Yb * np.abs(vbulge)*vbulge
    v_bary_sq = np.maximum(v_bary_sq, 0.0) * (km_to_m**2)
    r_safe = np.maximum(r_m, 1e16)
    g_bar = v_bary_sq / r_safe
    ratio = np.where(g_bar > 0, a0 / g_bar, 0.0)
    g_tot = g_bar * (0.5 + np.sqrt(0.25 + ratio))
    v_tot_m = np.sqrt(np.maximum(g_tot * r_m, 0.0))
    return v_tot_m / km_to_m

def eval_galaxy(g_data, a0, Yd, Yb=0.7, fd=1.0):
    rad = g_data[:, 0]
    vobs = g_data[:, 1]
    verr = g_data[:, 2]
    vgas = g_data[:, 3]
    vdisk = g_data[:, 4]
    vbulge = g_data[:, 5]
    v_pred = predict_v_derived(rad, vgas, vdisk, vbulge, a0, Yd, Yb, fd)
    chi2 = np.sum(((vobs - v_pred) / verr)**2)
    return chi2, len(rad)

def run_cv():
    files = sorted(list(SPARC_DIR.glob('*_rotmod.dat')))
    galaxies = []
    for f in files:
        g = load_galaxy(f)
        if len(g) >= 3:
            galaxies.append((f.stem.replace('_rotmod',''), g))
            
    n_galaxies = len(galaxies)
    k = 5
    # Deterministic split (identical to legacy run)
    np.random.seed(42)
    indices = np.random.permutation(n_galaxies)
    folds = np.array_split(indices, k)
    
    fold_results = []
    out_of_sample_chi2_per_pt = []
    total_out_chi2 = 0.0
    total_out_pts = 0
    
    for fold_idx in range(k):
        test_idx = folds[fold_idx]
        train_idx = np.setdiff1d(np.arange(n_galaxies), test_idx)
        
        train_gals = [galaxies[i] for i in train_idx]
        test_gals = [galaxies[i] for i in test_idx]
        
        # Train: fit global a0 on training set
        def obj_train_a0(a0_val):
            tot_c2 = 0.0
            for name, g in train_gals:
                has_b = np.max(g[:, 5]) > 0
                yb = 0.7 if has_b else 0.0
                def obj_yd(yd):
                    c2, _ = eval_galaxy(g, a0_val, yd, Yb=yb)
                    return c2 + ((yd - 0.5)/0.125)**2
                res = minimize_scalar(obj_yd, bounds=(0.05, 2.5), method='bounded')
                c2_data, _ = eval_galaxy(g, a0_val, res.x, Yb=yb)
                tot_c2 += c2_data
            return tot_c2
            
        res_a0 = minimize_scalar(obj_train_a0, bounds=(0.5e-10, 3.0e-10), method='bounded')
        trained_a0 = float(res_a0.x)
        
        # Test: evaluate on test galaxies using fixed population priors (Ydisk=0.5, Ybulge=0.7)
        test_chi2_list = []
        fold_out_chi2 = 0.0
        fold_out_pts = 0
        for name, g in test_gals:
            has_b = np.max(g[:, 5]) > 0
            yb = 0.7 if has_b else 0.0
            c2_test, n_pts = eval_galaxy(g, trained_a0, Yd=0.5, Yb=yb)
            test_chi2_list.append(c2_test / n_pts)
            out_of_sample_chi2_per_pt.append(c2_test / n_pts)
            fold_out_chi2 += c2_test
            fold_out_pts += n_pts
            
        total_out_chi2 += fold_out_chi2
        total_out_pts += fold_out_pts
        
        fold_results.append({
            "fold": fold_idx + 1,
            "train_size": len(train_gals),
            "test_size": len(test_gals),
            "trained_a0_ms2": trained_a0,
            "test_median_chi2_per_pt": float(np.median(test_chi2_list)),
            "test_aggregate_chi2_dof": float(fold_out_chi2 / fold_out_pts)
        })
        
    cv_summary = {
        "work_order": "D4_5_Fold_Cross_Validation",
        "date": "2026-08-14",
        "closure": "Derived mu(x) = x / (1 + x)",
        "folds": fold_results,
        "aggregate_out_of_sample": {
            "median_chi2_per_point": float(np.median(out_of_sample_chi2_per_pt)),
            "mean_chi2_per_point": float(np.mean(out_of_sample_chi2_per_pt)),
            "aggregate_chi2_dof": float(total_out_chi2 / total_out_pts),
            "total_out_points": total_out_pts
        }
    }
    
    (OUT_DIR / 'SPARC_DERIVED_CV_REPORT.json').write_text(json.dumps(cv_summary, indent=2))
    print("\n=== 5-FOLD CROSS VALIDATION COMPLETE ===")
    print(json.dumps(cv_summary, indent=2))

if __name__ == '__main__':
    run_cv()
