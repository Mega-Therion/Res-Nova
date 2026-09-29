#!/usr/bin/env python3
"""D7 Stage 2, step B (C1 elements): the discrete action on Bogner-Fox-Schmit bicubic Hermite elements.
Why: with nodal (Q1) elements the aether cannot represent a gradient field with zero discrete curl, and the curl^2 term
(coefficient ~5e8 x the lift at dwarf scales) then locks the tilt zero mode (diag_lift.py, DIAG_LIFT.txt). Here
  u = grad Lambda + curl(psi theta_hat):  U_R = Lambda_R - psi_z,  U_z = Lambda_z + psi_R + psi/R,
with Lambda and psi in C1 elements, so a gradient tilt has exactly zero curl at every quadrature point, and the scalar
is carried as the shifted field s = phi + Q0 gam Lambda, so the zero mode (d phi = chi, d u = -grad chi/Q0) is exactly the
pure Lambda direction. Every other field is in the same C1 space too: any combination whose large coefficients cancel
(the zero mode, and the Newtonian/MOND split Phihat = Psi - phi) must have all its members in one space, or the part one
member cannot follow is charged at the large coefficient.
Grid: the same stretched (xi, eta) rectangle as solve_fe.py (R = a sinh xi, z = a sinh eta); 4 DOFs per node and field
(f, f_xi, f_eta, f_xi_eta); 4x4 Gauss points per element. Unknown slots follow NAMES, with Lambda in the U_R slot, psi in
the U_z slot and s in the F slot. Boundary conditions: outer boundary, value Dirichlet (f and its tangential derivative
zero) for the metric and s, fully clamped (u = 0 there) for Lambda and psi; axis parity (S, W_z, A, D, Lambda, s even;
W_R, C, psi odd; B ~ R^2). The jets handed to local_derivs are the same 30 per point as before, so Lrest, Y (y_accurate)
and K are unchanged."""

import math, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import local_derivs as LD
from solve_steady import KB, A0T, NAMES, NF, NQ, FIX, mu_std, kfun
from solve_fe import y_accurate, plummer_fn

Q0 = 0.1
PARITY = {"S": "even", "W_R": "even", "W_z": "odd", "A": "even", "B": "r2", "C": "odd", "D": "even",
          "U_R": "even", "U_z": "odd", "F": "even"}
# W_R slot = Omega (even), W_z slot = omega (odd): h_0i = grad Omega + curl(omega theta_hat); U_R slot = Lambda (even),
# U_z slot = psi (odd): u = grad Lambda + curl(psi theta_hat); F slot = s = phi + Q0 gam Lambda
OUTER = {n: ("clamp" if n in ("U_R", "U_z", "W_R", "W_z") else "value") for n in NAMES}


def hermite(u):
    """1D cubic Hermite basis on [0, 1]: value functions P0, P1 and derivative functions D0, D1 with their first and
    second derivatives in u."""
    return {
        ("P", 0): (1 - 3 * u**2 + 2 * u**3, -6 * u + 6 * u**2, -6 + 12 * u),
        ("P", 1): (3 * u**2 - 2 * u**3, 6 * u - 6 * u**2, 6 - 12 * u),
        ("D", 0): (u - 2 * u**2 + u**3, 1 - 4 * u + 3 * u**2, -4 + 6 * u),
        ("D", 1): (-(u**2) + u**3, -2 * u + 3 * u**2, -2 + 6 * u),
    }


class GridC1:
    def __init__(self, nR, nz, a, xi_max, eta_max, ngp=4):
        self.nR, self.nz, self.a = nR, nz, a
        self.dxi, self.deta = xi_max / nR, 2 * eta_max / nz
        self.xi = np.arange(nR + 1) * self.dxi
        self.eta = -eta_max + np.arange(nz + 1) * self.deta
        self.Rn, self.zn = a * np.sinh(self.xi), a * np.sinh(self.eta)
        self.nnode = (nR + 1) * (nz + 1)
        x, w = np.polynomial.legendre.leggauss(ngp)
        gs, gw = (x + 1) / 2, w / 2
        I, J, P, Qi = np.meshgrid(
            np.arange(nR), np.arange(nz), np.arange(ngp), np.arange(ngp), indexing="ij"
        )
        self.ei, self.ej = I.ravel(), J.ravel()
        self.s, self.t = gs[P.ravel()], gs[Qi.ravel()]
        self.ng = self.ei.size
        xg = self.xi[self.ei] + self.s * self.dxi
        eg = self.eta[self.ej] + self.t * self.deta
        self.xg, self.eg = xg, eg
        self.Rg, self.zg = a * np.sinh(xg), a * np.sinh(eg)
        self.hRg, self.hzg = a * np.cosh(xg), a * np.cosh(eg)
        self.w = (
            2
            * math.pi
            * self.Rg
            * self.hRg
            * self.hzg
            * self.dxi
            * self.deta
            * gw[P.ravel()]
            * gw[Qi.ravel()]
        )

    def node(self, i, j):
        return i * (self.nz + 1) + j


class DofMapC1:
    """Global index of (field, node, d) with d = 0 f, 1 f_xi, 2 f_eta, 3 f_xi_eta; -1 where fixed to zero."""

    def __init__(self, g):
        self.g = g
        n = g.nnode
        ii = np.arange(n) // (g.nz + 1)
        jj = np.arange(n) % (g.nz + 1)
        redge, zedge, axis = ii == g.nR, (jj == 0) | (jj == g.nz), ii == 0
        self.index = np.full((NF, n, 4), -1, dtype=np.int64)
        count = 0
        for fi, name in enumerate(NAMES):
            fixed = np.zeros((n, 4), bool)
            if OUTER[name] == "clamp":
                fixed[redge | zedge, :] = True
            else:
                fixed[redge, 0] = fixed[redge, 2] = True
                fixed[zedge, 0] = fixed[zedge, 1] = True
            par = PARITY[name]
            if par == "even":
                fixed[axis, 1] = fixed[axis, 3] = True
            elif par == "odd":
                fixed[axis, 0] = fixed[axis, 2] = True
            else:  # B ~ R^2 on the axis: value and all first derivatives vanish there
                fixed[axis, :] = True
            free = ~fixed
            k = int(free.sum())
            self.index[fi][free] = count + np.arange(k)
            count += k
        self.ndof = count

    def to_nodes(self, x):
        out = np.zeros((NF, self.g.nnode, 4))
        m = self.index >= 0
        out[m] = x[self.index[m]]
        return out

    def from_nodes(self, arr):
        x = np.zeros(self.ndof)
        m = self.index >= 0
        x[self.index[m]] = arr[m]
        return x


def basis_at_gauss(g):
    """For each of the 16 local DOFs (corner a, b; kind d) the physical value and derivatives at every Gauss point:
    returns list of (a, b, d, dict(v, R, z, RR, Rz, zz))."""
    hs, ht = hermite(g.s), hermite(g.t)
    dxi, deta = g.dxi, g.deta
    thR, thz = np.tanh(g.xg), np.tanh(g.eg)
    out = []
    for a in (0, 1):
        for b in (0, 1):
            for d in range(4):
                kx = "D" if d in (1, 3) else "P"
                ky = "D" if d in (2, 3) else "P"
                X, X1, X2 = hs[(kx, a)]
                Y, Y1, Y2 = ht[(ky, b)]
                sx = dxi if kx == "D" else 1.0
                sy = deta if ky == "D" else 1.0
                X, X1, X2 = sx * X, sx * X1 / dxi, sx * X2 / dxi**2  # in xi
                Y, Y1, Y2 = sy * Y, sy * Y1 / deta, sy * Y2 / deta**2  # in eta
                v = X * Y
                fx, fe = X1 * Y, X * Y1
                fxx, fxe, fee = X2 * Y, X1 * Y1, X * Y2
                out.append(
                    (
                        a,
                        b,
                        d,
                        {
                            "v": v,
                            "R": fx / g.hRg,
                            "z": fe / g.hzg,
                            "RR": (fxx - thR * fx) / g.hRg**2,
                            "Rz": fxe / (g.hRg * g.hzg),
                            "zz": (fee - thz * fe) / g.hzg**2,
                        },
                    )
                )
    return out


def jet_operator_c1(g, dm, v_wind):
    """Sparse D: (ng * 30) x ndof, jets of the physical fields (with u and phi built from Lambda, psi, s)."""
    gam = 1 / math.sqrt(1 - v_wind**2)
    B = basis_at_gauss(g)
    k = np.arange(g.ng)
    rows, cols, vals = [], [], []

    def add(slot, comp, field, coef):
        """jet (slot, comp) += coef * basis contribution of `field` (coef: array over Gauss points, per local DOF)."""
        fi = FIX[field]
        for (a, b, d, bf), c in zip(B, coef):
            col = dm.index[fi][(g.ei + a) * (g.nz + 1) + (g.ej + b), d]
            m = col >= 0
            rows.append((k[m] * NQ + 3 * FIX[slot] + comp))
            cols.append(col[m])
            vals.append(c[m])

    iR = 1.0 / g.Rg
    for name in ("S", "A", "B", "C", "D"):
        add(name, 0, name, [bf["v"] for (_, _, _, bf) in B])
        add(name, 1, name, [bf["R"] for (_, _, _, bf) in B])
        add(name, 2, name, [bf["z"] for (_, _, _, bf) in B])

    def vector_from_potentials(slotR, slotZ, grad_pot, curl_pot):
        """vector (slotR, slotZ) = grad(grad_pot) + curl(curl_pot theta_hat), with values and first derivatives."""
        add(slotR, 0, grad_pot, [bf["R"] for (_, _, _, bf) in B]); add(slotR, 0, curl_pot, [-bf["z"] for (_, _, _, bf) in B])
        add(slotR, 1, grad_pot, [bf["RR"] for (_, _, _, bf) in B]); add(slotR, 1, curl_pot, [-bf["Rz"] for (_, _, _, bf) in B])
        add(slotR, 2, grad_pot, [bf["Rz"] for (_, _, _, bf) in B]); add(slotR, 2, curl_pot, [-bf["zz"] for (_, _, _, bf) in B])
        add(slotZ, 0, grad_pot, [bf["z"] for (_, _, _, bf) in B])
        add(slotZ, 0, curl_pot, [bf["R"] + bf["v"] * iR for (_, _, _, bf) in B])
        add(slotZ, 1, grad_pot, [bf["Rz"] for (_, _, _, bf) in B])
        add(slotZ, 1, curl_pot, [bf["RR"] + bf["R"] * iR - bf["v"] * iR**2 for (_, _, _, bf) in B])
        add(slotZ, 2, grad_pot, [bf["zz"] for (_, _, _, bf) in B])
        add(slotZ, 2, curl_pot, [bf["Rz"] + bf["z"] * iR for (_, _, _, bf) in B])

    vector_from_potentials("W_R", "W_z", "W_R", "W_z")  # Omega in the W_R slot, omega in the W_z slot
    L = "U_R"
    vector_from_potentials("U_R", "U_z", "U_R", "U_z")  # Lambda in the U_R slot, psi in the U_z slot
    for comp, key in ((0, "v"), (1, "R"), (2, "z")):
        add("F", comp, "F", [bf[key] for (_, _, _, bf) in B])
        add("F", comp, L, [-Q0 * gam * bf[key] for (_, _, _, bf) in B])
    return sps.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(g.ng * NQ, dm.ndof),
    )


class ProblemC1:
    def __init__(self, g, v, rho_fn, g_e=0.0, extended=True):
        self.g, self.v = g, v
        self.dt = np.longdouble if extended else np.float64
        self.dm = DofMapC1(g)
        self.D = jet_operator_c1(g, self.dm, v)
        self.qbg = np.zeros((g.ng, NQ))
        Jpe = float(mu_std(np.array(g_e / A0T))) if g_e > 0 else 0.0
        psi_z = (1 + Jpe) * g_e
        self.qbg[:, 3 * FIX["F"] + 2] = g_e
        self.qbg[:, 3 * FIX["S"] + 2] = -2 * psi_z
        self.qbg[:, 3 * FIX["A"] + 2] = -2 * psi_z
        rho_g = rho_fn(g.Rg, g.zg)
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
        self.solve_log = []

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

    def solve_linear(self, A, rhs, refine=3):
        lu = spla.splu(A.tocsc())
        y = lu.solve(rhs)
        for _ in range(refine):
            r = rhs - A @ y
            rel = np.linalg.norm(r) / np.linalg.norm(rhs)
            if rel < 1e-12:
                break
            y = y + lu.solve(r)
        rel = np.linalg.norm(rhs - A @ y) / np.linalg.norm(rhs)
        self.solve_log.append(float(rel))
        return y

    def lambda_dofs(self):
        """Global indices of the Lambda (aether gradient potential) DOFs: the zero-mode direction."""
        m = self.dm.index[FIX["U_R"]]
        return np.unique(m[m >= 0])

    def newton(self, x0, tol=1e-9, maxit=40, verbose=True, freeze=None):
        """Newton with row-norm equilibration and a backtracking line search. freeze: global DOF indices held fixed
        (dropped from the step; the residual is measured on the free rows only)."""
        x = x0.copy()
        free = np.ones(self.dm.ndof, bool)
        if freeze is not None:
            free[freeze] = False
        fidx = np.flatnonzero(free)
        grad, H, Y = self.grad_hess(x)
        rown = np.asarray(abs(H).sum(axis=1)).ravel()
        Sd = sps.diags(1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30)))
        norm0 = np.linalg.norm(Sd @ self.src)
        res = lambda gr: np.linalg.norm((Sd @ gr)[fidx]) / norm0
        for it in range(maxit):
            gn = res(grad)
            if verbose:
                print(
                    f"    newton {it}: equilibrated |grad|/|src| = {gn:.3e}"
                    + (
                        f"  (last linear solve rel. residual {self.solve_log[-1]:.1e})"
                        if self.solve_log
                        else ""
                    ),
                    flush=True,
                )
            if gn < tol:
                return x, True, gn
            A = (Sd @ H @ Sd).tocsr()[fidx][:, fidx]
            step = np.zeros(self.dm.ndof)
            step[fidx] = self.solve_linear(A, -(Sd @ grad)[fidx])
            step = Sd @ step
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


def initial_guess_c1(g, dm, M, b):
    """Spherical SZ solution (flux laws with J' = mu_std) as nodal Hermite data for S, A and s; u = 0."""
    RR, ZZ = np.meshgrid(g.Rn, g.zn, indexing="ij")
    R, Z = RR.ravel(), ZZ.ravel()
    r = np.hypot(R, Z)
    rs = np.geomspace(1e-8, 10 * r.max(), 6000)
    flux = M * rs**3 / (rs**2 + b**2) ** 1.5 / (12 * math.pi * rs**2)
    yv = flux / A0T
    gphi = A0T * np.sqrt(0.5 * (yv**2 + np.sqrt(yv**4 + 4 * yv**2)))
    cum = lambda gr: -np.flip(
        np.concatenate(
            [[0], np.cumsum(np.flip(0.5 * (gr[1:] + gr[:-1]) * np.diff(rs)))]
        )
    )
    out = np.zeros((NF, g.nnode, 4))
    hR = g.a * np.cosh(np.arcsinh(R / g.a))
    hz = g.a * np.cosh(np.arcsinh(Z / g.a))
    for name, pot, dpot in (
        ("S", lambda: -2 * (cum(flux) + cum(gphi)), lambda: -2 * (flux + gphi)),
        ("A", lambda: -2 * (cum(flux) + cum(gphi)), lambda: -2 * (flux + gphi)),
        ("F", lambda: cum(gphi), lambda: gphi),
    ):
        Pv, dP = pot(), dpot()
        d2P = np.gradient(dP, rs)
        f = np.interp(r, rs, Pv)
        f1 = np.interp(r, rs, dP)
        f2 = np.interp(r, rs, d2P)
        with np.errstate(invalid="ignore", divide="ignore"):
            nR_, nZ_ = np.where(r > 0, R / r, 0.0), np.where(r > 0, Z / r, 0.0)
            cross = np.where(r > 0, (f2 - f1 / np.where(r > 0, r, 1)) * nR_ * nZ_, 0.0)
        fi = FIX[name]
        out[fi, :, 0] = f
        out[fi, :, 1] = hR * f1 * nR_
        out[fi, :, 2] = hz * f1 * nZ_
        out[fi, :, 3] = hR * hz * cross
    return dm.from_nodes(out)


def static_cache_path(nR, nz, g_e, box):
    return f"cache_static_c1_{nR}x{nz}_ge{g_e / A0T:.4g}_box{box:g}.npz"


def static_solution(nR, nz, M, b, g_e, box, a=1e-4, tol=1e-10, maxit=25, verbose=False):
    """Static held solution on the C1 grid, cached in a file keyed by every parameter (checked on load)."""
    g = GridC1(nR, nz, a, math.asinh(box), math.asinh(box))
    P = ProblemC1(g, 0.0, plummer_fn(M, b), g_e)
    meta = np.array([nR, nz, M, b, g_e, box, a], dtype=float)
    path = static_cache_path(nR, nz, g_e, box)
    try:
        d = np.load(path)
        if d["x"].size == P.dm.ndof and np.array_equal(d["meta"], meta):
            return g, P, d["x"], float(d["residual"])
        print(
            f"cache {path} does not match the requested parameters; recomputing",
            flush=True,
        )
    except (OSError, KeyError):
        pass
    # two stages: the held static solution has Lambda = 0 (the aether's static source is divergence-free), and the
    # zero mode is soft and strongly non-linear, so converge everything else first with Lambda frozen at zero
    x, ok1, gn1 = P.newton(initial_guess_c1(g, P.dm, M, b), tol=tol, maxit=maxit, verbose=verbose, freeze=P.lambda_dofs())
    x, ok, gn = P.newton(x, tol=tol, maxit=maxit, verbose=verbose)
    if not ok:
        raise RuntimeError(
            f"static solve did not converge (residual {gn:.2e}) for {path}"
        )
    np.savez(path, x=x, residual=gn, meta=meta)
    return g, P, x, gn
