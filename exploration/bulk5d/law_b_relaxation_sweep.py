#!/usr/bin/env python3
"""Phase 3 Test L (PREREG_PHASE3.md): Law-B pinning sweep between Law A (gamma = 0) and Law C (gamma -> inf).

Law A equations of weyl_causal_envelope.py plus drag-momentum relaxation at rate gamma per e-fold, with the dark-bubble
sign (P0: the Weyl fluid gains what the wall gains):  F_W' -> F_W' - gamma F_d,
F_d = F_m + F_r + F_W - (2/3) E^2 K^2 (Psi' + Phi)  (0i constraint; Psi' + Phi = Qp).
gamma = 0 is Law A; gamma -> inf forces F_d -> 0 and turns the F_W equation into Law C's."""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from concurrent.futures import ProcessPoolExecutor
from scipy.integrate import cumulative_trapezoid, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "drag_gcosmo"))
import weyl_causal_envelope as W  # noqa: E402

W.ELL_ISW = list(range(2, 31))
_ORIG = W._solve_single_mode
GAMMAS = [0.0, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0]
CLOSURES = [("hu98", 0.1), ("hu98", 1.0 / 3.0), ("mb95_l8", 1.0 / 3.0)]
FITS = ("Pantheon+_best", "DES-Dovekie_best")


def solve_mode_B(task: tuple) -> tuple:
    run_key, idx_k, k, h, Om, kappa, law, closure, c_vis2, v_flux, ic_W, check_resid = task
    if not str(law).startswith("B:"):
        return _ORIG(task)
    gamma = float(str(law)[2:])
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
        tau_grid = tau_i + cumulative_trapezoid(inv_aH, Ng_tau, initial=0.0)
        dN_tau = float(Ng_tau[1] - Ng_tau[0])
    # constraint-satisfying adiabatic IC (as in the envelope)
    a, E_i, E2_i, Ep_i, OmW_i, _, _, _, _ = W.bg_at_N(N_i, h, Om, x0, OL)
    K2_i = (k / (a * H0_Mpc * E_i)) ** 2
    w_m = Om / (a * a * a)
    w_r = (4.0 / 3.0) * Or / (a**4) / (1.0 + K2_i / 3.0)
    w_W = ((4.0 / 3.0) * OmW_i / (1.0 + K2_i / 3.0)) if (x0 > 0.0 and ic_W == "adiabatic") else 0.0
    D_tot_i = -(2.0 / 3.0) * E2_i * (K2_i + 3.0 * (1.0 + x0 * a * a))
    dm_i = D_tot_i / (w_m + w_r + w_W)
    Dr_i = w_r * dm_i
    u_i = (2.0 / 3.0) * E2_i * K2_i / (w_m + w_r + w_W)
    um_i, Fr_i = u_i, w_r * u_i
    FW_i = (w_W * u_i) if x0 > 0.0 else 0.0
    if closure == "mb95_l8":
        y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, 1.0, FW_i] + [0.0] * 7
    else:
        y0 = [dm_i, um_i, Dr_i, Fr_i, 1.0, 1.0, FW_i, 0.0]

    def eval_rhs(N, y):
        dm, um, Dr, Fr, Psi, Qp, FW = y[0], y[1], y[2], y[3], y[4], y[5], y[6]
        SW = y[7]
        a_v, E, E2, Ep, OmW, _, _, q4, q4_W = W.bg_at_N(N, h, Om, x0, OL)
        a2 = a_v * a_v
        a3 = a2 * a_v
        a4 = a2 * a2
        Phi = Psi - shear_fac * a2 * SW
        Psi_p = Qp - Phi
        K2 = (k / (a_v * H0_Mpc * E)) ** 2
        DW = -(2.0 / 3.0) * E2 * (K2 * Psi + 3.0 * (1.0 + x0 * a2) * Qp) - Om / a3 * dm - Dr
        Qp_p = 0.5 / E2 * (Dr + DW) - 1.5 / E2 * SW - (3.0 + Ep) * Psi_p - (3.0 + 2.0 * Ep) * Phi
        u_F = 0.0 if v_flux == "bulk_rest" else um
        Fd = Om / a3 * um + Fr + FW - (2.0 / 3.0) * E2 * K2 * Qp
        FW_p = -(5.0 + Ep) * FW + K2 * (DW / 3.0 + (4.0 / 3.0) * OmW * Phi - SW) + q4 * u_F - gamma * Fd
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

    method = "DOP853" if gamma <= 300.0 else "LSODA"
    sol = solve_ivp(lambda N, y: eval_rhs(N, y)[0], (N_i, 0.0), y0, method=method, rtol=1e-7, atol=1e-10, t_eval=W.N_EVAL)
    if not sol.success or sol.y.shape[1] != len(W.N_EVAL):
        return (run_key, idx_k, False, None, None, None)
    n = len(W.N_EVAL)
    PhiW = np.empty(n)
    dPhiW_dz = np.empty(n)
    mx = 0.0
    for j in range(n):
        _, phiw, dN_val = eval_rhs(float(W.N_EVAL[j]), sol.y[:, j])
        PhiW[j] = phiw
        dPhiW_dz[j] = -math.exp(float(W.N_EVAL[j])) * dN_val
        mx = max(mx, abs(phiw))
    return (run_key, idx_k, True, PhiW, dPhiW_dz, {"max_abs_PhiW": float(mx)})


W._solve_single_mode = solve_mode_B


def main() -> int:
    pts = W.get_parameter_points()["points"]
    specs = {}
    for bg in FITS:
        for cl, c2 in CLOSURES:
            for g in GAMMAS:
                specs[f"B|{bg}|{cl}|{c2:.4f}|{g:g}"] = dict(law=f"B:{g}", bg_name=bg, closure=cl, c_vis2=c2,
                                                           v_flux="bulk_rest", ic_W="adiabatic", **pts[bg])
    NK = len(W.K_GRID)
    with ProcessPoolExecutor(max_workers=7) as pool:
        L = pts["LCDM_control"]
        t = [("LCDM", i, float(k), L["h"], L["Om"], 0.0, "C_Fd0", "hu98", 0.0, "bulk_rest", "adiabatic", False) for i, k in enumerate(W.K_GRID)]
        r = {x[1]: x for x in pool.map(solve_mode_B, t)}
        lobs = W.compute_observables_for_run(L["h"], L["Om"], 0.0, np.vstack([r[i][3] for i in range(NK)]), np.vstack([r[i][4] for i in range(NK)]))
        summ = W.build_and_run_runs(specs, pool, lobs)
    out = {}
    for key, v in summ.items():
        isw = v.get("ISW_ratio_by_ell") or {}
        if not isw:
            out[key] = {"stable": False, "pass": False}
            continue
        lens = v["A_phiphi_by_L"]
        out[key] = {"A_phiphi_mean": v["A_phiphi_mean"], "ISW_min": min(isw.values()), "ISW_max": max(isw.values()),
                    "pass": bool(all(abs(x - 1.0) <= 0.08 for x in lens.values()) and min(isw.values()) >= 0.4 and max(isw.values()) <= 1.6)}
    # controls against committed envelope runs (5 ell values there; compare on the same ell set)
    env = json.load(open(os.path.join(HERE, "..", "drag_gcosmo", "WEYL_CAUSAL_ENVELOPE.json")))["runs"]
    ctrl = {}
    for bg in FITS:
        for cl, c2 in CLOSURES:
            tagA = f"A_freefall|{bg}|hu98|cvis2={c2:.4f}|bulk_rest|adiabatic" if cl == "hu98" else f"A_freefall|{bg}|mb95_l8|bulk_rest|adiabatic"
            tagC = f"C_Fd0|{bg}|hu98|cvis2={c2:.4f}|bulk_rest|adiabatic" if cl == "hu98" else f"C_Fd0|{bg}|mb95_l8|bulk_rest|adiabatic"
            for g, tag, tol in ((0.0, tagA, 1e-3), (1000.0, tagC, 1e-2)):
                ref = env.get(tag)
                mine = summ.get(f"B|{bg}|{cl}|{c2:.4f}|{g:g}")
                if not ref or not mine or "ISW_ratio_by_ell" not in mine:
                    ctrl[f"{bg}|{cl}|{c2:.4f}|gamma={g:g}"] = {"ok": False, "why": "missing"}
                    continue
                ell5 = [str(e) for e in (2, 5, 10, 20, 30)]
                mi = max(mine["ISW_ratio_by_ell"][e] for e in ell5)
                ri = ref["ISW_ratio_min_max"][1]
                ma, ra = mine["A_phiphi_mean"], ref["A_phiphi_mean"]
                ok = abs(mi - ri) / ri <= tol and abs(ma - ra) / ra <= tol
                ctrl[f"{bg}|{cl}|{c2:.4f}|gamma={g:g}"] = {"ok": bool(ok), "ISW_max_mine": mi, "ISW_max_ref": ri, "A_mine": ma, "A_ref": ra, "tol": tol}
    gcrit = {}
    for bg in FITS:
        for cl, c2 in CLOSURES:
            passing = [g for g in GAMMAS if out[f"B|{bg}|{cl}|{c2:.4f}|{g:g}"]["pass"]]
            gcrit[f"{bg}|{cl}|{c2:.4f}"] = min(passing) if passing else None
    both = {}
    for cl, c2 in CLOSURES:
        both[f"{cl}|{c2:.4f}"] = [g for g in GAMMAS if all(out[f"B|{bg}|{cl}|{c2:.4f}|{g:g}"]["pass"] for bg in FITS)]
    res = {"controls": ctrl, "controls_all_ok": all(v.get("ok") for v in ctrl.values()), "gamma_crit": gcrit,
           "gammas_passing_both_fits": both, "grid": out}
    json.dump(res, open(os.path.join(HERE, "LAW_B_SWEEP.json"), "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("controls_all_ok", "gamma_crit", "gammas_passing_both_fits")}, indent=1))
    for k, v in ctrl.items():
        print("CTRL", k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
