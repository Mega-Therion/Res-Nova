#!/usr/bin/env python3
"""Blind test of P-OM-1 v2 on KiDS-Legacy (DR5 Cosmic Shear) & GAMA DR4.

Pre-registered: 03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md
(frozen and committed before running on unblinded KiDS-Legacy isolated lenses).

Evaluates the frozen pom1v2_mass_system.py / pom1_lensing_rar.py model:
  - Interpolating function: mu_std(x) = x / sqrt(1 + x^2)
  - Acceleration anchor: a0 = 1.1607e-10 m/s^2 (fixed; NOT refit)
  - Estimator conversion: g_obs = 4 * G * DeltaSigma * (73 / 70)
  - LTG baryons: Boselli+2014 cold gas on stellar mass (Q_LTG = 1.0)
  - ETG baryons: Chae+2021 hot gas (M_hot = 10^-5.414 M*^1.47) with no cold gas
  - Zero per-sample free parameter tuning.

Independent Blind Samples (disjoint from KiDS-1000 Brouwer+2021):
  1. DR5_New329 : 329 active KiDS-DR5 tiles absent from DR4 and G23 (photo-z calibrated on G09->G23)
  2. GAMA_G23   : Spectroscopic GAMA DR4 G23 paired with KiDS-Legacy shear
  3. GAMA_All4  : Full G09+G12+G15+G23 spectroscopic 3D isolated sample + KiDS-Legacy shear

Usage:
  python3 03_observer_jwst/pom1v2_blind_kids_legacy.py --self-test
  python3 03_observer_jwst/pom1v2_blind_kids_legacy.py
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
from scipy import integrate
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree
from scipy.stats import chi2 as chi2_dist

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pom1_lensing_rar as P  # noqa: E402
import pom1v2_mass_system as V2  # noqa: E402

# ------------------------------------------------------------------ Frozen Constants
C_LIGHT_KM_S = 299792.458
G_SI = 6.67430e-11
MSUN_KG = 1.98847e30
MPC_M = 3.0856775814913673e22
PC_M = 3.0856775814913673e16
# Sigma_crit constant: c^2 / (4 pi G) in (Msun / pc^2) * Mpc (~ 1.66287e6)
SIG_CR_FACTOR = ((C_LIGHT_KM_S * 1e3) ** 2 / (4.0 * math.pi * G_SI)) / (MSUN_KG / (PC_M ** 2)) / MPC_M

OM_P18, OL_P18, H0_B21 = 0.3153, 0.6847, 70.0
# KiDS-Legacy cosmic shear Table 1 (arXiv:2503.19441) multiplicative calibration bias per TOMOBIN 1..6
KIDS_M_GOLD = np.array([0.0, -0.023, -0.016, -0.011, +0.020, +0.030, +0.045], dtype=np.float64)

# B21 15 log10(g_bar) bin centers & edges: [-14.9826 .. -11.2837]
N_GB_BINS = 15
GB_LOG_EDGES = np.linspace(-14.8593 - 0.123285, -11.4070 + 0.123285, N_GB_BINS + 1)

# Pre-frozen G09->G23 photometric calibration (task-699, zero shear used)
BETA_Z_DR5 = np.array([-0.043490, 0.954353, -0.561158, 0.030555, 0.034788, -0.013131, 0.062737], dtype=np.float64)
DR5_GAMA_MASS_OFFSET = 0.1293  # Align DR5 (LePhare + ap2 at z_cal) to GAMA/Schombert+2014

WL_DTYPE = np.dtype([
    ("ra", "<f8"), ("dec", "<f8"), ("z_b", "<f4"), ("e1", "<f4"), ("e2", "<f4"),
    ("weight", "<f4"), ("tomobin", "i1"), ("patch_n", "i1"), ("is_new_dr5", "u1"),
])

WL_BIN_PATH = Path("/tmp/kids_legacy_wl_slim.bin")
NZ_FITS_PATH = Path("/tmp/kl_data/KiDS_Legacy_cosmic_shear_data_release/data/KiDS_Legacy_xipm.fits")
LENS_DIR = Path("/tmp/kids_lenses")
DR5_NEW_TILES_TXT = Path("/tmp/dr5_new_tiles.txt")


# ------------------------------------------------------------------ Cosmology & Lensing Geometry
def comoving_dist_mpc(z: float, om: float = OM_P18, ol: float = OL_P18, h0: float = H0_B21) -> float:
    val, _ = integrate.quad(lambda zp: 1.0 / math.sqrt(om * (1.0 + zp) ** 3 + ol), 0.0, float(z), epsrel=1e-9)
    return (C_LIGHT_KM_S / h0) * val


def build_distance_tables(z_max: float = 6.0):
    z_grid = np.linspace(0.0, z_max, 2401)
    # Fast trapezoidal cumulative integral for D_C(z)
    ez = np.sqrt(OM_P18 * (1.0 + z_grid) ** 3 + OL_P18)
    inv_ez = 1.0 / ez
    dz = z_grid[1] - z_grid[0]
    dc = np.zeros_like(z_grid)
    dc[1:] = np.cumsum(0.5 * (inv_ez[:-1] + inv_ez[1:]) * dz) * (C_LIGHT_KM_S / H0_B21)
    da = dc / (1.0 + z_grid)
    return z_grid, dc, da


def build_sigma_crit_inv_splines(z_mid: np.ndarray, nz_bins: np.ndarray):
    """Build Sigma_crit^{-1}(z_l, tomo) [pc^2 / Msun] integrated over exact n_tomo(z_s)."""
    z_grid, dc_grid, da_grid = build_distance_tables(max(float(z_mid.max()) + 0.1, 6.0))
    dc_s = np.interp(z_mid, z_grid, dc_grid)
    da_s = dc_s / (1.0 + z_mid)
    dz = np.gradient(z_mid)

    zl_knots = np.linspace(0.02, 0.58, 113)
    dc_l_knots = np.interp(zl_knots, z_grid, dc_grid)
    da_l_knots = dc_l_knots / (1.0 + zl_knots)

    # Normalize each bin strictly to 1
    splines = {}
    for b in range(nz_bins.shape[0]):
        nz = np.maximum(nz_bins[b], 0.0)
        nz = nz / np.sum(nz * dz)
        vals = np.zeros_like(zl_knots)
        for i, (zl, dcl, dal) in enumerate(zip(zl_knots, dc_l_knots, da_l_knots)):
            msk = z_mid > zl
            if not np.any(msk):
                continue
            dls = (dc_s[msk] - dcl) / (1.0 + z_mid[msk])
            ratio = np.maximum(dls, 0.0) / np.maximum(da_s[msk], 1e-12)
            integral = float(np.sum(nz[msk] * dz[msk] * ratio))
            vals[i] = (dal / SIG_CR_FACTOR) * integral
        splines[b + 1] = CubicSpline(zl_knots, vals)
    return splines, z_grid, dc_grid, da_grid


def load_kids_nz():
    from astropy.io import fits
    with fits.open(NZ_FITS_PATH, memmap=True) as h:
        nz = h["NZ_SOURCE"].data
        z_mid = np.asarray(nz["Z_MID"], np.float64)
        bins = np.vstack([np.asarray(nz[f"BIN{b}"], np.float64) for b in range(1, 7)])
    return z_mid, bins


# ------------------------------------------------------------------ Baryon Mass Model (Frozen v2)
def lens_baryon_mass_msun(log_mstar: np.ndarray, is_etg: np.ndarray, q_etg: float = 1.0, q_ltg: float = 1.0) -> np.ndarray:
    """Apply frozen Mistele+2024 / Brouwer+2021 gas prescriptions per lens in Msun (h70^-2)."""
    lm = np.asarray(log_mstar, np.float64).copy()
    etg = np.asarray(is_etg, bool)
    ms = np.where(etg, q_etg * (10.0 ** lm), q_ltg * (10.0 ** lm))
    lm_eff = np.log10(np.maximum(ms, 1.0))
    # LTG cold gas: Boselli+2014 / B21 Eq. 23
    f_cold = 10.0 ** (-0.69 * lm_eff + 6.63)
    m_ltg = ms * (1.0 + f_cold)
    # ETG hot gas: Chae+2021 / Mistele+2024 Eq. 4.1 (no cold gas)
    m_etg = ms + (10.0 ** (-5.414)) * (ms ** 1.47)
    return np.where(etg, m_etg, m_ltg)


def sph_xyz(ra: np.ndarray, dec: np.ndarray) -> np.ndarray:
    r, d = np.radians(ra), np.radians(dec)
    return np.column_stack([np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)])


# ------------------------------------------------------------------ Core Vectorized Pair Accumulator
def compute_binned_lensing(
    lenses: dict,
    s_ra: np.ndarray,
    s_dec: np.ndarray,
    s_zb: np.ndarray,
    s_e1: np.ndarray,
    s_e2: np.ndarray,
    s_w: np.ndarray,
    s_tomo: np.ndarray,
    sc_splines: dict,
    z_grid: np.ndarray,
    da_grid: np.ndarray,
    r_min_mpc: float = 0.03,
    r_max_mpc: float = 0.30,
    n_jk: int = 40,
    batch_size: int = 400,
    tree_s: cKDTree | None = None,
):
    """Accumulate (n_jk, 2 [LTG,ETG], 15 [log_gbar]) arrays of numerators/denominators."""
    n_l = len(lenses["ra"])
    if tree_s is None:
        tree_s = cKDTree(sph_xyz(s_ra, s_dec))

    l_ra = lenses["ra"]
    l_dec = lenses["dec"]
    l_z = lenses["z"]
    l_mb = lenses["mb"]
    l_etg = lenses["etg"].astype(np.int8)
    l_jk = lenses["jk"]
    l_da = np.interp(l_z, z_grid, da_grid)
    l_xyz = sph_xyz(l_ra, l_dec)
    # Query angular radius matching r_max_mpc
    l_rmax_rad = r_max_mpc / np.maximum(l_da, 1.0)

    # Pre-eval Sigma_crit_inv[n_l, 7] per tomographic bin 1..6 (0 unused)
    sc_inv_lens = np.zeros((n_l, 7), dtype=np.float64)
    for b in range(1, 7):
        sc_inv_lens[:, b] = np.maximum(sc_splines[b](l_z), 0.0)

    # Accumulators shape: (n_jk, 2, N_GB_BINS)
    acc_num_t = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_num_x = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_den_m = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_den_w = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_gb_w = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_npair = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.int64)

    m_gold_s = KIDS_M_GOLD[s_tomo]
    g_msun_div_mpc2 = (G_SI * MSUN_KG) / (MPC_M ** 2)

    for start in range(0, n_l, batch_size):
        end = min(start + batch_size, n_l)
        nbrs = tree_s.query_ball_point(l_xyz[start:end], r=l_rmax_rad[start:end])
        # Flatten pairs cleanly in vectorized arrays
        lens_local = []
        src_idx = []
        for k_loc, s_arr in enumerate(nbrs):
            if s_arr:
                lens_local.append(np.full(len(s_arr), start + k_loc, dtype=np.int32))
                src_idx.append(np.asarray(s_arr, dtype=np.int32))
        if not lens_local:
            continue
        li = np.concatenate(lens_local)
        si = np.concatenate(src_idx)

        # Foreground dilution cut: z_B + 0.2 > z_l
        cut = (s_zb[si] + 0.20) > l_z[li]
        if not np.any(cut):
            continue
        li, si = li[cut], si[cut]

        # Flat tangent-plane offsets in radians:
        # Image frame (East=-RA, North=+Dec): x = -dra*cos(dec_l), y = +ddec
        cos_dec_l = np.cos(np.radians(l_dec[li]))
        dra_deg = ((s_ra[si] - l_ra[li] + 180.0) % 360.0) - 180.0
        dra_rad = np.radians(dra_deg) * cos_dec_l
        ddec_rad = np.radians(s_dec[si] - l_dec[li])
        sep_rad = np.hypot(dra_rad, ddec_rad)
        r_mpc = sep_rad * l_da[li]

        rm = (r_mpc >= r_min_mpc) & (r_mpc <= r_max_mpc)
        if not np.any(rm):
            continue
        li, si, dra_rad, ddec_rad, r_mpc = li[rm], si[rm], dra_rad[rm], ddec_rad[rm], r_mpc[rm]

        # g_bar = G * M_b / R^2 -> bin in LOG10 edges
        gb = g_msun_div_mpc2 * l_mb[li] / (r_mpc * r_mpc)
        lgb = np.log10(np.maximum(gb, 1e-30))
        b_idx = np.searchsorted(GB_LOG_EDGES, lgb, side="right") - 1
        bm = (b_idx >= 0) & (b_idx < N_GB_BINS)
        if not np.any(bm):
            continue
        li, si, dra_rad, ddec_rad, gb, b_idx = li[bm], si[bm], dra_rad[bm], ddec_rad[bm], gb[bm], b_idx[bm]

        # Image-frame tangential & cross ellipticities:
        # phi_img = atan2(+ddec, -dra), cos(2 phi) = (x^2 - y^2)/r^2, sin(2 phi) = 2xy/r^2 (no trig needed!)
        x_img = -dra_rad
        y_img = ddec_rad
        r2_img = x_img * x_img + y_img * y_img
        c2 = (x_img * x_img - y_img * y_img) / np.maximum(r2_img, 1e-30)
        s2 = (2.0 * x_img * y_img) / np.maximum(r2_img, 1e-30)
        e1 = s_e1[si]
        e2 = s_e2[si]
        et = -e1 * c2 - e2 * s2
        ex = +e1 * s2 - e2 * c2

        sig_inv = sc_inv_lens[li, s_tomo[si]]
        valid_w = sig_inv > 0.0
        if not np.any(valid_w):
            continue
        li, si, b_idx, gb, et, ex, sig_inv = (
            li[valid_w], si[valid_w], b_idx[valid_w], gb[valid_w], et[valid_w], ex[valid_w], sig_inv[valid_w]
        )

        w_s = s_w[si]
        w_ls = w_s * sig_inv * sig_inv
        # Numerator: sum W_ls * Sigma_crit * e_t = sum w_s * Sigma_crit_inv * e_t
        wt_num = w_s * sig_inv * et
        wx_num = w_s * sig_inv * ex
        w_den_m = w_ls * (1.0 + m_gold_s[si])

        flat = (l_jk[li].astype(np.int64) * 2 + l_etg[li].astype(np.int64)) * N_GB_BINS + b_idx.astype(np.int64)
        n_tot = n_jk * 2 * N_GB_BINS
        acc_num_t += np.bincount(flat, weights=wt_num, minlength=n_tot).reshape(n_jk, 2, N_GB_BINS)
        acc_num_x += np.bincount(flat, weights=wx_num, minlength=n_tot).reshape(n_jk, 2, N_GB_BINS)
        acc_den_m += np.bincount(flat, weights=w_den_m, minlength=n_tot).reshape(n_jk, 2, N_GB_BINS)
        acc_den_w += np.bincount(flat, weights=w_ls, minlength=n_tot).reshape(n_jk, 2, N_GB_BINS)
        acc_gb_w += np.bincount(flat, weights=w_ls * gb, minlength=n_tot).reshape(n_jk, 2, N_GB_BINS)
        acc_npair += np.bincount(flat, minlength=n_tot).reshape(n_jk, 2, N_GB_BINS)

    return {
        "num_t": acc_num_t, "num_x": acc_num_x, "den_m": acc_den_m,
        "den_w": acc_den_w, "gb_w": acc_gb_w, "npair": acc_npair,
    }


def summarize_rar_from_accumulators(
    lens_acc: dict,
    rand_acc: dict | None = None,
    h0_conv: float = V2.H0_CONV,
    min_npair: int = 200,
    use_bins: slice | np.ndarray | None = None,
    label: str = "sample",
    q_etg: float = 1.0,
    q_ltg: float = 1.0,
):
    """Build g_bar, g_obs, cross-shear g_x, and full jackknife covariance; evaluate frozen P-OM-1 v2."""
    n_jk = lens_acc["num_t"].shape[0]
    nt = lens_acc["num_t"].sum(axis=0)
    nx = lens_acc["num_x"].sum(axis=0)
    dm = lens_acc["den_m"].sum(axis=0)
    dw = lens_acc["den_w"].sum(axis=0)
    gw = lens_acc["gb_w"].sum(axis=0)
    npair = lens_acc["npair"].sum(axis=0)

    # Full signal in [m/s^2] with H0=73 conversion
    conv = P.ESD_TO_G * h0_conv
    with np.errstate(divide="ignore", invalid="ignore"):
        g_t_raw = conv * nt / dm
        g_x = conv * nx / dm
        gb_mean = gw / dw
    if rand_acc is not None:
        rt = rand_acc["num_t"].sum(axis=0)
        rdm = rand_acc["den_m"].sum(axis=0)
        rnx = rand_acc["num_x"].sum(axis=0)
        with np.errstate(divide="ignore", invalid="ignore"):
            g_rand = np.where(rdm > 0, conv * rt / rdm, 0.0)
            gx_rand = np.where(rdm > 0, conv * rnx / rdm, 0.0)
        g_obs = g_t_raw - g_rand
        g_x = g_x - gx_rand
    else:
        g_rand = np.zeros_like(g_t_raw)
        g_obs = g_t_raw

    # Leave-one-out jackknife vectors (flattened 2*15 = 30)
    # Subtract sample rand profile from each LOO realization (or matched random LOO if aligned)
    nt_all = nt[None, :, :] - lens_acc["num_t"]
    nx_all = nx[None, :, :] - lens_acc["num_x"]
    dm_all = dm[None, :, :] - lens_acc["den_m"]
    with np.errstate(divide="ignore", invalid="ignore"):
        gt_loo = conv * nt_all / dm_all - g_rand[None, :, :]
        gx_loo = conv * nx_all / dm_all

    if rand_acc is not None and rand_acc["num_t"].shape[0] == n_jk:
        rt_tot = rand_acc["num_t"].sum(axis=0)
        rdm_tot = rand_acc["den_m"].sum(axis=0)
        rt_loo = rt_tot[None, :, :] - rand_acc["num_t"]
        rdm_loo = rdm_tot[None, :, :] - rand_acc["den_m"]
        with np.errstate(divide="ignore", invalid="ignore"):
            g_rand_loo = np.where(rdm_loo > 0, conv * rt_loo / rdm_loo, g_rand[None, :, :])
            gt_loo = conv * nt_all / dm_all - g_rand_loo

    # Select retained reliable bins
    if use_bins is None:
        # Reliable photo-z range GBAR_RELIABLE = 7.56e-14 (bins 8..14)
        bin_mask = np.zeros((2, N_GB_BINS), dtype=bool)
        bin_mask[:, 8:] = True
    else:
        bin_mask = np.asarray(use_bins, dtype=bool)
    ok_mask = bin_mask & (npair >= min_npair) & np.isfinite(gb_mean) & np.isfinite(g_obs) & (dm > 0)
    # Keep flat indices ordered: all retained late (0), then all retained early (1)
    idx_late = np.where(ok_mask[0])[0]
    idx_early = np.where(ok_mask[1])[0]

    gb_vec = np.concatenate([gb_mean[0, idx_late], gb_mean[1, idx_early]])
    d_vec = np.concatenate([g_obs[0, idx_late], g_obs[1, idx_early]])
    gx_vec = np.concatenate([g_x[0, idx_late], g_x[1, idx_early]])
    gr_vec = np.concatenate([g_rand[0, idx_late], g_rand[1, idx_early]])

    jk_mat = np.concatenate([gt_loo[:, 0, idx_late], gt_loo[:, 1, idx_early]], axis=1)
    jxk_mat = np.concatenate([gx_loo[:, 0, idx_late], gx_loo[:, 1, idx_early]], axis=1)

    # Filter out any JK cells with NaN (e.g. an empty outer patch)
    valid_jk = np.all(np.isfinite(jk_mat), axis=1)
    jk_mat = jk_mat[valid_jk]
    jxk_mat = jxk_mat[valid_jk]
    K = len(jk_mat)
    assert K >= len(d_vec) + 3, f"{label}: too few JK blocks ({K}) for {len(d_vec)} bins"

    jk_mean = jk_mat.mean(axis=0)
    diff = jk_mat - jk_mean[None, :]
    C = ((K - 1.0) / K) * (diff.T @ diff)

    jxk_diff = jxk_mat - jxk_mat.mean(axis=0)[None, :]
    Cx = ((K - 1.0) / K) * (jxk_diff.T @ jxk_diff)

    n = len(d_vec)
    hartlap = (K - n - 2.0) / (K - 1.0)

    def chi_fn(pred_v, cov=C):
        r = d_vec - pred_v
        return float(r @ np.linalg.solve(cov, r))

    pred_v = P.pred(gb_vec, P.A0_OBS)
    c0 = chi_fn(pred_v)
    p0 = float(chi2_dist.sf(c0, n))
    cN = chi_fn(4.0 / math.pi * gb_vec)
    pN = float(chi2_dist.sf(cN, n))
    c_cross = float(gx_vec @ np.linalg.solve(Cx, gx_vec))
    p_cross = float(chi2_dist.sf(c_cross, n))

    # Uniform +-0.2 dex mass systematic scan
    deltas = np.linspace(-P.MSTAR_SYS_DEX, P.MSTAR_SYS_DEX, 401)
    cs = [chi_fn(P.pred(gb_vec * (10.0 ** dl), P.A0_OBS)) for dl in deltas]
    k_best = int(np.argmin(cs))
    dm_best, cm_best = float(deltas[k_best]), float(cs[k_best])
    pm_best = float(chi2_dist.sf(cm_best, max(n - 1, 1)))

    if pN >= 1e-6:
        verdict = "NO_POWER"
    elif p0 >= 0.01:
        verdict = "PASS"
    elif pm_best >= 0.01:
        verdict = "PASS_WITHIN_MASS_SYSTEMATIC"
    else:
        verdict = "FAIL"

    # Per-type stats and early-minus-late universality test
    nl = len(idx_late)
    ne = len(idx_early)
    type_stats = {}
    for nm, sl in (("late", slice(0, nl)), ("early", slice(nl, n))):
        if (sl.stop - sl.start) > 0:
            r = d_vec[sl] - pred_v[sl]
            ct = float(r @ np.linalg.solve(C[sl, sl], r))
            type_stats[nm] = {
                "n_bins": int(sl.stop - sl.start),
                "chi2": ct,
                "p": float(chi2_dist.sf(ct, sl.stop - sl.start)),
                "median_obs_over_pred": float(np.median(d_vec[sl] / pred_v[sl])),
            }

    common = np.intersect1d(idx_late, idx_early)
    eml = None
    if len(common) > 0:
        il = np.searchsorted(idx_late, common)
        ie = nl + np.searchsorted(idx_early, common)
        rl = d_vec[il] / pred_v[il]
        re_ = d_vec[ie] / pred_v[ie]
        J = np.zeros((len(common), n))
        for t, (a, b) in enumerate(zip(ie, il)):
            J[t, a] = 1.0 / pred_v[a]
            J[t, b] = -1.0 / pred_v[b]
        dd = re_ - rl
        Cd = J @ C @ J.T
        cd = float(dd @ np.linalg.solve(Cd, dd))
        eml = {
            "chi2": cd, "dof": int(len(common)), "p": float(chi2_dist.sf(cd, len(common))),
            "median_log10_ratio": float(np.median(np.log10(np.maximum(re_, 1e-30) / np.maximum(rl, 1e-30)))),
        }

    # Detailed table rows for serialization
    rows_out = []
    for pos, (t_str, b_id) in enumerate([("LTG", int(b)) for b in idx_late] + [("ETG", int(b)) for b in idx_early]):
        ti = 0 if t_str == "LTG" else 1
        rows_out.append({
            "type": t_str, "bin": b_id, "npair": int(npair[ti, b_id]),
            "gbar": float(gb_vec[pos]), "gobs": float(d_vec[pos]),
            "err": float(math.sqrt(C[pos, pos])), "g_pred": float(pred_v[pos]),
            "g_cross": float(gx_vec[pos]), "err_cross": float(math.sqrt(Cx[pos, pos])),
            "g_rand": float(gr_vec[pos]),
        })

    return {
        "label": label,
        "verdict": verdict,
        "n_bins": int(n),
        "n_jk_active": int(K),
        "hartlap_factor": float(hartlap),
        "cond_C": float(np.linalg.cond(C)),
        "q_used": {"LTG": q_ltg, "ETG": q_etg},
        "h0_conv": float(h0_conv),
        "chi2": c0,
        "chi2_hartlap": c0 * hartlap,
        "p": p0,
        "p_hartlap": float(chi2_dist.sf(c0 * hartlap, n)),
        "newton_chi2": cN,
        "newton_p": pN,
        "cross_shear_chi2": c_cross,
        "cross_shear_p": p_cross,
        "max_abs_rand_over_obs": float(np.max(np.abs(gr_vec)) / np.median(np.abs(d_vec))),
        "mass_shift_best_dex": dm_best,
        "mass_shift_chi2": cm_best,
        "mass_shift_p": pm_best,
        "per_type": type_stats,
        "early_minus_late": eml,
        "bins": rows_out,
        "_d": d_vec, "_pred": pred_v, "_C": C, "_gb": gb_vec,
    }


def assign_spatial_jackknife(ra: np.ndarray, dec: np.ndarray, n_jk: int) -> np.ndarray:
    """Deterministic balanced 2D sky-quantile partitioning into <= n_jk contiguous-ish blocks."""
    # Factor n_jk into n_ra * n_dec
    nx = int(round(math.sqrt(n_jk * 1.5)))
    while n_jk % nx != 0 and nx > 1:
        nx -= 1
    ny = n_jk // nx
    # Rank RA quantiles into nx columns, then rank Dec within each RA strip into ny rows
    order_ra = np.argsort(ra)
    col_id = np.empty(len(ra), dtype=np.int32)
    col_id[order_ra] = (np.arange(len(ra)) * nx) // len(ra)
    jk = np.empty(len(ra), dtype=np.int32)
    for c in range(nx):
        m = np.where(col_id == c)[0]
        if len(m) == 0:
            continue
        o_d = m[np.argsort(dec[m])]
        jk[o_d] = c * ny + (np.arange(len(m)) * ny) // len(m)
    return jk


# ------------------------------------------------------------------ Self-Test (Standalone)
def run_self_test():
    # 1. Validate MOND point-mass forward model
    val = P.validate_model()
    assert val["model_checks_pass"], f"pom1 model check failed: {val}"

    # 2. Independent SI constant + analytic Delta-function n(z_s) check for build_sigma_crit_inv_splines
    assert 1.66e6 < SIG_CR_FACTOR < 1.67e6, f"Bad SIG_CR_FACTOR: {SIG_CR_FACTOR}"
    z_mid = np.linspace(0.025, 2.5, 50)
    nz_bins = np.zeros((6, len(z_mid)))
    idx_s = 20  # z_s = z_mid[idx_s]
    nz_bins[:, idx_s] = 1.0
    spl, zg, dcg, dag = build_sigma_crit_inv_splines(z_mid, nz_bins)
    zl_test = 0.25
    zs_test = float(z_mid[idx_s])
    dc_l = float(np.interp(zl_test, zg, dcg))
    da_l = dc_l / (1.0 + zl_test)
    dc_s = float(np.interp(zs_test, zg, dcg))
    da_s = dc_s / (1.0 + zs_test)
    dls = (dc_s - dc_l) / (1.0 + zs_test)
    exact_sc_inv = (da_l * dls / da_s) / SIG_CR_FACTOR
    got_sc_inv = float(spl[1](zl_test))
    assert abs(got_sc_inv / exact_sc_inv - 1.0) < 1e-6, f"Sigma_crit mismatch: {got_sc_inv} vs {exact_sc_inv}"

    # 3. Synthetic end-to-end lensing RAR simulation & jackknife recovery
    rng = np.random.default_rng(20261126)
    # Use realistic broad n(z_s) in 6 bins
    for b in range(6):
        zc = 0.35 + 0.16 * b
        nz_bins[b] = np.exp(-0.5 * ((z_mid - zc) / 0.15) ** 2)
    spl, zg, dcg, dag = build_sigma_crit_inv_splines(z_mid, nz_bins)

    # Generate mutually isolated synthetic lenses (spaced > 0.34 deg so neighbor shear doesn't overlap)
    gx, gy = np.meshgrid(np.linspace(10.0, 27.0, 48), np.linspace(-8.5, 8.5, 48))
    ra_l = gx.ravel() + rng.uniform(-0.04, 0.04, gx.size)
    dec_l = gy.ravel() + rng.uniform(-0.04, 0.04, gy.size)
    n_lens = len(ra_l)
    z_l = rng.uniform(0.15, 0.35, n_lens)
    etg_l = rng.random(n_lens) > 0.5
    logm_l = rng.uniform(10.1, 10.9, n_lens)
    mb_l = lens_baryon_mass_msun(logm_l, etg_l, q_etg=1.0, q_ltg=1.0)
    jk_l = assign_spatial_jackknife(ra_l, dec_l, 48)
    lenses = {"ra": ra_l, "dec": dec_l, "z": z_l, "mb": mb_l, "etg": etg_l, "jk": jk_l}

    # Synthetic sources inside same patch, with multiplicative bias & true shear around every lens
    n_src = 400000
    ra_s = rng.uniform(9.5, 27.5, n_src)
    dec_s = rng.uniform(-9.0, 9.0, n_src)
    tomo_s = rng.integers(3, 7, size=n_src, dtype=np.int8)
    zb_s = np.clip(0.45 + 0.16 * (tomo_s - 3) + rng.normal(0.0, 0.08, n_src), 0.15, 1.9)
    w_s = rng.uniform(5.0, 12.0, n_src)
    e1_s = rng.normal(0.0, 0.025, n_src)
    e2_s = rng.normal(0.0, 0.025, n_src)

    # Inject exact P-OM-1 v2 tangential shear from lenses (R in 0.03..0.30 Mpc) onto sources
    tree_l = cKDTree(sph_xyz(ra_l, dec_l))
    da_l_vec = np.interp(z_l, zg, dag)
    tree_s = cKDTree(sph_xyz(ra_s, dec_s))
    pairs = tree_l.query_ball_tree(tree_s, r=math.radians(0.15))
    g_mpc = (G_SI * MSUN_KG) / (MPC_M ** 2)
    m_gold_arr = KIDS_M_GOLD[tomo_s]
    for li, slist in enumerate(pairs):
        if not slist:
            continue
        si = np.asarray(slist, np.int32)
        si = si[(zb_s[si] + 0.2) > z_l[li]]
        if not len(si):
            continue
        cosd = math.cos(math.radians(dec_l[li]))
        dra = np.radians(ra_s[si] - ra_l[li]) * cosd
        ddec = np.radians(dec_s[si] - dec_l[li])
        x_im, y_im = -dra, ddec
        r2_im = x_im * x_im + y_im * y_im
        r_mpc = np.sqrt(r2_im) * da_l_vec[li]
        mk = (r_mpc >= 0.03) & (r_mpc <= 0.30)
        if not np.any(mk):
            continue
        si, x_im, y_im, r2_im, r_mpc = si[mk], x_im[mk], y_im[mk], r2_im[mk], r_mpc[mk]
        gb = g_mpc * mb_l[li] / (r_mpc * r_mpc)
        # g_obs(H0=70) = pred(gb, A0_OBS) / H0_CONV (because estimator applies H0_CONV)
        gobs_70 = P.pred(gb, P.A0_OBS) / V2.H0_CONV
        ds_true = gobs_70 / P.ESD_TO_G  # Msun/pc^2
        sig_inv = np.array([spl[int(t)](float(z_l[li])) for t in tomo_s[si]])
        gam_t = ds_true * sig_inv * (1.0 + m_gold_arr[si])
        c2 = (x_im * x_im - y_im * y_im) / r2_im
        s2 = (2.0 * x_im * y_im) / r2_im
        e1_s[si] += -gam_t * c2
        e2_s[si] += -gam_t * s2

    acc = compute_binned_lensing(lenses, ra_s, dec_s, zb_s, e1_s, e2_s, w_s, tomo_s, spl, zg, dag,
                                 r_min_mpc=0.03, r_max_mpc=0.30, n_jk=48, tree_s=tree_s)
    res = summarize_rar_from_accumulators(acc, None, h0_conv=V2.H0_CONV, min_npair=15, label="synthetic_pom1v2")
    assert res["verdict"] == "PASS", f"Synthetic recovery did not PASS: {res['verdict']} chi2={res['chi2']}/{res['n_bins']} p={res['p']}"
    assert res["newton_p"] < 1e-6, f"Synthetic Newton rejection too weak: {res['newton_p']}"
    assert res["cross_shear_p"] > 1e-3, f"Synthetic cross-shear failed null: {res['cross_shear_p']}"

    print(f"SELF-TEST PASS: Sigma_crit exact + synthetic lensing RAR recovery PASS (chi2={res['chi2']:.2f}/{res['n_bins']}, p={res['p']:.3f}, p_Newton={res['newton_p']:.2e}, p_cross={res['cross_shear_p']:.3f}).")


# ------------------------------------------------------------------ Data Builders (Blind Run)
def build_gama_lenses(z_grid, dc_grid, r_edge_margin: float = 0.3):
    from astropy.io import fits
    with fits.open(LENS_DIR / "DistancesFramesv14.fits", memmap=True) as hd:
        df = hd[1].data
        mq = (df["NQ"] >= 3) & (df["Z_TONRY"] > 0.05) & (df["Z_TONRY"] < 0.55)
        cids = np.asarray(df["CATAID"][mq], np.int64)
        ras = np.asarray(df["RA"][mq], np.float64)
        decs = np.asarray(df["DEC"][mq], np.float64)
        zs = np.asarray(df["Z_TONRY"][mq], np.float64)
    with fits.open(LENS_DIR / "gkvGamaIIMatchesv01.fits", memmap=True) as hm:
        mt = hm[1].data
        cmt, umt = np.asarray(mt["CATAID"], np.int64), np.asarray(mt["uberID"], np.int64)
    with fits.open(LENS_DIR / "StellarMassesGKVv24.fits", memmap=True) as hs:
        sm = hs[1].data
        usm, lsm, ur_sm = np.asarray(sm["uberID"], np.int64), np.asarray(sm["logmstar"], np.float64), np.asarray(sm["uminusr"], np.float64)
    ism = np.argsort(usm)
    us = usm[ism]
    pos = np.searchsorted(us, umt)
    ok = pos < len(us)
    hit = np.zeros(len(umt), bool)
    hit[ok] = (us[pos[ok]] == umt[ok])
    c2r = {int(c): (float(lsm[p]), float(ur_sm[p])) for c, p in zip(cmt[hit], ism[pos[hit]]) if c > 0 and lsm[p] > 5.0 and np.isfinite(lsm[p])}

    rows = [(r, d, z, *c2r[int(c)]) for c, r, d, z in zip(cids, ras, decs, zs) if int(c) in c2r]
    G = np.array(rows, np.float64)  # ra, dec, z, logm, uminusr

    dc = np.interp(G[:, 2], z_grid, dc_grid)
    rr, dd = np.radians(G[:, 0]), np.radians(G[:, 1])
    pos3d = np.column_stack([dc * np.cos(dd) * np.cos(rr), dc * np.cos(dd) * np.sin(rr), dc * np.sin(dd)])
    tree3d = cKDTree(pos3d)

    # Known GAMA box rectangles
    boxes = {
        "G09": (128.5, 141.5, -2.54, 3.50),
        "G12": (173.5, 186.5, -3.52, 2.50),
        "G15": (210.93, 224.0, -2.53, 3.50),
        "G23": (338.0, 352.0, -35.50, -29.61),
    }
    in_interior = np.zeros(len(G), dtype=bool)
    reg_id = np.full(len(G), "", dtype="U4")
    for nm, (r0, r1, d0, d1) in boxes.items():
        inbox = (G[:, 0] >= r0) & (G[:, 0] <= r1) & (G[:, 1] >= d0) & (G[:, 1] <= d1)
        reg_id[inbox] = nm
        in_int = (
            (G[:, 0] >= r0 + r_edge_margin) & (G[:, 0] <= r1 - r_edge_margin)
            & (G[:, 1] >= d0 + r_edge_margin) & (G[:, 1] <= d1 - r_edge_margin)
        )
        in_interior |= in_int

    m_cand = in_interior & (G[:, 2] > 0.1) & (G[:, 2] < 0.5) & (G[:, 3] < 11.0) & (G[:, 3] > 8.5)
    cidx = np.where(m_cand)[0]
    nbrs = tree3d.query_ball_point(pos3d[cidx], r=3.0)
    iso = np.zeros(len(G), dtype=bool)
    for idx, nb in zip(cidx, nbrs):
        m_th = G[idx, 3] - 1.0
        nb_arr = np.asarray(nb, np.int32)
        if not np.any((nb_arr != idx) & (G[nb_arr, 3] > m_th)):
            iso[idx] = True

    def pack(mask):
        return {
            "ra": G[mask, 0], "dec": G[mask, 1], "z": G[mask, 2],
            "logm": G[mask, 3], "etg": G[mask, 4] > 2.00,
            "reg": reg_id[mask],
        }

    return pack(iso & (reg_id == "G23")), pack(iso), boxes


def build_dr5_new329_lenses(z_grid, dc_grid, cyl_cut: float | None = None, raw_zb: bool = False):
    from astropy.io import fits
    dr5 = np.load(LENS_DIR / "kids_dr5_bright_new341_exact.npy")
    m_phot = (dr5[:, 10] > 5.0) & (dr5[:, 4] > 10.0) & (dr5[:, 5] > 10.0) & (dr5[:, 2] < 20.5)
    e = dr5[m_phot]
    ur_e = (e[:, 4] - e[:, 6]) - (e[:, 5] - e[:, 7])
    r_auto_raw = e[:, 5] - e[:, 3]

    if raw_zb:
        z_use = np.clip(e[:, 8], 0.02, 0.65)
        logm_use = e[:, 10] + 0.4 * r_auto_raw + 0.056
    else:
        X = np.column_stack([np.ones(len(e)), e[:, 8], e[:, 8] ** 2, e[:, 9], e[:, 2] - 18.5, ur_e - 2.3, r_auto_raw])
        z_use = np.clip(X @ BETA_Z_DR5, 0.02, 0.65)
        dl_cal = np.interp(z_use, z_grid, dc_grid) * (1.0 + z_use)
        z_b_clip = np.clip(e[:, 8], 0.01, 2.0)
        dl_zb = np.interp(z_b_clip, z_grid, dc_grid) * (1.0 + z_b_clip)
        logm_use = e[:, 10] + 0.4 * r_auto_raw + 2.0 * np.log10(dl_cal / dl_zb) + DR5_GAMA_MASS_OFFSET

    # Parse 341 new tile centers and exclude 4 tiles overlapping G23 + 8 uncovered tiles (checked cleanly)
    tiles = []
    for l in open(DR5_NEW_TILES_TXT):
        if l.strip():
            _, rs, ds = l.strip().split("_")
            ra_t, dec_t = float(rs.replace("p", ".").replace("m", "-")), float(ds.replace("p", ".").replace("m", "-"))
            in_g23 = (338.0 <= ra_t <= 352.0) and (-35.5 <= dec_t <= -29.5)
            if not in_g23:
                tiles.append((ra_t, dec_t))
    tiles = np.array(tiles, np.float64)

    dc5 = np.interp(z_use, z_grid, dc_grid)
    da5 = dc5 / (1.0 + z_use)
    p5 = sph_xyz(e[:, 0], e[:, 1]) * dc5[:, None]
    t5 = cKDTree(p5)
    t5_sky = cKDTree(sph_xyz(e[:, 0], e[:, 1]))

    # Load DR4 bright neighbors for border guard
    with fits.open(LENS_DIR / "KiDS_DR4_brightsample.fits", memmap=True) as hk:
        kd = hk[1].data
        mk = (kd["MASK"] == 0) & (kd["masked"] == 0) & (kd["zphot_ANNz2"] > 0.05) & (kd["zphot_ANNz2"] < 0.55)
        ra4 = np.asarray(kd["RAJ2000"][mk], np.float64)
        dec4 = np.asarray(kd["DECJ2000"][mk], np.float64)
        z4 = np.asarray(kd["zphot_ANNz2"][mk], np.float64)
        mag4 = np.asarray(kd["MAG_AUTO_CALIB"][mk], np.float64)
    dc4 = np.interp(z4, z_grid, dc_grid)
    dl4 = dc4 * (1.0 + z4)
    Mr4 = mag4 - 5.0 * np.log10(np.maximum(dl4, 1e-3) * 1e5)
    logm4 = 10.6 - 0.4 * (Mr4 + 21.8)
    p4 = sph_xyz(ra4, dec4) * dc4[:, None]
    t4 = cKDTree(p4)

    # Check membership inside 329 non-G23 DR5 tiles (0.48 deg half-width)
    cand_in_tiles = np.zeros(len(e), dtype=bool)
    for rt, dt in tiles:
        cosd = max(math.cos(math.radians(dt)), 0.2)
        dra = ((e[:, 0] - rt + 180.0) % 360.0) - 180.0
        cand_in_tiles |= (np.abs(dra) * cosd <= 0.48) & (np.abs(e[:, 1] - dt) <= 0.48)

    m_cand = cand_in_tiles & (e[:, 2] < 20.0) & (z_use > 0.1) & (z_use < 0.5) & (logm_use < 11.0) & (logm_use > 8.5)
    cidx = np.where(m_cand)[0]
    iso = np.zeros(len(e), dtype=bool)

    if cyl_cut is None:
        nb5 = t5.query_ball_point(p5[cidx], r=3.0)
        nb4 = t4.query_ball_point(p5[cidx], r=3.0)
        for idx, a5, a4 in zip(cidx, nb5, nb4):
            mth = logm_use[idx] - 1.0
            a5_arr = np.asarray(a5, np.int32)
            bad = np.any((a5_arr != idx) & (logm_use[a5_arr] > mth))
            if not bad and a4:
                j4 = np.asarray(a4, np.int32)
                dsky = np.hypot(((ra4[j4] - e[idx, 0] + 180.0) % 360.0 - 180.0) * math.cos(math.radians(e[idx, 1])), dec4[j4] - e[idx, 1]) * 3600.0
                bad = np.any((dsky > 2.0) & (logm4[j4] > mth))
            if not bad:
                iso[idx] = True
    else:
        # Strict projected R < 3 Mpc & |dz|/(1+z) < cyl_cut sensitivity check
        r_ang = 3.0 / np.maximum(da5[cidx], 1.0)
        nb5 = t5_sky.query_ball_point(sph_xyz(e[cidx, 0], e[cidx, 1]), r=r_ang)
        for idx, a5 in zip(cidx, nb5):
            mth = logm_use[idx] - 1.0
            a5_arr = np.asarray(a5, np.int32)
            dz = np.abs(z_use[a5_arr] - z_use[idx]) / (1.0 + z_use[idx])
            if not np.any((a5_arr != idx) & (dz < cyl_cut) & (logm_use[a5_arr] > mth)):
                iso[idx] = True

    return {
        "ra": e[iso, 0], "dec": e[iso, 1], "z": z_use[iso],
        "logm": logm_use[iso], "etg": ur_e[iso] > 2.5,
    }, tiles


def run_patch_accum(
    lenses_sub: dict,
    wl_mmap: np.memmap,
    sc_splines: dict,
    z_grid: np.ndarray,
    da_grid: np.ndarray,
    patches: list,
    n_jk: int,
    r_max_mpc: float,
    rand_mult: int = 5,
    rng_seed: int = 42,
    q_etg: float = 1.0,
    q_ltg: float = 1.0,
    rand_boxes: list | None = None,
    active_tiles: np.ndarray | None = None,
):
    """Run spatially chunked lensing accumulation + matched random subtraction cleanly across patches."""
    rng = np.random.default_rng(rng_seed)
    l_ra = lenses_sub["ra"]
    l_dec = lenses_sub["dec"]
    l_z = lenses_sub["z"]
    l_mb = lens_baryon_mass_msun(lenses_sub["logm"], lenses_sub["etg"], q_etg=q_etg, q_ltg=q_ltg)
    l_etg = lenses_sub["etg"]
    l_jk = assign_spatial_jackknife(l_ra, l_dec, n_jk)

    tot_acc = {k: np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64 if k != "npair" else np.int64)
               for k in ("num_t", "num_x", "den_m", "den_w", "gb_w", "npair")}
    tot_rand = {k: np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64 if k != "npair" else np.int64)
                for k in ("num_t", "num_x", "den_m", "den_w", "gb_w", "npair")}

    for r0, r1, d0, d1 in patches:
        ml = (l_ra >= r0) & (l_ra < r1) & (l_dec >= d0) & (l_dec <= d1)
        lo_ra = (r0 - 1.5) % 360.0
        hi_ra = (r1 + 1.5) % 360.0
        if lo_ra < hi_ra:
            ms_ra = (wl_mmap["ra"] >= lo_ra) & (wl_mmap["ra"] <= hi_ra)
        else:
            ms_ra = (wl_mmap["ra"] >= lo_ra) | (wl_mmap["ra"] <= hi_ra)
        ms = ms_ra & (wl_mmap["dec"] >= d0 - 1.5) & (wl_mmap["dec"] <= d1 + 1.5) & (wl_mmap["weight"] > 0)
        n_loc = int(ml.sum())
        if n_loc == 0 or int(ms.sum()) < 100:
            continue

        s_ra = np.array(wl_mmap["ra"][ms], dtype=np.float64)
        s_dec = np.array(wl_mmap["dec"][ms], dtype=np.float64)
        s_zb = np.array(wl_mmap["z_b"][ms], dtype=np.float64)
        s_e1 = np.array(wl_mmap["e1"][ms], dtype=np.float64)
        s_e2 = np.array(wl_mmap["e2"][ms], dtype=np.float64)
        s_w = np.array(wl_mmap["weight"][ms], dtype=np.float64)
        s_tomo = np.array(wl_mmap["tomobin"][ms], dtype=np.int8)
        tree_s = cKDTree(sph_xyz(s_ra, s_dec))

        sub_l = {"ra": l_ra[ml], "dec": l_dec[ml], "z": l_z[ml], "mb": l_mb[ml], "etg": l_etg[ml], "jk": l_jk[ml]}
        a_loc = compute_binned_lensing(sub_l, s_ra, s_dec, s_zb, s_e1, s_e2, s_w, s_tomo, sc_splines, z_grid, da_grid,
                                       r_min_mpc=0.03, r_max_mpc=r_max_mpc, n_jk=n_jk, tree_s=tree_s)
        for k in tot_acc:
            tot_acc[k] += a_loc[k]

        # Generate random points following exact patch lens geometry (active tiles or GAMA boxes)
        n_r = n_loc * rand_mult
        draw_idx = rng.integers(0, n_loc, size=n_r * 2)
        if active_tiles is not None:
            tm = (active_tiles[:, 0] >= r0) & (active_tiles[:, 0] < r1) & (active_tiles[:, 1] >= d0) & (active_tiles[:, 1] <= d1)
            t_loc = active_tiles[tm]
            if len(t_loc) == 0:
                continue
            ti = rng.integers(0, len(t_loc), size=len(draw_idx))
            cosd_t = np.maximum(np.cos(np.radians(t_loc[ti, 1])), 0.2)
            cand_ra = (t_loc[ti, 0] + rng.uniform(-0.46, 0.46, len(draw_idx)) / cosd_t) % 360.0
            cand_dec = np.clip(t_loc[ti, 1] + rng.uniform(-0.46, 0.46, len(draw_idx)), -89.0, 89.0)
        elif rand_boxes is not None:
            cand_ra = np.empty(len(draw_idx), dtype=np.float64)
            cand_dec = np.empty(len(draw_idx), dtype=np.float64)
            for br0, br1, bd0, bd1 in rand_boxes:
                if br0 >= r0 - 1.0 and br1 <= r1 + 1.0:
                    cand_ra = rng.uniform(br0 + 0.3, br1 - 0.3, len(draw_idx))
                    cand_dec = rng.uniform(bd0 + 0.3, bd1 - 0.3, len(draw_idx))
                    break
        else:
            cand_ra = (sub_l["ra"][draw_idx] + rng.uniform(-0.35, 0.35, len(draw_idx)) / np.maximum(np.cos(np.radians(sub_l["dec"][draw_idx])), 0.2)) % 360.0
            cand_dec = np.clip(sub_l["dec"][draw_idx] + rng.uniform(-0.35, 0.35, len(draw_idx)), -89.0, 89.0)

        # Keep random positions inside actual KiDS-Legacy covered tiles (>= 5 sources within 0.08 deg)
        n_near = tree_s.query_ball_point(sph_xyz(cand_ra, cand_dec), r=math.radians(0.08), return_length=True)
        good_r = np.where(n_near >= 5)[0][:n_r]
        if len(good_r) > 0:
            d_keep = draw_idx[good_r]
            # Assign each random lens to the spatial jackknife cell of its nearest real lens
            _, nn_l = cKDTree(sph_xyz(sub_l["ra"], sub_l["dec"])).query(sph_xyz(cand_ra[good_r], cand_dec[good_r]))
            jk_r = sub_l["jk"][nn_l]
            sub_r = {
                "ra": cand_ra[good_r], "dec": cand_dec[good_r],
                "z": sub_l["z"][d_keep], "mb": sub_l["mb"][d_keep], "etg": sub_l["etg"][d_keep], "jk": jk_r,
            }
            r_loc = compute_binned_lensing(sub_r, s_ra, s_dec, s_zb, s_e1, s_e2, s_w, s_tomo, sc_splines, z_grid, da_grid,
                                           r_min_mpc=0.03, r_max_mpc=r_max_mpc, n_jk=n_jk, tree_s=tree_s)
            for k in tot_rand:
                tot_rand[k] += r_loc[k]

    return tot_acc, tot_rand


# ------------------------------------------------------------------ Full Blind Execution
def run_main():
    t0 = time.time()
    assert WL_BIN_PATH.exists(), f"Missing {WL_BIN_PATH}"
    assert NZ_FITS_PATH.exists(), f"Missing {NZ_FITS_PATH}"
    P.ensure_data()
    assert P.validate_model()["model_checks_pass"]

    z_mid, nz_bins = load_kids_nz()
    sc_splines, z_grid, dc_grid, da_grid = build_sigma_crit_inv_splines(z_mid, nz_bins)
    wl = np.memmap(WL_BIN_PATH, dtype=WL_DTYPE, mode="r")
    assert len(wl) == 40894394

    # 1. Sample B (GAMA G23 blind) & Extension C (GAMA All4)
    gama_g23, gama_all4, gama_boxes = build_gama_lenses(z_grid, dc_grid, r_edge_margin=0.3)

    g23_box = [gama_boxes["G23"]]
    acc_g23, rand_g23 = run_patch_accum(
        gama_g23, wl, sc_splines, z_grid, da_grid,
        patches=g23_box, n_jk=64, r_max_mpc=0.30, rand_mult=5, rng_seed=101, q_etg=1.0, q_ltg=1.0, rand_boxes=g23_box
    )
    res_g23 = summarize_rar_from_accumulators(acc_g23, rand_g23, h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_G23_reliable", q_etg=1.0, q_ltg=1.0)

    # Full GAMA All4 (both reliable 0.3 Mpc & extended 1.5 Mpc; n_jk=96 for 26 extended bins)
    all4_patches = [gama_boxes["G09"], gama_boxes["G12"], gama_boxes["G15"], gama_boxes["G23"]]
    acc_all4, rand_all4 = run_patch_accum(
        gama_all4, wl, sc_splines, z_grid, da_grid,
        patches=all4_patches, n_jk=96, r_max_mpc=1.50, rand_mult=4, rng_seed=202, q_etg=1.0, q_ltg=1.0, rand_boxes=all4_patches
    )
    acc_all4_r03, rand_all4_r03 = run_patch_accum(
        gama_all4, wl, sc_splines, z_grid, da_grid,
        patches=all4_patches, n_jk=64, r_max_mpc=0.30, rand_mult=4, rng_seed=203, q_etg=1.0, q_ltg=1.0, rand_boxes=all4_patches
    )
    res_all4_rel = summarize_rar_from_accumulators(acc_all4_r03, rand_all4_r03, h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_reliable", q_etg=1.0, q_ltg=1.0)

    ext_mask = np.zeros((2, N_GB_BINS), dtype=bool)
    ext_mask[:, 2:] = True  # log10(g_bar) >= -14.49 down into deep MOND (spectroscopic 3D isolation!)
    res_all4_ext = summarize_rar_from_accumulators(acc_all4, rand_all4, h0_conv=V2.H0_CONV, min_npair=500, use_bins=ext_mask, label="GAMA_All4_extended_1.5Mpc", q_etg=1.0, q_ltg=1.0)

    # Mass-matched GAMA All4 diagnostic (10.2 <= log M* <= 10.9)
    mm_mask = (gama_all4["logm"] >= 10.2) & (gama_all4["logm"] <= 10.9)
    gama_mm = {k: v[mm_mask] for k, v in gama_all4.items()}
    acc_mm, rand_mm = run_patch_accum(
        gama_mm, wl, sc_splines, z_grid, da_grid,
        patches=all4_patches, n_jk=64, r_max_mpc=0.30, rand_mult=4, rng_seed=204, q_etg=1.0, q_ltg=1.0, rand_boxes=all4_patches
    )
    res_all4_mm = summarize_rar_from_accumulators(acc_mm, rand_mm, h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_mass_matched", q_etg=1.0, q_ltg=1.0)

    # 2. Sample A (DR5_New329 excluding DR4 and G23)
    dr5_lenses, tiles_dr5 = build_dr5_new329_lenses(z_grid, dc_grid, cyl_cut=None, raw_zb=False)
    dr5_patches = [
        (154.0, 195.0, -5.0, 5.0),
        (195.0, 232.0, -5.0, 5.0),
        (325.0, 360.0, -37.0, -25.0),
        (0.0, 60.0, -37.0, -25.0),
    ]
    acc_dr5, rand_dr5 = run_patch_accum(
        dr5_lenses, wl, sc_splines, z_grid, da_grid,
        patches=dr5_patches, n_jk=64, r_max_mpc=0.30, rand_mult=3, rng_seed=301,
        q_etg=1.0, q_ltg=1.0, active_tiles=tiles_dr5
    )
    res_dr5 = summarize_rar_from_accumulators(acc_dr5, rand_dr5, h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_zcal_Q1", q_etg=1.0, q_ltg=1.0)

    # Sensitivity S1 on DR5_New329: Mistele Q_ETG=1.4, raw DR5 Z_B + Q_ETG=1.4, and strict cylinder isolation |dz|/(1+z)<0.02
    acc_dr5_q14, rand_dr5_q14 = run_patch_accum(
        dr5_lenses, wl, sc_splines, z_grid, da_grid,
        patches=dr5_patches, n_jk=64, r_max_mpc=0.30, rand_mult=2, rng_seed=302,
        q_etg=1.4, q_ltg=1.0, active_tiles=tiles_dr5
    )
    res_dr5_q14 = summarize_rar_from_accumulators(acc_dr5_q14, rand_dr5_q14, h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_zcal_QETG1.4", q_etg=1.4, q_ltg=1.0)

    dr5_raw, _ = build_dr5_new329_lenses(z_grid, dc_grid, cyl_cut=None, raw_zb=True)
    acc_dr5_raw, rand_dr5_raw = run_patch_accum(
        dr5_raw, wl, sc_splines, z_grid, da_grid,
        patches=dr5_patches, n_jk=64, r_max_mpc=0.30, rand_mult=2, rng_seed=303,
        q_etg=1.4, q_ltg=1.0, active_tiles=tiles_dr5
    )
    res_dr5_raw = summarize_rar_from_accumulators(acc_dr5_raw, rand_dr5_raw, h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_rawZB_QETG1.4", q_etg=1.4, q_ltg=1.0)

    dr5_cyl, _ = build_dr5_new329_lenses(z_grid, dc_grid, cyl_cut=0.02, raw_zb=False)
    acc_dr5_cyl, rand_dr5_cyl = run_patch_accum(
        dr5_cyl, wl, sc_splines, z_grid, da_grid,
        patches=dr5_patches, n_jk=64, r_max_mpc=0.30, rand_mult=2, rng_seed=304,
        q_etg=1.0, q_ltg=1.0, active_tiles=tiles_dr5
    )
    res_dr5_cyl = summarize_rar_from_accumulators(acc_dr5_cyl, rand_dr5_cyl, h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_cyl_dz0.02", q_etg=1.0, q_ltg=1.0)

    # Sensitivity S2: No H0=73 conversion (H0=70) & v1 masses (no hot gas, Q=1) on DR5 & G23
    res_dr5_noH0 = summarize_rar_from_accumulators(acc_dr5, rand_dr5, h0_conv=1.0, min_npair=200, label="DR5_New329_noH0_conv", q_etg=1.0, q_ltg=1.0)
    res_g23_noH0 = summarize_rar_from_accumulators(acc_g23, rand_g23, h0_conv=1.0, min_npair=200, label="GAMA_G23_noH0_conv", q_etg=1.0, q_ltg=1.0)

    # Primary Headline Combined Blind Statistic: Disjoint DR5_New329 + GAMA_G23
    comb_chi2 = res_dr5["chi2"] + res_g23["chi2"]
    comb_dof = res_dr5["n_bins"] + res_g23["n_bins"]
    comb_p = float(chi2_dist.sf(comb_chi2, comb_dof))
    comb_newt_chi2 = res_dr5["newton_chi2"] + res_g23["newton_chi2"]
    comb_newt_p = float(chi2_dist.sf(comb_newt_chi2, comb_dof))

    deltas = np.linspace(-P.MSTAR_SYS_DEX, P.MSTAR_SYS_DEX, 401)
    comb_shifts = []
    for dl in deltas:
        r1 = res_dr5["_d"] - P.pred(res_dr5["_gb"] * (10.0 ** dl), P.A0_OBS)
        r2 = res_g23["_d"] - P.pred(res_g23["_gb"] * (10.0 ** dl), P.A0_OBS)
        c_dl = float(r1 @ np.linalg.solve(res_dr5["_C"], r1)) + float(r2 @ np.linalg.solve(res_g23["_C"], r2))
        comb_shifts.append(c_dl)
    k_c = int(np.argmin(comb_shifts))
    comb_mshift_best, comb_mshift_chi2 = float(deltas[k_c]), float(comb_shifts[k_c])
    comb_mshift_p = float(chi2_dist.sf(comb_mshift_chi2, comb_dof - 1))

    if comb_newt_p >= 1e-6:
        comb_verdict = "NO_POWER"
    elif comb_p >= 0.01:
        comb_verdict = "PASS"
    elif comb_mshift_p >= 0.01:
        comb_verdict = "PASS_WITHIN_MASS_SYSTEMATIC"
    else:
        comb_verdict = "FAIL"

    prereg_sha = hashlib.sha256((HERE / "PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md").read_bytes()).hexdigest()

    def _clean(d):
        return {k: v for k, v in d.items() if not k.startswith("_")}

    out = {
        "status": "completed",
        "protocol": "03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md",
        "protocol_sha256": prereg_sha,
        "epistemic_tag": "[D]",
        "euclid_tap_audit": "Zero she_* tables in public ESA Euclid Q1/DR1 TAP (2026-11-26); KiDS-Legacy DR5 run executed.",
        "sample_sizes": {
            "DR5_New329_isolated_total": int(len(dr5_lenses["ra"])),
            "DR5_New329_isolated_LTG": int((~dr5_lenses["etg"]).sum()),
            "DR5_New329_isolated_ETG": int(dr5_lenses["etg"].sum()),
            "GAMA_G23_isolated_total": int(len(gama_g23["ra"])),
            "GAMA_G23_isolated_LTG": int((~gama_g23["etg"]).sum()),
            "GAMA_G23_isolated_ETG": int(gama_g23["etg"].sum()),
            "GAMA_All4_isolated_total": int(len(gama_all4["ra"])),
        },
        "headline_blind_combined": {
            "components": ["DR5_New329_zcal_Q1", "GAMA_G23_reliable"],
            "verdict": comb_verdict,
            "chi2": comb_chi2,
            "dof": int(comb_dof),
            "p": comb_p,
            "newton_chi2": comb_newt_chi2,
            "newton_p": comb_newt_p,
            "mass_shift_best_dex": comb_mshift_best,
            "mass_shift_chi2": comb_mshift_chi2,
            "mass_shift_p": comb_mshift_p,
        },
        "DR5_New329_primary": _clean(res_dr5),
        "GAMA_G23_primary": _clean(res_g23),
        "GAMA_All4_reliable": _clean(res_all4_rel),
        "GAMA_All4_extended_1.5Mpc": _clean(res_all4_ext),
        "diagnostics": {
            "GAMA_All4_mass_matched": _clean(res_all4_mm),
            "DR5_New329_zcal_QETG1.4": _clean(res_dr5_q14),
            "DR5_New329_rawZB_QETG1.4": _clean(res_dr5_raw),
            "DR5_New329_cyl_dz0.02": _clean(res_dr5_cyl),
            "DR5_New329_noH0_conv": _clean(res_dr5_noH0),
            "GAMA_G23_noH0_conv": _clean(res_g23_noH0),
        },
        "run_seconds": round(time.time() - t0, 2),
    }

    (HERE / "POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json").write_text(json.dumps(out, indent=2) + "\n")
    (HERE / "POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md").write_text(_format_md(out))
    print(json.dumps({
        "headline_verdict": comb_verdict,
        "comb_chi2": f"{comb_chi2:.2f}/{comb_dof} (p={comb_p:.3g})",
        "DR5_New329": f"{res_dr5['verdict']} chi2={res_dr5['chi2']:.2f}/{res_dr5['n_bins']} p={res_dr5['p']:.3g}",
        "GAMA_G23": f"{res_g23['verdict']} chi2={res_g23['chi2']:.2f}/{res_g23['n_bins']} p={res_g23['p']:.3g}",
        "GAMA_All4_rel": f"{res_all4_rel['verdict']} chi2={res_all4_rel['chi2']:.2f}/{res_all4_rel['n_bins']} p={res_all4_rel['p']:.3g}",
        "GAMA_All4_ext": f"{res_all4_ext['verdict']} chi2={res_all4_ext['chi2']:.2f}/{res_all4_ext['n_bins']} p={res_all4_ext['p']:.3g}",
    }, indent=2))


def _format_md(out) -> str:
    h = out["headline_blind_combined"]
    s = out["sample_sizes"]
    lines = [
        "# P-OM-1 v2 Blind Run on KiDS-Legacy (DR5) & GAMA DR4 (2026-11-26)",
        "",
        f"**Protocol:** `03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md` (SHA-256: `{out['protocol_sha256']}`)",
        "**Script:** `03_observer_jwst/pom1v2_blind_kids_legacy.py` -> `POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json`",
        "**Epistemic Tag:** `[D]` computed blind weak-lensing outcome (KiDS-Legacy 40,894,394 sources; Euclid Q1/DR1 TAP exposes zero `she_*` tables)",
        "",
        "## 1. Headline Blind Combined Verdict (Strictly Disjoint Sky: `DR5_New329` + `GAMA_G23`)",
        "",
        f"- **Headline Blind Verdict:** **`{h['verdict']}`**",
        f"- **Combined $\\chi^2 / \\mathrm{{dof}}$:** `{h['chi2']:.2f} / {h['dof']}` (`p = {h['p']:.3g}`)",
        f"- **Newtonian Point-Mass Rejection:** $\\chi^2 = {h['newton_chi2']:.1f} / {h['dof']}$ (`p = {h['newton_p']:.2e}`)",
        f"- **Within $\\pm 0.2\\,\\mathrm{{dex}}$ mass shift:** $\\delta = {h['mass_shift_best_dex']:+.3f}\\,\\mathrm{{dex}}$, $\\chi^2 = {h['mass_shift_chi2']:.2f} / {h['dof']-1}$ (`p = {h['mass_shift_p']:.3g}`)",
        "",
        "## 2. Sample Summary (`g_bar > 7.56e-14` Reliable & Extended 1.5 Mpc)",
        "",
        "| Sample | Isolated Lenses | chi2 / dof | p | LTG (med obs/pred) | ETG (med obs/pred) | ETG-LTG p | Cross-shear p | Verdict |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for key, n_l in (
        ("DR5_New329_primary", s["DR5_New329_isolated_total"]),
        ("GAMA_G23_primary", s["GAMA_G23_isolated_total"]),
        ("GAMA_All4_reliable", s["GAMA_All4_isolated_total"]),
        ("GAMA_All4_extended_1.5Mpc", s["GAMA_All4_isolated_total"]),
    ):
        r = out[key]
        ltg = r["per_type"].get("late", {})
        etg = r["per_type"].get("early", {})
        eml_p = r["early_minus_late"]["p"] if r["early_minus_late"] else float("nan")
        lines.append(
            f"| `{key}` | {n_l:,d} | {r['chi2']:.2f} / {r['n_bins']} | {r['p']:.3g} | "
            f"{ltg.get('chi2',0):.1f}/{ltg.get('n_bins',0)} ({ltg.get('median_obs_over_pred',0):.2f}) | "
            f"{etg.get('chi2',0):.1f}/{etg.get('n_bins',0)} ({etg.get('median_obs_over_pred',0):.2f}) | "
            f"{eml_p:.3g} | {r['cross_shear_p']:.3g} | **`{r['verdict']}`** |"
        )
    lines.extend(["", "## 3. Systematic & Diagnostic Matrix", "", "| Variant | chi2 / dof | p | Mass shift | Early-Late p | Verdict |", "|---|---|---|---|---|---|"])
    for nm, r in out["diagnostics"].items():
        eml_p = r["early_minus_late"]["p"] if r["early_minus_late"] else float("nan")
        lines.append(
            f"| `{nm}` | {r['chi2']:.2f} / {r['n_bins']} | {r['p']:.3g} | {r['mass_shift_best_dex']:+.3f} (p={r['mass_shift_p']:.3g}) | {eml_p:.3g} | `{r['verdict']}` |"
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
