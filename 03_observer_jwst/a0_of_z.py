#!/usr/bin/env python3
"""
Pre-Registered Redshift Evolution of Acceleration Scale Test:
H_const (a0 = const) vs H_horizon (a0(z) = xi * c * H(z))

Usage:
  python3 03_observer_jwst/a0_of_z.py [--out REPORT.json] [--data CUSTOM_DATA.json]
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path

# Speed of light [m/s]
C_LIGHT = 2.99792458e8

# Default Planck 2018 cosmological parameters (same as SPARC baseline)
H0_KMS_MPC = 67.4
OMEGA_M = 0.315
OMEGA_LAMBDA = 0.685

# Conversion factor: km/s/Mpc to s^-1
# 1 Mpc = 3.085677581e19 km
MPC_IN_KM = 3.085677581e19
H0_SI = (H0_KMS_MPC) / MPC_IN_KM  # ~ 2.1843e-18 s^-1

# Frozen baseline acceleration from SPARC (A0_MEASUREMENT.json)
A0_SPARC_ZERO = 1.1160351336495208e-10  # m/s^2
XI_FROZEN = A0_SPARC_ZERO / (C_LIGHT * H0_SI)  # ~ 0.170427


def hubble_parameter(z, H0=H0_SI, Om=OMEGA_M, Ol=OMEGA_LAMBDA):
    """Compute H(z) in s^-1 for flat LCDM."""
    ez = math.sqrt(Om * (1.0 + z)**3 + Ol)
    return H0 * ez


def dual_channel_g_pred(g_bar, a0):
    """
    Evaluate predicted gravitational acceleration for mu(x) = x/(1+x).
    g * mu(g/a0) = g_bar  =>  g^2 / (g + a0) = g_bar  =>  g^2 - g_bar*g - g_bar*a0 = 0
    => g = g_bar * [ 1/2 + sqrt(1/4 + a0/g_bar) ]
    """
    if g_bar <= 0:
        return 0.0
    return g_bar * (0.5 + math.sqrt(0.25 + a0 / g_bar))


def load_quarantined_sample():
    """
    QUARANTINED SAMPLE -- UNDOCUMENTED PROVENANCE.

    These 20 rows have no documented acquisition record in the repository
    history: no source table, no retrieval command, no native catalogue
    identifiers, no checksum, and no selection rule. A provenance
    investigation traced their earliest recoverable occurrence to a point 37
    seconds before the commit that introduced them, with no data retrieval
    recorded; the origin before that point could not be determined.

    They are therefore NOT described here as real observational data. They are
    also NOT described as fabricated, synthetic, or placeholder -- no evidence
    establishes any of those labels either. The only supported description is
    "undocumented provenance".

    Consequence: this sample MUST NOT be used for scientific citation,
    significance claims, or claim-level advancement. It is retained solely so
    the harness has a fixed input for deterministic regression testing, and is
    reachable only via the explicit --quarantined-sample flag.

    Accelerations in SI units (m s^-2). See 03_observer_jwst/PROVENANCE.md.
    """
    raw_table = [
        # id, z, log10_gbar [m/s^2], log10_gobs [m/s^2], sigma_log_gobs
        {"id": "udf10_01", "z": 0.413, "log10_gbar": -10.42, "log10_gobs": -10.12, "sigma": 0.08},
        {"id": "udf10_02", "z": 0.468, "log10_gbar": -10.75, "log10_gobs": -10.35, "sigma": 0.09},
        {"id": "udf10_03", "z": 0.521, "log10_gbar": -10.28, "log10_gobs": -10.02, "sigma": 0.07},
        {"id": "udf10_04", "z": 0.578, "log10_gbar": -10.88, "log10_gobs": -10.42, "sigma": 0.10},
        {"id": "udf10_05", "z": 0.622, "log10_gbar": -10.35, "log10_gobs": -10.05, "sigma": 0.08},
        {"id": "udf10_06", "z": 0.684, "log10_gbar": -10.60, "log10_gobs": -10.22, "sigma": 0.09},
        {"id": "udf10_07", "z": 0.748, "log10_gbar": -10.50, "log10_gobs": -10.15, "sigma": 0.08},
        {"id": "udf10_08", "z": 0.812, "log10_gbar": -10.95, "log10_gobs": -10.45, "sigma": 0.11},
        {"id": "udf10_09", "z": 0.845, "log10_gbar": -10.30, "log10_gobs": -9.98,  "sigma": 0.07},
        {"id": "udf10_10", "z": 0.892, "log10_gbar": -10.70, "log10_gobs": -10.28, "sigma": 0.09},
        {"id": "udf10_11", "z": 0.940, "log10_gbar": -10.45, "log10_gobs": -10.08, "sigma": 0.08},
        {"id": "udf10_12", "z": 0.998, "log10_gbar": -10.82, "log10_gobs": -10.32, "sigma": 0.10},
        {"id": "udf10_13", "z": 1.045, "log10_gbar": -10.25, "log10_gobs": -9.92,  "sigma": 0.08},
        {"id": "udf10_14", "z": 1.096, "log10_gbar": -10.65, "log10_gobs": -10.20, "sigma": 0.09},
        {"id": "udf10_15", "z": 1.150, "log10_gbar": -10.38, "log10_gobs": -10.00, "sigma": 0.08},
        {"id": "udf10_16", "z": 1.215, "log10_gbar": -10.78, "log10_gobs": -10.28, "sigma": 0.10},
        {"id": "udf10_17", "z": 1.282, "log10_gbar": -10.55, "log10_gobs": -10.12, "sigma": 0.09},
        {"id": "udf10_18", "z": 1.340, "log10_gbar": -10.90, "log10_gobs": -10.38, "sigma": 0.11},
        {"id": "udf10_19", "z": 1.411, "log10_gbar": -10.48, "log10_gobs": -10.04, "sigma": 0.09},
        {"id": "udf10_20", "z": 1.440, "log10_gbar": -10.72, "log10_gobs": -10.22, "sigma": 0.10},
    ]

    points = []
    for r in raw_table:
        g_bar = 10.0 ** r["log10_gbar"]
        g_obs = 10.0 ** r["log10_gobs"]
        # Error propagation for log10: sigma_g / g = ln(10) * sigma_log10
        sigma_g = g_obs * math.log(10.0) * r["sigma"]
        points.append({
            "id": r["id"],
            "z": r["z"],
            "g_bar": g_bar,
            "g_obs": g_obs,
            "sigma_g": sigma_g,
            "log10_gbar": r["log10_gbar"],
            "log10_gobs": r["log10_gobs"],
            "provenance": "undocumented",
        })
    return points


def evaluate_hypotheses(points):
    """Evaluate H_const and H_horizon against kinematic points."""
    chi2_const = 0.0
    chi2_horizon = 0.0
    sep_S = 0.0

    residuals_const = []
    residuals_horizon = []

    for p in points:
        z = p["z"]
        g_bar = p["g_bar"]
        g_obs = p["g_obs"]
        sig = p["sigma_g"]

        # H_const prediction: a0 fixed at SPARC z=0 measurement
        a0_c = A0_SPARC_ZERO
        g_pred_c = dual_channel_g_pred(g_bar, a0_c)
        res_c = (g_obs - g_pred_c) / sig
        chi2_c_pt = res_c ** 2
        chi2_const += chi2_c_pt
        residuals_const.append(chi2_c_pt)

        # H_horizon prediction: a0(z) = xi * c * H(z)
        Hz = hubble_parameter(z)
        a0_h = XI_FROZEN * C_LIGHT * Hz
        g_pred_h = dual_channel_g_pred(g_bar, a0_h)
        res_h = (g_obs - g_pred_h) / sig
        chi2_h_pt = res_h ** 2
        chi2_horizon += chi2_h_pt
        residuals_horizon.append(chi2_h_pt)

        # Separation term for the closed-form significance (see below).
        sep_S += ((g_pred_h - g_pred_c) / sig) ** 2

    n_pts = len(points)
    delta_chi2 = chi2_const - chi2_horizon

    # Median and Mean per point
    sorted_c = sorted(residuals_const)
    sorted_h = sorted(residuals_horizon)
    median_chi2_c = sorted_c[n_pts // 2]
    median_chi2_h = sorted_h[n_pts // 2]
    mean_chi2_c = chi2_const / n_pts
    mean_chi2_h = chi2_horizon / n_pts

    # ---- Closed-form significance for two FULLY SPECIFIED hypotheses ----
    # Both H_const and H_horizon are fixed before this comparison: xi is frozen
    # at z=0 and mu(x) is frozen. ZERO parameters are re-fitted here. Wilks's
    # theorem therefore does NOT apply and delta_chi2 is not chi2_1 distributed.
    #
    # Because both models are fully specified, delta_chi2 is LINEAR in the data
    # and hence exactly Gaussian. With S = sum ((g_h - g_c)/sigma)^2:
    #     under H_const   : mean(delta_chi2) = -S,  sd = 2*sqrt(S)
    #     under H_horizon : mean(delta_chi2) = +S,  sd = 2*sqrt(S)
    # so the significance against a hypothesis is (delta_chi2 - mean)/(2 sqrt(S)).
    #
    # NOTE: the superseded shortcut sqrt(|delta_chi2|) is not a significance for
    # non-nested, zero-refitted-parameter models. It can happen to land close to
    # the correct value when the data sit near one hypothesis, but it does not
    # generalise and is not used here.
    #
    # CAVEAT: this expression does NOT yet propagate the frozen-a0 uncertainty,
    # measurement covariance, or selection effects. See Gate 2.
    if sep_S > 0.0:
        sd = 2.0 * math.sqrt(sep_S)
        z_vs_const = (delta_chi2 - (-sep_S)) / sd
        z_vs_horizon = (delta_chi2 - (sep_S)) / sd
        max_separation_sigma = math.sqrt(sep_S)
    else:
        z_vs_const = 0.0
        z_vs_horizon = 0.0
        max_separation_sigma = 0.0

    # Statistical comparison decision (harness behaviour; not an observational claim)
    if delta_chi2 >= 9.0:
        verdict = "H_horizon better describes this input than H_const (delta_chi2 >= 9.0)"
        favoured = "H_horizon"
        disfavoured = "H_const"
    elif delta_chi2 <= -9.0:
        verdict = "H_const better describes this input than H_horizon (delta_chi2 <= -9.0)"
        favoured = "H_const"
        disfavoured = "H_horizon"
    else:
        verdict = "Inconclusive at the pre-registered threshold (|delta_chi2| < 9.0)"
        favoured = "none"
        disfavoured = "none"

    return {
        "n_points": n_pts,
        "n_galaxies": len(set(p["id"] for p in points)),
        "z_min": min(p["z"] for p in points),
        "z_max": max(p["z"] for p in points),
        "z_median": sorted([p["z"] for p in points])[n_pts // 2],
        "chi2_H_const": chi2_const,
        "chi2_H_horizon": chi2_horizon,
        "delta_chi2_Hconst_minus_Hhorizon": delta_chi2,
        "separation_S": sep_S,
        "max_attainable_separation_sigma": max_separation_sigma,
        "z_vs_H_const_conditional": z_vs_const,
        "z_vs_H_horizon_conditional": z_vs_horizon,
        "median_chi2_pt_Hconst": median_chi2_c,
        "median_chi2_pt_Hhorizon": median_chi2_h,
        "mean_chi2_pt_Hconst": mean_chi2_c,
        "mean_chi2_pt_Hhorizon": mean_chi2_h,
        "better_fitting_hypothesis_on_this_input": favoured,
        "worse_fitting_hypothesis_on_this_input": disfavoured,
        "verdict": verdict,
        "verdict_scope": ("Describes how the harness scores two fixed hypotheses "
                          "against the supplied input. NOT an exclusion of any "
                          "hypothesis about the universe.")
    }


def main():
    parser = argparse.ArgumentParser(description="Pre-registered high-z a0(z) hypothesis test")
    parser.add_argument("--out", type=str, default="03_observer_jwst/A0_OF_Z_REPORT.json", help="Output JSON report path")
    parser.add_argument("--data", type=str, default="", help="Input JSON data file (required unless --quarantined-sample)")
    parser.add_argument("--quarantined-sample", action="store_true",
                        help=("Run against the retained 20-row sample of UNDOCUMENTED PROVENANCE. "
                              "For deterministic regression testing only. Results carry no "
                              "observational meaning. See 03_observer_jwst/PROVENANCE.md."))
    args = parser.parse_args()

    if not args.data and not args.quarantined_sample:
        parser.error(
            "No input specified.\n"
            "  --data PATH             run on a provenance-documented dataset (see PROVENANCE.md), or\n"
            "  --quarantined-sample    run on the retained undocumented-provenance sample\n"
            "                          (regression testing only; not an observational result)."
        )

    repo_root = Path(__file__).resolve().parent.parent

    if args.data:
        data_path = Path(args.data)
        if not data_path.is_absolute():
            data_path = repo_root / data_path
        with open(data_path, "r", encoding="utf-8") as f:
            points = json.load(f)
    else:
        points = load_quarantined_sample()
        sys.stderr.write(
            "WARNING: running on the QUARANTINED sample (undocumented provenance).\n"
            "         Output is a harness reproduction check, not evidence about the universe.\n"
        )

    if len(points) < 5:
        report = {
            "status": "insufficient",
            "n_points": len(points),
            "reason": "Fewer than 5 kinematic points provided",
            "shopping_list": [
                "VLT/MUSE 3D datacubes for 20+ disk galaxies at z=0.5-1.5",
                "JWST/NIRSpec IFU kinematics for star-forming disks at z > 1.5",
                "Resolved baryonic mass profiles (gas + stars) at matching resolution"
            ]
        }
    else:
        results = evaluate_hypotheses(points)
        report = {
            "status": "completed",
            "protocol": "PREREG_A0_OF_Z.md",
            "epistemic_classification": "[O] D0_PROPOSED",
            "result_type": ("conditional" if args.quarantined_sample else "observational_candidate"),
            "data_provenance": ("undocumented" if args.quarantined_sample else "see PROVENANCE.md"),
            "interpretation": (
                "Harness reproduction check on an input of undocumented provenance. "
                "This is NOT evidence about the universe and MUST NOT be cited, "
                "quoted as a significance, or used to advance any claim level."
                if args.quarantined_sample else
                "Conditional on the supplied dataset; see PROVENANCE.md and Gate 2 caveats."
            ),
            "gate_status": {
                "gate_1_provenance": ("NOT MET" if args.quarantined_sample else "see PROVENANCE.md"),
                "gate_2_inference": "PARTIAL - closed-form statistic only; a0 uncertainty, covariance, selection not yet propagated"
            },
            "preregistered_parameters": {
                "H0_kms_mpc": H0_KMS_MPC,
                "omega_m": OMEGA_M,
                "omega_lambda": OMEGA_LAMBDA,
                "mu_function": "x / (1 + x)",
                "a0_sparc_zero_ms2": A0_SPARC_ZERO,
                "xi_frozen": XI_FROZEN,
                "no_nfw_parameters": True
            },
            "preregistered_predictions": {
                "z_0_0": A0_SPARC_ZERO,
                "z_0_5": XI_FROZEN * C_LIGHT * hubble_parameter(0.5),
                "z_1_0": XI_FROZEN * C_LIGHT * hubble_parameter(1.0),
                "z_1_5": XI_FROZEN * C_LIGHT * hubble_parameter(1.5),
                "z_2_0": XI_FROZEN * C_LIGHT * hubble_parameter(2.0)
            },
            "dataset": {
                "source": ("undocumented provenance - see 03_observer_jwst/PROVENANCE.md"
                           if args.quarantined_sample else args.data),
                "n_galaxies": results["n_galaxies"],
                "n_kinematic_points": results["n_points"],
                "redshift_range": [results["z_min"], results["z_max"]],
                "redshift_median": results["z_median"]
            },
            "hypothesis_test_results": results
        }

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = repo_root / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to: {out_path}")
    print(f"Sample: N = {report['dataset']['n_kinematic_points']} points across {report['dataset']['n_galaxies']} galaxies (z = {results['z_min']} - {results['z_max']})")
    print(f"chi2(H_const)   = {results['chi2_H_const']:.3f} (median/pt: {results['median_chi2_pt_Hconst']:.3f})")
    print(f"chi2(H_horizon) = {results['chi2_H_horizon']:.3f} (median/pt: {results['median_chi2_pt_Hhorizon']:.3f})")
    print(f"Delta chi2 (H_const - H_horizon) = {results['delta_chi2_Hconst_minus_Hhorizon']:+.3f}")
    print(f"Separation S = {results['separation_S']:.3f} "
          f"(max attainable {results['max_attainable_separation_sigma']:.2f} sigma)")
    print(f"Conditional z vs H_const   = {results['z_vs_H_const_conditional']:+.2f}")
    print(f"Conditional z vs H_horizon = {results['z_vs_H_horizon_conditional']:+.2f}")
    print(f"Verdict: {results['verdict']}")
    if args.quarantined_sample:
        print("SCOPE: conditional harness output on undocumented-provenance input; "
              "not evidence about the universe.")


if __name__ == "__main__":
    main()
