#!/usr/bin/env python3
"""Action-form Gamma_r table at the working C, decision field only.

Same masses, mass ratios, orientations and radius grid as the published
action-form table. x* is held fixed. Output is the interpolant the C3
script reads. It does not rewrite TIDAL_TWO_BODY_TABLE.json.
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
RADII = json.loads((HERE / "TIDAL_TWO_BODY_SUMMARY.json").read_text())["forms"][
    "action"
]["r_kau"]


def cell(args):
    M, rk, q1, mu = args
    s = T.solve_binary(
        M, rk * 1e3 * T.AU, q1, mu, 1.9e-10, "action", xs=XS, c_zero=C_WORK
    )
    return M, rk, q1, mu, s["Gamma_r"], s["Gamma_t"]


def main():
    jobs = [
        (M, float(rk), q1, float(mu))
        for M in T.TAB_M
        for rk in RADII
        for q1 in T.TAB_Q1
        for mu in T.TAB_MU
    ]
    raw = {}
    with get_context("fork").Pool(4) as pool:
        for i, (M, rk, q1, mu, gr, gt) in enumerate(
            pool.imap_unordered(cell, jobs, chunksize=4)
        ):
            raw[(M, rk, q1, mu)] = (gr, gt)
            if i % 100 == 0:
                print(f"{i}/{len(jobs)}", flush=True)
    Gr = np.empty((len(T.TAB_M), len(RADII), len(T.TAB_Q1), len(T.TAB_MU)))
    Gt = np.empty_like(Gr)
    for a, M in enumerate(T.TAB_M):
        for b, rk in enumerate(RADII):
            for c, q1 in enumerate(T.TAB_Q1):
                for d, mu in enumerate(T.TAB_MU):
                    Gr[a, b, c, d], Gt[a, b, c, d] = raw[(M, float(rk), q1, float(mu))]
    out = {
        "C": C_WORK,
        "g_e": 1.9e-10,
        "x_star": XS,
        "a0": T.A0,
        "M_sun": T.TAB_M,
        "r_kau": list(map(float, RADII)),
        "q1": T.TAB_Q1,
        "mu_e": list(map(float, T.TAB_MU)),
        "mu_e_weights": list(map(float, T.TAB_MU_W)),
        "Gamma_r": np.round(Gr, 7).tolist(),
        "Gamma_t": np.round(Gt, 7).tolist(),
    }
    path = HERE / "WORKING_C_GAMMA_TABLE.json"
    path.write_text(json.dumps(out))
    print("wrote", path, "n", len(jobs), flush=True)


if __name__ == "__main__":
    main()
