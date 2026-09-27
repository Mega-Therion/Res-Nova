#!/usr/bin/env python3
"""Compare SZ's two parameter points (TARGET_D5 §2.5): CMB run (mu^-1 = 10 kpc) vs the quasistatic
requirement SZ state for galactic MOND (mu^-1 >~ 1 Mpc). Q0 = 0.1 Mpc^-1, K_B = 0.5, lambda_s = 1.
(a) regime: K2|Psi| (small-offset expansion valid if << 0.5; zero branch unstable if >~ 0.75)
(b) lift: omega_L^2 (k >> k*) = 4 pi G rho_phi (2-K_B) lam/(2+K_B lam), 4 pi G rho_phi = K2 Q0^2 |Psi|
(c) linear validity of the dragged analysis for a source's OWN field: v_rel^2 >> |Psi_source|
(d) R = omega_L/(k v_rel) with the ambient |Psi| up to 1e-5 (large-scale structure) to be conservative."""
from math import sqrt
c = 299792.458; Q0, KB, lam = 0.1, 0.5, 1.0
def point(mu_inv_kpc):
    mu = 1e3 / mu_inv_kpc; K2 = mu**2 * (2 - KB) / (2 * Q0**2)
    ks = mu * sqrt((1 + lam) / lam)
    cs = c * sqrt((2 - KB) * (1 + KB * lam / 2) / (K2 * KB))
    return mu, K2, ks, cs
print(f"{'point':34s} {'mu[Mpc^-1]':>10s} {'K2':>10s} {'1/k*':>10s} {'c_s[km/s]':>10s} {'K2|Psi_MW|':>11s} {'regime':>22s}")
psi_mw = 550**2 / (2 * c**2)
for name, mi in (("SZ CMB run (1/mu = 10 kpc)", 10), ("SZ quasistatic req. (1/mu = 1 Mpc)", 1000), ("1/mu = 3 Mpc", 3000)):
    mu, K2, ks, cs = point(mi)
    reg = "unstable at all k" if K2 * psi_mw > 0.75 else ("small-offset valid" if K2 * psi_mw < 0.05 else "transitional")
    print(f"{name:34s} {mu:10.2f} {K2:10.3g} {1e3/ks:8.2f}kpc {cs:10.0f} {K2*psi_mw:11.3g} {reg:>22s}")
print("\n(c) linear validity of the dragged analysis for each source's OWN field:  v_rel^2 / |Psi_source|  (>> 1 required)")
sys_ = [("Sun's own field at 7000 AU", 0.357, 240), ("wide binary (1.5 Msun, 0.05 pc)", 0.36, 240),
        ("Crater II (sigma ~ 2.7 km/s)", 2.7, 150), ("Fornax (sigma ~ 11 km/s)", 11.7, 150),
        ("Milky Way-like spiral (v_c 220)", 220, 75), ("field L* spiral (v_c 200)", 200, 60)]
for name, vint, vrel in sys_:
    ratio = (vrel / vint) ** 2
    print(f"  {name:34s} v_int={vint:6.2f} km/s  v_rel={vrel:4d} km/s  ratio={ratio:10.3g}  -> {'linear (dragged analysis applies)' if ratio > 10 else 'NON-linear: open'}")
print("\n(d) R = omega_L/(k v_rel) at the quasistatic-required point, ambient |Psi| = 1e-5 (conservative upper value):")
mu, K2, ks, cs = point(1000)
for name, r_kpc, vrel in (("Sun's EFE region (7000 AU)", 7000 * 4.848e-9, 240), ("wide binary (0.05 pc)", 5e-5, 240),
                          ("Crater II (r_h ~ 1 kpc)", 1.0, 150), ("Fornax (r_h ~ 0.7 kpc)", 0.7, 150)):
    k = 1e3 / r_kpc; psi = 1e-5
    wL2 = K2 * Q0**2 * psi * (2 - KB) * lam * (k**2 - ks**2) / ((2 + KB * lam) * k**2 + (2 - KB) * (1 + lam) * mu**2)
    print(f"  {name:28s} R = {sqrt(wL2)/(k*vrel/c):.2e}   (static branch would need v_rel < {sqrt(wL2)/k*c*1e3:.3g} m/s)")
