"""Newton convergence of the FE solver with the local physics in long double (16x32 and 24x48, g_e = 0.03 a0)."""
import math, time, numpy as np
import solve_fe as FE
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T; g_e = 0.03*FE.A0T
import sys; EXT = sys.argv[1] == "ld"
for n in ((16, 32), (24, 48)):
    g = FE.GridFE(*n, 1e-4, math.asinh(100.), math.asinh(100.))
    P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), g_e, extended=EXT)
    t = time.time()
    x, ok, gn = P.newton(FE.initial_guess_fe(g, P.dm, M, b), tol=1e-11, maxit=20, verbose=True)
    print(f"{n}: converged {ok}, residual {gn:.2e}, {time.time()-t:.0f}s", flush=True)
