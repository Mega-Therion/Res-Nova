"""C1 solver at 16x32 (g_e = 0.003 a0, box asinh(300)): (1) the wind's forcing on the Lambda rows at the stage-1 static
state, against the static (discretization) Lambda-row residual; (2) Newton at v = 1, 10, 100 km/s from the static
state with every DOF free: convergence and the observables at r_h."""
import math, time, numpy as np
import solve_c1 as C
from stage_c_continuation import observables
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T
t = time.time()
g = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
P0 = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), g_e)
lam = P0.lambda_dofs()
xs, ok, gn = P0.newton(C.initial_guess_c1(g, P0.dm, M, b), tol=1e-11, maxit=20, verbose=False, freeze=lam)
g0, _, _ = P0.grad_hess(xs, want_hess=False)
ref = observables(P0, xs)
print(f"stage-1 static: residual {gn:.1e}; |Lambda rows| of grad = {np.linalg.norm(g0[lam]):.3e} (absolute); {time.time()-t:.0f}s", flush=True)
for vk in (1.0, 10.0, 100.0):
    P = C.ProblemC1(g, vk/299792.458, C.plummer_fn(M, b), g_e)
    gv, _, _ = P.grad_hess(xs, want_hess=False)
    print(f"  v = {vk:g} km/s: |Lambda rows| of grad at the static state = {np.linalg.norm(gv[lam]):.3e}; "
          f"wind part {np.linalg.norm(gv[lam]-g0[lam]):.3e}", flush=True)
for vk in (1.0, 10.0, 100.0):
    t = time.time()
    P = C.ProblemC1(g, vk/299792.458, C.plummer_fn(M, b), g_e)
    x, ok, gn = P.newton(xs, tol=1e-10, maxit=20, verbose=False)
    ob = observables(P, x)
    k = "0.3kpc"
    print(f"v = {vk:g} km/s: converged {ok} ({gn:.1e}); g/g_static {ob[k]['g']/ref[k]['g']:.4f}, Y/Y_static {ob[k]['Y']/ref[k]['Y']:.4f}, "
          f"u/tilt {ob['max_u']/((vf**2/b)/0.1):.3e}; last solve residual {P.solve_log[-1] if P.solve_log else float('nan'):.1e}; {time.time()-t:.0f}s", flush=True)
