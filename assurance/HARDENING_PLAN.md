# Res-Nova Assurance and Research Hardening Plan

## Goal

Take Res-Nova as far as the repository’s evidence can support while preventing overclaiming. The objective is not to make every statement sound stronger; it is to make every important statement traceable from natural-language claim to source data, computation or formal proposition, verification environment, independent witness, and publication surface. The work will preserve valid results, retract or qualify unsupported wording, and connect the existing Res-Nova, MVPC-X, 4Leibniz, and RYTT assurance concepts into one governed system.

## Current baseline and constraints

The current Res-Nova Lean environment has been provisioned successfully with Lean `v4.33.0-rc1` and the repository-pinned Mathlib revision. The declared gate currently contains **29 targets**, not 30, and a fresh run has passed 29/29 with exit status 0. The repository already has useful safeguards: `scripts/check_claim_consistency.py`, the manuscript inventory checker, SPARC artifacts and parameter ledgers, MVPC manifests, and a CI workflow. However, the CI file intentionally excludes Lean kernel verification because cold-cache reproducibility remains an open problem. Several documents still contain stale 17/18-target wording, and the empirical materials distinguish strict Tier 0 from nuisance-parameter Tier 1 results; that distinction must become impossible to erase accidentally.

The plan assumes the user wants repository changes, reproducible research artifacts, and publication-ready documentation, but does not authorize changing scientific claims merely to obtain a cleaner narrative. Scientific conclusions will be treated as hypotheses or results according to evidence, not intention.

## Capability map and dependency order

| Module | Responsibility | Depends on |
|---|---|---|
| `assurance-contract` | Define evidence levels, claim states, and required witnesses | — |
| `claim-registry` | Make every headline numerical and scientific claim machine-addressable | `assurance-contract` |
| `formal-gate` | Harden Lean target inventory, assumptions, axiom reporting, and reproducible environments | `assurance-contract` |
| `empirical-repro` | Make SPARC and future analyses source-complete, deterministic, independently recheckable, and tier-explicit | `assurance-contract`, `claim-registry` |
| `manuscript-drift` | Keep README, LaTeX, PDFs, ledgers, manifests, and code synchronized | `claim-registry`, `formal-gate`, `empirical-repro` |
| `independent-review` | Add adversarial checks, alternative calculations, and evaluator rubrics | all preceding modules |
| `release-bundle` | Produce a versioned publication/reproduction package with a final assurance report | all preceding modules |

Build order: `assurance-contract` → (`claim-registry`, `formal-gate`, `empirical-repro`) → `manuscript-drift` → `independent-review` → `release-bundle`.

## Phase 1: Freeze scope and define the assurance contract

Create a reviewed specification before modifying code. Adopt the MVPC-X identity chain as the central contract: **natural claim → formal proposition or computational definition → declaration or code artifact → verification environment → evidence → witness**. Define assurance levels from proposed through publication-grade, with explicit conditions for promotion and explicit forbidden shortcuts. A passing Lean elaboration must not promote an empirically unsupported physical claim; a low residual must not promote a causal or universal claim; and a PDF must never outrank the executable artifact that produced it.

Define a canonical claim record containing: stable claim ID; exact wording; epistemic state (`proposed`, `derived`, `axiomatic`, `computed`, `formally verified`, `empirically supported`, `retracted`, or `conditional`); source data and hashes; code or theorem paths; assumptions; parameter tier; verification commands; environment lock; independent witness; and last verified commit. Require every headline claim to have one owner record and prohibit duplicate free-text definitions from becoming authoritative.

**Gate:** The specification is reviewed and approved before implementation. The claim states and promotion rules are unambiguous, and every existing publication headline can be assigned a claim ID or marked as legacy text.

## Phase 2: Harden the formal gate

Make `lakefile.lean` the single source of truth for formal targets. Generate or validate the shell target list from the Lake roots rather than maintaining two manually synchronized lists. Add an explicit report showing target count, file hashes, Lean version, Mathlib commit, cache provenance, elapsed time, warnings, `sorry` findings, and axiom dependencies.

Add a separate **assumption audit**. The current gate correctly warns that typeclass fields, structure fields, and theorem hypotheses can carry assumptions that a global `axiom` grep cannot reveal. Catalogue those assumptions by theorem and distinguish foundational Lean axioms from physical or model assumptions. Link every physical assumption to a claim-registry record and its empirical or literature support.

Add a formal semantic audit for suspiciously vacuous theorems. At minimum, detect propositions whose conclusion is syntactically identical to a definition, hard-coded output, or tautological rewriting; require negative controls where changing a supposedly meaningful constant causes the theorem to fail when the theorem is intended to establish that constant. Keep the existing GenerationIndex warning as a model for this work.

Solve cold-cache reproducibility in stages: first document a pinned container or Nix/OCI environment; then verify a clean machine with no pre-existing Mathlib; then publish the environment digest and cache manifest; only after those pass, consider a scheduled or release CI gate. Keep PR CI lightweight until the cold-cache process is proven. Do not hide multi-gigabyte dependency costs inside ordinary pull requests.

**Gate:** A clean environment can reproduce the formal result; the target count is one number everywhere; assumption and vacuity reports are attached to the release; and any warning is visible rather than silently discarded.

## Phase 3: Harden the SPARC empirical pipeline

Separate and label the existing analysis tiers in code, data, manuscript, and figures. Tier 0 must mean no per-galaxy freedom and must report its own fit quality. Tier 1 must list all nuisance parameters and compare only against a genuinely matched NFW row. Replace ambiguous “zero-parameter” language with the exact tier definition and parameter ledger reference.

Eliminate external absolute paths such as `/home/mega/...` from manifests and scripts. Add a source acquisition manifest with URL or archive provenance, license, retrieval date, file hashes, expected galaxy count, expected point count, and a fully offline mode using committed or release-attached inputs. Make every reproduction command work from a fresh clone plus a documented data artifact.

Implement independent rechecks for the headline `a₀` result. One path should use the existing production pipeline; a second path should independently parse the frozen fit data and recompute the estimator, uncertainty components, sample exclusions, and parameter totals. Compare both outputs with explicit tolerances. Add perturbation tests for distance scale, inclination, mass-to-light priors, sample selection, missing values, duplicate galaxies, and unit conversion. Use `validate-data` principles to check denominators, population definitions, aggregation grain, selection effects, and whether uncertainty components are being combined consistently.

Do not force `statsmodels` into the project unless a clearly defined inferential question and analysis-ready observations exist. If used, specify the outcome, covariates, model family, uncertainty treatment, diagnostics, multiple-testing policy, and out-of-sample or robustness checks before fitting. A model fit should be an additional analysis, not a retroactive justification for the existing theory.

**Gate:** Two independent implementations agree within declared tolerances; all inputs are reproducible and hashed; strict and nuisance tiers cannot be conflated; and the release report includes limitations and failed sensitivity checks.

## Phase 4: Connect formal, empirical, and publication claims

Create a claim graph that connects each headline statement to its formal theorem, empirical artifact, assumptions, and manuscript locations. The graph should expose missing edges rather than merely visualize existing ones. Examples of valuable connections include: the Lean `a₀` derivation versus the measured SPARC `a₀`; the Pillar IV coherence ceiling versus its physical assumptions; the TensorSpeed formal result versus the observational constraint it is intended to address; and the 4Leibniz/RYYT concepts versus any actual Res-Nova theorem or computation.

For each connection, classify the relationship as identity, derivation, consistency check, analogy, dependency, or conjectured bridge. Do not let a shared symbol, phrase, or diagram imply a mathematical implication. Any cross-repository contribution must cite a precise interface: theorem, schema, file, API, or data contract.

Generate Mermaid diagrams for: the claim-evidence graph, formal verification flow, SPARC provenance flow, and publication artifact dependency graph. Store the source diagrams beside the documentation and render them in CI so diagrams cannot drift from the documented nodes and edges.

**Gate:** Every headline claim has a visible evidence path, every cross-repository connection has a typed relationship, and unsupported connections are labeled as conjectures or research questions.

## Phase 5: Manuscript and publication hardening

Make the manuscript inventory checker and claim-consistency checker authoritative release gates. Update all stale counts, including 17/18-target text, to derive from the live inventory. Add a check that scans Markdown, TeX, HTML, JSON metadata, and generated publication summaries for forbidden or ambiguous phrases such as “zero free parameters,” “proved,” “universal,” “confirmed,” or “publication ready” unless accompanied by the required qualification and claim ID.

Build publication artifacts from a declared source commit and record the exact source hashes, toolchain, data version, build command, page count, and embedded artifact manifest. Make PDFs reproducible or clearly label them as generated snapshots. Maintain separate papers if that serves peer-review scope, but use a named monograph only after its chapter claims all resolve to the same assurance registry.

Run a no-AI-slop and human editorial pass only after claim correctness is fixed. The editorial pass should remove inflated language and preserve uncertainty rather than polish speculation into authority. Add a referee-facing “what is proven, derived, measured, assumed, conditional, retracted, and open” table to every release.

**Gate:** A clean release build produces a consistent manuscript/PDF/manifest bundle; no stale target counts or prohibited claim wording remain; and a referee can trace each headline sentence to evidence without relying on agent interpretation.

## Phase 6: Adversarial evaluation and independent review

Create an evaluator-optimizer loop with a fixed rubric covering formal correctness, assumption transparency, data provenance, numerical reproducibility, comparison fairness, statistical validity, manuscript consistency, and claim calibration. Use structured JSON results and bounded iterations. Add adversarial cases that attempt to: promote a historical PASS to a current PASS; count `lakefile.lean` as a theorem target; turn a Tier 1 nuisance fit into a zero-parameter claim; treat a skipped Groth16 test as verified; infer causality from a fit; or connect RYTT/4Leibniz concepts without a formal interface.

Have an independent reviewer or second implementation challenge the highest-impact claims. Prefer reviewers or scripts that do not share the production pipeline’s helper functions. Preserve dissent and failed attempts in the release evidence instead of deleting them.

**Gate:** The evaluator catches seeded false claims, independent recomputation agrees or identifies discrepancies, and all unresolved disagreements are visible in the assurance report.

## Custom skills: create only where reusable

Do not create a custom skill merely to encode Res-Nova’s one-off file paths. First run pressure tests against existing skills and project instructions. If repeated failures remain, create the following reusable skills using the required red-green-refactor process:

| Candidate skill | Trigger | Reusable content |
|---|---|---|
| `claim-evidence-assurance` | Auditing scientific or formal claims that span prose, code, data, and proofs | Claim-state taxonomy, evidence-chain checks, forbidden promotions, assurance report template |
| `formal-assumption-audit` | Reviewing Lean/Coq/Isabelle results where theorem hypotheses may hide domain assumptions | Assumption extraction, axiom classification, vacuity tests, negative controls |
| `reproducible-empirical-release` | Releasing computational research with datasets, fits, uncertainty, and publication artifacts | Source manifests, hashing, independent reruns, sensitivity checks, release bundles |
| `manuscript-drift-control` | Keeping papers and repository claims synchronized | Inventory extraction, forbidden wording checks, generated claim tables, PDF/source reconciliation |

Each new skill must have a failing pressure scenario before it is written, a concise trigger-only description, reusable scripts or references where appropriate, a validation run, and a test showing that the skill prevents the observed failure. Project-specific rules that can be enforced mechanically should remain scripts or repository instructions instead of becoming skills.

## Verification and acceptance criteria

The initiative is complete only when all of the following are true:

1. The formal gate verifies the exact declared target set from a clean, pinned environment, with an explicit assumption report.
2. The target count, Lean version, Mathlib revision, and verification status agree across scripts, CI, manuscripts, manifests, and PDFs.
3. SPARC inputs, code, outputs, parameter tiers, uncertainty calculations, and data provenance are reproducible offline from a release bundle.
4. An independent implementation reproduces the headline measurement within declared tolerances.
5. The 342-parameter comparison and all “zero-parameter” language are mathematically and statistically precise.
6. Every headline claim has a stable claim ID and a typed evidence chain.
7. Cross-repository connections are formal interfaces or explicitly labeled conjectural relationships.
8. CI catches seeded claim drift, stale inventory, missing artifacts, forbidden wording, and failed reproduction commands.
9. Publication artifacts are generated from a known commit and include a machine-readable assurance report.
10. An adversarial evaluator catches deliberate overclaims and does not promote skipped or historical results.

## Risks and decisions requiring user approval

The largest risk is scope expansion: turning every interesting idea in Chyren, 4Leibniz, and RYTT into a Res-Nova dependency would weaken rather than strengthen the project. The plan therefore treats cross-repository connections as typed interfaces and requires evidence before integration. Other risks include large Mathlib CI costs, external-data licensing, numerical disagreement between pipelines, and the possibility that some headline claims must be narrowed or retracted.

User approval is needed before implementation begins on: the assurance-level taxonomy; the canonical claim schema; whether to commit a release data bundle or use an external archive; the acceptable cold-cache CI budget; and which claims are publication-critical for the first hardening milestone.
