# Supplemental Independent Code Review: a₀(z) Pipeline

**Reviewer:** Safa (ChatGPT)  
**Review date:** 2026-11-13  
**Reviewed repository state:** `Mega-Therion/Res-Nova`, `main` at `95f4578bd57b1df593aec416155fcbb29a20ca9a`  
**Scope:** V1/V2 code, V1/V2/V3 preregistration records, current reports, and the existing 2026-11-09 code review.  
**Review type:** Static source review plus independent numerical checks of formulae and unit conversions. No repository script was executed and no raw observational data were re-analysed in this review.

## Executive verdict

The core forward-model algebra and the stated flat-ΛCDM expansion formula are internally consistent with the corresponding V1/V2 protocol definitions. The inspected primary hypothesis-evaluation functions contain no optimizer or test-stage parameter fitting: they evaluate the registered hypotheses using frozen inputs. The sign convention and ±9 Δχ² thresholds also match the V1 preregistration.

However, **the checked-in V1 and V2 scripts still load and execute a 20-row data table that the repository formally withdrew on 2026-09-27 for failed source provenance**. V2 can write a report marked `status: completed` and `[D] Computed Empirical Benchmark` while attaching the withdrawn dataset description. The V3 preregistration reports a newer inconclusive result but no V3 executable or machine-readable V3 report is present in the inspected `03_observer_jwst/` directory. The current pipeline therefore does not provide an auditable, fail-closed reproduction path for the live V3 result.

**Disposition:** retain V1/V2 scripts and reports as historical records, but do not run or cite them as current empirical evidence. The live a₀(z) conclusion remains **[O] open/inconclusive**, as the V3 protocol itself states. A V3 implementation and a provenance-controlled input dataset are required before any new quantitative claim.

## 1. Source inventory and provenance

The review is pinned to main commit `95f4578bd57b1df593aec416155fcbb29a20ca9a`.

Relevant source artifacts:

- `03_observer_jwst/a0_of_z.py` — V1 script; blob `9d593c102cdc73949301fe0b2327b315b81c222a`.
- `03_observer_jwst/a0_of_z_v2.py` — V2 script; blob `5d6cb2168f7e07e12ce6ff242550ed798eed7a36`.
- `03_observer_jwst/PREREG_A0_OF_Z.md` — V1 protocol; blob `b15cab59dbfd267d11b10aff8b195844334a1c04`.
- `03_observer_jwst/PREREG_A0_OF_Z_V2.md` — V2 protocol; blob `5ffee65dd423b378cc91d1e8e259b84e99d2c244`.
- `03_observer_jwst/PREREG_A0_OF_Z_V3.md` — V3 protocol; blob `5e579eb0bd0bc05d75c788c9f00598db3241aaff`.
- `03_observer_jwst/A0_OF_Z_REPORT.json` and `A0_OF_Z_REPORT_V2.json` — legacy output reports.
- `03_observer_jwst/CODE_REVIEW_A0_OF_Z.md` — existing review by Antigravity CLI, dated 2026-11-09.
- `03_observer_jwst/O4_REAL_DATA_MUSE_DARK_III_2026-09-27.md` — withdrawal and subsequent real-data assessment.

The V1 and V2 scripts themselves state in their headers that the 20-point table is withdrawn. The O4 audit explains why: the cited Bouché+2021 paper is a nine-galaxy pilot and does not contain the asserted 20-point kinematic table; the cited “Mercier+2022, A&A 667, A75” reference was not found, and the actual Mercier 2022 paper cited in the audit is a different article. The O4 audit explicitly says the table is withdrawn from all use and that both the V1 and V2 results computed from it are void.

## 2. Findings

### Critical — withdrawn rows remain executable by default

**V1:** `a0_of_z.py` calls `load_muse_dark_published_sample()` whenever `--data` is omitted. That loader returns the withdrawn hard-coded `udf10_01`…`udf10_20` table. The report path then labels the result `[D] Computed Empirical Benchmark` and repeats the false source attribution.

**V2:** `a0_of_z_v2.py` unconditionally loads the same hard-coded table in `main()`. It has no data-file argument or provenance gate. It then writes `status: completed`, `epistemic_classification: [D] Computed Empirical Benchmark`, and a dataset field naming the withdrawn sources.

The header warning is not an execution guard. A user can run the script normally and receive a fresh-looking report generated from withdrawn values. This is the highest-priority defect in the current pipeline.

**Required correction:** do not rewrite immutable historical records in place. Make a new maintained runner that requires an explicit data file plus a provenance manifest (source, version, SHA-256, sample definition, and independent-galaxy count); reject the withdrawn table and any unapproved dataset; and fail closed if provenance metadata is absent. Historical scripts should be clearly marked archival and should not be presented as current runnable analyses.

### Critical — V3 preregistration has no matching reproducible execution artifact

V3 (`PREREG_A0_OF_Z_V3.md`) states that the SPARC 175-galaxy benchmark (3,391 points) was re-extracted with `μ_std = x/√(1+x²)`, a documented nuisance-prior grid, profile likelihood over a₀, and 500 galaxy bootstraps. It records central (a₀=1.1562×10^{-10}), (χ²_{const}=11.366), (χ²_{horizon}=10.615), (Δχ²=+0.75), and an inconclusive 0.87σ result.

The inspected `03_observer_jwst/` directory contains V1/V2 scripts and V1/V2 JSON outputs, but no `a0_of_z_v3.py` or `A0_OF_Z_REPORT_V3.json`. The V3 document itself acknowledges an exact-pipeline reproduction gap: the in-repository extraction harness does not reproduce the historical μ_dual value in `A0_ESTIMATE.json`, because the original per-galaxy distance/inclination priors are outside the repository.

This does not prove the V3 calculation was not performed. It means this review cannot independently reproduce the reported V3 table from a checked-in executable and input/output bundle.

**Required correction:** commit the exact V3 execution code, frozen inputs, manifest/hashes, bootstrap seed/procedure, environment/tool versions, generated JSON report, and one command that regenerates the report byte-for-byte or within a declared numeric tolerance. Keep the stated limitation about the historical μ_dual harness mismatch visible.

### High — V1 sample-size gate disagrees with preregistration and has an error path

The V1 preregistration says the inconclusive/insufficient condition includes fewer than 10 independent galaxy kinematic bins. The V1 code checks only `len(points) < 5`. It does not test the number of independent galaxies or enforce the preregistered (N<10) boundary.

There is also a control-flow bug: when fewer than five points are supplied, the script constructs an `insufficient` report without a `dataset` object and without defining `results`; after writing that JSON it unconditionally prints `report['dataset']` and references `results`. The command therefore raises an exception after producing the report.

**Required correction:** in a new maintained runner, validate both the number of rows and the number of independent galaxy bins against the preregistered minimum before evaluating; return/exit cleanly on insufficient data; test exactly 0, 1, 4, 5, 9, and 10 independent bins. V2 has no corresponding minimum-sample/provenance check.

### Moderate — log-error propagation is an approximation, not exact

The scripts use `sigma_g = g_obs * ln(10) * sigma_log10`. This is the first-order differential propagation for converting a dex uncertainty to a linear uncertainty. The existing Antigravity review calls it “mathematically exact”; that description is incorrect. If the log-space uncertainty is Gaussian and the intended quantity is the standard deviation of the corresponding lognormal variable, the exact conversion is not the same expression.

For the legacy table's 0.07–0.11 dex values, the first-order approximation is roughly 2–5% below the lognormal standard deviation under that interpretation. This is a methodological detail to settle in the maintained runner and preregister before using data; it does not rescue or invalidate the withdrawn-table results, which are already void on provenance grounds.

### Moderate — existing review omits V3 and overstates the execution gate

The 2026-11-09 `CODE_REVIEW_A0_OF_Z.md` usefully identifies the μ_dual→μ_std change, the withdrawn data, and the 3σ decision rule. But it:
- says the code “correctly” gates live empirical claims even though V1/V2 still execute the withdrawn table by default;
- treats the V2 output as a computed empirical benchmark without clearly stating that the same input table was subsequently withdrawn and the V2 result voided;
- calls the dex-to-linear error propagation mathematically exact; and
- stops at V2, omitting the V3 preregistration's 0.87σ result and missing executable/report gap.

This supplement should be read alongside that existing review; it does not replace or delete it.

## 3. Independently checked mathematics and frozen inputs

The following parts are consistent with the source and protocol definitions:

1. **Flat-ΛCDM background:** `H(z) = H0 * sqrt(Ωm * (1 + z)^3 + ΩΛ)`, with `H0 = 67.4 km s⁻¹ Mpc⁻¹`, `Ωm = 0.315`, and `ΩΛ = 0.685`, is implemented consistently. The numeric `H(z)/H0` values at z = 0.5, 1.0, 1.5, and 2.0 are approximately 1.3222, 1.7903, 2.3679, and 3.0315.

2. **Frozen V1/V2 ξ:** using `c = 2.99792458×10^8 m/s` and the stated H₀ conversion gives `H0 = 2.18428524×10^-18 s^-1` and `ξ = 1.11603513×10^-10 / (c * H0) = 0.17043069`, matching the V1/V2 value to the displayed precision. This is the old μ_dual-extracted a₀ baseline; it is not the V3 baseline.

3. **V2 μ_std inversion:** solving `g * μ_std(g/a0) = gbar`, with `μ_std(x) = x / sqrt(1 + x^2)`, yields `g = sqrt(0.5 * (gbar^2 + sqrt(gbar^4 + 4*gbar^2*a0^2)))`, matching the code. Substitution checks at representative positive `gbar` and `a0` values recover `gbar` to floating-point precision.

4. **χ² and decision sign:** `χ² = Σ[(gobs - gpred)/σg]^2`, `Δχ² = χ²_const - χ²_horizon`, and the mapping `Δχ² ≥ +9` → horizon favoured, `Δχ² ≤ -9` → constant favoured, otherwise inconclusive, agree with the V1 preregistration.

5. **No test-stage parameter refit found:** the reviewed `evaluate_hypotheses()` / `evaluate()` functions use frozen `a0`, `ξ`, and cosmological inputs in forward predictions. I found no optimizer or fit step in those primary hypothesis-evaluation paths. V2's optional `--scan` varies `a0` and co-scales `ξ` as an explicitly exploratory sensitivity analysis; it is not a fit to the test data. The sensitivity scan should remain labelled exploratory and separate from the registered result.

For V3's central `a0 = 1.1562×10^-10 m/s²`, the corresponding definition `ξ = a0 / (c * H0)` gives approximately `0.17656`. The V3 protocol says ξ is co-scaled by definition, but the missing executable/report means the exact V3 code path and recorded frozen value could not be checked directly.

## 4. Required next steps, in order

1. **Quarantine the old execution path without erasing history.** Keep V1/V2 preregistrations and output reports as immutable historical evidence, but make the new maintained command refuse the withdrawn 20-row data and label old JSON outputs `[X] withdrawn` in any current-facing index.
2. **Reproduce V3 exactly.** Add the missing executable and report artifacts; include input data, hashes, bootstrap configuration/seed, environment, and a deterministic reproduction command.
3. **Define a real-data input contract.** Require independently traceable galaxy rows, source-level provenance, units, covariance/error semantics, galaxy identifiers, sample selection, and a declared minimum of 10 independent galaxy bins. Do not treat a published aggregate summary point as a substitute for per-galaxy raw inputs.
4. **Add fail-closed tests.** No default data; withdrawn source hash rejected; missing provenance rejected; duplicate/insufficient galaxy bins rejected; correct V1/V2 formula unit tests; stable report schema; explicit `insufficient` exit path with no traceback.
5. **Revisit uncertainty treatment before the next preregistration.** State whether dex uncertainties are Gaussian measurement standard deviations, confidence intervals, or another quantity; use and document the corresponding likelihood/error transform consistently.

## 5. Final status

- V1 math review: **PASS with caveats**; historical result void because both μ_dual and its input table were withdrawn.
- V2 math review: **PASS with caveats**; historical 2.06σ result void because its input table was withdrawn.
- V3 empirical result: **reported inconclusive [D] in the preregistration, not independently reproduced in this review**; exact pipeline validation remains [O].
- No evidence supports a current 3σ claim for either a constant a₀ or a horizon-tied a₀(z) from this pipeline.
- No analysis code, preregistration, raw data, or historical report was modified by this review.

