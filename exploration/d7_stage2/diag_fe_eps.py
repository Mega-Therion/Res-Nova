"""Where does the FE Newton residual floor sit when g_e = 0.03 a0 (no Dirichlet corner zero), and does continuation in
the Y floor EPS_Y remove it? Also: how much do the gate quantities move between the floor and iteration 8?
"""

import math
import numpy as np
import solve_fe as FE
import solve_steady as SS

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / FE.A0T
g_e = 0.03 * FE.A0T
g = FE.GridFE(16, 32, 1e-4, math.asinh(100.0), math.asinh(100.0))
P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), g_e)
x0 = FE.initial_guess_fe(g, P.dm, M, b)
off = P.dm.offsets


def where(x, label):
    grad, H, Y = P.grad_hess(x)
    rown = np.asarray(abs(H).sum(axis=1)).ravel()
    r = grad / np.sqrt(rown)
    n0 = np.linalg.norm(P.src / np.sqrt(rown))
    fi = SS.FIX["F"]
    seg = r[off[fi] : off[fi + 1]]
    k = int(np.argmax(np.abs(seg)))
    node = np.flatnonzero(P.dm.free[fi])[k]
    i, j = divmod(node, g.nz + 1)
    kmin = int(np.argmin(Y))
    print(
        f"{label}: residual {np.linalg.norm(r) / n0:.3e} (F part {np.linalg.norm(seg) / n0:.3e}); worst F node R={g.Rn[i]:.2e} z={g.zn[j]:.2e}; "
        f"min Y/EPS_Y = {Y.min() / SS.EPS_Y:.3g} at R={g.Rg[kmin]:.2e} z={g.zg[kmin]:.2e}",
        flush=True,
    )


def observables(x):
    q = (P.D @ x).reshape(g.ng, FE.NQ)
    c = lambda n, k: q[:, 3 * FE.FIX[n] + k]
    r = np.hypot(g.Rg, g.zg)
    sel = np.abs(r - 3e-4) < 0.12 * 3e-4
    Psi_r = -0.5 * (g.Rg * c("S", 1) + g.zg * c("S", 2)) / r
    return np.sum(Psi_r[sel] * g.w[sel]) / np.sum(g.w[sel])


x8, _, gn8 = P.newton(x0, tol=1e-12, maxit=8, verbose=False)
where(x8, "iteration 8, EPS_Y=(1e-3 a0)^2")
x30, _, gn30 = P.newton(x8, tol=1e-12, maxit=22, verbose=False)
where(x30, "iteration 30")
print(
    f"shell-averaged d_r Psi at r_h: it 8 {observables(x8):.10e}, it 30 {observables(x30):.10e}, rel change {abs(observables(x30) / observables(x8) - 1):.2e}"
)
# continuation in EPS_Y, starting from the initial guess
x = x0
for eps in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3):
    SS.EPS_Y = (eps * FE.A0T) ** 2
    x, ok, gn = P.newton(x, tol=1e-9, maxit=15, verbose=False)
    print(f"EPS_Y = ({eps:g} a0)^2: converged {ok}, residual {gn:.3e}", flush=True)
where(x, "after EPS continuation")
