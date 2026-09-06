#!/usr/bin/env python3
"""Does the EM sector, coupled to Res-Nova's physical metric, source negative pressure?

The coupling is NOT free. Photons are matter; matter couples to the physical metric
    g~_mn = A(phi) g_mn + B(phi) u_m u_n            (D7, D8)
so f(phi) is FIXED by (A,B). This script derives the induced Maxwell Lagrangian
symbolically, then evaluates the two constraints numerically.
"""
import sympy as sp

A, B, F2, E2 = sp.symbols('A B F2 E2', positive=True, real=True)

# --- inverse and volume element of the disformal metric -------------------
# g~^{mn} = (1/A)(g^{mn} - b u^m u^n),  b = B/(A-B)      [u.u = -1]
b = B/(A-B)
# det g~ = A^4 (1 - B/A) det g   (matrix determinant lemma, u.u = -1)
sqrt_g_tilde = A**sp.Rational(3,2)*(A-B)**sp.Rational(1,2)

# --- contract the field strength ------------------------------------------
# g~^{ma} g~^{nb} F_mn F_ab = (1/A^2)( F^2 - 2 b E^2 ),  E_m = F_mn u^n
# the b^2 piece vanishes: F_mn u^m u^n = 0 by antisymmetry
contraction = (F2 - 2*b*E2)/A**2

L = sp.simplify(-sp.Rational(1,4)*sqrt_g_tilde*contraction)
print("L_EM  =", sp.simplify(L))

# --- the two coefficients --------------------------------------------------
cF = sp.simplify(sp.expand(L).coeff(F2))     # multiplies F^2
cE = sp.simplify(sp.expand(L).coeff(E2))     # multiplies E^2
print("coeff F^2 =", sp.simplify(cF), "   -> f(phi) =", sp.simplify(-4*cF))
print("coeff E^2 =", sp.simplify(cE))

print("\nB -> 0 limit (strictly conformal):")
print("  coeff F^2 ->", sp.limit(cF, B, 0), "  (Maxwell: -1/4)")
print("  coeff E^2 ->", sp.limit(cE, B, 0))

# --- Res-Nova's own falsified map, as a cross-check of the algebra ---------
phi = sp.symbols('phi', real=True)
Am, Bm = sp.exp(-2*phi), -2*sp.sinh(2*phi)
print("\nRes-Nova map A=e^{-2phi}, B=-2sinh(2phi):")
print("  A - B      =", sp.simplify(Am-Bm), " (D8 has g~_00 = -e^{2phi})")
print("  f(phi)     =", sp.simplify((-4*cF).subs({A:Am,B:Bm})))
print("  c_gamma^2  =", sp.simplify(((A-B)/A).subs({A:Am,B:Bm})), " (D8 has e^{4phi})")

# --- small-B expansion: size of the departure from Maxwell ----------------
r = sp.symbols('r', positive=True)   # r = B/A
cF_r = sp.simplify(cF.subs(B, r*A))
print("\ndeparture from Maxwell, to O(B/A):")
print("  f  =", sp.series(sp.simplify(-4*cF_r), r, 0, 2))
