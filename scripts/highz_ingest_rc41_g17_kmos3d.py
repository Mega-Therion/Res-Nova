#!/usr/bin/env python3
"""Ingest per-galaxy high-z kinematic/structural tables into
02_galaxy_dynamics/highz_data/ with provenance headers.

Sources (all pinned by sha256; the source files live in the gitignored
02_galaxy_dynamics/highz_data/_src/ and are NOT committed):

  RC41  Genzel et al. 2020, ApJ 902, 98  (arXiv:2006.03046v2)  Table 1 + Table D1
  G17   Genzel et al. 2017, Nature 543, 397 (arXiv:1703.04310v1) Table 1
  KMOS3D Wisnioski et al. 2019, ApJ 886, 124 (arXiv:1909.11096v1) VizieR J/ApJ/886/124
        table5 + table6, cross-checked against the MPE release FITS catalogs.

The two Genzel papers are Word-generated PDFs with no TeX source on arXiv
(arXiv e-print endpoint serves the PDF). Numbers are taken from the PDF text
layer (pdftotext -layout), which was checked by eye against 450-dpi renders of
the same pages; the script then runs internal-consistency validators that fail
loudly on any extraction error. Only the 'mode' and 'environment' text cells
and the multi-line galaxy-name cells are transcribed from the rendered pages
(the text layer splits them across lines); they are not used numerically.

Nothing here computes a0. Derived columns are labelled 'derived_' and their
formula is stated in the file header.

Usage:  python3 scripts/highz_ingest_rc41_g17_kmos3d.py
Exit 0 only if every sha256 matches and every validator passes.
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "02_galaxy_dynamics" / "highz_data"
SRC = OUT / "_src"
RC100_CSV = OUT / "RC100_NestorShachar2023_table3_transcribed.csv"

SOURCES = {
    "arXiv_2006.03046_eprint.pdf": (
        "https://arxiv.org/pdf/2006.03046v2  (identical bytes served by https://export.arxiv.org/e-print/2006.03046)",
        "a8bf2f52caa7f9eb387c8c87429d0e2bad11308c33a1973de4f9770410c3f7d6",
    ),
    "arXiv_1703.04310_eprint.pdf": (
        "https://arxiv.org/pdf/1703.04310v1  (identical bytes served by https://export.arxiv.org/e-print/1703.04310)",
        "9926059ed950486e6982e3ec612303b4415832a3a01c091fc0035e564259e5d4",
    ),
    "J_ApJ_886_124_table5.dat": (
        "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/886/124/table5.dat",
        "24b1b12ec42c1d2dfc6aca7d3e965fd78b3c8ff9a68e36a7441f9a1448196a95",
    ),
    "J_ApJ_886_124_table6.dat": (
        "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/886/124/table6.dat",
        "fb37854047c6fb2d2e77db28f439e553e12afea3227052238bd48d3ebc804459",
    ),
    "KMOS3D_J_ApJ_886_124_ReadMe.txt": (
        "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/886/124/ReadMe",
        "7c0c129531f823c1cc603a195667c6c2b2e19f308a2c095868a9d5d2c62627bf",
    ),
    "k3d_fnlsp_table_v3.fits": (
        "https://www.mpe.mpg.de/resources/KMOS3D/catalogs/k3d_fnlsp_table_v3.fits.tgz (extracted)",
        "be2716e3e73755c03b94e55f1ae8aaf8f447434eeefef9a3e45a97ad302b1dea",
    ),
    "k3d_fnlsp_table_hafits_v3.fits": (
        "https://www.mpe.mpg.de/resources/KMOS3D/catalogs/k3d_fnlsp_table_hafits_v3.fits.tgz (extracted)",
        "7ef8269d19e95652dc0f7891e4a1c42a03c45393aadc0f8b0ec0815237398711",
    ),
    "arXiv_1909.11096v1_Wisnioski2019.pdf": (
        "https://arxiv.org/pdf/1909.11096v1",
        "9c36ae7d8a65be7a6af6ae1210d1f6c2f0b5deed76321f29df9d2b4a654b2c73",
    ),
}

FAILS: list[str] = []
T1_NOTES: list[str] = []


def check(cond: bool, msg: str) -> bool:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)
    return cond


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sources() -> None:
    missing = []
    for name, (url, digest) in SOURCES.items():
        p = SRC / name
        if not p.exists():
            missing.append((name, url))
            continue
        check(sha256(p) == digest, f"sha256 {name}")
    if missing:
        for name, url in missing:
            print(f"MISSING {name}: fetch from {url} into {SRC.relative_to(REPO)}/")
        sys.exit(2)


def pdftext(pdf: str, page: int) -> str:
    return subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(SRC / pdf), "-"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


NUM = re.compile(r"^-?\d+(?:\.\d+)?(?:E[+-]\d+)?$")


def norm(s: str) -> str:
    return re.sub(r"[\s_\-()/]", "", s.upper())


def aliases_of(names: list[str]) -> set[str]:
    out: set[str] = set()
    for name in names:
        out.add(norm(name))
        paren = re.findall(r"\(([^)]*)\)", name)
        out.update(norm(x) for x in paren)
        rest = re.sub(r"\([^)]*\)", " ", name)
        for part in re.split(r"[/\s]+", rest):
            if not part:
                continue
            out.add(norm(part))
            out.update(norm(q) for q in part.split("-") if q)
    return {
        a for a in out if len(a) >= 5 and re.search(r"[A-Z]", a) and re.search(r"\d", a)
    }


def load_rc100() -> list[dict]:
    rows = []
    with open(RC100_CSV) as f:
        for r in csv.DictReader(line for line in f if not line.startswith("#")):
            rows.append(r)
    return rows


def rel(p: Path) -> str:
    return str(p.relative_to(REPO))


def write_csv(
    path: Path, header_lines: list[str], fieldnames: list[str], rows: list[dict]
) -> None:
    with open(path, "w", newline="") as f:
        for line in header_lines:
            f.write("# " + line + "\n" if line else "#\n")
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(
                {k: ("NA" if r.get(k) in (None, "") else r[k]) for k in fieldnames}
            )
    print(f"wrote {rel(path)} ({len(rows)} rows)")


# ---------------------------------------------------------------- RC41 (Genzel+2020)
RC41_T1_NAMES = [
    "EGS3_10098/EGS4_30084",
    "U3_21388",
    "EGS4_21351",
    "EGS4_11261",
    "GS4_13143",
    "U3_05138",
    "GS4_03228",
    "GS4_32976",
    "COS4_01351",
    "COS3_22796",
    "U3_15226",
    "GS4_05881",
    "COS3_16954",
    "COS3_04796",
    "EGS_13035123",
    "EGS_13004291",
    "EGS_13003805",
    "G4-38153",
    "G4_24985",
    "zC_403741",
    "D3a_6397",
    "EGS_13011166",
    "GS4_43501 (GK 2438)",
    "GS4_14152",
    "K20_ID9-GS4_27404",
    "zC_405501",
    "SSA22_MD41",
    "BX389",
    "zC_407302",
    "GS3_24273",
    "zC_406690",
    "BX610",
    "K20_ID7-GS4_29868",
    "K20_ID6-GS3_22466-GS4_33689",
    "zC_400569",
    "BX482",
    "COS4_02672",
    "D3a_15504",
    "D3a_6004",
    "GS4_37124",
    "GS4_42930 (GK 2363)",
]
# Table D1 spellings; multi-line cells joined with the printed separator or one space.
RC41_D1_NAMES = [
    "EGS3_10098/EGS4_30084",
    "U3_21388",
    "EGS4_21351",
    "EGS4_11261",
    "GS4_13143",
    "U3_05138",
    "GS4_03228",
    "GS4_32796",
    "COS4_01351",
    "COS3_22796",
    "U3_15226",
    "GS4_05881",
    "COS3_16954",
    "COS3_04796",
    "EGS_13035123",
    "EGS_13004291",
    "EGS_13003805",
    "EGS4_38153",
    "EGS4_24985",
    "zC_403741",
    "D3a_6397",
    "EGS_13011166",
    "GS4_43501 GK_2438",
    "GS4_14152",
    "K20_ID9-GS4_27404",
    "zC_405501",
    "SSA22_MD41",
    "Q2343-BX_389",
    "zC_407302",
    "GS3_24273",
    "zC_406690",
    "Q2343-BX_610",
    "K20_ID7-GS4_29868",
    "K20_ID6-GS3_22466-GS4_33689",
    "zC_400569",
    "Q2346-BX_482",
    "COS4_02672",
    "D3a_15504",
    "D3a_6004",
    "GS4_37124",
    "GS4_42930 GK_2363",
]
# Table D1 column 33 'Mode', transcribed from the rendered page 53 (text layer splits cells).
RC41_MODE = [
    "NOEMA",
    "KMOS",
    "NOEMA",
    "NOEMA",
    "KMOS",
    "SINF-J",
    "KMOS",
    "KMOS",
    "SINF-J+KMOS",
    "SINF-J",
    "KMOS",
    "KMOS",
    "SINF-J",
    "SINF-J",
    "NOEMA",
    "NOEMA",
    "NOEMA",
    "NOEMA",
    "LBT/NOEMA",
    "SINF-H100+H250",
    "SINF-K100",
    "LBT/NOEMA",
    "SINF-H250/KMOS",
    "SINF-H250",
    "SINF-K250",
    "SINF-K100/K250",
    "SINF-K250",
    "SINF-K100/K250",
    "SINF-K100",
    "KMOS",
    "SINF-K100",
    "SINF-K100/K250",
    "SINF-K100/K250+KMOS",
    "SINF-K100/K250+KMOS",
    "SINF-K100",
    "SINF-K100/K250",
    "SINF-K250+KMOS",
    "SINF-K100/K250",
    "SINF-K100/K250",
    "KMOS",
    "SINF-K100",
]
# Table 1 column 11 'satellite/companion/merger', transcribed from rendered page 15.
RC41_ENV = {
    5: "interaction",
    6: "companion",
    13: "companion?",
    14: "satellite",
    16: "late stage merger",
    26: "interacting group with 3 members",
    28: "satellite",
    29: "satellite",
    31: "interacting fluffy satellite",
    33: "two companions?",
    34: "minor merger",
    35: "group with 3 members",
    36: "interacting group with 3 members",
    37: "companion",
    38: "interacting satellite",
    39: "companion?",
}

D1_COLS = [  # (printed column number, csv name, header as printed)
    (7, "logMstar_fit", "logM* (M_sun)"),
    (8, "logMDM_Moster18", "logM_DM (M_sun) Moster18"),
    (9, "logMgas", "logM_gas (M_sun)"),
    (10, "logMbar", "logM_baryon (M_sun)"),
    (11, "dlogMbar_fit_minus_input", "DlogM_baryon (M_sun) fit-input"),
    (12, "md_baryon_Moster18", "m_d,baryon Moster18"),
    (13, "md_baryon_prime_fDM_NFW", "m_d,baryon' f_DM & NFW"),
    (14, "dlogSFR_MS_W14", "dlog(SFR/SFR(MS)) W14"),
    (15, "SFR_Msun_yr", "SFR (M_sun/yr)"),
    (16, "Vc_Re_kms", "v_c (R_e) (km/s)"),
    (17, "sigma0_kms", "sigma_0 (km/s)"),
    (18, "Re_kpc", "R_e (kpc)"),
    (19, "nS", "n_S"),
    (20, "inclination_deg", "inclination (deg)"),
    (21, "BT_dyn", "B/T"),
    (22, "Rvir_kpc_Moster18", "R_virial (kpc) Moster18"),
    (23, "SigmaDM_Re_Moster18_Msun_kpc2", "S_DM(R_e) (M_sun kpc^-2) Moster18"),
    (24, "SigmaDM_Re_fit_Msun_kpc2", "S_DM(R_e) (M_sun kpc^-2) from fit"),
    (25, "dMDM_Re_deficit_data_minus_Moster18", "DM_DM(R_e)-deficit data-Moster18"),
    (
        26,
        "lambda_jbar_over_jDM_thick_turb",
        "lambda'(j_baryon/j_DM) thick, turbulent disk",
    ),
    (27, "fDM_Re", "f_DM (R_e)"),
    (28, "e_fDM_Re", "Df_DM"),
    (29, "alpha_inner", "alpha_inner"),
    (30, "e_alpha_inner", "Dalpha_inner"),
    (31, "Rout_over_Re", "R_out/R_e"),
    (32, "c_halo", "c DM-halo"),
]


def parse_rc41() -> list[dict]:
    pdf = "arXiv_2006.03046_eprint.pdf"
    # ---- Table D1 (page 53)
    d1_text = pdftext(pdf, 53)
    d1 = {}
    for line in d1_text.splitlines():
        m = re.match(r"^\s*(\d{1,2})\s+(.*)$", line)
        if not m:
            continue
        toks = m.group(2).split()
        nums = [t for t in toks if NUM.match(t)]
        if len(nums) < 27:
            continue
        row = int(m.group(1))
        fw = [i for i, t in enumerate(toks) if re.match(r'^\d*\.?\d+"$', t)]
        if not fw:  # the printed column-number header line has no FWHM cell
            continue
        check(len(fw) == 1, f"RC41 D1 row {row}: one FWHM token")
        vals = []
        for t in toks[: fw[0]]:
            if NUM.match(t):
                vals.append(t)
        check(
            len(vals) == 26,
            f"RC41 D1 row {row}: 26 numeric cells for cols 7-32 (got {len(vals)})",
        )
        tint = toks[fw[0] + 1]
        d1[row] = dict(zip([c[1] for c in D1_COLS], vals))
        d1[row]["FWHM_arcsec"] = toks[fw[0]].rstrip('"')
        d1[row]["Tint_h"] = tint
    check(
        sorted(d1) == list(range(1, 42)), f"RC41 D1: rows 1..41 present (got {len(d1)})"
    )
    for i, nm in enumerate(RC41_D1_NAMES, 1):
        first = re.split(r"[/\s]", nm)[0].split("-")[0]
        check(
            first in d1_text,
            f"RC41 D1 name token '{first}' (row {i}) present in text layer",
        )

    # ---- Table 1 (page 15)
    t1_text = pdftext(pdf, 15).split("Table 1. Overview")[0]
    t1 = []
    for line in t1_text.splitlines():
        fields = [f for f in re.split(r"\s{2,}", line.strip()) if f]
        zi = next(
            (i for i, f in enumerate(fields) if re.match(r"^[0-2]\.\d\d$", f)), None
        )
        if zi is None:
            continue
        run = []
        started = False
        for f in fields[zi + 1 :]:
            if NUM.match(f):
                run.append(f)
                started = True
            elif started:
                break
        if len(run) < 6:
            continue
        t1.append((fields[zi], run))
    check(len(t1) == 41, f"RC41 Table 1: 41 galaxy rows parsed (got {len(t1)})")

    rows = []
    for i in range(41):
        n = i + 1
        z, run = t1[i]
        if len(run) == 7:
            incl, vc, re_, kpcas, ms, btopt, btdyn = run
        elif len(run) == 6:
            incl, vc, re_, kpcas, ms, btdyn = run
            btopt = ""
        else:
            check(False, f"RC41 T1 row {n}: numeric run length {len(run)} not 6/7")
            continue
        d = d1[n]
        # cross-table consistency: Table 1 and Table D1 print the same quantities
        di = abs(float(incl) - float(d["inclination_deg"]))
        check(
            di <= 0.5,
            f"RC41 row {n}: inclination T1 {incl} ~ D1 {d['inclination_deg']} (<=0.5 deg)",
        )
        if di > 0:
            T1_NOTES.append(
                f"row {n}: inclination printed {incl} in Table 1 but {d['inclination_deg']} in Table D1"
            )
        check(
            float(vc) == float(d["Vc_Re_kms"]),
            f"RC41 row {n}: v_c(R_e) T1 {vc} == D1 {d['Vc_Re_kms']}",
        )
        check(
            float(re_) == float(d["Re_kpc"]),
            f"RC41 row {n}: R_e T1 {re_} == D1 {d['Re_kpc']}",
        )
        check(
            float(btdyn) == float(d["BT_dyn"]),
            f"RC41 row {n}: B/T dyn T1 {btdyn} == D1 {d['BT_dyn']}",
        )
        # baryon-mass identity: logMbar = log10(10^logM* + 10^logMgas) (D1 cols 7,9,10)
        lm = math.log10(10 ** float(d["logMstar_fit"]) + 10 ** float(d["logMgas"]))
        check(
            abs(lm - float(d["logMbar"])) <= 0.011,
            f"RC41 row {n}: log10(M*+Mgas)={lm:.3f} vs logMbar {d['logMbar']}",
        )
        r = {
            "rc41_row": n,
            "galaxy_T1": RC41_T1_NAMES[i],
            "galaxy_D1": RC41_D1_NAMES[i],
            "z": z,
            "kpc_per_arcsec_T1": kpcas,
            "logMstar_HSTinput_T1": ms,
            "BT_optical_T1": btopt,
            "inclination_T1": incl,
            "environment_T1": RC41_ENV.get(n, ""),
            "mode": RC41_MODE[i],
        }
        r.update(d)
        r["derived_logMbar_input"] = (
            f"{float(d['logMbar']) - float(d['dlogMbar_fit_minus_input']):.2f}"
        )
        rows.append(r)
    return rows


# ---------------------------------------------------------------- G17 (Genzel+2017)
def parse_g17() -> list[dict]:
    text = pdftext("arXiv_1703.04310_eprint.pdf", 5)
    block = text.split(
        "Table 1. Physical Parameters of Observed Star-Forming Galaxies"
    )[1]
    block = block.split("Total circular velocity at the half-light radius")[0]
    lines = block.splitlines()

    def row(pattern: str, occurrence: int = 0) -> list[str]:
        hits = [ln for ln in lines if re.search(pattern, ln)]
        check(
            len(hits) > occurrence, f"G17 Table 1 row /{pattern}/ #{occurrence} found"
        )
        fields = [f for f in re.split(r"\s{2,}", hits[occurrence].strip()) if f]
        vals = fields[-6:]
        check(len(vals) == 6, f"G17 row /{pattern}/: 6 values")
        return vals

    names = [
        f
        for f in re.split(
            r"\s{2,}", next(ln for ln in lines if "COS4 01351" in ln).strip()
        )
        if f
    ]
    check(
        names
        == [
            "COS4 01351",
            "D3a 6397",
            "GS4 43501",
            "zC 406690",
            "zC 400569",
            "D3a 15504",
        ],
        f"G17 galaxy names {names}",
    )
    z = row(r"^\s*redshift\s")
    kpcas = row(r"kpc/arcsec")
    mstar = row(r"^\s*M\* \(10")
    mbar_prior = row(r"Mbaryon\(gas\+stars\) \(10")
    r_h = row(r"H-band R1/2 \(kpc\)")
    incl = row(r"inclination")
    conc = row(r"concentration parameter c")
    vc = row(r"vc\(R1/2\) \(km/s\)")
    r_n1 = row(r"R1/2\(n=1\) \(kpc\)")
    sig = row(r"^\s*\S?0 \(km/s\)")
    mbar_fit = row(r"including bulge")
    bt = row(r"Mbulge/Mbaryon")
    fdm = row(r"fDM\(R1/2\)")

    def pm(s: str) -> tuple[str, str]:
        m = re.match(r"^([\d.]+)\s*±\s*([\d.]+)$", s)
        check(m is not None, f"G17 value±error parse '{s}'")
        return m.group(1), m.group(2)

    out = []
    for i in range(6):
        ms, ems = pm(mstar[i])
        mb, emb = pm(mbar_prior[i])
        rh, erh = pm(r_h[i])
        inc, einc = pm(incl[i])
        m = re.match(r"^([\d.]+)\s*\((±|<)([\d.]+)\)$", fdm[i])
        check(m is not None, f"G17 fDM parse '{fdm[i]}'")
        f_val, kind, f_err = m.groups()
        # stellar + gas prior vs baryon prior: must not be smaller than M* (sanity)
        check(
            float(mb) >= float(ms), f"G17 {names[i]}: Mbar prior {mb} >= M* prior {ms}"
        )
        out.append(
            {
                "galaxy": names[i],
                "z": z[i],
                "kpc_per_arcsec": kpcas[i],
                "Mstar_prior_1e11Msun": ms,
                "e_Mstar_prior_1e11Msun": ems,
                "Mbar_prior_1e11Msun": mb,
                "e_Mbar_prior_1e11Msun": emb,
                "R12_Hband_prior_kpc": rh,
                "e_R12_Hband_prior_kpc": erh,
                "inclination_deg": inc,
                "e_inclination_deg": einc,
                "c_halo": conc[i],
                "Vc_R12_kms": vc[i],
                "R12_n1_fit_kpc": r_n1[i],
                "sigma0_kms": sig[i],
                "Mbar_fit_incl_bulge_1e11Msun": mbar_fit[i],
                "Mbulge_over_Mbar": bt[i],
                "fDM_R12": f_val,
                "fDM_R12_2rms_err": f_err if kind == "±" else "",
                "fDM_R12_upper_limit_2rms": f_err if kind == "<" else "",
                "derived_logMstar_prior": f"{math.log10(float(ms) * 1e11):.3f}",
                "derived_logMbar_prior": f"{math.log10(float(mb) * 1e11):.3f}",
                "derived_logMbar_fit": f"{math.log10(float(mbar_fit[i]) * 1e11):.3f}",
            }
        )
    return out


# ---------------------------------------------------------------- KMOS3D (Wisnioski+2019)
def fw(line: str, a: int, b: int) -> str:
    return line[a - 1 : b].strip()


def parse_kmos3d() -> list[dict]:
    t5 = (SRC / "J_ApJ_886_124_table5.dat").read_text().splitlines()
    t6 = (SRC / "J_ApJ_886_124_table6.dat").read_text().splitlines()
    check(len(t5) == 785, f"KMOS3D table5 rows 785 (got {len(t5)})")
    check(len(t6) == 739, f"KMOS3D table6 rows 739 (got {len(t6)})")

    def nz(v: str, *sentinels: str) -> str:
        return "" if v in sentinels or v == "" else v

    ha = {}
    for ln in t6:
        ha[fw(ln, 1, 10)] = {
            "z_Ha": nz(fw(ln, 53, 62)),
            "e_z_Ha": nz(fw(ln, 64, 69)),
            "sigma_int_kms": nz(fw(ln, 71, 76)),
            "e_sigma_int_kms": nz(fw(ln, 78, 82)),
            "Ha_fit_flag": nz(fw(ln, 112, 113)),
        }
    rows = []
    for ln in t5:
        r = {
            "kmos3d_id": fw(ln, 1, 10),
            "field": fw(ln, 12, 18),
            "id_skelton14": nz(fw(ln, 20, 24), "99999"),
            "target_id": fw(ln, 26, 35),
            "primary_flag": fw(ln, 56, 56),
            "addgal_flag": fw(ln, 58, 58),
            "seg_flag": fw(ln, 60, 61),
            "zqual_flag": fw(ln, 63, 63),
            "ra_deg": fw(ln, 65, 83),
            "dec_deg": fw(ln, 85, 104),
            "z_target": fw(ln, 106, 115),
            "band": fw(ln, 117, 118),
            "psf_fwhm_arcsec": fw(ln, 127, 133),
            "z_kmos3d": nz(fw(ln, 135, 148), "-9999.0", "-9999"),
            "sfr_Msun_yr": fw(ln, 199, 212),
            "sfr_type_flag": fw(ln, 214, 216),
            "logMstar": fw(ln, 218, 222),
            "Av_mag": fw(ln, 224, 226),
            "Reff_H_arcsec": fw(ln, 228, 235),
            "e_Reff_H_arcsec": nz(fw(ln, 237, 249), "-999.0", "-999"),
            "q_H": fw(ln, 251, 258),
            "e_q_H": nz(fw(ln, 260, 272), "-999.0", "-999"),
            "hband_source_flag": fw(ln, 274, 274),
        }
        if r["z_kmos3d"] and float(r["z_kmos3d"]) < -900:
            r["z_kmos3d"] = ""
        if r["e_Reff_H_arcsec"] and float(r["e_Reff_H_arcsec"]) < -900:
            r["e_Reff_H_arcsec"] = ""
        if r["e_q_H"] and float(r["e_q_H"]) < -900:
            r["e_q_H"] = ""
        r.update(ha.get(r["kmos3d_id"], {}))
        rows.append(r)
    ids = [r["kmos3d_id"] for r in rows]
    check(len(set(ids)) == len(ids), f"KMOS3D ids unique ({len(set(ids))}/{len(ids)})")
    check(set(ha) <= set(ids), "KMOS3D table6 ids subset of table5 ids")

    # cross-check against the MPE release FITS
    try:
        from astropy.io import fits
    except ImportError:
        check(False, "astropy available for MPE FITS cross-check")
        return rows
    mpe = fits.open(SRC / "k3d_fnlsp_table_v3.fits")[1].data
    mpe_ha = fits.open(SRC / "k3d_fnlsp_table_hafits_v3.fits")[1].data
    check(
        len(mpe) == len(rows) and len(mpe_ha) == len(ha),
        f"MPE FITS row counts {len(mpe)}/{len(mpe_ha)} == VizieR {len(rows)}/{len(ha)}",
    )
    by = {str(x["ID"]).strip(): x for x in mpe}
    check(set(by) == set(ids), "MPE FITS ID set == VizieR table5 ID set")
    dz = dm = dr = 0.0
    for r in rows:
        x = by[r["kmos3d_id"]]
        dm = max(dm, abs(float(x["LMSTAR"]) - float(r["logMstar"])))
        dr = max(dr, abs(float(x["RHALF"]) - float(r["Reff_H_arcsec"])))
        if r["z_kmos3d"]:
            dz = max(dz, abs(float(x["Z"]) - float(r["z_kmos3d"])))
    check(
        dm < 0.006 and dr < 1e-5 and dz < 1e-4,
        f"MPE FITS vs VizieR max |dlogM*|={dm:.4f} |dRhalf|={dr:.2e} |dz|={dz:.2e}",
    )
    return rows


def kpc_per_arcsec(z: float) -> float:
    from astropy.cosmology import FlatLambdaCDM
    import astropy.units as u

    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    return (1 / cosmo.arcsec_per_kpc_proper(z)).to(u.kpc / u.arcsec).value


def main() -> int:
    verify_sources()
    rc100 = load_rc100()
    rc100_by = {}
    for r in rc100:
        rc100_by.setdefault(norm(r["galaxy"]), []).append(r)

    # ---------------- RC41
    rc41 = parse_rc41()
    al = {r["rc41_row"]: aliases_of([r["galaxy_T1"], r["galaxy_D1"]]) for r in rc41}
    counts: dict[str, int] = {}
    for s in al.values():
        for a in s:
            counts[a] = counts.get(a, 0) + 1
    for k in al:
        al[k] = {a for a in al[k] if counts[a] == 1}
    n_match = 0
    zdiff = []
    for r in rc41:
        hits = {h["idx"]: h for a in al[r["rc41_row"]] for h in rc100_by.get(a, [])}
        check(
            len(hits) <= 1,
            f"RC41 row {r['rc41_row']}: at most one RC100 match ({sorted(hits)})",
        )
        if len(hits) == 1:
            h = next(iter(hits.values()))
            r["in_RC100"] = "1"
            r["RC100_idx"] = h["idx"]
            r["RC100_name"] = h["galaxy"]
            n_match += 1
            if abs(float(h["z"]) - float(r["z"])) > 0.005:
                zdiff.append(f"{r['galaxy_T1']} z(RC41)={r['z']} z(RC100)={h['z']}")
        else:
            r["in_RC100"] = "0"
        r["aliases_normalized"] = ";".join(sorted(al[r["rc41_row"]]))
    check(n_match == 41, f"RC41 -> RC100 overlap 41/41 (got {n_match})")
    rc41_alias_to_row = {a: r for r in rc41 for a in al[r["rc41_row"]]}

    # Informational: T1 col 7 is printed to 0.1 from z printed to 0.01, so it is a loose
    # check; the tight cosmology check is the G17 'kpc/arcsec' row below.
    kdiff = [
        (r["rc41_row"], r["z"], r["kpc_per_arcsec_T1"], kpc_per_arcsec(float(r["z"])))
        for r in rc41
    ]
    worst = max(abs(k - float(t)) for _, _, t, k in kdiff)
    kpc_off = [
        f"row {n} (z={z}) printed {t} vs {k:.3f}"
        for n, z, t, k in kdiff
        if abs(k - float(t)) > 0.06
    ]
    print(
        f"INFO RC41 T1 kpc/arcsec vs FlatLambdaCDM(70,0.3): max |diff| {worst:.3f}; >0.06: {kpc_off}"
    )
    peak = max(kpc_per_arcsec(0.01 * i) for i in range(100, 250))
    check(
        peak < 8.6,
        f"FlatLambdaCDM(70,0.3) peak proper scale {peak:.3f} kpc/arcsec < 8.6 "
        "(RC41 row 22's printed 8.6 is not reproducible in the stated cosmology)",
    )

    # ---------------- G17
    g17 = parse_g17()
    for r in g17:
        hit = rc41_alias_to_row.get(norm(r["galaxy"]))
        r["in_RC41"] = "1" if hit else "0"
        r["RC41_row"] = hit["rc41_row"] if hit else ""
        hh = rc100_by.get(norm(r["galaxy"]), [])
        r["in_RC100"] = "1" if hh else "0"
        r["RC100_idx"] = hh[0]["idx"] if hh else ""
        dk = abs(kpc_per_arcsec(float(r["z"])) - float(r["kpc_per_arcsec"]))
        check(
            dk <= 0.02,
            f"G17 {r['galaxy']}: kpc/arcsec {r['kpc_per_arcsec']} vs FlatLambdaCDM(70,0.3) (|diff| {dk:.3f})",
        )
    check(all(r["in_RC41"] == "1" for r in g17), "G17: all 6 galaxies inside RC41")
    check(all(r["in_RC100"] == "1" for r in g17), "G17: all 6 galaxies inside RC100")
    for r in rc41:
        r["in_G17"] = (
            "1" if any(norm(g["galaxy"]) in al[r["rc41_row"]] for g in g17) else "0"
        )
    check(
        sum(r["in_G17"] == "1" for r in rc41) == 6,
        "RC41: exactly 6 rows flagged in_G17",
    )

    # revision spread for the same galaxy across the three files (not independent measurements)
    rc100_idx = {r["idx"]: r for r in rc100}
    spread = []
    for g in g17:
        a = next(r for r in rc41 if r["rc41_row"] == g["RC41_row"])
        b = rc100_idx[g["RC100_idx"]]
        spread.append(
            f"{g['galaxy']}: Vc = {g['Vc_R12_kms']} (G17) / {a['Vc_Re_kms']} (RC41) / {b['Vc_kms']} (RC100) km/s; "
            f"fDM = {g['fDM_R12']} / {a['fDM_Re']} / {b['fDM']}"
        )

    # ---------------- KMOS3D
    k3d = parse_kmos3d()
    rc100_k = 0
    for r in k3d:
        keys = {norm(r["kmos3d_id"]), norm(r["target_id"])}
        row41 = next(
            (rc41_alias_to_row[k] for k in keys if k in rc41_alias_to_row), None
        )
        r["in_RC41"] = "1" if row41 else "0"
        r["RC41_row"] = row41["rc41_row"] if row41 else ""
        direct = [h for k in keys for h in rc100_by.get(k, [])]
        if direct:
            r["in_RC100"], r["RC100_idx"], r["RC100_match"] = (
                "1",
                direct[0]["idx"],
                "id_or_target",
            )
        elif row41 and row41.get("in_RC100") == "1":
            r["in_RC100"], r["RC100_idx"], r["RC100_match"] = (
                "1",
                row41["RC100_idx"],
                "via_RC41_alias",
            )
        else:
            r["in_RC100"] = "0"
        if row41:
            check(
                "kmos3d_id" not in row41,
                f"RC41 row {row41['rc41_row']}: single KMOS3D match ({r['kmos3d_id']})",
            )
            row41["kmos3d_id"] = r["kmos3d_id"]
            if r["z_kmos3d"]:
                check(
                    abs(float(r["z_kmos3d"]) - float(row41["z"])) <= 0.01,
                    f"RC41 row {row41['rc41_row']}: z {row41['z']} vs KMOS3D {r['kmos3d_id']} z {r['z_kmos3d']}",
                )
        r["in_G17"] = "1" if any(norm(g["galaxy"]) in keys for g in g17) else "0"
        if r["z_kmos3d"]:
            s = kpc_per_arcsec(float(r["z_kmos3d"]))
            r["derived_kpc_per_arcsec"] = f"{s:.4f}"
            r["derived_Reff_H_kpc"] = f"{s * float(r['Reff_H_arcsec']):.3f}"
            if r["e_Reff_H_arcsec"]:
                r["derived_e_Reff_H_kpc"] = f"{s * float(r['e_Reff_H_arcsec']):.3f}"
        rc100_k += r["in_RC100"] == "1"
    k3d_rc100_idx = {r["RC100_idx"] for r in k3d if r["in_RC100"] == "1"}
    check(
        len(k3d_rc100_idx) == rc100_k,
        f"KMOS3D: RC100 matches are one-to-one ({rc100_k} rows, {len(k3d_rc100_idx)} idx)",
    )
    kfields = re.compile(r"^(U3|U4|COS3|COS4|GS3|GS4)\s")
    unmatched_kfield = [
        r["galaxy"]
        for r in rc100
        if kfields.match(r["galaxy"]) and r["idx"] not in k3d_rc100_idx
    ]
    print(
        f"INFO KMOS3D rows overlapping RC100: {rc100_k}; RC100 names with KMOS3D-style field prefix but no KMOS3D match: {unmatched_kfield}"
    )
    n_k_rc41 = sum(r["in_RC41"] == "1" for r in k3d)
    n_rc41_k = sum("kmos3d_id" in r for r in rc41)
    check(
        n_k_rc41 == n_rc41_k
        and all(r["primary_flag"] == "1" for r in k3d if r["in_RC41"] == "1"),
        f"KMOS3D<->RC41 overlap consistent: {n_k_rc41} KMOS3D rows (all primary targets) == {n_rc41_k} RC41 rows with kmos3d_id",
    )
    n_primary = sum(r["primary_flag"] == "1" for r in k3d)
    check(n_primary == 739, f"KMOS3D primary targets 739 (got {n_primary})")
    print(f"INFO KMOS3D rows overlapping RC41: {n_k_rc41}")
    # ID evidence from the KMOS3D catalog for the two RC41 names printed inconsistently
    k3d_by = {r["kmos3d_id"]: r for r in k3d}
    k3d_by_target = {r["target_id"]: r for r in k3d}
    id_notes = []
    for spelled in ("GS4_32976", "GS4_32796", "GS4_33689"):
        hit = k3d_by.get(spelled)
        id_notes.append(
            f"KMOS3D has {spelled}: "
            + (f"yes (z={hit['z_kmos3d']}, logM*={hit['logMstar']})" if hit else "no")
        )
    t = k3d_by_target.get("GS3_22466")
    if t:
        id_notes.append(
            f"KMOS3D maps original target GS3_22466 -> {t['kmos3d_id']} (z={t['z_kmos3d']}); RC41 row 34 prints"
            " GS4_33689, one digit different -- the RC41 row is linked to KMOS3D through GS3_22466"
        )
    for s_ in id_notes:
        print("INFO " + s_)

    # ---------------- write RC41
    rc41_fields = (
        [
            "rc41_row",
            "galaxy_T1",
            "galaxy_D1",
            "z",
            "Vc_Re_kms",
            "Re_kpc",
            "logMbar",
            "logMstar_fit",
            "logMgas",
            "fDM_Re",
            "e_fDM_Re",
            "sigma0_kms",
            "nS",
            "inclination_deg",
            "inclination_T1",
            "BT_dyn",
            "BT_optical_T1",
            "logMstar_HSTinput_T1",
            "dlogMbar_fit_minus_input",
            "derived_logMbar_input",
            "kpc_per_arcsec_T1",
        ]
        + [
            c[1]
            for c in D1_COLS
            if c[1]
            not in {
                "logMstar_fit",
                "logMgas",
                "logMbar",
                "dlogMbar_fit_minus_input",
                "Vc_Re_kms",
                "sigma0_kms",
                "Re_kpc",
                "nS",
                "inclination_deg",
                "BT_dyn",
                "fDM_Re",
                "e_fDM_Re",
            }
        ]
        + [
            "mode",
            "FWHM_arcsec",
            "Tint_h",
            "environment_T1",
            "in_RC100",
            "RC100_idx",
            "RC100_name",
            "in_G17",
            "kmos3d_id",
            "aliases_normalized",
        ]
    )
    s20 = SOURCES["arXiv_2006.03046_eprint.pdf"]
    hdr = (
        [
            "RC41 -- Genzel, Price, Uebler, Foerster Schreiber, et al. 2020, ApJ 902, 98,",
            "'Rotation Curves in z~1-2 Star-Forming Disks: Evidence for Cored Dark Matter Distributions' (arXiv:2006.03046v2).",
            f"SOURCE: {s20[0]}",
            f"SOURCE sha256 {s20[1]} (file {rel(SRC)}/arXiv_2006.03046_eprint.pdf, gitignored, not committed).",
            "No machine-readable table exists: not on VizieR (J/ApJ/902/98 -> 'Table or Catalog not found', queried 2026-09-16);",
            "arXiv has no TeX source (Word-generated PDF). Values come from the PDF text layer (pdftotext -layout) of",
            "Table 1 (PDF p.15) and Table D1 (PDF p.53), checked by eye against 450-dpi renders. Journal (IOP) version NOT compared.",
            "Built by scripts/highz_ingest_rc41_g17_kmos3d.py; every validator listed below passed at build time.",
            "",
            "PAPER CONVENTIONS (Table 1 caption, quoted): 'We are adopting a Omega_m=0.3, H0=70 km/s/Mpc LCDM Universe, and a",
            "Chabrier (2003) initial stellar mass function. Effective radii, inclinations, input stellar masses are derived from",
            "analysis of the optical HST ancillary information'. Gas priors: 'scaling relations give a prior on Mgas (e.g. Tacconi",
            "et al. 2018, Scoville et al. 2017)' (App. A).",
            "PRESSURE SUPPORT: Vc_Re_kms is the model total CIRCULAR velocity v_c(R_e) (= Table 1 col 5 = Table D1 col 16).",
            "The paper's rotation velocity is v_rot^2 = v_circ^2 - 2 sigma0^2 (R/R_d) (eq. A5, 'asymmetric drift'); so Vc is",
            "already pressure-support corrected. Do not re-apply a correction.",
            "CIRCULARITY WARNING: logMbar (D1 col 10) and logMstar_fit (D1 col 7) are DYNAMICAL-FIT outputs, not photometric.",
            "Verified identity on all 41 rows: logMbar = log10(10^logMstar_fit + 10^logMgas) to <=0.011 dex, i.e. col 7 is",
            "Mbar_fit - Mgas. fDM_Re (D1 col 27, 'averages between AC on and off', fDM = v_DM^2/v_c^2 at R_e) comes from the same",
            "fit. The photometric prior is logMstar_HSTinput_T1 (Table 1 col 8, printed to 0.1 dex); col 11 is printed",
            "'DlogM_baryon fit-input' (the 'D' is the PDF's rendering of Delta).",
            "",
            "COLUMNS (printed Table 1 / Table D1 column numbers; D1 skips 3-6; header text quoted as printed):",
            "  rc41_row = col 1; galaxy_T1 = Table 1 col 1 'galaxy'; galaxy_D1 = D1 col 2 'Target' (multi-line cells joined)",
            "  z = T1 col 2 'z'; kpc_per_arcsec_T1 = T1 col 7 'kpc/arcsec'; logMstar_HSTinput_T1 = T1 col 8 'logM_* HST input (M_sun)'",
            "  BT_optical_T1 = T1 col 9 'B/T optical light' (NA = blank in paper); environment_T1 = T1 col 11 'satellite/companion/merger'",
            "  (text, transcribed from the render; NA = blank). T1 cols 3,12-16 (morphology, companion geometry) omitted.",
        ]
        + [f"  {name} = D1 col {num} '{txt}'" for num, name, txt in D1_COLS]
        + [
            "  mode = D1 col 33 'Mode' (instrument; transcribed from render); FWHM_arcsec = D1 col 34; Tint_h = D1 col 35 'T_int (h)'",
            "  e_fDM_Re (col 28 'Df_DM') and e_alpha_inner (col 30): the paper states it 'adopt[s] the MCMC uncertainties' (App. A).",
            "  D1 cols 23-25 print 'S_DM' = Sigma_DM. No uncertainties are published for Vc, Re, logMbar in this table.",
            "VALIDATOR COVERAGE PER COLUMN: independently cross-checked = D1 cols 16 (Vc), 18 (Re), 20 (inclination), 21 (B/T)",
            "  [each equals its Table 1 twin] and cols 7, 9, 10 [baryon identity]; z, rc41_row and names are cross-checked",
            "  against RC100 / KMOS3D. All other numeric columns (8, 11-15, 17, 19, 22-32, 34, 35 and T1 cols 7-9) rest on",
            "  the PDF text layer alone, eyeball-checked against the 450-dpi render, with no independent arithmetic check.",
            "  derived_logMbar_input = logMbar - dlogMbar_fit_minus_input (arithmetic on two printed columns; NOT printed in paper).",
            "  in_RC100/RC100_idx/RC100_name: match to RC100_NestorShachar2023_table3_transcribed.csv by normalized-name alias",
            "  (uppercase, strip space _ - ( ) /; composites split on / space -; aliases shared by >1 RC41 row dropped).",
            "  in_G17: galaxy is one of the 6 in Genzel+2017 (G17_Genzel2017.csv). kmos3d_id: KMOS3D ID whose ID or original",
            "  targeting ID matches an alias (KMOS3D_Wisnioski2019.csv); NA = not a KMOS3D target.",
            "",
            "OVERLAP / DOUBLE COUNTING: G17 (6) is a subset of RC41 (41), which is a subset of RC100 (100): all 41 RC41 rows",
            "match an RC100 row (41/41). The same galaxy carries different values in the three files -- these are successive",
            "re-analyses by the same team, NOT independent measurements; use at most one file per galaxy:",
        ]
        + [f"  {s}" for s in spread]
        + [
            "RC41 vs RC100 name/z notes: Table 1 prints GS4_32976, Table D1 prints GS4_32796 (row 8); RC100 prints GS4 32976.",
            "Table 1 prints G4-38153 / G4_24985 where D1 prints EGS4_38153 / EGS4_24985 (rows 18, 19).",
        ]
        + [f"  z differs >0.005: {s}" for s in zdiff]
        + [f"  {s}" for s in id_notes]
        + [
            "  Every RC41 row with a kmos3d_id has |z_RC41 - z_KMOS3D| <= 0.01 (validator).",
            "",
            "VALIDATORS (all PASS at build): sha256 of source; 41 rows in each table; 26 numeric cells per D1 row;",
            "T1 v_c/R_e/B/T_dyn == D1 cols 16/18/21 exactly and T1 inclination == D1 col 20 to <=0.5 deg, all 41 rows;",
            "baryon identity above. The cosmology is confirmed by G17's printed 'kpc/arcsec' row (reproduced to <=0.02",
            "by astropy FlatLambdaCDM(H0=70, Om0=0.3)). RC41 T1 col 7 is looser: max |diff| "
            + f"{worst:.3f}; rows off by >0.06: "
            + ("; ".join(kpc_off) or "none")
            + f". The peak proper scale in that cosmology is {peak:.3f} kpc/arcsec, so a printed 8.6 cannot be exact:",
            "treat kpc_per_arcsec_T1 as indicative only.",
            "PAPER-INTERNAL DISCREPANCIES: "
            + ("; ".join(T1_NOTES) or "none")
            + ". inclination_deg carries the D1 value, inclination_T1 the Table 1 value.",
            "NA = not given in the paper.",
        ]
    )
    write_csv(OUT / "RC41_Genzel2020.csv", hdr, rc41_fields, rc41)

    # ---------------- write G17
    s17 = SOURCES["arXiv_1703.04310_eprint.pdf"]
    g17_fields = [
        "galaxy",
        "z",
        "Vc_R12_kms",
        "R12_n1_fit_kpc",
        "R12_Hband_prior_kpc",
        "e_R12_Hband_prior_kpc",
        "Mbar_fit_incl_bulge_1e11Msun",
        "Mbar_prior_1e11Msun",
        "e_Mbar_prior_1e11Msun",
        "Mstar_prior_1e11Msun",
        "e_Mstar_prior_1e11Msun",
        "fDM_R12",
        "fDM_R12_2rms_err",
        "fDM_R12_upper_limit_2rms",
        "sigma0_kms",
        "Mbulge_over_Mbar",
        "inclination_deg",
        "e_inclination_deg",
        "c_halo",
        "kpc_per_arcsec",
        "derived_logMbar_fit",
        "derived_logMbar_prior",
        "derived_logMstar_prior",
        "in_RC41",
        "RC41_row",
        "in_RC100",
        "RC100_idx",
    ]
    hdr17 = (
        [
            "G17 -- Genzel, Foerster Schreiber, Uebler, et al. 2017, Nature 543, 397,",
            "'Strongly baryon-dominated disk galaxies at the peak of galaxy formation ten billion years ago' (arXiv:1703.04310v1, only version).",
            f"SOURCE: {s17[0]}",
            f"SOURCE sha256 {s17[1]} (file {rel(SRC)}/arXiv_1703.04310_eprint.pdf, gitignored, not committed).",
            "No machine-readable table (Nature paper; no VizieR catalog; arXiv has no TeX source -- Word PDF). Values are from the",
            "PDF text layer of 'Table 1. Physical Parameters of Observed Star-Forming Galaxies' (PDF p.5). Nature version NOT compared.",
            "Built by scripts/highz_ingest_rc41_g17_kmos3d.py.",
            "",
            "CONVENTIONS (quoted): 'All physical units are based on a concordance, flat LCDM cosmology with Omega_m=0.3,",
            "Omega_baryon/Omega_m=0.17, H0=70 km s-1 Mpc-1' (Fig. 1 caption). IMF: stellar masses from SED fits 'adopting ... an",
            "IMF[43]', ref 43 = Chabrier (2003). Gas: 'We computed molecular gas masses from the general scaling relations",
            "between star formation rates, stellar masses, and molecular gas masses' ... 'the gas masses estimated from these",
            "scaling relations may be lower limits' (Methods).",
            "PRESSURE SUPPORT: corrected. Footnote a (quoted): 'Total circular velocity at the half-light radius (rest-frame",
            "optical) R1/2, including bulge, exponential disk (n=1) and dark matter, and corrected for asymmetric drift:",
            "vc(R)^2=vrot(R)^2+3.36 sigma0^2 (R/R1/2)|n=1.'",
            "",
            "COLUMNS (Table 1 rows; masses printed in units of 1e11 M_sun):",
            "  Priors block: 'M* (10^11 M_sun)' -> Mstar_prior (+-err); 'Mbaryon(gas+stars) (10^11 M_sun)' -> Mbar_prior (+-err);",
            "  'H-band R1/2 (kpc)' -> R12_Hband_prior (+-err); 'inclination (deg)' (+-err); 'dark matter concentration parameter c' -> c_halo.",
            "  Fit block: 'vc(R1/2) (km/s)^a' -> Vc_R12_kms; 'R1/2(n=1) (kpc)' -> R12_n1_fit_kpc; 'sigma0 (km/s)' -> sigma0_kms;",
            "  'Mbaryon(gas+stars, including bulge) (10^11 M_sun)' -> Mbar_fit_incl_bulge; 'Mbulge/Mbaryon';",
            "  'fDM(R1/2)=(vDM/vc)^2|R=R1/2^b' -> fDM_R12. Footnote b (quoted): 'numbers in the parentheses giving the +-2rms",
            "  (delta chi^2=4, ~95% probability) uncertainties, or upper limits. We use an NFW halo of concentration parameter c,",
            "  and no adiabatic contraction.' -> fDM_R12_2rms_err when printed '(+-x)', fDM_R12_upper_limit_2rms when '(<x)'.",
            "  'redshift', 'kpc/arcsec' as printed. derived_* = log10(value x 1e11), not printed in the paper.",
            "  Vc_R12_kms is evaluated at R1/2 -- which R1/2 (H-band prior or n=1 fit) is not stated beyond footnote a; both are kept.",
            "  No uncertainty is printed for Vc, R12_n1_fit, sigma0 or Mbar_fit.",
            "  VALIDATOR COVERAGE: only 'kpc/arcsec' (vs the stated cosmology), the value+-error syntax and Mbar_prior >= M*_prior",
            "  are checked. Vc_R12_kms, sigma0_kms, R12_n1_fit_kpc, Mbar_fit, Mbulge/Mbar, c and fDM have NO independent check",
            "  beyond the text layer (single table, 6 rows, read against the rendered page).",
            "",
            "OVERLAP / DOUBLE COUNTING: all 6 galaxies are in RC41 (Genzel+2020 uses 'the 6 RCs from Genzel et al. 2017') and in",
            "RC100. Values differ between the files because they are successive re-analyses, NOT independent measurements;",
            "use at most one file per galaxy:",
        ]
        + [f"  {s}" for s in spread]
        + [
            "VALIDATORS (PASS at build): sha256; 6 names; every value+-error parsed; Mbar_prior >= Mstar_prior;",
            "printed kpc/arcsec reproduced by FlatLambdaCDM(70,0.3) to <=0.02.",
            "NA = not given in the paper.",
        ]
    )
    write_csv(OUT / "G17_Genzel2017.csv", hdr17, g17_fields, g17)

    # ---------------- write KMOS3D
    k_fields = [
        "kmos3d_id",
        "field",
        "target_id",
        "id_skelton14",
        "z_kmos3d",
        "zqual_flag",
        "z_target",
        "logMstar",
        "Reff_H_arcsec",
        "e_Reff_H_arcsec",
        "derived_Reff_H_kpc",
        "derived_e_Reff_H_kpc",
        "derived_kpc_per_arcsec",
        "q_H",
        "e_q_H",
        "hband_source_flag",
        "sfr_Msun_yr",
        "sfr_type_flag",
        "Av_mag",
        "z_Ha",
        "e_z_Ha",
        "sigma_int_kms",
        "e_sigma_int_kms",
        "Ha_fit_flag",
        "primary_flag",
        "addgal_flag",
        "seg_flag",
        "band",
        "psf_fwhm_arcsec",
        "ra_deg",
        "dec_deg",
        "in_RC41",
        "RC41_row",
        "in_RC100",
        "RC100_idx",
        "RC100_match",
        "in_G17",
    ]
    hdrk = [
        "KMOS3D -- Wisnioski, Foerster Schreiber, Fossati, et al. 2019, ApJ 886, 124, 'The KMOS3D Survey: data release and",
        "final survey paper' (arXiv:1909.11096v1). VizieR J/ApJ/886/124 (doi:10.26093/cds/vizier.18860124), tables 5 and 6.",
        f"SOURCE table5: {SOURCES['J_ApJ_886_124_table5.dat'][0]} sha256 {SOURCES['J_ApJ_886_124_table5.dat'][1]}",
        f"SOURCE table6: {SOURCES['J_ApJ_886_124_table6.dat'][0]} sha256 {SOURCES['J_ApJ_886_124_table6.dat'][1]}",
        f"SOURCE ReadMe: {SOURCES['KMOS3D_J_ApJ_886_124_ReadMe.txt'][0]} sha256 {SOURCES['KMOS3D_J_ApJ_886_124_ReadMe.txt'][1]}",
        f"CROSS-CHECK: MPE release catalogs {SOURCES['k3d_fnlsp_table_v3.fits'][0]} (sha256 {SOURCES['k3d_fnlsp_table_v3.fits'][1]})",
        f"  and {SOURCES['k3d_fnlsp_table_hafits_v3.fits'][0]} (sha256 {SOURCES['k3d_fnlsp_table_hafits_v3.fits'][1]}):",
        "  row counts 785/739, identical ID sets, and z / logM* / R_half agree (validator PASS). Source files in",
        f"  {rel(SRC)}/ (gitignored, not committed). Built by scripts/highz_ingest_rc41_g17_kmos3d.py.",
        "",
        "*** NO KINEMATICS: the KMOS3D data release publishes NO rotation velocity, NO circular velocity, NO gas or baryonic",
        "*** mass and NO fDM per galaxy (VizieR table5/table6 and the MPE FITS contain none). sigma_int_kms is an",
        '*** aperture-integrated line width (1.5" radius circular aperture) -- NOT a disk sigma0 and NOT a rotation proxy.',
        "*** This file CANNOT feed the V^2/R or BTFR a0 routes by itself. It supplies z, M*, R_e and the ID crosswalk",
        "*** (original targeting IDs like U3_21388 -> KMOS3D U4_29145) used to de-duplicate RC41/RC100.",
        "PRESSURE SUPPORT: N/A (no rotation velocity in this release).",
        "",
        "CONVENTIONS (arXiv:1909.11096v1 Sec. 1, quoted): 'We assume a LambdaCDM cosmology with H0 = 70 km s-1 Mpc-1,",
        "Omega_m = 0.3, and Omega_Lambda = 0.7' ... 'Chabrier (2003) initial mass function.'",
        "",
        "COLUMNS (VizieR labels; explanations quoted from the ReadMe byte-by-byte description):",
        "  kmos3d_id=ID 'KMOS^3D^ unique identifier'; field=Field; target_id=Target 'KMOS^3D^ original targeting identifier'",
        "  ('KMOS3D ID when targeted, with field and 3D-HST (v2 or v4 catalog) object ID'); id_skelton14=S14 (NA for 99999)",
        "  z_kmos3d=z 'Measured KMOS3D redshift' (NA for -9999); zqual_flag=q_z '1 = redshift/detection is uncertain;",
        "  0 = redshift is secure; -1 = Non-detection'; z_target=zTar 'Best known redshift at time of observation from 3D-HST'",
        "  logMstar=M* 'Stellar mass' [log Msun] 'Derived from SED modeling following Wuyts+ (2011) ... FAST ... Bruzual &",
        "  Charlot (2003); Chabrier (2003) IMF; solar metallicity; Exponentially declining SFH with tau>300Myr'",
        "  Reff_H_arcsec=ReffH 'CANDELS H band major axis effective radius' [arcsec]; e_Reff_H_arcsec=e_ReffH (NA for -999)",
        "  q_H=Q 'CANDELS H band axis ratio'; e_q_H=e_Q; hband_source_flag=HFlag '1 = H-band fit from van der Wel+ (2012);",
        "  2 = H-band fit from Lang+ 2014'; sfr_Msun_yr=SFR 'From ladder of SFR indicators assuming a Chabrier (2003) IMF';",
        "  sfr_type_flag=f_SFR (5..1 = 160um/100um/70um/24um/SED); Av_mag=Av; primary_flag=P '1 = targeted as a primary",
        "  KMOS3D target, 0 = serendipitous galaxy detection'; addgal_flag=Add; seg_flag=Seg '1 = possible issues with",
        "  photometry and derived parameters resulting from over or under segmentation'; band=Band; psf_fwhm_arcsec=FWHM",
        "  'FWHM of Moffat model PSF; minor axis'; ra_deg, dec_deg = RAdeg, DEdeg (J2000).",
        "  From table6 (joined on ID; NA where absent): z_Ha=z 'Redshift (vacuum) from H{alpha} line fit' (1.5\" aperture);",
        "  e_z_Ha; sigma_int_kms=sigma 'Velocity dispersion' -- 'Properties from Gaussian line profile fits to the",
        '  spatially-integrated spectrum of each galaxy extracted in a circular aperture of 1.5" radius. The velocity',
        "  dispersion is corrected for the instrumental resolution'; e_sigma_int_kms; Ha_fit_flag=Flag '0 = reliable fit'",
        "  (-3 no fit, -2/-1 upper limits, 1 unreliable; value 2 also occurs, undocumented in the ReadMe note).",
        "  Omitted: File, Exp, Res, Ksmag, UMag, VMag, JMag, Ap, FHa, e_FHa, FCor.",
        "  derived_kpc_per_arcsec = proper kpc per arcsec at z_kmos3d for astropy FlatLambdaCDM(H0=70, Om0=0.3) (the paper's",
        "  cosmology; reproduces RC41 Table 1 col 7 and G17 Table 1 'kpc/arcsec'); derived_Reff_H_kpc = that x Reff_H_arcsec.",
        "  NA when z_kmos3d is missing (z_target is deliberately NOT substituted).",
        "  in_RC41/RC41_row: ID or target_id matches an RC41 alias; in_RC100/RC100_idx: matches an RC100 name directly",
        "  (RC100_match=id_or_target) or through the matched RC41 row (via_RC41_alias); in_G17 likewise.",
        "",
        f"OVERLAP: {rc100_k} rows overlap RC100 and {sum(r['in_RC41'] == '1' for r in k3d)} overlap RC41 by ID. RC100 names with a",
        f"KMOS3D-style field prefix that matched no KMOS3D row: {', '.join(unmatched_kfield) if unmatched_kfield else 'none'}.",
        "785 rows = 739 primary targets + 46 serendipitous detections (primary_flag=0): count galaxies with primary_flag=1,",
        "not rows. All RC41/RC100-overlapping rows are primary targets.",
        f"{sum(not r['z_kmos3d'] for r in k3d)} rows have no measured z_kmos3d (-9999 in source) and "
        f"{sum(not r.get('sigma_int_kms') for r in k3d)} have no sigma_int_kms. NA = not given.",
        "DE-DUPLICATION TRAP: Uebler+2017 (VizieR J/ApJ/842/121, the KMOS3D Tully-Fisher sample) is ID-less (sequence",
        "numbers only), so it cannot be de-duplicated against this file, RC41 or RC100 by ID.",
    ]
    write_csv(OUT / "KMOS3D_Wisnioski2019.csv", hdrk, k_fields, k3d)

    print()
    print(f"{len(FAILS)} validator failures")
    for f in FAILS:
        print("  " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
