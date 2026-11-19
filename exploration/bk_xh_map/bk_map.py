#!/usr/bin/env python3
"""BK condensation criterion vs the x_H >= 154 virial cut (see PREREG.md)."""
import json, math
hbar = 1.054571817e-34; eV = 1.78266192e-36; zeta32 = 2.6123753
Mpc = 3.0857e22; H0 = 67.4e3 / Mpc; G = 6.674e-11
rho_crit = 3 * H0**2 / (8 * math.pi * G); rho_x = 154 / (math.sqrt(3) / 2) * rho_crit
rho_BK = lambda m, s: zeta32 * m * (m**2 * s**2 / (2 * math.pi * hbar**2)) ** 1.5
sigma_c = lambda m, rho: math.sqrt(2 * math.pi * hbar**2 / m**2 * (rho / (zeta32 * m)) ** (2 / 3))   # rho_BK(m, sigma_c) = rho
out = {"rho_crit": rho_crit, "rho_xH154": rho_x, "rho_xH154_over_crit": rho_x / rho_crit, "sigma_c_kms_at_virial_density": {}}
for m_eV in (0.1, 0.3, 0.6, 1.0, 2.0, 5.0):
    out["sigma_c_kms_at_virial_density"][str(m_eV)] = sigma_c(m_eV * eV, rho_x) / 1e3
# m that puts sigma_c at the galaxy/cluster boundary (~400 km/s), and the BK/x_H density ratio over sigma for that m
m_star = None
lo, hi = 0.01, 100.0
for _ in range(80):
    mid = math.sqrt(lo * hi)
    if sigma_c(mid * eV, rho_x) / 1e3 > 400: lo = mid
    else: hi = mid
m_star = hi
out["m_eV_for_sigma_c_400kms"] = m_star
out["rhoBK_over_rhoxH_vs_sigma_at_m_star"] = {str(s): rho_BK(m_star * eV, s * 1e3) / rho_x for s in (50, 100, 200, 400, 800, 1200)}
out["scaling"] = "rho_BK / rho_xH = (sigma/sigma_c)^3; equal only at sigma = sigma_c."
out["verdict"] = ("PARTIAL. Both are density thresholds, but BK's scales as sigma^3 and x_H's does not. For sigma << sigma_c BK condenses "
                  "at densities far below the virial value, so x_H's virial cut is the stricter, binding condition (same answer: MOND on "
                  "inside collapsed galaxies). For sigma > sigma_c BK stays normal-phase in clusters while x_H switches MOND on. No single m "
                  "maps the two across galaxies and clusters.")
print(json.dumps(out, indent=1)); json.dump(out, open("BK_MAP.json", "w"), indent=1)
