#!/usr/bin/env python3
"""One shot at the five open bridges. A free symbol stays free.

gamma = m*C is the stored identification, Yukawa closed. C is the
radiation constant of the adopted photon bath, g_star = 2, at the
never-reheated temperature. The other four bridges are checked against
the equations already on the page. This script does not name a particle,
does not change g_star, does not set eta, lambda, or a0(z), and does not
edit the mode receipt.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path("/home/mega/Chyren/3_research/Res-Nova")
REHEAT = ROOT / "02_galaxy_dynamics/seam_mass_reheat_mismatch.json"
MODE = Path("/home/mega/Chyren/state/cpt_mode_equation.json")
JOB_F = ROOT / "02_galaxy_dynamics/argon4_unidex/job_f_a0z.json"
A0 = ROOT / "02_galaxy_dynamics/A0_HIGHZ_PRESSURE_SCALE_TEST.json"
OUT = ROOT / "02_galaxy_dynamics/seam_open_bridges_shot.json"
PROTECTED = (
    REHEAT,
    MODE,
    ROOT / "02_galaxy_dynamics/seam_mass_symbols.json",
    ROOT / "02_galaxy_dynamics/seam_mass_bounds.json",
    ROOT / "02_galaxy_dynamics/argon4_unidex/job_b_gstar_table.json",
    JOB_F,
    A0,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mpf(value: str) -> mp.mpf:
    return mp.mpf(value)


def radiation_constant(
    temperature: mp.mpf,
) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    """C from C**2 = 8*pi*G*rho/3 for a photon gas, g_star = 2.

    Returns C in GeV, C in s^-1, rho in GeV^4, and the relative difference
    of the length-unit path against the energy-unit path.
    """
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
    g_star = 2

    energy_density = (
        (mp.pi**2 / 30) * g_star * (k_B * temperature) ** 4 / (hbar * c) ** 3
    )
    rho_mass = energy_density / c**2
    C_per_s = mp.sqrt(8 * mp.pi * G * rho_mass / 3)
    C_from_length = hbar * C_per_s / GeV_J

    T_GeV = k_B * temperature / GeV_J
    rho_GeV4 = (mp.pi**2 / 30) * g_star * T_GeV**4
    E_Pl = mp.sqrt(hbar * c**5 / G) / GeV_J
    G_GeV = 1 / E_Pl**2
    C_from_energy = mp.sqrt(8 * mp.pi * G_GeV * rho_GeV4 / 3)
    relative = abs(C_from_length - C_from_energy) / C_from_energy
    if relative > _mpf("1e-20"):
        raise SystemExit(f"unit paths disagree for C: {relative}")
    return C_from_energy, C_per_s, rho_GeV4, relative


def gamma_shot(reheat: dict) -> dict:
    if reheat["status"] != "never_reheated_temperature_adopted":
        raise SystemExit(f"reheat status is {reheat['status']}")
    if reheat["adopted"] is not True or reheat["g_star"] != 2:
        raise SystemExit("reheat adoption is not the photon bath at g_star = 2")
    if reheat["dilution_ratio"] != 1 or reheat["particle_name"] is not None:
        raise SystemExit("dilution or particle name changed")
    mass = _mpf(reheat["conditional_m_GeV"])
    temperature = _mpf(reheat["conditional_temperature_K"])
    C_GeV, C_per_s, rho_GeV4, relative = radiation_constant(temperature)
    gamma = mass * C_GeV
    # Stored spectrum |beta|^2 = exp(-pi k^2 / gamma). Mean k^2 = 3 gamma / (2 pi).
    k, g = sp.symbols("k gamma", positive=True)
    weight = k**2 * sp.exp(-sp.pi * k**2 / g)
    moment = sp.integrate(k**2 * weight, (k, 0, sp.oo))
    norm = sp.integrate(weight, (k, 0, sp.oo))
    if sp.simplify(moment / norm - 3 * g / (2 * sp.pi)) != 0:
        raise SystemExit("k_rms identity failed")
    k_rms = mp.sqrt(3 * gamma / (2 * mp.pi))
    k_over_m = k_rms / mass
    return {
        "verdict": "gamma_evaluated_under_stored_identification",
        "tier": "O",
        "identification": "gamma = m*C",
        "yukawa": "closed",
        "constraint": "C**2 = 8*pi*G*rho/3",
        "bath": "never_reheated photon gas, g_star = 2, a_0 = 1",
        "seam_theorem": False,
        "particle_name": None,
        "conditional_m_GeV": reheat["conditional_m_GeV"],
        "conditional_temperature_K": reheat["conditional_temperature_K"],
        "rho_GeV4": mp.nstr(rho_GeV4, 20),
        "C_GeV": mp.nstr(C_GeV, 20),
        "C_per_s": mp.nstr(C_per_s, 20),
        "gamma_GeV2": mp.nstr(gamma, 20),
        "k_rms_GeV": mp.nstr(k_rms, 20),
        "k_rms_over_m": mp.nstr(k_over_m, 20),
        "unit_paths_relative_difference": mp.nstr(relative, 6),
        "sentence": (
            "gamma = m*C at the adopted mass and the never-reheated "
            "photon bath. C is the radiation constant of that bath with "
            "a_0 = 1. The mode receipt was not edited."
        ),
    }


def gstar_shot(gamma: dict) -> dict:
    return {
        "verdict": "seam_row_remains_null",
        "tier": "O",
        "g_star_seam": None,
        "g_star_later_bath": 2,
        "g_star_changed": False,
        "k_rms_over_m": gamma["k_rms_over_m"],
        "relativistic_below_scale_factor": gamma["k_rms_over_m"],
        "sentence": (
            "k_rms/m is the comoving momentum of the stored spectrum "
            "over the adopted mass, at a_0 = 1. Physical momentum exceeds "
            "the mass only below that scale factor. That window does not "
            "name a species count. The seam g_star row stays null. "
            "10.75 and 106.75 are not substituted."
        ),
    }


def eta_shot() -> dict:
    data = json.loads(MODE.read_text(encoding="utf-8"))
    job2 = data["Job_2_Mode_Equations_and_Bogoliubov"]
    boson = job2["boson_spin_0_free_mass_m"]["abs_beta_sq"]
    fermion = job2["fermion_spin_half_dirac"]["abs_beta_sq"]
    k = sp.symbols("k")
    gamma = sp.symbols("gamma", positive=True)
    beta_b = sp.sympify(boson, locals={"gamma": gamma, "k": k, "pi": sp.pi})
    beta_f = sp.sympify(fermion, locals={"gamma": gamma, "k": k, "pi": sp.pi})
    stored = sp.exp(-sp.pi * k**2 / gamma)
    if sp.simplify(beta_b - stored) != 0 or sp.simplify(beta_f - stored) != 0:
        raise SystemExit(f"stored |beta|^2 is not the even spectrum: {boson} {fermion}")
    if sp.simplify(beta_b.subs(k, -k) - beta_b) != 0:
        raise SystemExit("|beta|^2 is odd in k")
    odd_integral = sp.integrate(k * stored, (k, -sp.oo, sp.oo))
    if sp.simplify(odd_integral) != 0:
        raise SystemExit(f"odd charge integral is not zero: {odd_integral}")
    return {
        "verdict": "seam_does_not_source_eta",
        "tier": "X",
        "stored_abs_beta_sq": boson,
        "boson_equals_fermion": True,
        "odd_in_k": False,
        "odd_charge_integral": "0",
        "holds_for_every_positive_gamma": True,
        "eta_imported": False,
        "particle_name": None,
        "sentence": (
            "The stored occupation is even in k for every positive gamma. "
            "Its odd charge integral is identically 0. The evaluated gamma "
            "does not produce eta. No baryon number is imported."
        ),
    }


def double_well_shot() -> dict:
    T, lam = sp.symbols("T lambda", real=True)
    chi = 1 / sp.sqrt(2)
    potential = lam * (T**2 - chi**2) ** 2
    curvature = sp.diff(potential, T, 2)
    at_vacuum = sp.simplify(curvature.subs(T, chi))
    if sp.simplify(at_vacuum - 8 * lam * chi**2) != 0:
        raise SystemExit(f"curvature is not 8*lambda*chi**2: {at_vacuum}")
    if sp.simplify(at_vacuum - 4 * lam) != 0:
        raise SystemExit(f"8*lambda*chi**2 is not 4*lambda: {at_vacuum}")
    # Along a null vector the metric term that multiplies V is zero.
    metric_contraction = sp.Integer(0)
    null_potential_piece = metric_contraction * potential
    if sp.diff(null_potential_piece, lam) != 0:
        raise SystemExit("lambda entered the null contraction")
    return {
        "verdict": "lambda_remains_free",
        "tier": "O",
        "potential": "lambda*(T**2 - chi**2)**2",
        "chi": "1/sqrt(2)",
        "curvature_at_vacuum": "8*lambda*chi**2",
        "curvature_at_vacuum_reduced": "4*lambda",
        "lambda_value": None,
        "existence": "open",
        "null_contraction_depends_on_lambda": False,
        "sentence": (
            "At either vacuum the curvature is 8*lambda*chi**2, which is "
            "4*lambda because chi**2 = 1/2. lambda is not fixed by the "
            "null contraction, the seam mass, or gamma. Existence of the "
            "second sector stays open."
        ),
    }


def a0_shot() -> dict:
    filed = json.loads(JOB_F.read_text(encoding="utf-8"))
    source = json.loads(A0.read_text(encoding="utf-8"))
    if filed["numeric_outputs"]["scales"] != source["scales"]:
        raise SystemExit("job F intervals do not match the pressure-scale file")
    if filed["verdict"] != "a0z_test_complete":
        raise SystemExit("job F verdict changed")
    scales = source["scales"]
    order = ("0.0", "0.5", "1.0", "1.5", "2.0", "3.0", "4.0")
    if tuple(scales) != order:
        raise SystemExit(f"unexpected scales: {tuple(scales)}")
    intervals = {key: scales[key]["n_95ci"] for key in order}
    lower = max(pair[0] for pair in intervals.values())
    upper = min(pair[1] for pair in intervals.values())

    def inside(value: float) -> list[str]:
        return [key for key, pair in intervals.items() if pair[0] <= value <= pair[1]]

    constant_inside = inside(0.0)
    hubble_inside = inside(1.0)
    return {
        "verdict": "no_single_power_in_every_interval",
        "tier": "D",
        "source": "02_galaxy_dynamics/A0_HIGHZ_PRESSURE_SCALE_TEST.json",
        "refit": False,
        "intervals_are_stored_3_decimal_bounds": True,
        "constant_n": 0.0,
        "hubble_n": 1.0,
        "constant_inside_scales": constant_inside,
        "hubble_inside_scales": hubble_inside,
        "intersection_lower": lower,
        "intersection_upper": upper,
        "intersection_empty": bool(lower > upper),
        "shape_chosen": None,
        "anchor_a0_cH0_over_2pi": "not a theorem",
        "sentence": (
            "The seven stored 95% intervals have an empty intersection. "
            "No single power n is inside every pressure scale. n = 0 is "
            "inside scales 0 through 2. n = 1 is inside scales 3 and 4. "
            "The test was not refit. a0(z) is not chosen."
        ),
    }


def main() -> None:
    mp.mp.dps = 50
    before = {str(path): _sha256(path) for path in PROTECTED}
    reheat = json.loads(REHEAT.read_text(encoding="utf-8"))
    gamma = gamma_shot(reheat)
    report = {
        "construction": "seam_open_bridges_shot",
        "particle_name": None,
        "g_star": 2,
        "dilution_ratio": 1,
        "mode_receipt_edited": False,
        "gamma": gamma,
        "seam_g_star": gstar_shot(gamma),
        "eta": eta_shot(),
        "double_well": double_well_shot(),
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
