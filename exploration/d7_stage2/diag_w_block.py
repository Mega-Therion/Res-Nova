"""Local Hessian of Lrest in the h_0i jets (W_R, W_R_R, W_R_z, W_z, W_z_R, W_z_z) at a point on the static Q1 solution,
v = 0 and 100 km/s: is the W derivative block full rank (Laplacian-like) or does it only see curl or divergence?"""
import math, numpy as np
import solve_fe as FE, local_derivs as LD
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T; g_e = 0.003*FE.A0T
g, P, xs, res = FE.static_solution(32, 64, M, b, g_e, 300.0)
q = (P.D @ xs).reshape(g.ng, FE.NQ) + P.qbg
r = np.hypot(g.Rg, g.zg)
k = int(np.argmin(np.abs(r - 0.3e-3) + 1e3*np.abs(g.zg - 0.1e-3)))
names = ["W_R", "W_R_R", "W_R_z", "W_z", "W_z_R", "W_z_z"]
idx = [3, 4, 5, 6, 7, 8]
for v in (0.0, 100/299792.458):
    qa = [np.array([q[k, j]]) for j in range(FE.NQ)]
    HL = dict(zip(LD.HESS_L_KEYS, [float(np.asarray(t).ravel()[0]) if np.ndim(t) else float(t) for t in LD.hess_L_vals(qa, np.array([g.Rg[k]]), v)]))
    Hb = np.array([[HL.get(tuple(sorted((idx[a], idx[c]))), 0.0) for c in range(6)] for a in range(6)])
    print(f"v = {v*299792.458:g} km/s, R = {g.Rg[k]:.2e}: rows/cols {names}")
    for a in range(6):
        print("   " + " ".join(f"{Hb[a, c]:+.3e}" for c in range(6)))
    sub = Hb[np.ix_([1, 2, 4, 5], [1, 2, 4, 5])]
    ev, V = np.linalg.eigh(sub)
    print("   derivative sub-block eigenvalues:", " ".join(f"{e:+.3e}" for e in ev))
    for e, vec in zip(ev, V.T):
        print(f"     {e:+.3e}: (W_R_R, W_R_z, W_z_R, W_z_z) = " + " ".join(f"{c:+.3f}" for c in vec))
