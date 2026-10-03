# Scientific Data Register — Res Nova and Nova Conscientia

**Prepared:** 2026-10-03 UTC  
**Repositories audited:** [`Mega-Therion/Res-Nova`](https://github.com/Mega-Therion/Res-Nova), [`Mega-Therion/Nova-Conscientia`](https://github.com/Mega-Therion/Nova-Conscientia)  
**Purpose:** identify the scientific/empirical inputs required to reproduce, validate, or extend the claims currently made in the two repositories.

> **Intake check, 2026-10-03 (Claude Code), against Res-Nova `main`.** Every cited file exists and the dataset counts match. Corrections applied below:
> - the live a₀ is the μ_std value 1.1607×10⁻¹⁰, not the superseded 1.116×10⁻¹⁰;
> - the μ_std SPARC re-extraction was done on 2026-09-12; the remaining gap is the historical μ_dual number;
> - Cassini: μ_std alone fails the external-field quadrupole at +8.7σ, and duality screening restores a pass, with its covariant form open;
> - the D10 cluster data and scripts are in the repo since `2aac82f`;
> - two file paths are corrected.

## Executive finding

The repositories do **not** need one giant undifferentiated scientific database.

- **Res Nova** is a modified-gravity / cosmology / formal-verification research package. Its empirical backbone is the SPARC rotation-curve sample; its unresolved validation work is concentrated in solar-system constraints, cosmology likelihoods, high-redshift galaxy kinematics, and cluster/non-linear structure tests.
- **Nova Conscientia** currently needs **no external scientific dataset to reproduce its committed software tests**. Its committed benchmark is a deterministic synthetic simulation and explicitly is **not evidence about live frontier models**. The next evidence must be generated through preregistered experiments on heterogeneous model/agent stacks, not downloaded from an astronomy or biomedical database.

## Status vocabulary

| Status | Meaning |
|---|---|
| **Present / auditable** | Data or a frozen result is in the repository, with a manifest, receipt, or source hash. |
| **Fetchable / not vendored** | The repository provides a fetch path or names the official source, but raw data is intentionally external. |
| **Cited constraint** | A published measurement is used as a bound or comparison; reproducing the underlying analysis would require the source paper/data. |
| **Missing for independent validation** | The repository explicitly says the calculation is inherited, incomplete, or not independently reproduced. |
| **Withdrawn / do not use** | The input or result was retracted for traceability or methodological reasons. |
| **New experiment required** | No public database can substitute for the proposed measurement. |

## 1. Res Nova — data register

### A. Galactic rotation curves — primary empirical backbone

| Dataset / input | Needed fields | Repository evidence | Status / action |
|---|---|---|---|
| **SPARC 175-galaxy rotation-curve sample** | Per-galaxy radius, observed velocity and uncertainty, gas, stellar disk/bulge contributions, distance and inclination metadata; official `*_rotmod.dat` files | `02_galaxy_dynamics/fetch_sparc.sh`, `sparc_paths.py`, `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256`, `VERIFICATION_RUN_009/02_sparc_fetch/`, `scripts/fetch_verified_external_data.py` | **Fetchable / auditable.** Official CWRU `Rotmod_LTG.zip`; clean-clone walk reports 175/175 SHA-256 matches and zero drift. Download outside git and verify against the frozen manifest. |
| **SPARC-derived fit outputs** | `a0`, statistical/systematic uncertainty, per-galaxy residuals, nuisance parameters, parameter ledger, controls | `02_galaxy_dynamics/A0_REEXTRACTION_MU_STD.json`, `A0_REEXTRACTION_3MU_2026-09-16.json`, `A0_DISTANCE_CORRECTED_2026-09-16.json`, `PARAMETER_LEDGER.json`, `NFW_CONSTRAINED.json`; superseded: `A0_MEASUREMENT.json` | **Present / auditable.** The live value is the μ_std extraction: `a0 = 1.1607 × 10^-10 m s^-2`, 95% [0.972, 1.295] × 10^-10, over 175 galaxies / 3391 points (`CURRENT_STATE_READ_THIS_FIRST.md`). `A0_MEASUREMENT.json` (1.116 × 10^-10, 171 galaxies / 3375 points, μ_dual τ-closure) was marked superseded on 2026-09-17 and is kept for provenance only. |
| **Independent SPARC re-extraction under live `mu_std`** | Raw-data re-run using the current closure, identical priors, distance/inclination treatment, bootstrap/systematics protocol | `02_galaxy_dynamics/SPARC_MU_STD_RECOMPUTE_2026-09-12.md`, `sparc_a0_reextract_std.py` | **Present / auditable; one historical gap.** The μ_std re-extraction ran on 2026-09-12 (`A0_REEXTRACTION_MU_STD.json`: 1.156 × 10^-10; `03_observer_jwst/PREREG_A0_OF_Z_V3.md`). The same harness does not reproduce the historical μ_dual value in `A0_ESTIMATE.json` (1.107 × 10^-10; the harness gives 9.29 × 10^-11), because the original per-galaxy priors were never in the repo. A third-party rerun is still worth doing. |

**Priority:** highest. This is the minimum dataset needed for a clean third-party reproduction of the empirical core.

### B. Solar-system and weak-field constraints — current binding validation

| Dataset / input | Needed fields | Repository evidence | Status / action |
|---|---|---|---|
| **Cassini solar-system constraint** | The precise observable and covariance/limit used for the external-field quadrupole `Q2`; spacecraft/radio-tracking provenance; coordinate and sign conventions | `02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md`, `TARGET_D3_PPN_AND_SOLAR_SYSTEM.md` | **Cited constraint; independent data reduction missing.** The repo distinguishes the Q2 constraint from the weaker/ different PPN-`gamma` bound. Do not merge them. |
| **Saturn anomalous-perihelion constraint** | Bound and uncertainty on Saturn anomalous perihelion precession, units in mas/cy, ephemeris model and confidence convention | `TARGET_D3_PPN_AND_SOLAR_SYSTEM.md`; Hees et al. 2014, DOI `10.1103/PhysRevD.89.102002`; Fienga et al. 2011, DOI `10.1007/s10569-011-9377-8` | **Cited constraint.** This is the currently used route for the conditional `lambda_s ≲ 2.2` result; preserve the direct-Cassini and 1-sigma ephemeris readings as separate inputs. |
| **Planetary ephemeris residuals** | Mercury, Earth, Mars, Saturn residual perihelia / range / precession limits, full covariance if available | `TARGET_D3_PPN_AND_SOLAR_SYSTEM.md` tables | **Partially present as citation-level numbers.** A reproducible ephemeris fit would require source tables and model conventions, not just the summary limits. |
| **Cassini Q2 full radio-tracking dataset** | Raw/processed range and Doppler observations, maneuver model, ephemerides, nuisance parameters, covariance | `TARGET_D3_PPN_AND_SOLAR_SYSTEM.md` and `CASSINI_EFE_QUADRUPOLE_2026-09-27.md` | **Missing for a genuine independent Q2 analysis.** The repository’s current comparison is a constraint-level audit, not a re-fit of the mission data. |

**Priority:** highest for the live `mu_std` branch. μ_std alone fails the Cassini external-field quadrupole at the derived a₀ (+8.7σ, `CASSINI_EFE_QUADRUPOLE_2026-09-27.md`). The duality screening S(η) = 1/(1+η²) restores a pass: Cassini passes, SPARC is neutral, dwarfs survive (`PEER_REVIEW_READINESS.md`). What is open is its covariant realisation, which GW170817 requires to be metric-level `[O]`.

### C. Cosmology and expansion-history datasets

| Dataset / input | Needed fields | Repository evidence | Status / action |
|---|---|---|---|
| **Planck 2018 CMB TT/TE/EE spectra** | Binned spectra, covariance, masks/metadata, and the actual likelihood components (`plik_lite` TTTEEE, low-l, low-E as applicable) | `TARGET_D11_CMB_FIT.md` | **Partially fetchable; full likelihood missing.** The repository’s binned TT/TE/EE comparison is a validation of a scoring method, not the Planck likelihood. A real claim requires the official likelihood and covariance. |
| **Planck 2018 cosmological-parameter release** | Published best-fit parameters and covariance, release/version identifiers | `references.bib` (`Planck 2018 Results VI`, DOI `10.1051/0004-6361/201833910`) | **Cited / available.** Use only as a published comparison unless the likelihood is also used. |
| **Pantheon+ Type Ia supernova sample** | Official quality-cut sample, redshifts, corrected distance moduli, covariance, nuisance/calibration metadata | `04_cosmology/omega_ln2_pantheonplus.py`, `PREREG_OMEGA_LN2_PANTHEONPLUS.md` | **Fetchable / not vendored.** The repository names the official `PantheonPlusSH0ES/DataRelease`; reported analysis uses 1590 SNe after quality cuts. Hash the exact release and retain the covariance. |
| **DESI DR2 BAO** | Gaussian BAO measurements, covariance, tracer/redshift-bin labels, release/version | `04_cosmology/ceiling_model_bao_sn.py`, `O3_HORIZON_LANDING_ROUTE_2026-09-28.md` | **Fetchable / not vendored.** The repo references `bao_data/desi_bao_dr2 ALL_GCcomb` and arXiv `2503.14738`; freeze the exact data release and covariance before fitting. |
| **CMB + BAO combined likelihood** | Consistent joint covariance and nuisance treatment across Planck/DESI | `04_cosmology/O3_HORIZON_LANDING_ROUTE_2026-09-28.md` | **Missing for the central horizon-normalization question.** The next defensible step is a joint, preregistered fit—not another point comparison. |
| **Hubble-constant anchors** | Planck inference and SH0ES distance-ladder value with uncertainty and calibration definition | `references.bib`; `REPRESENTATION_AUDIT_A0_SPARC_2026-09-16.md` | **Present at citation level.** Keep Planck and SH0ES as distinct measurements; do not select one to rescue the `a0` coincidence. |

### D. High-redshift galaxy kinematics / JWST extension

| Dataset / input | Needed fields | Repository evidence | Status / action |
|---|---|---|---|
| **RC100 / high-z rotation-curve compilation** | Per-galaxy redshift, radius, velocity, uncertainty, baryonic decomposition, beam/pressure corrections, sample selection | `02_galaxy_dynamics/highz_data/`, `A0_HIGHZ_MEASUREMENT_2026-09-16.md` | **Partially present.** CSVs and a measurement note exist; source PDFs are gitignored and the fetch log says source-hash verification did not re-compare cell values. Rebuild a release bundle with source PDFs or stable URLs plus cell-level hashes. |
| **MUSE-DARK III** | Public per-galaxy measurements and uncertainties, selection function, calibration, redshift, model assumptions | `03_observer_jwst/O4_REAL_DATA_MUSE_DARK_III_2026-09-27.md` | **Missing / incomplete public-data traceability.** The repo explicitly notes that a per-galaxy data release is not stated. Use published aggregate values only as contextual evidence, not as a full re-analysis. |
| **JWST/NIRSpec high-z sample** | Frozen pre-registered catalogue at `z > 1.5`, kinematics, baryonic mass model, calibration and selection metadata | `OPEN_PROBLEMS_AND_TESTS.md`, `03_observer_jwst/PREREG_A0_OF_Z_V3.md` | **Missing; new data assembly required.** The withdrawn 20-point table must not be reused. A new catalogue and JSON-producing analysis are required before making JWST claims. |

### E. Clusters and non-linear structure formation

| Dataset / input | Needed fields | Repository evidence | Status / action |
|---|---|---|---|
| **Galaxy-cluster lensing / dynamics sample** | Cluster mass profiles, lensing shear, baryonic gas/stars, member velocities, redshift, covariance | `TARGET_D10_CLUSTERS.md`, `02_galaxy_dynamics/clusters/` | **Present / auditable.** The two VizieR tables (`J/ApJ/911/82`, Corasaniti, Sereno & Ettori 2021) and the scripts are in the repo since `2aac82f`. Rerunning reproduces the median lensing-to-baryonic ratios 1.96 (pure MOND), 1.54 (AeST MOND branch) and 1.13 (first order in μ², expansion parameter 0.81). The nonperturbative solve fails for a reason inside the model (§9) `[O]`. |
| **Non-linear structure-formation simulations** | Initial conditions, cosmological parameters, modified-gravity solver, N-body snapshots, power spectra, halo statistics | `TARGET_D5_COSMOLOGICAL_SECTOR.md`, `SUBMISSION/COVER_LETTER_PRD.md` | **Missing; new computation required.** The repo explicitly says the non-linear N-body calculation has not been run. Published equations are not a substitute for simulation outputs. |
| **DESI / large-scale-structure validation** | BAO and, if claimed, growth/RSD observables with covariance | `04_cosmology/` notes | **Partially specified.** Needed only if the cosmological sector is expanded beyond the current limited checks. |

### F. Physical constants and theory references

These are not “datasets” in the same sense, but they must be version-pinned for reproducibility:

- `c`, `G`, `H0`, `h`, `k_B`, and unit conversions: use a named constants release (prefer NIST/CODATA) and record the release/version.
- Published MOND/SPARC/AeST/Skordis–Złośnik equations: record DOI/arXiv identifiers and the exact equation/normalization used.
- GW speed constraints: use the published GW170817/GRB170817A constraint only as a cited bound unless a waveform dataset is actually reanalysed.
- Avoid treating a Lean theorem as physical validation: Lean proves the encoded mathematics under its hypotheses, not the empirical adequacy of the model.

## 2. Nova Conscientia — data register

### A. What is already reproducible without external scientific data

| Component | Current evidence | Status |
|---|---|---|
| Dual-channel algebra translation | Imported identities and provenance from Res Nova `Hamilgrangian.lean` | **Present as source/proof provenance; not new empirical data.** |
| QUMOND-inspired attention law | `core/topology_graph.py` plus Res Nova `QUMOND_PM_GATES.json` | **Present as inherited deterministic receipts.** It is an engineering analogy/translation, not evidence that agents gravitate. |
| Drift benchmark | `benchmarks/results/benchmark_receipt.json`; seeded synthetic stimulus, 40 trials × 50 cycles, 16 dimensions, swarm of 4 | **Present / reproducible mechanism check.** It is not a live-model experiment. |
| Ablation benchmark | `benchmarks/results/ablation_receipt.json` | **Present / reproducible mechanism check.** Interpret acceptance/collapse metrics only within the seeded simulation. |
| Unit/property tests and AST gate | `tests/`, `verification/ast_invariant_validation.py` | **Present / reproducible software evidence.** |

### B. Scientific/empirical data actually needed to validate Nova Conscientia’s open claims

| Experiment | Required data | Status |
|---|---|---|
| **E1 — external drift-collapse calibration** | Raw per-cycle embeddings/states, task anchor, model/provider/version, prompt/task, seed, temperature/sampling settings, intervention policy, threshold sweep, collapse definition, and complete receipts across heterogeneous agent stacks | **New experiment required.** This is the decisive test of whether `tau = 0.9539` generalizes beyond the tuning pipeline. |
| **E2 — purchasability-seam audit** | Proposal features, exploration momentum, soft-constraint violations, invariant outcomes, correction cost, acceptance/rejection, model and task metadata | **New experiment required.** No public database can provide this operational trace. |
| **E3 — consensus scaling** | Planted-flaw corpus, ground-truth labels, auditor/model identities, heterogeneity conditions, quorum settings, veto recall/precision, abstentions/errors, latency, cost, and cryptographic receipts | **New experiment required.** This needs a preregistered evaluation suite and human/audited labels. |
| **Minimal datasets for claims about drift, hallucination, or reward-hacking** | A task suite with independently verifiable answers, adversarially planted contradictions, long-horizon multi-agent traces, and held-out tasks | **Missing.** The current synthetic drift model cannot establish these claims. |

### Important boundary

The `0%` swarm collapse result is not an external scientific finding: the swarm arm is clipped at the same threshold used to define collapse. Any future report should retain the repository’s own caveat and avoid describing this as evidence that the system improves live frontier-model oversight.

## 3. Recommended acquisition order

### Phase 1 — reproduce the strongest existing empirical result

1. Fetch the official SPARC archive outside git.
2. Verify all 175 files against `RAW_DATA_MANIFEST.sha256`.
3. Re-run the live `mu_std` extraction with all priors and nuisance conventions recorded (done once in-repo on 2026-09-12, `A0_REEXTRACTION_MU_STD.json`; a third-party rerun is the open step).
4. Reconcile the result against `A0_MEASUREMENT.json`, explicitly separating the 171-galaxy measurement from the 175-galaxy raw sample.
5. Produce a new JSON receipt with source URL, release date, commit, hashes, units, filters, and count reconciliation.

### Phase 2 — close the current physical bottleneck

1. Assemble the Cassini Q2 and Saturn-precession constraints as separate datasets.
2. Reproduce the conditional `lambda_s` bound with a stated confidence convention.
3. Do not call this a full Cassini re-analysis unless raw radio-tracking data and covariance are obtained.

### Phase 3 — make the cosmology claims independently testable

1. Freeze Pantheon+ release and covariance.
2. Freeze DESI DR2 BAO release and covariance.
3. Obtain the Planck likelihood, not only binned spectra.
4. Run a joint preregistered CMB+BAO+SN comparison with all parameters refit; do not hold all Planck parameters fixed and call the result a likelihood fit.

### Phase 4 — validate the high-z and cluster claims

1. Replace the withdrawn JWST table with a traceable catalogue.
2. Rebuild the RC100/MUSE-DARK III input bundle with source-level and cell-level provenance.
3. Freeze the VizieR cluster table and perform a full cluster comparison.
4. Run the missing non-linear N-body calculation before claiming structure-formation support.

### Phase 5 — validate Nova Conscientia as computer science

1. Define E1–E3 preregistration documents and data schemas.
2. Collect live multi-model traces with held-out tasks and independent labels.
3. Report threshold selection separately from evaluation data to prevent calibration leakage.
4. Compare against unconstrained, gate-only, dual-channel, and independent oversight baselines.
5. Hash every raw trace bundle and publish machine-readable receipts.

## 4. Data that should **not** be used as current evidence

- Retired `mu_dual(x) = x/(1+x)` solar-system claims.
- The withdrawn 20-point high-redshift table and its 5.9-sigma / 2.06-sigma results.
- The historical “zero free parameters” SPARC language (RETRACTED: the framework has two irreducible parameters, the a₀ scale and the functional choice).

- `A0_MEASUREMENT.json`'s 1.116 × 10^-10 as the live a₀. It was superseded on 2026-09-17; use the μ_std value.
- The deterministic Nova Conscientia benchmark as evidence about live LLMs.
- The `Omega_Lambda = ln(2)` coincidence as a derived physical result.
- A binned Planck score as though it were the full Planck likelihood.
- A citation-level Cassini number as though it were an independent radio-tracking reanalysis.

## 5. Reprovenance template for every acquired dataset

For each future data bundle, record:

```text
Target:
Primary source / database:
Canonical identifier or release:
Access date:
Download URL / endpoint:
Time/version constraint:
Coordinate frame and units:
Server-side filters:
Local filters:
Expected record count:
Retrieved record count:
Excluded records and reasons:
Source-file SHA-256:
Transformation code and commit:
Analysis code and commit:
Known limitations:
```

## Bottom line

The **minimum scientifically meaningful acquisition** is not “all scientific data.” It is:

1. a fully reproducible SPARC re-extraction under the live `mu_std` branch;
2. separately auditable Cassini-Q2 and Saturn-ephemeris constraints;
3. the actual Planck likelihood plus frozen Pantheon+ and DESI DR2 inputs for any cosmology claim;
4. a traceable high-redshift catalogue and a real cluster/non-linear test if those claims remain in scope; and
5. newly generated, preregistered live-agent traces for Nova Conscientia E1–E3.

Everything else is either background literature, formal proof input, engineering provenance, or an explicitly quarantined/open hypothesis.
