import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import json

# Physical Constants
G = 6.67430e-11          # m^3 kg^-1 s^-2
M_sun = 1.9884e30        # kg
Mpc = 3.085677581e22     # m
a0 = 1.0557e-10          # m s^-2
mu = 1.0 / (0.9895 * Mpc)# m^-1  (~3.272e-23 m^-1)

# 12-Cluster Sample Data from TARGET_D10_CLUSTERS.md Table
clusters = [
    {'name': 'RX-J1347.5-1145', 'z': 0.451, 'M500': 22.20, 'fgas': 0.100, 'r500': 1.71, 'R_pure_MOND': 2.86},
    {'name': 'ABELL-1763',      'z': 0.228, 'M500': 16.01, 'fgas': 0.212, 'r500': 1.67, 'R_pure_MOND': 1.75},
    {'name': 'CL-J1226.9+3332', 'z': 0.890, 'M500': 15.30, 'fgas': 0.040, 'r500': 1.27, 'R_pure_MOND': 4.70},
    {'name': 'ABELL-1689',      'z': 0.183, 'M500': 15.03, 'fgas': 0.156, 'r500': 1.67, 'R_pure_MOND': 1.98},
    {'name': 'MACS-J0717.5+3745','z': 0.548, 'M500': 14.84, 'fgas': 0.170, 'r500': 1.44, 'R_pure_MOND': 2.16},
    {'name': 'ABELL-773',       'z': 0.217, 'M500': 10.14, 'fgas': 0.116, 'r500': 1.44, 'R_pure_MOND': 2.17},
    {'name': 'ABELL-209',       'z': 0.206, 'M500': 9.61,  'fgas': 0.146, 'r500': 1.42, 'R_pure_MOND': 1.92},
    {'name': 'ABELL-2142',      'z': 0.091, 'M500': 8.78,  'fgas': 0.158, 'r500': 1.44, 'R_pure_MOND': 1.76},
    {'name': 'RXC-J0532.9-3701','z': 0.275, 'M500': 6.55,  'fgas': 0.141, 'r500': 1.22, 'R_pure_MOND': 1.89},
    {'name': 'ABELL-383',       'z': 0.187, 'M500': 5.87,  'fgas': 0.121, 'r500': 1.22, 'R_pure_MOND': 1.93},
    {'name': 'ABELL-2034',      'z': 0.113, 'M500': 5.17,  'fgas': 0.073, 'r500': 1.20, 'R_pure_MOND': 2.31},
    {'name': 'RXC-J0232.2-4420','z': 0.284, 'M500': 4.44,  'fgas': 0.123, 'r500': 1.07, 'R_pure_MOND': 1.89},
]

# Response functions v(uE)
def v_pure_mond(uE):
    uE_safe = np.maximum(uE, 0.0)
    return np.sqrt(a0 * uE_safe)

def v_full_interp(uE):
    uE_safe = np.maximum(uE, 0.0)
    return (uE_safe + np.sqrt(uE_safe**2 + 4.0 * a0 * uE_safe)) / 2.0

# 1) First-Order Perturbative Expansion Calculation
def compute_first_order_expansion(c):
    M500_kg = c['M500'] * 1e14 * M_sun
    r500_m = c['r500'] * Mpc
    fbary = c['fgas'] + 0.015
    Mbary_kg = fbary * M500_kg
    W0 = G * Mbary_kg
    r_min = 1e-4 * Mpc

    # Analytical unperturbed MOND potential with Phi(r500) = 0
    # Phi_0(r) = -G Mbary / r - sqrt(a0 G Mbary) * ln(r500_m / r)
    # W1(r500) = W0 - mu^2 \int_{r_min}^{r500} r'^2 Phi_0(r') dr'
    # \int_{r_min}^{r500} (-G Mbary r' - sqrt(a0 G Mbary) r'^2 ln(r500/r')) dr'
    # \int r'^2 ln(r500/r') dr' = [r'^3/3 ln(r500/r') + r'^3/9]_{r_min}^{r500} = r500^3 / 9
    term1 = -G * Mbary_kg * (r500_m**2 - r_min**2) / 2.0
    term2 = -np.sqrt(a0 * G * Mbary_kg) * (r500_m**3 / 9.0)
    integral_phi = term1 + term2
    
    W1_500 = W0 - mu**2 * integral_phi
    exp_param = (W1_500 / W0) - 1.0  # W1/W0 - 1

    # Effective acceleration at r500
    uE_500 = W1_500 / r500_m**2
    
    # Pure MOND branch
    v_pure = np.sqrt(a0 * uE_500)
    g_pure = uE_500 + v_pure
    Mdyn_pure = g_pure * r500_m**2 / G
    R_pure_1st = M500_kg / Mdyn_pure

    # Full Interp branch
    v_interp = (uE_500 + np.sqrt(uE_500**2 + 4.0 * a0 * uE_500)) / 2.0
    g_interp = uE_500 + v_interp
    Mdyn_interp = g_interp * r500_m**2 / G
    R_interp_1st = M500_kg / Mdyn_interp

    return {
        'R_pure_1st': R_pure_1st,
        'R_interp_1st': R_interp_1st,
        'W_W0_ratio': W1_500 / W0,
        'exp_param': exp_param
    }

# 2) Full Non-linear BVP Shooting Solver
def solve_nonlinear_bvp(c, v_func, r_max_factor):
    M500_kg = c['M500'] * 1e14 * M_sun
    r500_m = c['r500'] * Mpc
    r_max_m = r_max_factor * r500_m
    fbary = c['fgas'] + 0.015
    Mbary_kg = fbary * M500_kg
    W0 = G * Mbary_kg
    r_min = 1e-4 * Mpc

    def odes(r, y):
        Phi, W = y[0], y[1]
        uE = W / (r**2)
        v_val = float(v_func(np.array([uE]))[0])
        dPhi_dr = uE + v_val
        dW_dr = - mu**2 * (r**2) * Phi
        return [dPhi_dr, dW_dr]

    def shoot_err(p):
        sol = solve_ivp(odes, (r_min, r_max_m), [p, W0], method='RK45', rtol=1e-8, atol=1e-10)
        if sol.status != 0:
            return 1e15
        return sol.y[0, -1]

    # Bracket search around analytical guess
    p_center = -G * Mbary_kg / r_min - np.sqrt(a0 * G * Mbary_kg) * np.log(r_max_m / r_min)
    ps = np.linspace(p_center * 5.0, p_center * 0.05, 300)
    errs = [shoot_err(p) for p in ps]

    root_p = None
    for i in range(len(ps)-1):
        if errs[i] * errs[i+1] <= 0 and abs(errs[i]) < 1e14 and abs(errs[i+1]) < 1e14:
            try:
                root_p = brentq(shoot_err, ps[i], ps[i+1])
                break
            except Exception:
                pass

    if root_p is None:
        return None

    # Detailed integration out to max(r500_m, r_max_m)
    r_eval_max = max(r500_m, r_max_m)
    sol = solve_ivp(odes, (r_min, r_eval_max), [root_p, W0], method='DOP853', rtol=1e-10, atol=1e-12, dense_output=True)

    # Evaluate at r500
    y_500 = sol.sol(r500_m)
    Phi_500, W_500 = y_500[0], y_500[1]
    uE_500 = W_500 / (r500_m**2)
    v_500 = float(v_func(np.array([uE_500]))[0])
    g_500 = uE_500 + v_500
    Mdyn_500 = g_500 * (r500_m**2) / G
    R_500 = M500_kg / Mdyn_500

    # Evaluate at 0.54 r500
    r_054 = 0.54 * r500_m
    y_054 = sol.sol(r_054)
    Phi_054, W_054 = y_054[0], y_054[1]
    uE_054 = W_054 / (r_054**2)
    v_054 = float(v_func(np.array([uE_054]))[0])
    g_054 = uE_054 + v_054
    Mdyn_054 = g_054 * (r_054**2) / G
    R_054 = M500_kg / Mdyn_054

    return {
        'root_p': root_p,
        'R_500': R_500,
        'W_500_ratio': W_500 / W0,
        'Mdyn_500_1014': Mdyn_500 / (1e14 * M_sun),
        'R_054': R_054,
        'W_054_ratio': W_054 / W0,
        'Mdyn_054_1014': Mdyn_054 / (1e14 * M_sun)
    }

# Run execution
print("=== RUNNING FULL D10 HELMHOLTZ CLUSTER SOLVER ===")

results_summary = []

for c in clusters:
    exp_res = compute_first_order_expansion(c)
    caseA_pure = solve_nonlinear_bvp(c, v_pure_mond, r_max_factor=1.0)
    caseA_interp = solve_nonlinear_bvp(c, v_full_interp, r_max_factor=1.0)
    caseB_pure = solve_nonlinear_bvp(c, v_pure_mond, r_max_factor=0.54)
    caseB_interp = solve_nonlinear_bvp(c, v_full_interp, r_max_factor=0.54)
    
    results_summary.append({
        'cluster': c['name'],
        'z': c['z'],
        'M500': c['M500'],
        'fgas': c['fgas'],
        'r500': c['r500'],
        'R_pure_MOND': c['R_pure_MOND'],
        '1st_order': {
            'R_pure': exp_res['R_pure_1st'],
            'R_interp': exp_res['R_interp_1st'],
            'W_W0': exp_res['W_W0_ratio'],
            'exp_param': exp_res['exp_param']
        },
        'caseA_rmax_r500': {
            'R_500_pure': caseA_pure['R_500'] if caseA_pure else None,
            'R_054_pure': caseA_pure['R_054'] if caseA_pure else None,
            'R_500_interp': caseA_interp['R_500'] if caseA_interp else None,
            'R_054_interp': caseA_interp['R_054'] if caseA_interp else None,
        },
        'caseB_rmax_r054': {
            'R_500_pure': caseB_pure['R_500'] if caseB_pure else None,
            'R_054_pure': caseB_pure['R_054'] if caseB_pure else None,
            'R_500_interp': caseB_interp['R_500'] if caseB_interp else None,
            'R_054_interp': caseB_interp['R_054'] if caseB_interp else None,
        }
    })

# Print Full Comparison Table
print("\nTABLE: 12-Cluster Comparison Across Solves")
print(f"{'Cluster':18s} | {'Pure MOND':10s} | {'1st-Ord Pure':12s} | {'1st-Ord Interp':14s} | {'Full Nonlin (r500)':18s} | {'Full Nonlin (0.54r500)':20s}")
print(f"{'':18s} | {'R_500':10s} | {'R_500':12s} | {'R_500':14s} | {'R_500 (p/i)':18s} | {'R_054 (p/i)':20s}")
print("-" * 105)

for r in results_summary:
    p_mond = f"{r['R_pure_MOND']:10.2f}"
    o1_p = f"{r['1st_order']['R_pure']:12.2f}"
    o1_i = f"{r['1st_order']['R_interp']:14.2f}"
    
    cA_p = r['caseA_rmax_r500']['R_500_pure']
    cA_i = r['caseA_rmax_r500']['R_500_interp']
    cA_str = f"{cA_p:.2f} / {cA_i:.2f}" if cA_p and cA_i else "FAILED"
    
    cB_p = r['caseB_rmax_r054']['R_054_pure']
    cB_i = r['caseB_rmax_r054']['R_054_interp']
    cB_str = f"{cB_p:.2f} / {cB_i:.2f}" if cB_p and cB_i else "FAILED"
    
    print(f"{r['cluster']:18s} | {p_mond} | {o1_p} | {o1_i} | {cA_str:18s} | {cB_str:20s}")

# Compute Medians and Means
pure_mond_list = [r['R_pure_MOND'] for r in results_summary]
o1_pure_list = [r['1st_order']['R_pure'] for r in results_summary]
o1_interp_list = [r['1st_order']['R_interp'] for r in results_summary]
exp_param_list = [r['1st_order']['exp_param'] for r in results_summary]

cA_500_pure_list = [r['caseA_rmax_r500']['R_500_pure'] for r in results_summary if r['caseA_rmax_r500']['R_500_pure'] is not None]
cA_500_interp_list = [r['caseA_rmax_r500']['R_500_interp'] for r in results_summary if r['caseA_rmax_r500']['R_500_interp'] is not None]
cA_054_pure_list = [r['caseA_rmax_r500']['R_054_pure'] for r in results_summary if r['caseA_rmax_r500']['R_054_pure'] is not None]
cA_054_interp_list = [r['caseA_rmax_r500']['R_054_interp'] for r in results_summary if r['caseA_rmax_r500']['R_054_interp'] is not None]

cB_500_pure_list = [r['caseB_rmax_r054']['R_500_pure'] for r in results_summary if r['caseB_rmax_r054']['R_500_pure'] is not None]
cB_500_interp_list = [r['caseB_rmax_r054']['R_500_interp'] for r in results_summary if r['caseB_rmax_r054']['R_500_interp'] is not None]
cB_054_pure_list = [r['caseB_rmax_r054']['R_054_pure'] for r in results_summary if r['caseB_rmax_r054']['R_054_pure'] is not None]
cB_054_interp_list = [r['caseB_rmax_r054']['R_054_interp'] for r in results_summary if r['caseB_rmax_r054']['R_054_interp'] is not None]

print("-" * 105)
print(f"{'MEDIAN':18s} | {np.median(pure_mond_list):10.2f} | {np.median(o1_pure_list):12.2f} | {np.median(o1_interp_list):14.2f} | {np.median(cA_500_pure_list):.2f} / {np.median(cA_500_interp_list):.2f}          | {np.median(cB_054_pure_list):.2f} / {np.median(cB_054_interp_list):.2f}")
print(f"{'MEAN':18s} | {np.mean(pure_mond_list):10.2f} | {np.mean(o1_pure_list):12.2f} | {np.mean(o1_interp_list):14.2f} | {np.mean(cA_500_pure_list):.2f} / {np.mean(cA_500_interp_list):.2f}          | {np.mean(cB_054_pure_list):.2f} / {np.mean(cB_054_interp_list):.2f}")
print(f"Median First-Order Expansion Parameter (W/W0 - 1) = {np.median(exp_param_list):.2f}")

# Save JSON results to shared workspace
with open('d10_results.json', 'w') as f:
    json.dump({
        'summary': {
            'pure_mond_median_R500': float(np.median(pure_mond_list)),
            'first_order_pure_median_R500': float(np.median(o1_pure_list)),
            'first_order_interp_median_R500': float(np.median(o1_interp_list)),
            'first_order_expansion_param_median': float(np.median(exp_param_list)),
            'nonlin_caseA_pure_median_R500': float(np.median(cA_500_pure_list)),
            'nonlin_caseA_interp_median_R500': float(np.median(cA_500_interp_list)),
            'nonlin_caseA_pure_median_R054': float(np.median(cA_054_pure_list)),
            'nonlin_caseA_interp_median_R054': float(np.median(cA_054_interp_list)),
            'nonlin_caseB_pure_median_R054': float(np.median(cB_054_pure_list)),
            'nonlin_caseB_interp_median_R054': float(np.median(cB_054_interp_list)),
            'nonlin_caseB_pure_median_R500': float(np.median(cB_500_pure_list)),
            'nonlin_caseB_interp_median_R500': float(np.median(cB_500_interp_list)),
        },
        'clusters': results_summary
    }, f, indent=2)

print("\nResults saved to d10_results.json")
