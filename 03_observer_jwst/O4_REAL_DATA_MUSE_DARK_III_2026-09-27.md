# O4 redshift test: the 20-point table is withdrawn; real high-z data are inconclusive on a₀(z)

> **⚠️ CORRECTION (same day, 2026-09-27 evening): §3 below overstated MUSE-DARK III.** The corpus already had a
> careful in-house measurement, `02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md`. Its likelihood input is
> RC100 (Nestor Shachar+2023, 100 galaxies, z = 0.6–2.6, source-hash verified), and it lists MUSE-DARK III as an
> external comparison row. Read together:
> - **The level agrees.** a₀ at z ~ 1–2 is ~2–2.6× the local value in both samples: RC100 gives 2.60× at
>   z = 0.87 and 2.29× at z = 1.96, relative to SPARC T3; MUSE-DARK III gives 2.05×.
> - **The shape inside the high-z range favours a CONSTANT, not H(z).** RC100's Hubble shape is worse by
>   Δχ² ≈ 9–21 (shape-only, stat-only). This is the only calibration-independent result. It is not
>   established, for three reasons: the photometric prior trend, untested Vc/beam-smearing bias, and failed
>   estimator self-tests.
> - **The step from z = 0 is calibration-limited.** With a 0.5-in-ln cross-method nuisance, constant a₀ becomes
>   the best fixed reading.
> - **Verdict: no reading is excluded.** The 13.4σ and 6.5σ pulls in §3 are anchored and statistical only; the
>   in-house audit shows such anchored σ values are uncalibrated. They are **withdrawn**.
> - **The a₀(0) = 1.00 ± 0.04 "match" to cH₀/2π is also withdrawn as evidence.** It is the intercept of a linear
>   model, and the flat high-z shape makes that intercept unreliable.
> - §1 (the table withdrawal) stands.


**Date:** 2026-09-27. **Tags:** `[C]` cited · `[D]` derived here · `[X]` withdrawn · `[O]` open.

## 1. The table used by `a0_of_z.py` and `a0_of_z_v2.py` is withdrawn `[X]`

Both scripts use 20 hardcoded (z, log g_bar, log g_obs, σ) points, labelled `udf10_01`…`udf10_20` and
attributed to "Bouché et al. (A&A 654, A49, 2021) and Mercier et al. (A&A 667, A75, 2022)". The repo's own
`gate2_inference.py` had already flagged them for missing provenance (Gate 1). Checked 2026-09-27:

- **Bouché et al. 2021, A&A 654, A49** exists: MUSE HUDF Survey XVI, the angular momentum of low-mass
  star-forming galaxies. It is a pilot study of **nine** z ≈ 1 galaxies. It does not contain a 20-point
  (z, g_bar, g_obs) table.
- **"Mercier et al. 2022, A&A 667, A75"** was not found. The Mercier et al. 2022 paper that does exist is
  **A&A 665, A54** (MAGIC survey scaling relations), which is a different article.
- The table itself is suspiciously regular. The redshifts rise monotonically and evenly from 0.413 to 1.440,
  and log g_bar alternates high and low.

Neither cited source contains the table. **It is withdrawn from all use.** The v1 5.9σ result was already
retracted `[X]` (2026-09-12). The v2 "inconclusive, 2.06σ" result was computed on the same table and is
**void** too. The scripts are kept as history, with a withdrawal note in their headers.

## 2. The real dataset `[C]`

**Ciocan, Bouché, Fensch, Krajnović, Freundlich, Desmond, Famaey & Techi 2026**, "MUSE-DARK III: The
evolution of the radial acceleration relation at intermediate redshifts", arXiv:2604.22613 (A&A, 2026).

- **Sample.** 79 star-forming galaxies, complete above M* > 10^8.8 M☉, at 0.33 < z < 1.44, from the MUSE
  HUDF.
- **Modelling.** 3D forward modelling with a disk-halo decomposition and pressure-support corrections.
- **RAR form.** McGaugh's a_tot = a_bar/(1 − e^{−√(a_bar/a₀)}).
- **Result.** a₀ rises with z. A linear fit gives **a₀(z) = (1.00 ± 0.04) + (1.59 ± 0.10)·z, in units of
  10⁻¹⁰ m/s²**. The whole sample gives a₀(z ≈ 1) = 2.38 ± 0.1. Across the four equal-population z-bins,
  a₀ goes from ≈ 1.99 (lowest) to ≈ 2.71 (highest).
- **Authors' reading.** The evolution is "faster than that of H(z)".
- **Data.** A per-galaxy data release is not stated.

## 3. What it says about O1 and O4 `[D]`, using the published summary numbers only

**The extrapolated local value matches the horizon scale.** a₀(0) = 1.00 ± 0.04 against the derived
cH₀/2π = **1.042** × 10⁻¹⁰ m/s². That is agreement at 1σ. The literature value 1.2 is 5σ away.
- Caveat: this a₀(0) extrapolates a linear fit from z ≥ 0.33. It is not a local measurement.

**Evolution models against the whole-sample point**, a₀ = 2.38 ± 0.1 at the implied median z = 0.87. All
predictions start from cH₀/2π, and the uncertainties are statistical only.

| model | predicted a₀(0.87) | pull |
|---|---|---|
| constant a₀ (AeST as written; O4's H_const) | 1.04 | +13.4σ |
| a₀ ∝ H(z) (O4's H_horizon) | 1.73 | +6.5σ |
| a₀ ∝ (1+z)^1.5 | 2.67 | −2.9σ |
| a₀ ∝ (1+z)^1.3 | 2.35 | +0.3σ |

**Reading.**
- **A constant a₀ is strongly disfavoured by this dataset.** That includes AeST as used in the corpus, where
  a₀ is a fixed constant.
- **The simplest horizon extension, a₀ ∝ H(z), has the right sign and the right local normalisation, but
  grows too slowly.**
- **The data prefer roughly a₀ ∝ (1+z)^1.3.** That is one summary point, so treat it as orientation, not a
  fit.
- **Systematics are not assessed here.** The authors note stellar M/L values below SPARC's; the IMF and
  pressure support also matter. A per-galaxy re-analysis with our own μ_std needs their data. Until then,
  every entry above is `[C]`-based.

## 4. Consequence for the covariant completion `[O]`

If a₀ really evolves, a constant-a₀ AeST cannot be the whole story. One natural covariant route uses the
aether itself. Its expansion scalar θ = ∇_μu^μ equals 3H on FLRW, so an acceleration scale built from θ
tracks the cosmic expansion automatically.
- Open problem: inside bound systems the local aether expansion is not 3H (D3 note 7 §32: the aether moves
  with the matter).
- Whether this route exists in the literature has not been checked. **Check before claiming.**

## Reproduce

`python3 03_observer_jwst/o4_muse_dark_iii_compare.py` regenerates `O4_MUSE_DARK_III_COMPARE.txt`.
