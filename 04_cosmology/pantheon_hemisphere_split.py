#!/usr/bin/env python3
"""Does direction matter for the supernova Hubble diagram? (RY 2026-09-28: light from ahead vs behind; intervening mass)
Split Pantheon+ (official zHD > 0.01 set, STAT+SYS covariance trimmed per subset, M marginalized per subset) into
hemispheres around an axis and fit each side separately:
  axis 1: the CMB dipole (our motion through the CMB frame; in this framework the aether-wind axis),
          Planck 2018 (l, b) = (264.021, 48.253) -> RA 167.942, Dec -6.944;
  axis 2: the Galactic centre (most intervening mass), RA 266.405, Dec -28.936.
Per side: flat LCDM Omega_m best fit (grid) and the dark-energy ceiling model's free ceiling (share ln 2 today, n = 1).
NOTE: zHD already removes our kinematic dipole and peculiar velocities (standard corrections); any residual
hemispherical difference is beyond standard kinematics. Prior art: Colin et al. 2019 (A&A 631, L13) vs Rubin & Heitlauf
2020 (ApJ 894, 68). Usage: pantheon_hemisphere_split.py  (data: fetch_external_data.sh)"""
import json, math
import numpy as np
import cosmo_data as cd
from omega_ln2_pantheonplus import load_cov, chi2_marginalized, official_mask
from ceiling_model_pantheonplus import E_lcdm, E_ceiling, mu_model, LN2, KAPPA

AXES = {"cmb_dipole": (167.942, -6.944), "galactic_centre": (266.405, -28.936)}

def unit(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    return np.stack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)], axis=-1)

def load(dat):
    with open(dat) as f:
        hdr = f.readline().split(); idx = {n: i for i, n in enumerate(hdr)}; rows = []
        for line in f:
            p = line.split()
            if len(p) == len(hdr):
                rows.append([float(p[idx[k]]) for k in ("zHEL", "zHD", "m_b_corr", "RA", "DEC")])
    return np.array(rows)

def fit(zhel, zhd, mb, cinv):
    grid = np.round(np.arange(0.10, 0.60001, 0.002), 4)
    c = np.array([chi2_marginalized(mb, mu_model(zhd, zhel, lambda z, om=om: E_lcdm(z, om)), cinv) for om in grid])
    i = int(np.argmin(c)); ok = grid[c - c[i] <= 1.0]
    ofs = np.round(np.arange(0.70, 0.9991, 0.004), 4)
    co = np.array([chi2_marginalized(mb, mu_model(zhd, zhel, lambda z, of=of: E_ceiling(z, LN2, of)), cinv) for of in ofs])
    j = int(np.argmin(co)); ok2 = ofs[co - co[j] <= 1.0]
    ck = chi2_marginalized(mb, mu_model(zhd, zhel, lambda z: E_ceiling(z, LN2, KAPPA)), cinv)
    return {"n": int(len(zhd)), "omega_m_best": float(grid[i]), "omega_m_1sigma": [float(ok.min()), float(ok.max())],
            "chi2_lcdm": float(c[i]), "omega_f_best": float(ofs[j]), "omega_f_1sigma": [float(ok2.min()), float(ok2.max())],
            "chi2_ceiling_kappa_minus_lcdm": float(ck - c[i])}

def main():
    A = load(cd.path("pantheon_dat")); cov = load_cov(cd.path("pantheon_cov")); ww = official_mask(A[:, 1])
    n_hat = unit(A[:, 3], A[:, 4]); out = {}
    for name, (ra, dec) in AXES.items():
        cosang = n_hat @ unit(ra, dec); out[name] = {}
        for side, sel in (("toward", cosang > 0), ("away", cosang < 0)):
            m = ww & sel; cinv = np.linalg.inv(cov[np.ix_(m, m)])
            out[name][side] = fit(A[m, 0], A[m, 1], A[m, 2], cinv)
            print(name, side, out[name][side], flush=True)
        t, a_ = out[name]["toward"], out[name]["away"]
        s1 = (t["omega_m_1sigma"][1] - t["omega_m_1sigma"][0]) / 2; s2 = (a_["omega_m_1sigma"][1] - a_["omega_m_1sigma"][0]) / 2
        out[name]["omega_m_difference_sigma"] = abs(t["omega_m_best"] - a_["omega_m_best"]) / math.hypot(s1, s2)
    json.dump(out, open(cd.out("PANTHEON_HEMISPHERE_SPLIT.json"), "w"), indent=2); print(json.dumps({k: v.get("omega_m_difference_sigma") for k, v in out.items()}))

if __name__ == "__main__":
    main()
