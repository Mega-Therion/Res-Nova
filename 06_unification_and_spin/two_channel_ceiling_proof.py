#!/usr/bin/env python3
"""UFW-C0 exact two-channel algebra audit.

This checks the stated inclusion-exclusion identity under the explicit
independent-Bernoulli premise. It does not derive physical channels or an
astrophysical spin ceiling.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parent
PROTOCOL = ROOT / "README.md"
OUTPUT = Path(__file__).with_name("two_channel_ceiling_results.json")


def sha256(path: Path) -> str:
    if path.exists():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return "0" * 64


def main() -> None:
    theta = sp.sqrt(2) / 2
    union_probability = sp.simplify(1 - (1 - theta) ** 2)
    expected_union = sp.sqrt(2) - sp.Rational(1, 2)
    chi = sp.sqrt(union_probability)
    expected_chi = sp.sqrt(sp.sqrt(2) - sp.Rational(1, 2))
    gate_mean = sp.simplify((sp.log(2) + theta) / 2)

    checks = {
        "union_equals_2theta_minus_theta_squared": sp.simplify(union_probability - (2 * theta - theta**2)),
        "union_exact_value": sp.simplify(union_probability - expected_union),
        "chi_exact_value": sp.simplify(chi - expected_chi),
        "gate_mean_exact_expression": sp.simplify(gate_mean - (sp.log(2) + sp.sqrt(2) / 2) / 2),
    }
    symbolic_pass = all(value == 0 for value in checks.values())

    mp.mp.dps = 100
    theta_mp = 1 / mp.sqrt(2)
    union_mp = 1 - (1 - theta_mp) ** 2
    chi_mp = mp.sqrt(union_mp)
    gate_mp = (mp.log(2) + theta_mp) / 2
    residuals = {
        "union_exact_residual": abs(union_mp - (mp.sqrt(2) - mp.mpf("0.5"))),
        "chi_exact_residual": abs(chi_mp - mp.sqrt(mp.sqrt(2) - mp.mpf("0.5"))),
    }
    numeric_pass = all(residual < mp.mpf("1e-70") for residual in residuals.values())

    result = {
        "model_id": "UFW-C0",
        "gate": "UFW-MATH-02 two-channel union algebra",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "event_premise": {
            "sample_space": "adopted abstract Bernoulli space",
            "events": ["A", "B"],
            "marginals": "P(A)=P(B)=1/sqrt(2)",
            "independence": "P(A intersection B)=P(A)P(B)",
            "physical_event_mapping_supplied": False,
        },
        "exact_values": {
            "theta": str(theta),
            "union_probability": str(union_probability),
            "chi_s": str(chi),
            "gate_arithmetic_mean": str(gate_mean),
        },
        "numerical_values_100_dps": {
            "union_probability": mp.nstr(union_mp, 30),
            "chi_s": mp.nstr(chi_mp, 30),
            "gate_arithmetic_mean": mp.nstr(gate_mp, 30),
        },
        "symbolic_residuals": {key: str(value) for key, value in checks.items()},
        "numeric_residuals_100_dps": {key: mp.nstr(value, 8) for key, value in residuals.items()},
        "symbolic_pass": symbolic_pass,
        "numeric_pass": numeric_pass,
        "algebra_status": "CONDITIONAL PASS" if symbolic_pass and numeric_pass else "FAIL",
        "physical_spin_ceiling_status": "NOT DERIVED",
        "physical_spin_ceiling_reason": "No physical probability space, two identified horizon events, independence derivation, or map from union probability to Kerr stress-energy flux is supplied. The two standard accretion contributions are fluxes, not automatically Bernoulli events.",
        "notation_conflict": "The blueprint's theta_amplitude=1/sqrt(2) differs from the current corpus convention that reserves theta=0.7 for a gate probability and 1/sqrt(2) for an amplitude-like quantity.",
        "input_hashes": {"protocol": sha256(PROTOCOL)},
        "script_hash": sha256(Path(__file__)),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "algebra_status": result["algebra_status"],
        "physical_spin_ceiling_status": result["physical_spin_ceiling_status"],
        "exact_values": result["exact_values"],
        "numerical_values_100_dps": result["numerical_values_100_dps"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
