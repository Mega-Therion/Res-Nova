# 🏛️ Verification Evidence Ledger: Findings F1–F8
**Author / Lead Investigator:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Repository (Res-Nova):** `Mega-Therion/Res-Nova`  
**Res-Nova Release:** `v1.5.0`  
**Evaluation Standard:** Sovereign Epistemic Covenant & Newton Epistemic Taxonomy (`[P]`, `[D]`, `[C]`, `[O]`)

---

## Executive Summary of Findings & Evidence Mapping

| Finding | Topic | Epistemic Status | Primary Corpus Location | Reference / Note |
|---|---|---|---|---|
| **F1** | AQUAL Weak-Field Field Equation | `[C]` Literature Baseline | `final_manuscript.tex` §2 | Bekenstein-Milgrom (1984) |
| **F2** | $\mu(x)$ Dual-Channel Derivative Identity | `[P]` (algebra) / `[O]` (closure) | `05_lean_formalization/DualChannelDerivation.lean`, `01_foundational_action/PAPER_01_NOTICE.md` | Dual-channel $\mu(x)=x/(1+x)$ `[P]`; single-channel quarantined |
| **F3** | $a_0 = cH_0/(2\pi)$ KMS Cancellation Null Result | `[O]` Horizon Normalization | `final_manuscript.tex` §3.2, `04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md` | Thermal KMS cancellation derived; $1/(2\pi)$ is open normalization |
| **F4** | Fixed Tier 0 SPARC Benchmark | `[D]` Empirical Evaluation | `02_galaxy_dynamics/PARAMETER_LEDGER.json` (Tier 0: median 9.20) | "Zero free parameters" language withdrawn as a working model class |
| **F5** | SPARC Nuisance Fits & Working $a_0$ | `[D]` Regularized Fit / Measurement | `02_galaxy_dynamics/A0_MEASUREMENT.json`, `PARAMETER_LEDGER.json` | Tier 1 ($N_{\text{par}}=374$, median 2.95); $a_0 = (1.116 \pm 0.128_{\text{stat}} \pm 0.097_{\text{syst}})\times 10^{-10}\text{ m/s}^2$ |
| **F6** | $\Omega_\Lambda = \ln 2 \approx 0.693$ Holographic / Disformal Boundary | `[O]` Conjectural Limit | Motivational Narrative Annex | Conjectured horizon boundary condition, not a derived density |
| **F7** | 17 Lean 4 Modules on Disk | `[P]` Kernel Verified / Diagnostic | `05_lean_formalization/*.lean` | `verify_all_proofs.sh` exit 0 on local gate; standard axioms only |
| **F8** | Empirical Provenance & Out-of-Sample Validation | `[D]` Cross-Validation / Bootstrap | `02_galaxy_dynamics/A0_MEASUREMENT.json` | 171 galaxies (3,375 points), bootstrap + honest CV |
| **F9** | Kerr Rapidity Equipartition & Sovereign Spin Ceiling | `[P]` (algebra) / `[O]` (dynamical action) | `06_unification_and_spin/rapidity_uniqueness_proof.py`, `two_channel_ceiling_proof.py` | Exact $\operatorname{arsinh}(1) = \ln(1+\sqrt{2}) = \operatorname{artanh}(1/\sqrt{2})$ and $\chi_s = \sqrt{\sqrt{2}-1/2} \approx 0.956145$ verified `[P]` at 100 dps |

---

## Detailed Evidence Dossier

### F1. AQUAL Weak-Field Euler-Lagrange Field Equation
* **Epistemic Classification:** `[C]` Cited Literature Baseline
* **File Paths:**
  - [`final_manuscript.tex`](final_manuscript.tex)
  - [`01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.tex`](01_foundational_action/PAPER_09_ALGEBRAIC_EQUIVALENCE_OF_TAU_TENSION_AND_AQUAL_SIMPLE_MU.tex)
* **Verbatim Mathematical Excerpt:**
```latex
\begin{equation}
\label{eq:aqual_field}
\nabla \cdot \left[ \mu\left(\frac{|\nabla\Phi|}{a_0}\right) \nabla\Phi \right] = 4\pi G \rho_{\text{bar}},
\end{equation}
where $\rho_{\text{bar}}$ is the baryonic mass density, $a_0$ is the characteristic acceleration scale, 
and $\mu(x)$ is an interpolation function satisfying $\mu(x) \to 1$ for $x \gg 1$ and $\mu(x) \to x$ for $x \ll 1$.

Under spherical or planar symmetry, this reduces to:
\begin{equation}
g \cdot \mu\left(\frac{g}{a_0}\right) = g_{\text{bar}}.
\end{equation}
```

---

### F2. $\mu(x)$ Dual-Channel Algebraic Identity and Single-Channel Quarantine
* **Epistemic Classification:** `[P]` (Dual-Channel Derivative Identity) / `[O]` (Physical Boundary Closure)
* **File Paths:**
  - [`05_lean_formalization/DualChannelDerivation.lean`](05_lean_formalization/DualChannelDerivation.lean)
  - [`05_lean_formalization/GODActionKinematics.lean`](05_lean_formalization/GODActionKinematics.lean)
  - [`01_foundational_action/PAPER_01_NOTICE.md`](01_foundational_action/PAPER_01_NOTICE.md)
  - [`final_manuscript.tex`](final_manuscript.tex)
* **Verified Theorems in `DualChannelDerivation.lean`:**
  - `dual_channel_flux_algebra`
  - `mu_derived_inversion`
  - `mu_derived_deep_mond_upper_bound`
  - `mu_derived_newtonian_bound`
* **Status:** The dual-channel algebraic identity is verified `[P]` in Lean 4. Historical single-channel $\operatorname{arcsinh}$ Lagrangian yields inverted physical limits and is quarantined as correspondence-false (`01_foundational_action/PAPER_01_NOTICE.md`). Uniqueness of the action in nature remains open `[O]`.

---

### F3. $a_0 = cH_0 / (2\pi)$ Horizon Thermodynamics KMS Cancellation Null Result
* **Epistemic Classification:** `[O]` Open Problem / Negative Result Disclosed
* **File Paths:**
  - [`final_manuscript.tex`](final_manuscript.tex) §3.2
  - [`04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md`](04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md)
* **Verbatim Mathematical Excerpt:**
```latex
Consider the Gibbons--Hawking temperature of a de Sitter cosmological horizon:
\begin{equation}
T_{\text{GH}} = \frac{\hbar H_0}{2\pi k_B},
\end{equation}
and the Unruh temperature associated with an observer experiencing constant acceleration $a$:
\begin{equation}
T_U = \frac{\hbar a}{2\pi c k_B}.
\end{equation}
Equating horizon thermal states ($T_U = T_{\text{GH}}$) yields:
\begin{equation}
\frac{\hbar a}{2\pi c k_B} = \frac{\hbar H_0}{2\pi k_B} \implies a = c H_0.
\end{equation}
The universal KMS factor $2\pi$ cancels identically. Therefore, thermal equilibrium derives $a = cH_0$, 
not $a_0 = \frac{cH_0}{2\pi}$. The additional $1/(2\pi)$ divisor is an open boundary normalization [O].
```

---

### F4. Fixed-Prescription SPARC Benchmarks
* **Epistemic Classification:** `[D]` Direct Empirical Computation
* **File Paths:**
  - [`02_galaxy_dynamics/PARAMETER_LEDGER.json`](02_galaxy_dynamics/PARAMETER_LEDGER.json)
  - [`02_galaxy_dynamics/sparc_reproduce.py`](02_galaxy_dynamics/sparc_reproduce.py)
* **Summary:**
  - Zero-free-parameter language is withdrawn as a working model class.
  - Tier 0 fixed-prescription benchmark ($a_0 = 1.042\times 10^{-10}\text{ m/s}^2$ from horizon formula) yields median $\chi^2_{\text{data}}/N_g = 9.20$ across 171 galaxies (vs MOND $1.2\times 10^{-10}$ median $11.35$).
  - Outperforms baryons-only controls, but remains a poor absolute fit without accounting for observational nuisances.

---

### F5. Matched Nuisance Fits and Working $a_0$ Measurement
* **Epistemic Classification:** `[D]` Empirical Evaluation / Measurement
* **File Paths:**
  - [`02_galaxy_dynamics/A0_MEASUREMENT.json`](02_galaxy_dynamics/A0_MEASUREMENT.json)
  - [`02_galaxy_dynamics/PARAMETER_LEDGER.json`](02_galaxy_dynamics/PARAMETER_LEDGER.json)
  - [`02_galaxy_dynamics/NFW_CONSTRAINED.json`](02_galaxy_dynamics/NFW_CONSTRAINED.json)
* **Summary:**
  - Working measurement: $a_0 = (1.116 \pm 0.128_{\text{stat}} \pm 0.097_{\text{syst}})\times 10^{-10}\text{ m/s}^2$ (total 14.4% error) across 171 galaxies (3,375 points).
  - Tension with horizon $cH_0/(2\pi)$: $0.46\sigma$; tension with MOND $1.2\times 10^{-10}$: $0.52\sigma$.
  - Tier 1 matched nuisance GOD fit: 374 parameters (171 galaxies), median $\chi^2_{\text{data}}/N_g = 2.95$.
  - NFW with cosmological concentration prior: 716 parameters (342 extra knobs vs GOD), median $\chi^2_{\text{data}}/N_g = 5.62$.

---

### F6. $\Omega_\Lambda = \ln 2 \approx 0.693$ Holographic Boundary Conjecture
* **Epistemic Classification:** `[O]` Conjectural Limit / Horizon Hypothesis
* **Summary:**
  - Homogeneous FLRW decoupling of the scalar ($\hat\nabla_\mu\phi=0 \implies \rho_\phi=0$) is proved `[P]` (`CovariantCompletion.lean`), falsifying dynamical-fluid interpretations.
  - The entropy bound conjecture $\Omega_\Lambda = \ln 2$ is quarantined to open problem O3 (`OPEN_PROBLEMS_AND_TESTS.md`).

---

### F7. Lean 4 Formal Verification Suite (17 Tracked Modules, Standard Foundational Axioms)
* **Epistemic Classification:** `[P]` Proved / Diagnostic / Assumption
* **Target Directory:** [`05_lean_formalization/`](05_lean_formalization/)
* **Status:** O6 — walked once in a clean worktree at 07185a6 (lake exe cache get + 17/17 PASS, VERIFICATION_RUN_007). Not yet demonstrated on a cold machine with empty host cache, and not yet a CI release gate.
* **Kernel Axiom Footprint:** Exclusively standard foundational axioms `[propext, Classical.choice, Quot.sound]`. (Documented structural/typeclass vacuity in `YettParadigm.lean` and `SovereignRegularity.lean` recorded in `THEORY_ASSUMPTION_AUDIT.md`).

| Lean 4 File | Headline Theorems / Scope Verified on Disk | Axiom Footprint | Role / Status |
|---|---|---|---|
| [`AXIOMS_V2.lean`](05_lean_formalization/AXIOMS_V2.lean) | `derived_simple_mu_bounds`, `deep_mond_baryonic_scaling` | `[propext, Classical.choice, Quot.sound]` | **ASSUMPTIONS `[O]`** (Typeclass declarations) |
| [`CosmologicalSector.lean`](05_lean_formalization/CosmologicalSector.lean) | `log_two_pos`, `log_two_lt_one`, `matter_density_bounds`, `spatial_flatness_sum` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`CovariantCompletion.lean`](05_lean_formalization/CovariantCompletion.lean) | `raqual_superluminal_obstruction`, `disformal_gamma_ppn_unity`, `preferred_frame_parameters_zero`, `no_dynamical_dark_energy_density` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`DeSitterExtremal.lean`](05_lean_formalization/DeSitterExtremal.lean) | `desitter_lapse_horizon`, `expr_cH_over_2pi_pos`, `desitter_flat_limit` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`DualChannelDerivation.lean`](05_lean_formalization/DualChannelDerivation.lean) | `dual_channel_flux_algebra`, `mu_derived_inversion`, `mu_derived_deep_mond_upper_bound`, `mu_derived_newtonian_bound` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`GODActionKinematics.lean`](05_lean_formalization/GODActionKinematics.lean) | `dual_channel_poly_identity`, `aqual_simple_mu_ratio`, `btfr_algebraic_scaling` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`ITActionClosure.lean`](05_lean_formalization/ITActionClosure.lean) | `tauLaw_eq_simple_mu_poly`, `btfr_deep_mond`, `flat_rotation_curve_n2` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`MuProjection.lean`](05_lean_formalization/MuProjection.lean) | `mu_simple_eq_cos`, `quadratic_law_root_unique`, `powerLaw_solves_dilaton_eom`, `powerLaw_iterated_deriv`, `exp_profile_fails_cubic` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`PPNLimits.lean`](05_lean_formalization/PPNLimits.lean) | `solar_system_precision_bound`, `cassini_radar_delay_satisfied` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`PrintAxioms.lean`](05_lean_formalization/PrintAxioms.lean) | Axiom reflection helper for `CovariantCompletion` | `[propext, Classical.choice, Quot.sound]` | **DIAGNOSTIC** (No proof content) |
| [`PrintAxiomsD8.lean`](05_lean_formalization/PrintAxiomsD8.lean) | `maxwellian_c13_vanishes`, `gw170817_concordance` | `[propext, Classical.choice, Quot.sound]` | **DIAGNOSTIC** (TensorSpeed reflection) |
| [`RelativisticStability.lean`](05_lean_formalization/RelativisticStability.lean) | `first_derivative_pos`, `second_derivative_pos`, `ghost_free_convexity` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`SOCasimirGenuine.lean`](05_lean_formalization/SOCasimirGenuine.lean) | `casimir_defining_rep`, `casimir_scalar_eq` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`SkordisZlosnikEmbedding.lean`](05_lean_formalization/SkordisZlosnikEmbedding.lean) | `sz_aqual_reduction`, `sz_tensor_speed_luminal`, `sz_weak_field_lensing` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`SovereignRegularity.lean`](05_lean_formalization/SovereignRegularity.lean) | `sovereign_regularity_theorem`, `bkm_no_blowup` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** (Assumptions documented) |
| [`TensorSpeed.lean`](05_lean_formalization/TensorSpeed.lean) | `maxwellian_c13_vanishes`, `foster_jacobson_alpha_1_eval`, `gw170817_deviation_of_pos` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`YettParadigm.lean`](05_lean_formalization/YettParadigm.lean) | `ramanujan_yett_spectral_gap_pos`, `chiral_phase_stable` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** (Assumptions documented) |

---

### F8. Empirical Provenance & Out-of-Sample Validation
* **Epistemic Classification:** `[D]` Direct Computational Benchmark
* **File Paths:**
  - [`02_galaxy_dynamics/A0_MEASUREMENT.json`](02_galaxy_dynamics/A0_MEASUREMENT.json)
  - [`02_galaxy_dynamics/A0_ESTIMATE.json`](02_galaxy_dynamics/A0_ESTIMATE.json)
* **Methodology:** 171 SPARC galaxies (3,375 kinematic data points) evaluated via bootstrap over galaxies and honest 5-fold cross-validation with per-fold $a_0$ retraining.

---

### F9. Kerr Rapidity Equipartition & Sovereign Spin Ceiling
* **Epistemic Classification:** `[P]` Proved (Algebraic Uniqueness) / `[O]` Open Problem (Dynamical Action Closure)
* **File Paths:**
  - [`06_unification_and_spin/rapidity_uniqueness_proof.py`](06_unification_and_spin/rapidity_uniqueness_proof.py)
  - [`06_unification_and_spin/two_channel_ceiling_proof.py`](06_unification_and_spin/two_channel_ceiling_proof.py)
  - [`06_unification_and_spin/arctanh_derivation_chain.py`](06_unification_and_spin/arctanh_derivation_chain.py)
  - [`06_unification_and_spin/kerr_toroidal_bounce.py`](06_unification_and_spin/kerr_toroidal_bounce.py)
  - [`06_unification_and_spin/thorne_equilibrium_fast.py`](06_unification_and_spin/thorne_equilibrium_fast.py)
* **Verified Algebraic Theorems:**
  - **Rapidity Identity:** $\operatorname{arsinh}(1) = \ln(1+\sqrt{2}) = \operatorname{artanh}(1/\sqrt{2})$ verified symbolically and to 100 decimal digits ($< 10^{-70}$ residual).
  - **Silver Ratio Odds:** $\frac{\theta}{1-\theta} = 1+\sqrt{2} = \delta_S$ at $\theta = 1/\sqrt{2}$.
  - **Two-Channel Ceiling:** $\chi_s = \sqrt{2\theta - \theta^2} = \sqrt{\sqrt{2} - 1/2} \approx 0.956145157584922$.
  - **Gate Arithmetic Mean:** $\theta_{\text{gate}} = \frac{1}{2}(\ln 2 + 1/\sqrt{2}) \approx 0.700127 \approx 0.700$.
* **Physics Scope & Boundaries:**
  - Proves the exact mathematical uniqueness of the rapidity equipartition state and the two-channel union formula.
  - Demonstrates that standard Thorne (1974) thin-disk photon capture reaches equilibrium at $a^* \approx 0.998$, whereas stabilizing spin at $\chi_s \approx 0.956$ requires the topological counter-torque $\tau_{\text{top}}$ from the inner Cauchy horizon quantum bounce.

