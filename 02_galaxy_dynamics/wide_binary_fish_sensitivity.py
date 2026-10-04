"""Exploratory (NOT pre-registered) checks on WIDE_BINARY_FISH:
1. eccentricity-prior sensitivity: gamma(s) shifted by -0.3, +0.3;
2. re-anchoring R to the 2-5 kAU bin instead of 0.5-2 kAU.
Output: WIDE_BINARY_FISH_SENSITIVITY.json
"""
import json
import sys

import numpy as np

import wide_binary_fish as w

base_gamma = w.gamma_of_s
c = dict(np.load(sys.argv[1]))
out = {}
for name, cut in w.CUTS.items():
    b = w.prepare(c, cut)
    for dg in (-0.3, 0.0, 0.3):
        w.gamma_of_s = lambda s, dg=dg: np.clip(base_gamma(s) + dg, 0.0, 2.0)
        res = w.run_bins(b, b["vt"], f"{name}/dgamma={dg}")
        rows, chi2 = w.ratios(res)
        # re-anchor to the 2-5 kAU bin
        a = res[1]
        re = []
        for r in res[2:]:
            R = r["alpha"] / a["alpha"]
            s = R * np.hypot((r["hi"] - r["lo"]) / 2 / r["alpha"], (a["hi"] - a["lo"]) / 2 / a["alpha"])
            re.append(dict(bin=r["bin"], R=R, sigma=s,
                           models={k: r["models"][k] / a["models"][k] for k in r["models"]}))
        chi2_re = {k: float(sum(((x["R"] - x["models"][k]) / x["sigma"]) ** 2 for x in re))
                   for k in ["N", "F", "E", "S", "P"]}
        out[f"{name}/dgamma={dg}"] = dict(rows=rows, chi2=chi2, reanchored_rows=re,
                                          chi2_reanchored_3dof=chi2_re)
json.dump(out, open("WIDE_BINARY_FISH_SENSITIVITY.json", "w"), indent=1, default=float)
