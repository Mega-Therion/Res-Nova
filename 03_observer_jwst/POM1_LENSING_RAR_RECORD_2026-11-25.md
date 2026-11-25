# P-OM-1 on KiDS-1000: result record (2026-11-25)

**Pre-registration:** `PREREG_POM1_LENSING_RAR_2026-11-25.md`, committed and pushed (`af7d6564`) together with the frozen script before the data comparison ran.
**Script / output:** `pom1_lensing_rar.py` → `POM1_LENSING_RAR.json`. Post-hoc cross-check: `pom1_posthoc_gama.py` → `POM1_POSTHOC_GAMA.json`.
**Data:** Brouwer et al. 2021 (B21, A&A 650, A113) KiDS-1000 lensing-RAR release, SHA-256 `73adc2d4…8733`.

## Verdict (pre-registered rule): **FAIL**

P-OM-1 as written fails on the KiDS-bright isolated lenses. "As written" means: μ_std, the observed a₀ = 1.1607×10⁻¹⁰, and baryons = stars + cold gas. Under the pre-declared tag, P-OM-1 as written is `[X]` on KiDS-1000. The optical map itself stays `[O]`.

| Primary range (7 bins, g_bar > 7.56×10⁻¹⁴) | χ² / dof | p |
|---|---|---|
| μ_std, a₀ = 1.1607×10⁻¹⁰ `[E]` | 52.1 / 7 | 6×10⁻⁹ |
| μ_std, a₀ = 1.0422×10⁻¹⁰ `[D]` | 67.4 / 7 | <10⁻¹¹ |
| Best uniform mass shift within ±0.2 dex (δ = +0.18 dex) | 21.9 / 6 | 0.0013 |
| Newtonian point mass (power gate) | 740 / 7 | 10⁻¹⁵⁵ (gate passed) |

- **Size of the miss:** the data lie a median 19% above the prediction. Six of the seven bins are high, by 1.4σ to 4.8σ; the highest-acceleration bin is 11% low.
- **No fitted a₀ rescues it:** the best fit (a₀ = 1.77×10⁻¹⁰) still gives χ² = 21.0 / 6 (p = 0.002). The residual has a slope, and no constant can remove a slope.
- **Same result as the original paper:** B21 found the same thing for MOND on these points: χ²_red = 4.0 on the 7 reliable bins, about 3.8σ (their Sect. 5.2).

## Where the failure comes from (diagnostics, no verdict)

| Sample (reliable range) | χ² / 7 at a₀ = 1.1607 | p | a₀ fitted (stat 1σ) |
|---|---|---|---|
| All isolated lenses | 52.1 | 6×10⁻⁹ | 1.77 (1.65–1.90) ×10⁻¹⁰ |
| Late types, low Sérsic index | **3.6** | **0.82** | 1.03 (0.88–1.19) ×10⁻¹⁰ |
| Late types, blue (u−r) | 12.3 | 0.09 | 0.95 (0.80–1.11) ×10⁻¹⁰ |
| Early types, high Sérsic index | 36.6 | <10⁻⁵ | 2.14 (1.93–2.35) ×10⁻¹⁰ |
| Early types, red (u−r) | 36.4 | <10⁻⁵ | 2.21 (2.01–2.42) ×10⁻¹⁰ |
| All, g_bar including B21's hot-gas estimate | 27.2 | 3×10⁻⁴ | 1.60 (1.50–1.71) ×10⁻¹⁰ |

- **Late types pass with no adjustment.** Disc galaxies are the population SPARC measures, and their lensing RAR matches μ_std at the observed a₀. In the low-Sérsic sample that holds at p = 0.82.
- **Early types sit 0.15 dex higher.** Red minus blue gives χ² = 28.1 / 7 (p = 2×10⁻⁴); the Sérsic split gives χ² = 20.9 / 7 (p = 0.004). This is B21's early/late difference. It is a problem for every single-metric theory, MOND included, and the map gives no new lever on it.
- **Two published explanations remain open:**
  1. *Unseen baryons around early types.* With B21's rough hot-gas estimate (hot gas equal to the stellar mass within 100 kpc), the combined sample passes within the mass band: δ = +0.14 dex gives χ² = 7.7 / 6, p = 0.26.
  2. *Isolation leakage.* Red galaxies cluster more. Mistele et al. 2024 (JCAP 04, 020) used a stricter isolation criterion with consistently estimated masses and found no early/late difference.

  Neither explanation can be checked with this data release.
- **Post-hoc, outside the verdict.** B21's spectroscopic GAMA sample has reliable isolation at all radii. There the same frozen model gives χ² = 18.9 / 15 (p = 0.22) over all bins, and 14.9 / 7 (p = 0.04) over the primary range. Its errors are about 4× larger. B21 report χ²_red = 0.8 for MOND on GAMA.

## The lensing a₀ (`[E]`, a new number for the corpus)

- **Late-type lenses:** 0.95–1.03×10⁻¹⁰ (statistical error ±15%). This is consistent with both 1.1607 `[E]` and 1.0422 `[D]`.
- **The stellar-mass systematic dominates.** A shift of ±0.2 dex moves the fitted a₀ by about ±0.2 dex; for the full sample the range is 1.11–2.82×10⁻¹⁰. As declared in the pre-registration, this cannot choose between the two a₀ conventions.
- **The a₀ depends on the population.** Early and late types differ by a factor of about 2.2. So until the early-type baryon budget or the isolation question is settled, "the lensing a₀" is not one number.

## What this changes

- **P-OM-1 as written is `[X]` on KiDS-1000** (B21 isolation, stars + cold gas). The scoped claim, that late-type lensing follows the baryons alone at the observed a₀, survives as a measurement, not a verdict. Testing it properly needs a new pre-registration on independent data.
- **The optical map's lensing tier inherits MOND's early-type problem.** A theory reading would need early types to carry roughly their stellar mass again in unseen gas, or the published early/late offset to be an isolation artefact (Mistele 2024).
- **ΛCDM is not excluded.** B21 report that the MICE ΛCDM mock reproduces the KiDS lensing RAR (χ²_red = 2.3). This data set does not separate geometric lensing from particle halos.
