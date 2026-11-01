#!/usr/bin/env python3
"""Adopt the never-reheated photon temperature as the conditional mass.

The mass receipt keeps the measured-CMB evaluation and is not rewritten.
g_star stays 2. The dilution ratio stays 1. The conditional mass in force
is the never-reheated evaluation printed here. The measured temperature
already includes electron-positron reheating, so a photon bath that never
received that entropy is cooler, at the same scale factor, by (4/11)**(1/3).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path("/home/mega/Chyren/3_research/Res-Nova")
MASS_RECEIPT = ROOT / "02_galaxy_dynamics/seam_mass_symbols.json"
OUT = ROOT / "02_galaxy_dynamics/seam_mass_reheat_mismatch.json"
UNCHANGED = (
    MASS_RECEIPT,
    ROOT / "02_galaxy_dynamics/seam_mass_bounds.json",
    Path("/home/mega/Chyren/state/cpt_mode_equation.json"),
    ROOT / "02_galaxy_dynamics/argon4_unidex/job_b_gstar_table.json",
)
STORED_MASS = "344685566.44462858219"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mpf(value: str) -> mp.mpf:
    return mp.mpf(value)


def heating_ratio() -> sp.Rational:
    """Entropy dumped into the photons by electron-positron annihilation.

    Photons contribute 2. Electrons and positrons contribute 4 * 7/8 = 7/2.
    After the pairs annihilate, that entropy is carried by the photons alone,
    so the temperature ratio is ((2 + 7/2) / 2)**(1/3) = (11/4)**(1/3).
    Neutrinos are the unheated clock. They are not inserted as g_star.
    """
    g_gamma = sp.Integer(2)
    g_pairs = 4 * sp.Rational(7, 8)
    if g_pairs != sp.Rational(7, 2):
        raise SystemExit(f"pair weight is not 7/2: {g_pairs}")
    ratio = sp.simplify((g_gamma + g_pairs) / g_gamma)
    if ratio != sp.Rational(11, 4):
        raise SystemExit(f"heating ratio is not 11/4: {ratio}")
    if sp.Rational(1, 3) * sp.Rational(6, 5) != sp.Rational(2, 5):
        raise SystemExit("temperature power on the mass is not 2/5")
    return ratio


def mass_at(pref: mp.mpf, temperature: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    """Same two unit paths as the mass receipt. g_star stays the literal 2."""
    mp.mp.dps = 50
    import scipy.constants as phys

    G_val, G_unit, _ = phys.physical_constants["Newtonian constant of gravitation"]
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

    G = _mpf(str(G_val))
    hbar = _mpf(str(hbar_val))
    c = _mpf(str(c_val))
    k_B = _mpf(str(k_val))
    e = _mpf(str(e_val))
    GeV_J = _mpf("1e9") * e
    Mpc = _mpf(str(phys.parsec)) * _mpf("1e6")
    H100 = _mpf("1e5") / Mpc
    omega = _mpf("0.120")
    g_star = 2

    rho_mass = 3 * H100**2 / (8 * mp.pi * G)
    rho_energy = rho_mass * c**2 * omega
    s_per_m3 = (2 * mp.pi**2 / 45) * g_star * (k_B * temperature / (hbar * c)) ** 3
    G_nat = G * hbar / c**3
    rho_per_m4 = rho_energy / (hbar * c)
    m_per_m = (
        pref
        * rho_per_m4 ** mp.mpf("0.4")
        / (G_nat ** mp.mpf("0.3") * s_per_m3 ** mp.mpf("0.4"))
    )
    m_GeV_length = m_per_m * hbar * c / GeV_J

    rho_GeV4 = rho_energy * (hbar * c) ** 3 / GeV_J**4
    T_GeV = k_B * temperature / GeV_J
    s_GeV3 = (2 * mp.pi**2 / 45) * g_star * T_GeV**3
    E_Pl = mp.sqrt(hbar * c**5 / G) / GeV_J
    G_GeV = 1 / E_Pl**2
    m_GeV_energy = (
        pref
        * rho_GeV4 ** mp.mpf("0.4")
        / (G_GeV ** mp.mpf("0.3") * s_GeV3 ** mp.mpf("0.4"))
    )
    return m_GeV_length, m_GeV_energy


def main() -> None:
    mp.mp.dps = 50
    before = {str(path): _sha256(path) for path in UNCHANGED}
    receipt = json.loads(MASS_RECEIPT.read_text(encoding="utf-8"))
    if receipt["status"] != "photon_ruler_dilution_one":
        raise SystemExit(f"unexpected status {receipt['status']}")
    if receipt["dilution_declaration"]["value"] != 1:
        raise SystemExit("dilution ratio is not 1")
    if receipt["g_star_declaration"]["value"] != 2:
        raise SystemExit("photon ruler is not 2")
    number = receipt["numeric_mass"]
    if number["particle_name"] is not None:
        raise SystemExit("mass receipt names a particle")
    if number["m_GeV"] != STORED_MASS:
        raise SystemExit(f"stored mass changed: {number['m_GeV']}")

    heating = heating_ratio()
    pref_expr = sp.sympify(receipt["prefactor"], locals={"pi": sp.pi})
    if pref_expr.free_symbols:
        raise SystemExit(f"prefactor kept a symbol: {pref_expr.free_symbols}")
    # The mass receipt builds this prefactor at mpmath's default 15 digits.
    mp.mp.dps = 15
    pref = _mpf(str(sp.N(pref_expr, 50)))
    mp.mp.dps = 50

    measured = _mpf("2.72548")
    length, energy = mass_at(pref, measured)
    relative = abs(length - energy) / energy
    if relative > _mpf("1e-20"):
        raise SystemExit(f"unit paths disagree at the measured temperature: {relative}")
    recomputed = mp.nstr(energy, 20)
    if recomputed != STORED_MASS:
        raise SystemExit(f"recomputed mass {recomputed} != stored {STORED_MASS}")

    # Cooler bath: same scale factor, no electron-positron entropy in the photons.
    cooler = measured / mp.power(mp.mpf(heating), mp.mpf(1) / 3)
    cool_length, cool_energy = mass_at(pref, cooler)
    cool_relative = abs(cool_length - cool_energy) / cool_energy
    if cool_relative > _mpf("1e-20"):
        raise SystemExit(
            f"unit paths disagree at the unreheated temperature: {cool_relative}"
        )

    factor = mp.power(mp.mpf(heating), mp.mpf(2) / 5)
    stored = _mpf(STORED_MASS)
    from_factor = stored * factor
    ratio = cool_energy / energy
    factor_relative = abs(ratio - factor) / factor
    if factor_relative > _mpf("1e-18"):
        raise SystemExit(
            f"temperature path and (11/4)**(2/5) disagree: {factor_relative}"
        )

    shift = from_factor - stored
    omega = [mp.mpf(edge) for edge in number["omega_c_h2_band_GeV"]]
    thermometer = [mp.mpf(edge) for edge in number["T_CMB_band_GeV"]]
    omega_half = (omega[1] - omega[0]) / 2
    thermometer_half = (thermometer[1] - thermometer[0]) / 2
    conditional = mp.nstr(from_factor, 20)
    conditional_T = mp.nstr(cooler, 20)
    # Lock the digits sized on 2026-10-31. A drift is a stop, not a new mass.
    if conditional != "516602109.72238893333":
        raise SystemExit(f"never-reheated mass drifted: {conditional}")
    if conditional_T != "1.945354563857973997":
        raise SystemExit(f"never-reheated temperature drifted: {conditional_T}")
    outside = bool(from_factor < omega[0] or from_factor > omega[1])
    if not outside:
        raise SystemExit("never-reheated mass fell inside the Omega import band")

    report = {
        "construction": "seam_mass_reheat_mismatch",
        "status": "never_reheated_temperature_adopted",
        "adopted": True,
        "conditional_mass_is": "never_reheated_photon_bath",
        "conditional_m_GeV": conditional,
        "conditional_temperature_K": conditional_T,
        "stored_receipt_rewritten": False,
        "mass_changed": False,
        "g_star_changed": False,
        "dilution_changed": False,
        "particle_name": None,
        "tier": "O",
        "heating_tier": "C",
        "stored_m_GeV": STORED_MASS,
        "g_star": 2,
        "dilution_ratio": 1,
        "heating_ratio": "11/4",
        "heating_count": "(2 + 7/2)/2",
        "entropy_ratio_never_reheated_over_measured": "4/11",
        "temperature_ratio_never_reheated_over_measured": "(4/11)**(1/3)",
        "temperature_never_reheated_K": mp.nstr(cooler, 20),
        "mass_power_of_heating_ratio": "2/5",
        "mass_factor_never_reheated_over_stored": mp.nstr(factor, 20),
        "mass_if_never_reheated_GeV": mp.nstr(from_factor, 20),
        "shift_GeV": mp.nstr(shift, 20),
        "fractional_shift": mp.nstr(mp.mpf(mp.nstr(factor, 20)) - 1, 20),
        "shift_over_omega_half_width": mp.nstr(shift / omega_half, 12),
        "shift_over_thermometer_half_width": mp.nstr(shift / thermometer_half, 12),
        "lies_outside_omega_import_band": outside,
        "unit_paths_relative_difference_measured": mp.nstr(relative, 6),
        "unit_paths_relative_difference_never_reheated": mp.nstr(cool_relative, 6),
        "factor_paths_relative_difference": mp.nstr(factor_relative, 6),
        "sentence": (
            "The measured CMB temperature at g_star = 2 already includes "
            "electron-positron reheating. The adopted conditional mass uses "
            "the never-reheated photon bath at the same scale factor, cooler "
            "by (4/11)**(1/3). The mass formula prints a value heavier by "
            "(11/4)**(2/5). g_star stays 2. The dilution ratio stays 1. "
            "No particle is named. The printed mass lies outside the imported "
            "Omega_c band. The density and the dilution ratio were not "
            "retuned. The measured-temperature evaluation remains in the "
            "mass receipt."
        ),
    }
    text = json.dumps(report, indent=2) + "\n"
    OUT.write_text(text, encoding="utf-8")
    after = {str(path): _sha256(path) for path in UNCHANGED}
    if after != before:
        raise SystemExit(f"protected file changed: {before} -> {after}")
    print(text, end="")


if __name__ == "__main__":
    main()
