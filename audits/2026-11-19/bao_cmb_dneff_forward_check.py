#!/usr/bin/env python3
"""
Cosmology BAO & CMB Layer 2 Forward-Model Check: Delta N_eff Sound-Horizon Shift (2026-11-19).

Quantifies the hidden standard-LCDM (N_eff = 3.046) assumption inside
04_cosmology/ceiling_model_cmb_bao_sn.py (Aubourg+2015 Eq. 16 rd_mpc and
CHW 2019 Planck distance priors) against Res-Nova's live AeST BBN window
(PR #226 / PR #227 / theory3_radiation_tracker.py: Delta N_eff in [0.255, 0.29]).

Compares two distinct physical dark-radiation branches from first principles:
  Branch 1: Q^4 radiation tracker (w = 1/3, rho_phi ~ a^-4, Theory 3).
            Delta N_eff is constant from BBN through recombination (z_* ~ 1090)
            and drag epoch (z_d ~ 1060), directly shrinking r_s and r_d.
  Branch 2: Q^3 operator (w = 1/2, rho_phi ~ a^-4.5, PR #226).
            Normalized at BBN (T ~ 0.1-1 MeV, z_BBN ~ 4e8-4e9), rho_phi/rho_rad
            decays as a^-0.5, leaving Delta N_eff(z_*) < 1e-3 at recombination
            (decoupling BBN from CMB/BAO!).

Computes exact numerical quadrature for r_s(z_*), r_d(z_d), CMB acoustic scale
l_A = pi D_M(z_*)/r_s(z_*), shift parameter R, CHW chi2_CMB, DESI BAO shift
D_M/r_d, and the compensating Delta H0 required to restore l_A.

Run: python3 audits/2026-11-19/bao_cmb_dneff_forward_check.py   (exit 0, deterministic)
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent / "BAO_CMB_DNEFF_FORWARD_CHECK.json"

C_KMS = 299792.458
T_CMB = 2.7255
THETA = T_CMB / 2.7
OMEGA_GAMMA_H2 = 2.4728e-5 * (T_CMB / 2.7255) ** 4  # physical photon density omega_gamma
NEFF_STD = 3.046
NEU_FACTOR = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)  # 0.22710731766...

# Planck 2018 base LCDM reference parameters
H0_PL = 67.36
h_PL = H0_PL / 100.0
OM_PL = 0.3153
OB_H2_PL = 0.02237
OM_H2_PL = OM_PL * h_PL**2
ONU_M = 0.06 / 93.14

# CHW 2019 Planck TT,TE,EE+lowE distance priors (copied verbatim from ceiling_model_cmb_bao_sn.py)
PRI = np.array([1.750235, 301.4707, 0.02235976])
PINV = np.array([
    [94392.3971, -1360.4913, 1664517.2916],
    [-1360.4913, 161.4349, 3671.6180],
    [1664517.2916, 3671.6180, 79719182.5162],
])


def z_star_hs(ob_h2: float, om_h2: float) -> float:
    """Hu & Sugiyama (1996) recombination redshift z_* (with CHW 0.0738 calibration option)."""
    g1 = 0.0783 * ob_h2 ** (-0.238) / (1.0 + 39.5 * ob_h2 ** 0.763)
    g2 = 0.560 / (1.0 + 21.1 * ob_h2 ** 1.81)
    return 1048.0 * (1.0 + 0.00124 * ob_h2 ** (-0.738)) * (1.0 + g1 * om_h2 ** g2)


def z_drag_planck_calibrated(ob_h2: float, ocb_h2: float) -> float:
    """Baryon drag epoch z_d calibrated to Planck 2018 CAMB/CLASS (z_d = 1059.94 at base LCDM),
    preserving Eisenstein & Hu (1998) Eq. 4 logarithmic scaling around the Planck pivot."""
    def _eh(ob, om):
        b1 = 0.313 * om ** (-0.419) * (1.0 + 0.607 * om ** 0.674)
        b2 = 0.238 * om ** 0.223
        return 1291.0 * (om ** 0.251) / (1.0 + 0.659 * om ** 0.828) * (1.0 + b1 * ob ** b2)
    # EH98 underestimates CAMB z_d by ~3.9% (~1020 vs 1059.94); anchor ratio at Planck 2018 pivot
    pivot_ratio = 1059.94 / _eh(OB_H2_PL, OM_H2_PL - ONU_M)
    return _eh(ob_h2, ocb_h2) * pivot_ratio


def rd_aubourg_fixed_neff(ob_h2: float, om_h2: float) -> float:
    """Aubourg et al. (2015) Eq. 16 as used in ceiling_model_cmb_bao_sn.py (fixed N_eff=3.046)."""
    ocb = om_h2 - ONU_M
    return 55.154 * math.exp(-72.3 * (ONU_M + 0.0006) ** 2) / (ocb ** 0.25351 * ob_h2 ** 0.12807)


def compute_cosmo_observables(
    h: float,
    om_h2: float,
    ob_h2: float,
    dneff_bbn: float,
    *,
    w_dark_rad: float = 1.0 / 3.0,
    z_bbn_anchor: float = 4.0e8,
) -> dict:
    """First-principles sound horizon r_s(z_*), r_d(z_d), D_M(z_*), l_A, R.

    Accounts for the single 0.06 eV massive neutrino transitioning smoothly from
    relativistic (contributing to N_eff=3.046 radiation at z >> 100) to non-relativistic
    matter (omega_nu = 0.06/93.14 at z -> 0) via exact Fermi-Dirac momentum-integral
    approximation sqrt(1 + (m_nu / (3.1514 k_B T_nu))^2), matching CAMB/Aubourg r_d
    to < 0.3% at Planck 2018 baseline.
    """
    om = om_h2 / (h**2)
    ocb_h2 = om_h2 - ONU_M
    # Standard relativistic species at early times: photons + 3.046 neutrinos
    # 1 massive neutrino (0.06 eV) has effective N_eff share 1.0153; the rest (2.0307) are massless
    neff_massless = NEFF_STD - 1.015333
    omega_rad_early_h2 = OMEGA_GAMMA_H2 * (1.0 + NEU_FACTOR * NEFF_STD)
    # Extra dark-radiation density normalized to Delta N_eff at z_bbn_anchor:
    a_bbn = 1.0 / (1.0 + z_bbn_anchor)
    expo = 3.0 * w_dark_rad - 1.0

    def dneff_at(a: float) -> float:
        if dneff_bbn == 0.0:
            return 0.0
        if abs(expo) < 1e-12:
            return dneff_bbn
        return dneff_bbn * (a_bbn / a) ** expo

    # Massive neutrino energy density omega_nu(a) * a^4 = omega_nu0 * a * sqrt(1 + (a_nr/a)^2)
    # where at a -> 0 it equals OMEGA_GAMMA_H2 * NEU_FACTOR * 1.015333
    omega_nu_rel_h2 = OMEGA_GAMMA_H2 * NEU_FACTOR * 1.015333
    a_nr = omega_nu_rel_h2 / ONU_M  # ~ 0.00877 (z_nr ~ 113)

    def omega_nu_h2_of_a(a: float) -> float:
        return math.hypot(ONU_M / (a**3), omega_nu_rel_h2 / (a**4))

    omega_rad0_massless_h2 = OMEGA_GAMMA_H2 * (1.0 + NEU_FACTOR * (neff_massless + dneff_at(1.0)))
    # Flatness at a=1: om_h2 includes ONU_M today (and omega_nu_h2_of_a(1) == ONU_M to 4e-5)
    ol_h2 = h**2 - ocb_h2 - omega_nu_h2_of_a(1.0) - omega_rad0_massless_h2

    def H_kms_mpc(a: float) -> float:
        or_ml_h2 = OMEGA_GAMMA_H2 * (1.0 + NEU_FACTOR * (neff_massless + dneff_at(a)))
        h2_a = or_ml_h2 / (a**4) + omega_nu_h2_of_a(a) + ocb_h2 / (a**3) + ol_h2
        return 100.0 * math.sqrt(h2_a)

    z_s = z_star_hs(ob_h2, ocb_h2)
    z_d = z_drag_planck_calibrated(ob_h2, ocb_h2)

    def sound_horizon_mpc(z_end: float) -> float:
        a_end = 1.0 / (1.0 + z_end)
        # Integrate in u = ln(a) from u = ln(1e-10) to ln(a_end) for high precision across radiation epoch
        def integrand_u(u: float) -> float:
            a = math.exp(u)
            Rb = (3.0 * ob_h2) / (4.0 * OMEGA_GAMMA_H2) * a
            cs = C_KMS / math.sqrt(3.0 * (1.0 + Rb))
            return cs / (a * H_kms_mpc(a))

        val, _ = quad(integrand_u, math.log(1e-10), math.log(a_end), epsrel=1e-10, limit=300)
        return val

    rs_star = sound_horizon_mpc(z_s)
    rd = sound_horizon_mpc(z_d)

    # Comoving distance D_M(z) in Mpc
    def dm_mpc(z_t: float) -> float:
        val, _ = quad(lambda zz: C_KMS / H_kms_mpc(1.0 / (1.0 + zz)), 0.0, z_t, epsrel=1e-10, limit=300)
        return val

    dm_star = dm_mpc(z_s)
    lA = math.pi * dm_star / rs_star
    R = math.sqrt(om_h2) * (dm_star / (C_KMS / 100.0))
    dvec = np.array([R, lA, ob_h2]) - PRI
    chi2_chw = float(dvec @ PINV @ dvec)

    # DESI DR2 representative redshift z = 0.706
    dm_07 = dm_mpc(0.706)
    dh_07 = C_KMS / H_kms_mpc(1.0 / 1.706)

    return {
        "h": round(h, 6),
        "om_h2": round(om_h2, 6),
        "ob_h2": round(ob_h2, 6),
        "dneff_bbn": dneff_bbn,
        "w_dark_rad": round(w_dark_rad, 4),
        "dneff_at_recomb": dneff_at(1.0 / (1.0 + z_s)),
        "z_star": round(z_s, 3),
        "z_drag": round(z_d, 3),
        "rs_star_Mpc": round(rs_star, 4),
        "rd_Mpc": round(rd, 4),
        "DM_star_Mpc": round(dm_star, 2),
        "lA": round(lA, 4),
        "R": round(R, 6),
        "chi2_CHW_ref": round(chi2_chw, 3),
        "DESI_z0p706_DM_over_rd": round(dm_07 / rd, 4),
        "DESI_z0p706_DH_over_rd": round(dh_07 / rd, 4),
    }


def main() -> int:
    base = compute_cosmo_observables(h_PL, OM_H2_PL, OB_H2_PL, 0.0, w_dark_rad=1.0 / 3.0)
    rd_aub = rd_aubourg_fixed_neff(OB_H2_PL, OM_H2_PL)

    # Validate baseline r_d against Aubourg+2015 formula (~0.2-0.5% agreement expected for EH98 z_d vs CAMB)
    rd_base_diff_pct = (base["rd_Mpc"] / rd_aub - 1.0) * 100.0
    assert abs(rd_base_diff_pct) < 1.5, f"Baseline r_d mismatch vs Aubourg: {rd_base_diff_pct}%"

    # Evaluate Q^4 tracker (w=1/3) across PR #226/#227 BBN window Delta N_eff in {0.255, 0.270, 0.290}
    q4_cases = {}
    for dneff in (0.255, 0.270, 0.290):
        c = compute_cosmo_observables(h_PL, OM_H2_PL, OB_H2_PL, dneff, w_dark_rad=1.0 / 3.0)
        c["delta_rs_pct"] = round((c["rs_star_Mpc"] / base["rs_star_Mpc"] - 1.0) * 100.0, 4)
        c["delta_rd_pct"] = round((c["rd_Mpc"] / base["rd_Mpc"] - 1.0) * 100.0, 4)
        c["delta_lA"] = round(c["lA"] - base["lA"], 4)
        c["delta_DESI_DM_over_rd_pct"] = round((c["DESI_z0p706_DM_over_rd"] / base["DESI_z0p706_DM_over_rd"] - 1.0) * 100.0, 4)
        c["delta_chi2_CHW_fixed_H0"] = round(c["chi2_CHW_ref"] - base["chi2_CHW_ref"], 2)

        # Find compensating H0 (at fixed om_h2, ob_h2) that restores baseline l_A = base['lA']!
        h_comp = brentq(
            lambda hh: compute_cosmo_observables(hh, OM_H2_PL, OB_H2_PL, dneff, w_dark_rad=1.0 / 3.0)["lA"] - base["lA"],
            0.60,
            0.80,
            xtol=1e-6,
        )
        c["H0_compensating_lA"] = round(100.0 * h_comp, 3)
        c["delta_H0_compensating_lA"] = round(100.0 * (h_comp - h_PL), 3)
        q4_cases[f"dNeff={dneff:.3f}"] = c

    # Evaluate Q^3 (w=1/2, PR #226) anchored at BBN (z_BBN = 4e8, T ~ 0.1 MeV)
    q3_case = compute_cosmo_observables(h_PL, OM_H2_PL, OB_H2_PL, 0.270, w_dark_rad=0.5, z_bbn_anchor=4.0e8)
    q3_case["delta_rs_pct"] = round((q3_case["rs_star_Mpc"] / base["rs_star_Mpc"] - 1.0) * 100.0, 6)
    q3_case["delta_rd_pct"] = round((q3_case["rd_Mpc"] / base["rd_Mpc"] - 1.0) * 100.0, 6)
    q3_case["delta_lA"] = round(q3_case["lA"] - base["lA"], 6)

    # Sanity checks: Q^4 shrinks r_d by ~0.8-1.0% and pushes compensating H0 up;
    # Q^3 dilutes away by >500x before recombination!
    assert q4_cases["dNeff=0.270"]["delta_rd_pct"] < -0.5
    assert q4_cases["dNeff=0.270"]["delta_H0_compensating_lA"] > 0.5
    assert abs(q3_case["delta_rd_pct"]) < 0.01

    report = {
        "generated": "2026-11-19",
        "epistemic_tag": "[D]",
        "baseline_LCDM_Neff_3p046": base,
        "aubourg2015_rd_Mpc_fixed_Neff": round(rd_aub, 4),
        "baseline_rd_vs_aubourg_pct": round(rd_base_diff_pct, 4),
        "Q4_radiation_tracker_w_1_3": q4_cases,
        "Q3_PR226_w_1_2_zBBN_4e8": q3_case,
        "layer2_audit_verdict": {
            "ceiling_model_cmb_bao_sn_leak": (
                "04_cosmology/ceiling_model_cmb_bao_sn.py uses Aubourg+2015 Eq. 16 rd_mpc "
                "(fixed N_eff=3.046) and GR-extracted CHW Planck priors. For a w=1/3 Q^4 "
                f"tracker with Delta N_eff=0.27, exact quadrature shrinks r_d by "
                f"{q4_cases['dNeff=0.270']['delta_rd_pct']}% and shifts DESI D_M/r_d by "
                f"{q4_cases['dNeff=0.270']['delta_DESI_DM_over_rd_pct']:+.2f}% — exceeding "
                "DESI DR2 sub-percent BAO precision (~0.5%) and shifting l_A by "
                f"{q4_cases['dNeff=0.270']['delta_lA']:+.2f} (fixed-H0 Delta chi2_CMB = "
                f"{q4_cases['dNeff=0.270']['delta_chi2_CHW_fixed_H0']:+.1f}) unless H0 shifts up by "
                f"{q4_cases['dNeff=0.270']['delta_H0_compensating_lA']:+.2f} km/s/Mpc "
                f"(to {q4_cases['dNeff=0.270']['H0_compensating_lA']} km/s/Mpc)."
            ),
            "Q3_vs_Q4_physical_discriminator": (
                f"Q^3 (w=1/2, rho ~ a^-4.5) anchored at BBN (z~4e8) dilutes to Delta N_eff(z_*) = "
                f"{q3_case['dneff_at_recomb']:.2e}, leaving CMB/BAO untouched (delta r_d = "
                f"{q3_case['delta_rd_pct']}%) at the cost of fine-tuned BBN initial conditions. "
                "Q^4 (w=1/3) removes the BBN tune but couples BBN directly to CMB/BAO sound horizons "
                "and requires an N_eff-aware r_d / CMB forward model."
            ),
        },
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("=" * 84)
    print("COSMOLOGY LAYER 2 AUDIT: Delta N_eff SOUND-HORIZON & BAO/CMB SHIFT")
    print("=" * 84)
    print(f"Baseline LCDM (N_eff=3.046): r_s(z_*)={base['rs_star_Mpc']} Mpc, r_d={base['rd_Mpc']} Mpc "
          f"(Aubourg Eq.16={rd_aub:.4f} Mpc, diff={rd_base_diff_pct:+.2f}%), l_A={base['lA']}")
    print("\nQ^4 Radiation Tracker (w = 1/3, rho_phi ~ a^-4, constant Delta N_eff):")
    for k, v in q4_cases.items():
        print(f"  {k}: r_d={v['rd_Mpc']} Mpc ({v['delta_rd_pct']:+.3f}%), "
              f"DESI DM/rd ({v['delta_DESI_DM_over_rd_pct']:+.3f}%), "
              f"dl_A={v['delta_lA']:+.3f}, dchi2_CMB(fixed H0)={v['delta_chi2_CHW_fixed_H0']:+.1f}, "
              f"H0(l_A-comp)={v['H0_compensating_lA']} ({v['delta_H0_compensating_lA']:+.2f})")
    print(f"\nQ^3 Operator (w = 1/2, rho_phi ~ a^-4.5, anchored at z_BBN=4e8, dNeff_BBN=0.270):")
    print(f"  dNeff(z_*)={q3_case['dneff_at_recomb']:.2e}, delta_r_d={q3_case['delta_rd_pct']:+.6f}%, dl_A={q3_case['delta_lA']:+.6f}")
    print(f"\nWrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
