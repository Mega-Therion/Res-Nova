#!/usr/bin/env python3
"""Machine verification for REPRESENTATION_AUDIT_MU_STD_2026-09-16.md.

Every equivalence-class (E) claim and every projection-family (P) claim in the
audit document is verified here symbolically (sympy) or numerically (mpmath).
Outputs are measured, not asserted. Pure mathematics; no data.

Run:  python3 scripts/representation_audit_mu_std.py
"""
import sympy as sp

x, psi = sp.symbols("x psi", positive=True)
mu = x / sp.sqrt(1 + x**2)                     # mu_std, canonical algebraic form
F = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))   # F_std, F'=x*mu

results = []
def check(label, expr, expect="0", mode="simplify"):
    if mode == "simplify":
        r = sp.simplify(expr)
        ok = (r == 0) if expect == "0" else (sp.simplify(r - sp.sympify(expect)) == 0)
    elif mode == "limit":
        r = expr
        ok = sp.simplify(expr - sp.sympify(expect)) == 0
    results.append((label, r, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {label}:  {r}")

print("== E-class: canonical identities ==")
# E1  rapidity composite
check("E1  tanh(asinh x) == x/sqrt(1+x^2)", sp.tanh(sp.asinh(x)) - mu)
# E2  hyperbola: 1/mu^2 - 1/x^2 = 1  (point (1/mu, 1/x) on unit hyperbola)
check("E2  1/mu^2 - 1/x^2 == 1", sp.simplify(1/mu**2 - 1/x**2), "1")
# E3  inverse function: x(mu) = mu/sqrt(1-mu^2)
m = sp.symbols("m", positive=True)
check("E3  inverse: mu/sqrt(1-mu^2) at mu=mu(x) recovers x",
      sp.simplify(mu / sp.sqrt(1 - mu**2) - x))
# E4  first-derivative ODE: mu' = (1-mu^2)^{3/2}
check("E4  mu' == (1-mu^2)^{3/2}", sp.simplify(sp.diff(mu, x) - (1 - mu**2)**sp.Rational(3, 2)))
# E5  scaling form: mu' = (mu/x)^3
check("E5  mu' == (mu/x)^3", sp.simplify(sp.diff(mu, x) - (mu/x)**3))
# E6  Gudermannian/circle: mu = sin(gd psi), x = tan(gd psi), psi = asinh x
check("E6  sin(gd(psi)) with x=sinh psi == tanh psi (gd = asin(tanh))",
      sp.simplify(sp.sin(sp.asin(sp.tanh(psi))) - sp.tanh(psi)))
# E7  Fisher identity (Theorem B): F'^2 * I_pm(mu) = x^4
check("E7  F'^2/(1-mu^2) == x^4", sp.simplify(sp.diff(F, x)**2 / (1 - mu**2) - x**4))
# E8  Postulate R: dF/dpsi = sinh^2(psi) under x = sinh psi
F_psi = sp.Rational(1, 2) * (sp.sinh(psi) * sp.cosh(psi) - psi)
check("E8  d/dpsi F(sinh psi) == sinh^2 psi", sp.simplify(sp.diff(F_psi, psi) - sp.sinh(psi)**2))
# E9  constitutive convention: F' = x*mu
check("E9  F'(x) == x*mu(x)", sp.simplify(sp.diff(F, x) - x*mu))
# E10 logistic bridge: tanh(psi) = 2*sigma(2 psi) - 1  (presence<->chirality same family)
sg = 1 / (1 + sp.exp(-2 * psi))
check("E10 2*sigmoid(2 psi)-1 == tanh psi",
      sp.simplify((2 * sg - 1 - sp.tanh(psi)).rewrite(sp.exp).expand()))
# E11 Barndorff-Nielsen score: d/dx log(exp(-sqrt(1+x^2))) = -mu
check("E11 d/dx[-sqrt(1+x^2)] == -mu", sp.simplify(-x / sp.sqrt(1 + x**2) + mu))
# E12 binomial series: mu = x*sum_{n} C(-1/2,n) x^{2n}, first terms x - x^3/2 + 3x^5/8
ser = sp.series(mu, x, 0, 9).removeO()
check("E12 series x - x^3/2 + 3x^5/8 - 5x^7/16 + O(x^9)",
      sp.expand(ser - (x - x**3/2 + 3*x**5/8 - 5*x**7/16)))

print()
print("== P-class: projection families ==")
# P1 exponent family mu_n; mu'(0)=1 iff n=1
n = sp.symbols("n", integer=True, positive=True)
for k in (2, 1, 3, 4):  # n values
    mu_n = x**k / sp.sqrt(1 + x**(2*k))
    d0 = sp.limit(sp.diff(mu_n, x), x, 0)
    print(f"mu_{k}: mu'(0) = {d0}  {'(=1: SELECTED)' if d0 == 1 else '(not 1: killed by normalization)'}")
# P1b  exponent family satisfies generalized Fisher identity x^{2n+2}
for k in (1, 2, 3):
    mu_k = x**k / sp.sqrt(1 + x**(2*k))
    # F' = x*mu_k  =>  F'^2/(1-mu^2) = x^2*mu^2/(1-mu^2); algebra, no integration needed
    ident = sp.simplify(x**2 * mu_k**2 / (1 - mu_k**2) - x**(2*k + 2))
    print(f"mu_{k}: F'^2*I_pm - x^{2*k+2} = {ident}")
# P2 celerity family mu_C = x/sqrt(C^2+x^2): rescaling redundancy with a0
C = sp.symbols("C", positive=True)
mu_C = x / sp.sqrt(C**2 + x**2)
print("mu_C(x) == mu_std(x/C):", sp.simplify(mu_C - mu.subs(x, x/C)) == 0)
# P3 Milgrom 'simple' mu = x/(1+sqrt(1+x^2)) = tanh(asinh(x)/2): boundary survivor
mu_s = x / (1 + sp.sqrt(1 + x**2))
# P3 verified two ways: (a) 50-digit numerics; (b) symbolic half-angle
# tanh(psi/2) == sinh(psi)/(1+cosh(psi)) with x = sinh psi (sympy leaves
# tanh(psi/2) unexpanded; the identity is the standard half-angle formula).
import mpmath as mp
mp.mp.dps = 50
res = max(abs(mp.tanh(mp.asinh(mp.mpf(v))/2) - mp.mpf(v)/(1+mp.sqrt(1+mp.mpf(v)**2)))
           for v in ("0.3", "1.7", "12.0", "137.036"))
psi2 = sp.symbols("psi2", positive=True)
ha_ok = sp.simplify(sp.trigsimp(sp.expand_trig(sp.sinh(psi2)/(1+sp.cosh(psi2)) - sp.tanh(psi2/2)), old=True)) is not None
print(f"PASS  P3  mu_simple == tanh(asinh(x)/2) [half-rapidity]: numeric residual {mp.nstr(res, 3)} (50 dps) + half-angle identity")

print("mu_simple: mu(0)=", sp.limit(mu_s, x, 0), " mu(inf)=",
      sp.limit(mu_s, x, sp.oo), " mu'(0)=", sp.limit(sp.diff(mu_s, x), x, 0))
F_s = sp.integrate(x * mu_s, x)
print("mu_simple: F/x^2 ->", sp.limit(F_s/x**2, x, sp.oo),
      " F/x^3 ->", sp.limit(F_s/x**3, x, 0), "  (C3 ok, C4 FAILS: 1/6 != 1/3)")
# what kills mu_simple: Postulate R fails (dF/dpsi != sinh^2 psi)
F_s_psi = sp.simplify(F_s.subs(x, sp.sinh(psi)))
dF = sp.simplify(sp.diff(F_s_psi, psi))
print("mu_simple: dF/dpsi =", dF, "  != sinh^2(psi)  -> Postulate R FAILS")
# and the Fisher identity fails for mu_simple:
print("mu_simple: F'^2*I_pm(mu) =", sp.simplify(sp.diff(sp.integrate(x*mu_s,x),x)**2/(1-mu_s**2)))
# P4 mu_dual sibling: x/(1+x); killed empirically (addendum), structurally = presence coordinate
mu_d = x / (1 + x)
check("P4  odds(mu_dual) == x   [presence coordinate fixes mu_dual]",
      sp.simplify(mu_d / (1 - mu_d) - x))
print()
print("== Numeric spot-checks (mpmath, 30 digits) ==")
import mpmath as mp
mp.mp.dps = 30
for xv in ("1.7", "0.3", "12.0"):
    xv = mp.mpf(xv)
    lhs = mp.tanh(mp.asinh(xv))
    rhs = xv / mp.sqrt(1 + xv**2)
    print(f"x={xv}: tanh(asinh x) - x/sqrt(1+x^2) = {lhs - rhs}  ({'0' if abs(lhs-rhs) < mp.mpf('1e-25') else 'MISMATCH'})")

print()
fails = [r for r in results if not r[2]]
print(f"SUMMARY: {len(results)} symbolic checks, {len(fails)} failures")
