#!/usr/bin/env python3
"""Angular gradient instability of the quartic-screened solar core, 2026-11-18. [D] algebra; [O] physics.

Spherical flux: 2 k4 y^3 + 2 k3 r y^2 + Z r^2 y = GM, with y = phi0'. Linearised principal symbol around phi0:
  radial  M_rr = Z + 4 k3 b + 6 k4 b^2
  angular M_perp = Z + 2 k3 (a + b) + 6 k4 a b,   a = y', b = y/r.
Result (SymPy, series in r): in the quartic-dominated core, M_perp -> -Z + 2 k3^2/(3 k4).
- Pure quartic (k3 = 0): M_perp -> -Z < 0. Inside the Vainshtein region the screened static solution's operator is non-elliptic in the
  angular directions; that is a gradient instability if the time-kinetic coefficient is positive.
- A cubic term stabilises the core iff 2 k3^2/(3 k4) > Z.
- Anisotropic Z (hand-derived to O(1), consistent with this series): an angular direction e1 sees
  -Z_{e2e2} + 2 k3^2/(3 k4), so the criterion is 2 k3^2/(3 k4) > Z_max.
- Near the Sun the Galileon cancels the Galactic tide (induced H1 = alpha I - T). The Z that enters is
  therefore the external-field AQUAL tensor A_e(I + L e e), not the Galaxy-cofactor-inflated one.
(My first hand derivation had the sign of the cubic term wrong; this is the corrected statement.)
"""
import sympy as sp
r, Z, k3, k4, GM = sp.symbols("r Z kappa3 kappa4 GM", positive=True)
c = sp.Symbol("c", positive=True)                                  # core value (GM/(2 k4))^(1/3)
# series solution y = c + y1 r + y2 r^2 + ...
y1, y2, y3 = sp.symbols("y1 y2 y3")
y = c + y1 * r + y2 * r**2 + y3 * r**3
flux = sp.expand(2 * k4 * y**3 + 2 * k3 * r * y**2 + Z * r**2 * y - 2 * k4 * c**3)
sol = sp.solve([flux.coeff(r, 1), flux.coeff(r, 2), flux.coeff(r, 3)], [y1, y2, y3], dict=True)[0]
ys = y.subs(sol)
a = sp.diff(ys, r); b = ys / r
Mperp = sp.series(sp.expand(Z + 2 * k3 * (a + b) + 6 * k4 * a * b), r, 0, 1).removeO()
Mperp0 = sp.simplify(sp.limit(Mperp, r, 0))
print("y1 =", sp.simplify(sol[y1]))
print("M_perp(r->0) =", Mperp0)
assert sp.simplify(Mperp0 - (-Z + 2 * k3**2 / (3 * k4))) == 0
# pure quartic
Mq = sp.simplify(Mperp0.subs(k3, 0)); print("pure quartic M_perp(r->0) =", Mq); assert Mq == -Z
# cubic-dominated region: y = sqrt(GM/(2 k3 r)) => a = -b/2; M_perp = Z + k3 b - 3 k4 b^2 > 0 iff k3 > 3 k4 b (cubic must beat quartic by 3x)
bb = sp.Symbol("b", positive=True)
Mc = sp.expand(Z + 2 * k3 * (-bb / 2 + bb) + 6 * k4 * (-bb / 2) * bb); print("cubic-region M_perp =", Mc)
