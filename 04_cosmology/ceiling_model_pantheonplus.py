#!/usr/bin/env python3
"""Dark-energy ceiling model vs Pantheon+ (RY 2026-09-28: 'if it freezes at all, around 0.954').
Model: the dark-energy share starts at Omega_Lambda0 = ln 2 today and approaches a ceiling Omega_f (kappa = sqrt(theta(2-theta))
= 0.953939 for theta = 0.7) instead of 1. Minimal form: r = rho_DE/rho_m grows logistically in ln a,
  d ln r / d ln a = 3 (1 - r/r_f)  <=>  w(a) = -(1 - r/r_f),   r_f = Omega_f/(1-Omega_f),  r0 = ln2/(1-ln2),
so w -> -1 early (Lambda-like) and w -> 0 late (the share freezes at Omega_f).  E^2(a) = a^-3 (1 + r(a)) / (1 + r0).
Same likelihood as omega_ln2_pantheonplus.py: Pantheon+SH0ES, STAT+SYS covariance, zHD > 0.01, M marginalized analytically.
The logistic form is ONE minimal realization of the ceiling; other approach laws give other (w0, wa).
Usage: ceiling_model_pantheonplus.py  (data: fetch_external_data.sh)"""
import json, math
import numpy as np
import cosmo_data as cd
from omega_ln2_pantheonplus import load_data, official_mask, load_cov, chi2_marginalized, C_KMS

LN2 = math.log(2.0)
KAPPA = math.sqrt(0.7 * (2 - 0.7))

def E_lcdm(z, om):
    return np.sqrt(om * (1 + z) ** 3 + 1 - om)

def E_ceiling(z, ol0, of):
    a = 1.0 / (1.0 + z); r0 = ol0 / (1 - ol0); rf = of / (1 - of)
    r = rf / (1 + (rf / r0 - 1) * a ** -3)
    return np.sqrt(a ** -3 * (1 + r) / (1 + r0))

def mu_model(zhd, zhel, Efun):
    zmax = float(np.max(zhd)) * 1.0000001
    zs = np.linspace(0.0, zmax, 200001); ez = Efun(zs)
    dc = np.concatenate(([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zs))) * C_KMS / 70.0
    return 5.0 * np.log10((1.0 + zhel) * np.interp(zhd, zs, dc)) + 25.0

def w0_wa(ol0, of):
    r0 = ol0 / (1 - ol0); rf = of / (1 - of); x = r0 / rf
    return -(1 - x), -3 * x * (1 - x)          # w0, wa  (w = w0 + wa (1 - a) near a = 1)

def main():
    zhel_all, zhd_all, mb_all = load_data(cd.path("pantheon_dat")); ww = official_mask(zhd_all)
    zhel, zhd, mb = zhel_all[ww], zhd_all[ww], mb_all[ww]
    cov = load_cov(cd.path("pantheon_cov"))[np.ix_(ww, ww)]; cinv = np.linalg.inv(cov)
    chi = lambda Efun: chi2_marginalized(mb, mu_model(zhd, zhel, Efun), cinv)
    grid = np.round(np.arange(0.10, 0.60001, 0.002), 4)
    c_l = np.array([chi(lambda z, om=om: E_lcdm(z, om)) for om in grid])
    i = int(np.argmin(c_l)); chi_min = float(c_l[i]); om_best = float(grid[i])
    chi_ln2 = chi(lambda z: E_lcdm(z, 1 - LN2))
    chi_ceil = chi(lambda z: E_ceiling(z, LN2, KAPPA))
    ofs = np.round(np.arange(0.70, 0.9991, 0.002), 4)
    c_of = np.array([chi(lambda z, of=of: E_ceiling(z, LN2, of)) for of in ofs])
    j = int(np.argmin(c_of))
    w0, wa = w0_wa(LN2, KAPPA)
    res = {"data": {"file_dat_sha256": "1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8",
                    "file_cov_sha256": "abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc", "n_sne": int(ww.sum())},
           "lcdm_free": {"omega_m": om_best, "chi2_min": chi_min},
           "lcdm_ln2": {"chi2": chi_ln2, "delta_chi2_vs_best": chi_ln2 - chi_min},
           "ceiling_kappa": {"omega_lambda0": LN2, "omega_f": KAPPA, "w0": w0, "wa": wa, "chi2": chi_ceil,
                             "delta_chi2_vs_best": chi_ceil - chi_min, "delta_chi2_vs_ln2_lambda": chi_ceil - chi_ln2},
           "ceiling_scan": {"omega_f_best": float(ofs[j]), "chi2_best": float(c_of[j]),
                            "delta_chi2_at_kappa": chi_ceil - float(c_of[j]),
                            "omega_f_within_1sigma": [float(ofs[k]) for k in (np.where(c_of - c_of[j] <= 1.0)[0][[0, -1]])]}}
    json.dump(res, open(cd.out("CEILING_MODEL_PANTHEONPLUS.json"), "w"), indent=2)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
