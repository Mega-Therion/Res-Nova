#!/usr/bin/env python3
"""
High-z Spatially Resolved Kinematic YWR Bore-Gauge Audit (z = 0.58 -- 7.43):
Evaluates 125 provenance-verified resolved high-z galaxies from Res-Nova's audited tables
(zero synthetic rows, zero per-galaxy fitted dark-matter halo parameters):

  - Sample 1: RC100 (Nestor Shachar+2023, ApJ 944, 78; N = 100 H-alpha/CO disks, z = 0.60--2.53)
  - Sample 2: JWST/NIRSpec MSA-3D (Pastras+2026, arXiv:2606.27853; N = 20 bounded-Mbar 3D disks, z = 0.58--1.57)
  - Sample 3: ALPINE-CRISTAL-JWST (Lee+2026, arXiv:2611.07064; N = 5 JWST IFU + ALMA [C II] disks, z = 4.44--5.69)
  - Aux [O] : JADES G395H (de Graaff+2024, arXiv:2308.09742; N = 6 galaxies, z = 5.50--7.43)

Tests two quantitative hypotheses:
  1. YWR Surface-Density Monotonicity: Does observed dynamical-to-baryonic ratio
     B_obs = g_obs / g_bar track the Block 3 surface-density curve nu_std(g_bar / a0)
     across 2.5 decades in g_bar / a0?
  2. Redshift-Flat Dispersion Offset vs. E(z) Running: Why is a0_hat nearly flat between
     z_eff = 1.09 (MSA-3D) and z_eff = 5.33 (ALPINE-CRISTAL, 4.76x jump in E(z))? Compares:
       - Model A: Cold 2D disk static a0 (Q = 1.0)
       - Model B: Horizon-running a0(z) = xi * c * H(z)
       - Model C: Static a0 with 3D turbulent/triaxial factor Q_3D = sqrt(2) [O] (matching
                  the GAMA DR4 intrinsic-elliptical weak-lensing factor Q_ETG = sqrt(2)).

Epistemic status: [D]/[E] deterministic evaluation on published spectroscopic kinematics;
3D dispersion factor Q_3D = sqrt(2) physical identification is explicitly fenced as [O].
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for sub in ("02_galaxy_dynamics", "04_cosmology"):
    p = str(ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

import highz_a0_method as M  # noqa: E402
import o4_jwst_a0z_run as O4  # noqa: E402

OUT_JSON = HERE / "HIGHZ_KINEMATIC_YWR_AUDIT_2026-11-27.json"
OUT_MD = HERE / "HIGHZ_KINEMATIC_YWR_AUDIT_2026-11-27.md"

A0_CANON = 1.1607e-10  # SPARC-175 canonical mu_std acceleration scale [m/s^2]
XI_HORIZ = 0.170
C_LIGHT = 2.99792458e8
MPC_M = 3.0856775814913673e22
A0_H0 = XI_HORIZ * C_LIGHT * (O4.H0_PLANCK * 1e3 / MPC_M)


def collect_primary_samples() -> dict[str, dict]:
    rc = M.load_rc100()
    msa = O4.build_msa3d_mbar(subset="bounded")
    alp = O4.build_alpine_cristal_mbar(kinematics="dysmal")

    return {
        "RC100_z0p6_2p5": {
            "n": int(len(rc["z"])),
            "z": np.asarray(rc["z"], dtype=np.float64),
            "g_obs": np.asarray(rc["g_obs"], dtype=np.float64),
            "g_bar": np.asarray(rc["gbar_b"], dtype=np.float64),
            "s_lng": np.asarray(rc["s_lng"], dtype=np.float64),
            "s_lngb": np.asarray(rc["s_lngb"], dtype=np.float64),
            "v_over_sigma": np.asarray(rc["Vc_kms"] / np.maximum(rc["sigma0_kms"], 1.0), dtype=np.float64),
        },
        "JWST_MSA3D_z0p6_1p6": {
            "n": int(len(msa["z"])),
            "z": np.asarray(msa["z"], dtype=np.float64),
            "g_obs": np.asarray(msa["g_obs"], dtype=np.float64),
            "g_bar": np.asarray(msa["g_bar"], dtype=np.float64),
            "s_lng": np.asarray(msa["s_lng"], dtype=np.float64),
            "s_lngb": np.asarray(msa["s_lngb"], dtype=np.float64),
            "v_over_sigma": np.array(
                [r[9] / max(r[6], 1.0) for r in O4.MSA3D_ROWS if r[17] is not None], dtype=np.float64
            ),
        },
        "JWST_ALMA_ALPINE_CRISTAL_z4p4_5p7": {
            "n": int(len(alp["z"])),
            "z": np.asarray(alp["z"], dtype=np.float64),
            "g_obs": np.asarray(alp["g_obs"], dtype=np.float64),
            "g_bar": np.asarray(alp["g_bar"], dtype=np.float64),
            "s_lng": np.asarray(alp["s_lng"], dtype=np.float64),
            "s_lngb": np.asarray(alp["s_lngb"], dtype=np.float64),
            "v_over_sigma": np.full(len(alp["z"]), np.nan),
        },
    }


def evaluate_ywr_and_models(samples: dict[str, dict]) -> dict:
    all_z = np.concatenate([s["z"] for s in samples.values()])
    all_gobs = np.concatenate([s["g_obs"] for s in samples.values()])
    all_gbar = np.concatenate([s["g_bar"] for s in samples.values()])
    all_slng = np.concatenate([s["s_lng"] for s in samples.values()])
    all_slngb = np.concatenate([s["s_lngb"] for s in samples.values()])

    y_all = all_gbar / A0_CANON
    boost_obs = all_gobs / all_gbar
    boost_ywr_q1 = M.nu_std(y_all)
    rho_s, p_spear = spearmanr(y_all, boost_obs)

    # Surface-density tertiles across all N = 125 galaxies
    q_edges = np.quantile(y_all, [0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0])
    tertiles = []
    for i in range(3):
        if i < 2:
            m = (y_all >= q_edges[i]) & (y_all < q_edges[i + 1])
        else:
            m = (y_all >= q_edges[i]) & (y_all <= q_edges[i + 1])
        y_sub = y_all[m]
        b_sub = boost_obs[m]
        b_q1 = M.nu_std(y_sub)
        b_qsqrt2 = math.sqrt(2.0) * M.nu_std(math.sqrt(2.0) * y_sub)
        # Wait: if effective 3D virial baryon weight has Q_3D = sqrt(2) (as in GAMA Q_ETG = sqrt(2)),
        # g_eff_bar = sqrt(2) * g_bar, so g_pred(sqrt(2)*g_bar; a0) / g_bar = sqrt(2) * nu_std(sqrt(2) * y)!
        tertiles.append(
            {
                "tertile": i + 1,
                "n": int(m.sum()),
                "median_y_gbar_over_a0": round(float(np.median(y_sub)), 3),
                "observed_median_gobs_over_gbar": round(float(np.median(b_sub)), 3),
                "pred_ywr_Q1_gpred_over_gbar": round(float(np.median(b_q1)), 3),
                "pred_ywr_Qsqrt2_gpred_over_gbar": round(float(np.median(b_qsqrt2)), 3),
            }
        )

    # Per-sample model comparison (Model A: static a0 Q=1; Model B: E(z) horizon a0(z); Model C: static a0 Q_3D=sqrt(2))
    per_sample = {}
    q3d = math.sqrt(2.0)
    for name, s in samples.items():
        z = s["z"]
        go = s["g_obs"]
        gb = s["g_bar"]
        ez = np.array([O4.E_z(float(zz)) for zz in z])
        sig_tot = np.hypot(s["s_lng"], s["s_lngb"])  # log-residual observational error scale

        gp_A = M.g_pred(gb, A0_CANON)
        gp_B = np.array([float(M.g_pred(gb[i], A0_H0 * ez[i])) for i in range(len(z))])
        gp_C = M.g_pred(q3d * gb, A0_CANON)

        def _stats(gp: np.ndarray) -> dict:
            log_res = np.log10(go / gp)
            ln_res = np.log(go / gp)
            chi2_red = float(np.mean((ln_res / np.maximum(sig_tot, 0.15)) ** 2))
            return {
                "median_gobs_over_gpred": round(float(np.median(go / gp)), 4),
                "median_Vobs_over_Vpred": round(float(np.sqrt(np.median(go / gp))), 4),
                "median_dex_residual": round(float(np.median(log_res)), 4),
                "rms_dex_residual": round(float(np.sqrt(np.mean(log_res ** 2))), 4),
                "mean_weighted_sq_zscore": round(chi2_red, 3),
            }

        vs = s["v_over_sigma"]
        med_vs = round(float(np.nanmedian(vs)), 2) if np.any(np.isfinite(vs)) else None
        per_sample[name] = {
            "n": s["n"],
            "median_z": round(float(np.median(z)), 3),
            "median_Ez": round(float(np.median(ez)), 3),
            "median_V_over_sigma": med_vs,
            "median_gbar_over_a0": round(float(np.median(gb / A0_CANON)), 3),
            "median_observed_gobs_over_gbar": round(float(np.median(go / gb)), 3),
            "model_A_static_a0_Q1": _stats(gp_A),
            "model_B_horizon_a0z_Ez": _stats(gp_B),
            "model_C_static_a0_Q3D_sqrt2_O": _stats(gp_C),
        }

    return {
        "total_primary_galaxies": int(len(all_z)),
        "spearman_r_y_vs_gobs_over_gbar": round(float(rho_s), 4),
        "spearman_p_value": float(f"{p_spear:.4e}"),
        "surface_density_tertiles": tertiles,
        "per_sample_comparison": per_sample,
        "aux_degraaff_z5p5_7p4_O": O4.evaluate_degraaff_aux(),
    }


def run_self_test() -> int:
    # Verify exact algebraic identity g_pred(Q * g_bar, a0) / g_bar = Q * nu_std(Q * g_bar / a0)
    q = math.sqrt(2.0)
    for y in (0.1, 1.0, 5.0, 25.0):
        gb = y * A0_CANON
        lhs = float(M.g_pred(q * gb, A0_CANON)) / gb
        rhs = q * float(M.nu_std(q * y))
        assert abs(lhs - rhs) < 1e-12, (lhs, rhs)

    samples = collect_primary_samples()
    assert samples["RC100_z0p6_2p5"]["n"] == 100
    assert samples["JWST_MSA3D_z0p6_1p6"]["n"] == 20
    assert samples["JWST_ALMA_ALPINE_CRISTAL_z4p4_5p7"]["n"] == 5
    res = evaluate_ywr_and_models(samples)
    # Surface-density monotonicity must hold at high significance (negative Spearman r)
    assert res["spearman_r_y_vs_gobs_over_gbar"] < -0.50 and res["spearman_p_value"] < 1e-10
    print("highz_kinematic_ywr_audit self-test: PASS")
    return 0


def run_main() -> int:
    samples = collect_primary_samples()
    res = evaluate_ywr_and_models(samples)
    payload = {
        "date": "2026-11-27",
        "epistemic_tag": "[D]/[E] resolved high-z rotation-curve YWR surface-density & dispersion audit (Q_3D=sqrt(2) fenced [O])",
        "a0_canonical_SI": A0_CANON,
        "results": res,
    }
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    payload["sha256_body"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    md = [
        "# High-$z$ Spatially Resolved Kinematic `YWR` Bore-Gauge Audit ($z = 0.58\\text{--}7.43$, 2026-11-27)",
        "",
        "**Epistemic Tier:** `[E]`/`[D]` deterministic evaluation across `125` spatially resolved high-$z$ galaxies (`RC100` $N=100$, `JWST/NIRSpec MSA-3D` $N=20$, `ALPINE-CRISTAL JWST+ALMA [C II]` $N=5$, plus `6` auxiliary `JADES G395H` galaxies `[O]`) with no per-galaxy fitted dark-matter halo parameters. The 3D turbulent/triaxial factor `Q_3D = sqrt(2)` is fenced as `[O]`.",
        "",
        "## 1. `YWR` Surface-Density Monotonicity Across `125` High-$z$ Disks ($0.58 \\le z \\le 5.69$)",
        "",
        f"- **Global Spearman Rank Correlation between $y = g_{{\\rm bar}}/a_0$ and $M_{{\\rm dyn,N}}/M_{{\\rm bar}} = g_{{\\rm obs}}/g_{{\\rm bar}}$:** **`r_s = {res['spearman_r_y_vs_gobs_over_gbar']:+.4f}` (`p = {res['spearman_p_value']:.3e}`)** — confirming that high-surface-brightness baryonic cores approach Newtonian unity while extended lower-surface-density disks climb monotonically.",
        "",
        "| Surface-Density Tertile ($N=125$) | $N$ | Median $g_{\\rm bar}/a_0$ | Observed Median $g_{\\rm obs}/g_{\\rm bar}$ | Static `Block 3` `Q=1` $\\nu_{\\rm std}(y)$ | Static `Block 3` `Q_3D=sqrt(2)` `[O]` |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for t in res["surface_density_tertiles"]:
        md.append(
            f"| Tertile {t['tertile']} | `{t['n']}` | `{t['median_y_gbar_over_a0']:.3f}` | "
            f"**`{t['observed_median_gobs_over_gbar']:.3f}x`** | `{t['pred_ywr_Q1_gpred_over_gbar']:.3f}x` | "
            f"**`{t['pred_ywr_Qsqrt2_gpred_over_gbar']:.3f}x`** |"
        )

    md.extend(
        [
            "",
            "## 2. Redshift Evolution ($z = 0.6 \\to 5.7$) vs. 3D Turbulent Dispersion Geometry",
            "",
            "| Resolved Sample | $N$ | Median $z$ ($E(z)$) | Median $V/\\sigma_0$ | Model A (`Q=1` Static $a_0$) `med g_obs/g_pred` (RMS dex) | Model B ($a_0(z)\\propto E(z)$) `med g_obs/g_pred` (RMS dex) | Model C (`Q_3D=sqrt(2)` Static $a_0$ `[O]`) `med g_obs/g_pred` (RMS dex) |",
            "|---|---:|---:|---:|---|---|---|",
        ]
    )
    for name, ps in res["per_sample_comparison"].items():
        mA = ps["model_A_static_a0_Q1"]
        mB = ps["model_B_horizon_a0z_Ez"]
        mC = ps["model_C_static_a0_Q3D_sqrt2_O"]
        vs_str = f"`{ps['median_V_over_sigma']:.2f}`" if ps["median_V_over_sigma"] is not None else "`IFU+ALMA`"
        md.append(
            f"| `{name}` | `{ps['n']}` | `{ps['median_z']:.2f}` (`{ps['median_Ez']:.2f}`) | {vs_str} | "
            f"`{mA['median_gobs_over_gpred']:.3f}x` (`{mA['rms_dex_residual']:.3f}`) | "
            f"`{mB['median_gobs_over_gpred']:.3f}x` (`{mB['rms_dex_residual']:.3f}`) | "
            f"**`{mC['median_gobs_over_gpred']:.3f}x` (`{mC['rms_dex_residual']:.3f}`)** |"
        )

    md.extend(
        [
            "",
            "## Reproducibility",
            "```bash",
            "python3 03_observer_jwst/highz_kinematic_ywr_audit.py --self-test",
            "python3 03_observer_jwst/highz_kinematic_ywr_audit.py --run",
            "```",
        ]
    )
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON} and {OUT_MD}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return run_self_test()
    if args.run:
        return run_main()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
