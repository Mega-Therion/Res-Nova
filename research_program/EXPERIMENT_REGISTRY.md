# Res-Nova Experiment Registry

**Purpose.** This registry is the operational record for new Res-Nova research. It exists to make analyses falsifiable before results are known. It does not change the status of any existing claim in `EPISTEMIC_BOUNDARY_v1.5.0.md`.

**Status vocabulary.** `planned` means a question is specified but no result exists. `preregistered` means data, model, and decision rules are frozen. `executing` means computation is underway. `under review` means an adversarial reproduction is required. `closed` means the ledger has been updated with an artifact and tag. `withdrawn` means the analysis was invalid or no longer addresses the stated question.

## Mandatory record for every experiment

| Field | Required content |
|---|---|
| Identifier | Stable ID of the form `RNP-YYYY-NNN`. Never reuse an ID. |
| Question | One falsifiable question, not a broad objective. |
| Competing hypotheses | At least one null/baseline model and one alternative. |
| Status and owners | Program state, analyst, independent reviewer, and date. |
| Inputs | Source URL/DOI, data release/version, checksum, and access date. |
| Analysis contract | Frozen code revision, environment lock/container, model equations, priors, selection/exclusion rules, and compute configuration. |
| Decision rule | Predeclared effect/fit/consistency metric, uncertainty method, and pass/fail/inconclusive conditions. |
| Negative controls | Analyses expected not to support the target hypothesis if the pipeline is calibrated. |
| Outputs | Immutable manifest, result JSON, figures, logs, and ledger link. |
| Claim posture | Proposed `[P]`, `[D]`, `[C]`, `[O]`, or withdrawn result; final posture is determined only after review. |

## Active program queue

### RNP-2026-001 — Clean-clone SPARC baseline reproduction

| Field | Specification |
|---|---|
| Status | **planned** — resolves existing engineering open problem O5. |
| Question | Can a clean checkout obtain the official SPARC mass-model data, verify a frozen manifest, and regenerate the current Res-Nova baseline outputs without author-specific file paths? |
| Competing hypotheses | H0: the published fetch/checksum path works on a clean machine. H1: undocumented paths, data drift, or preprocessing assumptions prevent exact reproduction. |
| Inputs | Official SPARC source; the repository’s `RAW_DATA_MANIFEST.sha256`; source/citation rules documented by SPARC. |
| Analysis contract | Fresh container or disposable virtual machine; network access recorded; no manually copied data; script accepts `--data-dir` and `SPARC_DATA_DIR`; all file hashes preserved. |
| Decision rule | **Pass:** all declared data files verify and baseline scripts run to the documented terminal artifact. **Fail:** unavailable/downloaded files, checksum mismatches, hidden paths, or undocumented manual repair. |
| Negative controls | Deliberately corrupt one file; set an invalid data directory; run with network disabled after fetch. Each must fail clearly and without silently using cached data. |
| Required artifacts | Download manifest, exact SHA-256 results, environment lock, stdout/stderr logs, baseline-result diff, and a short incident report for any divergence. |
| Promotion rule | This is an engineering result, not a new physics claim. O5 can be closed only when a clean runner has preserved the stated artifacts. |

### RNP-2026-002 — Cold-run Lean verification release gate

| Field | Specification |
|---|---|
| Status | **planned** — resolves existing formal reproducibility open problem O6. |
| Question | Does the declared Lean toolchain and manifest build every listed Res-Nova formal target on a cold runner with no inherited cache? |
| Competing hypotheses | H0: the formal suite is reproducible from pinned inputs. H1: a cache, toolchain, path, or undeclared dependency is required. |
| Inputs | `05_lean_formalization/lean-toolchain`, `lake-manifest.json`, formal target inventory, and a clean Git checkout. |
| Analysis contract | Ephemeral CI runner; clear Lake/Elan caches; exact toolchain resolution recorded; no `continue-on-error`; scripts must return nonzero on missing targets or active placeholders. |
| Decision rule | **Pass:** all inventory targets build and the proof receipt records commit/toolchain/Mathlib state. **Fail:** any missing toolchain, lock drift, proof build failure, or mismatch between inventory and run. |
| Negative controls | Add a test fixture containing active `sorry`; remove a declared target; invalidate a lock hash. The gate must fail in each case. |
| Required artifacts | CI log, proof receipt, target list, cache state declaration, artifact checksums, and badge/release link. |
| Promotion rule | A successful run supports only reproducibility of the stated theorem suite. It does not promote physics claims beyond their stated assumptions. |

### RNP-2026-003 — Galaxy-level hierarchical inference and predictive validation

| Field | Specification |
|---|---|
| Status | **planned** — follow-on empirical work package; does not supersede D4.3–D4.10 until ledgered. |
| Question | Under matched nuisance treatment, how do the dual-channel, standard MOND, and halo baselines compare in posterior predictive performance and sensitivity to galaxy-level systematics? |
| Competing hypotheses | H0: model ranking is not robust after hierarchical nuisance treatment and held-out diagnostics. H1: a predeclared comparison remains stable across the specified checks. |
| Inputs | A frozen, checksum-verified SPARC release; declared derived-data version; cited source documentation. |
| Analysis contract | Explicit galaxy-level generative model; priors for distance, inclination, and stellar mass-to-light parameters; matched nuisance freedom; galaxy-resampled uncertainty; exact comparator implementations; held-out galaxy or posterior predictive design chosen before execution. |
| Decision rule | Report the predeclared predictive score, calibration diagnostic, and uncertainty intervals. **Inconclusive** is an allowed result if rankings depend materially on reasonable priors or data treatment. No threshold may be selected after observing outcomes. |
| Negative controls | Synthetic data generated from each comparator; shuffled galaxy-level labels where appropriate; known parameter-recovery tests; recovery from a withheld subset. |
| Required artifacts | Pre-analysis plan, environment lock, sampler settings/seeds, posterior/summary objects, diagnostics, data manifest, figure source, and model-card table. |
| Promotion rule | Any result is `[D]` only if data, method, and output are frozen and an independent reviewer reproduces the principal tables. It cannot establish the horizon identity. |

### RNP-2026-004 — Covariant-branch constraint atlas

| Field | Specification |
|---|---|
| Status | **planned**. |
| Question | Within the explicitly stated Skordis–Złośnik-style embedding, which parameter/assumption regions are allowed, excluded, or unresolved after local, stability, wave, and lensing requirements are applied? |
| Competing hypotheses | H0: no nonempty region survives the declared constraints. H1: a nonempty conditional region remains after all stated checks. |
| Inputs | Formal source files; cited benchmark limits; derivation notebook(s); any numerical scan configuration. |
| Analysis contract | Every condition carries a source and tier (`[P]`, `[C]`, numerical evaluation, `[O]`); parameter prior/domain; sampling method; screening assumptions; and exact mapping to physical observables. |
| Decision rule | A region is **allowed** only if every applicable condition is evaluated under recorded assumptions. It is **excluded** if a defined constraint fails. It is **unresolved** if a condition is unavailable, not merely uncomputed. |
| Negative controls | Reproduce a known excluded RAQUAL/disformal branch; vary numerical resolution and parameterization; attempt to recover a known analytical limit. |
| Required artifacts | Constraint table, source map, symbolic derivations, scan code/data, numerical convergence report, and a one-page assumption audit. |
| Promotion rule | The result may establish conditional viability/exclusion, never a generic claim that modified gravity is viable. |

### RNP-2026-005 — Redshift evolution of the acceleration scale

| Field | Specification |
|---|---|
| Status | **concept stage**; resolves O1/O2 only if successfully executed. |
| Question | Does a named high-redshift dynamical tracer support an acceleration scale consistent with a constant value, a parameterized `a0(z)=\xi cH(z)` relation, or neither under a shared forward model? |
| Competing hypotheses | H0: `a0` is constant over the tested range. H1: `a0(z)=\xi cH(z)` with a constant \(\xi\). H2: a flexible evolution/selection model explains apparent differences. |
| Inputs | A single named public catalog/data release selected before model fitting, with documented selection function and calibration. |
| Analysis contract | Forward model for observable-to-dynamics conversion; cosmology assumptions; sample selection; treatment of beam smearing, inclination, pressure support, stellar populations, lensing/selection effects where applicable; blinding or held-out protocol if feasible. |
| Decision rule | The analysis must report model comparison and identifiability diagnostics. A non-discriminating result is the default acceptable outcome. Numerical agreement at one epoch is not confirmation. |
| Negative controls | Mock catalogs generated under constant and evolving cases; injected selection/calibration shifts; null tracers where the relation should not be inferred. |
| Required artifacts | Preregistration, public data manifest, mocks, inference code, calibration systematics table, result JSON, and independent replication plan. |
| Promotion rule | No public claim about a horizon tie is permitted unless this work reaches review with a discriminating, reproducible artifact. |

### RNP-2026-006 — Cosmological baseline replication before extension fitting

| Field | Specification |
|---|---|
| Status | **concept stage**. |
| Question | Can the selected public cosmology likelihood and baseline model be reproduced before a Res-Nova-specific extension is introduced? |
| Competing hypotheses | H0: the public baseline cannot be reproduced in the program environment. H1: it can be reproduced within preregistered numerical tolerances. |
| Inputs | A named official likelihood/data release; baseline code/version; documented nuisance/calibration configuration. |
| Analysis contract | Baseline replication occurs on a separate branch/repository area from speculative extension work. Tolerances are declared in advance. The code must not silently substitute data products or priors. |
| Decision rule | Extension fitting may start only after baseline parameters/likelihood values meet the declared tolerance. Failure is a result and blocks extension claims. |
| Negative controls | Intentionally mismatched release, altered nuisance prior, or wrong likelihood version must produce a detectable disagreement. |
| Required artifacts | Reproduction report, lockfile/container, likelihood provenance, chains/summaries where redistributable, and precise comparison table. |
| Promotion rule | This is a methodological gate. It does not add a Res-Nova cosmology result. |

## Review protocol

No experiment moves from `under review` to `closed` until a reviewer who did not make the primary result can execute the documented path or file a reproducible failure report. Where no external reviewer is available, a clean-room rerun by the same researcher on separate infrastructure is a minimum safeguard but is not labelled independent.

## Result-card template

Every closed experiment must publish this compact card next to its machine-readable result:

```markdown
### Result card — RNP-YYYY-NNN

**Question:**

**Status:** closed / withdrawn

**Claim posture:** [P] / [D] / [C] / [O] / superseded

**One-sentence result:**

**What this does not show:**

**Inputs and code:** data release, manifest hash, commit, environment lock

**Decision rule:**

**Negative controls:**

**Independent review:** reviewer, date, reproduction commit or failure report

**Ledger link:**
```

## Non-negotiable prohibitions

The registry may not be used to backfill a preregistration after a result is known, to convert a numerical coincidence into a derivation, to compare models with unequal flexibility without a parameter ledger, or to convert a failed/uncertain study into positive marketing. A withdrawn or inconclusive analysis remains part of the scientific record.
