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
| **F2** | $\mu(x)$ Dual-Channel vs Single-Channel Closure | `[P]` (algebra) / `[O]` (closure) | `05_lean_formalization/DualChannelDerivation.lean`, `01_foundational_action/PAPER_01_NOTICE.md` | Dual-channel $\mu(x)=x/(1+x)$ `[P]`; single-channel quarantined |
| **F3** | $a_0 = cH_0/(2\pi)$ KMS Cancellation Null Result | `[O]` Horizon Normalization | `final_manuscript.tex` §3.2, `04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md` | Thermal KMS cancellation derived; $1/(2\pi)$ is open normalization |
| **F4** | Fixed Tier 0 SPARC Benchmark | `[D]` Empirical Evaluation | `02_galaxy_dynamics/PARAMETER_LEDGER.json` (Tier 0: median 9.20) | "Zero free parameters" language withdrawn as a working model class |
| **F5** | SPARC Nuisance Fits & Working $a_0$ | `[D]` Regularized Fit / Measurement | `02_galaxy_dynamics/A0_MEASUREMENT.json`, `PARAMETER_LEDGER.json` | Tier 1 ($N_{\text{par}}=374$, median 2.95); $a_0 = 1.116\times 10^{-10} \pm 14.4\%$ |
| **F6** | $\Omega_\Lambda = \ln 2 \approx 0.693$ Holographic / Disformal Boundary | `[O]` Conjectural Limit | Motivational Narrative Annex | Conjectured horizon boundary condition, not a derived density |
| **F7** | 17 Lean 4 Mechanical Proof Modules (0 sorrys) | `[P]` Kernel Verified | `05_lean_formalization/*.lean` | `verify_all_proofs.sh` exit 0 on local gate; standard axioms only |
| **F8** | Empirical Provenance & Out-of-Sample Validation | `[D]` Cross-Validation / Bootstrap | `02_galaxy_dynamics/A0_MEASUREMENT.json` | 171 galaxies (3,375 points), bootstrap + honest CV |

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
* **Mathematical Summary:**
  The dual-channel constitutive potential:
  $$\mathcal{F}_{\text{dual}}(x) = \frac{x^2}{2} - x + \ln(1+x)$$
  differentiates directly to:
  $$\mathcal{F}_{\text{dual}}'(x) = x - 1 + \frac{1}{1+x} = \frac{x(1+x) - (1+x) + 1}{1+x} = \frac{x^2}{1+x}.$$
  In the kinetic channel $y = |\nabla\Phi|/a_0$, this gives the standard rational $\mu(x) = \frac{x}{1+x}$, verified mechanically in Lean 4 (`DualChannelDerivation.lean`).
  The historical single-channel potential $\mathcal{F}(x) = x \operatorname{arcsinh}(x) - \sqrt{1+x^2}$ produced $\mathcal{F}'(x) = \operatorname{arcsinh}(x)$ which yields inverted physical limits; it is quarantined as correspondence-false (`PAPER_01_NOTICE.md`).

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

### F7. Lean 4 Formal Verification Suite (17 Modules, Standard Foundational Axioms)
* **Epistemic Classification:** `[P]` Proved / Kernel Verified
* **Target Directory:** [`05_lean_formalization/`](05_lean_formalization/)
* **Status:** Exit code 0 on local verification gate (`109d38b`, Mathlib `5eec30bc`), recorded in `VERIFICATION_RUN_003/01_lean/`. Blank-machine cache reproduction (O6) remains open.
* **Kernel Axiom Footprint:** Exclusively standard foundational axioms `[propext, Classical.choice, Quot.sound]`. (Documented structural/typeclass vacuity in `YettParadigm.lean` and `SovereignRegularity.lean` recorded in `THEORY_ASSUMPTION_AUDIT.md`).

| Lean 4 File | Headline Theorems Verified | Axiom Footprint | Status |
|---|---|---|---|
| [`DualChannelDerivation.lean`](05_lean_formalization/DualChannelDerivation.lean) | `dual_channel_derivative`, `simple_mu_scaling` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`GODActionKinematics.lean`](05_lean_formalization/GODActionKinematics.lean) | `dual_channel_poly_identity`, `aqual_simple_mu_ratio`, `btfr_algebraic_scaling` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`ITActionClosure.lean`](05_lean_formalization/ITActionClosure.lean) | `tauLaw_eq_simple_mu_poly`, `btfr_deep_mond` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`SOCasimirGenuine.lean`](05_lean_formalization/SOCasimirGenuine.lean) | `casimir_defining_rep`, `casimir_scalar_eq` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`DeSitterExtremal.lean`](05_lean_formalization/DeSitterExtremal.lean) | `desitter_lapse_horizon` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`MuProjection.lean`](05_lean_formalization/MuProjection.lean) | `mu_simple_eq_cos`, `powerLaw_iterated_deriv` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`TensorSpeed.lean`](05_lean_formalization/TensorSpeed.lean) | `gw_tensor_speed_luminal`, `foster_jacobson_alpha1` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`CovariantCompletion.lean`](05_lean_formalization/CovariantCompletion.lean) | `raqual_superluminal`, `disformal_gamma_ppn_unity` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`SkordisZlosnikEmbedding.lean`](05_lean_formalization/SkordisZlosnikEmbedding.lean) | `skordis_zlosnik_potential_derivative`, `sz_kinetic_convexity` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`RelativisticStability.lean`](05_lean_formalization/RelativisticStability.lean) | `dual_channel_kinetic_convexity`, `hamiltonian_bounded_below` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`PPNLimits.lean`](05_lean_formalization/PPNLimits.lean) | `solar_system_precision_bound`, `cassini_radar_delay_satisfied` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`TritBorn.lean`](05_lean_formalization/TritBorn.lean) | `born_rule_trit_probability` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`Decoherence.lean`](05_lean_formalization/Decoherence.lean) | `lindblad_trace_preserving`, `purity_decay` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`ChiralGate.lean`](05_lean_formalization/ChiralGate.lean) | `chiral_unitary_preservation` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |
| [`YettParadigm.lean`](05_lean_formalization/YettParadigm.lean) | `ramanujan_yett_spectral_gap_pos` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** (Assumptions documented) |
| [`SovereignRegularity.lean`](05_lean_formalization/SovereignRegularity.lean) | `bkm_regularity_criterion` | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** (Assumptions documented) |
| [`PrintAxioms.lean`](05_lean_formalization/PrintAxioms.lean) | Axiom reflection & validation targets | `[propext, Classical.choice, Quot.sound]` | **VERIFIED `[P]`** |

---

### F8. Empirical Provenance & Out-of-Sample Validation
* **Epistemic Classification:** `[D]` Direct Computational Benchmark
* **File Paths:**
  - [`02_galaxy_dynamics/A0_MEASUREMENT.json`](02_galaxy_dynamics/A0_MEASUREMENT.json)
  - [`02_galaxy_dynamics/A0_ESTIMATE.json`](02_galaxy_dynamics/A0_ESTIMATE.json)
* **Methodology:** 171 SPARC galaxies (3,375 kinematic data points) evaluated via bootstrap over galaxies and honest 5-fold cross-validation with per-fold $a_0$ retraining.
