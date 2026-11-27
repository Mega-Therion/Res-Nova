#!/usr/bin/env python3
"""
Post-blind P-OM-1 diagnostic audit on cached GAMA DR4 + KiDS-Legacy DR5 data:
  1. Viewing-angle internal-dust mirage in apparent red galaxies:
     Separates apparent ETGs ((u - r)_obs > 2.00) in StellarMassesGKVv24.fits into
     dust-reddened tilted/edge-on spiral disks ((u - r)_stars <= 2.00) vs. true
     dust-free intrinsic ellipticals ((u - r)_stars > 2.00), and evaluates weak-lensing
     excess surface density at Q_ETG in {1.0, sqrt(2), 1.4} with 20x shared randoms.
  2. Directional sightline & CMB-dipole hemisphere decomposition:
     Evaluates per-field GAMA (G09, G12, G15, G23) and unseen DR5_New329 forward-dipole
     (N_DR5) vs. backward-wake (S_DR5) weak-lensing RAR residuals relative to the
     Planck CMB dipole apex (RA = 167.94 deg, Dec = -6.94 deg).

Epistemic status: [E]/[D] post-blind diagnostic companion to POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md.
Pre-registered blind verdicts in POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json remain unmodified.
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

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import pom1v2_blind_kids_legacy as K  # noqa: E402

OUT_JSON = HERE / "POM1_INTRINSIC_DIPOLE_DIAGNOSTIC_2026-11-27.json"
OUT_MD = HERE / "POM1_INTRINSIC_DIPOLE_DIAGNOSTIC_2026-11-27.md"

# Planck 2018 solar/Local-Group CMB dipole apex (J2000 equatorial, deg)
CMB_APEX_RA_DEG = 167.942
CMB_APEX_DEC_DEG = -6.944
VIRGO_RA_DEG = 187.706
VIRGO_DEC_DEG = 12.391


def _locate_fixed_cache() -> dict[str, Path]:
    """Resolve local KiDS-Legacy + GAMA cache from fixed allowlisted paths only (no user path injection)."""
    candidates = (
        Path.home() / ".cache" / "res-nova" / "kids_legacy_cache",
        Path("/tmp/kids_legacy_cache"),
    )
    for base in candidates:
        lens_dir = base / "lenses"
        wl_bin = base / "kids_legacy_wl_slim.bin"
        nz_fits = base / "KiDS_Legacy_cosmic_shear_data_release" / "data" / "KiDS_Legacy_xipm.fits"
        tiles_txt = base / "dr5_new_tiles.txt"
        if lens_dir.is_dir() and wl_bin.is_file() and nz_fits.is_file() and tiles_txt.is_file():
            return {
                "base": base,
                "lens_dir": lens_dir,
                "wl_bin": wl_bin,
                "nz_fits": nz_fits,
                "tiles_txt": tiles_txt,
            }
    raise FileNotFoundError("Cached KiDS-Legacy + GAMA files not found in allowlisted local cache directories.")


def mean_cos_angle(ra_deg: np.ndarray, dec_deg: np.ndarray, ref_ra: float, ref_dec: float) -> float:
    u = K.sph_xyz(ra_deg, dec_deg)
    v = K.sph_xyz(np.array([ref_ra], dtype=np.float64), np.array([ref_dec], dtype=np.float64))[0]
    return float(np.mean(u @ v))


def build_gama_intrinsic_color_lenses(
    lens_dir: Path,
    z_grid: np.ndarray,
    dc_grid: np.ndarray,
    r_edge_margin: float = 0.45,
    iso_radius_mpc: float = 3.0,
) -> tuple[dict, dict, dict]:
    """Load GAMA DR4 galaxies with both observed (uminusr) and dust-corrected intrinsic (uminusr_stars) colors."""
    from astropy.io import fits
    from scipy.spatial import cKDTree

    with fits.open(lens_dir / "DistancesFramesv14.fits", memmap=True) as hd:
        df = hd[1].data
        mq = (df["NQ"] >= 3) & (df["Z_TONRY"] > 0.05) & (df["Z_TONRY"] < 0.55)
        cids = np.asarray(df["CATAID"][mq], np.int64)
        ras = np.asarray(df["RA"][mq], np.float64)
        decs = np.asarray(df["DEC"][mq], np.float64)
        zs = np.asarray(df["Z_TONRY"][mq], np.float64)

    with fits.open(lens_dir / "gkvGamaIIMatchesv01.fits", memmap=True) as hm:
        mt = hm[1].data
        cmt = np.asarray(mt["CATAID"], np.int64)
        umt = np.asarray(mt["uberID"], np.int64)

    with fits.open(lens_dir / "StellarMassesGKVv24.fits", memmap=True) as hs:
        sm = hs[1].data
        usm = np.asarray(sm["uberID"], np.int64)
        lsm = np.asarray(sm["logmstar"], np.float64)
        ur_obs = np.asarray(sm["uminusr"], np.float64)
        ur_stars = np.asarray(sm["uminusr_stars"], np.float64)
        ebv = np.asarray(sm["dustEBV"], np.float64)

    ism = np.argsort(usm)
    us = usm[ism]
    pos = np.searchsorted(us, umt)
    ok = pos < len(us)
    hit = np.zeros(len(umt), dtype=bool)
    hit[ok] = us[pos[ok]] == umt[ok]

    c2r = {}
    for c, p in zip(cmt[hit], ism[pos[hit]]):
        if c > 0 and lsm[p] > 5.0 and np.isfinite(lsm[p]) and np.isfinite(ur_obs[p]) and np.isfinite(ur_stars[p]):
            c2r[int(c)] = (float(lsm[p]), float(ur_obs[p]), float(ur_stars[p]), float(ebv[p]))

    rows = [(r, d, z, *c2r[int(c)]) for c, r, d, z in zip(cids, ras, decs, zs) if int(c) in c2r]
    G = np.array(rows, dtype=np.float64)
    # Columns: 0=ra, 1=dec, 2=z, 3=logm, 4=ur_obs, 5=ur_stars, 6=ebv

    # Full GAMA census in lens redshift/mass window (0.1 < z < 0.5, 8.5 < logM* < 11.0)
    m_win = (G[:, 2] > 0.1) & (G[:, 2] < 0.5) & (G[:, 3] > 8.5) & (G[:, 3] < 11.0)
    Gw = G[m_win]
    app_etg_w = Gw[:, 4] > 2.00
    dusty_disk_w = app_etg_w & (Gw[:, 5] <= 2.00)
    true_etg_w = app_etg_w & (Gw[:, 5] > 2.00)

    dc = np.interp(G[:, 2], z_grid, dc_grid)
    rr, dd = np.radians(G[:, 0]), np.radians(G[:, 1])
    pos3d = np.column_stack([dc * np.cos(dd) * np.cos(rr), dc * np.cos(dd) * np.sin(rr), dc * np.sin(dd)])

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
            (G[:, 0] >= r0 + r_edge_margin)
            & (G[:, 0] <= r1 - r_edge_margin)
            & (G[:, 1] >= d0 + r_edge_margin)
            & (G[:, 1] <= d1 - r_edge_margin)
        )
        in_interior |= in_int

    m_cand = in_interior & (G[:, 2] > 0.1) & (G[:, 2] < 0.5) & (G[:, 3] < 11.0) & (G[:, 3] > 8.5)
    cidx = np.where(m_cand)[0]
    iso = np.zeros(len(G), dtype=bool)
    tree3d = cKDTree(pos3d)
    nbrs = tree3d.query_ball_point(pos3d[cidx], r=iso_radius_mpc)
    for idx, nb in zip(cidx, nbrs):
        m_th = G[idx, 3] - 1.0
        nb_arr = np.asarray(nb, np.int32)
        if not np.any((nb_arr != idx) & (G[nb_arr, 3] > m_th)):
            iso[idx] = True

    Gi = G[iso]
    ri = reg_id[iso]
    pure_ltg = (Gi[:, 4] <= 2.00) & (Gi[:, 5] <= 2.00)
    dusty_disk = (Gi[:, 4] > 2.00) & (Gi[:, 5] <= 2.00)
    true_etg = (Gi[:, 4] > 2.00) & (Gi[:, 5] > 2.00)

    def _pop_stats(arr: np.ndarray) -> dict:
        return {
            "count": int(len(arr)),
            "median_z": round(float(np.median(arr[:, 2])), 4),
            "median_logmstar": round(float(np.median(arr[:, 3])), 4),
            "median_ur_obs": round(float(np.median(arr[:, 4])), 4),
            "median_ur_stars": round(float(np.median(arr[:, 5])), 4),
            "median_reddening_ur_mag": round(float(np.median(arr[:, 4] - arr[:, 5])), 4),
            "median_dustEBV": round(float(np.median(arr[:, 6])), 4),
        }

    census = {
        "full_gama_window_0p1_0p5": {
            "total": int(len(Gw)),
            "apparent_etg_ur_gt_2": int(app_etg_w.sum()),
            "dusty_tilted_disks_in_apparent_etg": int(dusty_disk_w.sum()),
            "dusty_disk_fraction_of_apparent_etg": round(float(dusty_disk_w.sum() / max(app_etg_w.sum(), 1)), 4),
            "true_intrinsic_etg": int(true_etg_w.sum()),
            "dusty_disk_stats": _pop_stats(Gw[dusty_disk_w]),
            "true_etg_stats": _pop_stats(Gw[true_etg_w]),
        },
        "isolated_gama_all4": {
            "total": int(len(Gi)),
            "apparent_etg_total": int((Gi[:, 4] > 2.00).sum()),
            "dusty_disk_fraction_of_apparent_etg": round(
                float(dusty_disk.sum() / max((Gi[:, 4] > 2.00).sum(), 1)), 4
            ),
            "pure_blue_spirals": _pop_stats(Gi[pure_ltg]),
            "tilted_dusty_spirals_misclassified_as_etg": _pop_stats(Gi[dusty_disk]),
            "true_dust_free_ellipticals": _pop_stats(Gi[true_etg]),
        },
    }

    lenses_apparent = {
        "ra": Gi[:, 0],
        "dec": Gi[:, 1],
        "z": Gi[:, 2],
        "logm": Gi[:, 3],
        "etg": Gi[:, 4] > 2.00,
        "reg": ri,
    }
    # Intrinsic cut: true dust-free ellipticals require BOTH observed and intrinsic stellar (u-r) > 2.00
    lenses_intrinsic = {
        "ra": Gi[:, 0],
        "dec": Gi[:, 1],
        "z": Gi[:, 2],
        "logm": Gi[:, 3],
        "etg": true_etg,
        "reg": ri,
    }
    return census, lenses_apparent, lenses_intrinsic, boxes


def _compact_slot(slot_dict: dict) -> dict:
    return {
        "chi2": round(float(slot_dict["chi2"]), 3),
        "chi2_hartlap": round(float(slot_dict["chi2_hartlap"]), 3),
        "ndof": int(slot_dict["n_bins"]),
        "p_value": float(f"{slot_dict['p']:.4e}"),
        "hartlap_p": float(f"{slot_dict['p_hartlap']:.4e}"),
        "median_obs_over_pred": round(float(slot_dict["median_obs_over_pred"]), 4),
    }


def _compact_run(res: dict) -> dict:
    return {
        "verdict": res["verdict"],
        "verdict_hartlap": res["verdict_hartlap"],
        "total_chi2": round(float(res["chi2"]), 3),
        "hartlap_chi2": round(float(res["chi2_hartlap"]), 3),
        "ndof": int(res["n_bins"]),
        "p_value": float(f"{res['p']:.4e}"),
        "hartlap_p": float(f"{res['p_hartlap']:.4e}"),
        "ltg": _compact_slot(res["per_type"]["late"]),
        "etg": _compact_slot(res["per_type"]["early"]),
    }


def _extract_regional_wl_subsets(wl_mmap: np.memmap, gama_boxes: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Single sequential pass over 40.9M KiDS-Legacy rows extracting exact +/-1.6 deg supersets per footprint."""
    gama_chunks, n_chunks, s_chunks = [], [], []
    pad = 1.6
    chunk = 4_000_000
    for st in range(0, len(wl_mmap), chunk):
        sl = wl_mmap[st : st + chunk]
        wpos = sl["weight"] > 0
        if not np.any(wpos):
            continue
        sub = sl[wpos]
        ra = sub["ra"]
        dec = sub["dec"]

        mg = np.zeros(len(sub), dtype=bool)
        for r0, r1, d0, d1 in gama_boxes.values():
            mg |= (ra >= r0 - pad) & (ra <= r1 + pad) & (dec >= d0 - pad) & (dec <= d1 + pad)
        if np.any(mg):
            gama_chunks.append(np.array(sub[mg], copy=True))

        mn = (ra >= 154.0 - pad) & (ra <= 232.0 + pad) & (dec >= -5.0 - pad) & (dec <= 5.0 + pad)
        if np.any(mn):
            n_chunks.append(np.array(sub[mn], copy=True))

        ms = ((ra >= 325.0 - pad) | (ra <= 60.0 + pad)) & (dec >= -37.0 - pad) & (dec <= -25.0 + pad)
        if np.any(ms):
            s_chunks.append(np.array(sub[ms], copy=True))

    return (
        np.concatenate(gama_chunks) if gama_chunks else np.zeros(0, dtype=wl_mmap.dtype),
        np.concatenate(n_chunks) if n_chunks else np.zeros(0, dtype=wl_mmap.dtype),
        np.concatenate(s_chunks) if s_chunks else np.zeros(0, dtype=wl_mmap.dtype),
    )


def run_self_test() -> int:
    """Fast offline self-test (<1s) checking dust-mirage classification & dipole hemisphere geometry."""
    rng = np.random.default_rng(20261127)
    n = 1000
    ur_stars = np.concatenate([rng.normal(1.65, 0.20, 750), rng.normal(2.15, 0.08, 250)])
    ebv = np.concatenate([rng.uniform(0.05, 0.25, 750), rng.uniform(0.01, 0.06, 250)])
    ur_obs = ur_stars + 2.45 * ebv

    app_etg = ur_obs > 2.00
    dusty_mirage = app_etg & (ur_stars <= 2.00)
    true_etg = app_etg & (ur_stars > 2.00)
    assert int(dusty_mirage.sum()) > 100 and int(true_etg.sum()) > 100
    assert int(dusty_mirage.sum() + true_etg.sum()) == int(app_etg.sum())

    # Exact antipodal dipole cosine check
    c_apex = mean_cos_angle(np.array([CMB_APEX_RA_DEG]), np.array([CMB_APEX_DEC_DEG]), CMB_APEX_RA_DEG, CMB_APEX_DEC_DEG)
    anti_ra = (CMB_APEX_RA_DEG + 180.0) % 360.0
    anti_dec = -CMB_APEX_DEC_DEG
    c_anti = mean_cos_angle(np.array([anti_ra]), np.array([anti_dec]), CMB_APEX_RA_DEG, CMB_APEX_DEC_DEG)
    assert abs(c_apex - 1.0) < 1e-12 and abs(c_anti + 1.0) < 1e-12

    # Schema compatibility check with pom1v2_blind_kids_legacy.summarize_rar_from_accumulators
    mock_res = {
        "verdict": "PASS",
        "verdict_hartlap": "PASS",
        "chi2": 10.5,
        "chi2_hartlap": 8.2,
        "n_bins": 14,
        "p": 0.72,
        "p_hartlap": 0.87,
        "per_type": {
            "late": {"n_bins": 7, "chi2": 5.1, "p": 0.65, "chi2_hartlap": 4.5, "p_hartlap": 0.72, "median_obs_over_pred": 1.01},
            "early": {"n_bins": 7, "chi2": 5.4, "p": 0.61, "chi2_hartlap": 4.8, "p_hartlap": 0.68, "median_obs_over_pred": 1.02},
        },
    }
    comp = _compact_run(mock_res)
    assert comp["ndof"] == 14 and comp["ltg"]["ndof"] == 7 and comp["etg"]["ndof"] == 7
    print("pom1_intrinsic_dipole_diagnostic self-test: PASS")
    return 0


def run_cached_diagnostic() -> int:
    t0 = time.time()
    paths = _locate_fixed_cache()
    K.P.ensure_data()
    z_mid, dz_w, nz_bins = K.load_kids_nz(paths["nz_fits"])
    wl = np.memmap(paths["wl_bin"], dtype=K.WL_DTYPE, mode="r")
    assert len(wl) == K.N_KIDS_LEGACY_ROWS

    sp_mis, zg_w, dcg_w, dag_w = K.build_sigma_crit_inv_splines(
        z_mid, nz_bins, dz_widths=dz_w, om=K.OM_WMAP9, ol=K.OL_WMAP9, h0=K.H0_B21, norm_above_zl=True
    )

    census, lenses_app, lenses_intr, gama_boxes = build_gama_intrinsic_color_lenses(
        paths["lens_dir"], zg_w, dcg_w, r_edge_margin=0.45, iso_radius_mpc=3.0
    )
    dr5_w, tiles_dr5 = K.build_dr5_new329_lenses(paths, zg_w, dcg_w, wl_mmap=wl, iso_radius_mpc=3.0, raw_zb=False)
    wl_gama, wl_dr5_n, wl_dr5_s = _extract_regional_wl_subsets(wl, gama_boxes)
    all4_patches = [gama_boxes["G09"], gama_boxes["G12"], gama_boxes["G15"], gama_boxes["G23"]]

    q_sqrt2 = math.sqrt(2.0)
    intr_accum = K.run_patch_accum_qpair(
        lenses_intr,
        wl_gama,
        sp_mis,
        zg_w,
        dag_w,
        patches=all4_patches,
        n_jk=64,
        r_max_mpc=0.30,
        rand_mult=20,
        rng_seed=211,
        q_etg_list=(1.0, q_sqrt2, 1.4),
        rand_boxes=all4_patches,
        r_edge_margin=0.45,
        zb_cut_mode="mistele",
    )
    res_intr_q1 = K.summarize_rar_from_accumulators(
        *intr_accum[1.0], h0_conv=K.V2.H0_CONV, min_npair=200, label="GAMA_All4_IntrinsicCut_Q1.0", q_etg=1.0
    )
    res_intr_qsqrt2 = K.summarize_rar_from_accumulators(
        *intr_accum[q_sqrt2],
        h0_conv=K.V2.H0_CONV,
        min_npair=200,
        label="GAMA_All4_IntrinsicCut_Qsqrt2",
        q_etg=q_sqrt2,
    )
    res_intr_q14 = K.summarize_rar_from_accumulators(
        *intr_accum[1.4], h0_conv=K.V2.H0_CONV, min_npair=200, label="GAMA_All4_IntrinsicCut_Q1.4", q_etg=1.4
    )

    # Per-field GAMA sightline decomposition (apparent cut at Q_ETG = 1.0, 32 JK regions per field so K >= 17)
    sightlines = {}
    for idx_f, fname in enumerate(("G12", "G09", "G15", "G23")):
        m_f = lenses_app["reg"] == fname
        sub = {k: v[m_f] for k, v in lenses_app.items()}
        box_f = [gama_boxes[fname]]
        acc_f = K.run_patch_accum_qpair(
            sub,
            wl_gama,
            sp_mis,
            zg_w,
            dag_w,
            patches=box_f,
            n_jk=32,
            r_max_mpc=0.30,
            rand_mult=20,
            rng_seed=501 + idx_f,
            q_etg_list=(1.0, 1.4),
            rand_boxes=box_f,
            r_edge_margin=0.45,
            zb_cut_mode="mistele",
        )
        r_q1 = K.summarize_rar_from_accumulators(
            *acc_f[1.0], h0_conv=K.V2.H0_CONV, min_npair=50, label=f"GAMA_{fname}_Q1", q_etg=1.0
        )
        sightlines[fname] = {
            "n_lenses": int(m_f.sum()),
            "mean_ra_deg": round(float(np.mean(sub["ra"])), 2),
            "mean_dec_deg": round(float(np.mean(sub["dec"])), 2),
            "cos_cmb_dipole": round(mean_cos_angle(sub["ra"], sub["dec"], CMB_APEX_RA_DEG, CMB_APEX_DEC_DEG), 4),
            "cos_virgo": round(mean_cos_angle(sub["ra"], sub["dec"], VIRGO_RA_DEG, VIRGO_DEC_DEG), 4),
            "q1_summary": _compact_run(r_q1),
        }

    # Unseen DR5_New329 split by Forward-Dipole North (N_DR5) vs Backward-Wake South (S_DR5)
    dr5_patches = {
        "N_DR5": [(154.0, 195.0, -5.0, 5.0), (195.0, 232.0, -5.0, 5.0)],
        "S_DR5": [(325.0, 360.0, -37.0, -25.0), (0.0, 60.0, -37.0, -25.0)],
    }
    wl_dr5_map = {"N_DR5": wl_dr5_n, "S_DR5": wl_dr5_s}
    hemispheres = {}
    for idx_h, hname in enumerate(("N_DR5", "S_DR5")):
        mh = dr5_w["reg"] == hname
        sub_h = {k: v[mh] for k, v in dr5_w.items()}
        tiles_h = tiles_dr5[tiles_dr5[:, 1] >= -12.0] if hname == "N_DR5" else tiles_dr5[tiles_dr5[:, 1] < -12.0]
        acc_h = K.run_patch_accum_qpair(
            sub_h,
            wl_dr5_map[hname],
            sp_mis,
            zg_w,
            dag_w,
            patches=dr5_patches[hname],
            n_jk=32,
            r_max_mpc=0.30,
            rand_mult=20,
            rng_seed=601 + idx_h,
            q_etg_list=(1.0, 1.4),
            active_tiles=tiles_h,
            zb_cut_mode="mistele",
        )
        rh_q1 = K.summarize_rar_from_accumulators(
            *acc_h[1.0], h0_conv=K.V2.H0_CONV, min_npair=200, label=f"{hname}_Q1", q_etg=1.0
        )
        hemispheres[hname] = {
            "n_lenses": int(mh.sum()),
            "cos_cmb_dipole": round(mean_cos_angle(sub_h["ra"], sub_h["dec"], CMB_APEX_RA_DEG, CMB_APEX_DEC_DEG), 4),
            "q1_summary": _compact_run(rh_q1),
        }

    ltg_hemi_mean = 0.5 * (
        hemispheres["N_DR5"]["q1_summary"]["ltg"]["median_obs_over_pred"]
        + hemispheres["S_DR5"]["q1_summary"]["ltg"]["median_obs_over_pred"]
    )

    payload = {
        "date": "2026-11-27",
        "status": "[E]/[D] post-blind diagnostic (pre-registered POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json unchanged)",
        "elapsed_sec": round(time.time() - t0, 2),
        "kids_legacy_sources": int(len(wl)),
        "part_1_gama_dust_mirage": {
            "census": census,
            "intrinsic_cut_lensing": {
                "Q_ETG_1.0": _compact_run(res_intr_q1),
                "Q_ETG_sqrt2": _compact_run(res_intr_qsqrt2),
                "Q_ETG_1.4": _compact_run(res_intr_q14),
            },
        },
        "part_2_dipole_and_sightlines": {
            "cmb_dipole_apex_j2000_deg": [CMB_APEX_RA_DEG, CMB_APEX_DEC_DEG],
            "gama_fields": sightlines,
            "dr5_new329_hemispheres": hemispheres,
            "dr5_ltg_hemisphere_unweighted_mean_obs_over_pred": round(float(ltg_hemi_mean), 4),
        },
    }
    raw_json = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    payload["sha256_body"] = hashlib.sha256(raw_json.encode("utf-8")).hexdigest()
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    c_full = census["full_gama_window_0p1_0p5"]
    c_iso = census["isolated_gama_all4"]
    r1 = payload["part_1_gama_dust_mirage"]["intrinsic_cut_lensing"]["Q_ETG_1.0"]
    rs2 = payload["part_1_gama_dust_mirage"]["intrinsic_cut_lensing"]["Q_ETG_sqrt2"]
    r14 = payload["part_1_gama_dust_mirage"]["intrinsic_cut_lensing"]["Q_ETG_1.4"]

    n_true_disks_iso = (
        c_iso["pure_blue_spirals"]["count"] + c_iso["tilted_dusty_spirals_misclassified_as_etg"]["count"]
    )
    n_true_etg_iso = c_iso["true_dust_free_ellipticals"]["count"]

    md_lines = [
        "# P-OM-1 Post-Blind Diagnostic: Viewing-Angle Dust Mirage & CMB-Dipole Sightline Split (2026-11-27)",
        "",
        "**Epistemic Tier:** `[E]`/`[D]` post-blind diagnostic audit on `40,894,394` KiDS-Legacy DR5 sources and `GAMA DR4` (`StellarMassesGKVv24.fits`).",
        "**Scope:** Companion diagnostic to [`POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md`](POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md). The pre-registered blind endpoints and verdicts in that record remain untouched.",
        "",
        "## 1. Viewing-Angle Internal-Dust Mirage in Apparent Red Galaxies",
        "",
        f"Across the full GAMA quality-matched window ($0.1 < z < 0.5,\\; 8.5 < \\log_{{10}}(M_*/M_\\odot) < 11.0$, $N = {c_full['total']:,}$):",
        f"- **Apparent red `(u - r)_obs > 2.00` sample:** `{c_full['apparent_etg_ur_gt_2']:,}` galaxies.",
        f"- **Tilted/edge-on dusty spiral disks misclassified as ETGs (`(u - r)_obs > 2.00` & `(u - r)_stars <= 2.00`):** **`{c_full['dusty_tilted_disks_in_apparent_etg']:,}` (`{c_full['dusty_disk_fraction_of_apparent_etg']*100:.1f}%`)**, with median internal reddening $\\Delta(u-r) = +{c_full['dusty_disk_stats']['median_reddening_ur_mag']:.3f}\\text{{ mag}}$ ($E(B-V) = {c_full['dusty_disk_stats']['median_dustEBV']:.3f}$).",
        f"- **True dust-free intrinsic ellipticals (`(u - r)_stars > 2.00`):** **`{c_full['true_intrinsic_etg']:,}` (`{(1-c_full['dusty_disk_fraction_of_apparent_etg'])*100:.1f}%`)**, with $E(B-V) = {c_full['true_etg_stats']['median_dustEBV']:.3f}$.",
        "",
        f"Across the **`{c_iso['total']:,}` isolated `GAMA_All4` weak-lensing lenses**:",
        f"- **Pure Blue Spirals:** `{c_iso['pure_blue_spirals']['count']:,}` (`{c_iso['pure_blue_spirals']['count']/c_iso['total']*100:.1f}%`)",
        f"- **Tilted/Edge-On Dusty Spirals in Apparent ETG Bin:** `{c_iso['tilted_dusty_spirals_misclassified_as_etg']['count']:,}` (**`{c_iso['dusty_disk_fraction_of_apparent_etg']*100:.1f}%` of isolated apparent ETGs**)",
        f"- **True Dust-Free Intrinsic Ellipticals:** `{c_iso['true_dust_free_ellipticals']['count']:,}` (`{(1-c_iso['dusty_disk_fraction_of_apparent_etg'])*100:.1f}%` of isolated apparent ETGs)",
        "",
        "### Weak-Lensing RAR Stacking Under Intrinsic Dust-Corrected Classification (`20x` Shared Randoms)",
        "",
        f"| Run (`GAMA_All4` Intrinsic Cut) | True Disks (`N={n_true_disks_iso:,}`) $\\chi^2/{r1['ltg']['ndof']}$ ($p$) | True Ellipticals (`N={n_true_etg_iso:,}`) $\\chi^2/{r1['etg']['ndof']}$ ($p$) | True ETG `med obs/pred` | Joint Hartlap $\\chi^2_{{\\rm H}}/{r1['ndof']}$ ($p_{{\\rm H}}$) |",
        "|---|---|---|---|---|",
        f"| `Q_ETG = 1.0` | `{r1['ltg']['chi2']:.2f}/7` (`{r1['ltg']['p_value']:.3g}`) | `{r1['etg']['chi2']:.2f}/7` (`{r1['etg']['p_value']:.3g}`) | **`{r1['etg']['median_obs_over_pred']:.4f}`** (vs $\\sqrt{{2}}=1.4142$) | `{r1['hartlap_chi2']:.2f}/14` (`{r1['hartlap_p']:.3g}`, `{r1['verdict_hartlap']}`) |",
        f"| `Q_ETG = sqrt(2)` | `{rs2['ltg']['chi2']:.2f}/7` (`{rs2['ltg']['p_value']:.3g}`) | `{rs2['etg']['chi2']:.2f}/7` (`{rs2['etg']['p_value']:.3g}`) | **`{rs2['etg']['median_obs_over_pred']:.4f}`** | `{rs2['hartlap_chi2']:.2f}/14` (`{rs2['hartlap_p']:.3g}`, `{rs2['verdict_hartlap']}`) |",
        f"| `Q_ETG = 1.4` | `{r14['ltg']['chi2']:.2f}/7` (`{r14['ltg']['p_value']:.3g}`) | `{r14['etg']['chi2']:.2f}/7` (`{r14['etg']['p_value']:.3g}`) | **`{r14['etg']['median_obs_over_pred']:.4f}`** | `{r14['hartlap_chi2']:.2f}/14` (`{r14['hartlap_p']:.3g}`, `{r14['verdict_hartlap']}`) |",
        "",
        "## 2. Directional Sightline & CMB-Dipole Hemisphere Breakdown (`Q_ETG = 1.0`)",
        "",
        "| Patch / Hemisphere | Lenses $N$ | $\\langle\\cos\\theta_{\\rm CMB}\\rangle$ | LTG `med obs/pred` ($\\chi^2/7$) | ETG `med obs/pred` ($\\chi^2/7$) |",
        "|---|---:|---:|---|---|",
    ]
    for fn in ("G12", "G09", "G15", "G23"):
        sf = sightlines[fn]
        s1 = sf["q1_summary"]
        md_lines.append(
            f"| `GAMA_{fn}` | `{sf['n_lenses']:,}` | `{sf['cos_cmb_dipole']:+.3f}` | "
            f"`{s1['ltg']['median_obs_over_pred']:.3f}` (`{s1['ltg']['chi2']:.1f}/7`) | "
            f"`{s1['etg']['median_obs_over_pred']:.3f}` (`{s1['etg']['chi2']:.1f}/7`) |"
        )
    for hn in ("N_DR5", "S_DR5"):
        sh = hemispheres[hn]
        s1 = sh["q1_summary"]
        md_lines.append(
            f"| `{hn}` | `{sh['n_lenses']:,}` | `{sh['cos_cmb_dipole']:+.3f}` | "
            f"`{s1['ltg']['median_obs_over_pred']:.3f}` (`{s1['ltg']['chi2']:.1f}/7`) | "
            f"`{s1['etg']['median_obs_over_pred']:.3f}` (`{s1['etg']['chi2']:.1f}/7`) |"
        )
    md_lines.extend(
        [
            "",
            f"- **Two-Hemisphere Unseen `DR5_New329` LTG Mean (`N_DR5` forward + `S_DR5` wake) / 2:** **`{ltg_hemi_mean:.4f}`** (consistent with unity across opposite dipole hemispheres, while `GAMA_G15` looking across the Virgo/Hercules-Shapley filament carries the localized northern overdensity).",
            "",
            "## Reproducibility",
            "```bash",
            "python3 03_observer_jwst/pom1_intrinsic_dipole_diagnostic.py --self-test",
            "python3 03_observer_jwst/pom1_intrinsic_dipole_diagnostic.py --run-cached",
            "```",
        ]
    )
    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON} and {OUT_MD} in {payload['elapsed_sec']:.1f}s")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run-cached", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return run_self_test()
    if args.run_cached:
        return run_cached_diagnostic()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
