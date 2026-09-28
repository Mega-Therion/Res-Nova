"""Why does the FE Newton stall at ~1e-5? (1) Hessian vs finite-difference gradient; (2) residual by field;
(3) residual along the Newton step."""

import math
import numpy as np
import scipy.sparse.linalg as spla
import solve_fe as FE
import solve_steady as SS

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / FE.A0T
g = FE.GridFE(16, 32, 1e-4, math.asinh(100.0), math.asinh(100.0))
P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), 0.0)
x0 = FE.initial_guess_fe(g, P.dm, M, b)
x, ok, gn = P.newton(x0, tol=1e-8, maxit=9, verbose=False)
grad, H, Y = P.grad_hess(x)
print(
    f"after 9 its: residual {gn:.3e}; min Y/EPS_Y {Y.min() / SS.EPS_Y:.3g}, #Y<=0: {(Y <= 0).sum()}"
)
rng = np.random.default_rng(1)
off = P.dm.offsets
for trial in range(2):
    d = rng.standard_normal(P.dm.ndof)
    for fi in range(FE.NF):  # scale per field to the field's typical size
        s = np.abs(x[off[fi] : off[fi + 1]]).max() or 1e-12
        d[off[fi] : off[fi + 1]] *= s
    Hd = H @ d
    for eps in (1e-3, 1e-4, 1e-5, 1e-6):
        gp, _, _ = P.grad_hess(x + eps * d, want_hess=False)
        gm, _, _ = P.grad_hess(x - eps * d, want_hess=False)
        fd = (gp - gm) / (2 * eps)
        print(
            f"  trial {trial} eps {eps:.0e}: |Hd - fd|/|Hd| = {np.linalg.norm(Hd - fd) / np.linalg.norm(Hd):.3e}"
        )
rown = np.asarray(abs(H).sum(axis=1)).ravel()
Sd = 1 / np.sqrt(rown)
r = Sd * grad
n0 = np.linalg.norm(Sd * P.src)
print(f"residual (current-H equilibration) {np.linalg.norm(r) / n0:.3e}")
for fi, name in enumerate(FE.NAMES):
    seg = r[off[fi] : off[fi + 1]]
    if seg.size:
        k = int(np.argmax(np.abs(seg)))
        node = np.flatnonzero(P.dm.free[fi])[k]
        i, j = divmod(node, g.nz + 1)
        print(
            f"  field {name:4s}: |res| = {np.linalg.norm(seg) / n0:.3e}  worst node (i={i}, j={j}) R={g.Rn[i]:.2e} z={g.zn[j]:.2e}"
        )
# noise floor: evaluate the gradient at x and at x scaled by (1 + 1e-13)
g2, _, _ = P.grad_hess(x * (1 + 1e-13), want_hess=False)
print(
    f"gradient change under a 1e-13 relative rescale: {np.linalg.norm(Sd * (g2 - grad)) / n0:.3e}"
)
# along the Newton step
step = Sd * spla.spsolve(
    (
        P.dm
        and (lambda A: A)(
            __import__("scipy.sparse", fromlist=["diags"]).diags(Sd)
            @ H
            @ __import__("scipy.sparse", fromlist=["diags"]).diags(Sd)
        )
    ).tocsc(),
    -(Sd * grad),
)
for lam in (1.0, 0.5, 0.1, 1e-2, 1e-3):
    gt, _, _ = P.grad_hess(x + lam * step, want_hess=False)
    print(f"  lambda {lam:.0e}: residual {np.linalg.norm(Sd * gt) / n0:.3e}")
