#!/usr/bin/env python3
"""
Frozen profile-invariant core edge (smallest r where d ln rho_gas / d ln r = -2)
across all 12 X-COP clusters and 3 measured ICM models (2026-11-21).

PRE-REGISTRATION (frozen before running on any cluster):
  1. Core-edge invariant rule (SLOPE_TARGET = -2.0, NOT to be moved after seeing counts):
       For each of the 12 X-COP clusters and each measured ICM profile
       (M1_stacked_measured, M2_vikhlinin_CCNCC, M3_per_cluster_exact_vikhlinin),
       define r_core as the SMALLEST radius r in [1e-4 * R_500, r_v] where
           d ln(rho_gas) / d ln(r) = -2.0.
       If no root exists on that profile domain, keep r_core = R_500 and count the
       cluster as unchanged (unchanged_kept_R500 = True).
  2. Two-domain DOP853 segment solver (identical physics & solver to Gate 2 and
     nested_holographic_boundary_inheritance.py):
       - Outer boundary Phi(r_v) = 0 at r_v = R_200 * (200 / 177.8)^(1/3).
       - Universal mu_0 = 1 / (0.9895 Mpc), cosmic dust cap 5.36 * M_b(r_v)
         (reducing mu_eff <= mu_0 via brentq only if cap exceeded).
       - Interior core r <= r_core:  dW/dr = G dM_b/dr - mu^2 r^2 Phi(r),  dPhi/dr = g_MOND(W/r^2).
       - Outer infall r_core < r <= r_v:  dW/dr = G dM_b/dr,              dPhi/dr = g_MOND(W/r^2).
  3. Mandatory uniform control before scoring the new edge:
       First run r_core = R_500 across all 12 clusters x 3 models and assert exact
       reproduction of NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE.json medians
       (0.8685 / 0.8533, 0.8692 / 0.8546, 0.8669 / 0.8560) and [0.80, 1.25] counts
       (9/12, 9/12, 8/12) before running and reporting the -2.0 slope edge.
  4. Window & acceptance criterion:
       Report the change from the baseline 8/12 passing BOTH R_500 and R_200 inside
       [0.80, 1.25] across all 12 clusters, plus full per-cluster tables and both radii
       for every cluster outside [0.80, 1.25]. Never adjust the -2.0 slope afterward.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "exploration" / "d10_xcop"))
import gate2_xcop_measured_icm as g2  # noqa: E402

SLOPE_TARGET = -2.0
MODELS = (
    "M1_stacked_measured",
    "M2_vikhlinin_CCNCC",
    "M3_per_cluster_exact_vikhlinin",
)
REF_JSON_PATH = HERE / "NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE.json"


def gas_log_slope(x: float, model_tag: str, meta: dict) -> float:
    """Exact analytic d ln(rho_gas) / d ln(r) as a function of x = r / R_500."""
    xv = max(float(x), 1e-12)
    if model_tag == "M1_stacked_measured":
        lx = math.log(xv)
        sp_b = g2._STACK_SPLINES["med"]
        if lx < g2._STACK_LOGX[0]:
            return float(sp_b(g2._STACK_LOGX[0], 1))
        if lx > g2._STACK_LOGX[-1]:
            ly = g2._STACK_COLS["med"]
            return float((ly[-1] - ly[-2]) / (g2._STACK_LOGX[-1] - g2._STACK_LOGX[-2]))
        return float(sp_b(lx, 1))

    if model_tag == "M2_vikhlinin_CCNCC":
        _, ln_rc, ln_rs, al, be, ep = g2.VIKH_PARAMS[meta["cc"]]
    elif model_tag == "M3_per_cluster_exact_vikhlinin":
        _, ln_rc, ln_rs, al, be, _ = g2.VIKH_PARAMS[meta["cc"]]
        ep = meta["eps_fit"]
    else:
        raise ValueError(f"Unsupported model_tag: {model_tag}")

    rc = math.exp(ln_rc)
    rs = math.exp(ln_rs)
    u2 = (xv / rc) ** 2
    u3 = (xv / rs) ** 3
    return -0.5 * al - (3.0 * be - 0.5 * al) * (u2 / (1.0 + u2)) - 0.5 * ep * (u3 / (1.0 + u3))


def eval_shape_for_check(x: float, model_tag: str, meta: dict) -> float:
    """Gas density shape (up to constant) for finite-difference derivative verification."""
    if model_tag == "M1_stacked_measured":
        return float(g2.eval_stacked_shape(x, "med"))
    if model_tag == "M2_vikhlinin_CCNCC":
        _, ln_rc, ln_rs, al, be, ep = g2.VIKH_PARAMS[meta["cc"]]
        return float(g2.eval_vikh_shape(x, ln_rc, ln_rs, al, be, ep))
    if model_tag == "M3_per_cluster_exact_vikhlinin":
        _, ln_rc, ln_rs, al, be, _ = g2.VIKH_PARAMS[meta["cc"]]
        return float(g2.eval_vikh_shape(x, ln_rc, ln_rs, al, be, meta["eps_fit"]))
    raise ValueError(f"Unsupported model_tag: {model_tag}")


def verify_slope_derivative(model_tag: str, meta: dict) -> float:
    """Verify analytic gas_log_slope matches central finite differences on eval_*_shape."""
    eps = 1e-5
    max_err = 0.0
    for x_chk in (0.05, 0.2, 0.5, 1.0, 1.5):
        fd = math.log(
            eval_shape_for_check(x_chk * (1.0 + eps), model_tag, meta)
            / eval_shape_for_check(x_chk * (1.0 - eps), model_tag, meta)
        ) / math.log((1.0 + eps) / (1.0 - eps))
        an = gas_log_slope(x_chk, model_tag, meta)
        err = abs(an - fd)
        max_err = max(max_err, err)
        assert err < 1e-4, f"{meta['nm']} {model_tag} x={x_chk}: analytic={an} fd={fd}"
    return max_err


def find_slope_edge(model_tag: str, meta: dict, slope_target: float = SLOPE_TARGET) -> dict:
    """Find the smallest radius r in [1e-4 * R500, r_v] where d ln rho_gas / d ln r = slope_target."""
    x_min = 1e-4
    x_max = float(meta["rv"] / meta["R5"])
    xg = np.geomspace(x_min, x_max, 4000)
    vals = np.array([gas_log_slope(float(xv), model_tag, meta) - slope_target for xv in xg])

    roots = []
    for j in range(len(xg)):
        if vals[j] == 0.0:
            roots.append(float(xg[j]))
        if j + 1 < len(xg) and vals[j] * vals[j + 1] < 0.0:
            xr = float(brentq(
                lambda xx: gas_log_slope(xx, model_tag, meta) - slope_target,
                float(xg[j]),
                float(xg[j + 1]),
                xtol=1e-12,
                rtol=1e-12,
            ))
            roots.append(xr)

    # Deduplicate near-identical roots while preserving ascending radius order
    dedup = []
    for xr in sorted(roots):
        if not dedup or abs(xr - dedup[-1]) > 1e-8:
            dedup.append(xr)

    if dedup:
        x_core = dedup[0]
        r_core = x_core * meta["R5"]
        root_found = True
        unchanged = False
        slope_val = gas_log_slope(x_core, model_tag, meta)
        assert abs(slope_val - slope_target) < 1e-7
    else:
        x_core = 1.0
        r_core = float(meta["R5"])
        root_found = False
        unchanged = True
        slope_val = gas_log_slope(1.0, model_tag, meta)

    return {
        "r_core": float(r_core),
        "x_core": float(x_core),
        "r_core_Mpc": float(r_core / g2.MPC),
        "root_found": root_found,
        "unchanged_kept_R500": unchanged,
        "all_roots_x": [round(r, 6) for r in dedup],
        "slope_at_r_core": float(slope_val),
        "slope_at_R500": float(gas_log_slope(1.0, model_tag, meta)),
    }


def solve_two_domain_bvp(
    Mb, dM, R5: float, R2: float, rv: float, r_core: float, Mt5: float, Mt2: float, mu: float
) -> tuple[float, float, float, float]:
    """Two-domain BVP with Phi(r_v) = 0 and hydrostatic dust confined to r <= r_core."""
    rmin = 1e-4 * R5
    bad = {"u_nonpos": False}

    def rhs_core(r, y):
        W, Phi = y
        u = W / (r * r)
        if u <= 0.0:
            bad["u_nonpos"] = True
        return [g2.G * dM(r) - mu * mu * r * r * Phi, g2.law(u)]

    def rhs_infall(r, y):
        W, Phi = y
        u = W / (r * r)
        if u <= 0.0:
            bad["u_nonpos"] = True
        return [g2.G * dM(r), g2.law(u)]

    def shoot(P0: float, full: bool = False):
        bad["u_nonpos"] = False
        _, sol_fn, y_end, _ = g2._solve_segmented(
            rhs_core, rhs_infall, [g2.G * Mb(rmin), P0], rmin, rv, r_core, full=full
        )
        return sol_fn if full else float(y_end[1])

    g0 = -g2.law(g2.G * Mb(R5) / (R5**2)) * rv * 3.0
    idx = None
    grid = np.linspace(-6.0 * abs(g0), 2.0 * abs(g0), 17)
    F = [shoot(float(p)) for p in grid]
    idx = next((j for j in range(len(grid) - 1) if F[j] * F[j + 1] <= 0), None)
    if idx is None:
        grid = np.linspace(-12.0 * abs(g0), 4.0 * abs(g0), 65)
        F = [shoot(float(p)) for p in grid]
        idx = next(j for j in range(len(grid) - 1) if F[j] * F[j + 1] <= 0)
    P0 = brentq(shoot, float(grid[idx]), float(grid[idx + 1]), xtol=1e-6 * abs(g0))
    sol_fn = shoot(float(P0), True)
    assert not bad["u_nonpos"], f"Encountered u <= 0 at r_core={r_core}"
    Md = lambda r: g2.law(float(sol_fn(r)[0]) / (r * r)) * (r * r) / g2.G
    Md_out = float(sol_fn(rv)[0]) / g2.G - Mb(rv)
    dust_ratio = Md_out / (g2.COSMIC_RATIO * Mb(rv))
    return float(Mt5 / Md(R5)), float(Mt2 / Md(R2)), float(dust_ratio), float(P0)


def run_suite_with_rule(rows: list[list[str]], rule: str, baseline_res: dict | None = None) -> dict:
    """Execute 12 clusters x 3 models under rule in ('uniform_R500', 'frozen_slope_minus2')."""
    models_out = {}
    max_slope_fd_err = 0.0

    for model_tag in MODELS:
        r500_list, r200_list = [], []
        r500_d11, r200_d11 = [], []
        dust_ratios = []
        per_cluster = {}
        outside_r500 = {}
        outside_r200 = {}
        outside_either = {}
        unchanged_clusters = []

        for row in rows:
            Mb, dM, meta = g2.make_profile_for_cluster(row, model_tag)
            nm = meta["nm"]
            R5, R2, rv, Mt5, Mt2 = meta["R5"], meta["R2"], meta["rv"], meta["Mt5"], meta["Mt2"]
            max_slope_fd_err = max(max_slope_fd_err, verify_slope_derivative(model_tag, meta))

            if rule == "uniform_R500":
                edge_info = {
                    "r_core": float(R5),
                    "x_core": 1.0,
                    "r_core_Mpc": float(R5 / g2.MPC),
                    "root_found": False,
                    "unchanged_kept_R500": True,
                    "all_roots_x": [],
                    "slope_at_r_core": float(gas_log_slope(1.0, model_tag, meta)),
                    "slope_at_R500": float(gas_log_slope(1.0, model_tag, meta)),
                }
            elif rule == "frozen_slope_minus2":
                edge_info = find_slope_edge(model_tag, meta, SLOPE_TARGET)
            else:
                raise ValueError(rule)

            r_core = edge_info["r_core"]
            if edge_info["unchanged_kept_R500"]:
                unchanged_clusters.append(nm)

            R5_stat, R2_stat, dr_stat, P0_stat = solve_two_domain_bvp(
                Mb, dM, R5, R2, rv, r_core, Mt5, Mt2, g2.MU0
            )
            if dr_stat > 1.0:
                mu_eff = brentq(
                    lambda m: solve_two_domain_bvp(Mb, dM, R5, R2, rv, r_core, Mt5, Mt2, m)[2] - 1.0,
                    0.005 * g2.MU0,
                    g2.MU0,
                    xtol=1e-4 * g2.MU0,
                )
                R5_ratio, R2_ratio, dr_core, P0_val = solve_two_domain_bvp(
                    Mb, dM, R5, R2, rv, r_core, Mt5, Mt2, float(mu_eff)
                )
            else:
                mu_eff = g2.MU0
                R5_ratio, R2_ratio, dr_core, P0_val = R5_stat, R2_stat, dr_stat, P0_stat

            r500_list.append(R5_ratio)
            r200_list.append(R2_ratio)
            dust_ratios.append(dr_core)
            if nm != "A3266":
                r500_d11.append(R5_ratio)
                r200_d11.append(R2_ratio)

            in_500 = 0.80 <= R5_ratio <= 1.25
            in_200 = 0.80 <= R2_ratio <= 1.25
            in_both = in_500 and in_200
            if not in_500:
                outside_r500[nm] = round(R5_ratio, 4)
            if not in_200:
                outside_r200[nm] = round(R2_ratio, 4)
            if not in_both:
                outside_either[nm] = {
                    "R500_obs_over_mod": round(R5_ratio, 4),
                    "R200_obs_over_mod": round(R2_ratio, 4),
                }

            entry = {
                "R500_Mpc": round(float(R5 / g2.MPC), 4),
                "R200_Mpc": round(float(R2 / g2.MPC), 4),
                "r_core_over_R500": round(edge_info["x_core"], 4),
                "r_core_over_R200": round(float(r_core / R2), 4),
                "r_core_Mpc": round(edge_info["r_core_Mpc"], 4),
                "root_found": edge_info["root_found"],
                "unchanged_kept_R500": edge_info["unchanged_kept_R500"],
                "all_roots_x": edge_info["all_roots_x"],
                "slope_at_r_core": round(edge_info["slope_at_r_core"], 4),
                "slope_at_R500": round(edge_info["slope_at_R500"], 4),
                "R500_obs_over_mod": round(R5_ratio, 4),
                "R200_obs_over_mod": round(R2_ratio, 4),
                "in_080_125_R500": in_500,
                "in_080_125_R200": in_200,
                "in_080_125_both": in_both,
                "core_dust_ratio_of_cosmic": round(dr_core, 4),
                "mu_eff_over_mu0": round(float(mu_eff / g2.MU0), 4),
            }
            if baseline_res is not None:
                b_cl = baseline_res["models"][model_tag]["per_cluster"][nm]
                entry["baseline_R500_obs_over_mod"] = b_cl["R500_obs_over_mod"]
                entry["baseline_R200_obs_over_mod"] = b_cl["R200_obs_over_mod"]
                entry["delta_R500"] = round(R5_ratio - b_cl["R500_obs_over_mod"], 4)
                entry["delta_R200"] = round(R2_ratio - b_cl["R200_obs_over_mod"], 4)
            per_cluster[nm] = entry

        c500 = sum(1 for v in r500_list if 0.80 <= v <= 1.25)
        c200 = sum(1 for v in r200_list if 0.80 <= v <= 1.25)
        cboth = sum(1 for v5, v2 in zip(r500_list, r200_list) if 0.80 <= v5 <= 1.25 and 0.80 <= v2 <= 1.25)
        c500_w = sum(1 for v in r500_list if 0.70 <= v <= 1.40)
        c200_w = sum(1 for v in r200_list if 0.70 <= v <= 1.40)
        cboth_w = sum(1 for v5, v2 in zip(r500_list, r200_list) if 0.70 <= v5 <= 1.40 and 0.70 <= v2 <= 1.40)

        c500_d11 = sum(1 for v in r500_d11 if 0.80 <= v <= 1.25)
        c200_d11 = sum(1 for v in r200_d11 if 0.80 <= v <= 1.25)
        cboth_d11 = sum(1 for v5, v2 in zip(r500_d11, r200_d11) if 0.80 <= v5 <= 1.25 and 0.80 <= v2 <= 1.25)

        models_out[model_tag] = {
            "all12_med_R500": round(float(np.median(r500_list)), 4),
            "all12_med_R200": round(float(np.median(r200_list)), 4),
            "all12_in_080_125_R500": f"{c500}/12",
            "all12_in_080_125_R200": f"{c200}/12",
            "all12_in_080_125_both": f"{cboth}/12",
            "all12_in_080_125_both_int": cboth,
            "delta_both_from_8_of_12": cboth - 8,
            "all12_in_070_140_R500": f"{c500_w}/12",
            "all12_in_070_140_R200": f"{c200_w}/12",
            "all12_in_070_140_both": f"{cboth_w}/12",
            "direct11_med_R500": round(float(np.median(r500_d11)), 4),
            "direct11_med_R200": round(float(np.median(r200_d11)), 4),
            "direct11_in_080_125_R500": f"{c500_d11}/11",
            "direct11_in_080_125_R200": f"{c200_d11}/11",
            "direct11_in_080_125_both": f"{cboth_d11}/11",
            "n_changed_from_R500": len(rows) - len(unchanged_clusters),
            "n_unchanged_kept_R500": len(unchanged_clusters),
            "unchanged_clusters": unchanged_clusters,
            "clusters_outside_080_125_R500": outside_r500,
            "clusters_outside_080_125_R200": outside_r200,
            "clusters_outside_080_125_either": outside_either,
            "max_core_dust_ratio_of_cosmic": round(float(max(dust_ratios)), 4),
            "budget_caps_triggered": sum(1 for v in dust_ratios if v >= 1.0 - 1e-4),
            "per_cluster": per_cluster,
        }

    return {
        "max_slope_fd_err": float(max_slope_fd_err),
        "models": models_out,
    }


def run_audit() -> dict:
    tsv_path = ROOT / "exploration" / "d10_xcop" / "xcop_data.tsv"
    rows = []
    with open(tsv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("name"):
                continue
            rows.append(line.split())
    assert len(rows) == 12

    ref = json.loads(REF_JSON_PATH.read_text(encoding="utf-8"))
    ref_models = ref["xcop_r500_core_truncation_bvp"]["models"]

    # 1. Mandatory control: uniform r_core = R_500 must reproduce NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE.json
    ctrl = run_suite_with_rule(rows, rule="uniform_R500")
    for m in MODELS:
        cm = ctrl["models"][m]
        rm = ref_models[m]
        assert abs(cm["all12_med_R500"] - rm["all12_med_R500"]) <= 1e-4, f"Control med_R500 mismatch on {m}"
        assert abs(cm["all12_med_R200"] - rm["all12_med_R200"]) <= 1e-4, f"Control med_R200 mismatch on {m}"
        assert cm["all12_in_080_125_R500"] == rm["all12_in_080_125_R500"] == "9/12"
        assert cm["all12_in_080_125_R200"] == rm["all12_in_080_125_R200"] == "9/12"
        assert cm["all12_in_080_125_both"] == rm["all12_in_080_125_both"] == "8/12"

    # 2. Frozen -2.0 logarithmic gas-slope edge run on all 12 clusters x 3 ICM models
    slope_res = run_suite_with_rule(rows, rule="frozen_slope_minus2", baseline_res=ctrl)

    best_both = max(slope_res["models"][m]["all12_in_080_125_both_int"] for m in MODELS)
    deltas = [slope_res["models"][m]["delta_both_from_8_of_12"] for m in MODELS]
    med_r500_rng = [
        min(slope_res["models"][m]["all12_med_R500"] for m in MODELS),
        max(slope_res["models"][m]["all12_med_R500"] for m in MODELS),
    ]
    med_r200_rng = [
        min(slope_res["models"][m]["all12_med_R200"] for m in MODELS),
        max(slope_res["models"][m]["all12_med_R200"] for m in MODELS),
    ]

    summary_verdict = (
        f"Frozen d ln rho_gas / d ln r = -2.0 core edge yields medians {med_r500_rng[0]:.4f}-{med_r500_rng[1]:.4f} (R_500) "
        f"and {med_r200_rng[0]:.4f}-{med_r200_rng[1]:.4f} (R_200), changing the [0.80, 1.25] joint (both-radii) count "
        f"from 8/12 to {', '.join(slope_res['models'][m]['all12_in_080_125_both'] + f' ({m[:2]})' for m in MODELS)} "
        f"(deltas {deltas} relative to 8/12)."
    )

    return {
        "meta": {
            "date": "2026-11-21",
            "script": "audits/2026-11-21/xcop_core_edge_invariant.py",
            "epistemic_tag": "[D]",
            "preregistration": {
                "frozen_slope_target": SLOPE_TARGET,
                "rule": "Smallest radius r in [1e-4 * R_500, r_v] where d ln rho_gas / d ln r = -2.0 on each cluster's measured ICM profile; if absent, keep r_core = R_500 and count as unchanged.",
                "solver": "DOP853 two-segment BVP (exploration/d10_xcop/gate2_xcop_measured_icm.py), Phi(r_v) = 0, universal mu0 = 1/(0.9895 Mpc), cosmic cap 5.36 M_b(r_v).",
                "baseline_reference": "audits/2026-11-21/NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE.json",
                "slope_frozen_prior_to_solve": True,
            },
        },
        "uniform_R500_control": {
            "reproduces_NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE_json": True,
            "models": {
                m: {
                    k: ctrl["models"][m][k]
                    for k in (
                        "all12_med_R500",
                        "all12_med_R200",
                        "all12_in_080_125_R500",
                        "all12_in_080_125_R200",
                        "all12_in_080_125_both",
                    )
                }
                for m in MODELS
            },
        },
        "frozen_slope_minus2_edge": {
            "max_slope_finite_diff_check_err": slope_res["max_slope_fd_err"],
            "best_both_count_int": best_both,
            "summary": summary_verdict,
            "models": slope_res["models"],
        },
    }


def write_markdown(res: dict, out_md: Path) -> None:
    ctrl = res["uniform_R500_control"]
    edge = res["frozen_slope_minus2_edge"]
    lines = [
        "# X-COP Frozen Core-Edge Invariant ($d\\ln\\rho_{\\mathrm{gas}}/d\\ln r = -2$)",
        "",
        f"- **Date:** {res['meta']['date']}",
        f"- **Epistemic Tag:** `{res['meta']['epistemic_tag']}`",
        "- **Script:** `audits/2026-11-21/xcop_core_edge_invariant.py`",
        "- **Receipt:** `audits/2026-11-21/XCOP_CORE_EDGE_INVARIANT.json`",
        "",
        "## 1. Frozen Core-Edge Rule & Uniform-$R_{500}$ Control",
        "",
        "- **Frozen rule (not adjusted after inspection):** On each cluster's measured ICM profile, set $r_{\\mathrm{core}}$ to the **smallest radius** $r \\in [10^{-4} R_{500}, r_v]$ where $d\\ln\\rho_{\\mathrm{gas}} / d\\ln r = -2.0$. If no root exists on that domain, keep $r_{\\mathrm{core}} = R_{500}$ and count the cluster as unchanged.",
        f"- **Analytic slope self-check:** Verified against central finite differences on all 12 clusters $\\times$ 3 models (max error `{edge['max_slope_finite_diff_check_err']:.2e}`).",
        f"- **Mandatory uniform-$R_{{500}}$ control (`reproduces_NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE_json = {ctrl['reproduces_NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE_json']}`):**",
        "",
        "| Model (Uniform $r_{\\mathrm{core}} = R_{500}$) | Med $R_{500}$ | Med $R_{200}$ | `[0.80, 1.25]` ($R_{500}$ / $R_{200}$ / Both) |",
        "| :--- | :---: | :---: | :---: |",
    ]
    for m in MODELS:
        cm = ctrl["models"][m]
        lines.append(
            f"| `{m}` | `{cm['all12_med_R500']:.4f}` | `{cm['all12_med_R200']:.4f}` | "
            f"`{cm['all12_in_080_125_R500']}` / `{cm['all12_in_080_125_R200']}` / **`{cm['all12_in_080_125_both']}`** |"
        )

    lines.extend([
        "",
        "## 2. Frozen $d\\ln\\rho_{\\mathrm{gas}}/d\\ln r = -2.0$ Core Edge vs. `8/12` Baseline",
        "",
        f"> **{edge['summary']}**",
        "",
        "| Measured ICM Model | Unchanged ($=R_{500}$) | Med $R_{500}$ | Med $R_{200}$ | `[0.80, 1.25]` ($R_{500}$ / $R_{200}$ / Both) | $\\Delta$ vs `8/12` | `[0.70, 1.40]` ($R_{500}$ / $R_{200}$) | Max Dust / Cosmic | Budget Caps |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ])
    for m in MODELS:
        d = edge["models"][m]
        lines.append(
            f"| `{m}` | `{d['n_unchanged_kept_R500']}/12` | `{d['all12_med_R500']:.4f}` | `{d['all12_med_R200']:.4f}` | "
            f"`{d['all12_in_080_125_R500']}` / `{d['all12_in_080_125_R200']}` / **`{d['all12_in_080_125_both']}`** | "
            f"**`{d['delta_both_from_8_of_12']:+d}`** | `{d['all12_in_070_140_R500']}` / `{d['all12_in_070_140_R200']}` | "
            f"`{d['max_core_dust_ratio_of_cosmic']:.4f}` | `{d['budget_caps_triggered']}` |"
        )

    lines.extend([
        "",
        "### Outliers Outside `[0.80, 1.25]` (Both Radii Listed for Every Outlier)",
        "",
    ])
    for m in MODELS:
        d = edge["models"][m]
        lines.append(f"- **`{m}`** (`{d['all12_in_080_125_both']}` pass both; unchanged: `{d['unchanged_clusters']}`):")
        for nm, vals in d["clusters_outside_080_125_either"].items():
            rc_ov = d["per_cluster"][nm]["r_core_over_R500"]
            lines.append(
                f"  - `{nm}` ($r_{{\\mathrm{{core}}}}/R_{{500}} = {rc_ov:.4f}$): "
                f"$R_{{500}} = {vals['R500_obs_over_mod']:.4f}$, $R_{{200}} = {vals['R200_obs_over_mod']:.4f}$"
            )

    for m in MODELS:
        d = edge["models"][m]
        lines.extend([
            "",
            f"## 3. Full 12-Cluster Table — `{m}`",
            "",
            "| Cluster | $r_{\\mathrm{core}}/R_{500}$ | $r_{\\mathrm{core}}$ [Mpc] | Unchanged | $R_{500}$ (Baseline) | $R_{200}$ (Baseline) | Pass `[0.80, 1.25]` ($R_{500}$ / $R_{200}$ / Both) | Dust / Cosmic | $\\mu_{\\mathrm{eff}}/\\mu_0$ |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ])
        for nm, cl in d["per_cluster"].items():
            lines.append(
                f"| `{nm}` | `{cl['r_core_over_R500']:.4f}` | `{cl['r_core_Mpc']:.4f}` | `{cl['unchanged_kept_R500']}` | "
                f"`{cl['R500_obs_over_mod']:.4f}` (`{cl['baseline_R500_obs_over_mod']:.4f}`) | "
                f"`{cl['R200_obs_over_mod']:.4f}` (`{cl['baseline_R200_obs_over_mod']:.4f}`) | "
                f"`{cl['in_080_125_R500']}` / `{cl['in_080_125_R200']}` / **{cl['in_080_125_both']}** | "
                f"`{cl['core_dust_ratio_of_cosmic']:.4f}` | `{cl['mu_eff_over_mu0']:.4f}` |"
            )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    result = run_audit()
    out_json = HERE / "XCOP_CORE_EDGE_INVARIANT.json"
    out_md = HERE / "XCOP_CORE_EDGE_INVARIANT.md"
    out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_markdown(result, out_md)
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    for m in MODELS:
        d = result["frozen_slope_minus2_edge"]["models"][m]
        print(
            f"  {m}: med={d['all12_med_R500']} / {d['all12_med_R200']}, "
            f"[0.80,1.25]={d['all12_in_080_125_R500']} / {d['all12_in_080_125_R200']} / {d['all12_in_080_125_both']} "
            f"(delta vs 8/12: {d['delta_both_from_8_of_12']:+d}), unchanged={d['n_unchanged_kept_R500']}/12, "
            f"outside={list(d['clusters_outside_080_125_either'].keys())}"
        )
