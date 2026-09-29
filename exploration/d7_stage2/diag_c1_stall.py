"""C1 solver: where does Newton stall? Residual by field, Taylor remainder along the step split by field group, and the
softest modes' composition, at 16x32 (g_e = 0.003 a0, box asinh(300))."""
import math, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spla, resource, time
import solve_c1 as C
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T
t = time.time()
g = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
P = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), g_e)
x, ok, gn = P.newton(C.initial_guess_c1(g, P.dm, M, b), tol=1e-11, maxit=12, verbose=True)
print(f"ndof {P.dm.ndof}; converged {ok} ({gn:.2e}); peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss//1024} MB; {time.time()-t:.0f}s", flush=True)
grad, H, Y = P.grad_hess(x)
Sd = 1/np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()); n0 = np.linalg.norm(Sd*P.src)
idx = P.dm.index
slots = {n: np.unique(idx[C.FIX[n]][idx[C.FIX[n]] >= 0]) for n in C.NAMES}
lab = {"U_R": "Lambda", "U_z": "psi", "F": "s"}
r = Sd*grad
for n in C.NAMES:
    print(f"  residual in {lab.get(n, n):6s}: {np.linalg.norm(r[slots[n]])/n0:.3e}")
s = Sd*P.solve_linear(sps.diags(Sd)@H@sps.diags(Sd), -(Sd*grad))
groups = {"metric": ["S","W_R","W_z","A","B","C","D"], "Lambda": ["U_R"], "psi": ["U_z"], "s": ["F"]}
for gname, names in groups.items():
    m = np.zeros_like(s)
    for n in names: m[slots[n]] = 1
    sg = s*m
    for lam in (1e-3, 1e-1, 1.0):
        gt,_,_ = P.grad_hess(x+lam*sg, want_hess=False)
        rem = Sd*(gt - grad - lam*(H@sg))
        print(f"  step part {gname:6s} lam {lam:.0e}: Taylor remainder {np.linalg.norm(rem)/n0:.3e}, |lam H s| {np.linalg.norm(Sd*(lam*(H@sg)))/n0:.3e}")
A = (sps.diags(Sd)@H@sps.diags(Sd)).tocsc(); A = 0.5*(A+A.T)
ev, V = spla.eigsh(A, k=6, sigma=0, which="LM")
for i in np.argsort(np.abs(ev)):
    fw = {lab.get(n, n): float(np.linalg.norm(V[slots[n], i])**2) for n in C.NAMES}
    top = max(fw, key=fw.get)
    print(f"  eig {ev[i]:+.3e}: {top} ({fw[top]:.2f}); step share {abs(V[:, i] @ (s/Sd))/np.linalg.norm(s/Sd):.2e}")
