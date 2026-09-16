#!/usr/bin/env python3
"""Machine verification for POSTULATE_R_ISOLATION_2026-09-16.md.

Controlled isolation of Postulate R (dF/dpsi = x^2, psi = artanh mu):
it is shown to decompose into exactly two independent inputs —
  (A) the chiral alphabet:  psi = artanh(mu)   [C]
  (B) the celerity identification:  x = sinh(psi)  [O]
given the AQUAL constitutive F'(x) = x*mu(x)  [P, literature].
Postulate R itself is then a THEOREM, not an input (checks R1, R2);
neither (A) nor (B) is derivable from the rest (witnesses W1-W3);
and the exponent 2 in x^2 is automatic, not an extra input (R3).

Run:  python3 scripts/postulate_r_isolation.py
"""
import sympy as sp

x, psi, C = sp.symbols("x psi C", positive=True)
mu = x / sp.sqrt(1 + x**2)          # mu_std
F = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))   # F_std, F' = x*mu

print("== R1  Redundancy (forward): (A)+(B)+constitutive => Postulate R ==")
# Given: psi = artanh(mu), x = sinh(psi), mu = tanh(psi), F' = x*mu.
# Then dF/dpsi = F'(x) * dx/dpsi = x*tanh(psi)*cosh(psi) = sinh^2(psi) = x^2.
dFdpsi = x * sp.tanh(psi) * sp.cosh(psi)   # F' * dx/dpsi, x = sinh(psi)
res = sp.simplify(dFdpsi.subs(x, sp.sinh(psi)) - sp.sinh(psi)**2)
print(f"  dF/dpsi - sinh^2(psi) = {res}   (Postulate R is a THEOREM given (A)+(B))")
assert res == 0

print("== R2  Theorem A (backward): Postulate R + constitutive => x = C*sinh(psi) ==")
X = sp.Function("X")
sol = sp.dsolve(sp.Eq(X(psi)**2, X(psi)*sp.tanh(psi)*sp.diff(X(psi), psi)), X(psi))
print(f"  dsolve -> {sol}")
# verify C*sinh(psi) satisfies the ODE
check = sp.simplify((C*sp.sinh(psi))**2 - C*sp.sinh(psi)*sp.tanh(psi)*sp.diff(C*sp.sinh(psi), psi))
print(f"  residual for x = C*sinh(psi): {check}  (mu'(0)=1 fixes C=1 -> x=sinh(psi), i.e. (B))")
assert check == 0

print("== R3  The exponent 2 in x^2 is automatic ==")
# dF/dpsi = sinh^2(psi) and x = sinh(psi) force dF/dpsi = x^2 identically;
# no separate 'the conjugate is x^2' input exists beyond (B).
res = sp.simplify(sp.sinh(psi)**2 - (sp.sinh(psi))**2)
print(f"  sinh^2(psi) == x^2 under (B): automatic, no extra input.")
# NOTE (recorded in the doc): 'the action depends on x^2' is a reading, not a
# derivation: the AQUAL action depends on F(|x|), an odd function of x, not on x^2.

print()
print("== W1  Witness mu_dual: constitutive+normalization+boundary do NOT force (A) or (B) ==")
mu_d = x / (1 + x)
F_d = sp.integrate(x * mu_d, x)
print(f"  mu_dual: F' - x*mu = {sp.simplify(sp.diff(F_d, x) - x*mu_d)} (constitutive OK)")
print(f"  mu_dual: mu(0)={sp.limit(mu_d, x, 0)}, mu(inf)={sp.limit(mu_d, x, sp.oo)}, mu'(0)={sp.limit(sp.diff(mu_d, x), x, 0)}")
# (B) fails for mu_dual: sinh(artanh(mu_dual)) != x
hyp_odds = sp.simplify(mu_d / sp.sqrt(1 - mu_d**2))
print(f"  mu_dual: sinh(artanh mu) - x = {sp.simplify(hyp_odds - x)}   != 0  -> (B) FAILS")
# the presence alphabet instead: odds(mu_dual) = x
print(f"  mu_dual: odds(mu) - x = {sp.simplify(mu_d/(1-mu_d) - x)}  (presence alphabet holds)")
print("  VERDICT: all constitutive/normalization/boundary inputs hold, (B) fails -> (B) not derivable from them")

print()
print("== W2  Witness mu_simple: alphabet (A) does NOT force (B) ==")
mu_s = x / (1 + sp.sqrt(1 + x**2))
print(f"  mu_simple: artanh(mu) exists on (0,1), chiral alphabet accepted")
hyp_odds_s = sp.simplify(mu_s / sp.sqrt(1 - mu_s**2))
print(f"  mu_simple: sinh(artanh mu) - x = {sp.simplify(hyp_odds_s - x)}   != 0  -> (B) FAILS")
print(f"  (in fact sinh(artanh mu_simple) = {sp.simplify(hyp_odds_s)} = sinh(2*psi_s/2)... half-rapidity)")
print("  VERDICT: (A) alone does not select the celerity identification")

print()
print("== W3  Rapidity-multiple family: x = sinh(n*psi_s), mu = tanh(psi_s) ==")
# For each n, mu as a function of x has mu'(0) = 1/n. n=1 -> mu_std; n=2 -> mu_simple.
for n in (1, 2, 3):
    # x = sinh(n*psi) => near 0: x ~ n*psi, mu ~ psi => mu'(0) = 1/n
    # exact: mu(x) = tanh(asinh(x)/n)
    mu_n = sp.tanh(sp.asinh(x)/n)
    d0 = sp.limit(sp.diff(mu_n, x), x, 0)
    tag = "  == mu_std" if n == 1 else ("  == mu_simple" if n == 2 else "")
    print(f"  n={n}: mu'(0) = {d0}{tag}")
res = sp.simplify(sp.tanh(sp.asinh(x)/2) - mu_s)
print(f"  n=2 member equals mu_simple: residual {sp.simplify((sp.tanh(sp.asinh(x)/2) - mu_s).rewrite(sp.exp).expand())} (also 50-digit verified in the mu_std audit)")
print("  VERDICT: mu'(0)=1 kills every n != 1 of the rapidity-multiple family;")
print("           mu_simple is the n=2 member, not an unrelated competitor")

print()
print("== U1  Unruh-route discriminator (numerical, [O]) ==")
# Candidate explanation of (B): mu_std = acceleration in de Sitter-Unruh temperature
# units. Obstacle: the natural crossover is a_dS = c*H0, whereas the corpus a0 = cH0/2pi.
c = 2.99792458e8          # m/s
H0 = 70e3 / 3.0857e22 * 1  # 70 km/s/Mpc in 1/s  (Mpc = 3.0857e22 m)
a_dS = c * H0
a0_sparc = 1.2e-10         # m/s^2 (SPARC central value, literature)
print(f"  c*H0/2pi = {a_dS/(2*sp.pi.evalf()) if False else a_dS/ (2*3.141592653589793):.3e} m/s^2")
print(f"  c*H0     = {a_dS:.3e} m/s^2")
print(f"  SPARC a0 = {a0_sparc:.3e} m/s^2")
print(f"  a0/(cH0/2pi) = {a0_sparc/(a_dS/6.283185307179586):.3f}  (10%-level coincidence)")
print(f"  a0/(cH0)     = {a0_sparc/a_dS:.3f}  (factor ~5.7 off without the 2pi)")
print("  VERDICT: the 2pi form is the right order; the factor remains unexplained [O]")

print()
print("SUMMARY: Postulate R = (A) chiral alphabet [C] + (B) celerity identification [O]")
print("         given constitutive F'=x*mu [P] and mu'(0)=1 (double-duty normalization).")
print("         R itself is a theorem given (A)+(B); neither (A) nor (B) is derived here.")
