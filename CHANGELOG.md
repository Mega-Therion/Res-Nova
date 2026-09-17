# Changelog — Res Nova

All notable changes to the Res Nova technical manuscript, formal verification, and reproducibility package.

## [1.9.0] — 2026-09-16

### 2026-09-17 (v1.9.x, post-PR-70 hygiene)
- Moved `A0_HIGHZ_MEASUREMENT_2026-09-16.md` to `02_galaxy_dynamics/` (path fix: the
  public Research Atlas cites the prefixed path; the doc now sits with its data,
  scripts, and run logs). All in-repo references updated. No content changes.

### The finite algebraic core and the six interpretation obligations (layer 0 cycle)
- **Finite core frozen** (`CORE_OBJECTS_AUDIT_LEDGER_2026-09-16.md`): BT ≅ 2T (Q8 ⋊ C3) fully audited — order census, conjugacy-class partition {1,1,4,4,4,4,6}, complete character table, irrep dims {1,1,1,2,2,2,3}; all finite algebraic claims `[P]`.
- **μ_std representation audit + Postulate R isolation**: input boundary mapped; μ_dual killed (`[X]`, Cassini + chiral reading); the (μ, a₀) map measured on SPARC (175 galaxies, 3391 points, frozen harness) — rows pairwise disjoint, μ_std a₀ = 1.1607e-10 is the only cosmologically comparable object.
- **Obligations 1–6 discharged to their stated limits** (`PHYSICAL_INTERPRETATION_LAYER_0_2026-09-16.md`): Theorem B-cov (celerity identification derived as the unique covariant coupling); chiral alphabet reduced to the substrate double cover's kernel (GL(2,3) identified as the Pin⁺-type cover — a machine-verified trap); the 2π given its covariant home (the Euclidean closure of the K2 orbit, the channel's thermal circle).
- **Correction discipline (#58 → #59)**: the obligations-4-and-5 discharge of PR #58 overclaimed; PR #59 corrected it — Pin⁻ "forcing" restated N4 (circular), and SPARC's Hubble-flow distances (97/175, f_D=1 = H₀=73 per SPARC_Lelli2016c.mrt note 2) make the window→H₀ inversion ladder-covariant; 68% windows are not falsifiers. Layer 0's evening/final block carries a dated supersession note.
- **Distance-corrected a₀ verification (#60, 8/8, 95% intervals)**: T1 reproduces the frozen window to 0.000%; T2 (flow rescaled to Planck) shifts a₀ to 1.0975e-10 with the Planck anchor inside at <1σ; T3 (non-flow only, 78 galaxies) shifts a₀ by +0.2% — the flow formula is exonerated, the ladder zero point is the covariance, located and quantified. The relation a₀ = cH₀/2π is verified distance-robust; the inversion is NOT independent; no side is taken; maser-host geometric distances named as the mover.
- **N4 derived from the action level (#61, 13/13)**: the bespoke input "the channel is orientation-sensitive" retired — spinoriality (frozen: 2π = −I) + thermal-circle sheets + B-cov plane-reflection parity + the Kramers antiunitary lift `[C]` select Pin⁻ structurally (Pin⁺ would need orientation to be the point inversion, which B-cov excludes).
- **Exact-pipeline gap partially closed**: legacy a₀ = 1.107e-10 bracketed, not reproduced (reconstruction with per-galaxy D/I priors: 1.0243e-10, 68% [9.608, 10.853]e-11; +10.3% shift closes 53% of the gap; residual attributed to the original optimizer's undocumented specifics).
- **Reproducibility (#62)**: SPARC master table + rotmods read from the repo, not /tmp; PR #60's three treatment values reconfirmed from a repo-relative run (8/8).

**Program residual inputs after this cycle:** μ′(0) = 1, the horizon-selection reason, and the single `[C]` KMS/antiunitary identification.

## [1.8.0] — 2026-09-12

### Open targets closed
- **O5 — SPARC clean-clone fetch: CLOSED** (`VERIFICATION_RUN_009/02_sparc_fetch/`). `fetch_sparc.sh` executed end-to-end from a clean clone with `SPARC_DATA_DIR` isolated outside the repo: official CWRU `Rotmod_LTG.zip` downloaded, 175 `*_rotmod.dat` files extracted, **175/175 SHA-256 checksums verified against the frozen manifest, 0 drift, exit 0**. `fetch_sparc.sh` now falls back to `python3 zipfile` when `unzip` is absent (the SHA-256 manifest remains the sole content authority). SPARC data remains deliberately not vendored in git.
- Status docs (`README.md`, `FOR_REFEREES.md`, `RELEASE_CHECKLIST.md`, `RES_NOVA_VERIFICATION_LEDGER.md` F7, `PEER_REVIEW_READINESS.md`) updated from the stale 17-module / O6-open language to the current inventory: **43 gate targets** (18 manuscript modules + 25 adjacent-programme modules declared in `ADJACENT_MODULES.txt`), O6 closed 2026-09-08 (cold fetch `VERIFICATION_RUN_008` + CI `lean-gate` on every push, green at `d130413`).

### Physics corrections recorded earlier in this window (already on main; now ledgered here)
- **D7 ghost-free second derivative corrected (2026-09-08, #37):** `F''(K) = 1/(4√K(1+√K)²)`, not the previously published formula taken with respect to `u` instead of `K`. Linear screening ratio `F''/F' = 1/(2x₀²(1+x₀)) ≈ 0.00233` (**0.23%** growth enhancement, not 0.4%); screening is 1.7× stronger than previously published; no conclusion changes. Machine-checked as `CovariantCompletion.F_dual_ghost_free` + `F_dual_second_deriv_antitone`. See `GHOSTFREE_AND_SCREENING_CORRECTION_2026-09-08.md`.
- **D7 suppression restatement (2026-09-08, #38):** the "~250×" linear-growth suppression is `1/0.004`, the corrected value is `~429×`; label collision with the unrelated external-field-effect 250× disambiguated.
- **D3 PPN β bound + vacuity audit (2026-09-08, #36):** PPN β bounded; two D7 PPN theorems audited as vacuous and relabelled.
- **SU(2) envelope rungs adopted (2026-09-09, #39):** gate grows 39 → 43 targets, independently verified.

### D5 — Cosmological N-body test (pre-registered, fail-closed)
- **D5 executed at validation config** (N_pcl = N_grid = 256³, L = 200 Mpc/h,
  seed 42): patched gevolution with G_eff_tilde(a,k) Poisson-kernel modification
  per Hassani & Lombriser Sec. 2.4; two-arm design (α=1 theory, α=0.01 negative
  control) vs ΛCDM baseline, identical ICs; prereg hash-frozen before any
  production run (`04_cosmology/PREREG_D5_MG_EVOLUTION.md`).
- **V0 patch correctness:** PASS (frozen unit test, max relative kernel error < 1e-10).
- **V1 pipeline sensitivity (negative control): PASS** — α=0.01 median ΔP/P
  **+22.2%** at k ≤ 0.2 h/Mpc, z≈0 (gate ≥ +5%; linear prediction +20.4%).
- **V2 theory arm: INCONCLUSIVE — D5 stays open.** α=1 worst bin **3.03%**
  (k = 1.354 h/Mpc, z = 1); 124/180 bins above the 1% consistency bound at z=0;
  no bin reaches the 5% tension threshold. Nonlinear amplification is ~100× the
  linear prediction (0.005–0.036%) but bounded below the νHDM-style blow-up.
- **Fail-closed apparatus proven in the field:** the V1 gate caught a
  macroless-pipeline build defect (arm binaries compiled without
  `-DMG_ARM_A`/`-DMG_ARM_B` → all three runs bit-identical plain ΛCDM)
  before any verdict was published; corrected runs rebuilt with a
  byte-identity build guard (job fails if arm binary matches a plain build).
- Production runs executed on GitHub Actions (sandbox instability documented;
  six silent container deaths). Full run ledger: `04_cosmology/D5_RUN/`;
  broken-pipeline verdict preserved as evidence
  (`D5_RUN_VERDICT_MACROLESS_PIPELINE.json`). CLM-D5-03 resolved to Branch 3
  and inserted into `OPEN_PROBLEMS_AND_TESTS.md`.

## [1.7.0] — 2026-08-26

### Unification & Black Hole Spin Sector (UFW-C1 Milestone)
- **Exact Kerr Rapidity Equipartition Theorem (`06_unification_and_spin/rapidity_uniqueness_proof.py`):**
  - Proved symbolically and numerically to 100 decimal digits that $\operatorname{arsinh}(1) = \ln(1+\sqrt{2}) = \operatorname{artanh}(1/\sqrt{2}) \approx 0.881373587$.
  - Demonstrated that $\theta_{\text{amplitude}} = 1/\sqrt{2}$ is the unique velocity/spin where relativistic momentum equals rest mass ($\sinh(\psi)=1$, $p=mc$, $\gamma=\sqrt{2}$).
  - Proved the silver ratio odds relation $\frac{\theta}{1-\theta} = 1+\sqrt{2} \equiv \delta_S$.
  - Derived the gate arithmetic mean $\theta_{\text{gate}} = \frac{1}{2}(\ln 2 + 1/\sqrt{2}) \approx 0.700127 \approx 0.700$ ($0.018\%$ agreement with canonical $0.700$).
- **Two-Channel Sovereign Spin Ceiling (`06_unification_and_spin/two_channel_ceiling_proof.py`):**
  - Derived the closed-form sovereign spin ceiling $\chi_s = \sqrt{2\theta - \theta^2} = \sqrt{\sqrt{2} - 1/2} \approx 0.956145157584922$.
- **Horizon Dynamics & Cauchy Bounce (`06_unification_and_spin/kerr_toroidal_bounce.py`, `thorne_equilibrium_fast.py`):**
  - Evaluated the classical Thorne (1974) thin-disk deficit ($L_{\text{ms}}/E_{\text{ms}} - 2a^* \approx 0.395$ vs $0.054$).
  - Clarified that the $(1 - a^{*2})^{-1/2}$ curvature divergence is localized at the inner Cauchy horizon / throat pinch, driving the quantum topological counter-torque $\tau_{\text{top}}$ that arrests extremal spin at $\chi_s$.
- **Substrate & Triality Geometrodynamics (`06_unification_and_spin/so3_haar_derivation.py`, `e8_algebraic_sweep.py`):**
  - Ingested $V_2(\mathbb{R}^3) \cong \mathrm{SO}(3)$ Haar measure and $E_8$ root balanced ternary analysis into the canonical verification tree.
- **Evidence Ledgers:**
  - Added CLM-10, CLM-11 to `CLAIM_EVIDENCE_LEDGER.md` and Finding F9 to `RES_NOVA_VERIFICATION_LEDGER.md`.

## [1.6.2] — 2026-08-16

Submission build. `\sealfalse` — the Chyren watermark is off for the APS
copy, per the recommendation in `SUBMISSION/README.md`. The
`\sealtrue`/`\sealfalse` switch remains; flipping it back restores the
seal for repository or presentation copies. This is the build deposited
to Zenodo, so the archived source and the archived PDF correspond
exactly. No physics claims change.

## [1.6.1] — 2026-08-16

Submission-readiness release. No physics claims change.

### Manuscript
- **Corrected the constitutive relation.** v1.5.0 and earlier printed `μ(x) ≡ F'_dual(x) = x − 1 + 1/(1+x) = x/(1+x)`. The middle expression evaluates to `x²/(1+x)`, so that line conflated `F'` with `μ`. Corrected to `F'(x) = x²/(1+x)` and `μ = F'/x = x/(1+x)`, the AQUAL constitutive ratio already used in D2 and encoded in `DualChannelDerivation.lean`. Disclosed in a boxed in-text note, not silently patched. Nothing downstream changes — the field equation, `F''`, both limits and the SPARC benchmark all use `μ`, which is unchanged. The same error in the Lean module inventory row is also fixed.
- Narrowed one verification claim: `DualChannelDerivation.lean` certifies the channel-balance identity and the μ bounds; it does **not** symbolically differentiate `F_dual`. That step is hand/CAS-verified.
- New sections for D2 (conditional uniqueness), D7 (RMOND completion), D3 (solar system, Vainshtein, Q₂ prediction), D5 (cosmology), D6 (stability). Open problems O7–O9 added.
- Converted to **REVTeX 4.2** (`aps,prd,preprint`) with `apsrev4-2` bibliography. collaboration seal added behind a `\sealtrue`/`\sealfalse` switch.
- Acknowledgments state sole authorship; no non-human co-credit.
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
- **D7 — Covariant Completion:** RMOND action with F_dual free function. Background Friedmann unmodified. Linear screening F''/F' ≈ 0.004 [CORRECTED 2026-09-08 to 0.00233]. Resolves D5 overproduction (76× → 0.4% [corrected: 0.23%]). Ghost-free verified. c_T = c confirmed.
- **D7 Supplement — Coupling Optimization:** Vainshtein screening identified. Q₂ resolved at 70× below Cassini. Natural O(1) coupling constants viable. No fine-tuning needed.
- **D6 — Relativistic Stability:** Ghost-free (F''>0 ∀K>0). Hamiltonian bounded below. Strong coupling scale ~10⁻¹⁰ eV.

### Empirical Analysis (New)
- **D3 — PPN / Solar System:** MOND correction 1137× below Cassini. PPN parameters depend on D7, not on μ. Q₂ tension resolved via Vainshtein + F''/F' screening.
- **D5 — Cosmological Sector:** Growth factor computed. Non-relativistic 2× MOND → 76× excess. RMOND linear screening → 0.4% enhancement [CORRECTED 2026-09-08 to 0.23%]. νHDM crisis quantified (Russell et al. 2026). Non-linear regime identified as key open question.

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
- **Manuscript Alignment:** res_nova_manuscript.tex updated with O1 Lean proof and O4 redshift test result. O6 wording harmonized across README, manuscript, appendix, and ledgers. res_nova_manuscript.pdf rebuilt via pdflatex + bibtex + pdflatex + pdflatex.

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


> **CORRECTION 2026-09-16 (post-merge, PR #61 step v sign reversed):** the standard dictionary (Witten, *Fermion Path Integrals and Topological Phases*, arXiv:1508.04715, §1 and App. A) is Kramers T² = (−1)^F ⇔ spatial/Euclidean reflection R² = +1 ⇔ **Pin⁺**; T² = +1 ⇔ R² = (−1)^F ⇔ Pin⁻ — same convention as this corpus (Pin⁺ reflection lifts square +1). The Wick rotation supplies the factor that flips the sign; the minimal instance (iσ_yK)² = −I is the Lorentzian T, whose Euclidean reflection image squares to +I. So chain (i)–(v) as stated selects **Pin⁺**, not Pin⁻. Pin⁻ requires T² = +1 (Majorana-chain / class BDI sector). Obligation 4 is **OPEN** again; the arithmetic in `scripts/n4_action_derivation.py` is correct, the physics identification in step (v) is not.
