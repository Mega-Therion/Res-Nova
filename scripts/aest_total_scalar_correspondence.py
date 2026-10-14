#!/usr/bin/env python3
"""AeST: the scalar-channel function whose TOTAL quasistatic law is mu_std, and what the current one gives instead.

Setting (TARGET_D7_COVARIANT_COMPLETION.md section 2): in the quasistatic weak-field limit matter feels
Phi = Phi_hat + phi, with  lap Phi_hat = 4 pi G_hat rho  and  div[J'(Y) grad phi] = 4 pi G_hat rho,  Y = |grad phi|^2.
In spherical symmetry, away from the AeST mass term, with the two gradients aligned:
    g = g_hat + g_phi,   J'(Y) g_phi = g_hat,   g_hat = eta g_N,   eta = G_hat/G_N = lambda_s/(1 + lambda_s).
Write x = g/a0, y = g_N/a0, s = g_phi/a0, with a0 the fitted total-law scale. If the total law is x mu(x) = y
(mu = mu_std, as in the SPARC comparison), the scalar channel must satisfy
    s = x [1 - eta mu(x)],   J'(a0^2 s^2) = eta mu(x) / (1 - eta mu(x)),
    J(Y(x)) = a0^2 [2 eta F_std(x) - eta^2 y(x)^2],   F_std(x) = (x sqrt(1+x^2) - arsinh x)/2.
This is single-valued iff s(x) is monotone, iff lambda_s < (27 + 12 sqrt 6)/5 = 11.2788.
The function now in the corpus, J' = lambda_s mu_std(sqrt(Y)/a0_tilde) with a0_tilde = (1 + lambda_s) a0
(TARGET_D7 section 2.1 pattern; SZStdEmbedding.lean at a0 = 1), puts mu_std in the SCALAR channel. Its total law
is a different law; parts B and C measure the difference. Part D re-checks the stealth configuration that
TARGET_D3 section 34 already records. Exit 0 only if every check passes.
"""
import math
import sys

import mpmath as mp
import sympy as sp

ok_all = True


def check(name, ok, detail=""):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


# ---------------------------------------------------------------- A. the correspondence, exact
x, a0, eta, lam, t = sp.symbols("x a_0 eta lambda_s t", positive=True)
mu = x / sp.sqrt(1 + x**2)
y = x * mu
F = (x * sp.sqrt(1 + x**2) - sp.asinh(x)) / 2
s = x * (1 - eta * mu)
Jp = eta * mu / (1 - eta * mu)
J = a0**2 * (2 * eta * F - eta**2 * y**2)
Y = a0**2 * s**2

check("A1 F_std' = x mu_std = y", sp.simplify(sp.diff(F, x) - y) == 0)
check("A2 Gauss law on the curve: J' s = eta y  (J'(Y) g_phi = g_hat)", sp.simplify(Jp * s - eta * y) == 0)
check("A3 closed form: dJ/dx - J'(Y(x)) dY/dx = 0", sp.simplify(sp.diff(J, x) - Jp * sp.diff(Y, x)) == 0)
deep = sp.limit(J / ((2 * eta / (3 * a0)) * Y**sp.Rational(3, 2)), x, 0)
check("A4 deep MOND: J ~ (2 eta/(3 a0)) Y^(3/2) = (2 lambda_s/(3 a0_tilde)) Y^(3/2)",
      deep == 1 and sp.simplify((2 * eta / (3 * a0)).subs(eta, lam / (1 + lam)) - 2 * lam / (3 * (1 + lam) * a0)) == 0,
      f"(ratio -> {deep})")
check("A5 Newtonian end: J' -> eta/(1 - eta) = lambda_s",
      sp.simplify(sp.limit(Jp, x, sp.oo) - eta / (1 - eta)) == 0
      and sp.simplify((eta / (1 - eta)).subs(eta, lam / (1 + lam)) - lam) == 0)
yprime = x * (x**2 + 2) / (1 + x**2) ** sp.Rational(3, 2)
check("A6 s'(x) = 1 - eta y'(x), y'(x) = x(x^2+2)/(1+x^2)^(3/2)",
      sp.simplify(sp.diff(s, x) - (1 - eta * yprime)) == 0 and sp.simplify(sp.diff(y, x) - yprime) == 0)
check("A7 32(1+t)^3 - 27 t (t+2)^2 = (t-2)^2 (5t+8) >= 0, so y'^2 <= 32/27 with equality only at x = sqrt 2",
      sp.expand(32 * (1 + t) ** 3 - 27 * t * (t + 2) ** 2 - (t - 2) ** 2 * (5 * t + 8)) == 0
      and sp.simplify(yprime.subs(x, sp.sqrt(2)) - 4 * sp.sqrt(2) / (3 * sp.sqrt(3))) == 0)
q = 3 * sp.sqrt(3) / (4 * sp.sqrt(2))
check("A8 threshold: eta < 3 sqrt3/(4 sqrt2) <=> lambda_s < q/(1-q) = (27 + 12 sqrt 6)/5",
      sp.simplify(q / (1 - q) - (27 + 12 * sp.sqrt(6)) / 5) == 0, f"= {float(q / (1 - q)):.6f}")
check("A9 ghost condition 1: J' > 0 on the curve (0 < eta < 1, 0 < mu < 1 so 1 - eta mu > 0)",
      all(float(Jp.subs({eta: e, x: xv})) > 0 for e in (0.05, 0.5, 0.9) for xv in (1e-3, 0.5, 1.4, 10, 1e3)))
# J' + 2 Y J'' with J'' = (dJ'/dx)/(dY/dx): equals (d(J' s)/dx)/(ds/dx) = eta y'/s', so its sign is the sign of s'.
ghost2 = Jp + 2 * Y * sp.diff(Jp, x) / sp.diff(Y, x)
check("A10 ghost condition 2: J' + 2Y J'' = eta y'(x)/s'(x), positive iff s' > 0 (the same bound as A8)",
      sp.simplify(ghost2 - eta * yprime / (1 - eta * yprime)) == 0)
dJp = sp.simplify(sp.diff(Jp, x))
check("A11 J'' > 0 where s' > 0: dJ'/dx = eta mu'/(1 - eta mu)^2 > 0 and dY/dx = 2 a0^2 s s' > 0",
      sp.simplify(dJp - eta * sp.diff(mu, x) / (1 - eta * mu) ** 2) == 0)
# The scalar channel does NOT switch off at high acceleration: g = g_hat + g_phi with g_hat = eta g_N.
ghat_over_g = eta * y / x  # g_hat/g = eta g_N/g = eta y/x = eta mu
check("A12 high-acceleration channel split: g_hat/g -> eta and g_phi/g -> 1 - eta (not 0); sum = 1",
      sp.limit(ghat_over_g, x, sp.oo) == eta and sp.limit(s / x, x, sp.oo) - (1 - eta) == 0
      and sp.simplify(ghat_over_g + s / x - 1) == 0)
check("A13 total law deep limit is g ~ sqrt(a0 g_N), i.e. y/x^2 -> 1 as x -> 0 (not sqrt(a0 g_hat))",
      sp.limit(y / x ** 2, x, 0) == 1)

# ---------------------------------------------------------------- B. numerics: inversion, fold, comparison
def mu_f(z):
    return z / math.sqrt(1 + z * z)


def X_tot(yv):  # total law: x mu_std(x) = y, solved exactly
    return math.sqrt((yv * yv + yv * math.sqrt(yv * yv + 4)) / 2)


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def total_from_current(ls, yv, scale):
    """Total g/a0 when J' = ls * mu_std(g_phi/(scale a0)): solve ls mu(s/scale) s = eta y."""
    e = ls / (1 + ls)
    sv = bisect(lambda z: ls * mu_f(z / scale) * z - e * yv, 0.0, 10 * yv + 10)
    return e * yv + sv


def total_from_corr(ls, yv):
    """Total g/a0 when J' is the correspondence function: find x with s(x) = s, then J'(s) s = eta y."""
    e = ls / (1 + ls)
    s_of = lambda xv: xv * (1 - e * mu_f(xv))
    jp_of_s = lambda sv: (lambda xv: e * mu_f(xv) / (1 - e * mu_f(xv)))(bisect(lambda xv: s_of(xv) - sv, 0.0, 10 * sv / (1 - e) + 10))
    sv = bisect(lambda z: jp_of_s(z) * z - e * yv, 0.0, 10 * yv + 10, n=120)
    return e * yv + sv


grid = [10 ** (k / 20) for k in range(-60, 61)]
worst = max(abs(total_from_corr(ls, yv) / X_tot(yv) - 1) for ls in (0.5, 1.0, 2.6, 10.0) for yv in grid[::6])
check("B1 consistency of the inversion: the correspondence function returns the total mu_std law", worst < 1e-9,
      f"(max |g/g_tot - 1| = {worst:.1e}, lambda_s = 0.5, 1, 2.6, 10)")
e12 = 12 / 13
check("B2 above the bound the map folds: lambda_s = 12 gives s'(sqrt 2) < 0", 1 - e12 * 4 * math.sqrt(2) / (3 * math.sqrt(3)) < 0)
gaps = {}
for ls in (0.5, 1.0, 2.6):
    vals = [(abs(total_from_current(ls, yv, 1 + ls) / X_tot(yv) - 1), yv) for yv in grid]
    gaps[ls] = max(vals)
detail = ", ".join(f"lambda_s={k}: {v[0]:.3f} at gN/a0={v[1]:.2f}" for k, v in gaps.items())
check("B3 the current function's total law is not mu_std: max |g/g_tot - 1|", gaps[1.0][0] > 0.2, f"({detail})")
g1 = total_from_current(1.0, 1.0, 2.0)
check("B4 at g_N = a0, lambda_s = 1: current 1.564 a0 against the total law's 1.272 a0",
      abs(g1 - 1.5640) < 5e-4 and abs(X_tot(1.0) - 1.2720) < 5e-4, f"({g1:.4f}, {X_tot(1.0):.4f})")
deep_ok = all(abs(total_from_current(ls, 1e-6, 1 + ls) / X_tot(1e-6) - 1) < 0.002 for ls in (0.5, 1.0, 2.6))
check("B5 the a0_tilde scale is right at the deep end (ratio -> 1 at g_N = 1e-6 a0)", deep_ok)
d1 = [(ls, total_from_current(ls, 1e-6, 1.0) / X_tot(1e-6)) for ls in (0.5, 1.0, 2.6)]
check("B6 with a0 in place of a0_tilde (TARGET_D1_SUPPLEMENT section 5) the deep end is low by 1/sqrt(1+lambda_s)",
      all(abs(r * math.sqrt(1 + ls) - 1) < 0.002 for ls, r in d1), "(" + ", ".join(f"{r:.4f}" for _, r in d1) + ")")


def jp_ratio_max(ls):  # correspondence J' against the current J' at the same scalar gradient
    e = ls / (1 + ls)
    out = 0.0
    for xv in grid:
        sv = xv * (1 - e * mu_f(xv))
        out = max(out, abs((e * mu_f(xv) / (1 - e * mu_f(xv))) / (ls * mu_f(sv / (1 + ls))) - 1))
    return out


r01, r1 = jp_ratio_max(0.1), jp_ratio_max(1.0)
check("B7 the two functions agree at both ends and differ between", r1 > r01 > 0.01,
      f"(max |J'_corr/J'_current - 1| = {r01:.3f} at lambda_s = 0.1, {r1:.3f} at lambda_s = 1)")

# ---------------------------------------------------------------- C. the solar-system residual under each function
mp.mp.dps = 60
A0 = mp.mpf("1.1607e-10")
GM = mp.mpf("1.32712440018e20")
bodies = {"Mercury": mp.mpf("5.7909e10"), "Saturn": mp.mpf("1.4335e12")}


def resid_corr(gN):  # the correspondence reproduces the total law exactly: residual = a0 [X(y) - y]
    yv = gN / A0
    return A0 * (mp.sqrt((yv * yv + yv * mp.sqrt(yv * yv + 4)) / 2) - yv)


def resid_current(ls, gN):
    yv, ls = gN / A0, mp.mpf(ls)
    e = ls / (1 + ls)
    f = lambda z: ls * (z / (1 + ls)) / mp.sqrt(1 + (z / (1 + ls)) ** 2) * z - e * yv
    sv = mp.findroot(f, yv / (1 + ls))
    return A0 * (e * yv + sv - yv)


rows = []
for name, r in bodies.items():
    gN = GM / r**2
    base = A0**2 / (2 * gN)
    rc = resid_corr(gN) / base
    ru = [resid_current(ls, gN) / (base * (1 + ls) ** 3) for ls in (0.5, 1.0, 2.6, 10.0)]
    rows.append((name, rc, ru))
# The solution of J'(s) s = eta y under the correspondence function is s(X(y)) (A2), and it is the only one because
# the flux J' s rises monotonically with s (A10). So the total is X(y) for every admissible lambda_s, and lambda_s
# cannot enter the residual. The check measures that residual against a0^2/(2 g_N) at the two bodies.
check("C1 correspondence function: residual = a0^2/(2 g_N), with no lambda_s in it (by A2 and A10)",
      all(abs(rc - 1) < 1e-6 for _, rc, _ in rows), "(" + ", ".join(f"{n} {mp.nstr(rc, 8)}" for n, rc, _ in rows) + ")")
check("C2 current function: residual = (1 + lambda_s)^3 a0^2/(2 g_N), the scaling lambda_s_solar_system_check.py uses",
      all(abs(v - 1) < 1e-6 for _, _, ru in rows for v in ru), "(lambda_s = 0.5, 1, 2.6, 10; Mercury and Saturn)")

# ---------------------------------------------------------------- D. the stealth configuration (agrees with TARGET_D3 section 34)
T, r, th, ph, m, Q0, b, fY0, KB = sp.symbols("T r theta phi m Q_0 b f_Y0 K_B", positive=True)
v = sp.sqrt(2 * m / r)
co = [T, r, th, ph]
gdd = sp.Matrix([[-1 + v**2, v, 0, 0], [v, 1, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * sp.sin(th) ** 2]])
guu = sp.simplify(gdd.inv())
Ad = sp.Matrix([-1, 0, 0, 0])
Au = sp.simplify(guu * Ad)
d_ = sp.Matrix([Q0, 0, 0, 0])  # d_mu = partial_mu phi, phi = Q0 T
du = sp.simplify(guu * d_)
G = [[[sp.simplify(sum(guu[a, k] * (sp.diff(gdd[k, bb], co[c]) + sp.diff(gdd[k, c], co[bb]) - sp.diff(gdd[bb, c], co[k]))
                       for k in range(4)) / 2) for c in range(4)] for bb in range(4)] for a in range(4)]
nabA = [[sp.simplify(sp.diff(Au[a], co[c]) + sum(G[a][c][k] * Au[k] for k in range(4))) for c in range(4)] for a in range(4)]
Jv = [sp.simplify(sum(Au[c] * nabA[a][c] for c in range(4))) for a in range(4)]
Fm = sp.Matrix(4, 4, lambda i, j: sp.diff(Ad[j], co[i]) - sp.diff(Ad[i], co[j]))
check("D1 A.A = -1, F = 0, J^mu = 0, q^{mu nu} d_nu phi = 0 (Y = 0), Q = Q0",
      sp.simplify((Ad.T * Au)[0]) == -1 and Fm == sp.zeros(4, 4) and all(j == 0 for j in Jv)
      and sp.simplify((guu + Au * Au.T) * d_) == sp.zeros(4, 1) and sp.simplify((Au.T * d_)[0] - Q0) == 0)
Theta = sp.simplify(sum(nabA[a][a] for a in range(4)))
check("D2 expansion Theta = -(3/(2r)) sqrt(2m/r)", sp.simplify(Theta + sp.Rational(3, 2) / r * v) == 0)
lam_r = b * Q0 * Theta + (b + fY0) * Q0**2
# vector equation (half the A^mu variation; F = 0 and F_Q = 0 here):
# b[d_a nabla_mu A^a - nabla_n(A^n d_mu)] - (b + F_Y) Q d_mu - (1/2) F_Q d_mu - lambda A_mu = 0
def div_Ad(mu_i):
    return (sum(sp.diff(Au[n] * d_[mu_i], co[n]) for n in range(4))
            + sum(G[n][n][k] * Au[k] * d_[mu_i] for n in range(4) for k in range(4))
            - sum(G[k][n][mu_i] * Au[n] * d_[k] for n in range(4) for k in range(4)))


vec = [sp.simplify(b * (sum(d_[a] * nabA[a][mi] for a in range(4)) - div_Ad(mi)) - (b + fY0) * Q0 * d_[mi] - lam_r * Ad[mi])
       for mi in range(4)]
check("D3 the vector equation holds with lambda(r) = b Q0 Theta + (b + f_Y0) Q0^2", all(e == 0 for e in vec))
# metric source (A^mu held fixed): U = (1/2) g L + (b + F_Y) d d - lambda A A + b nabla(d A A) - 2b nabla(A A^(mu d^nu))
def div3(Tt):  # nabla_rho T^{rho mu nu}
    return [[sp.simplify(sum(sp.diff(Tt[p][i][j], co[p]) for p in range(4))
                         + sum(G[p][p][k] * Tt[k][i][j] for p in range(4) for k in range(4))
                         + sum(G[i][p][k] * Tt[p][k][j] for p in range(4) for k in range(4))
                         + sum(G[j][p][k] * Tt[p][i][k] for p in range(4) for k in range(4)))
             for j in range(4)] for i in range(4)]


T1 = [[[du[p] * Au[i] * Au[j] for j in range(4)] for i in range(4)] for p in range(4)]
T2 = [[[Au[p] * (Au[i] * du[j] + Au[j] * du[i]) / 2 for j in range(4)] for i in range(4)] for p in range(4)]
D1_, D2_ = div3(T1), div3(T2)
L_extra = 0  # -F(0, Q0) = 0, J.d = 0, Y = 0, A.A + 1 = 0 on the configuration
U = [[sp.simplify(guu[i, j] * L_extra / 2 + (b + fY0) * du[i] * du[j] - lam_r * Au[i] * Au[j] + b * D1_[i][j] - 2 * b * D2_[i][j])
      for j in range(4)] for i in range(4)]
check("D4 the extra-field metric source vanishes with that lambda", all(U[i][j] == 0 for i in range(4) for j in range(4)))


def ricci(a_, b_):
    return sp.simplify(sum(sp.diff(G[c][a_][b_], co[c]) - sp.diff(G[c][a_][c], co[b_])
                           + sum(G[c][c][k] * G[k][a_][b_] - G[c][b_][k] * G[k][a_][c] for k in range(4)) for c in range(4)))


check("D5 Ricci = 0: Painleve-Gullstrand Schwarzschild, so G_mu_nu = 0 closes the metric equation",
      all(ricci(i, j) == 0 for i in range(4) for j in range(i, 4)))

print("\nALL PASS" if ok_all else "\nSOME FAIL")
sys.exit(0 if ok_all else 1)
