"""Which components of the Newton step make the gradient jump at the floor? Split the step by field group."""
import math, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spla
import solve_fe as FE
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T; g_e = 0.03*FE.A0T
g = FE.GridFE(16, 32, 1e-4, math.asinh(100.), math.asinh(100.))
P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), g_e)
x, _, gn = P.newton(FE.initial_guess_fe(g, P.dm, M, b), tol=1e-12, maxit=10, verbose=False)
grad, H, Y = P.grad_hess(x)
Sd = 1/np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()); n0 = np.linalg.norm(Sd*P.src)
s = Sd*spla.spsolve((sps.diags(Sd)@H@sps.diags(Sd)).tocsc(), -(Sd*grad))
off = P.dm.offsets
groups = {"metric": ["S","W_R","W_z","A","B","C","D"], "aether": ["U_R","U_z"], "scalar": ["F"]}
for fi, n in enumerate(FE.NAMES):
    print(f"  {n:4s}: |x|_inf {np.abs(x[off[fi]:off[fi+1]]).max():.2e}  |s|_inf {np.abs(s[off[fi]:off[fi+1]]).max():.2e}")
for gname, names in groups.items():
    m = np.zeros_like(s)
    for n in names:
        fi = FE.FIX[n]; m[off[fi]:off[fi+1]] = 1
    sg = s*m
    for lam in (1e-3, 1e-1):
        gt,_,_ = P.grad_hess(x+lam*sg, want_hess=False)
        rem = Sd*(gt - grad - lam*(H@sg))
        print(f"step part {gname:6s} lambda {lam:.0e}: Taylor remainder {np.linalg.norm(rem)/n0:.3e}, |lambda H s_part| {np.linalg.norm(Sd*(lam*(H@sg)))/n0:.3e}")
