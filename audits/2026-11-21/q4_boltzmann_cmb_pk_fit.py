#!/usr/bin/env python3
"""Multi-species Boltzmann CMB (Planck 2018 plik_lite TTTEEE + DESI DR2 BAO) and Matter Power
Spectrum P(k) Audit for the surviving AeST Q^4 radiation tracker (Q4_PR226_running_lam_with_CDM).

Closes the remaining in-seat [O] cosmological calculation from Gate 1 (CURRENT_STATE_READ_THIS_FIRST.md
lines 16, 33, 176):
  Part A (Exact SymPy/Radau Multi-k Transfer Function Audit):
    - Integrates the exact Bianchi-verified 12-variable Conformal-Newtonian FLRW + AeST Q^4 +
      covariant running lambda_s(Q) + radiation + CDM system across 8 wavenumbers
      k in [0.005, 0.30] Mpc^-1 from deep radiation (x0 = 0.05) through a_eq, 3 a_eq (z_* ~ 1090),
      and 10 a_eq.
    - Compares Q4_PR226_running_lam_with_CDM (eps_Q = 0.039, KB = 0.008, lam0 = 11.2787,
      alpha = 1.15) against BOTH:
        (i) LCDM_base (eps_Q = 0), and
        (ii) GR_fluid_idr_matched (uncoupled w=1/3, cs^2=1/3, sigma=0 perfect-fluid dark radiation
             with identical eps_Q = 0.039, matching CLASS N_idr with idr_nature = fluid).
    - Quantifies the pure AeST vector-scalar [varphi, v_A] + running-lambda_s(Q) dynamical transfer
      ratios T_Phi_AeST_over_FluidIDR(k) and T_dm_AeST_over_FluidIDR(k).
  Part B (Full Multi-Species CLASS Boltzmann + Real Planck 2018 plik_lite_v22_TTTEEE 613x613
          Covariance + Real 13-Point DESI DR2 Gaussian BAO 13x13 Covariance + P(k, z=0)):
    - Validates PlikLite on Planck's shipped best-fit spectrum (chi2 = 548.50 / 613 = 0.895).
    - Evaluates and refits 5 models over (omega_b, omega_cdm, n_s, ln10^10 A_s, h) via parallel
      Gauss-Newton / Levenberg-Marquardt on the 626-bin (613 plik_lite + 13 DESI DR2 BAO) data vector:
        M0: LCDM_joint_fit (dNeff = 0)
        M1: AeST_Q4_unrefitted_at_LCDM_params (dNeff = 0.270, fluid + AeST T(k) dressing)
        M2: AeST_Q4_PR226_dNeff0p270_joint_fit (dNeff = 0.270 <=> eps_Q = 0.03625, fluid + AeST T(k))
        M3: AeST_Q4_Gate1_eps0p039_joint_fit (eps_Q = 0.0390 <=> dNeff = 0.2905, fluid + AeST T(k))
        M4: GR_freestream_dNeff0p270_joint_fit (dNeff = 0.270 in N_ur, free-streaming sigma != 0)
    - Computes exact P(k, z=0), sigma_8, S_8, acoustic peak positions, and Delta chi^2 breakdown.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import glob
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))

# Import Gate 1 SymPy/Radau transfer machinery
_g1_spec = importlib.util.spec_from_file_location("g1", os.path.join(HERE, "gate1_equality_cosh_vs_q4.py"))
g1 = importlib.util.module_from_spec(_g1_spec)
_g1_spec.loader.exec_module(g1)

# Import BAO/CMB exact first-principles sound-horizon & distance calculator
_d4_spec = importlib.util.spec_from_file_location(
    "d4", os.path.join(ROOT, "audits/2026-11-19/bao_cmb_dneff_forward_check.py")
)
d4 = importlib.util.module_from_spec(_d4_spec)
_d4_spec.loader.exec_module(d4)

# Import validated Planck 2018 plik_lite_v22_TTTEEE 613-bin likelihood
_pl_path = "/home/mega/Chyren/3_research/Research_and_Data/05_Scripts_and_Tools/02_cosmology_cmb_and_chi_field/cmb_aest/plik_lite.py"
_pl_spec = importlib.util.spec_from_file_location("pl", _pl_path)
pl = importlib.util.module_from_spec(_pl_spec)
_pl_spec.loader.exec_module(pl)

CLASS_BIN = os.path.expanduser("~/.chyren/cosmo/class_public/class")
TCMB_UK = 2.7255e6
ONU_M = 0.06 / 93.14
NEFF_STD = 3.046
NEU_FACTOR = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)  # 0.22710731766
# Ratio dNeff / eps_Q where eps_Q = rho_phi / rho_rad_std:
DNEFF_PER_EPSQ = (1.0 + NEU_FACTOR * NEFF_STD) / NEU_FACTOR  # 7.449203

K_GRID_MPC = [0.005, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30]


def part_a_aest_q4_vs_fluid_idr_transfer(funcs: dict) -> dict:
    """Integrate exact SymPy/Radau system across K_GRID_MPC for LCDM, GR_fluid_idr, and AeST Q^4."""
    H0_mpc = 67.4 / 299792.458
    Om_r0 = 9.0e-5
    Om_dm0 = 0.26
    a_eq = Om_r0 / Om_dm0
    eps_Q = 0.039

    specs = g1.make_specs(H0_mpc, Om_r0, Om_dm0, eps_Q, 10.0 * a_eq)
    rows = []
    max_e00_all = 0.0
    max_e0x_all = 0.0

    for k in K_GRID_MPC:
        # 1. Base LCDM (Om_r0, Om_dm0)
        r_lcdm = g1.integrate_transfer(
            funcs, specs["lcdm"], k, H0_mpc, Om_r0, Om_dm0, 0.0, 0.0, None,
            "physical_friedmann", (0.05, 4000.0), 10.0, a_eq
        )
        # 2. GR + uncoupled fluid dark radiation (w=1/3, cs^2=1/3, sigma=0) with identical eps_Q = 0.039
        # Note: in physical_friedmann mode, evaluate snapshots at the same physical scale factors a_eq_ref!
        r_fidr = g1.integrate_transfer(
            funcs, specs["lcdm"], k, H0_mpc, Om_r0 * (1.0 + eps_Q), Om_dm0, 0.0, 0.0, None,
            "physical_friedmann", (0.05, 4000.0), 10.0, a_eq
        )
        # 3. Full coupled AeST Q^4 + covariant running lambda_s(Q) + radiation + CDM
        r_q4 = g1.integrate_transfer(
            funcs, specs["q4_pr226"], k, H0_mpc, Om_r0, Om_dm0, 0.0, eps_Q, None,
            "physical_friedmann", (0.05, 4000.0), 10.0, a_eq
        )

        for r in (r_lcdm, r_fidr, r_q4):
            assert r["max_rel_E00"] < 1e-7 and r["max_rel_E0x"] < 1e-7
            max_e00_all = max(max_e00_all, r["max_rel_E00"])
            max_e0x_all = max(max_e0x_all, r["max_rel_E0x"])

        s_lc_1 = r_lcdm["snapshots"]["1p0_aeq"]
        s_lc_3 = r_lcdm["snapshots"]["3p0_aeq"]
        s_lc_10 = r_lcdm["snapshots"]["10p0_aeq"]

        s_fi_1 = r_fidr["snapshots"]["1p0_aeq"]
        s_fi_3 = r_fidr["snapshots"]["3p0_aeq"]
        s_fi_10 = r_fidr["snapshots"]["10p0_aeq"]

        s_q4_1 = r_q4["snapshots"]["1p0_aeq"]
        s_q4_3 = r_q4["snapshots"]["3p0_aeq"]
        s_q4_10 = r_q4["snapshots"]["10p0_aeq"]

        t_phi_fi_3 = s_q4_3["Phi"] / s_fi_3["Phi"]
        t_phi_fi_10 = s_q4_10["Phi"] / s_fi_10["Phi"]
        t_dm_fi_3 = s_q4_3["delta_dm"] / s_fi_3["delta_dm"]
        t_dm_fi_10 = s_q4_10["delta_dm"] / s_fi_10["delta_dm"]

        t_phi_lc_3 = s_q4_3["Phi"] / s_lc_3["Phi"]
        t_phi_lc_10 = s_q4_10["Phi"] / s_lc_10["Phi"]
        t_dm_lc_10 = s_q4_10["delta_dm"] / s_lc_10["delta_dm"]

        rows.append({
            "k_Mpc_inv": k,
            "at_1p0_aeq": {
                "T_Phi_AeST_over_FluidIDR": round(s_q4_1["Phi"] / s_fi_1["Phi"], 6),
                "T_dm_AeST_over_FluidIDR": round(s_q4_1["delta_dm"] / s_fi_1["delta_dm"], 6),
                "T_Phi_AeST_over_LCDM": round(s_q4_1["Phi"] / s_lc_1["Phi"], 6),
                "T_dm_AeST_over_LCDM": round(s_q4_1["delta_dm"] / s_lc_1["delta_dm"], 6),
            },
            "at_3p0_aeq_recomb": {
                "T_Phi_AeST_over_FluidIDR": round(t_phi_fi_3, 6),
                "T_dm_AeST_over_FluidIDR": round(t_dm_fi_3, 6),
                "T_Phi_AeST_over_LCDM": round(t_phi_lc_3, 6),
                "T_dm_AeST_over_LCDM": round(s_q4_3["delta_dm"] / s_lc_3["delta_dm"], 6),
            },
            "at_10p0_aeq_matter": {
                "T_Phi_AeST_over_FluidIDR": round(t_phi_fi_10, 6),
                "T_dm_AeST_over_FluidIDR": round(t_dm_fi_10, 6),
                "Pk_ratio_AeST_over_FluidIDR": round(t_dm_fi_10**2, 6),
                "T_Phi_AeST_over_LCDM": round(t_phi_lc_10, 6),
                "T_dm_AeST_over_LCDM": round(t_dm_lc_10, 6),
                "Pk_ratio_AeST_over_LCDM_fixed_params": round(t_dm_lc_10**2, 6),
            },
            "max_rel_E00_q4": r_q4["max_rel_E00"],
            "max_rel_E0x_q4": r_q4["max_rel_E0x"],
        })

    max_dev_phi_fi = max(abs(r["at_3p0_aeq_recomb"]["T_Phi_AeST_over_FluidIDR"] - 1.0) for r in rows)
    max_dev_dm_fi = max(abs(r["at_10p0_aeq_matter"]["T_dm_AeST_over_FluidIDR"] - 1.0) for r in rows)

    return {
        "eps_Q": eps_Q,
        "equivalent_dNeff": round(eps_Q * DNEFF_PER_EPSQ, 5),
        "max_rel_E00_across_all_24_runs": float(f"{max_e00_all:.3e}"),
        "max_rel_E0x_across_all_24_runs": float(f"{max_e0x_all:.3e}"),
        "max_abs_deviation_T_Phi_AeST_vs_FluidIDR_at_recomb": round(max_dev_phi_fi, 6),
        "max_abs_deviation_T_dm_AeST_vs_FluidIDR_at_10aeq": round(max_dev_dm_fi, 6),
        "k_grid_rows": rows,
    }


def load_desi_dr2_bao() -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray, np.ndarray]:
    """Load 13-point DESI DR2 Gaussian BAO mean vector, quantities, inverse covariance, and Cholesky factor."""
    mean_p = os.path.join(ROOT, "04_cosmology/external_data/desi_gaussian_bao_ALL_GCcomb_mean.txt")
    cov_p = os.path.join(ROOT, "04_cosmology/external_data/desi_gaussian_bao_ALL_GCcomb_cov.txt")
    zs, vals, qtypes = [], [], []
    with open(mean_p, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            zs.append(float(parts[0]))
            vals.append(float(parts[1]))
            qtypes.append(parts[2])
    cov = np.loadtxt(cov_p)
    icov = np.linalg.inv(cov)
    L_bao = np.linalg.cholesky(icov)  # icov = L_bao @ L_bao.T
    return np.array(zs), np.array(vals), qtypes, icov, L_bao


def eval_desi_bao_pred(h: float, om_h2: float, ob_h2: float, dneff: float, zs: np.ndarray, qtypes: list[str]) -> tuple[np.ndarray, float]:
    """First-principles DESI DR2 BAO predictions (with exact dNeff sound-horizon shift) and r_d [Mpc]."""
    # Reuse d4.compute_cosmo_observables structure across all DESI redshifts
    ocb_h2 = om_h2 - ONU_M
    neff_massless = NEFF_STD - 1.015333
    omega_nu_rel_h2 = d4.OMEGA_GAMMA_H2 * NEU_FACTOR * 1.015333

    def omega_nu_h2_of_a(a: float) -> float:
        return math.hypot(ONU_M / (a**3), omega_nu_rel_h2 / (a**4))

    or_ml_h2 = d4.OMEGA_GAMMA_H2 * (1.0 + NEU_FACTOR * (neff_massless + dneff))
    ol_h2 = (h**2) - ocb_h2 - omega_nu_h2_of_a(1.0) - or_ml_h2

    def H_kms_mpc(a: float) -> float:
        h2_a = or_ml_h2 / (a**4) + omega_nu_h2_of_a(a) + ocb_h2 / (a**3) + ol_h2
        return 100.0 * math.sqrt(max(h2_a, 1e-30))

    z_d = d4.z_drag_planck_calibrated(ob_h2, ocb_h2)
    a_d = 1.0 / (1.0 + z_d)
    u_grid = np.linspace(math.log(1e-10), math.log(a_d), 4000)
    a_grid = np.exp(u_grid)
    Rb_grid = (3.0 * ob_h2) / (4.0 * d4.OMEGA_GAMMA_H2) * a_grid
    cs_grid = d4.C_KMS / np.sqrt(3.0 * (1.0 + Rb_grid))
    H_grid = np.array([H_kms_mpc(float(av)) for av in a_grid])
    f_u = cs_grid / (a_grid * H_grid)
    rd = float(np.sum(0.5 * (f_u[1:] + f_u[:-1]) * np.diff(u_grid)))

    # Comoving distance grid up to max(zs) = 2.33
    z_max = float(np.max(zs)) * 1.001
    zg = np.linspace(0.0, z_max, 4000)
    invH = np.array([d4.C_KMS / H_kms_mpc(1.0 / (1.0 + float(zv))) for zv in zg])
    dm_g = np.concatenate([[0.0], np.cumsum(0.5 * (invH[1:] + invH[:-1]) * np.diff(zg))])

    preds = np.zeros(len(zs))
    for i, (zv, qt) in enumerate(zip(zs, qtypes)):
        dm = float(np.interp(zv, zg, dm_g))
        dh = d4.C_KMS / H_kms_mpc(1.0 / (1.0 + float(zv)))
        if qt == "DM_over_rs":
            preds[i] = dm / rd
        elif qt == "DH_over_rs":
            preds[i] = dh / rd
        elif qt == "DV_over_rs":
            preds[i] = ((zv * (dm**2) * dh) ** (1.0 / 3.0)) / rd
        else:
            raise ValueError(qt)
    return preds, rd


def compute_sigma8_from_pk(kh: np.ndarray, pk_h3: np.ndarray) -> float:
    """Compute sigma_8 from CLASS pk.dat columns (k [h/Mpc], P(k) [(Mpc/h)^3]) using top-hat R = 8 Mpc/h."""
    R = 8.0
    x = kh * R
    w = np.where(x < 1e-4, 1.0 - (x**2) / 10.0, 3.0 * (np.sin(x) - x * np.cos(x)) / (x**3))
    integrand = (kh**3) * pk_h3 * (w**2) / (2.0 * (math.pi**2))
    lnk = np.log(kh)
    return float(math.sqrt(np.sum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(lnk))))


def run_class_spectrum(
    theta: tuple[float, float, float, float, float],
    dneff: float,
    dr_mode: str,
    omp_threads: int = 2,
) -> dict | None:
    """Run CLASS for theta = (omega_b, omega_cdm, n_s, lnA, h) and return lensed Cls and P(k)."""
    ob, oc, ns, lnA, h = theta
    with tempfile.TemporaryDirectory(prefix="q4_cls_") as d:
        ini = os.path.join(d, "in.ini")
        root = os.path.join(d, "out_")
        if dr_mode == "none" or dneff == 0.0:
            dr_block = "N_ur = 2.0328\n"
        elif dr_mode == "fluid_idr":
            dr_block = f"N_ur = 2.0328\nN_idr = {dneff:.6f}\nidr_nature = fluid\n"
        elif dr_mode == "freestream_ur":
            dr_block = f"N_ur = {2.0328 + dneff:.6f}\n"
        else:
            raise ValueError(dr_mode)

        with open(ini, "w", encoding="utf-8") as f:
            f.write(
                f"""output = tCl,pCl,lCl,mPk
lensing = yes
l_max_scalars = 2550
P_k_max_1/Mpc = 1.0
omega_b = {ob:.7f}
omega_cdm = {oc:.7f}
h = {h:.7f}
tau_reio = 0.0544
n_s = {ns:.6f}
ln10^{{10}}A_s = {lnA:.6f}
{dr_block}N_ncdm = 1
m_ncdm = 0.06
T_ncdm = 0.71611
root = {root}
write parameters = no
"""
            )
        env = dict(os.environ, OMP_NUM_THREADS=str(omp_threads))
        r = subprocess.run([CLASS_BIN, ini], capture_output=True, env=env, timeout=120)
        if r.returncode != 0:
            return None
        cl_files = sorted(glob.glob(root + "*cl_lensed.dat"))
        pk_files = sorted(glob.glob(root + "*pk.dat"))
        if not cl_files or not pk_files:
            return None
        cl_arr = np.loadtxt(cl_files[0])
        pk_arr = np.loadtxt(pk_files[0])
        return {"cl": cl_arr, "pk": pk_arr}


def make_evaluator(
    plik: pl.PlikLite,
    L_plik: np.ndarray,
    bao_data: tuple[np.ndarray, np.ndarray, list[str], np.ndarray, np.ndarray],
    part_a: dict,
):
    """Build residual & summary evaluator for any model configuration."""
    zs_b, vals_b, qt_b, icov_b, L_bao = bao_data
    k_tab = np.log(np.array([r["k_Mpc_inv"] for r in part_a["k_grid_rows"]]))
    t_phi_tab = np.array([r["at_3p0_aeq_recomb"]["T_Phi_AeST_over_FluidIDR"] for r in part_a["k_grid_rows"]])
    t_dm_tab = np.array([r["at_10p0_aeq_matter"]["T_dm_AeST_over_FluidIDR"] for r in part_a["k_grid_rows"]])
    CHI_STAR_MPC = 13870.0

    def T_phi_sq_of_ell(ell_arr: np.ndarray) -> np.ndarray:
        lk = np.log(np.clip(ell_arr / CHI_STAR_MPC, K_GRID_MPC[0], K_GRID_MPC[-1]))
        tp = np.interp(lk, k_tab, t_phi_tab)
        return tp**2

    def T_dm_sq_of_k_mpc(k_mpc_arr: np.ndarray) -> np.ndarray:
        lk = np.log(np.clip(k_mpc_arr, K_GRID_MPC[0], K_GRID_MPC[-1]))
        td = np.interp(lk, k_tab, t_dm_tab)
        return td**2

    def eval_point(theta: tuple[float, float, float, float, float], dneff: float, dr_mode: str, apply_aest_transfer: bool, omp_threads: int = 2) -> dict:
        ob, oc, ns, lnA, h = theta
        res = run_class_spectrum(theta, dneff, dr_mode, omp_threads=omp_threads)
        if res is None:
            raise RuntimeError(f"CLASS failed at theta={theta}")
        cl = res["cl"]
        pk = res["pk"]
        ell = cl[:, 0]
        dl_tt = cl[:, 1] * (TCMB_UK**2)
        dl_ee = cl[:, 2] * (TCMB_UK**2)
        dl_te = cl[:, 3] * (TCMB_UK**2)

        # Undressed plik_lite vector & chi2
        g = np.arange(pl.LMIN, pl.LMAX + 1)
        f_conv = 2.0 * np.pi / (g * (g + 1.0))
        tt_u = np.interp(g, ell, dl_tt) * f_conv
        te_u = np.interp(g, ell, dl_te) * f_conv
        ee_u = np.interp(g, ell, dl_ee) * f_conv
        t_vec_undressed = pl.bin_theory(tt_u, te_u, ee_u, plik.blmin, plik.blmax, plik.bw)
        r_plik_undressed = plik.data - t_vec_undressed
        chi2_plik_undressed = float(r_plik_undressed @ plik.icov @ r_plik_undressed)

        # AeST vector-scalar transfer-dressed plik_lite vector & chi2
        factor_ell = T_phi_sq_of_ell(g) if apply_aest_transfer else np.ones_like(g, dtype=float)
        t_vec_dressed = pl.bin_theory(tt_u * factor_ell, te_u * factor_ell, ee_u * factor_ell, plik.blmin, plik.blmax, plik.bw)
        r_plik = plik.data - t_vec_dressed
        chi2_plik = float(r_plik @ plik.icov @ r_plik)
        u_plik = L_plik.T @ r_plik

        # DESI DR2 BAO
        om_h2 = ob + oc + ONU_M
        bao_pred, rd = eval_desi_bao_pred(h, om_h2, ob, dneff, zs_b, qt_b)
        r_bao = vals_b - bao_pred
        chi2_bao = float(r_bao @ icov_b @ r_bao)
        u_bao = L_bao.T @ r_bao

        # Matter power spectrum P(k) & sigma_8
        kh = pk[:, 0]
        pk_h3_undressed = pk[:, 1]
        k_mpc = kh * h
        factor_pk = T_dm_sq_of_k_mpc(k_mpc) if apply_aest_transfer else np.ones_like(k_mpc, dtype=float)
        pk_h3 = pk_h3_undressed * factor_pk
        sigma8 = compute_sigma8_from_pk(kh, pk_h3)
        sigma8_undressed = compute_sigma8_from_pk(kh, pk_h3_undressed)
        om0 = om_h2 / (h**2)
        s8 = sigma8 * math.sqrt(om0 / 0.3)

        # Interpolate P(k, z=0) in Mpc^3 at K_GRID_MPC
        pk_mpc3 = pk_h3 / (h**3)
        pk_at_grid = np.exp(np.interp(np.log(K_GRID_MPC), np.log(k_mpc), np.log(pk_mpc3)))

        # First 3 TT acoustic peak positions & heights
        def peak_info(lo: int, hi: int) -> tuple[float, float]:
            mask = (ell >= lo) & (ell <= hi)
            sub_l = ell[mask]
            sub_dl = dl_tt[mask] * (T_phi_sq_of_ell(sub_l) if apply_aest_transfer else 1.0)
            idx = int(np.argmax(sub_dl))
            return float(sub_l[idx]), float(sub_dl[idx])

        l1, h1 = peak_info(180, 260)
        l2, h2 = peak_info(480, 600)
        l3, h3 = peak_info(750, 900)

        return {
            "theta": [float(x) for x in theta],
            "omega_b": float(ob),
            "omega_cdm": float(oc),
            "omega_m_h2": float(om_h2),
            "Omega_m": float(om0),
            "H0": float(100.0 * h),
            "n_s": float(ns),
            "ln10_10_As": float(lnA),
            "dNeff": float(dneff),
            "dr_mode": dr_mode,
            "apply_aest_transfer": bool(apply_aest_transfer),
            "rd_Mpc": float(rd),
            "sigma8": float(sigma8),
            "sigma8_undressed": float(sigma8_undressed),
            "S8": float(s8),
            "chi2_plik": float(chi2_plik),
            "chi2_plik_undressed": float(chi2_plik_undressed),
            "chi2_desi_bao": float(chi2_bao),
            "chi2_total": float(chi2_plik + chi2_bao),
            "peaks_TT": {"l1": l1, "Dl1_uK2": round(h1, 2), "l2": l2, "Dl2_uK2": round(h2, 2), "l3": l3, "Dl3_uK2": round(h3, 2)},
            "pk_mpc3_at_grid": [float(x) for x in pk_at_grid],
            "_u": np.concatenate([u_plik, u_bao]),
        }

    return eval_point


def gauss_newton_refit(
    eval_point,
    theta0: list[float],
    dneff: float,
    dr_mode: str,
    apply_aest_transfer: bool,
    n_steps: int = 2,
) -> dict:
    """Parallel Gauss-Newton / Levenberg-Marquardt optimizer on the 626-bin Cholesky residual vector."""
    theta = np.array(theta0, dtype=float)
    steps_diff = np.array([4.0e-5, 1.5e-4, 1.0e-3, 1.0e-3, 1.0e-3], dtype=float)
    bounds_lo = np.array([0.019, 0.100, 0.90, 2.90, 0.60])
    bounds_hi = np.array([0.025, 0.145, 1.02, 3.20, 0.78])

    cur = eval_point(tuple(theta), dneff, dr_mode, apply_aest_transfer, omp_threads=4)

    for _ in range(n_steps):
        # Evaluate 5 forward-difference perturbed parameter vectors in parallel
        pert_thetas = []
        for j in range(5):
            tp = theta.copy()
            tp[j] += steps_diff[j]
            pert_thetas.append(tuple(tp))

        with ThreadPoolExecutor(max_workers=5) as ex:
            futs = [
                ex.submit(eval_point, pt, dneff, dr_mode, apply_aest_transfer, 2)
                for pt in pert_thetas
            ]
            pert_res = [f.result() for f in futs]

        u0 = cur["_u"]
        J = np.zeros((len(u0), 5), dtype=float)
        for j in range(5):
            J[:, j] = (pert_res[j]["_u"] - u0) / steps_diff[j]

        JTJ = J.T @ J
        g = J.T @ u0
        # Test 3 Levenberg-Marquardt damping levels in parallel and keep the best improvement
        cand_thetas = []
        for lam in (0.0, 0.1, 1.0):
            A = JTJ + lam * np.diag(np.diag(JTJ))
            delta = -np.linalg.solve(A, g)
            tc = np.clip(theta + delta, bounds_lo, bounds_hi)
            cand_thetas.append(tuple(tc))

        with ThreadPoolExecutor(max_workers=3) as ex:
            cand_res = list(ex.map(lambda pt: eval_point(pt, dneff, dr_mode, apply_aest_transfer, 2), cand_thetas))

        best_cand = min(cand_res, key=lambda r: r["chi2_total"])
        if best_cand["chi2_total"] < cur["chi2_total"] - 1e-4:
            improve = cur["chi2_total"] - best_cand["chi2_total"]
            cur = best_cand
            theta = np.array(cur["theta"], dtype=float)
            if improve < 0.05:
                break
        else:
            break

    return cur


def strip_private(d: dict, ref_lcdm: dict) -> dict:
    out = {k: v for k, v in d.items() if not k.startswith("_")}
    out["dchi2_plik_vs_LCDM"] = round(d["chi2_plik"] - ref_lcdm["chi2_plik"], 3)
    out["dchi2_bao_vs_LCDM"] = round(d["chi2_desi_bao"] - ref_lcdm["chi2_desi_bao"], 3)
    out["dchi2_total_vs_LCDM"] = round(d["chi2_total"] - ref_lcdm["chi2_total"], 3)
    out["aest_dressing_dchi2_plik"] = round(d["chi2_plik"] - d["chi2_plik_undressed"], 4)
    out["Pk_ratio_vs_LCDM_at_grid"] = [
        {"k_Mpc_inv": K_GRID_MPC[i], "Pk_over_Pk_LCDM": round(d["pk_mpc3_at_grid"][i] / ref_lcdm["pk_mpc3_at_grid"][i], 5)}
        for i in range(len(K_GRID_MPC))
    ]
    return out


def main() -> int:
    t0 = time.time()
    # 1. Validate PlikLite reader on Planck's shipped best-fit spectrum
    plik = pl.PlikLite()
    bf = np.loadtxt(os.path.join(pl.EXT, "bf_lite_plikTTTEEE_v22b_lowl_simall.minimum.theory_cl"))
    val_chi2 = plik.chi2(bf[:, 0], bf[:, 1], bf[:, 2], bf[:, 3])
    assert abs(val_chi2 - 548.5) < 1.0, f"PlikLite validation failed: {val_chi2}"
    L_plik = np.linalg.cholesky(plik.icov)
    bao_data = load_desi_dr2_bao()

    # 2. Part A: Exact SymPy/Radau AeST Q^4 vs Fluid-IDR and LCDM transfer ratios across 8 k-modes
    funcs = g1.f1_derive_flrw_with_cdm()
    part_a = part_a_aest_q4_vs_fluid_idr_transfer(funcs)

    # 3. Part B: Joint CLASS + PlikLite (613) + DESI DR2 BAO (13) fits
    eval_point = make_evaluator(plik, L_plik, bao_data, part_a)

    # M0: LCDM joint fit (warm-started from cmb_plik_results.json best fit)
    theta0_lcdm = [0.0222868, 0.120625, 0.961707, 3.04459, 0.670244]
    m0_lcdm = gauss_newton_refit(eval_point, theta0_lcdm, 0.0, "none", False, n_steps=2)

    # M1: AeST Q^4 (dNeff = 0.270) evaluated at M0's LCDM parameters without refitting
    m1_unrefit = eval_point(tuple(m0_lcdm["theta"]), 0.270, "fluid_idr", True, omp_threads=4)

    # M2: AeST Q^4 at canonical PR #226 BBN central point (dNeff = 0.270 <=> eps_Q = 0.03625), joint refit
    theta0_q4_270 = [0.02255, 0.1235, 0.968, 3.052, 0.692]
    m2_q4_270 = gauss_newton_refit(eval_point, theta0_q4_270, 0.270, "fluid_idr", True, n_steps=2)

    # M3: AeST Q^4 at Gate 1 top-of-window point (eps_Q = 0.0390 <=> dNeff = 0.29052), joint refit
    dneff_039 = round(0.039 * DNEFF_PER_EPSQ, 5)
    theta0_q4_039 = list(m2_q4_270["theta"])
    m3_q4_039 = gauss_newton_refit(eval_point, theta0_q4_039, dneff_039, "fluid_idr", True, n_steps=2)

    # M4: GR free-streaming extra radiation (dNeff = 0.270 in N_ur, sigma != 0), joint refit
    theta0_fs_270 = list(m2_q4_270["theta"])
    m4_fs_270 = gauss_newton_refit(eval_point, theta0_fs_270, 0.270, "freestream_ur", False, n_steps=2)

    models_out = {
        "M0_LCDM_joint_fit": strip_private(m0_lcdm, m0_lcdm),
        "M1_AeST_Q4_dNeff0p270_unrefitted_at_LCDM": strip_private(m1_unrefit, m0_lcdm),
        "M2_AeST_Q4_PR226_dNeff0p270_joint_fit": strip_private(m2_q4_270, m0_lcdm),
        "M3_AeST_Q4_Gate1_eps0p039_dNeff0p291_joint_fit": strip_private(m3_q4_039, m0_lcdm),
        "M4_GR_freestream_dNeff0p270_joint_fit": strip_private(m4_fs_270, m0_lcdm),
    }

    out = {
        "meta": {
            "date_utc": "2026-11-21",
            "plik_lite_validation_chi2": round(val_chi2, 2),
            "plik_lite_nbins": pl.NBIN,
            "desi_dr2_bao_nbins": len(bao_data[0]),
            "total_nbins": pl.NBIN + len(bao_data[0]),
            "elapsed_seconds": round(time.time() - t0, 2),
        },
        "part_A_sympy_radau_multi_k_transfer": part_a,
        "part_B_class_plik_desi_joint_fits": models_out,
        "summary_comparison": {
            "AeST_vector_scalar_perturbation_vs_FluidIDR": (
                f"Across k in [0.005, 0.30] Mpc^-1, full coupled AeST Q^4 + running lambda_s(Q) differs from an "
                f"uncoupled w=1/3, cs^2=1/3, sigma=0 perfect fluid by at most "
                f"{100.0*part_a['max_abs_deviation_T_Phi_AeST_vs_FluidIDR_at_recomb']:.3f}% in Phi(3 a_eq) and "
                f"{100.0*part_a['max_abs_deviation_T_dm_AeST_vs_FluidIDR_at_10aeq']:.3f}% in delta_m(10 a_eq), "
                f"shifting plik_lite chi^2 by only {models_out['M2_AeST_Q4_PR226_dNeff0p270_joint_fit']['aest_dressing_dchi2_plik']:+.3f}."
            ),
            "M0_LCDM": {
                "chi2_plik": round(m0_lcdm["chi2_plik"], 2),
                "chi2_bao": round(m0_lcdm["chi2_desi_bao"], 2),
                "chi2_total": round(m0_lcdm["chi2_total"], 2),
                "H0": round(m0_lcdm["H0"], 2),
                "omega_m_h2": round(m0_lcdm["omega_m_h2"], 5),
                "sigma8": round(m0_lcdm["sigma8"], 4),
                "S8": round(m0_lcdm["S8"], 4),
            },
            "M2_AeST_Q4_dNeff0p270": {
                "chi2_plik": round(m2_q4_270["chi2_plik"], 2),
                "chi2_bao": round(m2_q4_270["chi2_desi_bao"], 2),
                "chi2_total": round(m2_q4_270["chi2_total"], 2),
                "dchi2_vs_LCDM": models_out["M2_AeST_Q4_PR226_dNeff0p270_joint_fit"]["dchi2_total_vs_LCDM"],
                "H0": round(m2_q4_270["H0"], 2),
                "omega_m_h2": round(m2_q4_270["omega_m_h2"], 5),
                "sigma8": round(m2_q4_270["sigma8"], 4),
                "S8": round(m2_q4_270["S8"], 4),
            },
            "M3_AeST_Q4_eps0p039_dNeff0p291": {
                "chi2_plik": round(m3_q4_039["chi2_plik"], 2),
                "chi2_bao": round(m3_q4_039["chi2_desi_bao"], 2),
                "chi2_total": round(m3_q4_039["chi2_total"], 2),
                "dchi2_vs_LCDM": models_out["M3_AeST_Q4_Gate1_eps0p039_dNeff0p291_joint_fit"]["dchi2_total_vs_LCDM"],
                "H0": round(m3_q4_039["H0"], 2),
                "omega_m_h2": round(m3_q4_039["omega_m_h2"], 5),
                "sigma8": round(m3_q4_039["sigma8"], 4),
                "S8": round(m3_q4_039["S8"], 4),
            },
            "M4_GR_freestream_dNeff0p270": {
                "chi2_plik": round(m4_fs_270["chi2_plik"], 2),
                "chi2_bao": round(m4_fs_270["chi2_desi_bao"], 2),
                "chi2_total": round(m4_fs_270["chi2_total"], 2),
                "dchi2_vs_LCDM": models_out["M4_GR_freestream_dNeff0p270_joint_fit"]["dchi2_total_vs_LCDM"],
                "H0": round(m4_fs_270["H0"], 2),
                "omega_m_h2": round(m4_fs_270["omega_m_h2"], 5),
                "sigma8": round(m4_fs_270["sigma8"], 4),
                "S8": round(m4_fs_270["S8"], 4),
            },
        },
    }

    jpath = os.path.join(HERE, "Q4_BOLTZMANN_CMB_PK_FIT.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")

    print(json.dumps({
        "meta": out["meta"],
        "part_A_summary": {k: v for k, v in part_a.items() if k != "k_grid_rows"},
        "summary_comparison": out["summary_comparison"],
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
