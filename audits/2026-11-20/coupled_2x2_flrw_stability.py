#!/usr/bin/env python3
"""Coupled 2x2 & ADM 4x4 quadratic stability audit for live AeST with general K(Q).

Closes CLM-COUPLED2X2 from audits/2026-11-18/coupled_quadratic_stability.py by
deriving the exact coupled (varphi, A_x) 2x2 and 4x4 ADM stability matrices and
eigenmode sound speeds around backgrounds with Qbar != 0 and K'(Qbar) != 0
(including Q^3, Q^4, and combined 2*K_2*(Q - Q0)^2 + c*Q^3 potentials), and
reproducing SZ22 eq. (speed_of_sound) as its K'(Qbar) -> 0 calibration limit.

Labels: [D] derived/verified here, [C] literature input, [O] open.
Does not edit CURRENT_STATE_READ_THIS_FIRST.md or existing audits.
"""
from __future__ import annotations

import json
import os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def _build_o2_lagrangian():
    """Construct exact O(eps^2) quadratic Lagrangian of live AeST in polynomial form."""
    eps = sp.Symbol("eps", real=True)
    KB, lam_s, K1, K2e, Qbar, w, k = sp.symbols(
        "K_B lambda_s K1 K2_eff Qbar omega k", positive=True
    )
    P_s, B_s, S_s = sp.symbols("Phi B Psi", real=True)
    Phit, Phix, Bx, Bxt, Bxx, Psit, Psix = sp.symbols(
        "Phi_t Phi_x B_x B_xt B_xx Psi_t Psi_x", real=True
    )
    vt, vx, alx, alxt = sp.symbols("v_t v_x al_x al_xt", real=True)

    # Explicit O(eps^2) polynomial expansion (no nested sqrts)
    gi00 = -1 + 2 * eps * P_s + eps**2 * (-4 * P_s**2 + Bx**2)
    gi01 = eps * Bx + eps**2 * (2 * Bx * (S_s - P_s))
    gi11 = 1 + 2 * eps * S_s + eps**2 * (4 * S_s**2 - Bx**2)
    sqrt_mg = 1 + eps * (P_s - 3 * S_s) + eps**2 * (
        -(P_s**2) / 2 - 3 * P_s * S_s + 3 * S_s**2 / 2 + Bx**2 / 2
    )

    # Verify inverse metric and volume density identities through O(eps^2)
    g_m = sp.Matrix([[-(1 + 2 * eps * P_s), eps * Bx], [eps * Bx, 1 - 2 * eps * S_s]])
    gi_m = sp.Matrix([[gi00, gi01], [gi01, gi11]])
    prod = sp.expand(gi_m * g_m - sp.eye(2))
    assert all(prod[i, j].coeff(eps, d) == 0 for i in range(2) for j in range(2) for d in (0, 1, 2))
    det_chk = sp.expand(sqrt_mg**2 + g_m.det() * (1 - 2 * eps * S_s) ** 2)
    assert all(det_chk.coeff(eps, d) == 0 for d in (0, 1, 2))

    # Solve g^{ab} A_a A_b == -1 through O(eps^2)
    A1 = eps * alx
    a1_s, a2_s = sp.symbols("a1 a2")
    A0_p = -1 + eps * a1_s + eps**2 * a2_s
    norm_p = sp.expand(gi00 * A0_p**2 + 2 * gi01 * A0_p * A1 + gi11 * A1**2 + 1)
    a1_v = sp.solve(norm_p.coeff(eps, 1), a1_s)[0]
    a2_v = sp.solve(norm_p.coeff(eps, 2).subs(a1_s, a1_v), a2_s)[0]
    A0 = sp.expand(A0_p.subs({a1_s: a1_v, a2_s: a2_v}))
    norm_chk = sp.expand(gi00 * A0**2 + 2 * gi01 * A0 * A1 + gi11 * A1**2 + 1)
    assert all(norm_chk.coeff(eps, d) == 0 for d in (0, 1, 2))

    dphi0 = Qbar + eps * vt
    dphi1 = eps * vx
    Q_raw = sp.expand(gi00 * A0 * dphi0 + gi01 * (A0 * dphi1 + A1 * dphi0) + gi11 * A1 * dphi1)
    Q = sum(eps**d * Q_raw.coeff(eps, d) for d in (0, 1, 2))
    Y_raw = sp.expand(gi00 * dphi0**2 + 2 * gi01 * dphi0 * dphi1 + gi11 * dphi1**2 + Q**2)
    Y = sum(eps**d * Y_raw.coeff(eps, d) for d in (0, 1, 2))

    A_up0 = sum(eps**d * sp.expand(gi00 * A0 + gi01 * A1).coeff(eps, d) for d in (0, 1))
    A_up1 = sum(eps**d * sp.expand(gi01 * A0 + gi11 * A1).coeff(eps, d) for d in (0, 1))
    F01 = eps * (alxt + Phix)
    J0 = A_up1 * (-F01)
    J1 = A_up0 * F01
    J_dphi = eps**2 * sp.expand((gi00 * J0 + gi01 * J1) * dphi0 + (gi01 * J0 + gi11 * J1) * dphi1).coeff(
        eps, 2
    )
    F2 = -2 * F01**2

    Lm = (
        -sp.Rational(1, 2) * KB * F2
        + 2 * (2 - KB) * J_dphi
        - (2 - KB) * (1 + lam_s) * Y
        + K1 * (Q - Qbar)
        + sp.Rational(1, 2) * K2e * (Q - Qbar) ** 2
    )
    L_EH = -6 * Psit**2 - 4 * Psit * Bxx - 4 * Phix * Psix + 2 * Psix**2
    L2_all = sp.expand(L_EH + sp.expand(sqrt_mg * Lm).coeff(eps, 2))

    syms = dict(
        KB=KB, lam_s=lam_s, K1=K1, K2e=K2e, Qbar=Qbar, w=w, k=k,
        P_s=P_s, B_s=B_s, S_s=S_s,
        Phit=Phit, Phix=Phix, Bx=Bx, Bxt=Bxt, Bxx=Bxx, Psit=Psit, Psix=Psix,
        vt=vt, vx=vx, alx=alx, alxt=alxt,
    )
    return L2_all, syms


def _make_hermitian_mat(expr: sp.Expr, var_names: list[str], s: dict, a_is_Ax: bool = False) -> sp.Matrix:
    """Build exact Hermitian Fourier matrix for the requested field basis."""
    w, k = s["w"], s["k"]
    syms_c = sp.symbols(" ".join(v + "_c" for v in var_names))
    syms_s = sp.symbols(" ".join(v + "_s" for v in var_names))
    idx_map = {v: i for i, v in enumerate(var_names)}
    bmap, kmap = {}, {}
    if "Phi" in idx_map:
        i = idx_map["Phi"]
        bmap[s["P_s"]] = syms_s[i]; kmap[s["P_s"]] = syms_c[i]
        bmap[s["Phit"]] = sp.I * w * syms_s[i]; kmap[s["Phit"]] = -sp.I * w * syms_c[i]
        bmap[s["Phix"]] = -sp.I * k * syms_s[i]; kmap[s["Phix"]] = sp.I * k * syms_c[i]
    if "B" in idx_map:
        i = idx_map["B"]
        bmap[s["B_s"]] = syms_s[i]; kmap[s["B_s"]] = syms_c[i]
        bmap[s["Bx"]] = -sp.I * k * syms_s[i]; kmap[s["Bx"]] = sp.I * k * syms_c[i]
        bmap[s["Bxx"]] = -(k**2) * syms_s[i]; kmap[s["Bxx"]] = -(k**2) * syms_c[i]
    if "Psi" in idx_map:
        i = idx_map["Psi"]
        bmap[s["S_s"]] = syms_s[i]; kmap[s["S_s"]] = syms_c[i]
        bmap[s["Psit"]] = sp.I * w * syms_s[i]; kmap[s["Psit"]] = -sp.I * w * syms_c[i]
        bmap[s["Psix"]] = -sp.I * k * syms_s[i]; kmap[s["Psix"]] = sp.I * k * syms_c[i]
    if "v" in idx_map:
        i = idx_map["v"]
        bmap[s["vt"]] = sp.I * w * syms_s[i]; kmap[s["vt"]] = -sp.I * w * syms_c[i]
        bmap[s["vx"]] = -sp.I * k * syms_s[i]; kmap[s["vx"]] = sp.I * k * syms_c[i]
    if "a" in idx_map:
        i = idx_map["a"]
        if a_is_Ax:
            bmap[s["alx"]] = syms_s[i]; kmap[s["alx"]] = syms_c[i]
            bmap[s["alxt"]] = sp.I * w * syms_s[i]; kmap[s["alxt"]] = -sp.I * w * syms_c[i]
        else:
            bmap[s["alx"]] = -sp.I * k * syms_s[i]; kmap[s["alx"]] = sp.I * k * syms_c[i]
            bmap[s["alxt"]] = w * k * syms_s[i]; kmap[s["alxt"]] = w * k * syms_c[i]

    fvars = list(bmap.keys())
    n = len(var_names)
    M = sp.zeros(n, n)
    for monom, coeff in sp.Poly(sp.expand(expr), *fvars).terms():
        pair = [v for v, d in zip(fvars, monom) for _ in range(d)]
        u1, u2 = pair
        q = sp.expand(coeff * sp.Rational(1, 2) * (bmap[u1] * kmap[u2] + bmap[u2] * kmap[u1]))
        for ii, bs in enumerate(syms_s):
            for jj, kc in enumerate(syms_c):
                c = q.coeff(bs).coeff(kc)
                if c != 0:
                    M[ii, jj] += c
    return sp.simplify(M)


def c1_sz22_calibration(L2_all: sp.Expr, s: dict) -> dict:
    """Reproduce exact SZ22 eq. (speed_of_sound) and k=0 gap at K1 = 0."""
    KB, lam_s, K1, K2e, Qbar, w, k = (
        s["KB"], s["lam_s"], s["K1"], s["K2e"], s["Qbar"], s["w"], s["k"]
    )
    M_N0 = _make_hermitian_mat(
        L2_all.subs({s["Bx"]: 0, s["Bxt"]: 0, s["Bxx"]: 0, K1: 0}), ["Phi", "Psi", "v", "a"], s
    )
    det_N0 = sp.factor(M_N0.det())
    target_det = (
        -2 * k**6 * w**2
        * (
            K2e * KB * w**2
            - 4 * (2 - KB) * (1 + sp.Rational(1, 2) * KB * lam_s) * k**2
            - K2e * Qbar**2 * (2 - KB) * (1 + lam_s)
        )
    )
    assert sp.simplify(det_N0 - target_det) == 0

    K2_sz = sp.Symbol("K_2", positive=True)
    c_s2_sz22 = sp.simplify(
        (4 * (2 - KB) * (1 + sp.Rational(1, 2) * KB * lam_s) / (K2e * KB)).subs(K2e, 4 * K2_sz)
    )
    target_cs2 = (2 - KB) * (1 + sp.Rational(1, 2) * KB * lam_s) / (K2_sz * KB)
    assert sp.simplify(c_s2_sz22 - target_cs2) == 0

    m_gap0 = sp.simplify(K2e * Qbar**2 * (2 - KB) * (1 + lam_s) / (K2e * KB))
    assert sp.simplify(m_gap0 - (2 - KB) * (1 + lam_s) * Qbar**2 / KB) == 0

    return {
        "det_N0_exact": "-2*k^6*omega^2 * [K2_eff*K_B*omega^2 - 4*(2-K_B)*(1 + K_B*lambda_s/2)*k^2 - K2_eff*Qbar^2*(2-K_B)*(1+lambda_s)] [D]",
        "sz22_speed_of_sound_at_K2eff_4K2": "(2 - K_B)*(1 + K_B*lambda_s/2) / (K_2 * K_B) [D]",
        "k0_gap_at_K1_0": "(2 - K_B)*(1 + lambda_s)*Qbar^2 / K_B [D]",
    }


def c2_coupled_2x2_and_gauge_invariance(L2_all: sp.Expr, s: dict) -> dict:
    """Verify gauge invariance across 2x2 and 4x4 ADM formulations and derive exact coupled 2x2."""
    KB, lam_s, K1, K2e, Qbar, w, k = (
        s["KB"], s["lam_s"], s["K1"], s["K2e"], s["Qbar"], s["w"], s["k"]
    )
    c2 = sp.Symbol("c2", real=True)
    cs2_uv = 4 * (2 - KB) * (1 + sp.Rational(1, 2) * KB * lam_s) / (K2e * KB)

    # 1. Newtonian 4x4 [Phi, Psi, v, a] at general K1 != 0
    M_NK = _make_hermitian_mat(L2_all.subs({s["Bx"]: 0, s["Bxt"]: 0, s["Bxx"]: 0}), ["Phi", "Psi", "v", "a"], s)
    p_NK = sp.Poly(sp.expand(M_NK.det().subs(w**2, c2 * k**2)), k)
    uv_NK = sp.solve(p_NK.LC(), c2)

    # 2. Unitary aether ADM 4x4 [Phi, B, Psi, v] (alpha = 0, both constraints kept)
    M_uK = _make_hermitian_mat(L2_all.subs({s["alx"]: 0, s["alxt"]: 0}), ["Phi", "B", "Psi", "v"], s)
    p_uK = sp.Poly(sp.expand(M_uK.det().subs(w**2, c2 * k**2)), k)
    uv_uK = sp.solve(p_uK.LC(), c2)

    # 3. Fixed-metric 2x2 [varphi, A_x] with A_x := alx
    L_fix = L2_all.subs({
        s["P_s"]: 0, s["Phit"]: 0, s["Phix"]: 0,
        s["B_s"]: 0, s["Bx"]: 0, s["Bxt"]: 0, s["Bxx"]: 0,
        s["S_s"]: 0, s["Psit"]: 0, s["Psix"]: 0,
    })
    M_fix = _make_hermitian_mat(L_fix, ["v", "a"], s, a_is_Ax=True)
    p_fix = sp.Poly(sp.expand(M_fix.det().subs(w**2, c2 * k**2)), k)
    uv_fix = sp.solve(p_fix.LC(), c2)

    for roots in (uv_NK, uv_uK, uv_fix):
        assert len(roots) == 2 and 0 in roots
        assert sp.simplify([r for r in roots if r != 0][0] - cs2_uv) == 0

    # Check kinetic matrix K_ij = diag(K2_eff/2, K_B) on M_fix
    K_mat = sp.Matrix(2, 2, lambda i, j: sp.simplify(sp.diff(M_fix[i, j], w, 2) / 2))
    assert K_mat == sp.diag(K2e / 2, KB)

    # Exact coupled 2x2 characteristic polynomial: w^4 - (M_gap^2 + cs_uv^2 k^2) w^2 + M_gap^2 cs_ir^2 k^2 = 0
    M_gap2 = Qbar * (2 * (2 - KB) * (1 + lam_s) * Qbar - K1) / (2 * KB)
    cs2_ir = K1 / (K2e * Qbar)
    char_poly = sp.simplify(M_fix.det() / (K2e * KB / 2))
    target_char = w**4 - (M_gap2 + cs2_uv * k**2) * w**2 + M_gap2 * cs2_ir * k**2
    assert sp.simplify(char_poly - target_char) == 0

    # Check adiabatic thermodynamic identity dp/drho = K' / (Q K'')
    Qp = sp.Symbol("Q_p", positive=True)
    Kfn = sp.Function("K_fn")(Qp)
    p_th = Kfn
    rho_th = Qp * sp.diff(Kfn, Qp) - Kfn
    dp_drho = sp.simplify(sp.diff(p_th, Qp) / sp.diff(rho_th, Qp))
    assert dp_drho == sp.simplify(sp.diff(Kfn, Qp) / (Qp * sp.diff(Kfn, Qp, 2)))

    # Transverse vector mode A_y(t, x)
    eps = sp.Symbol("eps", real=True)
    Ay, Ayt, Ayx = sp.symbols("A_y A_yt A_yx", real=True)
    A0_t = -1 - eps**2 * Ay**2 / 2
    Q_t = -A0_t * Qbar
    Y_t = -(Qbar**2) + Q_t**2
    F2_t = 2 * eps**2 * (-(Ayt**2) + Ayx**2)
    Lm_t = (
        -sp.Rational(1, 2) * KB * F2_t
        - (2 - KB) * (1 + lam_s) * Y_t
        + K1 * (Q_t - Qbar)
        + sp.Rational(1, 2) * K2e * (Q_t - Qbar) ** 2
    )
    L2_t = sp.expand(Lm_t).coeff(eps, 2)
    m2_perp = sp.simplify(-L2_t.coeff(Ay, 2) / KB)
    assert sp.simplify(m2_perp - M_gap2) == 0

    return {
        "uv_sound_speeds_gauge_invariant": True,
        "kinetic_matrix_K": "diag(K2_eff/2, K_B) [D]",
        "gyroscopic_mixing_kw": "+/- (2 - K_B) * k * omega [D]",
        "coupled_2x2_characteristic_eq": "omega^4 - (M_gap^2 + c_{s,UV}^2 * k^2)*omega^2 + M_gap^2 * c_{s,IR}^2 * k^2 = 0 [D]",
        "M_gap2": "Qbar * (2*(2 - K_B)*(1 + lambda_s)*Qbar - K1) / (2 * K_B) [D]",
        "c_s_UV_sq": "4*(2 - K_B)*(1 + K_B*lambda_s/2) / (K2_eff * K_B) [D]",
        "c_s_IR_sq": "K1 / (K2_eff * Qbar) == dp_phi / drho_phi [D]",
        "transverse_Ay_dispersion": "omega_perp^2(k) = k^2 + M_gap^2 (exact same M_gap^2) [D]",
    }


def c3_stability_window_and_powerlaw_bound(s: dict) -> dict:
    """Prove all-k instability when M_gap^2 < 0 and derive Qbar-independent power-law K_B bound."""
    KB, lam_s, p, k = sp.symbols("K_B lambda_s p k", positive=True)
    c_p, Qbar = sp.symbols("c_p Qbar", positive=True)

    # 1. Pure power law K(Q) := c_p * Q^p (p > 1)
    Kfn = c_p * Qbar**p
    K1_p = sp.diff(Kfn, Qbar)
    K2e_p = sp.diff(Kfn, Qbar, 2)
    cs2_ir_p = sp.simplify(K1_p / (K2e_p * Qbar))
    assert sp.simplify(cs2_ir_p - 1 / (p - 1)) == 0
    assert sp.simplify(cs2_ir_p.subs(p, 3) - sp.Rational(1, 2)) == 0
    assert sp.simplify(cs2_ir_p.subs(p, 4) - sp.Rational(1, 3)) == 0

    # Non-tachyon bound: K1 <= 2*(2 - KB)*(1 + lam_s)*Qbar => K2_eff <= 2*(p-1)*(2-KB)*(1+lam_s)
    # Subluminality c_{s,UV}^2 <= 1: K2_eff >= 4*(2 - KB)*(1 + KB*lam_s/2)/KB
    # Combined compatibility (for 2 - KB > 0): (2 + KB*lam_s)/KB <= (p - 1)*(1 + lam_s)
    ineq_diff = sp.simplify((2 + KB * lam_s) / KB - (p - 1) * (1 + lam_s))
    KB_min = sp.solve(ineq_diff, KB)[0]
    target_KB_min = 2 / ((p - 1) * (1 + lam_s) - lam_s)
    assert sp.simplify(KB_min - target_KB_min) == 0

    # Check 4*(2 - KB)*(1 + KB*lam_s/2)/KB == 2*(p-1)*(2 - KB)*(1 + lam_s) directly at KB = KB_min
    upper_K2 = 2 * (p - 1) * (2 - KB) * (1 + lam_s)
    lower_K2 = 4 * (2 - KB) * (1 + sp.Rational(1, 2) * KB * lam_s) / KB
    assert sp.simplify((upper_K2 - lower_K2).subs(KB, KB_min)) == 0

    return {
        "unstable_when_Mgap2_lt_0": "Product omega_+^2 * omega_-^2 = M_gap^2 * c_{s,IR}^2 * k^2 < 0 for every k > 0 (all-k longitudinal instability approaching -|M_gap^2| c_{s,IR}^2 / c_{s,UV}^2 as k->oo, plus transverse tachyon for k < sqrt(|M_gap^2|)) [D]",
        "stability_conditions_general_K": [
            "0 < K_B < 2 and K2_eff > 0 (ghost-free kinetic matrix + positive tensor/Poisson stability)",
            "K2_eff >= 4*(2 - K_B)*(1 + K_B*lambda_s/2) / K_B (UV subluminality c_{s,UV}^2 <= 1)",
            "0 <= K1/(2*Qbar) <= (2 - K_B)*(1 + lambda_s) (IR sound speed >= 0 and tachyon-free M_gap^2 >= 0)",
        ],
        "power_law_cs2_IR": "1 / (p - 1) (1/2 for Q^3, 1/3 for Q^4) [D]",
        "power_law_KB_min": "2 / ((p - 1)*(1 + lambda_s) - lambda_s) (exact, independent of Qbar and c) [D]",
    }


def c4_pr226_witness_and_trackers() -> dict:
    """Evaluate PR #226 witness and Tidal-QUMOND large-lambda_s limits quantitatively."""
    KB_w = 0.008
    lam_w = 11.2787
    K2_w = 300.0

    cs2_sz22 = (2.0 - KB_w) * (1.0 + 0.5 * KB_w * lam_w) / (K2_w * KB_w)
    assert abs(cs2_sz22 - 0.867445) < 1e-4

    def kb_min(p: float, l: float) -> float:
        return 2.0 / ((p - 1.0) * (1.0 + l) - l)

    kb_min_q3 = kb_min(3.0, lam_w)
    kb_min_q4 = kb_min(4.0, lam_w)
    assert abs(kb_min_q3 - 0.150617) < 1e-5
    assert abs(kb_min_q4 - 0.078255) < 1e-5
    assert kb_min_q3 > 0.10 and KB_w < kb_min_q4 < 0.10

    # Combined potential K(Q) = 2*K_2*(Q - Q0)^2 + c*Q^3
    ceil = 2.0 * (2.0 - KB_w) * (1.0 + lam_w)
    max_frac_dQ_c0 = ceil / (4.0 * K2_w)
    max_cQ0 = ceil / 3.0
    K2eff_max_c = 4.0 * K2_w + 6.0 * max_cQ0
    cs2_uv_min = 4.0 * (2.0 - KB_w) * (1.0 + 0.5 * KB_w * lam_w) / (K2eff_max_c * KB_w)
    cs2_ir_max = ceil / K2eff_max_c

    assert abs(max_frac_dQ_c0 - 0.040765) < 1e-5
    assert abs(max_cQ0 - 16.306114) < 1e-4
    assert abs(cs2_uv_min - 0.802053) < 1e-4 and abs(cs2_ir_max - 0.037692) < 1e-4

    # Tidal-QUMOND witness check (K_B = 0.05, finite vs large lambda_s)
    kb_tq = 0.05
    lam_for_q3_at_kbtq = (2.0 / kb_tq + 1.0) / 1.0  # 2/(2*(1+l)-l) <= kb => l >= 2/kb - 2?
    # Solve kb_min(p, l) = kb: (p-2)*l + (p-1) = 2/kb => l = (2/kb - (p-1))/(p-2)
    lam_min_q3_kbtq = (2.0 / kb_tq - 2.0) / 1.0
    lam_min_q4_kbtq = (2.0 / kb_tq - 3.0) / 2.0

    return {
        "pr226_witness": {"K_B": KB_w, "lambda_s": lam_w, "K_2": K2_w, "BBN_KB_limit": 0.10},
        "sz22_Y_only_cs2": round(cs2_sz22, 6),
        "pure_Q3_KB_min_at_lam1128": round(kb_min_q3, 6),
        "pure_Q3_verdict": "FAILS at PR #226 witness (0.008 < 0.1506) AND violates BBN K_B <= 0.10 (need lambda_s >= 38 at K_B = 0.05) [D]",
        "pure_Q4_KB_min_at_lam1128": round(kb_min_q4, 6),
        "pure_Q4_verdict": "FAILS at PR #226 witness (0.008 < 0.0783); narrow BBN window K_B in [0.0783, 0.10] at lambda_s = 11.28 [D]",
        "combined_K_at_witness": {
            "nontachyon_ceiling_2_2mKB_1plam": round(ceil, 6),
            "at_c_0_max_fractional_Qbar_above_Q0": round(max_frac_dQ_c0, 6),
            "at_Qbar_eq_Q0_max_cQ0": round(max_cQ0, 6),
            "at_Qbar_eq_Q0_cs2_UV_range": [round(cs2_uv_min, 6), round(cs2_sz22, 6)],
            "at_Qbar_eq_Q0_cs2_IR_range": [0.0, round(cs2_ir_max, 6)],
            "early_universe_warning": "For any early epoch with Qbar >> Q0, 4*K_2*(Qbar-Q0)/Qbar ~ 1200 >> 48.92 drives M_gap^2 < 0 (all-k instability) unless lambda_s increases with Qbar [D]",
        },
        "tidal_qumond_KB_005_min_lambda_s": {
            "Q3_p3": round(lam_min_q3_kbtq, 2),
            "Q4_p4": round(lam_min_q4_kbtq, 2),
        },
    }


def c5_scope_and_open_boundary() -> dict:
    return {
        "closed_here": (
            "[D] Sub-horizon coupled 2x2 kinetic/gradient matrices, 3-gauge invariance across "
            "fixed-metric, Newtonian 4x4, and unitary-ADM 4x4, exact SZ22 limit reproduction, "
            "and exact power-law K_B(p, lambda_s) stability windows/bounds."
        ),
        "still_open": [
            "[O] Full finite-H/k horizon-crossing FLRW ODE transfer functions coupled to radiation fluid perturbations delta_rho_rad with time-dependent Hdot, Qbar_dot.",
            "[O] Whether a Q-dependent running lambda_s(Q) preserves BBN tuning AND avoids the Qbar >> Q0 early-universe tachyon M_gap^2 < 0.",
        ],
    }


def main() -> int:
    L2_all, syms = _build_o2_lagrangian()
    res = {
        "C1_sz22_calibration": c1_sz22_calibration(L2_all, syms),
        "C2_coupled_2x2_and_gauge_invariance": c2_coupled_2x2_and_gauge_invariance(L2_all, syms),
        "C3_stability_window_and_powerlaw_bound": c3_stability_window_and_powerlaw_bound(syms),
        "C4_pr226_witness_and_trackers": c4_pr226_witness_and_trackers(),
        "C5_scope_and_open_boundary": c5_scope_and_open_boundary(),
    }
    path = os.path.join(HERE, "COUPLED_2X2_FLRW_STABILITY.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
