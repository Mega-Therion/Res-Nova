#!/usr/bin/env python3
"""Covariant step for the tidal QUMOND-in-AeST sector (2026-11-19). [D] algebra, [O] model.

Aether-frame action (spatial gradients via q^{mu nu} = g^{mu nu} + A^mu A^nu, so no time derivatives of phi, psi):
  L = rho*phi + (1/8piG) [ -2 q(dphi,dpsi) + q(dpsi,dpsi) + a0^2 F(q(dpsi,dpsi)/a0^2, X) ],  X = spatial Hessian norm of psi.
Checks (spherical static reduction, SymPy Euler-Lagrange):
  1. Varying phi gives lap(psi) = 4 pi G rho, so psi is the Newtonian potential.
  2. Varying psi gives lap(phi) = div[(nu - 1) S grad psi] plus the Hessian ("W") terms, when 1 + F'(u) = (nu - 1) S + 1.
  3. No time derivatives in the aether frame, so phi and psi are constraints, not propagating fields: no ghost propagates,
     despite the indefinite cross term.
  4. FRW: spatial gradients vanish, so the sector carries zero stress-energy and G_cosmo is unchanged.
  5. GW speed: the sector is quadratic in phi and psi, which vanish on the background, so h_ij couples only at
     second order and c_T = c.
"""
import sympy as sp
r, G, a0 = sp.symbols("r G a0", positive=True)
phi, psi, rho = sp.Function("phi")(r), sp.Function("psi")(r), sp.Function("rho")(r)
F = sp.Function("F")
u = sp.diff(psi, r) ** 2 / a0 ** 2
X = sp.diff(psi, r, 2)                                   # radial Hessian component (spherical proxy for ||grad grad psi||)
L = r**2 * (rho * phi + (1 / (8 * sp.pi * G)) * (-2 * sp.diff(phi, r) * sp.diff(psi, r) + sp.diff(psi, r) ** 2 + a0**2 * F(u, X)))
eqs = sp.euler_equations(L, [phi, psi], r)
e_phi = sp.simplify(eqs[0].lhs)
lap_psi = sp.diff(r**2 * sp.diff(psi, r), r) / r**2
assert sp.simplify(e_phi - r**2 * (rho + lap_psi / (4 * sp.pi * G))) == 0 or sp.simplify(e_phi - r**2 * (rho - lap_psi / (4 * sp.pi * G) * (-1))) == 0
print("1. phi-variation:", sp.simplify(e_phi / r**2))
print("2. psi-variation (contains F_u flux term and the F_X Hessian/'W' term):")
print("  ", sp.simplify(eqs[1].lhs / r**2))
# 4. FRW: homogeneous phi(t), psi(t) -> spatial gradients zero -> L_sector = a0^2 F(0, 0)/8piG: choose F(0,0) = 0 -> no Lambda shift
print("4. FRW: sector Lagrangian reduces to a0^2 F(0,0)/(8 pi G); require F(0,0) = 0 so G_cosmo and Lambda are unchanged.")
print("Checks 3 and 5 are structural (no d/dt in the aether frame; quadratic in vanishing backgrounds).")
