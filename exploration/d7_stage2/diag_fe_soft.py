"""Is the Hessian right along the soft S modes that dominate the Newton step at the floor? Finite differences along the
softest S eigenvector, and the Taylor remainder along the Newton step as a function of lambda."""
import math, numpy as np, scipy.linalg as sla, scipy.sparse as sps
import solve_fe as FE
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T; g_e = 0.03*FE.A0T
g = FE.GridFE(16, 32, 1e-4, math.asinh(100.), math.asinh(100.))
P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), g_e)
x, _, gn = P.newton(FE.initial_guess_fe(g, P.dm, M, b), tol=1e-12, maxit=10, verbose=False)
grad, H, Y = P.grad_hess(x)
rown = np.asarray(abs(H).sum(axis=1)).ravel(); Sd = 1/np.sqrt(rown)
A = (sps.diags(Sd) @ H @ sps.diags(Sd)).toarray()
ev, V = sla.eigh(0.5*(A+A.T)); order = np.argsort(np.abs(ev))
off = P.dm.offsets; fS = FE.FIX["S"]
n0 = np.linalg.norm(Sd*P.src)
for k in order[:8]:
    v = V[:, k]
    if np.linalg.norm(v[off[fS]:off[fS+1]])**2 < 0.3: continue
    u = Sd*v                                   # physical direction
    scale = np.abs(x).max()/np.abs(u).max()
    for eps in (1e-6, 1e-4, 1e-2):
        e = eps*scale
        gp,_,_ = P.grad_hess(x+e*u, want_hess=False); gm,_,_ = P.grad_hess(x-e*u, want_hess=False)
        fd = Sd*(gp-gm)/(2*e); hv = Sd*(H@u)
        print(f"soft S mode eig {ev[k]:+.2e}, eps {eps:.0e}: |fd - Hv|/|Hv| = {np.linalg.norm(fd-hv)/np.linalg.norm(hv):.2e}, |Hv| = {np.linalg.norm(hv):.2e}")
    break
s = Sd*np.linalg.solve(A, -(Sd*grad))
print(f"|s|_inf/|x|_inf = {np.abs(s).max()/np.abs(x).max():.2e}")
for lam in (1e-3, 1e-2, 1e-1, 1.0):
    gt,_,_ = P.grad_hess(x+lam*s, want_hess=False)
    rem = Sd*(gt - grad - lam*(H@s))
    fi = int(np.searchsorted(off, int(np.argmax(np.abs(rem))), side="right")-1)
    print(f"lambda {lam:.0e}: residual {np.linalg.norm(Sd*gt)/n0:.3e}, Taylor remainder {np.linalg.norm(rem)/n0:.3e} (worst field {FE.NAMES[fi]})")
