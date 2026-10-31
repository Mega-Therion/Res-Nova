#!/usr/bin/env python3
"""
Q3 Algebraic-Elimination No-Go Audit:
Decides whether F_std(x) = (1/2)[x*sqrt(1+x^2) - arsinh(x)] can appear on-shell
by algebraically eliminating a finite set of auxiliary fields and Lagrange
multipliers from a classical polynomial action.

Citations verified on disk (read-only):
- /home/mega/Chyren/3_research/Res-Nova/TARGET_D2_PHYSICAL_ACTION_DERIVATION.md
  line 74: F_std(x) = (1/2)[x*sqrt(1+x^2) - arsinh(x)]
- /home/mega/Chyren/3_research/Res-Nova/TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md
  lines 51-62, 87-89, 127
- /home/mega/Chyren/3_research/Res-Nova/TARGET_D7_COVARIANT_COMPLETION.md
  lines 38-48, 84-108 (covariant AeST projector q_munu = g_munu + A_mu A_nu,
  invariant Y = q^{mu nu} nabla_mu phi nabla_nu phi, and factor-of-2 convention)
- /home/mega/Chyren/3_research/Res-Nova/05_lean_formalization/SZStdEmbedding.lean
  lines 41-48, 52-76: muStd(x) = x/sqrt(1+x^2), Fstd(x) = (x*sqrt(1+x^2)-arsinh(x))/2,
  Jstd(Y) = Fstd(sqrt(Y)), Jstd'(Y) = muStd(sqrt(Y))/2
"""

import json
import pathlib
import sys
import sympy as sp


def main() -> int:
    # =========================================================================
    # 1. STATE THE POLYNOMIAL ACTION CLASS C_poly AND TARGET FUNCTION F_std
    # =========================================================================
    class_definition = {
        "name": "C_poly (classical polynomial auxiliary-field action class)",
        "fields": [
            "g_{mu nu}",
            "A^mu",
            "U^mu",
            "phi",
            "chi_1, ..., chi_N (finite set of auxiliary scalars or tensors)",
            "lambda_1, ..., lambda_M (Lagrange multipliers for polynomial constraints)",
        ],
        "allowed_lagrangian_operations": (
            "Polynomials over C in the fields, their first derivatives, and "
            "Lagrange multipliers enforcing polynomial constraints (unit timelike "
            "g_{mu nu} U^mu U^nu + 1 = 0, linear locks, quadratic normalizations)."
        ),
        "forbidden_lagrangian_primitives": [
            "arsinh",
            "artanh",
            "ln",
            "exp",
            "non-integer fractional powers in L",
        ],
        "allowed_onshell_elimination_outputs": (
            "Algebraic branches (including radicals) solving polynomial stationary "
            "and constraint equations; transcendental logarithms are not inserted."
        ),
    }

    x = sp.Symbol("x", positive=True, real=True)
    Y = sp.Symbol("Y", positive=True, real=True)

    # Cited target kinetic function (TARGET_D2:74, SZStdEmbedding.lean:44):
    arsinh_log = sp.log(x + sp.sqrt(1 + x**2))
    F_std = sp.Rational(1, 2) * (x * sp.sqrt(1 + x**2) - sp.asinh(x))
    mu_std = x / sp.sqrt(1 + x**2)

    # Verify arsinh(x) == ln(x + sqrt(1+x^2)) for x > 0 via derivative + x->0 value
    diff_arsinh_log = sp.simplify(sp.diff(sp.asinh(x) - arsinh_log, x))
    val0_arsinh_log = (sp.asinh(x) - arsinh_log).subs(x, 0)
    assert diff_arsinh_log == 0 and val0_arsinh_log == 0

    # Verify F_std'(x)/x == mu_std(x) and factor-of-2 Y-convention (SZStdEmbedding.lean:75)
    assert sp.simplify(sp.diff(F_std, x) / x - mu_std) == 0
    J_std_Y = F_std.subs(x, sp.sqrt(Y))
    assert sp.simplify(2 * sp.diff(J_std_Y, Y) - mu_std.subs(x, sp.sqrt(Y))) == 0
    F_kin_std_Y = 2 * J_std_Y  # = sqrt(Y*(1+Y)) - asinh(sqrt(Y)), dF_kin_std/dY = mu_std(sqrt(Y))
    assert sp.simplify(sp.diff(F_kin_std_Y, Y) - mu_std.subs(x, sp.sqrt(Y))) == 0

    # Confirm stationary rewrite sigma = sqrt(Y/(1+Y)), int Y d(sigma) = artanh(sigma) - sigma
    # is NOT a polynomial elimination (uses artanh and presupposes sigma = mu_std):
    sigma = sp.Symbol("sigma", positive=True, real=True)
    legendre_rewrite = sp.integrate(sigma**2 / (1 - sigma**2), sigma)
    assert sp.simplify(sp.diff(legendre_rewrite - (sp.atanh(sigma) - sigma), sigma)) == 0

    # =========================================================================
    # 2. ELIMINATE AUXILIARIES WITH SYMPY: EXACT CHARACTERIZATION OF C_poly
    # =========================================================================
    # For any polynomial Lagrangian L(Y, chi_1, ..., chi_K) in K[Y, chi_1, ..., chi_K]
    # (grouping auxiliary fields and Lagrange multipliers together as chi),
    # the stationary/constraint system is dL/d(chi_a) = 0 (a = 1..K), and the
    # on-shell kinetic function W(Y) satisfies W - L(Y, chi) = 0.
    #
    # By algebraic Sard's theorem in characteristic 0, on each of the finitely many
    # irreducible components Z_i of V_crit = {nabla_chi L_Y = 0} over bar(C(Y)),
    # d(L_Y|_{Z_i}) = sum_a (dL/dchi_a) dchi_a = 0, so L_Y takes a single constant
    # value w_i in bar(C(Y)) on Z_i (even if Z_i has flat/gauge directions).
    # Hence EVERY on-shell branch W(Y) satisfies a non-zero polynomial equation
    # P(Y, W(Y)) = 0 with P in C[Y, W] \ {0}.
    Y_sym, W_sym = sp.symbols("Y_sym W_sym")
    chi1, chi2, lam1, lam2 = sp.symbols("chi1 chi2 lam1 lam2")
    c0, b1, m2 = sp.symbols("c0 b1 m2", nonzero=True)

    # 2A. Unconstrained quadratic auxiliary -> rational/polynomial W(Y)
    L_quad = c0 * Y_sym + b1 * Y_sym * chi1 - sp.Rational(1, 2) * m2 * chi1**2
    gb_quad = sp.groebner(
        [W_sym - L_quad, sp.diff(L_quad, chi1)],
        chi1,
        W_sym,
        order="lex",
    )
    poly_quad_YW = gb_quad[-1]
    assert chi1 not in poly_quad_YW.free_symbols
    W_quad_sol = sp.solve(poly_quad_YW, W_sym)[0]
    assert sp.simplify(W_quad_sol - (c0 * Y_sym + b1**2 * Y_sym**2 / (2 * m2))) == 0

    # 2B. Polynomial normalization constraint -> radical W(Y) = sqrt(1 + Y) - 1
    L_rad1 = (chi1 - 1) + lam1 * (chi1**2 - (1 + Y_sym))
    gb_rad1 = sp.groebner(
        [W_sym - L_rad1, sp.diff(L_rad1, chi1), sp.diff(L_rad1, lam1)],
        lam1,
        chi1,
        W_sym,
        order="lex",
    )
    poly_rad1_YW = gb_rad1[-1]  # W^2 + 2*W - Y = 0
    assert sp.expand(poly_rad1_YW - (W_sym**2 + 2 * W_sym - Y_sym)) == 0
    assert sp.simplify(poly_rad1_YW.subs({Y_sym: Y, W_sym: sp.sqrt(1 + Y) - 1})) == 0

    # 2C. Coupled polynomial auxiliaries -> algebraic piece A_alg(sqrt(Y)) = (1/2)*sqrt(Y*(1+Y))
    L_alg_part = (
        sp.Rational(1, 2) * chi2
        + lam1 * (chi1**2 - (1 + Y_sym))
        + lam2 * (chi2**2 - Y_sym * chi1**2)
    )
    gb_alg_part = sp.groebner(
        [
            W_sym - L_alg_part,
            sp.diff(L_alg_part, chi1),
            sp.diff(L_alg_part, chi2),
            sp.diff(L_alg_part, lam1),
            sp.diff(L_alg_part, lam2),
        ],
        lam1,
        lam2,
        chi1,
        chi2,
        W_sym,
        order="lex",
    )
    poly_alg_part_YW = gb_alg_part[-1]  # W^2 - Y*(Y + 1)/4 = 0
    assert sp.expand(4 * poly_alg_part_YW - (4 * W_sym**2 - Y_sym * (1 + Y_sym))) == 0
    A_alg_Y = sp.Rational(1, 2) * sp.sqrt(Y * (1 + Y))
    assert sp.simplify(poly_alg_part_YW.subs({Y_sym: Y, W_sym: A_alg_Y})) == 0

    # 2D. Converse realization: ANY separable algebraic function P(Y, W) = 0 is realized
    # on-shell by the 2-auxiliary polynomial Lagrangian L_P(Y, chi1, lam1) = chi1 + lam1*P(Y, chi1),
    # with variational consistency dW/dY == (dL_P/dY)|_{on-shell}.
    p1_sym, p0_sym = sp.symbols("p1_sym p0_sym")
    P_cubic = chi1**3 + (1 + Y_sym) * p1_sym * chi1 + Y_sym * p0_sym
    L_universal = chi1 + lam1 * P_cubic
    gb_universal = sp.groebner(
        [
            W_sym - L_universal,
            sp.diff(L_universal, chi1),
            sp.diff(L_universal, lam1),
        ],
        lam1,
        chi1,
        W_sym,
        order="lex",
    )
    poly_universal_YW = gb_universal[-1]
    assert sp.expand(poly_universal_YW - P_cubic.subs(chi1, W_sym)) == 0
    lam1_onshell = sp.solve(sp.diff(L_universal, chi1), lam1)[0]
    dLP_dY_onshell = sp.diff(L_universal, Y_sym).subs(lam1, lam1_onshell)
    dW_dY_implicit = -sp.diff(P_cubic, Y_sym) / sp.diff(P_cubic, chi1)
    assert sp.simplify(dLP_dY_onshell - dW_dY_implicit) == 0

    general_onshell_class_str = (
        "W(Y) in AlgebraicClosure(C(Y)): all functions W(Y) satisfying a non-zero "
        "polynomial relation P(Y, W(Y)) = sum_{k=0}^d p_k(Y) W(Y)^k = 0 with "
        "p_k(Y) in C[Y], p_d(Y) != 0, d >= 1."
    )

    # =========================================================================
    # 3. REQUIRED CHECK: SUBTRACT ALGEBRAIC CLASS FROM F_std & PROVE OBSTRUCTION
    # =========================================================================
    # Subtract the algebraic piece A_alg(x) = (1/2)*x*sqrt(1+x^2) (root of 4*A^2 - x^2*(1+x^2) = 0,
    # already realized inside C_poly by Template 2C) from F_std(x):
    A_alg_x = sp.Rational(1, 2) * x * sp.sqrt(1 + x**2)
    assert sp.simplify(4 * A_alg_x**2 - x**2 * (1 + x**2)) == 0

    F_remainder = sp.simplify(F_std - A_alg_x)
    assert sp.simplify(F_remainder + sp.Rational(1, 2) * sp.asinh(x)) == 0

    # Since AlgebraicClosure(C(Y)) == AlgebraicClosure(C(x)) (as x^2 - Y = 0 is algebraic)
    # and algebraic functions form a field, F_std(sqrt(Y)) is algebraic over C(Y)
    # if and only if w(x) = arsinh(x) is algebraic over C(x).
    #
    # We prove w(x) = arsinh(x) is NOT algebraic over C(x) via three exact SymPy checks:

    # --- Obstruction 3A: Power-series recurrence + Eisenstein's theorem (1852) ---
    # w(x) = arsinh(x) has derivative w'(x) = (1 + x^2)^(-1/2), so (1 + x^2)*w''(x) + x*w'(x) = 0.
    w_expr = sp.asinh(x)
    ode_residual = sp.simplify((1 + x**2) * sp.diff(w_expr, x, 2) + x * sp.diff(w_expr, x))
    assert ode_residual == 0

    # Substituting w(x) = sum_{n>=0} c_{2n+1} x^{2n+1} yields the exact recurrence:
    #   (2n + 1)*(2n)*c_{2n+1} + (2n - 1)^2 * c_{2n-1} = 0
    #   => c_{2n+1} = -((2n - 1)^2 / (2n*(2n + 1))) * c_{2n-1},  c_1 = 1
    #   => c_{2n+1} = (-1)^n * binomial(2n, n) / (4^n * (2n + 1)).
    n_int = sp.Symbol("n", integer=True, nonnegative=True)
    rec_ratio = -((2 * n_int - 1) ** 2) / (2 * n_int * (2 * n_int + 1))

    # Verify closed-form & recurrence coefficients against SymPy Maclaurin series up to x^55:
    series_asinh = sp.series(sp.asinh(x), x, 0, 56).removeO()
    series_A_alg = sp.series(A_alg_x, x, 0, 56).removeO()

    odd_primes_tested = []
    asinh_denom_primes = set()
    alg_denom_primes = set()

    c_prev = sp.Rational(1, 1)
    for n_val in range(0, 27):
        deg = 2 * n_val + 1
        c_series = sp.Rational(series_asinh.coeff(x, deg))
        c_closed = (
            ((-1) ** n_val)
            * sp.binomial(2 * n_val, n_val)
            / (sp.Integer(4) ** n_val * (2 * n_val + 1))
        )
        assert c_series == c_closed
        if n_val >= 1:
            c_rec = c_prev * rec_ratio.subs(n_int, n_val)
            assert c_rec == c_series
        c_prev = c_series

        for p_fac in sp.primefactors(c_series.q):
            asinh_denom_primes.add(int(p_fac))

        # Check A_alg(x) denominator primes for comparison (Eisenstein bound B = 4 -> only prime 2)
        c_alg = sp.Rational(series_A_alg.coeff(x, deg))
        for p_fac in sp.primefactors(c_alg.q):
            alg_denom_primes.add(int(p_fac))

        # For every odd prime p = 2*n + 1: p > n implies p does not divide (2n)!,
        # so gcd(binomial(p-1, (p-1)/2), p) = 1, hence p divides the reduced denominator of c_p!
        if deg >= 3 and sp.isprime(deg):
            p_prime = deg
            binom_num = int(sp.binomial(p_prime - 1, (p_prime - 1) // 2))
            assert sp.igcd(binom_num, p_prime) == 1
            assert c_series.q % p_prime == 0
            assert (c_series.q // p_prime) % p_prime != 0  # exact p-adic valuation v_p(c_p) = -1
            odd_primes_tested.append(
                {
                    "p": p_prime,
                    "c_p": str(c_series),
                    "denom": int(c_series.q),
                    "p_divides_reduced_denom": True,
                }
            )

    # Eisenstein's theorem: if sum c_k x^k in Q[[x]] is algebraic over C(x) (hence over Q(x)),
    # there exists B >= 1 such that B^k c_k in Z for all k >= 1, so ONLY primes dividing B
    # (finitely many primes) can divide denom(c_k).
    # Confirm A_alg(x) has ONLY prime {2} in denominators, whereas arsinh(x) injects EVERY odd prime p!
    assert alg_denom_primes <= {2}
    assert len(odd_primes_tested) == 15  # all odd primes from 3 to 53

    # --- Obstruction 3B: Branch-cut period at x = +-i & simple-pole residue at x = infinity ---
    # 1. Derivative dw/dx = 1/sqrt(1 + x^2) has square-root branch points at x = +i and x = -i.
    #    Integrating around the closed loop gamma encircling [-i, +i] (2 * int_{-i}^{+i} dx/sqrt(1+x^2),
    #    parametrized by x = i*s, s in [-1, 1]) yields non-zero period 2*pi*i:
    s_param = sp.Symbol("s", real=True)
    branch_cut_period = sp.simplify(
        2 * sp.I * sp.integrate(1 / sp.sqrt(1 - s_param**2), (s_param, -1, 1))
    )
    assert branch_cut_period == 2 * sp.pi * sp.I
    # Analytic continuation along gamma^k shifts w(x) -> w(x) + 2*pi*i*k for all k in Z
    # (infinitely many sheets), whereas any root of degree-d P(x, w) = 0 has <= d < infinity sheets.

    # 2. At x = infinity (local coordinate u = 1/x -> 0+), any algebraic function w in bar(C(x))
    #    has a Puiseux series w = sum_{m >= m0} alpha_m u^{m/e} (e >= 1) with NO log(u) term and
    #    ZERO u^(-1) residue in dw/du = sum_{m != 0} (m/e)*alpha_m u^{m/e - 1}.
    #    For w(x) = arsinh(1/u), dw/du = -1 / (u * sqrt(1 + u^2)) has simple-pole residue -1 != 0:
    u_inf = sp.Symbol("u", positive=True, real=True)
    dw_du = sp.simplify(sp.diff(sp.asinh(1 / u_inf), u_inf))
    assert sp.simplify(dw_du + 1 / (u_inf * sp.sqrt(1 + u_inf**2))) == 0
    u_complex = sp.Symbol("u_c")
    res_at_infinity = sp.residue(-1 / (u_complex * sp.sqrt(1 + u_complex**2)), u_complex, 0)
    assert res_at_infinity == -1

    # Correspondingly, the asymptotic expansion of F_std(x) at x -> +infinity contains -1/2 * ln(2x):
    F_std_u = F_std.rewrite(sp.log).subs(x, 1 / u_inf)
    F_std_asymp_u = sp.series(F_std_u, u_inf, 0, 4).removeO()
    F_std_asymp_x = sp.expand(F_std_asymp_u.subs(u_inf, 1 / x), force=True)
    expected_asymp_x = (
        sp.Rational(1, 2) * x**2
        + sp.Rational(1, 4)
        - sp.Rational(1, 2) * sp.log(2)
        - sp.Rational(1, 2) * sp.log(x)
        - sp.Rational(3, 16) / x**2
    )
    assert sp.simplify(F_std_asymp_x - expected_asymp_x) == 0
    assert F_std_asymp_x.coeff(sp.log(x)) == -sp.Rational(1, 2)

    # --- Obstruction 3C: Liouville minimal-polynomial proof on rational uniformizer t ---
    # Set t = x + sqrt(1 + x^2) (Euler uniformizer of s^2 = 1 + x^2: t^2 - 2*x*t - 1 = 0).
    # Then x = (t^2 - 1)/(2*t) in C(t), so C(x, sqrt(1+x^2)) = C(t) and bar(C(x)) = bar(C(t)),
    # while arsinh(x) = ln(t).
    t_uni = sp.Symbol("t", positive=True, real=True)
    x_of_t = (t_uni**2 - 1) / (2 * t_uni)
    sqrt_of_t = sp.sqrt(sp.factor(1 + x_of_t**2))
    assert sp.simplify(sqrt_of_t - (t_uni**2 + 1) / (2 * t_uni)) == 0
    assert sp.simplify((x_of_t + sqrt_of_t) - t_uni) == 0
    assert sp.simplify(sp.diff(x_of_t, t_uni) / sqrt_of_t - 1 / t_uni) == 0

    # If Q(t, ln t) = (ln t)^d + r_{d-1}(t)*(ln t)^(d-1) + ... + r_0(t) = 0 with d >= 1
    # were a monic minimal polynomial over C(t), differentiating wrt t gives a degree-(d-1)
    # polynomial in ln(t) with leading coefficient r_{d-1}'(t) + d/t = 0 => r_{d-1}'(t) = -d/t.
    # Every rational function r(t) in C(t) has Res_{t=0}(r'(t)) = 0 (since d/dt((t-a)^(-m))
    # = -m*(t-a)^(-m-1) has order >= 2), whereas Res_{t=0}(-d/t) = -d != 0 for all d >= 1.
    d_deg = sp.Symbol("d", integer=True, positive=True)
    m_pole = sp.Symbol("m", integer=True, positive=True)
    t_c, alpha_pole = sp.symbols("t_c alpha_pole", nonzero=True)
    a0_r, a1_r, a2_r = sp.symbols("a0_r a1_r a2_r")
    res_required = sp.residue(-d_deg / t_c, t_c, 0)
    polar_deriv_term = sp.diff(t_c ** (-m_pole), t_c)  # -m * t_c^(-m - 1), exponent <= -2 != -1
    exp_gap_from_minus_1 = sp.simplify((-m_pole - 1) - (-1))  # = -m != 0
    r_sample = (a2_r * t_c**2 + a1_r * t_c + a0_r) / (t_c**3 * (t_c - alpha_pole) ** 2)
    res_sample_0 = sp.simplify(sp.residue(sp.diff(r_sample, t_c), t_c, 0))
    res_sample_alpha = sp.simplify(sp.residue(sp.diff(r_sample, t_c), t_c, alpha_pole))
    assert res_required == -d_deg and res_required.is_nonzero is True
    assert sp.simplify(polar_deriv_term + m_pole * t_c ** (-m_pole - 1)) == 0
    assert exp_gap_from_minus_1.is_nonzero is True
    assert res_sample_0 == 0 and res_sample_alpha == 0

    # =========================================================================
    # 4. APPLY THE SAME TEST TO THE TWO-VECTOR ANSATZ
    #    q_{mu nu} U^mu U^nu = Y / a0_tilde^2  together with  U_mu U^mu = -1
    # =========================================================================
    # Decompose U^mu = gamma_U A^mu + U_perp^mu with A_mu U_perp^mu = 0, gamma_U = -A_mu U^mu.
    # Since g_{mu nu} = -A_mu A_nu + q_{mu nu}, U_mu U^mu = -1 <=> -gamma_U^2 + |U_perp|^2 + 1 = 0.
    # Let y = Y / a0_tilde^2 = x^2 > 0 be the dimensionless spatial scalar invariant.
    gamma_U, u_par, lam_U = sp.symbols("gamma_U u_par lam_U")
    alpha_c, beta_c, kappa_c = sp.symbols("alpha_c beta_c kappa_c", nonzero=True)
    y_dim = sp.Symbol("y_dim", positive=True, real=True)

    # 4A. Unlocked polynomial two-vector action (ONLY unit-timelike U_mu U^mu = -1 imposed):
    #     L_2vec = -alpha * gamma_U + beta * u_par * x + lam_U * (-gamma_U^2 + u_par^2 + 1)
    L_2vec_unlocked = (
        -alpha_c * gamma_U
        + beta_c * u_par * x
        + lam_U * (-(gamma_U**2) + u_par**2 + 1)
    )
    gb_2vec_unlocked = sp.groebner(
        [
            W_sym - L_2vec_unlocked,
            sp.diff(L_2vec_unlocked, gamma_U),
            sp.diff(L_2vec_unlocked, u_par),
            sp.diff(L_2vec_unlocked, lam_U),
        ],
        lam_U,
        gamma_U,
        u_par,
        W_sym,
        order="lex",
    )
    poly_2vec_unlocked = gb_2vec_unlocked[-1]  # W^2 - alpha_c^2 + beta_c^2 * x^2 = 0
    assert sp.expand(poly_2vec_unlocked - (W_sym**2 - alpha_c**2 + beta_c**2 * x**2)) == 0
    # Stationary ratio u_par / gamma_U = (beta_c / alpha_c) * x => u_par^2 = beta^2 x^2 / (alpha^2 - beta^2 x^2),
    # which does NOT yield q_{mu nu} U^mu U^nu = x^2 and produces purely algebraic W(x^2), never arsinh(x).
    sol_unlocked = sp.solve(
        [
            sp.diff(L_2vec_unlocked, gamma_U),
            sp.diff(L_2vec_unlocked, u_par),
            -(gamma_U**2) + u_par**2 + 1,
        ],
        [gamma_U, u_par, lam_U],
        dict=True,
    )
    u_par_sq_unlocked = sp.simplify(sol_unlocked[0][u_par] ** 2)
    assert sp.simplify(u_par_sq_unlocked - beta_c**2 * x**2 / (alpha_c**2 - beta_c**2 * x**2)) == 0

    # Adding quadratic spatial self-coupling (kappa_c/2)*u_par^2 still yields a degree-4 algebraic W(y):
    L_2vec_quad = L_2vec_unlocked - sp.Rational(1, 2) * kappa_c * u_par**2
    eq_c_q = sp.expand(sp.diff(L_2vec_quad, lam_U))     # -gamma_U^2 + u_par^2 + 1 = 0
    # On-shell W = L_2vec_quad|_{eq_c_q = 0}:
    eq_W_q = sp.expand(2 * (W_sym - L_2vec_quad.subs(lam_U, 0)))
    eq_g_q = sp.expand(sp.diff(L_2vec_quad, gamma_U))   # -alpha_c - 2*lam_U*gamma_U = 0
    eq_u_q = sp.expand(sp.diff(L_2vec_quad, u_par))     # beta_c*x + (2*lam_U - kappa_c)*u_par = 0
    # Eliminate lam_U (linear), then gamma_U (linear in eq_stat_q), then u_par:
    eq_stat_q = sp.resultant(eq_u_q, eq_g_q, lam_U)
    res_W_u = sp.resultant(eq_W_q, eq_stat_q, gamma_U)
    res_c_u = sp.resultant(eq_c_q, eq_stat_q, gamma_U)
    poly_2vec_quad_raw = sp.resultant(res_W_u, res_c_u, u_par)
    quad_factors = [
        fac
        for fac, _mult in sp.factor_list(poly_2vec_quad_raw)[1]
        if (W_sym in fac.free_symbols and x in fac.free_symbols)
    ]
    assert len(quad_factors) == 1
    poly_2vec_quad = quad_factors[0]
    deg_2vec_quad_W = sp.Poly(poly_2vec_quad, W_sym).degree()
    assert deg_2vec_quad_W == 4

    # 4B. Locked two-vector ansatz: q_{mu nu} U^mu U^nu = y (= x^2) AND U_mu U^mu = -1 written in by hand.
    u_perp_norm = sp.Symbol("u_perp_norm", positive=True, real=True)
    gamma_pos = sp.Symbol("gamma_pos", positive=True, real=True)
    locked_kinematics = sp.solve(
        [-(gamma_pos**2) + u_perp_norm**2 + 1, u_perp_norm**2 - x**2],
        [gamma_pos, u_perp_norm],
        dict=True,
    )
    assert len(locked_kinematics) == 1
    gamma_locked = locked_kinematics[0][gamma_pos]  # sqrt(1 + x^2)
    u_perp_locked = locked_kinematics[0][u_perp_norm]  # x
    v_boost_ratio = sp.simplify(u_perp_locked / gamma_locked)
    assert sp.simplify(v_boost_ratio - mu_std) == 0

    # Because q_{mu nu} U^mu U^nu = Y / a0_tilde^2 was imposed by hand rather than derived
    # from an unlocked polynomial variation, record the required verdict and do NOT count it:
    two_vector_lock_status = "lock inserted, not derived"
    two_vector_counted_as_pass = False

    # Furthermore, test the locked ansatz inside ANY polynomial action
    # L_locked = L_0(gamma_U, |U_perp|, y) + lam_U*(-gamma_U^2 + |U_perp|^2 + 1) + xi*(|U_perp|^2 - y):
    # Modulo gamma_U^2 = 1 + y and |U_perp|^2 = y, EVERY polynomial L_0 reduces on-shell to
    #   W_locked(y) = P0(y) + P1(y)*sqrt(y) + P2(y)*sqrt(1+y) + P3(y)*sqrt(y*(1+y))
    # with P0, P1, P2, P3 in C[y].
    # For example, L_0 = gamma_U - 1 gives W_locked(y) = sqrt(1+y) - 1, whose scalar variation
    # gives 2 * dW_locked/dy = 1/sqrt(1+y) != sqrt(y)/sqrt(1+y) (wrong normalization, fails mu(0)=0).
    W_bi_locked = sp.sqrt(1 + y_dim) - 1
    assert sp.simplify(2 * sp.diff(W_bi_locked, y_dim) - 1 / sp.sqrt(1 + y_dim)) == 0

    # Can ANY polynomials P0, P1, P2, P3 in C[y] satisfy 2 * dW_locked/dy = sqrt(y)/sqrt(1+y)?
    # Over the C(y)-linearly independent basis {1, sqrt(y), sqrt(1+y), sqrt(y*(1+y))},
    # only d/dy[P3(y)*sqrt(y*(1+y))] = [2*y*(1+y)*P3'(y) + (1+2*y)*P3(y)] / (2*sqrt(y*(1+y)))
    # lies in the C(y)*1/sqrt(y*(1+y)) summand where sqrt(y)/sqrt(1+y) = y / sqrt(y*(1+y)) lives.
    # Thus 2 * dW_locked/dy = y / sqrt(y*(1+y)) requires:
    #   2*y*(1+y)*P3'(y) + (1+2*y)*P3(y) = y   for some polynomial P3(y) in C[y].
    # If deg(P3) = m >= 0 with leading term c_m y^m (c_m != 0), LHS has degree m + 1 with
    # coefficient (2m + 2)*c_m != 0, forcing m + 1 = 1 => m = 0 => P3(y) = c_0 (constant).
    m_deg = sp.Symbol("m_deg", integer=True, nonnegative=True)
    lead_coeff_factor = sp.simplify(2 * m_deg + 2)
    assert sp.solve(m_deg + 1 - 1, m_deg) == [0]
    assert lead_coeff_factor.subs(m_deg, 0) == 2

    c0_const = sp.Symbol("c0_const")
    ode_poly_residual = sp.Poly((1 + 2 * y_dim) * c0_const - y_dim, y_dim)
    # Matching y^1 requires 2*c0_const - 1 = 0 (c0 = 1/2), while y^0 requires c0_const = 0:
    sol_P3_const = sp.solve(ode_poly_residual.coeffs(), [c0_const])
    assert sol_P3_const == []

    # At the closest algebraic candidate c0 = 1/2 (W_locked = (1/2)*sqrt(y*(1+y)) = A_alg),
    # the uncancelled derivative mismatch is 1/(2*sqrt(y*(1+y))) = d/dy[arsinh(sqrt(y))]:
    uncancelled_locked_deriv = sp.simplify(
        2 * sp.diff(sp.Rational(1, 2) * sp.sqrt(y_dim * (1 + y_dim)), y_dim)
        - sp.sqrt(y_dim) / sp.sqrt(1 + y_dim)
    )
    assert sp.simplify(uncancelled_locked_deriv - 1 / (2 * sp.sqrt(y_dim * (1 + y_dim)))) == 0
    assert sp.simplify(uncancelled_locked_deriv - sp.diff(sp.asinh(sp.sqrt(y_dim)), y_dim)) == 0

    # =========================================================================
    # 5. ONE-LINE BOUNDARY NOTE ON ONE-LOOP Tr ln (OUTSIDE THIS CLASS)
    # =========================================================================
    one_loop_note = (
        "A one-loop functional determinant (Tr ln) defines a quantum effective action "
        "outside the classical polynomial auxiliary class and is not evaluated here."
    )

    # =========================================================================
    # PRINT VERDICTS & WRITE JSON RECEIPT
    # =========================================================================
    verdict = "no-go: algebraic elimination cannot produce arsinh"

    print(verdict)
    print(f"general_onshell_class: {general_onshell_class_str}")
    print(f"algebraic_part_subtracted: F_std(x) - (1/2)*x*sqrt(1+x^2) = {F_remainder}")
    print(
        "obstruction_recurrence_eisenstein: "
        "(1+x^2)*w'' + x*w' = 0 => c_{2n+1} = -((2n-1)^2/(2n*(2n+1)))*c_{2n-1}, "
        "c_{2n+1} = (-1)^n*binomial(2n,n)/(4^n*(2n+1)); for every odd prime p = 2n+1, "
        "gcd(binomial(p-1,(p-1)/2), p) = 1 so v_p(c_p) = -1 (infinitely many primes in "
        "denominators, violating Eisenstein's theorem B^k*c_k in Z for algebraic series)."
    )
    print(
        "obstruction_branch_and_residue: "
        f"dw/dx = 1/sqrt(1+x^2) has period {branch_cut_period} across branch cut [-i, +i] "
        f"(infinitely many sheets w + 2*pi*i*Z) and residue {res_at_infinity} at u = 1/x = 0 "
        f"(producing -(1/2)*ln(2x) in F_std(x) as x -> +oo, violating Puiseux's theorem); "
        "on rational uniformizer t = x + sqrt(1+x^2), minimal polynomial degree d >= 1 "
        "forces r_{d-1}'(t) = -d/t with Res_{t=0}(-d/t) = -d != 0 = Res_{t=0}(r'(t))."
    )
    print(two_vector_lock_status)
    print(
        "two_vector_action_test: "
        "unlocked polynomial 2-vector elimination gives algebraic W(y) (deg 2 or 4, never arsinh); "
        "even on the hand-locked manifold (gamma_U = sqrt(1+y), |U_perp| = sqrt(y)), "
        "2*dW_locked/dy = sqrt(y)/sqrt(1+y) reduces to 2*y*(1+y)*P3'(y) + (1+2*y)*P3(y) = y, "
        f"which has polynomial solution set {sol_P3_const} (leaving uncancelled {uncancelled_locked_deriv} = d/dy asinh(sqrt(y)))."
    )
    print(one_loop_note)

    receipt = {
        "script": str(pathlib.Path(__file__).resolve()),
        "verdict": verdict,
        "exit_code": 0,
        "class_definition": class_definition,
        "target_function": {
            "F_std_x": "1/2 * (x * sqrt(1 + x^2) - asinh(x))",
            "arsinh_x": "log(x + sqrt(1 + x^2))",
            "mu_std_x": "x / sqrt(1 + x^2)",
            "F_std_prime_over_x_equals_mu_std": True,
            "two_J_std_prime_Y_equals_mu_std_sqrt_Y": True,
            "stationary_artanh_sigma_rewrite_counted_as_pass": False,
        },
        "sympy_auxiliary_elimination": {
            "general_onshell_kinetic_class": general_onshell_class_str,
            "quadratic_auxiliary_eliminated_poly": str(poly_quad_YW),
            "radical_constraint_eliminated_poly": str(poly_rad1_YW),
            "algebraic_half_of_Fstd_eliminated_poly": str(poly_alg_part_YW),
            "converse_realization_L_P": "chi + lambda * P(Y, chi)",
            "converse_variational_consistency_verified": True,
        },
        "transcendence_obstruction": {
            "algebraic_piece_A_alg": "1/2 * x * sqrt(1 + x^2)",
            "A_alg_defining_polynomial": "4*A^2 - x^2*(1 + x^2) = 0",
            "remainder_after_subtracting_A_alg": str(F_remainder),
            "fuchsian_ode": "(1 + x^2)*w''(x) + x*w'(x) = 0",
            "power_series_recurrence": "c_{2n+1} = -((2n - 1)^2 / (2n*(2n + 1))) * c_{2n-1}, c_1 = 1",
            "closed_form_coeff": "c_{2n+1} = (-1)^n * binomial(2n, n) / (4^n * (2n + 1))",
            "eisenstein_obstruction": {
                "A_alg_denom_primes_up_to_x55": sorted(alg_denom_primes),
                "arsinh_denom_primes_up_to_x55": sorted(asinh_denom_primes),
                "odd_primes_verified_v_p_eq_minus_1": odd_primes_tested,
                "infinite_prime_support_violates_eisenstein": True,
            },
            "branch_and_puiseux_obstruction": {
                "derivative": "1 / sqrt(1 + x^2)",
                "branch_points": ["I", "-I"],
                "period_around_cut": str(branch_cut_period),
                "monodromy_sheet_count": "infinite (w + 2*pi*I*Z)",
                "residue_of_dw_at_infinity_u_eq_0": int(res_at_infinity),
                "F_std_asymptotic_x_to_inf": str(F_std_asymp_x),
                "log_x_coefficient_at_infinity": "-1/2",
            },
            "liouville_minimal_polynomial_obstruction": {
                "euler_uniformizer": "t = x + sqrt(1 + x^2), t^2 - 2*x*t - 1 = 0",
                "required_rational_derivative": "r_{d-1}'(t) = -d/t (d >= 1)",
                "residue_of_required_rhs_at_t0": "-d != 0",
                "residue_of_any_rational_derivative_at_t0": 0,
            },
        },
        "two_vector_ansatz_audit": {
            "unlocked_eliminated_poly_linear": str(poly_2vec_unlocked),
            "unlocked_eliminated_poly_quadratic_degree_in_W": 4,
            "unlocked_u_par_squared": str(u_par_sq_unlocked),
            "locked_kinematic_ratio_v_equals_mu_std": True,
            "lock_verdict": two_vector_lock_status,
            "counted_as_derivation": two_vector_counted_as_pass,
            "locked_action_polynomial_ode": "2*y*(1 + y)*P3'(y) + (1 + 2*y)*P3(y) = y",
            "locked_action_polynomial_solutions": sol_P3_const,
            "uncancelled_derivative_remainder": str(uncancelled_locked_deriv),
        },
        "outside_class_note": one_loop_note,
    }

    receipt_path = pathlib.Path(__file__).with_suffix(".json")
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
