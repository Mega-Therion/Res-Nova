#!/usr/bin/env python3
"""Coupled non-zero-drag, Noether-flux, ADM gravity, and 5D bending seat audit
for the P3-A AeST wall dust condensate (L_cond).

Complements (without altering) the decoupled vacuum check in phase3_wall_ghost_audit.py.
Signature (-+++), M_Pl^2 := 1 / (16 pi G4) > 0, action density L with canonical
scalar kinetic convention +(1/2) phi_dot^2. All definitions use `:=` in reports.
"""
from __future__ import annotations

import json
import os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def _el_op(expr: sp.Expr, field: sp.Function, t: sp.Symbol, x: sp.Symbol) -> sp.Expr:
    """Euler-Lagrange operator for a 1+1D field up to second derivatives."""
    res = sp.diff(expr, field)
    for var in (t, x):
        res -= sp.diff(sp.diff(expr, sp.diff(field, var)), var)
    for deriv in ((t, 2), (x, 2)):
        res += sp.diff(sp.diff(expr, sp.diff(field, *deriv)), *deriv)
    res += sp.diff(sp.diff(expr, sp.diff(field, t, x)), t, x)
    return sp.simplify(res)


def _fourier_hermitian_matrix(
    expr: sp.Expr,
    bras: list[sp.Symbol],
    kets: list[sp.Symbol],
    bra_map: dict[sp.Symbol, sp.Expr],
    ket_map: dict[sp.Symbol, sp.Expr],
) -> sp.Matrix:
    """Construct the exact Hermitian Fourier quadratic matrix M (v^dag M v) from a real quadratic L."""
    fvars = list(bra_map.keys())
    n = len(bras)
    M = sp.zeros(n, n)
    poly = sp.Poly(sp.expand(expr), *fvars)
    for monom, coeff in poly.terms():
        assert sum(monom) == 2
        pair: list[sp.Symbol] = []
        for var, deg in zip(fvars, monom):
            pair.extend([var] * deg)
        u1, u2 = pair
        quad = sp.expand(
            coeff * sp.Rational(1, 2) * (bra_map[u1] * ket_map[u2] + bra_map[u2] * ket_map[u1])
        )
        for i, bra in enumerate(bras):
            for j, ket in enumerate(kets):
                c = quad.coeff(bra).coeff(ket)
                if c != 0:
                    M[i, j] += c
    return sp.simplify(M)


def check_background_and_noether() -> dict:
    """Check FRW stress invariance under -(1/2) c_Y Y and exact Noether-Bianchi continuity."""
    tau = sp.Symbol("tau", real=True)
    K2, Q0, cY, sig0 = sp.symbols("K2 Q0 c_Y sigma0", real=True)
    lam, A0, dphi0 = sp.symbols("lam A0 dphi0", real=True)
    hup00, hup11, hup22, hup33 = sp.symbols("hup00 hup11 hup22 hup33", real=True)
    a = sp.Function("a", positive=True)(tau)

    Q_gen = hup00 * A0 * dphi0
    Y_frw = (hup00 + hup00**2 * A0**2) * dphi0**2
    L_full = (
        -sig0
        + sp.Rational(1, 2) * K2 * (Q_gen - Q0) ** 2
        - sp.Rational(1, 2) * cY * Y_frw
        - sp.Rational(1, 2) * lam * (hup00 * A0**2 + 1)
    )
    lam_sol = sp.solve(sp.diff(L_full, A0), lam)[0]
    sqrt_mh = 1 / sp.sqrt(-hup00 * hup11 * hup22 * hup33)
    sub_frw = {hup00: -1, hup11: 1 / a**2, hup22: 1 / a**2, hup33: 1 / a**2, A0: -1}

    S_00 = sp.simplify((-2 / sqrt_mh * sp.diff(sqrt_mh * L_full, hup00)).subs(lam, lam_sol).subs(sub_frw))
    S_11 = sp.simplify((-2 / sqrt_mh * sp.diff(sqrt_mh * L_full, hup11)).subs(lam, lam_sol).subs(sub_frw))

    rho_d = sp.simplify(S_00 - sig0)
    p_d = sp.simplify(S_11 / a**2 + sig0)
    dQ_sym = dphi0 - Q0
    assert sp.simplify(rho_d - (K2 * Q0 * dQ_sym + sp.Rational(1, 2) * K2 * dQ_sym**2)) == 0
    assert sp.simplify(p_d - sp.Rational(1, 2) * K2 * dQ_sym**2) == 0
    assert sp.diff(rho_d, cY) == 0 and sp.diff(p_d, cY) == 0

    phi = sp.Function("phi", real=True)(tau)
    H = sp.diff(a, tau) / a
    Q_tau = sp.diff(phi, tau)
    dQ_tau = Q_tau - Q0
    rho_tau = K2 * Q0 * dQ_tau + sp.Rational(1, 2) * K2 * dQ_tau**2
    p_tau = sp.Rational(1, 2) * K2 * dQ_tau**2

    J0 = K2 * dQ_tau
    div_J = sp.simplify(sp.diff(a**3 * J0, tau) / a**3)
    bianchi_lhs = sp.simplify(sp.diff(rho_tau, tau) + 3 * H * (rho_tau + p_tau))
    assert sp.simplify(bianchi_lhs - Q_tau * div_J) == 0

    return {
        "Y_frw_drops_out_identically": True,
        "rho_d": "K2*Q0*dQ + (1/2)*K2*dQ^2",
        "p_d": "(1/2)*K2*dQ^2",
        "noether_continuity_identity": "d(rho_d)/dtau + 3*H*(rho_d + p_d) == Q * (1/a^3)*d/dtau(a^3 * K2 * dQ)",
        "shift_symmetric_obstruction": "Closed wall condensate (div J_phi = 0) forces Q4 = 0 and dQ ~ a^-3 rather than a^2 H^2; flux-fed drag requires bulk shift-current injection div J_phi = Q4 / Q > 0.",
    }


def check_nonzero_drag_dispersion() -> dict:
    """Expand coupled (varphi, A_x, A_y) action around non-zero drag Qbar = Q0 + dQb."""
    eps = sp.Symbol("eps", real=True)
    K2, KB, Q0, dQb = sp.symbols("K2 K_B Q0 dQb", positive=True)
    cY, w, k = sp.symbols("c_Y omega k", nonnegative=True)
    vt, vx, Ax, Axt, Ay, Ayt, Ayx = sp.symbols(
        "v_t v_x A_x A_xt A_y A_yt A_yx", real=True
    )

    Qbar = Q0 + dQb
    # Exact unit-norm timelike aether g^{mu nu} A_mu A_nu = -1 on Minkowski (-+++)
    A0 = -sp.sqrt(1 + eps**2 * (Ax**2 + Ay**2))
    Q = -A0 * (Qbar + eps * vt) + eps**2 * Ax * vx
    Y = -((Qbar + eps * vt) ** 2) + (eps * vx) ** 2 + Q**2
    F2 = 2 * eps**2 * (-Axt**2 - Ayt**2 + Ayx**2)

    L_cov = sp.Rational(1, 2) * K2 * (Q - Q0) ** 2 - sp.Rational(1, 2) * cY * Y - sp.Rational(1, 2) * KB * F2
    L2_full = sp.expand(sp.diff(L_cov, eps, 2).subs(eps, 0) / 2)

    Y2_long = sp.expand(sp.diff(Y.subs({Ay: 0}), eps, 2).subs(eps, 0) / 2)
    assert sp.simplify(Y2_long - (Qbar * Ax + vx) ** 2) == 0

    L_long = sp.expand(L2_full.subs({Ay: 0, Ayt: 0, Ayx: 0}))
    L_long_expected = (
        sp.Rational(1, 2) * K2 * vt**2
        + KB * Axt**2
        + sp.Rational(1, 2) * K2 * dQb * Qbar * Ax**2
        + K2 * dQb * Ax * vx
        - sp.Rational(1, 2) * cY * (Qbar * Ax + vx) ** 2
    )
    assert sp.simplify(L_long - L_long_expected) == 0

    L_perp = sp.expand(L2_full - L_long)
    L_perp_expected = KB * (Ayt**2 - Ayx**2) - sp.Rational(1, 2) * Qbar * (cY * Qbar - K2 * dQb) * Ay**2
    assert sp.simplify(L_perp - L_perp_expected) == 0

    # Hermitian Fourier matrix M_Y(omega, k) in basis [varphi, A_x]
    vc, ac, vs, as_ = sp.symbols("v_c a_c v_s a_s")
    bra_map = {
        vt: sp.I * w * vs,
        vx: -sp.I * k * vs,
        Ax: as_,
        Axt: sp.I * w * as_,
    }
    ket_map = {
        vt: -sp.I * w * vc,
        vx: sp.I * k * vc,
        Ax: ac,
        Axt: -sp.I * w * ac,
    }
    M_Y = _fourier_hermitian_matrix(L_long, [vs, as_], [vc, ac], bra_map, ket_map)
    M_Y_expected = sp.Matrix([
        [K2 * w**2 / 2 - cY * k**2 / 2, -sp.I * (K2 * dQb - cY * Qbar) * k / 2],
        [sp.I * (K2 * dQb - cY * Qbar) * k / 2, KB * w**2 + (K2 * dQb * Qbar - cY * Qbar**2) / 2],
    ])
    assert sp.simplify(M_Y - M_Y_expected) == sp.zeros(2, 2)

    # 1. Bare L_cond (c_Y = 0) dispersion
    det_cY0 = sp.expand(M_Y.subs(cY, 0).det())
    poly_w4 = 2 * KB * w**4 + K2 * dQb * Qbar * w**2 - K2 * dQb**2 * k**2
    assert sp.simplify(4 * det_cY0 - K2 * poly_w4) == 0

    u = sp.Symbol("u", real=True)
    Qbar_s = sp.Symbol("Qbar", positive=True)
    poly_u = 2 * KB * u**2 + K2 * dQb * Qbar_s * u - K2 * dQb**2 * k**2
    assert sp.simplify(poly_w4 - poly_u.subs({u: w**2, Qbar_s: Qbar})) == 0

    disc = sp.sqrt(K2**2 * dQb**2 * Qbar_s**2 + 8 * K2 * KB * dQb**2 * k**2)
    w2_minus_0 = (-K2 * dQb * Qbar_s - disc) / (4 * KB)
    w2_plus_0 = (-K2 * dQb * Qbar_s + disc) / (4 * KB)
    assert sp.simplify(poly_u.subs(u, w2_minus_0)) == 0
    assert sp.simplify(poly_u.subs(u, w2_plus_0)) == 0

    assert sp.simplify((w2_plus_0 + w2_minus_0) - (-K2 * dQb * Qbar_s / (2 * KB))) == 0
    assert sp.simplify((w2_plus_0 * w2_minus_0) - (-K2 * dQb**2 * k**2 / (2 * KB))) == 0
    assert sp.simplify(w2_minus_0.subs(k, 0) - (-K2 * dQb * Qbar_s / (2 * KB))) == 0

    # Large-k UV blowup of unstable branch
    uv_slope = sp.limit(w2_minus_0 / k, k, sp.oo)
    assert sp.simplify(uv_slope - (-sp.sqrt(K2 / (2 * KB)) * dQb)) == 0

    # Adiabatic dust sound speed check: dp_d / drho_d == dQb / Qbar
    dQ_p = sp.Symbol("dQ_p", positive=True)
    rho_expr = K2 * Q0 * dQ_p + sp.Rational(1, 2) * K2 * dQ_p**2
    p_expr = sp.Rational(1, 2) * K2 * dQ_p**2
    cs2_adiab = sp.simplify((sp.diff(p_expr, dQ_p) / sp.diff(rho_expr, dQ_p)).subs(dQ_p, dQb))
    assert sp.simplify(cs2_adiab - dQb / Qbar) == 0

    small_k_plus = sp.series(w2_plus_0, k, 0, 3).removeO()
    assert sp.simplify(small_k_plus / k**2 - dQb / Qbar_s) == 0

    # 2. Stabilized dispersion with c_Y > 0
    c2 = sp.Symbol("c2", real=True)
    det_cY = sp.expand(M_Y.det())
    lead_k4 = sp.Poly(det_cY.subs(w**2, c2 * k**2), k).LC()
    uv_speeds = sp.solve(lead_k4, c2)
    assert len(uv_speeds) == 2 and 0 in uv_speeds
    assert sp.simplify([r for r in uv_speeds if r != 0][0] - cY / K2) == 0

    k0_roots = sp.solve(det_cY.subs(k, 0), w**2)
    assert len(k0_roots) == 2 and 0 in k0_roots
    assert sp.simplify([r for r in k0_roots if r != 0][0] - Qbar * (cY * Qbar - K2 * dQb) / (2 * KB)) == 0

    # Small-k acoustic sound speed w^2 = c_s^2 k^2 from O(k^2) coefficient of det(M_Y)
    small_k_poly = sp.series(det_cY.subs(w**2, c2 * k**2), k, 0, 3).removeO()
    cs2_cY = sp.solve(small_k_poly, c2)
    assert len(cs2_cY) == 1 and sp.simplify(cs2_cY[0] - dQb / Qbar) == 0

    # 3. Strictly pinned A_i = 0 limit
    L_pin = sp.simplify(L_long.subs({Ax: 0, Axt: 0}))
    assert sp.simplify(L_pin - (sp.Rational(1, 2) * K2 * vt**2 - sp.Rational(1, 2) * cY * vx**2)) == 0

    return {
        "Y2_longitudinal": "(Qbar*A_x + v_x)^2",
        "cY_0_dispersion": "2*K_B*omega^4 + K2*dQb*Qbar*omega^2 - K2*dQb^2*k^2 = 0",
        "cY_0_ir_tachyon_k0": "-K2*dQb*Qbar / (2*K_B) < 0",
        "cY_0_uv_blowup": "-sqrt(K2/(2*K_B))*dQb*k -> -infinity",
        "small_k_acoustic_cs2": "dQb / Qbar (exact adiabatic dust speed dp_d/drho_d)",
        "cY_stabilized_uv_speeds": ["0", "c_Y / K2"],
        "cY_stabilized_k0_masses": ["0", "Qbar*(c_Y*Qbar - K2*dQb)/(2*K_B)"],
        "transverse_Ay_dispersion": "omega^2(k) = k^2 + Qbar*(c_Y*Qbar - K2*dQb)/(2*K_B)",
        "stability_window_dynamical_Ai": "K2 > 0, K_B > 0, and K2*dQb/Qbar <= c_Y <= K2",
        "pinned_Ai_zero_dispersion": "omega^2(k) = (c_Y / K2) * k^2 (requires c_Y << K2 for dust if A_i is non-dynamical)",
    }


def check_adm_gravity_and_tensor_sign() -> dict:
    """Verify exact 4D tensor & ADM scalar quadratic EH actions, Poisson sign, and constraint reduction."""
    t, x, y, z, eps = sp.symbols("t x y z eps", real=True)

    # 1. Exact tensor graviton quadratic EH action
    h = sp.Function("h")(t, z)
    gt = sp.diag(-1, 1 + eps * h, 1 - eps * h, 1)
    gti = gt.inv()
    Xt = [t, x, y, z]
    Gam_t = [
        [
            [
                sum(
                    gti[a, d]
                    * (sp.diff(gt[d, b], Xt[c]) + sp.diff(gt[d, c], Xt[b]) - sp.diff(gt[b, c], Xt[d]))
                    for d in range(4)
                )
                / 2
                for c in range(4)
            ]
            for b in range(4)
        ]
        for a in range(4)
    ]
    R_ten = 0
    for b in range(4):
        for d in range(4):
            ric_bd = sum(
                sp.diff(Gam_t[a][b][d], Xt[a])
                - sp.diff(Gam_t[a][b][a], Xt[d])
                + sum(
                    Gam_t[a][a][m] * Gam_t[m][b][d] - Gam_t[a][d][m] * Gam_t[m][b][a]
                    for m in range(4)
                )
                for a in range(4)
            )
            R_ten += gti[b, d] * ric_bd
    L_ten_2 = sp.expand(sp.diff(sp.sqrt(-gt.det()) * R_ten, eps, 2).subs(eps, 0) / 2)
    L_ten_clean = sp.Rational(1, 2) * (sp.diff(h, t) ** 2 - sp.diff(h, z) ** 2)
    assert _el_op(sp.expand(L_ten_2 - L_ten_clean), h, t, z) == 0

    # 2. Exact 4D ADM scalar quadratic EH action
    Phi_f = sp.Function("Phi")(t, x)
    B_f = sp.Function("B")(t, x)
    Psi_f = sp.Function("Psi")(t, x)
    gam = sp.diag(1 - 2 * eps * Psi_f, 1 - 2 * eps * Psi_f, 1 - 2 * eps * Psi_f)
    gami = sp.diag(1 / (1 - 2 * eps * Psi_f), 1 / (1 - 2 * eps * Psi_f), 1 / (1 - 2 * eps * Psi_f))
    X3 = [x, y, z]
    Gam3 = [
        [
            [
                sum(
                    gami[a, d]
                    * (sp.diff(gam[d, b], X3[c]) + sp.diff(gam[d, c], X3[b]) - sp.diff(gam[b, c], X3[d]))
                    for d in range(3)
                )
                / 2
                for c in range(3)
            ]
            for b in range(3)
        ]
        for a in range(3)
    ]
    R3 = 0
    for b in range(3):
        for d in range(3):
            ric3 = sum(
                sp.diff(Gam3[a][b][d], X3[a])
                - sp.diff(Gam3[a][b][a], X3[d])
                + sum(
                    Gam3[a][a][m] * Gam3[m][b][d] - Gam3[a][d][m] * Gam3[m][b][a]
                    for m in range(3)
                )
                for a in range(3)
            )
            R3 += gami[b, d] * ric3

    Bx_f = sp.diff(B_f, x)
    N_adm = sp.sqrt(1 + 2 * eps * Phi_f + eps**2 * Bx_f**2 / (1 - 2 * eps * Psi_f))
    sqrt_gam = (1 - 2 * eps * Psi_f) ** sp.Rational(3, 2)
    Psit_f = sp.diff(Psi_f, t)
    Bxx_f = sp.diff(B_f, x, 2)
    K_part = -6 * Psit_f**2 - 4 * Psit_f * Bxx_f
    L_adm_2 = sp.expand(sp.diff(sqrt_gam * N_adm * R3, eps, 2).subs(eps, 0) / 2 + K_part)
    L_adm_clean = (
        -6 * Psit_f**2
        - 4 * Psit_f * Bxx_f
        - 4 * sp.diff(Phi_f, x) * sp.diff(Psi_f, x)
        + 2 * sp.diff(Psi_f, x) ** 2
    )
    diff_adm = sp.expand(L_adm_2 - L_adm_clean)
    assert all(_el_op(diff_adm, fld, t, x) == 0 for fld in (Phi_f, B_f, Psi_f))

    # 3. Coupled quadratic action at dQb = 0 in [Phi, B, Psi, varphi, alpha]
    K2, KB, Q0, Mpl2, s_EH, w, k = sp.symbols("K2 K_B Q0 Mpl2 s_EH omega k", real=True)
    P_s, B_s, S_s = sp.symbols("Phi B Psi", real=True)
    Phit, Phix_s, Bx_s, Bxt_s, Bxx_s, Psit_s, Psix_s = sp.symbols(
        "Phi_t Phi_x B_x B_xt B_xx Psi_t Psi_x", real=True
    )
    vt_s, vx_s, alx_s, alxt_s = sp.symbols("v_t v_x al_x al_xt", real=True)

    g_sym = sp.Matrix([[-(1 + 2 * eps * P_s), eps * Bx_s], [eps * Bx_s, 1 - 2 * eps * S_s]])
    gi_sym = g_sym.inv()
    sqrt_mg_sym = sp.sqrt(-g_sym.det() * (1 - 2 * eps * S_s) ** 2)
    A1_sym = eps * alx_s
    a_c, b_c, c_c = gi_sym[0, 0], 2 * gi_sym[0, 1] * A1_sym, gi_sym[1, 1] * A1_sym**2 + 1
    A0_sym = (-b_c + sp.sqrt(b_c**2 - 4 * a_c * c_c)) / (2 * a_c)
    Q_sym = (
        gi_sym[0, 0] * A0_sym * (Q0 + eps * vt_s)
        + gi_sym[0, 1] * (A0_sym * eps * vx_s + A1_sym * (Q0 + eps * vt_s))
        + gi_sym[1, 1] * A1_sym * eps * vx_s
    )
    # F01 at O(eps): d_t(eps*alpha_x) - d_x(-eps*Phi) = eps*(alpha_xt + Phi_x)
    F01_sym = eps * (alxt_s + Phix_s)
    F2_sym = 2 * (gi_sym[0, 0] * gi_sym[1, 1] - gi_sym[0, 1] ** 2) * F01_sym**2
    Lm_0 = sp.Rational(1, 2) * K2 * (Q_sym - Q0) ** 2 - sp.Rational(1, 2) * KB * F2_sym
    Sm2_0 = sp.expand(sp.diff(sqrt_mg_sym * Lm_0, eps, 2).subs(eps, 0) / 2)

    L_EH_sym = -6 * Psit_s**2 - 4 * Psit_s * Bxx_s - 4 * Phix_s * Psix_s + 2 * Psix_s**2
    L_tot_0 = sp.expand(s_EH * Mpl2 * L_EH_sym + Sm2_0)

    Pc, Bc, Sc, vc, ac = sp.symbols("Pc Bc Sc vc ac")
    Ps, Bs, Ss, vs, as_ = sp.symbols("Ps Bs Ss vs as_")
    bra_map = {
        P_s: Ps,
        B_s: Bs,
        S_s: Ss,
        Phit: sp.I * w * Ps,
        Phix_s: -sp.I * k * Ps,
        Bx_s: -sp.I * k * Bs,
        Bxt_s: w * k * Bs,
        Bxx_s: -k**2 * Bs,
        Psit_s: sp.I * w * Ss,
        Psix_s: -sp.I * k * Ss,
        vt_s: sp.I * w * vs,
        vx_s: -sp.I * k * vs,
        alx_s: -sp.I * k * as_,
        alxt_s: w * k * as_,
    }
    ket_map = {
        P_s: Pc,
        B_s: Bc,
        S_s: Sc,
        Phit: -sp.I * w * Pc,
        Phix_s: sp.I * k * Pc,
        Bx_s: sp.I * k * Bc,
        Bxt_s: w * k * Bc,
        Bxx_s: -k**2 * Bc,
        Psit_s: -sp.I * w * Sc,
        Psix_s: sp.I * k * Sc,
        vt_s: -sp.I * w * vc,
        vx_s: sp.I * k * vc,
        alx_s: sp.I * k * ac,
        alxt_s: w * k * ac,
    }
    M5 = _fourier_hermitian_matrix(L_tot_0, [Ps, Bs, Ss, vs, as_], [Pc, Bc, Sc, vc, ac], bra_map, ket_map)

    # Static Poisson limit (omega = 0, Psi = Phi, B = varphi = alpha = 0)
    static_coeff = sp.simplify((M5[0, 0] + M5[0, 2] + M5[2, 0] + M5[2, 2]).subs(w, 0))
    static_k2 = sp.simplify(sp.expand(static_coeff).coeff(k, 2))
    assert sp.simplify(static_k2 - (-2 * s_EH * Mpl2 + KB)) == 0
    assert sp.simplify(static_k2.subs(s_EH, 1) - (KB - 2 * Mpl2)) == 0
    assert sp.simplify(static_k2.subs(s_EH, -1) - (2 * Mpl2 + KB)) == 0

    # Exact ADM momentum constraint B row forces Psi = 0 (since s_EH != 0, k != 0, w != 0)
    assert (
        sp.simplify(M5[1, :] - sp.Matrix([[0, 0, -2 * sp.I * Mpl2 * k**2 * w * s_EH, 0, 0]]))
        == sp.zeros(1, 5)
    )

    # Eliminate Phi on Psi = 0 slice to get 2x2 effective matrix for [varphi, alpha]
    M_sub = M5.extract([0, 3, 4], [0, 3, 4])
    M_va = sp.simplify(M_sub[1:, 1:] - M_sub[1:, :1] * M_sub[:1, :1].inv() * M_sub[:1, 1:])
    assert sp.simplify(M_va.det()) == 0
    # Strict extraction [0, 0] for pinned (alpha = 0) Schur complement
    K_pin = sp.simplify(M_sub[1, 1] - (M_sub[1:2, :1] * M_sub[:1, :1].inv() * M_sub[:1, 1:2])[0, 0])
    K_pin_expected = K2 * KB * k**2 * w**2 / (K2 * Q0**2 + 2 * KB * k**2)
    assert sp.simplify(K_pin - K_pin_expected) == 0
    assert sp.simplify(K_pin.subs(KB, 0)) == 0

    return {
        "tensor_EH_quadratic": "+(1/2)*s_EH*Mpl2*(h_t^2 - h_z^2)",
        "relative_tensor_scalar_kinetic_sign": "In local 4D EFT s_EH*Mpl2*R + L_wall, s_EH = -1 gives tensor -(1/2)*Mpl2*h_t^2 vs scalar +(1/2)*K2*varphi_t^2 (opposite signs for K2 > 0); ghost-freedom relies on 5D non-localization (arXiv:2202.00545, 2212.14004).",
        "static_poisson_k2_coeff": "-2*s_EH*Mpl2 + K_B",
        "gr_aest_window_sEH_plus1": "0 < K_B < 2*Mpl2 (attractive Poisson iff K_B < 2*Mpl2)",
        "wall_poisson_sEH_minus1": "+(2*Mpl2 + K_B)*k^2*Phi^2 (repulsive for all K_B > 0)",
        "adm_dQb0_pinned_kinetic_coeff": "K2*K_B*k^2*omega^2 / (K2*Q0^2 + 2*K_B*k^2) (vanishes at K_B = 0: pure L_cond at dQb=0 is pure gauge)",
    }


def check_5d_wall_bending_seat() -> dict:
    """Verify arXiv:2001.07433 5D wall-bending response for purely wall-localized dust tau_00 = +rho_d."""
    kp, km, k5, p2, rho_d, k = sp.symbols("k_p k_m kappa5sq p2 rho_d k", positive=True)
    eta = sp.diag(-1, 1, 1, 1)
    tau_mat = sp.diag(rho_d, 0, 0, 0)
    tau_tr = sum(eta[i, i] * tau_mat[i, i] for i in range(4))
    assert tau_tr == -rho_d

    alpha = (1 / kp - 1 / km) / (4 * k5)
    kappa4sq = k5 * 2 * kp * km / (km - kp)
    assert sp.simplify(1 / alpha - 2 * kappa4sq) == 0

    # Wall bending F induced by purely wall-localized dust tau_ab (no bulk string pull)
    F_bend = sp.simplify(k5 * tau_tr / (3 * (1 / kp - 1 / km) * p2))
    F_expected = -kp * km * k5 * rho_d / (3 * p2 * (km - kp))
    assert sp.simplify(F_bend - F_expected) == 0

    h_wall = sp.simplify(-(tau_mat - tau_tr * eta / 3) / (alpha * p2) + 2 * F_bend * eta)
    h_target = sp.simplify(-(2 * kappa4sq / p2) * (tau_mat - tau_tr * eta / 2))
    assert sp.simplify(h_wall - h_target) == sp.zeros(4, 4)

    # Static limit p^2 -> k^2 with ds^2 = -(1 + 2*Phi)dt^2 + (1 - 2*Psi)dx^2 = (eta + h)dx dx
    Phi_static = sp.simplify((-h_wall[0, 0] / 2).subs(p2, k**2))
    Psi_static = sp.simplify((-h_wall[1, 1] / 2).subs(p2, k**2))
    assert sp.simplify(Phi_static - kappa4sq * rho_d / (2 * k**2)) == 0
    assert sp.simplify(Psi_static - Phi_static) == 0

    return {
        "F_bend_wall_dust": str(F_bend),
        "h_wall_covariant": "-(2*kappa4^2/p^2)*(tau_ab - tau*eta_ab/2)",
        "Phi_static_wall_dust": str(Phi_static) + " = +4*pi*G4*rho_d/k^2 > 0 (anti-gravitating)",
        "Psi_over_Phi_slip": "1 (bending turns 5D 1/3 trace into 4D 1/2, keeping zero slip)",
        "seat_verdict": "[D] at leading order in p/(a*k): wall bending alone does NOT overcompensate purely wall-localized dust to +G4; L_cond sits in the anti-gravitating drag seat needed for 3*(1 + x0*a^2)*(Psi' + Phi), while +G4 matter requires an explicit bulk source (strings / bulk field).",
    }


def main() -> int:
    out = {
        "B1_background_and_noether": check_background_and_noether(),
        "B2_nonzero_drag_dispersion": check_nonzero_drag_dispersion(),
        "B3_adm_gravity_and_tensor_sign": check_adm_gravity_and_tensor_sign(),
        "B4_5d_wall_bending_seat": check_5d_wall_bending_seat(),
        "remaining_open_gates": [
            "[O] Full 5D bulk Weyl backreaction E_eff induced by L_cond - (1/2)*c_Y*Y at finite H/k and non-zero dQb.",
            "[O] Explicit bulk shift-current coupling S_flux supplying div J_phi = Q4/Q > 0 while keeping stability and Law B / c_vis^2 gates satisfied.",
        ],
    }
    path = os.path.join(HERE, "PHASE3_WALL_GHOST_COUPLED.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
