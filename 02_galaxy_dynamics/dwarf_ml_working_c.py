#!/usr/bin/env python3
"""Four dwarfs at the working C. Protocol: PREREG_DWARF_ML_WORKING_C_2026-10-16.md."""

import json
from pathlib import Path

import numpy as np

import dwarf_screening_test as D
import tidal_screening_two_body as T

HERE = Path(__file__).resolve().parent
A0 = 1.1607e-10
XS = 703588428133.2817
C_WORK = 0.579124707982253
V_MW = 200.0
NAMES = ("Crater II", "Carina", "Leo II", "Sculptor")
ML_GRID = np.geomspace(0.05, 400.0, 4000)
SQRT6 = np.sqrt(6.0)


def g_in(d, ml, screen):
    M = ml * d["L"] * D.MSUN
    rh = d["rh_pc"] * D.PC
    gN = D.G * M / rh**2
    if not screen:
        return gN, gN, 0.0
    Dgc = d["D_gc_kpc"] * 1e3 * D.PC
    gext = (V_MW * 1e3) ** 2 / Dgc
    Hext = SQRT6 * gext / Dgc
    r = np.geomspace(0.2 * rh, 5.0 * rh, 64)
    Hint = SQRT6 * D.G * M / r**3
    gNr = D.G * M / r**2
    x = T.C**2 * np.hypot(Hint, Hext) / A0**2
    y = np.maximum(gNr / A0, 1e-12)
    s, s1, _ = T.screen(x, XS, "action")
    nu = T.nu(y)
    w = -(T.C**2 / 2) * s1 * (T.P(y) - C_WORK) * Hint / np.hypot(Hint, Hext)
    gW = (2 / SQRT6) * np.gradient(r**3 * w, r) / r**3
    i = int(np.argmin(np.abs(r - rh)))
    geff = (1 + s[i] * (nu[i] - 1)) * gNr[i]
    return geff - gW[i], gNr[i], float(gW[i])


def sigma_kms(d, ml, screen):
    rh = d["rh_pc"] * D.PC
    gin, gN, gW = g_in(d, ml, screen)
    sig = np.sqrt(max(gin, 0.0) * rh / 3.0) / 1e3
    return sig, gW


def solve(d, target, screen):
    pred = np.array([sigma_kms(d, ml, screen)[0] for ml in ML_GRID])
    if target <= pred[0]:
        return float(ML_GRID[0]), "below-grid"
    if target >= pred[-1]:
        return float(ML_GRID[-1]), "above-grid"
    i = int(np.searchsorted(pred, target))
    w = (target - pred[i - 1]) / (pred[i] - pred[i - 1])
    ml = float(ML_GRID[i - 1] * (ML_GRID[i] / ML_GRID[i - 1]) ** w)
    return ml, "ok"


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
        r["name"]: r["ML_needed_1sig_low"]
        for r in json.loads((HERE / "BRANCH_RULE_SATELLITES.json").read_text())
    }
    rows = []
    rel = []
    for name in NAMES:
        d = by[name]
        lo = max(d["sig"] - d["em"], 1e-3)
        ml_n, _ = solve(d, d["sig"], False)
        ml_n_lo, _ = solve(d, lo, False)
        ml, _ = solve(d, d["sig"], True)
        ml_lo, _ = solve(d, lo, True)
        rel.append(abs(ml_n_lo - published[name]) / published[name])
        _, gW = sigma_kms(d, ml_lo, True)
        rows.append(
            {
                "name": name,
                "sigma_obs": d["sig"],
                "sigma_minus": d["em"],
                "ML_newton": ml_n,
                "ML_newton_1sig_low": ml_n_lo,
                "published_newton_1sig_low": published[name],
                "ML_screen": ml,
                "ML_screen_1sig_low": ml_lo,
                "g_W_at_decision_m_s2": gW,
            }
        )
        print(
            f"{name:12s} Newton-1s {ml_n_lo:.3f}  screen {ml:.3f}  screen-1s {ml_lo:.3f}",
            flush=True,
        )
    informative = bool(max(rel) < 1e-3)
    lows = [r["ML_screen_1sig_low"] for r in rows]
    out = {
        "prereg": "PREREG_DWARF_ML_WORKING_C_2026-10-16.md",
        "C": C_WORK,
        "x_star": XS,
        "a0": A0,
        "V_mw_kms": V_MW,
        "newton_control_informative": informative,
        "newton_control_max_rel": float(max(rel)),
        "verdict": verdict(lows) if informative else "not informative",
        "rows": rows,
    }
    path = HERE / "DWARF_ML_WORKING_C.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print(
        "informative",
        informative,
        "max_rel",
        max(rel),
        "verdict",
        out["verdict"],
        flush=True,
    )


if __name__ == "__main__":
    main()
