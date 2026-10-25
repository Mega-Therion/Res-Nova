#!/usr/bin/env python3
"""Batch 1 of INVERSE_SCREENING_WORKSTREAM_SPEC.md.

One frozen grid. No refinement after the numbers print.
"""

import json
import sys
from pathlib import Path

import numpy as np

from efe_quadrupole_q2 import A0_DERIVED, Q2
from parameter_ledger import YB_MEAN, YD_MEAN, chi2
from cassini_sparc_joint import nu_n, v_nu
from sparc_paths import resolve_sparc_dir
from parameter_ledger import load

SPEC_GRID = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, None)
Q2_LO = -3e-27
Q2_HI = 9e-27
GE = 1.9e-10
NU2 = nu_n(2)


def nu_s(s):
    if s is None:
        return NU2

    def fn(y):
        y = np.asarray(y, dtype=float)
        return 1.0 + (NU2(y) - 1.0) / (1.0 + (y / s) ** 2)

    return fn


def median_reduced(gals, nu):
    red = []
    for g in gals:
        yb = YB_MEAN if g["has_bulge"] else 0.0
        c = chi2(g, v_nu(g, nu, A0_DERIVED, YD_MEAN, yb, 1.0))
        n = len(g["r"])
        red.append(c / max(n, 1))
    return float(np.median(red)), int(sum(len(g["r"]) for g in gals)), len(gals)


def main():
    gals = load(resolve_sparc_dir(None))
    rows = []
    base, _, _ = median_reduced(gals, NU2)
    for s in SPEC_GRID:
        nu = nu_s(s)
        med, n_pts, n_gal = median_reduced(gals, nu)
        q2, q = Q2(nu, A0_DERIVED, GE)
        delta = 0.0 if s is None else med - base
        cassini = Q2_LO <= q2 <= Q2_HI
        sparc = delta is not None and abs(delta) < 1.0
        row = {
            "s": "inf" if s is None else s,
            "median_reduced_chi2": med,
            "delta_vs_nu2": delta,
            "Q2_s-2": float(q2),
            "q": float(q),
            "n_galaxies": n_gal,
            "n_points": n_pts,
            "sparc_gate": sparc if s is not None else None,
            "cassini_gate": cassini,
            "joint": bool(sparc and cassini) if s is not None else None,
        }
        rows.append(row)
        label = "inf" if s is None else f"{s:g}"
        dlt = "baseline" if delta is None else f"{delta:+.4f}"
        print(
            f"s={label:>5} med={med:.4f} d={dlt:>10} Q2={q2:.3e} "
            f"cassini={cassini} joint={row['joint']}",
            flush=True,
        )
    finite = [r for r in rows if r["s"] != "inf" and r["joint"]]
    winner = min(finite, key=lambda r: r["s"]) if finite else None
    out = {
        "spec": "INVERSE_SCREENING_WORKSTREAM_SPEC.md",
        "a0_m_s-2": A0_DERIVED,
        "g_e_m_s-2": GE,
        "Q2_window_s-2": [Q2_LO, Q2_HI],
        "baseline_median_reduced_chi2": base,
        "rows": rows,
        "smallest_passing_s": None if winner is None else winner["s"],
        "verdict": (
            "NO_JOINT_POINT_ON_FROZEN_GRID" if winner is None else "SMALLEST_PASSING_S"
        ),
    }
    dest = Path(__file__).resolve().parent / "INVERSE_SCREENING_BATCH1.json"
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(out["verdict"], out["smallest_passing_s"], file=sys.stderr)
    print(dest)


if __name__ == "__main__":
    main()
