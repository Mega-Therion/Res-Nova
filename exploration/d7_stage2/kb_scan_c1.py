#!/usr/bin/env python3
"""Pre-registered K_B scan at one grid. Criterion fixed before the run.

Grid, speed, and box match the converged 16x32, v=100 km/s, edge 10 kpc row of
BOX_SWEEP_C1_16x32.json. K_B = 0.5 must reproduce that row's Y/Y_static if the
solver is unchanged. K_B = 0.25 and K_B = 1.0 are the scan.

A held remnant means the Newton solve converges and Y/Y_static > 0.5.
Anything else is recorded and does not adopt a no-go. One grid cannot show
box convergence.
"""

import json
import math
import time

import numpy as np

import solve_c1 as C
import solve_steady as SS
from stage_c_c1 import observables

OUT = "KB_SCAN_C1_16x32.json"
KB_VALUES = (0.25, 0.5, 1.0)
nR, nz, B = 16, 32, 100.0
v = 100.0 / 299792.458
vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
rows = []
for kb in KB_VALUES:
    SS.KB = kb
    t = time.time()
    g = C.GridC1(nR, nz, 1e-4, math.asinh(B), math.asinh(B))
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, 0.0)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    ref = observables(P0, xs) if ok1 else None
    P = C.ProblemC1(g, v, rho, 0.0)
    x, ok, gn = P.newton(xs, tol=1e-10, maxit=40, verbose=False)
    row = {
        "K_B": kb,
        "converged": bool(ok),
        "residual": gn,
        "static_ok": [bool(ok1), bool(ok2)],
        "seconds": round(time.time() - t, 1),
    }
    if ok and ref is not None:
        ob = observables(P, x)
        k = "0.3kpc"
        row["Y_ratio"] = ob[k]["Y"] / ref[k]["Y"]
        row["g_ratio_static"] = ob[k]["g"] / ref[k]["g"]
        row["held_remnant"] = bool(row["Y_ratio"] > 0.5)
    else:
        row["held_remnant"] = False
    rows.append(row)
    print(json.dumps(row), flush=True)
    json.dump(
        {
            "preregistered": "Y/Y_static > 0.5 and converged counts as a held remnant. No no-go is adopted from one grid.",
            "rows": rows,
        },
        open(OUT, "w"),
        indent=1,
    )
print("wrote", OUT)
