#!/usr/bin/env python3
"""Residual beam-smearing test for the high-z a0 sample (RC100).

Open systematic (ii) of 02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md: "a z-dependent Vc or
beam-smearing bias was not tested". RC100's Vc and fDM come from beam-convolved forward models
(Nestor Shachar+2023, arXiv:2209.12199, sec. 3: the PSF and LSF are convolved into the model) [C],
so raw smearing is modelled. What can remain is a residual bias from an imperfect PSF model, which
would grow as the beam gets large compared with the galaxy.

Test [D]: per galaxy, a0_i from the fDM route under mu_std at R_e
    g_obs = Vc^2 / R_e,  mu = 1 - fDM,  x = mu / sqrt(1 - mu^2),  a0_i = g_obs / x,
and a resolution proxy r = beam / R_e(angular), with the sample's median beam 0.53" (the paper, sec. 2;
per-galaxy beams are not tabulated) and R_e converted with the Planck 2018 angular-diameter distance.
A residual smearing bias predicts ln a0_i correlated with ln r at fixed z. Reported: OLS slope of
ln a0_i on ln r with z and ln M_bar as controls, 2000-sample bootstrap, and Spearman rank correlations.
Limits: one median beam for all galaxies (AO and seeing-limited beams differ), and a0_i is a point
estimate, not the harness's joint likelihood.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy import integrate, stats

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "02_galaxy_dynamics/highz_data/RC100_NestorShachar2023_table3_transcribed.csv"
OUT = ROOT / "02_galaxy_dynamics/A0_HIGHZ_RESOLUTION_TEST.json"
C_KMS, H0, OM = 299792.458, 67.36, 0.3153          # Planck 2018 base LCDM (as the measurement audit)
BEAM_ARCSEC = 0.53
KPC_M = 3.0857e19


def d_a_kpc(z):
    dc = C_KMS / H0 * integrate.quad(lambda t: 1 / math.sqrt(OM * (1 + t) ** 3 + 1 - OM), 0, z)[0]
    return dc / (1 + z) * 1000.0                    # Mpc -> kpc


rows = list(csv.DictReader(l for l in SRC.open() if not l.startswith("#")))
z, lna0, lnr, lnmb, keep = [], [], [], [], 0
for r in rows:
    f = float(r["fDM"])
    if not 0.05 <= f <= 0.95:                       # mu -> 1 or 0 makes x singular
        continue
    vc, re = float(r["Vc_kms"]) * 1e3, float(r["Re_kpc"])
    g_obs = vc ** 2 / (re * KPC_M)
    mu = 1 - f
    a0 = g_obs / (mu / math.sqrt(1 - mu * mu))
    theta = re / d_a_kpc(float(r["z"])) * 206264.806
    z.append(float(r["z"])); lna0.append(math.log(a0)); lnr.append(math.log(BEAM_ARCSEC / theta))
    lnmb.append(float(r["logMbar"])); keep += 1
z, lna0, lnr, lnmb = map(np.array, (z, lna0, lnr, lnmb))

X = np.column_stack([np.ones_like(z), lnr, z, lnmb])
beta = np.linalg.lstsq(X, lna0, rcond=None)[0]
rng = np.random.default_rng(20261013)
boot = []
for _ in range(2000):
    i = rng.integers(0, len(z), len(z))
    boot.append(np.linalg.lstsq(X[i], lna0[i], rcond=None)[0][1])
lo, hi = np.percentile(boot, [2.5, 97.5])
rho_ar, p_ar = stats.spearmanr(lna0, lnr)
rho_rz, p_rz = stats.spearmanr(lnr, z)
resid = lna0 - np.column_stack([np.ones_like(z), z, lnmb]) @ np.linalg.lstsq(np.column_stack([np.ones_like(z), z, lnmb]), lna0, rcond=None)[0]
rho_part, p_part = stats.spearmanr(resid, lnr)

res = {"n_used": keep, "n_table": len(rows), "beam_arcsec": BEAM_ARCSEC,
       "median_beam_over_Re": round(float(np.exp(np.median(lnr))), 3),
       "slope_lna0_on_ln_beam_over_Re": round(float(beta[1]), 4), "slope_95ci_bootstrap": [round(float(lo), 4), round(float(hi), 4)],
       "spearman_lna0_vs_resolution": [round(float(rho_ar), 3), round(float(p_ar), 4)],
       "spearman_resolution_vs_z": [round(float(rho_rz), 3), round(float(p_rz), 4)],
       "spearman_lna0_resid_vs_resolution": [round(float(rho_part), 3), round(float(p_part), 4)]}
# what the allowed slope can do to the shape test: resolution worsens with z, so a bias in ln a0 per
# unit ln(beam/R_e) becomes a z-trend; compare with the Hubble-shape growth over z = 0.6..2.6
dlnr_dz = float(np.polyfit(z, lnr, 1)[0])
E = lambda zz: math.sqrt(OM * (1 + zz) ** 3 + 1 - OM)
res["dln_beam_over_Re_dz"] = round(dlnr_dz, 4)
res["implied_lna0_shift_z0p6_to_2p6_at_ci"] = [round(float(lo) * 2 * dlnr_dz, 3), round(float(hi) * 2 * dlnr_dz, 3)]
res["hubble_shape_lna0_growth_z0p6_to_2p6"] = round(math.log(E(2.6) / E(0.6)), 3)
res["check_median_beam_over_Re_vs_paper_0p75"] = abs(res["median_beam_over_Re"] - 0.75) < 0.05
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
