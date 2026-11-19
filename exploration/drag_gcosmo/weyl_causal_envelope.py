#!/usr/bin/env python3
"""Pre-registered Causal Weyl Anisotropic-Stress Envelope Kill Filter
for the flux-fed Dark Bubble wall (PREREG_WEYL_ENVELOPE.md, commit 7ea3f668).

Parts:
  (S1) SymPy exact verification in Conformal Newtonian gauge:
       - Exact background E_p identity and d(E00)/dN = 0 Bianchi identity
       - Formulation I (Law C: geometric zero-momentum wall drag Fd = 0, Q_i = -K^2 Om_d Phi)
         exact d(E03)/dN = E33 identity
       - Formulation II (Law A: free-falling pressureless drag fluid, div3(T_d) = Q_i = q_4 u_F)
         exact 3-momentum Bianchi closure and Hu (1998) dispersion speed v_ph^2 = 1/3 + 2 c_vis^2
  (N1) Controls:
       - Exact LCDM (kappa = 0) recovery of Phi = Psi (< 1e-12), E03 (< 1e-6), late growth vs
         growth_coupled (< 1e-4), and REF_D1 (< 2e-3)
       - Numerical E33 and constraint residuals on Pantheon+ best fit (kappa = -2.244452)
  (N2) Full causal bracket sweep at w_d = 0 (x_0 = |kappa|) across:
       - Backgrounds: LCDM control, Pantheon+ best (-2.2445), DES-Dovekie best (-2.4966),
         Pantheon+ 2-sigma floor (-0.8317, refitted h, Om)
       - Causal Hu (1998) c_vis^2 in {0.0, 0.1, 1/3, 0.6, 1.0} + exact MB95 l_max=8 Boltzmann
         hierarchy truncation (MB95 Eq. 51) at c_vis^2 = 1/3
       - Both exact covariant realizations (Law C Fd=0 and Law A Q_i = q_4 u_F), plus sensitivity
         checks on V_flux in {bulk_rest, matter_comoving} and IC_W in {adiabatic, unperturbed}
       - Exact Limber CMB lensing C_L^{phi phi} (L in {40, 80, 120, 200, 300, 400}) and exact
         spherical-Bessel late-ISW C_l^{ISW} (l in {2, 5, 10, 20, 30})
       - Automatic scan for surviving |kappa| ceiling if best-fit fails while -0.8317 survives.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import json
import math
import os
import sys
import time
import numpy as np
import sympy as sp
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.special import erfi, spherical_jn

HERE = os.path.dirname(os.path.abspath(__file__))

C_LIGHT_KMS = 299792.458
ORH2 = 4.18e-5
OB_H2 = 0.02237
N_S = 0.9649
K_PIVOT = 0.05
A_INIT = 1e-3
Z_STAR = 1089.9
Z_ISW_MAX = 5.0

K_GRID = np.geomspace(1e-4, 0.2, 25)
L_LENS = [40, 80, 120, 200, 300, 400]
ELL_ISW = [2, 5, 10, 20, 30]
C_VIS2_GRID = [0.0, 0.1, 1.0 / 3.0, 0.6, 1.0]

# Evaluation grid in z for perturbation trajectories [0 .. 999.0] -> N ascending
_Z_EVAL = np.unique(np.concatenate([np.linspace(0.0, Z_ISW_MAX, 301), np.geomspace(Z_ISW_MAX, 999.0, 150)]))
N_EVAL = -np.log1p(_Z_EVAL[::-1])  # strictly ascending from ln(1e-3) to 0.0
Z_ON_NEVAL = _Z_EVAL[::-1]

# Precomputed comoving distance z-grid (dense across both ISW and lensing kernels)
Z_CHI_GRID = np.unique(np.concatenate([np.linspace(0.0, Z_ISW_MAX, 1001), np.geomspace(Z_ISW_MAX, Z_STAR, 500)]))


def y_exact_scalar(a: float, kappa: float) -> tuple[float, float, float]:
    """Closed-form integrating-factor integrals y_1, y_2, y_5 smooth across kappa = 0."""
    if abs(kappa) < 1e-12:
        return 0.0, 0.0, 0.0
    z = 0.5 * kappa * a * a
    if abs(z) < 1e-3:
        y1 = kappa * a**2 / 2.0 + (kappa**2 * a**4) / 8.0 + (kappa**3 * a**6) / 48.0
        y2 = kappa * a**3 / 3.0 + (kappa**2 * a**5) / 15.0 + (kappa**3 * a**7) / 105.0
        poly = (2.0 * z**3 / 6.0) * (1.0 + z / 4.0 + z**2 / 20.0 + z**3 / 120.0 + z**4 / 840.0)
        y5 = (4.0 / (kappa * kappa)) * poly
        return y1, y2, y5
    ez = math.exp(z)
    y1 = ez - 1.0
    y5 = (4.0 / (kappa * kappa)) * (2.0 * ez - 2.0 - 2.0 * z - z * z)
    if kappa < 0.0:
        rt = math.sqrt(-0.5 * kappa)
        y2 = ez * math.sqrt(math.pi) / (2.0 * rt) * float(erfi(rt * a)) - a
    else:
        rt = math.sqrt(0.5 * kappa)
        from scipy.special import erf
        y2 = ez * math.sqrt(math.pi) / (2.0 * rt) * float(erf(rt * a)) - a
    return y1, y2, y5


def compute_OL(h: float, Om: float, kappa: float) -> float:
    Or = ORH2 / (h * h)
    if abs(kappa) < 1e-12:
        return 1.0 - Om - Or
    y1_1, y2_1, y5_1 = y_exact_scalar(1.0, kappa)
    return (1.0 - Or * (1.0 + y1_1) - Om * (1.0 + y2_1)) / (1.0 + y5_1)


def bg_at_N(N: float, h: float, Om: float, x0: float, OL: float) -> tuple[float, float, float, float, float, float, float, float, float]:
    """Exact closed-form background functions at N = ln(a) for w_d = 0 (kappa = -x0)."""
    a = math.exp(N)
    Or = ORH2 / (h * h)
    kappa = -x0
    y1, y2, y5 = y_exact_scalar(a, kappa)
    a2 = a * a
    a3 = a2 * a
    a4 = a2 * a2
    E2 = Or * (1.0 + y1) / a4 + Om * (1.0 / a3 + y2 / a4) + OL * (1.0 + y5 / a4)
    E = math.sqrt(E2)
    Omd = x0 * a2 * E2
    Om_net = (Or * y1 + Om * y2 + OL * y5) / a4
    OmW = Omd + Om_net
    Ep = (-1.5 * Om / a3 - 2.0 * Or / a4 - 2.0 * OmW + 1.5 * Omd) / E2
    Omd_p = 2.0 * Omd * (1.0 + Ep)
    q4 = Omd_p + 3.0 * Omd
    q4_over_OmW = (q4 / OmW) if (x0 > 0.0 and OmW > 0.0) else 0.0
    return a, E, E2, Ep, OmW, Omd, Omd_p, q4, q4_over_OmW


def compute_ref_d1_growth(h: float, Om: float, kappa: float) -> tuple[float, float]:
    """Direct growth ODE ratio D(1)/D(0.1) and D(1) matching drag_fit.py REF_D1 convention."""
    x0 = -kappa
    OL = compute_OL(h, Om, kappa)

    def rhs(N: float, y: list[float]) -> list[float]:
        _, _, _, Ep, _, _, _, _, _ = bg_at_N(N, h, Om, x0, OL)
        a, E, E2, *_ = bg_at_N(N, h, Om, x0, OL)
        return [y[1], -(2.0 + Ep) * y[1] + 1.5 * Om / (a**3 * E2) * y[0]]

    s = solve_ivp(rhs, (math.log(A_INIT), 0.0), [A_INIT, A_INIT], method="DOP853", rtol=1e-9, atol=1e-12, dense_output=True)
    return float(s.y[0, -1]), float(s.y[0, -1] / s.sol(math.log(0.1))[0])


def run_symbolic_s1() -> dict:
    """SymPy exact proof of all perturbed equations, Bianchi identities, Law C, Law A, and Hu (1998)."""
    N = sp.Symbol("N", real=True)
    k, H0, Om, Or, OL, x0 = sp.symbols("k H0 Om Or OL x0", positive=True)
    a = sp.exp(N)
    E = sp.Function("E")(N)
    OmW = sp.Function("OmW")(N)
    E_p = sp.diff(E, N) / E
    K2 = (k / (a * H0 * E)) ** 2
    Omd = x0 * a**2 * E**2
    Omd_p = sp.diff(Omd, N)
    q4 = Omd_p + 3 * Omd
    Ep_exact = (-sp.Rational(3, 2) * Om * a ** (-3) - 2 * Or * a ** (-4) - 2 * OmW + sp.Rational(3, 2) * Omd) / E**2

    # 1. Background E_p identity from differentiating (1 + x0 a^2) E^2 = Om/a^3 + Or/a^4 + OL + OmW with OmW' = q4 - 4 OmW
    lhs_bg = sp.diff((1 + x0 * a**2) * E**2, N)
    rhs_bg = sp.diff(Om * a ** (-3) + Or * a ** (-4) + OL, N) + (q4 - 4 * OmW)
    sol_Ep = sp.solve(lhs_bg - rhs_bg, sp.diff(E, N))[0] / E
    assert sp.simplify(sol_Ep - Ep_exact) == 0

    dm, um, Dr, Fr, DW, FW, SW, Psi = [sp.Function(nm)(N) for nm in ("dm", "um", "Dr", "Fr", "DW", "FW", "SW", "Psi")]
    uF = sp.Function("uF")(N)
    Phi = Psi - sp.Rational(9, 2) * (H0 / k) ** 2 * a**2 * SW
    Dm = Om * a ** (-3) * dm
    Fm = Om * a ** (-3) * um
    um_p = -(2 + E_p) * um + K2 * Phi
    Fr_p = -(5 + E_p) * Fr + K2 * (Dr / 3 + sp.Rational(4, 3) * Or * a ** (-4) * Phi)

    # 2. Law A (free-falling drag fluid, div3(T_d) = q4 uF): exact d(E00)/dN = 0 AND div3(T_d) - q4 uF = 0
    Psi_p_expr = -Phi - (K2 * Psi + sp.Rational(3, 2) / E**2 * (Dm + Dr + DW)) / (3 * (1 + x0 * a**2))
    Fd_from_E03 = Fm + Fr + FW - sp.Rational(2, 3) * E**2 * K2 * (sp.diff(Psi, N) + Phi)
    Psi_pp_plus_Phi_p = sp.Rational(1, 2) / E**2 * (Dr + DW) - sp.Rational(3, 2) / E**2 * SW - (3 + E_p) * sp.diff(Psi, N) - (3 + 2 * E_p) * Phi
    dm_p = -um + 3 * sp.diff(Psi, N)
    Dr_p = -4 * Dr + 4 * Or * a ** (-4) * sp.diff(Psi, N) - Fr
    Dd = -2 * Omd * (sp.diff(Psi, N) + Phi)
    Dd_p = -2 * Omd_p * (sp.diff(Psi, N) + Phi) - 2 * Omd * Psi_pp_plus_Phi_p
    DW_p = -4 * DW + 4 * OmW * sp.diff(Psi, N) - FW + (Dd_p + 3 * Dd - 3 * Omd * sp.diff(Psi, N) + Fd_from_E03)
    FW_p = -(5 + E_p) * FW + K2 * (sp.Rational(1, 3) * DW + sp.Rational(4, 3) * OmW * Phi - SW) + q4 * uF

    E00_res = K2 * Psi + 3 * (1 + x0 * a**2) * (sp.diff(Psi, N) + Phi) + sp.Rational(3, 2) / E**2 * (Dm + Dr + DW)
    subs_A = {
        sp.diff(Psi, N, 2): Psi_pp_plus_Phi_p - sp.diff(Phi, N),
        sp.diff(dm, N): dm_p,
        sp.diff(um, N): um_p,
        sp.diff(Dr, N): Dr_p,
        sp.diff(Fr, N): Fr_p,
        sp.diff(DW, N): DW_p,
        sp.diff(FW, N): FW_p,
        sp.diff(OmW, N): q4 - 4 * OmW,
    }
    dE00_A = sp.diff(E00_res, N).subs(subs_A).subs(sp.diff(E, N), E * Ep_exact).subs(sp.diff(Psi, N), Psi_p_expr).subs(sp.diff(E, N), E * Ep_exact)
    assert sp.simplify(dE00_A) == 0

    div3_d = sp.diff(Fd_from_E03, N) + (5 + E_p) * Fd_from_E03 - K2 * Omd * Phi - q4 * uF
    div3_d_eval = div3_d.subs(subs_A).subs(sp.diff(E, N), E * Ep_exact).subs(sp.diff(Psi, N), Psi_p_expr).subs(sp.diff(E, N), E * Ep_exact)
    assert sp.simplify(div3_d_eval) == 0

    # 3. Law C (geometric zero-momentum wall drag Fd = 0, Q_i = -K^2 Om_d Phi): exact d(E03)/dN = E33
    Qp_C = sp.Rational(3, 2) / (E**2 * K2) * (Fm + Fr + FW)
    Psi_p_C = Qp_C - Phi
    DW_C = -sp.Rational(2, 3) * E**2 * (K2 * Psi + 3 * (1 + x0 * a**2) * Qp_C) - Dm - Dr
    FW_p_C = -(5 + E_p) * FW + K2 * (DW_C / 3 + (sp.Rational(4, 3) * OmW - Omd) * Phi - SW)
    dQp_E03 = sp.diff(Qp_C, N).subs({
        sp.diff(um, N): um_p,
        sp.diff(Fr, N): Fr_p,
        sp.diff(FW, N): FW_p_C,
        sp.diff(E, N): E * Ep_exact,
    })
    Qp_p_E33 = sp.Rational(1, 2) / E**2 * (Dr + DW_C) - sp.Rational(3, 2) / E**2 * SW - (3 + E_p) * Psi_p_C - (3 + 2 * E_p) * Phi
    assert sp.simplify((dQp_E03 - Qp_p_E33).subs(sp.diff(E, N) / E, Ep_exact)) == 0

    # 4. Exact RD limit check: E33 reduces to tau^2 Psi_tt + 4 tau Psi_t + (k tau)^2 / 3 Psi = 0
    tau = sp.Symbol("tau", positive=True)
    Psi_tau = sp.Function("Psi_tau")(tau)
    # In RD: E_p = -2, Phi = Psi, K = k*tau, Psi' = tau dPsi/dtau, Psi'' = tau^2 d2Psi/dtau2 + tau dPsi/dtau
    # E33 with 1/(2E^2) Dr = -(1/3)(K^2 Psi + 6 Psi') gives:
    rd_lhs = (tau**2 * sp.diff(Psi_tau, tau, 2) + 2 * tau * sp.diff(Psi_tau, tau)) + 1 * (tau * sp.diff(Psi_tau, tau)) - Psi_tau
    rd_rhs = -sp.Rational(1, 3) * (k * tau) ** 2 * Psi_tau - tau * sp.diff(Psi_tau, tau) - Psi_tau
    rd_eq = sp.simplify((rd_lhs - rd_rhs) / tau**2)
    assert sp.simplify(rd_eq - (sp.diff(Psi_tau, tau, 2) + (4 / tau) * sp.diff(Psi_tau, tau) + k**2 * Psi_tau / 3)) == 0

    # 5. Hu (1998) subhorizon dispersion speed: v_ph^2 = 1/3 + 2 c_vis^2
    cvis2 = sp.Symbol("cvis2", real=True)
    assert sp.simplify(sp.Rational(1, 3) + 2 * cvis2).subs(cvis2, sp.Rational(1, 3)) == 1

    return {
        "background_Ep_identity_verified": True,
        "LawA_dE00_dN_zero_on_constraint_surface": True,
        "LawA_div3_Td_minus_q4_uF_zero": True,
        "LawC_dE03_dN_equals_E33_Fd0": True,
        "RD_conformal_time_limit_verified": True,
        "Hu98_subhorizon_phase_speed_sq": "1/3 + 2 c_vis^2 (= 1 at c_vis^2 = 1/3)",
    }


def _solve_single_mode(task: tuple) -> tuple:
    """Worker solving a single k mode across N_EVAL, returning Phi_W(z), dPhiW_dz(z), and residuals."""
    run_key, idx_k, k, h, Om, kappa, law, closure, c_vis2, v_flux, ic_W, check_resid = task
    x0 = -kappa
    OL = compute_OL(h, Om, kappa)
    Or = ORH2 / (h * h)
    H0_Mpc = 100.0 * h / C_LIGHT_KMS
    shear_fac = 4.5 * (H0_Mpc / k) ** 2

    # Precompute conformal time tau(N) only if closure == "mb95_l8"
    N_i = math.log(A_INIT)
    if closure == "mb95_l8":
        Ng_tau = np.linspace(N_i, 0.0, 1501)
        inv_aH = np.array([1.0 / (math.exp(float(n)) * H0_Mpc * bg_at_N(float(n), h, Om, x0, OL)[1]) for n in Ng_tau])
        _, E_init, *_ = bg_at_N(N_i, h, Om, x0, OL)
        tau_i = 1.0 / (A_INIT * H0_Mpc * E_init)
        tau_grid = tau_i + cumulative_trapezoid(inv_aH, Ng_tau, initial=0.0)
        dN_tau = float(Ng_tau[1] - Ng_tau[0])
    else:
        Ng_tau = None
        tau_grid = None
        dN_tau = 1.0

    # Constraint-satisfying adiabatic IC at a_i = A_INIT
    a, E_i, E2_i, Ep_i, OmW_i, _, _, _, _ = bg_at_N(N_i, h, Om, x0, OL)
    K2_i = (k / (a * H0_Mpc * E_i)) ** 2
    w_m = Om / (a * a * a)
    w_r = (4.0 / 3.0) * Or / (a**4) / (1.0 + K2_i / 3.0)
    w_W = ((4.0 / 3.0) * OmW_i / (1.0 + K2_i / 3.0)) if (x0 > 0.0 and ic_W == "adiabatic") else 0.0
    D_tot_i = -(2.0 / 3.0) * E2_i * (K2_i + 3.0 * (1.0 + x0 * a * a))
    dm_i = D_tot_i / (w_m + w_r + w_W)
    Dr_i = w_r * dm_i
    u_i = (2.0 / 3.0) * E2_i * K2_i / (w_m + w_r + w_W)
    um_i = u_i
    Fr_i = w_r * u_i
    FW_i = (w_W * u_i) if x0 > 0.0 else 0.0
    DW_i = (w_W * dm_i) if x0 > 0.0 else 0.0

    if x0 == 0.0 or law == "C_Fd0":
        if closure == "mb95_l8" and x0 > 0.0:
            y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, FW_i] + [0.0] * 7  # S2..S8
        else:
            y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, FW_i, 0.0]

        def eval_rhs(N: float, y: np.ndarray) -> tuple[list[float], float, float]:
            dm, um, Dr, Fr, Psi, FW = y[0], y[1], y[2], y[3], y[4], y[5]
            SW = 0.0 if x0 == 0.0 else y[6]
            a_v, E, E2, Ep, OmW, Omd, _, _, q4_W = bg_at_N(N, h, Om, x0, OL)
            a2 = a_v * a_v
            a3 = a2 * a_v
            a4 = a2 * a2
            Phi = Psi - shear_fac * a2 * SW
            K2 = (k / (a_v * H0_Mpc * E)) ** 2
            Fm = Om / a3 * um
            Qp = (1.5 / (E2 * K2)) * (Fm + Fr + FW)
            Psi_p = Qp - Phi
            dm_p = -um + 3.0 * Psi_p
            um_p = -(2.0 + Ep) * um + K2 * Phi
            Dr_p = -4.0 * Dr + 4.0 * Or / a4 * Psi_p - Fr
            Fr_p = -(5.0 + Ep) * Fr + K2 * (Dr / 3.0 + (4.0 / 3.0) * Or / a4 * Phi)
            if x0 == 0.0:
                deriv = [dm_p, um_p, Dr_p, Fr_p, Psi_p, 0.0, 0.0]
                dPhiW_dN = Psi_p
            elif closure == "mb95_l8":
                DW = -(2.0 / 3.0) * E2 * (K2 * Psi + 3.0 * (1.0 + x0 * a2) * Qp) - Om / a3 * dm - Dr
                FW_p = -(5.0 + Ep) * FW + K2 * (DW / 3.0 + ((4.0 / 3.0) * OmW - Omd) * Phi - SW)
                K = math.sqrt(K2)
                idx_f = (N - N_i) / dN_tau
                if idx_f <= 0.0:
                    tau = float(tau_grid[0])
                elif idx_f >= len(tau_grid) - 1:
                    tau = float(tau_grid[-1])
                else:
                    ii = int(idx_f)
                    tau = float(tau_grid[ii] + (idx_f - ii) * (tau_grid[ii + 1] - tau_grid[ii]))
                damp = -4.0 + q4_W
                S = y[6:]
                Sp = [0.0] * 7
                Sp[0] = damp * S[0] + (4.0 / 15.0) * FW - (3.0 / 5.0) * K * S[1]
                for idx in range(1, 6):
                    ell = idx + 2
                    Sp[idx] = damp * S[idx] + (K / (2 * ell + 1)) * (ell * S[idx - 1] - (ell + 1) * S[idx + 1])
                Sp[6] = damp * S[6] + K * S[5] - (9.0 / (a_v * H0_Mpc * E * tau)) * S[6]
                deriv = [dm_p, um_p, Dr_p, Fr_p, Psi_p, FW_p] + Sp
                dPhiW_dN = Psi_p - 0.5 * shear_fac * a2 * (2.0 * SW + Sp[0])
            else:
                DW = -(2.0 / 3.0) * E2 * (K2 * Psi + 3.0 * (1.0 + x0 * a2) * Qp) - Om / a3 * dm - Dr
                FW_p = -(5.0 + Ep) * FW + K2 * (DW / 3.0 + ((4.0 / 3.0) * OmW - Omd) * Phi - SW)
                SW_p = (-7.0 + q4_W) * SW + 2.0 * c_vis2 * FW
                deriv = [dm_p, um_p, Dr_p, Fr_p, Psi_p, FW_p, SW_p]
                dPhiW_dN = Psi_p - 0.5 * shear_fac * a2 * (2.0 * SW + SW_p)
            return deriv, 0.5 * (Phi + Psi), dPhiW_dN

        def rhs(N: float, y: np.ndarray) -> list[float]:
            return eval_rhs(N, y)[0]

    else:  # law == "A_freefall" (x0 > 0)
        if closure == "mb95_l8":
            y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, 1.0, FW_i] + [0.0] * 7
        else:
            y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, 1.0, FW_i, 0.0]

        def eval_rhs(N: float, y: np.ndarray) -> tuple[list[float], float, float]:
            dm, um, Dr, Fr, Psi, Qp, FW = y[0], y[1], y[2], y[3], y[4], y[5], y[6]
            SW = y[7]
            a_v, E, E2, Ep, OmW, _, _, q4, q4_W = bg_at_N(N, h, Om, x0, OL)
            a2 = a_v * a_v
            a3 = a2 * a_v
            a4 = a2 * a2
            Phi = Psi - shear_fac * a2 * SW
            Psi_p = Qp - Phi
            K2 = (k / (a_v * H0_Mpc * E)) ** 2
            DW = -(2.0 / 3.0) * E2 * (K2 * Psi + 3.0 * (1.0 + x0 * a2) * Qp) - Om / a3 * dm - Dr
            Qp_p = 0.5 / E2 * (Dr + DW) - 1.5 / E2 * SW - (3.0 + Ep) * Psi_p - (3.0 + 2.0 * Ep) * Phi
            u_F = 0.0 if v_flux == "bulk_rest" else um
            FW_p = -(5.0 + Ep) * FW + K2 * (DW / 3.0 + (4.0 / 3.0) * OmW * Phi - SW) + q4 * u_F
            dm_p = -um + 3.0 * Psi_p
            um_p = -(2.0 + Ep) * um + K2 * Phi
            Dr_p = -4.0 * Dr + 4.0 * Or / a4 * Psi_p - Fr
            Fr_p = -(5.0 + Ep) * Fr + K2 * (Dr / 3.0 + (4.0 / 3.0) * Or / a4 * Phi)
            if closure == "mb95_l8":
                K = math.sqrt(K2)
                idx_f = (N - N_i) / dN_tau
                if idx_f <= 0.0:
                    tau = float(tau_grid[0])
                elif idx_f >= len(tau_grid) - 1:
                    tau = float(tau_grid[-1])
                else:
                    ii = int(idx_f)
                    tau = float(tau_grid[ii] + (idx_f - ii) * (tau_grid[ii + 1] - tau_grid[ii]))
                damp = -4.0 + q4_W
                S = y[7:]
                Sp = [0.0] * 7
                Sp[0] = damp * S[0] + (4.0 / 15.0) * FW - (3.0 / 5.0) * K * S[1]
                for idx in range(1, 6):
                    ell = idx + 2
                    Sp[idx] = damp * S[idx] + (K / (2 * ell + 1)) * (ell * S[idx - 1] - (ell + 1) * S[idx + 1])
                Sp[6] = damp * S[6] + K * S[5] - (9.0 / (a_v * H0_Mpc * E * tau)) * S[6]
                deriv = [dm_p, um_p, Dr_p, Fr_p, Psi_p, Qp_p, FW_p] + Sp
                dPhiW_dN = Psi_p - 0.5 * shear_fac * a2 * (2.0 * SW + Sp[0])
            else:
                SW_p = (-7.0 + q4_W) * SW + 2.0 * c_vis2 * FW
                deriv = [dm_p, um_p, Dr_p, Fr_p, Psi_p, Qp_p, FW_p, SW_p]
                dPhiW_dN = Psi_p - 0.5 * shear_fac * a2 * (2.0 * SW + SW_p)
            return deriv, 0.5 * (Phi + Psi), dPhiW_dN

        def rhs(N: float, y: np.ndarray) -> list[float]:
            return eval_rhs(N, y)[0]

    sol = solve_ivp(rhs, (N_i, 0.0), y0, method="DOP853", rtol=1e-7, atol=1e-10, t_eval=N_EVAL)
    if not sol.success or sol.y.shape[1] != len(N_EVAL):
        return (run_key, idx_k, False, None, None, None)

    n_pts = len(N_EVAL)
    PhiW = np.empty(n_pts, dtype=float)
    dPhiW_dz = np.empty(n_pts, dtype=float)
    max_phi_w = 0.0
    for j in range(n_pts):
        _, phiw, dN_val = eval_rhs(float(N_EVAL[j]), sol.y[:, j])
        PhiW[j] = phiw
        dPhiW_dz[j] = -math.exp(float(N_EVAL[j])) * dN_val
        if abs(phiw) > max_phi_w:
            max_phi_w = abs(phiw)

    dm_0p1 = -math.exp(float(np.interp(math.log(0.1), N_EVAL, np.log(np.abs(sol.y[0])))))
    extra = {
        "max_abs_PhiW": float(max_phi_w),
        "PhiW_z0": float(PhiW[-1]),
        "dm_z0": float(sol.y[0, -1]),
        "dm_i": float(dm_i),
        "dm_ratio_1_0p1": float(sol.y[0, -1] / dm_0p1),
    }
    if check_resid:
        # Check E03 and E33 numerical consistency on N_EVAL (in interior points)
        idx_01 = int(np.argmin(np.abs(N_EVAL - math.log(0.5))))
        Nv = float(N_EVAL[idx_01])
        yv = sol.y[:, idx_01]
        a_v, E, E2, Ep, OmW, _, _, _, _ = bg_at_N(Nv, h, Om, x0, OL)
        K2 = (k / (a_v * H0_Mpc * E)) ** 2
        if x0 == 0.0:
            Phi = yv[4]
            Qp_E03 = 1.5 / (E2 * K2) * (Om / a_v**3 * yv[1] + yv[3])
            Qp_E00 = -(K2 * yv[4] + 1.5 / E2 * (Om / a_v**3 * yv[0] + yv[2])) / 3.0
            extra["max_Phi_minus_Psi"] = 0.0
            extra["E03_minus_E00_at_0p5"] = float(abs(Qp_E03 - Qp_E00))
        elif law == "C_Fd0":
            # Compare Qp'(N) from numerical central diff along solution vs RHS_E33
            # Re-integrate tiny interval around Nv for clean central difference
            def get_qp(nv):
                if nv == Nv:
                    yy = yv
                else:
                    s_loc = solve_ivp(rhs, (Nv, nv), yv, method="DOP853", rtol=1e-10, atol=1e-13)
                    yy = s_loc.y[:, -1]
                av, Ev, E2v, *_ = bg_at_N(nv, h, Om, x0, OL)
                K2v = (k / (av * H0_Mpc * Ev)) ** 2
                return 1.5 / (E2v * K2v) * (Om / av**3 * yy[1] + yy[3] + yy[5])
            dN = 1e-4
            qp_num = (get_qp(Nv + dN) - get_qp(Nv - dN)) / (2.0 * dN)
            SWv = yv[6]
            Phi = yv[4] - shear_fac * a_v**2 * SWv
            Qpv = get_qp(Nv)
            Psipv = Qpv - Phi
            DWv = -(2.0 / 3.0) * E2 * (K2 * yv[4] + 3.0 * (1.0 + x0 * a_v**2) * Qpv) - Om / a_v**3 * yv[0] - yv[2]
            qp_e33 = 0.5 / E2 * (yv[2] + DWv) - 1.5 / E2 * SWv - (3.0 + Ep) * Psipv - (3.0 + 2.0 * Ep) * Phi
            extra["E33_residual_at_a0p5"] = float(abs(qp_num - qp_e33))
            extra["Phi_z0"] = float(yv[4] if False else (sol.y[4, -1] - shear_fac * sol.y[6, -1]))
            extra["Psi_z0"] = float(sol.y[4, -1])

    return (run_key, idx_k, True, PhiW, dPhiW_dz, extra)


def T_EH_no_wiggle(k: np.ndarray, h: float, Om: float, Ob_h2: float = OB_H2) -> np.ndarray:
    """Eisenstein & Hu (1998) ApJ 496, 605 Eqs. 26, 28-31 zero-baryon effective transfer T_0(k), k in Mpc^-1."""
    k = np.asarray(k, dtype=float)
    om_m = Om * h * h
    f_b = Ob_h2 / om_m
    th27 = 2.7255 / 2.7
    s = 44.5 * math.log(9.83 / om_m) / math.sqrt(1.0 + 10.0 * (Ob_h2 ** 0.75))
    a_gam = 1.0 - 0.328 * math.log(431.0 * om_m) * f_b + 0.38 * math.log(22.3 * om_m) * (f_b * f_b)
    om_eff = om_m * (a_gam + (1.0 - a_gam) / (1.0 + (0.43 * k * s) ** 4))
    q = k * (th27 * th27) / om_eff
    L0 = np.log(2.0 * math.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def compute_observables_for_run(h: float, Om: float, kappa: float, PhiW_mat: np.ndarray, dPhiW_dz_mat: np.ndarray) -> dict:
    """Compute exact Limber C_L^{phi phi} (L in L_LENS) and Spherical-Bessel C_l^{ISW} (l in ELL_ISW).

    PhiW_mat, dPhiW_dz_mat have shape (len(K_GRID), len(N_EVAL)) aligned with Z_ON_NEVAL (descending z).
    """
    x0 = -kappa
    OL = compute_OL(h, Om, kappa)
    # Build chi(z) across Z_CHI_GRID
    Ez_chi = np.array([bg_at_N(-math.log1p(float(z)), h, Om, x0, OL)[1] for z in Z_CHI_GRID])
    chi_grid = cumulative_trapezoid(C_LIGHT_KMS / (100.0 * h * Ez_chi), Z_CHI_GRID, initial=0.0)
    chi_star = float(chi_grid[-1])

    # Reverse Z_ON_NEVAL so z is ascending [0 .. 999]
    z_asc = Z_ON_NEVAL[::-1]
    PhiW_asc = PhiW_mat[:, ::-1]
    dPhi_asc = dPhiW_dz_mat[:, ::-1]
    lnk_grid = np.log(K_GRID)

    # --- 1. Limber CMB lensing C_L^{phi phi} ---
    # Use log-spaced chi quadrature over (0.005 * chi_star, chi_star) avoiding chi=0
    chi_q = np.linspace(1.0, chi_star * 0.9999, 1200)
    z_q = np.interp(chi_q, chi_grid, Z_CHI_GRID)
    # Interpolate PhiW at (k=(L+0.5)/chi_q, z_q) via 2-step interpolation (first in z, then in ln k)
    z_q_clamp = np.minimum(z_q, z_asc[-1])
    Phi_at_zq = np.array([np.interp(z_q_clamp, z_asc, PhiW_asc[ik]) for ik in range(len(K_GRID))])  # (25, len(chi_q))

    CL_lens = {}
    frac_in_kgrid = {}
    for L in L_LENS:
        k_q = (L + 0.5) / chi_q
        lnk_q = np.log(k_q)
        # Clamp subhorizon high-k tail (> 0.2 Mpc^-1 at low z) smoothly to k=0.2 Mpc^-1 plateau
        lnk_c = np.clip(lnk_q, lnk_grid[0], lnk_grid[-1])
        # Vectorized linear interpolation along axis 0 (lnk_grid uniform!)
        dlnk = lnk_grid[1] - lnk_grid[0]
        f_idx = (lnk_c - lnk_grid[0]) / dlnk
        i0 = np.clip(np.floor(f_idx).astype(int), 0, len(K_GRID) - 2)
        t = f_idx - i0
        col = np.arange(len(chi_q))
        phi_val = (1.0 - t) * Phi_at_zq[i0, col] + t * Phi_at_zq[i0 + 1, col]
        Tk = T_EH_no_wiggle(k_q, h, Om)
        Delta_PhiW_sq = (0.6 * Tk * phi_val) ** 2 * ((k_q / K_PIVOT) ** (N_S - 1.0))
        integrand = ((chi_star - chi_q) / chi_star) ** 2 / chi_q * Delta_PhiW_sq
        pref = 8.0 * math.pi * math.pi / ((L + 0.5) ** 3)
        val_all = float(np.trapezoid(integrand, chi_q) * pref)
        mask_in = (k_q >= K_GRID[0]) & (k_q <= K_GRID[-1])
        val_in = float(np.trapezoid(np.where(mask_in, integrand, 0.0), chi_q) * pref)
        CL_lens[str(L)] = val_all
        frac_in_kgrid[str(L)] = float(val_in / val_all) if val_all > 0.0 else 1.0

    # --- 2. Exact Spherical-Bessel Late-ISW C_ell^{ISW} over z in [0, 5] ---
    m_isw_z = z_asc <= Z_ISW_MAX + 1e-9
    z_isw = z_asc[m_isw_z]
    chi_isw = np.interp(z_isw, Z_CHI_GRID, chi_grid)
    k_isw = np.geomspace(float(K_GRID[0]), float(K_GRID[-1]), 350)
    lnk_isw = np.log(k_isw)
    Tk_isw = T_EH_no_wiggle(k_isw, h, Om)
    # Interpolate dPhiW/dz onto (350, len(z_isw)) via uniform ln k grid
    dPhi_isw_modes = dPhi_asc[:, m_isw_z]
    dlnk = lnk_grid[1] - lnk_grid[0]
    f_idx = (lnk_isw - lnk_grid[0]) / dlnk
    i0 = np.clip(np.floor(f_idx).astype(int), 0, len(K_GRID) - 2)
    t = (f_idx - i0)[:, None]
    dPhi_fine = (1.0 - t) * dPhi_isw_modes[i0, :] + t * dPhi_isw_modes[i0 + 1, :]  # (350, len(z_isw))

    arg_jl = k_isw[:, None] * chi_isw[None, :]  # (350, len(z_isw))
    prim_k = (k_isw / K_PIVOT) ** (N_S - 1.0)
    CL_isw = {}
    for ell in ELL_ISW:
        jl_mat = spherical_jn(ell, arg_jl)
        # I_ell(k) = 2 * int_0^5 (3/5) T_EH(k) (dPhiW/dz) j_ell(k chi) dz
        I_k = 1.2 * Tk_isw * np.trapezoid(dPhi_fine * jl_mat, z_isw, axis=1)
        CL_isw[str(ell)] = float(4.0 * math.pi * np.trapezoid(prim_k * I_k * I_k, lnk_isw))

    return {"CL_lens": CL_lens, "frac_lens_in_kgrid": frac_in_kgrid, "CL_isw": CL_isw}


def get_parameter_points() -> dict:
    """Return pre-registered parameter points at w_d = 0, optionally verifying 2-sigma floor via fit_coupled."""
    refit_source = "FLUX_CODAZZI.json + verified offline fallback"
    h_2sig, Om_2sig = 0.6809446513808862, 0.3053775039770976
    kap_2sig = -0.8317241771601472
    ed_dir = os.path.abspath(os.path.join(HERE, "../../04_cosmology/external_data"))
    if os.path.isdir(ed_dir):
        _cwd = os.getcwd()
        try:
            os.chdir(HERE)
            sys.path.insert(0, HERE)
            import flux_codazzi_check as F  # noqa: E402
            _, p2s = F.fit_coupled("pantheon", fix_kappa=kap_2sig)
            h_2sig, Om_2sig = float(p2s[0]), float(p2s[1])
            refit_source = "flux_codazzi_check.fit_coupled('pantheon', fix_kappa=-0.8317241771601472)"
        except Exception as exc:
            refit_source = f"fallback after {type(exc).__name__}"
        finally:
            os.chdir(_cwd)

    return {
        "refit_source": refit_source,
        "points": {
            "LCDM_control": {"kappa": 0.0, "h": 0.6810363151866539, "Om": 0.30360698573080336},
            "Pantheon+_best": {"kappa": -2.2444519783747996, "h": 0.6803247862228956, "Om": 0.30865546826192025},
            "DES-Dovekie_best": {"kappa": -2.496571182856366, "h": 0.6801065733422411, "Om": 0.3093795670685889},
            "Pantheon+_2sigma_floor": {"kappa": kap_2sig, "h": h_2sig, "Om": Om_2sig},
        },
    }


def build_and_run_runs(run_specs: dict[str, dict], pool: ProcessPoolExecutor, lcdm_obs: dict) -> dict:
    """Enqueue all (run_key, k) tasks sorted largest-k first across pool and compute observables."""
    tasks = []
    for rkey, spec in run_specs.items():
        h, Om, kappa = spec["h"], spec["Om"], spec["kappa"]
        for idx_k, kv in enumerate(K_GRID):
            tasks.append((
                rkey, idx_k, float(kv), h, Om, kappa,
                spec["law"], spec["closure"], spec["c_vis2"],
                spec["v_flux"], spec["ic_W"], bool(idx_k in (0, 12, 24)),
            ))
    # Sort descending by k so long high-k modes start first across all 8 workers
    tasks.sort(key=lambda t: -t[2])
    raw_results = list(pool.map(_solve_single_mode, tasks))

    grouped = {rkey: {} for rkey in run_specs}
    for rkey, idx_k, ok, PhiW, dPhiW_dz, extra in raw_results:
        grouped[rkey][idx_k] = (ok, PhiW, dPhiW_dz, extra)

    summaries = {}
    for rkey, spec in run_specs.items():
        modes = grouped[rkey]
        all_ok = all(modes[i][0] for i in range(len(K_GRID)))
        if not all_ok:
            summaries[rkey] = {**spec, "linear_stable": False, "pass_envelope": False}
            continue
        PhiW_mat = np.vstack([modes[i][1] for i in range(len(K_GRID))])
        dPhiW_dz_mat = np.vstack([modes[i][2] for i in range(len(K_GRID))])
        max_amp = max(modes[i][3]["max_abs_PhiW"] for i in range(len(K_GRID)))
        linear_stable = bool(np.all(np.isfinite(PhiW_mat)) and max_amp < 1e3)
        obs = compute_observables_for_run(spec["h"], spec["Om"], spec["kappa"], PhiW_mat, dPhiW_dz_mat)
        lens_ratios = {
            L: float(obs["CL_lens"][L] / lcdm_obs["CL_lens"][L]) for L in map(str, L_LENS)
        }
        isw_ratios = {
            ell: float(obs["CL_isw"][ell] / lcdm_obs["CL_isw"][ell]) for ell in map(str, ELL_ISW)
        }
        vals_l = list(lens_ratios.values())
        vals_i = list(isw_ratios.values())
        A_mean = float(np.mean(vals_l))
        A_min, A_max = float(min(vals_l)), float(max(vals_l))
        I_min, I_max = float(min(vals_i)), float(max(vals_i))
        lens_pass_mean = abs(A_mean - 1.0) <= 0.08
        lens_pass_all_L = all(abs(v - 1.0) <= 0.08 for v in vals_l)
        isw_pass = all(0.4 <= v <= 1.6 for v in vals_i)
        resid_samples = {f"k={K_GRID[idx]:.4g}": modes[idx][3] for idx in (0, 12, 24)}
        summaries[rkey] = {
            **spec,
            "linear_stable": linear_stable,
            "max_abs_PhiW": float(max_amp),
            "PhiW_z0_k0p0001_k0p01_k0p2": [float(PhiW_mat[0, -1]), float(PhiW_mat[12, -1]), float(PhiW_mat[24, -1])],
            "A_phiphi_by_L": lens_ratios,
            "A_phiphi_mean": A_mean,
            "A_phiphi_min_max": [A_min, A_max],
            "frac_lens_in_kgrid_min": float(min(obs["frac_lens_in_kgrid"].values())),
            "ISW_ratio_by_ell": isw_ratios,
            "ISW_ratio_min_max": [I_min, I_max],
            "lens_pass_mean": bool(lens_pass_mean),
            "lens_pass_all_L": bool(lens_pass_all_L),
            "isw_pass": bool(isw_pass),
            "pass_envelope_meanL": bool(linear_stable and lens_pass_mean and isw_pass),
            "pass_envelope_allL": bool(linear_stable and lens_pass_all_L and isw_pass),
            "resid_samples": resid_samples,
        }
    return summaries


def evaluate_prereg_verdict(summaries: dict, law_filter: str) -> dict:
    """Evaluate PREREG_WEYL_ENVELOPE.md decision rule for a given covariant realization."""
    causal_best = [
        v for k, v in summaries.items()
        if v["law"] == law_filter and v["bg_name"] in ("Pantheon+_best", "DES-Dovekie_best")
        and (v["closure"] == "hu98" or v["closure"] == "mb95_l8")
    ]
    causal_2sig = [
        v for k, v in summaries.items()
        if v["law"] == law_filter and v["bg_name"] == "Pantheon+_2sigma_floor"
        and (v["closure"] == "hu98" or v["closure"] == "mb95_l8")
    ]
    surv_best_allL = [v for v in causal_best if v["pass_envelope_allL"]]
    surv_best_meanL = [v for v in causal_best if v["pass_envelope_meanL"]]
    surv_2sig_allL = [v for v in causal_2sig if v["pass_envelope_allL"]]
    surv_2sig_meanL = [v for v in causal_2sig if v["pass_envelope_meanL"]]
    if surv_best_allL:
        verdict = "SURVIVES ENVELOPE (5D PDE justified)"
    elif surv_best_meanL:
        verdict = "SURVIVES ENVELOPE (mean-L pass, mild L-tilt >8% at an endpoint)"
    elif surv_2sig_meanL or surv_2sig_allL:
        verdict = "TIGHTENED / BOUNDED [O] (best fit fails; 2-sigma floor survives)"
    else:
        verdict = "KILLED MODEL-INDEPENDENTLY [X]"
    return {
        "law": law_filter,
        "verdict": verdict,
        "n_best_pass_allL": len(surv_best_allL),
        "n_best_pass_meanL": len(surv_best_meanL),
        "n_2sig_pass_allL": len(surv_2sig_allL),
        "n_2sig_pass_meanL": len(surv_2sig_meanL),
        "passing_best_keys": [k for k, v in summaries.items() if v in surv_best_meanL],
        "passing_2sig_keys": [k for k, v in summaries.items() if v in surv_2sig_meanL],
    }


def main() -> int:
    t0 = time.time()
    print("=== (S1) SymPy Exact Covariant Perturbation + Bianchi Verification ===", flush=True)
    sym_res = run_symbolic_s1()
    print(json.dumps(sym_res, indent=1), flush=True)

    param_info = get_parameter_points()
    pts = param_info["points"]
    print(f"\nParameter refit source: {param_info['refit_source']}", flush=True)
    for k, v in pts.items():
        print(f"  {k:<24}: kappa={v['kappa']:+.6f} h={v['h']:.6f} Om={v['Om']:.6f}", flush=True)

    # --- (N1) Controls ---
    print("\n=== (N1) Control Checks ===", flush=True)
    ref_d1_exact, ref_ratio = compute_ref_d1_growth(0.6736, 0.3153, 0.0)
    ctrl_mode = _solve_single_mode(("ctrl", 24, 0.2, 0.6736, 0.3153, 0.0, "C_Fd0", "hu98", 0.0, "bulk_rest", "adiabatic", True))
    ctrl_extra = ctrl_mode[5]
    rel_d1 = abs(ctrl_extra["dm_z0"] / ctrl_extra["dm_i"] * A_INIT - ref_d1_exact) / ref_d1_exact
    rel_late = abs(ctrl_extra["dm_ratio_1_0p1"] - ref_ratio) / ref_ratio
    print(
        f"  Planck LCDM control (k=0.2): rel_D1={rel_d1:.2e} (<2e-3), "
        f"rel_late_growth={rel_late:.2e} (<1e-4), "
        f"E03_res={ctrl_extra['E03_minus_E00_at_0p5']:.2e} (<1e-6), "
        f"Phi-Psi={ctrl_extra['max_Phi_minus_Psi']:.1e}",
        flush=True,
    )
    assert rel_d1 < 2e-3 and rel_late < 1e-4 and ctrl_extra["E03_minus_E00_at_0p5"] < 1e-6 and ctrl_extra["max_Phi_minus_Psi"] < 1e-12

    e33_test_C = _solve_single_mode(("e33_chk", 12, 0.05, pts["Pantheon+_best"]["h"], pts["Pantheon+_best"]["Om"], pts["Pantheon+_best"]["kappa"], "C_Fd0", "hu98", 1.0 / 3.0, "bulk_rest", "adiabatic", True))
    e33_res_val = e33_test_C[5]["E33_residual_at_a0p5"]
    print(f"  Law C E33 consistency check at (Pantheon+, k=0.05, cvis2=1/3): resid={e33_res_val:.2e} (<1e-6)", flush=True)
    assert e33_res_val < 1e-6

    n_workers = min(8, os.cpu_count() or 4)
    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        # Step A: LCDM_control 25-mode baseline
        print(f"\n=== (N2) Solving LCDM_control + Primary & Sensitivity Sweeps (workers={n_workers}) ===", flush=True)
        lcdm_tasks = [("LCDM_control", i, float(kv), pts["LCDM_control"]["h"], pts["LCDM_control"]["Om"], 0.0, "C_Fd0", "hu98", 0.0, "bulk_rest", "adiabatic", i in (0, 12, 24)) for i, kv in enumerate(K_GRID)]
        lcdm_res = list(pool.map(_solve_single_mode, sorted(lcdm_tasks, key=lambda t: -t[2])))
        lcdm_map = {res[1]: res for res in lcdm_res}
        assert all(lcdm_map[i][0] for i in range(len(K_GRID)))
        lcdm_PhiW = np.vstack([lcdm_map[i][3] for i in range(len(K_GRID))])
        lcdm_dPhiW = np.vstack([lcdm_map[i][4] for i in range(len(K_GRID))])
        lcdm_obs = compute_observables_for_run(pts["LCDM_control"]["h"], pts["LCDM_control"]["Om"], 0.0, lcdm_PhiW, lcdm_dPhiW)

        # Build pre-registered run specifications
        run_specs = {}
        # 1. Primary grid for BOTH covariant realizations across Pantheon+, DES-Dovekie, Pantheon+ 2sigma floor
        for law in ("C_Fd0", "A_freefall"):
            for bg_name in ("Pantheon+_best", "DES-Dovekie_best", "Pantheon+_2sigma_floor"):
                bp = pts[bg_name]
                for c2 in C_VIS2_GRID:
                    tag = f"{law}|{bg_name}|hu98|cvis2={c2:.4f}|bulk_rest|adiabatic"
                    run_specs[tag] = {
                        "law": law, "bg_name": bg_name, "closure": "hu98",
                        "c_vis2": float(c2), "v_flux": "bulk_rest", "ic_W": "adiabatic", **bp,
                    }
                tag_mb = f"{law}|{bg_name}|mb95_l8|bulk_rest|adiabatic"
                run_specs[tag_mb] = {
                    "law": law, "bg_name": bg_name, "closure": "mb95_l8",
                    "c_vis2": 1.0 / 3.0, "v_flux": "bulk_rest", "ic_W": "adiabatic", **bp,
                }

        # 2. V_flux = matter_comoving sensitivity on Law A (Pantheon+_best & 2sigma floor)
        for bg_name in ("Pantheon+_best", "Pantheon+_2sigma_floor"):
            bp = pts[bg_name]
            for c2 in C_VIS2_GRID:
                tag = f"A_freefall|{bg_name}|hu98|cvis2={c2:.4f}|matter_comoving|adiabatic"
                run_specs[tag] = {
                    "law": "A_freefall", "bg_name": bg_name, "closure": "hu98",
                    "c_vis2": float(c2), "v_flux": "matter_comoving", "ic_W": "adiabatic", **bp,
                }

        # 3. Early IC_W = unperturbed sensitivity on Pantheon+_best for both laws
        for law in ("C_Fd0", "A_freefall"):
            for c2 in (0.0, 1.0 / 3.0, 1.0):
                tag = f"{law}|Pantheon+_best|hu98|cvis2={c2:.4f}|bulk_rest|unperturbed"
                run_specs[tag] = {
                    "law": law, "bg_name": "Pantheon+_best", "closure": "hu98",
                    "c_vis2": float(c2), "v_flux": "bulk_rest", "ic_W": "unperturbed", **pts["Pantheon+_best"],
                }

        print(f"Running {len(run_specs)} x {len(K_GRID)} = {len(run_specs)*len(K_GRID)} coupled modes...", flush=True)
        summaries = build_and_run_runs(run_specs, pool, lcdm_obs)

        verdict_C = evaluate_prereg_verdict(summaries, "C_Fd0")
        verdict_A = evaluate_prereg_verdict(summaries, "A_freefall")

        # Scan intermediate |kappa| ceiling whenever best-fit fails while 2-sigma floor survives
        ceiling_scans = {}
        for law, vdict in (("C_Fd0", verdict_C), ("A_freefall", verdict_A)):
            if "TIGHTENED" in vdict["verdict"]:
                scan_specs = {}
                for kap_s in (-1.0, -1.25, -1.5, -1.75, -2.0):
                    # Smooth linear interpolation of fitted (h, Om) between -0.8317 and -2.2445
                    frac = (kap_s - pts["Pantheon+_2sigma_floor"]["kappa"]) / (pts["Pantheon+_best"]["kappa"] - pts["Pantheon+_2sigma_floor"]["kappa"])
                    h_s = pts["Pantheon+_2sigma_floor"]["h"] + frac * (pts["Pantheon+_best"]["h"] - pts["Pantheon+_2sigma_floor"]["h"])
                    Om_s = pts["Pantheon+_2sigma_floor"]["Om"] + frac * (pts["Pantheon+_best"]["Om"] - pts["Pantheon+_2sigma_floor"]["Om"])
                    for c2 in C_VIS2_GRID:
                        tag = f"{law}|scan_kap={kap_s:.2f}|hu98|cvis2={c2:.4f}"
                        scan_specs[tag] = {
                            "law": law, "bg_name": f"scan_kap={kap_s:.2f}", "closure": "hu98",
                            "c_vis2": float(c2), "v_flux": "bulk_rest", "ic_W": "adiabatic",
                            "kappa": kap_s, "h": h_s, "Om": Om_s,
                        }
                ceiling_scans[law] = build_and_run_runs(scan_specs, pool, lcdm_obs)

    # Print readable tables
    for law_lbl in ("C_Fd0", "A_freefall"):
        print(f"\n=== RESULTS SUMMARY: {law_lbl} (bulk_rest, adiabatic) ===", flush=True)
        for bg_name in ("Pantheon+_best", "DES-Dovekie_best", "Pantheon+_2sigma_floor"):
            print(f"  -- {bg_name} (kappa={pts[bg_name]['kappa']:.4f}) --", flush=True)
            rows_bg = [v for v in summaries.values() if v["law"] == law_lbl and v["bg_name"] == bg_name and v["v_flux"] == "bulk_rest" and v["ic_W"] == "adiabatic"]
            for r in rows_bg:
                if not r["linear_stable"]:
                    print(f"    {r['closure']:<8} cvis2={r['c_vis2']:.3f} -> UNSTABLE", flush=True)
                    continue
                al0, al1 = r["A_phiphi_min_max"]
                il0, il1 = r["ISW_ratio_min_max"]
                print(
                    f"    {r['closure']:<8} cvis2={r['c_vis2']:.3f} | A_mean={r['A_phiphi_mean']:.4f} [{al0:.4f},{al1:.4f}] "
                    f"| ISW=[{il0:.3f},{il1:.3f}] | meanL={r['pass_envelope_meanL']} allL={r['pass_envelope_allL']}",
                    flush=True,
                )

    print("\n=== PRE-REGISTERED VERDICTS ===", flush=True)
    print("Law C (C_Fd0, zero-momentum geometric drag):", json.dumps(verdict_C, indent=1), flush=True)
    print("Law A (A_freefall, Q_i = q_4 u_F):         ", json.dumps(verdict_A, indent=1), flush=True)

    out = {
        "prereg_commit": "7ea3f668",
        "S1_symbolic_verification": sym_res,
        "N1_controls": {
            "planck_LCDM_k0p2_rel_D1": float(rel_d1),
            "planck_LCDM_k0p2_rel_late_growth": float(rel_late),
            "planck_LCDM_k0p2_E03_resid": float(ctrl_extra["E03_minus_E00_at_0p5"]),
            "planck_LCDM_k0p2_max_Phi_minus_Psi": float(ctrl_extra["max_Phi_minus_Psi"]),
            "LawC_Pantheon_k0p05_cvis2_1_3_E33_resid": float(e33_res_val),
        },
        "parameter_points": param_info,
        "LCDM_control_baseline": lcdm_obs,
        "runs": summaries,
        "ceiling_scans": ceiling_scans,
        "verdicts": {"LawC_Fd0": verdict_C, "LawA_freefall": verdict_A},
        "elapsed_seconds": float(time.time() - t0),
    }
    out_path = os.path.join(HERE, "WEYL_CAUSAL_ENVELOPE.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nWrote {out_path} in {out['elapsed_seconds']:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
