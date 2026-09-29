"""C1 solver, stage-2 stall at ~1e-5 (16x32, g_e = 0.003 a0, box asinh(300)): near-zero spectrum of the equilibrated
Hessian at the stall, the residual's projection on those modes, and whether the Lambda-row residual is noise."""
import math, os, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spla
import solve_c1 as C
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T
g = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
P = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), g_e)
lam = P.lambda_dofs()
path = "/tmp/claude-1000/-home-mega/6821b1a8-78a6-4fa5-b618-17e1fd36c784/scratchpad/c1_stage2_16x32.npy"
if os.path.exists(path):
    x = np.load(path)
else:
    x, _, _ = P.newton(C.initial_guess_c1(g, P.dm, M, b), tol=1e-11, maxit=15, verbose=False, freeze=lam)
    x, _, _ = P.newton(x, tol=1e-11, maxit=8, verbose=False)
    np.save(path, x)
grad, H, Y = P.grad_hess(x)
Sd = 1/np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()); n0 = np.linalg.norm(Sd*P.src)
idx = P.dm.index
slots = {n: np.unique(idx[C.FIX[n]][idx[C.FIX[n]] >= 0]) for n in C.NAMES}
lab = {"U_R": "Lambda", "U_z": "psi", "F": "s"}
r = Sd*grad
print("residual by field: " + ", ".join(f"{lab.get(n, n)} {np.linalg.norm(r[slots[n]])/n0:.2e}" for n in C.NAMES))
A = (sps.diags(Sd)@H@sps.diags(Sd)).tocsc(); A = (0.5*(A+A.T)).tocsc()
ev, V = spla.eigsh(A, k=12, sigma=0, which="LM")
rn = r/np.linalg.norm(r)
for i in np.argsort(np.abs(ev)):
    fw = {lab.get(n, n): float(np.linalg.norm(V[slots[n], i])**2) for n in C.NAMES}
    top = sorted(fw, key=fw.get, reverse=True)[:2]
    print(f"  eig {ev[i]:+.3e}: {top[0]} ({fw[top[0]]:.2f}), {top[1]} ({fw[top[1]]:.2f}); residual overlap {abs(V[:, i] @ rn):.2e}")
rng = np.random.default_rng(3)
for d in (1e-14, 1e-12):
    xp = x*(1 + d*rng.standard_normal(x.size))
    gp, _, _ = P.grad_hess(xp, want_hess=False)
    lin = Sd*(H@(xp - x))
    dr = Sd*(gp - grad) - lin
    print(f"random relative perturbation {d:.0e}: |d residual - linear| in Lambda rows {np.linalg.norm(dr[lam])/n0:.2e}, all rows {np.linalg.norm(dr)/n0:.2e}")
