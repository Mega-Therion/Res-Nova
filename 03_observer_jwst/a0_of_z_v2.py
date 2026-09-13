#!/usr/bin/env python3
"""
V2 Pre-Registered Redshift Evolution of Acceleration Scale Test:
H_const (a0 = const) vs H_horizon (a0(z) = xi * c * H(z))

CHANGES FROM V1 (PREREG_A0_OF_Z.md, immutable):
  - Frozen interpolating function: mu(x) = x / sqrt(1 + x^2)   [mu_std]
    V1 froze mu(x) = x/(1+x) [mu_dual], falsified 2026-09-12 (TARGET_D7 sec 4/11).
  - Everything else identical: same 20 MUSE-DARK/HUDF points, same cosmology
    (Planck 2018), same frozen a0(0) = SPARC baseline, same xi = a0(0)/(c H0),
    same 3-sigma delta-chi2 threshold, no NFW parameters.

Usage:
  python3 a0_of_z_v2.py [--out REPORT.json] [--validate] [--scan]
    --validate  reproduce the V1 mu_dual numbers first (must match A0_OF_Z_REPORT.json)
    --scan      sensitivity: a0(0) varied +/-30% (xi co-scaled) under mu_std
"""

import json
import math
import argparse
from pathlib import Path

C_LIGHT = 2.99792458e8
H0_KMS_MPC = 67.4
H0_SI = H0_KMS_MPC * 1000.0 / 3.0857e22   # s^-1
OMEGA_M, OMEGA_LAMBDA = 0.315, 0.685
A0_SPARC_ZERO = 1.1160351336495208e-10     # m/s^2 (frozen from SPARC baseline)
XI_FROZEN = A0_SPARC_ZERO / (C_LIGHT * H0_SI)  # ~0.170427

# --- V1 prediction for validation only (falsified mu_dual) ---
def dual_channel_g_pred(g_bar, a0):
    if g_bar <= 0: return 0.0
    return g_bar * (0.5 + math.sqrt(0.25 + a0 / g_bar))

# --- V2 prediction: mu_std(x) = x / sqrt(1+x^2) ---
def mu_std_g_pred(g_bar, a0):
    """g * mu_std(g/a0) = g_bar  =>  g^2 / sqrt(a0^2 + g^2) = g_bar
    => g^4 - g_bar^2 g^2 - g_bar^2 a0^2 = 0  (quartic in g, quadratic in u = g^2)
    u = [g_bar^2 + sqrt(g_bar^4 + 4 g_bar^2 a0^2)] / 2,  g = sqrt(u)
    Checks: g_bar >> a0 -> g -> g_bar;  g_bar << a0 -> g -> sqrt(g_bar a0)."""
    if g_bar <= 0: return 0.0
    u = 0.5 * (g_bar**2 + math.sqrt(g_bar**4 + 4.0 * g_bar**2 * a0**2))
    return math.sqrt(u)

def hubble_parameter(z, H0=H0_SI, Om=OMEGA_M, Ol=OMEGA_LAMBDA):
    return H0 * math.sqrt(Om * (1.0 + z)**3 + Ol)

def load_muse_dark_published_sample():
    raw_table = [
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
        g_bar, g_obs = 10.0**r["log10_gbar"], 10.0**r["log10_gobs"]
        points.append({"id": r["id"], "z": r["z"], "g_bar": g_bar, "g_obs": g_obs,
                       "sigma_g": g_obs * math.log(10.0) * r["sigma"]})
    return points

def evaluate(points, g_pred):
    chi2_c = chi2_h = 0.0
    for p in points:
        sig = p["sigma_g"]
        chi2_c += ((p["g_obs"] - g_pred(p["g_bar"], A0_SPARC_ZERO)) / sig)**2
        a0_h = XI_FROZEN * C_LIGHT * hubble_parameter(p["z"])
        chi2_h += ((p["g_obs"] - g_pred(p["g_bar"], a0_h)) / sig)**2
    d = chi2_c - chi2_h
    if d <= -9.0:   favoured, verdict = "H_const", "H_const favoured over H_horizon at >= 3 sigma"
    elif d >= 9.0:  favoured, verdict = "H_horizon", "H_horizon favoured over H_const at >= 3 sigma"
    else:           favoured, verdict = "none", "Inconclusive at 3 sigma threshold"
    return {"chi2_H_const": chi2_c, "chi2_H_horizon": chi2_h,
            "delta_chi2": d, "sigma": math.sqrt(abs(d)),
            "favoured": favoured, "verdict": verdict}

def evaluate_scaled(points, g_pred, a0_scale):
    """a0(0) scaled; xi co-scaled (xi = a0(0)/(c H0) is definition)."""
    global A0_SPARC_ZERO, XI_FROZEN
    A0_SPARC_ZERO = 1.1160351336495208e-10 * a0_scale
    XI_FROZEN = A0_SPARC_ZERO / (C_LIGHT * H0_SI)
    r = evaluate(points, g_pred)
    A0_SPARC_ZERO = 1.1160351336495208e-10
    XI_FROZEN = A0_SPARC_ZERO / (C_LIGHT * H0_SI)
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="A0_OF_Z_REPORT_V2.json")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--scan", action="store_true")
    args = ap.parse_args()
    points = load_muse_dark_published_sample()

    v1 = evaluate(points, dual_channel_g_pred)
    print(f"[mu_dual reproduction] chi2_c={v1['chi2_H_const']:.4f} chi2_h={v1['chi2_H_horizon']:.4f} dchi2={v1['delta_chi2']:.4f} sigma={v1['sigma']:.3f} favoured={v1['favoured']}")
    V1_EXPECTED = (5.371260049053887, 40.48609806449993)
    ok = abs(v1["chi2_H_const"] - V1_EXPECTED[0]) < 1e-6 and abs(v1["chi2_H_horizon"] - V1_EXPECTED[1]) < 1e-6
    print(f"  validation vs A0_OF_Z_REPORT.json: {'EXACT MATCH' if ok else 'MISMATCH'}")
    assert ok, "V1 reproduction failed - harness error"

    v2 = evaluate(points, mu_std_g_pred)
    print(f"\n[mu_std V2 RESULT]  chi2_c={v2['chi2_H_const']:.4f} chi2_h={v2['chi2_H_horizon']:.4f} dchi2={v2['delta_chi2']:.4f} sigma={v2['sigma']:.3f} favoured={v2['favoured']}")

    scan = []
    if args.scan:
        print("\n[sensitivity: a0(0) scaled +/-30%, xi co-scaled, mu_std]")
        for s in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3):
            r = evaluate_scaled(points, mu_std_g_pred, s)
            scan.append({"a0_scale": s, "chi2_c": r["chi2_H_const"], "chi2_h": r["chi2_H_horizon"], "dchi2": r["delta_chi2"], "favoured": r["favoured"]})
            print(f"  a0 x{s:.1f}: dchi2={r['delta_chi2']:+8.3f}  {r['favoured']}")

    report = {
        "status": "completed",
        "protocol": "PREREG_A0_OF_Z_V2.md",
        "epistemic_classification": "[D] Computed Empirical Benchmark",
        "supersedes": "A0_OF_Z_REPORT.json (extracted under falsified mu_dual)",
        "preregistered_parameters": {
            "H0_kms_mpc": H0_KMS_MPC, "omega_m": OMEGA_M, "omega_lambda": OMEGA_LAMBDA,
            "mu_function": "x / sqrt(1 + x^2)",
            "a0_sparc_zero_ms2": 1.1160351336495208e-10,
            "xi_frozen": 1.1160351336495208e-10 / (C_LIGHT * H0_SI),
            "no_nfw_parameters": True,
            "v1_reproduction_validated": ok,
        },
        "v1_reproduction": {"chi2_H_const": v1["chi2_H_const"], "chi2_H_horizon": v1["chi2_H_horizon"],
                            "delta_chi2": v1["delta_chi2"], "sigma": v1["sigma"], "favoured": v1["favoured"]},
        "hypothesis_test_results": v2,
        "a0_sensitivity_scan": scan,
        "dataset": {"source": "Published MUSE-DARK III / HUDF (Bouche+2021 / Mercier+2022)",
                    "n_galaxies": 20, "n_kinematic_points": 20,
                    "redshift_range": [0.413, 1.44], "redshift_median": 0.94},
    }
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport written to: {args.out}")

if __name__ == "__main__":
    main()
