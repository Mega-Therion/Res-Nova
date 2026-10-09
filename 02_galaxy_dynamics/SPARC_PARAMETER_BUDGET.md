# SPARC parameter budget

**Source of numbers:** `PARAMETER_LEDGER.json` and `NFW_CONSTRAINED.json` for the matched comparison, and `SPARC_175_summary.json` for the strict unit-M/L reproduction check. The tables below are generated from those files by `scripts/sparc_benchmark_tables.py`, and `scripts/local_gate.sh` fails when they drift.
**Scripts:** `parameter_ledger.py`, `nfw_constrained.py`, `sparc_reproduce.py`, `a0_measure.py`.
**This file replaces the older budget prose that still spoke the withdrawn zero-parameter language.**

Shared functional form for the GOD and MOND rows: μ_std(x) = x/√(1+x²), with the AQUAL convention F′ = xμ. Until 2026-10-09 this file printed the μ_dual-era benchmark (Tier 0: GOD 9.20 vs MOND 11.35; Tier 1: 2.95 vs 2.89, superseded) and the τ form of the retired μ_dual. PARAMETER_LEDGER.json had been recomputed under μ_std on 2026-09-12 (`SPARC_MU_STD_RECOMPUTE_2026-09-12.md`), and that recompute reverses the Tier 0 order.

Baryons, in every row: V_bar² = V_gas|V_gas| + Υ_disk V_disk² + Υ_bulge V_bul². Υ multiplies V², and a negative SPARC V_gas subtracts. The distance factor scales V_bar² and R together.

Nuisances `Y_d`, `Y_b`, `f_d` are observational, applied identically when present. They are counted in the free-parameter totals at Tier 1.

<!-- BEGIN GENERATED: sparc-budget (scripts/sparc_benchmark_tables.py; do not hand-edit) -->
## Tier 0: no per-galaxy freedom (canonical comparison)

Source: `PARAMETER_LEDGER.json` (`parameter_ledger.py`). 171 galaxies, 3,375 points (galaxies with at least 5 usable points). Mass-to-light fixed at the prior means, Υ_disk = 0.5 and Υ_bulge = 0.7; distance factor f_d = 1. Interpolating function μ_std(x) = x/√(1+x²) in both rows.

| Model | `a0` | Free params | Median reduced `χ²` | Aggregate `χ²`/dof | galaxies with `χ²_red` < 1 / < 2 |
|---|---|---:|---:|---:|---:|
| GOD | `cH0/(2π)` = 1.042×10⁻¹⁰, declared anchor `[O]` | 0 | 11.08 | 93.65 | 13 / 27 |
| MOND | literature 1.2×10⁻¹⁰ | 0 | 9.93 | 78.95 | 9 / 27 |
| NFW | — | — | cannot run | — | a halo with no parameters is not a halo |

This is the only tier that discriminates where `a0` came from. **MOND has the lower median here.**

## Tier 1: matched per-galaxy nuisances

374 free parameters = 171 Υ_disk + 32 Υ_bulge + 171 f_d, with Gaussian priors N(0.5, 0.125), N(0.7, 0.175) and N(1, 0.10). `a0` is not fitted in either μ row.

| Model | Free params | Median reduced `χ²` | Aggregate `χ²`/dof | `χ²_red` < 1 / < 2 | Notes |
|---|---:|---:|---:|---:|---|
| GOD | 374 | 3.36 | 6.09 | 21 / 55 | `a0` horizon anchor `[O]` |
| MOND | 374 | 3.41 | 6.03 | 23 / 55 | `a0` literature |
| NFW, free `c` | 716 | 1.92 | 4.58 | 53 / 88 | 97/171 railed at `c = 1`; **not** the ΛCDM row |
| NFW, cosmological-`c` prior | 716 | 5.62 | — | 8 / — | 3/171 railed; the fair ΛCDM-like row (`NFW_CONSTRAINED.json`) |

`716 − 374 = 342` extra NFW parameters versus GOD. Held to its own concentration prior, NFW's median is 5.62 against GOD's 3.36. GOD and MOND differ only in where `a0` comes from: median 3.36 vs 3.41, aggregate 6.09 vs 6.03, so neither leads.

## Strict unit-M/L reproduction check (not the comparison above)

Source: `SPARC_175_summary.json` (`sparc_reproduce.py`). 175 galaxies, 3,391 points (galaxies with at least 3 usable points; velocity errors floored at 1 km/s). Υ_disk = Υ_bulge = 1, f_d = 1. It differs from Tier 0 in sample, error floor and M/L, so its numbers are not interchangeable with Tier 0's.

| Model | Free params | Median reduced `χ²` | Aggregate `χ²`/dof | dof |
|---|---:|---:|---:|---:|
| GOD (`cH0/2π`) | 0 | 15.01 | 69.07 | 3,391 |
| MOND (1.2×10⁻¹⁰) | 0 | 17.01 | 78.05 | 3,391 |
| Baryons only (Newtonian control) | 0 | 51.58 | 204.66 | 3,391 |
| GOD, grid nuisance fit (Υ_disk, Υ_bulge, f_d; same priors) | 2–3 per galaxy | 3.06 | 7.78 | 3,009 |
<!-- END GENERATED: sparc-budget -->

## Working `a0` (not a budget row, a measurement)

`a0 = 1.1607\times 10^{-10}` (μ_std, `N=175`, 3391 points; bootstrap 68% `[1.059, 1.232]`, 95% `[0.972, 1.295]` ×10⁻¹⁰; `A0_DISTANCE_CORRECTED_2026-09-16.json` T1). **Superseded 2026-09-17:** `1.116\times 10^{-10}` ± `0.128` (stat) ± `0.097` (syst) ×10⁻¹⁰, `N=171`, 3375 points, total 14.4%, horizon `0.46\sigma`, MOND `0.52\sigma`, fitted under the retired μ_dual.

## Provenance tags (`PARAMETER_LEDGER.json`)

- GOD `a0`: called “DERIVED, `cH0/2π`” in the JSON, and correctly tagged `[O]` in the same field. The word DERIVED there is historical. This budget treats it as an external cosmological input, not a theorem.
- GOD and MOND `μ`: the same μ_std. It is the corpus's functional choice, irreducible parameter 2, structurally motivated and empirically selected; it is not derived from the action (`CURRENT_STATE_READ_THIS_FIRST.md`, D2). The dual-channel μ_dual of earlier versions is falsified (2026-09-12).
- NFW: two fitted halo numbers per galaxy.
