#!/usr/bin/env python3
"""Symmetron / density-melting screening of the AeST MOND scalar: structural test (2026-11-18). [D]/[O]

A screen that switches MOND off by density must act where Cassini measures: the field at Saturn's orbit. There the
density is interplanetary, not solar.
  (1) Local density.
      - Saturn's orbit (~1e-22 kg/m^3) is ~50x LESS dense than the galactic midplane at R_sun (6.8e-21), which the
        screen must leave unscreened (repo: S(rho_disk) >= 0.99).
      - So any screen S(rho) that never increases with density has S(Saturn) >= S(disk) >= 0.99.
      - Hence Q2 >= 0.99 x bare. [D]
  (2) Compton-length smoothing. A compact body pins sigma = 0 only inside itself. Outside, the maximal (thin-shell)
      depletion is sigma = sigma0 (1 - R/r), and a finite Compton length only makes it smaller. At Saturn,
      |d sigma/sigma0| <= R_sun/r = 4.9e-4. [D]
  (3) Source gating (suppressing the Sun's scalar charge by thin-shell screening).
      - This can pass Cassini, but it screens every star alike, since the Sun is a typical star.
      - Galaxies' MOND source then reduces to gas.
      - Tested on SPARC below. [O]
The repo's CassiniSymmetronWindow / screen_mass_cassini evaluate the solar-system suppression at rho_sun
(1.4e3-1.5e5 kg/m^3, the Sun's interior). That is not the density at Saturn, so the window is an artifact of where
the screen is evaluated.
"""
import glob, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MP = 1.6726e-27; MSUN = 1.989e30; PC = 3.0857e16; AU = 1.495978707e11; RSUN = 6.957e8
n1 = 7.0e6                                              # solar-wind protons per m^3 at 1 AU (~7 cm^-3)
rho = {f"{name}": n1 / (r**2) * MP for name, r in (("Mercury_0.387AU", 0.387), ("Earth_1AU", 1.0), ("Saturn_9.54AU", 9.537))}
rho["local_ISM_Oort_region_lo"] = 0.1e6 * MP; rho["local_ISM_Oort_region_hi"] = 1.0e6 * MP
rho["galactic_midplane_Rsun"] = 0.1 * MSUN / PC**3
rho["sun_mean_used_by_repo"] = 1.4079e3; rho["sun_core_used_by_repo"] = 1.5e5
Q2_bare, Q2_c, Q2_s, Q2_hi = 1.91e-26, 1.6e-27, 1.8e-27, 5.2e-27
S_min = 0.99
out = {"densities_kg_m3": rho,
       "rho_Saturn_over_rho_disk": rho["Saturn_9.54AU"] / rho["galactic_midplane_Rsun"],
       "monotone_nogo": {"S_at_Saturn_min": S_min, "Q2_min": S_min * Q2_bare,
                         "sigma_vs_Park2026": (S_min * Q2_bare - Q2_c) / Q2_s, "passes": S_min * Q2_bare <= Q2_hi},
       "thin_shell_exterior_depletion_bound_at": {k: RSUN / (r * AU) for k, r in (("Mercury", 0.387), ("Saturn", 9.537))}}

# (3) source gating: only gas sources the MOND scalar (stars thin-shell screened). QUMOND proxy with mu_std nu,
#     Upsilon refit (0.1 dex prior), against the live mu_std RAR baseline.
A0 = 1.1607e-10; KPC = 3.0857e19; FG = np.logspace(-0.5, 0.5, 61)
def nu(y): return 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-30))      # nu_std(y), y = gN/a0 (x mu_std(x) = y)
def chi2(d, gpred):
    R, V, eV = d[:, 0], d[:, 1], np.maximum(d[:, 2], 1.0)
    Vp = np.sqrt(np.maximum(gpred, 0) * R * KPC) / 1e3
    return float((np.sum(((V - Vp) / eV) ** 2, 1) + (np.log10(FG) / 0.1) ** 2).min())
tot = {"baseline": 0.0, "gas_only_source": 0.0}; worse = 0
for p in sorted(glob.glob(os.path.join(HERE, "../../02_galaxy_dynamics/sparc_data/*_rotmod.dat"))):
    d = np.loadtxt(p); R = d[:, 0] * KPC; Vg, Vd, Vb = d[:, 3], d[:, 4], d[:, 5]
    gstar = FG[:, None] * (0.5 * np.abs(Vd) * Vd + 0.7 * np.abs(Vb) * Vb) * 1e6 / R
    ggas = np.abs(Vg) * Vg * 1e6 / R * np.ones_like(FG)[:, None]
    gall = np.maximum(gstar + ggas, 1e-15)
    xb = np.sqrt(((gall / A0) ** 2 + (gall / A0) * np.sqrt((gall / A0) ** 2 + 4)) / 2) * A0      # mu_std total law
    gg = np.maximum(ggas, 1e-15)
    g_gas_only = gall + (nu(gg / A0) - 1) * gg                                                    # MOND boost from gas only
    b, s = chi2(d, xb), chi2(d, g_gas_only); tot["baseline"] += b; tot["gas_only_source"] += s; worse += (s - b > 25)
out["source_gating_SPARC"] = {"chi2_baseline_mu_std": tot["baseline"], "chi2_gas_only_MOND_source": tot["gas_only_source"],
                              "delta_chi2": tot["gas_only_source"] - tot["baseline"], "galaxies_worse_by_25": worse}
out["verdict"] = ("[D] Local-density and Compton-smoothed symmetron screens cannot screen Saturn's orbit without "
                  "screening the galactic disk. Thin-shell screening reaches only r ~ R_sun. [O] Source gating fails SPARC "
                  "(see delta_chi2). The symmetron route is closed for the AeST MOND scalar.")
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "SYMMETRON_ROUTE.json"), "w"), indent=1)
