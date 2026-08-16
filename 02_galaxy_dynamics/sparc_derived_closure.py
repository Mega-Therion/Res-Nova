#!/usr/bin/env python3
"""
Canonical SPARC Re-Run with Derived Closure mu(x) = x / (1 + x)
Work Order D4 - Pre-Registered Execution
Author: Ryan W. Yett / Mega-Therion / Chyren Sovereign Intelligence
Date: 2026-08-14
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import norm

from sparc_paths import resolve_sparc_dir

try:
    SPARC_DIR = resolve_sparc_dir()
except FileNotFoundError:
    SPARC_DIR = Path(__file__).resolve().parent / "sparc_data"

OUT_DIR = Path(__file__).resolve().parents[1] / "VERIFICATION_RUN_003" / "02_sparc"
FIG_DIR = Path(__file__).resolve().parents[1] / "VERIFICATION_RUN_003" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

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
    
    # Derived closure: mu(x) = x / (1 + x) => g = g_bar * (1/2 + sqrt(1/4 + a0/g_bar))
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

def run_d4():
    files = sorted(list(SPARC_DIR.glob('*_rotmod.dat')))
    galaxies = []
    total_pts = 0
    for f in files:
        g = load_galaxy(f)
        if len(g) >= 3:
            galaxies.append((f.stem.replace('_rotmod',''), g))
            total_pts += len(g)
            
    print(f"Loaded {len(galaxies)} valid SPARC galaxies with {total_pts} total points.")
    
    # Grid scan for profile likelihood of a0 in [0.5, 3.0] x 10^-10 m/s^2
    a0_grid = np.linspace(0.5e-10, 3.0e-10, 51)
    grid_chi2 = []
    
    print("Computing a0 profile likelihood over [0.5, 3.0] x 10^-10 m/s^2...")
    for a0_val in a0_grid:
        tot_c2 = 0.0
        for name, g in galaxies:
            has_b = np.max(g[:, 5]) > 0
            yb = 0.7 if has_b else 0.0
            def obj_yd(yd):
                c2, _ = eval_galaxy(g, a0_val, yd, Yb=yb)
                return c2 + ((yd - 0.5)/0.125)**2
            res = minimize_scalar(obj_yd, bounds=(0.05, 2.5), method='bounded')
            c2_data, _ = eval_galaxy(g, a0_val, res.x, Yb=yb)
            tot_c2 += c2_data
        grid_chi2.append(tot_c2)
        
    grid_chi2 = np.array(grid_chi2)
    best_idx = np.argmin(grid_chi2)
    best_a0 = a0_grid[best_idx]
    
    # Estimate 68% confidence interval from Delta chi2 = 1.0 (or profile curvature)
    min_chi2 = grid_chi2[best_idx]
    delta_chi2 = grid_chi2 - min_chi2
    # Quadratic fit near minimum
    poly = np.polyfit(a0_grid[max(0, best_idx-5):min(len(a0_grid), best_idx+6)], 
                      grid_chi2[max(0, best_idx-5):min(len(a0_grid), best_idx+6)], 2)
    sigma_a0 = 1.0 / np.sqrt(poly[0]) if poly[0] > 0 else 0.05e-10
    
    # Full fit evaluation at best_a0
    per_galaxy_results = []
    ydisk_values = []
    total_data_chi2 = 0.0
    chi2_per_pt_list = []
    
    # Load legacy zero-param chi2 per galaxy for comparison
    for name, g in galaxies:
        has_b = np.max(g[:, 5]) > 0
        yb = 0.7 if has_b else 0.0
        def obj_yd(yd):
            c2, _ = eval_galaxy(g, best_a0, yd, Yb=yb)
            return c2 + ((yd - 0.5)/0.125)**2
        res = minimize_scalar(obj_yd, bounds=(0.05, 2.5), method='bounded')
        yd_fit = float(res.x)
        c2_data, n_pts = eval_galaxy(g, best_a0, yd_fit, Yb=yb)
        
        # Legacy zero-param chi2 for this galaxy (mu_simple = x/sqrt(1+x^2), a0=1.2e-10, Y=1.0)
        # Using legacy formula
        rad, vobs, verr, vgas, vdisk, vbulge = g[:,0], g[:,1], g[:,2], g[:,3], g[:,4], g[:,5]
        v_bary_sq_leg = np.maximum(np.abs(vgas)*vgas + np.abs(vdisk)*vdisk + (0.7 if has_b else 0.0)*np.abs(vbulge)*vbulge, 0.0)*(1000.0**2)
        r_m_leg = rad * 3.085677581491367e19
        g_bar_leg = v_bary_sq_leg / np.maximum(r_m_leg, 1e16)
        g_tot_leg = np.sqrt(0.5*g_bar_leg**2 + np.sqrt(0.25*g_bar_leg**4 + (g_bar_leg**2)*(1.2e-10**2)))
        v_pred_leg = np.sqrt(np.maximum(g_tot_leg * r_m_leg, 0.0)) / 1000.0
        c2_legacy = np.sum(((vobs - v_pred_leg)/verr)**2)
        
        per_galaxy_results.append({
            "galaxy": name,
            "n_points": n_pts,
            "fitted_Ydisk": yd_fit,
            "chi2_derived": float(c2_data),
            "chi2_per_pt_derived": float(c2_data / n_pts),
            "chi2_legacy_zeroparam": float(c2_legacy),
            "chi2_per_pt_legacy": float(c2_legacy / n_pts)
        })
        ydisk_values.append(yd_fit)
        total_data_chi2 += c2_data
        chi2_per_pt_list.append(c2_data / n_pts)
        
    ydisk_values = np.array(ydisk_values)
    median_chi2_pt = float(np.median(chi2_per_pt_list))
    n_params = len(galaxies) + 1 # 176
    dof_nom = total_pts - n_params
    agg_chi2_dof = float(total_data_chi2 / dof_nom)
    
    # Discrepancy tension against cH0/(2pi) = 1.2e-10 (approx) and 1.042e-10
    a0_cH0_2pi = 1.042e-10
    tension_sigma = abs(best_a0 - a0_cH0_2pi) / sigma_a0
    
    manifest = {
        "work_order": "D4",
        "date": "2026-08-14",
        "sample": "175 SPARC galaxies (3,391 points)",
        "model": "Derived mu(x) = x / (1 + x)",
        "fitted_parameters": {
            "a0_posterior": {
                "median_m_s2": float(best_a0),
                "sigma_m_s2": float(sigma_a0),
                "cH0_2pi_value": a0_cH0_2pi,
                "tension_sigma": float(tension_sigma)
            },
            "Ydisk_distribution": {
                "mean": float(np.mean(ydisk_values)),
                "std": float(np.std(ydisk_values)),
                "median": float(np.median(ydisk_values)),
                "prior_mean": 0.5,
                "prior_std": 0.125
            }
        },
        "statistics": {
            "n_galaxies": len(galaxies),
            "n_points": total_pts,
            "nominal_dof": dof_nom,
            "total_chi2_data": float(total_data_chi2),
            "median_chi2_per_point": median_chi2_pt,
            "aggregate_chi2_nom_dof": agg_chi2_dof
        },
        "per_galaxy_table": per_galaxy_results
    }
    
    (OUT_DIR / 'SPARC_DERIVED_RUN_MANIFEST.json').write_text(json.dumps(manifest, indent=2))
    print("Saved SPARC_DERIVED_RUN_MANIFEST.json")
    
    # =========================================================================
    # GENERATE FIGURES
    # =========================================================================
    print("Generating diagnostic Figures A, B, C...")
    
    # Figure A: Ydisk distribution vs Prior
    plt.figure(figsize=(7, 5))
    plt.hist(ydisk_values, bins=25, density=True, alpha=0.6, color='steelblue', edgecolor='black', label='Fitted $\\Upsilon_{\\mathrm{disk}}$ (175 galaxies)')
    x_axis = np.linspace(0.05, 1.2, 200)
    plt.plot(x_axis, norm.pdf(x_axis, 0.5, 0.125), 'r--', lw=2.5, label='Prior $\\mathcal{N}(0.5, 0.125^2)$')
    plt.axvline(np.mean(ydisk_values), color='blue', linestyle='-', lw=2, label=f'Fitted Mean = {np.mean(ydisk_values):.3f}')
    plt.xlabel('Stellar Mass-to-Light Ratio $\\Upsilon_{\\mathrm{disk}}$ [$M_\\odot/L_\\odot$]', fontsize=11)
    plt.ylabel('Probability Density', fontsize=11)
    plt.title('Figure A: Distribution of Fitted $\\Upsilon_{\\mathrm{disk}}$ vs. Population Prior', fontsize=12, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig_a_ydisk_distribution.png', dpi=200)
    plt.close()
    
    # Figure B: a0 Posterior / Profile Likelihood
    plt.figure(figsize=(7, 5))
    plt.plot(a0_grid * 1e10, grid_chi2 / dof_nom, 'b-', lw=2.5, label='Profile $\\chi^2_{\\mathrm{nom}}/\\mathrm{dof}$')
    plt.axvline(best_a0 * 1e10, color='blue', linestyle='--', lw=2, label=f'Best Fit $a_0 = {best_a0*1e10:.3f} \\times 10^{{-10}}\\,\\mathrm{{m/s^2}}$')
    plt.axvline(1.042, color='green', linestyle=':', lw=2.5, label='$cH_0/(2\\pi) = 1.042 \\times 10^{-10}\\,\\mathrm{m/s^2}$')
    plt.axvline(1.200, color='red', linestyle='-.', lw=2.5, label='Standard MOND $a_0 = 1.200 \\times 10^{-10}\\,\\mathrm{m/s^2}$')
    plt.xlabel('Global Acceleration Scale $a_0$ [$10^{-10}\\,\\mathrm{m/s^2}$]', fontsize=11)
    plt.ylabel('Aggregate $\\chi^2_{\\mathrm{nom}}/\\mathrm{dof}$', fontsize=11)
    plt.title('Figure B: Profile Likelihood of Global $a_0$ Scale', fontsize=12, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig_b_a0_posterior.png', dpi=200)
    plt.close()
    
    # Figure C: Per-Galaxy chi2 Scatter (Derived vs Legacy Zero-Param)
    c2_der = [p['chi2_per_pt_derived'] for p in per_galaxy_results]
    c2_leg = [p['chi2_per_pt_legacy'] for p in per_galaxy_results]
    plt.figure(figsize=(7, 5))
    plt.scatter(c2_leg, c2_der, alpha=0.7, color='darkmagenta', edgecolors='k', s=45)
    lims = [0.1, max(max(c2_der), max(c2_leg))*1.2]
    plt.plot([0.01, 1000], [0.01, 1000], 'k--', alpha=0.6, label='1:1 Line (Equality)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Legacy Zero-Param $\\chi^2/N_g$ (Assumed $\\mu_{\\mathrm{simple}}$)', fontsize=11)
    plt.ylabel('Canonical 2-Param $\\chi^2/N_g$ (Derived $\\mu_{\\mathrm{derived}}$)', fontsize=11)
    plt.title('Figure C: Per-Galaxy Residuals (Derived 2-Param vs. Legacy Zero-Param)', fontsize=12, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig_c_galaxy_residuals_scatter.png', dpi=200)
    plt.close()
    
    print("Figures saved successfully to", FIG_DIR)

if __name__ == '__main__':
    run_d4()
