#!/usr/bin/env python3
"""UFW-C0 exact rapidity-identity audit.

This validates only the specified hyperbolic identities. It does not assert
that Kerr spin is a Lorentz rapidity or that sinh(psi)=1 is physically selected.
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
OUTPUT = Path(__file__).with_name("rapidity_uniqueness_results.json")


def sha256(path: Path) -> str:
    if path.exists():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return "0" * 64


def main() -> None:
    theta = sp.sqrt(2) / 2
    psi0 = sp.asinh(1)
    expected_psi0 = sp.log(1 + sp.sqrt(2))
    # Use exact rational logarithmic identities on the positive real branch.
    # This avoids treating a CAS branch-simplification limitation as a failed identity.
    t = 1 + sp.sqrt(2)
    atanh_ratio = sp.simplify((1 + theta) / (1 - theta))
    atanh_theta_log_form = sp.log(atanh_ratio) / 2
    checks = {
        "sinh_asinh_one": sp.simplify((t - 1 / t) / 2 - 1),
        "asinh_one_log_form": sp.simplify(psi0 - expected_psi0),
        "tanh_asinh_one": sp.simplify((t**2 - 1) / (t**2 + 1) - theta),
        "atanh_ratio_equals_square": sp.simplify(atanh_ratio - t**2),
        "positive_branch_log_square": sp.simplify(sp.expand_log(sp.log(t**2), force=True) / 2 - sp.log(t)),
        "inverse_coordinate": sp.simplify(sp.tanh(sp.atanh(sp.Symbol("a", positive=True))) - sp.Symbol("a", positive=True)),
        "silver_ratio_odds": sp.simplify(theta / (1 - theta) - (1 + sp.sqrt(2))),
    }
    symbolic_pass = all(value == 0 for value in checks.values())

    mp.mp.dps = 100
    theta_mp = 1 / mp.sqrt(2)
    psi_mp = mp.asinh(1)
    residuals = {
        "sinh_psi_minus_1": abs(mp.sinh(psi_mp) - 1),
        "psi_minus_log": abs(psi_mp - mp.log(1 + mp.sqrt(2))),
        "tanh_psi_minus_theta": abs(mp.tanh(psi_mp) - theta_mp),
        "atanh_theta_minus_psi": abs(mp.atanh(theta_mp) - psi_mp),
        "odds_minus_silver": abs(theta_mp / (1 - theta_mp) - (1 + mp.sqrt(2))),
    }
    numeric_pass = all(residual < mp.mpf("1e-70") for residual in residuals.values())

    result = {
        "model_id": "UFW-C0",
        "gate": "UFW-MATH-01 rapidity identities",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "precision_decimal_digits": 100,
        "definitions": {
            "a_star_coordinate_domain": "0 <= a_star < 1",
            "psi": "atanh(a_star)",
            "adopted_balance_premise": "sinh(psi_0) = 1",
            "theta_amplitude": "1/sqrt(2)",
        },
        "exact_values": {
            "psi_0": str(psi0),
            "psi_0_log_form": str(expected_psi0),
            "theta": str(theta),
            "silver_ratio": str(1 + sp.sqrt(2)),
        },
        "symbolic_residuals": {key: str(value) for key, value in checks.items()},
        "numeric_residuals_100_dps": {key: mp.nstr(value, 8) for key, value in residuals.items()},
        "symbolic_pass": symbolic_pass,
        "numeric_pass": numeric_pass,
        "algebra_status": "CONDITIONAL PASS" if symbolic_pass and numeric_pass else "FAIL",
        "physical_selection_status": "NOT DERIVED",
        "physical_selection_reason": "The identities require the adopted coordinate psi=atanh(a_star) and adopted condition sinh(psi)=1. No covariant Kerr or framework action, observer/tetrad construction, or conservation law selecting this condition is supplied.",
        "input_hashes": {"protocol": sha256(PROTOCOL)},
        "script_hash": sha256(Path(__file__)),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "algebra_status": result["algebra_status"],
        "physical_selection_status": result["physical_selection_status"],
        "exact_values": result["exact_values"],
        "numeric_residuals_100_dps": result["numeric_residuals_100_dps"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
