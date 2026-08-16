# Changelog — Res Nova

All notable changes to the Res Nova technical manuscript, formal verification, and reproducibility package.

## [1.6.1] — 2026-08-16

Submission-readiness release. No physics claims change.

### Manuscript
- **Corrected the constitutive relation.** v1.5.0 and earlier printed `μ(x) ≡ F'_dual(x) = x − 1 + 1/(1+x) = x/(1+x)`. The middle expression evaluates to `x²/(1+x)`, so that line conflated `F'` with `μ`. Corrected to `F'(x) = x²/(1+x)` and `μ = F'/x = x/(1+x)`, the AQUAL constitutive ratio already used in D2 and encoded in `DualChannelDerivation.lean`. Disclosed in a boxed in-text note, not silently patched. Nothing downstream changes — the field equation, `F''`, both limits and the SPARC benchmark all use `μ`, which is unchanged. The same error in the Lean module inventory row is also fixed.
- Narrowed one verification claim: `DualChannelDerivation.lean` certifies the channel-balance identity and the μ bounds; it does **not** symbolically differentiate `F_dual`. That step is hand/CAS-verified.
- New sections for D2 (conditional uniqueness), D7 (RMOND completion), D3 (solar system, Vainshtein, Q₂ prediction), D5 (cosmology), D6 (stability). Open problems O7–O9 added.
- Converted to **REVTeX 4.2** (`aps,prd,preprint`) with `apsrev4-2` bibliography. Chyren Collaboration seal added behind a `\sealtrue`/`\sealfalse` switch.
- Acknowledgments state AI use explicitly: LLM tools assisted under the author's direction, no AI system is an author.
- Abstract trimmed 396 → 211 words.
- All external citations verified against primary sources (Park et al. 2026; Russell et al. 2026; Thomas et al. 2023; Vainshtein 1972).

### Repository
- Repository made **public**; Data Availability now resolves for referees.
- `.zenodo.json` added for GitHub–Zenodo release archiving.
- `SUBMISSION/` package: PRD cover letter with four suggested referees, journal rationale, pre-submission checklist.
- `PEER_REVIEW_READINESS.md`: removed an in-progress recount artifact and fixed a 7-vs-8 self-contradiction (correct: 8 `[P]`, 4 `[P/O]`).

## [1.6.0] — 2026-08-16

### Theoretical Framework (New)
- **D2 — Physical Action Derivation:** 13 theorems proving F_dual is uniquely determined given 4 structural constraints. Padé[1/1] uniqueness, odds-ratio/Bayesian structure, Fisher information identity F'²·I = x³, dual-channel cancellation mechanism. Status: D2_PROPOSED (conditional uniqueness [P], Padé necessity [O]).
- **D7 — Covariant Completion:** RMOND action with F_dual free function. Background Friedmann unmodified. Linear screening F''/F' ≈ 0.004. Resolves D5 overproduction (76× → 0.4%). Ghost-free verified. c_T = c confirmed.
- **D7 Supplement — Coupling Optimization:** Vainshtein screening identified. Q₂ resolved at 70× below Cassini. Natural O(1) coupling constants viable. No fine-tuning needed.
- **D6 — Relativistic Stability:** Ghost-free (F''>0 ∀K>0). Hamiltonian bounded below. Strong coupling scale ~10⁻¹⁰ eV.

### Empirical Analysis (New)
- **D3 — PPN / Solar System:** MOND correction 1137× below Cassini. PPN parameters depend on D7, not on μ. Q₂ tension resolved via Vainshtein + F''/F' screening.
- **D5 — Cosmological Sector:** Growth factor computed. Non-relativistic 2× MOND → 76× excess. RMOND linear screening → 0.4% enhancement. νHDM crisis quantified (Russell et al. 2026). Non-linear regime identified as key open question.

### Epistemic Corrections
- **O1 rescored [P] → [P/O]:** 2π KMS cancellation proved; a₀=cH identification open (5.67× discrepancy; O4 disfavours at 5.9σ).
- **D2 rescored [P] → [P/O]:** Conditional uniqueness proved; Padé necessity open.
- **PR #16 merged:** AUDIT_LEAN_INVENTORY.md corrected for HorizonScale.lean presence on main.
- **PEER_REVIEW_READINESS.md:** 8/12 fully reviewable, 4/12 partially ready, 0/12 fully open.

### Infrastructure
- `04_cosmology/growth_factor_computation.py` — cosmological growth factor solver
- `02_galaxy_dynamics/ppn_solar_system.py` — PPN and solar system MOND correction computation
- `CLAIM_EVIDENCE_LEDGER_v1.6.0_SUPPLEMENT.md` — new claims from D2/D3/D5/D6/D7
- `PEER_REVIEW_READINESS.md` — peer review readiness assessment

## [1.5.0] — 2026-08-16

### Theoretical & Formal Layer
- **O1 — Horizon-Scale Derivation:** HorizonScale.lean formal proof completed. KMS 2π cancellation proved; a₀ = cH (ξ = 1), not cH/(2π). Axiom footprint documented in AUDIT_LEAN_INVENTORY.md. Status: D0_PROPOSED.
- **O4 — Pre-Registered Redshift Test:** a₀(z) test executed on 20 MUSE-DARK galaxies (z ≤ 1.44). H_const favoured over H_horizon at 5.9σ. Horizon-tied a₀(z) = ξcH(z) excluded at >3σ. Disfavours horizon interpretation; does not falsify MOND itself. Expanded pre-registration: JWST NIRSpec 3D kinematics (30–50 galaxies, z ≤ 3.0) + strong lensing (SLACS/BELLS, z ≤ 1.0), combined meta-analysis with Fisher's method. Timeline: Q3 2026 – Q2 2027.
- **D9 — Skordis–Złośnik Embedding:** TARGET_D9_SKORDIS_ZLOSNIK_EMBEDDING.md documents the RMOND embedding pathway. GW170817 sound speed constraint, PPN limits, and convexity guarantees catalogued.

### Empirical & Reproducibility
- **O5 — SPARC Automation:** fetch_sparc.sh downloads official CWRU Rotmod_LTG.zip with SHA-256 manifest verification. --data-dir support added to all 6 data-reading scripts. All hardcoded /home/mega paths removed from active files.
- **a₀ measurement:** Format standardized to (1.116 ± 0.128_stat ± 0.097_syst) × 10⁻¹⁰ m s⁻² across all ledger files.
- **F7 — Lean Module Inventory:** Rebuilt from exact git ls-files — 17 tracked Lean modules. PrintAxioms.lean/PrintAxiomsD8.lean classified DIAGNOSTIC; AXIOMS_V2.lean as ASSUMPTIONS [O].

### Verification
- **O6 — Clean Worktree Reproduction:** VERIFICATION_RUN_007 — isolated clone in /tmp/res_nova_o6_clean, no pre-existing .lake/packages/mathlib. 17/17 targets verified. Standard axiom footprint: [propext, Classical.choice, Quot.sound]. Not yet a CI release gate; cold-machine reproduction still open.
- **Manuscript Alignment:** final_manuscript.tex updated with O1 Lean proof and O4 redshift test result. O6 wording harmonized across README, manuscript, appendix, and ledgers. final_manuscript.pdf rebuilt via pdflatex + bibtex + pdflatex + pdflatex.

### Epistemic Realignment
- EPISTEMIC_BOUNDARY_v1.5.0.md — canonical boundary. Previous versions (v1.1.0–v1.4.0) archived in archive/.
- CLAIM_EVIDENCE_LEDGER.md — realigned with repo-relative root, dual-channel algebraic status for CLM-01, superseded status for CLM-05.
- RES_NOVA_VERIFICATION_LEDGER.md — findings F1–F8 realigned for v1.5.0 with repo-relative paths.
- CORPUS_DEPENDENCY_MAP.md — updated to 17 Lean modules and repo-relative paths.
- RELEASE_CHECKLIST.md — realigned to 17 Lean modules, Tier 1 374-param accounting.
- F2 algebra replaced with exact DualChannelDerivation.lean theorem names.

### Infrastructure
- MVPC-X Integration: Claim manifests for D1.2, D3.1, F7, O1, O6. Judge adapter with verdict log. Pinned to commit 09876e8.
- CI: check_manuscript_inventory.py wired to GitHub Actions verify.yml. Manifest validation + MVPC-X claim consumer judge in CI.
- Environment: environment.yml and requirements.txt added for reproducible environment specification.

### Open Problems Status
- O1: Formal proof done (HorizonScale.lean). Remaining: archive #print axioms for HorizonScale specifically.
- O4: Test completed (H_const favoured at 5.9σ). Remaining: expanded JWST/lensing meta-analysis (Q3 2026 – Q2 2027).
- O5: Resolved via Option A (automated fetch + manifest verification, data non-vendored).
- O6: Clean worktree walk done (17/17 PASS). Remaining: CI runner, cold-machine with empty host cache.

## [1.4.0] — 2026-08-15

Tagged release with dual-channel action, SPARC cross-validation pipeline, Lean 4 formalization suite, and reproducibility appendix. See git log at tag v1.4.0 (commit 651a70d) for full state.

## [1.1.0] — 2026-08-14

Expanded Lean formalization and SPARC benchmark integration.

## [1.0.0] — 2026-08-14

Initial repository creation. Foundational action derivation, manuscript skeleton, and Lean 4 proof infrastructure.
