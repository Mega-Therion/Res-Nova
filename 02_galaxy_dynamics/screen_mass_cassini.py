#!/usr/bin/env python3
"""Symmetron effective mass and Cassini external-field quadrupole (Q2) audit.

Citations:
- /home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/REPAIRED_COUPLING_CASSINI.md
- /home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/repaired_coupling_cassini.py
- /home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md
- /home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/efe_quadrupole_q2.py
- /home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/ASSEMBLY_GALAXY_ANCHOR_2026-10-04.md
- /home/mega/Chyren/3_research/Res-Nova/01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.tex (lines 692-715)
- /home/mega/Chyren/3_research/Res-Nova/01_foundational_action/PRD_Relativistic_Extension.tex (line 146)
- /home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/duality_screening_cone_check.py (line 116)
"""

import json
import math
from pathlib import Path
import sympy as sp


def main():
    here = Path(__file__).resolve().parent

    # -------------------------------------------------------------------------
    # 0. Established constants and unscreened Q2 values at the galaxy anchor
    #    (REPAIRED_COUPLING_CASSINI.md lines 13-22; repaired_coupling_cassini.py lines 26-43)
    # -------------------------------------------------------------------------
    a0_anchor = 1.163e-10            # m/s^2 (ASSEMBLY_GALAXY_ANCHOR_2026-10-04.md:9, REPAIRED_COUPLING_CASSINI.md:13)
    G_N = 6.67430e-11                # m^3 kg^-1 s^-2 (lambda_sc_unscreened.py:19, test_covariant_tidal_screening.py:18)
    c_light = 2.99792458e8           # m/s (lambda_sc_unscreened.py:18)
    GM_sun = 1.32712e20              # m^3 s^-2 (efe_quadrupole_q2.py:22)
    M_sun = 1.98847e30               # kg (test_covariant_tidal_screening.py:19)
    g_N_solar_limb = 274.0           # m/s^2 at r = R_sun (PRD_Relativistic_Extension.tex:146)
    L_sun = math.sqrt(GM_sun / g_N_solar_limb)  # 6.95957e8 m from corpus GM_sun & g_N(R_sun)

    # Cassini windows (REPAIRED_COUPLING_CASSINI.md:17-20, CASSINI_EFE_QUADRUPOLE_2026-09-27.md:10,90):
    # 2014 window (Hees et al. 2014): Q2 = (3.0 +/- 3.0)e-27 s^-2
    q2_2014_cen = 3.0e-27
    sigma_2014 = 3.0e-27
    # 2026 window (arXiv:2602.17884): Q2 = (1.6 +/- 1.8)e-27 s^-2
    q2_2026_cen = 1.6e-27
    sigma_2026 = 1.8e-27

    # Unscreened Q2 at galaxy anchor a0 = 1.163e-10 m/s^2 for mu(x) = x / sqrt(1 + x^2)
    # (REPAIRED_COUPLING_CASSINI.md:19-20):
    unscreened_rows = [
        {"g_e": 1.9e-10, "Q2_unscreened": 1.91e-26, "sigma_2014_unscreened": (1.91e-26 - q2_2014_cen) / sigma_2014, "sigma_2026_unscreened": (1.91e-26 - q2_2026_cen) / sigma_2026},
        {"g_e": 2.4e-10, "Q2_unscreened": 2.01e-26, "sigma_2014_unscreened": (2.01e-26 - q2_2014_cen) / sigma_2014, "sigma_2026_unscreened": (2.01e-26 - q2_2026_cen) / sigma_2026},
    ]

    # -------------------------------------------------------------------------
    # 1. Densities and Symmetron Potential from PAPER_09 (lines 692-715)
    # -------------------------------------------------------------------------
    # Solar densities:
    # (a) Standard Solar Model core density: 1.5e5 kg/m^3 (150 g/cm^3; standard solar core reference,
    #     not separately tabulated in Res-Nova; mean solar density from GM_sun in efe_quadrupole_q2.py:22
    #     and g_N(R_sun)=274 m/s^2 in PRD_Relativistic_Extension.tex:146 is rho_sun_mean = 1.4079e3 kg/m^3).
    rho_sun_core = 1.5e5                                               # kg/m^3 (150 g/cm^3, solar core)
    rho_sun_mean = M_sun / ((4.0 / 3.0) * math.pi * (L_sun ** 3))      # 1.4079e3 kg/m^3 (mean Sun from corpus GM_sun, g_N)

    # Galactic densities in the corpus:
    # (a) Anchor-scale characteristic volumetric density from l = c^2 / a0 (ASSEMBLY_GALAXY_ANCHOR_2026-10-04.md:15)
    #     via Poisson scale a0 / l = 4 * pi * G * rho_gal_anchor  =>  rho_gal_anchor = a0^2 / (4 * pi * G * c^2):
    l_anchor = (c_light ** 2) / a0_anchor
    rho_gal_anchor = (a0_anchor ** 2) / (4.0 * math.pi * G_N * (c_light ** 2))  # 1.7945e-28 kg/m^3
    # (b) Galactic disk midplane density at the Sun (duality_screening_cone_check.py:116):
    #     rho_disk = 0.1 * M_sun / pc^3 = 6.7698e-21 kg/m^3:
    rho_gal_disk = 0.1 * 1.989e30 / (3.0857e16 ** 3)                            # 6.7698e-21 kg/m^3

    # Symbolic symmetron derivation (PAPER_09 lines 695-708):
    # V_eff(chi) = lam * (chi - theta)^2 + (rho / (2 * M^2)) * chi^2
    chi, lam, M, theta, rho, r, L_odot = sp.symbols("chi lambda M theta rho r L_odot", positive=True, real=True)
    rho_odot_sym, rho_gal_sym = sp.symbols("rho_odot rho_gal", positive=True, real=True)

    V_eff = lam * (chi - theta) ** 2 + (rho / (2 * M ** 2)) * (chi ** 2)
    dV_dchi = sp.diff(V_eff, chi)
    d2V_dchi2 = sp.diff(V_eff, chi, 2)

    chi_min_expr = sp.simplify(sp.solve(sp.Eq(dV_dchi, 0), chi)[0])
    m_eff_sq_expr = sp.simplify(d2V_dchi2)
    m_eff_expr = sp.sqrt(m_eff_sq_expr)

    # Verify against PAPER_09 Eq. (699) and Eq. (707):
    assert sp.simplify(m_eff_sq_expr - (2 * lam + rho / M ** 2)) == 0
    assert sp.simplify(chi_min_expr - (2 * M ** 2 * lam * theta) / (2 * M ** 2 * lam + rho)) == 0

    # Evaluate symbolically at theta = 0.7 (PAPER_09 line 686):
    theta_val = sp.Rational(7, 10)
    chi_min_theta = sp.simplify(chi_min_expr.subs(theta, theta_val))

    # m_eff at solar-core density and galactic density (symbolic in lambda, M because PAPER_09 does not fix lambda or M):
    m_eff_sun_sym = m_eff_expr.subs(rho, rho_odot_sym)
    m_eff_gal_sym = m_eff_expr.subs(rho, rho_gal_sym)
    m_eff_L_sun_sym = sp.simplify(L_odot * m_eff_sun_sym)
    compton_in_solar_radii_sym = sp.simplify(1 / m_eff_L_sun_sym)

    # -------------------------------------------------------------------------
    # 2. Suppression mechanisms from PAPER_09 Eqs. (699) and (707)
    # -------------------------------------------------------------------------
    # Mechanism A: Yukawa factor exp(-m_eff * r)
    S_yukawa_sym = sp.exp(-m_eff_sun_sym * r)
    S_yukawa_at_L_sun = sp.exp(-m_eff_L_sun_sym)

    # Mechanism B: Vacuum expectation value ratio chi_min(rho_odot) / chi_min(rho_gal)
    # Note that theta = 0.7 cancels identically in the ratio:
    S_chi_ratio_sym = sp.simplify(chi_min_expr.subs(rho, rho_odot_sym) / chi_min_expr.subs(rho, rho_gal_sym))
    assert sp.simplify(S_chi_ratio_sym - (2 * M ** 2 * lam + rho_gal_sym) / (2 * M ** 2 * lam + rho_odot_sym)) == 0

    # -------------------------------------------------------------------------
    # 3. Apply symbolic suppression factor S to the two Q2 values and compute
    #    residuals in units of sigma_2014 = 3e-27 s^-2 and sigma_2026 = 1.8e-27 s^-2
    # -------------------------------------------------------------------------
    S_sym = sp.Symbol("S", nonnegative=True, real=True)
    suppressed_results = []
    for row in unscreened_rows:
        ge = row["g_e"]
        q2_u = row["Q2_unscreened"]
        # Symbolic expressions in terms of S (where S = S_yukawa or S = S_chi_ratio):
        c_2014 = q2_u / sigma_2014
        c_2026 = q2_u / sigma_2026
        off_2014 = q2_2014_cen / sigma_2014
        off_2026 = q2_2026_cen / sigma_2026

        suppressed_results.append({
            "g_e_m_s2": ge,
            "Q2_unscreened_s_minus_2": q2_u,
            "Q2_suppressed_yukawa_formula": f"{q2_u:.2e} * exp(-r * sqrt(2*lambda + rho_odot/M^2))",
            "Q2_suppressed_chi_ratio_formula": f"{q2_u:.2e} * (2*M^2*lambda + rho_gal) / (2*M^2*lambda + rho_odot)",
            "residual_2014_sigma_window_centered": f"({q2_u:.2e} * S - 3.00e-27) / 3.00e-27 = {c_2014:.6f} * S - {off_2014:.6f}",
            "residual_2014_sigma_raw_ratio": f"({q2_u:.2e} * S) / 3.00e-27 = {c_2014:.6f} * S",
            "residual_2026_sigma_window_centered": f"({q2_u:.2e} * S - 1.60e-27) / 1.80e-27 = {c_2026:.6f} * S - {off_2026:.6f}",
            "residual_2026_sigma_raw_ratio": f"({q2_u:.2e} * S) / 1.80e-27 = {c_2026:.6f} * S",
            "unscreened_S_eq_1_sigma_2014": row["sigma_2014_unscreened"],
            "unscreened_S_eq_1_sigma_2026": row["sigma_2026_unscreened"],
        })

    # -------------------------------------------------------------------------
    # 4. Required check: Are lambda and M fixed in the corpus?
    # -------------------------------------------------------------------------
    lambda_and_M_fixed_in_corpus = False
    epistemic_tag = "[O]"

    receipt = {
        "exit_code": 0,
        "epistemic_status": epistemic_tag,
        "lambda_and_M_fixed_in_corpus": lambda_and_M_fixed_in_corpus,
        "anchor_a0_m_s2": a0_anchor,
        "theta": 0.7,
        "densities": {
            "rho_sun_core_kg_m3": rho_sun_core,
            "rho_sun_core_source": "Standard Solar Model core density (1.5e5 kg/m^3 = 150 g/cm^3); not fixed in PAPER_09",
            "rho_sun_mean_kg_m3": rho_sun_mean,
            "rho_sun_mean_source": "Derived from GM_sun = 1.32712e20 m^3/s^2 (02_galaxy_dynamics/efe_quadrupole_q2.py:22), M_sun = 1.98847e30 kg (02_galaxy_dynamics/test_covariant_tidal_screening.py:19), and solar-limb g_N(R_sun) = 274 m/s^2 (01_foundational_action/PRD_Relativistic_Extension.tex:146)",
            "L_sun_m": L_sun,
            "rho_gal_anchor_kg_m3": rho_gal_anchor,
            "rho_gal_anchor_formula": "a0^2 / (4 * pi * G * c^2)",
            "rho_gal_anchor_source": "Anchor acceleration a0 = 1.163e-10 m/s^2 and length l = c^2 / a0 (02_galaxy_dynamics/ASSEMBLY_GALAXY_ANCHOR_2026-10-04.md:9,15)",
            "rho_gal_disk_kg_m3": rho_gal_disk,
            "rho_gal_disk_source": "0.1 M_sun / pc^3 local galactic midplane density (02_galaxy_dynamics/duality_screening_cone_check.py:116)",
        },
        "symmetron_formulas_PAPER_09": {
            "citation": "01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.tex:695-708",
            "V_eff": "lambda * (chi - theta)^2 + (rho / (2 * M^2)) * chi^2",
            "m_eff_sq": str(m_eff_sq_expr),
            "m_eff_solar": "sqrt(2*lambda + rho_odot / M**2)",
            "m_eff_galactic": "sqrt(2*lambda + rho_gal / M**2)",
            "m_eff_L_odot": "L_odot * sqrt(2*lambda + rho_odot / M**2)",
            "compton_wavelength_in_solar_radii": "1 / (L_odot * sqrt(2*lambda + rho_odot / M**2))",
            "chi_min": str(chi_min_expr),
            "chi_min_at_theta_0p7": str(chi_min_theta),
        },
        "suppression_factors": {
            "S_yukawa": "exp(-r * sqrt(2*lambda + rho_odot / M**2))",
            "S_yukawa_at_r_eq_L_odot": "exp(-L_odot * sqrt(2*lambda + rho_odot / M**2))",
            "S_chi_min_ratio": str(S_chi_ratio_sym),
            "repaired_disformal_coupling_S": 1.0,
            "repaired_disformal_note": "g_tilde_munu = g_munu + B d_mu chi d_nu chi (REPAIRED_COUPLING_CASSINI.md:8) contains neither V(chi) nor A(chi) and is unsourced by static dust (duality_screening_cone_check.py:69), leaving S = 1 unscreened.",
        },
        "suppressed_Q2_and_residuals": suppressed_results,
        "required_check": (
            "[O] lambda and M are not fixed in PAPER_09 or elsewhere in the Res-Nova corpus. "
            "The symmetron-suppressed Q2 and its 2014/2026 sigma residuals remain symbolic formulas in (lambda, M) [O]. "
            "In the repaired disformal coupling without free parameters (S = 1), Cassini FAILS both windows "
            "(+5.37 sigma / +5.70 sigma against 2014; +9.72 sigma / +10.28 sigma against 2026)."
        ),
    }

    json_path = here / "screen_mass_cassini.json"
    with open(json_path, "w") as f:
        json.dump(receipt, f, indent=2)

    print("exit_code = 0")
    print(f"rho_odot (solar core, SSM reference; not fixed in PAPER_09) = {rho_sun_core:.6e} kg/m^3")
    print(f"rho_odot_mean (efe_quadrupole_q2.py:22 + PRD_Relativistic_Extension.tex:146, L_odot = {L_sun:.6e} m) = {rho_sun_mean:.6e} kg/m^3")
    print(f"rho_gal_anchor = a0^2 / (4*pi*G*c^2) (ASSEMBLY_GALAXY_ANCHOR_2026-10-04.md:9,15) = {rho_gal_anchor:.6e} kg/m^3")
    print(f"rho_gal_disk (duality_screening_cone_check.py:116, 0.1 M_sun/pc^3) = {rho_gal_disk:.6e} kg/m^3")
    print(f"m_eff(rho_odot) = sqrt(2*lambda + rho_odot/M^2) = sqrt(2*lambda + ({rho_sun_core:.6e} kg/m^3)/M^2)  [O]")
    print(f"m_eff(rho_gal_anchor) = sqrt(2*lambda + rho_gal_anchor/M^2) = sqrt(2*lambda + ({rho_gal_anchor:.6e} kg/m^3)/M^2)  [O]")
    print(f"m_eff(rho_gal_disk) = sqrt(2*lambda + rho_gal_disk/M^2) = sqrt(2*lambda + ({rho_gal_disk:.6e} kg/m^3)/M^2)  [O]")
    print(f"m_eff * L_odot = L_odot * sqrt(2*lambda + rho_odot/M^2)  (Compton wavelength in solar radii: lambda_C / L_odot = 1 / (L_odot * sqrt(2*lambda + rho_odot/M^2)))  [O]")
    print(f"S_yukawa(r) = exp(-r * sqrt(2*lambda + rho_odot/M^2))  [O]")
    print(f"S_chi = chi_min(rho_odot) / chi_min(rho_gal) = (2*M^2*lambda + rho_gal) / (2*M^2*lambda + rho_odot)  (theta = 0.7 cancels)  [O]")
    for r_row in suppressed_results:
        print(
            f"g_e = {r_row['g_e_m_s2']:.1e} m/s^2 | Q2_supp = {r_row['Q2_unscreened_s_minus_2']:.2e} * S s^-2 "
            f"| 2014 residual: {r_row['residual_2014_sigma_window_centered']} (raw Q2_supp/sigma_2014 = {r_row['residual_2014_sigma_raw_ratio']}) "
            f"| 2026 residual: {r_row['residual_2026_sigma_window_centered']} (raw Q2_supp/sigma_2026 = {r_row['residual_2026_sigma_raw_ratio']})"
        )
    print(f"Required check: {receipt['required_check']}")


if __name__ == "__main__":
    main()
