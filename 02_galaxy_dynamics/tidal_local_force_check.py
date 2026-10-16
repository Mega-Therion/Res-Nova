#!/usr/bin/env python3
"""How good is the frozen pipeline's local-force step for the tidal screen? (post-hoc check, not pre-registered)
wide_binary_fish.simulate scales each Monte Carlo velocity by sqrt(Gamma) at the orbit's current radius. Here the speed
from the energy integral in Phi(r), built from the orientation-averaged action-form Gamma_r (M = 1 Msun by log-M
interpolation, q1 = 0.5), is compared with sqrt(Gamma(r)) times the Kepler speed, for orbits sharing peri and apo.
Usage: tidal_local_force_check.py [out.json]   (default TIDAL_LOCAL_FORCE_CHECK.json)"""
import json, sys
import numpy as np
from scipy.integrate import cumulative_trapezoid
t = json.load(open("TIDAL_TWO_BODY_TABLE.json"))
r = np.array(t["forms"]["action"]["r_kau"]); M = np.array(t["M_sun"])
out = {}
for ge in ("1.9e-10", "2.4e-10"):
    G = np.array(t["forms"]["action"][ge]["Gamma_r_orientation_avg"])[:, :, 0]   # (M, r) at q1 = 0.5
    lm = np.log(M); w = (np.log(1.0) - lm[2]) / (lm[3] - lm[2])
    g1 = (1 - w) * G[2] + w * G[3]                                                 # M = 1.0 by log-M interpolation
    rr = np.geomspace(r[0], r[-1], 20000); gam = np.interp(np.log(rr), np.log(r), g1)
    acc = gam / rr**2                                                              # units GM = 1, r in kAU
    Phi = cumulative_trapezoid(acc[::-1], rr[::-1], initial=0)[::-1] - gam[-1] / rr[-1]   # -Int_r^inf Gamma/r^2
    P = lambda x: np.interp(x, rr, Phi); Gm = lambda x: np.interp(x, rr, gam)
    rows = []
    for a_k, e in ((6, 0.5), (8, 0.5), (10, 0.5), (12, 0.5), (15, 0.5), (20, 0.5), (8, 0.7), (12, 0.7), (16, 0.7), (25, 0.7), (10, 0.3), (15, 0.3)):
        rp, ra = a_k * (1 - e), a_k * (1 + e)
        L2 = 2 * (P(ra) - P(rp)) / (1 / rp**2 - 1 / ra**2); E = P(rp) + L2 / (2 * rp**2)
        x = np.geomspace(rp * 1.0001, ra * 0.9999, 400)
        v_true = np.sqrt(np.maximum(2 * (E - P(x)), 0))
        v_lf = np.sqrt(Gm(x) * (2 / x - 1 / a_k))
        rel = v_true / v_lf - 1
        # time-weighted mean speed ratio over the orbit (dt ~ dr / v_r; use v_true radial velocity for weights)
        vr = np.sqrt(np.maximum(2 * (E - P(x)) - L2 / x**2, 1e-30)); wt = 1 / vr
        rows.append({"a_kau": a_k, "e": e, "max_abs_dv_over_v": float(np.max(np.abs(rel))),
                     "time_weighted_mean_dv_over_v": float(np.sum(rel * wt) / np.sum(wt))})
    out[ge] = rows
    print(ge, " ".join(f"(a={q['a_kau']},e={q['e']}: max {q['max_abs_dv_over_v']*100:.1f}%, mean {q['time_weighted_mean_dv_over_v']*100:+.1f}%)" for q in rows))
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "TIDAL_LOCAL_FORCE_CHECK.json", "w"), indent=1)
