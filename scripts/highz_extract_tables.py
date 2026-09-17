#!/usr/bin/env python3
"""Extract per-galaxy tables from arXiv LaTeX sources into CSVs (verbatim values, no back-fill).

Run from the Res-Nova repo root. Sources: 02_galaxy_dynamics/highz_data/_src/<arxiv>/ (gitignored).
Every numeric cell is parsed from the TeX table row; unparseable cells are left empty and flagged.
"""

import csv, re, os, datetime

SRC = "02_galaxy_dynamics/highz_data/_src"
OUT = "02_galaxy_dynamics/highz_data"
TODAY = datetime.date.today().isoformat()


def cell(s):
    """Return (value, err_plus, err_minus, flag) from a LaTeX table cell."""
    t = s.strip()
    flag = ""
    if "lesssim" in t:
        flag = "upper_limit"
    elif "gtrsim" in t:
        flag = "lower_limit"
    elif t.startswith("\\textit") or t.startswith("\\textit{"):
        flag = "held_fixed"
    t = re.sub(r"\\(lesssim|gtrsim|textit|hspace\{[^}]*\}|vspace\{[^}]*\})", " ", t)
    t = t.replace("$", " ").replace("{", " ").replace("}", " ").replace("~", " ")
    m = re.match(
        r"\s*\(?\s*(-?[\d.]+)\s*\\substack\s*\+\s*([\d.]+)\s*\\\\\s*-\s*([\d.]+)", t
    )
    if m:
        return m.group(1), m.group(2), m.group(3), flag
    m = re.match(r"\s*\(?\s*(-?[\d.]+)\s*\^\s*\+\s*([\d.]+)\s*_\s*-\s*([\d.]+)", t)
    if m:
        return m.group(1), m.group(2), m.group(3), flag
    m = re.match(r"\s*(-?[\d.]+)\s*\\pm\s*([\d.]+)", t)
    if m:
        return m.group(1), m.group(2), m.group(2), flag
    m = re.match(r"\s*\\sim\s*(-?[\d.]+)", t)
    if m:
        return m.group(1), "", "", "approx"
    m = re.match(r"\s*(-?[\d.]+)\s*$", t)
    if m:
        return m.group(1), "", "", flag
    return (
        "",
        "",
        "",
        ("missing" if t.strip() in ("-", "") else "unparsed:" + t.strip()[:30]),
    )


def rows(tex, start_pat, end_pat="\\end{tabular}"):
    txt = open(tex, encoding="utf-8", errors="replace").read()
    i = txt.index(start_pat)
    body = txt[i: txt.index(end_pat, i)]
    body = body.replace("\\\\%", "\\\\ %")
    body = re.sub(r"(?<!\\)%.*", "", body)
    body = re.sub(r"\\substack\s*\{\s*\+\s*([\d.]+)\s*\\\\\s*-\s*([\d.]+)\s*\}", r"^{+\1}_{-\2}", body)
    body = body.split("\\hline", 2)[-1] if body.count("\\hline") >= 2 else body
    out = []
    for r in body.split("\\\\"):
        r = r.replace("\n", " ")
        r = re.sub(r"\\(noalign|vspace)\s*\{(\\vskip\s*)?[^}]*\}|\\(hline|smallskip|medskip)", " ", r).strip()
        if r.count("&") >= 2 and r.split("&")[0].strip() not in ("ID", "Object"):
            out.append([c.strip() for c in r.split("&")])
    return out


def write(name, header_lines, cols, data):
    path = os.path.join(OUT, name + ".csv")
    with open(path, "w", newline="") as f:
        for h in header_lines:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(data)
    print(path, len(data))


def expand(cells):
    o = []
    for c in cells:
        o.extend(cell(c))
    return o


# ---------- ALPAKA (Rizzo+2023) ----------
tex = f"{SRC}/2303.16227/alpaka_v2.tex"
names = {}
for r in rows(tex, "label{tab:tab1}"):
    if re.match(r"^\d+$", r[0].strip()):
        names[r[0].strip()] = (
            r[1].strip(),
            r[4].strip(),
            r[6].strip().rstrip("\\").strip(),
        )
mstar = {}
for r in rows(tex, "label{tab:mstar}"):
    k = r[0].replace("$^{*}$", "").strip()
    if re.match(r"^\d+$", k):
        mstar[k] = (r[1], r[2], r[4].strip())
kin = {}
for r in rows(tex, "label{tab:vsigma}"):
    if re.match(r"^\d+$", r[0].strip()):
        kin[r[0].strip()] = r[1:5]
data = []
for k in sorted(names, key=int):
    nm, z, note = names[k]
    ms = mstar.get(k, ("-", "-", ""))
    kv = kin.get(k)
    data.append(
        [k, nm, z, note, ms[2]]
        + list(cell(ms[0]))
        + list(cell(ms[1]))
        + (expand(kv) if kv else ["", "", "", "not_disk"] * 4)
    )
cols = [
    "ID",
    "name",
    "z",
    "notes",
    "type_MS_SB",
    "Mstar_1e10Msun",
    "Mstar_ep",
    "Mstar_em",
    "Mstar_flag",
    "SFR_Msun_yr",
    "SFR_ep",
    "SFR_em",
    "SFR_flag",
]
for q in ["Vmax_kms", "sigma_m_kms", "Vext_kms", "sigma_ext_kms"]:
    cols += [q, q + "_ep", q + "_em", q + "_flag"]
write(
    "Rizzo2023_ALPAKA",
    [
        "source: Rizzo F. et al. 2023, A&A 679, A129, 'The ALMA-ALPAKA survey I' arXiv:2303.16227",
        "extracted: "
        + TODAY
        + " from arXiv e-print alpaka_v2.tex (tarball also holds aanda.tex/aanda2.tex drafts; numeric rows of tab:vsigma identical between alpaka_v2 and aanda2)",
        "tables: tab:tab1 (name,z), tab:mstar (M*,SFR SED/STARDUST), tab:vsigma (disks only; rotation velocities NOT pressure-support corrected)",
        "cosmology: Planck 2018 LCDM; IMF: Chabrier",
        "tracer: CO / [CI] (ALMA); velocities in km/s; errors as given (ep=+ em=-); no gas masses or rotation-curve points tabulated in paper (RCs figure-only)",
        "pressure_support_corrected: NO",
    ],
    cols,
    data,
)

# ---------- Roman-Oliveira+2023 kinematics ----------
tex = f"{SRC}/2302.03049/main.tex"
zmap = {}
for r in rows(tex, "label{tab:data}"):
    zmap[re.sub(r"\$.*", "", r[0]).strip()] = r[3].strip()
gas = {}
for r in rows(tex, "label{tab:masses}"):
    gas[r[0].strip()] = (r[1], r[2])
data = []
for r in rows(tex, "label{tab:vel}"):
    idn = r[0].strip()
    if idn.startswith("\\"):
        continue
    sfr = gas.get(idn, ("", ""))
    mh2 = sfr[1].replace("\\times 10^{", "e").replace("}", "")
    data.append(
        [idn, zmap.get(idn, "")]
        + expand(r[1:5])
        + list(cell(sfr[0]))
        + [mh2.replace("$", "").strip()]
    )
cols = ["ID", "z"]
for q in ["Vrot_max_kms", "Vrot_ext_kms", "sigma_mean_kms", "sigma_ext_kms"]:
    cols += [q, q + "_ep", q + "_em", q + "_flag"]
cols += ["SFR_Msun_yr", "SFR_ep", "SFR_em", "SFR_flag", "M_H2_Msun_literature_verbatim"]
write(
    "RomanOliveira2023_z4p5_kinematics",
    [
        "source: Roman-Oliveira F., Fraternali F., Rizzo F. 2023, MNRAS 521, 1045, arXiv:2302.03049",
        "extracted: "
        + TODAY
        + " from arXiv e-print main.tex tables tab:data, tab:masses, tab:vel",
        "tracer: [CII] 158um ALMA, 3DBarolo; AzTEC1 not a disc -> absent from tab:vel",
        "IMF: Chabrier (SFR normalised); M_H2 from literature CO with alpha_CO 0.8 (3 for J081740)",
        "pressure_support_corrected: NO (paper states these rotation velocities must not be used for dynamics; see RomanOliveira2024 file)",
    ],
    cols,
    data,
)

# ---------- Roman-Oliveira+2024 mass decomposition ----------
tex = f"{SRC}/2403.00904/aanda.tex"
more = {r[0].strip(): r[1:] for r in rows(tex, "label{tab:dy_more}")}
data = []
for r in rows(tex, "label{tab:dy_fid}"):
    idn = r[0].strip()
    m = more.get(idn, ["", "", ""])
    data.append(
        [idn]
        + expand(r[1:8])
        + list(cell(m[0]))
        + [cell(m[1])[0], cell(m[2].rstrip("\\ "))[0]]
    )
cols = ["ID"]
for q in [
    "log_Mstar",
    "Reff_star_kpc",
    "sersic_n",
    "gas_norm",
    "log_fbar",
    "log_Mgas",
    "log_M200",
]:
    cols += [q, q + "_ep", q + "_em", q + "_flag"]
cols += ["f_gas", "f_gas_ep", "f_gas_em", "f_gas_flag", "Reff_bar_kpc", "f_disc"]
write(
    "RomanOliveira2024_z4p5_massmodels",
    [
        "source: Roman-Oliveira F., Rizzo F., Fraternali F. 2024, A&A (arXiv:2403.00904) 'Dynamical modelling and origin of gas turbulence in z~4.5 galaxies'",
        "extracted: "
        + TODAY
        + " from arXiv e-print aanda.tex tables tab:dy_fid, tab:dy_more",
        "redshifts: see RomanOliveira2023_z4p5_kinematics.csv (same galaxies)",
        "cosmology: Planck 2018; IMF: Chabrier; masses in Msun (log10); flag held_fixed = italic in paper (fixed in fiducial model)",
        "pressure_support_corrected: YES (circular speed after asymmetric-drift correction; RC points figure-only, not tabulated)",
    ],
    cols,
    data,
)
