#!/usr/bin/env python3
"""One galaxy disk versus the algebraic MOND relation.

Units G = 1, a0 = 1. Field equation:
    laplacian(psi) = div(nu * grad Phi_N).
Algebraic curve: g = nu * g_N. A Plummer sphere is the control. An
exponential disk is the question. Isolated, so S = 1 and nu_eff = nu.
nu is the simple interpolating function.
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def nu_simple(y: np.ndarray) -> np.ndarray:
    y = np.maximum(np.asarray(y, dtype=float), 1e-8)
    return np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y**2)))


def build_laplacian(
    nR: int, nZ: int, dR: float, dZ: float, R: np.ndarray
) -> sparse.csr_matrix:
    def idx(i: int, j: int) -> int:
        return i * nZ + j

    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []

    def add(p: int, q: int, v: float) -> None:
        rows.append(p)
        cols.append(q)
        vals.append(v)

    for i in range(nR):
        for j in range(nZ):
            p = idx(i, j)
            if i == nR - 1 or j == 0 or j == nZ - 1:
                add(p, p, 1.0)
                continue
            add(p, p, -2.0 / dZ**2)
            add(p, idx(i, j + 1), 1.0 / dZ**2)
            add(p, idx(i, j - 1), 1.0 / dZ**2)
            if i == 0:
                # 2 * d^2/dR^2 at the axis, d^2/dR^2 = 2 (ψ1-ψ0)/dR^2
                add(p, p, -4.0 / dR**2)
                add(p, idx(1, j), 4.0 / dR**2)
            else:
                add(p, p, -2.0 / dR**2)
                add(p, idx(i + 1, j), 1.0 / dR**2 + 1.0 / (2.0 * R[i] * dR))
                add(p, idx(i - 1, j), 1.0 / dR**2 - 1.0 / (2.0 * R[i] * dR))
    return sparse.csr_matrix((vals, (rows, cols)), shape=(nR * nZ, nR * nZ))


def grad_R(field: np.ndarray, dR: float) -> np.ndarray:
    g = np.empty_like(field)
    g[1:-1, :] = (field[2:, :] - field[:-2, :]) / (2 * dR)
    g[0, :] = 0.0
    g[-1, :] = (field[-1, :] - field[-2, :]) / dR
    return g


def grad_Z(field: np.ndarray, dZ: float) -> np.ndarray:
    g = np.empty_like(field)
    g[:, 1:-1] = (field[:, 2:] - field[:, :-2]) / (2 * dZ)
    g[:, 0] = (field[:, 1] - field[:, 0]) / dZ
    g[:, -1] = (field[:, -1] - field[:, -2]) / dZ
    return g


def divergence(
    UR: np.ndarray, UZ: np.ndarray, R: np.ndarray, dR: float, dZ: float
) -> np.ndarray:
    dUR = np.empty_like(UR)
    dUR[1:-1, :] = (UR[2:, :] - UR[:-2, :]) / (2 * dR)
    dUR[0, :] = UR[1, :] / dR
    dUR[-1, :] = (UR[-1, :] - UR[-2, :]) / dR
    div = dUR + grad_Z(UZ, dZ)
    div[1:, :] += UR[1:, :] / R[1:, None]
    div[0, :] += dUR[0, :]  # second copy: dUR/dR + UR/R -> 2 dUR/dR
    return div


def monopole_psi(radius: np.ndarray, mass: float) -> np.ndarray:
    """ψ(r) = ∫_r^∞ ν(GM/s^2) GM/s^2 ds, so dψ/dr = ν g_N for a point mass."""
    s = np.linspace(float(np.min(radius)), float(np.max(radius)) * 40.0, 4000)
    g = mass / s**2
    integrand = nu_simple(g) * g
    # cumulative integral from the outside
    ds = np.gradient(s)
    tail = np.cumsum((integrand * ds)[::-1])[::-1]
    # interpolate onto the requested radii. s[0] is the inner edge of this table,
    # so build a table from min radius outward and also cover smaller r by extending.
    s_tab = np.linspace(1e-3, float(np.max(radius)) * 40.0, 8000)
    g_tab = mass / np.maximum(s_tab, 1e-3) ** 2
    integ = nu_simple(g_tab) * g_tab
    tail_tab = np.cumsum((integ * np.gradient(s_tab))[::-1])[::-1]
    return np.interp(radius, s_tab, tail_tab)


def solve_poisson(
    L: sparse.csr_matrix, rhs: np.ndarray, boundary: np.ndarray
) -> np.ndarray:
    nR, nZ = rhs.shape
    b = rhs.copy()
    b[-1, :] = boundary[-1, :]
    b[:, 0] = boundary[:, 0]
    b[:, -1] = boundary[:, -1]
    sol = spsolve(L, b.reshape(-1))
    return sol.reshape(nR, nZ)


def report(name: str, alg: np.ndarray, pde: np.ndarray, R: np.ndarray) -> None:
    m = (R > 0.5) & (R < 5.0)
    rel = np.abs(pde[m] - alg[m]) / np.maximum(np.abs(alg[m]), 1e-8)
    print(
        f"{name}: median |g_pde - g_alg| / |g_alg| = {np.median(rel):.4f} "
        f"max={np.max(rel):.4f} on {int(m.sum())} midplane radii in (0.5, 5)"
    )
    for target in (0.5, 1.0, 2.0, 3.0, 4.0, 5.0):
        k = int(np.argmin(np.abs(R - target)))
        if abs(alg[k]) < 1e-10:
            continue
        print(
            f"  R={R[k]:.2f} alg={alg[k]:.4f} pde={pde[k]:.4f} rel={abs(pde[k]-alg[k])/abs(alg[k]):.4f}"
        )


def main() -> None:
    nR, nZ = 121, 161
    R = np.linspace(0.0, 20.0, nR)
    Z = np.linspace(-8.0, 8.0, nZ)
    dR, dZ = float(R[1] - R[0]), float(Z[1] - Z[0])
    RR, ZZ = np.meshgrid(R, Z, indexing="ij")
    L = build_laplacian(nR, nZ, dR, dZ, R)
    j0 = int(np.argmin(np.abs(Z)))

    # --- Plummer control ---
    b, M = 1.0, 1.0
    radius = np.sqrt(RR**2 + ZZ**2)
    Phi = -M / np.sqrt(radius**2 + b**2)
    gR, gZ = grad_R(Phi, dR), grad_Z(Phi, dZ)
    # analytic radial derivative, so the control is not limited by grad(Phi)
    g_exact = M * radius / (radius**2 + b**2) ** 1.5
    gR = np.where(radius > 0, g_exact * RR / np.maximum(radius, 1e-12), 0.0)
    gZ = np.where(radius > 0, g_exact * ZZ / np.maximum(radius, 1e-12), 0.0)
    gmag = np.sqrt(gR**2 + gZ**2)
    nu = nu_simple(gmag)
    div = divergence(nu * gR, nu * gZ, R, dR, dZ)
    boundary = monopole_psi(np.maximum(radius, 1e-3), M)
    # Plummer is not a point mass. Use the spherical integral of its own g.
    # Rebuild boundary from g_exact along each radius by interpolating a 1D integral.
    r1 = np.linspace(0.0, 80.0, 8001)
    g1 = M * r1 / (r1**2 + b**2) ** 1.5
    integ = nu_simple(np.maximum(g1, 1e-12)) * g1
    tail = np.cumsum((integ * np.gradient(r1))[::-1])[::-1]
    boundary = np.interp(radius, r1, tail)
    psi = solve_poisson(L, div, boundary)
    report("plummer", (nu * g_exact)[:, j0], grad_R(psi, dR)[:, j0], R)

    # --- exponential disk ---
    Rd, zd, Sigma0 = 2.0, 0.3, 0.5
    rho0 = Sigma0 / (zd * np.sqrt(2.0 * np.pi))
    rho = rho0 * np.exp(-RR / Rd) * np.exp(-0.5 * (ZZ / zd) ** 2)
    mass = float(Sigma0 * 2.0 * np.pi * Rd**2)
    Phi_d = solve_poisson(L, 4.0 * np.pi * rho, -mass / np.maximum(radius, 1e-3))
    gR, gZ = grad_R(Phi_d, dR), grad_Z(Phi_d, dZ)
    gmag = np.sqrt(gR**2 + gZ**2)
    nu = nu_simple(gmag)
    div = divergence(nu * gR, nu * gZ, R, dR, dZ)
    boundary = monopole_psi(np.maximum(radius, 1e-3), mass)
    psi = solve_poisson(L, div, boundary)
    report("disk", (nu * gR)[:, j0], grad_R(psi, dR)[:, j0], R)
    print(f"disk mass={mass:.4f} Rd={Rd} zd={zd} Sigma0={Sigma0}")


if __name__ == "__main__":
    main()
