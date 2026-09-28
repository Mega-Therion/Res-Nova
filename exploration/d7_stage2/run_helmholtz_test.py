import math, time, numpy as np
import solve_steady as SS
vf = 10/299792.458; b=3e-4; M = 12*math.pi*vf**4/SS.A0T
for (nR, nz) in ((16, 32), (24, 48), (32, 64)):
    g = SS.Grid(nR, nz, 1e-4, math.asinh(100.), math.asinh(100.)); rho = SS.plummer(g, M, b)
    P = SS.ProblemH(g, 0.0, rho, 0.0)
    f0 = SS.initial_guess(g, M, b, 0.0)
    t = time.time(); print(f"--- {nR}x{nz}", flush=True)
    fp, ok, gn = P.newton(f0, tol=1e-9, maxit=25, verbose=True)
    f = P.full(fp); q = (P.D @ f).reshape(g.ncell, SS.NQ); U = np.hypot(q[:, 3*SS.FIX['U_R']], q[:, 3*SS.FIX['U_z']])
    print(f'{nR}x{nz}: converged {ok}, residual {gn:.2e}, max|u| = {U.max():.2e}, {time.time()-t:.0f}s', flush=True)
