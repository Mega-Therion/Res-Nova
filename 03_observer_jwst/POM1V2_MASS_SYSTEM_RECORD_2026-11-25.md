# P-OM-1 v2 on KiDS-1000: result record (2026-11-25)

**Pre-registration:** `PREREG_POM1V2_MASS_SYSTEM_2026-11-25.md`. The rule and the frozen script were committed and pushed (`ef4672a0`) before the run.
**Script / output:** `pom1v2_mass_system.py` → `POM1V2_MASS_SYSTEM.json`. It reuses the frozen v1 forward model unchanged.
**What v2 is:** v1 written correctly. All lens-side inputs are moved to the system on which a₀ = 1.1607×10⁻¹⁰ was measured, using conversions published by Mistele et al. 2024:
- H₀ = 73;
- early-type stellar masses ×1.4, late-type ×1.0, on the kinematic stellar-population model;
- hot X-ray gas around early types (Chae et al. 2021 scaling).

Nothing was fitted. The two irreducible inputs (μ_std, a₀) are unchanged.

## Verdict (pre-registered rule): **PASS**

The test uses the colour-split lenses on the reliable range, 7 late-type bins plus 7 early-type bins, with the joint covariance.

| | χ² / bins | p |
|---|---|---|
| **v2: all inputs on the kinematic system** | **17.8 / 14** | **0.22** |
| late types only | 11.1 / 7 | median obs/pred 0.97 |
| early types only | 6.7 / 7 | median obs/pred 1.13 |
| early minus late (universality) | 8.6 / 7 | 0.28 (offset +0.04 dex, not significant) |
| *v1 inputs, same statistic (reference)* | *48.6 / 14* | *1×10⁻⁵ (early minus late 28.1 / 7)* |
| Newtonian point mass (power gate) | — | 3×10⁻⁹³ (gate passed) |

## Robustness (diagnostics)

| Variation | Joint χ² / 14 | p | Early minus late |
|---|---|---|---|
| Sérsic split instead of colour (n > 2 = early) | 14.1 | 0.44 | 3.9 / 7 (p = 0.79) |
| Representative lens mass −0.2 dex (F_ETG = 1.48) | 23.8 | 0.048 | 11.5 / 7 (p = 0.12) |
| Representative lens mass +0.2 dex (F_ETG = 1.88) | 14.3 | 0.43 | 6.9 / 7 (p = 0.44) |
| Without the H₀ = 73 step | 16.2 | 0.30 | 8.6 / 7 |

The pass does not hinge on the H₀ step. It holds over the ±0.2 dex range of representative masses, though only barely at the low end.

## What this means

- **v1's failure was an inconsistent baryon census, not the law.** v1 put the SPARC-calibrated a₀ against early-type masses that were about 1.7× too low on the kinematic scale (stars on a different stellar-population model, and hot gas left out).
- **With one consistent mass system the early/late split disappears.** Late and early types then lie on the same μ_std relation at the same a₀. This is the single-metric expectation, and it agrees with Mistele et al. 2024's own reanalysis.
- **The pass is a consistency re-test, not a blind prediction.** The data were seen in v1. The size of the conversion was computed before registration. Each type uses one mean-mass conversion. B21's looser isolation was used, because this release has no other.
- **A blind test is still needed.** It requires new lensing data (KiDS-Legacy, Euclid) with this frozen recipe.
- **Tags:**
  - P-OM-1 v2: consistent with KiDS-1000 on re-test `[D]`.
  - v1 stays `[X]` as written.
  - The optical map stays `[O]`.
  - ΛCDM is still not separated by these data (B21 MICE).
