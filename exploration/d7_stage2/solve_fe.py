#!/usr/bin/env python3
"""D7 Stage 2, step B (finite elements): the discrete action on bilinear elements with 2x2 Gauss quadrature.
Why: the cell-centred central-difference jets of solve_steady.py leave checkerboard (odd-even) modes almost free in the
linear operator; the non-linear terms then excite them and Newton stalls (diag_stall.py: the softest Hessian modes
flip sign between neighbours). Full (2x2) quadrature on bilinear elements has no such hourglass modes.
Grid: nodes at xi_i = i dxi (i = 0..nR, so the axis R = 0 is a node line) and eta_j = -eta_max + j deta (j = 0..nz),
with R = a sinh(xi) and z = a sinh(eta). Outer boundary nodes (i = nR, j = 0, j = nz) are Dirichlet zero. On the axis,
fields odd in R (W_R, C, U_R) are zero and even fields are free (natural symmetric condition).
Action: S = sum over Gauss points of w_g [Lrest(q_g) - K(Y(q_g))] + sum_g w_g rho_g S_g / 2, with q_g the jet
(value, d_R, d_z) from bilinear interpolation and w_g = 2 pi R_g (dR/dxi)(dz/deta) (dxi deta / 4).
Everything else (local physics, K, the external-field background, Newton with row-norm equilibration and line
search) is as in solve_steady.py."""

import math, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import local_derivs as LD
from solve_steady import KB, A0T, NAMES, ODD_IN_R, NF, NQ, FIX, mu_std, kfun

GP = (0.5 - 0.5 / math.sqrt(3), 0.5 + 0.5 / math.sqrt(3))


class GridFE:
    def __init__(self, nR, nz, a, xi_max, eta_max):
        self.nR, self.nz, self.a = nR, nz, a
        self.dxi, self.deta = xi_max / nR, 2 * eta_max / nz
        self.xi = np.arange(nR + 1) * self.dxi
        self.eta = -eta_max + np.arange(nz + 1) * self.deta
        self.Rn, self.zn = a * np.sinh(self.xi), a * np.sinh(self.eta)
        self.nnode = (nR + 1) * (nz + 1)
        # Gauss points: element (i, j) spans [xi_i, xi_{i+1}] x [eta_j, eta_{j+1}]
        rows = []
        for i in range(nR):
            for j in range(nz):
                for s in GP:
                    for t in GP:
                        rows.append((i, j, s, t))
        self.gp = rows
        self.ng = len(rows)
        xg = np.array([self.xi[i] + s * self.dxi for (i, j, s, t) in rows])
        eg = np.array([self.eta[j] + t * self.deta for (i, j, s, t) in rows])
        self.Rg, self.zg = a * np.sinh(xg), a * np.sinh(eg)
        self.hRg, self.hzg = a * np.cosh(xg), a * np.cosh(eg)
        self.w = 2 * math.pi * self.Rg * self.hRg * self.hzg * self.dxi * self.deta / 4

    def node(self, i, j):
        return i * (self.nz + 1) + j


class DofMap:
    """Free nodes per field -> global dof index."""

    def __init__(self, g):
        self.g = g
        free = []
        for name in NAMES:
            m = np.ones((g.nR + 1, g.nz + 1), bool)
            m[g.nR, :] = False
            m[:, 0] = False
            m[:, g.nz] = False
            if name in ODD_IN_R:
                m[0, :] = False
            free.append(m.ravel())
        self.free = free
        self.offsets = np.cumsum([0] + [int(m.sum()) for m in free])
        self.ndof = int(self.offsets[-1])
        self.index = []
        for fi in range(NF):
            idx = -np.ones(g.nnode, int)
            idx[self.free[fi]] = self.offsets[fi] + np.arange(int(self.free[fi].sum()))
            self.index.append(idx)

    def to_nodes(self, x):
        out = np.zeros((NF, self.g.nnode))
        for fi in range(NF):
            out[fi, self.free[fi]] = x[self.offsets[fi] : self.offsets[fi + 1]]
        return out

    def from_nodes(self, arr):
        return np.concatenate([arr[fi, self.free[fi]] for fi in range(NF)])


def jet_operator_fe(g, dm):
    rows, cols, vals = [], [], []
    for k, (i, j, s, t) in enumerate(g.gp):
        corners = [
            (i, j, (1 - s) * (1 - t), -(1 - t), -(1 - s)),
            (i + 1, j, s * (1 - t), (1 - t), -s),
            (i, j + 1, (1 - s) * t, -t, (1 - s)),
            (i + 1, j + 1, s * t, t, s),
        ]
        for fi in range(NF):
            base = k * NQ + 3 * fi
            for ii, jj, N, dNs, dNt in corners:
                col = dm.index[fi][g.node(ii, jj)]
                if col < 0:
                    continue
                rows += [base, base + 1, base + 2]
                cols += [col, col, col]
                vals += [N, dNs / (g.dxi * g.hRg[k]), dNt / (g.deta * g.hzg[k])]
    return sps.csr_matrix((vals, (rows, cols)), shape=(g.ng * NQ, dm.ndof))


def y_accurate(q, R, v):
    """Y from local_derivs.val_Y without its catastrophic cancellation. In val_Y the three O(Q0^2) = O(1e-2) pieces
    x3 + x8 + x15^2/100 (x3 = -gam^2/100, x8 = x7^2/100, x7 = 10 F_z + v gam, x15 = 10 F_R U_R + x10 x7 + gam x14)
    cancel down to Y ~ 1e-12. Exactly, since 1 + v^2 gam^2 - gam^2 = 0 and x14 - gam = (x13 - gam^2)/(x14 + gam):
        x3 + x8 + x15^2/100 = (2 e15 + e15^2 + 20 v gam F_z + 100 F_z^2)/100,   e15 = x15 - 1
        e15 = 10 F_R U_R + 10 U_z F_z + v gam U_z - 10 v gam F_z + gam (U_R^2 + U_z^2 - 2 v gam U_z)/(x14 + gam).
    The O(h Q0^2) pair S x3 + S x15 gam x13/(100 x14) cancels the same way: with d14 = x14 - gam, it equals
        S gam (x15 x14 - gam)/100 = S gam (gam e15 + d14 + e15 d14)/100.
    The remaining terms are copied from val_Y. Checked against a 50-digit evaluation of val_Y (gate_y_accurate.py).
    """
    S, W_R, W_z, A, B, C, D = q[0], q[3], q[6], q[9], q[12], q[15], q[18]
    U_R, U_z, F_R, F_z = q[21], q[24], q[28], q[29]
    one = np.ones_like(F_z)
    gam = one / np.sqrt(one - v * v)
    x0 = F_R**2
    x1 = A + B
    x5 = F_R / 5
    x6 = v * gam
    x7 = 10 * F_z + x6
    x8 = x7**2 / 100
    x9 = A + D
    x10 = U_z - x6
    x11 = U_R**2
    x12 = x10**2
    x14 = np.sqrt(x11 + x12 + 1)
    x15 = 10 * F_R * U_R + x10 * x7 + x14 * gam
    d14 = (x11 + U_z**2 - 2 * v * gam * U_z) / (x14 + gam)
    # v gam U_z + gam d14 and 2 e15 + 20 v gam F_z also cancel at first order; combined analytically:
    f15 = (
        10 * F_R * U_R
        + 10 * U_z * F_z
        + (v * gam * U_z * d14 + gam * (x11 + U_z**2)) / (x14 + gam)
    )
    e15 = f15 - 10 * v * gam * F_z
    T0 = (2 * f15 + e15**2 + 100 * F_z**2) / 100
    TS = S * gam * (gam * e15 + d14 + e15 * d14) / 100
    rest = (
        -C * x5 * x7
        + W_R * gam * x5
        + W_z * gam * x7 / 50
        - x0 * x1
        + x0
        - x8 * x9
        + x15
        * gam
        * (2 * C * U_R * x10 + x1 * x11 + x12 * x9 + 2 * x14 * (U_R * W_R + W_z * x10))
        / (100 * x14)
    )
    return T0 + TS + rest


class ProblemFE:
    """Y (the MOND invariant) comes from y_accurate: local_derivs.val_Y builds it from O(Q0^2) ~ 1e-2 terms that cancel
    down to Y ~ 1e-12, losing ~7 digits in float64 (2e-7 at the solution, up to 3e-2 at small-Y test points, against a
    50-digit evaluation), and that noise capped Newton at a residual of ~1e-5 (diag_fe_Y.py). extended=True also runs
    the rest of the local physics (Lrest, dY, K) in long double, which covers the milder O(v) cancellations in dY at
    finite wind speed; with y_accurate alone Newton already reaches 2e-12 at v = 0."""

    def __init__(self, g, v, rho_fn, g_e=0.0, extended=True):
        self.g, self.v = g, v
        self.dt = np.longdouble if extended else np.float64
        self.dm = DofMap(g)
        self.D = jet_operator_fe(g, self.dm)
        self.qbg = np.zeros((g.ng, NQ))
        Jpe = float(mu_std(np.array(g_e / A0T))) if g_e > 0 else 0.0
        psi_z = (1 + Jpe) * g_e
        self.qbg[:, 3 * FIX["F"] + 2] = g_e
        self.qbg[:, 3 * FIX["S"] + 2] = -2 * psi_z
        self.qbg[:, 3 * FIX["A"] + 2] = -2 * psi_z
        rho_g = rho_fn(g.Rg, g.zg)
        # matter: sum_g w rho S_g / 2, S_g = value row of the S jet
        Svalrows = np.arange(g.ng) * NQ + 3 * FIX["S"]
        self.src = self.D[Svalrows, :].T @ (0.5 * rho_g * g.w)
        keys = sorted(
            set(LD.HESS_L_KEYS)
            | set(LD.HESS_Y_KEYS)
            | {(j, i) for (i, j) in LD.HESS_L_KEYS + LD.HESS_Y_KEYS}
        )
        self.hkeys = keys
        c = np.arange(g.ng)
        self.Wrows = np.concatenate([c * NQ + i for (i, j) in keys])
        self.Wcols = np.concatenate([c * NQ + j for (i, j) in keys])

    def grad_hess(self, x, want_hess=True):
        g, dt = self.g, self.dt
        q = (self.D @ x).reshape(g.ng, NQ) + self.qbg
        qa = [q[:, k].astype(dt) for k in range(NQ)]
        Rg, v = g.Rg.astype(dt), dt(self.v)
        arr = lambda t: np.broadcast_to(np.asarray(t, dtype=dt), (g.ng,))
        gL = np.array([arr(t) for t in LD.grad_L(qa, Rg, v)])
        gY = np.array([arr(t) for t in LD.grad_Y(qa, Rg, v)])
        Y = arr(y_accurate(qa, Rg, v))
        K1, K2 = kfun(Y)
        gq = (gL - K1 * gY).astype(float)
        grad = self.D.T @ (gq * g.w).T.ravel() + self.src
        Y = Y.astype(float)
        if not want_hess:
            return grad, None, Y
        HL = dict(zip(LD.HESS_L_KEYS, (arr(t) for t in LD.hess_L_vals(qa, Rg, v))))
        HY = dict(zip(LD.HESS_Y_KEYS, (arr(t) for t in LD.hess_Y_vals(qa, Rg, v))))
        z0 = np.zeros(g.ng, dtype=dt)
        vals = []
        for i, j in self.hkeys:
            a, b = (i, j) if i <= j else (j, i)
            vals.append(
                (
                    HL.get((a, b), z0) - K1 * HY.get((a, b), z0) - K2 * gY[i] * gY[j]
                ).astype(float)
                * g.w
            )
        W = sps.csr_matrix(
            (np.concatenate(vals), (self.Wrows, self.Wcols)),
            shape=(g.ng * NQ, g.ng * NQ),
        )
        return grad, (self.D.T @ W @ self.D).tocsc(), Y

    def newton(self, x0, tol=1e-9, maxit=40, verbose=True):
        x = x0.copy()
        grad, H, Y = self.grad_hess(x)
        rown = np.asarray(abs(H).sum(axis=1)).ravel()
        Sd = sps.diags(1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30)))
        norm0 = np.linalg.norm(Sd @ self.src)
        res = lambda gr: np.linalg.norm(Sd @ gr) / norm0
        for it in range(maxit):
            gn = res(grad)
            if verbose:
                print(
                    f"    newton {it}: equilibrated |grad|/|src| = {gn:.3e}", flush=True
                )
            if gn < tol:
                return x, True, gn
            step = Sd @ spla.spsolve((Sd @ H @ Sd).tocsc(), -(Sd @ grad))
            lam = 1.0
            while True:
                gt, _, _ = self.grad_hess(x + lam * step, want_hess=False)
                if res(gt) < gn * (1 - 1e-4 * lam) or lam < 1e-4:
                    break
                lam *= 0.5
            if verbose and lam < 1:
                print(f"      line search: lambda = {lam:.3g}", flush=True)
            x = x + lam * step
            grad, H, Y = self.grad_hess(x)
        return x, False, res(grad)

    def nodes(self, x):
        return self.dm.to_nodes(x)


def plummer_fn(M, b):
    return (
        lambda R, z: 3 * M / (4 * math.pi * b**3) * (1 + (R**2 + z**2) / b**2) ** -2.5
    )


def initial_guess_fe(g, dm, M, b):
    """Spherical SZ solution at the nodes (flux law with J' = mu_std), u = 0, other metric parts 0."""
    RR, ZZ = np.meshgrid(g.Rn, g.zn, indexing="ij")
    r = np.sqrt(RR**2 + ZZ**2).ravel()
    rs = np.geomspace(1e-7, 10 * r.max(), 4000)
    Menc = M * rs**3 / (rs**2 + b**2) ** 1.5
    flux = Menc / (12 * math.pi * rs**2)
    yv = flux / A0T
    x = np.sqrt(0.5 * (yv**2 + np.sqrt(yv**4 + 4 * yv**2)))
    gphi = x * A0T
    cum = lambda gr: -np.flip(
        np.concatenate(
            [[0], np.cumsum(np.flip(0.5 * (gr[1:] + gr[:-1]) * np.diff(rs)))]
        )
    )
    F = np.interp(r, rs, cum(gphi))
    Ph = np.interp(r, rs, cum(flux))
    arr = np.zeros((NF, g.nnode))
    arr[FIX["F"]] = F
    arr[FIX["S"]] = -2 * (Ph + F)
    arr[FIX["A"]] = -2 * (Ph + F)
    return dm.from_nodes(arr)


def static_cache_path(nR, nz, g_e, box):
    return f"cache_static_fe_{nR}x{nz}_ge{g_e / A0T:.4g}_box{box:g}.npz"


def static_solution(nR, nz, M, b, g_e, box, a=1e-4, tol=1e-10, maxit=20):
    """The static (v = 0) held solution for a Plummer dwarf (M, b) in an external field g_e, on the FE grid with
    xi_max = eta_max = asinh(box). Cached in a file keyed by every parameter, and the parameters stored in the file are
    checked on load (a cache keyed by grid size alone would silently hand back a solution for another g_e or box)."""
    g = GridFE(nR, nz, a, math.asinh(box), math.asinh(box))
    P = ProblemFE(g, 0.0, plummer_fn(M, b), g_e)
    meta = np.array([nR, nz, M, b, g_e, box, a], dtype=float)
    path = static_cache_path(nR, nz, g_e, box)
    try:
        d = np.load(path)
        if d["x"].size == P.dm.ndof and np.array_equal(d["meta"], meta):
            return g, P, d["x"], float(d["residual"])
        print(f"cache {path} does not match the requested parameters; recomputing", flush=True)
    except (OSError, KeyError):
        pass
    x, ok, gn = P.newton(initial_guess_fe(g, P.dm, M, b), tol=tol, maxit=maxit, verbose=False)
    if not ok:
        raise RuntimeError(f"static solve did not converge (residual {gn:.2e}) for {path}")
    np.savez(path, x=x, residual=gn, meta=meta)
    return g, P, x, gn
