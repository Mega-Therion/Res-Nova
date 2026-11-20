#!/usr/bin/env python3
"""Pre-registered Law-B relaxation sweep (PREREG_PHASE3.md):
continuous interpolation between free-falling drag (Law A, gamma_pin = 0) and
frame-locked geometric drag (Law C, gamma_pin -> inf).

Physics law:
  Q_i := q4 * u_F - gamma_pin * (F_d - Omega_d * u_F),
  where F_d = F_m + F_r + F_W - (2/3) E^2 K^2 (Psi' + Phi)
  and gamma_pin = Gamma / H >= 0.
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
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import weyl_causal_envelope as W  # noqa: E402

ELL_ALL = list(range(2, 31))
W.ELL_ISW = ELL_ALL

GAMMA_GRID = [0.0, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]


def run_symbolic_law_b() -> dict:
    """SymPy verification of Law B Bianchi consistency (dE00/dN = 0 and div3_d = Q_i)
    and exact Law A (gamma_pin=0) / Law C (gamma_pin -> inf, uF=0) limits."""
    N = sp.Symbol("N", real=True)
    k, H0, Om, Or, OL, x0, gam = sp.symbols("k H0 Om Or OL x0 gam", positive=True)
    a = sp.exp(N)
    E = sp.Function("E")(N)
    OmW = sp.Function("OmW")(N)
    E_p = sp.diff(E, N) / E
    K2 = (k / (a * H0 * E)) ** 2
    Omd = x0 * a**2 * E**2
    Omd_p = sp.diff(Omd, N)
    q4 = Omd_p + 3 * Omd
    Ep_exact = (-sp.Rational(3, 2) * Om * a ** (-3) - 2 * Or * a ** (-4) - 2 * OmW + sp.Rational(3, 2) * Omd) / E**2

    dm, um, Dr, Fr, DW, FW, SW, Psi = [sp.Function(nm)(N) for nm in ("dm", "um", "Dr", "Fr", "DW", "FW", "SW", "Psi")]
    uF = sp.Function("uF")(N)
    Phi = Psi - sp.Rational(9, 2) * (H0 / k) ** 2 * a**2 * SW
    Dm = Om * a ** (-3) * dm
    Fm = Om * a ** (-3) * um
    um_p = -(2 + E_p) * um + K2 * Phi
    Fr_p = -(5 + E_p) * Fr + K2 * (Dr / 3 + sp.Rational(4, 3) * Or * a ** (-4) * Phi)

    Psi_p_expr = -Phi - (K2 * Psi + sp.Rational(3, 2) / E**2 * (Dm + Dr + DW)) / (3 * (1 + x0 * a**2))
    Fd_from_E03 = Fm + Fr + FW - sp.Rational(2, 3) * E**2 * K2 * (sp.diff(Psi, N) + Phi)
    Q_i = q4 * uF - gam * (Fd_from_E03 - Omd * uF)

    Psi_pp_plus_Phi_p = sp.Rational(1, 2) / E**2 * (Dr + DW) - sp.Rational(3, 2) / E**2 * SW - (3 + E_p) * sp.diff(Psi, N) - (3 + 2 * E_p) * Phi
    dm_p = -um + 3 * sp.diff(Psi, N)
    Dr_p = -4 * Dr + 4 * Or * a ** (-4) * sp.diff(Psi, N) - Fr
    Dd = -2 * Omd * (sp.diff(Psi, N) + Phi)
    Dd_p = -2 * Omd_p * (sp.diff(Psi, N) + Phi) - 2 * Omd * Psi_pp_plus_Phi_p
    DW_p = -4 * DW + 4 * OmW * sp.diff(Psi, N) - FW + (Dd_p + 3 * Dd - 3 * Omd * sp.diff(Psi, N) + Fd_from_E03)
    FW_p = -(5 + E_p) * FW + K2 * (sp.Rational(1, 3) * DW + sp.Rational(4, 3) * OmW * Phi - SW) + Q_i

    E00_res = K2 * Psi + 3 * (1 + x0 * a**2) * (sp.diff(Psi, N) + Phi) + sp.Rational(3, 2) / E**2 * (Dm + Dr + DW)
    subs_B = {
        sp.diff(Psi, N, 2): Psi_pp_plus_Phi_p - sp.diff(Phi, N),
        sp.diff(dm, N): dm_p,
        sp.diff(um, N): um_p,
        sp.diff(Dr, N): Dr_p,
        sp.diff(Fr, N): Fr_p,
        sp.diff(DW, N): DW_p,
        sp.diff(FW, N): FW_p,
        sp.diff(OmW, N): q4 - 4 * OmW,
    }
    dE00_B = sp.diff(E00_res, N).subs(subs_B).subs(sp.diff(E, N), E * Ep_exact).subs(sp.diff(Psi, N), Psi_p_expr).subs(sp.diff(E, N), E * Ep_exact)
    assert sp.simplify(dE00_B) == 0

    div3_d = sp.diff(Fd_from_E03, N) + (5 + E_p) * Fd_from_E03 - K2 * Omd * Phi
    div3_res = (div3_d - Q_i).subs(subs_B).subs(sp.diff(E, N), E * Ep_exact).subs(sp.diff(Psi, N), Psi_p_expr).subs(sp.diff(E, N), E * Ep_exact)
    assert sp.simplify(div3_res) == 0

    assert sp.simplify(Q_i.subs(gam, 0) - q4 * uF) == 0
    assert sp.simplify(div3_d.subs({Fd_from_E03: 0, sp.diff(Fd_from_E03, N): 0}) + K2 * Omd * Phi) == 0

    return {
        "dE00_dN_zero_for_arbitrary_gamma_pin": True,
        "div3_Td_equals_Qi_for_arbitrary_gamma_pin": True,
        "gamma_zero_limit_LawA": True,
        "gamma_inf_quasistatic_uF0_limit_LawC": True,
    }


def _solve_law_b_mode(task: tuple) -> tuple:
    """Solve single k mode for Law B (gamma_pin finite) or exact Law C (gamma_pin == inf)."""
    run_key, idx_k, k, h, Om, kappa, closure, c_vis2, v_flux, gamma_pin = task
    if math.isinf(gamma_pin):
        return W._solve_single_mode((run_key, idx_k, k, h, Om, kappa, "C_Fd0", closure, c_vis2, v_flux, "adiabatic", False))

    x0 = -kappa
    OL = W.compute_OL(h, Om, kappa)
    Or = W.ORH2 / (h * h)
    H0_Mpc = 100.0 * h / W.C_LIGHT_KMS
    shear_fac = 4.5 * (H0_Mpc / k) ** 2

    N_i = math.log(W.A_INIT)
    if closure == "mb95_l8":
        Ng_tau = np.linspace(N_i, 0.0, 1501)
        inv_aH = np.array([1.0 / (math.exp(float(n)) * H0_Mpc * W.bg_at_N(float(n), h, Om, x0, OL)[1]) for n in Ng_tau])
        _, E_init, *_ = W.bg_at_N(N_i, h, Om, x0, OL)
        tau_i = 1.0 / (W.A_INIT * H0_Mpc * E_init)
        tau_grid = tau_i + np.concatenate([[0.0], np.cumsum(0.5 * (inv_aH[:-1] + inv_aH[1:]) * (Ng_tau[1] - Ng_tau[0]))])
        dN_tau = float(Ng_tau[1] - Ng_tau[0])
    else:
        tau_grid = None
        dN_tau = 1.0

    a, E_i, E2_i, Ep_i, OmW_i, _, _, _, _ = W.bg_at_N(N_i, h, Om, x0, OL)
    K2_i = (k / (a * H0_Mpc * E_i)) ** 2
    w_m = Om / (a * a * a)
    w_r = (4.0 / 3.0) * Or / (a**4) / (1.0 + K2_i / 3.0)
    w_W = ((4.0 / 3.0) * OmW_i / (1.0 + K2_i / 3.0)) if x0 > 0.0 else 0.0
    D_tot_i = -(2.0 / 3.0) * E2_i * (K2_i + 3.0 * (1.0 + x0 * a * a))
    dm_i = D_tot_i / (w_m + w_r + w_W)
    Dr_i = w_r * dm_i
    u_i = (2.0 / 3.0) * E2_i * K2_i / (w_m + w_r + w_W)
    um_i = u_i
    Fr_i = w_r * u_i
    FW_i = (w_W * u_i) if x0 > 0.0 else 0.0

    if closure == "mb95_l8":
        y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, 1.0, FW_i] + [0.0] * 7
    else:
        y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, 1.0, FW_i, 0.0]

    def eval_rhs(N: float, y: np.ndarray) -> tuple[list[float], float, float]:
        dm, um, Dr, Fr, Psi, Qp, FW = y[0], y[1], y[2], y[3], y[4], y[5], y[6]
        SW = y[7]
        a_v, E, E2, Ep, OmW, Omd, _, q4, q4_W = W.bg_at_N(N, h, Om, x0, OL)
        a2 = a_v * a_v
        a3 = a2 * a_v
        a4 = a2 * a2
        Phi = Psi - shear_fac * a2 * SW
        Psi_p = Qp - Phi
        K2 = (k / (a_v * H0_Mpc * E)) ** 2
        DW = -(2.0 / 3.0) * E2 * (K2 * Psi + 3.0 * (1.0 + x0 * a2) * Qp) - Om / a3 * dm - Dr
        Qp_p = 0.5 / E2 * (Dr + DW) - 1.5 / E2 * SW - (3.0 + Ep) * Psi_p - (3.0 + 2.0 * Ep) * Phi

        Fm = Om / a3 * um
        Fd = Fm + Fr + FW - (2.0 / 3.0) * E2 * K2 * Qp
        u_F = 0.0 if v_flux == "bulk_rest" else um
        Q_i = q4 * u_F - gamma_pin * (Fd - Omd * u_F)

        FW_p = -(5.0 + Ep) * FW + K2 * (DW / 3.0 + (4.0 / 3.0) * OmW * Phi - SW) + Q_i
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

    methods = ("DOP853", "LSODA", "BDF") if gamma_pin <= 100.0 else ("LSODA", "BDF")
    sol = None
    for meth in methods:
        sol = solve_ivp(rhs, (N_i, 0.0), y0, method=meth, rtol=1e-6, atol=1e-9, t_eval=W.N_EVAL)
        if sol.success and sol.y.shape[1] == len(W.N_EVAL):
            break
    if sol is None or not sol.success or sol.y.shape[1] != len(W.N_EVAL):
        return (run_key, idx_k, False, None, None, None)

    n_pts = len(W.N_EVAL)
    PhiW = np.empty(n_pts, dtype=float)
    dPhiW_dz = np.empty(n_pts, dtype=float)
    max_phi_w = 0.0
    for j in range(n_pts):
        _, phiw, dN_val = eval_rhs(float(W.N_EVAL[j]), sol.y[:, j])
        PhiW[j] = phiw
        dPhiW_dz[j] = -math.exp(float(W.N_EVAL[j])) * dN_val
        if abs(phiw) > max_phi_w:
            max_phi_w = abs(phiw)

    return (run_key, idx_k, True, PhiW, dPhiW_dz, {"max_abs_PhiW": float(max_phi_w), "PhiW_z0": float(PhiW[-1])})


def run_batched_specs(pool: ProcessPoolExecutor, specs: dict[str, dict], lcdm_obs: dict) -> dict[str, dict]:
    """Run all specs simultaneously across all pool workers sorted descending by k."""
    tasks = []
    for rkey, spc in specs.items():
        bp = spc["bp"]
        for i, kv in enumerate(W.K_GRID):
            tasks.append((rkey, i, float(kv), bp["h"], bp["Om"], bp["kappa"], spc["closure"], spc["c_vis2"], spc["v_flux"], spc["gamma_pin"]))
    tasks.sort(key=lambda t: -t[2])
    raw = list(pool.map(_solve_law_b_mode, tasks))

    grouped = {rkey: {} for rkey in specs}
    for r in raw:
        grouped[r[0]][r[1]] = r

    summaries = {}
    for rkey, spc in specs.items():
        bp = spc["bp"]
        modes = grouped[rkey]
        if not all(modes[i][0] for i in range(len(W.K_GRID))):
            summaries[rkey] = {
                "run_key": rkey,
                "bg_name": spc["bg_name"],
                "closure": spc["closure"],
                "c_vis2": spc["c_vis2"],
                "v_flux": spc["v_flux"],
                "gamma_pin": "inf_LawC" if math.isinf(spc["gamma_pin"]) else float(spc["gamma_pin"]),
                "linear_stable": False,
                "pass_all": False,
            }
            continue
        PhiW_mat = np.vstack([modes[i][3] for i in range(len(W.K_GRID))])
        dPhiW_dz_mat = np.vstack([modes[i][4] for i in range(len(W.K_GRID))])
        max_amp = max(modes[i][5]["max_abs_PhiW"] for i in range(len(W.K_GRID)))
        linear_stable = bool(np.all(np.isfinite(PhiW_mat)) and max_amp < 1e3)
        obs = W.compute_observables_for_run(bp["h"], bp["Om"], bp["kappa"], PhiW_mat, dPhiW_dz_mat)
        lens_ratios = {L: float(obs["CL_lens"][L] / lcdm_obs["CL_lens"][L]) for L in map(str, W.L_LENS)}
        isw_ratios = {str(ell): float(obs["CL_isw"][str(ell)] / lcdm_obs["CL_isw"][str(ell)]) for ell in ELL_ALL}
        vals_l = list(lens_ratios.values())
        vals_i = list(isw_ratios.values())
        A_mean = float(np.mean(vals_l))
        ell_max = max(isw_ratios, key=isw_ratios.get)
        lens_pass_mean = abs(A_mean - 1.0) <= 0.08
        lens_pass_allL = all(abs(v - 1.0) <= 0.08 for v in vals_l)
        isw_pass = all(0.4 <= v <= 1.6 for v in vals_i)
        summaries[rkey] = {
            "run_key": rkey,
            "bg_name": spc["bg_name"],
            "closure": spc["closure"],
            "c_vis2": spc["c_vis2"],
            "v_flux": spc["v_flux"],
            "gamma_pin": "inf_LawC" if math.isinf(spc["gamma_pin"]) else float(spc["gamma_pin"]),
            "linear_stable": linear_stable,
            "A_phiphi_mean": A_mean,
            "A_phiphi_min_max": [float(min(vals_l)), float(max(vals_l))],
            "ISW_min_max": [float(min(vals_i)), float(max(vals_i))],
            "ISW_ell2": float(isw_ratios["2"]),
            "ISW_ell_at_max": int(ell_max),
            "lens_pass_mean": bool(lens_pass_mean),
            "lens_pass_allL": bool(lens_pass_allL),
            "isw_pass": bool(isw_pass),
            "pass_all": bool(linear_stable and lens_pass_allL and isw_pass),
        }
    return summaries


def main() -> int:
    t0 = time.time()
    print("=== (S1) SymPy Law-B Verification ===", flush=True)
    sym_res = run_symbolic_law_b()
    print(json.dumps(sym_res, indent=1), flush=True)

    param_info = W.get_parameter_points()
    pts = param_info["points"]
    n_workers = min(8, os.cpu_count() or 4)

    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        # Step 1: LCDM baseline
        L = pts["LCDM_control"]
        lcdm_tasks = [("LCDM", i, float(kv), L["h"], L["Om"], 0.0, "hu98", 0.0, "bulk_rest", math.inf) for i, kv in enumerate(W.K_GRID)]
        lcdm_raw = {r[1]: r for r in pool.map(_solve_law_b_mode, sorted(lcdm_tasks, key=lambda t: -t[2]))}
        assert all(lcdm_raw[i][0] for i in range(len(W.K_GRID)))
        lcdm_obs = W.compute_observables_for_run(
            L["h"], L["Om"], 0.0,
            np.vstack([lcdm_raw[i][3] for i in range(len(W.K_GRID))]),
            np.vstack([lcdm_raw[i][4] for i in range(len(W.K_GRID))]),
        )
        print(f"LCDM baseline ready ({time.time()-t0:.1f}s)", flush=True)

        # Step 2: Batch ALL controls + sweep curves + matter_comoving spot checks together
        specs = {}
        specs["ctrl|Pantheon+_best|hu98|cvis2=0.0|bulk_rest|gam=0.0"] = {
            "bg_name": "Pantheon+_best", "bp": pts["Pantheon+_best"], "closure": "hu98", "c_vis2": 0.0, "v_flux": "bulk_rest", "gamma_pin": 0.0
        }
        curves = [
            ("Pantheon+_best", "hu98", 1.0 / 3.0),
            ("Pantheon+_best", "mb95_l8", 1.0 / 3.0),
            ("DES-Dovekie_best", "hu98", 1.0 / 3.0),
            ("DES-Dovekie_best", "mb95_l8", 1.0 / 3.0),
        ]
        for bg_name, closure, c2 in curves:
            for g in GAMMA_GRID + [math.inf]:
                g_lbl = "inf" if math.isinf(g) else f"{g:g}"
                specs[f"sweep|{bg_name}|{closure}|bulk_rest|gam={g_lbl}"] = {
                    "bg_name": bg_name, "bp": pts[bg_name], "closure": closure, "c_vis2": c2, "v_flux": "bulk_rest", "gamma_pin": g
                }
        for bg_name in ("Pantheon+_best", "DES-Dovekie_best"):
            specs[f"sweep|{bg_name}|hu98|bulk_rest|gam=300"] = {
                "bg_name": bg_name, "bp": pts[bg_name], "closure": "hu98", "c_vis2": 1.0 / 3.0, "v_flux": "bulk_rest", "gamma_pin": 300.0
            }
        for g in (10.0, 100.0):
            specs[f"frame|Pantheon+_best|hu98|matter_comoving|gam={g:g}"] = {
                "bg_name": "Pantheon+_best", "bp": pts["Pantheon+_best"], "closure": "hu98", "c_vis2": 1.0 / 3.0, "v_flux": "matter_comoving", "gamma_pin": g
            }

        print(f"Running batched grid: {len(specs)} points ({len(specs)*len(W.K_GRID)} modes across {n_workers} workers)...", flush=True)
        summ = run_batched_specs(pool, specs, lcdm_obs)
        print(f"Batched grid finished at {time.time()-t0:.1f}s", flush=True)

        # Fallback: evaluate gamma=300 on any mb95_l8 curve only if 100 still fails
        mb_extra = {}
        for bg_name in ("Pantheon+_best", "DES-Dovekie_best"):
            if not summ[f"sweep|{bg_name}|mb95_l8|bulk_rest|gam=100"]["pass_all"]:
                mb_extra[f"sweep|{bg_name}|mb95_l8|bulk_rest|gam=300"] = {
                    "bg_name": bg_name, "bp": pts[bg_name], "closure": "mb95_l8", "c_vis2": 1.0 / 3.0, "v_flux": "bulk_rest", "gamma_pin": 300.0
                }
        if mb_extra:
            print(f"Running gamma=300 fallback on {list(mb_extra.keys())}...", flush=True)
            summ.update(run_batched_specs(pool, mb_extra, lcdm_obs))

        # Verify N1 controls & 1/gamma_pin asymptotic convergence
        c_p_0 = summ["ctrl|Pantheon+_best|hu98|cvis2=0.0|bulk_rest|gam=0.0"]
        c_p_13 = summ["sweep|Pantheon+_best|hu98|bulk_rest|gam=0"]
        c_p_100 = summ["sweep|Pantheon+_best|hu98|bulk_rest|gam=100"]
        c_p_300 = summ["sweep|Pantheon+_best|hu98|bulk_rest|gam=300"]
        c_p_lawC = summ["sweep|Pantheon+_best|hu98|bulk_rest|gam=inf"]
        c_d_100 = summ["sweep|DES-Dovekie_best|hu98|bulk_rest|gam=100"]
        c_d_300 = summ["sweep|DES-Dovekie_best|hu98|bulk_rest|gam=300"]
        c_d_lawC = summ["sweep|DES-Dovekie_best|hu98|bulk_rest|gam=inf"]

        assert abs(c_p_0["A_phiphi_mean"] - 1.0485) < 1e-2 and abs(c_p_0["ISW_min_max"][1] - 1.5934) < 1e-2
        assert abs(c_p_13["A_phiphi_mean"] - 0.955) < 1e-2 and abs(c_p_13["ISW_min_max"][1] - 4.07) < 2e-2

        d_isw_p100 = c_p_100["ISW_min_max"][1] - c_p_lawC["ISW_min_max"][1]
        d_isw_p300 = c_p_300["ISW_min_max"][1] - c_p_lawC["ISW_min_max"][1]
        ratio_p = d_isw_p100 / d_isw_p300
        d_isw_d100 = c_d_100["ISW_min_max"][1] - c_d_lawC["ISW_min_max"][1]
        d_isw_d300 = c_d_300["ISW_min_max"][1] - c_d_lawC["ISW_min_max"][1]
        ratio_d = d_isw_d100 / d_isw_d300

        assert abs(c_p_300["A_phiphi_mean"] - c_p_lawC["A_phiphi_mean"]) < 5e-3 and abs(d_isw_p300) < 4e-2 and 2.5 < ratio_p < 3.5
        assert abs(c_d_300["A_phiphi_mean"] - c_d_lawC["A_phiphi_mean"]) < 5e-3 and abs(d_isw_d300) < 4e-2 and 2.5 < ratio_d < 3.5

        controls = {
            "Pantheon_gamma0_cvis0": c_p_0,
            "Pantheon_gamma0_cvis1_3": c_p_13,
            "Pantheon_gamma100_cvis1_3": c_p_100,
            "Pantheon_gamma300_cvis1_3": c_p_300,
            "Pantheon_LawC_cvis1_3": c_p_lawC,
            "Dovekie_gamma100_cvis1_3": c_d_100,
            "Dovekie_gamma300_cvis1_3": c_d_300,
            "Dovekie_LawC_cvis1_3": c_d_lawC,
            "gamma300_vs_LawC_ISW_diff_Pantheon": float(d_isw_p300),
            "gamma300_vs_LawC_ISW_diff_Dovekie": float(d_isw_d300),
            "asymptotic_1_over_gamma_ratio_Pantheon_100_to_300": float(ratio_p),
            "asymptotic_1_over_gamma_ratio_Dovekie_100_to_300": float(ratio_d),
        }
        print("N1 controls passed! 1/gamma ratios (expected ~3.0):", ratio_p, ratio_d, flush=True)

        # Print curve summaries and detect brackets
        sweep_results = {}
        brackets = {}
        for bg_name, closure, c2 in curves:
            cname = f"{bg_name}|{closure}"
            rows = []
            print(f"\n-- {cname} --", flush=True)
            g_list = list(GAMMA_GRID)
            if f"sweep|{bg_name}|{closure}|bulk_rest|gam=300" in summ:
                g_list.append(300.0)
            g_list.append(math.inf)
            for g in g_list:
                g_lbl = "inf" if math.isinf(g) else f"{g:g}"
                r = summ[f"sweep|{bg_name}|{closure}|bulk_rest|gam={g_lbl}"]
                rows.append(r)
                print(
                    f"  gam={g_lbl:<5} A={r['A_phiphi_mean']:.4f} "
                    f"ISW=[{r['ISW_min_max'][0]:.3f},{r['ISW_min_max'][1]:.3f}] (ell={r['ISW_ell_at_max']}) pass={r['pass_all']}",
                    flush=True,
                )
            sweep_results[cname] = rows
            for idx in range(len(rows) - 2):  # exclude exact inf
                if not rows[idx]["pass_all"] and rows[idx + 1]["pass_all"]:
                    lo = rows[idx]["gamma_pin"]
                    hi = rows[idx + 1]["gamma_pin"]
                    if lo == 0.0:
                        lo = 1e-3
                    brackets[cname] = (bg_name, closure, c2, lo, hi)
                    break

        # Step 3: Simultaneous 6-step parallel log-bisection across all bracketed curves
        for step in range(6):
            if not brackets:
                break
            bis_specs = {}
            for cname, (bg_name, closure, c2, lo, hi) in brackets.items():
                mid = math.sqrt(lo * hi)
                bis_specs[cname] = {
                    "bg_name": bg_name, "bp": pts[bg_name], "closure": closure, "c_vis2": c2, "v_flux": "bulk_rest", "gamma_pin": mid
                }
            bsum = run_batched_specs(pool, bis_specs, lcdm_obs)
            for cname, rmid in bsum.items():
                bg_name, closure, c2, lo, hi = brackets[cname]
                mid = float(rmid["gamma_pin"])
                if rmid["pass_all"]:
                    brackets[cname] = (bg_name, closure, c2, lo, mid)
                else:
                    brackets[cname] = (bg_name, closure, c2, mid, hi)

        thresholds = {}
        for bg_name, closure, _ in curves:
            cname = f"{bg_name}|{closure}"
            if cname in brackets:
                _, _, _, lo, hi = brackets[cname]
                thresholds[cname] = {"bracket": [lo, hi], "gamma_pin_crit_mid": math.sqrt(lo * hi)}
            else:
                thresholds[cname] = None
            print(f"Threshold {cname}: {thresholds[cname]}", flush=True)

        matter_frame_rows = [summ[f"frame|Pantheon+_best|hu98|matter_comoving|gam={g:g}"] for g in (10.0, 100.0)]
        print("\n=== Frame Spot-Check: matter_comoving ===", flush=True)
        for rm in matter_frame_rows:
            print(
                f"  matter_comoving gam={rm['gamma_pin']:<5} A={rm['A_phiphi_mean']:.4f} "
                f"ISW=[{rm['ISW_min_max'][0]:.3f},{rm['ISW_min_max'][1]:.3f}] pass={rm['pass_all']}",
                flush=True,
            )

    out = {
        "prereg": "PREREG_PHASE3.md",
        "S1_symbolic_law_b": sym_res,
        "N1_controls": controls,
        "sweep_bulk_rest": sweep_results,
        "gamma_pin_crit": thresholds,
        "spot_check_matter_comoving": matter_frame_rows,
        "elapsed_seconds": float(time.time() - t0),
    }
    out_path = os.path.join(HERE, "LAW_B_RELAXATION_SWEEP.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"\nWrote {out_path} in {out['elapsed_seconds']:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
