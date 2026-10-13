#!/usr/bin/env python3
"""The physical rule that ties the even part to the odd part: the corpus's own driven, damped two-level system.

Model (Res-Nova 05_lean_formalization/PillarIV_AntiDriftGate.lean, section 2): H = u sigma_x, jump operator
sigma_minus with rate gamma, GKSL generator L(rho) = -i[H, rho] + gamma (L rho L+ - 1/2 {L+ L, rho}).

chirality_of_a_chain.py showed that for a classical chain chi (from pi) and the sign (loop affinity) are
independent, so a link needs added structure. Here the structure is the dynamics itself. In the steady state:
  * the populations are the even part: unchanged by the mirror (complex conjugation, equivalently u -> -u);
  * the coherence rho_01 is purely imaginary, the odd part: the mirror flips its sign;
  * balance of the excited population:  2 u Im(rho_01) = gamma rho_11   (drive in = decay out);
  * eliminating u and gamma between the two steady-state equations gives an identity free of both:
        (Im rho_01)^2 = rho_11 (1 - 2 rho_11);
  * so the coherence C = 2 |rho_01| obeys C^2 = 4 p (1 - 2 p) with p = rho_11, and its maximum is 1/sqrt 2,
    reached at p = 1/4, u/gamma = 1/(2 sqrt 2). That is the lower end of the band [1/sqrt 2, kappa].
Solved here from the generator itself (not from the file's stated answer), then compared. Exit 0 only if all pass.
"""
import sys
import sympy as sp

ok_all = True


def check(name, ok, detail=""):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


u, g = sp.symbols("u gamma", positive=True)
p, a, b = sp.symbols("p a b", real=True)                 # rho_11 = p, rho_01 = a + i b
rho = sp.Matrix([[1 - p, a + sp.I * b], [a - sp.I * b, p]])
H = sp.Matrix([[0, u], [u, 0]])
Lm = sp.Matrix([[0, 1], [0, 0]]); Lp = Lm.T
gen = -sp.I * (H * rho - rho * H) + g * (Lm * rho * Lp - sp.Rational(1, 2) * (Lp * Lm * rho + rho * Lp * Lm))
eqs = [sp.re(sp.expand(gen[1, 1])), sp.re(sp.expand(gen[0, 1])), sp.im(sp.expand(gen[0, 1]))]
sol = sp.solve(eqs, [p, a, b], dict=True)[0]
D = g ** 2 + 8 * u ** 2
check("G1 steady state solved from the generator matches the corpus's formula",
      sp.simplify(sol[p] - 4 * u ** 2 / D) == 0 and sol[a] == 0 and sp.simplify(sol[b] - 2 * g * u / D) == 0,
      f"rho_11 = {sp.factor(sol[p])}, rho_01 = i * {sp.factor(sol[b])}")
check("G2 the coherence is purely imaginary (real part 0)", sol[a] == 0)
solm = {k: v.subs(u, -u) for k, v in sol.items()}
check("G3 mirror (u -> -u, i.e. complex conjugation): populations unchanged, coherence flips sign",
      sp.simplify(solm[p] - sol[p]) == 0 and sp.simplify(solm[b] + sol[b]) == 0)
check("G4 balance: 2 u Im(rho_01) = gamma rho_11", sp.simplify(2 * u * sol[b] - g * sol[p]) == 0)
check("G5 identity free of u and gamma: (Im rho_01)^2 = rho_11 (1 - 2 rho_11)", sp.simplify(sol[b] ** 2 - sol[p] * (1 - 2 * sol[p])) == 0)
x = sp.symbols("x", positive=True)
C = sp.simplify((2 * sol[b]).subs(u, x * g))
check("G6 C = 2 |rho_01| = 4x / (1 + 8 x^2) with x = u / gamma (the corpus's coherence function)", sp.simplify(C - 4 * x / (1 + 8 * x ** 2)) == 0)
xs = sp.solve(sp.diff(C, x), x)
check("G7 its maximum is 1/sqrt 2 at x = 1/(2 sqrt 2), where rho_11 = 1/4",
      xs == [sp.sqrt(2) / 4] and sp.simplify(C.subs(x, xs[0]) - 1 / sp.sqrt(2)) == 0 and sp.simplify(sol[p].subs(u, xs[0] * g) - sp.Rational(1, 4)) == 0)
pp = sp.symbols("p", positive=True)
check("G8 same ceiling from the identity alone: max of 4 p (1 - 2p) is 1/2 at p = 1/4", sp.solve(sp.diff(4 * pp * (1 - 2 * pp), pp), pp) == [sp.Rational(1, 4)]
      and (4 * pp * (1 - 2 * pp)).subs(pp, sp.Rational(1, 4)) == sp.Rational(1, 2))
check("G9 positivity of rho: |rho_01|^2 <= rho_00 rho_11 holds, with equality only at u = 0",
      sp.simplify((1 - sol[p]) * sol[p] - sol[b] ** 2 - sol[p] ** 2) == 0, "rho_00 rho_11 - |rho_01|^2 = rho_11^2 >= 0")
# ---- The same steady state written in Res-Nova's interpolating function ---------------------------------------------
# mu_std(y) = y / sqrt(1 + y^2). Put y = 2 sqrt(2) u / gamma and mu = mu_std(y). Then, exactly:
#     rho_11 = mu^2 / 2,     Im rho_01 = mu sqrt(1 - mu^2) / sqrt 2,     C = 2 |rho_01| = sqrt 2 * mu * sqrt(1 - mu^2).
# The retracted premise was "coherence = mu(u/gamma)". The true statement is that the EXCITED POPULATION is mu^2/2,
# and the coherence is sqrt 2 mu sqrt(1 - mu^2), which peaks at mu = 1/sqrt 2, i.e. at y = 1, with value 1/sqrt 2.
yv = 2 * sp.sqrt(2) * u / g
mu = yv / sp.sqrt(1 + yv ** 2)
check("G10 excited population = mu_std(y)^2 / 2 with y = 2 sqrt(2) u / gamma", sp.simplify(sol[p] - mu ** 2 / 2) == 0)
check("G11 Im rho_01 = mu sqrt(1 - mu^2) / sqrt 2", sp.simplify(sol[b] - mu * sp.sqrt(1 - mu ** 2) / sp.sqrt(2)) == 0)
m_ = sp.symbols("m", positive=True)
Cm = sp.sqrt(2) * m_ * sp.sqrt(1 - m_ ** 2)
crit = sp.solve(sp.diff(Cm, m_), m_)
check("G12 coherence sqrt 2 mu sqrt(1 - mu^2) peaks at mu = 1/sqrt 2 with value 1/sqrt 2",
      crit == [sp.sqrt(2) / 2] and sp.simplify(Cm.subs(m_, crit[0]) - 1 / sp.sqrt(2)) == 0)
check("G13 mu = 1/sqrt 2 is y = 1: the point x = 1 of mu_std, where g = a0 in the galaxy reading",
      sp.simplify((1 / sp.sqrt(1 + 1)) - 1 / sp.sqrt(2)) == 0 and sp.simplify(mu.subs(u, g / (2 * sp.sqrt(2))) - 1 / sp.sqrt(2)) == 0)
check("G14 the retracted premise fails as stated: coherence != mu(u/gamma)", sp.simplify(C - x / sp.sqrt(1 + x ** 2)) != 0)

print("\nALL PASS" if ok_all else "\nSOME FAIL")
sys.exit(0 if ok_all else 1)
