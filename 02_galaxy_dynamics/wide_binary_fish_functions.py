"""Robustness of WIDE_BINARY_FISH model predictions to the interpolating function and a0.
Measured R(s) is model-independent and taken from WIDE_BINARY_FISH.json; only the model
curves are recomputed. Same pre-registered chi2 (4 dof, 18.5).
Output: WIDE_BINARY_FISH_FUNCTIONS.json
"""
import json
import sys

import numpy as np

import wide_binary_fish as w

FUN = {
    "mu_std (nu_2)": lambda y: (0.5 * (1 + np.sqrt(1 + 4 * y**-2.0))) ** 0.5,
    "simple (nu_1)": lambda y: 0.5 * (1 + np.sqrt(1 + 4 / y)),
    "RAR (nubar_0.5)": lambda y: 1 / (-np.expm1(-np.sqrt(y))),
    "nu_6": lambda y: (0.5 * (1 + np.sqrt(1 + 4 * y**-6.0))) ** (1 / 6),
    "nuhat_4": lambda y: (-np.expm1(-y**2.0)) ** (-1 / 4),
}
A0S = [1.042e-10, 1.2e-10]
meas = json.load(open("WIDE_BINARY_FISH.json"))
c = dict(np.load(sys.argv[1]))
out = {}
for name, cut in w.CUTS.items():
    b = w.prepare(c, cut)
    rows = meas[name]["data"]["rows"]
    for fn, nu in FUN.items():
        for a0 in A0S:
            w.nu_std, w.A0 = nu, a0
            preds = {k: [] for k in ["F", "E", "S", "P"]}
            ctrl = None
            for i, (lo, hi) in enumerate(w.BINS):
                m = (b["s"] >= lo) & (b["s"] < hi)
                sub = {k: v[m] for k, v in b.items()}
                pdf, cdf = w.template(w.simulate(sub, "N")[0])
                al = {k: w.fit_alpha(w.simulate(sub, k, nmc=40)[0], pdf, cdf, fix_c=0)["alpha"]
                      for k in preds}
                if i == 0:
                    ctrl = al
                else:
                    for k in preds:
                        preds[k].append(al[k] / ctrl[k])
            chi2 = {k: float(sum(((r["R"] - p) / r["sigma"]) ** 2 for r, p in zip(rows, v)))
                    for k, v in preds.items()}
            key = f"{name}|{fn}|a0={a0:.3e}"
            out[key] = dict(pred=preds, chi2=chi2)
            print(key, {k: [round(x, 3) for x in v] for k, v in preds.items()},
                  {k: round(v, 1) for k, v in chi2.items()}, flush=True)
json.dump(out, open("WIDE_BINARY_FISH_FUNCTIONS.json", "w"), indent=1)
