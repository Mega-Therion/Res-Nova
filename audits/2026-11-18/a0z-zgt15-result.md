# Track 2 result: a curated `z > 1.5` manifest, and an honest `[U]` on `a₀(z)`

**Date:** 2026-11-18
**Receipt:** `audits/2026-11-18/a0z_zgt15_manifest.py` (exit 0, deterministic)
**Manifest:** `audits/2026-11-18/a0z_zgt15_manifest.json`
**Verdict:** `[U]` — the sample cannot separate constant `a₀` from `a₀ ∝ H(z)`.

---

## 1. `a0_z_fail_closed_runner.py` does not exist

The brief asked me to check before building. It is **not** in Res-Nova. The nearest real artifact is `scripts/a0_highz_pressure_scale_test.py`, which runs on RC100 across the full redshift range and scans the pressure-support systematic. Nothing here fabricates the named runner; this is a new manifest builder plus a shape fit that reuses that script's estimator (fDM route, `μ_std`, at `R_e`).

## 2. Two data-integrity traps, both caught before they corrupted a fit

**(a) RC41 is a strict subset of RC100 at `z > 1.5`.** All 20 of RC41's `z > 1.5` objects carry `in_RC100 = 1`. Combining the two catalogues naively would **double-count every high-z galaxy**. RC41 is therefore used here only as an **inclination source**, joined on `RC100_idx`.

**(b) RC100 carries no inclination column.** The requested `incl ≥ 30°` cut is applicable to only the 20 objects RC41 covers. The fit is reported twice for that reason, and the inclination-unavailable 36 are flagged rather than silently kept.

## 3. The manifest

| source | citation | arXiv / DOI | SHA-256 |
|---|---|---|---|
| RC100 (Table 3) | Nestor Shachar, Price, Morishita et al. 2023, ApJ 944, 78 | arXiv:2209.12199v1 | `162913dcd6f05af0…` |
| RC41 | Genzel, Price, Übler, Förster Schreiber et al. 2020, ApJ 902, 98 | arXiv:2006.03046v2, doi:10.3847/1538-4357/abb0ea | `c1f4eb37ec249f85…` |

Both citations verified against arXiv directly, not inferred from the CSV headers.

- `z > 1.5` objects: **54**
- inclination verified (from RC41, `≥ 30°`): **18**
- inclination unavailable (RC100 has no column): **36**

No withdrawn V1/V2 table is used. The superseded `A0_OF_Z_REPORT.json` (extracted under the falsified `mu_dual`) is not touched; `A0_OF_Z_REPORT_V2.json` covers `z = 0.41–1.44` and so does not satisfy `z > 1.5` either.

## 4. The fit

Model: `ln a₀ = c + n ln E(z) + b(log M_bar − 10.5)`, with `n = 1` the `H(z)`-tied shape and `n = 0` constant. `a₀(SPARC) = 1.1607×10⁻¹⁰ m s⁻²`.

| sample | N | `z` median | `a₀` median | vs SPARC | `n` | 95% CI | `Δχ²` | verdict |
|---|---|---|---|---|---|---|---|---|
| full `z>1.5` | 51 | 2.18 | `2.82×10⁻¹⁰` | 2.43× | −0.745 | [−2.25, 0.92] | 6.08 (2.47σ) | `[U]` |
| incl-verified | 18 | 2.20 | `3.90×10⁻¹⁰` | 3.36× | 0.889 | [−1.35, 7.54] | −0.47 (0.68σ) | `[U]` |

`χ²_ν` = 1.485 (const) / 1.612 (Hubble) for the full sample; 1.939 / 1.908 for the incl-verified subset.

## 5. `[U]` Why this is inconclusive, and the trap in reading it

Both samples leave `n = 0` and `n = 1` inside the 95% interval. The incl-verified subset has `N = 18` and a CI spanning `[−1.35, 7.54]` — it constrains nothing. The full sample reaches only 2.47σ, below the 3σ threshold this corpus uses.

**The trap.** The median `a₀` sits at 2.4–3.4× SPARC at `z ≈ 2.2`, and `E(2.2) ≈ 3.3`. That coincidence is tempting and it is **not** a detection:

1. The within-sample shape fit does not discriminate — the CI covers both hypotheses.
2. The two samples **disagree** (2.43× vs 3.36×) on a quantity that should be robust if it were real.
3. A 2–3× offset in the fDM route at high `z` is exactly what pressure-support and beam-smearing systematics produce — the systematic `a0_highz_pressure_scale_test.py` exists to probe.

So: `[U]`, and the median offset must not be cited as evidence for `a₀ ∝ H(z)`.

## 6. What would resolve it

Not a larger cut of the same data. The binding limitation is that **RC100 has no inclinations and no machine-readable table** (it was transcribed by eye from PDF pages 27–29, per its own header). A real test needs a sample with published per-object inclinations at `z > 1.5` and an independent handle on the pressure-support correction.

## 7. Verdict table

| Claim | Tag |
|---|---|
| `a0_z_fail_closed_runner.py` absent from Res-Nova | `[P]` |
| RC41 `z>1.5` is a strict subset of RC100 (20/20) | `[P]` |
| RC100 has no inclination column | `[P]` |
| Manifest: 54 objects, 18 inclination-verified | `[P]` |
| Both citations verified against arXiv | `[P]` |
| `a₀(z)` shape resolved by this sample | **`[U]` no** |
| Median offset as evidence for `a₀ ∝ H(z)` | **`[U]` not a detection** |
