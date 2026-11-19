#!/usr/bin/env python3
"""AeST + QUMOND-type tidal sector entering the single metric (2026-11-19). [D] for the static reduction.

Static weak-field Lagrangian (units 1/8piG; g00 = -(1+2Phi), gij = (1-2Psi) delta, aether acceleration J_i = d_i Phi):
  L = rho*Phi + (1/8piG)[ Psi'^2 - 2 Phi'Psi'        (Einstein-Hilbert)
                          + 2 Phi' phi'               (AeST-type J.grad(phi) mixing, unit weight)
                          - phi'^2 + 2 phi' psi'      (aux sector, spatial gradients only)
                          + a0^2 F(psi'^2/a0^2, psi'') ]   (QUMOND function with tidal (Hessian) argument)
Claim: with rho = -lap(Phi_N)/(4 pi G),
  Psi = Phi,   Phi = Phi_N + phi,   psi = -Phi_N,
and phi fixed by a Poisson equation sourced by Phi_N through F (the QUMOND phantom potential with tidal screen).
So matter, photons and GWs all see one potential: gamma = 1, and lensing equals dynamics.
"""
import sympy as sp
r, G, a0 = sp.symbols("r G a0", positive=True)
Phi, Psi, ph, ps = [sp.Function(n)(r) for n in ("Phi", "Psi", "ph", "ps")]
PhiN = sp.Function("PhiN")(r); F = sp.Function("F")
d = lambda f: sp.diff(f, r)
lap = lambda f: sp.diff(r**2 * d(f), r) / r**2
rho = sp.Function("rho")(r)
L = r**2 * (rho * Phi + (d(Psi)**2 - 2 * d(Phi) * d(Psi) + 2 * d(Phi) * d(ph) - d(ph)**2 + 2 * d(ph) * d(ps)
                         + a0**2 * F(d(ps)**2 / a0**2, sp.diff(ps, r, 2))) / (8 * sp.pi * G))
E = {str(f.func): sp.simplify(eq.lhs) for f, eq in zip((Phi, Psi, ph, ps), sp.euler_equations(L, [Phi, Psi, ph, ps], r))}
sub = {Psi: PhiN + ph, Phi: PhiN + ph, ps: -PhiN, rho: -lap(PhiN) / (4 * sp.pi * G)}
def apply(e):
    e = e.subs(rho, sub[rho])
    for f in (Psi, Phi, ps):
        e = e.subs(f, sub[f])
    return sp.simplify(e.doit())
for k in ("Phi", "Psi", "ph"):
    v = apply(E[k]); print(f"{k}-equation on the claimed solution:", v); assert v == 0, k
ps_eq = apply(E["ps"])
print("psi-equation (determines phi; the QUMOND+tidal Poisson equation):")
print("  ", sp.simplify(ps_eq * 4 * sp.pi * G / r**2))
