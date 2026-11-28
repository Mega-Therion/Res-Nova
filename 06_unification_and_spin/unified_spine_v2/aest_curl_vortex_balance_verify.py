#!/usr/bin/env python3
"""SymPy symbolic verifier for Angle 3: AeST K_B Curl-Vortex Balance."""
import sympy as sp

K_B, c0, lam, u0, r, s = sp.symbols("K_B c0 lam u0 r s")

hill_vort = 15 * u0 * r * s
aest_curl = c0 * r * s
energy = K_B * aest_curl**2
residual = sp.expand(2 * energy - lam * hill_vort**2)
factored = sp.expand((2 * K_B * c0**2 - 225 * lam * u0**2) * r**2 * s**2)

assert sp.simplify(residual - factored) == 0, "Factorization mismatch"
matched = residual.subs(2 * K_B * c0**2, 225 * lam * u0**2)
assert sp.simplify(matched) == 0, "Matched coupling did not vanish"

print("PASS: Angle 3 (AeST K_B Curl-Vortex Balance) SymPy verification succeeded.")
