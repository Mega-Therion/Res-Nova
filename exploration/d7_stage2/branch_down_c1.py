#!/usr/bin/env python3
"""Exploratory (not gated): follow the stripped steady state found at 100 km/s (16x32, g_e = 0.003 a0, box asinh(300);
test_c1_wind.py) up to 300 km/s and down toward v = 0 by continuation, to see where that branch ends. Same observables
as stage_c_c1.py. Output: BRANCH_DOWN_C1_ge0.003_16x32.json."""
import json, math, time
import numpy as np
import solve_c1 as C
from stage_c_c1 import observables, near_zero_modes
C_KMS = 299792.458
vf = 10/C_KMS; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T; Q0 = 0.1
g = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
rho = C.plummer_fn(M, b)
P0 = C.ProblemC1(g, 0.0, rho, g_e)
xs, ok, gn = P0.newton(C.initial_guess_c1(g, P0.dm, M, b), tol=1e-11, maxit=20, verbose=False, freeze=P0.lambda_dofs())
ref = observables(P0, xs); tilt = (vf**2/b)/Q0
log = {"static_residual": gn, "rows": []}
def record(v, x, ok, gn, P, secs):
    ob = observables(P, x); k = "0.3kpc"
    row = {"v_kms": v, "converged": bool(ok), "residual": gn, "seconds": secs,
           "g_ratio_static": ob[k]["g"]/ref[k]["g"], "g_ratio_phihat_flux": ob[k]["g"]/ob[k]["flux"],
           "Y_ratio": ob[k]["Y"]/ref[k]["Y"], "u_over_tilt": ob["max_u"]/tilt}
    if ok:
        row["near_zero_modes"] = near_zero_modes(P, x)
    log["rows"].append(row); json.dump(log, open("BRANCH_DOWN_C1_ge0.003_16x32.json", "w"), indent=1)
    m0 = row.get("near_zero_modes", {}).get("modes", [{}])[0]
    print(f"v = {v:g}: converged {ok} ({gn:.1e}); g/g_static {row['g_ratio_static']:.4f}, g/phihat-flux {row['g_ratio_phihat_flux']:.3f}, "
          f"Y/Y_static {row['Y_ratio']:.4f}, u/tilt {row['u_over_tilt']:.2e}; eig nearest 0 {m0.get('eig')} ({m0.get('field')}); {secs:.0f}s", flush=True)
t = time.time(); P = C.ProblemC1(g, 100/C_KMS, rho, g_e)
x100, ok, gn = P.newton(xs, tol=1e-10, maxit=25, verbose=False); record(100.0, x100, ok, gn, P, time.time()-t)
for seq in ((150.0, 200.0, 300.0), (75.0, 50.0, 30.0, 20.0, 15.0, 10.0, 7.0, 5.0, 3.0, 2.0, 1.5, 1.0, 0.7, 0.5, 0.3, 0.1)):
    x = x100
    for v in seq:
        t = time.time(); P = C.ProblemC1(g, v/C_KMS, rho, g_e)
        xn, ok, gn = P.newton(x, tol=1e-10, maxit=25, verbose=False)
        record(v, xn, ok, gn, P, time.time()-t)
        if not ok:
            print(f"branch lost at v = {v:g} km/s (from the previous converged speed)", flush=True)
            break
        x = xn
