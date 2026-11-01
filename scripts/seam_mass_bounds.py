#!/usr/bin/env python3
"""Bound check for the conditional seam mass. The mass is not changed.

The object under test is a cold relic that is all of Omega_c, produced by
the seam yield. Thermal-freeze-out ceilings are recorded and not applied.
Decay ceilings apply only if a decay is added. The stack has none.
"""

from __future__ import annotations

import json

import mpmath as mp
import sympy as sp

MASS_RECEIPT = (
    "/home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/seam_mass_symbols.json"
)
OUT = "/home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/seam_mass_bounds.json"


def k_rms_identity() -> None:
    """Occupation |beta|^2 = exp(-pi k^2 / gamma). Weight is the k^2 measure."""
    k, gamma = sp.symbols("k gamma", positive=True)
    weight = k**2 * sp.exp(-sp.pi * k**2 / gamma)
    moment = sp.integrate(k**2 * weight, (k, 0, sp.oo))
    norm = sp.integrate(weight, (k, 0, sp.oo))
    mean = sp.simplify(moment / norm)
    if sp.simplify(mean - 3 * gamma / (2 * sp.pi)) != 0:
        raise SystemExit(f"k_rms identity failed: {mean}")


def main() -> None:
    mp.mp.dps = 40
    k_rms_identity()
    receipt = json.loads(open(MASS_RECEIPT, encoding="utf-8").read())
    if receipt["status"] != "photon_ruler_dilution_one":
        raise SystemExit(f"unexpected status {receipt['status']}")
    if receipt["dilution_declaration"]["value"] != 1:
        raise SystemExit("dilution ratio is not 1")
    if receipt["g_star_declaration"]["value"] != 2:
        raise SystemExit("photon ruler is not 2")
    number = receipt["numeric_mass"]
    if number["particle_name"] is not None:
        raise SystemExit("mass receipt already names a particle")
    m_GeV = mp.mpf(number["m_GeV"])

    # Planck 2018 results VI, arXiv:1807.06209, abstract.
    H0_km = mp.mpf("67.4")
    omega_m = mp.mpf("0.315")
    omega_c_h2 = mp.mpf(number["imports"]["omega_c_h2"]["value"])
    omega_c_unc = mp.mpf(number["imports"]["omega_c_h2"]["uncertainty"])
    T_K = mp.mpf(number["imports"]["T_CMB_K"]["value"])

    import scipy.constants as phys

    G = mp.mpf(str(phys.physical_constants["Newtonian constant of gravitation"][0]))
    hbar = mp.mpf(str(phys.physical_constants["reduced Planck constant"][0]))
    c = mp.mpf(str(phys.physical_constants["speed of light in vacuum"][0]))
    k_B = mp.mpf(str(phys.physical_constants["Boltzmann constant"][0]))
    e = mp.mpf(str(phys.physical_constants["elementary charge"][0]))
    GeV_J = mp.mpf("1e9") * e
    Mpc = mp.mpf(str(phys.parsec)) * mp.mpf("1e6")
    H0 = H0_km * mp.mpf("1e3") / Mpc

    # Photon bath only, g_star = 2. rho = (pi**2/30)*g*T**4.
    T_GeV = k_B * T_K / GeV_J
    rho_gamma_GeV4 = (mp.pi**2 / 30) * 2 * T_GeV**4
    E_Pl = mp.sqrt(hbar * c**5 / G) / GeV_J
    H0_GeV = hbar * H0 / GeV_J
    rho_crit_GeV4 = 3 * H0_GeV**2 * E_Pl**2 / (8 * mp.pi)
    omega_gamma = rho_gamma_GeV4 / rho_crit_GeV4
    a_eq = omega_gamma / omega_m
    # Flat matter plus photon radiation. H**2 / H0**2 = omega_m/a**3 + omega_gamma/a**4.
    H_eq = H0_GeV * mp.sqrt(2 * omega_m / a_eq**3)

    # During radiation domination, v = sqrt(3 H / (2 pi m)). Redshift v after equality.
    v_eq = mp.sqrt(3 * H_eq / (2 * mp.pi * m_GeV))
    if v_eq >= 1:
        raise SystemExit(f"relic is still relativistic at equality: {v_eq}")
    v_today = v_eq * a_eq

    # Comoving horizon at the non-relativistic transition, radiation era.
    # v(a) = v_eq * a_eq / a, so a_nr = v_eq * a_eq.
    a_nr = v_eq * a_eq
    H_nr = H0_GeV * mp.sqrt(omega_gamma / a_nr**4)
    chi_nr_GeV_inv = 1 / (a_nr * H_nr)
    hbar_c_GeV_Mpc = (hbar * c / GeV_J) / Mpc
    chi_nr_Mpc = chi_nr_GeV_inv * hbar_c_GeV_Mpc

    # Age from the same Planck abstract parameters. Radiation omitted.
    omega_l = 1 - omega_m

    def age_integrand(a: mp.mpf) -> mp.mpf:
        hubble = H0 * mp.sqrt(omega_m / a**3 + omega_l)
        return 1 / (a * hubble)

    t0 = mp.quad(age_integrand, [mp.mpf("1e-8"), mp.mpf("1")])
    fractional = omega_c_unc / omega_c_h2
    tau_density_s = t0 / fractional

    # Local flux. Blanco and Hooper, arXiv:1811.05988, use 0.4 GeV/cm**3.
    rho_local = mp.mpf("0.4") * mp.mpf("1e6")
    n_local = rho_local / m_GeV
    v_halo = mp.mpf("220e3")
    year = mp.mpf("365.25") * mp.mpf("86400")
    flux_year = n_local * v_halo * year

    # Schwarzschild radius over the Compton length: 2 (m/M_Pl)**2.
    rs_over_compton = 2 * (m_GeV / E_Pl) ** 2

    gk_TeV = mp.mpf("340")
    m_TeV = m_GeV / mp.mpf("1000")
    rows = [
        {
            "limit": "Griest and Kamionkowski, Phys. Rev. Lett. 64 615 (1990)",
            "statement": "A stable elementary particle that was once in thermal equilibrium cannot exceed 340 TeV.",
            "mass_over_limit": mp.nstr(m_TeV / gk_TeV, 12),
            "applies": False,
            "reason": "The seam yield is a Bogoliubov occupation, and the massless limit has beta = 0. The particle was not placed in thermal equilibrium.",
        },
        {
            "limit": "Smirnov and Beacom, arXiv:1904.11503",
            "statement": "For a thermal WIMP the unitarity ceiling falls below 100 TeV, or to 140 TeV in the self-conjugate case. The 340 TeV figure assumed Omega h^2 = 1.",
            "applies": False,
            "reason": "The premise is still thermal freeze-out.",
        },
        {
            "limit": "Blanco and Hooper, arXiv:1811.05988, introduction",
            "statement": "CMB and large-scale structure require a lifetime no less than about 2e19 s even when the decay products are invisible.",
            "imported_floor_s": "2e19",
            "applies": False,
            "reason": "The floor binds a particle that decays. This stack has no decay.",
        },
        {
            "limit": "Blanco and Hooper, arXiv:1811.05988, abstract and section 1",
            "statement": "For Standard Model decay channels and masses from 10 GeV to 1 EeV, the lifetime is generally above (1-5)e28 s.",
            "mass_inside_quoted_window": bool(mp.mpf("10") <= m_GeV <= mp.mpf("1e9")),
            "applies": False,
            "reason": "The window contains this mass. The limit still needs a decay into a Standard Model state. This stack has none.",
        },
        {
            "limit": "Direct-detection cross section",
            "statement": "Published nuclear-recoil limits at this mass constrain a nucleon cross section. The local flux is large enough that the exposure is not empty.",
            "applies": False,
            "reason": "The stack specifies no cross section. The mass by itself is not the excluded quantity.",
        },
        {
            "limit": "Thermal warm-dark-matter free-streaming bound",
            "statement": "A thermal keV-scale spectrum is the object those bounds exclude.",
            "applies": False,
            "reason": (
                "At photon-matter equality the seam spectrum has v = "
                + mp.nstr(v_eq, 6)
                + ". A thermal keV spectrum is a different object."
            ),
        },
    ]
    if rs_over_compton >= 1:
        raise SystemExit("conditional mass is inside its Schwarzschild radius")

    report = {
        "construction": "seam_mass_bounds",
        "status": "no_imported_limit_excludes_the_mass",
        "mass_GeV": number["m_GeV"],
        "mass_changed": False,
        "particle_name": None,
        "statement": (
            "The mass "
            + number["m_GeV"]
            + " GeV is held fixed. No imported limit excludes the mass. No particle is named."
        ),
        "tier": "O",
        "object": "cold relic, all of Omega_c, seam yield, no decay in the stack",
        "velocity_today": mp.nstr(v_today, 12),
        "velocity_at_equality": mp.nstr(v_eq, 12),
        "equality_scale_factor": mp.nstr(a_eq, 12),
        "comoving_horizon_at_nonrelativistic_transition_Mpc": mp.nstr(chi_nr_Mpc, 12),
        "nonrelativistic_transition_before_equality": True,
        "schwarzschild_over_compton": mp.nstr(rs_over_compton, 12),
        "age_s_from_planck_abstract": mp.nstr(t0, 12),
        "omega_fractional_half_width": mp.nstr(fractional, 12),
        "lifetime_to_stay_inside_omega_band_s": mp.nstr(tau_density_s, 12),
        "local_density_GeV_per_cm3": "0.4",
        "local_density_source": "Blanco and Hooper, arXiv:1811.05988, section 3.1",
        "halo_speed_m_per_s": "220000",
        "local_flux_per_m2_per_year": mp.nstr(flux_year, 12),
        "rows": rows,
    }
    text = json.dumps(report, indent=2)
    with open(OUT, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
