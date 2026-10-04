"""Uncertainty for WIDE_BINARY_STEP: bootstrap of the matched median ratio,
an unmatched random-pairing comparison, and a near/near null.
Output: WIDE_BINARY_STEP_BOOTSTRAP.json
"""
import json
import sys

import numpy as np

import wide_binary_fish as F
import wide_binary_step as S

c = dict(np.load(sys.argv[1]))
rng = np.random.default_rng(7)
out = {}
for name, cut in F.CUTS.items():
    b = F.prepare(c, cut)
    _, ex = S.surviving_mask(c, cut, b)
    s, vt, M, d, r = b["s"], b["vt"], b["M"], ex["d_pc"], ex["rca"]
    near_i = np.where((s >= 1000) & (s < 2000))[0]
    far_i = np.where((s >= 2000) & (s < 5000))[0]
    used = np.zeros(len(near_i), bool)
    rat = []
    for j in far_i:
        sc = (((M[near_i] - M[j]) / 0.15) ** 2 + ((d[near_i] - d[j]) / 20) ** 2
              + (np.log10(r[near_i] + 1e-6) - np.log10(r[j] + 1e-6)) ** 2)
        sc[used] = 1e9
        k = int(np.argmin(sc))
        if sc[k] > 6:
            continue
        used[k] = True
        if vt[near_i[k]] > 0 and vt[j] < 5 and vt[near_i[k]] < 5:
            rat.append(vt[j] / vt[near_i[k]])
    rat = np.array(rat)
    n = len(rat)
    bs = [np.median(rng.choice(rat, n)) for _ in range(2000)]
    a = vt[far_i]; a = a[a < 5]
    bn = vt[near_i]; bn = bn[bn < 5]
    un = [np.median(rng.choice(a, n) / rng.choice(bn, n)) for _ in range(500)]
    nn = [np.median(rng.choice(bn, n) / rng.choice(bn, n)) for _ in range(500)]
    out[name] = dict(n=n, matched_median=float(np.median(rat)), matched_se=float(np.std(bs)),
                     unmatched_random_pair_median=float(np.median(un)),
                     null_near_near_median=float(np.median(nn)), null_se=float(np.std(nn)))
    print(name, out[name])
json.dump(out, open("WIDE_BINARY_STEP_BOOTSTRAP.json", "w"), indent=1)
