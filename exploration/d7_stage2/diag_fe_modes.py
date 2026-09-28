"""FE solver at the residual floor (16x32, g_e = 0.03 a0): the softest modes of the equilibrated Hessian, the linear-solve
accuracy, and where the Newton step is large."""

import math
import numpy as np
import scipy.linalg as sla
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_fe as FE

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / FE.A0T
g_e = 0.03 * FE.A0T
g = FE.GridFE(16, 32, 1e-4, math.asinh(100.0), math.asinh(100.0))
P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), g_e)
x, _, gn = P.newton(
    FE.initial_guess_fe(g, P.dm, M, b), tol=1e-12, maxit=10, verbose=False
)
grad, H, Y = P.grad_hess(x)
rown = np.asarray(abs(H).sum(axis=1)).ravel()
Sd = 1 / np.sqrt(rown)
A = (sps.diags(Sd) @ H @ sps.diags(Sd)).toarray()
print(
    f"residual {gn:.3e}; asymmetry |A-A^T|/|A| = {np.linalg.norm(A - A.T) / np.linalg.norm(A):.2e}",
    flush=True,
)
ev, V = sla.eigh(0.5 * (A + A.T))
order = np.argsort(np.abs(ev))
print(
    f"|eig| range: {np.abs(ev).min():.3e} .. {np.abs(ev).max():.3e}; #neg {int((ev < 0).sum())} of {ev.size}"
)
off = P.dm.offsets
rhs = -(Sd * grad)
s = np.linalg.solve(A, rhs)
print(
    f"dense solve relative residual {np.linalg.norm(A @ s - rhs) / np.linalg.norm(rhs):.2e}"
)
coef = V.T @ rhs
for k in order[:8]:
    v = V[:, k]
    fw = [np.linalg.norm(v[off[f] : off[f + 1]]) ** 2 for f in range(FE.NF)]
    fi = int(np.argmax(fw))
    seg = v[off[fi] : off[fi + 1]]
    node = np.flatnonzero(P.dm.free[fi])[int(np.argmax(np.abs(seg)))]
    i, j = divmod(node, g.nz + 1)
    print(
        f"  eig {ev[k]:+.3e}: field {FE.NAMES[fi]} ({fw[fi]:.2f}), peak R={g.Rn[i]:.2e} z={g.zn[j]:.2e}; "
        f"rhs overlap {abs(coef[k]) / np.linalg.norm(rhs):.2e}, step share {abs(coef[k] / ev[k]) / np.linalg.norm(s):.2e}"
    )
big = np.argsort(np.abs(s))[::-1][:5]
for d in big:
    fi = int(np.searchsorted(off, d, side="right") - 1)
    node = np.flatnonzero(P.dm.free[fi])[d - off[fi]]
    i, j = divmod(node, g.nz + 1)
    print(
        f"  largest step entries: field {FE.NAMES[fi]} R={g.Rn[i]:.2e} z={g.zn[j]:.2e} |s|={abs(s[d]):.3e} (x there {abs(x[d]):.3e})"
    )
