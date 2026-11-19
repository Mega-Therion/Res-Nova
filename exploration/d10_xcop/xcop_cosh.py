#!/usr/bin/env python3
"""Pre-registered X-COP R200 test with the corpus's own Cosh K(Q) (PREREG_COSH.md, 29b64d1a).

Replaces quadratic dust source -mu^2 r^2 Phi with Cosh: mu^2 r^2 Phi_c sinh(-Phi / Phi_c),
Phi_c = c^2 r, across the exact pre-registered grid r in {inf, 1e-3, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6}.

Includes:
  1. Verbatim #257 Test C reproduction (mode="testc_exact", no events, 6-step np.gradient on N=800)
     at r = inf to satisfy the PREREG_COSH.md control check and quantify the #257 sawtooth bias.
  2. Continuum-converged smooth_phi solver (RK45 rtol=1e-7, deg-14 log-log polynomial derivative,
     0.75-relaxed fixed point to max|dS| < 1e-4, O(1) S(r) lookup, overflow/W-zero events,
     Bratu turning-point refinement, finite-difference self-consistency residual fd_resid,
     and 8-worker multiprocessing).
  3. Independent DOP853 N=400 deg-14 cross-check if any finite r passes PREREG_COSH.md.
  4. Secondary fixed-mu free-boundary Phi0 cap diagnostic at 1e-4, 3e-5, 1e-5 (+ any passing r).
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import importlib.util
import json
import math
import os
import sys
import time
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
D_CL = os.path.abspath(os.path.join(HERE, "../../02_galaxy_dynamics/clusters"))
_cwd = os.getcwd()
os.chdir(D_CL)
_spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py")
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)
os.chdir(_cwd)

MPC, G, MS = cm.MPC_M, cm.G_SI, cm.MSUN
C_LIGHT = 2.99792458e8
MU0 = 1.0 / (0.9895 * MPC)
XHLOW = 154.0
Om = 0.315
H0 = 67.4e3 / MPC
Hz = lambda z: H0 * math.sqrt(Om * (1.0 + z) ** 3 + 1.0 - Om)

A0 = cm.A0
INV_A0 = 1.0 / A0


def g_mond_fast(u: float) -> float:
    if u <= 0.0:
        return 0.0
    s = u * INV_A0
    return A0 * math.sqrt(0.5 * (s * s + s * math.sqrt(s * s + 4.0)))


law = lambda u: cm.g_mond(max(u, 0.0))

PREG_GRID = ["inf", "1e-3", "1e-4", "3e-5", "1e-5", "3e-6", "1e-6"]


def shape_mass(x: float, xc: float, beta: float) -> float:
    return quad(lambda r: r**2 * (1.0 + (r / xc) ** 2) ** (-1.5 * beta), 0.0, x, limit=200)[0]


def load_xcop() -> list[dict]:
    rows = []
    with open(os.path.join(HERE, "xcop_data.tsv")) as f:
        for l in f:
            if not l.startswith("#") and l.strip():
                nm, z, R5, R2, MH5, MH2, f5, f2, Mt5, Mt2 = l.split("\t")
                z_f = float(z)
                R5_m, R2_m = float(R5) * MPC, float(R2) * MPC
                Mg5 = float(f5) * float(MH5) * 1e14 * MS
                Mg2 = float(f2) * float(MH2) * 1e14 * MS
                Mt5_v, Mt2_v = float(Mt5) * 1e14 * MS, float(Mt2) * 1e14 * MS
                xc = 0.1
                beta = brentq(lambda b: shape_mass(R2_m / R5_m, xc, b) / shape_mass(1.0, xc, b) - Mg2 / Mg5, 0.3, 3.0)
                rv = R2_m * (200.0 / 177.8) ** (1.0 / 3.0)
                rc = xc * R5_m
                A = 1.09 * Mg5 / (4.0 * math.pi * R5_m**3 * shape_mass(1.0, xc, beta))
                rg = np.linspace(0.0, rv, 4001)
                rhov = A * (1.0 + (rg / rc) ** 2) ** (-1.5 * beta)
                Mb_g = np.concatenate([[0.0], np.cumsum(0.5 * (4.0 * math.pi * rg[1:] ** 2 * rhov[1:] + 4.0 * math.pi * rg[:-1] ** 2 * rhov[:-1]) * np.diff(rg))])
                rows.append({
                    "name": nm,
                    "z": z_f,
                    "Hz": Hz(z_f),
                    "R5": R5_m,
                    "R2": R2_m,
                    "rv": rv,
                    "rc": rc,
                    "beta": float(beta),
                    "A": float(A),
                    "Mg5": Mg5,
                    "Mt5": Mt5_v,
                    "Mt2": Mt2_v,
                    "fbar500": float(1.09 * Mg5 / Mt5_v),
                    "rg": rg,
                    "Mb_g": Mb_g,
                    "Mb_rmin": float(np.interp(1e-4 * R5_m, rg, Mb_g)),
                    "Mb_R5": float(np.interp(R5_m, rg, Mb_g)),
                    "Mb_R2": float(np.interp(R2_m, rg, Mb_g)),
                    "Mb_rv": float(Mb_g[-1]),
                })
    return rows


def _solve_testc_exact_cluster(cl: dict) -> dict:
    """Verbatim reproduction of #257 Test C (xcop_screened_full.py) at r = inf with zero events."""
    R5, R2, rv, A, rc, beta, Hz_val = cl["R5"], cl["R2"], cl["rv"], cl["A"], cl["rc"], cl["beta"], cl["Hz"]
    rho = lambda r: A * (1.0 + (r / rc) ** 2) ** (-1.5 * beta)
    rg, Mb_g = cl["rg"], cl["Mb_g"]
    Mb = lambda r: np.interp(r, rg, Mb_g)
    STAB = [np.array([0.0, 1e30]), np.array([1.0, 1.0])]

    def solve(mu: float):
        rmin = 1e-4 * R5
        Sx = lambda r: float(np.interp(r, STAB[0], STAB[1]))
        glaw = lambda u, r: u + Sx(r) * (law(u) - u)
        rhs = lambda r, y: [G * 4.0 * math.pi * r**2 * rho(r) - mu**2 * r**2 * y[1], glaw(y[0] / r**2, r)]

        def shoot(P0: float, full: bool = False):
            s = solve_ivp(rhs, (rmin, rv), [G * Mb(rmin), P0], method="DOP853", rtol=1e-8, atol=[1e21, 1.0], dense_output=full)
            return s if full else s.y[1, -1]

        g0 = -law(G * Mb(R5) / R5**2) * rv * 3.0
        grid = np.linspace(-6.0 * abs(g0), 2.0 * abs(g0), 41)
        F = [shoot(p) for p in grid]
        i = next(i for i in range(40) if F[i] * F[i + 1] < 0.0)
        s = shoot(brentq(shoot, grid[i], grid[i + 1], xtol=1e-6 * abs(g0)), True)
        Md = lambda r: glaw(s.sol(r)[0] / r**2, r) * r**2 / G
        rr = np.linspace(1e-3 * R5, rv, 800)
        gt = np.array([glaw(s.sol(x)[0] / x**2, x) for x in rr])
        return cl["Mt5"] / Md(R5), cl["Mt2"] / Md(R2), ((s.sol(rv)[0] - G * Mb(rv)) / G) / (5.36 * Mb(rv)), rr, gt

    def iterate(mu: float):
        STAB[0], STAB[1] = np.array([0.0, 1e30]), np.array([1.0, 1.0])
        last = None
        max_dS = 0.0
        Snew = np.ones(800)
        for _ in range(6):
            a5, a2, dr, rr, gt = solve(mu)
            gp = np.gradient(gt, rr)
            xh = np.sqrt(gp**2 + 2.0 * (gt / rr) ** 2) / Hz_val**2
            Snew = 1.0 / (1.0 + (XHLOW / xh) ** 2)
            if len(STAB[1]) == len(Snew):
                max_dS = float(np.max(np.abs(Snew - STAB[1])))
            STAB[0], STAB[1] = rr, Snew
            last = a5
        a5, a2, dr, _, _ = solve(mu)
        return a5, a2, dr, abs(a5 - last), float(np.interp(R2, rr, Snew)), max_dS, float(np.max(np.abs(np.diff(Snew))))

    Rm5 = cl["Mt5"] / (law(G * Mb(R5) / R5**2) * R5**2 / G)
    Rm2 = cl["Mt2"] / (law(G * Mb(R2) / R2**2) * R2**2 / G)
    S5, S2, dust, conv, S_R200, max_dS_st, jump_st = iterate(MU0)
    if dust > 1.0:
        sc = brentq(lambda s: iterate(MU0 * s)[2] - 1.0, 1e-3, 1.0, xtol=1e-3)
        C5, C2, _, _, _, max_dS_cp, _ = iterate(MU0 * sc)
    else:
        sc, C5, C2, max_dS_cp = 1.0, S5, S2, max_dS_st
    return {
        "name": cl["name"],
        "beta": cl["beta"],
        "fbar500": cl["fbar500"],
        "R500_pureMOND": float(Rm5),
        "R200_pureMOND": float(Rm2),
        "static_converged": True,
        "capped_converged": True,
        "R500_static": float(S5),
        "R200_static": float(S2),
        "dust_ratio": float(dust),
        "mu_scale_cap": float(sc),
        "last_change": float(conv),
        "S_at_R200": float(S_R200),
        "max_dS": float(max(max_dS_st, max_dS_cp)),
        "max_dS_grid_jump": float(jump_st),
        "R500_capped": float(C5),
        "R200_capped": float(C2),
    }


def solve_single_bvp(
    cl: dict,
    mu: float,
    r_cosh: float,
    rr_S: np.ndarray,
    S_arr: np.ndarray,
    P0_hint: float | None = None,
    free_Phi0: bool = False,
    ode_method: str = "RK45",
    ode_rtol: float = 1e-7,
):
    """Solve one spherical BVP on [rmin, rv] for fixed S(r) tabulation with O(1) lookup."""
    R5, rv, A, rc, beta = cl["R5"], cl["rv"], cl["A"], cl["rc"], cl["beta"]
    Mb_rmin, Mb_rv = cl["Mb_rmin"], cl["Mb_rv"]
    rmin = 1e-4 * R5
    is_inf = not math.isfinite(r_cosh)
    PHIC = C_LIGHT**2 * r_cosh if not is_inf else 1.0
    inv_PHIC = 1.0 / PHIC
    four_pi_G = 4.0 * math.pi * G
    mu2 = mu * mu
    inv_rc2 = 1.0 / (rc * rc)
    neg_15b = -1.5 * beta

    r0_g = float(rr_S[0])
    inv_dr = (len(rr_S) - 1) / float(rr_S[-1] - r0_g)
    n_g = len(rr_S) - 1
    S_list = S_arr.tolist()

    def get_S(r: float) -> float:
        idx_f = (r - r0_g) * inv_dr
        if idx_f <= 0.0:
            return S_list[0]
        if idx_f >= n_g:
            return S_list[n_g]
        i = int(idx_f)
        return S_list[i] + (idx_f - i) * (S_list[i + 1] - S_list[i])

    def glaw(u: float, r: float) -> float:
        S = get_S(r)
        return u + S * (g_mond_fast(u) - u)

    if is_inf:
        def rhs(r, y):
            W, P = y[0], y[1]
            r2 = r * r
            u = W / r2 if W > 0.0 else 0.0
            rho_r = A * (1.0 + r2 * inv_rc2) ** neg_15b
            src_val = 0.0 if (free_Phi0 and P >= 0.0) else -P
            S = get_S(r)
            gm = g_mond_fast(u)
            return [four_pi_G * r2 * rho_r + mu2 * r2 * src_val, u + S * (gm - u)]
    else:
        def rhs(r, y):
            W, P = y[0], y[1]
            r2 = r * r
            u = W / r2 if W > 0.0 else 0.0
            rho_r = A * (1.0 + r2 * inv_rc2) ** neg_15b
            if free_Phi0 and P >= 0.0:
                src_val = 0.0
            else:
                arg = -P * inv_PHIC
                if arg > 80.0:
                    arg = 80.0
                elif arg < -80.0:
                    arg = -80.0
                src_val = PHIC * math.sinh(arg)
            S = get_S(r)
            gm = g_mond_fast(u)
            return [four_pi_G * r2 * rho_r + mu2 * r2 * src_val, u + S * (gm - u)]

    def ev_W_zero(r, y):
        return y[0]

    ev_W_zero.terminal = True
    ev_W_zero.direction = -1

    if not is_inf:
        def ev_ovf(r, y):
            return min(50.0 - abs(y[1]) * inv_PHIC, 1e55 - abs(y[0]))
    else:
        def ev_ovf(r, y):
            return 1e55 - abs(y[0])

    ev_ovf.terminal = True
    ev_ovf.direction = -1
    events = [ev_W_zero, ev_ovf]

    def integrate(P0: float, full: bool = False):
        s = solve_ivp(
            rhs,
            (rmin, rv),
            [G * Mb_rmin, P0],
            method=ode_method,
            rtol=ode_rtol,
            atol=[1e21, 1.0],
            events=events,
            dense_output=full,
        )
        hit_W = len(s.t_events[0]) > 0
        hit_ovf = len(s.t_events[1]) > 0
        if hit_W:
            reason = "W_zero"
            val = float("nan")
        elif not s.success:
            reason = "fail"
            val = float("nan")
        elif hit_ovf:
            reason = "ovf_pos" if s.y[1, -1] >= 0.0 else "ovf_neg"
            val = float(s.y[1, -1])
        else:
            reason = "ok"
            val = float(s.y[1, -1])
        return (s, hit_W, hit_ovf, reason, val) if full else (val, reason)

    if free_Phi0:
        assert P0_hint is not None
        s, hit_W, hit_ovf, reason, val = integrate(P0_hint, True)
        if hit_W or hit_ovf or not s.success:
            return {"converged": False}
        Md = lambda r: glaw(max(s.sol(r)[0], 0.0) / (r * r), r) * r * r / G
        R5_val = cl["Mt5"] / Md(R5)
        R2_val = cl["Mt2"] / Md(cl["R2"])
        dust_val = ((s.sol(rv)[0] - G * Mb_rv) / G) / (5.36 * Mb_rv)
        edge_pts = np.linspace(rmin, rv, 800)
        psi_vals = s.sol(edge_pts)[1]
        pos_idx = np.where(psi_vals >= 0.0)[0]
        R_edge = float(edge_pts[pos_idx[0]]) if len(pos_idx) > 0 else float(rv)
        return {
            "converged": True,
            "P0": float(P0_hint),
            "R500": float(R5_val),
            "R200": float(R2_val),
            "dust_ratio": float(dust_val),
            "R_edge_over_rv": float(R_edge / rv),
            "sol": s,
            "glaw": glaw,
        }

    def shoot_val(p: float) -> float:
        v, rsn = integrate(p)
        if rsn == "W_zero":
            return +1e30  # Phi turned positive early inside rv; sits on positive-Phi side of root
        return v

    g0 = g_mond_fast(G * cl["Mb_R5"] / (R5 * R5)) * rv * 3.0
    max_neg = 12.0 * abs(g0) if is_inf else min(12.0 * abs(g0), 48.0 * PHIC)

    root_P0 = None
    if P0_hint is not None and -max_neg < P0_hint < 0.0:
        for f_lo, f_hi in ((1.15, 0.85), (2.0, 0.5)):
            lo_w = max(-max_neg, f_lo * P0_hint)
            hi_w = min(-1e-6 * min(abs(g0), max_neg), f_hi * P0_hint)
            if lo_w < hi_w:
                flo, rlo = integrate(lo_w)
                fhi, rhi = integrate(hi_w)
                if rlo == "ok" and rhi == "ok" and flo * fhi <= 0.0:
                    root_P0 = brentq(shoot_val, lo_w, hi_w, xtol=1e-6 * max(abs(P0_hint), 1e6))
                    break

    if root_P0 is None and is_inf:
        lo_i, hi_i = -8.0 * abs(g0), 0.0
        flo, rlo = integrate(lo_i)
        fhi, rhi = integrate(hi_i)
        if rlo == "ok" and rhi == "ok" and flo * fhi <= 0.0:
            root_P0 = brentq(shoot_val, lo_i, hi_i, xtol=1e-6 * abs(g0))

    if root_P0 is None:
        scale_list = list(-np.geomspace(1e-3 * min(abs(g0), max_neg), max_neg, 28))
        if not is_inf and max_neg > 5.0 * PHIC:
            extra = list(-np.linspace(0.5 * PHIC, min(max_neg, 30.0 * PHIC), 18))
            scale_list = sorted(set(scale_list + extra), reverse=True)
        pts = np.array([0.0] + scale_list, dtype=float)
        vals = []
        reasons = []
        ovf_streak = 0
        for p in pts:
            v, rsn = integrate(float(p))
            vals.append(v)
            reasons.append(rsn)
            if len(vals) >= 2 and reasons[-2] == "ok" and reasons[-1] == "ok" and vals[-2] * vals[-1] <= 0.0:
                root_P0 = brentq(shoot_val, float(pts[len(vals) - 1]), float(pts[len(vals) - 2]), xtol=1e-6 * max(abs(pts[len(vals) - 1]), 1e6))
                break
            # If transitioning directly from W_zero (too shallow, Phi turned positive inside rv) to ok < 0:
            if len(vals) >= 2 and reasons[-2] == "W_zero" and reasons[-1] == "ok" and vals[-1] <= 0.0:
                p_neg = float(pts[len(vals) - 1])
                p_wz = float(pts[len(vals) - 2])
                # Refine interval to find ok with >= 0 near W_zero boundary
                found_pos = None
                lo_s, hi_s = p_neg, p_wz
                for _ in range(12):
                    mid = 0.5 * (lo_s + hi_s)
                    vm, rm = integrate(mid)
                    if rm == "W_zero":
                        hi_s = mid
                    elif rm == "ok" and vm >= 0.0:
                        found_pos = (mid, vm)
                        break
                    elif rm == "ok" and vm < 0.0:
                        lo_s = mid
                        p_neg = mid
                    else:
                        break
                if found_pos is not None:
                    root_P0 = brentq(shoot_val, p_neg, found_pos[0], xtol=1e-6 * max(abs(p_neg), 1e6))
                    break
            if rsn in ("ovf_pos", "ovf_neg", "fail"):
                ovf_streak += 1
                if ovf_streak >= 3 and any(r0 == "ok" for r0 in reasons):
                    break
            else:
                ovf_streak = 0

        if root_P0 is None:
            ok_idx = [i for i, rsn in enumerate(reasons) if rsn == "ok" and math.isfinite(vals[i])]
            if len(ok_idx) >= 3:
                k_min = min(ok_idx, key=lambda i: vals[i])
                lo_i = max(0, k_min - 1)
                hi_i = min(len(pts) - 1, k_min + 1)
                if hi_i > lo_i:
                    def min_obj(p):
                        v, rsn = integrate(float(p))
                        return v if (rsn == "ok" and math.isfinite(v)) else 1e30
                    res = minimize_scalar(
                        min_obj,
                        bounds=(float(pts[hi_i]), float(pts[lo_i])),
                        method="bounded",
                        options={"xatol": 1e-5 * max(abs(pts[k_min]), 1e6)},
                    )
                    if res.fun <= 0.0:
                        hi_p = float(pts[lo_i]) if reasons[lo_i] == "ok" and vals[lo_i] > 0 else float(pts[k_min])
                        v_hi, r_hi = integrate(hi_p)
                        if r_hi == "ok" and v_hi >= 0.0:
                            root_P0 = brentq(shoot_val, float(res.x), hi_p, xtol=1e-6 * max(abs(res.x), 1e6))

    if root_P0 is None:
        return {"converged": False}

    s, hit_W, hit_ovf, reason, _ = integrate(root_P0, True)
    if reason != "ok" or not s.success:
        return {"converged": False}

    Md = lambda r: glaw(max(s.sol(r)[0], 0.0) / (r * r), r) * r * r / G
    return {
        "converged": True,
        "P0": float(root_P0),
        "u_center": float(-root_P0 / PHIC) if not is_inf else 0.0,
        "R500": float(cl["Mt5"] / Md(R5)),
        "R200": float(cl["Mt2"] / Md(cl["R2"])),
        "dust_ratio": float(((s.sol(rv)[0] - G * Mb_rv) / G) / (5.36 * Mb_rv)),
        "sol": s,
        "glaw": glaw,
    }


def solve_cluster_smooth(
    cl: dict,
    mu: float,
    r_cosh: float,
    S_init: np.ndarray | None = None,
    P0_init: float | None = None,
    N_grid: int = 200,
    poly_deg: int = 14,
    ode_method: str = "RK45",
    ode_rtol: float = 1e-7,
):
    """Continuum-converged x_H(Phi) fixed-point iteration with deg-14 log-log derivative."""
    R5, R2, rv, Hz_val = cl["R5"], cl["R2"], cl["rv"], cl["Hz"]
    rr = np.linspace(1e-3 * R5, rv, N_grid)
    lr = np.log(rr / R5)
    S_arr = np.ones_like(rr) if S_init is None else np.interp(rr, np.linspace(1e-3 * R5, rv, len(S_init)), S_init)
    P0_hint = P0_init
    max_dS = 1.0
    fin = None
    gt = None
    for it in range(25):
        res = solve_single_bvp(
            cl, mu, r_cosh, rr, S_arr, P0_hint=P0_hint,
            ode_method=ode_method, ode_rtol=ode_rtol,
        )
        if not res["converged"]:
            return {"converged": False}
        P0_hint = res["P0"]
        s, glaw = res["sol"], res["glaw"]
        gt = np.array([glaw(max(s.sol(x)[0], 0.0) / (x * x), x) for x in rr])
        lg = np.log(np.maximum(gt, 1e-30))
        coef = np.polyfit(lr, lg, poly_deg)
        dlogg_dlogr = np.polyval(np.polyder(coef), lr)
        gp = (gt / rr) * dlogg_dlogr
        xh = np.sqrt(gp * gp + 2.0 * (gt / rr) ** 2) / (Hz_val * Hz_val)
        S_raw = 1.0 / (1.0 + (XHLOW / xh) ** 2)
        S_next = 0.25 * S_arr + 0.75 * S_raw
        max_dS = float(np.max(np.abs(S_next - S_arr)))
        S_arr = S_next
        fin = res
        if it >= 1 and max_dS < 1e-4:
            break

    fin = solve_single_bvp(
        cl, mu, r_cosh, rr, S_arr, P0_hint=P0_hint,
        ode_method=ode_method, ode_rtol=ode_rtol,
    )
    if not fin["converged"]:
        return {"converged": False}
    s, glaw = fin["sol"], fin["glaw"]
    gt = np.array([glaw(max(s.sol(x)[0], 0.0) / (x * x), x) for x in rr])
    gp_fd = np.gradient(gt, rr)
    xh_fd = np.sqrt(gp_fd * gp_fd + 2.0 * (gt / rr) ** 2) / (Hz_val * Hz_val)
    S_fd = 1.0 / (1.0 + (XHLOW / xh_fd) ** 2)
    fd_resid = float(np.max(np.abs(S_fd[2:-2] - S_arr[2:-2])))
    return {
        "converged": True,
        "R500": fin["R500"],
        "R200": fin["R200"],
        "dust_ratio": fin["dust_ratio"],
        "S_at_R200": float(np.interp(R2, rr, S_arr)),
        "u_center": fin["u_center"],
        "P0": fin["P0"],
        "max_dS": max_dS,
        "fd_resid": fd_resid,
        "max_dS_grid_jump": float(np.max(np.abs(np.diff(S_arr)))),
        "n_iter": it + 1,
        "rr": rr,
        "S_arr": S_arr,
    }


def _run_smooth_cluster_task(args: tuple[dict, float]) -> dict:
    cl, r_cosh = args
    Rm5 = cl["Mt5"] / (law(G * cl["Mb_R5"] / cl["R5"] ** 2) * cl["R5"] ** 2 / G)
    Rm2 = cl["Mt2"] / (law(G * cl["Mb_R2"] / cl["R2"] ** 2) * cl["R2"] ** 2 / G)
    st = solve_cluster_smooth(cl, MU0, r_cosh)
    if not st["converged"]:
        s_test = np.linspace(0.05, 0.95, 19)
        cap_row = None
        for idx in range(len(s_test) - 1, -1, -1):
            r_hi = solve_cluster_smooth(cl, MU0 * float(s_test[idx]), r_cosh)
            if r_hi["converged"]:
                if r_hi["dust_ratio"] >= 1.0:
                    cache = [r_hi["S_arr"], r_hi["P0"]]
                    def ddiff(sv):
                        rt = solve_cluster_smooth(cl, MU0 * sv, r_cosh, S_init=cache[0], P0_init=cache[1])
                        if rt["converged"]:
                            cache[0], cache[1] = rt["S_arr"], rt["P0"]
                            return rt["dust_ratio"] - 1.0
                        return +1e3
                    sc = brentq(ddiff, 1e-3, float(s_test[idx]), xtol=1e-3)
                    cap_row = solve_cluster_smooth(cl, MU0 * sc, r_cosh, S_init=cache[0], P0_init=cache[1])
                    cap_row["sc"] = sc
                else:
                    cap_row = r_hi
                    cap_row["sc"] = float(s_test[idx])
                break
        return {
            "name": cl["name"],
            "beta": cl["beta"],
            "fbar500": cl["fbar500"],
            "R500_pureMOND": float(Rm5),
            "R200_pureMOND": float(Rm2),
            "static_converged": False,
            "capped_converged": bool(cap_row is not None),
            "R500_capped": cap_row["R500"] if cap_row else None,
            "R200_capped": cap_row["R200"] if cap_row else None,
            "mu_scale_cap": cap_row["sc"] if cap_row else None,
            "max_dS": float(cap_row["max_dS"]) if cap_row else None,
            "fd_resid": float(cap_row["fd_resid"]) if cap_row else None,
        }

    if st["dust_ratio"] > 1.0:
        cache = [st["S_arr"], st["P0"]]
        def ddiff_c(sv):
            rt = solve_cluster_smooth(cl, MU0 * sv, r_cosh, S_init=cache[0], P0_init=cache[1])
            if rt["converged"]:
                cache[0], cache[1] = rt["S_arr"], rt["P0"]
                return rt["dust_ratio"] - 1.0
            return -10.0
        sc = brentq(ddiff_c, 0.3 if math.isfinite(r_cosh) else 0.5, 1.0, xtol=1e-3)
        cp = solve_cluster_smooth(cl, MU0 * sc, r_cosh, S_init=cache[0], P0_init=cache[1])
        C5, C2 = cp["R500"], cp["R200"]
        max_dS = max(st["max_dS"], cp["max_dS"])
        fd_resid = max(st["fd_resid"], cp["fd_resid"])
        cp_conv = cp["converged"]
    else:
        sc, C5, C2 = 1.0, st["R500"], st["R200"]
        max_dS = st["max_dS"]
        fd_resid = st["fd_resid"]
        cp_conv = True

    return {
        "name": cl["name"],
        "beta": cl["beta"],
        "fbar500": cl["fbar500"],
        "R500_pureMOND": float(Rm5),
        "R200_pureMOND": float(Rm2),
        "static_converged": True,
        "capped_converged": bool(cp_conv),
        "R500_static": float(st["R500"]),
        "R200_static": float(st["R200"]),
        "dust_ratio": float(st["dust_ratio"]),
        "mu_scale_cap": float(sc),
        "S_at_R200": float(st["S_at_R200"]),
        "u_center": float(st["u_center"]),
        "max_dS": float(max_dS),
        "fd_resid": float(fd_resid),
        "max_dS_grid_jump": float(st["max_dS_grid_jump"]),
        "R500_capped": float(C5),
        "R200_capped": float(C2),
    }


def _solve_free_boundary_Phi0_task(args: tuple[dict, float]) -> dict:
    cl, r_cosh = args
    st = solve_cluster_smooth(cl, MU0, r_cosh)
    if not st["converged"]:
        return {"name": cl["name"], "converged": False}
    if st["dust_ratio"] <= 1.0:
        return {
            "name": cl["name"],
            "converged": True,
            "capped": False,
            "R500": st["R500"],
            "R200": st["R200"],
            "dust_ratio": st["dust_ratio"],
            "R_edge_over_rv": 1.0,
        }
    rr, S_arr = st["rr"], st["S_arr"]

    def excess(P0: float) -> float:
        r_fb = solve_single_bvp(cl, MU0, r_cosh, rr, S_arr, P0_hint=P0, free_Phi0=True)
        if not r_fb["converged"]:
            return +10.0
        return r_fb["dust_ratio"] - 1.0

    f_lo = excess(st["P0"])
    if f_lo <= 0.0:
        return {"name": cl["name"], "converged": False}
    P0_star = brentq(excess, st["P0"], 0.0, xtol=1e-6 * abs(st["P0"]))
    fin = solve_single_bvp(cl, MU0, r_cosh, rr, S_arr, P0_hint=P0_star, free_Phi0=True)
    if not fin["converged"]:
        return {"name": cl["name"], "converged": False}
    return {
        "name": cl["name"],
        "converged": True,
        "capped": True,
        "R500": fin["R500"],
        "R200": fin["R200"],
        "dust_ratio": fin["dust_ratio"],
        "R_edge_over_rv": fin["R_edge_over_rv"],
    }


def summarize_rows(rows: list[dict], r_str: str, mode: str) -> dict:
    r_cosh = float(r_str)
    n_st_conv = int(sum(r["static_converged"] for r in rows))
    n_cp_conv = int(sum(r["capped_converged"] for r in rows))

    def stat_block(key: str):
        vals = [r[key] for r in rows if r.get(key) is not None]
        if not vals:
            return {"n_conv": 0, "median": None, "n_in_0.7_1.4": 0}
        return {
            "n_conv": len(vals),
            "median": float(np.median(vals)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals)),
            "n_in_0.7_1.4": int(sum(0.7 <= v <= 1.4 for v in vals)),
        }

    summ = {
        "r_cosh": r_str,
        "mode": mode,
        "in_D5_window": bool(r_str == "inf" or (2.5e-8 < r_cosh <= 2e-2)),
        "n_static_converged": n_st_conv,
        "n_capped_converged": n_cp_conv,
        "R500_static": stat_block("R500_static"),
        "R200_static": stat_block("R200_static"),
        "R500_capped": stat_block("R500_capped"),
        "R200_capped": stat_block("R200_capped"),
    }
    dusts = [r["dust_ratio"] for r in rows if r.get("dust_ratio") is not None]
    summ["median_dust_ratio"] = float(np.median(dusts)) if dusts else None
    summ["n_dust_exceeds"] = int(sum(d > 1.0 for d in dusts)) if dusts else None
    summ["max_dS_across_sample"] = float(max((r["max_dS"] for r in rows if r.get("max_dS") is not None), default=0.0))
    fds = [r["fd_resid"] for r in rows if r.get("fd_resid") is not None]
    if fds:
        summ["max_fd_resid_across_sample"] = float(max(fds))

    r5c, r2c = summ["R500_capped"], summ["R200_capped"]
    pass_all = (
        n_cp_conv == len(rows)
        and summ["in_D5_window"]
        and r5c["median"] is not None and 0.80 <= r5c["median"] <= 1.25 and r5c["n_in_0.7_1.4"] >= 9
        and r2c["median"] is not None and 0.80 <= r2c["median"] <= 1.25 and r2c["n_in_0.7_1.4"] >= 9
    )
    summ["prereg_pass_capped"] = bool(pass_all)
    summ["all_static_converged"] = bool(n_st_conv == len(rows))
    summ["verdict"] = (
        "PASS (CLOSES)"
        if (pass_all and n_st_conv == len(rows))
        else ("PASS_CAPPED_STATIC_COLLAPSED" if pass_all else "FAILS")
    )
    return {"summary": summ, "rows": rows, "xH_low": XHLOW}


def dop853_crosscheck(clusters: list[dict], r_str: str) -> dict:
    """Independent DOP853 rtol=1e-8 N=400 deg-14 cross-check on 3 representative clusters."""
    r_cosh = float(r_str)
    names = ("A1644", "A2029", "A3266")
    sub = [cl for cl in clusters if cl["name"] in names]
    diffs = []
    details = {}
    for cl in sub:
        rk = solve_cluster_smooth(cl, MU0, r_cosh)
        dp = solve_cluster_smooth(cl, MU0, r_cosh, N_grid=400, poly_deg=14, ode_method="DOP853", ode_rtol=1e-8)
        if rk["converged"] and dp["converged"]:
            d5 = abs(rk["R500"] - dp["R500"]) / dp["R500"]
            d2 = abs(rk["R200"] - dp["R200"]) / dp["R200"]
            diffs.extend([d5, d2])
            details[cl["name"]] = {"rk_R500_R200": [rk["R500"], rk["R200"]], "dp_R500_R200": [dp["R500"], dp["R200"]], "rel_diff": [d5, d2]}
        else:
            details[cl["name"]] = {"rk_conv": rk["converged"], "dp_conv": dp["converged"]}
    return {"r_cosh": r_str, "max_rel_diff_vs_DOP853_N400": float(max(diffs)) if diffs else None, "details": details}


def main() -> int:
    t_start = time.time()
    clusters = load_xcop()
    n_workers = min(8, os.cpu_count() or 4)
    print(f"Loaded {len(clusters)} X-COP clusters, workers={n_workers}", flush=True)

    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        print("=== CONTROL AUDIT at r = inf ===", flush=True)
        rows_testc = list(pool.map(_solve_testc_exact_cluster, clusters))
        ctrl_testc = summarize_rows(rows_testc, "inf", "testc_exact")

        rows_smooth_inf = list(pool.map(_run_smooth_cluster_task, [(cl, float("inf")) for cl in clusters]))
        ctrl_smooth = summarize_rows(rows_smooth_inf, "inf", "smooth_phi")

        a16_tc = next(r for r in ctrl_testc["rows"] if r["name"] == "A1644")
        a16_sm = next(r for r in ctrl_smooth["rows"] if r["name"] == "A1644")
        print(
            f"  Test C (#257 verbatim): R500_cap={ctrl_testc['summary']['R500_capped']['median']:.4f} "
            f"({ctrl_testc['summary']['R500_capped']['n_in_0.7_1.4']}/12), "
            f"R200_cap={ctrl_testc['summary']['R200_capped']['median']:.4f} "
            f"({ctrl_testc['summary']['R200_capped']['n_in_0.7_1.4']}/12), "
            f"max_dS={ctrl_testc['summary']['max_dS_across_sample']:.3f}, "
            f"A1644 R200={a16_tc['R200_capped']:.3f} (jump {a16_tc['max_dS_grid_jump']:.3f})",
            flush=True,
        )
        print(
            f"  Smooth-Phi (deg-14 poly, max_dS<1e-4): R500_cap={ctrl_smooth['summary']['R500_capped']['median']:.4f} "
            f"({ctrl_smooth['summary']['R500_capped']['n_in_0.7_1.4']}/12), "
            f"R200_cap={ctrl_smooth['summary']['R200_capped']['median']:.4f} "
            f"({ctrl_smooth['summary']['R200_capped']['n_in_0.7_1.4']}/12), "
            f"max_dS={ctrl_smooth['summary']['max_dS_across_sample']:.1e}, "
            f"max_fd_resid={ctrl_smooth['summary']['max_fd_resid_across_sample']:.2e}, "
            f"A1644 R200={a16_sm['R200_capped']:.3f}",
            flush=True,
        )

        with open(os.path.join(HERE, "XCOP_COSH_inf.json"), "w") as f:
            json.dump(ctrl_smooth, f, indent=1)

        grid_summaries = {"inf_testc_repro": ctrl_testc["summary"], "inf_smooth": ctrl_smooth["summary"]}
        print("\n=== PRE-REGISTERED COSH GRID (smooth_phi, max_dS < 1e-4) ===", flush=True)
        for r_str in PREG_GRID:
            if r_str == "inf":
                res = ctrl_smooth
            else:
                r_cosh = float(r_str)
                rows_r = list(pool.map(_run_smooth_cluster_task, [(cl, r_cosh) for cl in clusters]))
                res = summarize_rows(rows_r, r_str, "smooth_phi")
                with open(os.path.join(HERE, f"XCOP_COSH_{r_str}.json"), "w") as f:
                    json.dump(res, f, indent=1)
            grid_summaries[r_str] = res["summary"]
            s = res["summary"]
            r5s, r2s = s["R500_capped"], s["R200_capped"]
            r5m = f"{r5s['median']:.3f}" if r5s["median"] is not None else "None"
            r2m = f"{r2s['median']:.3f}" if r2s["median"] is not None else "None"
            fdm = s.get("max_fd_resid_across_sample")
            fd_txt = f"{fdm:.2e}" if fdm is not None else "None"
            print(
                f"  r={r_str:<5} st_conv={s['n_static_converged']:2d}/12 cp_conv={s['n_capped_converged']:2d}/12 | "
                f"R500_cap={r5m} ({r5s['n_in_0.7_1.4']:2d}/12) R200_cap={r2m} ({r2s['n_in_0.7_1.4']:2d}/12) | "
                f"med_dust={s['median_dust_ratio']} fd_res={fd_txt} -> {s['verdict']}",
                flush=True,
            )

        passing_finite = [
            r_str for r_str in PREG_GRID if r_str != "inf" and grid_summaries[r_str].get("prereg_pass_capped")
        ]
        xchecks = {}
        for r_str in passing_finite:
            xchecks[r_str] = dop853_crosscheck(clusters, r_str)
            print(f"\n=== DOP853 N=400 CROSS-CHECK at r={r_str}: max_rel_diff={xchecks[r_str]['max_rel_diff_vs_DOP853_N400']} ===", flush=True)

        diag_r = ["1e-4", "3e-5", "1e-5"]
        for r_str in passing_finite:
            if r_str not in diag_r:
                diag_r.append(r_str)

        fb_diag = {}
        print("\n=== SECONDARY DIAGNOSTIC: Fixed-mu Free-Boundary Phi0 Cap ===", flush=True)
        for r_str in diag_r:
            r_cosh = float(r_str)
            fb_rows = list(pool.map(_solve_free_boundary_Phi0_task, [(cl, r_cosh) for cl in clusters]))
            conv = [r for r in fb_rows if r["converged"]]
            if len(conv) == len(clusters):
                r5_vals = [r["R500"] for r in conv]
                r2_vals = [r["R200"] for r in conv]
                fb_diag[r_str] = {
                    "n_conv": len(conv),
                    "R500_median": float(np.median(r5_vals)),
                    "R500_in_0.7_1.4": int(sum(0.7 <= v <= 1.4 for v in r5_vals)),
                    "R200_median": float(np.median(r2_vals)),
                    "R200_in_0.7_1.4": int(sum(0.7 <= v <= 1.4 for v in r2_vals)),
                    "rows": fb_rows,
                }
                print(
                    f"  free-Phi0 r={r_str}: R500={fb_diag[r_str]['R500_median']:.3f} "
                    f"({fb_diag[r_str]['R500_in_0.7_1.4']}/12), "
                    f"R200={fb_diag[r_str]['R200_median']:.3f} ({fb_diag[r_str]['R200_in_0.7_1.4']}/12)",
                    flush=True,
                )
            else:
                fb_diag[r_str] = {"n_conv": len(conv), "rows": fb_rows}
                print(f"  free-Phi0 r={r_str}: converged={len(conv)}/12", flush=True)

    summary_out = {
        "prereg_commit": "29b64d1a",
        "control_audit": {
            "testc_exact_repro": ctrl_testc["summary"],
            "smooth_phi_inf": ctrl_smooth["summary"],
            "sawtooth_delta_R200_capped": float(ctrl_smooth["summary"]["R200_capped"]["median"] - ctrl_testc["summary"]["R200_capped"]["median"]),
            "sawtooth_delta_R200_static": float(ctrl_smooth["summary"]["R200_static"]["median"] - ctrl_testc["summary"]["R200_static"]["median"]),
            "A1644_sawtooth_R200_testc_vs_smooth": [a16_tc["R200_capped"], a16_sm["R200_capped"]],
        },
        "grid_summaries": grid_summaries,
        "dop853_crosschecks": xchecks,
        "secondary_free_boundary_Phi0_diagnostic": fb_diag,
        "elapsed_seconds": float(time.time() - t_start),
    }
    with open(os.path.join(HERE, "XCOP_COSH_SUMMARY.json"), "w") as f:
        json.dump(summary_out, f, indent=1)
    print(f"\nCompleted Track 1 in {summary_out['elapsed_seconds']:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
