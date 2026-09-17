# a0(z) at high redshift: measurement audit (2026-09-16)

Branch `measure/a0-highz`. Follows PR #67 (`LIGHT_CONE_A0_AUDIT_2026-09-16.md`) and
`HORIZON_SELECTION_AUDIT_2026-09-16.md`. Every a0(z) number here is **[C]** (it depends on a
dynamical-fit calibration that this audit cannot remove).

## Verdict

**The data cannot tell Hubble-form growth from constancy.** [O]

- **Growth from z = 0 to the high-z sample.** The high-z normalization is flat at about 2.2 to 2.6 times a0_T3.
  With the SPARC anchor pinned and statistical errors only, that step "rejects" constancy.
  The step is not established as physics: it disappears once a cross-method calibration
  term of 0.5 in ln is allowed, and each listed systematic on its own is about that size.
- **Shape within z = 0.6 to 2.6.** Every variant favors a constant shape.
  The Hubble *shape* is worse by Δχ² 8.9 to 19.8, statistical errors only.
  The free slope n has a 95% interval that contains 0 in all nominal variants.
  This is the only result that does not depend on the calibration, and it leans toward **constancy**.
  It is still **not** established, for three reasons:
  (i) fDM comes from the same GR+NFW fit as a photometric prior whose own z-trend (+0.53) is near the fitted trend (+0.38);
  (ii) a z-dependent Vc or beam-smearing bias was not tested;
  (iii) the estimator fails its own bias and coverage self-tests (S6, S8).
- **Recommended citation:** "high-z a0 is flat across z = 0.6 to 2.6 at [C]; the step from z = 0 is calibration-limited; no reading is excluded" [O].

## Datasets and provenance

| file (`02_galaxy_dynamics/highz_data/`) | role | provenance check |
|---|---|---|
| `RC100_NestorShachar2023_table3_transcribed.csv` | **only likelihood input** (100 galaxies) | source-hash PASS (arXiv:2209.12199v1 PDF). Transcription was re-checked by eye: 1400 cells, 0 fixes. A reviewer re-read rows 41 to 80 against p.28, and all match. The Σ_DM column recomputes for 100 of 100 rows. |
| `RC41_Genzel2020.csv` | dedupe; photometric-input M_bar for the prior-trend test | source-hash PASS; all 41 rows map onto RC100 |
| `G17_Genzel2017.csv` | dedupe only | source-hash PASS; all 6 rows map onto RC100 |
| `Ubler2017_KMOS3D_TFR.csv` | BTFR cross-check only | source-hash PASS. Cells were **not** compared against the .dat file. |
| `HighZ_TF_published_fits.csv` | Ubler bTFR offsets (flagged as regime-limited) | HAND (typed from the TeX; no hash) |
| `Ciocan2026_MUSEDARKIII_a0.csv` | external comparison row, not merged | HAND |
| other CSVs (KROSS, ALPAKA, z≈4.5, ALESS073, KMOS3D release) | built, not used in this measurement | provenance headers present |

The anchor is `A0_DISTANCE_CORRECTED_2026-09-16.json`, row **T3** (non-flow SPARC, μ_std): a0 = 1.16306e-10, 95% [0.9664, 1.3239]e-10, σ_ln = 0.0805.
(CURRENT_STATE's 1.1607e-10 is T1, all 175 galaxies.)
Source PDFs and TeX are in `highz_data/_src/`, which is gitignored and not committed.
In `fetch_highz_data.sh`, "PASS" now reads "source-hash only; cell values not re-compared".

## Method and leverage

- **Interpolating function.** μ_std(x) = x/√(1+x²), with exact inverse a0 = (g/g_bar)·√(g² − g_bar²) [P]. The helper module is `02_galaxy_dynamics/highz_a0_method.py`.
- **Two routes.** The fDM route uses g_bar = (1−fDM)·g_obs. The M_bar route uses g_bar = k·G·M_bar/Re², with k = 0.5368 (oblate q = 0.2).
  Both come from the same Genzel-team fit, so the M_bar route is a consistency check, not an independent measurement.
- **Leverage.**
  - Per-galaxy information on ln a0 scales as x⁻⁴. The median g_obs/a0 is 2.29, and only 11% of the sample has x < 1.
  - No single galaxy constrains a0. The estimator is a population errors-in-variables likelihood per z-bin (`JointA0Likelihood`).
  - The Fisher estimate on all 100 galaxies is σ(ln a0) = 0.091.
- **Selection.** RC100 was chosen for extended rotation curves, which favors massive, baryon-dominated disks. The informative regime x < 1 is under-represented.
- **Distance dependence.** The fDM route scales as D^(−1 − w(1+x²)), where w is the unknown weight of the photometric prior [O].
  At w = 0 the slope is −1, and re-assuming the cosmology moves ln a0 by ≤ 0.04.
- **Cosmology.** Readings are evaluated in Planck 2018 (67.36, 0.3153); RC100 distances use (70, 0.3).
  The difference is ≤ 0.03 in ln at w = 0 and 1.654 vs 1.629 in the H(z) prediction at z = 0.87.
  Both are far below the systematics. Recorded and not changed.

## a0(z)/a0_T3 (fDM route; statistical intervals, `a0_highz_measurement_run.txt`)

| bin | N | z_eff | a0/a0_T3 | 95% | Hubble pred | Λ | Kodama |
|---|---|---|---|---|---|---|---|
| z < 1.2 | 32 | 0.867 | 2.597 | [1.954, 3.427] | 1.654 | 1.000 | 0.948 |
| z ≥ 1.2 | 68 | 1.960 | 2.286 | [1.930, 2.685] | 2.976 | 1.000 | 1.200 |

With 4 bins, the fDM route gives 2.471, 2.634, 2.544 and 2.196; the M_bar route gives 3.234, 3.208, 3.087 and 2.257.
With 2 bins, the M_bar route gives 3.363 and 2.491.
External: Ciocan+2026 a0(z~1) = 2.38e-10 (95% CI, ΛCDM decomposition). That is 2.05× a0_T3, or 1.98× the paper's own local 1.2e-10.

## Model comparison, all variants

### Nominal variants

Columns 3 to 5 give the significance of each reading against the free power law (1+z)^n.

- **stat-only:** the nominal 1-dof σ, anchored.
- **cov-corr:** Δχ²/1.75, correcting for the helper's cov68 ≈ 0.55.
- **+calib:** the anchor carries an extra 0.5 ln cross-method nuisance.

| variant | power-law GOF χ²/dof (p) | stat-only H / Λ / K | cov-corr H / Λ / K | +calib H / Λ / K | +calib n 95% | shape-only χ² H / Λ / K, n 95% |
|---|---|---|---|---|---|---|
| fDM 2-bin | 9.04/1 (0.003) | 3.00 / 7.27 / 6.33 | 2.27 / 5.50 / 4.78 | 3.73 / 0.33 / 1.87 | [−0.49, 0.70] | 17.19 / 0.63 / 4.80, [−0.99, 0.43] |
| fDM 4-bin | 12.70/3 (0.005) | 2.87 / 7.04 / 6.19 | 2.17 / 5.32 / 4.68 | 4.11 / 0.16 / 2.58 | [−0.49, 0.57] | 20.93 / 1.17 / 8.60, [−0.88, 0.35] |
| M_bar 2-bin | 9.86/1 (0.002) | 1.88 / 5.57 / 5.29 | 1.42 / 4.21 / 4.00 | 2.70 / 0.49 / 1.66 | [−0.59, 0.97] | 12.46 / 1.48 / 4.76, [−1.74, 0.40] |
| M_bar 4-bin | 11.68/3 (0.009) | 2.16 / 5.49 / 5.26 | 1.64 / 4.15 / 3.97 | 3.13 / 0.34 / 1.98 | [−0.61, 0.85] | 15.44 / 1.85 / 6.46, [−1.63, 0.34] |

### Reading the table

- **The reference model fits badly.** The anchored power law is rejected at p ≈ 0.002 to 0.009, so the anchored σ values are not calibrated.
  Birge-rescaled values are in the run log; for example, Λ drops to 2.4σ in fDM 2-bin.
- **The anchored ranking reverses with the nuisance.** Adding the calibration nuisance makes Λ the best fixed reading in every variant.
  Hubble becomes the worst, at 2.7 to 4.1σ against the power law.
- **These σ are indicative only.** They are 1-dof Wilks conversions on non-nested readings and were not bootstrap-calibrated.

### Mass-shift systematics (2-bin, ±0.2 dex)

The fDM route assumes w = 1, the prior-dominated case. At w = 0 the fDM route does not change.

| route | shift | anchored favorite (no nuisance) | +calib favorite | shape-only favorite |
|---|---|---|---|---|
| fDM / M_bar | M* +0.2 | Λ / Λ | Λ / Λ | Λ / Λ |
| fDM / M_bar | M* −0.2 | Hubble / Hubble | Λ / Λ | Λ / Λ |
| fDM / M_bar | gas +0.2 | Λ / Hubble | Λ / Λ | Λ / Λ |
| fDM / M_bar | gas −0.2 | Hubble / Hubble | Λ / Λ | Λ / Λ |

## Systematics budget, in ln a0

The Hubble vs constant separation at z = 1 is 0.58. Every row below is comparable to it.

| source | shift | size |
|---|---|---|
| fDM zero-point | ±0.05 / ±0.11 | +0.22/−0.24 / +0.46/−0.54 |
| Vc scale | ±5% (V_bar fixed) | +0.46/−0.50 |
| pressure-support α | 0.5 / 1.5 | −0.55/+0.41 |
| IMF, w = 1 | +0.23 / −0.20 dex | −0.82 / +0.63 |
| gas, w = 1 | ±0.25 dex | up to −0.93/+0.73 |
| M_bar-route geometry | k from q = 0.2 to a deprojected sphere | +0.91 |
| BTFR H0 zero-point | — | 0.161 |

Vc-scale and pressure-α variants were **not** added to the flip table. A z-dependent beam-smearing bias was not tested [O].

## Checks, as measured

- **`scripts/a0_highz_measurement.py`:** exit 0, 10/10 pass. Runtime 187 s.
  - C5: bias −0.0265, cov95 0.93.
  - C6 and C7: rejection rate 1.00, but these are **unverified guards**. Inflating errors ×3 did not make them fire.
  - C9: 0.96 shuffled vs 0.17 unshuffled.
- **Earlier sabotage runs, on copies:**
  - Broken dedupe made C3 FAIL, exit 1.
  - Truth ×1.5 made C5 and C8 FAIL, exit 1.
  - Disabling the shuffle made C9 FAIL, exit 1.
  - Errors ×3 produced no FAIL, exit 0.
- **Helper self-test** (`highz_a0_method.py --jobs 8 --n-real 60 --n-real-aux 30`): **exit 1, 15/18**, 250 s.
  - S6 FAIL: max |Δln a0| = 0.0418.
  - S8 FAIL: bias −0.0392 at 1× and −0.0416 at 1.791×.
  - These estimator defects are open.
  - Log: `highz_data/highz_a0_method_selftest_run.txt`.

## What is established

| claim | label |
|---|---|
| μ_std inversion, leverage x⁻⁴, and distance slopes | [P] |
| RC100 transcription matches the source (100/100 Σ_DM; 40 rows re-read by eye) | [D] |
| high-z a0 (Genzel-team calibration) ≈ 2.2 to 2.6× a0_T3, flat across z = 0.6 to 2.6 | [C] |
| Hubble-form growth | **not established** [O] |
| constancy | **not established** (favored in shape, [C]) [O] |
| Kodama form | **not established** [O] |
| exclusion of any reading at Nσ | **withdrawn**: the anchored σ are uncalibrated and systematics-dominated |
| BTFR-route a0 | not convertible (only 11% of the sample has x < 1) |

## Stray plot `a0_z_analysis.png` (not ours; untouched, untracked, added to `.git/info/exclude`)

The plot was made by a Gemini antigravity-ide session (brain 7a3ec09f…, `scratch/a0_z_analysis.py`). Do not cite it or its χ²/ν values.

| plotted point | verdict |
|---|---|
| Ciocan+2026 2.38e-10 | **real** (95% CI). The plotted linear model uses the wrong intercept (1.20 instead of the paper's 1.0), and the plot overstates the claim ("EXCLUDES constant"). |
| Ubler+2017 1.05e-10 | **fabricated as an a0**. That paper measures a TF zero-point. |
| Genzel+2020 / "Mercier+2022" 1.15e-10 | **fabricated**. No such a0 value exists in the source. |
| Milgrom 2017 1.3e-10 | **fabricated as a measurement**. The paper only excludes ~4a0 at z~2. |
| local 1.20e-10 | real (standard SPARC RAR value) |

Three of the five points are invented, so the plot's fits are meaningless.
Its legend also labels the worse model (χ²/ν 39.6 vs 20.4) as "BEST FIT".

## Reviewer issues

**Fixed:**
1. Power-law goodness of fit is now reported per variant (χ²/dof, p), with Birge-rescaled σ alongside.
2. Coverage undercoverage: cov68-corrected σ (Δχ²/1.75) is reported. The raw values are labelled stat-only nominal.
3. Anchor step has no calibration term: a 0.5 ln cross-method nuisance variant was added, and it reverses the anchored ranking.
4. Non-nested 1-dof conversion and look-elsewhere: σ values are labelled indicative. The headline now quotes a range across variants and no maximum.
5. Normalization is a method offset (astrophysics) and the "excluded at Nσ" wording (claims): the wording is withdrawn and the anchored verdict is [O].
6. fDM circularity: the trend claim stays [C] and the prior-trend test is reported.
7. "Hubble does best": replaced by a statement that the rankings disagree and flip.
8. C6 and C7 are relabelled unverified guards in the script output.
9. Routes as a cross-check: M_bar is presented as a consistency check only. The helper's S6/S8 FAILs are carried into this document.
10. Provenance "PASS": relabelled as source-hash only.
11. Ciocan ratio: both 2.05 (vs T3) and 1.98 (vs 1.2) are given, and the 95% CI convention is noted.
12. RC100 selection bias is stated explicitly.
13. Cosmology used for the predictions is stated, with its size.

**Rejected or not done, with reasons:**
- *Parametric bootstrap p-values*: not done. The helper's 200-realization path exceeds 590 s. The indicative labels and the calibration-nuisance variant cover the conclusion.
- *Vc-scale and pressure-α in the flip table, and z-dependent beam-smearing injection*: not done this cycle. Recorded as [O] above.
- *Leave-one-survey-out or equal-N 3-bin variant*: not done. The 2-bin and 4-bin variants agree.
- *Weighting to x ≲ 2*: not done. N_eff would fall below the Fisher estimate for z < 1.2 (22).
- *fDM zero-point prior inside χ²*: covered by the 0.5 ln calibration nuisance, which exceeds the A.4 ±0.11 prior.
- *Cell-by-cell comparison of Ubler vs .dat*: not done. The file is not a likelihood input. Relabelled only.
- *Hand-typed files*: no action needed; they stay out of the likelihood.
- *H(z) cosmology inconsistency*: rejected as negligible (see Method).

## Files

- `scripts/a0_highz_measurement.py`
- `scripts/fetch_highz_data.sh`
- `scripts/highz_extract_tables.py`
- `scripts/highz_ingest_rc41_g17_kmos3d.py`
- `scripts/highz_tf_samples_build.py`
- `02_galaxy_dynamics/highz_a0_method.py`
- `02_galaxy_dynamics/HIGHZ_A0_METHOD_SELFTEST_2026-09-16.json`
- `02_galaxy_dynamics/highz_data/*.csv`
- run logs `02_galaxy_dynamics/highz_data/*_run.txt`
