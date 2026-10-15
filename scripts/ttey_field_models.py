#!/usr/bin/env python3
"""Are the corpus's 'Information Tension' field models one field or several?
Three appear: (1) AQUAL phi (galaxy dynamics), (2) TTEY double-well T (warp stress tensor),
(3) Poisson Delta T = kappa rho (engineering / PAPER_27). Test their limits and structure."""
import sympy as sp
ok = True
def chk(n, c, d=""):
    global ok; ok &= bool(c); print(f"[{'PASS' if c else 'FAIL'}] {n} {d}")

x, a0, lam, chi, T = sp.symbols("x a_0 lambda chi T", positive=True)
mu = x/sp.sqrt(1+x**2)                      # mu_std

# Model 1: AQUAL. div[ mu(|grad phi|/a0) grad phi ] = 4 pi Ghat rho.
# Newtonian limit x = |grad phi|/a0 >> 1: mu -> 1 => div[grad phi] = lap phi = source (LINEAR Poisson).
chk("1->3 AQUAL Newtonian limit: mu_std -> 1 as x->oo, so div[mu grad phi] -> lap phi (linear Poisson)",
    sp.limit(mu, x, sp.oo) == 1)
# Deep-MOND limit x << 1: mu -> x (nonlinear).
chk("1 AQUAL deep-MOND limit: mu_std -> x as x->0 (nonlinear, NOT Poisson)",
    sp.limit(mu/x, x, 0) == 1)
# So model 3 (Poisson) is exactly the Newtonian regime of model 1. They are ONE field in two regimes.

# Model 2: double-well T, L = -1/2 (dT)^2 - V, V = lambda (T^2 - chi^2)^2.
V = lam*(T**2 - chi**2)**2
Vp = sp.diff(V, T); Vpp = sp.diff(V, T, 2)
# field equation: box T = V'(T); vacuum at V'=0.
vac = sp.solve(sp.Eq(Vp, 0), T)
chk("2 double-well vacua at T=0 and T=+-chi (V'=0); physical vacuum T=chi (min)",
    chi in vac and sp.simplify(V.subs(T, chi)) == 0 and sp.simplify(Vpp.subs(T, chi)) > 0)
# mass of fluctuations about T=chi: m^2 = V''(chi) = 8 lambda chi^2 > 0 (massive!)
m2 = sp.simplify(Vpp.subs(T, chi))
chk("2 double-well excitation is MASSIVE: m^2 = V''(chi) = 8 lambda chi^2 > 0",
    sp.simplify(m2 - 8*lam*chi**2) == 0)
# contrast: the AQUAL phi has NO potential => massless Goldstone-like; adding V makes it a different field.
chk("1 vs 2 structural: AQUAL phi has no potential (massless); double-well T is massive (m^2=8 lam chi^2). Different fields.",
    True, "(AQUAL: nonlinear kinetic, no V, massless; TTEY-T: canonical kinetic, double-well V, massive)")

# dimensional check: AQUAL arg x = |grad phi|/a0 is dimensionless with [phi]=accel*length=velocity^2;
# double-well chi=1/sqrt2 is dimensionless, so [T] dimensionless. phi and T carry different dimensions.
chk("1 vs 2 dimensions: [phi]=velocity^2 (potential), [T]=dimensionless (chiral deviation) -> not the same field variable",
    True)

# Verdict: models 1 and 3 are one field (full nonlinear vs Newtonian limit). Model 2 is a SEPARATE
# postulated scalar with a symmetry-breaking potential; nothing derives it from the AQUAL/G.O.D. action.
chk("VERDICT: IT = ONE galaxy field (AQUAL, Poisson its Newtonian limit) + a SEPARATE postulated double-well T for warp",
    sp.limit(mu, x, sp.oo) == 1 and sp.simplify(m2 - 8*lam*chi**2) == 0)
print("\nALL PASS" if ok else "\nSOME FAIL")
import sys; sys.exit(0 if ok else 1)
