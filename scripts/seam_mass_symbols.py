#!/usr/bin/env python3
"""Symbolic mass reduction under one declared assumption.

Constant-mass line already stored on both mode operators: gamma = m * C.
Yukawa factor omitted. The dark-matter identification rho_dm0 = m * n0 is
an assumption, tagged before the solve. No numerical mass is substituted.

After that root, an adopted declaration (2026-10-31, tier O) sets the
entropy ruler to the photon gas, g_star = 2. A second adopted declaration
sets the dilution ratio to 1. Textbook values of G_N, the CMB temperature,
and Omega_c h^2 are then imported. The resulting mass is conditional on
that stack. It is not a seam theorem and it names no particle.
"""

from __future__ import annotations

import json

import mpmath as mp
import sympy as sp


def _mpf(value: str) -> mp.mpf:
    return mp.mpf(value)


def conditional_mass(pref: mp.mpf) -> dict:
    """Import G_N, T_CMB, and Omega_c h^2. Two unit paths must agree.

    The dilution ratio is already 1, so it does not change the prefactor.
    Entropy is the photon gas at the measured CMB temperature, g_star = 2.
    """
    import scipy.constants as phys

    mp.mp.dps = 50
    G_val, G_unit, G_unc = phys.physical_constants["Newtonian constant of gravitation"]
    hbar_val, hbar_unit, _ = phys.physical_constants["reduced Planck constant"]
    c_val, c_unit, _ = phys.physical_constants["speed of light in vacuum"]
    k_val, k_unit, _ = phys.physical_constants["Boltzmann constant"]
    e_val, e_unit, _ = phys.physical_constants["elementary charge"]
    if (G_unit, hbar_unit, c_unit, k_unit, e_unit) != (
        "m^3 kg^-1 s^-2",
        "J s",
        "m s^-1",
        "J K^-1",
        "C",
    ):
        raise SystemExit("scipy constant units changed")

    # Fixsen 2009, ApJ 707 916, literature compilation. Not the WMAP recalibration.
    T_K = _mpf("2.72548")
    T_unc = _mpf("0.00057")
    # Planck 2018 results VI, arXiv:1807.06209, abstract combined analysis, 68%.
    omega = _mpf("0.120")
    omega_unc = _mpf("0.001")

    G = _mpf(str(G_val))
    G_sigma = _mpf(str(G_unc))
    hbar = _mpf(str(hbar_val))
    c = _mpf(str(c_val))
    k_B = _mpf(str(k_val))
    e = _mpf(str(e_val))
    GeV_J = _mpf("1e9") * e
    Mpc = _mpf(str(phys.parsec)) * _mpf("1e6")
    H100 = _mpf("1e5") / Mpc

    def evaluate(G_N: mp.mpf, T: mp.mpf, omega_c_h2: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
        rho_mass = 3 * H100**2 / (8 * mp.pi * G_N)
        rho_energy = rho_mass * c**2 * omega_c_h2
        s_per_m3 = (2 * mp.pi**2 / 45) * 2 * (k_B * T / (hbar * c)) ** 3
        G_nat = G_N * hbar / c**3
        rho_per_m4 = rho_energy / (hbar * c)
        m_per_m = (
            pref
            * rho_per_m4 ** mp.mpf("0.4")
            / (G_nat ** mp.mpf("0.3") * s_per_m3 ** mp.mpf("0.4"))
        )
        m_GeV_length = m_per_m * hbar * c / GeV_J

        rho_GeV4 = rho_energy * (hbar * c) ** 3 / GeV_J**4
        T_GeV = k_B * T / GeV_J
        s_GeV3 = (2 * mp.pi**2 / 45) * 2 * T_GeV**3
        E_Pl = mp.sqrt(hbar * c**5 / G_N) / GeV_J
        G_GeV = 1 / E_Pl**2
        m_GeV_energy = (
            pref
            * rho_GeV4 ** mp.mpf("0.4")
            / (G_GeV ** mp.mpf("0.3") * s_GeV3 ** mp.mpf("0.4"))
        )
        return m_GeV_length, m_GeV_energy

    central_length, central_energy = evaluate(G, T_K, omega)
    relative = abs(central_length - central_energy) / central_energy
    if relative > mp.mpf("1e-20"):
        raise SystemExit(f"unit paths disagree: {relative}")

    low_o, _ = evaluate(G, T_K, omega - omega_unc)
    high_o, _ = evaluate(G, T_K, omega + omega_unc)
    low_T, _ = evaluate(G, T_K - T_unc, omega)
    high_T, _ = evaluate(G, T_K + T_unc, omega)
    low_G, _ = evaluate(G + G_sigma, T_K, omega)
    high_G, _ = evaluate(G - G_sigma, T_K, omega)

    def pair(lo: mp.mpf, hi: mp.mpf) -> list[str]:
        left, right = sorted((lo, hi))
        return [mp.nstr(left, 20), mp.nstr(right, 20)]

    return {
        "tier": "O",
        "particle_name": None,
        "dilution_ratio": 1,
        "imports": {
            "G_N": {
                "value": str(G_val),
                "uncertainty": str(G_unc),
                "unit": G_unit,
                "source": "scipy.constants CODATA, scipy "
                + __import__("scipy").__version__,
                "tier": "C",
            },
            "T_CMB_K": {
                "value": "2.72548",
                "uncertainty": "0.00057",
                "source": "Fixsen 2009 ApJ 707 916, arXiv:0911.1955, literature compilation",
                "tier": "C",
            },
            "omega_c_h2": {
                "value": "0.120",
                "uncertainty": "0.001",
                "interval": "68%",
                "source": "Planck 2018 results VI, arXiv:1807.06209, abstract combined analysis",
                "tier": "C",
                "includes_baryons": False,
            },
        },
        "entropy": "photon gas, g_star = 2, s = (2*pi**2/45)*g_star*T**3",
        "unit_paths_relative_difference": mp.nstr(relative, 6),
        "m_GeV": mp.nstr(central_energy, 20),
        "omega_c_h2_band_GeV": pair(low_o, high_o),
        "T_CMB_band_GeV": pair(low_T, high_T),
        "G_N_band_GeV": pair(low_G, high_G),
    }


def main() -> None:
    m, C, g_star = sp.symbols("m C g_star", positive=True)
    rho_dm0, s_0, rho_r0, G_N = sp.symbols("rho_dm0 s_0 rho_r0 G_N", positive=True)
    gamma, k = sp.symbols("gamma k", positive=True)

    # Stored yield. Not recomputed from the mode equation.
    I = sp.Integer(1) / (8 * sp.pi ** sp.Rational(3, 2))

    # Integral of the stored spectrum |beta|^2 = exp(-pi k^2 / gamma).
    integrand = (4 * sp.pi * k**2 / (2 * sp.pi) ** 3) * sp.exp(-sp.pi * k**2 / gamma)
    n_c_integral = sp.simplify(sp.integrate(integrand, (k, 0, sp.oo)))
    n_c_from_I = sp.simplify(
        (I / sp.pi ** sp.Rational(3, 2)) * gamma ** sp.Rational(3, 2)
    )
    if sp.simplify(n_c_integral - n_c_from_I) != 0:
        raise SystemExit("stored I does not match the integral of the stored spectrum")

    # Declared before the solve. Constant mass. Yukawa closed.
    gamma_decl = m * C
    n_c = sp.simplify(n_c_from_I.subs(gamma, gamma_decl))

    # Job 1 stored constraint.
    C_of_rho = sp.sqrt(sp.Rational(8, 3) * sp.pi * G_N * rho_r0)

    # Textbook import, natural units, g_*S = g_*. Comoving entropy s * a^3.
    s_rad = (
        sp.Rational(4, 3)
        * (sp.pi**2 * g_star / 30) ** sp.Rational(1, 4)
        * rho_r0 ** sp.Rational(3, 4)
    )

    # Assumption, written before the algebra: produced particles are the dark matter,
    # and the yield n_c / s_rad is the yield that meets the present entropy.
    # n_c scales as m**(3/2), so rho_dm0 scales as m**(5/2). The positive root is unique.
    prefactor = sp.simplify(n_c / (m ** sp.Rational(3, 2)))
    if prefactor.has(m):
        raise SystemExit(f"n_c is not a pure m**(3/2) monomial: {n_c}")
    m_expr = (rho_dm0 * s_rad / (prefactor * s_0)) ** sp.Rational(2, 5)
    residual = sp.simplify(rho_dm0 - m_expr * (n_c.subs(m, m_expr) / s_rad) * s_0)
    if residual != 0:
        raise SystemExit(f"positive root misses the assumption: {residual}")
    m_reduced = sp.simplify(m_expr.subs(C, C_of_rho))
    m_reduced = sp.powdenest(m_reduced, force=True)
    m_reduced = sp.simplify(m_reduced)

    def power(expr: sp.Expr, symbol: sp.Symbol) -> sp.Expr:
        return sp.simplify(expr).as_coeff_exponent(symbol)[1]

    powers = {
        "rho_dm0": str(power(m_reduced, rho_dm0)),
        "s_0": str(power(m_reduced, s_0)),
        "g_star": str(power(m_reduced, g_star)),
        "G_N": str(power(m_reduced, G_N)),
        "rho_r0": str(power(m_reduced, rho_r0)),
        "m_in_n_c": str(power(n_c, m)),
    }
    if powers["rho_r0"] != "0":
        raise SystemExit(f"rho_r0 survived: {powers['rho_r0']}")
    if powers["rho_dm0"] != "2/5":
        raise SystemExit(f"rho_dm0 power is {powers['rho_dm0']}")

    # Adopted 2026-10-31, tier O, after the symbolic root and not before it.
    # The seam integral has no g_*. This value is the entropy weight of a
    # later bath with one shared temperature: the photon gas, two helicities.
    # A graviton is not on the list. No density is given a number.
    g_photon = sp.Integer(2)
    bare = sp.simplify(m_reduced / g_star ** sp.Rational(1, 10))
    if bare.has(g_star):
        raise SystemExit(f"g_star did not factor as a pure tenth root: {m_reduced}")
    m_photon = sp.simplify(
        sp.powdenest(bare * g_photon ** sp.Rational(1, 10), force=True)
    )
    if sp.simplify(m_photon - m_reduced.subs(g_star, g_photon)) != 0:
        raise SystemExit("photon substitution missed the tenth-root factor")
    if set(m_photon.free_symbols) != {G_N, rho_dm0, s_0}:
        raise SystemExit(
            f"photon root kept an unexpected symbol: {m_photon.free_symbols}"
        )

    s_rad_photon = s_rad.subs(g_star, g_photon)
    n_at_photon = n_c.subs({m: m_photon, C: C_of_rho})
    residual_photon = sp.simplify(
        rho_dm0 - m_photon * (n_at_photon / s_rad_photon) * s_0
    )
    if residual_photon != 0:
        raise SystemExit(f"photon root misses the assumption: {residual_photon}")

    # Adopted 2026-10-31, tier O. Comoving photon entropy is conserved.
    # Dividing the yield by D multiplies this root by D**(2/5). D = 1.
    D = sp.symbols("D", positive=True)
    m_diluted = m_photon * D ** sp.Rational(2, 5)
    n_diluted = n_c.subs({m: m_diluted, C: C_of_rho})
    residual_diluted = sp.simplify(
        rho_dm0 - m_diluted * (n_diluted / s_rad_photon) * s_0 / D
    )
    if residual_diluted != 0:
        raise SystemExit(f"dilution power is not 2/5: {residual_diluted}")
    if sp.simplify(m_diluted.subs(D, 1) - m_photon) != 0:
        raise SystemExit("D = 1 did not recover the photon root")

    pref_expr = sp.simplify(
        m_photon
        * G_N ** sp.Rational(3, 10)
        * s_0 ** sp.Rational(2, 5)
        / rho_dm0 ** sp.Rational(2, 5)
    )
    if pref_expr.free_symbols:
        raise SystemExit(f"prefactor kept a symbol: {pref_expr}")
    number = conditional_mass(mp.mpf(str(sp.N(pref_expr, 50))))

    free = sorted(str(s) for s in m_reduced.free_symbols)
    free_photon = sorted(str(s) for s in m_photon.free_symbols)
    factor_exact = g_photon ** sp.Rational(1, 10)
    receipt = {
        "construction": "seam_mass_symbols",
        "status": "photon_ruler_dilution_one",
        "gamma": "m*C",
        "yukawa": "closed",
        "I": "1/(8*pi**(3/2))",
        "assumption_before_solve": "rho_dm0 = m * (n_c / s_rad) * s_0",
        "assumption_tier": "O",
        "entropy_import": "(4/3)*(pi**2*g_star/30)**(1/4)*rho_r0**(3/4)",
        "entropy_tier": "C",
        "entropy_unit_system": "hbar = c = k_B = 1, g_*S = g_*",
        "constraint": "C**2 = 8*pi*G_N*rho_r0/3",
        "n_c": str(n_c),
        "m_expression": str(m_reduced),
        "powers": powers,
        "free_symbols_before_declaration": free,
        "g_star_declaration": {
            "adopted": True,
            "date": "2026-10-31",
            "tier": "O",
            "value": 2,
            "species": "photon, two helicities",
            "graviton_included": False,
            "seam_theorem": False,
            "job_b_seam_row": "unchanged null",
            "sentence": (
                "The seam has no thermal epoch. g_* is the entropy weight "
                "of a later bath in which every relativistic species shares "
                "one temperature. The adopted bath is the photon gas."
            ),
        },
        "g_star_factor": "2**(1/10)",
        "g_star_factor_numeric": str(sp.N(factor_exact, 20)),
        "m_expression_photon_ruler": str(m_photon),
        "free_symbols": free_photon,
        "dilution_declaration": {
            "adopted": True,
            "date": "2026-10-31",
            "tier": "O",
            "value": 1,
            "power_on_m": "2/5",
            "sentence": (
                "Comoving photon entropy is conserved between the ruler "
                "and today. The dilution ratio is 1."
            ),
        },
        "prefactor": str(pref_expr),
        "numeric_mass": number,
    }
    text = json.dumps(receipt, indent=2)
    out = "/home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/seam_mass_symbols.json"
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
