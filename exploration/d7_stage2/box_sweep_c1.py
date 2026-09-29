#!/usr/bin/env python3
"""Exploratory: box-size dependence of the stripped steady state. The isolated dwarf's remainder at r_h fell from
g/g_static = 0.173 (box 10 kpc) to 0.110 (30 kpc) at 100 km/s, so the outer clamp (u = 0, phi = 0 at the box) holds part of
it up. Sweep xi_max = eta_max = asinh(B) for B = 100, 300, 1000, 3000, 10000 (edge at ~B x 0.1 kpc), g_e = 0, v = 100 km/s,
Newton from the static state. Usage: box_sweep_c1.py <nR> <nz>. Output: BOX_SWEEP_C1_<nR>x<nz>.json."""
import json, math, sys, time
import numpy as np
import solve_c1 as C
from stage_c_c1 import observables
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; Q0 = 0.1
nR, nz = int(sys.argv[1]), int(sys.argv[2])
out = {"grid": [nR, nz], "v_kms": 100.0, "g_e_over_a0": 0.0, "rows": []}
for B in (100.0, 300.0, 1000.0, 3000.0, 10000.0):
    t = time.time()
    g = C.GridC1(nR, nz, 1e-4, math.asinh(B), math.asinh(B))
    rho = C.plummer_fn(M, b)
    P0 = C.ProblemC1(g, 0.0, rho, 0.0)
    x1, ok1, r1 = P0.newton(C.initial_guess_c1(g, P0.dm, M, b), tol=1e-11, maxit=25, verbose=False, freeze=P0.lambda_dofs())
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    ref = observables(P0, xs)
    P = C.ProblemC1(g, 100/299792.458, rho, 0.0)
    x, ok, gn = P.newton(xs, tol=1e-10, maxit=40, verbose=False)
    row = {"box_B": B, "edge_kpc": 0.1*B, "static": [bool(ok1), r1, bool(ok2), r2], "converged": bool(ok), "residual": gn,
           "seconds": round(time.time()-t, 1)}
    k = "0.3kpc"
    if ok:
        ob = observables(P, x)
        row.update({"g_ratio_static": ob[k]["g"]/ref[k]["g"], "g_ratio_phihat_flux": ob[k]["g"]/ob[k]["flux"],
                    "Y_ratio": ob[k]["Y"]/ref[k]["Y"], "static_g_over_flux": ref[k]["g"]/ref[k]["flux"],
                    "u_over_tilt": ob["max_u"]/((vf**2/b)/Q0)})
        np.save(f"cache_branch/boxsweep_B{B:g}_{nR}x{nz}_v100.npy", x)
    out["rows"].append(row); json.dump(out, open(f"BOX_SWEEP_C1_{nR}x{nz}.json", "w"), indent=1)
    print(f"box edge {0.1*B:g} kpc: static {ok1}/{ok2}; 100 km/s converged {ok} ({gn:.1e})"
          + (f": g/g_static {row['g_ratio_static']:.4f}, g/phihat-flux {row['g_ratio_phihat_flux']:.3f}, Y/Y_static {row['Y_ratio']:.4f}, static g/flux {row['static_g_over_flux']:.2f}" if ok else "")
          + f" [{row['seconds']:.0f}s]", flush=True)
