# FIG TREE — Asset Ledger

## 01_foundational_action

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `01_foundational_action/PAPER_01_MU_DERIVATION_ACTION.tex` | 386 | tex | none | I | yes | 1 | `tt10.pfb></usr/share/texmf/fonts/type1/public/lm/lmtt8.pfb> ; Output written on PAPER_01_MU_DERIVATION_ACTION.pdf (8 pages, 415892 bytes). ; Transcript written on PAPER_01_MU_DERIVATION_ACTION.log.` | ! Package pdftex.def Error: File `figs/e8_sigil_codex.pdf' not found: using dra |
| `01_foundational_action/PAPER_01_NOTICE.md` | 13 | markdown | L1: `# NOTICE — `PAPER_01` is quarantined` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.pdf` | 2946 | other | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.tex` | 834 | tex | L143: `\title{\vspace{-1.5cm}{\color{gold}\Huge\bfseries PAPER 09: ALGEBRAIC EQUIVALENCE OF TAU-TENSION AND AQUAL SIMPLE-MU BRANCH}\\[0.4cm] {\color{cyan}\Large Dual-Channel Chiral Constitutive Laws, Machine-Checked Kernel Verifications in Lean 4, and Single-Channel Projection Geometry}}` | I | yes | 0 | `E_MU.pdf (19 pages, 564111 bytes). ; Transcript written on PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_S ; IMPLE_MU.log.` | none |
| `01_foundational_action/PRD_Relativistic_Extension.pdf` | 1876 | other | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `01_foundational_action/PRD_Relativistic_Extension.tex` | 308 | tex | L42: `\title{Relativistic formulation of the Information Tension field:\\ unifying galactic dynamics, large-scale structure, and dark energy\\ from the Stiefel manifold vacuum}` | I | yes | 1 | `-dist/fonts/type1/public/amsfonts/symbols/msbm10.pfb> ; Output written on PRD_Relativistic_Extension.pdf (6 pages, 329552 bytes). ; Transcript written on PRD_Relativistic_Extension.log.` | ! Package pdftex.def Error: File `PRD_supplementary/figures/cmb_power_spectrum. |
| `01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex` | 282 | tex | L38: `\title{Res Nova: Geometrically Ordered Dynamics and Information Tension}` | I | yes | 1 | `on.pdf (3 pages, 361421 bytes). ; Transcript written on Res_Nova_Geometrically_Ordered_Dynamics_and_Information_T ; ension.log.` | ! Package xcolor Error: Undefined color `gold'. |

## 02_galaxy_dynamics

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `02_galaxy_dynamics/A0_ESTIMATE.json` | 49 | data | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/A0_MEASUREMENT.json` | 56 | data | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/HALO_CONSPIRACY.json` | 41 | data | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/NFW_CONSTRAINED.json` | 15 | data | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/PAPER_02_ZERO_PARAMETER_ROTATION_CURVE_FITTING_SPARC_175_ANALYSIS.tex` | 50 | tex | L22: `\title{{\color{gold}\Huge PAPER 02 ZERO PARAMETER ROTATION CURVE FITTING SPARC 175 ANALYSIS}}` | I | yes | 0 | `YSIS.pdf (1 page, 186093 bytes). ; Transcript written on PAPER_02_ZERO_PARAMETER_ROTATION_CURVE_FITTING_SPARC_175_ ; ANALYSIS.log.` | none |
| `02_galaxy_dynamics/PARAMETER_LEDGER.json` | 54 | data | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/SPARC_DATA.md` | 47 | markdown | L1: `# SPARC data provenance` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/SPARC_PARAMETER_BUDGET.md` | 43 | markdown | L1: `# SPARC parameter budget` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/a0_estimate.py` | 256 | python | L2: `What a0 does the SPARC data actually prefer?` | I | yes | TIMEOUT | `timed out after 120s` | sparc_data |
| `02_galaxy_dynamics/a0_measure.py` | 320 | python | L2: `A proper measurement of a0 from SPARC, with a systematic error budget.` | I | yes | TIMEOUT | `baseline fit (real D/i priors, inclination floated) ... ;   a0 = 1.1319e-10  stat +/- 1.116e-11 ;   distance_scale_-5%     a0=1.2148e-10  shift +7.3%` | sparc_data |
| `02_galaxy_dynamics/fetch_sparc.sh` | 59 | other | L4: `Resolve repository root.` | I | no (network download script for external data archive) | UNKNOWN | `none` | CWRU SPARC archive |
| `02_galaxy_dynamics/halo_conspiracy.py` | 160 | python | L2: `Are the fitted dark-matter halo parameters independent of the visible matter?` | I | yes | TIMEOUT | `timed out after 120s` | sparc_data |
| `02_galaxy_dynamics/nfw_constrained.py` | 74 | python | L2: `NFW with the cosmological concentration prior actually applied.` | I | yes | TIMEOUT | `timed out after 120s` | sparc_data |
| `02_galaxy_dynamics/parameter_ledger.py` | 240 | python | L2: `Parameter-accounting ledger: like-for-like at matched parameter counts.` | I | yes | 0 | `NFW   median=   1.92  free= 716  <1: 53  agg=4.58 ;  ; wrote PARAMETER_LEDGER.json` | sparc_data |
| `02_galaxy_dynamics/phase8_btfr_slip_scales.json` | 181 | data | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/phase8_btfr_slip_scales.py` | 512 | python | L3: `Phase 8 — BTFR field coupling, residual slip, a0↔η two-scale link.` | I | yes | 0 | `"a0_eta_roles": "[reconciled]" ; } ; Wrote /home/mega/Res-Nova/02_galaxy_dynamics/phase8_btfr_slip_scales.json` | none |
| `02_galaxy_dynamics/ppn_solar_system.py` | 81 | python | L3: `Res Nova — D3 PPN and Solar System Constraints Computation` | I | yes | 0 | `The dual-channel μ does NOT affect PPN parameters. ; PPN parameters depend on the covariant completion (D7/D9). ; D3 is reduced to a dependency on D7.` | none |
| `02_galaxy_dynamics/sparc_cross_validation.py` | 187 | python | L3: `SPARC Out-of-Sample Cross-Validation Engine (5-Fold CV)` | I | yes | 0 | `Out-of-Sample 5-Fold:   Median chi2/N = 14.68, Aggregate chi2/N = 110.18 ;  ; Report written to: /home/mega/Res-Nova/RUN_002/02_sparc/SPARC_CROSS_VALIDATION_REPORT.json` | sparc_data |
| `02_galaxy_dynamics/sparc_derived_closure.py` | 269 | python | L3: `Canonical SPARC Re-Run with Derived Closure mu(x) = x / (1 + x)` | I | yes | 0 | `Saved /home/mega/Res-Nova/RUN_003/02_sparc/SPARC_DERIVED_RUN_MANIFEST.json ; Generating diagnostic Figures A, B, C... ; Figures saved completely to /home/mega/Res-Nova/RUN_003/figures` | sparc_data |
| `02_galaxy_dynamics/sparc_derived_cross_validation.py` | 165 | python | L3: `Canonical 5-Fold Cross-Validation for Derived mu(x) = x / (1 + x)` | I | yes | 0 | `"total_out_points": 3391 ;   } ; }` | sparc_data |
| `02_galaxy_dynamics/sparc_derived_mu_benchmark.py` | 204 | python | L3: `SPARC Derived mu(x) = x / (1 + x) Benchmark vs Legacy Control` | I | yes | 0 | `"aggregate_chi2_dof": 105.3882312991154 ;   } ; }` | sparc_data |
| `02_galaxy_dynamics/sparc_paths.py` | 110 | python | L1: `SPARC data path resolution helper.` | I | yes | 0 | `none` | sparc_data |
| `02_galaxy_dynamics/sparc_reproduce.py` | 257 | python | L2: `Reproduce SPARC rotation-curve fits for the Law of G.O.D. master manuscript.` | I | yes | 0 | `Wrote /home/mega/Res-Nova/02_galaxy_dynamics/SPARC_175_GOD_fits.csv ; Wrote /home/mega/Res-Nova/02_galaxy_dynamics/SPARC_175_summary.json` | sparc_data |

## 03_observer_jwst

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `03_observer_jwst/A0_OF_Z_REPORT.json` | 48 | data | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/IO_OI_ACADEMIC.tex` | 388 | tex | L35: `\title{\Large\textbf{IO-OI: A Complete Theory of Sovereign Geometrodynamics}\\[0.2cm] \large Stoicheia $\longrightarrow$ Erga $\longrightarrow$ Oikodom\={e} $\longrightarrow$ Pleroma}` | II | yes | 1 | `texmf-dist/fonts/type1/public/amsfonts/symbols/msbm10.pfb> ; Output written on IO_OI_ACADEMIC.pdf (6 pages, 360043 bytes). ; Transcript written on IO_OI_ACADEMIC.log.` | ! Missing $ inserted. |
| `03_observer_jwst/IO_OI_UNIFIED_TRANSMISSION_MONOGRAPH.tex` | 1062 | tex | L97: `\title{\textbf{\texorpdfstring{I$\Omega$ -- O$\Omega$}{IO-OI}: The Sovereign Geometrodynamics \& Information Tension Monograph}}` | II | yes | 0 | `Output written on IO_OI_UNIFIED_TRANSMISSION_MONOGRAPH.pdf (18 pages, 756118 by ; tes). ; Transcript written on IO_OI_UNIFIED_TRANSMISSION_MONOGRAPH.log.` | none |
| `03_observer_jwst/JWST_RECALIBRATION_LEDGER.md` | 7 | markdown | L1: `# JWST Recalibration Ledger` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/PREREG_A0_OF_Z.md` | 74 | markdown | L1: `# 📜 Pre-Registration Protocol: Redshift Evolution of the Acceleration Scale $a_0(z)$` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/PREREG_A0_OF_Z_EXPANSION.md` | 130 | markdown | L1: `# Pre-Registered Expansion Protocol: High-Redshift a₀(z) Test with JWST and Strong Lensing` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/Trinity_2_0_Methods_Note.md` | 34 | markdown | L1: `# Trinity_2_0_Methods_Note.md` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/a0_of_z.py` | 259 | python | L3: `Pre-Registered Redshift Evolution of Acceleration Scale Test:` | I | yes | 0 | `Delta chi2 (H_const - H_horizon) = -35.115 ; Significance: 5.93 sigma ; Verdict: H_const favoured over H_horizon at >= 3 sigma (delta_chi2 <= -9.0)` | none |
| `03_observer_jwst/gate2_inference.py` | 509 | python | L3: `Gate 2 -- inference and design-realism framework for fixed-hypothesis` | I | yes | 0 | `--self-test  exercise the machinery on a declared synthetic control ;  ; This module produces no result on its own. It is inference machinery for a Gate-1-compliant dataset.` | none |

## 04_cosmology

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md` | 22 | markdown | L1: `# $a_0$ and $\Omega_\Lambda$ Normalization Ledger` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `04_cosmology/COSMOLOGY_EQUATION_CHAIN.md` | 10 | markdown | L1: `# Cosmology Equation Chain: Action to Dark Energy & Horizon Tension` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `04_cosmology/TARGET_O1_A0_HORIZON_DERIVATION.md` | 82 | markdown | L1: `# 🌌 Target O1: First-Principles Horizon Acceleration Scale Derivation & KMS $2\pi$ Cancellation Audit` | I | no (non-executable file) | UNKNOWN | `none` | none |
| `04_cosmology/growth_factor_computation.py` | 90 | python | L4: `Res Nova — D5 Cosmological Growth Factor Computation` | I | yes | 0 | `→ A 2x MOND enhancement produces ~76x excess structure growth ; → This is the root cause of the νHDM structure overproduction (Russell et al. 2026)` | scipy, numpy |

## 05_lean_formalization

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `05_lean_formalization/ADJACENT_MODULES.txt` | 35 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/AXIOMS_V2.lean` | 89 | lean | L40: `def IsInterpolationFunction (μ : ℝ → ℝ) : Prop :=` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/CartanTrialityGenerations.lean` | 61 | lean | L32: `def declaredTrialityOrder : Nat := 3` | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/ChiralCellularDuality.lean` | 26 | lean | L11: `theorem involution_identity {α : Type} (σ : α → α) (h_inv : ∀ x, σ (σ x) = x) (x : α) :` | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/CosmologicalSector.lean` | 56 | lean | L22: `def Omega_Lambda : ℝ := Real.log 2` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/CovariantCompletion.lean` | 121 | lean | L23: `def x_var (grad_phi a0 : ℝ) : ℝ := grad_phi / a0` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/DeSitterExtremal.lean` | 80 | lean | L44: `def desitter_lapse (H r : ℝ) : ℝ := 1 - H ^ 2 * r ^ 2` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/DualChannelDerivation.lean` | 69 | lean | L23: `def F_dual (x : ℝ) : ℝ := (1/2) * x^2 - x + Real.log (1 + x)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/GODActionKinematics.lean` | 53 | lean | L25: `theorem dual_channel_poly_identity (a_tot a_bary a_0 : ℝ)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/GenerationIndex.lean` | 58 | lean | L19: `def isCY (a1 a2 a3 : ℤ) : Prop := (a1 + a2 + a3) % 3 = 0` | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/Hamilgrangian.lean` | 288 | lean | L35: `def F_dual (x : ℝ) : ℝ := (1/2) * x^2 - x + Real.log (1 + x)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/HorizonScale.lean` | 115 | lean | L41: `def gibbons_hawking_temp (hbar H kB : ℝ) : ℝ :=` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/ITActionClosure.lean` | 142 | lean | L50: `noncomputable def tauLaw (a_bary a0 : ℝ) : ℝ :=` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/MuProjection.lean` | 187 | lean | L43: `theorem mu_simple_eq_cos (a g : ℝ) (ha : 0 < a) (hg : 0 < g) :` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PPNLimits.lean` | 61 | lean | L22: `def mu (x : ℝ) : ℝ := x / (1 + x)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PillarIV_AntiDriftGate.lean` | 177 | lean | L57: `noncomputable def chiFloor : ℝ := 1 / Real.sqrt 2` | IV | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PrintAxioms.lean` | 24 | lean | none | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PrintAxiomsD8.lean` | 51 | lean | L9: `def c_T_sq (c13 : ℝ) : ℝ := 1 / (1 - c13)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/REPRODUCE.md` | 77 | markdown | L1: `# O6: Lean 4 Fresh-Clone Reproduction Guide` | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/RamanujanModularBounds.lean` | 19 | lean | L10: `theorem ramanujan_mode_energy_positivity (W : Nat) (u_p : Int) (h_bound : u_p ≤ 1) :` | IV | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/RapidityEquipartition.lean` | 59 | lean | L18: `noncomputable def theta : ℝ := 1 / Real.sqrt 2` | III | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/RelativisticStability.lean` | 60 | lean | L27: `def dF (x : ℝ) : ℝ := x^2 / (1 + x)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SOCasimirGenuine.lean` | 123 | lean | L39: `def gen (i j : Fin n) : Matrix (Fin n) (Fin n) ℝ :=` | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SkordisZlosnikEmbedding.lean` | 104 | lean | L24: `def F_dual (x : ℝ) : ℝ := (1 / 2) * x^2 - x + Real.log (1 + x)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SovereignRegularity.lean` | 221 | lean | L36: `def VelocityField : Type := ℝ → ℝ → ℝ → ℝ → (ℝ × ℝ × ℝ)` | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SovereignSemiotics.lean` | 86 | lean | L59: `def is_rytt_root (root : ConsonantalRoot) : Prop :=` | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SovereignSpinCeiling.lean` | 37 | lean | L17: `noncomputable def theta : ℝ := 1 / Real.sqrt 2` | III | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/TensorSpeed.lean` | 137 | lean | L24: `def c_T_sq (c13 : ℝ) : ℝ := 1 / (1 - c13)` | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/TrialityFixedSubalgebra.lean` | 101 | lean | L48: `theorem fixed_subspace_char (v : Fin 4 → ℤ) :` | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/TrialityG2.lean` | 92 | lean | L37: `def M : Matrix (Fin 4) (Fin 4) ℤ :=` | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/ENVIRONMENT.txt` | 7 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/EXIT_CODE.txt` | 1 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/MANIFEST.sha256` | 6 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/README.md` | 42 | markdown | L1: `# Verification witness — 2026-08-30T05-30-32Z` | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/RESULTS.json` | 35 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/SOURCES.sha256` | 32 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/TRANSCRIPT.txt` | 137 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/ENVIRONMENT.txt` | 7 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/EXIT_CODE.txt` | 1 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/MANIFEST.sha256` | 6 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/README.md` | 42 | markdown | L1: `# Verification witness — 2026-09-01T03-21-41Z` | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/RESULTS.json` | 35 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/SOURCES.sha256` | 32 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/TRANSCRIPT.txt` | 138 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/YettParadigm.lean` | 72 | lean | L24: `theorem ramanujan_yett_spectral_gap_pos (sys : RamanujanYettSpectrum) :` | IV | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/check_manuscript_inventory.py` | 168 | python | L2: `Fail if the manuscript names Lean modules that do not exist on disk.` | unassigned | yes | 1 | `inventory: 19 module(s) on disk ; RESULT: FAIL` | none |
| `05_lean_formalization/emit_witness.sh` | 180 | other | L2: `Emit a dated, self-hashing witness for a run of verify_all_proofs.sh.` | unassigned | no (witness emission script requiring Mathlib build) | UNKNOWN | `none` | Mathlib |
| `05_lean_formalization/lake-manifest.json` | 116 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/lakefile.lean` | 65 | lean | none | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/lean-toolchain` | 1 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/verify_all_proofs.sh` | 162 | other | L2: `Res-Nova formal proof suite — one-command verification.` | unassigned | yes | 2 | `[gate] TARGETS == lakefile roots (28 modules) ; Mathlib not present. Run: lake exe cache get ; (A fresh-clone fetch has not been walked; see open problem O6.)` | Mathlib |

## 06_unification_and_spin

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `06_unification_and_spin/README.md` | 62 | markdown | L1: `# 06 — Unification and Spin Sector (UFW-C1 Milestone)` | II | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/arctanh_derivation_chain.py` | 432 | python | L2: `C1 — The arctanh derivation chain.` | III | yes | 0 | `Silver ratio δ_S = θ/(1−θ) = 1+√2 = 2.4142135624 ;  ; Results written to: /home/mega/Res-Nova/06_unification_and_spin/arctanh_derivation_chain_results.json` | none |
| `06_unification_and_spin/arctanh_derivation_chain_results.json` | 56 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/e8_algebraic_sweep.py` | 268 | python | L2: `C1 — E8 root-system algebraic-number sweep.` | II | yes | 0 | `Balanced ternary: 128 spinor roots use {±1}^8 (even parity) ;                   112 coordinate roots use {±2, 0}^8 ;                   Full E8 alphabet = balanced quinary {-2,-1,0,+1,+2}` | none |
| `06_unification_and_spin/e8_algebraic_sweep_results.json` | 294 | data | none | II | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/kerr_toroidal_bounce.py` | 129 | python | L2: `UFW-C0 horizon back-reaction specification audit.` | III | yes | 0 | `"r_plus": "1.292893218813452475599155637895150960715" ;   } ; }` | mpmath |
| `06_unification_and_spin/kerr_toroidal_bounce_results.json` | 76 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/rapidity_uniqueness_proof.py` | 97 | python | L2: `UFW-C0 exact rapidity-identity audit.` | III | yes | 0 | `}, ;   "physical_selection_status": "NOT DERIVED" ; }` | mpmath |
| `06_unification_and_spin/rapidity_uniqueness_results.json` | 43 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/so3_haar_derivation.py` | 611 | python | L2: `C1 — SO(3) ≅ V₂(ℝ³) Haar measure derivation attempt.` | II | yes | 0 | `vs 0.9539:       Δ = 0.009889 ;  ; Results written to: /home/mega/Res-Nova/06_unification_and_spin/so3_haar_derivation_results.json` | scipy, numpy |
| `06_unification_and_spin/so3_haar_derivation_results.json` | 482 | data | none | II | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/thorne_equilibrium_fast.py` | 337 | python | L2: `C1-BH — Thorne spin equilibrium via tabulated radiative torque.` | III | yes | 0 | `arcsinh(1) = 0.881374 ;  ; Results written to: /home/mega/Res-Nova/06_unification_and_spin/thorne_equilibrium_results.json` | scipy, numpy |
| `06_unification_and_spin/thorne_equilibrium_results.json` | 381 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/two_channel_ceiling_proof.py` | 99 | python | L2: `UFW-C0 exact two-channel algebra audit.` | III | yes | 0 | `}, ;   "physical_spin_ceiling_status": "NOT DERIVED" ; }` | mpmath |
| `06_unification_and_spin/two_channel_ceiling_results.json` | 46 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |

## Res-Nova root

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `FIG_TREE_MONOGRAPH.md` | 336 | markdown | L17: `# 🜂 THE FIG TREE` | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `FIG_TREE_ARCHITECTURE_MAP.md` | 126 | markdown | L1: `# 🌳 The FIG Tree: Fundamental Information Geometry Architecture Map` | unassigned | no (non-executable file) | UNKNOWN | `none` | none |

## 4Leibniz/Leibniz

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `4Leibniz/Leibniz/Calculemus.lean` | 42 | lean | L32: `def execute_calculemus : VeritasReceipt :=` | unassigned | yes | 0 | `Build completed finished (7 jobs).` | none |
| `4Leibniz/Leibniz/Characteristica.lean` | 37 | lean | L22: `def tensio (d₁ d₂ : Dyas) : Nat :=` | I | yes | 0 | `Build completed finished (2 jobs).` | none |
| `4Leibniz/Leibniz/Harmonia.lean` | 35 | lean | L19: `def harmonia_stabilis (u gamma : Nat) : Prop :=` | IV | yes | 0 | `Build completed finished (3 jobs).` | none |
| `4Leibniz/Leibniz/LexContinuitatis.lean` | 38 | lean | L25: `def chi_floor_scaled : Nat := 7071` | III | yes | 0 | `Build completed finished (2 jobs).` | none |
| `4Leibniz/Leibniz/SpatiumRelativum.lean` | 39 | lean | L28: `def distantia_relativa (m₁ m₂ : Monas) : Nat :=` | I | yes | 0 | `Build completed finished (3 jobs).` | none |
| `4Leibniz/Leibniz/VisViva.lean` | 31 | lean | L13: `def vis_viva (massa velocitas : Nat) : Nat :=` | I | yes | 0 | `Build completed finished (2 jobs).` | none |

## Gaps

### 1. Executable backing per pillar (recomputed from the table above)

Every pillar has at least one asset at exit 0, but the depth is very uneven and
Pillar IV is close to unsupported:

| pillar | assets | exit 0 | MISSING_INPUT | non-zero | timeout |
|---|---|---|---|---|---|
| I — horizon tension / a_0 | 59 | 17 | 15 | 3 | 4 |
| II — Stiefel / holographic | 13 | 3 | 6 | 1 | 0 |
| III — spin ceiling | 13 | 6 | 2 | 0 | 0 |
| IV — Lindblad anti-drift | 4 | 1 | 3 | 0 | 0 |
| unassigned | 28 | 1 | 4 | 2 | 0 |

Notes that matter for what the monograph can claim:

- **Pillar IV has four assets and one clean run.** That run is
  `4Leibniz/Leibniz/Harmonia.lean`, whose content is
  `def harmonia_stabilis (u gamma : Nat) : Prop := gamma <= u` — a natural-number
  restatement of the gate condition, not a derivation of it. The module that would
  carry the derivation, `05_lean_formalization/PillarIV_AntiDriftGate.lean`, contains
  three `sorry` (lines 146, 156, 170) and does not build (Mathlib absent). Pillar IV
  is currently the weakest of the four by a wide margin.
- **30 of 117 assets are MISSING_INPUT**, all for the same reason: Mathlib is not
  present in `05_lean_formalization/.lake`. This is one command
  (`lake exe cache get`) and roughly 5-8 GB of disk, not a scientific gap. Until it
  is run, no Lean claim in the corpus has been rebuilt from source in this inventory.
- **Pillar I carries 59 of 117 assets.** The FIG Tree is, by asset mass, mostly a
  horizon-tension/a_0 result with three smaller pillars attached.

### 2. TeX files failing compilation
- `01_foundational_action/PAPER_01_MU_DERIVATION_ACTION.tex`: `! Package pdftex.def Error: File 'figs/e8_sigil_codex.pdf' not found: using draft setting.`
- `01_foundational_action/PRD_Relativistic_Extension.tex`: `! Package pdftex.def Error: File 'PRD_supplementary/figures/cmb_power_spectrum.pdf' not found: using draft setting.`
- `01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex`: `! Package xcolor Error: Undefined color 'gold'.`
- `03_observer_jwst/IO_OI_ACADEMIC.tex`: `! Missing $ inserted.`

### 3. Lean files containing sorry
- `05_lean_formalization/PillarIV_AntiDriftGate.lean:146`
- `05_lean_formalization/PillarIV_AntiDriftGate.lean:156`
- `05_lean_formalization/PillarIV_AntiDriftGate.lean:170`

### 4. Claims in FIG_TREE_MONOGRAPH.md untraced to inventory files
- Claim V.1 (Kerr photon-capture saturation derivation): The derivation of the saturation ceiling kappa_Y from Kerr photon-capture geometry is not contained in any inventory file (monograph L186-187 acknowledges this as an open empirical observation, not a derivation).
- Black hole spin ceiling test dataset: The observational test cited in monograph L186 ("kappa occupied 6/10 vs Thorne 0/10 on accretion-grown black holes") is not present in any inventory file.
- Theorem VI.1 (Lindblad-GKSL master equation derivation): The assertion that open dissipative systems governed by Lindblad generators have steady-state coherence mu(u/gamma) is an open stub with sorries (PillarIV_AntiDriftGate.lean:146, 156) and is not established in any inventory file.
- Trinity Survey 409 observational signals (monograph L84): The dataset containing the 409 JWST/Hubble signals cited in Zenodo DOI 10.5281/zenodo.20027657 is not present in the inventory files.
- Reciprocal relation chi_Y * kappa_Y ~= ln 2 (monograph L246): Acknowledged in monograph as an open relation differing by 2.7%, with no derivation file in the inventory.

## Phase 2 — Repair Log

### Package-Level Lake Build
- **Directory**: `05_lean_formalization`
- **Command**: `lake build`
- **Exit Code**: `0`
- **Output Tail** (last 3 lines verbatim):
```text
info: RapidityEquipartition.lean:56:0: 'RapidityEquipartition.arsinh_one_eq_artanh_theta' depends on axioms: [propext, Classical.choice, Quot.sound]
info: RapidityEquipartition.lean:57:0: 'RapidityEquipartition.theta_odds_eq_silver_ratio' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (3365 jobs).
```

### Individual Lean Module Builds
| module | command | exit_code | output_tail |
|---|---|---|---|
| `AXIOMS_V2.lean` | `lake build +AXIOMS_V2` | 0 | `Build completed successfully (1936 jobs).` |
| `CartanTrialityGenerations.lean` | `lake build +CartanTrialityGenerations` | 0 | `Build completed successfully (2 jobs).` |
| `ChiralCellularDuality.lean` | `lake build +ChiralCellularDuality` | 0 | `Build completed successfully (2 jobs).` |
| `CosmologicalSector.lean` | `lake build +CosmologicalSector` | 0 | `Build completed successfully (1945 jobs).` |
| `CovariantCompletion.lean` | `lake build +CovariantCompletion` | 0 | `Build completed successfully (1945 jobs).` |
| `DeSitterExtremal.lean` | `lake build +DeSitterExtremal` | 0 | `  [apply] _hr<br>Note: This linter can be disabled with `set_option linter.unusedVariables false`<br>Build completed successfully (3004 jobs).` |
| `DualChannelDerivation.lean` | `lake build +DualChannelDerivation` | 0 | `Build completed successfully (2007 jobs).` |
| `GODActionKinematics.lean` | `lake build +GODActionKinematics` | 0 | `info: GODActionKinematics.lean:50:0: 'GODTheory.aqual_simple_mu_ratio' depends on axioms: [propext, Classical.choice, Quot.sound]<br>info: GODActionKinematics.lean:51:0: 'GODTheory.btfr_algebraic_scaling' depends on axioms: [propext, Classical.choice, Quot.sound]<br>Build completed successfully (2007 jobs).` |
| `GenerationIndex.lean` | `lake build +GenerationIndex` | 0 | `Build completed successfully (862 jobs).` |
| `Hamilgrangian.lean` | `lake build +Hamilgrangian` | 0 | `Build completed successfully (2150 jobs).` |
| `HorizonScale.lean` | `lake build +HorizonScale` | 0 | `Build completed successfully (3004 jobs).` |
| `ITActionClosure.lean` | `lake build +ITActionClosure` | 0 | `Build completed successfully (2631 jobs).` |
| `MuProjection.lean` | `lake build +MuProjection` | 0 | `  [apply] _hb<br>Note: This linter can be disabled with `set_option linter.unusedVariables false`<br>Build completed successfully (2164 jobs).` |
| `PPNLimits.lean` | `lake build +PPNLimits` | 0 | `Build completed successfully (2007 jobs).` |
| `PillarIV_AntiDriftGate.lean` | `lake build +PillarIV_AntiDriftGate` | 1 | `error: unknown module `PillarIV_AntiDriftGate`` |
| `PrintAxioms.lean` | `lake build +PrintAxioms` | 0 | ` Classical.choice,<br> Quot.sound]<br>Build completed successfully (2105 jobs).` |
| `PrintAxiomsD8.lean` | `lake build +PrintAxiomsD8` | 0 | `info: PrintAxiomsD8.lean:46:0: 'ResNova.TensorSpeed.physical_frame_tensor_speed_unity' depends on axioms: [propext, Classical.choice, Quot.sound]<br>info: PrintAxiomsD8.lean:47:0: 'ResNova.TensorSpeed.gw170817_concordance' depends on axioms: [propext, Classical.choice, Quot.sound]<br>Build completed successfully (1945 jobs).` |
| `RamanujanModularBounds.lean` | `lake build +RamanujanModularBounds` | 0 | `Build completed successfully (2 jobs).` |
| `RapidityEquipartition.lean` | `lake build +RapidityEquipartition` | 0 | `info: RapidityEquipartition.lean:56:0: 'RapidityEquipartition.arsinh_one_eq_artanh_theta' depends on axioms: [propext, Classical.choice, Quot.sound]<br>info: RapidityEquipartition.lean:57:0: 'RapidityEquipartition.theta_odds_eq_silver_ratio' depends on axioms: [propext, Classical.choice, Quot.sound]<br>Build completed successfully (3114 jobs).` |
| `RelativisticStability.lean` | `lake build +RelativisticStability` | 0 | `Build completed successfully (2007 jobs).` |
| `SOCasimirGenuine.lean` | `lake build +SOCasimirGenuine` | 0 | `Build completed successfully (3004 jobs).` |
| `SkordisZlosnikEmbedding.lean` | `lake build +SkordisZlosnikEmbedding` | 0 | `info: SkordisZlosnikEmbedding.lean:99:0: 'ResNova.SkordisZlosnik.sz_tensor_speed_luminal' depends on axioms: [propext, Classical.choice, Quot.sound]<br>info: SkordisZlosnikEmbedding.lean:100:0: 'ResNova.SkordisZlosnik.sz_weak_field_lensing' depends on axioms: [propext, Classical.choice, Quot.sound]<br>Build completed successfully (1945 jobs).` |
| `SovereignRegularity.lean` | `lake build +SovereignRegularity` | 0 | `  [apply] _hθ_high<br>Note: This linter can be disabled with `set_option linter.unusedVariables false`<br>Build completed successfully (1936 jobs).` |
| `SovereignSemiotics.lean` | `lake build +SovereignSemiotics` | 0 | `Build completed successfully (819 jobs).` |
| `SovereignSpinCeiling.lean` | `lake build +SovereignSpinCeiling` | 0 | `info: SovereignSpinCeiling.lean:34:0: 'SovereignSpinCeiling.two_theta_sub_theta_sq' depends on axioms: [propext, Classical.choice, Quot.sound]<br>info: SovereignSpinCeiling.lean:35:0: 'SovereignSpinCeiling.sovereign_spin_ceiling_eq' depends on axioms: [propext, Classical.choice, Quot.sound]<br>Build completed successfully (3004 jobs).` |
| `TensorSpeed.lean` | `lake build +TensorSpeed` | 0 | `info: TensorSpeed.lean:132:0: 'ResNova.TensorSpeed.speed_ratio_lt_one_of_pos' depends on axioms: [propext, Classical.choice, Quot.sound]<br>info: TensorSpeed.lean:133:0: 'ResNova.TensorSpeed.gw170817_deviation_of_pos' depends on axioms: [propext, Classical.choice, Quot.sound]<br>Build completed successfully (1945 jobs).` |
| `TrialityFixedSubalgebra.lean` | `lake build +TrialityFixedSubalgebra` | 0 | `warning: TrialityG2.lean:75:31: 'norm_num' tactic does nothing<br>Note: This linter can be disabled with `set_option linter.unusedTactic false`<br>Build completed successfully (1431 jobs).` |
| `TrialityG2.lean` | `lake build +TrialityG2` | 0 | `warning: TrialityG2.lean:75:31: 'norm_num' tactic does nothing<br>Note: This linter can be disabled with `set_option linter.unusedTactic false`<br>Build completed successfully (1411 jobs).` |
| `YettParadigm.lean` | `lake build +YettParadigm` | 0 | `Build completed successfully (769 jobs).` |
| `lakefile.lean` | `lake build +lakefile` | 1 | `error: unknown module `lakefile`` |

### TeX File Compile Investigations and Repairs

#### TeX 1: `01_foundational_action/PAPER_01_MU_DERIVATION_ACTION.tex`
- **Status**: Not changed (exit code 1)
- **Missing input**: `figs/e8_sigil_codex.pdf`
- **Filesystem search**: FOUND at:
  - `/home/mega/aeon-work/brain/50_Mathematical_Notation/publication_preview/figs/e8_sigil_codex.pdf`
  - `/home/mega/aeon-work/research/07_Domain_Tiers_and_Data/Datasets/research/00_CANONICAL/figs/e8_sigil_codex.pdf`
  - `/home/mega/Chyren/Chyren_Second_Brain/50_Mathematical_Notation/publication_preview/figs/e8_sigil_codex.pdf`
- **Reason not changed**: Per Task B instructions, the file was not copied or substituted, no `\includegraphics` was commented out, and draft mode was not enabled.

#### TeX 2: `01_foundational_action/PRD_Relativistic_Extension.tex`
- **Status**: Not changed (exit code 1)
- **Missing input**: `PRD_supplementary/figures/cmb_power_spectrum.pdf`
- **Filesystem search**: `NOT FOUND`
  - Note: Only a PNG file exists at `/home/mega/aeon-work/research/07_Domain_Tiers_and_Data/Datasets/research/05_REFERENCES/mega_nz_cloud_only/PRD_Relativistic_Submission/PRD_Relativistic_Submission/PRD_supplementary/figures/cmb_power_spectrum.png`.
- **Reason not changed**: Per Task B instructions, no figure was substituted, no `\includegraphics` was commented out, and draft mode was not enabled.

#### TeX 3: `01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex`
- **Status**: Fixed (compiles cleanly at exit code 0)
- **Missing input**: Missing color `gold`
- **Exact diff**:
```diff
--- a/01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex
+++ b/01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex
@@ -12,2 +12,3 @@
 \usepackage{xcolor}
+\definecolor{gold}{HTML}{E6B84C}
```

#### TeX 4: `03_observer_jwst/IO_OI_ACADEMIC.tex`
- **Status**: Fixed (compiles cleanly at exit code 0)
- **Missing input**: Missing math delimiter (`$`) due to unclosed/extraneous text in display math environment, and missing `gold` color
- **Exact diff**:
```diff
--- a/03_observer_jwst/IO_OI_ACADEMIC.tex
+++ b/03_observer_jwst/IO_OI_ACADEMIC.tex
@@ -6,2 +6,4 @@
 \usepackage{amssymb}
+\usepackage{xcolor}
+\definecolor{gold}{HTML}{E6B84C}
@@ -78,3 +80,2 @@
-\begin{equation}
-\label{eq:stiefel}
 \vspace{10pt}
@@ -83,2 +84,4 @@
 \textbf{\textsf{Vacuum Manifold Classification:}}
+\begin{equation}
+\label{eq:stiefel}
 \mathcal{M}_{\mathrm{vac}} = \frac{\mathrm{SO}(8)}{\mathrm{SO}(7)} \cong S^7, \quad \dim(\mathcal{M}_{\mathrm{vac}}) = 7
```

### Defects Found and Not Fixed
FOUND, NOT FIXED: 05_lean_formalization/PillarIV_AntiDriftGate.lean is present on disk but omitted from roots in lakefile.lean; contains 3 unproven sorry statements (lines 146, 156, 170).
FOUND, NOT FIXED: 05_lean_formalization/lakefile.lean is a package configuration script, not a declared module root; lake build +lakefile fails with exit code 1.
FOUND, NOT FIXED: 01_foundational_action/PRD_Relativistic_Extension.tex requires PRD_supplementary/figures/cmb_power_spectrum.pdf, but only a PNG format image exists on disk.
