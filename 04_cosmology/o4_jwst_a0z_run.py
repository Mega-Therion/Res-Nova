#!/usr/bin/env python3
"""
O4 JWST/NIRSpec high-z a0(z) test — PRE-REGISTERED FROZEN PROTOCOL RUN.

Protocol: 04_cosmology/PREREG_O4_JWST_A0Z_2026-11-26.md (registered 2026-11-26).
Extends O4 beyond RC100 (04_cosmology/PREREG_O4_HIGHZ_A0Z.md) onto purely JWST/NIRSpec
resolved galaxy kinematics across z = 0.575 -- 5.689 (7x span in E(z)):

  Bin 1: MSA-3D (Pastras+2026, arXiv:2606.27853; Cycle 1 JWST/NIRSpec + NIRCam)
         - Primary bounded-M_bar subset: N = 20 (15 Golden + 5 Good), z = 0.575 -- 1.567
         - Full N = 30 f_DM(R_e) & lower-bound M_bar sensitivity checks
  Bin 2: ALPINE-CRISTAL-JWST (Lee+2026, arXiv:2611.07064; JWST/NIRSpec-IFU + ALMA [C II])
         - Primary: all 5 W15-confirmed rotating disks, z = 4.4403 -- 5.6886
         - Direct halo-free baryons: M_bar = M_* + M_gas([C II])
  Aux  : de Graaff+2024 (arXiv:2308.09742; 6 JADES G395H galaxies, z = 5.504 -- 7.432)
         - [O] Reference only (no measured cold-gas mass; excluded from primary chi2)

Frozen hypotheses (zero free per-run parameter tuning of a0(0) or xi):
  H_const   : a0(z) = 1.116e-10 m/s^2 (SPARC T3 baseline)
  H_horizon : a0(z) = xi * c * H(z), xi = 0.170 (Planck 2018 H0=67.36, Om=0.3153)

Usage:
  python3 04_cosmology/o4_jwst_a0z_run.py --self-test
  python3 04_cosmology/o4_jwst_a0z_run.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "02_galaxy_dynamics"))
import highz_a0_method as M  # noqa: E402

# ------------------------------------------------------------------ Frozen Constants
A0_CONST = 1.116e-10         # SPARC T3 baseline [m/s^2]
A0_CONST_T1 = 1.1607e-10     # SPARC T1 all-175 sensitivity [m/s^2]
XI = 0.170                   # A0_MEASUREMENT.json fixed horizon factor
C_LIGHT = 2.99792458e8
MPC = 3.0856775814913673e22
KPC = 3.0856775814913673e19
GM_SUN = 1.32712440018e20

# Cosmologies
H0_PLANCK, OM_PLANCK, OL_PLANCK = 67.36, 0.3153, 0.6847
H0_LIT, OM_LIT, OL_LIT = 70.00, 0.3000, 0.7000

H0_SI = H0_PLANCK * 1e3 / MPC
A0_H0 = XI * C_LIGHT * H0_SI  # 1.1128e-10 m/s^2

LN10 = math.log(10.0)
B1 = M.sersic_b(1.0)
R_FACTOR = 2.2 / B1          # R_2.2 / R_e = 2.2 / 1.678347 = 1.310813


# ------------------------------------------------------------------ Cosmology Helpers
def E_z(z: float, om: float = OM_PLANCK, ol: float = OL_PLANCK) -> float:
    return math.sqrt(om * (1.0 + z) ** 3 + ol)


def angular_diameter_dist_mpc(z: float, h0: float, om: float, ol: float) -> float:
    val, _ = integrate.quad(
        lambda zp: 1.0 / math.sqrt(om * (1.0 + zp) ** 3 + ol),
        0.0,
        float(z),
        epsabs=1e-10,
        epsrel=1e-10,
    )
    dc_mpc = (C_LIGHT / 1e3 / h0) * val
    return dc_mpc / (1.0 + z)


def f_DA_planck_over_lit(z: float) -> float:
    """Ratio D_A(Planck18) / D_A(70, 0.3, 0.7)."""
    return (
        angular_diameter_dist_mpc(z, H0_PLANCK, OM_PLANCK, OL_PLANCK)
        / angular_diameter_dist_mpc(z, H0_LIT, OM_LIT, OL_LIT)
    )


# ------------------------------------------------------------------ Provenance-Verified Tables
# 1. MSA-3D (arXiv:2606.27853 v14)
# Fields per row:
# id, tier, z, Re_disk_kpc, logMstar, SFR,
# sig0, sig0_p, sig0_m, vrot22, vrot22_p, vrot22_m,
# fdm, fdm_p, fdm_m, bt, bt_limit_dir (None/"<" /">"),
# logMbar (None if upper limit), logMbar_upper,
# mbar_stat_p, mbar_stat_m, mbar_sys_p, mbar_sys_m, flag_outlier
MSA3D_ROWS = [
    # Golden sample (N = 24; 15 bounded + 9 upper limits)
    ("2111",  "Golden", 0.575, 3.97,  9.97,  1.6, 53.2, 3.3, 12.3, 154.0, 12.0, 11.0, 0.71, 0.08, 0.13, 0.26, None,  10.05, None,  0.10, 0.11, 0.16, 0.09, False),
    ("2145",  "Golden", 1.173, 3.16,  9.19,  1.4, 43.3, 2.0,  7.9,  76.0, 12.0,  8.0, 0.47, 0.27, 0.18, 0.02, "<",    9.82, None,  0.10, 0.11, 0.13, 0.22, False),
    ("2465",  "Golden", 1.245, 3.31,  9.30,  1.6, 43.4, 3.5,  7.5, 133.0,  7.0,  8.0, 0.76, 0.17, 0.25, 0.02, None,   9.82, None,  0.33, 0.34, 0.22, 0.21, False),
    ("2824",  "Golden", 0.980, 2.47,  9.49,  0.7, 42.5, 4.2, 10.1, 173.0, 17.0, 17.0, 0.92, 0.03, 0.06, 0.21, None,   None,  9.43, 0.00, 0.00, 0.00, 0.00, False),
    ("3399",  "Golden", 1.337, 2.65,  9.81,  3.5, 54.0, 1.9,  5.4, 108.0, 11.0, 10.0, 0.76, 0.05, 0.08, 0.32, None,   None,  9.61, 0.00, 0.00, 0.00, 0.00, False),
    ("4391",  "Golden", 1.079, 1.43,  9.48,  2.7, 49.5, 5.2,  7.7, 136.0, 69.0, 34.0, 0.50, 0.46, 0.21, 0.05, "<",    9.84, None,  0.29, 0.32, 0.20, 0.39, False),
    ("6199",  "Golden", 1.592, 5.86, 10.00, 17.8, 45.2, 1.6,  5.3,  93.0, 20.0, 25.0, 0.66, 0.09, 0.09, 0.18, None,   None,  9.99, 0.00, 0.00, 0.00, 0.00, True),
    ("6430",  "Golden", 1.172, 4.38,  9.79,  8.9, 58.4, 2.3,  6.3, 133.0, 24.0, 24.0, 0.83, 0.17, 0.40, 0.04, None,   9.82, None,  0.54, 0.15, 0.27, 0.51, True),
    ("7314",  "Golden", 1.283, 1.60,  9.55,  4.8, 61.0, 2.7,  4.9, 101.0, 16.0, 17.0, 0.62, 0.38, 0.33, 0.09, "<",    9.66, None,  0.32, 0.40, 0.12, 0.31, False),
    ("7561",  "Golden", 1.029, 2.84,  9.21,  3.0, 48.0, 3.7,  6.9,  86.0, 12.0, 19.0, 0.13, 0.87, 0.13, 0.07, None,  10.14, None,  0.09, 0.29, 0.06, 0.39, False),
    ("8365",  "Golden", 1.685, 2.09,  9.56,  3.4, 35.3, 2.4,  6.6, 132.0, 10.0, 10.0, 0.79, 0.06, 0.07, 0.02, None,   None,  9.53, 0.00, 0.00, 0.00, 0.00, False),
    ("8576",  "Golden", 1.567, 2.38,  9.60,  3.3, 46.5, 3.0,  5.3, 179.0, 38.0, 27.0, 0.87, 0.06, 0.08, 0.02, None,   9.60, None,  0.25, 0.21, 0.12, 0.13, False),
    ("8942",  "Golden", 1.176, 1.70,  9.86, 16.2, 53.1, 5.6,  6.2, 153.0, 26.0,  6.0, 0.69, 0.08, 0.06, 0.02, None,   None,  9.78, 0.00, 0.00, 0.00, 0.00, False),
    ("9424",  "Golden", 0.976, 3.86,  9.76,  5.4, 43.1, 2.8,  9.8, 127.0, 12.0, 11.0, 0.71, 0.09, 0.20, 0.23, ">",    9.84, None,  0.03, 0.02, 0.32, 0.14, True),
    ("9636",  "Golden", 0.737, 3.28,  9.35,  1.7, 33.5, 3.6, 20.3, 106.0,  7.0,  6.0, 0.75, 0.13, 0.15, 0.02, None,   9.60, None,  0.19, 0.20, 0.14, 0.20, False),
    ("9812",  "Golden", 0.738, 4.51,  9.97,  3.6, 42.4, 2.8, 13.4, 189.0, 34.0, 23.0, 0.44, 0.28, 0.25, 0.02, None,  10.59, None,  0.14, 0.21, 0.18, 0.17, False),
    ("9960",  "Golden", 1.514, 2.69, 11.06,  6.0, 42.9, 3.6,  6.4, 300.0,  9.0,  9.0, 0.33, 0.19, 0.16, 0.30, "<",   10.83, None,  0.08, 0.09, 0.13, 0.15, False),
    ("10910", "Golden", 0.742, 4.98,  9.57,  1.5, 36.0, 3.3, 17.4, 150.0, 13.0, 11.0, 0.87, 0.10, 0.15, 0.02, None,   9.79, None,  0.37, 0.35, 0.21, 0.22, False),
    ("11225", "Golden", 1.052, 3.39,  9.67, 12.6, 62.9, 1.8,  5.9, 102.0, 49.0,  6.0, 0.79, 0.09, 0.15, 0.02, None,   None,  9.80, 0.00, 0.00, 0.00, 0.00, False),
    ("11843", "Golden", 1.465, 3.17, 10.74, 19.0, 53.7, 7.1,  6.5, 273.0, 15.0, 17.0, 0.69, 0.07, 0.14, 0.02, None,   None, 10.52, 0.00, 0.00, 0.00, 0.00, False),
    ("12015", "Golden", 1.235, 2.39, 10.08, 11.2, 57.7, 2.2,  5.7, 167.0, 18.0, 16.0, 0.75, 0.10, 0.14, 0.02, None,   None,  9.89, 0.00, 0.00, 0.00, 0.00, False),
    ("12239", "Golden", 0.894, 2.10,  9.49,  1.5, 56.1, 3.4,  8.2, 129.0, 18.0, 16.0, 0.85, 0.09, 0.13, 0.02, None,   9.43, None,  0.29, 0.25, 0.12, 0.19, False),
    ("18586", "Golden", 0.756, 1.49,  9.01,  3.3, 42.8, 3.3, 13.1,  74.0, 12.0,  9.0, 0.67, 0.19, 0.23, 0.02, None,   9.26, None,  0.23, 0.24, 0.19, 0.25, False),
    ("29470", "Golden", 1.042, 3.02,  9.71,  2.1, 39.8, 2.2, 10.1, 128.0, 15.0, 12.0, 0.83, 0.05, 0.05, 0.11, "<",    None,  9.53, 0.00, 0.00, 0.00, 0.00, False),
    # Good sample (N = 6; 5 bounded + 1 upper limit)
    ("8512",  "Good",   1.104, 5.45, 10.32,  3.2, 42.8, 2.0,  8.6, 177.0, 163.0, 106.0, 0.71, 0.29, 0.33, 0.22, None, 10.27, None, 0.37, 0.35, 0.12, 0.29, False),
    ("9337",  "Good",   1.172, 5.56,  9.27,  3.9, 36.5, 2.4,  8.9,  57.0,  27.0,  48.0, 0.69, 0.19, 0.23, 0.11, "<",  None,  9.59, 0.00, 0.00, 0.00, 0.00, False),
    ("10107", "Good",   1.010, 3.24, 10.01,  3.6, 60.0, 2.5,  6.5, 112.0,  51.0,  22.0, 0.35, 0.42, 0.35, 0.10, None, 10.28, None, 0.32, 0.30, 0.51, 0.33, False),
    ("13182", "Good",   1.540, 4.17, 10.25, 15.8, 64.6, 2.7,  6.6, 179.0, 206.0, 128.0, 0.60, 0.40, 0.60, 0.21, None, 10.39, None, 0.47, 0.42, 0.15, 0.41, False),
    ("13416", "Good",   1.540, 2.30, 10.76, 20.0, 39.7, 4.2,  8.1, 169.0,  15.0,  13.0, 0.03, 0.09, 0.03, 0.60, None, 10.48, None, 0.04, 0.04, 0.13, 0.19, False),
    ("18188", "Good",   0.822, 6.24,  9.56,  0.8, 43.9, 2.6, 11.4, 108.0,  29.0,  15.0, 0.69, 0.31, 0.25, 0.07, "<",  10.07, None, 0.30, 0.30, 0.03, 0.40, False),
]

# 2. ALPINE-CRISTAL-JWST (arXiv:2611.07064, Tables 1 & 2)
# Fields: id, z, Re_arcsec, Re_kpc, logMstar, e_logMstar, logMgas, e_logMgas,
# Vc_nonparam, e_Vc_nonparam, Vc_dysmal, e_Vc_dysmal, borderline_flag
ALPINE_CRISTAL_ROWS = [
    ("DC-494763", 5.2337, 0.19, 1.17,  9.51, 0.36, 10.17, 0.31, 153.0,  29.0, 186.0, 20.0, False),
    ("DC-519281", 5.5759, 0.16, 0.95,  9.84, 0.39, 10.21, 0.32, 282.0,  77.0, 315.0, 55.0, False),
    ("DC-536534", 5.6886, 0.21, 1.23, 10.40, 0.29, 10.39, 0.32, 254.0,  78.0, 219.0, 32.0, False),
    ("DC-630594", 4.4403, 0.22, 1.46,  9.68, 0.32, 10.27, 0.31, 179.0,  56.0, 195.0, 27.0, False),
    ("DC-742174", 5.6360, 0.40, 2.36,  9.51, 0.40,  9.64, 0.32, 197.0, 105.0, 197.0, 31.0, True),
]

# 3. Auxiliary de Graaff+2024 (arXiv:2308.09742, Tables 2-4) — [O] order-of-magnitude check only
# Fields: id, z, Re_arcsec, logMdyn, e_logMdyn, logMstar, e_logMstar, sfr, v_re, e_v_re, sig0
DEGRAAFF_ROWS = [
    ("JADES-NS-00016745", 5.56616, 0.320, 10.23, 0.080, 8.80, 0.040, 12.60, 105.0, 13.0, 55.0),
    ("JADES-NS-00019606", 5.88979, 0.117,  9.17, 0.060, 7.54, 0.040,  1.46,   5.0,  4.0, 39.1),
    ("JADES-NS-00022251", 5.79912, 0.122,  9.23, 0.030, 8.21, 0.050,  6.20,  23.0,  4.0, 39.0),
    ("JADES-NS-00047100", 7.43173, 0.130,  9.85, 0.070, 8.53, 0.110,  5.10,  91.0, 18.5, 71.0),
    ("JADES-NS-10016374", 5.50411, 0.084,  9.45, 0.070, 7.86, 0.070,  2.19,  16.0,  9.5, 62.0),
    ("JADES-NS-20086025", 7.26270, 0.360, 10.31, 0.195, 8.85, 0.180, 24.00, 155.0, 18.0, 25.0),
]


# ------------------------------------------------------------------ Builders
def _sym_err(p: float, m: float, mode: str = "mid") -> float:
    if mode == "mid":
        return 0.5 * (p + m)
    if mode == "max":
        return max(p, m)
    if mode == "lo":
        return m
    if mode == "hi":
        return p
    raise ValueError(mode)


def build_msa3d_mbar(
    subset: str = "bounded",
    golden_only: bool = False,
    drop_flagged: bool = False,
    err_mode: str = "mid",
    bt_limit_mode: str = "half",
    adc_coef: float = 1.2 * 2.2,  # 2.64 from finite-thickness q=0.25 paper eq. (6)
    re_frac_err: float = 0.10,
    planck_conv: bool = True,
):
    rows = []
    for r in MSA3D_ROWS:
        (gid, tier, z, re_kpc, logMs, sfr, s0, s0p, s0m, vr, vrp, vrm,
         fdm, fdmp, fdmm, bt, bt_lim, lMb, lMb_up, stp, stm, syp, sym, flagged) = r
        if golden_only and tier != "Golden":
            continue
        if drop_flagged and flagged:
            continue
        if subset == "bounded" and lMb is None:
            continue

        if lMb is not None:
            logMbar = lMb
            ep = math.hypot(stp, syp)
            em = math.hypot(stm, sym)
            e_logMbar = _sym_err(ep, em, err_mode)
        else:
            # Halo-free lower/median prior sensitivity for censored rows only
            # (using paper-stated median M_mol/M_*=0.9 + 0.08 dex HI = 10^0.359 * M_*, with 0.30 dex scatter)
            if subset == "all_paper_gas":
                logMbar = logMs + math.log10(1.9) + 0.08
                e_logMbar = 0.30
            elif subset == "all_mstar_floor":
                logMbar = logMs
                e_logMbar = 0.30
            else:
                raise ValueError(subset)

        e_vr = _sym_err(vrp, vrm, err_mode)
        e_s0 = _sym_err(s0p, s0m, err_mode)
        vc2 = vr * vr + adc_coef * s0 * s0
        vc = math.sqrt(vc2)
        e_vc2 = math.hypot(2.0 * vr * e_vr, 2.0 * adc_coef * s0 * e_s0)
        e_vc = e_vc2 / (2.0 * vc)

        f_d = f_DA_planck_over_lit(z) if planck_conv else 1.0
        re_use = re_kpc * f_d
        mbar_msun = (10.0 ** logMbar) * (f_d ** 2)
        r22_kpc = R_FACTOR * re_use

        if bt_lim == ">":
            if bt_limit_mode == "half":
                bt_eff = 0.5 * (bt + 1.0)
            elif bt_limit_mode == "zero":
                bt_eff = bt
            elif bt_limit_mode == "upper":
                bt_eff = 1.0
            else:
                raise ValueError(bt_limit_mode)
        elif bt_lim:
            if bt_limit_mode == "half":
                bt_eff = 0.5 * bt
            elif bt_limit_mode == "zero":
                bt_eff = 0.0
            elif bt_limit_mode == "upper":
                bt_eff = bt
            else:
                raise ValueError(bt_limit_mode)
        else:
            bt_eff = bt

        k_disk = M.k_spheroid(R_FACTOR, 1.0, 0.25)
        k_bulge = M.k_spheroid(R_FACTOR * re_use / 1.0, 4.0, 1.0)
        k_eff = (1.0 - bt_eff) * k_disk + bt_eff * k_bulge

        g_obs = (vc * 1e3) ** 2 / (r22_kpc * KPC)
        g_bar = k_eff * GM_SUN * mbar_msun / (r22_kpc * KPC) ** 2
        s_V = e_vc / vc
        s_R = re_frac_err
        s_M = LN10 * e_logMbar

        rows.append({
            "id": gid,
            "z": z,
            "lng": math.log(g_obs),
            "s_lng": math.hypot(2.0 * s_V, s_R),
            "lngb": math.log(g_bar),
            "s_lngb": math.hypot(s_M, 2.0 * s_R),
            "c": 2.0 * (s_R ** 2),
            "g_obs": g_obs,
            "g_bar": g_bar,
            "Vc": vc,
            "logMbar": math.log10(mbar_msun),
            "Re_kpc": re_use,
        })
    return _pack_view(rows, "mbar")


def build_msa3d_fdm(
    golden_only: bool = False,
    drop_flagged: bool = False,
    err_mode: str = "mid",
    adc_coef: float = 1.2 * 2.2,
    re_frac_err: float = 0.10,
    planck_conv: bool = True,
):
    rows = []
    for r in MSA3D_ROWS:
        (gid, tier, z, re_kpc, logMs, sfr, s0, s0p, s0m, vr, vrp, vrm,
         fdm, fdmp, fdmm, bt, bt_lim, lMb, lMb_up, stp, stm, syp, sym, flagged) = r
        if golden_only and tier != "Golden":
            continue
        if drop_flagged and flagged:
            continue
        e_vr = _sym_err(vrp, vrm, err_mode)
        e_s0 = _sym_err(s0p, s0m, err_mode)
        vc2 = vr * vr + adc_coef * s0 * s0
        vc = math.sqrt(vc2)
        e_vc = math.hypot(2.0 * vr * e_vr, 2.0 * adc_coef * s0 * e_s0) / (2.0 * vc)
        f_d = f_DA_planck_over_lit(z) if planck_conv else 1.0
        re_use = re_kpc * f_d
        # Evaluate f_DM at R_e paired with circular velocity measured on plateau at 2.2 R_s
        g_obs = (vc * 1e3) ** 2 / (re_use * KPC)
        s_V = e_vc / vc
        s_R = re_frac_err
        rows.append({
            "id": gid,
            "z": z,
            "lng": math.log(g_obs),
            "s_lng": math.hypot(2.0 * s_V, s_R),
            "f": fdm,
            "s_f": _sym_err(fdmp, fdmm, err_mode),
            "g_obs": g_obs,
        })
    return _pack_view(rows, "fdm")


def build_alpine_cristal_mbar(
    kinematics: str = "dysmal",
    drop_borderline: bool = False,
    gas_shift_dex: float = 0.0,
    re_frac_floor: float = 0.05,  # 0.01 arcsec / ~0.2 arcsec
    planck_conv: bool = True,
):
    rows = []
    for r in ALPINE_CRISTAL_ROWS:
        (gid, z, re_as, re_kpc, lMs, e_lMs, lMg, e_lMg, v_np, ev_np, v_dy, ev_dy, borderline) = r
        if drop_borderline and borderline:
            continue
        if kinematics == "dysmal":
            vc, e_vc = v_dy, ev_dy
        elif kinematics == "nonparam":
            vc, e_vc = v_np, ev_np
        else:
            raise ValueError(kinematics)

        f_d = f_DA_planck_over_lit(z) if planck_conv else 1.0
        re_use = re_kpc * f_d
        r22_kpc = R_FACTOR * re_use

        ms = (10.0 ** lMs) * (f_d ** 2)
        mg = (10.0 ** (lMg + gas_shift_dex)) * (f_d ** 2)
        mbar = ms + mg
        sig_ms = ms * LN10 * e_lMs
        sig_mg = mg * LN10 * e_lMg
        sig_mbar = math.hypot(sig_ms, sig_mg)
        s_M = sig_mbar / mbar  # fractional = sigma_ln(M_bar)

        k_eff = M.k_spheroid(R_FACTOR, 1.0, 0.20)  # q=0.20, B/T=0 per paper §3.4
        g_obs = (vc * 1e3) ** 2 / (r22_kpc * KPC)
        g_bar = k_eff * GM_SUN * mbar / (r22_kpc * KPC) ** 2
        s_V = e_vc / vc
        s_R = max(0.01 / re_as, re_frac_floor)

        rows.append({
            "id": gid,
            "z": z,
            "lng": math.log(g_obs),
            "s_lng": math.hypot(2.0 * s_V, s_R),
            "lngb": math.log(g_bar),
            "s_lngb": math.hypot(s_M, 2.0 * s_R),
            "c": 2.0 * (s_R ** 2),
            "g_obs": g_obs,
            "g_bar": g_bar,
            "Vc": vc,
            "logMbar": math.log10(mbar),
            "Re_kpc": re_use,
        })
    return _pack_view(rows, "mbar")


def _pack_view(rows, route):
    out = {"id": [r["id"] for r in rows]}
    keys = ["z", "lng", "s_lng", "g_obs"]
    if route == "mbar":
        keys += ["lngb", "s_lngb", "c", "g_bar"]
    else:
        keys += ["f", "s_f"]
    for k in keys:
        out[k] = np.array([r[k] for r in rows], float)
    return out


# ------------------------------------------------------------------ Inference Helpers
def fit_bin_profile(data, route, grid):
    sub = {"lng": data["lng"], "s_lng": data["s_lng"]}
    if route == "mbar":
        sub.update({"lngb": data["lngb"], "s_lngb": data["s_lngb"], "c": data["c"]})
    else:
        sub.update({"f": data["f"], "s_f": data["s_f"]})
    lik = M.JointA0Likelihood(sub, route=route)
    s = lik.fit(grid)
    # Fisher weight per galaxy around A0_CONST for bin-effective E(z)
    x = data["g_obs"] / A0_CONST
    J = x / (1.0 + x * x) ** 1.5
    if route == "fdm":
        w = (J ** 2) / (data["s_f"] ** 2 + (J ** 2) * (data["s_lng"] ** 2))
    else:
        w = 1.0 / (data["s_lng"] ** 2 + data["s_lngb"] ** 2)
    ez = np.array([E_z(zz) for zz in data["z"]], float)
    lnR = float(np.sum(w * np.log(ez)) / np.sum(w))
    g, dchi = s["dchi2_fn"]
    return {
        "n": int(len(data["z"])),
        "z_range": [float(data["z"].min()), float(data["z"].max())],
        "z_eff": float(np.sum(w * data["z"]) / np.sum(w)),
        "E_eff": float(math.exp(lnR)),
        "lnR": lnR,
        "a0_hat": float(math.exp(s["lna0_hat"])),
        "a0_68": [None if x is None else float(math.exp(x)) for x in s["ci68"]],
        "a0_95": [None if x is None else float(math.exp(x)) for x in s["ci95"]],
        "sig_best": float(s["sig_best"]),
        "at_edge": bool(s["at_edge"]),
        "chi2_const": float(np.interp(math.log(A0_CONST), g, dchi)),
        "chi2_horizon": float(np.interp(math.log(A0_H0) + lnR, g, dchi)),
        "g": g,
        "dchi": dchi,
    }


def evaluate_2bin(b1_info, b2_info, a0_const=A0_CONST, a0_h0=A0_H0):
    chi2_const = (
        float(np.interp(math.log(a0_const), b1_info["g"], b1_info["dchi"]))
        + float(np.interp(math.log(a0_const), b2_info["g"], b2_info["dchi"]))
    )
    chi2_horizon = (
        float(np.interp(math.log(a0_h0) + b1_info["lnR"], b1_info["g"], b1_info["dchi"]))
        + float(np.interp(math.log(a0_h0) + b2_info["lnR"], b2_info["g"], b2_info["dchi"]))
    )
    dchi2 = chi2_const - chi2_horizon
    sigma = math.sqrt(abs(dchi2)) * (1.0 if dchi2 >= 0 else -1.0)

    # Normalization-free shape test & continuous exponent fit a0(z) = A_piv * (E(z)/E1)^n
    bins = [b1_info, b2_info]
    lnAs = math.log(A0_CONST) + np.arange(-3.0, 3.5 + 1e-9, 0.005)

    def shape_min(lnRs):
        tot = np.zeros_like(lnAs)
        for b, lr in zip(bins, lnRs):
            tot += np.interp(lnAs + lr, b["g"], b["dchi"], left=1e6, right=1e6)
        return float(np.min(tot)), float(math.exp(lnAs[int(np.argmin(tot))]))

    sh_const, sh_const_a = shape_min([0.0, 0.0])
    sh_horiz, sh_horiz_a = shape_min([b["lnR"] for b in bins])
    sh_dchi2 = sh_const - sh_horiz
    sh_sigma = math.sqrt(abs(sh_dchi2)) * (1.0 if sh_dchi2 >= 0 else -1.0)

    # Profile exponent n across bins using exact bin dchi curves
    # Fix log-offset from b1, shift b2 by n * (lnR2 - lnR1)
    dlr = b2_info["lnR"] - b1_info["lnR"]
    n_grid = np.linspace(-4.0, 3.5, 751)
    dchi_n = []
    for n in n_grid:
        cmin, _ = shape_min([0.0, n * dlr])
        dchi_n.append(cmin)
    dchi_n = np.array(dchi_n)
    c_min = float(dchi_n.min())
    dchi_n -= c_min
    i0 = int(np.argmin(dchi_n))
    n_hat = round(float(n_grid[i0]), 4)
    n_lo = next((round(float(n_grid[j]), 4) for j in range(i0, 0, -1) if dchi_n[j - 1] > 1.0), None)
    n_hi = next((round(float(n_grid[j]), 4) for j in range(i0, len(n_grid) - 1) if dchi_n[j + 1] > 1.0), None)

    if dchi2 <= -9.0:
        verdict = "H_CONST_FAVORED"
    elif dchi2 >= 9.0 and sh_dchi2 >= 9.0:
        verdict = "H_HORIZON_FAVORED"
    elif dchi2 >= 9.0:
        verdict = "CONFOUNDED"
    else:
        verdict = "INCONCLUSIVE"

    return {
        "chi2_const": chi2_const,
        "chi2_horizon": chi2_horizon,
        "delta_chi2": dchi2,
        "sigma": sigma,
        "shape_chi2_const": sh_const,
        "shape_chi2_horizon": sh_horiz,
        "shape_delta_chi2": sh_dchi2,
        "shape_sigma": sh_sigma,
        "shape_a0_const_fit": sh_const_a,
        "shape_a0_horiz_fit": sh_horiz_a,
        "n_exponent_fit": {"n_hat": n_hat, "ci68": [n_lo, n_hi], "dlr_bins": dlr},
        "verdict": verdict,
    }


def evaluate_multibin(bin_infos, a0_const=A0_CONST, a0_h0=A0_H0):
    chi2_const = sum(float(np.interp(math.log(a0_const), b["g"], b["dchi"])) for b in bin_infos)
    chi2_horizon = sum(float(np.interp(math.log(a0_h0) + b["lnR"], b["g"], b["dchi"])) for b in bin_infos)
    dchi2 = chi2_const - chi2_horizon
    lnAs = math.log(A0_CONST) + np.arange(-3.0, 3.5 + 1e-9, 0.005)
    tot_c = np.zeros_like(lnAs)
    tot_h = np.zeros_like(lnAs)
    for b in bin_infos:
        tot_c += np.interp(lnAs, b["g"], b["dchi"], left=1e6, right=1e6)
        tot_h += np.interp(lnAs + b["lnR"], b["g"], b["dchi"], left=1e6, right=1e6)
    sh_c = float(np.min(tot_c))
    sh_h = float(np.min(tot_h))
    sh_d = sh_c - sh_h
    n_grid = np.linspace(-4.0, 3.5, 751)
    lr0 = bin_infos[0]["lnR"]
    vals = []
    for n in n_grid:
        tot = np.zeros_like(lnAs)
        for b in bin_infos:
            tot += np.interp(lnAs + n * (b["lnR"] - lr0), b["g"], b["dchi"], left=1e6, right=1e6)
        vals.append(float(np.min(tot)))
    vals = np.array(vals) - min(vals)
    i0 = int(np.argmin(vals))
    n_hat = round(float(n_grid[i0]), 4)
    n_lo = next((round(float(n_grid[j]), 4) for j in range(i0, 0, -1) if vals[j - 1] > 1.0), None)
    n_hi = next((round(float(n_grid[j]), 4) for j in range(i0, len(n_grid) - 1) if vals[j + 1] > 1.0), None)
    return {
        "chi2_const": chi2_const,
        "chi2_horizon": chi2_horizon,
        "delta_chi2": dchi2,
        "shape_chi2_const": sh_c,
        "shape_chi2_horizon": sh_h,
        "shape_delta_chi2": sh_d,
        "n_exponent_fit": {"n_hat": n_hat, "ci68": [n_lo, n_hi]},
    }


def evaluate_degraaff_aux():
    """Exploratory [O] comparison on JADES G395H galaxies (no measured cold gas)."""
    out = []
    for gid, z, re_as, lMdyn, e_lMdyn, lMst, e_lMst, sfr, v_re, e_v_re, sig0 in DEGRAAFF_ROWS:
        f_d = f_DA_planck_over_lit(z)
        re_kpc = re_as * angular_diameter_dist_mpc(z, H0_PLANCK, OM_PLANCK, OL_PLANCK) * 1e3 / 206264.806247
        mdyn = (10.0 ** lMdyn) * (f_d ** 2)
        mstar = (10.0 ** lMst) * (f_d ** 2)
        # Spherical dynamical acceleration at Re: g_dyn ~ G M_dyn(<Re) / Re^2 with M_dyn(<Re) = 0.5 M_dyn
        g_dyn = 0.5 * GM_SUN * mdyn / (re_kpc * KPC) ** 2
        g_star = 0.5 * GM_SUN * mstar / (re_kpc * KPC) ** 2
        # Paper notes M_gas ~ 10 * M_* implied by Kennicutt-Schmidt SFR (approx M_bar ~ 11 M_*)
        g_bar_11 = 11.0 * g_star
        g_const_11 = float(M.g_pred(g_bar_11, A0_CONST))
        g_horiz_11 = float(M.g_pred(g_bar_11, A0_H0 * E_z(z)))
        out.append({
            "id": gid,
            "z": z,
            "E_z": E_z(z),
            "g_dyn": g_dyn,
            "g_star_only": g_star,
            "g_bar_assumed_11x_mstar": g_bar_11,
            "g_pred_const_11x": g_const_11,
            "g_pred_horizon_11x": g_horiz_11,
            "ratio_dyn_over_const": g_dyn / g_const_11,
            "ratio_dyn_over_horizon": g_dyn / g_horiz_11,
        })
    return out


# ------------------------------------------------------------------ Self-Test
def run_self_test():
    # 1. Exact data integrity counts
    assert len(MSA3D_ROWS) == 30, len(MSA3D_ROWS)
    n_golden = sum(1 for r in MSA3D_ROWS if r[1] == "Golden")
    n_bnd = sum(1 for r in MSA3D_ROWS if r[17] is not None)
    assert n_golden == 24 and n_bnd == 20
    assert len(ALPINE_CRISTAL_ROWS) == 5
    assert len(DEGRAAFF_ROWS) == 6

    # 1b. Lower-limit B/T handling check (ID 9424: B/T > 0.23 in v14 Table 3)
    row_9424 = [x for x in MSA3D_ROWS if x[0] == "9424"][0]
    assert row_9424[16] == ">", f"Expected lower-limit flag '>' for 9424, got {row_9424[16]!r}"
    gb_lo = build_msa3d_mbar("bounded", bt_limit_mode="zero")["g_bar"]
    gb_mid = build_msa3d_mbar("bounded", bt_limit_mode="half")["g_bar"]
    gb_hi = build_msa3d_mbar("bounded", bt_limit_mode="upper")["g_bar"]
    idx_9424 = build_msa3d_mbar("bounded")["id"].index("9424")
    # Bulge is denser than disk -> higher B/T increases k_eff and g_bar at 2.2 R_s
    assert gb_lo[idx_9424] < gb_mid[idx_9424] < gb_hi[idx_9424]

    # 2. Cosmology conversion exact invariance of g_bar and f_D(z) sanity
    assert abs(f_DA_planck_over_lit(1.0) - 1.02) < 0.02
    a_no = build_alpine_cristal_mbar(planck_conv=False)
    a_pl = build_alpine_cristal_mbar(planck_conv=True)
    assert np.allclose(a_no["g_bar"], a_pl["g_bar"], rtol=1e-12), "g_bar must be D_A-invariant!"
    for i, r in enumerate(ALPINE_CRISTAL_ROWS):
        fd = f_DA_planck_over_lit(r[1])
        assert abs(a_no["g_obs"][i] / a_pl["g_obs"][i] - fd) < 1e-10

    # 3. Deterministic exactness (low-noise Asimov) + noisy Monte Carlo recovery (n=0 vs n=1)
    rng = np.random.default_rng(20261126)
    grid = math.log(A0_CONST) + np.arange(math.log(0.02), math.log(50.0) + 1e-9, 0.06)
    msa_real = build_msa3d_mbar("bounded")
    alp_real = build_alpine_cristal_mbar("dysmal")
    for test_kind in ("exact_asimov", "noisy_mc"):
        for true_mode in ("const", "horizon"):
            b1_list, b2_list = [], []
            for d_base, bin_tag in ((msa_real, "b1"), (alp_real, "b2")):
                rep = 5 if (test_kind == "noisy_mc" and bin_tag == "b2") else (3 if test_kind == "noisy_mc" else 2)
                zz = np.tile(d_base["z"], rep)
                gb = np.tile(d_base["g_bar"], rep)
                a0_vec = np.array([A0_CONST if true_mode == "const" else A0_H0 * E_z(float(z)) for z in zz])
                if test_kind == "exact_asimov":
                    # Small observational errors matching noiseless data variance for exact likelihood inversion check
                    err = {"s_lnV": np.full_like(zz, 0.03), "s_lnR": np.full_like(zz, 0.02), "s_lnM": np.full_like(zz, 0.08)}
                    sim = M.asimov(gb, err, a0_vec, route="mbar")
                else:
                    err = {"s_lnV": np.tile(0.5 * d_base["s_lng"], rep), "s_lnR": np.full_like(zz, 0.05), "s_lnM": np.tile(d_base["s_lngb"], rep)}
                    sim = M.simulate(gb, err, a0_vec, 0.05, rng, route="mbar")
                sim["z"] = zz
                sim["g_obs"] = np.exp(sim["lng"])
                info = fit_bin_profile(sim, "mbar", grid)
                if bin_tag == "b1":
                    b1_list.append(info)
                else:
                    b2_list.append(info)
            res = evaluate_2bin(b1_list[0], b2_list[0])
            tol_n = 0.08 if test_kind == "exact_asimov" else 0.75
            thr = 50.0 if test_kind == "exact_asimov" else 9.0
            if true_mode == "const":
                assert res["delta_chi2"] < -thr, f"{test_kind} const failed: {res['delta_chi2']}"
                assert abs(res["n_exponent_fit"]["n_hat"] - 0.0) < tol_n, res["n_exponent_fit"]
            else:
                assert res["delta_chi2"] > thr and res["shape_delta_chi2"] > (25.0 if test_kind == "exact_asimov" else 9.0), res
                assert abs(res["n_exponent_fit"]["n_hat"] - 1.0) < tol_n, res["n_exponent_fit"]

    print("SELF-TEST PASS: O4 JWST invariants, cosmology D_A scaling, Asimov & noisy n=0 / n=1 recovery OK.")


# ------------------------------------------------------------------ Main Execution
def run_main():
    t0 = time.time()
    grid = math.log(A0_CONST) + np.arange(math.log(0.01), math.log(100.0) + 1e-9, 0.02)

    # Primary headline: MSA-3D (N=20 bounded mbar) + ALPINE-CRISTAL-JWST (N=5 DYSMALpy)
    d_msa = build_msa3d_mbar(subset="bounded")
    d_alp = build_alpine_cristal_mbar(kinematics="dysmal")
    b1 = fit_bin_profile(d_msa, "mbar", grid)
    b2 = fit_bin_profile(d_alp, "mbar", grid)
    headline = evaluate_2bin(b1, b2, A0_CONST)

    # Sensitivity & Robustness Suite (strictly enumerated in prereg)
    sens = {}

    # S1: Individual bins alone vs const & vs horizon
    sens["bin1_msa3d_bounded_N20"] = {
        "n": b1["n"], "z_range": b1["z_range"], "z_eff": b1["z_eff"], "E_eff": b1["E_eff"],
        "a0_hat": b1["a0_hat"], "a0_68": b1["a0_68"], "a0_95": b1["a0_95"],
        "chi2_const": b1["chi2_const"], "chi2_horizon": b1["chi2_horizon"],
        "delta_chi2": b1["chi2_const"] - b1["chi2_horizon"],
    }
    sens["bin2_alpine_cristal_dysmal_N5"] = {
        "n": b2["n"], "z_range": b2["z_range"], "z_eff": b2["z_eff"], "E_eff": b2["E_eff"],
        "a0_hat": b2["a0_hat"], "a0_68": b2["a0_68"], "a0_95": b2["a0_95"],
        "chi2_const": b2["chi2_const"], "chi2_horizon": b2["chi2_horizon"],
        "delta_chi2": b2["chi2_const"] - b2["chi2_horizon"],
    }

    # S2: MSA-3D all N=30 via f_DM(R_e) (no censoring)
    d_msa_fdm = build_msa3d_fdm()
    b1_fdm = fit_bin_profile(d_msa_fdm, "fdm", grid)
    sens["msa3d_fdm_all_N30"] = {
        "n": b1_fdm["n"], "z_eff": b1_fdm["z_eff"], "E_eff": b1_fdm["E_eff"],
        "a0_hat": b1_fdm["a0_hat"], "a0_68": b1_fdm["a0_68"],
        "chi2_const": b1_fdm["chi2_const"], "chi2_horizon": b1_fdm["chi2_horizon"],
        "delta_chi2": b1_fdm["chi2_const"] - b1_fdm["chi2_horizon"],
    }
    sens["joint_msa3d_fdm30_plus_alpine5"] = evaluate_2bin(b1_fdm, b2, A0_CONST)

    # S3: MSA-3D all N=30 with paper median gas on censored + pure M_* floor
    b1_pgas = fit_bin_profile(build_msa3d_mbar("all_paper_gas"), "mbar", grid)
    b1_mst = fit_bin_profile(build_msa3d_mbar("all_mstar_floor"), "mbar", grid)
    sens["joint_msa3d_N30_paper_gas_plus_alpine5"] = evaluate_2bin(b1_pgas, b2, A0_CONST)
    sens["joint_msa3d_N30_mstar_floor_plus_alpine5"] = evaluate_2bin(b1_mst, b2, A0_CONST)

    # S4: Outlier & quality pruning (Golden only, drop residual outliers 6199/6430/9424, drop DC-742174)
    b1_gold = fit_bin_profile(build_msa3d_mbar("bounded", golden_only=True, drop_flagged=True), "mbar", grid)
    b2_clean = fit_bin_profile(build_alpine_cristal_mbar("dysmal", drop_borderline=True), "mbar", grid)
    sens["joint_clean_golden13_plus_alpine4"] = evaluate_2bin(b1_gold, b2_clean, A0_CONST)

    # S5: ALPINE-CRISTAL non-parametric V_circ & -0.2 dex [CII]/dust gas systematic
    b2_np = fit_bin_profile(build_alpine_cristal_mbar("nonparam"), "mbar", grid)
    b2_g2 = fit_bin_profile(build_alpine_cristal_mbar("dysmal", gas_shift_dex=-0.2), "mbar", grid)
    sens["alpine_nonparam_N5"] = {"a0_hat": b2_np["a0_hat"], "a0_68": b2_np["a0_68"],
                                  "delta_chi2": b2_np["chi2_const"] - b2_np["chi2_horizon"]}
    sens["joint_msa20_plus_alpine_nonparam5"] = evaluate_2bin(b1, b2_np, A0_CONST)
    sens["joint_msa20_plus_alpine_gas_minus_0p2dex"] = evaluate_2bin(b1, b2_g2, A0_CONST)

    # S6: Asymmetric error sensitivity (lower vs upper vs max) & ADC thin-disk vs q=0.25 & SPARC T1 a0
    b1_lo = fit_bin_profile(build_msa3d_mbar("bounded", err_mode="lo"), "mbar", grid)
    b1_hi = fit_bin_profile(build_msa3d_mbar("bounded", err_mode="hi"), "mbar", grid)
    b1_thin = fit_bin_profile(build_msa3d_mbar("bounded", adc_coef=2.0 * 2.2), "mbar", grid)
    sens["joint_msa_err_lo"] = evaluate_2bin(b1_lo, b2, A0_CONST)
    sens["joint_msa_err_hi"] = evaluate_2bin(b1_hi, b2, A0_CONST)
    sens["joint_msa_thin_adc"] = evaluate_2bin(b1_thin, b2, A0_CONST)
    sens["joint_sparc_T1_baseline"] = evaluate_2bin(b1, b2, A0_CONST_T1, A0_CONST_T1)

    # S7: Combined RC100 (non-JWST, fdm 2-bin) + JWST (2-bin mbar) 4-bin meta-comparison
    d_rc = M.load_rc100()
    z_rc = np.asarray(d_rc["z"], float)
    rc_bins = []
    for lo, hi in ((0.6, 1.2), (1.2, 2.61)):
        sel = np.where((z_rc >= lo) & (z_rc < hi))[0]
        v_rc = M.data_view(d_rc, sel, "fdm")
        v_rc["z"] = z_rc[sel]
        v_rc["g_obs"] = d_rc["g_obs"][sel]
        v_rc["s_f"] = d_rc["e_fDM"][sel]
        v_rc["s_lng"] = d_rc["s_lng"][sel]
        rc_bins.append(fit_bin_profile(v_rc, "fdm", grid))
    sens["combined_4bin_RC100_plus_JWST"] = evaluate_multibin(rc_bins + [b1, b2], A0_CONST)

    # S8: Auxiliary de Graaff+2024 [O] check
    aux_degraaff = evaluate_degraaff_aux()

    # Clean non-JSON-serializable arrays before dumping
    def _clean_bin(bi):
        return {k: v for k, v in bi.items() if k not in ("g", "dchi", "P_raw")}

    def _strip(obj):
        if isinstance(obj, dict):
            return {k: _strip(v) for k, v in obj.items() if k not in ("g", "dchi", "P_raw")}
        if isinstance(obj, list):
            return [_strip(x) for x in obj]
        return obj

    prereg_sha = hashlib.sha256((HERE / "PREREG_O4_JWST_A0Z_2026-11-26.md").read_bytes()).hexdigest()

    result = {
        "status": "completed",
        "protocol": "04_cosmology/PREREG_O4_JWST_A0Z_2026-11-26.md",
        "protocol_sha256": prereg_sha,
        "epistemic_tag": "[D]",
        "frozen_inputs": {
            "a0_const_SI": A0_CONST,
            "a0_const_T1_SI": A0_CONST_T1,
            "xi": XI,
            "H0_planck": H0_PLANCK,
            "Omega_m_planck": OM_PLANCK,
            "H0_lit": H0_LIT,
            "Omega_m_lit": OM_LIT,
        },
        "primary_bins": {
            "bin1_msa3d_bounded_mbar": _clean_bin(b1),
            "bin2_alpine_cristal_dysmal_mbar": _clean_bin(b2),
        },
        "headline_2bin_result": headline,
        "sensitivity_suite": _strip(sens),
        "auxiliary_degraaff2024_O": aux_degraaff,
        "run_seconds": round(time.time() - t0, 2),
    }

    out_json = HERE / "O4_JWST_A0Z_RESULT.json"
    out_json.write_text(json.dumps(result, indent=2) + "\n")

    # Emit crisp summary markdown record
    rec_md = _format_record(result, d_msa, d_alp)
    out_md = HERE / "O4_JWST_A0Z_RECORD_2026-11-26.md"
    out_md.write_text(rec_md)

    print(json.dumps({
        "verdict": headline["verdict"],
        "delta_chi2": headline["delta_chi2"],
        "sigma": headline["sigma"],
        "shape_delta_chi2": headline["shape_delta_chi2"],
        "shape_sigma": headline["shape_sigma"],
        "n_exponent_fit": headline["n_exponent_fit"],
        "bin1_a0_hat": b1["a0_hat"],
        "bin2_a0_hat": b2["a0_hat"],
    }, indent=2))


def _fmt_ci(ci) -> str:
    lo = "-inf" if ci[0] is None else f"{ci[0]:+.2f}"
    hi = "+inf" if ci[1] is None else f"{ci[1]:+.2f}"
    return f"[{lo}, {hi}]"


def _format_record(res, d_msa, d_alp) -> str:
    h = res["headline_2bin_result"]
    b1 = res["primary_bins"]["bin1_msa3d_bounded_mbar"]
    b2 = res["primary_bins"]["bin2_alpine_cristal_dysmal_mbar"]
    s = res["sensitivity_suite"]
    n_fit = h["n_exponent_fit"]
    lines = [
        "# O4 JWST/NIRSpec a0(z) Execution Record (2026-11-26)",
        "",
        f"**Protocol:** `04_cosmology/PREREG_O4_JWST_A0Z_2026-11-26.md` (SHA-256: `{res['protocol_sha256']}`)",
        "**Script:** `04_cosmology/o4_jwst_a0z_run.py` -> `O4_JWST_A0Z_RESULT.json`",
        "**Epistemic Tag:** `[D]` computed test output on published JWST catalogs (auxiliary de Graaff+2024 `[O]`)",
        "",
        "## 1. Headline Primary Result (Pure JWST/NIRSpec 2-Bin `mbar`, N = 25)",
        "",
        f"- **Verdict:** **`{h['verdict']}`**",
        f"- **Mechanical $\\Delta\\chi^2 = \\chi^2_{{\\rm const}} - \\chi^2_{{\\rm horizon}}$:** `{h['delta_chi2']:+.2f}` (`{h['sigma']:+.2f}`$\\sigma$)",
        f"- **Shape-only $\\Delta\\chi^2_{{\\rm shape}}$ (free overall normalization):** `{h['shape_delta_chi2']:+.2f}` (`{h['shape_sigma']:+.2f}`$\\sigma$)",
        f"- **Fitted scaling exponent $n$ in $a_0(z) \\propto E(z)^n$:** `n = {n_fit['n_hat']:.2f}` (68% CI: `{_fmt_ci(n_fit['ci68'])}`)",
        "",
        "| Bin | Sample | N | z_eff | E(z_eff) | a0_hat (1e-10 m/s^2) | 68% CI | sigma_int | chi2_const | chi2_horizon |",
        "|---|---|---|---|---|---|---|---|---|---|",
        f"| 1 | MSA-3D bounded (`2606.27853`) | {b1['n']} | {b1['z_eff']:.3f} | {b1['E_eff']:.3f} | {b1['a0_hat']/1e-10:.3f} | {b1['a0_68'][0]/1e-10:.3f}--{b1['a0_68'][1]/1e-10:.3f} | {b1['sig_best']:.2f} | {b1['chi2_const']:.2f} | {b1['chi2_horizon']:.2f} |",
        f"| 2 | ALPINE-CRISTAL (`2611.07064`) | {b2['n']} | {b2['z_eff']:.3f} | {b2['E_eff']:.3f} | {b2['a0_hat']/1e-10:.3f} | {b2['a0_68'][0]/1e-10:.3f}--{b2['a0_68'][1]/1e-10:.3f} | {b2['sig_best']:.2f} | {b2['chi2_const']:.2f} | {b2['chi2_horizon']:.2f} |",
        "",
        "## 2. Sensitivity & Systematic Suite",
        "",
        "| Variant | Delta-chi2 | Shape Delta-chi2 | n_hat (68% CI) | Verdict / Note |",
        "|---|---|---|---|---|",
    ]
    for k in (
        "joint_msa3d_fdm30_plus_alpine5",
        "joint_msa3d_N30_paper_gas_plus_alpine5",
        "joint_msa3d_N30_mstar_floor_plus_alpine5",
        "joint_clean_golden13_plus_alpine4",
        "joint_msa20_plus_alpine_nonparam5",
        "joint_msa20_plus_alpine_gas_minus_0p2dex",
        "joint_msa_err_lo",
        "joint_msa_err_hi",
        "joint_msa_thin_adc",
        "joint_sparc_T1_baseline",
        "combined_4bin_RC100_plus_JWST",
    ):
        v = s[k]
        nf = v["n_exponent_fit"]
        lines.append(
            f"| `{k}` | `{v['delta_chi2']:+.2f}` | `{v['shape_delta_chi2']:+.2f}` | `{nf['n_hat']:.2f}` ({_fmt_ci(nf['ci68'])}) | {v.get('verdict', '4-bin meta')} |"
        )
    lines.extend([
        "",
        "## 3. Auxiliary de Graaff+2024 Check (`[O]`, Excluded from Primary)",
        "",
        "| Galaxy | z | E(z) | g_dyn / g_pred_const (11x M*) | g_dyn / g_pred_horizon (11x M*) |",
        "|---|---|---|---|---|",
    ])
    for row in res["auxiliary_degraaff2024_O"]:
        lines.append(
            f"| `{row['id']}` | {row['z']:.3f} | {row['E_z']:.2f} | {row['ratio_dyn_over_const']:.2f}x | {row['ratio_dyn_over_horizon']:.2f}x |"
        )
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        run_self_test()
    else:
        run_main()


if __name__ == "__main__":
    main()
