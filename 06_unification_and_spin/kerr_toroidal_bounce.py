#!/usr/bin/env python3
"""UFW-C0 horizon back-reaction specification audit.

This script evaluates standard Kerr kinematics and the torque required by the
proposed modified ODE at the proposed target. It never invents tau_top or
integrates a tuned trajectory, because the blueprint supplies no action,
field content, units, coefficient, or boundary conditions for that term.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parent
PROTOCOL = ROOT / "README.md"
OUTPUT = Path(__file__).with_name("kerr_toroidal_bounce_results.json")


def sha256(path: Path) -> str:
    if path.exists():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return "0" * 64


def r_isco(a: mp.mpf) -> mp.mpf:
    z1 = 1 + (1 - a*a) ** (mp.mpf(1)/3) * ((1+a) ** (mp.mpf(1)/3) + (1-a) ** (mp.mpf(1)/3))
    z2 = mp.sqrt(3*a*a + z1*z1)
    return 3 + z2 - mp.sqrt((3-z1) * (3+z1+2*z2))


def isco_energy_and_l(a: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    r = r_isco(a)
    sr = mp.sqrt(r)
    denom = r ** mp.mpf("0.75") * mp.sqrt(r ** mp.mpf("1.5") - 3*sr + 2*a)
    energy = (r ** mp.mpf("1.5") - 2*sr + a) / denom
    ell = (r*r - 2*a*sr + a*a) / denom
    return r, energy, ell


def kerr_kretschmann_equator(a: mp.mpf, mass: mp.mpf = mp.mpf(1)) -> mp.mpf:
    """R_abcd R^abcd at theta=pi/2 on the outer Kerr horizon."""
    r_plus = mass * (1 + mp.sqrt(1 - a*a))
    return 48 * mass**2 / r_plus**6


def main() -> None:
    mp.mp.dps = 80
    chi = mp.sqrt(mp.sqrt(2) - mp.mpf("0.5"))
    gap = 2 * mp.sqrt(1 - chi*chi)
    rplus = 1 + mp.sqrt(1-chi*chi)
    rminus = 1 - mp.sqrt(1-chi*chi)
    r_ms, energy, ell = isco_energy_and_l(chi)
    matter_rhs = ell / energy - 2*chi
    # With L_cap=E_cap=0, the proposed ODE would require this numerator torque.
    tau_required_matter_only = ell - 2*chi*energy
    k_chi = kerr_kretschmann_equator(chi)
    k_extremal_limit = mp.mpf(48)
    curvature_samples = []
    for a in (mp.mpf("0"), chi, mp.mpf("0.99"), mp.mpf("0.999"), mp.mpf("0.999999")):
        curvature_samples.append({
            "a_star": mp.nstr(a, 30),
            "equatorial_horizon_kretschmann_M4": mp.nstr(kerr_kretschmann_equator(a), 30),
            "proposed_divergent_factor": mp.nstr(1/mp.sqrt(1-a*a), 30),
        })

    blockers = {
        "covariant_action": "absent",
        "dynamical_fields_and_symmetries": "absent",
        "tau_top_definition_and_units": "absent",
        "torque_coefficient_or_normalisation": "absent",
        "curvature_invariant_definition": "absent",
        "stress_tensor_and_conservation_law": "absent",
        "horizon_boundary_and_regularization_conditions": "absent",
        "coupling_to_accretion_fluxes": "absent",
    }
    result = {
        "model_id": "UFW-C0",
        "gate": "UFW-DYN horizon back-reaction closure",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "units": "G=c=M=1; all reported horizon radii and gaps are in M; curvature is M^-4",
        "target": {
            "chi_s_exact": "sqrt(sqrt(2)-1/2)",
            "chi_s_numeric": mp.nstr(chi, 40),
            "r_plus": mp.nstr(rplus, 40),
            "r_minus": mp.nstr(rminus, 40),
            "horizon_gap": mp.nstr(gap, 40),
            "blueprint_gap_formula_residual": mp.nstr(abs(gap - 2*mp.sqrt(1-chi*chi)), 8),
        },
        "matter_only_isco_at_target": {
            "r_ms": mp.nstr(r_ms, 40),
            "E_ms": mp.nstr(energy, 40),
            "L_ms_over_M": mp.nstr(ell, 40),
            "da_star_dlnM_without_capture_or_topological_torque": mp.nstr(matter_rhs, 40),
            "tau_top_required_if_photon_terms_are_set_to_zero": mp.nstr(tau_required_matter_only, 40),
            "interpretation": "This is a target-conditioned cancellation requirement, not a derived torque law.",
        },
        "curvature_audit": {
            "standard_equatorial_horizon_kretschmann": "48 M^2/r_plus^6",
            "value_at_target_M4": mp.nstr(k_chi, 40),
            "extremal_equatorial_limit_M4": mp.nstr(k_extremal_limit, 40),
            "proposed_scaling": "(1-a_star^2)^(-1/2)",
            "compatibility": "FAIL for the equatorial Kerr Kretschmann scalar: the proposed factor diverges as a_star->1 while this invariant tends to finite 48/M^4.",
            "samples": curvature_samples,
        },
        "equilibrium_identity": {
            "from_blueprint_ode": "tau_top = L_ms + L_cap - 2 a_star (E_ms + E_cap) at equilibrium",
            "consequence": "For any chosen target and specified fluxes, this identity can define a cancelling tau_top. It does not predict the target unless tau_top is independently derived and fixed.",
        },
        "missing_requirements": blockers,
        "dynamics_status": "BLOCKED",
        "block_reason": "The new topological torque is not derived from a covariant action or complete effective theory. The asserted curvature scaling is not a defined invariant law and is incompatible with the standard equatorial Kerr Kretschmann behavior. No ODE trajectory or spin ceiling is calculated.",
        "input_hashes": {"protocol": sha256(PROTOCOL)},
        "script_hash": sha256(Path(__file__)),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "target": result["target"],
        "matter_only_isco_at_target": result["matter_only_isco_at_target"],
        "curvature_audit": result["curvature_audit"],
        "dynamics_status": result["dynamics_status"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
