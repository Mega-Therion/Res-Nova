#!/usr/bin/env python3
"""Exploratory diagnostic (no solve): does a Hessian direction soften as the box grows?
Runs stage_c_c1.near_zero_modes on the five cached converged fixed-resolution box-sweep solutions
(box_sweep_c1.py 16 32 fixed; 100 km/s, g_e = 0) and records, per box, the six smallest |eigenvalues| of the
equilibrated wind Hessian and the field that dominates each. Hypothesis under test (PREREG_BOX_EXTEND_2026-10-06.md,
attempt-2 note): a near-null direction appears with box size and explains the line-search failures beyond 1000 kpc.
Sequential, one box at a time. Writes BOX_ZERO_MODES_C1.json only."""

import json, math, time
import numpy as np
import solve_c1 as C
from stage_c_c1 import near_zero_modes

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
V = 100 / 299792.458
CASES = [
    (100.0, 16, 32),
    (300.0, 20, 40),
    (1000.0, 23, 46),
    (3000.0, 27, 54),
    (10000.0, 30, 60),
]
out = {
    "note": "equilibrated wind Hessian at the cached converged stripped state; eig = smallest |eigenvalues| (eigsh, sigma=0)",
    "rows": [],
}
for B, nR, nz in CASES:
    t = time.time()
    g = C.GridC1(nR, nz, 1e-4, math.asinh(B), math.asinh(B))
    P = C.ProblemC1(g, V, C.plummer_fn(M, b), 0.0)
    x = np.load(f"cache_branch/boxsweep_B{B:g}_{nR}x{nz}_v100.npy")
    nz_modes = near_zero_modes(P, x, k=6)
    row = {
        "edge_kpc": 0.1 * B,
        "grid": [nR, nz],
        "ndof": int(P.dm.ndof),
        "modes": nz_modes,
        "seconds": round(time.time() - t, 1),
    }
    out["rows"].append(row)
    json.dump(out, open("BOX_ZERO_MODES_C1.json", "w"), indent=1)
    m = nz_modes.get("modes", [])
    print(
        f"edge {0.1*B:g} kpc ({nR}x{nz}, {P.dm.ndof} dof): "
        + (
            ", ".join(f"{r['eig']:.3e} [{r['field']} {r['weight']}]" for r in m)
            if m
            else str(nz_modes)
        )
        + f"  ({row['seconds']:.0f}s)",
        flush=True,
    )
