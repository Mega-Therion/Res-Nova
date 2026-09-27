#!/usr/bin/env python3
"""Branch criterion with the CONSTRAINED zero-mode dispersion (aest_dispersion_offset.py -> offset_zero_branch.py):
  omega_L^2 = K2 Q0 qbar (2-K_B) lam (k^2 - k*^2) / [(2+K_B lam) k^2 + (2-K_B)(1+lam) mu^2]
  mu^2 = 2 K2 Q0^2/(2-K_B),  k*^2 = (1+lam) mu^2 / lam,  qbar = -Q0 Psi (potential well), 4 pi G rho_phi = K2 Q0 qbar.
k > k*: restoring; held iff R = omega_L/(k v) >> 1.  k < k*: omega_L^2 < 0 -> no restoring force (Jeans-like growth at
rate -> sqrt(K2 Q0 qbar) for k << k*): branch not set by this linear criterion (non-linear structure formation, D5).
SZ Cosh example: K2 = 7.5e5, Q0 = 0.1 Mpc^-1, K_B = 0.5; lambda_s = 1 (and 0.3, 2.2 for sensitivity)."""
from math import sqrt
c = 299792.458
K2, Q0, KB = 7.5e5, 0.1, 0.5
AU_kpc = 4.848e-9
rows = [("Sun, EFE region (7000 AU)", 7000 * AU_kpc, 550, 370, 240),
        ("wide binary (0.05 pc)", 5e-5, 550, 370, 240),
        ("Fornax dSph (1 kpc)", 1, 300, 552, 150),
        ("SPARC dwarf, field (5 kpc)", 5, 150, 400, 60),
        ("Milky Way disk (10 kpc)", 10, 550, 552, 75),
        ("SPARC L* spiral (15 kpc)", 15, 450, 400, 60)]
for lam in (1.0, 0.3, 2.2):
    mu2 = 2 * K2 * Q0**2 / (2 - KB); ks2 = (1 + lam) * mu2 / lam
    print(f"\nlambda_s = {lam}:  mu = {sqrt(mu2):.1f} Mpc^-1 (1/mu = {1e3/sqrt(mu2):.1f} kpc), k* = {sqrt(ks2):.1f} Mpc^-1 (1/k* = {1e3/sqrt(ks2):.2f} kpc)")
    print(f"  {'system':28s} {'R (A: CMB frame)':>20s} {'R (B: local flow)':>20s}")
    for name, r, vesc, vA, vB in rows:
        k = 1e3 / r
        psi = vesc**2 / (2 * c**2); qbar = Q0 * psi
        wL2 = K2 * Q0 * qbar * (2 - KB) * lam * (k**2 - ks2) / ((2 + KB * lam) * k**2 + (2 - KB) * (1 + lam) * mu2)
        if wL2 <= 0:
            print(f"  {name:28s} {'k < k*: Jeans regime, no restoring force':>41s}")
            continue
        out = []
        for v in (vA, vB):
            R = sqrt(wL2) / (k * v / c)
            out.append(f"{R:9.2e} {'held' if R > 3 else ('dragged' if R < 1/3 else 'marginal'):>8s}")
        print(f"  {name:28s} {out[0]:>20s} {out[1]:>20s}")
