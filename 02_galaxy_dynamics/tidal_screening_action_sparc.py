#!/usr/bin/env python3
"""SPARC under the action form at the Cassini-calibrated x*_A. PREREG_TIDAL_WIDE_BINARY_2026-10-15.md, section 5.
1. The divergence part: refit SPARC with S(x) at x*_A (fit_tidal, h_z = 0.1 kpc); K1 rule dchi2 <= 0 unchanged.
2. The W part is not solved for disks. Estimate at each SPARC point from the spherical identity
   g_W,r = (2/sqrt6) r^-3 (r^3 w~)',  w~ = -(c^2/2) S'(x) P(y) |H| / Hn,  reported as |g_W| / g_N. An estimate, not a fit.
Writes TIDAL_ACTION_SPARC.json.
"""
import json

import numpy as np

import environment_screening as E
import tidal_screening_sparc_cassini as TS
import tidal_screening_two_body as T
from parameter_ledger import KM_TO_M, KPC_TO_M, load, v_bary_sq
from sparc_paths import resolve_sparc_dir


def main():
    xs = json.load(open("TIDAL_ACTION_CASSINI.json"))["x_star_action"]
    d = resolve_sparc_dir(None)
    gals = load(d)
    sb = TS.sb_columns(d, gals)
    base = [E.fit1(g, TS.A0, 0.0) for g in gals]
    cb = sum(c for c, _ in base)
    fits = [TS.fit_tidal(g, sb[g["name"]], TS.A0, xs, 0.1) for g in gals]
    ct = sum(f[0] for f in fits)
    est = []
    for g in gals:
        yd, yb, fd = TS.YD_MEAN, (TS.YB_MEAN if g["has_bulge"] else 0.0), 1.0
        r = g["r"] * fd * KPC_TO_M
        gN = v_bary_sq(g, yd, yb, fd) * KM_TO_M**2 / r
        x = TS.tidal_x(g, sb[g["name"]], yd, yb, fd, 0.1)
        y = np.maximum(gN / TS.A0, 1e-12)
        _, S1, _ = T.screen(x, xs, "action")
        wt = -(T.C**2 / 2) * S1 * T.P(y)
        gW = (2 / np.sqrt(6)) * np.gradient(r**3 * wt, r) / r**3
        est.append(float(np.max(np.abs(gW) / gN)))
    out = {"x_star_action": xs, "n": len(gals), "chi2_unscreened": cb, "chi2_divergence_part_at_xA": ct,
           "dchi2": ct - cb, "verdict_K1_divergence_part": "PASS" if ct - cb <= 0 else "FAIL",
           "galaxies_worse": int(sum(f[0] > b[0] + 1e-6 for f, b in zip(fits, base))),
           "max_fractional_dg_divergence_part": max(f[2] for f in fits), "max_x": max(f[3] for f in fits),
           "W_part_spherical_estimate_max_gW_over_gN": max(est),
           "W_part_estimate_note": "spherical identity at the ledger-mean Upsilon; a disk solve is not done"}
    print(json.dumps({k: v for k, v in out.items() if k != "W_part_estimate_note"}, indent=1))
    json.dump(out, open("TIDAL_ACTION_SPARC.json", "w"), indent=1)


if __name__ == "__main__":
    main()
