#!/usr/bin/env python3
"""
Multi-Tier Evaluation of the Zero-Parameter 3D Phase-Space Dispersion Law Q_3D(V_rot / sigma_0):

    Q_3D(xi) = sqrt((xi^2 + 6) / (xi^2 + 3)) = sqrt(1 + 3 / (xi^2 + 3)),   xi = V_rot / sigma_0

Interpolates smoothly with ZERO free parameters between:
  - Cold 2D planar spiral disks (xi -> inf):      Q_3D -> 1.0000
  - Halfway equipartition transition (xi = sqrt3): Q_3D -> sqrt(3/2) = 1.2247
  - Isotropic 3D dispersion spheres (xi -> 0):    Q_3D -> sqrt(2)   = 1.4142

Evaluates Q_3D(V_rot / sigma_0) across four real observational tiers on disk:
  1. Cold z ~ 0 thin spiral benchmark (SPARC-like V_rot / sigma_0 in [8, 15])
  2. RC100 z = 0.6--2.5 resolved H-alpha/CO disks (N = 100, per-galaxy V_rot & sigma_0)
  3. JWST/NIRSpec MSA-3D z = 0.58--1.57 3D slit-stepping disks (N = 20 bounded-Mbar, per-galaxy V_rot & sigma_0)
  4. GAMA DR4 + KiDS-Legacy DR5 isolated dust-free intrinsic ellipticals (N = 5,418, xi -> 0 => Q_3D = sqrt(2))

Reports BOTH constitutive coupling prescriptions side-by-side without cherry-picking:
  - Prescription I (Effective Baryon Coupling):  g_pred = g_MOND(Q_3D * g_bar; a0)   [exact match to weak-lensing Q_ETG]
  - Prescription II (3D Virial Trace Projection): g_pred = Q_3D^2 * g_MOND(g_bar; a0) [phase-space kinetic projection]

Epistemic status: [P] algebraic bounds in 05_lean_formalization/DispersionQuadrature.lean;
[D]/[E] deterministic evaluation on published kinematic & weak-lensing catalogs;
[O] physical covariant Jeans / effective baryon coupling derivation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for sub in ("02_galaxy_dynamics", "03_observer_jwst", "04_cosmology"):
    p = str(ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

import highz_a0_method as M  # noqa: E402
import o4_jwst_a0z_run as O4  # noqa: E402

WL_DIAG_JSON = ROOT / "03_observer_jwst" / "POM1_INTRINSIC_DIPOLE_DIAGNOSTIC_2026-11-27.json"
OUT_JSON = HERE / "DISPERSION_QUADRATURE_AUDIT_2026-11-27.json"
OUT_MD = HERE / "DISPERSION_QUADRATURE_AUDIT_2026-11-27.md"

A0_CANON = 1.1607e-10  # SPARC-175 canonical mu_std acceleration scale [m/s^2]


def q3d_from_xi(xi: float | np.ndarray) -> float | np.ndarray:
    """Zero-parameter phase-space quadrature factor Q_3D(V_rot / sigma_0) in [1, sqrt(2)]."""
    x2 = np.square(xi)
    return np.sqrt((x2 + 6.0) / (x2 + 3.0))


def _residual_summary(g_obs: np.ndarray, g_pred: np.ndarray, sig_ln_tot: np.ndarray) -> dict:
    ratio = g_obs / g_pred
    dex = np.log10(ratio)
    ln_r = np.log(ratio)
    mean_chi2_dof = float(np.mean((ln_r / np.maximum(sig_ln_tot, 0.15)) ** 2))
    return {
        "median_gobs_over_gpred": round(float(np.median(ratio)), 4),
        "median_dex_residual": round(float(np.median(dex)), 4),
        "rms_dex_residual": round(float(np.sqrt(np.mean(dex ** 2))), 4),
        "mean_sq_zscore": round(mean_chi2_dof, 3),
    }


def evaluate_all_tiers() -> dict:
    # 1. Cold z ~ 0 thin-disk enclosure check (SPARC typical V_rot ~ 120-220 km/s, sigma_0 ~ 10-15 km/s => xi ~ 8..15)
    cold_ladder = []
    for xi_val in (15.0, 12.0, 10.0, 8.0, math.sqrt(3.0), 0.0):
        qv = float(q3d_from_xi(xi_val))
        cold_ladder.append({
            "Vrot_over_sigma0": round(xi_val, 4),
            "Q_3D": round(qv, 6),
            "Q_3D_squared": round(qv * qv, 6),
        })

    # 2. RC100 (N = 100, z = 0.60--2.53): reconstruct V_rot from V_c^2 = V_rot^2 + 3.36 * sigma_0^2 at R_e
    rc = M.load_rc100()
    vc_rc = np.asarray(rc["Vc_kms"], dtype=np.float64)
    s0_rc = np.maximum(np.asarray(rc["sigma0_kms"], dtype=np.float64), 1.0)
    vrot_rc = np.sqrt(np.maximum(vc_rc ** 2 - M.BURKERT_COEF * (s0_rc ** 2), 0.0))
    xi_rc = vrot_rc / s0_rc
    q_rc = q3d_from_xi(xi_rc)
    gobs_rc = np.asarray(rc["g_obs"], dtype=np.float64)
    gbar_rc = np.asarray(rc["gbar_b"], dtype=np.float64)
    sig_rc = np.hypot(rc["s_lng"], rc["s_lngb"])

    # 3. JWST/NIRSpec MSA-3D (N = 20 bounded-Mbar, z = 0.58--1.57): direct measured V_rot(2.2 R_s) and sigma_0
    msa = O4.build_msa3d_mbar(subset="bounded")
    bnd_rows = [r for r in O4.MSA3D_ROWS if r[17] is not None]
    vrot_msa = np.array([float(r[9]) for r in bnd_rows], dtype=np.float64)
    s0_msa = np.maximum(np.array([float(r[6]) for r in bnd_rows], dtype=np.float64), 1.0)
    xi_msa = vrot_msa / s0_msa
    q_msa = q3d_from_xi(xi_msa)
    gobs_msa = np.asarray(msa["g_obs"], dtype=np.float64)
    gbar_msa = np.asarray(msa["g_bar"], dtype=np.float64)
    sig_msa = np.hypot(msa["s_lng"], msa["s_lngb"])

    # 4. GAMA DR4 + KiDS-Legacy DR5 isolated dust-free ellipticals (xi -> 0 => Q_3D(0) = sqrt(2))
    wl_summary = None
    if WL_DIAG_JSON.is_file():
        wl_raw = json.loads(WL_DIAG_JSON.read_text(encoding="utf-8"))
        ic = wl_raw["part_1_gama_dust_mirage"]["intrinsic_cut_lensing"]
        wl_summary = {
            "n_true_disks": 39632,
            "n_true_ellipticals": 5418,
            "Q_3D_at_xi_0": round(float(q3d_from_xi(0.0)), 6),
            "ETG_chi2_ndof_at_Q1": f"{ic['Q_ETG_1.0']['etg']['chi2']}/{ic['Q_ETG_1.0']['etg']['ndof']}",
            "ETG_p_at_Q1": ic["Q_ETG_1.0"]["etg"]["p_value"],
            "ETG_chi2_ndof_at_Qsqrt2": f"{ic['Q_ETG_sqrt2']['etg']['chi2']}/{ic['Q_ETG_sqrt2']['etg']['ndof']}",
            "ETG_p_at_Qsqrt2": ic["Q_ETG_sqrt2"]["etg"]["p_value"],
            "Joint_Hartlap_verdict_at_Qsqrt2": ic["Q_ETG_sqrt2"]["verdict_hartlap"],
            "Joint_Hartlap_p_at_Qsqrt2": ic["Q_ETG_sqrt2"]["hartlap_p"],
        }

    def _pack_kinematic_sample(label: str, z_arr: np.ndarray, xi_arr: np.ndarray, q_arr: np.ndarray,
                               go: np.ndarray, gb: np.ndarray, sig_ln: np.ndarray) -> dict:
        gp_q1 = M.g_pred(gb, A0_CANON)
        gp_baryon_q = M.g_pred(q_arr * gb, A0_CANON)
        gp_virial_q2 = (q_arr ** 2) * M.g_pred(gb, A0_CANON)
        gp_const_sqrt2 = M.g_pred(math.sqrt(2.0) * gb, A0_CANON)
        return {
            "label": label,
            "n": int(len(z_arr)),
            "median_z": round(float(np.median(z_arr)), 3),
            "median_Vrot_over_sigma0": round(float(np.median(xi_arr)), 3),
            "iqr_Vrot_over_sigma0": [round(float(np.percentile(xi_arr, 25)), 3), round(float(np.percentile(xi_arr, 75)), 3)],
            "median_Q3D_individual": round(float(np.median(q_arr)), 4),
            "baseline_Q1_thin_disk": _residual_summary(go, gp_q1, sig_ln),
            "prescription_I_baryon_Q3D_xi_O": _residual_summary(go, gp_baryon_q, sig_ln),
            "prescription_II_virial_Q3D_sq_xi_O": _residual_summary(go, gp_virial_q2, sig_ln),
            "ceiling_constant_Q_sqrt2_O": _residual_summary(go, gp_const_sqrt2, sig_ln),
        }

    return {
        "analytic_ladder": cold_ladder,
        "kinematic_tiers": {
            "RC100_N100": _pack_kinematic_sample("RC100 (z = 0.60--2.53)", np.asarray(rc["z"]), xi_rc, q_rc, gobs_rc, gbar_rc, sig_rc),
            "JWST_MSA3D_N20": _pack_kinematic_sample("JWST MSA-3D (z = 0.58--1.57)", np.asarray(msa["z"]), xi_msa, q_msa, gobs_msa, gbar_msa, sig_msa),
        },
        "weak_lensing_elliptical_endpoint": wl_summary,
    }


def run_self_test() -> int:
    assert abs(float(q3d_from_xi(0.0)) - math.sqrt(2.0)) < 1e-15
    assert abs(float(q3d_from_xi(math.sqrt(3.0))) - math.sqrt(1.5)) < 1e-15
    assert 1.0 < float(q3d_from_xi(10.0)) < 1.015
    # Verify strict decreasing monotonicity
    xis = np.linspace(0.0, 20.0, 201)
    qs = q3d_from_xi(xis)
    assert np.all(np.diff(qs) < 0.0)
    res = evaluate_all_tiers()
    assert res["kinematic_tiers"]["RC100_N100"]["n"] == 100
    assert res["kinematic_tiers"]["JWST_MSA3D_N20"]["n"] == 20
    # MSA-3D is more dispersion-supported than RC100, so its median Q_3D(xi) must be strictly larger
    assert (
        res["kinematic_tiers"]["JWST_MSA3D_N20"]["median_Q3D_individual"]
        > res["kinematic_tiers"]["RC100_N100"]["median_Q3D_individual"]
    )
    print("dispersion_quadrature_audit self-test: PASS")
    return 0


def run_main() -> int:
    res = evaluate_all_tiers()
    payload = {
        "date": "2026-11-27",
        "epistemic_tag": "[P] bounds in DispersionQuadrature.lean + [D]/[E] catalog evaluation + [O] physical Jeans/baryon bridge",
        "formula": "Q_3D(V_rot / sigma_0) = sqrt(((V_rot / sigma_0)^2 + 6) / ((V_rot / sigma_0)^2 + 3))",
        "a0_canonical_SI": A0_CANON,
        "results": res,
    }
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    payload["sha256_body"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    rc_s = res["kinematic_tiers"]["RC100_N100"]
    ms_s = res["kinematic_tiers"]["JWST_MSA3D_N20"]
    wl_s = res["weak_lensing_elliptical_endpoint"]

    md = [
        "# Multi-Tier Evaluation of the 3D Phase-Space Dispersion Quadrature Law $Q_{\\rm 3D}(V_{\\rm rot}/\\sigma_0)$ (2026-11-27)",
        "",
        "**Epistemic Tier:** `[P]` algebraic bounds & endpoint theorems in [`05_lean_formalization/DispersionQuadrature.lean`](../05_lean_formalization/DispersionQuadrature.lean); `[D]`/`[E]` evaluation on `RC100` ($N=100$), `JWST MSA-3D` ($N=20$), and `GAMA/KiDS-Legacy` ($N=45,050$) with no per-galaxy fitted parameters; `[O]` physical covariant Jeans / effective baryon coupling identification.",
        "",
        "## 1. Closed-Form Law & Exact Endpoints (Fixed Phase-Space DoF Ratio: $1$ Azimuthal vs. $3$ Dispersion)",
        "",
        "$$Q_{\\rm 3D}(\\xi) = \\sqrt{1 + \\frac{3}{\\xi^2 + 3}} = \\sqrt{\\frac{\\xi^2 + 6}{\\xi^2 + 3}}, \\qquad \\xi \\equiv \\frac{V_{\\rm rot}}{\\sigma_0} \\in [0, \\infty)$$",
        "",
        "| Physical Regime | $\\xi = V_{\\rm rot}/\\sigma_0$ | $Q_{\\rm 3D}(\\xi)$ | $Q_{\\rm 3D}^2(\\xi)$ | Observational Anchor |",
        "|---|---:|---:|---:|---|",
    ]
    labels_map = {
        15.0: "Ultra-cold thin spiral (`SPARC` high-$V$)",
        12.0: "Cold spiral disk (`SPARC` typical)",
        10.0: "Cold disk `<1.5%` Lean enclosure (`Theorem 10`)",
        8.0: "Warm spiral disk",
        round(math.sqrt(3.0), 4): "Exact equipartition midpoint (`Theorem 9`, $V^2 = 3\\sigma_0^2$)",
        0.0: "Pure dispersion sphere (`Theorem 7`, `GAMA` true ETGs)",
    }
    for row in res["analytic_ladder"]:
        md.append(
            f"| {labels_map.get(row['Vrot_over_sigma0'], '')} | `{row['Vrot_over_sigma0']:.4f}` | "
            f"**`{row['Q_3D']:.4f}`** | `{row['Q_3D_squared']:.4f}` | — |"
        )

    md.extend([
        "",
        "## 2. Per-Galaxy Kinematic Evaluation (`RC100` $N=100$ & `JWST MSA-3D` $N=20$, Fixed Static $a_0$)",
        "",
        "Both constitutive prescriptions are reported side-by-side without selection bias:",
        "- **Prescription I (`g_MOND(Q_3D(xi) * g_bar; a0)` `[O]`):** Effective baryon coupling (identical in form to weak-lensing `Q_ETG`).",
        "- **Prescription II (`Q_3D(xi)^2 * g_MOND(g_bar; a0)` `[O]`):** Direct 3D phase-space virial trace projection.",
        "",
        "| Sample | $N$ | Med $V_{\\rm rot}/\\sigma_0$ (IQR) | Med $Q_{\\rm 3D}(\\xi_i)$ | Thin-Disk `Q=1` `med g_obs/g_pred` (`<z^2>`) | Presc. I `g_MOND(Q_3D g_bar)` `med` (`<z^2>`) | Presc. II `Q_3D^2 g_MOND(g_bar)` `med` (`<z^2>`) |",
        "|---|---:|---:|---:|---|---|---|",
    ])
    for s in (rc_s, ms_s):
        b0 = s["baseline_Q1_thin_disk"]
        p1 = s["prescription_I_baryon_Q3D_xi_O"]
        p2 = s["prescription_II_virial_Q3D_sq_xi_O"]
        md.append(
            f"| `{s['label']}` | `{s['n']}` | `{s['median_Vrot_over_sigma0']:.2f}` (`{s['iqr_Vrot_over_sigma0'][0]:.2f}–{s['iqr_Vrot_over_sigma0'][1]:.2f}`) | "
            f"**`{s['median_Q3D_individual']:.4f}`** | `{b0['median_gobs_over_gpred']:.3f}x` (`{b0['mean_sq_zscore']:.2f}`) | "
            f"`{p1['median_gobs_over_gpred']:.3f}x` (`{p1['mean_sq_zscore']:.2f}`) | "
            f"**`{p2['median_gobs_over_gpred']:.3f}x` (`{p2['mean_sq_zscore']:.2f}`)** |"
        )

    if wl_s:
        md.extend([
            "",
            "## 3. Exact $\\xi \\to 0$ Endpoint Match on `GAMA DR4 / KiDS-Legacy DR5` Weak Lensing (`40.9M` Sources)",
            "",
            f"- For dispersion-supported intrinsic ellipticals ($\\xi = V_{{\\rm rot}}/\\sigma_0 \\to 0$, $N = {wl_s['n_true_ellipticals']:,}$ isolated lenses), $Q_{{\\rm 3D}}(0) = \\sqrt{{2}} = {wl_s['Q_3D_at_xi_0']:.6f}$ reduces ETG weak-lensing $\\chi^2/\\mathrm{{ndof}}$ from `{wl_s['ETG_chi2_ndof_at_Q1']}` ($p = {wl_s['ETG_p_at_Q1']:.3g}$) to **`{wl_s['ETG_chi2_ndof_at_Qsqrt2']}` ($p = {wl_s['ETG_p_at_Qsqrt2']:.3g}$)**, achieving a joint Hartlap **`{wl_s['Joint_Hartlap_verdict_at_Qsqrt2']}`** ($p_{{\\rm H}} = {wl_s['Joint_Hartlap_p_at_Qsqrt2']:.3g}$) while leaving cold spirals ($N = {wl_s['n_true_disks']:,}$) invariant.",
        ])

    md.extend([
        "",
        "## Reproducibility",
        "```bash",
        "/home/mega/.elan/bin/lean 05_lean_formalization/DispersionQuadrature.lean",
        "python3 02_galaxy_dynamics/dispersion_quadrature_audit.py --self-test",
        "python3 02_galaxy_dynamics/dispersion_quadrature_audit.py --run",
        "```",
    ])
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
