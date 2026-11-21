#!/usr/bin/env python3
"""Gate 1 audit: Keep or kill the Cosh tracker vs Q^4 through matter-radiation equality.

Extends audits/2026-11-20/flrw_finite_hk_radiation_transfer.py by adding pressureless CDM
(Omega_m, delta_m, theta_m) to the exact linearized Conformal-Newtonian AeST + radiation
FLRW system, re-proving exact symbolic Bianchi conservation (dE00/dtau == 0, dE0x/dtau == 0)
with CDM included, verifying exact continuity with the radiation-era x=50 run (10.493924
for PR226 Cosh vs pure-radiation GR; 0.897430 for Q^4), and integrating through a_eq to
10 * a_eq at k = 0.2 Mpc^-1 (and cross-checks k = 0.1, 0.05 Mpc^-1) against BOTH:
  (1) Pure-radiation GR (Omega_m = 0), and
  (2) Matched LCDM (Omega_r0 = 9e-5, Omega_m0 = 0.26, a_eq = 3.4615e-4).

Labels: [P] proved, [D] derived here, [C] cited, [X] killed/excluded, [O] open.
"""
from __future__ import annotations

import json
import math
import os
import sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))


def f1_derive_flrw_with_cdm() -> dict:
    """Derive exact linearized FLRW AeST + radiation + CDM equations and prove Bianchi."""
    tau, x, eps, KB, k = sp.symbols("tau x eps K_B k", real=True)
    a = sp.Function("a")(tau)
    Qb = sp.Function("Qbar")(tau)
    U0 = sp.Function("U0")(tau)
    K1 = sp.Function("K1")(tau)
    K2e = sp.Function("K2e")(tau)
    lam_s = sp.Function("lam_s")(tau)
    rho_r = sp.Function("rho_r")(tau)
    rho_m = sp.Function("rho_m")(tau)

    Ph = sp.Function("Phi")(tau)
    vp = sp.Function("varphi")(tau)
    vA = sp.Function("vA")(tau)
    dr = sp.Function("delta_r")(tau)
    tr = sp.Function("theta_r")(tau)
    dm = sp.Function("delta_m")(tau)
    tm = sp.Function("theta_m")(tau)

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

    # Zero linear AeST anisotropic stress (Psi == Phi identically)
    E_hT = EL(dens.coeff(eps, 2), hTx).subs({hTx: 0, Bsx: 0})
    assert sp.simplify(E_hT) == 0

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

    # Full AeST + radiation + pressureless CDM constraint & spatial equations
    E00 = sp.simplify(a**2 * (dG00 - (dT00 - rho_r * dr - rho_m * dm)))
    E0x = sp.simplify(a**2 * (dG01 - (dT01 + sp.Rational(4, 3) * rho_r * tr / k + rho_m * tm / k)))
    E_Psi = sp.simplify(a**2 * (dGii - (dTii + rho_r * dr)))

    # Exact Bianchi identity verification with CDM + radiation + AeST
    bg_subs = {
        app: a**3 * (2 * rho_m + Qb * K1 - 4 * U0) / 12,
        sp.diff(rho_r, tau): -4 * H * rho_r,
        sp.diff(rho_m, tau): -3 * H * rho_m,
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
            sp.diff(dm, tau): -tm + 3 * Php,
            sp.diff(tm, tau): -H * tm + k**2 * Ph,
            Phpp: Phpp_sol,
            sp.diff(vp, tau, 2): vppp_sol,
            sp.diff(vA, tau, 2): vApp_sol,
        })
        e = e.subs(dr, dr_sol).subs(Php, Php_sol)
        e = sp.expand(e.subs(bg_subs).subs(bg_subs))
        ap_s = sp.Symbol("ap")
        e = sp.expand(e.subs(ap, ap_s))
        num, _ = sp.together(e).as_numer_denom()
        rem = sp.Poly(num, ap_s).rem(sp.Poly(ap_s**2 - a**4 * (rho_r + rho_m + (Qb * K1 - U0) / 2) / 3, ap_s))
        return sp.simplify(rem.as_expr())

    assert bianchi_check(sp.diff(E00, tau)) == 0
    assert bianchi_check(sp.diff(E0x, tau)) == 0

    # Compile fast numerical lambdas
    a_s, ap_s, app_s = sp.symbols("a_s ap_s app_s", real=True)
    Qb_s, Qbp_s, U0_s, K1_s, K2e_s, K2ep_s = sp.symbols("Qb_s Qbp_s U0_s K1_s K2e_s K2ep_s", real=True)
    lam_ss, lamp_ss, rho_rs, rho_ms = sp.symbols("lam_ss lamp_ss rho_rs rho_ms", real=True)
    Ph_s, Php_s, dr_s, tr_s, dm_s, tm_s = sp.symbols("Ph_s Php_s dr_s tr_s dm_s tm_s", real=True)
    vp_s, vpp_s, vA_s, vAp_s = sp.symbols("vp_s vpp_s vA_s vAp_s", real=True)

    sym_map = {
        sp.diff(a, tau, 2): app_s, ap: ap_s, a: a_s,
        sp.diff(Qb, tau): Qbp_s, Qb: Qb_s,
        U0: U0_s, K1: K1_s,
        sp.diff(K2e, tau): K2ep_s, K2e: K2e_s,
        sp.diff(lam_s, tau): lamp_ss, lam_s: lam_ss,
        rho_r: rho_rs, rho_m: rho_ms,
        Php: Php_s, Ph: Ph_s, dr: dr_s, tr: tr_s, dm: dm_s, tm: tm_s,
        sp.diff(vp, tau): vpp_s, vp: vp_s,
        sp.diff(vA, tau): vAp_s, vA: vA_s,
    }
    args = (KB, k, a_s, ap_s, app_s, Qb_s, Qbp_s, U0_s, K1_s, K2e_s, K2ep_s, lam_ss, lamp_ss,
            rho_rs, rho_ms, Ph_s, Php_s, dr_s, tr_s, dm_s, tm_s, vp_s, vpp_s, vA_s, vAp_s)

    def to_sym(ex: sp.Expr) -> sp.Expr:
        ex1 = ex.subs({
            sp.diff(K1, tau): -3 * (ap / a) * K1,
            sp.diff(U0, tau): K1 * (-3 * (ap / a) * K1 / K2e),
            sp.diff(rho_r, tau): -4 * (ap / a) * rho_r,
            sp.diff(rho_m, tau): -3 * (ap / a) * rho_m,
        })
        res = sp.simplify(ex1.subs(sym_map))
        assert not res.has(sp.Derivative), f"Unmapped Derivative in {res}"
        return res

    E00_num = to_sym(E00)
    E0x_num = to_sym(E0x)
    Phpp_num = to_sym(Phpp_sol)
    vppp_num = to_sym(vppp_sol)
    vApp_num = to_sym(vApp_sol)
    # Adiabatic IC helpers: set tm = tr and dm = (3/4)*dr symbolically inside E0x, E00
    tr0_ad_num = to_sym(sp.solve(E0x.subs(tm, tr), tr)[0])
    dr0_ad_num = to_sym(sp.solve(E00.subs(dm, sp.Rational(3, 4) * dr), dr)[0])
    delta_rho_phi_num = to_sym(-dT00)

    return {
        "E00": sp.lambdify(args, E00_num, "math"),
        "E0x": sp.lambdify(args, E0x_num, "math"),
        "Phpp": sp.lambdify(args, Phpp_num, "math"),
        "vppp": sp.lambdify(args, vppp_num, "math"),
        "vApp": sp.lambdify(args, vApp_num, "math"),
        "tr0_ad": sp.lambdify(args, tr0_ad_num, "math"),
        "dr0_ad": sp.lambdify(args, dr0_ad_num, "math"),
        "delta_rho_phi": sp.lambdify(args, delta_rho_phi_num, "math"),
    }


class ModelSpec:
    """Background potential U(Q) and running coupling lambda_s(Q)."""

    def __init__(self, name: str, kind: str, KB: float, lam0: float, **kw):
        self.name = name
        self.kind = kind
        self.KB = KB
        self.lam0 = lam0
        self.kw = kw

    def eval_U(self, Q: float) -> tuple[float, float, float, float]:
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
            _, K1, K2e, _ = self.eval_U(Q)
            denom = 2.0 * (2.0 - self.KB) * Q
            dl = 1.05 * (K2e * Q - K1) / (2.0 * (2.0 - self.KB) * (Q**2))
            return self.lam0 + 1.05 * K1 / denom, dl
        if run_mode == "q4_power":
            c = self.kw["c"]
            alpha = self.kw["alpha"]
            coef = 4.0 * alpha * c / (2.0 * (2.0 - self.KB))
            return self.lam0 + coef * (Q**2), 2.0 * coef * Q
        raise ValueError(run_mode)


def eval_cosh_Q_at_a(a_val: float, K2: float, Q0: float, Z0: float, H0_mpc: float, Om_phi0: float) -> float:
    """Exact analytic solution of dQ/d(ln a) = -3 K1/K2e for cosh: sinh Z(a) = (2 w0 / r)/a^3."""
    r = Z0 / Q0
    w0 = 3.0 * (H0_mpc**2) * Om_phi0 / (4.0 * K2 * (Q0**2))
    Z = math.asinh((2.0 * w0 / r) / (a_val**3))
    return Q0 * (1.0 + r * Z)


def integrate_transfer(
    funcs: dict,
    spec: ModelSpec,
    k: float,
    H0_mpc: float,
    Om_r0: float,
    Om_m0: float,
    Om_phi_today: float,
    eps_Q_q4: float,
    c_q4_ref_a: float | None,
    mode: str,
    x_span: tuple[float, float] = (0.05, 50.0),
    a_target_mult_eq: float | None = None,
    a_eq_ref: float = 9.0e-5 / 0.26,
) -> dict:
    """Integrate FLRW background + perturbations across radiation -> matter equality.

    mode == 'x50_continuity': exact background normalization of flrw_finite_hk_radiation_transfer.py
        (H_* = k / a_*, rho_r_* = 3 H_*^2 - rho_phi_*) for regression verification.
    mode == 'physical_friedmann': exact physical Friedmann density rho_r(a) = 3 H0^2 Om_r0 / a^4,
        rho_m(a) = 3 H0^2 Om_m0 / a^3, with exact Q(a) determined by cosh analytic law or q4 eps_Q.
    """
    a_star_r = math.sqrt(Om_r0) * H0_mpc / k
    x0 = x_span[0]

    def q_at_a_init(a_ref: float) -> float:
        if spec.kind == "gr":
            return 0.0
        if spec.kind == "cosh":
            return eval_cosh_Q_at_a(a_ref, spec.kw["K2"], spec.kw["Q0"], spec.kw["Z0"], H0_mpc, Om_phi_today)
        if spec.kind == "q4":
            rho_r_ref = 3.0 * (H0_mpc**2) * Om_r0 / (a_ref**4)
            rho_phi_ref = eps_Q_q4 * rho_r_ref
            # rho_phi = (3/2) c Q^4 => Q^4 = (2 rho_phi)/(3 c)
            return ((2.0 * rho_phi_ref) / (3.0 * spec.kw["c"])) ** 0.25
        raise ValueError(spec.kind)

    if mode == "x50_continuity":
        H_star = k / a_star_r
        rho_tot_star = 3.0 * (H_star**2)
        if spec.kind == "q4":
            rho_phi_s = (eps_Q_q4 / (1.0 + eps_Q_q4)) * rho_tot_star
            Q_at_star = ((2.0 * rho_phi_s) / (3.0 * spec.kw["c"])) ** 0.25
        else:
            Q_at_star = q_at_a_init(a_star_r)
        U_s, K1_s, _, _ = spec.eval_U(Q_at_star)
        rho_phi_star = 0.5 * (Q_at_star * K1_s - U_s) if spec.kind != "gr" else 0.0
        rho_r_star = rho_tot_star - rho_phi_star
        rho_m_star = 0.0
        a_norm = a_star_r

        def bg_rhs_x(x_val: float, y: list[float]) -> list[float]:
            a_v, Q_v = y
            rr = rho_r_star * ((a_norm / a_v) ** 4)
            rm = rho_m_star * ((a_norm / a_v) ** 3)
            U_v, K1_v, K2e_v, _ = spec.eval_U(Q_v)
            rp = 0.5 * (Q_v * K1_v - U_v) if spec.kind != "gr" else 0.0
            Hp = math.sqrt((rr + rm + rp) / 3.0)
            Hc = a_v * Hp
            return [a_v * Hc / k, (-3.0 * (Hc / k) * (K1_v / K2e_v) if spec.kind != "gr" else 0.0)]

        sol_bg0 = solve_ivp(bg_rhs_x, (1.0, x0), [a_star_r, Q_at_star], method="DOP853", rtol=1e-12, atol=1e-15)
        assert sol_bg0.success
        a0, Q0_init = float(sol_bg0.y[0, -1]), float(sol_bg0.y[1, -1])
    elif mode == "physical_friedmann":
        a_norm = 1.0
        rho_r_star = 3.0 * (H0_mpc**2) * Om_r0
        rho_m_star = 3.0 * (H0_mpc**2) * Om_m0
        # Compute exact conformal time x(a) = k * \int_0^a da/(a^2 H(a)) to find (a0, Q0_init) at exact x0 = 0.05!
        # Start deep in radiation at a_tiny = 1e-8 (where x << 1e-3), integrating forward in ln(a) with state [x, Q]
        a_tiny = 1.0e-8
        Q_tiny = q_at_a_init(a_tiny)
        rr_t = rho_r_star / (a_tiny**4)
        rm_t = rho_m_star / (a_tiny**3)
        U_t, K1_t, _, _ = spec.eval_U(Q_tiny)
        rp_t = 0.5 * (Q_tiny * K1_t - U_t) if spec.kind != "gr" else 0.0
        Hp_t = math.sqrt((rr_t + rm_t + rp_t) / 3.0)
        x_tiny = k / (a_tiny * Hp_t)  # Exact in rad dom: tau = 1/(a H)
        assert x_tiny < x0 * 0.1

        def bg_lna(lna: float, y: list[float]) -> list[float]:
            x_v, Q_v = y
            av = math.exp(lna)
            rr = rho_r_star / (av**4)
            rm = rho_m_star / (av**3)
            U_v, K1_v, K2e_v, _ = spec.eval_U(Q_v)
            rp = 0.5 * (Q_v * K1_v - U_v) if spec.kind != "gr" else 0.0
            Hp = math.sqrt((rr + rm + rp) / 3.0)
            return [k / (av * Hp), (-3.0 * (K1_v / K2e_v) if spec.kind != "gr" else 0.0)]

        def reach_x0(lna: float, y: list[float]) -> float:
            return y[0] - x0

        reach_x0.terminal = True
        reach_x0.direction = 1
        sol_ic = solve_ivp(bg_lna, (math.log(a_tiny), 0.0), [x_tiny, Q_tiny], events=reach_x0, rtol=1e-12, atol=1e-15)
        assert len(sol_ic.t_events[0]) == 1
        a0 = math.exp(float(sol_ic.t_events[0][0]))
        Q0_init = float(sol_ic.y_events[0][0][1])
    else:
        raise ValueError(mode)

    def eval_bg_derivs(a_v: float, Q_v: float):
        rr = rho_r_star * ((a_norm / a_v) ** 4)
        rm = rho_m_star * ((a_norm / a_v) ** 3)
        Uv, K1v, K2ev, K3v = spec.eval_U(Q_v)
        rp = 0.5 * (Q_v * K1v - Uv) if spec.kind != "gr" else 0.0
        Hpv = math.sqrt((rr + rm + rp) / 3.0)
        apv = (a_v**2) * Hpv
        appv = (a_v**3) * (2.0 * rm + (Q_v * K1v - 4.0 * Uv if spec.kind != "gr" else 0.0)) / 12.0
        Qbpv = -3.0 * (apv / a_v) * (K1v / K2ev) if spec.kind != "gr" else 0.0
        K2epv = K3v * Qbpv if spec.kind != "gr" else 0.0
        lamv, dlv = spec.eval_lam(Q_v)
        lampv = dlv * Qbpv if spec.kind != "gr" else 0.0
        return rr, rm, Uv, K1v, K2ev, K3v, rp, apv, appv, Qbpv, K2epv, lamv, lampv

    rr0, rm0, U0_i, K1_i, K2e_i, K3_i, rp0, ap0, app0, Qbp0, K2ep0, lam0_i, lamp0_i = eval_bg_derivs(a0, Q0_init)

    # Super-horizon adiabatic ICs normalized to Phi(0) = 1.0
    Ph0 = 1.0 - (x0**2) / 30.0
    Php0 = k * (-x0 / 15.0)
    if spec.kind == "gr":
        vp0, vpp0, vA0, vAp0 = 0.0, 0.0, 0.0, 0.0
        tr0 = funcs["tr0_ad"](spec.KB, k, a0, ap0, app0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, rr0, rm0, Ph0, Php0, 0.0, 0.0, 0.0, 0.0, vp0, vpp0, vA0, vAp0)
        tm0 = tr0 if Om_m0 > 0.0 else 0.0
        dr0 = funcs["dr0_ad"](spec.KB, k, a0, ap0, app0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, rr0, rm0, Ph0, Php0, 0.0, tr0, 0.0, tm0, vp0, vpp0, vA0, vAp0)
        dm0 = 0.75 * dr0 if Om_m0 > 0.0 else 0.0
    else:
        H_c0 = ap0 / a0
        vp0 = 0.5 * a0 * Q0_init / H_c0 * Ph0
        vpp0 = a0 * (Ph0 * Q0_init + Ph0 * Qbp0 / (2.0 * H_c0))
        vA0 = k * vp0 / (a0 * Q0_init)
        vAp0 = k * (vpp0 / (a0 * Q0_init) - vp0 * (ap0 / (a0 * Q0_init) + Qbp0 / (Q0_init**2)) / a0)
        tr0 = funcs["tr0_ad"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, U0_i, K1_i, K2e_i, K2ep0, lam0_i, lamp0_i, rr0, rm0, Ph0, Php0, 0.0, 0.0, 0.0, 0.0, vp0, vpp0, vA0, vAp0)
        tm0 = tr0 if Om_m0 > 0.0 else 0.0
        dr0 = funcs["dr0_ad"](spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, U0_i, K1_i, K2e_i, K2ep0, lam0_i, lamp0_i, rr0, rm0, Ph0, Php0, 0.0, tr0, 0.0, tm0, vp0, vpp0, vA0, vAp0)
        dm0 = 0.75 * dr0 if Om_m0 > 0.0 else 0.0

    # Verify adiabaticity & exact constraints at x0
    arg0 = (spec.KB, k, a0, ap0, app0, Q0_init, Qbp0, U0_i, K1_i, K2e_i, K2ep0, lam0_i, lamp0_i,
            rr0, rm0, Ph0, Php0, dr0, tr0, dm0, tm0, vp0, vpp0, vA0, vAp0)
    assert abs(funcs["E00"](*arg0)) < 1e-10 and abs(funcs["E0x"](*arg0)) < 1e-10
    if spec.kind != "gr":
        delta_phi_0 = funcs["delta_rho_phi"](*arg0) / rp0
        w_phi0 = 0.5 * U0_i / rp0
        # Adiabatic scalar check: delta_phi / dr == (3/4)*(1 + w_phi) to O((H*x0)^2)
        expected_ratio = 0.75 * (1.0 + w_phi0)
        assert abs((delta_phi_0 / dr0) / expected_ratio - 1.0) < 0.02, (
            f"{spec.name} IC adiabaticity mismatch: ratio={delta_phi_0/dr0:.6f} vs {expected_ratio:.6f}"
        )

    def ode_rhs_aest(x_val: float, y: np.ndarray) -> list[float]:
        av, Qv, Phv, Phpv, drv, trv, dmv, tmv, vpv, vppv, vAv, vApv = y
        rrv, rmv, Uv, K1v, K2ev, _, _, apv, appv, Qbpv, K2epv, lamv, lampv = eval_bg_derivs(av, Qv)
        argv = (spec.KB, k, av, apv, appv, Qv, Qbpv, Uv, K1v, K2ev, K2epv, lamv, lampv,
                rrv, rmv, Phv, Phpv, drv, trv, dmv, tmv, vpv, vppv, vAv, vApv)
        Phppv = funcs["Phpp"](*argv)
        drpv = -(4.0 / 3.0) * trv + 4.0 * Phpv
        trpv = (k**2) * (0.25 * drv + Phv)
        Hcv = apv / av
        dmpv = -tmv + 3.0 * Phpv
        tmpv = -Hcv * tmv + (k**2) * Phv
        vpppv = funcs["vppp"](*argv)
        vAppv = funcs["vApp"](*argv)
        return [
            apv / k, Qbpv / k,
            Phpv / k, Phppv / k,
            drpv / k, trpv / k,
            dmpv / k, tmpv / k,
            vppv / k, vpppv / k,
            vApv / k, vAppv / k,
        ]

    def ode_rhs_gr(x_val: float, y: np.ndarray) -> list[float]:
        av, Phv, Phpv, drv, trv, dmv, tmv = y
        rrv, rmv, Uv, K1v, K2ev, _, _, apv, appv, Qbpv, K2epv, lamv, lampv = eval_bg_derivs(av, 0.0)
        argv = (spec.KB, k, av, apv, appv, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                rrv, rmv, Phv, Phpv, drv, trv, dmv, tmv, 0.0, 0.0, 0.0, 0.0)
        Phppv = funcs["Phpp"](*argv)
        drpv = -(4.0 / 3.0) * trv + 4.0 * Phpv
        trpv = (k**2) * (0.25 * drv + Phv)
        Hcv = apv / av
        dmpv = -tmv + 3.0 * Phpv
        tmpv = -Hcv * tmv + (k**2) * Phv
        return [
            apv / k,
            Phpv / k, Phppv / k,
            drpv / k, trpv / k,
            dmpv / k, tmpv / k,
        ]

    a_stop = a_target_mult_eq * a_eq_ref if a_target_mult_eq is not None else None

    def stop_a_event(x_val: float, y: np.ndarray) -> float:
        return a_stop - y[0] if a_stop is not None else 1.0

    stop_a_event.terminal = True
    stop_a_event.direction = -1

    # Indices differ slightly between 7-var GR ([a, Ph, Php, dr, tr, dm, tm]) and 12-var AeST
    idx_ph, idx_dr = (1, 3) if spec.kind == "gr" else (2, 4)

    def blowup_event(x_val: float, y: np.ndarray) -> float:
        return 1.0e12 - max(abs(y[idx_ph]), abs(y[idx_dr]))

    blowup_event.terminal = True

    x_max = x_span[1]
    if spec.kind == "gr":
        y0 = [a0, Ph0, Php0, dr0, tr0, dm0, tm0]
        ode_fn = ode_rhs_gr
    else:
        y0 = [a0, Q0_init, Ph0, Php0, dr0, tr0, dm0, tm0, vp0, vpp0, vA0, vAp0]
        ode_fn = ode_rhs_aest
    sol = solve_ivp(
        ode_fn, (x0, x_max), y0, method="Radau",
        events=[stop_a_event, blowup_event], dense_output=True,
        rtol=1e-9, atol=1e-12, max_step=0.5 if x_max > 100 else np.inf
    )
    assert sol.success
    if a_stop is not None:
        assert len(sol.t_events[0]) == 1, f"{spec.name} did not reach a_stop={a_stop} by x={x_max} (reached a={sol.y[0,-1]})"

    # Dense grid diagnostics & constraint residuals across full run
    x_grid = np.geomspace(x0, float(sol.t[-1]), 400)
    y_grid = sol.sol(x_grid)

    def diag_at_state(xv: float, state: np.ndarray) -> dict:
        if spec.kind == "gr":
            av, Phv, Phpv, drv, trv, dmv, tmv = [float(z) for z in state]
            Qv, vpv, vppv, vAv, vApv = 0.0, 0.0, 0.0, 0.0, 0.0
        else:
            av, Qv, Phv, Phpv, drv, trv, dmv, tmv, vpv, vppv, vAv, vApv = [float(z) for z in state]
        rrv, rmv, Uv, K1v, K2ev, _, rpv, apv, appv, Qbpv, K2epv, lamv, lampv = eval_bg_derivs(av, Qv)
        argv = (spec.KB, k, av, apv, appv, Qv, Qbpv, Uv, K1v, K2ev, K2epv, lamv, lampv,
                rrv, rmv, Phv, Phpv, drv, trv, dmv, tmv, vpv, vppv, vAv, vApv)
        e00 = funcs["E00"](*argv)
        e0x = funcs["E0x"](*argv)
        scale00 = (
            (av**2) * (rrv * max(1.0, abs(drv)) + rmv * max(1.0, abs(dmv)) + abs(rpv))
            + (k**2) * abs(Phv)
            + (av**2) * abs(K2ev * Qv * (abs(vppv / av) + abs(Qv * Phv)))
            + 1e-30
        )
        scale0x = (
            2.0 * k * ((apv / av) * abs(Phv) + abs(Phpv))
            + (av**2) * (rrv * abs(trv) + rmv * abs(tmv)) / k
            + (av**2) * abs(K1v * k * vpv / (2.0 * av))
            + 1e-30
        )
        drp_phi = funcs["delta_rho_phi"](*argv) if spec.kind != "gr" else 0.0
        dphi = (drp_phi / rpv) if spec.kind != "gr" else None
        Hv = apv / (av**2)
        if spec.kind != "gr":
            Mgap2 = Qv * (2.0 * (2.0 - spec.KB) * (1.0 + lamv) * Qv - K1v) / (2.0 * spec.KB)
            cs2_uv = 4.0 * (2.0 - spec.KB) * (1.0 + 0.5 * spec.KB * lamv) / (K2ev * spec.KB)
            cs2_ir = K1v / (K2ev * Qv)
            w_phi = (0.5 * Uv) / rpv
            mg_h2 = Mgap2 / (Hv**2)
        else:
            cs2_uv = cs2_ir = w_phi = mg_h2 = None
        # Total matter+phi DM contrast:
        delta_dm = (
            dphi if (spec.kind != "gr" and Om_m0 == 0.0)
            else (dmv if Om_m0 > 0.0 else None)
        )
        return {
            "x": xv, "a": av, "a_over_aeq": av / a_eq_ref,
            "Phi": Phv, "delta_r": drv, "delta_m": dmv if Om_m0 > 0 else None,
            "delta_phi": dphi, "delta_dm": delta_dm,
            "rel_E00": abs(e00) / scale00, "rel_E0x": abs(e0x) / scale0x,
            "w_phi": w_phi, "cs2_IR": cs2_ir, "cs2_UV": cs2_uv, "Mgap2_over_H2": mg_h2,
        }

    max_rel_E00 = 0.0
    max_rel_E0x = 0.0
    min_Mgap2_H2 = math.inf
    max_cs2_UV = 0.0
    min_cs2_IR = math.inf
    max_cs2_IR = -math.inf
    for i in range(len(x_grid)):
        dg = diag_at_state(float(x_grid[i]), y_grid[:, i])
        max_rel_E00 = max(max_rel_E00, dg["rel_E00"])
        max_rel_E0x = max(max_rel_E0x, dg["rel_E0x"])
        if dg["Mgap2_over_H2"] is not None:
            min_Mgap2_H2 = min(min_Mgap2_H2, dg["Mgap2_over_H2"])
            max_cs2_UV = max(max_cs2_UV, dg["cs2_UV"])
            min_cs2_IR = min(min_cs2_IR, dg["cs2_IR"])
            max_cs2_IR = max(max_cs2_IR, dg["cs2_IR"])

    # Interpolate exact snapshots at requested a/a_eq and at x=50
    snapshots = {}
    if float(sol.t[-1]) >= 50.0 - 1e-9:
        snapshots["x50"] = diag_at_state(50.0, sol.sol(50.0))
    if a_target_mult_eq is not None:
        a_dense = sol.y[0]
        x_dense = sol.t
        for mult_lbl, mult_val in [("0p1_aeq", 0.1), ("0p5_aeq", 0.5), ("1p0_aeq", 1.0), ("3p0_aeq", 3.0), ("10p0_aeq", 10.0)]:
            target_a = mult_val * a_eq_ref
            if target_a <= a_dense[-1] * (1.0 + 1e-9):
                # Refine x where a(x) == target_a on dense interpolant
                if abs(target_a - a_dense[-1]) < 1e-12 * target_a:
                    xt = float(x_dense[-1])
                else:
                    idx = int(np.searchsorted(a_dense, target_a))
                    xl, xr = float(x_dense[max(0, idx - 1)]), float(x_dense[min(len(x_dense) - 1, idx)])
                    for _ in range(50):
                        xm = 0.5 * (xl + xr)
                        if float(sol.sol(xm)[0]) < target_a:
                            xl = xm
                        else:
                            xr = xm
                    xt = 0.5 * (xl + xr)
                snapshots[mult_lbl] = diag_at_state(xt, sol.sol(xt))

    max_err = None
    if spec.kind == "gr" and Om_m0 == 0.0 and mode == "x50_continuity":
        s = x_grid / math.sqrt(3.0)
        Ph_ex = 3.0 * (np.sin(s) - s * np.cos(s)) / (s**3)
        max_err = float(np.max(np.abs(y_grid[1] - Ph_ex)))

    return {
        "name": spec.name,
        "mode": mode,
        "k_Mpc_inv": k,
        "Om_m0": Om_m0,
        "x_reached": float(sol.t[-1]),
        "a_reached": float(sol.y[0, -1]),
        "max_rel_E00": float(f"{max_rel_E00:.3e}"),
        "max_rel_E0x": float(f"{max_rel_E0x:.3e}"),
        "max_GR_analytic_err": max_err,
        "min_Mgap2_over_H2": None if spec.kind == "gr" else float(f"{min_Mgap2_H2:.6e}"),
        "max_cs2_UV": None if spec.kind == "gr" else float(f"{max_cs2_UV:.6f}"),
        "cs2_IR_range": None if spec.kind == "gr" else [float(f"{min_cs2_IR:.6e}"), float(f"{max_cs2_IR:.6e}")],
        "snapshots": snapshots,
    }


def make_specs(H0_mpc: float, Om_r0: float, Om_phi_today: float, eps_Q: float, a_q4_ref: float) -> dict[str, ModelSpec]:
    Q0_pr = math.sqrt((2.0 - 0.008) / (2.0 * 300.0))
    Z0_pr_1e3 = 1.0e-3 * Q0_pr
    Z0_pr_1e4 = 1.0e-4 * Q0_pr

    # For Q^4, choose c so that c*Q(a_q4_ref)^2 = 150 => cs2_UV(a_q4_ref) = 0.9616 < 1 everywhere for a <= a_q4_ref
    rho_r_ref = 3.0 * (H0_mpc**2) * Om_r0 / (a_q4_ref**4)
    rho_phi_ref = eps_Q * rho_r_ref
    cQ2_ref = 150.0
    Q_ref = math.sqrt(2.0 * rho_phi_ref / (3.0 * cQ2_ref))
    c_q4 = cQ2_ref / (Q_ref**2)

    return {
        "gr_rad": ModelSpec("GR_pure_radiation", "gr", KB=0.0, lam0=0.0),
        "lcdm": ModelSpec("LCDM_matched_Om0p26", "gr", KB=0.0, lam0=0.0),
        "cosh_pr226": ModelSpec("PR226_Cosh_running_lam", "cosh", KB=0.008, lam0=11.2787, K2=300.0, Q0=Q0_pr, Z0=Z0_pr_1e3, run_mode="cosh_even"),
        "cosh_pr226_r1e4": ModelSpec("PR226_Cosh_running_lam_r1e4", "cosh", KB=0.008, lam0=11.2787, K2=300.0, Q0=Q0_pr, Z0=Z0_pr_1e4, run_mode="cosh_even"),
        "cosh_sz21": ModelSpec("SZ21_Cosh_running_lam", "cosh", KB=0.5, lam0=0.0, K2=7.5e5, Q0=0.1, Z0=1.0e-3, run_mode="cosh_lin_onset"),
        "q4_pr226": ModelSpec("Q4_PR226_running_lam", "q4", KB=0.008, lam0=11.2787, c=c_q4, alpha=1.15, run_mode="q4_power"),
    }


def main() -> int:
    funcs = f1_derive_flrw_with_cdm()

    H0_mpc = 67.4 / 299792.458
    Om_r0 = 9.0e-5
    Om_dm0 = 0.26
    a_eq = Om_r0 / Om_dm0  # 3.461538e-4
    eps_Q = 0.039

    # Step 1a: Continuity reproduction check matching flrw_finite_hk_radiation_transfer.py (x in [0.05, 50], k=0.2)
    k_rad = 0.2
    a_star_rad = math.sqrt(Om_r0) * H0_mpc / k_rad
    a_x50_rad = 50.0 * a_star_rad  # exact end scale factor of flrw_finite_hk_radiation_transfer.py Case 5b
    # Scale Q4 for x50_continuity exact reproduction
    rho_tot_s_cont = 3.0 * ((k_rad / a_star_rad) ** 2)
    rho_phi_q4_cont = (eps_Q / (1.0 + eps_Q)) * rho_tot_s_cont
    cQ2_cont = 150.0 * 2500.0
    Q_cont = math.sqrt(2.0 * rho_phi_q4_cont / (3.0 * cQ2_cont))
    q4_cont_spec = ModelSpec("Q4_PR226_running_lam_cont", "q4", KB=0.008, lam0=11.2787, c=cQ2_cont / (Q_cont**2), alpha=1.15, run_mode="q4_power")
    specs_cont = make_specs(H0_mpc, Om_r0, Om_dm0, eps_Q, 10.0 * a_eq)

    cont_gr = integrate_transfer(funcs, specs_cont["gr_rad"], k_rad, H0_mpc, Om_r0, 0.0, 0.0, 0.0, None, "x50_continuity", (0.05, 50.0), None, a_eq)
    cont_cosh = integrate_transfer(funcs, specs_cont["cosh_pr226"], k_rad, H0_mpc, Om_r0, 0.0, Om_dm0, 0.0, None, "x50_continuity", (0.05, 50.0), None, a_eq)
    cont_q4 = integrate_transfer(funcs, q4_cont_spec, k_rad, H0_mpc, Om_r0, 0.0, 0.0, eps_Q, None, "x50_continuity", (0.05, 50.0), None, a_eq)
    assert cont_gr["max_GR_analytic_err"] < 1e-7
    assert abs(cont_cosh["snapshots"]["x50"]["Phi"] / cont_gr["snapshots"]["x50"]["Phi"] - 10.493924) < 1e-4
    assert abs(cont_cosh["snapshots"]["x50"]["delta_r"] / cont_gr["snapshots"]["x50"]["delta_r"] - 0.853832) < 1e-4
    assert abs(cont_q4["snapshots"]["x50"]["Phi"] / cont_gr["snapshots"]["x50"]["Phi"] - 0.897430) < 1e-4

    # Step 1b: Equality runs from x0 = 0.05 through a = 10 * a_eq
    specs = make_specs(H0_mpc, Om_r0, Om_dm0, eps_Q, 10.0 * a_eq)
    equality_runs = {}
    comparisons = {}

    for k in (0.2, 0.1, 0.05):
        k_tag = f"k_{str(k).replace('.', 'p')}"
        # Run GR pure radiation (up to x_max matching a=10*a_eq or beyond)
        r_gr = integrate_transfer(funcs, specs["gr_rad"], k, H0_mpc, Om_r0, 0.0, 0.0, 0.0, None, "physical_friedmann", (0.05, 2000.0), 10.0, a_eq)
        r_lcdm = integrate_transfer(funcs, specs["lcdm"], k, H0_mpc, Om_r0, Om_dm0, 0.0, 0.0, None, "physical_friedmann", (0.05, 2000.0), 10.0, a_eq)
        r_cosh = integrate_transfer(funcs, specs["cosh_pr226"], k, H0_mpc, Om_r0, 0.0, Om_dm0, 0.0, None, "physical_friedmann", (0.05, 2000.0), 10.0, a_eq)
        r_q4_cdm = integrate_transfer(funcs, specs["q4_pr226"], k, H0_mpc, Om_r0, Om_dm0, 0.0, eps_Q, None, "physical_friedmann", (0.05, 2000.0), 10.0, a_eq)

        models_k = {
            "GR_pure_radiation": r_gr,
            "LCDM_matched_Om0p26": r_lcdm,
            "PR226_Cosh_running_lam": r_cosh,
            "Q4_PR226_running_lam_with_CDM": r_q4_cdm,
        }
        if k == 0.2:
            models_k["PR226_Cosh_running_lam_r1e4"] = integrate_transfer(funcs, specs["cosh_pr226_r1e4"], k, H0_mpc, Om_r0, 0.0, Om_dm0, 0.0, None, "physical_friedmann", (0.05, 2000.0), 10.0, a_eq)
            models_k["Q4_PR226_running_lam_pure_rad"] = integrate_transfer(funcs, specs["q4_pr226"], k, H0_mpc, Om_r0, 0.0, 0.0, eps_Q, None, "physical_friedmann", (0.05, 2000.0), 10.0, a_eq)
        if k in (0.2, 0.05):
            models_k["SZ21_Cosh_running_lam"] = integrate_transfer(funcs, specs["cosh_sz21"], k, H0_mpc, Om_r0, 0.0, Om_dm0, 0.0, None, "physical_friedmann", (0.05, 2000.0), 10.0, a_eq)

        for mk, res in models_k.items():
            assert res["max_rel_E00"] < 1e-7, f"{mk} k={k} E00={res['max_rel_E00']}"
            assert res["max_rel_E0x"] < 1e-7, f"{mk} k={k} E0x={res['max_rel_E0x']}"
            if res["min_Mgap2_over_H2"] is not None:
                assert res["min_Mgap2_over_H2"] > 0.0 and res["max_cs2_UV"] < 1.0

        equality_runs[k_tag] = models_k
        comp_k = {}
        for mk, res in models_k.items():
            if mk == "GR_pure_radiation":
                continue
            comp_m = {}
            for sn in ("0p5_aeq", "1p0_aeq", "3p0_aeq", "10p0_aeq"):
                s = res["snapshots"][sn]
                s_gr = r_gr["snapshots"][sn]
                s_lc = r_lcdm["snapshots"][sn]
                entry = {
                    "x": round(s["x"], 4),
                    "Phi": s["Phi"],
                    "Phi_LCDM": s_lc["Phi"],
                    "Phi_over_radGR": round(s["Phi"] / s_gr["Phi"], 6),
                    "Phi_over_LCDM": round(s["Phi"] / s_lc["Phi"], 6),
                    "delta_r_over_LCDM": round(s["delta_r"] / s_lc["delta_r"], 6),
                }
                if s["delta_dm"] is not None:
                    entry["delta_dm"] = s["delta_dm"]
                    entry["delta_dm_LCDM"] = s_lc["delta_dm"]
                    entry["delta_dm_over_LCDM"] = round(s["delta_dm"] / s_lc["delta_dm"], 6)
                if s["cs2_IR"] is not None:
                    entry["cs2_IR"] = s["cs2_IR"]
                    entry["cs2_UV"] = s["cs2_UV"]
                comp_m[sn] = entry
            comp_k[mk] = comp_m
        comparisons[k_tag] = comp_k

    # Evaluate Gate 1 kill/keep rule on PR226_Cosh_running_lam at k = 0.2 Mpc^-1
    c_k02 = comparisons["k_0p2"]["PR226_Cosh_running_lam"]
    q_k02 = comparisons["k_0p2"]["Q4_PR226_running_lam_with_CDM"]
    phi_lc_1 = c_k02["1p0_aeq"]["Phi_over_LCDM"]
    phi_lc_3 = c_k02["3p0_aeq"]["Phi_over_LCDM"]
    phi_gr_1 = c_k02["1p0_aeq"]["Phi_over_radGR"]
    dm_lc_1 = c_k02["1p0_aeq"]["delta_dm_over_LCDM"]
    dm_lc_3 = c_k02["3p0_aeq"]["delta_dm_over_LCDM"]

    cosh_tracks_lcdm = (
        0.70 <= phi_lc_1 <= 1.30
        and 0.70 <= phi_lc_3 <= 1.30
        and 0.70 <= dm_lc_3 <= 1.30
    )

    out = {
        "meta": {
            "H0_Mpc_inv": H0_mpc,
            "Om_r0": Om_r0,
            "Om_dm0": Om_dm0,
            "a_eq": a_eq,
            "eps_Q_q4": eps_Q,
        },
        "symbolic_verification": {
            "linear_AeST_anisotropic_stress_hT": "0 identically (Psi == Phi at O(eps)) [P/D]",
            "bianchi_dE00_dtau_with_cdm": "0 identically [D]",
            "bianchi_dE0x_dtau_with_cdm": "0 identically [D]",
        },
        "x50_continuity_control_k0p2": {
            "GR_max_analytic_err": cont_gr["max_GR_analytic_err"],
            "PR226_Cosh_Phi_over_radGR_x50": round(cont_cosh["snapshots"]["x50"]["Phi"] / cont_gr["snapshots"]["x50"]["Phi"], 6),
            "PR226_Cosh_delta_r_over_radGR_x50": round(cont_cosh["snapshots"]["x50"]["delta_r"] / cont_gr["snapshots"]["x50"]["delta_r"], 6),
            "Q4_PR226_Phi_over_radGR_x50": round(cont_q4["snapshots"]["x50"]["Phi"] / cont_gr["snapshots"]["x50"]["Phi"], 6),
            "Q4_PR226_delta_r_over_radGR_x50": round(cont_q4["snapshots"]["x50"]["delta_r"] / cont_gr["snapshots"]["x50"]["delta_r"], 6),
        },
        "comparisons_against_radGR_and_LCDM": comparisons,
        "equality_runs": equality_runs,
        "gate1_diagnosis": {
            "why_x50_was_10p49": (
                f"At x=50 (a={a_x50_rad:.3e} = 1.54*a_eq), GR_pure_radiation had Omega_m=0 so Phi_rad decayed as x^-2 to "
                f"{cont_gr['snapshots']['x50']['Phi']:.6f}, while Cosh (Omega_phi=0.26) had already entered equality. "
                "When compared apples-to-apples against matched LCDM (Omega_m=0.26), the potential and DM contrast ratios tell the true dynamical story."
            ),
            "PR226_Cosh_k0p2_at_aeq": c_k02["1p0_aeq"],
            "PR226_Cosh_k0p2_at_3aeq": c_k02["3p0_aeq"],
            "PR226_Cosh_k0p2_at_10aeq": c_k02["10p0_aeq"],
            "Q4_with_CDM_k0p2_at_aeq": q_k02["1p0_aeq"],
            "Q4_with_CDM_k0p2_at_3aeq": q_k02["3p0_aeq"],
            "Q4_with_CDM_k0p2_at_10aeq": q_k02["10p0_aeq"],
            "cosh_passes_within_30pct_of_LCDM": bool(cosh_tracks_lcdm),
            "verdict": "REPLAN_NEEDED_COSH_TRACKS_LCDM" if cosh_tracks_lcdm else "COSH_KILLED_[X]",
        },
    }

    jpath = os.path.join(HERE, "GATE1_EQUALITY_COSH_VS_Q4.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")

    print(json.dumps({
        "symbolic_verification": out["symbolic_verification"],
        "x50_continuity_control_k0p2": out["x50_continuity_control_k0p2"],
        "comparisons": out["comparisons_against_radGR_and_LCDM"],
        "gate1_diagnosis": out["gate1_diagnosis"],
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
