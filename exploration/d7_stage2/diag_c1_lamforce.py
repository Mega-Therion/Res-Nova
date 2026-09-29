"""C1 solver, 16x32, after stage 1 (Lambda frozen at 0): what forces the Lambda rows?
(1) S - A (isotropy of the static metric; the aether's source uses h00 = S, the Newtonian channel uses both);
(2) the Lambda-row residual split by jet: the U-slot part (aether equation) and the F-slot part (-Q0 gam x scalar eq.),
    each against the size of their largest single contributions (cancellation depth);
(3) the same at 24x48, to see how the forcing scales with h."""
import math, numpy as np, scipy.sparse as sps
import solve_c1 as C
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T
for n in ((16, 32), (24, 48)):
    g = C.GridC1(*n, 1e-4, math.asinh(300.), math.asinh(300.))
    P = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), g_e)
    lam = P.lambda_dofs()
    x, ok, gn = P.newton(C.initial_guess_c1(g, P.dm, M, b), tol=1e-11, maxit=15, verbose=False, freeze=lam)
    q = (P.D @ x).reshape(g.ng, C.NQ)
    S, A = q[:, 3*C.FIX["S"]], q[:, 3*C.FIX["A"]]
    r = np.hypot(g.Rg, g.zg); inner = r < 1.2e-3
    print(f"{n}: stage 1 residual {gn:.1e}; max|S - A|/max|S| (r < 1.2 kpc) {np.abs(S-A)[inner].max()/np.abs(S)[inner].max():.2e}; "
          f"B, D max/|S| {np.abs(q[:, 3*C.FIX['B']])[inner].max()/np.abs(S)[inner].max():.1e}, {np.abs(q[:, 3*C.FIX['D']])[inner].max()/np.abs(S)[inner].max():.1e}")
    grad, H, Y = P.grad_hess(x)
    # the gradient's pieces: gq per jet at the Gauss points, assembled through the Lambda columns only
    qt = q + P.qbg
    dt = np.longdouble
    import local_derivs as LD
    qa = [qt[:, k].astype(dt) for k in range(C.NQ)]
    Rg = g.Rg.astype(dt)
    gL = np.array([np.broadcast_to(np.asarray(t, dtype=dt), (g.ng,)) for t in LD.grad_L(qa, Rg, dt(0))])
    gY = np.array([np.broadcast_to(np.asarray(t, dtype=dt), (g.ng,)) for t in LD.grad_Y(qa, Rg, dt(0))])
    K1, K2 = C.kfun(np.broadcast_to(np.asarray(C.y_accurate(qa, Rg, dt(0)), dtype=dt), (g.ng,)))
    gq = (gL - K1*gY).astype(float) * g.w          # (NQ, ng)
    DL = P.D[:, lam]
    def part(slots):
        v = np.zeros((C.NQ, g.ng))
        for sl in slots:
            for c in range(3):
                v[3*C.FIX[sl]+c] = gq[3*C.FIX[sl]+c]
        return DL.T @ v.T.ravel()
    rU, rF = part(["U_R", "U_z"]), part(["F"])
    tot = rU + rF
    print(f"   Lambda rows: |aether part| {np.linalg.norm(rU):.3e}, |scalar part| {np.linalg.norm(rF):.3e}, |sum| {np.linalg.norm(tot):.3e} "
          f"(sum/part = {np.linalg.norm(tot)/np.linalg.norm(rU):.2e}); check vs grad {np.linalg.norm(grad[lam] - tot)/np.linalg.norm(tot):.1e}")
