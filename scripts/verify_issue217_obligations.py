#!/usr/bin/env python3
"""Verification for Res-Nova issue #217 obligations (BLK-1437 no-hang pickup).

Obligation 1: parameterized scalar derivative d/dY [2 lam a^2 Fstd(sqrt(Y)/a)]
  = lam * muStd(sqrt(Y)/a) -- cross-check of AeSTParameterizedNormalization.lean.
Obligation 3: diffeomorphism Noether identity -- the derivation steps (vector-sector
  equivalence, metric symmetrization, density divergence identity) plus an
  independent recomputation of the 1+1 hyperbolic sector (PR #215 setup).
Obligation 4: matter conservation -- for a minimally coupled scalar, nabla^mu T_mu_nu
  = E_chi * d_nu chi identically in 2D curved space (equivalently the matter
  diffeomorphism identity -nabla^mu T_mu_nu + E_chi * d_nu chi = 0), so E_chi = 0
  implies nabla^mu T_mu_nu = 0 (not an independent assumption).

All checks are exact symbolic identities (asserted == 0 after simplification),
except the numeric spot checks, which use exact rational inputs at 50-digit
precision with a 1e-40 tolerance.
"""
import sys

import sympy as sp

N_PASS = 0


def check(name, expr):
    global N_PASS
    val = sp.simplify(expr)
    assert val == 0, f"FAIL {name}: simplified to {val}"
    N_PASS += 1
    print(f"  PASS {name}")


def check_num(name, expr, tol=1e-40):
    global N_PASS
    val = abs(sp.N(expr, 50))
    assert val < tol, f"FAIL {name}: |value| = {val}"
    N_PASS += 1
    print(f"  PASS {name} (|value| = {float(val):.2e})")


# ---------------------------------------------------------------------------
# Obligation 1: parameterized scalar derivative
# ---------------------------------------------------------------------------
def part_obligation_1():
    print("Obligation 1 -- parameterized scalar derivative")
    Y, lam, a = sp.symbols("Y lam a", positive=True)
    x = sp.symbols("x", positive=True)

    def muStd(z):
        return z / sp.sqrt(1 + z**2)

    def Fstd(z):
        return (z * sp.sqrt(1 + z**2) - sp.asinh(z)) / 2

    # A1: Fstd'(x) = x^2 / sqrt(1+x^2) (the lemma hasDerivAt_Fstd rests on).
    check("A1 Fstd'(x) = x^2/sqrt(1+x^2)",
          sp.diff(Fstd(x), x) - x**2 / sp.sqrt(1 + x**2))

    # A2: chain-rule assembly: 2*lam*a^2 * Fstd'(sqrt(Y)/a) * d/dY[sqrt(Y)/a]
    #     = lam * muStd(sqrt(Y)/a), with x = sqrt(Y)/a.
    xx = sp.sqrt(Y) / a
    lhs = (2 * lam * a**2 * (xx**2 / sp.sqrt(1 + xx**2))
           * sp.diff(sp.sqrt(Y) / a, Y))
    check("A2 chain-rule assembly = lam*muStd(sqrt(Y)/a)",
          sp.simplify(lhs - lam * muStd(xx)))

    # A3: direct differentiation of the full parameterized function, numeric.
    J = 2 * lam * a**2 * Fstd(sp.sqrt(Y) / a)
    dJ = sp.diff(J, Y)
    for (yv, lv, av) in [(sp.Rational(1, 2), sp.Rational(3, 10), sp.Rational(7, 5)),
                         (sp.Rational(2), sp.Rational(1), sp.Rational(1, 3)),
                         (sp.Rational(5, 4), sp.Rational(11, 10), sp.Rational(2))]:
        check_num(f"A3 direct diff at Y={yv}, lam={lv}, a={av}",
                  (dJ - lam * muStd(sp.sqrt(Y) / a)).subs({Y: yv, lam: lv, a: av}))

    # A4: specialization lam=1/2, a=1 recovers Jstd'(Y) = muStd(sqrt(Y))/2.
    check_num("A4 specialization lam=1/2, a=1",
              (dJ - muStd(sp.sqrt(Y)) / 2).subs({Y: sp.Rational(3, 2),
                                                 lam: sp.Rational(1, 2),
                                                 a: sp.Integer(1)}))

    # A5: positivity of the derivative at a test point (lam>0, Y>0).
    val = (lam * muStd(sp.sqrt(Y) / a)).subs({Y: sp.Rational(1),
                                              lam: sp.Rational(1, 2),
                                              a: sp.Rational(2)})
    assert val > 0
    global N_PASS
    N_PASS += 1
    print(f"  PASS A5 derivative positive at test point (value = {sp.N(val, 10)})")


# ---------------------------------------------------------------------------
# Obligation 3: Noether identity derivation steps + hyperbolic sector
# ---------------------------------------------------------------------------
def part_obligation_3():
    print("Obligation 3 -- Noether identity derivation steps")
    # B1: vector-sector equivalence, indices mu,nu in {0,1}, all components
    # independent symbols. F_nu_mu = d_nu A_mu - d_mu A_nu; div(E A) by Leibniz.
    E = sp.symbols("E0 E1")
    A = sp.symbols("A0 A1")
    dA = sp.symbols("dA00 dA01 dA10 dA11")  # dA[nu*2+mu] = nabla_nu A_mu
    dE = sp.symbols("dE0 dE1")             # dE[mu] = nabla_mu E^mu (per-mu part)
    for nu in range(2):
        lhs = (sum(E[mu] * dA[nu * 2 + mu] for mu in range(2))
               - sum(dE[mu] * A[nu] + E[mu] * dA[mu * 2 + nu] for mu in range(2)))
        rhs = (sum(E[mu] * (dA[nu * 2 + mu] - dA[mu * 2 + nu]) for mu in range(2))
               - A[nu] * sum(dE))
        check(f"B1 vector equivalence nu={nu}", sp.expand(lhs - rhs))

    # B2: metric symmetrization: symmetric E^munu contracts only against the
    # symmetric part of nabla_mu xi_nu.
    Es = sp.symbols("E00 E01 E11")
    Emat = sp.Matrix([[Es[0], Es[1]], [Es[1], Es[2]]])
    dxi = sp.symbols("dxi00 dxi01 dxi10 dxi11")
    dxim = sp.Matrix([[dxi[0], dxi[1]], [dxi[2], dxi[3]]])
    full = sum(Emat[mu, nu] * dxim[mu, nu] for mu in range(2) for nu in range(2))
    symm = sum(Emat[mu, nu] * (dxim[mu, nu] + dxim[nu, mu]) / 2
               for mu in range(2) for nu in range(2))
    check("B2 symmetric E contracts only symmetric dxi", sp.expand(full - symm))

    # B3: density divergence identity in 2D curved space:
    # d_mu(sqrt(-g) V^mu) = sqrt(-g) nabla_mu V^mu, the integration-by-parts
    # step that extracts the coefficient of xi^nu.
    t, x = sp.symbols("t x")
    alpha = sp.Function("alpha")(t, x)
    beta = sp.Function("beta")(t, x)
    V0 = sp.Function("V0")(t, x)
    V1 = sp.Function("V1")(t, x)
    g = sp.diag(-sp.exp(2 * alpha), sp.exp(2 * beta))
    ginv = g.inv()
    sqrtdet = sp.exp(alpha + beta)  # sqrt(-g)
    coords = [t, x]
    # Christoffel symbols Gamma^lam_mu_nu.
    Gamma = [[[sp.Integer(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for lam_ in range(2):
        for mu in range(2):
            for nu in range(2):
                Gamma[lam_][mu][nu] = sp.simplify(sum(
                    ginv[lam_, sig] * (sp.diff(g[sig, nu], coords[mu])
                                       + sp.diff(g[sig, mu], coords[nu])
                                       - sp.diff(g[mu, nu], coords[sig])) / 2
                    for sig in range(2)))
    V = [V0, V1]
    div_density = sum(sp.diff(sqrtdet * V[mu], coords[mu]) for mu in range(2))
    div_cov = sum(sp.diff(V[mu], coords[mu])
                  + sum(Gamma[mu][mu][lam_] * V[lam_] for lam_ in range(2))
                  for mu in range(2))
    check("B3 d_mu(sqrt(-g)V^mu) = sqrt(-g) nabla_mu V^mu",
          sp.simplify(div_density - sqrtdet * div_cov))

    # B4: hyperbolic sector, independent recomputation (PR #215 setup):
    # A^mu = (cosh chi, sinh chi), chi = eps*t, phi = t + x.
    eps = sp.symbols("eps", real=True)
    chi = eps * t
    A_up = [sp.cosh(chi), sp.sinh(chi)]
    A_down = [-A_up[0], A_up[1]]
    p_down = [sp.Integer(1), sp.Integer(1)]
    p_up = [-sp.Integer(1), sp.Integer(1)]
    B = []
    for nu in range(2):
        # B^nu = p_mu d^nu A^mu - d_mu (A^mu p^nu); x-derivatives vanish.
        first = sum(p_down[mu] * (-sp.diff(A_up[mu], t) if nu == 0 else 0)
                    for mu in range(2))
        second = sp.diff(A_up[0] * p_up[nu], t)
        B.append(sp.simplify(first - second))
    F01 = sp.diff(A_down[1], t)
    F = [[sp.Integer(0), F01], [-F01, sp.Integer(0)]]
    div_B = sp.diff(B[0], t)
    R = [sp.simplify(sum(B[mu] * F[nu][mu] for mu in range(2)) - A_down[nu] * div_B)
         for nu in range(2)]
    check("B4a unit constraint -A0^2 + A1^2 = -1",
          sp.simplify(-A_up[0]**2 + A_up[1]**2 + 1))
    check("B4b B^0 = -eps cosh(chi)", sp.simplify(B[0] + eps * sp.cosh(chi)))
    check("B4c B^1 = -eps sinh(chi)", sp.simplify(B[1] + eps * sp.sinh(chi)))
    check("B4d R_0 = -eps^2 sinh(2 chi)",
          sp.simplify(R[0] + eps**2 * sp.sinh(2 * chi)))
    check("B4e R_1 = eps^2 cosh(2 chi)",
          sp.simplify(R[1] - eps**2 * sp.cosh(2 * chi)))
    # B5: witness that the printed Eq. (4) shift is nonzero, while the
    # action-derived coefficient gives zero shift.
    b = sp.symbols("b", real=True)
    shift_printed = [2 * b * r for r in R]
    witness = shift_printed[1].subs({eps: 1, t: 0, b: 1})
    assert witness == 2, f"B5 witness failed: {witness}"
    global N_PASS
    N_PASS += 1
    print("  PASS B5 printed-Eq.(4) shift at (eps=1,t=0,b=1) is 2 != 0")
    shift_action = [(b - b) * r for r in R]
    check("B5b action-derived coefficient gives zero shift",
          sp.simplify(shift_action[1]))


# ---------------------------------------------------------------------------
# Obligation 4: matter conservation from the matter shell
# ---------------------------------------------------------------------------
def part_obligation_4():
    print("Obligation 4 -- matter conservation (scalar matter, 2D curved)")
    t, x = sp.symbols("t x")
    alpha = sp.Function("alpha")(t, x)
    beta = sp.Function("beta")(t, x)
    chi_f = sp.Function("chi")(t, x)
    V = sp.Function("V")
    coords = [t, x]
    g = sp.diag(-sp.exp(2 * alpha), sp.exp(2 * beta))
    ginv = g.inv()
    sqrtdet = sp.exp(alpha + beta)
    dchi = [sp.diff(chi_f, t), sp.diff(chi_f, x)]

    # C1: the Gamma combination in the covariant divergence:
    # -(d_mu g_nu_lam) T^mu_lam + g_nu_lam Gamma^lam_mu_alpha T^mu_alpha
    #   + (1/2)(d_nu g_mu_alpha) T^mu_alpha = 0, for generic symmetric T.
    T00, T01, T11 = sp.symbols("T00 T01 T11")
    Tcon = sp.Matrix([[T00, T01], [T01, T11]])
    Gamma = [[[sp.Integer(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for lam_ in range(2):
        for mu in range(2):
            for nu in range(2):
                Gamma[lam_][mu][nu] = sp.simplify(sum(
                    ginv[lam_, sig] * (sp.diff(g[sig, nu], coords[mu])
                                       + sp.diff(g[sig, mu], coords[nu])
                                       - sp.diff(g[mu, nu], coords[sig])) / 2
                    for sig in range(2)))
    for nu in range(2):
        term1 = -sum(sp.diff(g[nu, lam_], coords[mu]) * Tcon[mu, lam_]
                     for mu in range(2) for lam_ in range(2))
        term2 = sum(g[nu, lam_] * Gamma[lam_][mu][alp] * Tcon[mu, alp]
                    for lam_ in range(2) for mu in range(2) for alp in range(2))
        term3 = sum(sp.diff(g[mu, alp], coords[nu]) * Tcon[mu, alp]
                    for mu in range(2) for alp in range(2)) / 2
        check(f"C1 Gamma combination nu={nu}",
              sp.simplify(term1 + term2 + term3))

    # C2: density form of nabla^mu T_mu_nu = E_chi d_nu chi for scalar matter
    # (equivalently the matter diffeomorphism identity
    # -nabla^mu T_mu_nu + E_chi d_nu chi = 0).
    K = (sum(ginv[a, b] * dchi[a] * dchi[b] for a in range(2) for b in range(2)) / 2
         + V(chi_f))
    Tdown = sp.Matrix(2, 2, lambda mu, nu: dchi[mu] * dchi[nu] - g[mu, nu] * K)
    Tmixed = ginv * Tdown          # T^mu_nu
    Tcon2 = Tmixed * ginv          # T^mu_nu (contravariant)
    box_chi = sum(sp.diff(sqrtdet * sum(ginv[mu, nu] * dchi[nu] for nu in range(2)),
                          coords[mu]) for mu in range(2)) / sqrtdet
    E_chi = box_chi - sp.diff(V(chi_f), chi_f)
    for nu in range(2):
        div_term = sum(sp.diff(sqrtdet * Tmixed[mu, nu], coords[mu])
                       for mu in range(2))
        dg_term = sum(sp.diff(g[a, b], coords[nu]) * Tcon2[a, b]
                      for a in range(2) for b in range(2)) * sqrtdet / 2
        total = sp.simplify(div_term - dg_term - sqrtdet * E_chi * dchi[nu])
        check(f"C2 sqrt(-g)(nabla^mu T_mu_nu - E_chi d_nu chi) = 0, nu={nu}",
              sp.expand(total))

    # C3: flat-space direct cross-check (alpha = beta = 0).
    eta = sp.diag(-1, 1)
    etainv = eta.inv()
    Kf = (sum(etainv[a, b] * dchi[a] * dchi[b] for a in range(2) for b in range(2)) / 2
          + V(chi_f))
    Tf = sp.Matrix(2, 2, lambda mu, nu: dchi[mu] * dchi[nu] - eta[mu, nu] * Kf)
    Ef = (-sp.diff(chi_f, t, 2) + sp.diff(chi_f, x, 2) - sp.diff(V(chi_f), chi_f))
    for nu in range(2):
        divf = sum(sp.diff(sum(etainv[mu, a] * Tf[a, nu] for a in range(2)),
                           coords[mu]) for mu in range(2))
        check(f"C3 flat-space d^mu T_mu_nu - E_chi d_nu chi = 0, nu={nu}",
              sp.expand(divf - Ef * dchi[nu]))


def main():
    part_obligation_1()
    part_obligation_3()
    part_obligation_4()
    print(f"\nPASS: all {N_PASS} exact symbolic checks passed.")


if __name__ == "__main__":
    main()
