#!/usr/bin/env python3
"""Cross-checks for DRAG_FIT: (1) extend the x0 profile beyond the pre-registered grid (BAO+SN+CMB);
(2) the same pipeline with w0wa (CPL) dark energy and standard G, for comparison."""
import json, sys
import numpy as np
from scipy.optimize import minimize
exec(open("drag_fit.py").read().split("out = {}")[0])
prof = [(float(x), fit(fix_x0=x)[0]) for x in np.linspace(0.0, 2.0, 21)]
cbest = min(c for _, c in prof)
ORH2_ = ORH2
def E_cpl(z, h, Om, w0, wa):
    a = 1 / (1 + z); Or = ORH2_ / h**2; OL = 1 - Om - Or
    de = OL * a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return np.sqrt(Om / a**3 + Or / a**4 + de)
def chi2_cpl(q):
    h, Om, w0, wa = q
    global E
    E0 = E
    E = lambda z, h_, Om_, x0_: E_cpl(z, h_, Om_, w0, wa)
    try: v = chi2_bg((h, Om, 0.0))
    finally: E = E0
    return v
best = None
for s in ([0.68, 0.31, -0.9, -0.5], [0.68, 0.31, -1.0, 0.0], [0.68, 0.31, -0.7, -1.0]):
    r = minimize(chi2_cpl, s, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 8000})
    if best is None or r.fun < best.fun: best = r
lcdm = fit(fix_x0=0.0)[0]
out = {"x0_profile_BAO_SN_CMB": prof, "x0_2sigma_extended": [min(x for x, c in prof if c <= cbest + 4), max(x for x, c in prof if c <= cbest + 4)],
       "w0wa": {"chi2": float(best.fun), "params_h_Om_w0_wa": [float(v) for v in best.x], "dchi2_vs_LCDM": float(best.fun - lcdm)},
       "LCDM_chi2": lcdm}
print(json.dumps(out, indent=1)); json.dump(out, open("DRAG_CROSSCHECK.json", "w"), indent=1)
