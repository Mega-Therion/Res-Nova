#!/usr/bin/env python3
"""POST-HOC cross-check for P-OM-1 (NOT part of the pre-registered verdict; written after the FAIL was seen).

Runs the frozen P-OM-1 forward model on B21's GAMA isolated-lens RAR (spectroscopic redshifts, so the isolation
criterion stays reliable at large radii, B21 Sect. 5.2). B21 report MOND chi2_red = 0.8 on GAMA against 4.6 on
KiDS-bright. Question asked: does the same frozen model (nothing fitted) that fails on KiDS-bright pass on GAMA?
Output: POM1_POSTHOC_GAMA.json
"""
import json

import numpy as np

import pom1_lensing_rar as P

P.ensure_data()
g, y, e = P.load_esd("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt")
C = P.load_cov("Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt", [g])
rel = g > P.GBAR_RELIABLE
idx = np.where(rel)[0]
out = {"status": "POST-HOC; does not change the pre-registered P-OM-1 verdict",
       "all_bins": P.verdict_block(g, y, C, "GAMA isolated, all bins (spectroscopic isolation)"),
       "gbar_gt_7.56e-14": P.verdict_block(g[rel], y[rel], C[np.ix_(idx, idx)], "GAMA isolated, same range as the KiDS primary"),
       "bins": [{"gbar": float(a), "gobs": float(b), "err": float(c),
                 "obs_over_pred_a0_obs": float(b / P.pred(np.array([a]), P.A0_OBS)[0])} for a, b, c in zip(g, y, e)]}
json.dump(out, open(P.HERE / "POM1_POSTHOC_GAMA.json", "w"), indent=1)
for k in ("all_bins", "gbar_gt_7.56e-14"):
    b = out[k]
    print(k, "chi2(a0=1.1607) =", round(b["a0_obs_1.1607"]["chi2"], 2), "/", b["n_bins"], " p =", round(b["a0_obs_1.1607"]["p"], 4),
          "| a0 fit", f"{b['a0_fit']['a0_best']:.3e}", [f"{v:.3e}" for v in b["a0_fit"]["a0_1sigma"]])
