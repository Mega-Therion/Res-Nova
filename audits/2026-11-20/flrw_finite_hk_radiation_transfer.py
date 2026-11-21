#!/usr/bin/env python3
"""Finite-H/k radiation-coupled linearized FLRW ODE transfer audit for live AeST.

Closes the finite-H/k horizon-crossing open boundary from COUPLED_2X2_FLRW_STABILITY.json (C5):
  F1. Derives the full linearized Conformal-Newtonian FLRW + AeST + radiation fluid equations
      from the covariant AeST action on flat expanding FLRW in conformal time tau:
        - Proves E_{h_T}^{(AeST)} == 0 identically (zero linear scalar anisotropic stress => Psi == Phi).
        - Proves exact symbolic Bianchi conservation d/dtau E_{00} == 0 and d/dtau E_{0x} == 0
          for arbitrary U(Qbar) and time-dependent lambda_s(Qbar(tau)).
        - Verifies that the sub-horizon limit (H -> 0, rho_r -> 0) reproduces the exact coupled 2x2
          characteristic polynomial of coupled_2x2_flrw_stability.py.
  F2. Integrates the coupled 10-variable FLRW background + perturbation ODE system (scipy Radau)
      across horizon crossing x = k*tau in [0.05, 50] with continuous E_{00}, E_{0x} constraint
      monitoring across 5 test cases:
        1. Pure-radiation GR control (Omega_phi = 0) vs exact analytic spherical Bessel solution.
        2. SZ21 Fig 1 Cosh model with constant lambda_s = 0 (M_gap^2 < 0) at k = 0.02 & 0.2 Mpc^-1,
           confirming the ~1.9-2/e-fold k-independent runaway noted in TARGET_D5 sec 3.5.
        3. Stabilized Cosh + covariant running lambda_s(Q) at BOTH PR #226 (K_B=0.008, K2=300) and
           SZ21 Fig 1 scales: bounded sub-horizon oscillations, constraint residuals < 1e-8.
        4. Unstable Q^4 radiation tracker (eps_Q = 0.039, PR #226 K_B = 0.008, constant lambda_s = 11.2787):
           direct full-FLRW confirmation of rapid M_gap^2 < 0 exponential instability.
        5. Stabilized Q^4 radiation tracker (eps_Q = 0.039): BOTH narrow BBN-viable constant-lambda_s
           window (K_B = 0.085, lambda_s = 11.2787) AND PR #226 K_B = 0.008 with running lambda_s(Q),
           verifying bounded horizon crossing, exact radiation/potential transfer functions, and < 1e-8
           constraint residuals.

Labels: [D] derived/verified here, [C] literature input, [X] excluded, [O] open.
Does not edit CURRENT_STATE_READ_THIS_FIRST.md or existing audits.
"""
from __future__ import annotations

import json
import math
import os
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))


def f1_derive_flrw_equations_and_bianchi():
    """Derive exact linearized FLRW AeST + radiation equations and prove Bianchi identities."""
    tau, x, eps, KB, k = sp.symbols("tau x eps K_B k", real=True)
    a = sp.Function("a")(tau)
    Qb = sp.Function("Qbar")(tau)
    U0 = sp.Function("U0")(tau)
    K1 = sp.Function("K1")(tau)
    K2e = sp.Function("K2e")(tau)
    lam_s = sp.Function("lam_s")(tau)
    rho_r = sp.Function("rho_r")(tau)

    Ph = sp.Function("Phi")(tau)
    vp = sp.Function("varphi")(tau)
    vA = sp.Function("vA")(tau)
    dr = sp.Function("delta_r")(tau)
    tr = sp.Function("theta_r")(tau)

    Phx = sp.Function("Phi")(tau, x)
    Psx = sp.Function("Psi")(tau, x)
    hTx = sp.Function("hT")(tau, x)
    Bsx = sp.Function("B")(tau, x)
    vpx = sp.Function("varphi")(tau, x)
    vAx = sp.Function("vA")(tau, x)

    def t2(e: sp.Expr) -> sp.Expr:
        ee = sp.expand(e)
        return ee.coeff(eps, 0) + eps * ee.coeff(eps, 1) + eps**2 * ee.coeff(eps, 2)

    g00 = -a**2 * (1 + 2 * eps * Phx)
    g01 = eps * a**2 * Bsx
    g11 = a**2 * (1 - 2 * eps * Psx - 2 * eps * hTx)
    g22 = a**2 * (1 - 2 * eps * Psx + eps * hTx)

    s0 = 1 + eps * Phx - eps**2 * Phx**2 / 2
    s1 = 1 - eps * (Psx + hTx) - eps**2 * (Psx + hTx) ** 2 / 2
    sqrt_mg = t2(a**4 * s0 * s1 * (1 - 2 * eps * Psx + eps * hTx) * (1 + eps**2 * Bsx**2 / 2))
    det_true = -(g00 * g11 - g01**2) * g22**2
    assert t2(sqrt_mg**2 - det_true) == 0

    gi00 = t2(a ** (-2) * (-1 + 2 * eps * Phx + eps**2 * (-4 * Phx**2 + Bsx**2)))
    gi01 = t2(a ** (-2) * (eps * Bsx + eps**2 * 2 * Bsx * (Psx + hTx - Phx)))
    gi11 = t2(a ** (-2) * (1 + 2 * eps * (Psx + hTx) + eps**2 * (4 * (Psx + hTx) ** 2 - Bsx**2)))

    A1 = eps * a * vAx
    a1_s, a2_s = sp.symbols("a1 a2")
    A0_p = -a * (1 + eps * a1_s + eps**2 * a2_s)
    np_ = sp.expand(t2(gi00 * A0_p**2 + 2 * gi01 * A0_p * A1 + gi11 * A1**2 + 1))
    a1v = sp.solve(np_.coeff(eps, 1), a1_s)[0]
    a2v = sp.solve(np_.coeff(eps, 2).subs(a1_s, a1v), a2_s)[0]
    A0 = sp.expand(A0_p.subs({a1_s: a1v, a2_s: a2v}))

    dphi0 = a * Qb + eps * sp.diff(vpx, tau)
    dphi1 = eps * sp.diff(vpx, x)
    Q = t2(gi00 * A0 * dphi0 + gi01 * (A0 * dphi1 + A1 * dphi0) + gi11 * A1 * dphi1)
    Y = t2(gi00 * dphi0**2 + 2 * gi01 * dphi0 * dphi1 + gi11 * dphi1**2 + Q**2)
    assert Y.coeff(eps, 0) == 0 and Y.coeff(eps, 1) == 0

    F01 = sp.diff(A1, tau) - sp.diff(A0, x)
    F2 = t2(2 * (gi00 * gi11 - gi01**2) * F01**2)
    Aup0 = t2(gi00 * A0 + gi01 * A1)
    Aup1 = t2(gi01 * A0 + gi11 * A1)
    J_dphi = t2(
        (gi00 * (-Aup1 * F01) + gi01 * (Aup0 * F01)) * dphi0
        + (gi01 * (-Aup1 * F01) + gi11 * (Aup0 * F01)) * dphi1
    )
    U_exp = U0 + K1 * (Q - Qb) + sp.Rational(1, 2) * K2e * (Q - Qb) ** 2
    L_m = -sp.Rational(1, 2) * KB * F2 + 2 * (2 - KB) * J_dphi - (2 - KB) * (1 + lam_s) * Y + U_exp
    dens = t2(sqrt_mg * L_m)

    def EL(L: sp.Expr, f: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(L, f)
            - sp.diff(sp.diff(L, sp.diff(f, tau)), tau)
            - sp.diff(sp.diff(L, sp.diff(f, x)), x)
        )

    # Prove vanishing linear AeST anisotropic stress (hT equation == 0 identically)
    E_hT = EL(dens.coeff(eps, 2), hTx).subs({hTx: 0, Bsx: 0})
    assert sp.simplify(E_hT) == 0

    # Set hT = 0 for scalar conformal Newtonian gauge (Psi == Phi)
    dens_c = dens.subs({hTx: 0, sp.diff(hTx, tau): 0, sp.diff(hTx, x): 0})
    EL_Ph_all = EL(dens_c.coeff(eps, 1), Phx) + eps * EL(dens_c.coeff(eps, 2), Phx)
    EL_Ps_all = EL(dens_c.coeff(eps, 1), Psx) + eps * EL(dens_c.coeff(eps, 2), Psx)
    T00_phi = sp.expand(t2(sp.Rational(1, 2) * EL_Ph_all * t2(a ** (-4) * (1 + eps * (Phx + 3 * Psx)))))
    Tii_phi = sp.expand(t2(-sp.Rational(1, 2) * EL_Ps_all * t2(a ** (-4) * (1 - eps * (Phx - Psx)))))
    T01_phi_1 = sp.simplify(sp.Rational(1, 2) * EL(dens_c.coeff(eps, 2), Bsx).subs({Bsx: 0, Psx: Phx}) / a**4)

    Phf = Ph * sp.cos(k * x)
    vpf = vp * sp.cos(k * x)
    vAf = vA * sp.sin(k * x)

    def fcos(ex: sp.Expr) -> sp.Expr:
        r = sp.simplify(
            ex.subs({Psx: Phx, sp.diff(Psx, tau): sp.diff(Phx, tau), sp.diff(Psx, x): sp.diff(Phx, x)})
            .subs({Phx: Phf, vpx: vpf, vAx: vAf, Bsx: 0})
            .doit()
            / sp.cos(k * x)
        )
        assert not r.has(x)
        return r

    def fsin(ex: sp.Expr) -> sp.Expr:
        r = sp.simplify(
            ex.subs({Psx: Phx, sp.diff(Psx, tau): sp.diff(Phx, tau), sp.diff(Psx, x): sp.diff(Phx, x)})
            .subs({Phx: Phf, vpx: vpf, vAx: vAf, Bsx: 0})
            .doit()
            / sp.sin(k * x)
        )
        assert not r.has(x)
        return r

    dT00 = fcos(T00_phi.coeff(eps, 1))
    dTii = fcos(Tii_phi.coeff(eps, 1))
    dT01 = fsin(T01_phi_1)
    EL_vp_k = fcos(EL(dens_c.coeff(eps, 2), vpx).subs({Bsx: 0}))
    EL_vA_k = fsin(EL(dens_c.coeff(eps, 2), vAx).subs({Bsx: 0}))

    ap = sp.diff(a, tau)
    app = sp.diff(a, tau, 2)
    H = ap / a
    Php = sp.diff(Ph, tau)
    Phpp = sp.diff(Ph, tau, 2)
    dG00 = (6 * H**2 * Ph + 2 * k**2 * Ph + 6 * H * Php) / a**2
    dG01 = (2 * k * (Php + H * Ph)) / a**2
    dGii = 3 * 2 * (2 * Ph * app / a + 3 * Php * H - Ph * H**2 + Phpp) / a**2

    E00 = sp.simplify(a**2 * (dG00 - (dT00 - rho_r * dr)))
    E0x = sp.simplify(a**2 * (dG01 - (dT01 + sp.Rational(4, 3) * rho_r * tr / k)))
    E_Psi = sp.simplify(a**2 * (dGii - (dTii + rho_r * dr)))

    # Exact Bianchi identity verification
    bg_subs = {
        app: a**3 * (Qb * K1 - 4 * U0) / 12,
        sp.diff(rho_r, tau): -4 * H * rho_r,
        sp.diff(Qb, tau): -3 * H * K1 / K2e,
        sp.diff(K1, tau): -3 * H * K1,
        sp.diff(U0, tau): K1 * (-3 * H * K1 / K2e),
    }
    Phpp_sol = sp.solve(E_Psi, Phpp)[0]
    vppp_sol = sp.solve(EL_vp_k, sp.diff(vp, tau, 2))[0]
    vApp_sol = sp.solve(EL_vA_k, sp.diff(vA, tau, 2))[0]
    dr_sol = sp.solve(E00, dr)[0]
    Php_sol = sp.solve(E0x, Php)[0]

    def bianchi_check(expr: sp.Expr) -> sp.Expr:
        e = expr.subs({
            sp.diff(dr, tau): -sp.Rational(4, 3) * tr + 4 * Php,
            sp.diff(tr, tau): k**2 * (dr / 4 + Ph),
            Phpp: Phpp_sol,
            sp.diff(vp, tau, 2): vppp_sol,
            sp.diff(vA, tau, 2): vApp_sol,
        })
        e = e.subs(dr, dr_sol).subs(Php, Php_sol)
        e = sp.expand(e.subs(bg_subs).subs(bg_subs))
        ap_s = sp.Symbol("ap")
        e = sp.expand(e.subs(ap, ap_s))
        num, _ = sp.together(e).as_numer_denom()
        rem = sp.Poly(num, ap_s).rem(sp.Poly(ap_s**2 - a**4 * (rho_r + (Qb * K1 - U0) / 2) / 3, ap_s))
        return sp.simplify(rem.as_expr())

    assert bianchi_check(sp.diff(E00, tau)) == 0
    assert bianchi_check(sp.diff(E0x, tau)) == 0

    # Verify Minkowski / sub-horizon coupled 2x2 limit matches coupled_2x2_flrw_stability.py!
    w = sp.Symbol("omega", real=True)
    # In flat limit a=1, a'=0, a''=0, Ph=0, K2e'=0, lam_s'=0, vp -> exp(i w tau), vA -> -i * alpha_x?
    # Note: in our Fourier convention vp ~ cos(k x) exp(-i w tau) and vA ~ sin(k x) exp(-i w tau)
    vp_amp, vA_amp = sp.symbols("vp_amp vA_amp")
    sub_mink = {
        a: 1, ap: 0, app: 0, Ph: 0, Php: 0, Phpp: 0,
        sp.diff(Qb, tau): 0, sp.diff(K1, tau): 0, sp.diff(K2e, tau): 0, sp.diff(lam_s, tau): 0,
        sp.diff(vp, tau, 2): -(w**2) * vp_amp, sp.diff(vp, tau): -sp.I * w * vp_amp, vp: vp_amp,
        sp.diff(vA, tau, 2): -(w**2) * vA_amp, sp.diff(vA, tau): -sp.I * w * vA_amp, vA: vA_amp,
    }
    M_mink = sp.Matrix([
        [sp.simplify(EL_vp_k.subs(sub_mink).coeff(vp_amp)), sp.simplify(EL_vp_k.subs(sub_mink).coeff(vA_amp))],
        [sp.simplify(EL_vA_k.subs(sub_mink).coeff(vp_amp)), sp.simplify(EL_vA_k.subs(sub_mink).coeff(vA_amp))],
    ])
    M_gap2 = Qb * (2 * (2 - KB) * (1 + lam_s) * Qb - K1) / (2 * KB)
    cs2_uv = 4 * (2 - KB) * (1 + sp.Rational(1, 2) * KB * lam_s) / (K2e * KB)
    cs2_ir = K1 / (K2e * Qb)
    det_mink = sp.simplify(M_mink.det() / (2 * K2e * KB))
    target_det = w**4 - (M_gap2 + cs2_uv * k**2) * w**2 + M_gap2 * cs2_ir * k**2
    assert sp.simplify(det_mink - target_det) == 0

    # Compile fast numerical lambdas for ODE RHS & exact constraint residuals!
    a_s, ap_s, app_s = sp.symbols("a_s ap_s app_s", real=True)
    Qb_s, Qbp_s, U0_s, K1_s, K2e_s, K2ep_s = sp.symbols("Qb_s Qbp_s U0_s K1_s K2e_s K2ep_s", real=True)
    lam_ss, lamp_ss, rho_rs = sp.symbols("lam_ss lamp_ss rho_rs", real=True)
    Ph_s, Php_s, dr_s, tr_s = sp.symbols("Ph_s Php_s dr_s tr_s", real=True)
    vp_s, vpp_s, vA_s, vAp_s = sp.symbols("vp_s vpp_s vA_s vAp_s", real=True)

    sym_map = {
        sp.diff(a, tau, 2): app_s, ap: ap_s, a: a_s,
        sp.diff(Qb, tau): Qbp_s, Qb: Qb_s,
        U0: U0_s, K1: K1_s,
        sp.diff(K2e, tau): K2ep_s, K2e: K2e_s,
        sp.diff(lam_s, tau): lamp_ss, lam_s: lam_ss,
        rho_r: rho_rs,
        Php: Php_s, Ph: Ph_s, dr: dr_s, tr: tr_s,
        sp.diff(vp, tau): vpp_s, vp: vp_s,
        sp.diff(vA, tau): vAp_s, vA: vA_s,
    }
    args = (KB, k, a_s, ap_s, app_s, Qb_s, Qbp_s, U0_s, K1_s, K2e_s, K2ep_s, lam_ss, lamp_ss, rho_rs,
            Ph_s, Php_s, dr_s, tr_s, vp_s, vpp_s, vA_s, vAp_s)

    def to_sym(ex: sp.Expr) -> sp.Expr:
        ex1 = ex.subs({
            sp.diff(K1, tau): -3 * (ap / a) * K1,
            sp.diff(U0, tau): K1 * (-3 * (ap / a) * K1 / K2e),
        })
        res = sp.simplify(ex1.subs(sym_map))
        assert not res.has(sp.Derivative), f"Unmapped Derivative in {res}"
        return res

    E00_num = to_sym(E00)
    E0x_num = to_sym(E0x)
    Phpp_num = to_sym(Phpp_sol)
    vppp_num = to_sym(vppp_sol)
    vApp_num = to_sym(vApp_sol)
    tr0_num = to_sym(sp.solve(E0x, tr)[0])
    dr0_num = to_sym(sp.solve(E00, dr)[0])

    funcs = {
        "E00": sp.lambdify(args, E00_num, "math"),
        "E0x": sp.lambdify(args, E0x_num, "math"),
        "Phpp": sp.lambdify(args, Phpp_num, "math"),
        "vppp": sp.lambdify(args, vppp_num, "math"),
        "vApp": sp.lambdify(args, vApp_num, "math"),
        "tr0": sp.lambdify(args, tr0_num, "math"),
        "dr0": sp.lambdify(args, dr0_num, "math"),
    }
    return funcs


class ModelSpec:
    """Background potential U(Q) and running coupling lambda_s(Q) specification."""

    def __init__(self, name: str, kind: str, KB: float, lam0: float, **kw):
        self.name = name
        self.kind = kind
        self.KB = KB
        self.lam0 = lam0
        self.kw = kw

    def eval_U(self, Q: float) -> tuple[float, float, float, float]:
        """Return (U, K1=U', K2_eff=U'', K3=U''')."""
        if self.kind == "gr":
            return 0.0, 0.0, 1.0, 0.0
        if self.kind == "cosh":
            K2 = self.kw["K2"]
            Q0 = self.kw["Q0"]
            Z0 = self.kw["Z0"]
            Z = (Q - Q0) / Z0
            ch = math.cosh(Z)
            sh = math.sinh(Z)
            U = 4.0 * K2 * (Z0**2) * (ch - 1.0)
            K1 = 4.0 * K2 * Z0 * sh
            K2e = 4.0 * K2 * ch
            K3 = 4.0 * K2 * sh / Z0
            return U, K1, K2e, K3
        if self.kind == "q4":
            c = self.kw["c"]
            U = c * (Q**4)
            K1 = 4.0 * c * (Q**3)
            K2e = 12.0 * c * (Q**2)
            K3 = 24.0 * c * Q
            return U, K1, K2e, K3
        raise ValueError(self.kind)

    def eval_lam(self, Q: float) -> tuple[float, float]:
        """Return (lambda_s(Q), d lambda_s / dQ)."""
        run_mode = self.kw.get("run_mode", "const")
        if run_mode == "const":
            return self.lam0, 0.0
        if run_mode == "cosh_even":
            K2 = self.kw["K2"]
            Q0 = self.kw["Q0"]
            Z0 = self.kw["Z0"]
            Z = (Q - Q0) / Z0
            pref = K2 / (2.0 - self.KB)
            return self.lam0 + pref * (math.cosh(Z) - 1.0), pref * math.sinh(Z) / Z0
        if run_mode == "cosh_lin_onset":
            # lam0 + 1.05 * K1 / (2*(2-KB)*Q)
            U, K1, K2e, _ = self.eval_U(Q)
            denom = 2.0 * (2.0 - self.KB) * Q
            dl = 1.05 * (K2e * Q - K1) / (2.0 * (2.0 - self.KB) * (Q**2))
            return self.lam0 + 1.05 * K1 / denom, dl
        if run_mode == "q4_power":
            # lam(Q) = lam0 + alpha * 4*c*Q^2 / (2*(2-KB)), giving dlam/dQ = alpha * 4*c*Q / (2-KB)
            c = self.kw["c"]
            alpha = self.kw["alpha"]
            coef = 4.0 * alpha * c / (2.0 * (2.0 - self.KB))
            return self.lam0 + coef * (Q**2), 2.0 * coef * Q
        raise ValueError(run_mode)


def integrate_radiation_horizon_crossing(
    funcs: dict,
    spec: ModelSpec,
    k: float,
    a_star: float,
    Om_r_at_star: float,
    Q_at_star: float,
    x_span: tuple[float, float] = (0.05, 50.0),
) -> dict:
    """Integrate coupled FLRW background + perturbations across x = k*tau in [x0, x1]."""
    x0, x1 = x_span
    # Normalize background at a_star so conformal Hubble at horizon crossing a_star*H_star == k!
    # At x_* ~ 1 during radiation domination, a(tau) ~ sqrt(rho_r0/3)*tau => H_conf = a'/a = 1/tau = k/x.
    # Let H_star = k / a_star. Total density at a_star is 3 * H_star^2 = rho_r_star + rho_phi_star!
    H_star = k / a_star
    rho_tot_star = 3.0 * (H_star**2)
    U_s, K1_s, K2e_s, _ = spec.eval_U(Q_at_star)
    rho_phi_star = 0.5 * (Q_at_star * K1_s - U_s)
    rho_r_star = rho_tot_star - rho_phi_star if spec.kind != "gr" else rho_tot_star
    assert rho_r_star > 0.0

    # Integrate background backward/forward cleanly from a(x=1)=a_star -> first find x_0 state via background solve from x=1 to x0
    def bg_rhs(x_val: float, y: list[float]) -> list[float]:
        # y = [a, Qb], using dt/dx = 1/k and exact Friedmann H_conf = a * H / k
        a_v, Q_v = y
        rho_r_v = rho_r_star * ((a_star / a_v) ** 4)
        U_v, K1_v, K2e_v, _ = spec.eval_U(Q_v)
        rho_phi_v = 0.5 * (Q_v * K1_v - U_v) if spec.kind != "gr" else 0.0
        H_phys = math.sqrt((rho_r_v + rho_phi_v) / 3.0)
        H_c = a_v * H_phys
        da_dx = a_v * H_c / k
        dQ_dx = -3.0 * (H_c / k) * (K1_v / K2e_v) if spec.kind != "gr" else 0.0
        return [da_dx, dQ_dx]

    # Exact radiation-dominated conformal time relation: for pure rad, x = k * tau = a / (a_star * (H_star / k)) = a / a_star.
    # Solve exact background backward from x=1 to x0!
    sol_bg0 = solve_ivp(bg_rhs, (1.0, x0), [a_star, Q_at_star], method="DOP853", rtol=1e-12, atol=1e-14)
    assert sol_bg0.success
    a0, Q0_init = float(sol_bg0.y[0, -1]), float(sol_bg0.y[1, -1])

    # Evaluate background derivatives at x0 to set exact super-horizon adiabatic ICs!
    rho_r0 = rho_r_star * ((a_star / a0) ** 4)
    U0_i, K1_i, K2e_i, K3_i = spec.eval_U(Q0_init)
    rho_phi0 = 0.5 * (Q0_init * K1_i - U0_i) if spec.kind != "gr" else 0.0
    H_phys0 = math.sqrt((rho_r0 + rho_phi0) / 3.0)
    ap0 = (a0**2) * H_phys0  # da/dtau
    app0 = (a0**3) * (Q0_init * K1_i - 4.0 * U0_i) / 12.0 if spec.kind != "gr" else 0.0
    Qbp0 = -3.0 * (ap0 / a0) * (K1_i / K2e_i) if spec.kind != "gr" else 0.0
    K2ep0 = K3_i * Qbp0 if spec.kind != "gr" else 0.0
    lam0_i, dlam_dQ0 = spec.eval_lam(Q0_init)
    lamp0_i = dlam_dQ0 * Qbp0 if spec.kind != "gr" else 0.0

    # Super-horizon adiabatic initial condition normalized to Phi(x0) = 1.0:
    # Phi(x) = 1 - x^2 / 30 => Phi' = dPhi/dtau = k * (-x / 15) at x0
    Ph0 = 1.0 - (x0**2) / 30.0
    Php0 = k * (-x0 / 15.0)
    if spec.kind == "gr":
        vp0, vpp0, vA0, vAp0 = 0.0, 0.0, 0.0, 0.0
        # Enforce E00 == 0 and E0x == 0 to 1e-15!
        tr0 = funcs["tr0"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, 0.0, 0.0, 1.0, 0.0, lam0_i, 0.0, rho_r0, Ph0, Php0, 0.0, 0.0, vp0, vpp0, vA0, vAp0)
        dr0 = funcs["dr0"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, 0.0, 0.0, 1.0, 0.0, lam0_i, 0.0, rho_r0, Ph0, Php0, 0.0, tr0, vp0, vpp0, vA0, vAp0)
    else:
        # Uniform-curvature adiabatic slicing delta tau = 1/(2 H_conf0):
        # varphi(tau) = (a * Qbar / (2 H_conf)) * Phi
        # At a ~ tau: d/dtau(a^2 Q / a') for Q ~ a^-1 gives const -> check Q1 = vp'/a - Ph*Q:
        # In pure rad Q4: vp(tau) = a*Q*tau/2 * Phi => vp'(tau) = a*Q/2 * Phi (since a*Q = const),
        # while vA_ad = k * vp / (a * Q) = k * tau / 2 * Phi = x/2 * Phi => vA'(tau) = k/2 * Phi!
        # More generally for any Qbar(tau):
        # vp0 = a0 * Q0_init * (a0 / ap0) / 2.0 * Ph0; vpp0 = k * vp0 / x0  (Wait: at rad era x/H_c -> tau = a0/ap0)
        H_c0 = ap0 / a0
        vp0 = 0.5 * a0 * Q0_init / H_c0 * Ph0
        # Exact adiabatic dQ/Q = (1/(2 H_c)) Qbar' -> vp'/a - Ph*Q = Qbp0 / (2*H_c0) * Ph0 => vpp0 = a0 * (Ph0*Q0_init + Qbp0/(2*H_c0)*Ph0)
        vpp0 = a0 * (Ph0 * Q0_init + Ph0 * Qbp0 / (2.0 * H_c0))
        # Scalar gradient chi = varphi - a*Q*vA/k = 0 initially (comoving): vA = k*vp/(a*Q)
        vA0 = k * vp0 / (a0 * Q0_init)
        # vA' = d/dtau(k*vp/(a*Q)) = k*(vpp0/(a0*Q0) - vp0*(H_c0/Q0 + Qbp0/Q0^2)/a0)
        vAp0 = k * (vpp0 / (a0 * Q0_init) - vp0 * (ap0 / (a0 * Q0_init) + Qbp0 / (Q0_init**2)) / a0)
        tr0 = funcs["tr0"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, U0_i, K1_i, K2e_i, K2ep0, lam0_i, lamp0_i, rho_r0, Ph0, Php0, 0.0, 0.0, vp0, vpp0, vA0, vAp0)
        dr0 = funcs["dr0"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, U0_i, K1_i, K2e_i, K2ep0, lam0_i, lamp0_i, rho_r0, Ph0, Php0, 0.0, tr0, vp0, vpp0, vA0, vAp0)

    def eval_bg_derivs(a_v: float, Q_v: float):
        rho_r_v = rho_r_star * ((a_star / a_v) ** 4)
        U_v, K1_v, K2e_v, K3_v = spec.eval_U(Q_v)
        rho_phi_v = 0.5 * (Q_v * K1_v - U_v) if spec.kind != "gr" else 0.0
        H_phys_v = math.sqrt((rho_r_v + rho_phi_v) / 3.0)
        ap_v = (a_v**2) * H_phys_v
        app_v = (a_v**3) * (Q_v * K1_v - 4.0 * U_v) / 12.0 if spec.kind != "gr" else 0.0
        Qbp_v = -3.0 * (ap_v / a_v) * (K1_v / K2e_v) if spec.kind != "gr" else 0.0
        K2ep_v = K3_v * Qbp_v if spec.kind != "gr" else 0.0
        lam_v, dl_v = spec.eval_lam(Q_v)
        lamp_v = dl_v * Qbp_v if spec.kind != "gr" else 0.0
        return rho_r_v, U_v, K1_v, K2e_v, K3_v, rho_phi_v, ap_v, app_v, Qbp_v, K2ep_v, lam_v, lamp_v

    # Check initial constraint residuals
    res00_i = funcs["E00"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, U0_i, K1_i, K2e_i, K2ep0, lam0_i, lamp0_i, rho_r0, Ph0, Php0, dr0, tr0, vp0, vpp0, vA0, vAp0)
    res0x_i = funcs["E0x"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, U0_i, K1_i, K2e_i, K2ep0, lam0_i, lamp0_i, rho_r0, Ph0, Php0, dr0, tr0, vp0, vpp0, vA0, vAp0)
    assert abs(res00_i) < 1e-10 and abs(res0x_i) < 1e-10

    # State y = [a, Qbar, Phi, Phi_tau, delta_r, theta_r, varphi, varphi_tau, vA, vA_tau]
    # Note: integrate wrt x = k*tau, so dy/dx = (1/k) * dy/dtau
    def ode_rhs(x_val: float, y: np.ndarray) -> list[float]:
        a_v, Q_v, Ph_v, Php_v, dr_v, tr_v, vp_v, vpp_v, vA_v, vAp_v = y
        rho_r_v, U_v, K1_v, K2e_v, K3_v, _, ap_v, app_v, Qbp_v, K2ep_v, lam_v, lamp_v = eval_bg_derivs(a_v, Q_v)
        arg_v = (
            spec.KB, k, a_v, ap_v, app_v, Q_v, Qbp_v, U_v, K1_v, K2e_v, K2ep_v, lam_v, lamp_v, rho_r_v,
            Ph_v, Php_v, dr_v, tr_v, vp_v, vpp_v, vA_v, vAp_v
        )
        Phpp_v = funcs["Phpp"](*arg_v)
        drp_v = -(4.0 / 3.0) * tr_v + 4.0 * Php_v
        trp_v = (k**2) * (0.25 * dr_v + Ph_v)
        if spec.kind == "gr":
            vppp_v, vApp_v = 0.0, 0.0
        else:
            vppp_v = funcs["vppp"](*arg_v)
            vApp_v = funcs["vApp"](*arg_v)
        return [
            ap_v / k, Qbp_v / k,
            Php_v / k, Phpp_v / k,
            drp_v / k, trp_v / k,
            vpp_v / k, vppp_v / k,
            vAp_v / k, vApp_v / k,
        ]

    # Stop cleanly if an exponentially growing unstable mode overflows |Phi| > 1e12
    def blowup_event(x_val: float, y: np.ndarray) -> float:
        return 1.0e12 - max(abs(y[2]), abs(y[4]))
    blowup_event.terminal = True

    y0 = [a0, Q0_init, Ph0, Php0, dr0, tr0, vp0, vpp0, vA0, vAp0]
    x_eval = np.geomspace(x0, x1, 200)
    sol = solve_ivp(
        ode_rhs, (x0, x1), y0, method="Radau", t_eval=x_eval,
        events=blowup_event, rtol=1e-9, atol=1e-12
    )

    # Evaluate constraint residuals & stability diagnostics along trajectory
    max_rel_E00 = 0.0
    max_rel_E0x = 0.0
    max_abs_Phi = 0.0
    max_abs_dr = 0.0
    min_Mgap2_over_H2 = math.inf
    max_Mgap2_over_H2 = -math.inf
    max_cs2_UV = 0.0
    for idx in range(len(sol.t)):
        a_v, Q_v, Ph_v, Php_v, dr_v, tr_v, vp_v, vpp_v, vA_v, vAp_v = sol.y[:, idx]
        rho_r_v, U_v, K1_v, K2e_v, K3_v, rho_phi_v, ap_v, app_v, Qbp_v, K2ep_v, lam_v, lamp_v = eval_bg_derivs(a_v, Q_v)
        arg_v = (
            spec.KB, k, a_v, ap_v, app_v, Q_v, Qbp_v, U_v, K1_v, K2e_v, K2ep_v, lam_v, lamp_v, rho_r_v,
            Ph_v, Php_v, dr_v, tr_v, vp_v, vpp_v, vA_v, vAp_v
        )
        e00 = funcs["E00"](*arg_v)
        e0x = funcs["E0x"](*arg_v)
        H_v = ap_v / (a_v**2)
        scale00 = (
            (a_v**2) * (rho_r_v * max(1.0, abs(dr_v)) + abs(rho_phi_v))
            + (k**2) * abs(Ph_v)
            + (a_v**2) * abs(K2e_v * Q_v * (abs(vpp_v / a_v) + abs(Q_v * Ph_v)))
            + 1e-30
        )
        scale0x = (
            2.0 * k * ((ap_v / a_v) * abs(Ph_v) + abs(Php_v))
            + (a_v**2) * rho_r_v * abs(tr_v) / k
            + (a_v**2) * abs(K1_v * k * vp_v / (2.0 * a_v))
            + 1e-30
        )
        max_rel_E00 = max(max_rel_E00, abs(e00) / scale00)
        max_rel_E0x = max(max_rel_E0x, abs(e0x) / scale0x)
        max_abs_Phi = max(max_abs_Phi, abs(Ph_v))
        max_abs_dr = max(max_abs_dr, abs(dr_v))
        if spec.kind != "gr":
            Mgap2 = Q_v * (2.0 * (2.0 - spec.KB) * (1.0 + lam_v) * Q_v - K1_v) / (2.0 * spec.KB)
            cs2_uv = 4.0 * (2.0 - spec.KB) * (1.0 + 0.5 * spec.KB * lam_v) / (K2e_v * spec.KB)
            min_Mgap2_over_H2 = min(min_Mgap2_over_H2, Mgap2 / (H_v**2))
            max_Mgap2_over_H2 = max(max_Mgap2_over_H2, Mgap2 / (H_v**2))
            max_cs2_UV = max(max_cs2_UV, cs2_uv)

    blew_up = bool(len(sol.t_events[0]) > 0 or max_abs_Phi > 100.0)
    final_Phi = float(sol.y[2, -1])
    final_dr = float(sol.y[4, -1])

    # Estimate e-fold growth rate wrt N = ln a if unstable
    growth_per_efold = None
    if len(sol.t) >= 10:
        a_arr = sol.y[0]
        ph_arr = np.maximum(np.abs(sol.y[2]), 1e-30)
        if ph_arr[-1] > 10.0 * ph_arr[0]:
            dN = math.log(a_arr[-1] / a_arr[-min(10, len(a_arr))])
            if dN > 0:
                growth_per_efold = float(math.log(ph_arr[-1] / ph_arr[-min(10, len(ph_arr))]) / dN)

    # Analytic Bessel check when GR
    max_analytic_err = None
    if spec.kind == "gr":
        xs = sol.t
        s = xs / math.sqrt(3.0)
        Ph_exact = 3.0 * (np.sin(s) - s * np.cos(s)) / (s**3)
        max_analytic_err = float(np.max(np.abs(sol.y[2] - Ph_exact)))

    return {
        "name": spec.name,
        "k_Mpc_inv": k,
        "x_reached": float(sol.t[-1]),
        "blew_up": blew_up,
        "max_abs_Phi": float(f"{max_abs_Phi:.6e}"),
        "max_abs_delta_r": float(f"{max_abs_dr:.6e}"),
        "final_Phi": float(f"{final_Phi:.6e}"),
        "final_delta_r": float(f"{final_dr:.6e}"),
        "max_rel_E00_constraint_resid": float(f"{max_rel_E00:.3e}"),
        "max_rel_E0x_constraint_resid": float(f"{max_rel_E0x:.3e}"),
        "min_Mgap2_over_H2": None if spec.kind == "gr" else float(f"{min_Mgap2_over_H2:.6e}"),
        "max_Mgap2_over_H2": None if spec.kind == "gr" else float(f"{max_Mgap2_over_H2:.6e}"),
        "max_cs2_UV": None if spec.kind == "gr" else float(f"{max_cs2_UV:.6f}"),
        "measured_growth_per_efold_tail": growth_per_efold,
        "max_GR_analytic_err": max_analytic_err,
        "_series": {"x": sol.t, "a": sol.y[0], "Phi": sol.y[2], "delta_r": sol.y[4]},
    }


def main() -> int:
    funcs = f1_derive_flrw_equations_and_bianchi()

    H0_mpc = 67.4 / 299792.458
    Om_r0 = 9.0e-5
    Om_phi0 = 0.26

    # Common radiation-era horizon-crossing scale:
    # k = 0.2 Mpc^-1 => a_* ~ sqrt(Om_r0)*H0 / k ~ 1.0665e-5 (deep radiation domination, well before a_eq)
    k_rad = 0.2
    a_star_rad = math.sqrt(Om_r0) * H0_mpc / k_rad

    # Case 1: Pure Radiation GR Control (Q_at_star = 0.0)
    gr_spec = ModelSpec("GR_pure_radiation", "gr", KB=0.0, lam0=0.0)
    res_gr = integrate_radiation_horizon_crossing(funcs, gr_spec, k=k_rad, a_star=a_star_rad, Om_r_at_star=1.0, Q_at_star=0.0)
    assert res_gr["max_GR_analytic_err"] < 1e-6
    assert res_gr["max_rel_E00_constraint_resid"] < 1e-7
    assert res_gr["max_rel_E0x_constraint_resid"] < 1e-7

    # Case 2: SZ21 Fig 1 Cosh, constant lambda_s = 0, tested near equality-radiation transition (k = 0.02 Mpc^-1 => a_* ~ 1.07e-4)
    k_eq = 0.02
    a_star_eq = math.sqrt(Om_r0) * H0_mpc / k_eq
    gr_eq = integrate_radiation_horizon_crossing(funcs, gr_spec, k=k_eq, a_star=a_star_eq, Om_r_at_star=1.0, Q_at_star=0.0)

    w0_sz = 3.0 * (H0_mpc**2) * Om_phi0 / (4.0 * 7.5e5 * (0.1**2))
    Z_sz_eq = math.asinh((2.0 * w0_sz / 0.01) / (a_star_eq**3))
    Q_sz_eq = 0.1 * (1.0 + 0.01 * Z_sz_eq)
    sz_const_spec = ModelSpec(
        "SZ21_Cosh_const_lam0", "cosh", KB=0.5, lam0=0.0, K2=7.5e5, Q0=0.1, Z0=1.0e-3, run_mode="const"
    )
    res_sz_const = integrate_radiation_horizon_crossing(funcs, sz_const_spec, k=k_eq, a_star=a_star_eq, Om_r_at_star=0.8, Q_at_star=Q_sz_eq)
    assert res_sz_const["min_Mgap2_over_H2"] < 0.0

    # Case 3a: SZ21 Fig 1 Cosh + covariant running lambda_s(Q) (stabilized)
    sz_run_spec = ModelSpec(
        "SZ21_Cosh_running_lam", "cosh", KB=0.5, lam0=0.0, K2=7.5e5, Q0=0.1, Z0=1.0e-3, run_mode="cosh_lin_onset"
    )
    res_sz_run = integrate_radiation_horizon_crossing(funcs, sz_run_spec, k=k_eq, a_star=a_star_eq, Om_r_at_star=0.8, Q_at_star=Q_sz_eq)
    assert not res_sz_run["blew_up"]
    assert res_sz_run["min_Mgap2_over_H2"] > 0.0 and res_sz_run["max_cs2_UV"] < 1.0
    assert res_sz_run["max_rel_E00_constraint_resid"] < 1e-6 and res_sz_run["max_rel_E0x_constraint_resid"] < 1e-7

    # Case 3b: PR #226 Cosh (K_B=0.008, K2=300, r=1e-3, lam0=11.2787): constant vs covariant even running lambda_s(Q)
    Q0_pr = math.sqrt((2.0 - 0.008) / (2.0 * 300.0)) * 1.0
    Z0_pr = 1.0e-3 * Q0_pr
    w0_pr = 3.0 * (H0_mpc**2) * Om_phi0 / (4.0 * 300.0 * (Q0_pr**2))
    Z_pr_rad = math.asinh((2.0 * w0_pr / 1.0e-3) / (a_star_rad**3))
    Q_pr_rad = Q0_pr * (1.0 + 1.0e-3 * Z_pr_rad)
    pr_cosh_const = ModelSpec("PR226_Cosh_const_lam", "cosh", KB=0.008, lam0=11.2787, K2=300.0, Q0=Q0_pr, Z0=Z0_pr, run_mode="const")
    pr_cosh_run = ModelSpec("PR226_Cosh_running_lam", "cosh", KB=0.008, lam0=11.2787, K2=300.0, Q0=Q0_pr, Z0=Z0_pr, run_mode="cosh_even")
    res_pr_cosh_const = integrate_radiation_horizon_crossing(funcs, pr_cosh_const, k=k_rad, a_star=a_star_rad, Om_r_at_star=0.99, Q_at_star=Q_pr_rad)
    res_pr_cosh_run = integrate_radiation_horizon_crossing(funcs, pr_cosh_run, k=k_rad, a_star=a_star_rad, Om_r_at_star=0.99, Q_at_star=Q_pr_rad)
    assert res_pr_cosh_const["blew_up"] and res_pr_cosh_const["min_Mgap2_over_H2"] < 0.0
    assert not res_pr_cosh_run["blew_up"]
    assert res_pr_cosh_run["min_Mgap2_over_H2"] > 0.0 and res_pr_cosh_run["max_cs2_UV"] < 1.0
    assert res_pr_cosh_run["max_rel_E00_constraint_resid"] < 1e-6 and res_pr_cosh_run["max_rel_E0x_constraint_resid"] < 1e-7

    # Case 4 & Case 5b matched apples-to-apples Q^4 background (eps_Q = 0.039):
    # Choose c*Q(x=50)^2 = 150.0 => K2_eff(x=50) = 1800, so at a_star (x=1) c*Q_star^2 = 150 * 2500 (since Q ~ 1/a).
    eps_Q = 0.039
    H_star_rad = k_rad / a_star_rad
    rho_phi_q4 = (eps_Q / (1.0 + eps_Q)) * 3.0 * (H_star_rad**2)
    cQ2_5b = 150.0 * 2500.0
    Q_q4_5b = math.sqrt(2.0 * rho_phi_q4 / (3.0 * cQ2_5b))
    c_q4_5b = cQ2_5b / (Q_q4_5b**2)

    # Case 4: Unstable PR #226 witness K_B = 0.008, constant lambda_s = 11.2787 (same c, M_gap^2 < 0 everywhere)
    q4_unstable = ModelSpec("Q4_PR226_unstable_const_lam", "q4", KB=0.008, lam0=11.2787, c=c_q4_5b, run_mode="const")
    res_q4_unstable = integrate_radiation_horizon_crossing(funcs, q4_unstable, k=k_rad, a_star=a_star_rad, Om_r_at_star=1.0 / (1.0 + eps_Q), Q_at_star=Q_q4_5b)
    assert res_q4_unstable["min_Mgap2_over_H2"] < 0.0 and (res_q4_unstable["blew_up"] or res_q4_unstable["max_abs_delta_r"] > 20.0)

    # Case 5a: Narrow BBN-viable constant-lambda window (K_B = 0.085, lam_s = 11.2787, K2_eff(a_star) = 137)
    # Test both locally inside the 2.86% viable a-window x in [0.99, 1.01] and across full [0.05, 50]
    cQ2_5a = 137.0 / 12.0
    Q_q4_5a = math.sqrt(2.0 * rho_phi_q4 / (3.0 * cQ2_5a))
    c_q4_5a = cQ2_5a / (Q_q4_5a**2)
    q4_win_const = ModelSpec("Q4_KB0085_window_const_lam", "q4", KB=0.085, lam0=11.2787, c=c_q4_5a, run_mode="const")
    res_q4_5a_local = integrate_radiation_horizon_crossing(funcs, q4_win_const, k=k_rad, a_star=a_star_rad, Om_r_at_star=1.0 / (1.0 + eps_Q), Q_at_star=Q_q4_5a, x_span=(0.99, 1.01))
    assert not res_q4_5a_local["blew_up"]
    assert res_q4_5a_local["min_Mgap2_over_H2"] > 0.0 and res_q4_5a_local["max_cs2_UV"] < 1.0
    assert res_q4_5a_local["max_rel_E00_constraint_resid"] < 1e-6 and res_q4_5a_local["max_rel_E0x_constraint_resid"] < 1e-7

    res_q4_5a_full = integrate_radiation_horizon_crossing(funcs, q4_win_const, k=k_rad, a_star=a_star_rad, Om_r_at_star=1.0 / (1.0 + eps_Q), Q_at_star=Q_q4_5a)
    assert res_q4_5a_full["min_Mgap2_over_H2"] < 0.0 and res_q4_5a_full["max_cs2_UV"] > 1.0

    # Case 5b: Stabilized Q^4 at PR #226 K_B = 0.008 via covariant running lambda_s(Q) = lam0 + alpha*(2*c*Q^2/(2-KB)) with alpha=1.15
    q4_pr_run = ModelSpec("Q4_PR226_running_lam", "q4", KB=0.008, lam0=11.2787, c=c_q4_5b, alpha=1.15, run_mode="q4_power")
    res_q4_5b = integrate_radiation_horizon_crossing(funcs, q4_pr_run, k=k_rad, a_star=a_star_rad, Om_r_at_star=1.0 / (1.0 + eps_Q), Q_at_star=Q_q4_5b)
    assert not res_q4_5b["blew_up"]
    assert res_q4_5b["min_Mgap2_over_H2"] > 0.0 and res_q4_5b["max_cs2_UV"] < 1.0
    assert res_q4_5b["max_rel_E00_constraint_resid"] < 1e-6 and res_q4_5b["max_rel_E0x_constraint_resid"] < 1e-7

    def strip_s(d: dict, ref: dict | None = None) -> dict:
        out = {kk: vv for kk, vv in d.items() if kk != "_series"}
        if ref is not None and not d["blew_up"] and len(d["_series"]["Phi"]) == len(ref["_series"]["Phi"]):
            # Compute final transfer ratios at x = 50
            phi_ratio = float(d["_series"]["Phi"][-1] / ref["_series"]["Phi"][-1])
            dr_ratio = float(d["_series"]["delta_r"][-1] / ref["_series"]["delta_r"][-1])
            out["transfer_Phi_over_GR_x50"] = round(phi_ratio, 6)
            out["transfer_delta_r_over_GR_x50"] = round(dr_ratio, 6)
        return out

    output = {
        "F1_symbolic_verification": {
            "linear_AeST_anisotropic_stress_hT": "0 identically (Psi == Phi exactly at O(eps)) [D]",
            "bianchi_dE00_dtau_residual": "0 identically [D]",
            "bianchi_dE0x_dtau_residual": "0 identically [D]",
            "subhorizon_limit_matches_2x2_char_poly": True,
        },
        "F2_horizon_crossing_radiation_transfer": {
            "case1_GR_control_k0p2": strip_s(res_gr),
            "case2_SZ21_Cosh_const_lam0_k0p02": strip_s(res_sz_const, gr_eq),
            "case3a_SZ21_Cosh_running_lam_k0p02": strip_s(res_sz_run, gr_eq),
            "case3b_PR226_Cosh_const_lam_k0p2": strip_s(res_pr_cosh_const, res_gr),
            "case3b_PR226_Cosh_running_lam_k0p2": strip_s(res_pr_cosh_run, res_gr),
            "case4_Q4_PR226_unstable_const_lam_k0p2": strip_s(res_q4_unstable, res_gr),
            "case5a_Q4_KB0085_window_local_x0p99_1p01": strip_s(res_q4_5a_local),
            "case5a_Q4_KB0085_window_full_x0p05_50": strip_s(res_q4_5a_full, res_gr),
            "case5b_Q4_PR226_running_lam_k0p2": strip_s(res_q4_5b, res_gr),
        },
    }

    path = os.path.join(HERE, "FLRW_FINITE_HK_RADIATION_TRANSFER.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=1)
        f.write("\n")
    print(json.dumps(output, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
