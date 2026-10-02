"""Precision floor at finite wind: one Newton solve at v = 100 and 300 km/s from the static solution (16x32), for
g_e = 0.03 a0 and 0.003 a0 (box asinh(300)), tol 1e-11."""
import math, time, numpy as np
import solve_fe as FE
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T
for ge, box in ((0.03, 100.0), (0.003, 300.0)):
    g = FE.GridFE(16, 32, 1e-4, math.asinh(box), math.asinh(box))
    P0 = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), ge*FE.A0T)
    xs, ok, gn = P0.newton(FE.initial_guess_fe(g, P0.dm, M, b), tol=1e-11, maxit=20, verbose=False)
    print(f"g_e = {ge} a0, box asinh({box:g}): static converged {ok}, residual {gn:.1e}", flush=True)
    for vk in (100.0, 300.0):
        P = FE.ProblemFE(g, vk/299792.458, FE.plummer_fn(M, b), ge*FE.A0T)
        t = time.time()
        x, ok, gn = P.newton(xs, tol=1e-11, maxit=30, verbose=True)
        U = np.abs(x[P.dm.offsets[FE.FIX['U_R']]:P.dm.offsets[FE.FIX['U_z']+1]]).max()
        print(f"   v = {vk:g} km/s: converged {ok}, residual {gn:.1e}, max|u| {U:.2e} (stealth tilt {(vf**2/b)/0.1:.2e}), {time.time()-t:.0f}s", flush=True)
