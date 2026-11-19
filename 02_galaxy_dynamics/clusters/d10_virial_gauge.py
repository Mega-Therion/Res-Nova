#!/usr/bin/env python3
"""D10 mu^2 Phi correction with the gauge fixed at the x_H = 154 virial boundary (PREREG_D10_VIRIAL_GAUGE.md)."""
import json, math, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py"); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
spec2 = importlib.util.spec_from_file_location("gt", "d10_gauge_test.py")
MPC, G, MS, A0 = cm.MPC_M, cm.G_SI, cm.MSUN, cm.A0
H0i = cm.H0_KMS / cm.C_KMS
K2 = 3 * H0i**2 * cm.OM_M / (4 * 0.1**2 * 1.23e-8)
MU = math.sqrt(2 * K2 / (2 - 0.1)) * 0.1 / MPC
RCF, N = 0.1, 6000
M200 = {}
for l in open("corasaniti2021_table1_lensing.dat"):
    if len(l) < 50: continue
    M200[cm.norm(l[0:20])] = float(l[27:32])
rows = []
for key, c in cm.load().items():
    M500 = c["M500"] * 1e14 * MS; fbar = c["fgas"] + 0.015
    r500 = cm.r_delta(M500, c["z"]); rc = RCF * r500
    r200 = cm.r_delta(M200[key] * 1e14 * MS, c["z"], 200.0); rv = r200 * (200 / 177.8) ** (1 / 3)
    norm = fbar * M500 / ((r500 / rc) - math.atan(r500 / rc))
    r = np.linspace(1e-4 * r500, rv, N); dr = r[1] - r[0]
    Menc = norm * ((r / rc) - np.arctan(r / rc)); uE = G * Menc / r**2; g = uE + np.sqrt(uE * A0)
    Phi = -np.flip(np.cumsum(np.flip(g) * dr))          # Phi(rv) = 0
    corr = -MU**2 * np.cumsum(r**2 * Phi) * dr
    i5 = int(np.searchsorted(r, r500)); W0 = G * Menc[i5]; W = W0 + corr[i5]
    uE1 = max(W, 0) / r[i5] ** 2; g1 = uE1 + math.sqrt(uE1 * A0)
    rows.append(dict(name=c["name"], rv_over_r500=rv / r500, W_over_W0=W / W0, R_mu2=M500 / (g1 * r[i5] ** 2 / G)))
md = lambda a: float(np.median(a))
out = {"gauge": "Phi(r_v)=0, r_v at x_H=154 (mean enclosed density 177.8 rho_c)", "N": len(rows),
       "median_rv_over_r500": md([x["rv_over_r500"] for x in rows]),
       "median_expansion_param": md([x["W_over_W0"] - 1 for x in rows]),
       "median_R_mu2": md([x["R_mu2"] for x in rows]), "rows": rows}
ep, R = out["median_expansion_param"], out["median_R_mu2"]
out["verdict"] = ("CLOSES at first order" if 0.8 <= R <= 1.25 and ep < 0.5 else
                  "INCONCLUSIVE (R in range, expansion param >= 0.5)" if 0.8 <= R <= 1.25 else "FAILS (R outside [0.8,1.25])")
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
for x in rows: print(f"  {x['name']:<20} rv/r500={x['rv_over_r500']:.2f}  W/W0={x['W_over_W0']:.2f}  R={x['R_mu2']:.2f}")
json.dump(out, open("D10_VIRIAL_GAUGE.json", "w"), indent=1)
