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

## Screen consistency: tests A, B, C (`../tidal_aest/PREREG_XH_BARYONIC.md`, pre-registered per stage)
**Gap found in review.** The candidate's virial screen S_lin(x_H) was validated on SPARC using x_H from the *observed* field. In a theory without dark matter, "Φ_N" is ambiguous: it could mean the baryonic field or the full metric potential.

| Test | x_H defined on | Result |
|---|---|---|
| **A**: SPARC | baryons | 1.9% of points have S < 0.99 at 154, against the 1% rule: **fails narrowly**. Minimum x_H = 363, so S ≥ 0.85. The largest passing value is x_H,low = 110. |
| **B**: X-COP, S on MOND | baryons, x_H,low = 110 | R₅₀₀ = 2.11, R₂₀₀ = 2.56: **fails decisively**. Baryonic x_H is only about 26–65 in cluster outskirts, so MOND is screened off there. |
| **C**: X-COP, S on MOND | full metric potential (self-consistent; converged to 3×10⁻⁴), x_H,low = 154 | **R₅₀₀ = 0.92, 12/12: passes.** R₂₀₀ = 0.755, 8/12: **fails narrowly**, improved from 0.62 and 1/12. |

**Conclusions.**
- **The screen must be defined on the full metric potential.** The baryonic definition is ruled out [X] by clusters (B), and is marginal on SPARC (A). The full-field definition keeps SPARC at 0% (as in `xh_screen.py`) and leaves linear growth unchanged (linear modes have x_H ≲ 1 either way). It is also the natural covariant choice, since Ψ = Φ is the metric potential.
- With it, the candidate reproduces cluster masses at R₅₀₀ (12/12, median 0.92). At R₂₀₀ it comes within one cluster and 0.045 in the median of the pre-registered criterion.
- Median S at R₂₀₀ is 0.82: the screen is acting in the outskirts, exactly where the overshoot was.
- **Remaining [O]:** a residual ~25% outer overshoot at R₂₀₀. The candidates (not tuned here) are the boundary radius (splashback), the inner gas shape (β-model assumed), and the 5–15% non-thermal-pressure corrections already folded into M_tot.

## R₂₀₀ systematics sweep (`PREREG_SYSTEMATICS.md`, `xcop_systematics.py` → `XCOP_SYST_*.json`)
Each systematic was varied one at a time within its physical range, and every configuration is reported.

| Configuration | R₅₀₀ (median, in band) | R₂₀₀ (median, in band) |
|---|---|---|
| Baseline (Test C) | 0.922, 12/12 | 0.755, 8/12 |
| Gas core r_c = 0.05 R₅₀₀ | 0.921, 12/12 | 0.776, 9/12 |
| Gas core r_c = 0.2 R₅₀₀ | 0.924, 12/12 | 0.771, 9/12 |
| M_HSE (no non-thermal correction) | 0.881, 11/12 | 0.710, 7/12 |
| Boundary 1.2 r_v | 0.844, 11/12 | 0.600, 3/12 |
| Boundary at splashback (≥ 1.4 r₂₀₀) | — | ill-posed: past the Lane–Emden radius for 5–11/12 clusters (§14) |

**Verdict: not closed, and not systematics-limited.**
- **R₅₀₀ is robust:** it passes in every configuration.
- **R₂₀₀ is robust too, but as an overshoot.** Every allowed configuration gives a median of 0.60–0.78. The best variant reaches 9/12, but its median is still below 0.8.
- So the excess dynamical mass at R₂₀₀ (about 25%) is a genuine prediction of this model, not a modelling artefact. **[D]: the candidate's mass profile is too extended between R₅₀₀ and R₂₀₀.**
- That makes it a falsifiable target. Weak-lensing mass profiles to R₂₀₀ on X-COP-like clusters would confirm or kill it.
