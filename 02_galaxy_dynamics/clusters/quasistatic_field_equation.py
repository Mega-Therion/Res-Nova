#!/usr/bin/env python3
"""The AeST quasi-static field equation, varied from SZ's PUBLISHED action. 2026-09-24.

Letter arXiv:2007.00082 eq. `NT_quasi_Phi`:

  S = - INT d^4x { (2-K_B)/(16 pi Gt) [ |grad Phi|^2 - 2 grad Phi . grad phi
                                        + |grad phi|^2 - mu^2 Phi^2 + J(Y) ]
                   + Phi rho }

with J(Y) = F(Y,Q_0)/(2-K_B) and mu = sqrt(2 K_2/(2-K_B)) Q_0.

The point: the mu^2 Phi^2 term turns Poisson into HELMHOLTZ, and SZ state the MOND
solution holds only for r <~ r_C ~ (r_M mu^-2)^(1/3). We check the sign and the scale.
"""
import sympy as sp

x, y, z = sp.symbols('x y z')
KB, Gt, mu, rho = sp.symbols('K_B Gtilde mu rho', positive=True)
Phi = sp.Function('Phi')(x, y, z)
vph = sp.Function('varphi')(x, y, z)
A = (2 - KB)/(16*sp.pi*Gt)

def grad2(f):   return sum(sp.diff(f, v)**2 for v in (x, y, z))
def dot(f, g):  return sum(sp.diff(f, v)*sp.diff(g, v) for v in (x, y, z))
def lap(f):     return sum(sp.diff(f, v, 2) for v in (x, y, z))

# Lagrangian density, J(Y) dropped (it is the MOND/AQUAL piece, unchanged from AQUAL)
L = -( A*(grad2(Phi) - 2*dot(Phi, vph) + grad2(vph) - mu**2*Phi**2) + Phi*rho )

def euler_lagrange(L, f):
    e = sp.diff(L, f)
    for v in (x, y, z):
        e -= sp.diff(sp.diff(L, sp.diff(f, v)), v)
    return sp.simplify(sp.expand(e))

eqPhi = euler_lagrange(L, Phi)
eqvph = euler_lagrange(L, vph)
print("delta S / delta Phi = 0  ->")
print("   ", sp.simplify(eqPhi/(2*A)), " = 0\n")
print("delta S / delta varphi = 0  ->")
print("   ", sp.simplify(eqvph/(2*A)), " = 0\n")

# solve the Phi equation for the structure
lhs = sp.simplify(sp.expand(eqPhi/(2*A)))
print("Rearranged, with lap(Phi) isolated:")
sol = sp.solve(sp.Eq(lhs, 0), lap(Phi))
print("   lap(Phi) =", sp.simplify(sol[0]) if sol else "(see above)")
print()
print("=" * 78)
print("THE Phi EQUATION, collected by hand from the numerator above:")
print()
print("      lap(Phi) + mu^2 Phi - lap(varphi) = 8 pi Gt rho / (2 - K_B)")
print()
print("STRUCTURE: Phi carries a +mu^2 Phi term. That is HELMHOLTZ, not Poisson and NOT")
print("  Yukawa -- the sign is positive, so the point-mass Green's function goes like")
print("  cos(mu r)/r: OSCILLATORY, not exponentially screened. This is exactly what SZ")
print("  describe as 'oscillatory for r >~ r_C'.")
print()
print("HONEST LIMIT OF THIS SCRIPT: J(Y) was dropped, which DEGENERATES the varphi")
print("  sector -- the varphi equation collapses to lap(varphi) = lap(Phi), and feeding")
print("  that back gives the contentless mu^2 Phi = 8 pi Gt rho/(2-K_B). So this")
print("  establishes the OPERATOR STRUCTURE only. With J(Y) present, lap(varphi) is")
print("  replaced by the AQUAL/MOND operator and the system is nonlinear.")
print("  A real cluster prediction requires solving THAT. Not done here.")
print()
print("CONSEQUENCE FOR D10: at r_500 the clusters sit at r ~ 2 r_C, past the first")
print("  turning point of that oscillation. The MOND force law used in D10 is outside")
print("  its domain of validity there, by AeST's own structure. D10's 1.96 is a correct")
print("  test of PURE MOND. It is NOT the AeST prediction at r_500.")
