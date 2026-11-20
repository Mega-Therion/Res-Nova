#!/usr/bin/env python3
"""One-sheet SymPy Jacobian split (J_sym = (J+J^T)/2, J_anti = (J-J^T)/2)
and D56 Jordan classification audit across the live Chyren / Res-Nova stack.

Checks:
  J1  ITT/AQUAL scalar kinetic Hessian J^{mu nu} := d^2 f(y) / (dv_mu dv_nu)
      plus explicit disformal metric check (noting RN-GEA-RETIRED-001).
  J2  Live AeST aether gradient J_{mu nu} := nabla_mu A_nu, F_{mu nu} isolation,
      and specialization to the dark-bubble bulk-Killing unit covector u_mu = -N d_mu T.
  J3  D56 invariant audit: H_4(R) = Sym^2(R^4) (rank 4, quartic det) vs
      H_2(O) ~ R^{1,9} (rank 2, quadratic norm), closing [X] the antisymmetric-piece guess.
  J4  3D Navier-Stokes velocity gradient J_{ij} = d_j u_i split into strain S and vorticity Omega.
"""
from __future__ import annotations

import json
import os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def check_j1_itt_aqual_hessian() -> dict:
    # General 4D symmetric inverse metric g^{ab} and covariant gradient v_a = d_a chi
    ell = sp.Symbol("ell", positive=True)
    v = list(sp.symbols("v0 v1 v2 v3", real=True))
    g_inv = sp.Matrix(
        4,
        4,
        lambda i, j: sp.Symbol(f"ginv_{min(i, j)}{max(i, j)}", real=True),
    )
    assert g_inv - g_inv.T == sp.zeros(4, 4)

    y_expr = ell**2 * (sp.Matrix(v).T * g_inv * sp.Matrix(v))[0]
    f_fn = sp.Function("f")
    f_val = f_fn(y_expr)

    # J^{mu nu} := d^2 f / (d v_mu d v_nu)
    J_up = sp.Matrix(4, 4, lambda mu, nu: sp.simplify(sp.diff(f_val, v[mu], v[nu])))
    J_sym = sp.simplify((J_up + J_up.T) / 2)
    J_anti = sp.simplify((J_up - J_up.T) / 2)
    assert J_anti == sp.zeros(4, 4)

    # Compare against expected disformal acoustic metric 2 ell^2 [f'(y) g^{mu nu} + 2 ell^2 f''(y) v^mu v^nu]
    v_up = g_inv * sp.Matrix(v)
    fp = sp.diff(f_fn(sp.Symbol("y_dummy")), sp.Symbol("y_dummy")).subs(sp.Symbol("y_dummy"), y_expr)
    fpp = sp.diff(f_fn(sp.Symbol("y_dummy")), sp.Symbol("y_dummy"), 2).subs(sp.Symbol("y_dummy"), y_expr)
    expected = 2 * ell**2 * (fp * g_inv + 2 * ell**2 * fpp * (v_up * v_up.T))
    assert sp.simplify(J_sym - expected) == sp.zeros(4, 4)

    # Check explicit f_std(y) = sqrt(y*(1+y)) - asinh(sqrt(y)) and Postulate R y -> 0+ blow-up
    y = sp.Symbol("y", positive=True)
    x = sp.Symbol("x", positive=True)
    f_std = sp.sqrt(y * (1 + y)) - sp.asinh(sp.sqrt(y))
    fp_std = sp.simplify(sp.diff(f_std, y))
    fpp_std = sp.simplify(sp.diff(f_std, y, 2))
    mu_from_f = sp.simplify(fp_std.subs(y, x**2))
    mu_std = x / sp.sqrt(1 + x**2)
    assert sp.simplify(mu_from_f - mu_std) == 0
    assert sp.simplify(fpp_std - 1 / (2 * sp.sqrt(y) * (1 + y) ** sp.Rational(3, 2))) == 0
    fpp_lim_0 = sp.limit(fpp_std, y, 0, "+")
    assert fpp_lim_0 == sp.oo

    # Explicit ITT disformal metric g_tilde_{mu nu} = g_{mu nu} + 2 ell^2 v_mu v_nu
    g_cov = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"g_{min(i, j)}{max(i, j)}", real=True))
    g_tilde = g_cov + 2 * ell**2 * (sp.Matrix(v) * sp.Matrix(v).T)
    assert sp.simplify((g_tilde - g_tilde.T) / 2) == sp.zeros(4, 4)

    return {
        "J_anti_identically_zero": True,
        "J_sym_form": "2*ell^2 * (f'(y)*g^{mu nu} + 2*ell^2*f''(y)*v^mu*v^nu) (acoustic disformal metric, NOT c*g^{mu nu})",
        "f_std_prime_at_x2_equals_mu_std": True,
        "f_std_double_prime": str(fpp_std),
        "f_std_double_prime_limit_y_0plus": str(fpp_lim_0),
        "disformal_g_tilde_antisym_zero": True,
        "canon_scope_note": "ITT disformal matter coupling is retired [X] in Res-Nova (RN-GEA-RETIRED-001); live AeST couples matter minimally to g_{mu nu}.",
    }


def check_j2_aest_aether_gradient() -> dict:
    # Arbitrary 4x4 covariant gradient J_{mu nu} := nabla_mu A_nu and symmetric metric inverse
    J = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"J_{i}{j}", real=True))
    S = (J + J.T) / 2
    A = (J - J.T) / 2
    F = J - J.T  # F_{mu nu} = nabla_mu A_nu - nabla_nu A_mu = 2 A_{mu nu}
    assert sp.simplify(F - 2 * A) == sp.zeros(4, 4)

    g_inv = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"ginv_{min(i, j)}{max(i, j)}", real=True))
    KB = sp.Symbol("K_B", real=True)
    # Kinetic term -(K_B / 2) F_{mu nu} F^{mu nu} = -(K_B / 2) sum g^{mu alpha} g^{nu beta} F_{mu nu} F_{alpha beta}
    F_up = g_inv * F * g_inv
    L_F = -sp.Rational(1, 2) * KB * sum(F[mu, nu] * F_up[mu, nu] for mu in range(4) for nu in range(4))
    A_up = g_inv * A * g_inv
    L_A = -2 * KB * sum(A[mu, nu] * A_up[mu, nu] for mu in range(4) for nu in range(4))
    assert sp.simplify(L_F - L_A) == 0

    # Verify explicitly in terms of independent (S_{ij}, A_{ij}) symbols that L_F has zero S dependence
    S_sym = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"S_{min(i, j)}{max(i, j)}", real=True))
    A_sym = sp.Matrix(
        4,
        4,
        lambda i, j: 0 if i == j else (sp.Symbol(f"A_{i}{j}", real=True) if i < j else -sp.Symbol(f"A_{j}{i}", real=True)),
    )
    J_decomp = S_sym + A_sym
    F_decomp = J_decomp - J_decomp.T
    L_decomp = -sp.Rational(1, 2) * KB * sum(
        F_decomp[mu, nu] * (g_inv * F_decomp * g_inv)[mu, nu] for mu in range(4) for nu in range(4)
    )
    s_vars = {S_sym[i, j] for i in range(4) for j in range(i, 4)}
    assert s_vars.isdisjoint(sp.expand(L_decomp).free_symbols)

    # Specialize to hypersurface-orthogonal unit timelike covector u_mu = -N d_mu T (dark-bubble Killing frame)
    # in Conformal Newtonian gauge coordinates (t, x, y, z) to O(eps)
    t, x, y, z, eps = sp.symbols("t x y z eps", real=True)
    coords = [t, x, y, z]
    a = sp.Function("a", positive=True)(t)
    Phi = sp.Function("Phi")(x, y, z)
    Psi = sp.Function("Psi")(x, y, z)

    g_cn = sp.diag(-(a**2) * (1 + 2 * eps * Phi), a**2 * (1 - 2 * eps * Psi), a**2 * (1 - 2 * eps * Psi), a**2 * (1 - 2 * eps * Psi))
    ginv_cn = g_cn.inv()
    u_cov = sp.Matrix([-a * (1 + eps * Phi), 0, 0, 0])  # u_mu = -N d_mu t
    norm_u = sp.series((u_cov.T * ginv_cn * u_cov)[0], eps, 0, 2).removeO()
    assert sp.simplify(norm_u + 1) == 0  # u_mu u^mu = -1 + O(eps^2)

    # F_{mu nu} = d_mu u_nu - d_nu u_mu (Christoffels cancel in antisymmetrized covariant derivative)
    F_cn = sp.Matrix(4, 4, lambda mu, nu: sp.simplify(sp.diff(u_cov[nu], coords[mu]) - sp.diff(u_cov[mu], coords[nu])))
    # Spatial vorticity vanishes identically (Frobenius hypersurface-orthogonality)
    assert F_cn[1:, 1:] == sp.zeros(3, 3)
    # Background (eps = 0) gives F_{mu nu} = 0 identically
    assert F_cn.subs(eps, 0) == sp.zeros(4, 4)
    # Perturbed (eps != 0) gives electric component F_{0i} = eps * a * d_i Phi
    grad_Phi = [sp.diff(Phi, coords[i]) for i in (1, 2, 3)]
    for idx_i in range(3):
        assert sp.simplify(F_cn[0, idx_i + 1] - eps * a * grad_Phi[idx_i]) == 0

    # Verify covariant identity F_{mu nu} = u_nu a_mu - u_mu a_nu to O(eps) where a_mu = u^alpha nabla_alpha u_mu
    u_up = sp.Matrix([sp.series((ginv_cn * u_cov)[i], eps, 0, 2).removeO() for i in range(4)])
    Gam = [
        [
            [
                sp.series(
                    sum(
                        ginv_cn[lam, rho]
                        * (
                            sp.diff(g_cn[rho, mu], coords[nu])
                            + sp.diff(g_cn[rho, nu], coords[mu])
                            - sp.diff(g_cn[mu, nu], coords[rho])
                        )
                        / 2
                        for rho in range(4)
                    ),
                    eps,
                    0,
                    2,
                ).removeO()
                for nu in range(4)
            ]
            for mu in range(4)
        ]
        for lam in range(4)
    ]
    a_cov = sp.Matrix(
        [
            sp.series(
                sum(
                    u_up[alp] * (sp.diff(u_cov[mu], coords[alp]) - sum(Gam[lam][alp][mu] * u_cov[lam] for lam in range(4)))
                    for alp in range(4)
                ),
                eps,
                0,
                2,
            ).removeO()
            for mu in range(4)
        ]
    )
    F_from_acc = sp.Matrix(4, 4, lambda mu, nu: sp.series(u_cov[nu] * a_cov[mu] - u_cov[mu] * a_cov[nu], eps, 0, 2).removeO())
    assert sp.simplify(F_cn - F_from_acc) == sp.zeros(4, 4)

    F2_cn = sp.series(sum(F_cn[mu, nu] * (ginv_cn * F_cn * ginv_cn)[mu, nu] for mu in range(4) for nu in range(4)), eps, 0, 3).removeO()
    grad_sq = sum(g**2 for g in grad_Phi)
    assert sp.simplify(F2_cn + 2 * eps**2 * grad_sq / a**2) == 0

    return {
        "L_KB_depends_only_on_antisym": True,
        "S_vars_absent_from_L_KB": True,
        "hypersurface_orthogonal_u_norm": "u_mu u^mu = -1 + O(eps^2)",
        "spatial_vorticity_Fij_zero": True,
        "background_F_identically_zero": True,
        "linear_F0i": "eps * a(t) * d_i Phi",
        "covariant_identity_F_equals_u_wedge_a": "F_{mu nu} = u_nu a_mu - u_mu a_nu (verified to O(eps))",
        "F_sq_leading_order": str(sp.simplify(F2_cn)),
    }


def check_j3_d56_classification() -> dict:
    # H_4(R) = Sym^2(R^4): 10-parameter symmetric 4x4 matrix
    lam = sp.Symbol("lam", real=True)
    m_syms = sp.symbols("m00 m01 m02 m03 m11 m12 m13 m22 m23 m33", real=True)
    M = sp.Matrix(
        [
            [m_syms[0], m_syms[1], m_syms[2], m_syms[3]],
            [m_syms[1], m_syms[4], m_syms[5], m_syms[6]],
            [m_syms[2], m_syms[5], m_syms[7], m_syms[8]],
            [m_syms[3], m_syms[6], m_syms[8], m_syms[9]],
        ]
    )
    assert (M - M.T) / 2 == sp.zeros(4, 4)
    det_M = M.det()
    det_lam_M = (lam * M).det()
    assert sp.simplify(det_lam_M - lam**4 * det_M) == 0

    # H_2(O) ~ R^{1,9}: 10-parameter Jordan norm N_2 = a*b - sum_{i=0}^7 x_i^2
    a, b = sp.symbols("a b", real=True)
    xs = list(sp.symbols("x0:8", real=True))
    h2_vars = [a, b] + xs
    N2 = a * b - sum(xi**2 for xi in xs)
    N2_lam = N2.subs({v: lam * v for v in h2_vars})
    assert sp.simplify(N2_lam - lam**2 * N2) == 0

    H_N2 = sp.hessian(N2, h2_vars)
    assert H_N2 - H_N2.T == sp.zeros(10, 10)
    eigs = H_N2.eigenvals()
    assert eigs == {sp.Integer(1): 1, sp.Integer(-1): 1, sp.Integer(-2): 8}
    pos_count = sum(mult for val, mult in eigs.items() if val > 0)
    neg_count = sum(mult for val, mult in eigs.items() if val < 0)
    assert (pos_count, neg_count) == (1, 9)

    return {
        "H4R_antisymmetric_part_zero": True,
        "H4R_det_degree": 4,
        "H2O_norm_degree": 2,
        "H2O_hessian_eigenvalues": {str(k): int(v) for k, v in eigs.items()},
        "H2O_signature": [pos_count, neg_count],
        "youtube_brainstorm_antisym_guess_verdict": "[X] Neither 10-space is antisymmetric; rank/norm degree (4 vs 2) separates H_4(R) from H_2(O).",
    }


def check_j4_navier_stokes_velgrad() -> dict:
    x, y, z = sp.symbols("x y z", real=True)
    coords = [x, y, z]
    u = [sp.Function(f"u{i}")(x, y, z) for i in range(3)]
    J = sp.Matrix(3, 3, lambda i, j: sp.diff(u[i], coords[j]))
    S = (J + J.T) / 2
    Om = (J - J.T) / 2
    div_u = sum(sp.diff(u[i], coords[i]) for i in range(3))
    assert sp.simplify(S.trace() - div_u) == 0
    # curl u
    omega = [
        sp.diff(u[2], y) - sp.diff(u[1], z),
        sp.diff(u[0], z) - sp.diff(u[2], x),
        sp.diff(u[1], x) - sp.diff(u[0], y),
    ]
    eps_tensor = [[[int(sp.LeviCivita(i, j, k)) for k in range(3)] for j in range(3)] for i in range(3)]
    Om_from_curl = sp.Matrix(
        3,
        3,
        lambda i, j: -sp.Rational(1, 2) * sum(eps_tensor[i][j][k] * omega[k] for k in range(3)),
    )
    assert sp.simplify(Om - Om_from_curl) == sp.zeros(3, 3)
    return {
        "S_trace_equals_div_u": True,
        "Omega_equals_minus_half_eps_omega": True,
    }


def main() -> int:
    res = {
        "J1_itt_aqual_hessian": check_j1_itt_aqual_hessian(),
        "J2_aest_aether_gradient": check_j2_aest_aether_gradient(),
        "J3_d56_classification": check_j3_d56_classification(),
        "J4_navier_stokes_velgrad": check_j4_navier_stokes_velgrad(),
    }
    out_path = os.path.join(HERE, "JACOBIAN_SPLIT_AND_D56_AUDIT.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
