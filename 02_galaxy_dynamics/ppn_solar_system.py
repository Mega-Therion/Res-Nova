import numpy as np

# Res Nova — D3 PPN and Solar System Constraints Computation
# Computes MOND corrections and PPN parameter estimates for the dual-channel action
# Author: R.W. Yett / Sovereign Architecture Group
# Date: 2026-08-16

# Constants
G = 6.674e-11  # m^3 kg^-1 s^-2
M_sun = 1.989e30  # kg
AU = 1.496e11  # m
a0 = 1.2e-10  # MOND acceleration m/s^2
c = 3e8  # m/s

# The dual-channel interpolation function
def mu_simple(x):
    """The 'simple' μ = x/(1+x) used in Res Nova's dual-channel action."""
    return x / (1.0 + x)

def mond_acceleration(g_N, a0_val=a0):
    """Compute MOND acceleration from Newtonian acceleration (simple μ).
    g * μ(g/a₀) = g_N → g² - g_N·g - g_N·a₀ = 0 → g = (g_N + √(g_N² + 4g_N·a₀))/2
    """
    return (g_N + np.sqrt(g_N**2 + 4 * g_N * a0_val)) / 2.0

def solar_system_profile():
    """Compute the MOND correction at each planet's orbit."""
    bodies = [
        ("Mercury", 0.39), ("Venus", 0.72), ("Earth", 1.0),
        ("Mars", 1.52), ("Jupiter", 5.2), ("Saturn", 9.5),
        ("Pioneer scale", 20.0),
    ]
    
    print('=== SOLAR SYSTEM MOND CORRECTION PROFILE ===')
    print(f'{"Body":<20} {"g_N (m/s²)":<15} {"g_N/a₀":<12} {"μ":<14} {"1-μ":<12} {"MOND corr":<12}')
    for name, r_au in bodies:
        r = r_au * AU
        g_N = G * M_sun / r**2
        x = g_N / a0
        mu = mu_simple(x)
        corr = 1.0 / mu - 1.0
        print(f'{name:<20} {g_N:<15.3e} {x:<12.2e} {mu:<14.10f} {1-mu:<12.2e} {corr:<12.2e}')
    
    # Cassini comparison
    g_earth = G * M_sun / AU**2
    corr_earth = a0 / g_earth
    cassini_bound = 2.3e-5
    print(f'\nMOND correction at Earth: {corr_earth:.2e}')
    print(f'Cassini bound |γ-1|: {cassini_bound:.2e}')
    print(f'Safety margin: {cassini_bound / corr_earth:.0f}×')

def external_field_effect():
    """Compute the external field effect (Q₂) tension."""
    g_ext = 1.9e-10  # Galactic external field at Sun's position
    x_ext = g_ext / a0
    mu_ext = mu_simple(x_ext)
    
    print('\n=== EXTERNAL FIELD EFFECT (Q₂) ===')
    print(f'Galactic external field: g_ext = {g_ext:.1e} m/s²')
    print(f'g_ext/a₀ = {x_ext:.2f}')
    print(f'μ(g_ext/a₀) = {mu_ext:.6f}')
    print(f'Cassini Q₂ constraint: (1.6 ± 1.8) × 10⁻²⁷ s⁻²')
    print(f'MOND boost at Sun constrained to < 2% (95% CL)')
    print(f'Galaxy rotation curves require ~60% boost → 3-15σ tension')

def ppn_summary():
    """Summarize PPN parameter findings."""
    print('\n=== PPN PARAMETER SUMMARY ===')
    print('In the Newtonian regime (a >> a₀):')
    print('  μ(x) → 1 - a₀/a + (a₀/a)² - ...')
    print('  F_dual → ½x² (standard Newtonian)')
    print('  PPN γ ≈ 1 (requires RMOND screening)')
    print('  PPN β ≈ 1 (requires standard nonlinearity)')
    print('\nThe dual-channel μ does NOT affect PPN parameters.')
    print('PPN parameters depend on the covariant completion (D7/D9).')
    print('D3 is reduced to a dependency on D7.')

if __name__ == '__main__':
    solar_system_profile()
    external_field_effect()
    ppn_summary()
