#!/usr/bin/env python3
"""Stellar M/L for four dwarfs under nu6. Protocol: PREREG_NU6_DWARF_ML_2026-10-16.md.

No parameter is fitted. The BLK-39 rule is applied to the numbers this script computes.
"""

import json
from pathlib import Path

import numpy as np

import dwarf_screening_test as D

HERE = Path(__file__).resolve().parent
A0 = 1.1607e-10
V_MW = 200.0
NAMES = ("Crater II", "Carina", "Leo II", "Sculptor")
ML_GRID = np.geomspace(0.05, 400.0, 4000)


def nu6(y):
    y = np.maximum(y, 1e-100)
    return (0.5 * (1.0 + np.sqrt(1.0 + 4.0 * y**-6.0))) ** (1.0 / 6.0)


def boost_nu6(x):
    """1/mu6(x), with x = g/a0 and y*nu6(y) = x."""
    x = float(x)
    lo, hi = 1e-12, max(x, 1.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mid * float(nu6(mid)) < x:
            lo = mid
        else:
            hi = mid
    y = 0.5 * (lo + hi)
    return float(x / y)


def sigma_kms(d, ml, boost):
    M = ml * d["L"] * D.MSUN
    rh = d["rh_pc"] * D.PC
    sN = np.sqrt(D.G * M / (3.0 * rh))
    siso = (4.0 * D.G * M * A0 / 81.0) ** 0.25
    sefe = sN * np.sqrt(boost)
    s = min(siso, sefe)
    which = "iso" if siso <= sefe else "efe"
    return s / 1e3, sN / 1e3, which


def solve(d, target, boost):
    pred = np.array([sigma_kms(d, ml, boost)[0] for ml in ML_GRID])
    if target <= pred[0]:
        return float(ML_GRID[0]), "below-grid"
    if target >= pred[-1]:
        return float(ML_GRID[-1]), "above-grid"
    i = int(np.searchsorted(pred, target))
    w = (target - pred[i - 1]) / (pred[i] - pred[i - 1])
    ml = float(ML_GRID[i - 1] * (ML_GRID[i] / ML_GRID[i - 1]) ** w)
    return ml, sigma_kms(d, ml, boost)[2]


def verdict(lows):
    if all(v <= 3.0 for v in lows):
        return "pass"
    if all(v >= 5.0 for v in lows):
        return "fail"
    return "inconclusive"


def main():
    by = {d["name"]: d for d in D.load()}
    missing = [n for n in NAMES if n not in by]
    if missing:
        raise SystemExit(f"missing dwarfs: {missing}")
    published = {
        r["name"]: r
        for r in json.loads((HERE / "BRANCH_RULE_SATELLITES.json").read_text())
    }
    rows = []
    rel = []
    for name in NAMES:
        d = by[name]
        ge = (V_MW * 1e3) ** 2 / (d["D_gc_kpc"] * 1e3 * D.PC)
        x = ge / A0
        b = boost_nu6(x)
        ml, branch = solve(d, d["sig"], b)
        lo_sig = max(d["sig"] - d["em"], 1e-3)
        ml_lo, branch_lo = solve(d, lo_sig, b)
        ml_n = 2.0 * (d["sig"] / D.predict(d, 2.0, V_MW, A0)["N"]) ** 2
        ml_n_lo = 2.0 * (lo_sig / D.predict(d, 2.0, V_MW, A0)["N"]) ** 2
        pub = published[name]["ML_needed_1sig_low"]
        rel.append(abs(ml_n_lo - pub) / pub)
        sig_at2, _, _ = sigma_kms(d, 2.0, b)
        rows.append(
            {
                "name": name,
                "D_gc_kpc": d["D_gc_kpc"],
                "sigma_obs": d["sig"],
                "sigma_minus": d["em"],
                "g_ext_over_a0": x,
                "boost": b,
                "sigma_nu6_at_ML2": sig_at2,
                "branch_at_central": branch,
                "branch_at_decision": branch_lo,
                "ML_nu6": ml,
                "ML_nu6_1sig_low": ml_lo,
                "ML_newton": ml_n,
                "ML_newton_1sig_low": ml_n_lo,
                "published_newton_1sig_low": pub,
            }
        )
        print(
            f"{name:12s} boost {b:.4f}  nu6 ML {ml:.3f}  at -1s {ml_lo:.3f} ({branch_lo})  Newton -1s {ml_n_lo:.3f}"
        )
    informative = bool(max(rel) < 1e-3)
    lows = [r["ML_nu6_1sig_low"] for r in rows]
    out = {
        "prereg": "PREREG_NU6_DWARF_ML_2026-10-16.md",
        "a0": A0,
        "V_mw_kms": V_MW,
        "newton_control_informative": informative,
        "newton_control_max_rel": float(max(rel)),
        "verdict": verdict(lows) if informative else "not informative",
        "rows": rows,
    }
    path = HERE / "NU6_DWARF_ML.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path)
    print("informative", informative, "verdict", out["verdict"])


if __name__ == "__main__":
    main()
