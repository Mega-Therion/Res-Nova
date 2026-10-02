"""Local Hessian of Lrest in the aether-derivative jets (U_R_R, U_R_z, U_z_R, U_z_z) at a point on the static solution.
F^2 alone gives only the curl combination (U_R_z - U_z_R)^2 at quadratic order about u = 0 (plus the axisymmetric
U_R/R pieces); any divergence-type (U_R_R + U_R/R + U_z_z)^2 term would stiffen the gradient (zero) mode."""
import math, numpy as np
import solve_fe as FE, local_derivs as LD
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/FE.A0T; g_e = 0.003*FE.A0T
g, P, xs, res = FE.static_solution(32, 64, M, b, g_e, 300.0)
q = (P.D @ xs).reshape(g.ng, FE.NQ) + P.qbg
r = np.hypot(g.Rg, g.zg)
k = int(np.argmin(np.abs(r - 0.3e-3) + 1e3*np.abs(g.zg - 0.1e-3)))
print(f"point R = {g.Rg[k]:.3e}, z = {g.zg[k]:.3e}")
for v in (0.0, 100/299792.458):
    qa = [np.array([q[k, j]]) for j in range(FE.NQ)]
    HL = dict(zip(LD.HESS_L_KEYS, [float(np.asarray(t).ravel()[0]) if np.ndim(t) else float(t) for t in LD.hess_L_vals(qa, np.array([g.Rg[k]]), v)]))
    idx = [21, 22, 23, 24, 25, 26]
    names = ["U_R", "U_R_R", "U_R_z", "U_z", "U_z_R", "U_z_z"]
    Hb = np.zeros((6, 6))
    for a in range(6):
        for c in range(6):
            i, j = sorted((idx[a], idx[c]))
            Hb[a, c] = HL.get((i, j), 0.0)
    print(f"v = {v*299792.458:g} km/s, block rows/cols {names}:")
    for a in range(6):
        print("   " + " ".join(f"{Hb[a, c]:+.3e}" for c in range(6)))
