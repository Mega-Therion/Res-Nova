#!/usr/bin/env python3
"""Exploratory (not gated): the steady state of the dwarf at satellite speeds, reached by Newton straight from the static
held solution (continuation from rest is not usable: on the isolated dwarf even 0.125 km/s gives a huge outer-region
response, DIAG_C1_LOWV.txt). Configurations (g_e/a0, box): (0.003, 300), (0, 100), (0.03, 100); speeds 100, 150, 300 km/s
(each from the static state, falling back to the previous speed's solution); grid from argv.
Usage: stripped_highv_c1.py <nR> <nz> [g_e:box ...] (default the three configurations above). Output: STRIPPED_HIGHV_C1_<nR>x<nz>.json (rewritten after every solve).
"""

import json, math, sys, time
import numpy as np
import solve_c1 as C
from stage_c_c1 import observables, near_zero_modes

C_KMS = 299792.458
vf = 10 / C_KMS
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
Q0 = 0.1
nR, nz = int(sys.argv[1]), int(sys.argv[2])
out = {"grid": [nR, nz], "cases": []}
path = f"STRIPPED_HIGHV_C1_{nR}x{nz}" + ("_" + "_".join(sys.argv[3:]).replace(":", "b") if len(sys.argv) > 3 else "") + ".json"
CONFIGS = [tuple(float(t) for t in c.split(':')) for c in sys.argv[3:]] or [(0.003, 300.0), (0.0, 100.0), (0.03, 100.0)]
for ge_a0, box in CONFIGS:
    g_e = ge_a0 * C.A0T
    g = C.GridC1(nR, nz, 1e-4, math.asinh(box), math.asinh(box))
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, g_e)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=20,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    ref = observables(P0, xs)
    case = {
        "g_e_over_a0": ge_a0,
        "box": box,
        "static": {
            "stage1": [bool(ok1), r1],
            "free": [bool(ok2), r2],
            "g_over_phihat_flux_rh": ref["0.3kpc"]["g"] / ref["0.3kpc"]["flux"],
        },
        "speeds": [],
    }
    out["cases"].append(case)
    x_last = None
    for vk in (100.0, 150.0, 300.0):
        t = time.time()
        P = C.ProblemC1(g, vk / C_KMS, rho, g_e)
        x, ok, gn = P.newton(xs, tol=1e-10, maxit=30, verbose=False)
        start = "static"
        if not ok and x_last is not None:
            x, ok, gn = P.newton(x_last, tol=1e-10, maxit=30, verbose=False)
            start = "previous speed"
        row = {
            "v_kms": vk,
            "converged": bool(ok),
            "residual": gn,
            "start": start,
            "seconds": round(time.time() - t, 1),
        }
        if ok:
            ob = observables(P, x)
            for key in ob:
                if key.endswith("kpc"):
                    row[key] = {
                        "g_ratio_static": ob[key]["g"] / ref[key]["g"],
                        "g_ratio_phihat_flux": ob[key]["g"] / ob[key]["flux"],
                        "Y_ratio": ob[key]["Y"] / ref[key]["Y"],
                    }
            row["u_over_tilt"] = ob["max_u"] / ((vf**2 / b) / Q0)
            row["near_zero_modes"] = near_zero_modes(P, x)
            np.save(
                f"cache_branch/highv_ge{ge_a0:g}_box{box:g}_{nR}x{nz}_v{vk:g}.npy", x
            )
            x_last = x
        case["speeds"].append(row)
        json.dump(out, open(path, "w"), indent=1)
        k = "0.3kpc"
        msg = (
            (
                f"g/g_static {row[k]['g_ratio_static']:.4f}, g/phihat-flux {row[k]['g_ratio_phihat_flux']:.3f}, Y/Y_static {row[k]['Y_ratio']:.4f}, "
                f"u/tilt {row['u_over_tilt']:.2e}"
            )
            if ok
            else ""
        )
        print(
            f"g_e {ge_a0:g} box {box:g} ({nR}x{nz}) v = {vk:g}: converged {ok} ({gn:.1e}, from {start}) {msg}",
            flush=True,
        )
