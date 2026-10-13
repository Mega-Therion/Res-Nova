#!/usr/bin/env python3
"""Does the flat high-z a0 shape survive where fDM is set by the data rather than the prior?

Open systematic (i) of 02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md: RC100's fDM comes from a
GR+NFW fit that carries a photometric prior with its own z-trend, so a flat a0(z) could come from the prior.
Where the kinematics constrain fDM tightly, the prior has less weight. If the prior were faking constancy,
the shape slope n should differ between galaxies with tight and loose fDM errors.

Model [D]: per galaxy, a0_i from the fDM route under mu_std at R_e (as a0_highz_resolution_test.py), then
    ln a0_i = c + n ln E(z) + b (log M_bar - 10.5)
weighted by the propagated fDM error. n = 1 is the Hubble shape, n = 0 is constant a0. Fitted on the
whole sample and on the halves split at the median fractional fDM error, with a 2000-sample bootstrap.
Limits: per-galaxy point estimates, not the joint likelihood; e_fDM measures total constraint, not the
prior's weight directly.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "02_galaxy_dynamics/highz_data/RC100_NestorShachar2023_table3_transcribed.csv"
OUT = ROOT / "02_galaxy_dynamics/A0_HIGHZ_PRIOR_SPLIT_TEST.json"
OM = 0.3153
KPC_M = 3.0857e19


def ln_a0(vc, re, f):
    g = (vc * 1e3) ** 2 / (re * KPC_M)
    mu = 1 - f
    return math.log(g * math.sqrt(1 - mu * mu) / mu)


rows = list(csv.DictReader(l for l in SRC.open() if not l.startswith("#")))
D = []
for r in rows:
    f, ef = float(r["fDM"]), float(r["e_fDM"])
    if not 0.05 <= f <= 0.95:
        continue
    vc, re = float(r["Vc_kms"]), float(r["Re_kpc"])
    y = ln_a0(vc, re, f)
    dy = (ln_a0(vc, re, min(f + 0.01, 0.99)) - ln_a0(vc, re, max(f - 0.01, 0.01))) / 0.02
    sig = math.hypot(dy * ef, 2 * float(r["e_Vc_kms"]) / vc, float(r["e_Re_kpc"]) / re)
    z = float(r["z"])
    D.append((y, math.log(math.sqrt(OM * (1 + z) ** 3 + 1 - OM)), float(r["logMbar"]) - 10.5, sig, ef / f, z, f, ef))
D = np.array(D)


def fit(A, rng=None, nboot=2000):
    y, lnE, m, s = A[:, 0], A[:, 1], A[:, 2], A[:, 3]
    def one(i):
        X = np.column_stack([np.ones(len(i)), lnE[i], m[i]]) / s[i, None]
        return np.linalg.lstsq(X, y[i] / s[i], rcond=None)[0][1]
    n = one(np.arange(len(y)))
    rng = rng or np.random.default_rng(20261013)
    bs = [one(rng.integers(0, len(y), len(y))) for _ in range(nboot)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"N": int(len(y)), "n": round(float(n), 3), "n_95ci": [round(float(lo), 3), round(float(hi), 3)],
            "median_frac_e_fDM": round(float(np.median(A[:, 4])), 3)}


cut = np.median(D[:, 4])
t = D[:, 4] <= cut
ca = np.median(D[:, 7])
res = {"all": fit(D), "tight_frac_e_fDM": fit(D[t]), "loose_frac_e_fDM": fit(D[~t]),
       "split_at_frac_e_fDM": round(float(cut), 3),
       "confound_tight_vs_loose_median_z": [round(float(np.median(D[t, 5])), 2), round(float(np.median(D[~t, 5])), 2)],
       "confound_tight_vs_loose_median_fDM": [round(float(np.median(D[t, 6])), 2), round(float(np.median(D[~t, 6])), 2)],
       "tight_abs_e_fDM": fit(D[D[:, 7] <= ca]), "loose_abs_e_fDM": fit(D[D[:, 7] > ca]),
       "fDM_below_0p4": fit(D[D[:, 6] < 0.4]), "fDM_above_0p4": fit(D[D[:, 6] >= 0.4]),
       "hubble_n": 1.0, "constant_n": 0.0,
       "reading": "The two error splits disagree in sign, and the fractional split tracks fDM and z, so the published table cannot separate prior from data."}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
