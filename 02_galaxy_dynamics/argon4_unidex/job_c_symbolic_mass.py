#!/usr/bin/env python3
"""
job_c_symbolic_mass.py — Worker C: Symbolic mass reduction and exponent audit.

Specific Task for Job C:
- Start from I = 1/(8 pi^(3/2)), |beta|^2 = exp(-pi k^2/gamma), and radiation
  continuity derived without new constants.
- Either derive power 2/5 from those inputs, or stop at first missing relation
  and set exponent_status to copied_not_derived.
- Free symbols that must remain symbols: m, y, C, g_star, rho_dm0, s_0.
- Identifying produced species with dark matter is [O] until Job C records
  identification as assumption rather than result. If identification required
  for 2/5, say so and leave mass symbolic.
- Verdict: mass_remains_symbolic. Tier O on mass, tier D only on algebra
  actually reduced.
- Neighbor constrained: list of symbols still free.
- Neighbor forbidden: numerical dark-matter mass, neutrino name, I itself (fixed equal to 1/(8 pi^(3/2))).
"""

import os
import sys
import json
import sympy as sp

def run_job_c():
    # -------------------------------------------------------------------------
    # 1. Define symbolic variables with genuine physical/mathematical properties
    # -------------------------------------------------------------------------
    k, gamma = sp.symbols('k gamma', positive=True, real=True)
    m, y, C, g_star, rho_dm0, s_0 = sp.symbols('m y C g_star rho_dm0 s_0', positive=True, real=True)
    s_rad, G_N, rho_r0, I_sym = sp.symbols('s_rad G_N rho_r0 I_sym', positive=True, real=True)

    # -------------------------------------------------------------------------
    # 2. Phase-space Bogoliubov integration in SymPy (Tier D Algebra)
    # -------------------------------------------------------------------------
    # Comoving number density: n_c = int (d^3 k / (2*pi)^3) * |beta_k|^2
    # with |beta_k|^2 = exp(-pi * k^2 / gamma)
    integrand = (4 * sp.pi * k**2 / (2 * sp.pi)**3) * sp.exp(-sp.pi * k**2 / gamma)
    n_c_int = sp.integrate(integrand, (k, 0, sp.oo))
    
    # Direct yield relation: I = 1 / (8 * pi^(3/2))
    # n_c_int evaluates to gamma^(3/2) / (8 * pi^3) = (I / pi^(3/2)) * gamma^(3/2)
    I_val = sp.Rational(1, 8) / (sp.pi**(sp.Rational(3, 2)))
    n_c_from_I = (I_val / (sp.pi**(sp.Rational(3, 2)))) * gamma**(sp.Rational(3, 2))
    assert sp.simplify(n_c_int - n_c_from_I) == 0, "Phase space integral must match (I/pi^(3/2))*gamma^(3/2)"

    # Tetrad coupling: gamma = y * m * C (or m * C when y=1)
    # Yields comoving particle number density scaling: n_c proportional to m^(3/2)
    n_c_sym = (I_sym / (sp.pi**(sp.Rational(3, 2)))) * (y * m * C)**(sp.Rational(3, 2))
    m_power_in_nc = sp.simplify(n_c_sym).as_coeff_exponent(m)[1]

    # -------------------------------------------------------------------------
    # 3. Radiation Continuity (without new constants)
    # -------------------------------------------------------------------------
    # a(tau) = C * tau, rho_r(tau) = rho_r0 / a(tau)^4
    # Zero-constraint/Friedmann: C^2 = 8 * pi * G_N * rho_r0 / 3
    # Comoving entropy: S = s * a^3 = s_rad = (4/3) * (pi^2 * g_star / 30)^(1/4) * rho_r0^(3/4)
    # Number-to-entropy ratio: Y = n_c / s_rad
    Y_sym = n_c_sym / s_rad

    # -------------------------------------------------------------------------
    # 4. Epistemic Audit of Power 2/5 and Missing Relations
    # -------------------------------------------------------------------------
    # From I, |beta|^2, and radiation continuity alone:
    # We only have n_c proportional to m^(3/2). There is NO relation connecting m
    # to the observed present-day dark matter density rho_dm0.
    # The first missing relation is the identification of the created species
    # with present-day dark matter: rho_dm0 = m * n0.
    first_missing = "identification_of_produced_species_with_dark_matter (rho_dm0 = m * n0)"

    # -------------------------------------------------------------------------
    # 5. Recording Species Identification as Assumption [O]
    # -------------------------------------------------------------------------
    # Identifying produced species with dark matter is recorded as an assumption [O],
    # NOT a result of the seam. Identification IS required to obtain exponent 2/5.
    identification_status = "recorded_as_assumption_not_result"
    id_required_for_2_5 = True

    # -------------------------------------------------------------------------
    # 6. Algebraic Reduction Under Assumption [O] (Tier D Algebra)
    # -------------------------------------------------------------------------
    # Under assumption rho_dm0 = m * n0 = m * Y * s_0:
    # rho_dm0 = m * ( (I_sym / pi^(3/2)) * (y * m * C)^(3/2) / s_rad ) * s_0
    #         = m^(5/2) * ( (I_sym / pi^(3/2)) * (y * C)^(3/2) * s_0 / s_rad )
    dm_eq = sp.Eq(rho_dm0, m * Y_sym * s_0)
    m_solutions = sp.solve(dm_eq, m)
    # Extract real positive root
    m_sol = m_solutions[0]
    
    # Verified powers:
    power_rho_dm0 = sp.simplify(m_sol).as_coeff_exponent(rho_dm0)[1]
    power_s_0 = sp.simplify(m_sol).as_coeff_exponent(s_0)[1]
    power_y = sp.simplify(m_sol).as_coeff_exponent(y)[1]
    power_C = sp.simplify(m_sol).as_coeff_exponent(C)[1]
    power_I = sp.simplify(m_sol).as_coeff_exponent(I_sym)[1]

    assert power_rho_dm0 == sp.Rational(2, 5), "rho_dm0 exponent must be 2/5"
    assert power_s_0 == -sp.Rational(2, 5), "s_0 exponent must be -2/5"

    # Radiation background density rho_r0 cancellation check:
    C_expr = sp.sqrt(sp.Rational(8, 3) * sp.pi * G_N * rho_r0)
    s_rad_expr = sp.Rational(4, 3) * (sp.pi**2 * g_star / 30)**sp.Rational(1, 4) * rho_r0**sp.Rational(3, 4)
    m_sol_expanded = sp.simplify(m_sol.subs([(C, C_expr), (s_rad, s_rad_expr)]))
    power_rho_r0 = sp.simplify(m_sol_expanded).as_coeff_exponent(rho_r0)[1]
    assert power_rho_r0 == 0, "rho_r0 must cancel identically"

    # -------------------------------------------------------------------------
    # 7. Assemble Machine Receipt
    # -------------------------------------------------------------------------
    receipt = {
        "job": "C",
        "exit_code": 0,
        "verdict": "mass_remains_symbolic",
        "tier": "O",
        "neighbor_constrained": "list of symbols still free",
        "neighbor_forbidden": "numerical dark-matter mass, neutrino name, I itself (fixed equal to 1/(8 π^(3/2)))",
        "free_symbols": [
            "m",
            "y",
            "C",
            "g_star",
            "rho_dm0",
            "s_0"
        ],
        "numeric_outputs": {},
        "script": "job_c_symbolic_mass.py",
        "exponent_status": "copied_not_derived",
        "first_missing_relation": first_missing,
        "identification_of_species_with_dark_matter": identification_status,
        "identification_required_for_2_5": id_required_for_2_5,
        "algebra_tier": "D",
        "mass_tier": "O",
        "algebraic_reduction": {
            "phase_space_integral": "int (d^3k/(2pi)^3) exp(-pi k^2/gamma) = gamma^(3/2)/(8 pi^3)",
            "comoving_particle_density_nc": "(I / pi^(3/2)) * (y * m * C)^(3/2)",
            "unassisted_m_exponent_in_nc": str(m_power_in_nc),
            "dark_matter_density_relation": "rho_dm0 = m * n0 = m * (nc / s_rad) * s_0",
            "combined_m_exponent_before_inversion": "5/2",
            "reduced_m_exponent": str(power_rho_dm0),
            "rho_r0_cancellation": "rho_r0 cancels identically between C^(3/2) and s_rad",
            "symbolic_mass_expression": "((rho_dm0 / s_0) * (pi^(3/2) * s_rad) / (I_sym * y^(3/2) * C^(3/2)))^(2/5)"
        },
        "summary": "Phase-space integration gives nc proportional to m^(3/2) [tier D]. Equating to observed dark matter density requires assuming rho_dm0 = m*n0 [tier O], which is not derived from seam inputs. Under this assumption, algebra yields exponent 2/5. Stopping at the first missing relation marks exponent copied_not_derived from pure seam. All symbols remain free; mass remains symbolic [tier O]."
    }

    # Write receipt to target json file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(output_dir, "job_c_symbolic_mass.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    # Print single JSON object to stdout
    print(json.dumps(receipt, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(run_job_c())
