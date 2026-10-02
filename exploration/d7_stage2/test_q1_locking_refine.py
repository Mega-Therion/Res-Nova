"""Background confirmation of the locking diagnosis on the Q1 solver (solve_fe.py): if locking suppresses the wind
response, the v = 1 km/s response should grow roughly as 1/h^2 under refinement (32x64 -> 48x96 -> 64x128:
about x2.2, then x4 overall). If it does not grow, something besides locking also suppresses it.
Setup: g_e = 0.003 a0, box asinh(300)."""
import math, time, numpy as np
import solve_fe as FE
from stage_c_continuation import observables
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T; g_e = 0.003*FE.A0T
for n in ((32, 64), (48, 96), (64, 128)):
    t = time.time()
    g, P0, xs, r0 = FE.static_solution(*n, M, b, g_e, 300.0)
    ref = observables(P0, xs)
    P = FE.ProblemFE(g, 1.0/299792.458, FE.plummer_fn(M, b), g_e)
    x, ok, gn = P.newton(xs, tol=1e-10, maxit=25, verbose=False)
    ob = observables(P, x)
    print(f"{n}: converged {ok} ({gn:.1e}); at r_h: Y/Y_static - 1 = {ob['0.3kpc']['Y']/ref['0.3kpc']['Y'] - 1:+.3e}, "
          f"g/g_static - 1 = {ob['0.3kpc']['g']/ref['0.3kpc']['g'] - 1:+.3e}; u/tilt {ob['max_u']/((vf**2/b)/0.1):.3e}; {time.time()-t:.0f}s", flush=True)
