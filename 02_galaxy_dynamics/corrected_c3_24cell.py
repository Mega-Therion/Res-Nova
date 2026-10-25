#!/usr/bin/env python3
"""24-cell corrected-C3 grid. Contract: CORRECTED_C3_24CELL_SPEC.md. One run."""

import hashlib
import json
import math
from pathlib import Path

import numpy as np

from efe_quadrupole_q2 import Q2

A0_FIT = 1.1607e-10
A0_DER = 1.0422e-10
GE = (1.9e-10, 2.4e-10)
LAMBDAS = (0.1, 1.0, 2.0)
Q2_CENTER = 1.6e-27
Q2_SIGMA = 1.8e-27
Y_GRID = np.logspace(-6, 6, 241)


def mu_std(z):
    z = np.asarray(z, dtype=float)
    return z / np.sqrt(1.0 + z * z)


def x_tot(y):
    y = float(y)
    return math.sqrt((y * y + y * math.sqrt(y * y + 4.0)) / 2.0)


def bisect(f, lo, hi, n=80):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def g_over_a0_d9(ls, y):
    """g/a0 for J' = ls * mu_std(g_phi / ((1+ls) a0))."""
    eta = ls / (1.0 + ls)
    scale = 1.0 + ls
    s = bisect(
        lambda z: ls * (z / scale) / math.sqrt(1.0 + (z / scale) ** 2) * z - eta * y,
        0.0,
        10.0 * y + 10.0,
    )
    return eta * y + s


def nu_interpolant(samples):
    ys = Y_GRID
    logy = np.log(ys)

    def nu(y):
        y = np.asarray(y, dtype=float)
        out = np.empty(y.shape, dtype=float)
        flat = y.ravel()
        out.ravel()[:] = np.interp(np.log(np.maximum(flat, 1e-30)), logy, samples)
        return out

    return nu


def samples_for(branch, ls):
    if branch == "J_total":
        return np.array([x_tot(y) / y for y in Y_GRID])
    if branch != "J_D9":
        raise ValueError(branch)
    return np.array([g_over_a0_d9(ls, float(y)) / float(y) for y in Y_GRID])


def main():
    rows = []
    cache = {}
    for branch in ("J_D9", "J_total"):
        for ls in LAMBDAS:
            key = (branch, None if branch == "J_total" else ls)
            if key not in cache:
                cache[key] = nu_interpolant(samples_for(branch, ls))
            nu = cache[key]
            for a0_name, a0 in (("fitted", A0_FIT), ("derived", A0_DER)):
                for ge in GE:
                    q2, q = Q2(nu, a0, ge)
                    q2 = float(q2)
                    sigma = (q2 - Q2_CENTER) / Q2_SIGMA
                    inside = abs(q2 - Q2_CENTER) <= Q2_SIGMA
                    row = {
                        "branch": branch,
                        "lambda_s": ls,
                        "a0": a0_name,
                        "a0_m_s-2": a0,
                        "g_e_m_s-2": ge,
                        "eta": ls / (1.0 + ls),
                        "split": "K = eta * eta_e, G_hat = eta * G_N",
                        "Q2_s-2": q2,
                        "q": float(q),
                        "sigma": sigma,
                        "cell": "INSIDE" if inside else "OUTSIDE",
                    }
                    rows.append(row)
                    print(
                        f"{branch:8} ls={ls:<3} {a0_name:8} ge={ge:.1e} "
                        f"Q2={q2:.6e} sigma={sigma:+.3f} {row['cell']}",
                        flush=True,
                    )
    n_in = sum(1 for r in rows if r["cell"] == "INSIDE")
    if n_in == len(rows):
        verdict = "ALL_INSIDE"
    elif n_in == 0:
        verdict = "NONE_INSIDE"
    else:
        verdict = "MIXED"
    out = {
        "spec": "CORRECTED_C3_24CELL_SPEC.md",
        "split": "K = eta * eta_e with eta = lambda_s / (1 + lambda_s)",
        "solver": "Hees Q2 of spherical quasistatic nu; not the unpublished LGL collocation",
        "window_center_s-2": Q2_CENTER,
        "window_sigma_s-2": Q2_SIGMA,
        "n_cells": len(rows),
        "n_inside": n_in,
        "verdict": verdict,
        "rows": rows,
    }
    dest = Path(__file__).resolve().parent / "CORRECTED_C3_24CELL.json"
    dest.write_text(json.dumps(out, indent=1) + "\n")
    here = Path(__file__).resolve()
    for path in (here, dest, here.parent / "CORRECTED_C3_24CELL_SPEC.md"):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"sha256 {digest}  {path.name}")
    print("verdict", verdict, "inside", n_in, "of", len(rows))


if __name__ == "__main__":
    main()
