#!/usr/bin/env python3
"""
SPARC Derived mu(x) = x / (1 + x) Benchmark vs Legacy Control
Author: Ryan W. Yett / Res-Nova Program
Date: 2026-08-14

Evaluates:
1. Strict Zero-Parameter Derived mu: mu = x / (1 + x), a0 = cH0/(2pi) = 1.042e-10 m/s^2, Ydisk=1.0, Ybulge=1.0, fd=1.0
2. Semi-Empirical 2-Parameter Model: mu = x / (1 + x), Ydisk fitted per galaxy (prior 0.5 +/- 0.125), a0 global search / fit
3. Legacy Control comparison: mu = x / sqrt(1 + x^2) [legacy 144.04]
"""

import os
import json
import argparse
import numpy as np
from pathlib import Path
from scipy.optimize import minimize, minimize_scalar
from sparc_paths import resolve_sparc_dir


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


def predict_v(rad, vgas, vdisk, vbulge, a0, Yd, Yb=0.7, fd=1.0, mu_type='derived'):
    # Convert km/s and kpc to SI
    kpc_to_m = 3.085677581491367e19
    km_to_m = 1000.0
    
    r_m = rad * kpc_to_m * fd
    # Baryonic velocity squared
    v_bary_sq = np.abs(vgas)*vgas + Yd * np.abs(vdisk)*vdisk + Yb * np.abs(vbulge)*vbulge
    v_bary_sq = np.maximum(v_bary_sq, 0.0) * (km_to_m**2)
    
    # Newtonian baryonic acceleration
    # Avoid div by zero
    r_safe = np.maximum(r_m, 1e16)
    g_bar = v_bary_sq / r_safe
    
    # Invert mu(g/a0) * g = g_bar
    if mu_type == 'derived':
        # mu(x) = x / (1 + x) => g * (g/a0)/(1 + g/a0) = g_bar => g^2 - g_bar * g - g_bar * a0 = 0
        # g = g_bar * (1/2 + sqrt(1/4 + a0 / g_bar))
        ratio = np.where(g_bar > 0, a0 / g_bar, 0.0)
        g_tot = g_bar * (0.5 + np.sqrt(0.25 + ratio))
    elif mu_type == 'legacy':
        # For standard mu: mu(x) = x/sqrt(1+x^2), g = sqrt(g_bar^2/2 + sqrt(g_bar^4/4 + g_bar^2 * a0^2))
        g_tot = np.sqrt(0.5 * g_bar**2 + np.sqrt(0.25 * g_bar**4 + (g_bar**2) * (a0**2)))
    
    v_tot_m = np.sqrt(np.maximum(g_tot * r_m, 0.0))
    v_tot_kms = v_tot_m / km_to_m
    return v_tot_kms


def eval_galaxy(g_data, a0, Yd, Yb=0.7, fd=1.0, mu_type='derived'):
    rad = g_data[:, 0]
    vobs = g_data[:, 1]
    verr = g_data[:, 2]
    vgas = g_data[:, 3]
    vdisk = g_data[:, 4]
    vbulge = g_data[:, 5]
    
    v_pred = predict_v(rad, vgas, vdisk, vbulge, a0, Yd, Yb, fd, mu_type)
    chi2 = np.sum(((vobs - v_pred) / verr)**2)
    return chi2, len(rad)


def run_benchmark(data_dir=None, out_path=None):
    sparc_dir = resolve_sparc_dir(data_dir)
    files = sorted(list(sparc_dir.glob('*_rotmod.dat')))
    galaxies = []
    total_pts = 0
    for f in files:
        g = load_galaxy(f)
        if len(g) >= 3:
            galaxies.append((f.stem.replace('_rotmod',''), g))
            total_pts += len(g)
            
    print(f"Loaded {len(galaxies)} valid SPARC galaxies with {total_pts} total points from {sparc_dir}.")
    
    # 1. Strict Zero-Parameter Derived mu: a0 = 1.042e-10, Yd=1.0, Yb=1.0, fd=1.0
    a0_zero = 1.042e-10
    chi2_zero_list = []
    for name, g in galaxies:
        c2, n = eval_galaxy(g, a0_zero, Yd=1.0, Yb=1.0, fd=1.0, mu_type='derived')
        chi2_zero_list.append(c2 / n)
    
    median_zero = np.median(chi2_zero_list)
    agg_zero = np.sum([eval_galaxy(g, a0_zero, 1.0, 1.0, 1.0, 'derived')[0] for _, g in galaxies]) / total_pts
    
    # 2. Fit global a0 with Ydisk fitted per galaxy (with prior Yd ~ N(0.5, 0.125^2))
    def objective_a0(log_a0):
        a0_val = 10**log_a0
        tot_chi2 = 0.0
        for name, g in galaxies:
            has_bulge = np.max(g[:, 5]) > 0
            yb = 0.7 if has_bulge else 0.0
            
            def obj_yd(yd):
                c2, _ = eval_galaxy(g, a0_val, yd, Yb=yb, fd=1.0, mu_type='derived')
                prior_pen = ((yd - 0.5)/0.125)**2
                return c2 + prior_pen
                
            res = minimize_scalar(obj_yd, bounds=(0.05, 2.5), method='bounded')
            c2_data, _ = eval_galaxy(g, a0_val, res.x, Yb=yb, fd=1.0, mu_type='derived')
            tot_chi2 += c2_data
        return tot_chi2

    print("Optimizing global a0 with per-galaxy fitted Ydisk...")
    res_a0 = minimize_scalar(objective_a0, bounds=(-11.0, -9.0), method='bounded')
    best_a0 = 10**res_a0.x
    
    # Compute per-galaxy stats for best a0
    chi2_2par_list = []
    total_2par_chi2 = 0.0
    yd_fits = {}
    
    for name, g in galaxies:
        has_bulge = np.max(g[:, 5]) > 0
        yb = 0.7 if has_bulge else 0.0
        def obj_yd(yd):
            c2, _ = eval_galaxy(g, best_a0, yd, Yb=yb, fd=1.0, mu_type='derived')
            return c2 + ((yd - 0.5)/0.125)**2
        res = minimize_scalar(obj_yd, bounds=(0.05, 2.5), method='bounded')
        c2_data, n = eval_galaxy(g, best_a0, res.x, Yb=yb, fd=1.0, mu_type='derived')
        chi2_2par_list.append(c2_data / n)
        total_2par_chi2 += c2_data
        yd_fits[name] = float(res.x)
        
    n_params_2par = len(galaxies) + 1 # 175 Ydisk + 1 global a0 = 176 params
    dof_nom_2par = total_pts - n_params_2par
    
    median_2par = np.median(chi2_2par_list)
    agg_2par = total_2par_chi2 / dof_nom_2par
    
    # 3. Legacy Control: Standard MOND mu = x / sqrt(1 + x^2) with standard a0 = 1.2e-10, Yd=1.0
    chi2_legacy_list = []
    for name, g in galaxies:
        c2, n = eval_galaxy(g, 1.2e-10, Yd=1.0, Yb=1.0, fd=1.0, mu_type='legacy')
        chi2_legacy_list.append(c2 / n)
    median_legacy = np.median(chi2_legacy_list)
    agg_legacy = np.sum([eval_galaxy(g, 1.2e-10, 1.0, 1.0, 1.0, 'legacy')[0] for _, g in galaxies]) / total_pts

    results = {
        "n_galaxies": len(galaxies),
        "n_points": total_pts,
        "derived_zero_param": {
            "mu_function": "mu(x) = x / (1 + x) [Derived D1]",
            "a0": a0_zero,
            "median_chi2_per_point": float(median_zero),
            "aggregate_chi2_dof": float(agg_zero)
        },
        "derived_2parameter_global_a0": {
            "mu_function": "mu(x) = x / (1 + x) [Derived D1]",
            "best_a0_ms2": float(best_a0),
            "n_params": n_params_2par,
            "nominal_dof": dof_nom_2par,
            "median_chi2_per_point": float(median_2par),
            "aggregate_chi2_nom_dof": float(agg_2par)
        },
        "legacy_control_standard_mond": {
            "mu_function": "mu(x) = x / sqrt(1 + x^2) [Standard Pythagorean MOND]",
            "a0": 1.2e-10,
            "median_chi2_per_point": float(median_legacy),
            "aggregate_chi2_dof": float(agg_legacy)
        }
    }
    
    out_file = Path(out_path) if out_path else Path(__file__).resolve().parents[1] / "VERIFICATION_RUN_002" / "02_sparc" / "SPARC_DERIVED_MU_BENCHMARK_REPORT.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, indent=2))
    print("\n=== BENCHMARK COMPLETE ===")
    print(json.dumps(results, indent=2))


def main():
    ap = argparse.ArgumentParser(description="SPARC Derived mu(x) Benchmark vs Legacy Control.")
    ap.add_argument("--data-dir", default=None, help="Path to SPARC rotmod directory")
    ap.add_argument("--out", default=None, help="Output JSON path")
    args = ap.parse_args()
    run_benchmark(args.data_dir, args.out)


if __name__ == '__main__':
    main()
