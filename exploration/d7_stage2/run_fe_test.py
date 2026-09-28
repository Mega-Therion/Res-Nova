import math, time, numpy as np
import solve_fe as FE
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T
for (nR, nz) in ((16, 32), (24, 48), (32, 64)):
    g = FE.GridFE(nR, nz, 1e-4, math.asinh(100.), math.asinh(100.))
    P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), 0.0)
    x0 = FE.initial_guess_fe(g, P.dm, M, b)
    t = time.time(); print(f"--- FE {nR}x{nz}: {P.dm.ndof} dofs", flush=True)
    x, ok, gn = P.newton(x0, tol=1e-8, maxit=25, verbose=True)
    nd = P.nodes(x); U = np.hypot(nd[FE.FIX['U_R']], nd[FE.FIX['U_z']])
    print(f"FE {nR}x{nz}: converged {ok}, residual {gn:.2e}, max|u| = {U.max():.2e}, {time.time()-t:.0f}s", flush=True)
