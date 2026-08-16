import numpy as np
from scipy.integrate import solve_ivp

# Res Nova — D5 Cosmological Growth Factor Computation
# Computes the linear growth factor D(a) for ΛCDM and MOND-enhanced cosmologies
# Author: R.W. Yett / Sovereign Architecture Group
# Date: 2026-08-16

# Cosmological parameters (Planck 2018)
Omega_m = 0.315
Omega_L = 0.685
H0_kms = 70.0  # km/s/Mpc
a0_mond = 1.2e-10  # m/s^2

# The cosmic coincidence: H₀c / a₀ ≈ 5.7
# Horizon-scale acceleration is ~6× a₀ (Newtonian regime)
# Cluster-scale acceleration is ~10⁻⁴× a₀ (deep-MOND regime)

def Hubble(a):
    return np.sqrt(Omega_m * a**(-3) + Omega_L)

def growth_equation(u, y, enhancement=1.0):
    """
    Linear growth equation in terms of u = ln(a).
    
    D'' + [2 + d ln H / d ln a] D' - (3/2) Ω_m(a) × ξ × D = 0
    
    where ξ is the MOND enhancement factor (ξ=1 for ΛCDM).
    
    In matter domination: D ∝ a^λ where λ = (-1/2 + √(1/4 + 6ξ)) / 2
    """
    D, Dp = y
    a = np.exp(u)
    Ha2 = Omega_m * a**(-3) + Omega_L
    dlnH_dlna = -1.5 * Omega_m * a**(-3) / Ha2
    f_coeff = 2.0 + dlnH_dlna
    g_coeff = 1.5 * Omega_m * a**(-3) / Ha2 * enhancement
    Dpp = -f_coeff * Dp + g_coeff * D
    return [Dp, Dpp]

def compute_growth(enhancement=1.0, a_min=1e-4, n_points=500):
    """Compute the growth factor D(a) for a given enhancement."""
    u_init = np.log(a_min)
    u_final = 0.0
    u_eval = np.linspace(u_init, u_final, n_points)
    
    # IC: D = a, D' = a (matter-dominated growing mode)
    D0 = a_min
    Dp0 = a_min
    
    sol = solve_ivp(growth_equation, [u_init, u_final], [D0, Dp0],
                    args=(enhancement,), t_eval=u_eval, method='RK45',
                    rtol=1e-10, atol=1e-12)
    
    a_vals = np.exp(u_eval)
    D_vals = sol.y[0]
    return a_vals, D_vals

def growth_exponent_matter_dom(enhancement):
    """Analytic growth exponent in matter domination."""
    return (-0.5 + np.sqrt(0.25 + 6.0 * enhancement)) / 2.0

if __name__ == '__main__':
    print('=== RES NOVA D5: COSMOLOGICAL GROWTH FACTOR ===')
    print(f'Ω_m = {Omega_m}, Ω_Λ = {Omega_L}, H₀ = {H0_kms} km/s/Mpc')
    print()
    
    # Compute growth factors
    a, D_lcdm = compute_growth(1.0)
    _, D_mond2 = compute_growth(2.0)
    _, D_mond3 = compute_growth(3.0)
    
    # Analytic exponents
    for enh in [1.0, 1.5, 2.0, 3.0]:
        lam = growth_exponent_matter_dom(enh)
        print(f'Enhancement ξ={enh:.1f}: growth exponent λ={lam:.3f} (D ∝ a^{lam:.3f})')
    
    print()
    print(f'{"a":>8} {"z":>8} {"D_LCDM":>10} {"D_M2x":>10} {"D_M3x":>10} {"2x/LCDM":>10} {"3x/LCDM":>10}')
    for i in range(0, len(a), 50):
        z = 1.0/a[i] - 1.0
        r2 = D_mond2[i] / D_lcdm[i]
        r3 = D_mond3[i] / D_lcdm[i]
        print(f'{a[i]:8.4f} {z:8.2f} {D_lcdm[i]:10.4f} {D_mond2[i]:10.4f} {D_mond3[i]:10.4f} {r2:10.3f} {r3:10.3f}')
    
    print(f'\nFinal amplification at z=0:')
    print(f'  D_MOND(2x)/D_LCDM = {D_mond2[-1]/D_lcdm[-1]:.1f}x')
    print(f'  D_MOND(3x)/D_LCDM = {D_mond3[-1]/D_lcdm[-1]:.1f}x')
    print(f'\n→ A 2x MOND enhancement produces ~{D_mond2[-1]/D_lcdm[-1]:.0f}x excess structure growth')
    print(f'→ This is the root cause of the νHDM structure overproduction (Russell et al. 2026)')
