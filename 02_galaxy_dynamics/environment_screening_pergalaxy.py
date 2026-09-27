#!/usr/bin/env python3
"""Per-galaxy environmental screening, with controls.
eta_i = e_env,i * 1.2e-10 / a0_derived, e_env from Chae et al. 2020 (large-scale structure,
independent of the rotation curves). Matched set: SPARC galaxies with an e_env value.
Controls: (a) uniform eta = median; (b) e_env shuffled among galaxies (20 permutations).
If the true assignment beats the shuffles, environment itself matters, not just a weaker boost."""
import json
import numpy as np
from environment_screening import fit1, A0_DERIVED
from parameter_ledger import load
from sparc_paths import resolve_sparc_dir

ext = json.load(open("CHAE2020_EXTERNAL_FIELDS.json"))["galaxies"]
gals = [g for g in load(resolve_sparc_dir(None)) if g["name"] in ext]
eta = np.array([ext[g["name"]]["e_env"] * 1.2e-10 / A0_DERIVED for g in gals])
print(f"matched galaxies: {len(gals)}; eta median {np.median(eta):.3f}, range {eta.min():.3f}-{eta.max():.3f}")
def total(etas):
    fits = [fit1(g, A0_DERIVED, e) for g, e in zip(gals, etas)]
    c = sum(x for x, _ in fits)
    med = float(np.median([x / max(len(g["r"]) - k, 1) for (x, k), g in zip(fits, gals)]))
    return c, med
c0, m0 = total(np.zeros(len(gals)))
ct, mt = total(eta)
cu, mu_ = total(np.full(len(gals), np.median(eta)))
rng = np.random.default_rng(1790)
shuf = [total(rng.permutation(eta))[0] for _ in range(20)]
s = 6.09
out = {"n": len(gals), "eta_median": float(np.median(eta)), "unscreened": [c0, m0], "true_eta": [ct, mt], "uniform_median": [cu, mu_],
       "shuffled_chi2": shuf, "dchi2_true_over_s": (ct - c0) / s, "dchi2_uniform_over_s": (cu - c0) / s,
       "true_minus_shuffled_mean_over_s": (ct - np.mean(shuf)) / s, "shuffled_std_over_s": float(np.std(shuf) / s),
       "frac_shuffles_beating_true": float(np.mean(np.array(shuf) <= ct))}
print(f"unscreened:        chi2 {c0:.1f}  t1 median {m0:.3f}")
print(f"true eta:          chi2 {ct:.1f}  t1 median {mt:.3f}  dchi2/s {(ct-c0)/s:+.1f}")
print(f"uniform (median):  chi2 {cu:.1f}  t1 median {mu_:.3f}  dchi2/s {(cu-c0)/s:+.1f}")
print(f"shuffled (20):     mean chi2 {np.mean(shuf):.1f} ± {np.std(shuf):.1f};  true - shuffled mean = {(ct-np.mean(shuf))/s:+.2f} (in chi2/s), shuffle sd {np.std(shuf)/s:.2f}")
print(f"fraction of shuffles doing at least as well as the true assignment: {out['frac_shuffles_beating_true']:.2f}")
json.dump(out, open("ENVIRONMENT_SCREENING_PERGALAXY.json", "w"), indent=1)
