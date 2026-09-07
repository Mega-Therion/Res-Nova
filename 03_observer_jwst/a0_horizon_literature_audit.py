#!/usr/bin/env python3
"""Audit the horizon-tied a0 prediction against a published RAR evolution summary.

This is a cited-summary audit, not a re-analysis of the MUSE data. The published
paper reports a0(z~1), a linear slope a1, and the redshift interval. We compute
the Res-Nova horizon prediction from the repository's frozen z=0 a0 and compare
central values and local slopes. The output remains [C]+[D], not [P].
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

C_LIGHT = 299_792_458.0
H0_KMS_MPC = 67.4
OMEGA_M = 0.315
OMEGA_LAMBDA = 0.685
A0_LOCAL = 1.1160351336495209e-10
# Published MUSE-DARK III summary values; uncertainties are quoted 95% CIs.
MUSE_A0_Z1 = 2.38e-10
MUSE_A0_Z1_LO = 0.10e-10
MUSE_A0_Z1_HI = 0.12e-10
MUSE_A1 = 1.59e-10
MUSE_A1_LO = 0.10e-10
MUSE_A1_HI = 0.11e-10


def h0_si() -> float:
    """Convert H0 from km/s/Mpc to s^-1."""
    # One megaparsec in metres; H0 is supplied in km s^-1 Mpc^-1.
    mpc_m = 3.0856775814913673e22
    return H0_KMS_MPC * 1000.0 / mpc_m


def hubble_ratio(z: float) -> float:
    return math.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_LAMBDA)


def horizon_a0(z: float) -> float:
    xi = A0_LOCAL / (C_LIGHT * h0_si())
    return xi * C_LIGHT * h0_si() * hubble_ratio(z)


def horizon_slope_at_zero() -> float:
    # dH/dz at z=0 for flat LambdaCDM, multiplied by xi*c.
    return A0_LOCAL * 1.5 * OMEGA_M


def build_report() -> dict[str, object]:
    pred_z1 = horizon_a0(1.0)
    central_difference = MUSE_A0_Z1 - pred_z1
    slope_ratio = MUSE_A1 / horizon_slope_at_zero()
    return {
        "status": "completed_literature_audit",
        "epistemic_classification": "[C]+[D] cited summary plus deterministic derived comparison; not a raw-data reanalysis",
        "question": "Does current intermediate-redshift evidence support the exact horizon law a0(z)=xi*c*H(z)?",
        "frozen_res_nova_inputs": {
            "a0_local_m_s2": A0_LOCAL,
            "H0_km_s_Mpc": H0_KMS_MPC,
            "omega_m": OMEGA_M,
            "omega_lambda": OMEGA_LAMBDA,
            "xi": A0_LOCAL / (C_LIGHT * h0_si()),
        },
        "published_muse_dark_iii_summary": {
            "sample_size_galaxies": 79,
            "redshift_range": [0.33, 1.44],
            "a0_z1_m_s2": MUSE_A0_Z1,
            "a0_z1_95ci_minus_m_s2": MUSE_A0_Z1_LO,
            "a0_z1_95ci_plus_m_s2": MUSE_A0_Z1_HI,
            "linear_slope_a1_m_s2_per_z": MUSE_A1,
            "a1_95ci_minus_m_s2_per_z": MUSE_A1_LO,
            "a1_95ci_plus_m_s2_per_z": MUSE_A1_HI,
            "source_doi": "10.1051/0004-6361/202659230",
            "source_url": "https://doi.org/10.1051/0004-6361/202659230",
        },
        "horizon_prediction": {
            "a0_z1_m_s2": pred_z1,
            "local_slope_at_z0_m_s2_per_z": horizon_slope_at_zero(),
        },
        "derived_comparison": {
            "central_difference_m_s2": central_difference,
            "central_ratio_muse_to_horizon_at_z1": MUSE_A0_Z1 / pred_z1,
            "published_slope_to_horizon_local_slope_ratio": slope_ratio,
            "interpretation": "The cited summary reports positive evolution, but its central slope is substantially faster than the exact flat-LambdaCDM horizon law. This disfavors the exact horizon scaling as a phenomenological description; it does not derive or falsify the underlying action.",
        },
        "limitations": [
            "The MUSE-DARK III paper reports model-derived accelerations, not a repository-vendored raw point table.",
            "The comparison uses published summary values and does not propagate correlated systematics or refit the 79-galaxy sample.",
            "The result addresses the exact a0 proportional to H(z) law, not every possible horizon-inspired model.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("03_observer_jwst/A0_HORIZON_LITERATURE_AUDIT.json"))
    args = parser.parse_args()
    report = build_report()
    out = args.out if args.out.is_absolute() else Path(__file__).resolve().parents[1] / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["derived_comparison"], indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
