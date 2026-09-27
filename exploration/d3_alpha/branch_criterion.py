# HELD 2026-09-27: branch criterion uses the FROZEN-METRIC zero-mode kinetic term; constraint back-reaction
# (SZ PRD 106 104041, Y-mode Hamiltonian) may change omega_L. Do not cite its table until
# aest_dispersion_offset.py (constrained dispersion with Qbar = Q0 + qbar) is reconciled. See TARGET_D3_ALPHA_WORKING note 4.
#!/usr/bin/env python3
"""Held-vs-dragged branch criterion for AeST's zero mode (SZ Cosh parameters).
omega_L^2 = 2 K2 Q0^2 |Psi| k^2 / (K_B k^2 + 2 K2 Q0^2)   (verified lift, zero_mode_lift.py)
held (static/MOND branch) iff R = omega_L / (k v) >> 1 ; dragged (aether free-falls, GR) iff R << 1.
|Psi| = local potential depth relative to the cosmic mean, estimated from escape speed |Psi| = v_esc^2/(2c^2).
Two readings of v: (A) velocity relative to the CMB frame; (B) velocity relative to the local bulk flow / host.
"""
from math import sqrt
c = 299792.458                     # km/s
K2, Q0, KB = 7.5e5, 0.1, 0.5       # Q0 in Mpc^-1 (SZ Cosh example, TARGET_D5)
MQ = sqrt(2 * K2 * Q0**2 / KB)     # Mpc^-1
print(f"M_Q = sqrt(2 K2 Q0^2 / K_B) = {MQ:.1f} Mpc^-1  ->  1/M_Q = {1e3/MQ:.2f} kpc")
def R(r_kpc, vesc, v):
    k = 1e3 / r_kpc                                    # Mpc^-1
    psi = vesc**2 / (2 * c**2)
    wL = sqrt(2 * K2 * Q0**2 * psi * k**2 / (KB * k**2 + 2 * K2 * Q0**2))
    return wL / (k * v / c)
AU_kpc = 4.848e-9
rows = [
 ("Sun, EFE region (r=7000 AU)", 7000 * AU_kpc, 550, 370, 240),
 ("wide binary (0.05 pc)",      5e-5,          550, 370, 240),
 ("Milky Way disk (10 kpc)",    10,            550, 552, 75),
 ("Fornax dSph (1 kpc, 140 kpc out)", 1,       300, 552, 150),
 ("SPARC dwarf, field (5 kpc)",  5,            150, 400, 60),
 ("SPARC L* spiral, field (15 kpc)", 15,       450, 400, 60),
 ("cluster core (300 kpc)",     300,           2500, 300, 150),
]
print(f"\n{'system':34s} {'R (A: CMB frame)':>17s} {'R (B: local flow)':>18s}")
for name, r, vesc, vA, vB in rows:
    ra, rb = R(r, vesc, vA), R(r, vesc, vB)
    fa = "held" if ra > 3 else ("dragged" if ra < 1/3 else "marginal")
    fb = "held" if rb > 3 else ("dragged" if rb < 1/3 else "marginal")
    print(f"{name:34s} {ra:10.2e} {fa:>7s} {rb:10.2e} {fb:>7s}")
# second-order gradient instability where Psi > 0 (condensate-underdense): growth rate <= M_Q sqrt(Psi)
for psi in (1e-6, 1e-5):
    G = MQ * sqrt(psi)                                  # Mpc^-1 (times c)
    t_myr = (1 / G) * 3.0857e19 / c / 3.156e13           # Mpc/c in Myr
    print(f"Psi=+{psi:g}: max growth rate M_Q sqrt(Psi) = {G:.3f} Mpc^-1 c  -> e-fold time {t_myr:.1f} Myr")
