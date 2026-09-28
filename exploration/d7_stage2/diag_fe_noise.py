"""Gradient noise floor at the stall: residual change under tiny rescales of x, with and without the external field."""
import math, numpy as np, scipy.sparse as sps
import solve_fe as FE
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T
g = FE.GridFE(16, 32, 1e-4, math.asinh(100.), math.asinh(100.))
for ge in (0.0, 0.03*FE.A0T):
    P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), ge)
    x, _, gn = P.newton(FE.initial_guess_fe(g, P.dm, M, b), tol=1e-12, maxit=10, verbose=False)
    grad, H, Y = P.grad_hess(x)
    Sd = 1/np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()); n0 = np.linalg.norm(Sd*P.src)
    off = P.dm.offsets; fF = FE.FIX["F"]
    print(f"g_e = {ge/FE.A0T:.2f} a0: residual {np.linalg.norm(Sd*grad)/n0:.3e}")
    for d in (1e-16, 1e-15, 1e-14, 1e-13, 1e-12):
        g2,_,_ = P.grad_hess(x*(1+d), want_hess=False)
        dg = Sd*(g2-grad); lin = Sd*(H@(d*x))
        print(f"   rescale {d:.0e}: |d grad| {np.linalg.norm(dg)/n0:.3e}, linear prediction {np.linalg.norm(lin)/n0:.3e}, "
              f"|d grad - lin| {np.linalg.norm(dg-lin)/n0:.3e} (F rows {np.linalg.norm((dg-lin)[off[fF]:off[fF+1]])/n0:.3e})")
