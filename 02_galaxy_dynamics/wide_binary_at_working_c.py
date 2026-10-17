#!/usr/bin/env python3
"""Action-form wide-binary Gamma_r at C=0 and at the working C.

One mass, one mass ratio, the decision Galactic field, x* held fixed.
Orientation average uses the same 4-point Gauss rule as the published table.
"""

import json
from multiprocessing import get_context
from pathlib import Path

import numpy as np

import tidal_screening_two_body as T

HERE = Path(__file__).resolve().parent
XS = 703588428133.2817
SOL = json.loads((HERE / "SCREENED_C_SOLUTIONS.json").read_text())
C_WORK = next(r for r in SOL["fields"] if abs(r["g_e_m_s2"] - 1.9e-10) < 1e-14)[
    "C_oort_peak"
]["C"]
RADII = sorted(set(np.round(np.geomspace(3.0, 40.0, 10), 5).tolist() + [8.0, 17.5]))


def cell(args):
    c_zero, rk, mu = args
    s = T.solve_binary(
        0.8, rk * 1e3 * T.AU, 0.5, mu, 1.9e-10, "action", xs=XS, c_zero=c_zero
    )
    return c_zero, rk, mu, s["Gamma_r"]


def main():
    jobs = [
        (c, rk, float(mu)) for c in (0.0, C_WORK) for rk in RADII for mu in T.TAB_MU
    ]
    raw = {}
    with get_context("fork").Pool(4) as pool:
        for i, (c, rk, mu, g) in enumerate(
            pool.imap_unordered(cell, jobs, chunksize=4)
        ):
            raw[(c, rk, mu)] = g
            if i % 16 == 0:
                print(i, flush=True)
    w = np.array(T.TAB_MU_W)
    rows = []
    for rk in RADII:
        g0 = np.array([raw[(0.0, rk, float(mu))] for mu in T.TAB_MU])
        gw = np.array([raw[(C_WORK, rk, float(mu))] for mu in T.TAB_MU])
        a0, aw = float(0.5 * g0 @ w), float(0.5 * gw @ w)
        rows.append(
            {"r_kau": rk, "Gamma_C0": a0, "Gamma_C_working": aw, "delta": aw - a0}
        )
        print(f"{rk:8.3f}  {a0:.5f}  {aw:.5f}  {aw - a0:+.5f}", flush=True)
    out = {
        "M_sun": 0.8,
        "q1": 0.5,
        "g_e": 1.9e-10,
        "x_star": XS,
        "C_working": C_WORK,
        "published_C0_dip": {"Gamma": 0.901, "r_kau": 8.0},
        "published_C0_peak": {"Gamma": 1.343, "r_kau": 17.5},
        "rows": rows,
    }
    g0 = np.array([r["Gamma_C0"] for r in rows])
    gw = np.array([r["Gamma_C_working"] for r in rows])
    rr = np.array(RADII)
    out["C0_min"] = {"Gamma": float(g0.min()), "r_kau": float(rr[int(np.argmin(g0))])}
    out["C_working_min"] = {
        "Gamma": float(gw.min()),
        "r_kau": float(rr[int(np.argmin(gw))]),
    }
    out["C0_max"] = {"Gamma": float(g0.max()), "r_kau": float(rr[int(np.argmax(g0))])}
    out["C_working_max"] = {
        "Gamma": float(gw.max()),
        "r_kau": float(rr[int(np.argmax(gw))]),
    }
    out["max_abs_delta"] = float(np.max(np.abs(gw - g0)))
    path = HERE / "WIDE_BINARY_AT_WORKING_C.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path, "max |dGamma|", out["max_abs_delta"], flush=True)


if __name__ == "__main__":
    main()
