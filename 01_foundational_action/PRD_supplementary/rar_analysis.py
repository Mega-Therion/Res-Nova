#!/usr/bin/env python3
"""
Parameter-free vs Marginalized YC vs SPARC:
RAR, full-curve chi2, BIC, and figure generation.
Supports both fixed M/L (0 free parameters) and optimized M/L (marginalized).
"""
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import minimize

# Paths
SUB_DIR = Path(__file__).parent
DATA_PATH = SUB_DIR.parent.parent.parent/"experiments/lab/calibration-engine/data/sparc_fortress.json"
FIG_DIR = SUB_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

# Load data
d = json.load(open(DATA_PATH))

# Constants
c = 2.99792458e8              # m/s
H0_PLANCK = 67.4              # km/s/Mpc
H0_SI = H0_PLANCK * 1e3 / 3.0857e22 # s^-1
A0_YC = c * H0_SI / (2 * math.pi) # m/s^2  (cH0/2pi)
A0_MOND = 1.2e-10             # m/s^2  (empirical MOND)
KPC = 3.0857e19               # m
KM = 1e3                      # m/s

def interp(ab, a0):
    """Interpolating function: simple MOND form."""
    return ab * (0.5 + math.sqrt(0.25 + a0 / ab)) if ab > 0 else 0.0

# -----------------------------------------------------------------------------
# 1. RUN ANALYSIS (FIXED vs OPTIMIZED)
# -----------------------------------------------------------------------------

# We will collect data for all galaxies
galaxies_data = []

for g in d['galaxies']:
    pts = [p for p in g.get('rotation_curve', []) if p.get('v_obs', 0) > 0 and p.get('r_kpc', 0) > 0]
    if len(pts) < 3:
        continue
    
    # Check if this galaxy has a bulge component
    has_bulge = any(p.get('v_bulge', 0) > 0 for p in pts)
    galaxies_data.append({
        'id': g['id'],
        'pts': pts,
        'has_bulge': has_bulge,
        'h_disk_kpc': g.get('h_disk_kpc', 1.0)
    })

print(f"Loaded {len(galaxies_data)} galaxies with valid rotation curves.")

# Let's define functions to run the analysis
def run_analysis(optimize_ml=False):
    gobs_all = []
    gbar_all = []
    
    # Store per-point predictions and errors for chi2 calculation
    chi2 = {'YC': 0.0, 'MOND': 0.0, 'BARY': 0.0}
    ok = {'YC': 0, 'MOND': 0}
    N = 0
    
    # Save optimized parameters if applicable
    opt_params = {}
    
    for g in galaxies_data:
        pts = g['pts']
        has_bulge = g['has_bulge']
        n = len(pts)
        
        # Loss function for M/L optimization
        def get_chi2_gal(params, a0, is_bary=False):
            ud = params[0]
            ub = params[1] if has_bulge else 0.0
            val = 0.0
            for p in pts:
                r = p['r_kpc']*KPC
                vo = p['v_obs']*KM
                ve = max(p.get('v_err', 0) or 0, 3)*KM
                vg = p.get('v_gas', 0)*KM
                vd = p.get('v_disk', 0)*KM
                vb = p.get('v_bulge', 0)*KM
                
                vbar2 = vg*abs(vg) + ud*vd*vd + ub*vb*vb
                vbar = math.sqrt(vbar2) if vbar2 > 0 else 0.0
                ab = vbar*vbar/r if r > 0 else 0.0
                
                if is_bary:
                    vpred = vbar
                else:
                    vpred = math.sqrt(interp(ab, a0)*r) if ab > 0 else 0.0
                val += ((vo - vpred)/ve)**2
            return val
        
        # Determine best M/L parameters
        if optimize_ml:
            bounds = [(0.1, 2.0)]
            if has_bulge:
                bounds.append((0.1, 2.0))
                init_guess = [0.5, 0.7]
            else:
                init_guess = [0.5]
                
            res_yc = minimize(lambda p: get_chi2_gal(p, A0_YC), init_guess, bounds=bounds, method='L-BFGS-B')
            res_mond = minimize(lambda p: get_chi2_gal(p, A0_MOND), init_guess, bounds=bounds, method='L-BFGS-B')
            res_bary = minimize(lambda p: get_chi2_gal(p, 0.0, is_bary=True), init_guess, bounds=bounds, method='L-BFGS-B')
            
            p_yc = res_yc.x
            p_mond = res_mond.x
            p_bary = res_bary.x
            
            chi2_yc_g = res_yc.fun
            chi2_mond_g = res_mond.fun
            chi2_bary_g = res_bary.fun
            
            opt_params[g['id']] = {
                'YC': (p_yc[0], p_yc[1] if has_bulge else 0.0),
                'MOND': (p_mond[0], p_mond[1] if has_bulge else 0.0),
                'BARY': (p_bary[0], p_bary[1] if has_bulge else 0.0)
            }
        else:
            p_yc = [0.5, 0.7]
            p_mond = [0.5, 0.7]
            p_bary = [0.5, 0.7]
            chi2_yc_g = get_chi2_gal(p_yc, A0_YC)
            chi2_mond_g = get_chi2_gal(p_mond, A0_MOND)
            chi2_bary_g = get_chi2_gal(p_bary, 0.0, is_bary=True)
            
        chi2['YC'] += chi2_yc_g
        chi2['MOND'] += chi2_mond_g
        chi2['BARY'] += chi2_bary_g
        
        if chi2_yc_g / n < 5.0:
            ok['YC'] += 1
        if chi2_mond_g / n < 5.0:
            ok['MOND'] += 1
            
        # Collect accelerations for RAR
        ud_yc = p_yc[0]
        ub_yc = p_yc[1] if has_bulge else 0.0
        for p in pts:
            r = p['r_kpc']*KPC
            vo = p['v_obs']*KM
            vg = p.get('v_gas', 0)*KM
            vd = p.get('v_disk', 0)*KM
            vb = p.get('v_bulge', 0)*KM
            
            vbar2 = vg*abs(vg) + ud_yc*vd*vd + ub_yc*vb*vb
            vbar = math.sqrt(vbar2) if vbar2 > 0 else 0.0
            ab = vbar*vbar/r if r > 0 else 0.0
            
            if ab > 0:
                gobs_all.append(vo*vo/r)
                gbar_all.append(ab)
                N += 1
                
    gobs = np.array(gobs_all)
    gbar = np.array(gbar_all)
    
    # Calculate residual scatter in dex (about YC)
    gpred_yc = np.array([interp(gb, A0_YC) for gb in gbar])
    residuals_yc = np.log10(gobs) - np.log10(gpred_yc)
    median_res_yc = np.median(residuals_yc)
    rms_res_yc = np.std(residuals_yc)
    
    # Calculate residual scatter in dex (about MOND)
    gpred_mond = np.array([interp(gb, A0_MOND) for gb in gbar])
    residuals_mond = np.log10(gobs) - np.log10(gpred_mond)
    median_res_mond = np.median(residuals_mond)
    rms_res_mond = np.std(residuals_mond)
    
    return {
        'N': N,
        'chi2': chi2,
        'ok': ok,
        'gobs': gobs,
        'gbar': gbar,
        'residuals_yc': residuals_yc,
        'median_res_yc': median_res_yc,
        'rms_res_yc': rms_res_yc,
        'residuals_mond': residuals_mond,
        'median_res_mond': median_res_mond,
        'rms_res_mond': rms_res_mond,
        'opt_params': opt_params if optimize_ml else None
    }

print("\n--- Running Fixed M/L (0 free parameters) ---")
res_fixed = run_analysis(optimize_ml=False)
print(f"Points={res_fixed['N']}  galaxies={len(galaxies_data)}")
for k in ['BARY', 'YC', 'MOND']:
    print(f"  {k}: chi2={res_fixed['chi2'][k]:.0f} red={res_fixed['chi2'][k]/res_fixed['N']:.2f}")
print(f"  Acceptable: YC={res_fixed['ok']['YC']}/{len(galaxies_data)} MOND={res_fixed['ok']['MOND']}/{len(galaxies_data)}")
print(f"  YC Residual dex: median={res_fixed['median_res_yc']:.4f}, rms={res_fixed['rms_res_yc']:.4f}")

print("\n--- Running Optimized M/L (marginalized) ---")
res_opt = run_analysis(optimize_ml=True)
print(f"Points={res_opt['N']}  galaxies={len(galaxies_data)}")
for k in ['BARY', 'YC', 'MOND']:
    print(f"  {k}: chi2={res_opt['chi2'][k]:.0f} red={res_opt['chi2'][k]/res_opt['N']:.2f}")
print(f"  Acceptable: YC={res_opt['ok']['YC']}/{len(galaxies_data)} MOND={res_opt['ok']['MOND']}/{len(galaxies_data)}")
print(f"  YC Residual dex: median={res_opt['median_res_yc']:.4f}, rms={res_opt['rms_res_yc']:.4f}")

# Save data for manuscript reproducibility
np.savez(SUB_DIR / 'RAR_data.npz',
         # Fixed M/L data
         gobs_fixed=res_fixed['gobs'],
         gbar_fixed=res_fixed['gbar'],
         chi2_fixed_yc=res_fixed['chi2']['YC'],
         chi2_fixed_mond=res_fixed['chi2']['MOND'],
         chi2_fixed_bary=res_fixed['chi2']['BARY'],
         rms_fixed_yc=res_fixed['rms_res_yc'],
         ok_fixed_yc=res_fixed['ok']['YC'],
         ok_fixed_mond=res_fixed['ok']['MOND'],
         # Optimized M/L data
         gobs_opt=res_opt['gobs'],
         gbar_opt=res_opt['gbar'],
         chi2_opt_yc=res_opt['chi2']['YC'],
         chi2_opt_mond=res_opt['chi2']['MOND'],
         chi2_opt_bary=res_opt['chi2']['BARY'],
         rms_opt_yc=res_opt['rms_res_yc'],
         ok_opt_yc=res_opt['ok']['YC'],
         ok_opt_mond=res_opt['ok']['MOND'],
         a0_yc=A0_YC,
         a0_mond=A0_MOND,
         ndata=res_fixed['N'],
         ngal=len(galaxies_data))

# Save BIC comparison JSON
# k_params: LCDM NFW has ~2 parameters per galaxy = 2 * 135 (or 2 * 175 = 350)
# Let's keep the parameter counts:
# Fixed case: YC and MOND have 0 free parameters, BARY has 0. LCDM NFW has 270 (or 2*175=350)
# Optimized case: YC, MOND, and BARY have 1 or 2 parameters per galaxy (let's say average 1.25 per galaxy)
k_params_fixed = {'BARY': 0, 'YC': 0, 'MOND': 0, 'LCDM': 2 * len(galaxies_data)}
k_params_opt = {'BARY': 1.25 * len(galaxies_data), 'YC': 1.25 * len(galaxies_data), 'MOND': 1.25 * len(galaxies_data)}

bic_fixed = {
    "Baryonic (no DM)": {
        "chi2": float(res_fixed['chi2']['BARY']),
        "chi2_red": float(res_fixed['chi2']['BARY']/res_fixed['N']),
        "k_params": k_params_fixed['BARY'],
        "BIC": float(res_fixed['chi2']['BARY'] + k_params_fixed['BARY'] * math.log(res_fixed['N']))
    },
    "YC a0=cH0/2pi (fixed M/L)": {
        "chi2": float(res_fixed['chi2']['YC']),
        "chi2_red": float(res_fixed['chi2']['YC']/res_fixed['N']),
        "k_params": k_params_fixed['YC'],
        "BIC": float(res_fixed['chi2']['YC'] + k_params_fixed['YC'] * math.log(res_fixed['N']))
    },
    "MOND empirical a0 (fixed M/L)": {
        "chi2": float(res_fixed['chi2']['MOND']),
        "chi2_red": float(res_fixed['chi2']['MOND']/res_fixed['N']),
        "k_params": k_params_fixed['MOND'],
        "BIC": float(res_fixed['chi2']['MOND'] + k_params_fixed['MOND'] * math.log(res_fixed['N']))
    },
    "YC a0=cH0/2pi (optimized M/L)": {
        "chi2": float(res_opt['chi2']['YC']),
        "chi2_red": float(res_opt['chi2']['YC']/res_opt['N']),
        "k_params": k_params_opt['YC'],
        "BIC": float(res_opt['chi2']['YC'] + k_params_opt['YC'] * math.log(res_opt['N']))
    },
    "MOND empirical a0 (optimized M/L)": {
        "chi2": float(res_opt['chi2']['MOND']),
        "chi2_red": float(res_opt['chi2']['MOND']/res_opt['N']),
        "k_params": k_params_opt['MOND'],
        "BIC": float(res_opt['chi2']['MOND'] + k_params_opt['MOND'] * math.log(res_opt['N']))
    }
}

with open(SUB_DIR / 'model_comparison_BIC.json', 'w') as f:
    json.dump(bic_fixed, f, indent=2)

# -----------------------------------------------------------------------------
# 2. GENERATE FIGURES (PUBLICATION QUALITY)
# -----------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 14,
    'legend.fontsize': 10,
    'figure.dpi': 300
})

# Color palette
C_BARY = '#7f7f7f' # Gray
C_YC = '#1f77b4'   # Deep Blue
C_MOND = '#ff7f0e' # Vibrant Orange
C_DATA = '#2ca02c' # Green (points)

# --- FIG 1: Radial Acceleration Relation (Fixed vs Optimized) ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True)

# Fixed M/L Panel
ax = axes[0]
ax.scatter(np.log10(res_fixed['gbar']), np.log10(res_fixed['gobs']), 
           s=2, alpha=0.3, color=C_DATA, label='SPARC data (fixed M/L)')
gb_arr = np.logspace(-15, -8, 500)
go_yc_arr = np.array([interp(gb, A0_YC) for gb in gb_arr])
go_mond_arr = np.array([interp(gb, A0_MOND) for gb in gb_arr])

ax.plot(np.log10(gb_arr), np.log10(gb_arr), '--', color=C_BARY, label='Newtonian (No DM)')
ax.plot(np.log10(gb_arr), np.log10(go_yc_arr), '-', color=C_YC, linewidth=2, label=r'YC: $a_0 = c H_0 / 2\pi$')
ax.plot(np.log10(gb_arr), np.log10(go_mond_arr), ':', color=C_MOND, linewidth=2, label=r'MOND: $a_0 = 1.2\times 10^{-10}$')
ax.set_xlim(-14.5, -8.5)
ax.set_ylim(-14.5, -8.5)
ax.set_xlabel(r'$\log_{10}(g_{\rm bar}\,\,[\mathrm{m\,s^{-2}}])$')
ax.set_ylabel(r'$\log_{10}(g_{\rm obs}\,\,[\mathrm{m\,s^{-2}}])$')
ax.set_title('A: Zero-Parameter Model (Fixed M/L)')
ax.legend(loc='lower right', frameon=True)

# Optimized M/L Panel
ax = axes[1]
ax.scatter(np.log10(res_opt['gbar']), np.log10(res_opt['gobs']), 
           s=2, alpha=0.3, color=C_DATA, label='SPARC data (fitted M/L)')
ax.plot(np.log10(gb_arr), np.log10(gb_arr), '--', color=C_BARY)
ax.plot(np.log10(gb_arr), np.log10(go_yc_arr), '-', color=C_YC, linewidth=2)
ax.plot(np.log10(gb_arr), np.log10(go_mond_arr), ':', color=C_MOND, linewidth=2)
ax.set_xlim(-14.5, -8.5)
ax.set_xlabel(r'$\log_{10}(g_{\rm bar}\,\,[\mathrm{m\,s^{-2}}])$')
ax.set_title('B: Marginalized Model (Fitted M/L per galaxy)')
ax.legend(loc='lower right', frameon=True)

plt.tight_layout()
plt.savefig(FIG_DIR / "fig1_RAR.png", dpi=300)
plt.close()

# --- FIG 2: Residuals Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Fixed M/L Panel
ax = axes[0]
ax.hist(res_fixed['residuals_yc'], bins=40, range=(-0.6, 0.6), histtype='step', 
        color=C_YC, linewidth=2, label=f'YC (rms={res_fixed["rms_res_yc"]:.3f} dex)')
ax.hist(res_fixed['residuals_mond'], bins=40, range=(-0.6, 0.6), histtype='step', 
        color=C_MOND, linewidth=1.5, linestyle=':', label=f'MOND (rms={res_fixed["rms_res_mond"]:.3f} dex)')
ax.axvline(0, color='black', linestyle='--', alpha=0.5)
ax.set_xlabel('Residual: ' + r'$\log_{10}(g_{\rm obs}) - \log_{10}(g_{\rm pred})$')
ax.set_ylabel('Number of Points')
ax.set_title('A: Residuals with Fixed M/L')
ax.legend(loc='upper right', frameon=True)

# Optimized M/L Panel
ax = axes[1]
ax.hist(res_opt['residuals_yc'], bins=40, range=(-0.6, 0.6), histtype='step', 
        color=C_YC, linewidth=2, label=f'YC (rms={res_opt["rms_res_yc"]:.3f} dex)')
ax.hist(res_opt['residuals_mond'], bins=40, range=(-0.6, 0.6), histtype='step', 
        color=C_MOND, linewidth=1.5, linestyle=':', label=f'MOND (rms={res_opt["rms_res_mond"]:.3f} dex)')
ax.axvline(0, color='black', linestyle='--', alpha=0.5)
ax.set_xlabel('Residual: ' + r'$\log_{10}(g_{\rm obs}) - \log_{10}(g_{\rm pred})$')
ax.set_ylabel('Number of Points')
ax.set_title('B: Residuals with Fitted M/L')
ax.legend(loc='upper right', frameon=True)

plt.tight_layout()
plt.savefig(FIG_DIR / "fig2_residuals.png", dpi=300)
plt.close()

# --- FIG 3: Example rotation curves for 4 galaxies ---
# Selected galaxies: NGC 3198, NGC 2403, DDO 154, UGC 2885
target_gals = ['NGC3198', 'NGC2403', 'DDO154', 'UGC02885']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for idx, g_id in enumerate(target_gals):
    # Find galaxy in d
    gal = None
    for item in d['galaxies']:
        if item['id'] == g_id:
            gal = item
            break
    if not gal:
        continue
    
    ax = axes[idx]
    pts = [p for p in gal.get('rotation_curve', []) if p.get('v_obs', 0) > 0 and p.get('r_kpc', 0) > 0]
    
    r_arr = np.array([p['r_kpc'] for p in pts])
    vo_arr = np.array([p['v_obs'] for p in pts])
    ve_arr = np.array([max(p.get('v_err', 0) or 0, 3) for p in pts])
    
    vg_arr = np.array([p.get('v_gas', 0) for p in pts])
    vd_arr = np.array([p.get('v_disk', 0) for p in pts])
    vb_arr = np.array([p.get('v_bulge', 0) for p in pts])
    
    # Plot observations
    ax.errorbar(r_arr, vo_arr, yerr=ve_arr, fmt='o', color='black', label='Observed (SPARC)', zorder=5)
    
    # 1. Plot Newtonian Baryonic (fixed M/L)
    vbar2_fixed = vg_arr**2 + 0.5 * vd_arr**2 + 0.7 * vb_arr**2
    vbar_fixed = np.sqrt(np.maximum(vbar2_fixed, 0))
    ax.plot(r_arr, vbar_fixed, '--', color=C_BARY, label='Baryonic (Newtonian)')
    
    # 2. Plot YC (fixed M/L)
    vyc_fixed = []
    for r, vbar in zip(r_arr, vbar_fixed):
        ab = (vbar*KM)**2 / (r*KPC) if r > 0 else 0
        vyc_fixed.append(math.sqrt(interp(ab, A0_YC)*r*KPC)/KM)
    ax.plot(r_arr, vyc_fixed, '-', color=C_YC, label='YC (Fixed M/L)', linewidth=2)
    
    # 3. Plot YC (fitted M/L)
    if res_opt['opt_params'] and g_id in res_opt['opt_params']:
        ud_opt, ub_opt = res_opt['opt_params'][g_id]['YC']
        vbar2_opt = vg_arr**2 + ud_opt * vd_arr**2 + ub_opt * vb_arr**2
        vbar_opt = np.sqrt(np.maximum(vbar2_opt, 0))
        vyc_opt = []
        for r, vbar in zip(r_arr, vbar_opt):
            ab = (vbar*KM)**2 / (r*KPC) if r > 0 else 0
            vyc_opt.append(math.sqrt(interp(ab, A0_YC)*r*KPC)/KM)
        ax.plot(r_arr, vyc_opt, ':', color='#d62728', label=f'YC (Fitted: {ud_opt:.2f}/{ub_opt:.2f})', linewidth=2.5)
        
    ax.set_xlabel('Radius r (kpc)')
    ax.set_ylabel('Velocity V (km/s)')
    ax.set_title(f'Galaxy {g_id}')
    ax.legend(loc='best', frameon=True)

plt.tight_layout()
plt.savefig(FIG_DIR / "fig3_example_curves.png", dpi=300)
plt.close()

print("\n✓ Generated figures in figures/")
print("✓ Saved RAR_data.npz and model_comparison_BIC.json")
print("Done.")
