#!/usr/bin/env python3
"""Coefficients of the Laplacian terms in the frozen-metric zero-mode lift (zero_mode_lift.py dropped them as
vacuum-vanishing, which holds only where Psi, Phi, vphi are harmonic). Fit
   EL[L21] == EL[ 2K2Q0^2 Psi|gL|^2 + a*Lap(Psi)|gL|^2 + b*Lap(Phi)|gL|^2 + g*Lap(vphi)|gL|^2 ]
for constants a, b, g (up to total derivatives)."""
import sympy as sp
exec(open('zero_mode_lift.py').read().split("# kinetic check")[0])
LamS = sp.Function('Lam')(x, y, z)
L21 = coeff(build(LamS), 2, 1)
gl2 = sum(sp.diff(LamS, v)**2 for v in (x, y, z))
lap = lambda f: sum(sp.diff(f, v, 2) for v in (x, y, z))
a, b, g = sp.symbols('a b g')
cand = 2*K2*Q0**2*Psi*gl2 + a*lap(Psi)*gl2 + b*lap(Phi)*gl2 + g*lap(vphi)*gl2
diff = sp.expand(EL(L21, LamS) - EL(cand, LamS))
# collect coefficients of independent derivative monomials and solve for a, b, g
eqs = sp.Poly(diff, *sorted(diff.atoms(sp.Derivative), key=str)).coeffs()
sol = sp.solve(eqs, [a, b, g], dict=True)
print("solution:", sol)
if sol:
    rem = sp.simplify(diff.subs(sol[0]))
    print("remainder after fit (must be 0):", rem)
