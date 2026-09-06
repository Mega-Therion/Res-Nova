#!/usr/bin/env python3
"""PREP (stage 1): Godel metric, causal structure, and the CTC threshold.

Establishes the geometry before any holonomy is computed. Nothing here is a
holonomy result; this stage exists to fix conventions and verify the threshold.

Godel line element, cylindrical form (Hawking & Ellis eq. 5.7):

  ds^2 = 4a^2[ -dt^2 + dr^2 - (sinh^4 r - sinh^2 r) dphi^2
               + 2*sqrt(2)*sinh^2 r  dphi dt + dz^2 ]
"""
import sympy as sp

t, r, phi, z, a = sp.symbols('t r phi z a', real=True, positive=True)

g = sp.zeros(4, 4)
# coordinate order: (t, r, phi, z)
g[0,0] = -4*a**2
g[1,1] =  4*a**2
g[2,2] = -4*a**2*(sp.sinh(r)**4 - sp.sinh(r)**2)
g[3,3] =  4*a**2
g[0,2] = g[2,0] = 4*a**2*sp.sqrt(2)*sp.sinh(r)**2

print("g_phiphi =", sp.simplify(g[2,2]))
gpp = sp.simplify(g[2,2]/(4*a**2))
print("g_phiphi/(4a^2) =", sp.factor(gpp), "= sinh^2(r)*(1 - sinh^2(r))")

# A phi-circle (t, r, z fixed) is TIMELIKE -- a CTC -- when g_phiphi < 0.
print("\nCTC condition: g_phiphi < 0  <=>  sinh^2(r) > 1  <=>  sinh(r) > 1")
sol = sp.solve(sp.Eq(sp.sinh(r), 1), r)
print("threshold r_c =", sol, "= arcsinh(1) =", float(sp.asinh(1)))

# The convergence with the framework's theta.
theta_godel = sp.tanh(sp.asinh(1))
print("\ntanh(arcsinh 1) =", sp.simplify(theta_godel), "=", float(theta_godel))
print("1/sqrt(2)       =", float(1/sp.sqrt(2)))
print("EXACT MATCH:", sp.simplify(theta_godel - 1/sp.sqrt(2)) == 0)

# Sanity: signature and determinant off the threshold
for rv in [0.5, float(sp.asinh(1)), 1.5]:
    val = float(gpp.subs(r, rv))
    kind = "spacelike circle" if val > 0 else ("NULL (threshold)" if abs(val) < 1e-12 else "TIMELIKE -> CTC")
    print(f"  r={rv:.4f}  sinh r={float(sp.sinh(rv)):.4f}  g_phiphi/(4a^2)={val:+.6f}  {kind}")

sp.pprint(g)
