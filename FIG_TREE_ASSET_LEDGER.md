# FIG TREE — Asset Ledger

## 01_foundational_action

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `01_foundational_action/PAPER_01_MU_DERIVATION_ACTION.tex` | 386 | tex | L119: "First-Principles Action Derivation of the Universal Galactic Interpolation Function $\mu(x)$ from Conformal Scalar-Tensor Dynamics" | I | yes | 1 | `tt10.pfb></usr/share/texmf/fonts/type1/public/lm/lmtt8.pfb> ; Output written on PAPER_01_MU_DERIVATION_ACTION.pdf (8 pages, 415892 bytes). ; Transcript written on PAPER_01_MU_DERIVATION_ACTION.log.` | ! Package pdftex.def Error: File `figs/e8_sigil_codex.pdf' not found: using dra |
| `01_foundational_action/PAPER_01_NOTICE.md` | 13 | markdown | L3: "Paper 01 is an exploratory, work-in-progress manuscript reflecting early development of the conformal scalar-tensor framework." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.pdf` | 2946 | other | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.tex` | 834 | tex | L22: "\title{Algebraic Equivalence of Horizon-Tension Action and AQUAL Simple-$\mu$ Formulation}" | I | yes | 0 | `E_MU.pdf (19 pages, 564111 bytes). ; Transcript written on PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_S ; IMPLE_MU.log.` | none |
| `01_foundational_action/PRD_Relativistic_Extension.pdf` | 1876 | other | none | I | no (non-executable file) | UNKNOWN | `none` | none |
| `01_foundational_action/PRD_Relativistic_Extension.tex` | 308 | tex | L23: "\title{Relativistic Extension of Information-Theoretic Horizon Gravity: Action Principle, Gravitational Slip, and Cosmological Perturbations}" | I | yes | 1 | `-dist/fonts/type1/public/amsfonts/symbols/msbm10.pfb> ; Output written on PRD_Relativistic_Extension.pdf (6 pages, 329552 bytes). ; Transcript written on PRD_Relativistic_Extension.log.` | ! Package pdftex.def Error: File `PRD_supplementary/figures/cmb_power_spectrum. |
| `01_foundational_action/Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex` | 282 | tex | L34: "\title{Geometrically Ordered Dynamics and Information Tension: A Relativistic Framework for Emergent Acceleration}" | I | yes | 1 | `on.pdf (3 pages, 361421 bytes). ; Transcript written on Res_Nova_Geometrically_Ordered_Dynamics_and_Information_T ; ension.log.` | ! Package xcolor Error: Undefined color `gold'. |

## 02_galaxy_dynamics

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `02_galaxy_dynamics/A0_ESTIMATE.json` | 49 | data | L2: ""estimate_mode": "profile_likelihood"" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/A0_MEASUREMENT.json` | 56 | data | L2: ""a0_central": 1.1319230910006764e-10" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/HALO_CONSPIRACY.json` | 41 | data | L3: ""mond_sigma": 0.11181285226490333" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/NFW_CONSTRAINED.json` | 15 | data | L3: ""dof": 716" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/PAPER_02_ZERO_PARAMETER_ROTATION_CURVE_FITTING_SPARC_175_ANALYSIS.tex` | 50 | tex | L21: "\title{Zero-Parameter Rotation Curve Fitting: Analysis of 175 Galaxies from the SPARC Database under Geometrically Ordered Dynamics}" | I | yes | 0 | `YSIS.pdf (1 page, 186093 bytes). ; Transcript written on PAPER_02_ZERO_PARAMETER_ROTATION_CURVE_FITTING_SPARC_175_ ; ANALYSIS.log.` | none |
| `02_galaxy_dynamics/PARAMETER_LEDGER.json` | 54 | data | L4: ""n_galaxies": 175" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/SPARC_DATA.md` | 47 | markdown | L3: "SPARC (Spitzer Photometry and Accurate Rotation Curves) Database" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/SPARC_PARAMETER_BUDGET.md` | 43 | markdown | L3: "Accounting of free vs fixed parameters across all SPARC-175 rotation curve fits." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/a0_estimate.py` | 256 | python | L7: "Fast a0 estimation from SPARC data using median RAR residual minimization." | I | yes | TIMEOUT | `timed out after 120s` | sparc_data |
| `02_galaxy_dynamics/a0_measure.py` | 320 | python | L7: "Definitive a0 measurement with MCMC error budget over 175 SPARC galaxies." | I | yes | TIMEOUT | `baseline fit (real D/i priors, inclination floated) ... ;   a0 = 1.1319e-10  stat +/- 1.116e-11 ;   distance_scale_-5%     a0=1.2148e-10  shift +7.3%` | sparc_data |
| `02_galaxy_dynamics/fetch_sparc.sh` | 59 | other | L5: "Download and extract SPARC rotation curve data from CWRU." | I | no (network download script for external data archive) | UNKNOWN | `none` | CWRU SPARC archive |
| `02_galaxy_dynamics/halo_conspiracy.py` | 160 | python | L7: "Quantify the disk-halo conspiracy: scatter in (V_obs / V_bar) vs MOND prediction." | I | yes | TIMEOUT | `timed out after 120s` | sparc_data |
| `02_galaxy_dynamics/nfw_constrained.py` | 74 | python | L7: "Constrained NFW fits: test whether Lambda-CDM NFW profiles can match SPARC without MOND acceleration scale." | I | yes | TIMEOUT | `timed out after 120s` | sparc_data |
| `02_galaxy_dynamics/parameter_ledger.py` | 240 | python | L6: "Audit and compile parameter count across all models applied to SPARC-175." | I | yes | 0 | `NFW   median=   1.92  free= 716  <1: 53  agg=4.58 ;  ; wrote PARAMETER_LEDGER.json` | sparc_data |
| `02_galaxy_dynamics/phase8_btfr_slip_scales.json` | 181 | data | L2: ""btfr_slope": 4.0" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `02_galaxy_dynamics/phase8_btfr_slip_scales.py` | 512 | python | L7: "Reconcile Baryonic Tully-Fisher Relation (BTFR) slope and normalization under gravitational slip." | I | yes | 0 | `"a0_eta_roles": "[reconciled]" ; } ; Wrote /home/mega/Res-Nova/02_galaxy_dynamics/phase8_btfr_slip_scales.json` | none |
| `02_galaxy_dynamics/ppn_solar_system.py` | 81 | python | L6: "PPN parameter evaluation: Solar System constraints (/gamma_PPN - 1/ < 2.3e-5) under dual-channel action." | I | yes | 0 | `The dual-channel μ does NOT affect PPN parameters. ; PPN parameters depend on the covariant completion (D7/D9). ; D3 is reduced to a dependency on D7.` | none |
| `02_galaxy_dynamics/sparc_cross_validation.py` | 187 | python | L8: "5-fold out-of-sample split-sample testing of zero-parameter rotation curve fits on SPARC-175." | I | yes | 0 | `Out-of-Sample 5-Fold:   Median chi2/N = 14.68, Aggregate chi2/N = 110.18 ;  ; Report written to: /home/mega/Res-Nova/RUN_002/02_sparc/SPARC_CROSS_VALIDATION_REPORT.json` | sparc_data |
| `02_galaxy_dynamics/sparc_derived_closure.py` | 269 | python | L8: "Run full SPARC-175 sample through derived mu closure and write run manifest." | I | yes | 0 | `Saved /home/mega/Res-Nova/RUN_003/02_sparc/SPARC_DERIVED_RUN_MANIFEST.json ; Generating diagnostic Figures A, B, C... ; Figures saved completely to /home/mega/Res-Nova/RUN_003/figures` | sparc_data |
| `02_galaxy_dynamics/sparc_derived_cross_validation.py` | 165 | python | L8: "Split-sample testing of derived mu formulation across galaxy morphological types." | I | yes | 0 | `"total_out_points": 3391 ;   } ; }` | sparc_data |
| `02_galaxy_dynamics/sparc_derived_mu_benchmark.py` | 204 | python | L8: "Benchmark derived mu against standard empirical interpolation functions on SPARC-175." | I | yes | 0 | `"aggregate_chi2_dof": 105.3882312991154 ;   } ; }` | sparc_data |
| `02_galaxy_dynamics/sparc_paths.py` | 110 | python | none | I | yes | 0 | `none` | sparc_data |
| `02_galaxy_dynamics/sparc_reproduce.py` | 257 | python | L7: "Reproduce SPARC-175 rotation curve fits under Geometrically Ordered Dynamics." | I | yes | 0 | `Wrote /home/mega/Res-Nova/02_galaxy_dynamics/SPARC_175_GOD_fits.csv ; Wrote /home/mega/Res-Nova/02_galaxy_dynamics/SPARC_175_summary.json` | sparc_data |

## 03_observer_jwst

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `03_observer_jwst/A0_OF_Z_REPORT.json` | 48 | data | L4: ""h_const_favoured": true" | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/IO_OI_ACADEMIC.tex` | 388 | tex | L24: "\title{Inside-Out and Outside-In: Holographic Duality of the Cosmic Acceleration Scale}" | II | yes | 1 | `texmf-dist/fonts/type1/public/amsfonts/symbols/msbm10.pfb> ; Output written on IO_OI_ACADEMIC.pdf (6 pages, 360043 bytes). ; Transcript written on IO_OI_ACADEMIC.log.` | ! Missing $ inserted. |
| `03_observer_jwst/IO_OI_UNIFIED_TRANSMISSION_MONOGRAPH.tex` | 1062 | tex | L70: "\title{The IO/OI Transmission: Unified Holographic Geometry and Galactic Acceleration}" | II | yes | 0 | `Output written on IO_OI_UNIFIED_TRANSMISSION_MONOGRAPH.pdf (18 pages, 756118 by ; tes). ; Transcript written on IO_OI_UNIFIED_TRANSMISSION_MONOGRAPH.log.` | none |
| `03_observer_jwst/JWST_RECALIBRATION_LEDGER.md` | 7 | markdown | L3: "Systematic ledger of JWST high-redshift galaxy mass recalibration." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/PREREG_A0_OF_Z.md` | 74 | markdown | L4: "Pre-registration of the redshift evolution test for a0(z)." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/PREREG_A0_OF_Z_EXPANSION.md` | 130 | markdown | L3: "Expanded pre-registration protocol incorporating high-z JWST rotation curves." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/Trinity_2_0_Methods_Note.md` | 34 | markdown | L3: "Methods note on Trinity 2.0 calibration and dark-matter halo growth constraints." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `03_observer_jwst/a0_of_z.py` | 259 | python | L7: "Statistical test of a0(z) redshift scaling: H(z) vs constant H0." | I | yes | 0 | `Delta chi2 (H_const - H_horizon) = -35.115 ; Significance: 5.93 sigma ; Verdict: H_const favoured over H_horizon at >= 3 sigma (delta_chi2 <= -9.0)` | none |
| `03_observer_jwst/gate2_inference.py` | 509 | python | L7: "Gate-2 statistical inference engine for high-redshift galaxy kinematics." | I | yes | 0 | `--self-test  exercise the machinery on a declared synthetic control ;  ; This module produces no result on its own. It is inference machinery for a Gate-1-compliant dataset.` | none |

## 04_cosmology

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md` | 22 | markdown | L4: "Reconciliation of a0 horizon derivation with cosmological parameters (Omega_m, Omega_Lambda, H0)." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `04_cosmology/COSMOLOGY_EQUATION_CHAIN.md` | 10 | markdown | L4: "Complete equation derivation chain connecting horizon action to linear perturbation growth." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `04_cosmology/TARGET_O1_A0_HORIZON_DERIVATION.md` | 82 | markdown | L14: "Derivation of a0 = cH0/(2*pi) from cosmological horizon information entropy." | I | no (non-executable file) | UNKNOWN | `none` | none |
| `04_cosmology/growth_factor_computation.py` | 90 | python | L7: "Linear perturbation growth factor D(z) computation comparing standard LCDM with MOND enhancement." | I | yes | 0 | `→ A 2x MOND enhancement produces ~76x excess structure growth ; → This is the root cause of the νHDM structure overproduction (Russell et al. 2026)` | scipy, numpy |

## 05_lean_formalization

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `05_lean_formalization/ADJACENT_MODULES.txt` | 35 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/AXIOMS_V2.lean` | 89 | lean | L13: "axiom a0_definition : a0 = c * H0 / (2 * Real.pi)" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/CartanTrialityGenerations.lean` | 61 | lean | L26: "theorem generation_count_eq_three : Fintype.card Generation = 3" | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/ChiralCellularDuality.lean` | 26 | lean | L8: "theorem chiral_cellular_duality (chi : ℝ) (hchi : 0 < chi) : chi + 1/chi ≥ 2" | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/CosmologicalSector.lean` | 56 | lean | L14: "theorem background_flrw_conservation (H rho p : ℝ) : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/CovariantCompletion.lean` | 121 | lean | L14: "theorem covariant_action_diffeo_invariant : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/DeSitterExtremal.lean` | 80 | lean | L15: "theorem desitter_extremal_surface_area : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/DualChannelDerivation.lean` | 69 | lean | L14: "theorem dual_channel_mu_interpolation (x : ℝ) (hx : 0 < x) : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/GODActionKinematics.lean` | 53 | lean | L12: "theorem god_aqual_equivalence : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/GenerationIndex.lean` | 58 | lean | L12: "theorem z3_orbifold_three_generations : True" | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/Hamilgrangian.lean` | 288 | lean | L14: "theorem hamilgrangian_legendre_duality : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/HorizonScale.lean` | 115 | lean | L18: "theorem kms_two_pi_cancellation (T : ℝ) (hT : 0 < T) : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/ITActionClosure.lean` | 142 | lean | L14: "theorem it_action_closure_identity : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/MuProjection.lean` | 187 | lean | L16: "theorem mu_limits_zero_infinity (x : ℝ) : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PPNLimits.lean` | 61 | lean | L12: "theorem ppn_gamma_unity : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PillarIV_AntiDriftGate.lean` | 177 | lean | L112: "theorem antiDrift_gate {u gamma : ℝ} (hg : 0 < gamma) (hu : 0 ≤ u) : chiFloor ≤ mu (u / gamma) ↔ gamma ≤ u" | IV | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PrintAxioms.lean` | 24 | lean | none | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/PrintAxiomsD8.lean` | 51 | lean | L9: "def c_T_sq (c13 : ℝ) : ℝ := 1 / (1 - c13)" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/REPRODUCE.md` | 77 | markdown | L3: "Reproduction guide for formal test suite suite." | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/RamanujanModularBounds.lean` | 19 | lean | L9: "theorem ramanujan_ground_state_stability : True" | IV | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/RapidityEquipartition.lean` | 59 | lean | L21: "theorem arsinh_one_eq_log_one_add_sqrt_two : Real.arsinh 1 = Real.log (1 + Real.sqrt 2)" | III | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/RelativisticStability.lean` | 60 | lean | L12: "theorem ghost_free_hamiltonian_bounded : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SOCasimirGenuine.lean` | 123 | lean | L12: "theorem so_casimir_defining_rep (N : ℕ) : True" | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SkordisZlosnikEmbedding.lean` | 104 | lean | L16: "theorem rmond_parent_membership : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SovereignRegularity.lean` | 221 | lean | L28: "theorem navier_stokes_adcc_regularity : True" | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SovereignSemiotics.lean` | 86 | lean | L12: "theorem distinction_geometry_triality : True" | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/SovereignSpinCeiling.lean` | 37 | lean | L10: "theorem spin_ceiling_algebraic_bound : True" | III | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/TensorSpeed.lean` | 137 | lean | L18: "theorem tensor_propagation_speed_luminal : True" | I | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/TrialityFixedSubalgebra.lean` | 101 | lean | L14: "theorem g2_fixed_under_triality : True" | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/TrialityG2.lean` | 92 | lean | L14: "theorem g2_automorphism_closure : True" | II | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/ENVIRONMENT.txt` | 7 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/EXIT_CODE.txt` | 1 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/MANIFEST.sha256` | 6 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/README.md` | 42 | markdown | L3: "Formal test suite witness receipt from 2026-08-30." | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/RESULTS.json` | 35 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/SOURCES.sha256` | 32 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-08-30T05-30-32Z/TRANSCRIPT.txt` | 137 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/ENVIRONMENT.txt` | 7 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/EXIT_CODE.txt` | 1 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/MANIFEST.sha256` | 6 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/README.md` | 42 | markdown | L3: "Formal test suite witness receipt from 2026-09-01." | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/RESULTS.json` | 35 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/SOURCES.sha256` | 32 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/WITNESS/2026-09-01T03-21-41Z/TRANSCRIPT.txt` | 138 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/YettParadigm.lean` | 72 | lean | L24: "theorem ramanujan_yett_spectral_gap_pos (sys : RamanujanYettSystem) : 0 < sys.spectral_gap" | IV | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/check_manuscript_inventory.py` | 168 | python | L12: "Check on-disk Lean modules against manuscript targets." | unassigned | yes | 1 | `inventory: 19 module(s) on disk ; RESULT: FAIL` | none |
| `05_lean_formalization/emit_witness.sh` | 180 | other | L2: "Emit a dated, self-hashing witness for a run of run_all_theorems_gate" | unassigned | no (witness emission script requiring Mathlib build) | UNKNOWN | `none` | Mathlib |
| `05_lean_formalization/lake-manifest.json` | 116 | data | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/lakefile.lean` | 65 | lean | L5: "package «ResNovaFormal»" | unassigned | yes | MISSING_INPUT | `Mathlib not present. Run: lake exe cache get` | Mathlib (commit 5eec30bc56ed5a23be2e27c544a949ba0bceddeb) |
| `05_lean_formalization/lean-toolchain` | 1 | other | none | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `05_lean_formalization/verify_all_proofs.sh` | 162 | other | L2: "Res-Nova formal derivation suite — one-command test suite." | unassigned | yes | 2 | `[gate] TARGETS == lakefile roots (28 modules) ; Mathlib not present. Run: lake exe cache get ; (A fresh-clone fetch has not been walked; see open problem O6.)` | Mathlib |

## 06_unification_and_spin

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `06_unification_and_spin/README.md` | 62 | markdown | L3: "Unification algebra, E8 roots, and Kerr spin ceiling derivations." | II | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/arctanh_derivation_chain.py` | 432 | python | L8: "Derive arctanh spin saturation chain and silver ratio relations." | III | yes | 0 | `Silver ratio δ_S = θ/(1−θ) = 1+√2 = 2.4142135624 ;  ; Results written to: /home/mega/Res-Nova/06_unification_and_spin/arctanh_derivation_chain_results.json` | none |
| `06_unification_and_spin/arctanh_derivation_chain_results.json` | 56 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/e8_algebraic_sweep.py` | 268 | python | L8: "Sweep E8 root lattice projections and balanced ternary/quinary alphabets." | II | yes | 0 | `Balanced ternary: 128 spinor roots use {±1}^8 (even parity) ;                   112 coordinate roots use {±2, 0}^8 ;                   Full E8 alphabet = balanced quinary {-2,-1,0,+1,+2}` | none |
| `06_unification_and_spin/e8_algebraic_sweep_results.json` | 294 | data | none | II | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/kerr_toroidal_bounce.py` | 129 | python | L8: "Kerr metric equatorial geodesic analysis and photon capture boundaries." | III | yes | 0 | `"r_plus": "1.292893218813452475599155637895150960715" ;   } ; }` | mpmath |
| `06_unification_and_spin/kerr_toroidal_bounce_results.json` | 76 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/rapidity_uniqueness_proof.py` | 97 | python | L8: "Evaluate algebraic uniqueness of rapidity parameterization for spin ceiling." | III | yes | 0 | `}, ;   "physical_selection_status": "NOT DERIVED" ; }` | mpmath |
| `06_unification_and_spin/rapidity_uniqueness_results.json` | 43 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/so3_haar_derivation.py` | 611 | python | L8: "Compute SO(3) Haar measure projection on Stiefel manifold V_5,2." | II | yes | 0 | `vs 0.9539:       Δ = 0.009889 ;  ; Results written to: /home/mega/Res-Nova/06_unification_and_spin/so3_haar_derivation_results.json` | scipy, numpy |
| `06_unification_and_spin/so3_haar_derivation_results.json` | 482 | data | none | II | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/thorne_equilibrium_fast.py` | 337 | python | L8: "Numerical evaluation of Thorne accretion-torque spin equilibrium." | III | yes | 0 | `arcsinh(1) = 0.881374 ;  ; Results written to: /home/mega/Res-Nova/06_unification_and_spin/thorne_equilibrium_results.json` | scipy, numpy |
| `06_unification_and_spin/thorne_equilibrium_results.json` | 381 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |
| `06_unification_and_spin/two_channel_ceiling_proof.py` | 99 | python | L8: "Two-channel algebraic ceiling derivation for rotating black hole horizon." | III | yes | 0 | `}, ;   "physical_spin_ceiling_status": "NOT DERIVED" ; }` | mpmath |
| `06_unification_and_spin/two_channel_ceiling_results.json` | 46 | data | none | III | no (non-executable file) | UNKNOWN | `none` | none |

## Res-Nova root

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `FIG_TREE_MONOGRAPH.md` | 336 | markdown | L16: "The Fundamental Information Gravity (FIG) Tree Monograph" | unassigned | no (non-executable file) | UNKNOWN | `none` | none |
| `FIG_TREE_ARCHITECTURE_MAP.md` | 126 | markdown | L3: "Structural Blueprint: Root, Trunk, Branch, and Fruit Layers of the FIG Tree" | unassigned | no (non-executable file) | UNKNOWN | `none` | none |

## 4Leibniz/Leibniz

| path | lines | kind | claims | pillar | executes | exit_code | output_tail | depends_on |
|---|---|---|---|---|---|---|---|---|
| `4Leibniz/Leibniz/Calculemus.lean` | 42 | lean | L13: "theorem calculemus_foundation : True" | unassigned | yes | 0 | `Build completed finished (7 jobs).` | none |
| `4Leibniz/Leibniz/Characteristica.lean` | 37 | lean | L17: "def a0_characteristica (c H0 : Nat) : Nat := c * H0 / 6" | I | yes | 0 | `Build completed finished (2 jobs).` | none |
| `4Leibniz/Leibniz/Harmonia.lean` | 35 | lean | L19: "def harmonia_stabilis (u gamma : Nat) : Prop := gamma <= u" | IV | yes | 0 | `Build completed finished (3 jobs).` | none |
| `4Leibniz/Leibniz/LexContinuitatis.lean` | 38 | lean | L14: "def spin_ceiling_continuous (kappa : Nat) : Prop := kappa <= 954" | III | yes | 0 | `Build completed finished (2 jobs).` | none |
| `4Leibniz/Leibniz/SpatiumRelativum.lean` | 39 | lean | L16: "def spatium_relativum_relation : Prop := True" | I | yes | 0 | `Build completed finished (3 jobs).` | none |
| `4Leibniz/Leibniz/VisViva.lean` | 31 | lean | L15: "def vis_viva_kinetic_energy (m v : Nat) : Nat := m * v^2 / 2" | I | yes | 0 | `Build completed finished (2 jobs).` | none |

## Gaps

### 1. Pillars with no executable asset backing
- None. Every pillar (I, II, III, IV) has at least one executable asset (`.py`, `.lean`, or `.tex`) backing it in the inventory.

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
