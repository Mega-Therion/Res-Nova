"""Exploratory: Newton straight from the static held state at 15, 10, 7, 5, 3, 2, 1 km/s (16x32, g_e = 0.003 a0, box
asinh(300)); the stripped branch traced down from 100 km/s is lost just below 20 km/s with no eigenvalue approaching zero
(DIAG_FOLD_C1.txt), so test whether steady states exist below 20 km/s by another route. Also retries each failed speed from
the 20 km/s stripped state with the fixed Newton."""
import math, time, numpy as np
import solve_c1 as C
from stage_c_c1 import observables
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T
g = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
rho = C.plummer_fn(M, b)
P0 = C.ProblemC1(g, 0.0, rho, g_e)
xs, ok, gn = P0.newton(C.initial_guess_c1(g, P0.dm, M, b), tol=1e-11, maxit=20, verbose=False, freeze=P0.lambda_dofs())
ref = observables(P0, xs); tilt = (vf**2/b)/0.1
x20 = np.load("cache_branch/stripped_ge0.003_16x32_v20.npy")
for vk in (15.0, 10.0, 7.0, 5.0, 3.0, 2.0, 1.0):
    for start, x0 in (("static", xs), ("stripped@20", x20)):
        t = time.time(); P = C.ProblemC1(g, vk/299792.458, rho, g_e)
        x, ok, gn = P.newton(x0, tol=1e-10, maxit=30, verbose=False)
        msg = ""
        if ok:
            ob = observables(P, x); k = "0.3kpc"
            msg = f"g/g_static {ob[k]['g']/ref[k]['g']:.4f}, g/phihat-flux {ob[k]['g']/ob[k]['flux']:.3f}, Y/Y_static {ob[k]['Y']/ref[k]['Y']:.4f}, u/tilt {ob['max_u']/tilt:.2e}"
            np.save(f"cache_branch/lowv_{start.replace('@','_')}_ge0.003_16x32_v{vk:g}.npy", x)
        print(f"v = {vk:g} from {start}: converged {ok} ({gn:.1e}) {msg} [{time.time()-t:.0f}s]", flush=True)
