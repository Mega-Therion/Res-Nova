# Pre-Registered Protocol: P-OM-1 v2, the lensing RAR on the kinematic mass system

**Status:** Immutable pre-registered protocol. It was committed and pushed together with the analysis script before the script ran on data.
**Registered:** 2026-11-25
**Supersedes nothing.** P-OM-1 v1 stays on record as FAIL as written (`POM1_LENSING_RAR_RECORD_2026-11-25.md`, `[X]` on KiDS-1000). v2 is a new, corrected statement of the claim, and it gets its own verdict.

## 0. What was wrong with "as written", and what v2 changes

v1 compared an a₀ measured on the SPARC (kinematic) system with lensing data whose inputs were on a different system. Mistele et al. 2024 (JCAP 04, 020, Sects. 3–4) list the differences and publish the conversions. v2 applies those conversions to the lens side. Nothing is fitted to lensing here, and the two irreducible inputs (μ_std and a₀ = 1.1607×10⁻¹⁰) stay fixed:

1. **Distance scale.** The kinematic system uses H₀ = 73. g_obs scales as h, so the data are multiplied by 73/70. g_bar does not depend on h.
2. **Stellar masses.** They are moved onto the kinematic stellar-population model (Schombert & McGaugh 2014): M* = Q M*_KiDS. Here Q = 1.0 for late types and Q = 1.4 for early types, as Mistele et al. measured by re-analysing the KiDS photometry. The colour split is u − r = 2.5, the same as B21's.
3. **Gas.** Late types keep B21's cold gas, which Mistele et al. call "practically indistinguishable" from theirs. Early types carry hot X-ray gas from the Chae et al. 2021 scaling, M_hot = 10^−5.414 M*^1.47 (M* on the converted system), and no cold gas.
4. **Representative mass.** The gas terms depend on mass. They are evaluated at log M*_KiDS = 10.61, B21's isolated-sample mean; the colour samples are mass-matched to within 0.025 dex.
   - This gives F_ETG = 1.672 (g_bar × 1.672) and F_LTG = 1.000.
   - Cross-check: Mistele et al. state that Q_ETG ≈ 1.7 with B21's gas would give similar results.

## 1. Disclosure (this is a consistency re-test, not a blind test)

- The KiDS data were seen in v1. Late types passed and early types were 0.15 dex high.
- Before registering, I computed the conversion's size: about +0.11 dex in the deep-MOND prediction for early types, and +0.018 dex in the data from H₀.
- Mistele et al. (their Appendix D.2) report that their masses with B21's looser isolation (3 Mpc rather than their 4 Mpc) reduce the early/late difference but do not remove it. This release only contains B21's isolation.
- So a PASS here is weaker evidence than v1's FAIL was. The blind test of v2 needs independent lensing data (KiDS-Legacy, Euclid).

## 2. Frozen data and model

- **Data:** B21 colour-split release files (`Fig-8_RAR-KiDS-isolated_Colorbin_1/2`, joint covariance), the same tarball and SHA-256 as v1.
- **Reliable range:** set by the original bins, g_bar,B21 > 7.56×10⁻¹⁴ (R < 0.3 Mpc/h70). That gives 7 late-type and 7 early-type bins, 14 in total.
- **Model:** the frozen v1 forward model, unchanged: point masses, μ_std, a₀ = 1.1607×10⁻¹⁰, and B21's own ΔΣ → g estimator. Each type's bins are relabelled g_bar → F_type · g_bar.

## 3. Statistic and decision rule (frozen; the script prints the verdict)

The statistic is the joint χ² over the 14 bins with the full joint covariance. No parameter is fitted.

- **PASS:** p ≥ 0.01.
- **PASS_WITHIN_MASS_SYSTEMATIC:** p < 0.01, but one uniform shift |δ| ≤ 0.2 dex of all g_bar gives p ≥ 0.01 (13 degrees of freedom).
- **FAIL:** otherwise.
- **Power gate:** a Newtonian point mass on the converted masses must give p < 10⁻⁶. Otherwise the result is `NO_POWER`.

## 4. Reported without a verdict

- Per-type χ², and the early-minus-late difference of fractional residuals (joint covariance, first-order propagation). The difference tests universality.
- The Sérsic split (n > 2 treated as early type) with the same conversion. Mistele's Q is defined by colour, so this is approximate.
- Sensitivity of the colour result to the representative mass (±0.2 dex) and to leaving out the H₀ conversion.
- The v1 inputs on the same joint statistic, for reference.

## 5. Tags (declared in advance)

- Outcomes are `[D]`. The optical map stays `[O]`. v1 stays `[X]` as written.
- **PASS:** "P-OM-1 v2 (all baryons on the kinematic mass system) consistent with KiDS-1000 on re-test; blind test pending."
- **FAIL:** the mass-system conversion alone does not reconcile P-OM-1 with KiDS-1000 under B21's isolation.

## 6. Artifacts

- Script: `03_observer_jwst/pom1v2_mass_system.py` (imports the frozen v1 model from `pom1_lensing_rar.py`)
- Output: `03_observer_jwst/POM1V2_MASS_SYSTEM.json`
- Record: `03_observer_jwst/POM1V2_MASS_SYSTEM_RECORD_2026-11-25.md`
