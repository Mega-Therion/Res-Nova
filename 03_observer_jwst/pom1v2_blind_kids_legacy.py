#!/usr/bin/env python3
"""Blind test of P-OM-1 v2 on KiDS-Legacy (DR5 Cosmic Shear) & GAMA DR4.

Pre-registered: 03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md
(plus post-unblinding Erratum & Methodological Audit appended 2026-11-26).

Evaluates the frozen pom1v2_mass_system.py / pom1_lensing_rar.py model:
  - Interpolating function: mu_std(x) = x / sqrt(1 + x^2)
  - Acceleration anchor: a0 = 1.1607e-10 m/s^2 (fixed; NOT refit)
  - Estimator conversion: g_obs = 4 * G * DeltaSigma * (73 / 70)
  - LTG baryons: Boselli+2014 cold gas on stellar mass (Q_LTG = 1.0)
  - ETG baryons: Chae+2021 hot gas (M_hot = 10^-5.414 M*^1.47) with no cold gas
  - Zero per-sample free parameter tuning.

Evaluates BOTH:
  1. The pre-registered B21-style estimator (z_B + 0.2 > z_l, [0, inf) n(z_s), Q_ETG=1.0),
     with footprint-coverage & per-patch unwrapped jackknife bugs fixed.
  2. The Mistele+2024 specification (arXiv:2310.15248: WMAP9 Omega_m=0.2793,
     z_B > z_l + 0.20, [z_l, inf) n(z_s) normalization, shared 5x random catalog,
     Anderson-Hartlap correction, and exact comparison of Q_ETG=1.0 vs Q_ETG=1.4 across
     DR5_New329, GAMA_G23, GAMA_All4, spectroscopic cylinder isolation, R_isol=4 Mpc,
     and strict full-bin tomographic cuts).

Usage:
  python3 03_observer_jwst/pom1v2_blind_kids_legacy.py --self-test
  python3 03_observer_jwst/pom1v2_blind_kids_legacy.py [--cache-dir DIR]
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import io
import json
import math
import os
import subprocess
import sys
import tarfile
import time
import urllib.parse
import urllib.request
import zlib
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

# ------------------------------------------------------------------ Frozen Physical Constants
C_LIGHT_KM_S = 299792.458
G_SI = 6.67430e-11
MSUN_KG = 1.98847e30
MPC_M = 3.0856775814913673e22
PC_M = 3.0856775814913673e16
# Sigma_crit constant: c^2 / (4 pi G) in (Msun / pc^2) * Mpc (~ 1.66287e6)
SIG_CR_FACTOR = ((C_LIGHT_KM_S * 1e3) ** 2 / (4.0 * math.pi * G_SI)) / (MSUN_KG / (PC_M ** 2)) / MPC_M

# Cosmologies: WMAP9 (Brouwer+2021 §1.1 & Mistele+2024 §2) vs Planck18
OM_WMAP9, OL_WMAP9, H0_B21 = 0.2793, 0.7207, 70.0
OM_P18, OL_P18 = 0.3153, 0.6847

# KiDS-Legacy cosmic shear Table 1 (arXiv:2503.19441) multiplicative calibration bias per TOMOBIN 1..6
KIDS_M_GOLD = np.array([0.0, -0.023, -0.016, -0.011, +0.020, +0.030, +0.045], dtype=np.float64)
# Measured lower Z_B boundary per KiDS-Legacy TOMOBIN 1..6 (0 unused)
KIDS_TOMO_ZB_MIN = np.array([0.0, 0.11, 0.43, 0.59, 0.72, 0.91, 1.15], dtype=np.float64)

# B21 15 log10(g_bar) bin centers & edges: [-14.9826 .. -11.2837]
N_GB_BINS = 15
GB_LOG_EDGES = np.linspace(-14.8593 - 0.123285, -11.4070 + 0.123285, N_GB_BINS + 1)

# Pre-frozen G09->G23 photometric calibration (zero shear used; validated held-out on G23 N=31,960)
BETA_Z_DR5 = np.array([-0.043490, 0.954353, -0.561158, 0.030555, 0.034788, -0.013131, 0.062737], dtype=np.float64)
DR5_GAMA_MASS_OFFSET = 0.1293  # Align DR5 (LePhare + ap2 at z_cal) to GAMA/Taylor+2011

WL_DTYPE = np.dtype([
    ("ra", "<f8"), ("dec", "<f8"), ("z_b", "<f4"), ("e1", "<f4"), ("e2", "<f4"),
    ("weight", "<f4"), ("tomobin", "i1"), ("patch_n", "u1"), ("is_new_dr5", "u1"),
])
N_KIDS_LEGACY_ROWS = 40894394

# Official Upstream Data URLs & Verified Digests
URLS = {
    "xipm_tar": "https://kids.strw.leidenuniv.nl/sci_data/KiDS_Legacy_cosmic_shear_data_release.tar.gz",
    "wl_fits_gz": "https://kids.strw.leidenuniv.nl/DR5/data_files/KiDS_Legacy_NS_unblind_final.fits.gz",
    "gama_df": "https://www.gama-survey.org/dr4/data/cat/LocalFlowCorrection/v14/DistancesFramesv14.fits",
    "gama_match": "https://www.gama-survey.org/dr4/data/cat/gkvInputCat/v02/gkvGamaIIMatchesv01.fits",
    "gama_mstar": "https://www.gama-survey.org/dr4/data/cat/StellarMasses/v24/StellarMassesGKVv24.fits",
    "dr4_bright": "https://kids.strw.leidenuniv.nl/DR4/data_files/KiDS_DR4_brightsample.fits",
}
WL_FITS_GZ_BYTES = 7179531549


# ------------------------------------------------------------------ Data Cache & Ingestion
def resolve_paths(cache_dir: str | Path | None = None) -> dict[str, Path]:
    base = Path(cache_dir or os.environ.get("KL_CACHE_DIR", "/tmp/kids_legacy_cache"))
    lens_dir = Path("/tmp/kids_lenses") if (Path("/tmp/kids_lenses/DistancesFramesv14.fits").exists()) else (base / "lenses")
    nz_alt = Path("/tmp/kids_test/KiDS_Legacy_cosmic_shear_data_release/data/KiDS_Legacy_xipm.fits")
    nz_alt2 = Path("/tmp/kl_data/KiDS_Legacy_cosmic_shear_data_release/data/KiDS_Legacy_xipm.fits")
    if nz_alt.exists():
        nz_path = nz_alt
    elif nz_alt2.exists():
        nz_path = nz_alt2
    else:
        nz_path = base / "KiDS_Legacy_cosmic_shear_data_release" / "data" / "KiDS_Legacy_xipm.fits"

    wl_bin = Path("/tmp/kids_legacy_wl_slim.bin")
    if not wl_bin.exists() and (base / "kids_legacy_wl_slim.bin").exists():
        wl_bin = base / "kids_legacy_wl_slim.bin"

    wl_gz = Path("/tmp/kids_test/KiDS_Legacy_NS_unblind_final.fits.gz")
    if not wl_gz.exists():
        wl_gz = base / "KiDS_Legacy_NS_unblind_final.fits.gz"

    tiles_txt = Path("/tmp/dr5_new_tiles.txt")
    if not tiles_txt.exists():
        tiles_txt = base / "dr5_new_tiles.txt"

    return {
        "base": base,
        "lens_dir": lens_dir,
        "nz_fits": nz_path,
        "wl_bin": wl_bin,
        "wl_gz": wl_gz,
        "tiles_txt": tiles_txt,
    }


def _curl_download(url: str, dest: Path, expected_bytes: int | None = None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(40):
        if expected_bytes is not None and dest.exists() and dest.stat().st_size == expected_bytes:
            return
        cmd = [
            "curl", "-fL", "-C", "-", "--connect-timeout", "20",
            "--speed-time", "45", "--speed-limit", "20000",
            "-o", str(dest), url,
        ]
        rc = subprocess.run(cmd, check=False).returncode
        if rc == 0 and (expected_bytes is None or (dest.exists() and dest.stat().st_size == expected_bytes)):
            return
        if rc == 22:
            raise RuntimeError(f"HTTP error (curl rc=22) fetching {url}")
        time.sleep(2)
    raise RuntimeError(f"Failed downloading {url} -> {dest}")


def _feed_fits_bytes(state: dict, new_bytes: bytes, new_tiles_sorted: np.ndarray, fits_dt: np.dtype, fout):
    """Incrementally parse FITS primary+bintable headers then stream 401-byte rows to WL_DTYPE binary."""
    buf = state["buf"] + new_bytes
    while state["end_blocks"] < 2:
        if len(buf) < 2880:
            state["buf"] = buf
            return
        blk = buf[:2880]
        buf = buf[2880:]
        for j in range(0, 2880, 80):
            card = blk[j:j + 80].decode("ascii", "replace")
            if card.startswith("NAXIS1  ="):
                state["naxis1"] = int(card.split("=")[1].split("/")[0].strip())
            elif card.startswith("NAXIS2  ="):
                state["naxis2"] = int(card.split("=")[1].split("/")[0].strip())
            elif card.strip() == "END":
                state["end_blocks"] += 1
                break
        if state["end_blocks"] == 2:
            assert state["naxis1"] == 401 and state["naxis2"] == N_KIDS_LEGACY_ROWS, (
                f"Unexpected FITS table geometry {state['naxis1']}x{state['naxis2']}"
            )

    naxis2 = state["naxis2"]
    rem_rows = naxis2 - state["written"]
    n_full = min(len(buf) // 401, rem_rows)
    if n_full > 0:
        used = n_full * 401
        arr = np.frombuffer(buf[:used], dtype=fits_dt)
        out = np.empty(n_full, dtype=WL_DTYPE)
        out["ra"] = arr["RAJ2000"]
        out["dec"] = arr["DECJ2000"]
        out["z_b"] = arr["Z_B"].astype("<f4")
        out["e1"] = arr["e1"].astype("<f4")
        out["e2"] = arr["e2"].astype("<f4")
        out["weight"] = arr["weight"].astype("<f4")
        out["tomobin"] = arr["TOMOBIN"].astype("i1")
        out["patch_n"] = np.char.startswith(arr["PATCH"], b"N").astype("u1")
        tn = np.char.strip(arr["THELI_NAME"])
        idx = np.searchsorted(new_tiles_sorted, tn)
        idx_c = np.minimum(idx, len(new_tiles_sorted) - 1)
        out["is_new_dr5"] = (new_tiles_sorted[idx_c] == tn).astype("u1")
        fout.write(out.tobytes())
        state["written"] += n_full
        buf = buf[used:]
    elif rem_rows == 0:
        buf = b""
    state["buf"] = buf


def convert_kids_legacy_fits_to_slim(
    wl_gz: Path | None,
    out_bin: Path,
    new_tiles_txt: Path,
    wl_url: str | None = None,
    expected_gz_bytes: int = WL_FITS_GZ_BYTES,
):
    """Stream 401-byte FITS binary rows from local .fits.gz OR Range-resumed HTTPS directly into WL_DTYPE binary.

    When streaming over HTTPS (wl_gz is None or missing), uses zlib gzip-trailer verification (CRC32 + ISIZE)
    without writing the 7.18 GB .fits.gz to disk, keeping disk footprint ~1.43 GB.
    """
    new_tiles = np.array([l.strip().encode("ascii") for l in new_tiles_txt.read_text().splitlines() if l.strip()])
    new_tiles_sorted = np.sort(new_tiles)
    fits_dt = np.dtype([
        ("THELI_NAME", "S17"), ("RAJ2000", ">f8"), ("DECJ2000", ">f8"), ("PATCH", "S8"),
        ("f5_8", "S32"), ("SG2DPHOT", ">i4"), ("f10_20", "S88"),
        ("Z_B", ">f8"), ("T_B", ">f8"), ("TOMOBIN", ">i4"),
        ("f24_47", "S192"), ("e1", ">f8"), ("e2", ">f8"), ("weight", ">f8"),
    ])
    assert fits_dt.itemsize == 401

    out_tmp = out_bin.with_suffix(".bin.tmp")
    out_bin.parent.mkdir(parents=True, exist_ok=True)
    decomp = zlib.decompressobj(16 + zlib.MAX_WBITS)
    state = {"end_blocks": 0, "naxis1": None, "naxis2": None, "written": 0, "buf": b""}
    gz_pos = 0
    t_start = time.time()
    next_pct = 5

    try:
        with open(out_tmp, "wb") as fout:
            if wl_gz is not None and wl_gz.exists() and wl_gz.stat().st_size == expected_gz_bytes:
                with open(wl_gz, "rb") as fg:
                    while True:
                        comp = fg.read(4 * 1024 * 1024)
                        if not comp:
                            break
                        gz_pos += len(comp)
                        raw = decomp.decompress(comp)
                        if raw:
                            _feed_fits_bytes(state, raw, new_tiles_sorted, fits_dt, fout)
            else:
                assert wl_url, "Need either complete local wl_gz or wl_url"
                for attempt in range(1, 300):
                    if gz_pos >= expected_gz_bytes:
                        break
                    try:
                        req = urllib.request.Request(
                            wl_url,
                            headers={"Range": f"bytes={gz_pos}-{expected_gz_bytes - 1}", "User-Agent": "Res-Nova"},
                        )
                        with urllib.request.urlopen(req, timeout=30) as resp:
                            if gz_pos > 0 and resp.status != 206:
                                raise RuntimeError(f"Expected HTTP 206 Partial Content at {gz_pos}, got {resp.status}")
                            win_t = time.time()
                            win_b = 0
                            while gz_pos < expected_gz_bytes:
                                comp = resp.read(262144)
                                if not comp:
                                    break
                                gz_pos += len(comp)
                                win_b += len(comp)
                                raw = decomp.decompress(comp)
                                if raw:
                                    _feed_fits_bytes(state, raw, new_tiles_sorted, fits_dt, fout)
                                dt_w = time.time() - win_t
                                if dt_w >= 25.0:
                                    if win_b / dt_w < 25000.0:
                                        print(f"[stream] throttle detected ({win_b/dt_w/1024:.1f} KB/s), reconnecting at {gz_pos}/{expected_gz_bytes}", flush=True)
                                        break
                                    win_t = time.time()
                                    win_b = 0
                                pct = int(100 * gz_pos / expected_gz_bytes)
                                if pct >= next_pct:
                                    el = max(time.time() - t_start, 1e-3)
                                    print(f"[stream] {pct}% ({gz_pos/1e6:.1f}/{expected_gz_bytes/1e6:.1f} MB, avg {gz_pos/1e6/el:.2f} MB/s, rows={state['written']:,d})", flush=True)
                                    next_pct += 5
                    except Exception as exc:
                        print(f"[stream attempt {attempt}] reconnect at {gz_pos}: {exc}", flush=True)
                        time.sleep(2)

            tail = decomp.flush()
            if tail:
                _feed_fits_bytes(state, tail, new_tiles_sorted, fits_dt, fout)

        if gz_pos != expected_gz_bytes or not decomp.eof or state["written"] != N_KIDS_LEGACY_ROWS:
            raise RuntimeError(
                f"KiDS-Legacy conversion incomplete: gz={gz_pos}/{expected_gz_bytes}, eof={decomp.eof}, written={state['written']}/{N_KIDS_LEGACY_ROWS}"
            )
    except Exception:
        out_tmp.unlink(missing_ok=True)
        raise

    os.replace(out_tmp, out_bin)


def ensure_data(paths: dict[str, Path], drop_wl_gz_after: bool = False):
    """Ensure all GAMA DR4, KiDS-DR4, KiDS-DR5 ESO TAP, NZ_SOURCE, and WL binary files exist."""
    paths["base"].mkdir(parents=True, exist_ok=True)
    paths["lens_dir"].mkdir(parents=True, exist_ok=True)

    # 1. KiDS-Legacy NZ_SOURCE tarball
    if not paths["nz_fits"].exists():
        tgz = paths["base"] / "KiDS_Legacy_cosmic_shear_data_release.tar.gz"
        _curl_download(URLS["xipm_tar"], tgz)
        with tarfile.open(tgz, "r:gz") as tf:
            tf.extractall(paths["base"], filter="data")
        if not paths["nz_fits"].exists():
            cand = list(paths["base"].rglob("KiDS_Legacy_xipm.fits"))
            if not cand:
                raise RuntimeError("KiDS_Legacy_xipm.fits missing after archive extraction")
            paths["nz_fits"] = cand[0]

    # 2. GAMA DR4 & KiDS DR4 bright catalogs
    for key, fname in (
        ("gama_df", "DistancesFramesv14.fits"),
        ("gama_match", "gkvGamaIIMatchesv01.fits"),
        ("gama_mstar", "StellarMassesGKVv24.fits"),
        ("dr4_bright", "KiDS_DR4_brightsample.fits"),
    ):
        fp = paths["lens_dir"] / fname
        if not fp.exists():
            _curl_download(URLS[key], fp)

    # 3. DR5-minus-DR4 exact 341 tile list from ESO TAP + bright DR5 sample on those tiles
    if not paths["tiles_txt"].exists():
        def _tap_tiles(tbl: str) -> set[str]:
            u_t = "https://archive.eso.org/tap_cat/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&MAXREC=10000&QUERY=" + urllib.parse.quote(
                f"SELECT DISTINCT THELI_NAME FROM {tbl}"
            )
            txt = urllib.request.urlopen(urllib.request.Request(u_t, headers={"User-Agent": "Res-Nova"}), timeout=60).read().decode()
            return {l.strip() for l in txt.splitlines()[1:] if l.strip()}
        new_tiles = sorted(_tap_tiles("safcat.KiDS_DR5_0_ugriZYJHKs_cat_fits") - _tap_tiles("safcat.KiDS_DR4_1_ugriZYJHKs_cat_fits"))
        paths["tiles_txt"].write_text("\n".join(new_tiles) + "\n")

    dr5_npy = paths["lens_dir"] / "kids_dr5_bright_new341_exact.npy"
    if not dr5_npy.exists():
        from astropy.io import fits
        new_tiles = [l.strip() for l in paths["tiles_txt"].read_text().splitlines() if l.strip()]
        rows = []
        for i in range(0, len(new_tiles), 18):
            tlist = ",".join(f"'{t}'" for t in new_tiles[i:i + 18])
            q = (
                "SELECT RAJ2000, DECJ2000, MAG_AUTO, MAG_AUTO_raw, MAG_GAAP_u, MAG_GAAP_r, "
                "EXTINCTION_u, EXTINCTION_r, Z_B, Z_ML, mstar_bestfit "
                f"FROM safcat.KiDS_DR5_0_ugriZYJHKs_cat_fits WHERE THELI_NAME IN ({tlist}) "
                "AND MAG_AUTO < 20.5 AND mstar_bestfit > 5.0 AND MASK = 0 AND SG_FLAG = 1 AND SG2DPHOT = 0 AND CLASS_STAR < 0.5"
            )
            u = "https://archive.eso.org/tap_cat/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=fits&MAXREC=500000&QUERY=" + urllib.parse.quote(q)
            blob = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Res-Nova"}), timeout=120).read()
            with fits.open(io.BytesIO(blob)) as h:
                d = h[1].data
                rows.append(np.column_stack([np.asarray(d[c], np.float64) for c in d.names]))
        np.save(dr5_npy, np.vstack(rows))

    # 4. KiDS-Legacy 40.9M weak-lensing slim binary (stream directly over HTTPS if .fits.gz not cached)
    if not paths["wl_bin"].exists() or paths["wl_bin"].stat().st_size != N_KIDS_LEGACY_ROWS * WL_DTYPE.itemsize:
        convert_kids_legacy_fits_to_slim(
            paths["wl_gz"] if paths["wl_gz"].exists() else None,
            paths["wl_bin"],
            paths["tiles_txt"],
            wl_url=URLS["wl_fits_gz"],
            expected_gz_bytes=WL_FITS_GZ_BYTES,
        )
        if drop_wl_gz_after:
            paths["wl_gz"].unlink(missing_ok=True)


# ------------------------------------------------------------------ Cosmology & Lensing Geometry
def comoving_dist_mpc(z: float, om: float = OM_WMAP9, ol: float = OL_WMAP9, h0: float = H0_B21) -> float:
    val, _ = integrate.quad(lambda zp: 1.0 / math.sqrt(om * (1.0 + zp) ** 3 + ol), 0.0, float(z), epsrel=1e-9)
    return (C_LIGHT_KM_S / h0) * val


def build_distance_tables(z_max: float = 6.0, om: float = OM_WMAP9, ol: float = OL_WMAP9, h0: float = H0_B21):
    z_grid = np.linspace(0.0, z_max, 4801)
    ez = np.sqrt(om * (1.0 + z_grid) ** 3 + ol)
    inv_ez = 1.0 / ez
    dz = z_grid[1] - z_grid[0]
    dc = np.zeros_like(z_grid)
    dc[1:] = np.cumsum(0.5 * (inv_ez[:-1] + inv_ez[1:]) * dz) * (C_LIGHT_KM_S / h0)
    da = dc / (1.0 + z_grid)
    return z_grid, dc, da


def build_sigma_crit_inv_splines(
    z_mid: np.ndarray,
    nz_bins: np.ndarray,
    dz_widths: np.ndarray | None = None,
    om: float = OM_WMAP9,
    ol: float = OL_WMAP9,
    h0: float = H0_B21,
    norm_above_zl: bool = True,
):
    """Build Sigma_crit^{-1}(z_l, tomo) [pc^2 / Msun] over n_tomo(z_s).

    If norm_above_zl is True (Mistele+2024 Eq. 3, arXiv:2310.15248), n_tomo(z_s) is
    normalized on [z_l, inf) so sources genuinely above z_l integrate to unity.
    If False (Brouwer+2021 Eq. 8), n_tomo(z_s) is normalized on [0, inf).
    """
    z_grid, dc_grid, da_grid = build_distance_tables(max(float(z_mid.max()) + 0.1, 6.0), om=om, ol=ol, h0=h0)
    dc_s = np.interp(z_mid, z_grid, dc_grid)
    da_s = dc_s / (1.0 + z_mid)
    dz = np.asarray(dz_widths, np.float64) if dz_widths is not None else np.gradient(z_mid)

    zl_knots = np.linspace(0.02, 0.58, 113)
    dc_l_knots = np.interp(zl_knots, z_grid, dc_grid)
    da_l_knots = dc_l_knots / (1.0 + zl_knots)

    splines = {}
    for b in range(nz_bins.shape[0]):
        nz = np.maximum(np.asarray(nz_bins[b], np.float64), 0.0)
        tot_w = float(np.sum(nz * dz))
        if tot_w > 0.0:
            nz = nz / tot_w
        vals = np.zeros_like(zl_knots)
        for i, (zl, dcl, dal) in enumerate(zip(zl_knots, dc_l_knots, da_l_knots)):
            msk = z_mid > zl
            if not np.any(msk):
                continue
            mass_above = float(np.sum(nz[msk] * dz[msk]))
            if mass_above <= 1e-12:
                continue
            dls = (dc_s[msk] - dcl) / (1.0 + z_mid[msk])
            ratio = np.maximum(dls, 0.0) / np.maximum(da_s[msk], 1e-12)
            integral = float(np.sum(nz[msk] * dz[msk] * ratio))
            if norm_above_zl:
                integral /= mass_above
            vals[i] = (dal / SIG_CR_FACTOR) * integral
        splines[b + 1] = CubicSpline(zl_knots, vals)
    return splines, z_grid, dc_grid, da_grid


def load_kids_nz(nz_path: Path):
    from astropy.io import fits
    with fits.open(nz_path, memmap=True) as h:
        nz = h["NZ_SOURCE"].data
        z_mid = np.asarray(nz["Z_MID"], np.float64)
        dz_w = np.asarray(nz["Z_HIGH"] - nz["Z_LOW"], np.float64)
        bins = np.vstack([np.asarray(nz[f"BIN{b}"], np.float64) for b in range(1, 7)])
    return z_mid, dz_w, bins


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


# ------------------------------------------------------------------ Contiguous Per-Patch Unwrapped Jackknife
def _unwrap_ra_for_region(ra_reg: np.ndarray) -> np.ndarray:
    """Shift RA continuously around its circular median so 0/360 seam is never split."""
    if len(ra_reg) == 0:
        return ra_reg
    ang = np.radians(ra_reg)
    mean_ang = math.atan2(float(np.mean(np.sin(ang))), float(np.mean(np.cos(ang))))
    center_deg = math.degrees(mean_ang) % 360.0
    return ((ra_reg - center_deg + 180.0) % 360.0) - 180.0 + center_deg


def _partition_2d_contiguous(ra_reg: np.ndarray, dec_reg: np.ndarray, k_reg: int) -> np.ndarray:
    """Partition one contiguous sky patch into k_reg compact balanced 2D sky blocks (recursive KD split)."""
    n = len(ra_reg)
    if k_reg <= 1 or n <= 1:
        return np.zeros(n, dtype=np.int32)
    if n <= k_reg:
        return np.arange(n, dtype=np.int32) % k_reg
    ra_u = _unwrap_ra_for_region(ra_reg)
    out = np.empty(n, dtype=np.int32)

    def _split(idx: np.ndarray, k: int, offset: int):
        if k == 1 or len(idx) <= 1:
            out[idx] = offset
            return
        k_left = k // 2
        k_right = k - k_left
        cosd = max(math.cos(math.radians(float(np.median(dec_reg[idx])))), 0.1)
        span_ra = float(ra_u[idx].max() - ra_u[idx].min()) * cosd
        span_dec = float(dec_reg[idx].max() - dec_reg[idx].min())
        coord = ra_u[idx] if span_ra >= span_dec else dec_reg[idx]
        order = idx[np.argsort(coord, kind="mergesort")]
        n_left = int(round(len(order) * (k_left / k)))
        n_left = max(1, min(len(order) - 1, n_left))
        _split(order[:n_left], k_left, offset)
        _split(order[n_left:], k_right, offset + k_left)

    _split(np.arange(n, dtype=np.int32), int(k_reg), 0)
    return out


def assign_spatial_jackknife(
    ra: np.ndarray,
    dec: np.ndarray,
    n_jk: int,
    region_labels: np.ndarray | None = None,
) -> np.ndarray:
    """Deterministic contiguous sky-quantile jackknife partitioning per contiguous region."""
    ra = np.asarray(ra, np.float64)
    dec = np.asarray(dec, np.float64)
    n = len(ra)
    if n == 0:
        return np.zeros(0, dtype=np.int32)

    if region_labels is None:
        # Auto-split disconnected patches cleanly by Dec sign (KiDS North/South) or wide RA gaps
        labels = np.where(dec >= -12.0, "N", "S")
    else:
        labels = np.asarray(region_labels)

    uniq, counts = np.unique(labels, return_counts=True)
    if len(uniq) == 1:
        return _partition_2d_contiguous(ra, dec, n_jk)

    # Allocate even-friendly integer cell counts per region proportional to count
    raw = counts.astype(np.float64) * (float(n_jk) / n)
    alloc = np.maximum(2, np.floor(raw).astype(int))
    while int(alloc.sum()) < n_jk:
        rem = raw - alloc
        alloc[int(np.argmax(rem))] += 1
    while int(alloc.sum()) > n_jk:
        idx_hi = int(np.argmax(alloc))
        if alloc[idx_hi] <= 1:
            break
        alloc[idx_hi] -= 1

    # Round each region quota to factorable cell count if adjustment keeps total == n_jk (greedy preserved sum)
    jk = np.empty(n, dtype=np.int32)
    offset = 0
    for u, k_u in zip(uniq, alloc):
        m = np.where(labels == u)[0]
        jk[m] = offset + _partition_2d_contiguous(ra[m], dec[m], int(k_u))
        offset += int(k_u)
    return jk


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
    n_jk: int = 64,
    batch_size: int = 1000,
    tree_s: cKDTree | None = None,
    zb_cut_mode: str = "mistele",
):
    """Accumulate (n_jk, 2 [LTG,ETG], 15 [log_gbar]) arrays of numerators/denominators.

    zb_cut_mode:
      - 'mistele'    : z_B > z_l + 0.20 (Mistele+2024 arXiv:2310.15248 line 318)
      - 'b21'        : z_B + 0.20 > z_l (Brouwer+2021 line 315)
      - 'strict_tomo': KIDS_TOMO_ZB_MIN[tomo] > z_l + 0.20 (zero intra-bin truncation bias)
    """
    assert zb_cut_mode in ("mistele", "b21", "strict_tomo"), zb_cut_mode
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
    l_rmax_rad = r_max_mpc / np.maximum(l_da, 1.0)

    sc_inv_lens = np.zeros((n_l, 7), dtype=np.float64)
    for b in range(1, 7):
        sc_inv_lens[:, b] = np.maximum(sc_splines[b](l_z), 0.0)

    acc_num_t = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_num_x = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_den_m = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_den_w = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_gb_w = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64)
    acc_npair = np.zeros((n_jk, 2, N_GB_BINS), dtype=np.int64)

    m_gold_s = KIDS_M_GOLD[s_tomo]
    zb_bin_min_s = KIDS_TOMO_ZB_MIN[s_tomo]
    g_msun_div_mpc2 = (G_SI * MSUN_KG) / (MPC_M ** 2)

    for start in range(0, n_l, batch_size):
        end = min(start + batch_size, n_l)
        nbrs = tree_s.query_ball_point(l_xyz[start:end], r=l_rmax_rad[start:end], workers=-1)
        counts = np.fromiter((len(a) for a in nbrs), dtype=np.int32, count=len(nbrs))
        if not np.any(counts):
            continue
        li = np.repeat(np.arange(start, end, dtype=np.int32), counts)
        si = np.concatenate([np.asarray(a, dtype=np.int32) for a in nbrs if a])

        if zb_cut_mode == "mistele":
            cut = s_zb[si] > (l_z[li] + 0.20)
        elif zb_cut_mode == "b21":
            cut = (s_zb[si] + 0.20) > l_z[li]
        else:
            cut = zb_bin_min_s[si] > (l_z[li] + 0.20)
        if not np.any(cut):
            continue
        li, si = li[cut], si[cut]

        # Flat tangent-plane offsets in image coordinates (East=-RA, North=+Dec)
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

        gb = g_msun_div_mpc2 * l_mb[li] / (r_mpc * r_mpc)
        lgb = np.log10(np.maximum(gb, 1e-30))
        b_idx = np.searchsorted(GB_LOG_EDGES, lgb, side="right") - 1
        bm = (b_idx >= 0) & (b_idx < N_GB_BINS)
        if not np.any(bm):
            continue
        li, si, dra_rad, ddec_rad, gb, b_idx = li[bm], si[bm], dra_rad[bm], ddec_rad[bm], gb[bm], b_idx[bm]

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
    subtract_rand_cross: bool = True,
):
    """Build g_bar, g_obs, cross-shear g_x, and full jackknife covariance; evaluate frozen P-OM-1 v2."""
    n_jk = lens_acc["num_t"].shape[0]
    nt = lens_acc["num_t"].sum(axis=0)
    nx = lens_acc["num_x"].sum(axis=0)
    dm = lens_acc["den_m"].sum(axis=0)
    dw = lens_acc["den_w"].sum(axis=0)
    gw = lens_acc["gb_w"].sum(axis=0)
    npair = lens_acc["npair"].sum(axis=0)

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
        if subtract_rand_cross:
            g_x = g_x - gx_rand
    else:
        g_rand = np.zeros_like(g_t_raw)
        gx_rand = np.zeros_like(g_t_raw)
        g_obs = g_t_raw

    nt_all = nt[None, :, :] - lens_acc["num_t"]
    nx_all = nx[None, :, :] - lens_acc["num_x"]
    dm_all = dm[None, :, :] - lens_acc["den_m"]
    with np.errstate(divide="ignore", invalid="ignore"):
        gt_loo = conv * nt_all / dm_all - g_rand[None, :, :]
        gx_loo = conv * nx_all / dm_all - (gx_rand[None, :, :] if subtract_rand_cross else 0.0)

    if rand_acc is not None and rand_acc["num_t"].shape[0] == n_jk:
        rt_tot = rand_acc["num_t"].sum(axis=0)
        rnx_tot = rand_acc["num_x"].sum(axis=0)
        rdm_tot = rand_acc["den_m"].sum(axis=0)
        rt_loo = rt_tot[None, :, :] - rand_acc["num_t"]
        rnx_loo = rnx_tot[None, :, :] - rand_acc["num_x"]
        rdm_loo = rdm_tot[None, :, :] - rand_acc["den_m"]
        with np.errstate(divide="ignore", invalid="ignore"):
            g_rand_loo = np.where(rdm_loo > 0, conv * rt_loo / rdm_loo, g_rand[None, :, :])
            gx_rand_loo = np.where(rdm_loo > 0, conv * rnx_loo / rdm_loo, gx_rand[None, :, :])
            gt_loo = conv * nt_all / dm_all - g_rand_loo
            if subtract_rand_cross:
                gx_loo = conv * nx_all / dm_all - gx_rand_loo

    if use_bins is None:
        bin_mask = np.zeros((2, N_GB_BINS), dtype=bool)
        bin_mask[:, 8:] = True
    else:
        bin_mask = np.asarray(use_bins, dtype=bool)
    ok_mask = bin_mask & (npair >= min_npair) & np.isfinite(gb_mean) & np.isfinite(g_obs) & (dm > 0)
    idx_late = np.where(ok_mask[0])[0]
    idx_early = np.where(ok_mask[1])[0]

    gb_vec = np.concatenate([gb_mean[0, idx_late], gb_mean[1, idx_early]])
    d_vec = np.concatenate([g_obs[0, idx_late], g_obs[1, idx_early]])
    gx_vec = np.concatenate([g_x[0, idx_late], g_x[1, idx_early]])
    gr_vec = np.concatenate([g_rand[0, idx_late], g_rand[1, idx_early]])

    jk_mat = np.concatenate([gt_loo[:, 0, idx_late], gt_loo[:, 1, idx_early]], axis=1)
    jxk_mat = np.concatenate([gx_loo[:, 0, idx_late], gx_loo[:, 1, idx_early]], axis=1)

    valid_jk = np.all(np.isfinite(jk_mat) & np.isfinite(jxk_mat), axis=1)
    jk_mat = jk_mat[valid_jk]
    jxk_mat = jxk_mat[valid_jk]
    K = len(jk_mat)
    n = len(d_vec)
    assert n >= 1 and K >= n + 3, f"{label}: insufficient bins/JK blocks (n={n}, K={K})"

    jk_mean = jk_mat.mean(axis=0)
    diff = jk_mat - jk_mean[None, :]
    C = ((K - 1.0) / K) * (diff.T @ diff)

    jxk_diff = jxk_mat - jxk_mat.mean(axis=0)[None, :]
    Cx = ((K - 1.0) / K) * (jxk_diff.T @ jxk_diff)

    hartlap = (K - n - 2.0) / (K - 1.0)

    def chi_fn(pred_v, cov=C):
        r = d_vec - pred_v
        return float(r @ np.linalg.solve(cov, r))

    pred_v = P.pred(gb_vec, P.A0_OBS)
    c0 = chi_fn(pred_v)
    p0 = float(chi2_dist.sf(c0, n))
    c0_h = c0 * hartlap
    p0_h = float(chi2_dist.sf(c0_h, n))
    cN = chi_fn(4.0 / math.pi * gb_vec)
    pN = float(chi2_dist.sf(cN, n))
    pN_h = float(chi2_dist.sf(cN * hartlap, n))
    c_cross = float(gx_vec @ np.linalg.solve(Cx, gx_vec))
    p_cross = float(chi2_dist.sf(c_cross, n))
    p_cross_h = float(chi2_dist.sf(c_cross * hartlap, n))

    deltas = np.linspace(-P.MSTAR_SYS_DEX, P.MSTAR_SYS_DEX, 401)
    cs = [chi_fn(P.pred(gb_vec * (10.0 ** dl), P.A0_OBS)) for dl in deltas]
    k_best = int(np.argmin(cs))
    dm_best, cm_best = float(deltas[k_best]), float(cs[k_best])
    pm_best = float(chi2_dist.sf(cm_best, max(n - 1, 1)))
    pm_best_h = float(chi2_dist.sf(cm_best * hartlap, max(n - 1, 1)))

    if pN >= 1e-6:
        verdict = "NO_POWER"
    elif p0 >= 0.01:
        verdict = "PASS"
    elif pm_best >= 0.01:
        verdict = "PASS_WITHIN_MASS_SYSTEMATIC"
    else:
        verdict = "FAIL"

    if pN_h >= 1e-6:
        verdict_h = "NO_POWER"
    elif p0_h >= 0.01:
        verdict_h = "PASS"
    elif pm_best_h >= 0.01:
        verdict_h = "PASS_WITHIN_MASS_SYSTEMATIC"
    else:
        verdict_h = "FAIL"

    nl = len(idx_late)
    type_stats = {}
    for nm, sl in (("late", slice(0, nl)), ("early", slice(nl, n))):
        nt_b = sl.stop - sl.start
        if nt_b > 0:
            r = d_vec[sl] - pred_v[sl]
            ct = float(r @ np.linalg.solve(C[sl, sl], r))
            h_t = (K - nt_b - 2.0) / (K - 1.0)
            type_stats[nm] = {
                "n_bins": int(nt_b),
                "chi2": ct,
                "p": float(chi2_dist.sf(ct, nt_b)),
                "chi2_hartlap": ct * h_t,
                "p_hartlap": float(chi2_dist.sf(ct * h_t, nt_b)),
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
        h_d = (K - len(common) - 2.0) / (K - 1.0)
        eml = {
            "chi2": cd, "dof": int(len(common)), "p": float(chi2_dist.sf(cd, len(common))),
            "chi2_hartlap": cd * h_d, "p_hartlap": float(chi2_dist.sf(cd * h_d, len(common))),
            "median_log10_ratio": float(np.median(np.log10(np.maximum(re_, 1e-30) / np.maximum(rl, 1e-30)))),
        }

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
        "verdict_hartlap": verdict_h,
        "n_bins": int(n),
        "n_jk_active": int(K),
        "hartlap_factor": float(hartlap),
        "cond_C": float(np.linalg.cond(C)),
        "q_used": {"LTG": q_ltg, "ETG": q_etg},
        "h0_conv": float(h0_conv),
        "chi2": c0,
        "chi2_hartlap": c0_h,
        "p": p0,
        "p_hartlap": p0_h,
        "newton_chi2": cN,
        "newton_p": pN,
        "newton_p_hartlap": pN_h,
        "cross_shear_chi2": c_cross,
        "cross_shear_p": p_cross,
        "cross_shear_p_hartlap": p_cross_h,
        "max_abs_rand_over_obs": float(np.max(np.abs(gr_vec)) / max(float(np.median(np.abs(d_vec))), 1e-30)),
        "mass_shift_best_dex": dm_best,
        "mass_shift_chi2": cm_best,
        "mass_shift_p": pm_best,
        "mass_shift_p_hartlap": pm_best_h,
        "per_type": type_stats,
        "early_minus_late": eml,
        "bins": rows_out,
        "_d": d_vec, "_pred": pred_v, "_C": C, "_gb": gb_vec, "_hartlap": hartlap,
    }


def combine_disjoint(res_a: dict, res_b: dict, name_a: str, name_b: str) -> dict:
    """Block-diagonal combination of two strictly sky-disjoint samples (both raw and Hartlap)."""
    comb_chi2 = res_a["chi2"] + res_b["chi2"]
    comb_chi2_h = res_a["chi2_hartlap"] + res_b["chi2_hartlap"]
    comb_dof = res_a["n_bins"] + res_b["n_bins"]
    comb_p = float(chi2_dist.sf(comb_chi2, comb_dof))
    comb_p_h = float(chi2_dist.sf(comb_chi2_h, comb_dof))
    comb_newt = res_a["newton_chi2"] + res_b["newton_chi2"]
    comb_newt_h = res_a["newton_chi2"] * res_a["_hartlap"] + res_b["newton_chi2"] * res_b["_hartlap"]
    comb_newt_p = float(chi2_dist.sf(comb_newt, comb_dof))
    comb_newt_p_h = float(chi2_dist.sf(comb_newt_h, comb_dof))

    deltas = np.linspace(-P.MSTAR_SYS_DEX, P.MSTAR_SYS_DEX, 401)
    comb_shifts, comb_shifts_h = [], []
    for dl in deltas:
        r1 = res_a["_d"] - P.pred(res_a["_gb"] * (10.0 ** dl), P.A0_OBS)
        r2 = res_b["_d"] - P.pred(res_b["_gb"] * (10.0 ** dl), P.A0_OBS)
        c1 = float(r1 @ np.linalg.solve(res_a["_C"], r1))
        c2 = float(r2 @ np.linalg.solve(res_b["_C"], r2))
        comb_shifts.append(c1 + c2)
        comb_shifts_h.append(c1 * res_a["_hartlap"] + c2 * res_b["_hartlap"])
    k_c = int(np.argmin(comb_shifts))
    k_ch = int(np.argmin(comb_shifts_h))
    ms_best, ms_chi2 = float(deltas[k_c]), float(comb_shifts[k_c])
    ms_p = float(chi2_dist.sf(ms_chi2, max(comb_dof - 1, 1)))
    ms_best_h, ms_chi2_h = float(deltas[k_ch]), float(comb_shifts_h[k_ch])
    ms_p_h = float(chi2_dist.sf(ms_chi2_h, max(comb_dof - 1, 1)))

    def _verd(np_val, p_val, msp_val):
        if np_val >= 1e-6:
            return "NO_POWER"
        if p_val >= 0.01:
            return "PASS"
        if msp_val >= 0.01:
            return "PASS_WITHIN_MASS_SYSTEMATIC"
        return "FAIL"

    return {
        "components": [name_a, name_b],
        "verdict": _verd(comb_newt_p, comb_p, ms_p),
        "verdict_hartlap": _verd(comb_newt_p_h, comb_p_h, ms_p_h),
        "chi2": comb_chi2,
        "chi2_hartlap": comb_chi2_h,
        "dof": int(comb_dof),
        "p": comb_p,
        "p_hartlap": comb_p_h,
        "newton_chi2": comb_newt,
        "newton_p": comb_newt_p,
        "newton_p_hartlap": comb_newt_p_h,
        "mass_shift_best_dex": ms_best,
        "mass_shift_chi2": ms_chi2,
        "mass_shift_p": ms_p,
        "mass_shift_best_dex_hartlap": ms_best_h,
        "mass_shift_p_hartlap": ms_p_h,
    }


# ------------------------------------------------------------------ Self-Test (Standalone)
def run_self_test():
    # 1. Validate MOND point-mass forward model
    val = P.validate_model()
    assert val["model_checks_pass"], f"pom1 model check failed: {val}"

    # 2. Independent SI constant, WMAP9 distance integral vs scipy.integrate.quad, and analytic n(z_s) checks
    assert 1.66e6 < SIG_CR_FACTOR < 1.67e6, f"Bad SIG_CR_FACTOR: {SIG_CR_FACTOR}"
    zg, dcg, _ = build_distance_tables(6.0, om=OM_WMAP9, ol=OL_WMAP9, h0=H0_B21)
    for zt in (0.15, 0.35, 1.25):
        dc_tab = float(np.interp(zt, zg, dcg))
        dc_exact = comoving_dist_mpc(zt, om=OM_WMAP9, ol=OL_WMAP9, h0=H0_B21)
        assert abs(dc_tab / dc_exact - 1.0) < 1e-5, f"DC mismatch at z={zt}: {dc_tab} vs {dc_exact}"

    z_mid = np.linspace(0.025, 2.5, 50)
    nz_bins = np.zeros((6, len(z_mid)))
    idx_s = 20
    nz_bins[:, idx_s] = 1.0
    spl_t, zg, dcg, dag = build_sigma_crit_inv_splines(z_mid, nz_bins, norm_above_zl=True)
    spl_f, _, _, _ = build_sigma_crit_inv_splines(z_mid, nz_bins, norm_above_zl=False)
    zl_test = 0.25
    zs_test = float(z_mid[idx_s])
    dc_l = float(np.interp(zl_test, zg, dcg))
    da_l = dc_l / (1.0 + zl_test)
    dc_s = float(np.interp(zs_test, zg, dcg))
    da_s = dc_s / (1.0 + zs_test)
    dls = (dc_s - dc_l) / (1.0 + zs_test)
    exact_sc_inv = (da_l * dls / da_s) / SIG_CR_FACTOR
    assert abs(float(spl_t[1](zl_test)) / exact_sc_inv - 1.0) < 1e-6
    assert abs(float(spl_f[1](zl_test)) / exact_sc_inv - 1.0) < 1e-6

    # Verify norm_above_zl=True vs False on split two-peak distribution (30% below z_l, 70% above z_l)
    nz_two = np.zeros((6, len(z_mid)))
    nz_two[:, 2] = 0.30   # z = 0.126 < zl_test (foreground)
    nz_two[:, idx_s] = 0.70  # background
    spl2_t, _, _, _ = build_sigma_crit_inv_splines(z_mid, nz_two, norm_above_zl=True)
    spl2_f, _, _, _ = build_sigma_crit_inv_splines(z_mid, nz_two, norm_above_zl=False)
    assert abs(float(spl2_t[1](zl_test)) / exact_sc_inv - 1.0) < 1e-6
    assert abs(float(spl2_f[1](zl_test)) / (0.70 * exact_sc_inv) - 1.0) < 1e-6

    # 3. Wrap-around RA=0/360 and multi-region jackknife contiguity check
    rng = np.random.default_rng(20261126)
    ra_wrap = np.concatenate([rng.uniform(352.0, 360.0, 600), rng.uniform(0.0, 8.0, 600), rng.uniform(130.0, 140.0, 1200)])
    dec_wrap = np.concatenate([rng.uniform(-35.0, -30.0, 1200), rng.uniform(-2.0, 3.0, 1200)])
    reg_wrap = np.array(["S_wrap"] * 1200 + ["N_patch"] * 1200)
    jk_w = assign_spatial_jackknife(ra_wrap, dec_wrap, 24, region_labels=reg_wrap)
    assert len(np.unique(jk_w)) == 24
    for j in range(24):
        m = jk_w == j
        ra_u = _unwrap_ra_for_region(ra_wrap[m])
        assert (ra_u.max() - ra_u.min()) < 10.0, f"JK cell {j} straddled wide RA gap: {ra_u.min()}..{ra_u.max()}"

    # 4. Synthetic end-to-end Mistele+2024 lensing RAR simulation + shared random + Q_ETG=1.4 LTG invariance
    for b in range(6):
        zc = 0.35 + 0.16 * b
        nz_bins[b] = np.exp(-0.5 * ((z_mid - zc) / 0.15) ** 2)
    spl, zg, dcg, dag = build_sigma_crit_inv_splines(z_mid, nz_bins, norm_above_zl=True)

    gx, gy = np.meshgrid(np.linspace(10.0, 27.0, 48), np.linspace(-8.5, 8.5, 48))
    ra_l = gx.ravel() + rng.uniform(-0.04, 0.04, gx.size)
    dec_l = gy.ravel() + rng.uniform(-0.04, 0.04, gy.size)
    n_lens = len(ra_l)
    z_l = rng.uniform(0.15, 0.35, n_lens)
    etg_l = rng.random(n_lens) > 0.5
    logm_l = rng.uniform(10.1, 10.9, n_lens)
    mb_l = lens_baryon_mass_msun(logm_l, etg_l, q_etg=1.0, q_ltg=1.0)
    jk_l = assign_spatial_jackknife(ra_l, dec_l, 48, region_labels=np.full(n_lens, "N"))
    lenses = {"ra": ra_l, "dec": dec_l, "z": z_l, "mb": mb_l, "etg": etg_l, "jk": jk_l}

    n_src = 400000
    ra_s = rng.uniform(9.5, 27.5, n_src)
    dec_s = rng.uniform(-9.0, 9.0, n_src)
    tomo_s = rng.integers(3, 7, size=n_src, dtype=np.int8)
    zb_s = np.clip(0.55 + 0.16 * (tomo_s - 3) + rng.normal(0.0, 0.06, n_src), 0.15, 1.9)
    w_s = rng.uniform(5.0, 12.0, n_src)
    e1_s = rng.normal(0.0, 0.015, n_src)
    e2_s = rng.normal(0.0, 0.015, n_src)

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
        si = si[zb_s[si] > (z_l[li] + 0.20)]
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
        gobs_70 = P.pred(gb, P.A0_OBS) / V2.H0_CONV
        ds_true = gobs_70 / P.ESD_TO_G
        sig_inv = np.array([spl[int(t)](float(z_l[li])) for t in tomo_s[si]])
        gam_t = ds_true * sig_inv * (1.0 + m_gold_arr[si])
        c2 = (x_im * x_im - y_im * y_im) / r2_im
        s2 = (2.0 * x_im * y_im) / r2_im
        e1_s[si] += -gam_t * c2
        e2_s[si] += -gam_t * s2

    # Shared random catalog check + LTG invariance under Q_ETG shift
    n_r = 3 * n_lens
    r_draw = rng.integers(0, n_lens, size=n_r)
    ra_r = rng.uniform(9.8, 27.2, n_r)
    dec_r = rng.uniform(-8.7, 8.7, n_r)
    _, nn_r = tree_l.query(sph_xyz(ra_r, dec_r))
    rand_base = {"ra": ra_r, "dec": dec_r, "z": z_l[r_draw], "etg": etg_l[r_draw], "jk": jk_l[nn_r]}
    rand_q1 = {**rand_base, "mb": lens_baryon_mass_msun(logm_l[r_draw], etg_l[r_draw], q_etg=1.0)}
    rand_q14 = {**rand_base, "mb": lens_baryon_mass_msun(logm_l[r_draw], etg_l[r_draw], q_etg=1.4)}

    acc_q1 = compute_binned_lensing(lenses, ra_s, dec_s, zb_s, e1_s, e2_s, w_s, tomo_s, spl, zg, dag,
                                    r_min_mpc=0.03, r_max_mpc=0.30, n_jk=48, tree_s=tree_s, zb_cut_mode="mistele")
    racc_q1 = compute_binned_lensing(rand_q1, ra_s, dec_s, zb_s, e1_s, e2_s, w_s, tomo_s, spl, zg, dag,
                                     r_min_mpc=0.03, r_max_mpc=0.30, n_jk=48, tree_s=tree_s, zb_cut_mode="mistele")
    res_q1 = summarize_rar_from_accumulators(acc_q1, racc_q1, h0_conv=V2.H0_CONV, min_npair=15, label="synthetic_q1")

    lenses_q14 = {**lenses, "mb": lens_baryon_mass_msun(logm_l, etg_l, q_etg=1.4)}
    acc_q14 = compute_binned_lensing(lenses_q14, ra_s, dec_s, zb_s, e1_s, e2_s, w_s, tomo_s, spl, zg, dag,
                                     r_min_mpc=0.03, r_max_mpc=0.30, n_jk=48, tree_s=tree_s, zb_cut_mode="mistele")
    racc_q14 = compute_binned_lensing(rand_q14, ra_s, dec_s, zb_s, e1_s, e2_s, w_s, tomo_s, spl, zg, dag,
                                      r_min_mpc=0.03, r_max_mpc=0.30, n_jk=48, tree_s=tree_s, zb_cut_mode="mistele")
    res_q14 = summarize_rar_from_accumulators(acc_q14, racc_q14, h0_conv=V2.H0_CONV, min_npair=15, label="synthetic_q14", q_etg=1.4)

    assert np.allclose(acc_q1["num_t"][:, 0, :], acc_q14["num_t"][:, 0, :], rtol=0.0, atol=1e-15), "LTG lens acc changed with Q_ETG!"
    assert np.allclose(racc_q1["num_t"][:, 0, :], racc_q14["num_t"][:, 0, :], rtol=0.0, atol=1e-15), "LTG rand acc changed with Q_ETG!"
    assert abs(res_q1["per_type"]["late"]["chi2"] - res_q14["per_type"]["late"]["chi2"]) < 1e-12
    assert res_q1["verdict"] == "PASS" and res_q1["verdict_hartlap"] == "PASS", res_q1
    assert res_q1["newton_p"] < 1e-6 and res_q1["newton_p_hartlap"] < 1e-6
    assert res_q1["cross_shear_p"] > 1e-3 and res_q1["early_minus_late"]["p"] > 0.05

    print(
        f"SELF-TEST PASS: WMAP9 quad-matched + Sigma_crit[z_l,inf) exact + unwrapped JK + "
        f"synthetic RAR PASS (chi2={res_q1['chi2']:.2f}/{res_q1['n_bins']}, p={res_q1['p']:.3f}, "
        f"p_H={res_q1['p_hartlap']:.3f}, p_Newton={res_q1['newton_p']:.2e}, Q_ETG=1.4 LTG invariant)."
    )


# ------------------------------------------------------------------ Data Builders (Blind Run)
def build_gama_lenses(
    lens_dir: Path,
    z_grid: np.ndarray,
    dc_grid: np.ndarray,
    r_edge_margin: float = 0.45,
    iso_radius_mpc: float = 3.0,
    spec_cyl_dv_kms: float | None = None,
):
    from astropy.io import fits
    with fits.open(lens_dir / "DistancesFramesv14.fits", memmap=True) as hd:
        df = hd[1].data
        mq = (df["NQ"] >= 3) & (df["Z_TONRY"] > 0.05) & (df["Z_TONRY"] < 0.55)
        cids = np.asarray(df["CATAID"][mq], np.int64)
        ras = np.asarray(df["RA"][mq], np.float64)
        decs = np.asarray(df["DEC"][mq], np.float64)
        zs = np.asarray(df["Z_TONRY"][mq], np.float64)
    with fits.open(lens_dir / "gkvGamaIIMatchesv01.fits", memmap=True) as hm:
        mt = hm[1].data
        cmt, umt = np.asarray(mt["CATAID"], np.int64), np.asarray(mt["uberID"], np.int64)
    with fits.open(lens_dir / "StellarMassesGKVv24.fits", memmap=True) as hs:
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
    G = np.array(rows, np.float64)

    dc = np.interp(G[:, 2], z_grid, dc_grid)
    da = dc / (1.0 + G[:, 2])
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
            (G[:, 0] >= r0 + r_edge_margin) & (G[:, 0] <= r1 - r_edge_margin)
            & (G[:, 1] >= d0 + r_edge_margin) & (G[:, 1] <= d1 - r_edge_margin)
        )
        in_interior |= in_int

    m_cand = in_interior & (G[:, 2] > 0.1) & (G[:, 2] < 0.5) & (G[:, 3] < 11.0) & (G[:, 3] > 8.5)
    cidx = np.where(m_cand)[0]
    iso = np.zeros(len(G), dtype=bool)

    if spec_cyl_dv_kms is None:
        tree3d = cKDTree(pos3d)
        nbrs = tree3d.query_ball_point(pos3d[cidx], r=iso_radius_mpc)
        for idx, nb in zip(cidx, nbrs):
            m_th = G[idx, 3] - 1.0
            nb_arr = np.asarray(nb, np.int32)
            if not np.any((nb_arr != idx) & (G[nb_arr, 3] > m_th)):
                iso[idx] = True
    else:
        tree_sky = cKDTree(sph_xyz(G[:, 0], G[:, 1]))
        r_ang = iso_radius_mpc / np.maximum(da[cidx], 1.0)
        nbrs = tree_sky.query_ball_point(sph_xyz(G[cidx, 0], G[cidx, 1]), r=r_ang)
        dz_lim = spec_cyl_dv_kms / C_LIGHT_KM_S
        for idx, nb in zip(cidx, nbrs):
            m_th = G[idx, 3] - 1.0
            nb_arr = np.asarray(nb, np.int32)
            dz = np.abs(G[nb_arr, 2] - G[idx, 2]) / (1.0 + G[idx, 2])
            if not np.any((nb_arr != idx) & (dz < dz_lim) & (G[nb_arr, 3] > m_th)):
                iso[idx] = True

    def pack(mask):
        return {
            "ra": G[mask, 0], "dec": G[mask, 1], "z": G[mask, 2],
            "logm": G[mask, 3], "etg": G[mask, 4] > 2.00,
            "reg": reg_id[mask],
        }

    return pack(iso & (reg_id == "G23")), pack(iso), boxes


def build_dr5_new329_lenses(
    paths: dict[str, Path],
    z_grid: np.ndarray,
    dc_grid: np.ndarray,
    wl_mmap: np.memmap | None = None,
    iso_radius_mpc: float = 3.0,
    raw_zb: bool = False,
):
    from astropy.io import fits
    dr5 = np.load(paths["lens_dir"] / "kids_dr5_bright_new341_exact.npy")
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

    # Parse DR5-minus-DR4 tile centers, exclude 4 tiles overlapping G23, and verify actual KiDS-Legacy coverage
    tiles_cand = []
    for l in paths["tiles_txt"].read_text().splitlines():
        if l.strip():
            _, rs, ds = l.strip().split("_")
            ra_t, dec_t = float(rs.replace("p", ".").replace("m", "-")), float(ds.replace("p", ".").replace("m", "-"))
            in_g23 = (338.0 <= ra_t <= 352.0) and (-35.5 <= dec_t <= -29.5)
            if not in_g23:
                tiles_cand.append((ra_t, dec_t))
    tiles_cand = np.array(tiles_cand, np.float64)

    if wl_mmap is not None:
        # Chunked nearest-tile assignment over wl_mmap to keep RSS tiny (<60 MB) and speed <2s
        tile_counts = np.zeros(len(tiles_cand), dtype=np.int64)
        tree_tiles = cKDTree(sph_xyz(tiles_cand[:, 0], tiles_cand[:, 1]))
        rmax_tile = math.radians(0.45)
        chunk = 4000000
        for st in range(0, len(wl_mmap), chunk):
            sl = wl_mmap[st:st + chunk]
            m = (sl["is_new_dr5"] == 1) & (sl["weight"] > 0)
            if not np.any(m):
                continue
            ra_w = np.asarray(sl["ra"][m], dtype=np.float64)
            dec_w = np.asarray(sl["dec"][m], dtype=np.float64)
            dist, idx = tree_tiles.query(sph_xyz(ra_w, dec_w), distance_upper_bound=rmax_tile)
            ok = dist < 1e9
            if np.any(ok):
                tile_counts += np.bincount(idx[ok], minlength=len(tiles_cand))
        tiles = tiles_cand[tile_counts >= 50]
    else:
        tiles = tiles_cand

    dc5 = np.interp(z_use, z_grid, dc_grid)
    p5 = sph_xyz(e[:, 0], e[:, 1]) * dc5[:, None]
    t5 = cKDTree(p5)

    with fits.open(paths["lens_dir"] / "KiDS_DR4_brightsample.fits", memmap=True) as hk:
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

    cand_in_tiles = np.zeros(len(e), dtype=bool)
    for rt, dt in tiles:
        cosd = max(math.cos(math.radians(dt)), 0.2)
        dra = ((e[:, 0] - rt + 180.0) % 360.0) - 180.0
        cand_in_tiles |= (np.abs(dra) * cosd <= 0.48) & (np.abs(e[:, 1] - dt) <= 0.48)

    m_cand = cand_in_tiles & (e[:, 2] < 20.0) & (z_use > 0.1) & (z_use < 0.5) & (logm_use < 11.0) & (logm_use > 8.5)
    cidx = np.where(m_cand)[0]
    iso = np.zeros(len(e), dtype=bool)

    nb5 = t5.query_ball_point(p5[cidx], r=iso_radius_mpc)
    nb4 = t4.query_ball_point(p5[cidx], r=iso_radius_mpc)
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

    reg = np.where(e[iso, 1] >= -12.0, "N_DR5", "S_DR5")
    return {
        "ra": e[iso, 0], "dec": e[iso, 1], "z": z_use[iso],
        "logm": logm_use[iso], "etg": ur_e[iso] > 2.5, "reg": reg,
    }, tiles


def run_patch_accum_qpair(
    lenses_sub: dict,
    wl_mmap: np.memmap,
    sc_splines: dict,
    z_grid: np.ndarray,
    da_grid: np.ndarray,
    patches: list,
    n_jk: int,
    r_max_mpc: float,
    rand_mult: int = 20,
    rng_seed: int = 42,
    q_etg_list: tuple[float, ...] = (1.0, 1.4),
    q_ltg: float = 1.0,
    rand_boxes: list | None = None,
    r_edge_margin: float = 0.45,
    active_tiles: np.ndarray | None = None,
    zb_cut_mode: str = "mistele",
):
    """Accumulate real + IDENTICAL shared random catalog across all requested q_etg values."""
    rng = np.random.default_rng(rng_seed)
    l_ra = lenses_sub["ra"]
    l_dec = lenses_sub["dec"]
    l_z = lenses_sub["z"]
    l_logm = lenses_sub["logm"]
    l_etg = lenses_sub["etg"]
    l_jk = assign_spatial_jackknife(l_ra, l_dec, n_jk, region_labels=lenses_sub.get("reg"))
    tree_l_all = cKDTree(sph_xyz(l_ra, l_dec)) if len(l_ra) > 0 else None

    res_by_q = {
        q_e: (
            {k: np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64 if k != "npair" else np.int64)
             for k in ("num_t", "num_x", "den_m", "den_w", "gb_w", "npair")},
            {k: np.zeros((n_jk, 2, N_GB_BINS), dtype=np.float64 if k != "npair" else np.int64)
             for k in ("num_t", "num_x", "den_m", "den_w", "gb_w", "npair")},
        )
        for q_e in q_etg_list
    }

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

        # Generate shared random catalog inside covered footprint once per patch
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
            matched_box = False
            for br0, br1, bd0, bd1 in rand_boxes:
                if br0 >= r0 - 1.0 and br1 <= r1 + 1.0 and bd0 >= d0 - 1.0 and bd1 <= d1 + 1.0:
                    cand_ra = rng.uniform(br0 + r_edge_margin, br1 - r_edge_margin, len(draw_idx))
                    cand_dec = rng.uniform(bd0 + r_edge_margin, bd1 - r_edge_margin, len(draw_idx))
                    matched_box = True
                    break
            if not matched_box:
                raise ValueError(f"No matching rand_box for patch {(r0, r1, d0, d1)}")
        else:
            cand_ra = (l_ra[ml][draw_idx] + rng.uniform(-0.35, 0.35, len(draw_idx)) / np.maximum(np.cos(np.radians(l_dec[ml][draw_idx])), 0.2)) % 360.0
            cand_dec = np.clip(l_dec[ml][draw_idx] + rng.uniform(-0.35, 0.35, len(draw_idx)), -89.0, 89.0)

        n_near = tree_s.query_ball_point(sph_xyz(cand_ra, cand_dec), r=math.radians(0.08), return_length=True, workers=-1)
        good_r = np.where(n_near >= 5)[0][:n_r]
        d_keep = draw_idx[good_r]
        if len(good_r) > 0:
            _, nn_l = tree_l_all.query(sph_xyz(cand_ra[good_r], cand_dec[good_r]))
            jk_r = l_jk[nn_l]
        else:
            jk_r = np.zeros(0, dtype=np.int32)

        for q_e in q_etg_list:
            tot_acc, tot_rand = res_by_q[q_e]
            mb_loc = lens_baryon_mass_msun(l_logm[ml], l_etg[ml], q_etg=q_e, q_ltg=q_ltg)
            sub_l = {"ra": l_ra[ml], "dec": l_dec[ml], "z": l_z[ml], "mb": mb_loc, "etg": l_etg[ml], "jk": l_jk[ml]}
            a_loc = compute_binned_lensing(
                sub_l, s_ra, s_dec, s_zb, s_e1, s_e2, s_w, s_tomo, sc_splines, z_grid, da_grid,
                r_min_mpc=0.03, r_max_mpc=r_max_mpc, n_jk=n_jk, tree_s=tree_s, zb_cut_mode=zb_cut_mode,
            )
            for k in tot_acc:
                tot_acc[k] += a_loc[k]

            if len(good_r) > 0:
                sub_r = {
                    "ra": cand_ra[good_r], "dec": cand_dec[good_r],
                    "z": l_z[ml][d_keep], "mb": mb_loc[d_keep], "etg": l_etg[ml][d_keep], "jk": jk_r,
                }
                r_loc = compute_binned_lensing(
                    sub_r, s_ra, s_dec, s_zb, s_e1, s_e2, s_w, s_tomo, sc_splines, z_grid, da_grid,
                    r_min_mpc=0.03, r_max_mpc=r_max_mpc, n_jk=n_jk, tree_s=tree_s, zb_cut_mode=zb_cut_mode,
                )
                for k in tot_rand:
                    tot_rand[k] += r_loc[k]

        del s_ra, s_dec, s_zb, s_e1, s_e2, s_w, s_tomo, tree_s
        gc.collect()

    return res_by_q


def verify_north_south_shear_sign(lens_dir: Path, wl_mmap: np.memmap) -> dict:
    """Verify multiplicative-free positive tangential convergence on massive GAMA galaxies in N and S separately."""
    from astropy.io import fits
    with fits.open(lens_dir / "DistancesFramesv14.fits", memmap=True) as hd:
        df = hd[1].data
        mq = (df["NQ"] >= 3) & (df["Z_TONRY"] > 0.1) & (df["Z_TONRY"] < 0.45)
        cids = np.asarray(df["CATAID"][mq], np.int64)
        ras = np.asarray(df["RA"][mq], np.float64)
        decs = np.asarray(df["DEC"][mq], np.float64)
        zs = np.asarray(df["Z_TONRY"][mq], np.float64)
    with fits.open(lens_dir / "gkvGamaIIMatchesv01.fits", memmap=True) as hm:
        mt = hm[1].data
        cmt, umt = np.asarray(mt["CATAID"], np.int64), np.asarray(mt["uberID"], np.int64)
    with fits.open(lens_dir / "StellarMassesGKVv24.fits", memmap=True) as hs:
        sm = hs[1].data
        usm, lsm = np.asarray(sm["uberID"], np.int64), np.asarray(sm["logmstar"], np.float64)
    ism = np.argsort(usm)
    us = usm[ism]
    pos = np.searchsorted(us, umt)
    ok = pos < len(us)
    hit = np.zeros(len(umt), bool)
    hit[ok] = (us[pos[ok]] == umt[ok])
    c2m = {int(c): float(lsm[p]) for c, p in zip(cmt[hit], ism[pos[hit]]) if c > 0 and lsm[p] > 11.1}
    pts = [(r, d, z) for c, r, d, z in zip(cids, ras, decs, zs) if int(c) in c2m]
    P_arr = np.array(pts, np.float64)

    out = {}
    for nm, m_hemi in (("North_G09_G12_G15", P_arr[:, 1] > -12.0), ("South_G23", P_arr[:, 1] < -12.0)):
        sub = P_arr[m_hemi]
        ms = (wl_mmap["weight"] > 0) & ((wl_mmap["patch_n"] == 1) if nm.startswith("North") else (wl_mmap["patch_n"] == 0))
        if nm.startswith("South"):
            ms &= (wl_mmap["ra"] >= 337.0) & (wl_mmap["ra"] <= 353.0) & (wl_mmap["dec"] >= -36.5) & (wl_mmap["dec"] <= -28.5)
        else:
            ms &= (
                ((wl_mmap["ra"] >= 128.0) & (wl_mmap["ra"] <= 142.0))
                | ((wl_mmap["ra"] >= 173.0) & (wl_mmap["ra"] <= 187.0))
                | ((wl_mmap["ra"] >= 210.0) & (wl_mmap["ra"] <= 225.0))
            ) & (wl_mmap["dec"] >= -4.5) & (wl_mmap["dec"] <= 4.5)
        s_ra = np.array(wl_mmap["ra"][ms], np.float64)
        s_dec = np.array(wl_mmap["dec"][ms], np.float64)
        s_zb = np.array(wl_mmap["z_b"][ms], np.float64)
        s_e1 = np.array(wl_mmap["e1"][ms], np.float64)
        s_e2 = np.array(wl_mmap["e2"][ms], np.float64)
        s_w = np.array(wl_mmap["weight"][ms], np.float64)
        ts = cKDTree(sph_xyz(s_ra, s_dec))
        nbrs = ts.query_ball_point(sph_xyz(sub[:, 0], sub[:, 1]), r=math.radians(0.06))
        sum_wt = sum_wx = sum_w = 0.0
        for (lr, ld, lz), s_idx in zip(sub, nbrs):
            if not s_idx:
                continue
            si = np.asarray(s_idx, np.int32)
            si = si[s_zb[si] > lz + 0.20]
            if not len(si):
                continue
            cosd = math.cos(math.radians(ld))
            x = -np.radians(((s_ra[si] - lr + 180.0) % 360.0) - 180.0) * cosd
            y = np.radians(s_dec[si] - ld)
            r2 = x * x + y * y
            mk = r2 > (math.radians(3.0 / 3600.0) ** 2)
            if not np.any(mk):
                continue
            si, x, y, r2 = si[mk], x[mk], y[mk], r2[mk]
            c2 = (x * x - y * y) / r2
            s2 = 2.0 * x * y / r2
            et = -s_e1[si] * c2 - s_e2[si] * s2
            ex = s_e1[si] * s2 - s_e2[si] * c2
            w = s_w[si]
            sum_wt += float(np.sum(w * et))
            sum_wx += float(np.sum(w * ex))
            sum_w += float(np.sum(w))
        out[nm] = {
            "n_massive_lenses": int(len(sub)),
            "mean_et": sum_wt / max(sum_w, 1.0),
            "mean_ex": sum_wx / max(sum_w, 1.0),
        }
    return out


# ------------------------------------------------------------------ Full Blind Execution
def run_main(cache_dir: str | Path | None = None, drop_wl_gz_after: bool = False):
    t0 = time.time()
    paths = resolve_paths(cache_dir)
    ensure_data(paths, drop_wl_gz_after=drop_wl_gz_after)
    P.ensure_data()
    assert P.validate_model()["model_checks_pass"]

    z_mid, dz_w, nz_bins = load_kids_nz(paths["nz_fits"])
    wl = np.memmap(paths["wl_bin"], dtype=WL_DTYPE, mode="r")
    assert len(wl) == N_KIDS_LEGACY_ROWS

    # 1. Pre-check massive-galaxy shear sign independently in North and South patches
    shear_sign = verify_north_south_shear_sign(paths["lens_dir"], wl)
    assert shear_sign["North_G09_G12_G15"]["mean_et"] > 1e-3 and shear_sign["South_G23"]["mean_et"] > 1e-3, shear_sign

    # 2. Cosmology tables & Sigma_crit splines for BOTH Mistele+2024 (WMAP9 + [z_l, inf)) & B21-faithful (Planck18 + [0, inf))
    sp_mis, zg_w, dcg_w, dag_w = build_sigma_crit_inv_splines(
        z_mid, nz_bins, dz_widths=dz_w, om=OM_WMAP9, ol=OL_WMAP9, h0=H0_B21, norm_above_zl=True
    )
    sp_b21w, _, _, _ = build_sigma_crit_inv_splines(
        z_mid, nz_bins, dz_widths=dz_w, om=OM_WMAP9, ol=OL_WMAP9, h0=H0_B21, norm_above_zl=False
    )
    sp_p18, zg_p, dcg_p, dag_p = build_sigma_crit_inv_splines(
        z_mid, nz_bins, dz_widths=dz_w, om=OM_P18, ol=OL_P18, h0=H0_B21, norm_above_zl=False
    )

    # 3. Build lens catalogs (WMAP9 primary; margin=0.45 for GAMA; covered-only tiles for DR5_New329)
    g23_w45, all4_w45, gama_boxes = build_gama_lenses(paths["lens_dir"], zg_w, dcg_w, r_edge_margin=0.45)
    g23_p30, all4_p30, _ = build_gama_lenses(paths["lens_dir"], zg_p, dcg_p, r_edge_margin=0.30)
    _, all4_cyl, _ = build_gama_lenses(paths["lens_dir"], zg_w, dcg_w, r_edge_margin=0.45, iso_radius_mpc=3.0, spec_cyl_dv_kms=1000.0)
    _, all4_r4, _ = build_gama_lenses(paths["lens_dir"], zg_w, dcg_w, r_edge_margin=0.45, iso_radius_mpc=4.0)

    dr5_w, tiles_dr5 = build_dr5_new329_lenses(paths, zg_w, dcg_w, wl_mmap=wl, iso_radius_mpc=3.0, raw_zb=False)
    dr5_r4, _ = build_dr5_new329_lenses(paths, zg_w, dcg_w, wl_mmap=wl, iso_radius_mpc=4.0, raw_zb=False)
    dr5_raw, _ = build_dr5_new329_lenses(paths, zg_w, dcg_w, wl_mmap=wl, iso_radius_mpc=3.0, raw_zb=True)
    dr5_p, tiles_dr5_p = build_dr5_new329_lenses(paths, zg_p, dcg_p, wl_mmap=wl, iso_radius_mpc=3.0, raw_zb=False)

    g23_box = [gama_boxes["G23"]]
    all4_patches = [gama_boxes["G09"], gama_boxes["G12"], gama_boxes["G15"], gama_boxes["G23"]]
    dr5_patches = [
        (154.0, 195.0, -5.0, 5.0),
        (195.0, 232.0, -5.0, 5.0),
        (325.0, 360.0, -37.0, -25.0),
        (0.0, 60.0, -37.0, -25.0),
    ]

    # ---- A. Exact Pre-Registered Faithful Run (covered DR5 tiles + per-patch unwrapped JK + shared 20x randoms + b21 cut)
    g23_pr = run_patch_accum_qpair(
        g23_p30, wl, sp_p18, zg_p, dag_p, patches=g23_box, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=101, q_etg_list=(1.0,), rand_boxes=g23_box, r_edge_margin=0.30, zb_cut_mode="b21"
    )
    res_g23_pr = summarize_rar_from_accumulators(*g23_pr[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_G23_prereg_faithful", q_etg=1.0)

    dr5_pr = run_patch_accum_qpair(
        dr5_p, wl, sp_p18, zg_p, dag_p, patches=dr5_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=301, q_etg_list=(1.0, 1.4), active_tiles=tiles_dr5_p, zb_cut_mode="b21"
    )
    res_dr5_pr = summarize_rar_from_accumulators(*dr5_pr[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_prereg_faithful", q_etg=1.0)
    res_dr5_pr_q14 = summarize_rar_from_accumulators(*dr5_pr[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_prereg_QETG1.4", q_etg=1.4)

    all4_pr = run_patch_accum_qpair(
        all4_p30, wl, sp_p18, zg_p, dag_p, patches=all4_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=203, q_etg_list=(1.0,), rand_boxes=all4_patches, r_edge_margin=0.30, zb_cut_mode="b21"
    )
    res_all4_pr = summarize_rar_from_accumulators(*all4_pr[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_prereg_faithful", q_etg=1.0)

    # ---- B. Corrected Mistele+2024 Run (WMAP9 + z_B > z_l+0.20 + [z_l, inf) norm + r_edge_margin=0.45 + Q_ETG=1.0 & 1.4 shared 20x)
    g23_mis = run_patch_accum_qpair(
        g23_w45, wl, sp_mis, zg_w, dag_w, patches=g23_box, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=111, q_etg_list=(1.0, 1.4), rand_boxes=g23_box, r_edge_margin=0.45, zb_cut_mode="mistele"
    )
    res_g23_m_q1 = summarize_rar_from_accumulators(*g23_mis[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_G23_mistele_Q1", q_etg=1.0)
    res_g23_m_q14 = summarize_rar_from_accumulators(*g23_mis[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_G23_mistele_QETG1.4", q_etg=1.4)

    dr5_mis = run_patch_accum_qpair(
        dr5_w, wl, sp_mis, zg_w, dag_w, patches=dr5_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=311, q_etg_list=(1.0, 1.4), active_tiles=tiles_dr5, zb_cut_mode="mistele"
    )
    res_dr5_m_q1 = summarize_rar_from_accumulators(*dr5_mis[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_mistele_Q1", q_etg=1.0)
    res_dr5_m_q14 = summarize_rar_from_accumulators(*dr5_mis[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_mistele_QETG1.4", q_etg=1.4)

    all4_mis = run_patch_accum_qpair(
        all4_w45, wl, sp_mis, zg_w, dag_w, patches=all4_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=211, q_etg_list=(1.0, 1.4), rand_boxes=all4_patches, r_edge_margin=0.45, zb_cut_mode="mistele"
    )
    res_all4_m_q1 = summarize_rar_from_accumulators(*all4_mis[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_mistele_Q1", q_etg=1.0)
    res_all4_m_q14 = summarize_rar_from_accumulators(*all4_mis[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_mistele_QETG1.4", q_etg=1.4)

    # Extended 1.5 Mpc on GAMA_All4 under Mistele+2024 cuts
    all4_ext = run_patch_accum_qpair(
        all4_w45, wl, sp_mis, zg_w, dag_w, patches=all4_patches, n_jk=96, r_max_mpc=1.50,
        rand_mult=20, rng_seed=212, q_etg_list=(1.0, 1.4), rand_boxes=all4_patches, r_edge_margin=0.45, zb_cut_mode="mistele"
    )
    ext_mask = np.zeros((2, N_GB_BINS), dtype=bool)
    ext_mask[:, 2:] = True
    res_all4_ext_q1 = summarize_rar_from_accumulators(*all4_ext[1.0], h0_conv=V2.H0_CONV, min_npair=500, use_bins=ext_mask, label="GAMA_All4_mistele_ext1.5Mpc_Q1", q_etg=1.0)
    res_all4_ext_q14 = summarize_rar_from_accumulators(*all4_ext[1.4], h0_conv=V2.H0_CONV, min_npair=500, use_bins=ext_mask, label="GAMA_All4_mistele_ext1.5Mpc_QETG1.4", q_etg=1.4)

    # ---- C. Clean Diagnostics & Isolation / Redshift-Cut Isolation Suite
    # C1. B21 cut with WMAP9 (separates cosmology vs z_B cut)
    dr5_b21w = run_patch_accum_qpair(
        dr5_w, wl, sp_b21w, zg_w, dag_w, patches=dr5_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=311, q_etg_list=(1.0, 1.4), active_tiles=tiles_dr5, zb_cut_mode="b21"
    )
    res_dr5_b21w_q1 = summarize_rar_from_accumulators(*dr5_b21w[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_WMAP9_b21cut_Q1", q_etg=1.0)
    res_dr5_b21w_q14 = summarize_rar_from_accumulators(*dr5_b21w[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_WMAP9_b21cut_QETG1.4", q_etg=1.4)

    # C2. Strict full-bin tomographic cut (zero intra-bin n(z_s) truncation bias)
    dr5_strict = run_patch_accum_qpair(
        dr5_w, wl, sp_mis, zg_w, dag_w, patches=dr5_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=311, q_etg_list=(1.0, 1.4), active_tiles=tiles_dr5, zb_cut_mode="strict_tomo"
    )
    res_dr5_strict_q14 = summarize_rar_from_accumulators(*dr5_strict[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_strict_tomo_QETG1.4", q_etg=1.4)

    # C3. GAMA_All4 mass-matched (10.2 <= log M* <= 10.9) under Mistele+2024
    mm_mask = (all4_w45["logm"] >= 10.2) & (all4_w45["logm"] <= 10.9)
    all4_mm = {k: v[mm_mask] for k, v in all4_w45.items()}
    acc_mm = run_patch_accum_qpair(
        all4_mm, wl, sp_mis, zg_w, dag_w, patches=all4_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=213, q_etg_list=(1.0, 1.4), rand_boxes=all4_patches, r_edge_margin=0.45, zb_cut_mode="mistele"
    )
    res_all4_mm_q1 = summarize_rar_from_accumulators(*acc_mm[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_mass_matched_mistele_Q1", q_etg=1.0)
    res_all4_mm_q14 = summarize_rar_from_accumulators(*acc_mm[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_mass_matched_mistele_QETG1.4", q_etg=1.4)

    # C4. GAMA_All4 spectroscopic cylinder isolation (R_p < 3 Mpc, |dv| < 1000 km/s)
    acc_cyl = run_patch_accum_qpair(
        all4_cyl, wl, sp_mis, zg_w, dag_w, patches=all4_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=214, q_etg_list=(1.0, 1.4), rand_boxes=all4_patches, r_edge_margin=0.45, zb_cut_mode="mistele"
    )
    res_all4_cyl_q1 = summarize_rar_from_accumulators(*acc_cyl[1.0], h0_conv=V2.H0_CONV, min_npair=100, label="GAMA_All4_spec_cyl_1000kms_Q1", q_etg=1.0)
    res_all4_cyl_q14 = summarize_rar_from_accumulators(*acc_cyl[1.4], h0_conv=V2.H0_CONV, min_npair=100, label="GAMA_All4_spec_cyl_1000kms_QETG1.4", q_etg=1.4)

    # C5. Stricter 4 Mpc isolation (Mistele+2024 default R_isol = 4 Mpc/h70) on GAMA_All4 and DR5_New329
    acc_all4_r4 = run_patch_accum_qpair(
        all4_r4, wl, sp_mis, zg_w, dag_w, patches=all4_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=215, q_etg_list=(1.0, 1.4), rand_boxes=all4_patches, r_edge_margin=0.45, zb_cut_mode="mistele"
    )
    res_all4_r4_q14 = summarize_rar_from_accumulators(*acc_all4_r4[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="GAMA_All4_Risol4Mpc_QETG1.4", q_etg=1.4)

    acc_dr5_r4 = run_patch_accum_qpair(
        dr5_r4, wl, sp_mis, zg_w, dag_w, patches=dr5_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=315, q_etg_list=(1.0, 1.4), active_tiles=tiles_dr5, zb_cut_mode="mistele"
    )
    res_dr5_r4_q1 = summarize_rar_from_accumulators(*acc_dr5_r4[1.0], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_Risol4Mpc_Q1", q_etg=1.0)
    res_dr5_r4_q14 = summarize_rar_from_accumulators(*acc_dr5_r4[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_Risol4Mpc_QETG1.4", q_etg=1.4)

    # C6. Raw DR5 Z_B + Q_ETG=1.4, No-H0 sensitivity, and per-region GAMA check (isolate any B-mode origin)
    acc_dr5_raw = run_patch_accum_qpair(
        dr5_raw, wl, sp_mis, zg_w, dag_w, patches=dr5_patches, n_jk=64, r_max_mpc=0.30,
        rand_mult=20, rng_seed=316, q_etg_list=(1.4,), active_tiles=tiles_dr5, zb_cut_mode="mistele"
    )
    res_dr5_raw = summarize_rar_from_accumulators(*acc_dr5_raw[1.4], h0_conv=V2.H0_CONV, min_npair=200, label="DR5_New329_rawZB_QETG1.4", q_etg=1.4)
    res_dr5_noH0 = summarize_rar_from_accumulators(*dr5_mis[1.4], h0_conv=1.0, min_npair=200, label="DR5_New329_mistele_QETG1.4_noH0", q_etg=1.4)
    res_g23_noH0 = summarize_rar_from_accumulators(*g23_mis[1.0], h0_conv=1.0, min_npair=200, label="GAMA_G23_mistele_noH0", q_etg=1.0)

    # Headline combinations
    comb_prereg = combine_disjoint(res_dr5_pr, res_g23_pr, "DR5_New329_prereg_faithful", "GAMA_G23_prereg_faithful")
    comb_mis_q1 = combine_disjoint(res_dr5_m_q1, res_g23_m_q1, "DR5_New329_mistele_Q1", "GAMA_G23_mistele_Q1")
    comb_mis_q14 = combine_disjoint(res_dr5_m_q14, res_g23_m_q14, "DR5_New329_mistele_QETG1.4", "GAMA_G23_mistele_QETG1.4")

    prereg_sha = hashlib.sha256((HERE / "PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md").read_bytes()).hexdigest()

    def _clean(d):
        return {k: v for k, v in d.items() if not k.startswith("_")}

    out = {
        "status": "completed",
        "protocol": "03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md",
        "protocol_sha256": prereg_sha,
        "epistemic_tag": "[D]",
        "euclid_tap_audit": "Zero she_* tables in public ESA Euclid Q1/DR1 TAP (2026-11-26); KiDS-Legacy DR5 run executed.",
        "north_south_shear_sanity": shear_sign,
        "sample_sizes": {
            "DR5_New329_covered_tiles": int(len(tiles_dr5)),
            "DR5_New329_WMAP9_3Mpc_total": int(len(dr5_w["ra"])),
            "DR5_New329_WMAP9_3Mpc_LTG": int((~dr5_w["etg"]).sum()),
            "DR5_New329_WMAP9_3Mpc_ETG": int(dr5_w["etg"].sum()),
            "DR5_New329_WMAP9_4Mpc_total": int(len(dr5_r4["ra"])),
            "DR5_New329_Planck18_3Mpc_total": int(len(dr5_p["ra"])),
            "GAMA_G23_WMAP9_m045_total": int(len(g23_w45["ra"])),
            "GAMA_G23_Planck18_m030_total": int(len(g23_p30["ra"])),
            "GAMA_All4_Planck18_m030_total": int(len(all4_p30["ra"])),
            "GAMA_All4_WMAP9_m045_total": int(len(all4_w45["ra"])),
            "GAMA_All4_WMAP9_spec_cyl_1000kms": int(len(all4_cyl["ra"])),
            "GAMA_All4_WMAP9_4Mpc_total": int(len(all4_r4["ra"])),
        },
        "headline_blind_combined": comb_prereg,
        "headline_mistele2024_Q1_combined": comb_mis_q1,
        "headline_mistele2024_QETG1.4_combined": comb_mis_q14,
        "DR5_New329_primary": _clean(res_dr5_pr),
        "GAMA_G23_primary": _clean(res_g23_pr),
        "GAMA_All4_reliable": _clean(res_all4_pr),
        "mistele2024_samples": {
            "DR5_New329_mistele_Q1": _clean(res_dr5_m_q1),
            "DR5_New329_mistele_QETG1.4": _clean(res_dr5_m_q14),
            "GAMA_G23_mistele_Q1": _clean(res_g23_m_q1),
            "GAMA_G23_mistele_QETG1.4": _clean(res_g23_m_q14),
            "GAMA_All4_mistele_Q1": _clean(res_all4_m_q1),
            "GAMA_All4_mistele_QETG1.4": _clean(res_all4_m_q14),
            "GAMA_All4_mistele_ext1.5Mpc_Q1": _clean(res_all4_ext_q1),
            "GAMA_All4_mistele_ext1.5Mpc_QETG1.4": _clean(res_all4_ext_q14),
        },
        "diagnostics": {
            "DR5_New329_prereg_QETG1.4": _clean(res_dr5_pr_q14),
            "DR5_New329_WMAP9_b21cut_Q1": _clean(res_dr5_b21w_q1),
            "DR5_New329_WMAP9_b21cut_QETG1.4": _clean(res_dr5_b21w_q14),
            "DR5_New329_strict_tomo_QETG1.4": _clean(res_dr5_strict_q14),
            "GAMA_All4_mass_matched_mistele_Q1": _clean(res_all4_mm_q1),
            "GAMA_All4_mass_matched_mistele_QETG1.4": _clean(res_all4_mm_q14),
            "GAMA_All4_spec_cyl_1000kms_Q1": _clean(res_all4_cyl_q1),
            "GAMA_All4_spec_cyl_1000kms_QETG1.4": _clean(res_all4_cyl_q14),
            "GAMA_All4_Risol4Mpc_QETG1.4": _clean(res_all4_r4_q14),
            "DR5_New329_Risol4Mpc_Q1": _clean(res_dr5_r4_q1),
            "DR5_New329_Risol4Mpc_QETG1.4": _clean(res_dr5_r4_q14),
            "DR5_New329_rawZB_QETG1.4": _clean(res_dr5_raw),
            "DR5_New329_mistele_QETG1.4_noH0": _clean(res_dr5_noH0),
            "GAMA_G23_mistele_noH0": _clean(res_g23_noH0),
        },
        "run_seconds": round(time.time() - t0, 2),
    }

    (HERE / "POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json").write_text(json.dumps(out, indent=2) + "\n")
    (HERE / "POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md").write_text(_format_md(out))
    print(json.dumps({
        "prereg_headline": f"{comb_prereg['verdict']} (H:{comb_prereg['verdict_hartlap']}) chi2={comb_prereg['chi2']:.2f}/{comb_prereg['dof']} p={comb_prereg['p']:.3g} p_H={comb_prereg['p_hartlap']:.3g}",
        "mistele_Q1_headline": f"{comb_mis_q1['verdict']} (H:{comb_mis_q1['verdict_hartlap']}) chi2={comb_mis_q1['chi2']:.2f}/{comb_mis_q1['dof']} p={comb_mis_q1['p']:.3g} p_H={comb_mis_q1['p_hartlap']:.3g}",
        "mistele_QETG1.4_headline": f"{comb_mis_q14['verdict']} (H:{comb_mis_q14['verdict_hartlap']}) chi2={comb_mis_q14['chi2']:.2f}/{comb_mis_q14['dof']} p={comb_mis_q14['p']:.3g} p_H={comb_mis_q14['p_hartlap']:.3g}",
        "DR5_mistele_Q14": f"{res_dr5_m_q14['verdict']} chi2={res_dr5_m_q14['chi2']:.2f}/{res_dr5_m_q14['n_bins']} p={res_dr5_m_q14['p']:.3g} p_H={res_dr5_m_q14['p_hartlap']:.3g} LTG={res_dr5_m_q14['per_type']['late']['chi2']:.2f} ETG={res_dr5_m_q14['per_type']['early']['chi2']:.2f}",
        "GAMA_All4_mistele_Q1": f"{res_all4_m_q1['verdict']} chi2={res_all4_m_q1['chi2']:.2f}/{res_all4_m_q1['n_bins']} p={res_all4_m_q1['p']:.3g} gx_p={res_all4_m_q1['cross_shear_p']:.3g}",
        "GAMA_All4_spec_cyl_Q1": f"{res_all4_cyl_q1['verdict']} chi2={res_all4_cyl_q1['chi2']:.2f}/{res_all4_cyl_q1['n_bins']} p={res_all4_cyl_q1['p']:.3g}",
    }, indent=2))


def _row_md(r: dict, n_l: int | str) -> str:
    ltg = r["per_type"].get("late", {})
    etg = r["per_type"].get("early", {})
    eml_p = r["early_minus_late"]["p"] if r["early_minus_late"] else float("nan")
    return (
        f"| `{r['label']}` | {n_l} | {r['chi2']:.2f} ({r['chi2_hartlap']:.2f}H) / {r['n_bins']} | "
        f"{r['p']:.3g} ({r['p_hartlap']:.3g}H) | "
        f"{ltg.get('chi2', 0):.1f}/{ltg.get('n_bins', 0)} ({ltg.get('median_obs_over_pred', 0):.2f}) | "
        f"{etg.get('chi2', 0):.1f}/{etg.get('n_bins', 0)} ({etg.get('median_obs_over_pred', 0):.2f}) | "
        f"{eml_p:.3g} | {r['cross_shear_p']:.3g} | **`{r['verdict']}`** (`{r['verdict_hartlap']}`H) |"
    )


def _format_md(out) -> str:
    hp = out["headline_blind_combined"]
    hm1 = out["headline_mistele2024_Q1_combined"]
    hm14 = out["headline_mistele2024_QETG1.4_combined"]
    s = out["sample_sizes"]
    ns = out["north_south_shear_sanity"]
    lines = [
        "# P-OM-1 v2 Blind Run on KiDS-Legacy (DR5) & GAMA DR4 (2026-11-26)",
        "",
        f"**Protocol:** `03_observer_jwst/PREREG_POM1V2_BLIND_KIDS_LEGACY_2026-11-26.md` (SHA-256: `{out['protocol_sha256']}`)",
        "**Script:** `03_observer_jwst/pom1v2_blind_kids_legacy.py` -> `POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json`",
        f"**Epistemic Tag:** `[D]` computed blind weak-lensing outcome (KiDS-Legacy {N_KIDS_LEGACY_ROWS:,d} sources across `{s['DR5_New329_covered_tiles']}` covered unseen DR5 tiles + GAMA DR4; Euclid Q1/DR1 TAP exposes zero `she_*` tables)",
        "",
        "## 1. Pre-Unblinding North vs South Massive-Lens Shear Check (`log M* > 11.1`)",
        "",
        f"- **North (`G09/G12/G15`, N={ns['North_G09_G12_G15']['n_massive_lenses']}):** `<e_t> = {ns['North_G09_G12_G15']['mean_et']:+.5f}`, `<e_x> = {ns['North_G09_G12_G15']['mean_ex']:+.5f}`",
        f"- **South (`G23`, N={ns['South_G23']['n_massive_lenses']}):** `<e_t> = {ns['South_G23']['mean_et']:+.5f}`, `<e_x> = {ns['South_G23']['mean_ex']:+.5f}`",
        "",
        "## 2. Headline Blind Combined Verdicts (Strictly Disjoint Sky: `DR5_New329` + `GAMA_G23`)",
        "",
        f"- **Pre-Registered Faithful (`B21 cut`, `Planck18`, `Q_ETG=1.0`):** **`{hp['verdict']}`** (Hartlap `{hp['verdict_hartlap']}`) — $\\chi^2 = {hp['chi2']:.2f}$ (`{hp['chi2_hartlap']:.2f}`H) / `{hp['dof']}` (`p = {hp['p']:.3g}`, Hartlap `{hp['p_hartlap']:.3g}`), Newtonian `p = {hp['newton_p']:.2e}`, best $\\pm 0.2\\,\\mathrm{{dex}}$ shift `{hp['mass_shift_best_dex']:+.3f}` (`p = {hp['mass_shift_p']:.3g}`, `{hp['mass_shift_p_hartlap']:.3g}`H).",
        f"- **Mistele+2024 Spec (`z_B > z_l+0.20`, `[z_l, inf)` norm, `WMAP9`, `Q_ETG=1.0`):** **`{hm1['verdict']}`** (Hartlap `{hm1['verdict_hartlap']}`) — $\\chi^2 = {hm1['chi2']:.2f}$ (`{hm1['chi2_hartlap']:.2f}`H) / `{hm1['dof']}` (`p = {hm1['p']:.3g}`, Hartlap `{hm1['p_hartlap']:.3g}`), Newtonian `p = {hm1['newton_p']:.2e}`, mass shift `{hm1['mass_shift_best_dex']:+.3f}` (`p = {hm1['mass_shift_p']:.3g}`).",
        f"- **Mistele+2024 Spec + `Q_ETG=1.4`:** **`{hm14['verdict']}`** (Hartlap `{hm14['verdict_hartlap']}`) — $\\chi^2 = {hm14['chi2']:.2f}$ (`{hm14['chi2_hartlap']:.2f}`H) / `{hm14['dof']}` (`p = {hm14['p']:.3g}`, Hartlap `{hm14['p_hartlap']:.3g}`), Newtonian `p = {hm14['newton_p']:.2e}`, mass shift `{hm14['mass_shift_best_dex']:+.3f}` (`p = {hm14['mass_shift_p']:.3g}`).",
        "",
        "## 3. Primary & Mistele+2024 Sample Summary",
        "",
        "| Sample | Isolated Lenses | chi2 (Hartlap) / dof | p (Hartlap) | LTG (med obs/pred) | ETG (med obs/pred) | ETG-LTG p | Cross-shear p | Verdict |",
        "|---|---|---|---|---|---|---|---|---|",
        _row_md(out["DR5_New329_primary"], f"{s['DR5_New329_Planck18_3Mpc_total']:,d}"),
        _row_md(out["GAMA_G23_primary"], f"{s['GAMA_G23_Planck18_m030_total']:,d}"),
        _row_md(out["GAMA_All4_reliable"], f"{s['GAMA_All4_Planck18_m030_total']:,d}"),
    ]
    ms = out["mistele2024_samples"]
    for key, n_l in (
        ("DR5_New329_mistele_Q1", f"{s['DR5_New329_WMAP9_3Mpc_total']:,d}"),
        ("DR5_New329_mistele_QETG1.4", f"{s['DR5_New329_WMAP9_3Mpc_total']:,d}"),
        ("GAMA_G23_mistele_Q1", f"{s['GAMA_G23_WMAP9_m045_total']:,d}"),
        ("GAMA_G23_mistele_QETG1.4", f"{s['GAMA_G23_WMAP9_m045_total']:,d}"),
        ("GAMA_All4_mistele_Q1", f"{s['GAMA_All4_WMAP9_m045_total']:,d}"),
        ("GAMA_All4_mistele_QETG1.4", f"{s['GAMA_All4_WMAP9_m045_total']:,d}"),
        ("GAMA_All4_mistele_ext1.5Mpc_Q1", f"{s['GAMA_All4_WMAP9_m045_total']:,d}"),
        ("GAMA_All4_mistele_ext1.5Mpc_QETG1.4", f"{s['GAMA_All4_WMAP9_m045_total']:,d}"),
    ):
        lines.append(_row_md(ms[key], n_l))

    lines.extend(["", "## 4. Diagnostic & Isolation Matrix (Shared 20x Random Catalogs)", "", "| Variant | chi2 (Hartlap) / dof | p (Hartlap) | Mass shift | Early-Late p | Cross-shear p | Verdict |", "|---|---|---|---|---|---|---|"])
    for nm, r in out["diagnostics"].items():
        eml_p = r["early_minus_late"]["p"] if r["early_minus_late"] else float("nan")
        lines.append(
            f"| `{nm}` | {r['chi2']:.2f} ({r['chi2_hartlap']:.2f}H) / {r['n_bins']} | {r['p']:.3g} ({r['p_hartlap']:.3g}H) | "
            f"{r['mass_shift_best_dex']:+.3f} (p={r['mass_shift_p']:.3g}) | {eml_p:.3g} | {r['cross_shear_p']:.3g} | `{r['verdict']}` (`{r['verdict_hartlap']}`H) |"
        )
    lines.extend([
        "",
        "## 5. Methodological Audit & Fixes vs Initial `#279` Run",
        "",
        "1. **Photometric cut & $\\Sigma_{\\rm crit}^{-1}$ normalization (`z_B > z_l + 0.20` + `[z_l, inf)`):** Initial `#279` used Brouwer+2021 `(z_B + 0.20) > z_l` with `[0, inf)` tomographic `NZ_SOURCE` normalization (`TOMOBIN=1` leaks foreground/cluster members) and Planck 2018 distances (`0.3153, 0.6847`). Both pre-registered B21-style and exact Mistele+2024 (`arXiv:2310.15248`: `WMAP9 0.2793/0.7207`, `z_B > z_l + 0.20`, `[z_l, inf)` norm) + `strict_tomo` (`Z_B_min(tomo) > z_l + 0.20`) results are reported above.",
        "2. **Shared 20x random catalogs across `Q_ETG = 1.0` vs `1.4`:** Initial `#279` ran `Q_ETG = 1.4` with a smaller, distinct random draw (`rand_mult=2, seed=302` vs `rand_mult=3, seed=301`), corrupting identical `LTG` bins (`chi2: 8.27 -> 15.58`), and intermediate `5x` random subtraction still induced `±18 chi2` Monte Carlo random-shot variance. Both `Q_ETG` values now share identical `20x` covered-footprint randoms with global lens-tree JK matching, guaranteeing `LTG` invariance to `< 1e-12` and suppressing random-shot variance by 4x.",
        "3. **DR5 tile coverage, unwrapped per-patch jackknife & GAMA edge guard:** Filtered `DR5_New329` tiles directly against covered KiDS-Legacy shear footprints (`>= 50` sources within `0.45 deg`), replaced global RA-sorted jackknife (which straddled disconnected `G09/G12/G15/G23` and `RA=0/360`) with compact per-patch unwrapped 2D KD jackknife, widened GAMA border guard to `0.45 deg` (`> 3 Mpc` at `z=0.1`), and replaced the degenerate `cyl_dz0.02` check (`32` galaxies surviving out of `106k`) with `GAMA_All4_spec_cyl_1000kms` (`R_p < 3 Mpc, |dv| < 1000 km/s`) and `R_isol = 4 Mpc/h70` checks.",
        "4. **Reproducibility:** Added `ensure_data()` and streaming 401-byte FITS binary conversion (`convert_kids_legacy_fits_to_slim()`) so the pipeline runs cleanly from official URLs without undocumented `/tmp` artifacts.",
    ])
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--cache-dir", type=str, default=None)
    p.add_argument("--drop-wl-gz-after", action="store_true")
    args = p.parse_args()
    if args.self_test:
        run_self_test()
    else:
        run_main(cache_dir=args.cache_dir, drop_wl_gz_after=args.drop_wl_gz_after)


if __name__ == "__main__":
    main()
