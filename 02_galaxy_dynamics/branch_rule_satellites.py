#!/usr/bin/env python3
"""Branch-selection rule vs Milky Way satellites (D7 supplement, 2026-09-27).
Rule under test: a system moving through an ambient aether faster than both its escape speed and the linear hold
threshold C*v_f (C = 0.19-0.27, D3 note 7 sec.26) is on the stealth/dragged branch, i.e. Newtonian. Satellites move at
100-640 km/s through the Milky Way's (held) aether, so the rule predicts Newtonian dynamics. Measure what stellar M/L
each satellite would then need: sigma_obs^2 / sigma_N(M/L=2)^2 * 2 (sigma_N from dwarf_screening_test, stars only)."""
import json, numpy as np
import dwarf_screening_test as D
from efe_quadrupole_q2 import A0_DERIVED
rows = []
for d in D.load():
    if d["name"] in ("Large Magellanic Cloud", "Small Magellanic Cloud", "Sagittarius"): continue
    p = D.predict(d, 2.0, 200, A0_DERIVED)
    ml_need = 2.0 * (d["sig"] / p["N"]) ** 2
    lo = max(d["sig"] - d["em"], 1e-3); ml_need_lo = 2.0 * (lo / p["N"]) ** 2          # at the -1 sigma dispersion
    vesc = np.sqrt(2 * D.G * 2.0 * d["L"] * D.MSUN / (d["rh_pc"] * D.PC)) / 1e3
    rows.append({"name": d["name"], "sig": d["sig"], "sigN": p["N"], "sigMOND": p["MOND"], "ML_needed": ml_need, "ML_needed_1sig_low": ml_need_lo, "v_esc_kms": vesc})
rows.sort(key=lambda r: r["ML_needed"])
n = len(rows)
for thr in (3, 5, 10):
    k = sum(r["ML_needed_1sig_low"] > thr for r in rows)
    print(f"satellites needing stellar M/L > {thr:2d} if Newtonian (even at sigma - 1 sigma): {k}/{n}")
print(f"\n{'dwarf':18s} {'sig_obs':>7s} {'sig_N':>6s} {'sig_MOND':>8s} {'M/L needed':>10s} {'(at -1s)':>9s} {'v_esc':>6s}")
for r in rows:
    print(f"{r['name'][:18]:18s} {r['sig']:7.2f} {r['sigN']:6.2f} {r['sigMOND']:8.2f} {r['ML_needed']:10.1f} {r['ML_needed_1sig_low']:9.1f} {r['v_esc_kms']:6.1f}")
json.dump(rows, open("BRANCH_RULE_SATELLITES.json", "w"), indent=1)
