"""How many pairs the joint step-model test needs: replicate the d<500 pc
strict sample k times (k independent Newtonian draws per binary) and measure
power at a 5% step. Synthetic only. Output: WIDE_BINARY_STEP_POWER_SCALE.json
"""
import json
import sys

import numpy as np
from scipy.stats import norm

import wide_binary_fish as F
import wide_binary_step as S
import wide_binary_step_power3 as P3

NTRIAL = 20


def synth_k(b, m, onset, amp, k):
    sub = {kk: v[m] for kk, v in b.items()}
    vt, idx = F.simulate(sub, "N", nmc=k)
    s = sub["s"][idx]
    return s, vt * (1 + amp * norm.cdf((np.log(s) - np.log(onset)) / P3.W))


c = dict(np.load(sys.argv[1]))
F.DMAX = S.DMAX = 0.5
b = F.prepare(c, F.CUTS["clean"])
_ok, ex = S.surviving_mask(c, F.CUTS["clean"], b)
d = ex["d_pc"]
tests = {"test1": (d < 200, d >= 200, float(np.median(d[d >= 200]) / np.median(d[d < 200]))),
         "test2": (b["M"] < 1.0, b["M"] >= 1.5, float(np.sqrt(np.median(b["M"][b["M"] >= 1.5]) / np.median(b["M"][b["M"] < 1.0]))))}
out = {}
for k in (5, 10, 20):
    for tname, (m1, m2, P) in tests.items():
        r = {}
        for truth, shift in (("AU", 1.0), ("alternative", P)):
            calls = [P3.call(P3.slice_R(*synth_k(b, m1, P3.S0, 0.05, k)),
                             P3.slice_R(*synth_k(b, m2, P3.S0 * shift, 0.05, k)), P) for _ in range(NTRIAL)]
            want = "AU" if truth == "AU" else "alternative"
            r[f"truth_{truth}_correct"] = calls.count(want) / NTRIAL
        out[f"k{k}_{tname}"] = dict(k=k, n_pairs=int(k * len(b["s"])), **r)
        print(k, k * len(b["s"]), tname, r, flush=True)
json.dump(out, open("WIDE_BINARY_STEP_POWER_SCALE.json", "w"), indent=1)
