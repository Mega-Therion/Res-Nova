import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# Cosmological parameters
Omega_m0 = 0.315
Omega_r0 = 9.2e-5
H0 = 1.0  # Normalized Hubble constant
lambda_chi_over_H02 = 1e5  # Ratio of the potential coupling to H0^2

def H_squared(N):
    # N = ln(a). a = 1 today (N=0).
    return H0**2 * (Omega_m0 * np.exp(-3*N) + Omega_r0 * np.exp(-4*N))

def dH_dN_over_H(N):
    num = -3 * Omega_m0 * np.exp(-3*N) - 4 * Omega_r0 * np.exp(-4*N)
    den = 2 * (Omega_m0 * np.exp(-3*N) + Omega_r0 * np.exp(-4*N))
    return num / den

def V_prime(chi):
    # V' = 4 * lambda * chi * (chi^2 - 0.5)
    return 4 * lambda_chi_over_H02 * chi * (chi**2 - 0.5)

def derivative(N, y):
    chi, chi_prime = y
    
    # ODE: chi'' + (3 + H'/H) chi' + V'/H^2 = 0
    H2 = H_squared(N)
    H_ratio = dH_dN_over_H(N)
    
    chi_double_prime = -(3 + H_ratio) * chi_prime - V_prime(chi) / H2
    
    return [chi_prime, chi_double_prime]

# Integration range: from CMB (z ~ 1100, N ~ -7) to Today (z = 0, N = 0)
N_start = -7.0
N_end = 0.0

# Initial conditions at CMB: field displaced from 1/sqrt(2) ~ 0.707
y0 = [0.1, 0.0]  # chi = 0.1, dchi/dN = 0

sol = solve_ivp(derivative, [N_start, N_end], y0, t_eval=np.linspace(N_start, N_end, 5000), method='Radau')

N_vals = sol.t
chi_vals = sol.y[0]
z_vals = np.exp(-N_vals) - 1

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(N_vals, chi_vals, label=r'$\chi(N)$ field evolution', color='blue')
plt.axhline(1/np.sqrt(2), color='red', linestyle='--', label=r'Geometric Bound ($1/\sqrt{2}$)')
plt.axhline(-1/np.sqrt(2), color='red', linestyle='--')
plt.xlabel('Number of e-folds $N = \ln(a)$ (0 is Today, -7 is CMB)')
plt.ylabel(r'Information Tension Field $\chi$')
plt.title('Cosmological Background Evolution of the $\chi$ Field')
plt.legend()
plt.grid(True)
plt.savefig('chi_evolution.png', dpi=300)
print("Simulation complete. Plot saved as chi_evolution.png.")
print(f"Final value of chi at N=0 (Today): {chi_vals[-1]:.5f}")
