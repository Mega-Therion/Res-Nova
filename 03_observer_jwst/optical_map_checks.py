#!/usr/bin/env python3
"""Observation-tier optical map, v0: the numbers behind OPTICAL_MAP_v0_2026-11-25.md.

C1  GW170817 bound on any light-only (disformal) optical term, vs the deflection galaxy lensing needs.
C2  Distance duality D_L = (1+z) D_M (1+z)^eps, measured from Pantheon+ (shape, M free) + DESI DR2 BAO (r_d free):
    bounds any optical brightening or dimming that grows with z out to z ~ 2.3.  [E] measurement, no pass/fail.
C3  OmegaCDM (Omega_L = ln 2) vs Planck LCDM at JWST redshifts: luminosity-distance and cosmic-age ratios.
C4  The 141.99 provenance: CEERS-93316 is at z = 4.912 (Arrabal Haro et al. 2023, Nature 622, 707), not z ~ 16.
Output: OPTICAL_MAP_CHECKS.json"""
import json, math, sys
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
sys.path.insert(0, "../04_cosmology")
import cosmo_data as cd
from ceiling_model_bao_sn import load_bao
from omega_ln2_pantheonplus import load_data, official_mask, load_cov, chi2_marginalized

out = {}
C_KMS = 299792.458

# ---------------- C1 ----------------
# Disformal optical metric g~ = g + 2 l^2 dchi dchi: light along grad chi moves at c(1 - l^2 |grad chi|^2) to first order.
# GW170817: |c_gw - c_em|/c <= ~1e-15 over D = 40 Mpc (Abbott et al. 2017, ApJL 848 L13: -3e-15 .. +7e-16).
# Light-only lensing deflection scales like the same small parameter times (path / gradient scale): alpha ~ eps_d * (L/lambda).
eps_bound = 1e-15
frac_in_galaxies = 2 * 0.3 / 40.0      # ~300 kpc of halo at each end of a 40 Mpc path
eps_in_gal = eps_bound / frac_in_galaxies
alpha_needed = 1e-5                     # galaxy-scale Einstein angle ~ 1-2 arcsec ~ 5-10 micro-rad
L_over_lambda = 10.0                    # generous: path through a halo / gradient scale
out["C1_gw170817"] = {"speed_bound_eps": eps_bound, "eps_inside_galaxies_max": eps_in_gal,
                      "light_only_deflection_max_rad": eps_in_gal * L_over_lambda, "galaxy_lensing_needs_rad": alpha_needed,
                      "shortfall_factor": alpha_needed / (eps_in_gal * L_over_lambda),
                      "reading": "A light-only optical term can supply at most ~1e-12 of the needed deflection. "
                                 "Lensing 'dark matter' must therefore come from the metric that gravitational waves also "
                                 "follow (single metric): the ITT phantom potential, not a photon-only effect."}

# ---------------- C2 ----------------
zb, db, qb, Cb = load_bao(cd.path("desi_mean"), cd.path("desi_cov")); Cbi = np.linalg.inv(Cb)
zhel_all, zhd_all, mb_all = load_data(cd.path("pantheon_dat")); ww = official_mask(zhd_all)
zhel, zhd, mb = zhel_all[ww], zhd_all[ww], mb_all[ww]
sinv = np.linalg.inv(load_cov(cd.path("pantheon_cov"))[np.ix_(ww, ww)])
zg = np.linspace(0, 2.5, 25001)
def DM_unit(om):            # comoving distance in c/H0 units, flat LCDM shape (radiation negligible at z < 2.5)
    ez = np.sqrt(om * (1 + zg)**3 + 1 - om)
    return np.concatenate(([0.0], np.cumsum(0.5 * (1 / ez[1:] + 1 / ez[:-1]) * np.diff(zg))))
def chi2(p):
    om, eps, alpha = p      # alpha = c / (H0 r_d)
    if not (0.05 < om < 0.7 and -0.5 < eps < 0.5 and 10 < alpha < 60): return 1e12
    dm = DM_unit(om)
    E = lambda z: np.sqrt(om * (1 + z)**3 + 1 - om)
    DMz = np.interp(zb, zg, dm) * alpha; DHz = alpha / E(zb); DVz = (zb * DMz**2 * DHz)**(1 / 3)
    pred = np.array([{"DM_over_rs": DMz[i], "DH_over_rs": DHz[i], "DV_over_rs": DVz[i]}[qb[i]] for i in range(len(zb))])
    r = db - pred; cb = float(r @ Cbi @ r)
    mu = 5 * np.log10((1 + zhel) * np.interp(zhd, zg, dm) * (1 + zhd)**eps) + 25.0
    return cb + chi2_marginalized(mb, mu, sinv)
best = minimize(chi2, [0.30, 0.0, 30.0], method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-6, "maxiter": 6000})
best = minimize(chi2, best.x, method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-6, "maxiter": 6000})
c0 = best.fun
# profile likelihood in eps
eps_grid = np.linspace(best.x[1] - 0.15, best.x[1] + 0.15, 61)
prof = []
for e in eps_grid:
    f = minimize(lambda q: chi2([q[0], e, q[1]]), [best.x[0], best.x[2]], method="Nelder-Mead",
                 options={"xatol": 1e-7, "fatol": 1e-6, "maxiter": 3000})
    prof.append(f.fun - c0)
prof = np.array(prof); inside = eps_grid[prof <= 1.0]
eps_lo, eps_hi = float(inside.min()), float(inside.max())
z_hi = float(max(zb.max(), zhd.max()))
out["C2_distance_duality"] = {
    "model": "D_L = (1+z) D_M (1+z)^eps; M (SN) and r_d (BAO) free; flat-LCDM shape for D_M",
    "best": {"omega_m": best.x[0], "eps": best.x[1], "c_over_H0_rd": best.x[2], "chi2": c0},
    "eps_1sigma": [eps_lo, eps_hi],
    # flux ~ D_L^-2, so a duality factor (1+z)^eps changes flux by (1+z)^(-2 eps)
    "flux_change_at_z_2_3_percent_best": float(100 * (3.3**(-2 * best.x[1]) - 1)),
    "flux_change_at_z_2_3_percent_1sigma_range": [float(100 * (3.3**(-2 * eps_hi) - 1)), float(100 * (3.3**(-2 * eps_lo) - 1))],
    "reading": "Any optical effect that brightens or dims distant sources relative to the geometric (BAO) distance is "
               "bounded at this level out to z ~ 2.3."}

# ---------------- C3 ----------------
def cosmo(om, h, z):
    ol = 1 - om
    E = lambda x: math.sqrt(om * (1 + x)**3 + ol + 8.4e-5 / h**2 * (1 + x)**4)
    dc = quad(lambda x: 1 / E(x), 0, z, limit=200)[0] * C_KMS / (100 * h)
    age = quad(lambda x: 1 / ((1 + x) * E(x)), z, np.inf, limit=400)[0] * 977.8 / (100 * h)   # Gyr
    return (1 + z) * dc, age
rows = {}
for z in (7, 10, 12, 14.44):
    dl_p, t_p = cosmo(0.3153, 0.6736, z)       # Planck 2018 LCDM
    dl_o, t_o = cosmo(1 - math.log(2) - 9e-5, 0.6802, z)   # OmegaCDM point from O3 run (#271)
    rows[str(z)] = {"DL_ratio_omegacdm_over_planck": dl_o / dl_p, "luminosity_ratio": (dl_o / dl_p)**2,
                    "age_planck_Myr": t_p * 1e3, "age_omegacdm_Myr": t_o * 1e3, "age_ratio": t_o / t_p}
out["C3_omegacdm_vs_planck_at_jwst_z"] = rows

# ---------------- C4 ----------------
out["C4_141_99_provenance"] = {
    "object": "CEERS-93316", "photometric_z": 16.4, "spectroscopic_z": 4.912,
    "source": "Arrabal Haro et al. 2023, Nature 622, 707 (arXiv:2303.15431): 'another candidate with suggested z~16 instead has z = 4.9'",
    "reading": "The 141.99 'boost' was traced (project_god_theory_141) to this object's apparent mass excess at z ~ 16.7. "
               "At z = 4.9 that excess does not exist. The factor has no surviving empirical anchor."}

json.dump(out, open("OPTICAL_MAP_CHECKS.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
