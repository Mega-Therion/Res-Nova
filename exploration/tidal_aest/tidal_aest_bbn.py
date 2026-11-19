#!/usr/bin/env python3
"""Tidal screen with an AeST two-field (QUMOND-type) scalar sector: BBN and local-G gates. [D] algebra, [O] model."""
import json, math
GM = 1.32712e20; AU = 1.495978707e11; c = 2.99792458e8; a0 = 1.1607e-10; xstar = 7.04e11
nu = lambda y: math.sqrt(0.5 * (1 + math.sqrt(1 + 4 / y**2)))     # mu_std QUMOND nu
def share(r):
    g = GM / r**2; x = c**2 * (2 * GM / r**3 * math.sqrt(1.5)) / a0**2   # Frobenius norm of point-mass tidal tensor: sqrt(6) GM/r^3
    S = 1 / (1 + (x / xstar) ** 2)
    return (nu(g / a0) - 1) * S, (nu(g / a0) - 1), S, x
rows = {}
for name, r in (("Mercury", 0.387), ("Earth", 1.0), ("Saturn", 9.537), ("Neptune", 30.1)):
    s, raw, S, x = share(r * AU); rows[name] = {"share": s, "unscreened_share": raw, "S": S, "x": x}
# BBN: c4_eff = local scalar share (it vanishes in the tracking sense: QUMOND has no linear-regime share)
out = {"rows": rows}
for KB in (0.0, 0.05, 0.1, 0.2):
    c4 = rows["Saturn"]["share"]
    GN_over_G = 1 / (1 - (KB + c4) / 2); Gc_over_G = 1.0
    out[f"G_cosmo_over_G_local_KB={KB}"] = Gc_over_G / GN_over_G
# r-dependence of the anomaly: extra acceleration delta g = share(r) * g_N, as constant-type precession at Mercury
rm = 0.387 * AU; dg = rows["Mercury"]["share"] * GM / rm**2
out["mercury_extra_accel"] = dg
out["mercury_prec_mas_cy_upper"] = 2 * math.pi * dg * rm**2 / GM * (100 / 0.2408) * 206264.8e3
out["verdict"] = {"BBN_5pct_KB_le_0.1": all(out[f"G_cosmo_over_G_local_KB={k}"] >= 0.95 for k in (0.0, 0.05, 0.1)),
                  "mercury_ok": out["mercury_prec_mas_cy_upper"] <= 1.6}
print(json.dumps(out, indent=1)); json.dump(out, open("TIDAL_AEST_BBN.json", "w"), indent=1)
