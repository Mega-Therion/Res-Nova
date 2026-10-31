#!/usr/bin/env python3
"""
Q3 Action-Forcing Audit (TARGET_D2 §9 Q3 & TARGET_D2_SUPPLEMENT §6 item 4):
Does the covariant AeST (or AQUAL) action force mu(x) = x / sqrt(1 + x^2),
or is that function an external input?

Citations verified on disk (read-only):
- /home/mega/Chyren/3_research/Res-Nova/TARGET_D2_PHYSICAL_ACTION_DERIVATION.md
  lines 30, 50-56, 70-78, 86, 100-104, 112-116, 230-262, 323
- /home/mega/Chyren/3_research/Res-Nova/TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md
  lines 12-18, 50-81, 107-131, 145-172, 190-195, 226-269, 376
- /home/mega/Chyren/3_research/Res-Nova/TARGET_D7_COVARIANT_COMPLETION.md
  lines 38-48, 69-74, 80-108, 128-139, 300-317, 329-352, 408-411
- /home/mega/Chyren/3_research/Res-Nova/05_lean_formalization/MuNDuality.lean
  lines 42-60
- /home/mega/Chyren/3_research/Res-Nova/05_lean_formalization/SZStdEmbedding.lean
  lines 41-96
- /home/mega/Chyren/3_research/Res-Nova/05_lean_formalization/AeSTTotalScalarCorrespondence.lean
  lines 15-36, 46-62, 84-85, 145-163, 199-200
"""

import json
import pathlib
import sys
import sympy as sp


def euler_lagrange_3d(L_expr, field_func, coords):
    """Compute dL/df - sum_i d/dx_i (dL / d(df/dx_i)) in 3D Cartesian coordinates."""
    df_list = [sp.diff(field_func, c) for c in coords]
    dummy_grads = [sp.Symbol(f"_g{i}", real=True) for i in range(len(coords))]
    subs_to_dummy = dict(zip(df_list, dummy_grads))
    subs_from_dummy = dict(zip(dummy_grads, df_list))

    L_dummy = L_expr.subs(subs_to_dummy)
    dL_df = sp.diff(L_dummy, field_func).subs(subs_from_dummy)

    div_term = sp.S.Zero
    for c, dg in zip(coords, dummy_grads):
        pi_i = sp.diff(L_dummy, dg).subs(subs_from_dummy)
        div_term += sp.diff(pi_i, c)

    return sp.simplify(dL_df - div_term)


def compute_christoffel_4d(g, g_inv, coords):
    """Compute 4D Christoffel symbols Gamma^lam_{mu nu}."""
    n = 4
    Gamma = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for lam in range(n):
        for mu in range(n):
            for nu in range(mu, n):
                val = sp.S.Zero
                for sig in range(n):
                    if g_inv[lam, sig] != 0:
                        val += sp.Rational(1, 2) * g_inv[lam, sig] * (
                            sp.diff(g[sig, mu], coords[nu])
                            + sp.diff(g[sig, nu], coords[mu])
                            - sp.diff(g[mu, nu], coords[sig])
                        )
                Gamma[lam][mu][nu] = val
                Gamma[lam][nu][mu] = val
    return Gamma


def compute_ricci_scalar_4d(g_inv, Gamma, coords):
    """Compute 4D Ricci scalar R = g^{mu nu} R_{mu nu}."""
    n = 4
    R_scalar = sp.S.Zero
    for mu in range(n):
        for nu in range(n):
            if g_inv[mu, nu] == 0:
                continue
            R_munu = sp.S.Zero
            for rho in range(n):
                R_munu += (
                    sp.diff(Gamma[rho][mu][nu], coords[rho])
                    - sp.diff(Gamma[rho][mu][rho], coords[nu])
                )
                for lam in range(n):
                    R_munu += (
                        Gamma[rho][rho][lam] * Gamma[lam][mu][nu]
                        - Gamma[rho][nu][lam] * Gamma[lam][mu][rho]
                    )
            R_scalar += g_inv[mu, nu] * R_munu
    return R_scalar


def main():
    # =========================================================================
    # 1. AQUAL EULER-LAGRANGE VARIATION & CONVENTION RECONCILIATION
    #    Citations:
    #    - TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:86, 100-104
    #    - TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md:50-62
    #    - TARGET_D7_COVARIANT_COMPLETION.md:97-108
    # =========================================================================
    x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
    coords_3d = (x1, x2, x3)
    a0, G, pi_sym = sp.symbols("a0 G pi", positive=True, real=True)

    Phi_fn = sp.Function("Phi")(x1, x2, x3)
    rho_fn = sp.Function("rho")(x1, x2, x3)

    grad_Phi_sq = sum(sp.diff(Phi_fn, c) ** 2 for c in coords_3d)
    Y_inv = grad_Phi_sq / a0**2
    x_mag = sp.sqrt(grad_Phi_sq) / a0

    # 1A. Action in terms of quadratic kinetic invariant Y = |grad Phi|^2 / a0^2
    F_kin = sp.Function("F_kin")
    L_aqual_Y = -(a0**2 / (8 * pi_sym * G)) * F_kin(Y_inv) - rho_fn * Phi_fn
    EL_aqual_Y = euler_lagrange_3d(L_aqual_Y, Phi_fn, coords_3d)

    # Expected: (1 / (4*pi*G)) * div(F_kin'(Y) * grad Phi) - rho = 0
    Y_pos = sp.Symbol("Y", positive=True, real=True)
    dFkin_dY_at_Yinv = sp.Subs(sp.diff(F_kin(Y_pos), Y_pos), Y_pos, Y_inv)
    expected_div_Y = sum(
        sp.diff(dFkin_dY_at_Yinv * sp.diff(Phi_fn, c), c)
        for c in coords_3d
    )
    residual_EL_aqual_Y = sp.simplify(
        (EL_aqual_Y - (expected_div_Y / (4 * pi_sym * G) - rho_fn)).doit()
    )
    assert residual_EL_aqual_Y == 0, f"AQUAL Y-variation mismatch: {residual_EL_aqual_Y}"

    # 1B. Chain-rule relation between F_kin(Y) and TARGET_D2's F_D2(x) (x = sqrt(Y))
    x_pos = sp.Symbol("x", positive=True, real=True)
    F_D2 = sp.Function("F_D2")
    mu_gen = sp.Function("mu")

    # Under F_kin(Y) = 2 * F_D2(sqrt(Y)), dF_kin/dY = F_D2'(x) / x = mu(x)
    dFkin_dY_from_FD2 = sp.simplify(
        sp.diff(2 * F_D2(sp.sqrt(Y_pos)), Y_pos).subs(Y_pos, x_pos**2)
    )
    assert sp.simplify(dFkin_dY_from_FD2 - sp.diff(F_D2(x_pos), x_pos) / x_pos) == 0

    # Without the factor of 2 in S = -(a0^2 / 8*pi*G) int F_D2(|grad Phi|/a0) d^3x
    # (the exact factor-of-2 discrepancy noted at TARGET_D7_COVARIANT_COMPLETION.md:97-104):
    L_aqual_D2_literal = -(a0**2 / (8 * pi_sym * G)) * F_D2(x_mag) - rho_fn * Phi_fn
    EL_aqual_D2_literal = euler_lagrange_3d(L_aqual_D2_literal, Phi_fn, coords_3d)
    expected_div_D2_literal = sum(
        sp.diff(
            (sp.Subs(sp.diff(F_D2(x_pos), x_pos), x_pos, x_mag) / x_mag)
            * sp.diff(Phi_fn, c),
            c,
        )
        for c in coords_3d
    )
    residual_D2_literal = sp.simplify(
        (EL_aqual_D2_literal - (expected_div_D2_literal / (8 * pi_sym * G) - rho_fn)).doit()
    )
    assert residual_D2_literal == 0

    # Verify why sqrt(1+x^2) - 1 is EXCLUDED (banned move, TARGET_D2_SUPPLEMENT:52-62):
    F_wrong = sp.sqrt(1 + x_pos**2) - 1
    mu_from_F_wrong = sp.simplify(sp.diff(F_wrong, x_pos) / x_pos)
    c3_wrong = sp.limit(F_wrong / x_pos**2, x_pos, sp.oo)
    c4_wrong = sp.limit(F_wrong / x_pos**3, x_pos, 0, dir="+")
    assert c3_wrong == 0  # Fails C3 (requires 1/2)
    assert c4_wrong == sp.oo  # Fails C4 (requires finite c > 0)

    # =========================================================================
    # 2. COVARIANT AeST ACTION VARIATION & QUASISTATIC WEAK-FIELD REDUCTION
    #    Citations:
    #    - TARGET_D7_COVARIANT_COMPLETION.md:38-48 (covariant AeST action eq. 5)
    #    - TARGET_D7_COVARIANT_COMPLETION.md:70, 80-94, 103-107, 128-136
    # =========================================================================
    # 2A. Exact covariant scalar shift-symmetry current P^mu from arbitrary F_cov(Y, Q)
    KB = sp.Symbol("K_B", real=True)
    G_tilde, G_hat = sp.symbols("G_tilde G_hat", positive=True, real=True)
    Y_cov, Q_cov = sp.symbols("Y_cov Q_cov", real=True)
    F_cov = sp.Function("F_cov")

    # Covariant scalar gradient components phi_mu and background tensors q^{mu nu}, A^mu, J^mu
    phi_0, phi_1 = sp.symbols("phi_0 phi_1", real=True)
    A0_up, J0_up, q11_up = sp.symbols("A0_up J0_up q11_up", real=True)
    Y_expr_cov = q11_up * phi_1**2
    Q_expr_cov = A0_up * phi_0
    L_scalar_cov = (
        2 * (2 - KB) * J0_up * phi_0
        - (2 - KB) * Y_expr_cov
        - F_cov(Y_expr_cov, Q_expr_cov)
    )
    P0_cov = sp.simplify(-sp.Rational(1, 2) * sp.diff(L_scalar_cov, phi_0))
    P1_cov = sp.simplify(-sp.Rational(1, 2) * sp.diff(L_scalar_cov, phi_1))
    # Verify P^1 = [(2 - K_B) + dF_cov/dY] * q^{11} * phi_1 for arbitrary F_cov
    expected_P1 = (
        (2 - KB) + sp.Subs(sp.diff(F_cov(Y_cov, Q_cov), Y_cov), (Y_cov, Q_cov), (Y_expr_cov, Q_expr_cov))
    ) * q11_up * phi_1
    assert sp.simplify(P1_cov - expected_P1) == 0

    # 2B. Full 4D weak-field quasistatic expansion of AeST action for arbitrary J(Y)
    t_coord = sp.Symbol("t", real=True)
    coords_4d = (t_coord, x1, x2, x3)
    eps = sp.Symbol("eps", real=True)
    Q0 = sp.Symbol("Q0", positive=True, real=True)

    def trunc2(expr):
        expanded = sp.expand(expr)
        return (
            expanded.coeff(eps, 0)
            + eps * expanded.coeff(eps, 1)
            + eps**2 * expanded.coeff(eps, 2)
        )

    Psi_wf = sp.Function("Psi")(x1, x2, x3)
    Phi_wf = sp.Function("Phi_m")(x1, x2, x3)
    varphi_wf = sp.Function("varphi")(x1, x2, x3)

    u_psi, u_phi = sp.symbols("u_psi u_phi", real=True)
    wf_subs = {u_psi: Psi_wf, u_phi: Phi_wf}

    g_4d = sp.diag(
        -(1 + 2 * eps * Psi_wf),
        1 - 2 * eps * Phi_wf,
        1 - 2 * eps * Phi_wf,
        1 - 2 * eps * Phi_wf,
    )
    inv_g00 = sp.series(-1 / (1 + 2 * eps * u_psi), eps, 0, 3).removeO().subs(wf_subs)
    inv_gii = sp.series(1 / (1 - 2 * eps * u_phi), eps, 0, 3).removeO().subs(wf_subs)
    g_4d_inv = sp.diag(inv_g00, inv_gii, inv_gii, inv_gii)
    sqrt_neg_g = (
        sp.series(sp.sqrt((1 + 2 * eps * u_psi) * (1 - 2 * eps * u_phi) ** 3), eps, 0, 3)
        .removeO()
        .subs(wf_subs)
    )

    Gamma_4d_raw = compute_christoffel_4d(g_4d, g_4d_inv, coords_4d)
    Gamma_4d = [
        [[trunc2(Gamma_4d_raw[l][m][n]) for n in range(4)] for m in range(4)]
        for l in range(4)
    ]
    R_4d = trunc2(compute_ricci_scalar_4d(g_4d_inv, Gamma_4d, coords_4d))

    # Landau-Lifshitz bulk first-derivative Einstein-Hilbert density + exact total divergence
    L_EH_bulk = sp.S.Zero
    for mu in range(4):
        for nu in range(4):
            if g_4d_inv[mu, nu] == 0:
                continue
            term = sp.S.Zero
            for rho in range(4):
                for lam in range(4):
                    term += (
                        Gamma_4d[rho][mu][lam] * Gamma_4d[lam][nu][rho]
                        - Gamma_4d[rho][mu][nu] * Gamma_4d[lam][rho][lam]
                    )
            L_EH_bulk += trunc2(sqrt_neg_g * g_4d_inv[mu, nu] * term)
    L_EH_bulk = trunc2(L_EH_bulk)

    div_V = sp.S.Zero
    for alpha in range(4):
        V_alpha = sp.S.Zero
        for mu in range(4):
            for nu in range(4):
                V_alpha += trunc2(
                    sqrt_neg_g
                    * (
                        g_4d_inv[mu, nu] * Gamma_4d[alpha][mu][nu]
                        - g_4d_inv[alpha, mu] * Gamma_4d[nu][mu][nu]
                    )
                )
        div_V += trunc2(sp.diff(V_alpha, coords_4d[alpha]))
    div_V = trunc2(div_V)

    eh_ibp_residual = sp.expand(trunc2(sqrt_neg_g * R_4d) - L_EH_bulk - div_V)
    assert eh_ibp_residual == 0, f"4D EH IBP identity failed: {eh_ibp_residual}"

    L_EH_quad = sp.expand(L_EH_bulk.coeff(eps, 2))
    grad_Phi_wf_sq = sum(sp.diff(Phi_wf, c) ** 2 for c in coords_3d)
    grad_Psi_wf_sq = sum(sp.diff(Psi_wf, c) ** 2 for c in coords_3d)
    grad_Phi_dot_Psi = sum(sp.diff(Phi_wf, c) * sp.diff(Psi_wf, c) for c in coords_3d)
    grad_Psi_dot_varphi = sum(sp.diff(Psi_wf, c) * sp.diff(varphi_wf, c) for c in coords_3d)
    grad_varphi_sq = sum(sp.diff(varphi_wf, c) ** 2 for c in coords_3d)

    assert sp.expand(L_EH_quad - (2 * grad_Phi_wf_sq - 4 * grad_Phi_dot_Psi)) == 0

    # Unit-timelike aether A_mu = (-sqrt(1 + 2*eps*Psi), 0, 0, 0), A^mu A_mu = -1 to O(eps^2)
    A0_cov_wf = sp.series(-sp.sqrt(1 + 2 * eps * u_psi), eps, 0, 3).removeO().subs(wf_subs)
    A_cov = [A0_cov_wf, sp.S.Zero, sp.S.Zero, sp.S.Zero]
    A_up = [trunc2(g_4d_inv[mu, mu] * A_cov[mu]) for mu in range(4)]
    assert trunc2(sum(A_up[mu] * A_cov[mu] for mu in range(4)) + 1) == 0

    # F_{mu nu} = d_mu A_nu - d_nu A_mu and -K_B/2 F^{mu nu} F_{mu nu}
    F_sq = sp.S.Zero
    for mu in range(4):
        for nu in range(4):
            F_munu = trunc2(sp.diff(A_cov[nu], coords_4d[mu]) - sp.diff(A_cov[mu], coords_4d[nu]))
            F_sq += trunc2(g_4d_inv[mu, mu] * g_4d_inv[nu, nu] * F_munu**2)
    aether_F_quad = sp.expand(trunc2(-sp.Rational(1, 2) * KB * sqrt_neg_g * F_sq).coeff(eps, 2))
    assert sp.expand(aether_F_quad - KB * grad_Psi_wf_sq) == 0

    # J_mu = A^alpha nabla_alpha A_mu and 2*(2-K_B)*J^mu nabla_mu phi with phi = Q0*t + eps*varphi
    phi_4d = Q0 * t_coord + eps * varphi_wf
    J_cov = [sp.S.Zero] * 4
    for mu in range(4):
        for alpha in range(4):
            nabla_alpha_A_mu = sp.diff(A_cov[mu], coords_4d[alpha]) - sum(
                Gamma_4d[lam][alpha][mu] * A_cov[lam] for lam in range(4)
            )
            J_cov[mu] += trunc2(A_up[alpha] * nabla_alpha_A_mu)
    J_dot_dphi = sum(
        trunc2(g_4d_inv[mu, mu] * J_cov[mu] * sp.diff(phi_4d, coords_4d[mu])) for mu in range(4)
    )
    J_term_quad = sp.expand(trunc2(2 * (2 - KB) * sqrt_neg_g * J_dot_dphi).coeff(eps, 2))
    assert sp.expand(J_term_quad - 2 * (2 - KB) * grad_Psi_dot_varphi) == 0

    # Y = q^{mu nu} nabla_mu phi nabla_nu phi with q^{mu nu} = g^{mu nu} + A^mu A^nu
    Y_4d = sp.S.Zero
    for mu in range(4):
        for nu in range(4):
            q_munu_up = trunc2(
                (g_4d_inv[mu, nu] if mu == nu else sp.S.Zero) + A_up[mu] * A_up[nu]
            )
            Y_4d += trunc2(q_munu_up * sp.diff(phi_4d, coords_4d[mu]) * sp.diff(phi_4d, coords_4d[nu]))
    Y_quad = sp.expand(trunc2(Y_4d).coeff(eps, 2))
    assert sp.expand(Y_quad - grad_varphi_sq) == 0

    # Combine all quadratic kinetic terms + general free function J_fn(Y) := F_cov(Y, Q0)/(2 - K_B)
    J_fn = sp.Function("J")
    bracket_QS = (
        L_EH_quad
        + aether_F_quad
        + J_term_quad
        - (2 - KB) * grad_varphi_sq
        - (2 - KB) * J_fn(grad_varphi_sq)
    )

    # Step 2B.1: Vary wrt Phi_wf -> proves nabla^2(Phi - Psi) = 0 for EVERY J_fn(Y)
    EL_Phi_wf = euler_lagrange_3d(bracket_QS, Phi_wf, coords_3d)
    lap_Phi_minus_Psi = sum(sp.diff(Phi_wf - Psi_wf, c, 2) for c in coords_3d)
    assert sp.simplify(EL_Phi_wf - (-4 * lap_Phi_minus_Psi)) == 0

    # Step 2B.2: Substitute Phi = Psi = Phi_hat + varphi -> completes square to -(2-K_B)*[|grad Phi_hat|^2 + J(Y)]
    Phi_hat_wf = sp.Function("Phi_hat")(x1, x2, x3)
    grad_Phi_hat_sq = sum(sp.diff(Phi_hat_wf, c) ** 2 for c in coords_3d)
    bracket_on_Phi_eq_Psi = sp.simplify(
        bracket_QS.subs(Phi_wf, Psi_wf).subs(Psi_wf, Phi_hat_wf + varphi_wf).doit()
    )
    expected_completed_square = -(2 - KB) * (grad_Phi_hat_sq + J_fn(grad_varphi_sq))
    assert sp.simplify(bracket_on_Phi_eq_Psi - expected_completed_square) == 0

    # Step 2B.3: With G_tilde = (1 - K_B/2)*G_hat (TARGET_D7:82), (2-K_B)/(16*pi*G_tilde) = 1/(8*pi*G_hat)
    prefactor_ratio = sp.simplify(
        ((2 - KB) / (16 * pi_sym * G_tilde)).subs(G_tilde, (1 - KB / 2) * G_hat)
        - 1 / (8 * pi_sym * G_hat)
    )
    assert prefactor_ratio == 0

    # Step 2B.4: Vary TARGET_D7 eq. (2) (line 84) wrt Phi_hat and varphi for arbitrary J_fn(Y)
    L_D7_eq2 = (1 / (8 * pi_sym * G_hat)) * (
        grad_Phi_hat_sq + J_fn(grad_varphi_sq)
    ) + (Phi_hat_wf + varphi_wf) * rho_fn
    EL_Phi_hat = euler_lagrange_3d(L_D7_eq2, Phi_hat_wf, coords_3d)
    EL_varphi = euler_lagrange_3d(L_D7_eq2, varphi_wf, coords_3d)

    lap_Phi_hat = sum(sp.diff(Phi_hat_wf, c, 2) for c in coords_3d)
    dJ_dY_at_varphi = sp.Subs(sp.diff(J_fn(Y_pos), Y_pos), Y_pos, grad_varphi_sq)
    div_Jp_grad_varphi = sum(
        sp.diff(dJ_dY_at_varphi * sp.diff(varphi_wf, c), c)
        for c in coords_3d
    )
    assert sp.simplify((EL_Phi_hat - (rho_fn - lap_Phi_hat / (4 * pi_sym * G_hat))).doit()) == 0
    assert sp.simplify((EL_varphi - (rho_fn - div_Jp_grad_varphi / (4 * pi_sym * G_hat))).doit()) == 0

    # Step 2C: Normalizations G_N = (1 + 1/lam_s)*G_hat and a0_tilde = (1 + lam_s)*a0 (TARGET_D7:128-136)
    lam_s, a0_tilde, g_N_sym = sp.symbols("lambda_s a0_tilde g_N", positive=True, real=True)
    # Tracking limit J'(Y) -> lam_s => g_varphi = g_hat / lam_s => g = g_hat * (1 + 1/lam_s) = g_N
    G_N_expr = sp.simplify((1 + 1 / lam_s) * G_hat)
    # Deep-MOND limit J'(Y) -> lam_s * sqrt(Y) / a0_tilde => lam_s * g_varphi^2 / a0_tilde = g_hat
    # With g ~ g_varphi (only as lam_s -> 0; at finite lam_s, SZ deep-MOND requires
    # J(Y) -> (2*lam_s / (3*(1+lam_s)*a0)) * Y^{3/2} so J'(Y) -> (lam_s / ((1+lam_s)*a0)) * sqrt(Y))
    # Matching lam_s * sqrt(Y) / a0_tilde == (lam_s / ((1+lam_s)*a0)) * sqrt(Y) forces a0_tilde = (1+lam_s)*a0:
    a0_tilde_sol = sp.solve(
        sp.Eq(lam_s / a0_tilde, lam_s / ((1 + lam_s) * a0)), a0_tilde
    )[0]
    assert sp.simplify(a0_tilde_sol - (1 + lam_s) * a0) == 0

    # =========================================================================
    # 3. TEST EVERY ALLOWED CONSISTENCY CONDITION FROM ACTION & CITED FILES
    # =========================================================================
    # 3A. Luminal tensor speed c_T = c (TARGET_D7_COVARIANT_COMPLETION.md:329-341)
    z_coord = x3
    h_plus = sp.Function("h_p")(t_coord, z_coord)
    h_cross = sp.Function("h_x")(t_coord, z_coord)
    hp_s, hx_s = sp.symbols("hp_s hx_s", real=True)
    tt_subs = {hp_s: h_plus, hx_s: h_cross}

    g_tt = sp.Matrix(
        [
            [-1, 0, 0, 0],
            [0, 1 + eps * h_plus, eps * h_cross, 0],
            [0, eps * h_cross, 1 - eps * h_plus, 0],
            [0, 0, 0, 1],
        ]
    )
    g_tt_alg = sp.Matrix(
        [
            [-1, 0, 0, 0],
            [0, 1 + eps * hp_s, eps * hx_s, 0],
            [0, eps * hx_s, 1 - eps * hp_s, 0],
            [0, 0, 0, 1],
        ]
    )
    g_tt_inv_alg = g_tt_alg.inv()
    g_tt_inv = sp.Matrix(
        4,
        4,
        lambda i, j: sp.series(g_tt_inv_alg[i, j], eps, 0, 3).removeO().subs(tt_subs),
    )
    sqrt_neg_g_tt = (
        sp.series(sp.sqrt(-g_tt_alg.det()), eps, 0, 3).removeO().subs(tt_subs)
    )
    Gamma_tt_raw = compute_christoffel_4d(g_tt, g_tt_inv, coords_4d)
    Gamma_tt = [
        [[trunc2(Gamma_tt_raw[l][m][n]) for n in range(4)] for m in range(4)]
        for l in range(4)
    ]

    R_tt = trunc2(compute_ricci_scalar_4d(g_tt_inv, Gamma_tt, coords_4d))
    L_full_tt_quad = sp.expand(trunc2(sqrt_neg_g_tt * R_tt).coeff(eps, 2))
    # Vary L_full_tt_quad wrt h_plus(t, z):
    dh_dt = sp.diff(h_plus, t_coord)
    dh_dz = sp.diff(h_plus, z_coord)
    dh_dt2 = sp.diff(h_plus, t_coord, 2)
    dh_dz2 = sp.diff(h_plus, z_coord, 2)
    d1, d2, d3, d4 = sp.symbols("_d1 _d2 _d3 _d4", real=True)
    L_tt_sub = L_full_tt_quad.subs({dh_dt2: d3, dh_dz2: d4, dh_dt: d1, dh_dz: d2})
    EL_h_plus = sp.simplify(
        sp.diff(L_tt_sub, h_plus)
        - sp.diff(sp.diff(L_tt_sub, d1).subs({d1: dh_dt, d2: dh_dz, d3: dh_dt2, d4: dh_dz2}), t_coord)
        - sp.diff(sp.diff(L_tt_sub, d2).subs({d1: dh_dt, d2: dh_dz, d3: dh_dt2, d4: dh_dz2}), z_coord)
        + sp.diff(sp.diff(L_tt_sub, d3).subs({d1: dh_dt, d2: dh_dz, d3: dh_dt2, d4: dh_dz2}), t_coord, 2)
        + sp.diff(sp.diff(L_tt_sub, d4).subs({d1: dh_dt, d2: dh_dz, d3: dh_dt2, d4: dh_dz2}), z_coord, 2)
    ).subs({d1: dh_dt, d2: dh_dz, d3: dh_dt2, d4: dh_dz2})
    # Wave operator is proportional to (d_t^2 - d_z^2) h_plus => c_T^2 = 1:
    c_T_sq = sp.simplify(-EL_h_plus.coeff(dh_dz2) / EL_h_plus.coeff(dh_dt2))
    assert c_T_sq == 1, f"Expected c_T^2 = 1, got {c_T_sq}"

    # Verify AeST scalar & vector invariants Y, Q, F^2, J.dphi on background A_mu=(-1,0,0,0), phi=Q0*t:
    A_tt_cov = [-sp.S.One, sp.S.Zero, sp.S.Zero, sp.S.Zero]
    A_tt_up = [sp.S.One, sp.S.Zero, sp.S.Zero, sp.S.Zero]
    phi_bg = Q0 * t_coord
    Y_tt = sp.simplify(
        sum(
            (g_tt_inv[mu, nu] + A_tt_up[mu] * A_tt_up[nu])
            * sp.diff(phi_bg, coords_4d[mu])
            * sp.diff(phi_bg, coords_4d[nu])
            for mu in range(4)
            for nu in range(4)
        )
    )
    Q_tt = sp.simplify(sum(A_tt_up[mu] * sp.diff(phi_bg, coords_4d[mu]) for mu in range(4)))
    assert Y_tt == 0 and Q_tt == Q0
    # Because Y_tt = 0 and Q_tt = Q0 carry ZERO h_plus/h_cross derivatives, F_cov(Y, Q) contributes
    # at most cosmological constant F_cov(0, Q0) * sqrt(-g_tt) (zero on condensate minimum F_cov(0, Q0)=0)
    # and shifts c_T^2 by 0 for EVERY F_cov(Y, Q)!

    # 3B. Quasistatic scalar ghost-freedom & convexity
    # Citations: TARGET_D7:300-308, TARGET_D2:53 (C2), TARGET_D2_SUPPLEMENT:71-74
    u_pos = sp.Symbol("u", positive=True, real=True)
    J_general = 2 * lam_s * a0_tilde**2 * F_D2(sp.sqrt(Y_pos) / a0_tilde)
    Jp_general = sp.simplify(sp.diff(J_general, Y_pos).subs(Y_pos, a0_tilde**2 * u_pos**2))
    longitudinal_general = sp.simplify(
        (sp.diff(J_general, Y_pos) + 2 * Y_pos * sp.diff(J_general, Y_pos, 2)).subs(
            Y_pos, a0_tilde**2 * u_pos**2
        )
    )
    assert sp.simplify(Jp_general - lam_s * sp.diff(F_D2(u_pos), u_pos) / u_pos) == 0
    assert sp.simplify(longitudinal_general - lam_s * sp.diff(F_D2(u_pos), u_pos, 2)) == 0

    # 3C. Explicit verification that an INFINITE FAMILY and distinct non-family witnesses
    #     survive ALL action + consistency + boundary + analyticity conditions simultaneously:
    #     - C1: F(0) = 0 (TARGET_D2:52)
    #     - C2 / Ghost-freedom: F'(x) > 0 and F''(x) = d/dx[x*mu(x)] > 0 for all x > 0
    #       (TARGET_D2:53, TARGET_D7:301-302)
    #     - C3: lim_{x->oo} F(x)/x^2 = 1/2 <=> mu(oo) = 1 (TARGET_D2:54, 115; TARGET_D7:129)
    #     - C4 + mu'(0)=1: lim_{x->0} F(x)/x^3 = 1/3 <=> mu(0)=0, mu'(0)=1 (TARGET_D2:55, 114, 116; TARGET_D7:128)
    #     - C5: Real-analytic at x = 0 (TARGET_D2:56)
    #     - c_T = c (TARGET_D7:339) and Phi = Psi (TARGET_D7:349)

    n_sym = sp.Symbol("n", integer=True, positive=True)
    mu_n_sym = x_pos / (1 + x_pos**n_sym) ** (sp.S.One / n_sym)
    duality_n_check = sp.simplify(
        mu_n_sym**n_sym + (mu_n_sym.subs(x_pos, 1 / x_pos)) ** n_sym
    )
    assert duality_n_check == 1  # MuNDuality.lean:55-56 holds for EVERY integer n >= 1

    d_x_mu_n = sp.simplify(sp.diff(x_pos * mu_n_sym, x_pos))
    expected_d_x_mu_n = x_pos * (2 + x_pos**n_sym) / (1 + x_pos**n_sym) ** (1 + sp.S.One / n_sym)
    assert sp.simplify(d_x_mu_n - expected_d_x_mu_n) == 0

    x_real = sp.Symbol("x_r", real=True)
    candidates = [
        (
            "mu_1 (F_dual, n=1)",
            x_real / (1 + x_real),
            sp.Rational(1, 2) * x_real**2 - x_real + sp.log(1 + x_real),
        ),
        (
            "mu_2 (mu_std, n=2)",
            x_real / sp.sqrt(1 + x_real**2),
            sp.Rational(1, 2) * (x_real * sp.sqrt(1 + x_real**2) - sp.asinh(x_real)),
        ),
        (
            "mu_3 (l^3 member, n=3)",
            x_real / (1 + x_real**3) ** sp.Rational(1, 3),
            None,
        ),
        (
            "mu_4 (l^4 member, n=4)",
            x_real / (1 + x_real**4) ** sp.Rational(1, 4),
            None,
        ),
        (
            "mu_exp (non-l^n analytic)",
            1 - sp.exp(-x_real),
            sp.Rational(1, 2) * x_real**2 - 1 + (x_real + 1) * sp.exp(-x_real),
        ),
        (
            "mu_tanh (non-l^n analytic)",
            sp.tanh(x_real),
            None,
        ),
    ]

    surviving_witnesses = []
    for label, mu_expr_r, F_closed_r in candidates:
        mu_0 = sp.simplify(mu_expr_r.subs(x_real, 0))
        dmu_0 = sp.simplify(sp.diff(mu_expr_r, x_real).subs(x_real, 0))
        mu_xp = mu_expr_r.subs(x_real, x_pos)
        mu_inf = sp.limit(mu_xp, x_pos, sp.oo)
        Fpp_xp = sp.simplify(sp.diff(x_pos * mu_xp, x_pos))

        # Taylor series of x * mu(x) at x = 0 confirms analyticity (C5) and F(x) = x^3/3 + O(x^4) (C1, C4)
        integrand_series = sp.series(x_real * mu_expr_r, x_real, 0, 6).removeO()
        F_series_0 = sp.integrate(integrand_series, x_real)
        c1_val = sp.simplify(F_series_0.subs(x_real, 0))
        c4_val = sp.limit(F_series_0 / x_real**3, x_real, 0)
        # By L'Hopital: lim_{x->oo} (int_0^x t*mu(t) dt) / x^2 = lim_{x->oo} (x*mu(x)) / (2*x) = mu(oo)/2
        if F_closed_r is not None:
            F_xp = F_closed_r.subs(x_real, x_pos)
            assert sp.simplify(sp.diff(F_xp, x_pos) - x_pos * mu_xp) == 0
            c3_val = sp.limit(F_xp / x_pos**2, x_pos, sp.oo)
        else:
            c3_val = sp.Rational(1, 2) * mu_inf

        # Sample positivity of mu(x) and F''(x) = (x*mu(x))' across (0, oo)
        pos_samples = all(
            float(mu_xp.subs(x_pos, v)) > 0 and float(Fpp_xp.subs(x_pos, v)) > 0
            for v in (sp.Rational(1, 10), sp.S.One, sp.Integer(10))
        )
        assert mu_0 == 0 and dmu_0 == 1 and mu_inf == 1
        assert c1_val == 0 and c4_val == sp.Rational(1, 3) and c3_val == sp.Rational(1, 2)
        assert pos_samples

        surviving_witnesses.append(
            {
                "name": label,
                "mu_x": str(mu_xp),
                "F_double_prime_x": str(Fpp_xp),
                "mu_0": int(mu_0),
                "mu_prime_0": int(dmu_0),
                "mu_inf": int(mu_inf),
                "C1_F0_eq_0": True,
                "C2_ghost_free_Fpp_pos": True,
                "C3_F_over_x2_inf": str(c3_val),
                "C4_F_over_x3_zero": str(c4_val),
                "C5_real_analytic_at_0": True,
                "c_T_eq_c": True,
                "Phi_eq_Psi": True,
            }
        )

    # =========================================================================
    # 4. NAMED FAMILY REDUCTIONS IN SUPPLEMENT / D2 ARE EXTERNAL INPUTS,
    #    NOT CONSEQUENCES OF THE ACTION
    #    Citations:
    #    - TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md:145-172 (Theorems B, C, D)
    #    - TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md:190-195, 234-249, 376 (§5, §6)
    #    - TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:230-255 (Theorem 9.3, Q1'-Q3)
    # =========================================================================
    m_sym = sp.Symbol("m", positive=True, real=True)
    k_exp = sp.Symbol("k", positive=True, real=True)
    # Theorem C (TARGET_D2_SUPPLEMENT:158): F'(x)^2 * I_pm(mu) = x^k with F'(x)=x*mu, I_pm(m)=1/(1-m^2)
    eq_thm_C = sp.Eq((x_pos * m_sym) ** 2 / (1 - m_sym**2), x_pos**k_exp)
    sol_thm_C = [s for s in sp.solve(eq_thm_C, m_sym) if sp.simplify(s.subs({x_pos: 2, k_exp: 4})) > 0]
    assert len(sol_thm_C) == 1
    mu_thm_C = sp.simplify(sol_thm_C[0])
    expected_mu_thm_C = x_pos ** ((k_exp - 2) / 2) / sp.sqrt(1 + x_pos ** (k_exp - 2))
    assert sp.simplify(mu_thm_C**2 - expected_mu_thm_C**2) == 0
    assert sp.simplify(mu_thm_C.subs(k_exp, 4) - x_pos / sp.sqrt(1 + x_pos**2)) == 0

    # Theorem 9.3 (TARGET_D2:231): F'(x)^2 * I_Bern(mu) = x^{n+2} with I_Bern(p)=1/(p*(1-p))
    eq_thm_93 = sp.Eq((x_pos * m_sym) ** 2 / (m_sym * (1 - m_sym)), x_pos ** (n_sym + 2))
    sol_thm_93 = sp.solve(eq_thm_93, m_sym)[0]
    assert sp.simplify(sol_thm_93 - x_pos**n_sym / (1 + x_pos**n_sym)) == 0

    # Reparametrization non-invariance (TARGET_D2_SUPPLEMENT:190-195):
    # For ANY invertible mu(x), defining I_u(mu) := x(mu)^{k-2} / mu^2 makes F'(x)^2 * I_u(mu) = x^k tautological:
    reparam_identity = sp.simplify((x_pos * m_sym) ** 2 * (x_pos ** (k_exp - 2) / m_sym**2) - x_pos**k_exp)
    assert reparam_identity == 0

    # =========================================================================
    # 5. PRINT DERIVATION SUMMARY & WRITE JSON RECEIPT
    # =========================================================================
    receipt = {
        "exit_code": 0,
        "verdict": "Q3 remains [O]",
        "does_covariant_action_force_mu_std": False,
        "killing_step_from_action": None,
        "general_allowed_mu": {
            "aqual_variation_only": {
                "action": "S = -(a0^2 / 8*pi*G) * int F_kin(Y) d^3x - int rho*Phi d^3x, Y = |grad Phi|^2 / a0^2 = x^2",
                "d2_convention_relation": "F_kin(Y) = 2 * F_D2(sqrt(Y)), F_D2'(x) = x * mu(x)",
                "euler_lagrange": "div[ (dF_kin/dY) * grad Phi ] = 4*pi*G*rho",
                "literal_d2_line_100_without_factor_2": "div[ (F_D2'(x)/x) * grad Phi ] = 8*pi*G*rho (TARGET_D7_COVARIANT_COMPLETION.md:97-104)",
                "most_general_mu": "mu(x) = dF_kin/dY |_{Y=x^2} = F_D2'(x) / x for arbitrary F_kin in C^2((0, oo))",
            },
            "aest_covariant_variation": {
                "citation": "TARGET_D7_COVARIANT_COMPLETION.md:38-48, 70, 80-94, 103-107, 128-139",
                "free_bivariate_function": "F_cov(Y, Q) in C^2, with quasistatic slice J(Y) := F_cov(Y, Q0) / (2 - K_B)",
                "weak_field_metric_slip": "Phi = Psi identically for all F_cov(Y, Q) (gamma_PPN = 1)",
                "quasistatic_euler_lagrange": [
                    "nabla^2 Phi_hat = 4*pi*G_hat*rho",
                    "div[ J'(Y) * grad varphi ] = 4*pi*G_hat*rho, Y = |grad varphi|^2, Phi = Phi_hat + varphi",
                ],
                "scalar_channel_mu": "mu_varphi(u) = J'(a0_tilde^2 * u^2) / lambda_s = F'(u) / u, u = |grad varphi| / a0_tilde",
                "curl_free_total_mu_implicit": "g = g_hat + g_varphi, J'(g_varphi^2)*g_varphi = g_hat = (lambda_s/(1+lambda_s))*g_N, mu_tot(g/a0) = g_N / g",
            },
            "after_all_cited_action_and_boundary_conditions": {
                "admissible_class": (
                    "mu(x) = F'(x)/x for ANY F in C^omega([0, oo)) cap C^2((0, oo)) with "
                    "F(0)=0, F'(0)=0, F''(0)=0, F'''(0)=2 (so mu(0)=0, mu'(0)=1, F(x)/x^3 -> 1/3), "
                    "F''(x) = d/dx[x*mu(x)] > 0 and F'(x) > 0 for all x > 0 (ghost-freedom / C2), "
                    "and lim_{x->oo} F'(x)/x = 1 (so mu(oo)=1, F(x)/x^2 -> 1/2)."
                ),
                "infinite_dimensional": True,
            },
        },
        "condition_by_condition_audit": [
            {
                "condition": "Covariant / quasistatic Euler-Lagrange variation",
                "citation": "TARGET_D7_COVARIANT_COMPLETION.md:38-40, 84-90; TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:86, 100-104",
                "kills_rivals_to_mu_std": False,
                "survivors": "All C^2 free functions F_cov(Y, Q) / J(Y) / F_D2(x)",
            },
            {
                "condition": "Luminal gravitational-wave speed c_T = c",
                "citation": "TARGET_D7_COVARIANT_COMPLETION.md:329-341, 410",
                "measured_c_T_squared": str(c_T_sq),
                "kills_rivals_to_mu_std": False,
                "survivors": "Every F_cov(Y, Q) identically (Y=0, Q=Q0 on background carry zero TT spin-2 derivatives)",
            },
            {
                "condition": "Weak-field lensing potential equality Phi = Psi (gamma_PPN = 1)",
                "citation": "TARGET_D7_COVARIANT_COMPLETION.md:80-82, 349-352, 411",
                "kills_rivals_to_mu_std": False,
                "survivors": "Every F_cov(Y, Q) identically",
            },
            {
                "condition": "Quasistatic scalar ghost-freedom J'(Y) > 0 and J'(Y) + 2*Y*J''(Y) > 0 (C2: F''(x) > 0)",
                "citation": "TARGET_D7_COVARIANT_COMPLETION.md:300-308; TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:53; TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md:71-74",
                "kills_rivals_to_mu_std": False,
                "survivors": "Infinite-dimensional open convex cone {mu(x) > 0, d/dx[x*mu(x)] > 0 on (0, oo)}",
            },
            {
                "condition": "Boundary & regularity conditions C1, C3, C4, C5 and mu(0)=0, mu(oo)=1, mu'(0)=1 (plus x -> 1/x duality)",
                "citation": "TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:52-56, 70-78, 114-116; TARGET_D7_COVARIANT_COMPLETION.md:128-136; 05_lean_formalization/MuNDuality.lean:42-60",
                "kills_rivals_to_mu_std": False,
                "survivors": "Infinite-dimensional real-analytic convex family including mu_n(x) = x/(1+x^n)^(1/n) for all integers n >= 1, 1 - exp(-x), tanh(x)",
            },
        ],
        "external_postulate_family_reductions_not_from_action": [
            {
                "condition": "Chiral Fisher identity F'(x)^2 * I_pm(mu) = x^k under Postulate R (I_pm(m) = 1/(1-m^2))",
                "citation": "TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md:107-110, 145-167, 190-195, 234-249, 376",
                "status": "External input postulate [O]/[C], NOT a consequence of the action",
                "reduced_family": "mu_k(x) = x^((k-2)/2) / sqrt(1 + x^(k-2)); mu'(0)=1 selects k=4 -> x/sqrt(1+x^2)",
            },
            {
                "condition": "Bernoulli Fisher identity F'(x)^2 * I(mu) = x^(n+2) / Pade [1/1] minimality",
                "citation": "TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:112-116, 230-255",
                "status": "External input postulate [O], NOT a consequence of the action",
                "reduced_family": "mu_n(x) = x^n / (1 + x^n); mu'(0)=1 selects n=1 -> x/(1+x)",
            },
        ],
        "banned_moves_excluded": {
            "wrong_normalization_sqrt_1_plus_x2_minus_1": {
                "citation": "TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md:52-62",
                "dF_dx_over_x": str(mu_from_F_wrong),
                "C3_limit_F_over_x2_inf": str(c3_wrong),
                "C4_limit_F_over_x3_zero": str(c4_wrong),
                "used_as_aqual_candidate": False,
            },
            "milgrom_1999_modified_inertia_merged": False,
            "retracted_sinh_psi_eq_1_gate_used": False,
            "empirical_cassini_or_sparc_fit_used_to_select": False,
        },
        "verified_surviving_witnesses": surviving_witnesses,
    }

    out_json = pathlib.Path(
        "/home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/q3_action_forces_mu.json"
    )
    out_json.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    print("AQUAL_EL_Y: div[ (dF_kin/dY) * grad(Phi) ] = 4*pi*G*rho, Y = |grad(Phi)|^2 / a0^2")
    print("AQUAL_D2_RELATION: F_kin(Y) = 2 * F_D2(sqrt(Y)), mu(x) = dF_kin/dY = F_D2'(x) / x")
    print("AEST_WEAK_FIELD_SLIP: Phi = Psi (for every F_cov(Y, Q))")
    print("AEST_QS_EL_1: nabla^2(Phi_hat) = 4*pi*G_hat*rho")
    print("AEST_QS_EL_2: div[ J'(Y) * grad(varphi) ] = 4*pi*G_hat*rho, J(Y) = F_cov(Y, Q0)/(2 - K_B)")
    print("C_T_SQUARED: 1 (for every F_cov(Y, Q))")
    print("GHOST_FREEDOM: J'(Y) = lambda_s * mu_varphi(u) > 0, J'(Y) + 2*Y*J''(Y) = lambda_s * d/du[u*mu_varphi(u)] > 0")
    print(
        "GENERAL_MU_ALLOWED: mu(x) = F'(x)/x for any real-analytic F on [0, oo) with F(0)=0, "
        "F'(0)=0, F''(0)=0, F'''(0)=2, F''(x) > 0 for all x > 0, and lim_{x->oo} F'(x)/x = 1 "
        "(surviving examples: mu_n(x) = x/(1+x^n)^(1/n) for every integer n >= 1, 1 - exp(-x), tanh(x))"
    )
    print("FREE_FUNCTION_LEFT_BY_VARIATION: F_cov(Y, Q) -> quasistatic slice J(Y) = F_cov(Y, Q0)/(2 - K_B) = 2*lambda_s*a0_tilde^2*F(sqrt(Y)/a0_tilde)")
    print("EXTERNAL_INPUT_FAMILY_1 (not from action, TARGET_D2_SUPPLEMENT:158): F'(x)^2 * I_pm(mu) = x^k => mu_k(x) = x^((k-2)/2)/sqrt(1 + x^(k-2))")
    print("EXTERNAL_INPUT_FAMILY_2 (not from action, TARGET_D2:231): F'(x)^2 * I(mu) = x^(n+2) => mu_n(x) = x^n/(1 + x^n)")
    print("Q3 remains [O]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
