#!/usr/bin/env python3
"""How much does the pressure-support correction move the high-z a0 shape?

Open part of systematic (ii) in 02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md: the Vc scale.
RC100's circular velocity includes a pressure-support correction for an exponential disk with constant
dispersion (Burkert et al. 2010; Nestor Shachar+2023 eq. 8), which at R_e reads
    V_circ^2 = V_rot^2 + 3.36 sigma0^2        [C]
Turbulence rises with z, so a wrong correction scale would put a z-trend into a0.

Test [D]: rescale the correction by s (s = 1 as published, s = 0 none, s = 2 doubled):
    V_c'^2 = V_c^2 + (s - 1) 3.36 sigma0^2,   V_bar^2 = (1 - fDM) V_c^2 held fixed,   fDM' = 1 - V_bar^2 / V_c'^2,
recompute per-galaxy a0 (fDM route, mu_std, at R_e) and refit the shape slope n in
    ln a0_i = c + n ln E(z) + b (log M_bar - 10.5),
weighted as in a0_highz_prior_split_test.py. n = 1 is the Hubble shape, n = 0 constant.
Limits: the correction is applied at R_e only; per-galaxy point estimates.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "02_galaxy_dynamics/highz_data/RC100_NestorShachar2023_table3_transcribed.csv"
OUT = ROOT / "02_galaxy_dynamics/A0_HIGHZ_PRESSURE_SCALE_TEST.json"
OM, KPC_M, K_BURKERT = 0.3153, 3.0857e19, 3.36

rows = list(csv.DictReader(l for l in SRC.open() if not l.startswith("#")))


def ln_a0(vc2, re, f):
    g = vc2 * 1e6 / (re * KPC_M)
    mu = 1 - f
    return math.log(g * math.sqrt(1 - mu * mu) / mu)


def dataset(s):
    D = []
    for r in rows:
        f0, ef = float(r["fDM"]), float(r["e_fDM"])
        if not 0.05 <= f0 <= 0.95:
            continue
        vc, sg, re = float(r["Vc_kms"]), float(r["sigma0_kms"]), float(r["Re_kpc"])
        vb2 = (1 - f0) * vc * vc
        vc2 = vc * vc + (s - 1) * K_BURKERT * sg * sg
        if vc2 <= vb2 * 1.0526:                   # keep fDM' >= 0.05, as for the published values
            continue
        f = 1 - vb2 / vc2
        if f > 0.95:
            continue
        y = ln_a0(vc2, re, f)
        dy = (ln_a0(vc2, re, min(f + 0.01, 0.99)) - ln_a0(vc2, re, max(f - 0.01, 0.01))) / 0.02
        sig = math.hypot(dy * ef, 2 * float(r["e_Vc_kms"]) / vc, float(r["e_Re_kpc"]) / re)
        z = float(r["z"])
        D.append((y, math.log(math.sqrt(OM * (1 + z) ** 3 + 1 - OM)), float(r["logMbar"]) - 10.5, sig, sg / vc, z))
    return np.array(D)


def fit(A, nboot=2000):
    y, lnE, m, s = A[:, 0], A[:, 1], A[:, 2], A[:, 3]
    def one(i):
        X = np.column_stack([np.ones(len(i)), lnE[i], m[i]]) / s[i, None]
        return np.linalg.lstsq(X, y[i] / s[i], rcond=None)[0][1]
    rng = np.random.default_rng(20261013)
    bs = [one(rng.integers(0, len(y), len(y))) for _ in range(nboot)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"N": int(len(y)), "n": round(float(one(np.arange(len(y)))), 3), "n_95ci": [round(float(lo), 3), round(float(hi), 3)]}


base = dataset(1.0)
res = {"sigma0_over_Vc_vs_z_slope": round(float(np.polyfit(base[:, 5], base[:, 4], 1)[0]), 4),
       "median_sigma0_over_Vc": round(float(np.median(base[:, 4])), 3),
       "scales": {str(s): fit(dataset(s)) for s in (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0)},
       "hubble_n": 1.0, "constant_n": 0.0}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
