"""Is the stripped state's residual acceleration a property of AeST or of the Y floor inside J'? The stripped state has
Y at 1.5-2% of static, within ~14x of EPS_Y = (1e-3 a0)^2, where J' is floored at mu(1e-3). Re-solve the 100 km/s state
(16x32, g_e = 0.003 a0, box asinh(300)) with EPS_Y = (3e-3 a0)^2, (1e-3 a0)^2 (baseline), (3e-4 a0)^2 and (1e-4 a0)^2, each
static + Newton from static, and compare g/g_static, g/phihat-flux, Y/Y_static at r_h. Insensitive -> physical; sensitive
-> artefact of the regularisation."""
import math, time, numpy as np
import solve_c1 as C, solve_steady as SS
from stage_c_c1 import observables
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T
g = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
rho = C.plummer_fn(M, b)
for eps in (3e-3, 1e-3, 3e-4, 1e-4):
    SS.EPS_Y = (eps*C.A0T)**2
    t = time.time()
    P0 = C.ProblemC1(g, 0.0, rho, g_e)
    xs, ok0, g0 = P0.newton(C.initial_guess_c1(g, P0.dm, M, b), tol=1e-11, maxit=25, verbose=False, freeze=P0.lambda_dofs())
    ref = observables(P0, xs)
    P = C.ProblemC1(g, 100/299792.458, rho, g_e)
    x, ok, gn = P.newton(xs, tol=1e-10, maxit=40, verbose=False)
    k = "0.3kpc"
    if ok:
        ob = observables(P, x)
        print(f"EPS_Y = ({eps:g} a0)^2: static {ok0} ({g0:.1e}); 100 km/s converged ({gn:.1e}): g/g_static {ob[k]['g']/ref[k]['g']:.4f}, "
              f"g/phihat-flux {ob[k]['g']/ob[k]['flux']:.3f}, Y/Y_static {ob[k]['Y']/ref[k]['Y']:.4f}; static g/phihat-flux {ref[k]['g']/ref[k]['flux']:.3f} [{time.time()-t:.0f}s]", flush=True)
    else:
        print(f"EPS_Y = ({eps:g} a0)^2: static {ok0} ({g0:.1e}); 100 km/s NOT converged ({gn:.1e}) [{time.time()-t:.0f}s]", flush=True)
