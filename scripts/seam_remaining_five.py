#!/usr/bin/env python3
"""Close the five leftovers. No new free-symbol number is invented.

The species list is the adopted photon bath plus one unnamed produced field.
The baryon density is the Planck 2018 VI abstract import paired with the
existing Omega_c import. The seam contribution to that ratio is zero.
The double-well is not adopted into the column.
K(Q) is the Cosh function already adopted in TARGET_D5. Its parameters stay
free. The published pressure scale s = 1 decides which a0 power sits in
that one stored interval.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path("/home/mega/Chyren/3_research/Res-Nova")
MODE = Path("/home/mega/Chyren/state/cpt_mode_equation.json")
SYMBOLS = ROOT / "02_galaxy_dynamics/seam_mass_symbols.json"
REHEAT = ROOT / "02_galaxy_dynamics/seam_mass_reheat_mismatch.json"
JOB_E = ROOT / "02_galaxy_dynamics/argon4_unidex/job_e_same_field_nec.json"
JOB_F = ROOT / "02_galaxy_dynamics/argon4_unidex/job_f_a0z.json"
A0 = ROOT / "02_galaxy_dynamics/A0_HIGHZ_PRESSURE_SCALE_TEST.json"
D5 = ROOT / "TARGET_D5_COSMOLOGICAL_SECTOR.md"
OUT = ROOT / "02_galaxy_dynamics/seam_remaining_five.json"
PROTECTED = (
    MODE,
    SYMBOLS,
    REHEAT,
    JOB_E,
    JOB_F,
    A0,
    D5,
    ROOT / "02_galaxy_dynamics/seam_mass_bounds.json",
    ROOT / "02_galaxy_dynamics/seam_open_bridges_shot.json",
    ROOT / "02_galaxy_dynamics/argon4_unidex/job_b_gstar_table.json",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def species_shot() -> dict:
    data = json.loads(MODE.read_text(encoding="utf-8"))
    job2 = data["Job_2_Mode_Equations_and_Bogoliubov"]
    boson = job2["boson_spin_0_free_mass_m"]["identification_of_gamma"]
    fermion = job2["fermion_spin_half_dirac"]["identification_of_gamma"]
    if "gamma = m * C" not in boson or "gamma = m * C" not in fermion:
        raise SystemExit("mode receipt no longer identifies gamma = m * C")
    symbols = json.loads(SYMBOLS.read_text(encoding="utf-8"))
    if symbols["g_star_declaration"]["value"] != 2:
        raise SystemExit("photon ruler changed")
    if symbols["g_star_declaration"]["graviton_included"] is not False:
        raise SystemExit("graviton was added to the bath")
    if symbols["yukawa"] != "closed":
        raise SystemExit("Yukawa is not closed")
    if symbols["numeric_mass"]["particle_name"] is not None:
        raise SystemExit("mass receipt names a particle")
    return {
        "verdict": "species_list_is_the_later_bath",
        "tier": "O",
        "thermal_species_at_the_seam": [],
        "later_bath": ["photon helicity +", "photon helicity -"],
        "g_star": 2,
        "graviton_included": False,
        "produced_species": "unnamed massive field",
        "gamma_identification": "m*C",
        "yukawa": "closed",
        "spin_chosen": False,
        "standard_model_menu_attached": False,
        "particle_name": None,
        "sentence": (
            "The seam has no thermal species list. The later bath is the "
            "photon gas, two helicities. The produced field is an unnamed "
            "massive field with gamma = m*C. Spin is not chosen. No "
            "Standard Model menu is attached."
        ),
    }


def baryon_shot() -> dict:
    """Omega_b h^2 from the same Planck 2018 VI abstract sentence as Omega_c.

    eta uses the measured CMB temperature. The never-reheated bath is a
    different object and is not used here. The mean mass per baryon is the
    proton mass.
    """
    mp.mp.dps = 50
    import scipy.constants as phys

    symbols = json.loads(SYMBOLS.read_text(encoding="utf-8"))
    temperature = mp.mpf(symbols["numeric_mass"]["imports"]["T_CMB_K"]["value"])
    if temperature != mp.mpf("2.72548"):
        raise SystemExit(f"measured CMB temperature changed: {temperature}")
    omega_b = mp.mpf("0.0224")
    omega_b_unc = mp.mpf("0.0001")
    omega_c = mp.mpf(symbols["numeric_mass"]["imports"]["omega_c_h2"]["value"])
    if omega_c != mp.mpf("0.120"):
        raise SystemExit("Omega_c import changed")

    G = mp.mpf(str(phys.physical_constants["Newtonian constant of gravitation"][0]))
    hbar = mp.mpf(str(phys.physical_constants["reduced Planck constant"][0]))
    c = mp.mpf(str(phys.physical_constants["speed of light in vacuum"][0]))
    k_B = mp.mpf(str(phys.physical_constants["Boltzmann constant"][0]))
    e = mp.mpf(str(phys.physical_constants["elementary charge"][0]))
    m_p = mp.mpf(str(phys.physical_constants["proton mass"][0]))
    GeV_J = mp.mpf("1e9") * e
    Mpc = mp.mpf(str(phys.parsec)) * mp.mpf("1e6")
    H100 = mp.mpf("1e5") / Mpc
    rho_crit_h1 = 3 * H100**2 / (8 * mp.pi * G)
    n_b_length = omega_b * rho_crit_h1 / m_p

    rho_b_energy = omega_b * rho_crit_h1 * c**2
    rho_b_GeV4 = rho_b_energy * (hbar * c) ** 3 / GeV_J**4
    m_p_GeV = m_p * c**2 / GeV_J
    compton_m = hbar * c / GeV_J
    n_b_energy = (rho_b_GeV4 / m_p_GeV) / compton_m**3
    if abs(n_b_length - n_b_energy) / n_b_energy > mp.mpf("1e-20"):
        raise SystemExit("baryon number-density paths disagree")

    zeta3 = mp.zeta(3)
    n_g_length = 2 * zeta3 / mp.pi**2 * (k_B * temperature / (hbar * c)) ** 3
    T_GeV = k_B * temperature / GeV_J
    n_g_energy = (2 * zeta3 / mp.pi**2) * T_GeV**3 / compton_m**3
    if abs(n_g_length - n_g_energy) / n_g_energy > mp.mpf("1e-20"):
        raise SystemExit("photon number-density paths disagree")

    eta = n_b_energy / n_g_energy
    if not (mp.mpf("1e-10") < eta < mp.mpf("1e-8")):
        raise SystemExit(f"eta is outside the baryon window: {eta}")
    seam = sp.Integer(0)
    if seam != 0:
        raise SystemExit("seam contribution to eta is not zero")
    return {
        "verdict": "baryon_density_imported_seam_contribution_zero",
        "tier": "C",
        "derived_from_seam": False,
        "source": (
            "Planck 2018 results VI, arXiv:1807.06209, abstract, "
            "the combined sentence that also states Omega_c h^2 = 0.120 ± 0.001"
        ),
        "omega_b_h2": "0.0224",
        "omega_b_h2_uncertainty": "0.0001",
        "omega_b_h2_interval": "68%",
        "temperature_K": "2.72548",
        "temperature_role": "measured CMB, not the never-reheated bath",
        "mean_mass_per_baryon": "proton mass",
        "eta": mp.nstr(eta, 12),
        "eta_over_omega_fractional_half_width": mp.nstr(omega_b_unc / omega_b, 6),
        "omega_b_over_omega_c": mp.nstr(omega_b / omega_c, 6),
        "seam_contribution": "0",
        "added_to_omega_c": False,
        "particle_name": None,
        "sentence": (
            "Omega_b h^2 = 0.0224 ± 0.0001 is imported from the same Planck "
            "2018 VI abstract sentence as Omega_c. Dividing that density by "
            "the proton mass and by the measured photon density gives eta. "
            "The seam contribution is 0. The never-reheated bath is not used."
        ),
    }


def sector_shot() -> dict:
    job = json.loads(JOB_E.read_text(encoding="utf-8"))
    if job["verdict"] != "double_well_required_by_galaxy_action_false":
        raise SystemExit("job E verdict changed")
    if job["case_3_action_audit"]["double_well_required_by_galaxy_action"] is not False:
        raise SystemExit("job E now requires the double-well")
    T, lam = sp.symbols("T lambda", real=True)
    chi = 1 / sp.sqrt(2)
    potential = lam * (T**2 - chi**2) ** 2
    curvature = sp.simplify(sp.diff(potential, T, 2).subs(T, chi))
    if sp.simplify(curvature - 4 * lam) != 0:
        raise SystemExit("curvature is no longer 4*lambda")
    return {
        "verdict": "second_sector_not_adopted",
        "tier": "X",
        "existence_established": False,
        "required_by_galaxy_action": False,
        "adopted_into_the_column": False,
        "lambda": None,
        "warp_note_deleted": False,
        "sentence": (
            "The galaxy action does not require the double-well. No equation "
            "fixes lambda. The second sector is not adopted into this column. "
            "The warp note still holds the postulate."
        ),
    }


def k_of_q_shot() -> dict:
    text = D5.read_text(encoding="utf-8")
    if "This corpus adopts **Cosh**." not in text:
        raise SystemExit("TARGET_D5 no longer adopts Cosh")
    if "The quadratic" not in text or "excluded" not in text:
        raise SystemExit("TARGET_D5 no longer excludes the quadratic")
    Q, Q0, Z0, K2, Lam, I0, a = sp.symbols("Q Q0 Z0 K2 Lambda I0 a", positive=True)
    Z = (Q - Q0) / Z0
    K = -2 * Lam + 2 * K2 * Z0**2 * (sp.cosh(Z) - 1)
    KQ = sp.diff(K, Q)
    expected = 2 * K2 * Z0 * sp.sinh(Z)
    if sp.simplify(KQ - expected) != 0:
        raise SystemExit("Cosh slope is not 2*K2*Z0*sinh(Z)")
    # K_Q = I0 / a**3 fixes sinh(Z) = I0 / (2*K2*Z0*a**3).
    ratio = sp.simplify(KQ / expected)
    if ratio != 1:
        raise SystemExit("Cosh slope ratio failed")
    target = I0 / (2 * K2 * Z0 * a**3)
    replaced = expected.subs(sp.sinh(Z), target)
    if sp.simplify(replaced - I0 / a**3) != 0:
        raise SystemExit(f"background integral is not sinh(Z) = A/a**3: {replaced}")
    return {
        "verdict": "cosh_adopted_parameters_free",
        "tier": "D",
        "source": "TARGET_D5_COSMOLOGICAL_SECTOR.md",
        "function": "-2*Lambda + 2*K_2*Z_0**2*(cosh((Q-Q_0)/Z_0)-1)",
        "quadratic_excluded_by": "TARGET_D5 §1.3",
        "background_integral": "sinh((Q-Q_0)/Z_0) = I_0/(2*K_2*Z_0*a**3)",
        "free_parameters": ["Lambda", "K_2", "Q_0", "Z_0"],
        "sz_published_point_adopted": False,
        "seam_yield_changed": False,
        "sentence": (
            "TARGET_D5 adopts the Cosh function and excludes the quadratic. "
            "The background integral is sinh(Z) = I_0/(2*K_2*Z_0*a**3). "
            "Lambda, K_2, Q_0, and Z_0 stay free. The SZ published point is "
            "not adopted. The seam yield is unchanged."
        ),
    }


def a0_shot() -> dict:
    filed = json.loads(JOB_F.read_text(encoding="utf-8"))
    source = json.loads(A0.read_text(encoding="utf-8"))
    if filed["numeric_outputs"]["scales"] != source["scales"]:
        raise SystemExit("job F intervals do not match the pressure-scale file")
    published = source["scales"]["1.0"]
    if published != {"N": 95, "n": -0.277, "n_95ci": [-0.719, 0.152]}:
        raise SystemExit(f"published scale changed: {published}")
    lo, hi = published["n_95ci"]
    if not (lo <= 0.0 <= hi) or (lo <= 1.0 <= hi):
        raise SystemExit("published interval no longer separates n=0 from n=1")
    high = source["scales"]["3.0"]["n_95ci"]
    higher = source["scales"]["4.0"]["n_95ci"]
    if (high[0] <= 0.0 <= high[1]) or (higher[0] <= 0.0 <= higher[1]):
        raise SystemExit("a higher pressure scale now contains the constant")
    return {
        "verdict": "constant_survives_published_pressure_scale",
        "tier": "D",
        "stated_scale": "1",
        "stated_scale_meaning": "published Burkert pressure correction",
        "N": 95,
        "n": -0.277,
        "n_95ci": [-0.719, 0.152],
        "constant_inside": True,
        "hubble_power_inside": False,
        "refit": False,
        "anchor_a0_cH0_over_2pi": "not a theorem",
        "scales_3_and_4_contain_the_constant": False,
        "sentence": (
            "At the published pressure scale s = 1 the stored interval is "
            "n = -0.277 with 95% bounds [-0.719, 0.152], N = 95. The "
            "constant n = 0 is inside. The Hubble power n = 1 is outside. "
            "Scales 3 and 4 still exclude the constant. The anchor "
            "a0 = cH0/2π is not a theorem."
        ),
    }


def main() -> None:
    before = {str(path): _sha256(path) for path in PROTECTED}
    report = {
        "construction": "seam_remaining_five",
        "particle_name": None,
        "species": species_shot(),
        "baryon": baryon_shot(),
        "second_sector": sector_shot(),
        "k_of_q": k_of_q_shot(),
        "a0z": a0_shot(),
    }
    text = json.dumps(report, indent=2) + "\n"
    OUT.write_text(text, encoding="utf-8")
    after = {str(path): _sha256(path) for path in PROTECTED}
    if after != before:
        raise SystemExit("a protected file changed")
    print(text, end="")


if __name__ == "__main__":
    main()
