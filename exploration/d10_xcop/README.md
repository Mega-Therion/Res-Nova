# D10 AeST cluster test on X-COP: passes at R₅₀₀, fails at R₂₀₀ (2026-11-19)
Pre-registered in `PREREG.md` (a2ea966, before any number). Data in `xcop_data.tsv`: Ettori et al. 2019; Eckert et al. 2019, with gas and non-thermal-corrected total mass measured to R₂₀₀. Script `xcop_test.py` → `XCOP_RESULT.json`. 12 clusters.

| Model | median R₅₀₀ | in [0.7, 1.4] | median R₂₀₀ | in [0.7, 1.4] |
|---|---|---|---|---|
| Pure MOND (μ_std) | 1.90 | 0/12 | 1.49 | 2/12 |
| AeST static | 0.80 | 9/12 | 0.60 | 1/12 |
| **AeST supply-capped** | **0.83** | **12/12 (CLOSES)** | **0.62** | **1/12 (FAILS)** |

**What it means.**
- **At R₅₀₀ the pre-registered primary criterion passes.** This is the first time in the corpus: on clusters with measured outer gas, AeST's dust sector (well-posed virial boundary, cosmic supply cap) accounts for the mass at R₅₀₀ in every cluster, with no tuning.
- **At R₂₀₀ it fails by overshooting.** From R₅₀₀ to R₂₀₀ the model adds too much mass: R falls 0.83 → 0.62 while pure MOND's rises toward 1. The extra AeST mass is too extended.
  - Its radial profile, not its amount, is now the discriminating failure.
  - The R₂₀₀ figure sits 4% inside the Φ(r_v) = 0 boundary, so it is the most boundary-sensitive number in the test.
- The supply cap binds in 4/12 clusters (A2029, A2142, A3266, ZwCl1215). The median dust need is 0.76 of the cosmic allowance.
- **Gas profile.** A β-model fitted to the two measured gas masses (β = 0.58–0.86, r_c = 0.1 R₅₀₀). The inner shape is assumed, but the masses at both test radii are measured.

**Verdict.** Mixed, and sharper than any earlier D10 result. The cluster mass at R₅₀₀ is reproduced (12/12); the mass growth to R₂₀₀ is not (1/12).
- **[O], the next question:** what sets the AeST dust's outer profile? Candidates are the boundary radius (the splashback radius rather than r_v) and the onset of the x_H screen in the cluster outskirts, which the static solve here does not include.
