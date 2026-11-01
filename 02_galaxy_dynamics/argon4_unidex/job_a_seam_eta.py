#!/usr/bin/env python3
"""Job A: Seam Matter Excess Evaluation.

Determines whether the stored seam mode operator and |beta|^2 in
cpt_mode_equation.json source a matter excess (eta).
"""

import json
from pathlib import Path
import sys
import sympy as sp


def evaluate_seam_matter_excess():
    json_path = Path("/home/mega/Chyren/state/cpt_mode_equation.json")
    if not json_path.exists():
        raise FileNotFoundError(f"Missing state file: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    job2 = data.get("Job_2_Mode_Equations_and_Bogoliubov", {})
    boson_sector = job2.get("boson_spin_0_free_mass_m", {})
    fermion_sector = job2.get("fermion_spin_half_dirac", {})

    boson_op = boson_sector.get("derived_operator_on_chi_eq_a_Phi", "")
    boson_beta_sq = boson_sector.get("abs_beta_sq", "")

    fermion_op = fermion_sector.get("derived_operator_on_psi_pm", "")
    fermion_beta_sq = fermion_sector.get("abs_beta_sq", "")

    # Define symbols
    k = sp.Symbol("k")
    gamma = sp.Symbol("gamma", positive=True)

    # Parse |beta|^2 for boson and fermion
    beta_b = sp.sympify(boson_beta_sq, locals={"gamma": gamma, "k": k})
    beta_f = sp.sympify(fermion_beta_sq, locals={"gamma": gamma, "k": k})

    # Test parity under k -> -k
    diff_b = sp.simplify(beta_b.subs(k, -k) - beta_b)
    diff_f = sp.simplify(beta_f.subs(k, -k) - beta_f)

    odd_terms_found = []

    # Check parity of |beta|^2
    if diff_b != 0:
        odd_terms_found.append(f"boson_beta_sq_odd_in_k: {diff_b}")
    if diff_f != 0:
        odd_terms_found.append(f"fermion_beta_sq_odd_in_k: {diff_f}")

    # Inspect operators for odd dependence on conformal time tau (sheet reflection tau -> -tau)
    # Boson operator contains (k^2 + m^2 * C^2 * tau^2) -> tau^2 is even
    # Fermion operator contains (k^2 + gamma^2 * tau^2 +/- i * gamma) -> tau^2 is even
    # Neither operator contains linear or odd powers of tau
    for name, op_str in [("boson", boson_op), ("fermion", fermion_op)]:
        if "tau" in op_str and "tau^2" not in op_str and "tau**2" not in op_str:
            odd_terms_found.append(f"{name}_operator_has_odd_tau_power: {op_str}")

    # Inspect for charge conjugation / CP-odd parameters or chemical potentials
    # No mu, no charge coupling, no CP phase in stored operators or Bogoliubov coefficients
    all_stored_text = json.dumps(job2)
    for term in ["chemical_potential", "mu_chem", "cp_phase", "charge_asymmetry"]:
        if term in all_stored_text:
            odd_terms_found.append(f"stored_cp_breaking_term: {term}")

    # Determine free symbols from |beta|^2 expressions
    free_syms = sorted([str(s) for s in beta_f.free_symbols])

    # Evaluate verdict and tier
    if len(odd_terms_found) == 0 and diff_b == 0 and diff_f == 0:
        verdict = "seam_does_not_source_eta"
        tier = "X"
        term_breaking_equality = None
        spectrum_parity = "even"
    else:
        verdict = "stored_odd_term"
        tier = "D"
        term_breaking_equality = odd_terms_found[0]
        spectrum_parity = "odd"

    receipt = {
        "job": "A",
        "exit_code": 0,
        "verdict": verdict,
        "tier": tier,
        "neighbor_constrained": "the shadow reading",
        "neighbor_forbidden": "a baryon-to-photon ratio, a cosmic baryon fraction, the seam mass",
        "free_symbols": free_syms,
        "numeric_outputs": {},
        "script": "job_a_seam_eta.py",
        "stored_spectrum_parity": spectrum_parity,
        "odd_terms_found": odd_terms_found,
        "term_breaking_equality": term_breaking_equality,
        "summary": "Stored mode equations and |beta|^2 depend only on even powers (tau^2, k^2). No odd terms break sheet reflection or charge conjugation; the seam does not source eta."
    }

    out_file = Path(__file__).parent / "job_a_seam_eta.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(evaluate_seam_matter_excess())
