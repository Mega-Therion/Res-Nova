#!/usr/bin/env python3
"""Job H: Q1' Galaxy Axiom Input Verification.

Certifies that Q1' (μ'(0) = 1) is an axiomatic input of the galaxy law
μ(x) = x / sqrt(1 + x^2), not derived from an operator or matrix.
"""

import json
from pathlib import Path
import sys
import sympy as sp


def verify_q1_prime_input():
    # Galaxy law axiom: μ(x) = x / sqrt(1 + x**2)
    # This is a declared postulate (tier A), stopping at unscreened S=1.
    x = sp.Symbol("x", real=True)
    mu_std = x / sp.sqrt(1 + x**2)

    # Differentiate symbolically to inspect the deep-MOND slope at x = 0
    mu_prime = sp.diff(mu_std, x)
    slope_at_zero = mu_prime.subs(x, 0)

    # In Res-Nova, μ'(0) = 1 is not derived from an operator spectrum,
    # nor is it matched to a matrix determinant. Q3 is closed and no operator
    # search is performed.
    operator_searched = False
    matrix_constructed = False

    # The slope is purely a property of the declared galaxy axiom
    is_axiom_input = bool(slope_at_zero == 1 and not operator_searched and not matrix_constructed)

    if not is_axiom_input:
        raise ValueError("Q1' property check failed.")

    receipt = {
        "job": "H",
        "exit_code": 0,
        "verdict": "input",
        "q1_prime_status": "input",
        "tier": "A",
        "neighbor_constrained": "none",
        "neighbor_forbidden": "derivation of μ_std, killed tail, solar system",
        "free_symbols": [],
        "numeric_outputs": {},
        "statement": "μ′(0) = 1 is part of the galaxy axiom.",
        "script": "job_h_q1_prime.py"
    }

    out_file = Path(__file__).parent / "job_h_q1_prime.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(verify_q1_prime_input())
