# 🏛️ Verification Evidence Ledger: Findings F1–F8

> **BRANCH NOTICE (2026-09-20).** The results below concern
> $\mathcal{F}_{\text{dual}}(x) = \tfrac12 x^2 - x + \ln(1+x)$ and its constitutive
> ratio $\mu(x) = x/(1+x)$. **That branch was falsified on 2026-09-12** — it leaves
> an unscreened solar-system anomalous acceleration far above the Cassini bound —
> and the theory is rebuilt on $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$.
>
> The algebraic statements here remain **true as mathematics**: $\mathcal{F}_{\text{dual}}$
> really does have the stated constitutive structure, Padé minimality and
> ghost-freedom. What is retracted is their status as claims about the *physical*
> model. A `[P]` below should be read as "proved about $\mathcal{F}_{\text{dual}}$",
> not "proved about the theory". See `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`
> for the live derivation.
> The retired objects named below are $\mathcal{F}_{\text{dual}}$ / `F_dual` and
> $\mu_{\text{dual}}(x) = x/(1+x)$, **falsified 2026-09-12**. The live branch is
> $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$ (AeST / Skordis–Złośnik). Statements here
> remain valid as mathematics *about* the retired branch; none is a claim about the
> live model.


**Author / Lead Investigator:** R.W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Repository (Res-Nova):** `Mega-Therion/Res-Nova`  
**Res-Nova Release:** `v1.5.0`  
**Evaluation Standard:** Sovereign Epistemic Covenant & Newton Epistemic Taxonomy (`[P]`, `[D]`, `[C]`, `[O]`)

---

## Executive Summary of Findings & Evidence Mapping

| Finding | Topic | Epistemic Status | Primary Corpus Location | Reference / Note |
|---|---|---|---|---|
| **F1** | AQUAL Weak-Field Field Equation | `[C]` Literature Baseline | `res_nova_manuscript.tex` §2 | Bekenstein-Milgrom (1984) |
| **F2** | $\mu(x)$ Dual-Channel Derivative Identity | `[P]` (algebra) / `[O]` (closure) | `05_lean_formalization/DualChannelDerivation.lean`, `01_foundational_action/PAPER_01_NOTICE.md` | Dual-channel $\mu(x)=x/(1+x)$ `[P]`; single-channel quarantined |
| **F3** | $a_0 = cH_0/(2\pi)$ KMS Cancellation Null Result | `[O]` Horizon Normalization | `res_nova_manuscript.tex` §3.2, `04_cosmology/A0_AND_OMEGA_NORMALIZATION_LEDGER.md` | Thermal KMS cancellation derived; $1/(2\pi)$ is open normalization |
| **F4** | Fixed Tier 0 SPARC Benchmark | `[D]` Empirical Evaluation | `02_galaxy_dynamics/PARAMETER_LEDGER.json` (Tier 0: median 9.20) | "Zero free parameters" language withdrawn as a working model class |
| **F5** | SPARC Nuisance Fits & Working $a_0$ | `[D]` Regularized Fit / Measurement | `02_galaxy_dynamics/A0_MEASUREMENT.json`, `PARAMETER_LEDGER.json` | Tier 1 ($N_{\text{par}}=374$, median 2.95); $a_0 = (1.116 \pm 0.128_{\text{stat}} \pm 0.097_{\text{syst}})\times 10^{-10}\text{ m/s}^2$ |
| **F6** | $\Omega_\Lambda = \ln 2 \approx 0.693$ Holographic / Disformal Boundary | `[O]` Conjectural Limit | Motivational Narrative Annex | Conjectured horizon boundary condition, not a derived density |
| **F7** | 17 Lean 4 Modules on Disk | `[P]` Kernel Verified / Diagnostic | `05_lean_formalization/*.lean` | `verify_all_proofs.sh` exit 0 on local gate; standard axioms only |
| **F8** | Empirical Provenance & Out-of-Sample Validation | `[D]` Cross-Validation / Bootstrap | `02_galaxy_dynamics/A0_MEASUREMENT.json` | 171 galaxies (3,375 points), bootstrap + honest CV |
| **F9** | Kerr Rapidity Equipartition & Sovereign Spin Ceiling | `[P]` (algebra) / `[O]` (dynamical action) | `06_unification_and_spin/rapidity_uniqueness_proof.py`, `two_channel_ceiling_proof.py` | Exact $\operatorname{arsinh}(1) = \ln(1+\sqrt{2}) = \operatorname{artanh}(1/\sqrt{2})$ and $\chi_s = \sqrt{\sqrt{2}-1/2} \approx 0.956145$ verified `[P]` at 100 dps |
| **F10** | Canonical $\mu_{\text{std}}$ Foundations, Gradient Characteristic Speed & Monopole Tail (corrected 2026-09-30) | `[P]` Kernel Verified / `[D]` Ephemerides | `05_lean_formalization/MuStdFoundations.lean`, `scripts/verify_mu_std_cassini_and_limits.py` | Derivative identity $F_{\text{std}}'=x\mu_{\text{std}}$, strict convexity $F_{\text{std}}''>0$, P(X)-completion speed along the gradient $c_\parallel^2 = xF''/F' = (x^2+2)/(x^2+1) \in (1,2]$ (**superluminal**), and Saturn monopole tail $1-\mu_{\text{std}} \le 2\times10^{-12}$ `[P]`. **Retracted:** "$c_s^2\in[1/2,1)$, subluminal" (was $1/c_\parallel^2$) and "Cassini clearance" (monopole ≠ $\gamma-1$; EFE quadrupole fails) |
| **F11** | AeST Stealth / Dragged Branch Exact GR Sector & Vanishing Residuals (scope corrected 2026-09-30) | `[D]` Symbolic CAS (residuals) / `[P]` Kernel (kinematic identities only) / `[C]` Skordis & Vokrouhlický 2024 | `exploration/d3_alpha/dragged_branch_exact_check.py`, `05_lean_formalization/AeSTStealthSector.lean` | All 8 field-equation residuals vanish on PG Schwarzschild at $F_Q(Q_0)=0$ and not at $Q_1 = 1.1Q_0$ (negative control) `[D]`. The Lean module proves only $P^{00}=0$, $\mathcal{Y}=0$, $Q=Q_0$; its PPN theorems are `rfl` on defined values. Applies only on the dragged branch (D7 branch selection `[O]`) |

---

## Detailed Evidence Dossier

### F1. AQUAL Weak-Field Euler-Lagrange Field Equation
* **Epistemic Classification:** `[C]` Cited Literature Baseline
* **File Paths:**
  - [`res_nova_manuscript.tex`](res_nova_manuscript.tex)
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
  - [`res_nova_manuscript.tex`](res_nova_manuscript.tex)
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
  - [`res_nova_manuscript.tex`](res_nova_manuscript.tex) §3.2
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
  - **Corrected 2026-09-12** (see `02_galaxy_dynamics/SPARC_MU_STD_RECOMPUTE_2026-09-12.md`): the interpolation function used to compute this benchmark, $\mu_{\text{dual}}(x)=x/(1+x)$, was found falsified for solar-system use (Mercury perihelion precession ~1000$\times$ the observed bound). Recomputed under the corrected $\mu_{\text{std}}(x)=x/\sqrt{1+x^2}$: median $\chi^2_{\text{data}}/N_g = 11.077$ (was 9.20) across 171 galaxies, vs MOND $1.2\times 10^{-10}$ median $9.935$ (was 11.35). **The headline flips — GOD no longer outperforms MOND at tier 0; MOND's fitted $a_0$ now fits the median galaxy better.** Under $\mu_{\text{std}}$, GOD's interpolation function is identical to standard MOND's; the comparison reduces to $a_0$ provenance alone (derived vs.\ fitted).
  - Independently of the $\mu$ correction: the underlying code was found to implement only one interpolation function despite this file's prior text implying GOD and MOND used distinct ones — that framing was never accurate.

---

### F5. Matched Nuisance Fits and Working $a_0$ Measurement
* **Epistemic Classification:** `[D]` Empirical Evaluation / Measurement
* **File Paths:**
  - [`02_galaxy_dynamics/A0_MEASUREMENT.json`](02_galaxy_dynamics/A0_MEASUREMENT.json)
  - [`02_galaxy_dynamics/PARAMETER_LEDGER.json`](02_galaxy_dynamics/PARAMETER_LEDGER.json)
  - [`02_galaxy_dynamics/NFW_CONSTRAINED.json`](02_galaxy_dynamics/NFW_CONSTRAINED.json)
* **Summary:**
  - Working measurement: $a_0 = (1.116 \pm 0.128_{\text{stat}} \pm 0.097_{\text{syst}})\times 10^{-10}\text{ m/s}^2$ (total 14.4% error) across 171 galaxies (3,375 points). **SUPERSEDED 2026-09-17 — provenance only.** The live object is the $\mu_{\text{std}}$ row, $a_0 = 1.1607\times10^{-10}$ on 175 galaxies (3,391 points). The gap between the two is *not* the closure effect: it mixes sample, distance treatment and closure. On one frozen harness the closure effect alone is $9.2420\times10^{-11}\to1.16067\times10^{-10}$, **+25.6%**. See `docs/A0_CLOSURE_EVOLUTION.md`.
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

> **SUPERSEDED 2026-09-09 (RUN_009-era inventory).** The suite now gates **43 targets**: the 17 modules tabulated below, plus `HorizonScale.lean`, and the adjacent-programme modules declared in `05_lean_formalization/ADJACENT_MODULES.txt` (GUT/E8 generation structure, the chiral-crack programme, the SU(2) envelope rungs adopted in #39, and related work). The table below is retained as the historical 17-module core of the manuscript's formal inventory — it is not the current gate census; the live census is `05_lean_formalization/check_target_inventory.py` (PASS, 43 targets, gate ≡ lakefile ≡ disk). O6 is closed (cold fetch RUN_008 + CI `lean-gate` on every push, green at `d130413`).
* **Epistemic Classification:** `[P]` Proved / Diagnostic / Assumption
* **Target Directory:** [`05_lean_formalization/`](05_lean_formalization/)
* **Status:** O6 — closed 2026-09-08. Cold machine: VERIFICATION_RUN_008 fetched all 8678 cache files from origin with no Mathlib cache on disk and the gate passed. CI release gate: the `lean-gate` job in `.github/workflows/verify.yml` runs `verify_all_proofs.sh` on push, schedule, and dispatch — green at `d130413`, 43/43 targets, gate list set-identical to `lakefile.lean` roots.
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
| [`SovereignRegularity.lean`](05_lean_formalization/SovereignRegularity.lean) | `assumed_vorticity_bound_projection`, `product_bound_below_threshold` (renamed 2026-10-08 from `sovereign_regularity_theorem`, `bkm_no_blowup`) | `[propext, Classical.choice, Quot.sound]` | Machine-checked, **`[arith]`**: the first returns its own assumed field (`st.h_controlled T hT`), the second is arithmetic on it. No regularity or BKM content. *(Corrected 2026-10-08 from "VERIFIED `[P]`".)* |
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

---

### F10. Canonical $\mu_{\text{std}}$ Foundations, Gradient Characteristic Speed & Monopole Tail
> **Corrected 2026-09-30.** The 2026-09-29 version of this entry certified "scalar perturbation
> sound speed $c_s^2 = (1+x^2)/(x^2+2) \in [1/2,1)$, strictly subluminal" and "Cassini clearance".
> Both are retracted. The first expression is $\mu/(x\mu)'$, a ratio of spatial stiffnesses with no
> time-derivative coefficient in it; it is the reciprocal of the actual characteristic speed, which is
> superluminal. It was typed in by hand, so its proofs closed for any $\mu$ (not substitutable).
> The second compared the monopole $1-\mu$ with the Cassini bound on $\gamma-1$, a different observable,
> while the binding Cassini test (EFE quadrupole) is one bare $\mu_{\text{std}}$ fails
> (`02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md`).

* **Epistemic Classification:** `[P]` Proved (constitutive derivative, convexity, characteristic speed, monopole tail) / `[D]` Ephemerides benchmark
* **File Paths:**
  - [`05_lean_formalization/MuStdFoundations.lean`](05_lean_formalization/MuStdFoundations.lean)
  - [`scripts/verify_mu_std_cassini_and_limits.py`](scripts/verify_mu_std_cassini_and_limits.py)
  - [`scripts/repro/cassini_clearance_receipt.json`](scripts/repro/cassini_clearance_receipt.json) (filename kept for link stability; contents are monopole-only)
  - [`res_nova_manuscript.tex`](res_nova_manuscript.tex) §3.3
* **Verified Formal Theorems (`MuStdFoundations.lean`):**
  - **Constitutive Derivative Identity:** $F_{\text{std}}'(x) = x^2/\sqrt{1+x^2} = x\,\mu_{\text{std}}(x)$ (`F_std_deriv_eq`).
  - **Strict Convexity:** $F_{\text{std}}''(x) = x(x^2+2)/(1+x^2)^{3/2} > 0$ for all $x > 0$ (`F_std_deriv2_positivity`), hence strict convexity on $[0, \infty)$ (`F_std_strict_convexity`).
  - **Characteristic Speed Along the Gradient:** `c_long_sq x := x · deriv (deriv F_std) x / deriv F_std x` equals $(x^2+2)/(x^2+1)$ for $x>0$ (`c_long_sq_eq`), with $1 < c_\parallel^2 \le 2$ (`c_long_sq_superluminal`, `c_long_sq_le_two`). In the relativistic P(X) completion this is the speed along the background gradient ($c_\perp^2 = 1$): **superluminal**, the known RAQUAL acausality. AeST's scalar speed is D6's separate result. Sabotage-tested 2026-09-30: replacing `F_std` by $x^3/3$ in the definition breaks `c_long_sq_eq`.
  - **Inverse-Square Screened Tail:** $1 - \mu_{\text{std}}(x) \le 1/(2x^2)$ for all $x \ge 1$ (`deviation_le_inv_two_sq`).
  - **Saturn Monopole Deviation:** for $x \ge 5\times10^5$, $1 - \mu_{\text{std}}(x) \le 2\times10^{-12}$ (`saturn_monopole_deviation_le`). Monopole only; not a Cassini clearance.
* **Ephemerides Benchmark (`verify_mu_std_cassini_and_limits.py`, live $a_0 = 1.1607\times10^{-10}$):**
  - Saturn: $x = 5.564\times10^5$, $1-\mu_{\text{std}} = 1.615\times10^{-12}$, $\Delta g = 1.04\times10^{-16}\,\text{m/s}^2$.
  - Mercury residual force: $\Delta g(\mu_{\text{std}}) = 1.70\times10^{-19}\,\text{m/s}^2$ vs unshielded $\Delta g(\mu_{\text{dual}}) \approx a_0$.
  - The 2026-09-29 run used the superseded μ_dual-era $a_0 = 1.116\times10^{-10}$.

---

### F11. AeST Stealth / Dragged Branch Exact GR Sector & Field Equation Residuals (Target D3 §34)
> **Scope corrected 2026-09-30.** The field-equation content is carried by the symbolic CAS check
> below `[D]` and by the published stealth solution (Skordis & Vokrouhlický 2024, arXiv:2412.15395)
> `[C]`. The Lean module contains no field equation: it proves one-line kinematic identities by
> `ring`, and its PPN theorems are `rfl` on values it defines. The result holds only on the dragged
> branch; branch selection is open (D7).

* **Epistemic Classification:** `[D]` Symbolic CAS Verification (residuals) / `[P]` Lean (kinematic identities only)
* **File Paths:**
  - [`exploration/d3_alpha/dragged_branch_exact_check.py`](exploration/d3_alpha/dragged_branch_exact_check.py)
  - [`05_lean_formalization/AeSTStealthSector.lean`](05_lean_formalization/AeSTStealthSector.lean)
  - [`PEER_REVIEW_READINESS.md`](PEER_REVIEW_READINESS.md) §1 Target D3
* **Lean identities (`AeSTStealthSector.lean`):**
  - $P^{00} = -1 + (1)(1) = 0$ (`P00_vanishes`); hence $\mathcal{Y} = 0$ in the free-fall frame (`Y_stealth_is_zero`).
  - $Q = Q_0$ (`Q_stealth_eq_Q0`, `condensate_offset_zero`); the ansatz $c_Y\mathcal{Y} - 2K_2(Q-Q_0)^2$ vanishes there (`F_kinetic_stealth_vanishes`).
  - `stealth_ppn_*`: definitional (`rfl`) restatements of the imported GR values; not a derivation.
* **Symbolic CAS Verification (`dragged_branch_exact_check.py`):**
  - Evaluated on Painlevé–Gullstrand Schwarzschild geometry with radial inflow $v = \sqrt{2M/r}$, non-zero expansion $\theta = -(3/2)\sqrt{2M/r^3}$, and $\phi = Q_0 T$.
  - All 8 Euler–Lagrange field equation residuals ($E_f, E_h, E_k, E_s, E_{A_t}, E_{A_r}, E_\phi, E_\lambda$) vanish identically to 0 at the condensate minimum ($F_Q(Q_0)=0$).
  - Negative control (re-run 2026-09-30, exit 0): with $Q_1 = 1.1\,Q_0$ five residuals are nonzero, so the check is not vacuous.



