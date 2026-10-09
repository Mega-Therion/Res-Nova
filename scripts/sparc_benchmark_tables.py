#!/usr/bin/env python3
"""Generate every SPARC benchmark table in the corpus from the result JSONs, and check them.

Until 2026-10-09 the canonical manuscript, FOR_REFEREES.md and SPARC_PARAMETER_BUDGET.md were
still printing the mu_dual-era benchmark (Tier 0: GOD 9.20 vs MOND 11.35; Tier 1: GOD 2.95 vs
MOND 2.89) three weeks after PARAMETER_LEDGER.json had been recomputed under mu_std. Under mu_std
the order at Tier 0 is the reverse. Hand-copied numbers drift. So these tables are generated,
and the gate fails when a surface no longer matches its source.

Sources (each table names its own):
  02_galaxy_dynamics/PARAMETER_LEDGER.json   canonical matched comparison (parameter_ledger.py)
  02_galaxy_dynamics/NFW_CONSTRAINED.json    NFW with a cosmological concentration prior
  02_galaxy_dynamics/SPARC_175_summary.json  strict unit-M/L reproduction (sparc_reproduce.py)

A generated block sits between marker lines:
  markdown:  <!-- BEGIN GENERATED: <id> -->  ...  <!-- END GENERATED: <id> -->
  LaTeX:     % BEGIN GENERATED: <id>          ...  % END GENERATED: <id>

    python3 scripts/sparc_benchmark_tables.py --write       # rewrite every block
    python3 scripts/sparc_benchmark_tables.py --check       # exit 1 if any block is stale or missing
    python3 scripts/sparc_benchmark_tables.py --self-test   # sabotage a copy; the check must fail
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GD = "02_galaxy_dynamics"


def load(root: Path) -> dict:
    L = json.loads((root / GD / "PARAMETER_LEDGER.json").read_text())
    N = json.loads((root / GD / "NFW_CONSTRAINED.json").read_text())
    S = json.loads((root / GD / "SPARC_175_summary.json").read_text())
    t1 = L["tier1_GOD"]
    n_gal = (L["tier1_NFW"]["total_free_params"] - t1["total_free_params"]) // 2  # NFW adds 2 per galaxy
    n_bulge = t1["total_free_params"] - 2 * n_gal                                 # Yd + fd per galaxy, Yb per bulge
    if abs(L["tier1_NFW"]["median_reduced_chi2"] - N["NFW_free_c"]["median_reduced_chi2"]) > 1e-3:
        raise SystemExit("PARAMETER_LEDGER tier1_NFW and NFW_CONSTRAINED NFW_free_c disagree; rerun both")
    return {"L": L, "N": N, "S": S, "n_gal": n_gal, "n_bulge": n_bulge}


def f2(x: float) -> str:
    return f"{x:.2f}"


def lead(a: float, b: float, na: str, nb: str) -> str:
    return na if a < b else nb


def md_budget(v: dict) -> str:
    L, N, S, n, nb = v["L"], v["N"], v["S"], v["n_gal"], v["n_bulge"]
    t0g, t0m, t1g, t1m, t1n = L["tier0_GOD"], L["tier0_MOND"], L["tier1_GOD"], L["tier1_MOND"], L["tier1_NFW"]
    nc, nf = N["NFW_cosmological_c_prior"], N["NFW_free_c"]
    sg, sm, sn, nu, ag, dof = S["strict_GOD"], S["strict_MOND"], S["newtonian"], S["nuisance_GOD"], S["aggregate_chi2_per_dof"], S["total_dof"]
    return "\n".join([
        f"## Tier 0: no per-galaxy freedom (canonical comparison)",
        "",
        f"Source: `PARAMETER_LEDGER.json` (`parameter_ledger.py`). {n} galaxies, {t0g['total_points']:,} points "
        f"(galaxies with at least 5 usable points). Mass-to-light fixed at the prior means, "
        f"Υ_disk = 0.5 and Υ_bulge = 0.7; distance factor f_d = 1. Interpolating function μ_std(x) = x/√(1+x²) in both rows.",
        "",
        "| Model | `a0` | Free params | Median reduced `χ²` | Aggregate `χ²`/dof | galaxies with `χ²_red` < 1 / < 2 |",
        "|---|---|---:|---:|---:|---:|",
        f"| GOD | `cH0/(2π)` = 1.042×10⁻¹⁰, declared anchor `[O]` | 0 | {f2(t0g['median_reduced_chi2'])} | {f2(t0g['aggregate_chi2_per_dof'])} | {t0g['frac_under_1']} / {t0g['frac_under_2']} |",
        f"| MOND | literature 1.2×10⁻¹⁰ | 0 | {f2(t0m['median_reduced_chi2'])} | {f2(t0m['aggregate_chi2_per_dof'])} | {t0m['frac_under_1']} / {t0m['frac_under_2']} |",
        "| NFW | — | — | cannot run | — | a halo with no parameters is not a halo |",
        "",
        f"This is the only tier that discriminates where `a0` came from. **{lead(t0m['median_reduced_chi2'], t0g['median_reduced_chi2'], 'MOND', 'GOD')} has the lower median here.**",
        "",
        "## Tier 1: matched per-galaxy nuisances",
        "",
        f"{t1g['total_free_params']} free parameters = {n} Υ_disk + {nb} Υ_bulge + {n} f_d, with Gaussian priors "
        "N(0.5, 0.125), N(0.7, 0.175) and N(1, 0.10). `a0` is not fitted in either μ row.",
        "",
        "| Model | Free params | Median reduced `χ²` | Aggregate `χ²`/dof | `χ²_red` < 1 / < 2 | Notes |",
        "|---|---:|---:|---:|---:|---|",
        f"| GOD | {t1g['total_free_params']} | {f2(t1g['median_reduced_chi2'])} | {f2(t1g['aggregate_chi2_per_dof'])} | {t1g['frac_under_1']} / {t1g['frac_under_2']} | `a0` horizon anchor `[O]` |",
        f"| MOND | {t1m['total_free_params']} | {f2(t1m['median_reduced_chi2'])} | {f2(t1m['aggregate_chi2_per_dof'])} | {t1m['frac_under_1']} / {t1m['frac_under_2']} | `a0` literature |",
        f"| NFW, free `c` | {t1n['total_free_params']} | {f2(t1n['median_reduced_chi2'])} | {f2(t1n['aggregate_chi2_per_dof'])} | {t1n['frac_under_1']} / {t1n['frac_under_2']} | {nf['n_railed_c_low']}/{n} railed at `c = 1`; **not** the ΛCDM row |",
        f"| NFW, cosmological-`c` prior | {nc['total_free_params']} | {f2(nc['median_reduced_chi2'])} | — | {nc['frac_under_1']} / — | {nc['n_railed_c_low']}/{n} railed; the fair ΛCDM-like row (`NFW_CONSTRAINED.json`) |",
        "",
        f"`{t1n['total_free_params']} − {t1g['total_free_params']} = {t1n['total_free_params'] - t1g['total_free_params']}` "
        f"extra NFW parameters versus GOD. Held to its own concentration prior, NFW's median is {f2(nc['median_reduced_chi2'])} "
        f"against GOD's {f2(t1g['median_reduced_chi2'])}. GOD and MOND differ only in where `a0` comes from: "
        f"median {f2(t1g['median_reduced_chi2'])} vs {f2(t1m['median_reduced_chi2'])}, aggregate "
        f"{f2(t1g['aggregate_chi2_per_dof'])} vs {f2(t1m['aggregate_chi2_per_dof'])}, so neither leads.",
        "",
        "## Strict unit-M/L reproduction check (not the comparison above)",
        "",
        f"Source: `SPARC_175_summary.json` (`sparc_reproduce.py`). {S['n_galaxies']} galaxies, {S['n_points']:,} points "
        "(galaxies with at least 3 usable points; velocity errors floored at 1 km/s). Υ_disk = Υ_bulge = 1, f_d = 1. "
        "It differs from Tier 0 in sample, error floor and M/L, so its numbers are not interchangeable with Tier 0's.",
        "",
        "| Model | Free params | Median reduced `χ²` | Aggregate `χ²`/dof | dof |",
        "|---|---:|---:|---:|---:|",
        f"| GOD (`cH0/2π`) | 0 | {f2(sg['median'])} | {f2(ag['strict_GOD'])} | {dof['strict_GOD']:,} |",
        f"| MOND (1.2×10⁻¹⁰) | 0 | {f2(sm['median'])} | {f2(ag['strict_MOND'])} | {dof['strict_MOND']:,} |",
        f"| Baryons only (Newtonian control) | 0 | {f2(sn['median'])} | {f2(ag['newtonian'])} | {dof['newtonian']:,} |",
        f"| GOD, grid nuisance fit (Υ_disk, Υ_bulge, f_d; same priors) | 2–3 per galaxy | {f2(nu['median'])} | {f2(ag['nuisance_GOD'])} | {dof['nuisance_GOD']:,} |",
    ])


def md_referee(v: dict) -> str:
    L, N, S = v["L"], v["N"], v["S"]
    t0g, t0m, t1g, t1m, t1n, nc = L["tier0_GOD"], L["tier0_MOND"], L["tier1_GOD"], L["tier1_MOND"], L["tier1_NFW"], N["NFW_cosmological_c_prior"]
    return "\n".join([
        f"- Tier 0 (canonical, {v['n_gal']} galaxies, M/L at the prior means): GOD median {f2(t0g['median_reduced_chi2'])} vs MOND "
        f"{f2(t0m['median_reduced_chi2'])}; {lead(t0m['median_reduced_chi2'], t0g['median_reduced_chi2'], 'MOND', 'GOD')} has the lower median. "
        "Source: `PARAMETER_LEDGER.json`.",
        f"- Tier 1: GOD median {f2(t1g['median_reduced_chi2'])} / {t1g['total_free_params']} parameters; MOND {f2(t1m['median_reduced_chi2'])} / "
        f"{t1m['total_free_params']}; NFW free-c {f2(t1n['median_reduced_chi2'])} / {t1n['total_free_params']}; NFW cosmological-c "
        f"{f2(nc['median_reduced_chi2'])} / {nc['total_free_params']}.",
        f"- Extra NFW knobs versus GOD at Tier 1: {t1n['total_free_params'] - t1g['total_free_params']}.",
        f"- Strict unit-M/L check ({S['n_galaxies']} galaxies, `SPARC_175_summary.json`): GOD median {f2(S['strict_GOD']['median'])}, "
        f"MOND {f2(S['strict_MOND']['median'])}, baryons-only {f2(S['newtonian']['median'])}. A reproduction check with a different "
        "sample and M/L, not the Tier 0 comparison.",
    ])


def tex_results(v: dict) -> str:
    L, N = v["L"], v["N"]
    t0g, t0m, t1g, t1m, t1n, nc, nf = (L["tier0_GOD"], L["tier0_MOND"], L["tier1_GOD"], L["tier1_MOND"], L["tier1_NFW"],
                                        N["NFW_cosmological_c_prior"], N["NFW_free_c"])
    n = v["n_gal"]
    return "\n".join([
        r"\begin{tabularx}{\textwidth}{@{}l c c c X@{}}",
        r"\toprule",
        r"\textbf{Specification} & \textbf{Free Params} & \textbf{Median $\chi^2_{\text{data}}/N_g$} & \textbf{Aggregate $\chi^2/\mathrm{dof}$} & \textbf{Role} \\",
        r"\midrule",
        rf"GOD Tier 0 (prior-mean $M/L$, horizon $a_0$) $\mathbf{{[D]}}$ & 0 & {f2(t0g['median_reduced_chi2'])} & {f2(t0g['aggregate_chi2_per_dof'])} & Tests the $a_0$ source \\",
        rf"MOND Tier 0 (prior-mean $M/L$, literature $a_0$) $\mathbf{{[D]}}$ & 0 & {f2(t0m['median_reduced_chi2'])} & {f2(t0m['aggregate_chi2_per_dof'])} & Same, literature $a_0$ \\",
        rf"\textbf{{GOD Tier 1}} $\mathbf{{[D]}}$ & {t1g['total_free_params']} & {f2(t1g['median_reduced_chi2'])} & {f2(t1g['aggregate_chi2_per_dof'])} & $\mu_{{\text{{std}}}}$, horizon $a_0$ \\",
        rf"MOND Tier 1 $\mathbf{{[D]}}$ & {t1m['total_free_params']} & {f2(t1m['median_reduced_chi2'])} & {f2(t1m['aggregate_chi2_per_dof'])} & $\mu_{{\text{{std}}}}$, literature $a_0$ \\",
        rf"NFW Free $c$ $\mathbf{{[D]}}$ & {t1n['total_free_params']} & {f2(t1n['median_reduced_chi2'])} & {f2(t1n['aggregate_chi2_per_dof'])} & {nf['n_railed_c_low']}/{n} railed at $c=1$; not $\Lambda$CDM \\",
        rf"\textbf{{NFW Cosmological-$c$ Prior}} $\mathbf{{[D]}}$ & {nc['total_free_params']} & {f2(nc['median_reduced_chi2'])} & --- & Fair $\Lambda$CDM-like row; {nc['total_free_params'] - t1g['total_free_params']} extra parameters vs GOD \\",
        r"\bottomrule",
        r"\end{tabularx}",
        rf"\caption{{Matched-parameter SPARC benchmark on {n} galaxies under $\mu_{{\text{{std}}}}$ (\texttt{{PARAMETER\_LEDGER.json}}, "
        rf"\texttt{{NFW\_CONSTRAINED.json}}; generated by \texttt{{scripts/sparc\_benchmark\_tables.py}}). At Tier~0, "
        rf"{lead(t0m['median_reduced_chi2'], t0g['median_reduced_chi2'], 'MOND', 'GOD')} has the lower median. At Tier~1, GOD and MOND differ only in where "
        rf"$a_0$ comes from and neither leads. The fair cosmological NFW model uses {nc['total_free_params'] - t1g['total_free_params']} more parameters "
        rf"({nc['total_free_params']} total) for median {f2(nc['median_reduced_chi2'])}.}}",
        r"\label{tab:sparc_results}",
    ])


def tex_strict(v: dict) -> str:
    S = v["S"]
    ag, dof = S["aggregate_chi2_per_dof"], S["total_dof"]
    return "\n".join([
        r"Metric & Strict (unit $M/L$, no per-galaxy freedom) & Nuisance (priors) \\",
        r"\colrule",
        rf"Galaxies Analyzed ($N$) & {S['n_galaxies']} & {S['n_galaxies']} \\",
        r"Free Parameters / Galaxy & 0 (fixed $a_0$, $\Upsilon=1.0$, $f_d=1.0$) & 2--3 ($\Upsilon_{\mathrm{disk}}, \Upsilon_{\mathrm{bulge}}, f_d$) \\",
        rf"Total Degrees of Freedom & {dof['strict_GOD']:,} & {dof['nuisance_GOD']:,} \\",
        rf"Median per-galaxy $\chi^2/N$ & ${f2(S['strict_GOD']['median'])}$ & ${f2(S['nuisance_GOD']['median'])}$ \\",
        rf"Aggregate $\chi^2/\mathrm{{dof}}$ & ${f2(ag['strict_GOD'])}$ & ${f2(ag['nuisance_GOD'])}$ \\",
        rf"Newtonian Control & $\chi^2/\mathrm{{dof}} = {f2(ag['newtonian'])}$ (excluded) & -- \\",
    ])


def md_audit(v: dict) -> str:
    S = v["S"]
    ag, dof = S["aggregate_chi2_per_dof"], S["total_dof"]
    n_free = S["n_points"] - dof["nuisance_GOD"]

    def row(label, params, key):
        st = S[key]
        return (f"| {label} | {params} | **{S['n_points']:,} / {dof[key]:,}** | **{f2(st['median'])}** | "
                f"**{f2(st['mean'])}** | **{f2(ag[key])}** |")
    return "\n".join([
        "| Model / Control Specification | Free Params / Priors | Total Points / DOF | Median $\\chi^2_{\\text{data}}/N_g$ | Mean $\\chi^2_{\\text{data}}/N_g$ | Aggregate $\\sum\\chi^2_{\\text{data}}/\\text{DOF}$ |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
        row("**Strict GOD, unit $M/L$** [D]", "0 ($\\Upsilon=1.0, f_d=1.0, a_0=\\frac{cH_0}{2\\pi}$)", "strict_GOD"),
        row("**Strict MOND, unit $M/L$** [D]", "0 ($\\Upsilon=1.0, f_d=1.0, a_0=1.2\\times10^{-10}$)", "strict_MOND"),
        row("**GOD, grid nuisance fit** [D]", f"{n_free} params (Gaussian priors)", "nuisance_GOD"),
        row("**Baryons-only, unit $M/L$** [D]", "0 ($\\Upsilon_{\\text{disk}}=\\Upsilon_{\\text{bulge}}=1.0$)", "newtonian"),
        row("**Baryons-only, prior-mean $M/L$** [D]", "0 ($\\Upsilon_{\\text{disk}}=0.5, \\Upsilon_{\\text{bulge}}=0.7$)", "newtonian_prior_mean_ML"),
    ])


def tex_status(v: dict) -> str:
    S, L = v["S"], v["L"]
    ag, dof = S["aggregate_chi2_per_dof"], S["total_dof"]
    n_free = S["n_points"] - dof["nuisance_GOD"]
    t0g, t0m = L["tier0_GOD"], L["tier0_MOND"]
    return "\n".join([
        rf"SPARC Tier 0 (prior-mean $M/L$, $a_0=\frac{{cH_0}}{{2\pi}}$ declared) & \textbf{{[D] Computed}} & Median $\chi^2_{{\text{{data}}}}/N_g = {f2(t0g['median_reduced_chi2'])}$ vs MOND ${f2(t0m['median_reduced_chi2'])}$ ({v['n_gal']} galaxies, \texttt{{PARAMETER\_LEDGER.json}}). Two irreducible inputs: the $a_0$ scale and the $\mu$ choice. \\",
        rf"SPARC strict unit-$M/L$ check & \textbf{{[D] Computed}} & Median $\chi^2_{{\text{{data}}}}/N_g = {f2(S['strict_GOD']['median'])}$, aggregate $\sum\chi^2_{{\text{{data}}}}/\text{{dof}} = {f2(ag['strict_GOD'])}$ (${S['n_points']:,} / {dof['strict_GOD']:,}$, \texttt{{SPARC\_175\_summary.json}}). \\",
        rf"SPARC grid nuisance fit & \textbf{{[D] Computed}} & Median $\chi^2_{{\text{{data}}}}/N_g = {f2(S['nuisance_GOD']['median'])}$, aggregate $\sum\chi^2_{{\text{{data}}}}/\text{{dof}} = {f2(ag['nuisance_GOD'])}$ (${S['n_points']:,} / {dof['nuisance_GOD']:,}$, $N_{{\text{{par}}}}={n_free}$, Gaussian priors). \\",
        rf"Baryons-Only Baseline (Unit $M/L$) & \textbf{{[D] Computed}} & Median $\chi^2_{{\text{{data}}}}/N_g = {f2(S['newtonian']['median'])}$, aggregate $\sum\chi^2_{{\text{{data}}}}/\text{{dof}} = {f2(ag['newtonian'])}$. \\",
        rf"Baryons-Only Baseline (prior-mean $M/L$) & \textbf{{[D] Computed}} & Median $\chi^2_{{\text{{data}}}}/N_g = {f2(S['newtonian_prior_mean_ML']['median'])}$, aggregate $\sum\chi^2_{{\text{{data}}}}/\text{{dof}} = {f2(ag['newtonian_prior_mean_ML'])}$. \\",
    ])


# Prose mentions outside generated blocks: (file, label, needle builder). The needle must appear verbatim.
MENTIONS = [
    ("CLAIM_EVIDENCE_LEDGER.md", "CLM-04 strict median", lambda v: f"= {f2(v['S']['strict_GOD']['median'])}$"),
    ("CLAIM_EVIDENCE_LEDGER.md", "CLM-06 baryons-only median", lambda v: f"= {f2(v['S']['newtonian']['median'])}$"),
    ("assurance/claims.json", "CLM-04 wording", lambda v: f"median reduced chi-squared of {f2(v['S']['strict_GOD']['median'])}"),
    ("assurance/claims.json", "CLM-06 wording", lambda v: f"median chi2_data/N_g = {f2(v['S']['newtonian']['median'])}"),
    ("RES_NOVA_VERIFICATION_LEDGER.md", "F4 Tier 0", lambda v: f"Tier 0: GOD median {f2(v['L']['tier0_GOD']['median_reduced_chi2'])}"),
    ("RES_NOVA_VERIFICATION_LEDGER.md", "Tier 1 GOD", lambda v: f"$\\chi^2_{{\\text{{data}}}}/N_g = {f2(v['L']['tier1_GOD']['median_reduced_chi2'])}$"),
    ("RELEASE_CHECKLIST.md", "Tier 1 GOD", lambda v: f"$\\chi^2_{{\\text{{data}}}}/N_g = {f2(v['L']['tier1_GOD']['median_reduced_chi2'])}$"),
    ("res_nova_manuscript.tex", "raw-data digest", lambda v: v["S"]["data"]["sha256_of_manifest"]),
    ("THEORY_CONSISTENCY_AUDIT.md", "raw-data digest", lambda v: v["S"]["data"]["sha256_of_manifest"]),
    ("01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex", "abstract (vi)",
     lambda v: f"(median $\\chi^2/N = {f2(v['S']['strict_GOD']['median'])}$, aggregate $\\chi^2/\\mathrm{{dof}} = {f2(v['S']['aggregate_chi2_per_dof']['strict_GOD'])}$)"),
    ("03_observer_jwst/IO_OI_UNIFIED_TRANSMISSION_MONOGRAPH.tex", "strict medians", lambda v: f"${f2(v['S']['strict_GOD']['median'])}$ at the derived scale versus ${f2(v['S']['strict_MOND']['median'])}$"),
]


# (surface, block id, renderer, comment style)
BLOCKS = [
    (f"{GD}/SPARC_PARAMETER_BUDGET.md", "sparc-budget", md_budget, "md"),
    ("FOR_REFEREES.md", "sparc-referee-numbers", md_referee, "md"),
    ("res_nova_manuscript.tex", "sparc-results-table", tex_results, "tex"),
    ("01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex", "sparc-strict-table", tex_strict, "tex"),
    ("THEORY_CONSISTENCY_AUDIT.md", "sparc-audit-table", md_audit, "md"),
    ("build/STATUS_AND_SCOPE.tex", "sparc-status-rows", tex_status, "tex"),
]


def markers(block_id: str, style: str) -> tuple[str, str]:
    tag = f"GENERATED: {block_id} (scripts/sparc_benchmark_tables.py; do not hand-edit)"
    if style == "md":
        return f"<!-- BEGIN {tag} -->", f"<!-- END GENERATED: {block_id} -->"
    return f"% BEGIN {tag}", f"% END GENERATED: {block_id}"


def splice(text: str, begin: str, end: str, body: str) -> tuple[str, str | None]:
    """Return (new text, current body). current body is None if the markers are missing."""
    pat = re.compile(re.escape(begin) + r"\n(.*?)\n?" + re.escape(end), re.S)
    m = pat.search(text)
    if not m:
        return text, None
    return text[:m.start()] + f"{begin}\n{body}\n{end}" + text[m.end():], m.group(1)


def run(root: Path, write: bool) -> list[str]:
    v = load(root)
    problems = []
    for rel, bid, render, style in BLOCKS:
        p = root / rel
        begin, end = markers(bid, style)
        text = p.read_text()
        body = render(v)
        new, cur = splice(text, begin, end, body)
        if cur is None:
            problems.append(f"{rel}: markers for '{bid}' missing")
            continue
        if cur.rstrip("\n") != body:
            if write:
                p.write_text(new)
            else:
                problems.append(f"{rel}: block '{bid}' is stale; run --write")
    for rel, label, needle in MENTIONS:
        n = needle(v)
        if n not in (root / rel).read_text():
            problems.append(f"{rel}: {label} does not read {n!r} (hand-maintained; update it to the source value)")
    return problems


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        for rel in ({r for r, *_ in BLOCKS} | {r for r, *_ in MENTIONS}
                    | {f"{GD}/PARAMETER_LEDGER.json", f"{GD}/NFW_CONSTRAINED.json", f"{GD}/SPARC_175_summary.json"}):
            (t / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, t / rel)
        if run(t, write=False):
            print("self-test: the unmodified copy is already stale; run --write first")
            return 1
        failures = 0
        # 1. hand-edit a number inside a generated block
        p = t / "FOR_REFEREES.md"
        s = p.read_text()
        m = re.search(r"\d+\.\d\d", s[s.index("BEGIN GENERATED: sparc-referee-numbers"):])
        p.write_text(s.replace(m.group(0), "9.20", 1) if m else s)
        failures += 0 if run(t, write=False) else 1
        shutil.copy(ROOT / "FOR_REFEREES.md", p)
        # 2. change a source number
        lp = t / GD / "PARAMETER_LEDGER.json"
        d = json.loads(lp.read_text())
        d["tier0_GOD"]["median_reduced_chi2"] = 9.20
        lp.write_text(json.dumps(d))
        failures += 0 if run(t, write=False) else 1
        shutil.copy(ROOT / GD / "PARAMETER_LEDGER.json", lp)
        # 3. delete a marker
        mp = t / "res_nova_manuscript.tex"
        mp.write_text(mp.read_text().replace("% END GENERATED: sparc-results-table", "", 1))
        failures += 0 if run(t, write=False) else 1
        shutil.copy(ROOT / "res_nova_manuscript.tex", mp)
        # 4. hand-maintained prose mention drifts
        cp = t / "CLAIM_EVIDENCE_LEDGER.md"
        cs = cp.read_text()
        needle = MENTIONS[0][2](load(t))
        cp.write_text(cs.replace(needle, "= 29.12$", 1))
        failures += 0 if run(t, write=False) else 1
    print("self-test: " + ("PASS (4/4 sabotages detected)" if not failures else f"FAIL ({failures} sabotage(s) undetected)"))
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    problems = run(ROOT, write="--write" in argv)
    for p in problems:
        print(p)
    print(f"sparc benchmark tables: {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
