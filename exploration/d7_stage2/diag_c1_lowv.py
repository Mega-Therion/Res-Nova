"""Isolated dwarf (g_e = 0, box asinh(100), 16x32), C1 solver: why does Newton from the static state fail at tiny wind
speeds? Near-zero spectrum of the equilibrated Hessian at v = 0 and 0.125 km/s, the first Newton step's size per field,
and the fixed-Newton residual trajectory at 0.125 km/s."""
import math, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spla
import solve_c1 as C
from stage_c_c1 import near_zero_modes, observables
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T
g = C.GridC1(16, 32, 1e-4, math.asinh(100.), math.asinh(100.))
rho = C.plummer_fn(M, b)
P0 = C.ProblemC1(g, 0.0, rho, 0.0)
x1, _, _ = P0.newton(C.initial_guess_c1(g, P0.dm, M, b), tol=1e-11, maxit=20, verbose=False, freeze=P0.lambda_dofs())
xs, ok, gn = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
print(f"static (Lambda free): converged {ok} ({gn:.1e})", flush=True)
for vk in (0.0, 0.125):
    P = C.ProblemC1(g, vk/299792.458, rho, 0.0)
    m = near_zero_modes(P, xs, k=8)
    print(f"v = {vk} km/s near-zero modes: " + "; ".join(f"{r['eig']:+.2e} {r['field']}({r['weight']})" for r in m.get("modes", [])), flush=True)
P = C.ProblemC1(g, 0.125/299792.458, rho, 0.0)
grad, H, _ = P.grad_hess(xs)
Sd = sps.diags(1/np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()))
step = Sd @ P.solve_linear(Sd @ H @ Sd, -(Sd @ grad))
idx = P.dm.index; lab = {"W_R": "Omega", "W_z": "omega", "U_R": "Lambda", "U_z": "psi", "F": "s"}
for n in C.NAMES:
    mm = np.unique(idx[C.FIX[n]][idx[C.FIX[n]] >= 0])
    print(f"   first step, {lab.get(n, n):6s}: max|step| {np.abs(step[mm]).max():.2e}, max|x_static| {np.abs(xs[mm]).max():.2e}", flush=True)
ob0 = observables(P0, xs); ob1 = observables(P, xs + step)
print(f"after the full first step: g/g_static(r_h) {ob1['0.3kpc']['g']/ob0['0.3kpc']['g']:.4f}, max|u| {ob1['max_u']:.2e} (tilt {(vf**2/b)/0.1:.2e})", flush=True)
x, ok, gn = P.newton(xs, tol=1e-10, maxit=25, verbose=True)
print(f"fixed Newton at 0.125 km/s: converged {ok} ({gn:.1e})")
