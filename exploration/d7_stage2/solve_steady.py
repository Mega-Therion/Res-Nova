#!/usr/bin/env python3
"""D7 Stage 2, step B: steady state of a dwarf in an aether wind, from the discrete action.
Lagrangian (per unit volume, axisymmetric): L = Lrest(q) - K(Y(q)) + L_m, where q is the local jet (value, d_R, d_z of
S = h00, W_R, W_z, A, B, C, D, U_R, U_z, F = phi), Lrest and Y come from reduce_axisym.py (derivatives compiled in
local_derivs.py), and K(Y) = (2 - K_B)(Y + J(Y)) with J' = mu_std(sqrt(Y)/a0t).
Matter couples to the metric g (AeST is written in the matter frame): L_m = -rho Psi = rho S / 2 (units 16 pi G~ = 1).
Static check (static_reduction.py): at v = 0 this is -(3/2)|grad(Psi - phi)|^2 - (3/2) J(|grad phi|^2) - rho Psi, i.e.
del^2 Phihat = rho/3 and div(J' grad phi) = rho/3, with Phihat = Psi - phi (AeST's SZ reduction; 4 pi Ghat = 16 pi G~/3
when 16 pi G~ = 1).
Grid: cell centres on a stretched (R, z) grid, R = a sinh(xi), z = a sinh(eta), with axis parity from each field's
tensor rank and zero Dirichlet data beyond the outer boundary. The action is S = sum_cells w_c L(q_c) with
w = 2 pi R (dR/dxi)(dz/deta) dxi deta, and q = D f + q_bg. q_bg carries the external field along z: phi_z = g_e and
Psi_z = (1 + J'(g_e)) g_e, which satisfies the aether alignment with u = 0.
Newton's method on grad_f S = 0 with the exact sparse Hessian D^T W D, diagonal scaling and a backtracking line search.
Units: Mpc, c = 1."""

import math, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import local_derivs as LD

KB = 0.5
A0T = 2 * 3.577e-5
NAMES = ["S", "W_R", "W_z", "A", "B", "C", "D", "U_R", "U_z", "F"]
ODD_IN_R = {"W_R", "C", "U_R"}
NF, NQ = len(NAMES), 3 * len(NAMES)
FIX = {n: i for i, n in enumerate(NAMES)}
SCALE = {
    n: (3e-5 if n in ("U_R", "U_z") else 1e-9) for n in NAMES
}  # typical sizes, for conditioning


def mu_std(x):
    return x / np.sqrt(1 + x * x)


EPS_Y = (1e-3 * A0T) ** 2     # floor inside J': deep MOND is a degenerate (p-Laplacian) operator at zero field; this
                              # only changes J' where |grad phi| < 1e-3 a0t (a sliver at the dwarf's exact centre)


def kfun(Y):
    """K'(Y), K''(Y) for K = (2-K_B)(Y + J(Y)), J'(Y) = mu_std(sqrt(Y + EPS_Y)/a0t)."""
    Y = np.maximum(Y, 0.0) + EPS_Y
    x = np.sqrt(Y) / A0T
    K1 = (2 - KB) * (1 + mu_std(x))
    K2 = (2 - KB) * (1 + x * x) ** -1.5 / (2 * A0T * np.sqrt(Y))
    return K1, K2


class Grid:
    def __init__(self, nR, nz, a, xi_max, eta_max):
        self.nR, self.nz, self.a = nR, nz, a
        self.dxi, self.deta = xi_max / nR, 2 * eta_max / nz
        xi = (np.arange(nR) + 0.5) * self.dxi
        eta = -eta_max + (np.arange(nz) + 0.5) * self.deta
        self.R, self.z = a * np.sinh(xi), a * np.sinh(eta)
        self.hR, self.hz = a * np.cosh(xi), a * np.cosh(eta)  # dR/dxi, dz/deta
        self.ncell = nR * nz
        RR, ZZ = np.meshgrid(self.R, self.z, indexing="ij")
        self.Rc, self.zc = RR.ravel(), ZZ.ravel()  # cell-major (i, j) -> i*nz + j
        HR, HZ = np.meshgrid(self.hR, self.hz, indexing="ij")
        self.w = 2 * math.pi * self.Rc * HR.ravel() * HZ.ravel() * self.dxi * self.deta
        self.hRc, self.hzc = HR.ravel(), HZ.ravel()

    def fidx(self, f, i, j):
        return (f * self.nR + i) * self.nz + j


def jet_operator(g):
    rows, cols, vals = [], [], []
    for f, name in enumerate(NAMES):
        par = -1.0 if name in ODD_IN_R else 1.0
        for i in range(g.nR):
            for j in range(g.nz):
                c = i * g.nz + j
                base = c * NQ + 3 * f
                rows.append(base)
                cols.append(g.fidx(f, i, j))
                vals.append(1.0)
                cR = 0.5 / (g.dxi * g.hR[i])
                for di, s_ in ((1, cR), (-1, -cR)):
                    ii = i + di
                    if ii < 0:
                        rows.append(base + 1)
                        cols.append(g.fidx(f, 0, j))
                        vals.append(s_ * par)
                    elif ii < g.nR:
                        rows.append(base + 1)
                        cols.append(g.fidx(f, ii, j))
                        vals.append(s_)
                cz = 0.5 / (g.deta * g.hz[j])
                for dj, s_ in ((1, cz), (-1, -cz)):
                    jj = j + dj
                    if 0 <= jj < g.nz:
                        rows.append(base + 2)
                        cols.append(g.fidx(f, i, jj))
                        vals.append(s_)
    return sps.csr_matrix((vals, (rows, cols)), shape=(g.ncell * NQ, NF * g.ncell))


class Problem:
    def __init__(self, g, v, rho, g_e=0.0):
        self.g, self.v = g, v
        self.D = jet_operator(g)
        self.qbg = np.zeros((g.ncell, NQ))
        Jpe = float(mu_std(np.array(g_e / A0T))) if g_e > 0 else 0.0
        psi_z = (1 + Jpe) * g_e
        self.qbg[:, 3 * FIX["F"] + 2] = g_e
        self.qbg[:, 3 * FIX["S"] + 2] = -2 * psi_z
        self.qbg[:, 3 * FIX["A"] + 2] = -2 * psi_z
        self.src = np.zeros(NF * g.ncell)
        self.src[FIX["S"] * g.ncell : (FIX["S"] + 1) * g.ncell] = 0.5 * rho * g.w
        self.scale = np.concatenate([np.full(g.ncell, SCALE[n]) for n in NAMES])
        # sparsity pattern of the per-cell Hessian (union of Lrest and Y patterns, symmetric)
        keys = sorted(
            set(LD.HESS_L_KEYS)
            | set(LD.HESS_Y_KEYS)
            | {(j, i) for (i, j) in LD.HESS_L_KEYS + LD.HESS_Y_KEYS}
        )
        self.hkeys = keys
        c = np.arange(g.ncell)
        self.Wrows = np.concatenate([c * NQ + i for (i, j) in keys])
        self.Wcols = np.concatenate([c * NQ + j for (i, j) in keys])

    def local(self, f):
        g = self.g
        q = (self.D @ f).reshape(g.ncell, NQ) + self.qbg
        qa = [q[:, k] for k in range(NQ)]
        gL = np.array(
            [np.broadcast_to(x, (g.ncell,)) for x in LD.grad_L(qa, g.Rc, self.v)]
        )  # (NQ, ncell)
        gY = np.array(
            [np.broadcast_to(x, (g.ncell,)) for x in LD.grad_Y(qa, g.Rc, self.v)]
        )
        Y = np.broadcast_to(
            np.asarray(LD.val_Y(qa, g.Rc, self.v)[0], dtype=float), (g.ncell,)
        )
        HLv = LD.hess_L_vals(qa, g.Rc, self.v)
        HYv = LD.hess_Y_vals(qa, g.Rc, self.v)
        HL = {
            k: np.broadcast_to(np.asarray(x, dtype=float), (g.ncell,))
            for k, x in zip(LD.HESS_L_KEYS, HLv)
        }
        HY = {
            k: np.broadcast_to(np.asarray(x, dtype=float), (g.ncell,))
            for k, x in zip(LD.HESS_Y_KEYS, HYv)
        }
        return q, gL, gY, Y, HL, HY

    def grad_hess(self, f, want_hess=True):
        g = self.g
        q, gL, gY, Y, HL, HY = self.local(f)
        K1, K2 = kfun(Y)
        gq = gL - K1 * gY  # dL/dq per cell, (NQ, ncell)
        grad = self.D.T @ (gq * g.w).T.ravel() + self.src
        if not want_hess:
            return grad, None, Y
        z0 = np.zeros(g.ncell)
        vals = []
        for i, j in self.hkeys:
            a, b = (i, j) if i <= j else (j, i)
            h = HL.get((a, b), z0) - K1 * HY.get((a, b), z0) - K2 * gY[i] * gY[j]
            vals.append(h * g.w)
        W = sps.csr_matrix(
            (np.concatenate(vals), (self.Wrows, self.Wcols)),
            shape=(g.ncell * NQ, g.ncell * NQ),
        )
        H = (self.D.T @ W @ self.D).tocsc()
        return grad, H, Y

    def newton(self, f0, tol=1e-9, maxit=40, verbose=True):
        """Newton on grad S = 0 with symmetric row-norm equilibration taken from the Hessian at the current iterate: the
        aether's gradient modes (held only by the lift) and its curl modes differ in stiffness by ~1e10, so fixed
        hand-picked scales leave the system unsolvable in double precision. The residual is the equilibrated gradient,
        and a backtracking line search acts on it."""
        f = f0.copy()
        grad, H, Y = self.grad_hess(f)
        rown = np.asarray(abs(H).sum(axis=1)).ravel()                 # row 1-norms: robust to zero diagonals (h00 at K_B = 1/2)
        dsc = 1.0 / np.sqrt(np.maximum(rown, 1e-300 + rown.max() * 1e-30))
        Sd = sps.diags(dsc)
        norm0 = np.linalg.norm(Sd @ self.src)
        res = lambda gr: np.linalg.norm(Sd @ gr) / norm0
        for it in range(maxit):
            gn = res(grad)
            if verbose:
                print(f"    newton {it}: equilibrated |grad|/|src| = {gn:.3e}", flush=True)
            if gn < tol:
                return f, True, gn
            step = Sd @ spla.spsolve((Sd @ H @ Sd).tocsc(), -(Sd @ grad))
            lam = 1.0
            while True:
                gt, _, _ = self.grad_hess(f + lam * step, want_hess=False)
                if res(gt) < gn * (1 - 1e-4 * lam) or lam < 1e-4:
                    break
                lam *= 0.5
            if verbose and lam < 1:
                print(f"      line search: lambda = {lam:.3g}", flush=True)
            f = f + lam * step
            grad, H, Y = self.grad_hess(f)
        return f, False, res(grad)


def plummer(g, M, b):
    r2 = g.Rc**2 + g.zc**2
    return 3 * M / (4 * math.pi * b**3) * (1 + r2 / b**2) ** -2.5


def initial_guess(g, M, b, g_e):
    """Spherical SZ solution for the internal fields (flux law, J' = mu_std), u = 0, other metric parts 0."""
    r = np.sqrt(g.Rc**2 + g.zc**2)
    rs = np.geomspace(1e-7, 10 * r.max(), 4000)
    Menc = M * rs**3 / (rs**2 + b**2) ** 1.5
    flux = Menc / (12 * math.pi * rs**2)  # del^2 Phihat = rho/3, same for J' grad phi
    # invert mu_std(x) x = flux / a0t for x = |grad phi| / a0t
    yv = flux / A0T
    x = np.sqrt(0.5 * (yv**2 + np.sqrt(yv**4 + 4 * yv**2)))
    gphi = x * A0T
    # potentials relative to the table's outer radius: phi(r) = -int_r^rmax |grad phi| dr
    phi = -np.flip(
        np.concatenate(
            [[0], np.cumsum(np.flip(0.5 * (gphi[1:] + gphi[:-1]) * np.diff(rs)))]
        )
    )
    phihat = -np.flip(
        np.concatenate(
            [[0], np.cumsum(np.flip(0.5 * (flux[1:] + flux[:-1]) * np.diff(rs)))]
        )
    )
    F = np.interp(r, rs, phi)
    Ph = np.interp(r, rs, phihat)
    f = np.zeros(NF * g.ncell)
    psi = Ph + F
    f[FIX["F"] * g.ncell : (FIX["F"] + 1) * g.ncell] = F
    f[FIX["S"] * g.ncell : (FIX["S"] + 1) * g.ncell] = -2 * psi
    f[FIX["A"] * g.ncell : (FIX["A"] + 1) * g.ncell] = -2 * psi
    return f


def interpolate(f_coarse, gc, gf):
    """Bilinear interpolation of a solution between stretched grids, done in (xi, eta), where both grids are uniform.
    Outside the coarse cell centres it extends by the field's axis parity and decays to the Dirichlet zero."""
    from scipy.interpolate import RegularGridInterpolator
    xi_c = np.arcsinh(gc.R / gc.a); eta_c = np.arcsinh(gc.z / gc.a)
    xi_f = np.arcsinh(gf.R / gf.a); eta_f = np.arcsinh(gf.z / gf.a)
    out = np.zeros(NF * gf.ncell)
    XF, EF = np.meshgrid(xi_f, eta_f, indexing="ij")
    pts = np.stack([XF.ravel(), EF.ravel()], -1)
    for fi, name in enumerate(NAMES):
        par = -1.0 if name in ODD_IN_R else 1.0
        vals = f_coarse[fi * gc.ncell:(fi + 1) * gc.ncell].reshape(gc.nR, gc.nz)
        # pad: mirror across the axis (parity) and zero one cell beyond the outer boundary
        xi_p = np.concatenate([[-xi_c[0]], xi_c, [xi_c[-1] + gc.dxi]])
        eta_p = np.concatenate([[eta_c[0] - gc.deta], eta_c, [eta_c[-1] + gc.deta]])
        vp = np.zeros((gc.nR + 2, gc.nz + 2))
        vp[1:-1, 1:-1] = vals; vp[0, 1:-1] = par * vals[0]
        interp = RegularGridInterpolator((xi_p, eta_p), vp, bounds_error=False, fill_value=0.0)
        out[fi * gf.ncell:(fi + 1) * gf.ncell] = interp(pts)
    return out
