# Pre-Registered Protocol: P-OM-1, the weak-lensing RAR (KiDS-1000) against the optical map

**Status:** Immutable pre-registered protocol. It was committed, together with the analysis script, before the data comparison was run. Only the model self-check (no data) ran before registration.
**Registered:** 2026-11-25
**Target:** P-OM-1 in `OPTICAL_MAP_v0_2026-11-25.md`, under the tier ruling `OBSERVATION_TIER_DIRECTIVE_2026-11-25.md`. This is a test path, not a closure attempt. The optical map stays `[O]` in every outcome.

## 0. What kind of test this is (declared before the run)

- **A replication.** P-OM-1 says the lensing signal around a galaxy follows the phantom profile set by its baryons alone, with the asymptote ΔΣ → √(G M_b a₀)/(4 G R). Single-metric MOND makes the same prediction. On this data set, Brouwer et al. 2021 (B21, A&A 650, A113) and Mistele et al. 2024 (JCAP 04, 020) already found MOND-like behaviour at a₀ = 1.2×10⁻¹⁰. B21 also found that ΛCDM reproduces the data when its stellar-to-halo mass relation is right (their MICE comparison).
- **What a PASS means.** The observation-tier map passes its first data check with zero free parameters and the corpus's own μ_std and observed a₀. It is not evidence for ITT over MOND or over ΛCDM.
- **What a FAIL means.** P-OM-1 as written (μ_std with the observed a₀) fails on KiDS-1000.
- **New number this produces.** The a₀ that the lensing RAR prefers under μ_std. The corpus's literature sweep records that nobody has extracted it (`02_galaxy_dynamics/literature_sweep_2026-10-28/notes/constraint_landscape.md:104`).

## 1. Disclosure

Before registration, the data README and the main data file were opened. Two bins were checked by hand against deep MOND at a₀ = 1.16×10⁻¹⁰: the lowest-acceleration bin came out within about 6%, and the highest within about 10%. To keep that look from steering the analysis, every choice below is taken from B21's own definitions, not tuned.

## 2. Frozen data

- **Source:** the B21 KiDS-1000 data release, `https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar.tar`, SHA-256 `73adc2d4e848fa0a6a43187f7b5447e749b92eaec4a795b9902b0beaf8a78733`. The script downloads it, checks the hash, and extracts it into the gitignored `04_cosmology/external_data/brouwer2021_rar/`.
- **Primary file:** `Fig-4-5-C1_RAR-KiDS-isolated` (15 bins in g_bar) and its full covariance matrix. Both get the multiplicative bias correction exactly as the README specifies.
- **Observable:** g_obs = 4 G ΔΣ (B21 Eq. 7), using the README constants G = 4.52×10⁻³⁰ pc³ M☉⁻¹ s⁻² and 3.086×10¹⁶ m/pc.
- **Baryons:** B21's g_bar. It counts stars plus cold gas, treats each galaxy as a point mass at R > 30 kpc, and normalises stellar masses to GAMA.
- **Isolation:** B21's criterion, no satellite with more than 10% of the lens's stellar mass within 3 Mpc/h70.
- **Primary range:** g_bar > 7.56×10⁻¹⁴ m s⁻², which leaves 7 bins. This is B21's own boundary (Sect. 4.1): R < 0.3 Mpc/h70 at the sample's mean galaxy mass, where the photometric-redshift isolation is reliable.

## 3. Frozen prediction (zero free parameters)

- **Model:** each lens is a baryonic point mass. The metric potential follows μ_std with a₀ = 1.1607×10⁻¹⁰ m s⁻², the canonical observed value `[E]`.
- **Forward modelling:** the enclosed mass (point mass plus phantom density) is projected exactly into ΔΣ(R), then converted with the same Eq. 7 estimator that was applied to the data, so B21's SIS-conversion bias cancels. The closed form is in the header of `pom1_lensing_rar.py`.
- **Model self-check (run before registration, no data):**
  - deep-MOND limit √y reproduced to 4×10⁻⁵ at y = 10⁻⁴;
  - Newtonian limit (4/π) y reproduced to 10⁻⁶;
  - independent brute-force projection agrees to 1.3×10⁻¹¹;
  - interpolation error 2.5×10⁻¹¹.
- **Effect of the conversion in this data range:** across the data range (y ≤ 0.04), the estimator differs from the plain RAR value ν(y)·y by less than 0.5%.

## 4. Statistic and decision rule (frozen; the script prints the verdict)

The statistic is χ² with the full covariance on the primary range: 7 bins, 7 degrees of freedom, nothing fitted.

- **PASS:** p ≥ 0.01 at nominal masses.
- **PASS_WITHIN_MASS_SYSTEMATIC:** p < 0.01 at nominal masses, but a single uniform shift of g_bar within B21's stellar-mass band (|δ| ≤ 0.2 dex) reaches p ≥ 0.01 (6 degrees of freedom).
- **FAIL:** neither of the above.
- **Power gate:** the Newtonian point mass, (4/π) g_bar through the same estimator, must give p < 10⁻⁶ on the primary range. Otherwise the verdict is `NO_POWER` and no conclusion is drawn.

No other cut, data file, or refit can change the verdict.

## 5. Reported without a verdict

- **S0:** the same χ² at a₀ = 1.0422×10⁻¹⁰ (cH₀/2π, `[D]`).
- **S1:** all 15 bins. Below 7.56×10⁻¹⁴, B21 estimate that satellites can raise ΔΣ by about 30%.
- **S2:** B21's hot-gas variant of g_bar.
- **a₀ fit:** the best a₀ and its Δχ² = 1 interval on the primary range, refit with g_bar shifted by ±0.2 dex.
  - *Declared in advance:* in the deep-MOND regime a₀ ∝ g_obs²/g_bar, so the ±0.2 dex mass systematic moves a₀ by about ±0.2 dex. That is four times the 0.047 dex gap between 1.1607 and 1.0422.
  - The lensing a₀ cannot choose between the two conventions. It is an `[E]` measurement only.
- **S3:** the early/late splits (B21's colour and Sérsic bins).
  - Each bin is compared with the same prediction, and the bins are compared with each other.
  - B21 report a difference of at least 6σ. Mistele et al. 2024, with stricter isolation and consistently estimated masses, find none.
  - This release contains only B21's isolation, so S3 is recorded as a measurement and cannot settle that disagreement.
- **Not tested here:**
  - flatness beyond 0.3 Mpc (the map's "to ~1 Mpc" relies on Mistele 2024's stricter isolation, and their catalogue is not public);
  - the external-field effect.

## 6. Epistemic tags (declared in advance)

- The test outcomes are `[D]`: numbers computed from public data with a fixed script.
- The optical map stays `[O]` in every branch.
  - PASS: P-OM-1 is recorded as replicated on KiDS-1000 with the corpus's a₀ and μ_std (shared with MOND; ΛCDM matches through its stellar-to-halo mass relation).
  - FAIL: P-OM-1 as written is `[X]` on KiDS-1000.
- This is not a JWST test. The quarantine on JWST language in the tier directive stays in force.

## 7. Artifacts

- Script: `03_observer_jwst/pom1_lensing_rar.py`
- Output: `03_observer_jwst/POM1_LENSING_RAR.json`
- Record: `03_observer_jwst/POM1_LENSING_RAR_RECORD_2026-11-25.md`
