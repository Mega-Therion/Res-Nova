#!/usr/bin/env python3
"""
Build the z >~ 0.5 per-galaxy Tully-Fisher / kinematic sample CSVs in
02_galaxy_dynamics/highz_data/ from the CDS (VizieR) and Harvard Dataverse source files.

This script transcribes; it does not fit, correct, or convert anything. The only derived
columns are labelled as such (a log10 of a published linear mass, a redshift-band label
read off the published counts, and ID joins that are verified before they are written).

Sources (fixed-width files parsed with the byte ranges of each catalogue ReadMe):
  Ubler+2017, ApJ 842, 121 (arXiv:1703.04321)          CDS J/ApJ/842/121   table3.dat
  Harrison+2017, MNRAS 467, 1965 (arXiv:1701.05561)    CDS J/MNRAS/467/1965 krossv2.dat
  Tiley+2019a, MNRAS 482, 2166 (arXiv:1810.07202)      CDS J/MNRAS/482/2166 tablea1.dat
  Sharma+2021, MNRAS 503, 1753 (arXiv:2005.00279)      CDS J/MNRAS/503/1753 catalog.dat
                                                       + Dataverse doi:10.7910/DVN/MHRG4O FITS
Published fit parameters (no per-galaxy tables exist for these) are written to
HighZ_TF_published_fits.csv from values transcribed out of the arXiv LaTeX sources:
  Tiley+2016, MNRAS 460, 103 (arXiv:1604.06103) Tables 3-4; Ubler+2017 Table 2;
  Tiley+2019a Tables 4-5; Harrison+2017 Sec. 4.2 text.

Source files live in 02_galaxy_dynamics/highz_data/_src/ (gitignored). Run with --fetch
to download any that are missing; every file is sha256-checked before use.

Checks (exit 0 iff all pass):
  C1  every parsed catalogue has exactly the ReadMe "Records" row count
  C2  Ubler table3: z is sorted and splits 65/24/46 at the two z gaps (YJ/H/K counts of
      the paper, Sec. 2.4), so the band label is read off the published counts
  C3  Harrison Mass == 0.2 * 10**(-0.4*(M_H - 4.71)) (the paper's fixed M/L, Sec. 2.2)
  C4  every Tiley KROSS ID is a Harrison KID and Tiley logv2.2 == log10(Harrison V2.2)
      (the Tiley ReadMe says the KROSS values were taken from Harrison)
  C5  Tiley sub-sample counts equal the paper's Table 1: KROSS 259 rot-dom / 112 disky,
      SAMI matched 186/70, SAMI original 309/134
  C6  Sharma VizieR catalog values equal the authors' Dataverse FITS (rel. tol 1e-4);
      proves the VizieR "log" labels on Re/Vout/VPGCout/Sigma/LHa/FHa are wrong
      (values are linear: Re range 0.695-7.73 kpc vs abstract 0.69-7.76 kpc). Tolerance per
      value = max(1e-4 relative, half a unit of the last digit VizieR printed) -- PA is printed
      to 0.001 deg, so a pure relative test misfires on small PAs.
Sabotage tests run 2026-09-16 (in memory, output redirected to the scratchpad): Harrison Mass
x1.01 -> C3 FAIL; Harrison V22 x1.001 -> C4 FAIL; Sharma VPGC_out x1.01 -> C6 FAIL (100x tol);
Sharma PA +0.002 deg -> C6 FAIL (3.4x tol). Clean run: 0.93x tol, exit 0.
"""

import argparse
import hashlib
import math
import sys
import urllib.request
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "02_galaxy_dynamics" / "highz_data"
SRC = OUT / "_src"

CDS = "https://cdsarc.cds.unistra.fr/ftp"
SOURCES = {
    "Ubler2017_J_ApJ_842_121_table3.dat": (
        f"{CDS}/J/ApJ/842/121/table3.dat",
        "b46ee156730a43cfbc89b957d56bd7f244da2535c872f4fc8739e7ec7811ca59",
    ),
    "Ubler2017_J_ApJ_842_121_ReadMe": (
        f"{CDS}/J/ApJ/842/121/ReadMe",
        "3717fc8d8cbc01a3eb80114c47f12585f235f246fbef65120bb9263724018864",
    ),
    "Harrison2017_J_MNRAS_467_1965_krossv2.dat": (
        f"{CDS}/J/MNRAS/467/1965/krossv2.dat",
        "32fc75d86e84fc113e6d86f9160dac90d79f3458bbc9a2f48a1a8de8b2c228dc",
    ),
    "Harrison2017_J_MNRAS_467_1965_ReadMe": (
        f"{CDS}/J/MNRAS/467/1965/ReadMe",
        "587f59d739929ce7c0cbc1afb554c032e754bebf42022601ce84629fe4d35a3b",
    ),
    "Tiley2019a_J_MNRAS_482_2166_tablea1.dat": (
        f"{CDS}/J/MNRAS/482/2166/tablea1.dat",
        "fb56ada2ca9aa1f0cd23dc30bf2d2231076e95f0ddfde095b1f760ee7e80d044",
    ),
    "Tiley2019a_J_MNRAS_482_2166_ReadMe": (
        f"{CDS}/J/MNRAS/482/2166/ReadMe",
        "f90553147d5dd120db266eeb27f8d6bac095d02a641938956561579a0671a29f",
    ),
    "Sharma2021_J_MNRAS_503_1753_catalog.dat": (
        f"{CDS}/J/MNRAS/503/1753/catalog.dat",
        "b91ea011fd98ceacf1b30a18123da2c4a20162d78edbf383fbff37c72b57df45",
    ),
    "Sharma2021_J_MNRAS_503_1753_ReadMe": (
        f"{CDS}/J/MNRAS/503/1753/ReadMe",
        "9435ed65bcd8294bd986a2d0795c5b3841c86252e597679dcc9de9f34a894bf2",
    ),
    "Sharma2021_dataverse_gsharma_2020_catalog.fits": (
        "https://dataverse.harvard.edu/api/access/datafile/4325248",
        "507c2e0834957950f30d72eb99832d95ac75f31628e412351731448be859c942",
    ),
}

# arXiv e-print tarballs read on 2026-09-16 for conventions and published fits
# (not stored in the repo; sha256 recorded so the quotes can be re-checked).
EPRINTS = {
    "1703.04321": "27903922c3362f9bbb989679669cd485510981f91fca6d336d32cd84afda99fb",
    "1701.05561": "1d8a45dce5bf8bd0cd6ba0d1c899bcd3b6112221b5ddd7195635b060b48f378e",
    "1810.07202": "60e435eef57b04ada920fd18bf335f69d0f79f93942626fb30d871eb7f1fd7aa",
    "1811.05982": "180c2cf5a042b20af2db7f846858f29d91e8ffe6e23c6196936f80803364f559",
    "1604.06103": "822440d8bfb96d339f37d0256fe778c303e0a1295d70cad2bcac6540e67a8eb3",
    "1902.09554": "710730417ada00c890b0335990273931a33de865b26d83cfd82f918d07175b00",
    "2005.00279": "6b3289e27e7c45e0f8c738eb7909adcd58f69db8193c8024726ac28cb850f635",
}

FAIL = []


def check(ok, label):
    print(("PASS " if ok else "FAIL ") + label)
    if not ok:
        FAIL.append(label)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_sources(fetch):
    SRC.mkdir(parents=True, exist_ok=True)
    for name, (url, digest) in SOURCES.items():
        p = SRC / name
        if not p.exists():
            if not fetch:
                sys.exit(f"missing {p.relative_to(REPO)}; rerun with --fetch")
            print(f"fetch {url}")
            urllib.request.urlretrieve(url, p)
        got = sha256(p)
        check(got == digest, f"sha256 {name}")


def cut(line, a, b):
    """1-indexed inclusive byte range, as written in CDS ReadMe files."""
    return line[a - 1 : b].strip()


def num(s):
    return float(s) if s != "" else None


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, float):
        return repr(v)
    return str(v)


def write_csv(path, header_lines, columns, rows):
    with open(path, "w", encoding="utf-8") as fh:
        for h in header_lines:
            fh.write("# " + h + "\n" if h else "#\n")
        fh.write(",".join(columns) + "\n")
        for r in rows:
            cells = []
            for c in columns:
                s = fmt(r.get(c))
                if "," in s or '"' in s:
                    s = '"' + s.replace('"', '""') + '"'
                cells.append(s)
            fh.write(",".join(cells) + "\n")
    print(f"wrote {path.relative_to(REPO)} ({len(rows)} rows)")


def read_lines(name):
    with open(SRC / name, encoding="ascii") as fh:
        return [ln.rstrip("\n") for ln in fh if ln.strip()]


# ----------------------------------------------------------------------------- Ubler+2017
def build_ubler():
    lines = read_lines("Ubler2017_J_ApJ_842_121_table3.dat")
    check(len(lines) == 135, f"C1 Ubler table3 rows {len(lines)} == 135")
    rows = []
    for ln in lines:
        rows.append(
            dict(
                seq=int(cut(ln, 1, 3)),
                z=num(cut(ln, 5, 9)),
                logMstar=num(cut(ln, 11, 15)),
                logMbar=num(cut(ln, 17, 21)),
                Vcirc_max_kms=num(cut(ln, 23, 27)),
                sigma0_kms=num(cut(ln, 29, 33)),
            )
        )
    zs = [r["z"] for r in rows]
    check(zs == sorted(zs), "C2 Ubler z sorted by seq")
    gaps = [i for i in range(1, len(zs)) if zs[i] - zs[i - 1] > 0.08]
    check(gaps == [65, 89], f"C2 Ubler z gaps after seq {gaps} == [65, 89] (65/24/46)")
    for i, r in enumerate(rows):
        r["band_derived"] = "YJ" if i < 65 else ("H" if i < 89 else "K")
    hdr = [
        "Ubler et al. 2017, ApJ 842, 121 (doi:10.3847/1538-4357/aa7558; arXiv:1703.04321v2) Table 3",
        '"Physical properties of galaxies in our TFR sample" -- KMOS3D Tully-Fisher sample, 135 SFGs, 0.6<z<2.6.',
        "SOURCE: CDS/VizieR J/ApJ/842/121 table3.dat (Records=135), "
        f"sha256 {SOURCES['Ubler2017_J_ApJ_842_121_table3.dat'][1]}.",
        "  Cross-check 2026-09-16: all 135 rows identical to the full table in the arXiv LaTeX source",
        f"  (e-print sha256 {EPRINTS['1703.04321']}; rows 6-115 sit in a comment block there).",
        "NO galaxy names, NO radii, NO per-galaxy uncertainties are published. Paper Sec. 2.2: adopted",
        "  uncertainties 0.15 dex (M*), 0.20 dex (M_gas), ~0.15 dex (M_bar); Sec. 4.3.2: median Vcirc error 20 km/s.",
        'CONVENTIONS (paper Sec. 1 end): "we adopt a Chabrier (2003) initial mass function (IMF) and a flat LCDM',
        '  cosmology with H0=70 km s^-1 Mpc^-1, Omega_Lambda=0.7, and Omega_m=0.3."',
        "  M* from SED fits (Bruzual & Charlot 2003, Wuyts+2011). M_bar = M* + M_gas, M_gas from the Tacconi+2017",
        '  depletion-time scaling (molecular only; "the inferred gas masses correspond to lower limits").',
        "  Distance: M* and M_bar scale as D_L^2 (flux-based, H0=70 flat LCDM Om=0.3).",
        "VELOCITY: Vcirc_max = maximum of the modelled circular velocity (DYSMAL forward model, thick exponential",
        "  disc n_S=1, q0=0.25). PRESSURE-SUPPORT CORRECTED: v_circ(r)^2 = v_rot(r)^2 + 2 sigma0^2 r/R_d",
        "  (Burkert+2010), paper Sec. 2.3 eq. 1. sigma0 = modelled intrinsic dispersion (km/s).",
        "  Selection: peak velocity covered by data; v_rot,max/sigma0 > sqrt(4.4); no close neighbours.",
        "band_derived is NOT a published per-row column: the paper gives 65/24/46 targets in YJ/H/K",
        "  (z~0.9/1.5/2.3); z is sorted and has gaps exactly after seq 65 (1.032->1.306) and 89 (1.665->2.028).",
        "  Table 2 fits: z~0.9 subsample = YJ (65), z~2.3 subsample = K (46). [D]",
        "Published fixed-slope fits: see HighZ_TF_published_fits.csv (paper Table 2).",
        "Built by scripts/highz_tf_samples_build.py on 2026-09-16.",
    ]
    cols = [
        "seq",
        "z",
        "band_derived",
        "logMstar",
        "logMbar",
        "Vcirc_max_kms",
        "sigma0_kms",
    ]
    write_csv(OUT / "Ubler2017_KMOS3D_TFR.csv", hdr, cols, rows)


# -------------------------------------------------------------------------- Harrison+2017
H17_SPEC = [  # (csv name, a, b, kind) from the J/MNRAS/467/1965 ReadMe byte-by-byte block
    ("KID", 1, 3, "i"),
    ("Name", 5, 26, "s"),
    ("RAdeg", 28, 37, "f"),
    ("DEdeg", 39, 48, "f"),
    ("Kmag_AB", 50, 57, "f"),
    ("rmag_AB", 59, 66, "f"),
    ("zmag_AB", 68, 75, "f"),
    ("MH_AB", 77, 82, "f"),
    ("Mstar_fixedML_Msun", 84, 105, "f"),
    ("VDW12_n", 107, 114, "f"),
    ("im_type", 116, 117, "s"),
    ("quality_flag", 119, 119, "i"),
    ("PA_im_deg", 121, 130, "f"),
    ("R12_kpc", 132, 140, "f"),
    ("e_R12_kpc", 142, 149, "f"),
    ("R_flag", 151, 153, "f"),
    ("b_over_a", 155, 162, "f"),
    ("theta_im_deg", 164, 171, "f"),
    ("e_theta_im_deg", 173, 180, "f"),
    ("theta_flag", 182, 182, "i"),
    ("z", 184, 191, "f"),
    ("F_Ha_mW_m2", 193, 214, "f"),
    ("L_Ha_1e-7W", 216, 237, "f"),
    ("SFR_Msun_yr", 239, 247, "f"),
    ("sigma_tot_kms", 249, 256, "f"),
    ("AGN_flag", 258, 258, "i"),
    ("IRR_flag", 260, 260, "i"),
    ("VEL_PA_deg", 262, 271, "f"),
    ("V22_obs_kms", 273, 281, "f"),
    ("V22_kms", 283, 292, "f"),
    ("VC_obs_kms", 294, 302, "f"),
    ("VC_kms", 304, 313, "f"),
    ("VC_err_lo_kms", 315, 324, "f"),
    ("VC_err_hi_kms", 326, 335, "f"),
    ("EXTRAP_flag", 337, 337, "i"),
    ("KIN_TYPE", 339, 341, "s"),
    ("JS_limit", 343, 343, "s"),
    ("JS_kms_kpc", 344, 350, "f"),
    ("JS_err_lo", 352, 358, "f"),
    ("JS_err_hi", 360, 367, "f"),
    ("JN_kms_kpc", 369, 375, "f"),
    ("sigma0_obs_kms", 377, 384, "f"),
    ("e_sigma0_obs_kms", 386, 393, "f"),
    ("sigma0_kms", 395, 402, "f"),
    ("e_sigma0_kms", 404, 411, "f"),
    ("sigma0_flag", 413, 413, "s"),
    ("RD_RPSF", 415, 424, "f"),
    ("e_RD_RPSF", 426, 435, "f"),
    ("Q_g", 437, 446, "f"),
    ("Q_g_err_hi", 448, 457, "f"),
    ("Q_g_err_lo", 459, 468, "f"),
]


def parse_spec(line, spec):
    r = {}
    for name, a, b, kind in spec:
        s = cut(line, a, b)
        if kind == "s":
            r[name] = s
        elif s == "":
            r[name] = None
        elif kind == "i":
            r[name] = int(s)
        else:
            r[name] = float(s)
    return r


def load_harrison():
    lines = read_lines("Harrison2017_J_MNRAS_467_1965_krossv2.dat")
    check(len(lines) == 586, f"C1 Harrison krossv2 rows {len(lines)} == 586")
    rows = [parse_spec(ln, H17_SPEC) for ln in lines]
    return rows


def build_harrison(rows):
    worst = 0.0
    for r in rows:
        m = r["Mstar_fixedML_Msun"]
        r["logMstar_fixedML_derived"] = round(math.log10(m), 6)
        pred = 0.2 * 10 ** (-0.4 * (r["MH_AB"] - 4.71))
        worst = max(worst, abs(math.log10(m / pred)))
    check(
        worst < 1e-5,
        f"C3 Harrison Mass == 0.2*10^(-0.4(M_H-4.71)), max |dlog| {worst:.2e}",
    )
    hdr = [
        "Harrison et al. 2017, MNRAS 467, 1965 (doi:10.1093/mnras/stx217; arXiv:1701.05561v2) Appendix A catalogue",
        "KROSS (KMOS Redshift One Spectroscopic Survey) V2 catalogue: 586 Halpha-detected SFGs, z=0.6-1.0.",
        "SOURCE: CDS/VizieR J/MNRAS/467/1965 krossv2.dat (Records=586), "
        f"sha256 {SOURCES['Harrison2017_J_MNRAS_467_1965_krossv2.dat'][1]}.",
        "  All 51 ReadMe columns kept, renamed; ReadMe null marker -999 is kept VERBATIM (not blanked);",
        "  blank fields are empty. No rows are cut: filter on quality_flag / AGN_flag / IRR_flag /",
        "  EXTRAP_flag / KIN_TYPE / theta_im_deg (<25 deg excluded in paper) downstream.",
        "  Measured 2026-09-16: -999 in 114 rows (sigma0*, RD_RPSF*, Q_g*); VDW12_n == 0.0 in 478 rows and",
        "  negative apparent mags (rmag 9, Kmag 4, zmag 2 rows) appear in the source -- kept verbatim; the",
        "  ReadMe does not define them as nulls. quality_flag counts 1/2/3/4 = 433/88/31/34.",
        'CONVENTIONS (paper Sec. 1, last paragraph): "we assume a Chabrier IMF (Chabrier 2003), quote all magnitudes as AB',
        '  magnitudes and assume that H0 = 70 km/s/Mpc, Omega_M = 0.3 and Omega_Lambda = 0.7".',
        'STELLAR MASS (paper Sec. 2.2): NOT SED-fitted. "we use interpolated absolute rest-frame H-band AB',
        "  magnitudes (M_H) and convert to stellar masses with a fixed mass-to-light ratio (Upsilon_H=0.2)",
        '  following M* = Upsilon_H x 10^(-0.4 x (M_H - 4.71))"; "The inner 68 per cent range is 0.3 dex',
        '  around the median mass-to-light ratio which we take to be the systematic uncertainty".',
        "  Checked C3: Mstar_fixedML_Msun reproduces that formula from MH_AB to <1e-5 dex. M* scales as D_L^2.",
        "  logMstar_fixedML_derived = log10(Mstar_fixedML_Msun) [derived here]. NO gas / baryonic masses.",
        "RADIUS: R12_kpc = deconvolved continuum half-light radius R_1/2 from broad-band imaging (kpc at H0=70,",
        "  i.e. scales as D_A). R_flag: 1 = upper limit, 0.5 = estimated from kinematic fit.",
        'VELOCITY: VC_kms = intrinsic v_C at 2 R_1/2 "after inclination and beam-smearing corrections" (ReadMe);',
        '  ReadMe: 2 R_1/2 "(i.e. ~=3.4 RD)"; paper Sec. 4.1: "made at 2xR1/2 (i.e., ~3R_D)".',
        "  V22_kms = same at 1.3 R_1/2 (~2.2 R_D). NOT PRESSURE-SUPPORT CORRECTED: the word 'pressure' does",
        "  not occur in the arXiv source; Sharma+2021 (Sharma2021_KROSS_PGC.csv) supplies pressure-gradient",
        "  corrected V for 344 of these galaxies. sigma0_kms = beam-smearing-corrected dispersion.",
        "  EXTRAP_flag: 1 = vC extrapolated >2 pixels beyond the data; 2 = vC estimated by scaling sigma_tot.",
        "  KIN_TYPE: RT+ gold rotation-dominated, RT rotation-dominated, DN dispersion-dominated, X unresolved.",
        "PUBLISHED FIT (Sec. 4.2): see HighZ_TF_published_fits.csv (log v_C = b + a[log M* - 10.10]).",
        "Built by scripts/highz_tf_samples_build.py on 2026-09-16.",
    ]
    cols = [s[0] for s in H17_SPEC]
    cols.insert(cols.index("Mstar_fixedML_Msun") + 1, "logMstar_fixedML_derived")
    write_csv(OUT / "Harrison2017_KROSS.csv", hdr, cols, rows)


# ---------------------------------------------------------------------------- Tiley+2019a
def build_tiley(h17):
    lines = read_lines("Tiley2019a_J_MNRAS_482_2166_tablea1.dat")
    check(len(lines) == 754, f"C1 Tiley tablea1 rows {len(lines)} == 754")
    hk = {r["KID"]: r for r in h17}
    rows, dmax, missing = [], 0.0, 0
    for ln in lines:
        r = dict(
            survey=cut(ln, 1, 13),
            id=int(cut(ln, 15, 20)),
            disky_flag=int(cut(ln, 22, 22)),
            logv22_kms=num(cut(ln, 24, 40)),
            e_logv22=num(cut(ln, 42, 62)),
            logMstar_SED=num(cut(ln, 64, 71)),
            e_logMstar=num(cut(ln, 73, 75)),
            MK_vega=num(cut(ln, 77, 83)),
            e_MK=num(cut(ln, 85, 89)),
        )
        if r["survey"] == "KROSS":
            h = hk.get(r["id"])
            if h is None:
                missing += 1
            else:
                dmax = max(dmax, abs(r["logv22_kms"] - math.log10(h["V22_kms"])))
                for src, dst in [
                    ("z", "H17_z"),
                    ("R12_kpc", "H17_R12_kpc"),
                    ("e_R12_kpc", "H17_e_R12_kpc"),
                    ("R_flag", "H17_R_flag"),
                    ("theta_im_deg", "H17_theta_im_deg"),
                    ("sigma0_kms", "H17_sigma0_kms"),
                    ("e_sigma0_kms", "H17_e_sigma0_kms"),
                    ("VC_kms", "H17_VC_kms"),
                    ("quality_flag", "H17_quality_flag"),
                    ("KIN_TYPE", "H17_KIN_TYPE"),
                    ("AGN_flag", "H17_AGN_flag"),
                    ("IRR_flag", "H17_IRR_flag"),
                ]:
                    r[dst] = h[src]
        rows.append(r)
    check(
        missing == 0 and dmax < 1e-6,
        f"C4 Tiley KROSS IDs in Harrison (missing {missing}), max |dlogv22| {dmax:.2e}",
    )
    cnt = Counter((r["survey"], r["disky_flag"]) for r in rows)
    want = {"KROSS": (259, 112), "SAMI_matched": (186, 70), "SAMI_original": (309, 134)}
    for s, (nrot, ndisk) in want.items():
        got = (cnt[(s, 0)] + cnt[(s, 1)], cnt[(s, 1)])
        check(
            got == (nrot, ndisk), f"C5 Tiley {s} rot-dom/disky {got} == {(nrot, ndisk)}"
        )
    hdr = [
        "Tiley et al. 2019, MNRAS 482, 2166 (doi:10.1093/mnras/sty2794; arXiv:1810.07202v1) Table A1",
        'KROSS-SAMI: "The derived properties used to construct the KROSS, original SAMI, and matched SAMI TFRs',
        'for the rot-dom and disky sub-samples". 754 rows = KROSS 259 (z~0.9) + SAMI_matched 186 + SAMI_original 309',
        "(SAMI rows are the z~0 baseline, 0.004<z<0.095, NOT high-z). NOTE: this is NOT arXiv:1811.05982 (see notes).",
        "SOURCE: CDS/VizieR J/MNRAS/482/2166 tablea1.dat (Records=754), "
        f"sha256 {SOURCES['Tiley2019a_J_MNRAS_482_2166_tablea1.dat'][1]}.",
        "  The Durham release URL named in the paper (astro.dur.ac.uk/KROSS/data.html) returned HTTP 404 on 2026-09-16.",
        'CONVENTIONS (paper Sec. 1 end): "A Nine-Year Wilkinson Microwave Anisotropy Probe (WMAP9; Hinshaw+2013)',
        "  cosmology is used throughout this work. All magnitudes are quoted in the Vega system. All stellar masses",
        '  assume a Chabrier initial mass function." The numerical WMAP9 parameter set is NOT quoted in the paper.',
        "  logMstar_SED: LePhare SED fit (BC03), per ReadMe; e_logMstar is a uniform 0.2. M* scales as D_L^2.",
        "VELOCITY: logv22 = log10 of Harrison+2017 v_2.2 (1.3 r_e ~ 2.2 disc scale lengths), corrected for",
        "  inclination and beam smearing only (paper Sec. 3.4: v2.2 = eps_R,PSF v2.2,obs / sin i). NOT pressure-corrected.",
        "  disky_flag: 0 = rot-dom only (v2.2/sigma + err > 1); 1 = also disky (> 3 and R^2 > 80%).",
        "  rot-dom cuts (paper Table 1): dv/v <= 0.3, r_Halpha,max >= 1.3 r_e, 45 < i < 85 deg.",
        "H17_* COLUMNS ARE A JOIN, not Tiley data: KROSS id == Harrison+2017 KID, verified C4 (all 259 IDs present,",
        "  logv22 == log10(H17 V22_kms) to <1e-6). H17_R12_kpc is the half-light radius at H0=70 (D_A scaling);",
        "  Tiley's WMAP9 masses and Harrison's H0=70 radii therefore mix two cosmologies at the few-% level.",
        "PUBLISHED FITS (Tables 4-5): see HighZ_TF_published_fits.csv.",
        "Built by scripts/highz_tf_samples_build.py on 2026-09-16.",
    ]
    cols = [
        "survey",
        "id",
        "disky_flag",
        "logv22_kms",
        "e_logv22",
        "logMstar_SED",
        "e_logMstar",
        "MK_vega",
        "e_MK",
        "H17_z",
        "H17_R12_kpc",
        "H17_e_R12_kpc",
        "H17_R_flag",
        "H17_theta_im_deg",
        "H17_sigma0_kms",
        "H17_e_sigma0_kms",
        "H17_VC_kms",
        "H17_quality_flag",
        "H17_KIN_TYPE",
        "H17_AGN_flag",
        "H17_IRR_flag",
    ]
    write_csv(OUT / "Tiley2019a_KROSS_SAMI_TFR.csv", hdr, cols, rows)
    return {r["id"]: r for r in rows if r["survey"] == "KROSS"}


# ---------------------------------------------------------------------------- Sharma+2021
S21_SPEC = [  # byte ranges from the J/MNRAS/503/1753 ReadMe; names follow the Dataverse FITS
    ("KID", 1, 3, "i"),
    ("Name", 5, 26, "s"),
    ("Quality", 28, 28, "i"),
    ("Flag_PA", 30, 33, "s"),
    ("RAdeg", 35, 44, "f"),
    ("DEdeg", 46, 55, "f"),
    ("z", 57, 64, "f"),
    ("PA_deg", 66, 73, "f"),
    ("INC_deg", 75, 81, "f"),
    ("MH_AB", 83, 88, "f"),
    ("zmag_AB", 90, 99, "f"),
    ("Kmag_AB", 101, 110, "f"),
    ("Re_kpc", 112, 119, "f"),
    ("Re_err_kpc", 121, 128, "f"),
    ("Vout_kms", 130, 138, "f"),
    ("Vout_err_kms", 140, 149, "f"),
    ("VPGC_out_kms", 151, 159, "f"),
    ("VPGC_out_err_kms", 161, 170, "f"),
    ("Sigma_kms", 172, 180, "f"),
    ("Sigma_err_kms", 182, 191, "f"),
    ("L_Ha_erg_s", 193, 204, "f"),
    ("L_Ha_err_erg_s", 206, 217, "f"),
    ("F_Ha_erg_s_cm2", 219, 230, "f"),
]
S21_FITS = {
    "Quality": "Quality",
    "z": "redshift",
    "PA_deg": "PA",
    "INC_deg": "INC",
    "MH_AB": "Mag_H",
    "Re_kpc": "Re",
    "Re_err_kpc": "Re_err",
    "Vout_kms": "Vout",
    "Vout_err_kms": "Vout_err",
    "VPGC_out_kms": "VPGC_out",
    "VPGC_out_err_kms": "VPGC_out_err",
    "Sigma_kms": "Sigma",
    "Sigma_err_kms": "Sigma_err",
    "L_Ha_erg_s": "L_Ha",
    "L_Ha_err_erg_s": "L_Ha_err",
    "F_Ha_erg_s_cm2": "F_Ha",
}


def build_sharma(h17, t19):
    lines = read_lines("Sharma2021_J_MNRAS_503_1753_catalog.dat")
    check(len(lines) == 344, f"C1 Sharma catalog rows {len(lines)} == 344")
    rows = [parse_spec(ln, S21_SPEC) for ln in lines]
    for ln, r in zip(lines, rows):
        r["_raw"] = {n: cut(ln, a, b) for n, a, b, _ in S21_SPEC}
    try:
        from astropy.io import fits
    except ImportError:
        check(False, "C6 astropy needed to read the Dataverse FITS")
    else:
        data = fits.open(SRC / "Sharma2021_dataverse_gsharma_2020_catalog.fits")[1].data
        byk = {int(k): i for i, k in enumerate(data["KID"])}
        worst, nmatch = 0.0, 0
        for r in rows:
            i = byk.get(r["KID"])
            if i is None:
                continue
            nmatch += 1
            for c, fc in S21_FITS.items():
                ref = float(data[fc][i])
                # tolerance: 1e-4 relative, or half a unit in the last digit VizieR printed
                raw = r["_raw"][c]
                dec = len(raw.split(".")[1]) if ("." in raw and "e" not in raw.lower()) else None
                tol = max(1e-4 * abs(ref), 0.5 * 10.0 ** (-dec) + 1e-12 if dec else 0.0)
                worst = max(worst, abs(r[c] - ref) / tol)
        check(
            nmatch == 344 and worst <= 1.0,
            f"C6 Sharma VizieR == Dataverse FITS for {nmatch}/344 KIDs, "
            f"max |diff|/tol {worst:.2f} (tol = max(1e-4 rel, printed precision))",
        )
        re = [r["Re_kpc"] for r in rows]
        check(
            0.69 <= min(re) < 0.70 and 7.7 < max(re) < 7.8,
            f"C6 Sharma Re is linear kpc: range {min(re):.3f}-{max(re):.3f} (abstract 0.69-7.76)",
        )
    hk = {r["KID"]: r for r in h17}
    for r in rows:
        h = hk.get(r["KID"])
        r["H17_logMstar_fixedML"] = (
            round(math.log10(h["Mstar_fixedML_Msun"]), 6) if h else None
        )
        r["H17_R12_kpc"] = h["R12_kpc"] if h else None
        t = t19.get(r["KID"])
        r["T19_logMstar_SED"] = t["logMstar_SED"] if t else None
        r["T19_disky_flag"] = t["disky_flag"] if t else None
    n_h = sum(r["H17_logMstar_fixedML"] is not None for r in rows)
    n_t = sum(r["T19_logMstar_SED"] is not None for r in rows)
    check(n_h == 344, f"C6 all Sharma KIDs present in Harrison ({n_h}/344)")
    hdr = [
        "Sharma et al. 2021, MNRAS 503, 1753 (doi:10.1093/mnras/stab249; arXiv:2005.00279) released catalogue",
        '"Flat rotation curves of z~1 star-forming galaxies": 344 KROSS galaxies re-modelled with 3D-Barolo.',
        "SOURCE: CDS/VizieR J/MNRAS/503/1753 catalog.dat (Records=344), "
        f"sha256 {SOURCES['Sharma2021_J_MNRAS_503_1753_catalog.dat'][1]};",
        "  cross-checked C6 against the authors' Harvard Dataverse file doi:10.7910/DVN/MHRG4O",
        f"  (gsharma_2020_catalog.fits, md5 43037198cef3cc89376984cb76a8dd61, sha256 {SOURCES['Sharma2021_dataverse_gsharma_2020_catalog.fits'][1]}).",
        "VIZIER LABEL DEFECT: the CDS ReadMe labels Re, Vout, VPGCout, Sigma, LHa, FHa (and their errors) as log",
        "  quantities ([kpc], [km/s], ...). The numbers are LINEAR: they equal the Dataverse FITS columns and Re spans",
        "  0.695-7.73 kpc, matching the abstract's 0.69<=R_e[kpc]<=7.76. Columns here are named as linear.",
        "CONVENTIONS: no cosmology statement found in the arXiv source; Re, M_H, PA, magnitudes are adopted from",
        "  Harrison+2017 (H0=70, Om=0.3, OL=0.7, Chabrier). Quality: 1 best, 2 reasonable, 3 discarded by the authors.",
        "VELOCITY: Vout_kms = 3D-Barolo rotation velocity at R_out = 6.4 R_D, R_D = 0.59 R_e (beam smearing",
        "  handled in 3D; paper Sec. 3.1 figure caption: R_out = R_2opt = 3.78 R_e); VPGC_out_kms = same after",
        "  PRESSURE-GRADIENT CORRECTION (paper Sec. 3.2):",
        "  V_c^PGC = sqrt(V_phi^2 - sigma_R^2 [dln Sigma/dln R + dln sigma_R^2/dln R + (1-alpha)/2]).",
        "  => R_out_kpc = 3.78*Re_kpc (not a column; compute downstream). Sigma_kms = weighted",
        "  mean intrinsic dispersion. L_Ha in erg/s (10^-7 W), F_Ha in erg/s/cm^2 (mW/m^2), no extinction correction.",
        "STELLAR MASS: the paper's LePhare masses (supplied by A. Tiley) are NOT in the released catalogue.",
        f"  T19_* = JOIN to Tiley2019a KROSS rows by KID ({n_t}/344 present; SED masses, WMAP9).",
        f"  H17_* = JOIN to Harrison+2017 by KID ({n_h}/344; fixed M/L=0.2 H-band mass, H0=70; R_1/2 kpc).",
        "Built by scripts/highz_tf_samples_build.py on 2026-09-16.",
    ]
    cols = [s[0] for s in S21_SPEC] + [
        "T19_logMstar_SED",
        "T19_disky_flag",
        "H17_logMstar_fixedML",
        "H17_R12_kpc",
    ]
    write_csv(OUT / "Sharma2021_KROSS_PGC.csv", hdr, cols, rows)


# ------------------------------------------------------------------- published fit params
FIT_COLS = [
    "paper",
    "arxiv",
    "table_or_section",
    "relation",
    "sample",
    "z_range",
    "z_typical",
    "N",
    "form",
    "slope",
    "slope_err",
    "slope_status",
    "zero_point",
    "zero_point_err",
    "pivot",
    "scatter_int",
    "scatter_int_err",
    "offset_vs_z0",
    "offset_vs_z0_err",
    "offset_reference",
    "velocity",
    "pressure_corrected",
    "mass_def",
    "cosmology_imf",
]

U17 = dict(
    paper="Ubler+2017 ApJ 842 121",
    arxiv="1703.04321",
    form="log(M/Msun) = a*log(vcirc/vref) + b; vref=242 km/s (inverse regression, mpfitexy; b bootstrapped)",
    pivot="vref=242 km/s",
    velocity="vcirc,max (DYSMAL max modelled circular velocity)",
    pressure_corrected="yes (Burkert+2010, eq. 1)",
    cosmology_imf="flat LCDM H0=70 Om=0.3 OL=0.7; Chabrier",
)
T16 = dict(
    paper="Tiley+2016 MNRAS 460 103",
    arxiv="1604.06103",
    form="log(M*/Msun) = m*(log V80 - x0) + b; x0 = median log V80 (pivot column)",
    velocity="V80 = arctan-model rotation velocity at r80 (80% of Halpha flux)",
    pressure_corrected="no",
    mass_def="M* SED (HyperZ), uniform +-0.2 dex (Sec. 2.6)",
    cosmology_imf="H0=72 Om=0.27 OL=0.73; Chabrier",
)
T19 = dict(
    paper="Tiley+2019a MNRAS 482 2166",
    arxiv="1810.07202",
    form="hyper-fit orthogonal line; zero_point = log(M*/Msun) at v2.2=100 km/s (Table 4 header)",
    pivot="v2.2=100 km/s",
    velocity="v2.2 at 1.3 r_e (inclination + beam-smearing corrected)",
    pressure_corrected="no",
    mass_def="M* SED (LePhare)",
    cosmology_imf="WMAP9 (parameters not quoted); Chabrier",
)
H17 = dict(
    paper="Harrison+2017 MNRAS 467 1965",
    arxiv="1701.05561",
    form="log v_C = b + a*[log M* - 10.10] (velocity as dependent variable; mpfit; bootstrap errors)",
    pivot="log M* = 10.10",
    velocity="v_C at 2 R_1/2 (inclination + beam-smearing corrected)",
    pressure_corrected="no",
    mass_def="M* = 0.2 L_H (fixed M/L, 0.3 dex systematic)",
    cosmology_imf="H0=70 Om=0.3 OL=0.7; Chabrier",
)


def fitrows():
    R = []

    def add(base, **kw):
        d = dict(base)
        d.update(kw)
        R.append(d)

    u_s = dict(
        relation="sTFR",
        mass_def="M* SED (BC03), 0.15 dex",
        slope=3.60,
        slope_status="fixed to Reyes+2011 (1/0.278); Reyes zero-point shifted -0.034 dex Kroupa->Chabrier",
        offset_reference="Reyes+2011 (Fig. 5 caption)",
    )
    u_b = dict(
        relation="bTFR",
        mass_def="M_bar = M* + M_gas(Tacconi+2017, molecular); ~0.15 dex",
        slope=3.75,
        slope_status="fixed to Lelli+2016 (SPARC BTFR)",
        offset_reference="Lelli+2016 (Fig. 5 caption)",
    )
    for rel in (u_s, u_b):
        b = dict(U17)
        b.update(rel)
        full = 10.50 if rel is u_s else 10.75
        z09 = 10.49 if rel is u_s else 10.68
        z23 = 10.51 if rel is u_s else 10.85
        sc = (0.22, 0.21, 0.26) if rel is u_s else (0.23, 0.22, 0.26)
        off = (-0.44, -0.42) if rel is u_s else (-0.44, -0.27)
        add(
            b,
            table_or_section="Table 2",
            sample="full TFR sample",
            z_range="0.6-2.6",
            N=135,
            zero_point=full,
            zero_point_err=0.03,
            scatter_int=sc[0],
        )
        add(
            b,
            table_or_section="Table 2; Fig. 5",
            sample="YJ subsample",
            z_range="0.602-1.032 (YJ)",
            z_typical="0.9",
            N=65,
            zero_point=z09,
            zero_point_err=0.04,
            scatter_int=sc[1],
            offset_vs_z0=off[0],
        )
        add(
            b,
            table_or_section="Table 2; Fig. 5",
            sample="K subsample",
            z_range="2.028-2.529 (K)",
            z_typical="2.3",
            N=46,
            zero_point=z23,
            zero_point_err=0.05,
            scatter_int=sc[2],
            offset_vs_z0=off[1],
        )

    add(
        T16,
        table_or_section="Table 3",
        relation="M* TFR",
        sample="z~0 comparison (P05+R11+RH04)",
        z_range="~0",
        z_typical="0",
        slope=3.68,
        slope_err=0.08,
        slope_status="free (bisector)",
        zero_point=10.20,
        zero_point_err=0.01,
        pivot="2.17",
        scatter_int=0.16,
        scatter_int_err=0.01,
        mass_def="literature M*, converted to Chabrier",
    )
    add(
        T16,
        table_or_section="Table 3",
        relation="M* TFR",
        sample="KROSS all",
        z_range="0.8-1.0",
        slope=2.1,
        slope_err=0.2,
        slope_status="free (bisector)",
        zero_point=10.06,
        zero_point_err=0.05,
        pivot="2.14",
        scatter_int=0.38,
        scatter_int_err=0.02,
    )
    add(
        T16,
        table_or_section="Table 3",
        relation="M* TFR",
        sample="KROSS disky (V80/sigma>3)",
        z_range="0.8-1.0",
        N=56,
        slope=4.7,
        slope_err=0.4,
        slope_status="free (bisector)",
        zero_point=10.0,
        zero_point_err=0.3,
        pivot="2.25",
        scatter_int=0.25,
        scatter_int_err=0.05,
    )
    add(
        T16,
        table_or_section="Table 4",
        relation="M* TFR",
        sample="KROSS all",
        z_range="0.8-1.0",
        N=210,
        slope=3.68,
        slope_status="fixed to z~0 comparison",
        zero_point=10.08,
        zero_point_err=0.04,
        pivot="2.14",
        scatter_int=0.58,
        scatter_int_err=0.03,
        offset_vs_z0=0.02,
        offset_vs_z0_err=0.08,
        offset_reference="Tiley+2016 z~0 composite",
    )
    add(
        T16,
        table_or_section="Table 4",
        relation="M* TFR",
        sample="KROSS disky (V80/sigma>3)",
        z_range="0.8-1.0",
        N=56,
        slope=3.68,
        slope_status="fixed to z~0 comparison",
        zero_point=10.05,
        zero_point_err=0.05,
        pivot="2.25",
        scatter_int=0.26,
        scatter_int_err=0.05,
        offset_vs_z0=-0.41,
        offset_vs_z0_err=0.08,
        offset_reference="Tiley+2016 z~0 composite",
    )

    t = [
        ("SAMI_original", "rot-dom", "free", 4.0, 0.1, 9.66, 0.03, 309),
        ("SAMI_original", "disky", "free", 4.5, 0.2, 9.37, 0.03, 134),
        ("SAMI_matched", "rot-dom", "free", 3.4, 0.2, 9.87, 0.04, 186),
        (
            "SAMI_matched",
            "rot-dom",
            "fixed (to SAMI_original)",
            4.0,
            None,
            9.88,
            0.04,
            186,
        ),
        ("SAMI_matched", "disky", "free", 4.3, 0.4, 9.44, 0.04, 70),
        (
            "SAMI_matched",
            "disky",
            "fixed (to SAMI_original)",
            4.5,
            None,
            9.41,
            0.04,
            70,
        ),
        ("KROSS", "rot-dom", "free", 3.7, 0.3, 9.88, 0.04, 259),
        ("KROSS", "rot-dom", "fixed (to SAMI_matched)", 3.4, None, 9.89, 0.04, 259),
        ("KROSS", "disky", "free", 5.2, 0.6, 9.19, 0.05, 112),
        ("KROSS", "disky", "fixed (to SAMI_matched)", 4.3, None, 9.35, 0.04, 112),
    ]
    vert = {
        ("SAMI_original", "rot-dom", "free"): (0.53, 0.03),
        ("SAMI_original", "disky", "free"): (0.30, 0.03),
        ("SAMI_matched", "rot-dom", "free"): (0.42, 0.04),
        ("SAMI_matched", "rot-dom", "fixed (to SAMI_original)"): (0.52, 0.04),
        ("SAMI_matched", "disky", "free"): (0.26, 0.05),
        ("SAMI_matched", "disky", "fixed (to SAMI_original)"): (0.28, 0.04),
        ("KROSS", "rot-dom", "free"): (0.66, 0.07),
        ("KROSS", "rot-dom", "fixed (to SAMI_matched)"): (0.61, 0.03),
        ("KROSS", "disky", "free"): (0.39, 0.07),
        ("KROSS", "disky", "fixed (to SAMI_matched)"): (0.33, 0.04),
    }
    for surv, samp, st, s, se, zp, zpe, n in t:
        kw = {}
        if surv == "KROSS" and st.startswith("fixed"):
            kw = dict(
                offset_vs_z0=0.02 if samp == "rot-dom" else -0.09,
                offset_vs_z0_err=0.06,
                offset_reference="KROSS - SAMI_matched, Table 5",
            )
        sv = vert[(surv, samp, st)]
        add(
            T19,
            table_or_section="Table 4" + ("; Table 5" if kw else ""),
            relation="M* TFR",
            sample=f"{surv} {samp}",
            z_range="0.6-1.0 (KROSS)" if surv == "KROSS" else "0.004-0.095 (SAMI)",
            z_typical="0.9" if surv == "KROSS" else "~0",
            N=n,
            slope=s,
            slope_err=se,
            slope_status=st,
            zero_point=zp,
            zero_point_err=zpe,
            scatter_int=sv[0],
            scatter_int_err=sv[1],
            **kw,
        )

    add(
        H17,
        table_or_section="Sec. 4.2 text",
        relation="inverse M* TFR (v_C vs M*)",
        sample="rotation-dominated (v_C/sigma0>1), quality 1-3",
        z_range="0.6-1.0",
        z_typical="0.9",
        slope=0.33,
        slope_err=0.11,
        slope_status="free",
        zero_point=2.12,
        zero_point_err=0.04,
        offset_reference="Reyes+2011: a=0.278+-0.010, b=2.142+-0.004 (no evolution claimed)",
    )
    add(
        H17,
        table_or_section="Sec. 4.2 text",
        relation="inverse M* TFR (v_C vs M*)",
        sample="gold (RT+)",
        z_range="0.6-1.0",
        z_typical="0.9",
        slope=0.39,
        slope_status="free (no errors quoted)",
        zero_point=2.17,
    )
    return R


def build_fits():
    hdr = [
        "Published high-z Tully-Fisher fit parameters, transcribed from the arXiv LaTeX sources (2026-09-16).",
        "e-print sha256: " + "; ".join(f"{k} {v}" for k, v in EPRINTS.items() if v),
        "Scatter columns: Ubler = intrinsic scatter zeta_int in dex of mass (errors not given);",
        "  Tiley+2016 = sigma_int (dex of mass); Tiley+2019a = sigma_int,vert (dex of mass).",
        "Table numbers follow the order of table environments in the arXiv source (VizieR's table3/tablea1",
        "  names agree with that order for Ubler and Tiley+2019a).",
        "Price+2020 (MOSDEF, ApJ 894 91, arXiv:1902.09554) publishes NO TF fit and NO per-galaxy table;",
        "  its Table 4 gives median log10(Mdyn/Mbar) per bin -- not transcribed here (see agent notes).",
        "Tiley+2019b (MNRAS 485 934, arXiv:1811.05982) publishes no TF fit and no tables (stacked rotation curves).",
        "Distance: every zero-point is in log M, and M scales as D_L^2 under each paper's cosmology.",
    ]
    rows = fitrows()
    write_csv(OUT / "HighZ_TF_published_fits.csv", hdr, FIT_COLS, rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument(
        "--fetch", action="store_true", help="download missing source files"
    )
    args = ap.parse_args()
    ensure_sources(args.fetch)
    if FAIL:
        print(f"{len(FAIL)} FAILED: {FAIL}")
        return 1
    build_ubler()
    h17 = load_harrison()
    build_harrison(h17)
    t19 = build_tiley(h17)
    build_sharma(h17, t19)
    build_fits()
    print(f"{len(FAIL)} failed checks")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
