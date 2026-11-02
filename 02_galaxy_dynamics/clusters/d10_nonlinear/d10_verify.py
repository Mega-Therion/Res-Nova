import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# Constants
G = 6.67430e-11 # m^3 kg^-1 s^-2
M_sun = 1.9884e30 # kg
Mpc = 3.085677581e22 # m
a0 = 1.0557e-10 # m/s^2
mu = 1.0 / (0.9895 * Mpc) # m^-1

# 12 Clusters data from TARGET_D10_CLUSTERS.md
clusters = [
    {'name': 'RX-J1347.5-1145', 'z': 0.451, 'M500': 22.20, 'fgas': 0.100, 'r500': 1.71, 'R_std': 2.86},
    {'name': 'ABELL-1763', 'z': 0.228, 'M500': 16.01, 'fgas': 0.212, 'r500': 1.67, 'R_std': 1.75},
    {'name': 'CL-J1226.9+3332', 'z': 0.890, 'M500': 15.30, 'fgas': 0.040, 'r500': 1.27, 'R_std': 4.70},
    {'name': 'ABELL-1689', 'z': 0.183, 'M500': 15.03, 'fgas': 0.156, 'r500': 1.67, 'R_std': 1.98},
    {'name': 'MACS-J0717.5+3745', 'z': 0.548, 'M500': 14.84, 'fgas': 0.170, 'r500': 1.44, 'R_std': 2.16},
    {'name': 'ABELL-773', 'z': 0.217, 'M500': 10.14, 'fgas': 0.116, 'r500': 1.44, 'R_std': 2.17},
    {'name': 'ABELL-209', 'z': 0.206, 'M500': 9.61, 'fgas': 0.146, 'r500': 1.42, 'R_std': 1.92},
    {'name': 'ABELL-2142', 'z': 0.091, 'M500': 8.78, 'fgas': 0.158, 'r500': 1.44, 'R_std': 1.76},
    {'name': 'RXC-J0532.9-3701', 'z': 0.275, 'M500': 6.55, 'fgas': 0.141, 'r500': 1.22, 'R_std': 1.89},
    {'name': 'ABELL-383', 'z': 0.187, 'M500': 5.87, 'fgas': 0.121, 'r500': 1.22, 'R_std': 1.93},
    {'name': 'ABELL-2034', 'z': 0.113, 'M500': 5.17, 'fgas': 0.073, 'r500': 1.20, 'R_std': 2.31},
    {'name': 'RXC-J0232.2-4420', 'z': 0.284, 'M500': 4.44, 'fgas': 0.123, 'r500': 1.07, 'R_std': 1.89},
]

def v_pure_mond(uE):
    return np.where(uE >= 0, np.sqrt(a0 * uE), -np.sqrt(a0 * np.abs(uE)))

def v_full_interp(uE):
    # uE = v^2 / (a0 + v)
    res = np.zeros_like(uE)
    pos = uE >= 0
    res[pos] = (uE[pos] + np.sqrt(uE[pos]**2 + 4 * a0 * uE[pos])) / 2.0
    neg = ~pos
    res[neg] = (uE[neg] - np.sqrt(uE[neg]**2 - 4 * a0 * uE[neg])) / 2.0
    return res

def solve_cluster(c, v_func, r_max_factor=1.0):
    M500_kg = c['M500'] * 1e14 * M_sun
    r500_m = c['r500'] * Mpc
    r_max_m = r_max_factor * r500_m
    
    fbary = c['fgas'] + 0.015
    Mbary_kg = fbary * M500_kg
    W0 = G * Mbary_kg
    r_min = 1e-4 * Mpc

    def odes(r, y):
        Phi = y[0]
        W = y[1]
        uE = W / r**2
        if isinstance(uE, np.ndarray):
            v_val = v_func(uE)
        else:
            v_val = float(v_func(np.array([uE]))[0])
        dPhi_dr = uE + v_val
        dW_dr = - mu**2 * r**2 * Phi
        return [dPhi_dr, dW_dr]

    def shoot_err(p):
        sol = solve_ivp(odes, (r_min, r_max_m), [p, W0], method='RK45', rtol=1e-8, atol=1e-10)
        return sol.y[0, -1]

    # Search for root p in a wide interval
    # Estimate p range
    p_center = -G * Mbary_kg / r_min - np.sqrt(a0 * G * Mbary_kg) * np.log(r_max_m / r_min)
    p_min = p_center * 3.0
    p_max = p_center * 0.1

    # Grid search for sign change
    ps = np.linspace(p_min, p_max, 100)
    errs = [shoot_err(p) for p in ps]
    
    root_p = None
    for i in range(len(ps)-1):
        if errs[i] * errs[i+1] <= 0:
            root_p = brentq(shoot_err, ps[i], ps[i+1])
            break
            
    if root_p is None:
        return None

    sol = solve_ivp(odes, (r_min, r_max_m), [root_p, W0], method='RK45', rtol=1e-10, atol=1e-12, dense_output=True)
    
    # Evaluate at r500
    y_500 = sol.sol(r500_m)
    Phi_500, W_500 = y_500[0], y_500[1]
    uE_500 = W_500 / r500_m**2
    v_500 = float(v_func(np.array([uE_500]))[0])
    g_500 = uE_500 + v_500
    Mdyn_500 = g_500 * r500_m**2 / G
    R_500 = M500_kg / Mdyn_500
    
    # Evaluate at 0.54 r500
    r_054 = 0.54 * r500_m
    y_054 = sol.sol(r_054)
    Phi_054, W_054 = y_054[0], y_054[1]
    uE_054 = W_054 / r_054**2
    v_054 = float(v_func(np.array([uE_054]))[0])
    g_054 = uE_054 + v_054
    Mdyn_054 = g_054 * r_054**2 / G
    
    # In lensing, what is enclosed weak lensing mass M_lens(0.54 r500)?
    # For a NFW/point/cluster profile, enclosed mass at 0.54 r500:
    # If we assume lensing profile follows same spatial scaling or point mass:
    # Under point mass assumption: M_lens(0.54 r500) = M500
    # Under NFW (c=3-4), M(0.54 r500) / M500 is ~0.60-0.65.
    R_054_point = M500_kg / Mdyn_054
    
    return {
        'R_500': R_500,
        'W_500_ratio': W_500 / W0,
        'Mdyn_500': Mdyn_500 / (1e14 * M_sun),
        'R_054_point': R_054_point,
        'W_054_ratio': W_054 / W0,
        'Mdyn_054': Mdyn_054 / (1e14 * M_sun)
    }

print("Running full non-linear solves for all 12 clusters...")
print("1) Pure MOND branch with boundary Phi(r500) = 0:")
print(f"{'Cluster':18s} | {'R_std':6s} | {'R_500':6s} | {'W/W0(r500)':9s} | {'R_054':6s} | {'W/W0(0.54)':9s}")
print("-" * 65)

r500_results_pure = []
r054_results_pure = []

for c in clusters:
    res = solve_cluster(c, v_pure_mond, r_max_factor=1.0)
    if res:
        r500_results_pure.append(res['R_500'])
        r054_results_pure.append(res['R_054_point'])
        print(f"{c['name']:18s} | {c['R_std']:6.2f} | {res['R_500']:6.2f} | {res['W_500_ratio']:9.2f} | {res['R_054_point']:6.2f} | {res['W_054_ratio']:9.2f}")
    else:
        print(f"{c['name']:18s} | {c['R_std']:6.2f} | FAILED")

print(f"Median R_500 (pure MOND branch) = {np.median(r500_results_pure):.2f}")
print(f"Mean R_500 (pure MOND branch)   = {np.mean(r500_results_pure):.2f}")

print("\n2) Full interpolation branch with boundary Phi(r500) = 0:")
print(f"{'Cluster':18s} | {'R_std':6s} | {'R_500':6s} | {'W/W0(r500)':9s} | {'R_054':6s} | {'W/W0(0.54)':9s}")
print("-" * 65)

r500_results_full = []
r054_results_full = []

for c in clusters:
    res = solve_cluster(c, v_full_interp, r_max_factor=1.0)
    if res:
        r500_results_full.append(res['R_500'])
        r054_results_full.append(res['R_054_point'])
        print(f"{c['name']:18s} | {c['R_std']:6.2f} | {res['R_500']:6.2f} | {res['W_500_ratio']:9.2f} | {res['R_054_point']:6.2f} | {res['W_054_ratio']:9.2f}")
    else:
        print(f"{c['name']:18s} | {c['R_std']:6.2f} | FAILED")

print(f"Median R_500 (full interp branch) = {np.median(r500_results_full):.2f}")
print(f"Mean R_500 (full interp branch)   = {np.mean(r500_results_full):.2f}")
