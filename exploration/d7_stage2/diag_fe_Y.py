"""Does Y (the MOND invariant) carry roundoff noise from cancelling O(Q0^2) terms? Compare Y(x + lam s_metric) - Y(x)
with the linear prediction gY . D s, per Gauss point; and evaluate Y's formula in higher precision at a few points."""
import math, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spla
import solve_fe as FE, local_derivs as LD
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T; g_e = 0.03*FE.A0T
g = FE.GridFE(16, 32, 1e-4, math.asinh(100.), math.asinh(100.))
P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), g_e)
x, _, gn = P.newton(FE.initial_guess_fe(g, P.dm, M, b), tol=1e-12, maxit=10, verbose=False)
grad, H, Y = P.grad_hess(x)
Sd = 1/np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel())
s = Sd*spla.spsolve((sps.diags(Sd)@H@sps.diags(Sd)).tocsc(), -(Sd*grad))
off = P.dm.offsets
m = np.zeros_like(s)
for n in ["S","W_R","W_z","A","B","C","D"]:
    fi = FE.FIX[n]; m[off[fi]:off[fi+1]] = 1
sm = 1e-3*s*m
def Yof(xx):
    q = (P.D@xx).reshape(g.ng, FE.NQ) + P.qbg
    return np.broadcast_to(np.asarray(LD.val_Y([q[:,k] for k in range(FE.NQ)], g.Rg, 0.0)[0], dtype=float), (g.ng,)), q
Y0, q0 = Yof(x); Y1, _ = Yof(x+sm)
gY = np.array([np.broadcast_to(np.asarray(t, dtype=float), (g.ng,)) for t in LD.grad_Y([q0[:,k] for k in range(FE.NQ)], g.Rg, 0.0)])
dq = (P.D@sm).reshape(g.ng, FE.NQ)
lin = np.sum(gY.T*dq, axis=1)
err = (Y1-Y0) - lin
k = int(np.argmax(np.abs(err)/Y0))
print(f"max |dY - lin|/Y = {np.max(np.abs(err)/Y0):.3e} at R={g.Rg[k]:.2e} z={g.zg[k]:.2e}, Y there {Y0[k]:.3e}; |lin|/Y there {abs(lin[k])/Y0[k]:.3e}")
print(f"median |dY - lin|/Y = {np.median(np.abs(err)/Y0):.3e}")
# same Y formula in 50-digit arithmetic at the worst point
import mpmath as mp; mp.mp.dps = 50
src = open("local_derivs.py").read()
i0 = src.index("def val_Y("); body = src[i0:]
ns = {"sqrt": mp.sqrt, "np": type("npmp", (), {"sqrt": staticmethod(mp.sqrt)})}
exec(body.replace("np.sqrt", "sqrt"), ns)
qq = [mp.mpf(float(q0[k, j])) for j in range(FE.NQ)]
Yhi = ns["val_Y"](qq, mp.mpf(float(g.Rg[k])), mp.mpf(0))[0]
print(f"Y at that point: float64 {Y0[k]:.16e}, 50-digit {mp.nstr(Yhi, 17)}, rel diff {float(abs(Y0[k]-Yhi)/abs(Yhi)):.2e}")
