#!/usr/bin/env python3
"""Exploratory (not gated): trace the stripped steady state (16x32, g_e = 0.003 a0, box asinh(300)) downward from 100 km/s
with adaptive steps (secant predictor, then last solution; bisect on failure down to 1/64 of the step or 0.02 km/s), using
the fixed Newton (stops instead of stepping uphill). Saves each converged state. The first trace (branch_down_c1.py, no
bisection, old Newton) lost the branch between 30 and 20 km/s. Output: BRANCH_DOWN_C1_V2_ge0.003_16x32.json."""
import json, math, os, time
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
os.makedirs("cache_branch", exist_ok=True)
log = {"static_residual": gn, "rows": []}
def record(v, x, gn, P, secs):
    ob = observables(P, x); k = "0.3kpc"
    row = {"v_kms": v, "residual": gn, "seconds": round(secs, 1), "g_ratio_static": ob[k]["g"]/ref[k]["g"],
           "g_ratio_phihat_flux": ob[k]["g"]/ob[k]["flux"], "Y_ratio": ob[k]["Y"]/ref[k]["Y"], "u_over_tilt": ob["max_u"]/tilt,
           "near_zero_modes": near_zero_modes(P, x)}
    log["rows"].append(row); json.dump(log, open("BRANCH_DOWN_C1_V2_ge0.003_16x32.json", "w"), indent=1)
    np.save(f"cache_branch/stripped_ge0.003_16x32_v{v:g}.npy", x)
    m0 = row["near_zero_modes"].get("modes", [{}])[0]
    print(f"v = {v:g}: residual {gn:.1e}; g/g_static {row['g_ratio_static']:.4f}, g/phihat-flux {row['g_ratio_phihat_flux']:.3f}, "
          f"Y/Y_static {row['Y_ratio']:.4f}, u/tilt {row['u_over_tilt']:.2e}; eig nearest 0 {m0.get('eig')} ({m0.get('field')}); {secs:.0f}s", flush=True)
t = time.time(); P = C.ProblemC1(g, 100/C_KMS, rho, g_e)
x_prev, ok, gn = P.newton(xs, tol=1e-10, maxit=25, verbose=False)
assert ok, f"100 km/s did not converge ({gn:.1e})"
record(100.0, x_prev, gn, P, time.time()-t)
x_pp, v_prev, v_pp = None, 100.0, None
for v_target in (75.0, 50.0, 40.0, 30.0, 25.0, 20.0, 15.0, 12.0, 10.0, 8.0, 6.0, 5.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.0, 0.7, 0.5, 0.3, 0.1):
    v_try, step0 = v_target, v_prev - v_target
    while True:
        t = time.time(); P = C.ProblemC1(g, v_try/C_KMS, rho, g_e)
        guess = x_prev if x_pp is None else x_prev + (v_try - v_prev)/(v_prev - v_pp)*(x_prev - x_pp)
        x, ok, gn = P.newton(guess, tol=1e-10, maxit=30, verbose=False)
        if not ok and x_pp is not None:
            x, ok, gn = P.newton(x_prev, tol=1e-10, maxit=30, verbose=False)
        if ok:
            record(v_try, x, gn, P, time.time()-t)
            x_pp, v_pp, x_prev, v_prev = x_prev, v_prev, x, v_try
            if v_try == v_target:
                break
            v_try = v_target
            continue
        print(f"v = {v_try:g}: Newton failed ({gn:.1e}) from {v_prev:g}; bisecting", flush=True)
        if v_prev - v_try <= max(0.02, step0/64):
            log["lost"] = {"last_converged_kms": v_prev, "failed_at_kms": v_try, "residual": gn}
            json.dump(log, open("BRANCH_DOWN_C1_V2_ge0.003_16x32.json", "w"), indent=1)
            print(f"BRANCH LOST between {v_prev:g} and {v_try:g} km/s", flush=True)
            raise SystemExit
        v_try = 0.5*(v_prev + v_try)
print("BRANCH TRACED to the lowest speed", flush=True)
