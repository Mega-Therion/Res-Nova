<div align="center">

# 🌌 RES NOVA
### Geometrically Ordered Dynamics & Dual-Channel MOND Completion
**A Rigorous Mathematical Derivation, Machine-Verified Foundation, and Empirical SPARC Benchmark**

---

[![Release](https://img.shields.io/badge/Release-v1.4.0-0052FF.svg?style=for-the-badge&logo=github)](https://github.com/Mega-Therion/Res-Nova/releases/tag/v1.4.0)
[![Lean 4 Verified](https://img.shields.io/badge/Lean_4-15_Modules_Verified-4B32C3.svg?style=for-the-badge&logo=lean)](05_lean_formalization/)
[![Epistemic Covenant](https://img.shields.io/badge/Epistemic_Hygiene-%5BP%5D_%5BD%5D_%5BC%5D_%5BO%5D-D4AF37.svg?style=for-the-badge)](EPISTEMIC_BOUNDARY_v1.4.0.md)
[![SPARC Benchmark](https://img.shields.io/badge/SPARC_175-Median_%CF%87%C2%B2%2FNg_%3D_2.92-00C781.svg?style=for-the-badge)](02_galaxy_dynamics/)
[![Vercel Live](https://img.shields.io/badge/Observatory-Live_Deployment-000000.svg?style=for-the-badge&logo=vercel)](https://res-nova-observatory.vercel.app)

<br/>

**Author:** [Ryan W. Yett](https://orcid.org/0009-0000-8803-1250) &nbsp;|&nbsp; **Affiliation:** Independent Theoretical Research &nbsp;|&nbsp; **Status:** Public Release `v1.4.0`

[**Interactive Observatory ↗**](https://res-nova-observatory.vercel.app) &nbsp;•&nbsp; [**Master Manuscript (PDF) 📄**](final_manuscript.pdf) &nbsp;•&nbsp; [**Formal Proof Suite 📐**](05_lean_formalization/) &nbsp;•&nbsp; [**Empirical Ledger 📊**](CLAIM_EVIDENCE_LEDGER.md)

</div>

---

## 🏛️ Theoretical Overview

**Res-Nova** provides a closed variational derivation, empirical cross-validation, and 4D covariant embedding of the non-relativistic modified gravity action, resolving longstanding discrepancies between variational Lagrangian formulation, empirical galaxy rotation curves, and gravitational wave speed bounds ($c_T = c$).

```
                      ┌───────────────────────────────────────────────┐
                      │    Bulk Kinetic Flux + Horizon Dissipation    │
                      └───────────────────────┬───────────────────────┘
                                              │ Variational Action
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │     Dual-Channel Kinetic Potential F(x)       │
                      │       F(x) = ½x² - x + ln(1 + x)              │
                      └───────────────────────┬───────────────────────┘
                                              │ Euler-Lagrange Variation
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │    Rational Interpolation Function μ(x)       │
                      │               μ(x) = x / (1 + x)              │
                      └───────────────┬───────────────┬───────────────┘
                                      │               │
                     Empirical Test   ▼               ▼   4D Covariant Embedding
          ┌───────────────────────────────────┐     ┌───────────────────────────────────┐
          │  SPARC 175-Galaxy Database        │     │  Skordis-Złośnik RMOND Parent     │
          │  • 3,391 Kinematic Radii          │     │  • c_T = c_γ = c (GW170817 Bound) │
          │  • Median χ²_data / Ng = 2.92     │     │  • γ_PPN = 1.0 (Solar System GR)  │
          │  • Nominal DOF_nom = 3,009        │     │  • Zero FLRW Dark Energy Pole     │
          └───────────────────────────────────┘     └───────────────────────────────────┘
```

---

## ⚡ Core Mathematical & Empirical Pillars

### 1. Dual-Channel Variational Closure $\mathbf{[P]}$
The single-channel action $\mathcal{F}_{\text{single}}'(x) = \operatorname{arcsinh}(x)$ exhibits unphysical asymptotic saturation ($\mu \to 0$ as $x \to \infty$), failing correspondence. Balancing bulk kinetic flux with horizon relative-entropy dissipation isolates the unique **Dual-Channel Action**:

$$\mathcal{F}_{\text{dual}}(x) = \frac{1}{2}x^2 - x + \ln(1+x), \quad x = \frac{|\nabla \Phi|}{a_0}$$

Its direct Euler–Lagrange variation produces the canonical rational interpolation function:

$$\mu(x) = \mathcal{F}_{\text{dual}}'(x) = \frac{x}{1+x}$$

$$\lim_{x \to 0} \mu(x) = x \quad (\text{Deep MOND / BTFR } M \propto V^4), \qquad \lim_{x \to \infty} \mu(x) = 1 \quad (\text{Newtonian Limit})$$

---

### 2. SPARC 175-Galaxy Empirical Benchmark $\mathbf{[D]}$
Evaluated across all $N = 175$ uncurated galaxies ($3,391$ resolved rotation curve measurements) in the Spitzer Photometry and Accurate Rotation Curves (SPARC) database:

| Specification | Free Parameters | Points / $\text{DOF}_{\text{nom}}$ | Median $\chi^2/N_g$ | Mean $\chi^2/N_g$ | Aggregate $\chi^2/\text{DOF}$ | Scientific Role |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Baryons-Only (Std SPARC)** $\mathbf{[D]}$ | 0 | 3,391 / 3,391 | 85.23 | 267.92 | 406.49 | Null baseline |
| **Baryons-Only (Unit $M/L$)** $\mathbf{[D]}$ | 0 | 3,391 / 3,391 | 51.58 | 157.58 | 204.65 | Fixed control |
| **Strict Zero-Param ($\mu_{\text{simple}}$)** $\mathbf{[D]}$ | 0 | 3,391 / 3,391 | 29.12 | 100.40 | 144.04 | Heuristic control |
| **Canonical Dual-Channel ($\mu_{\text{derived}}$)** $\mathbf{[D]}$ | **176** | **3,391 / 3,215** | **2.92** | **7.84** | **11.23** | **Headline Model** |
| **5-Fold Cross-Validation** $\mathbf{[D]}$ | — | 3,391 / 3,391 | **14.33** | **32.18** | **56.11** | **Out-of-sample Generalization** |

* Fitted universal acceleration scale: $a_0 = (9.433 \pm 0.050) \times 10^{-11} \text{ m/s}^2$
* Horizon acceleration scale: $a_0 \approx cH_0 / (2\pi)$ consistent within $\sim 9.5\%$ systematic cosmological bounds.

---

### 3. 4D Covariant Metric Completion & GW170817 Soundness $\mathbf{[P]}$
- **Pure RAQUAL Falsification $\mathbf{[P]}$:** Pure scalar k-essence generates superluminal acoustic propagation cones ($c_\parallel > 1$) in all galactic halo potentials, mathematically ruling out pure scalar completions.
- **Disformal Metric Split Falsification $\mathbf{[P]}$:** Conformal-disformal transitions $B(\phi) \ne 0$ violate the multi-messenger constraint $|c_T/c_\gamma - 1| \le 10^{-15}$ from GW170817/GRB 170817A.
- **Skordis–Złośnik (RMOND) Parent Embedding $\mathbf{[P]}$:** The derived dual-channel function embeds into the unit-timelike vector Skordis–Złośnik (2021) action:

$$\mathcal{J}(\mathcal{Y}) = \frac{1}{2}\mathcal{Y} - \sqrt{\mathcal{Y}} + \ln(1 + \sqrt{\mathcal{Y}}), \qquad 2\mathcal{J}'(\mathcal{Y}) = \frac{\sqrt{\mathcal{Y}}}{1 + \sqrt{\mathcal{Y}}} \equiv \mu(\sqrt{\mathcal{Y}})$$

$$\text{Guaranteeing: } \quad c_T \equiv c_\gamma \equiv c, \quad \gamma_{\text{PPN}} = 1.00000, \quad \alpha_1 = \alpha_2 = 0, \quad \mathcal{J}''(\mathcal{Y}) > 0$$

---

## 📐 Machine-Checked Formal Proof Inventory (Lean 4)

All foundational propositions are mechanically certified in **Lean 4 / Mathlib** with **0 warnings, 0 errors, 0 `sorry` shortcuts, and zero custom unproven axioms**:

| Module | Headline Theorem | Mechanical Guarantee | Epistemic Status |
| :--- | :--- | :--- | :---: |
| [`CovariantCompletion.lean`](05_lean_formalization/CovariantCompletion.lean) | `raqual_superluminal_obstruction` | $c_\parallel^2 = 1 + \frac{1}{1+x} > 1$ (Superluminal cone obstruction) | $\mathbf{[P]}$ |
| [`CovariantCompletion.lean`](05_lean_formalization/CovariantCompletion.lean) | `disformal_gamma_ppn_unity` | $\gamma_{\text{PPN}} = 1$ and preferred-frame $\alpha_1 = \alpha_2 = 0$ | $\mathbf{[P]}$ |
| [`CovariantCompletion.lean`](05_lean_formalization/CovariantCompletion.lean) | `no_dynamical_dark_energy_density` | $\hat{\nabla}_\mu \phi = 0$ on homogeneous FLRW backgrounds | $\mathbf{[P]}$ |
| [`SkordisZlosnikEmbedding.lean`](05_lean_formalization/SkordisZlosnikEmbedding.lean) | `skordis_zlosnik_kinetic_convexity` | $\mathcal{J}''(\mathcal{Y}) = \frac{1}{4(1+\sqrt{\mathcal{Y}})^2} > 0$ (Ghost & gradient stability) | $\mathbf{[P]}$ |
| [`TensorSpeed.lean`](05_lean_formalization/TensorSpeed.lean) | `gw170817_speed_identity` | $c_T^2 = 1/(1-c_{13}) \equiv 1$ under Maxwellian vector coupling | $\mathbf{[P]}$ |
| [`GODActionKinematics.lean`](05_lean_formalization/GODActionKinematics.lean) | `dual_channel_poly_identity` | $\mathcal{F}_{\text{dual}}'(x) = x/(1+x)$ and point-mass BTFR $M \propto V^4$ | $\mathbf{[P]}$ |
| [`SovereignRegularity.lean`](05_lean_formalization/SovereignRegularity.lean) | `sovereign_regularity_theorem` | Conditional Beale–Kato–Majda integral boundedness | $\mathbf{[P]}$ |
| [`SOCasimirGenuine.lean`](05_lean_formalization/SOCasimirGenuine.lean) | `casimir_defining_rep` | Quadratic Casimir eigenvalue $C_2(\mathfrak{so}(n)) = (n-1)/2$ | $\mathbf{[P]}$ |

Axiom verification via `#print axioms`:
```lean
-- All theorems strictly depend solely on core foundationals:
[propext, Classical.choice, Quot.sound]
```

---

## 🔬 The Sovereign Epistemic Covenant

To prevent speculative inflation and enforce strict scientific hygiene:

$$\begin{aligned}
\mathbf{[P]} & \quad \textbf{Proved (Lean 4 Kernel Certified):} \text{ Mathematical truth within formal axiomatic system.} \\
\mathbf{[D]} & \quad \textbf{Direct Empirical (Computed):} \text{ Evaluated from raw SPARC data via auditable, reproducible scripts.} \\
\mathbf{[C]} & \quad \textbf{Cited Literature:} \text{ Authentic peer-reviewed baselines (McGaugh 2016, Skordis 2021).} \\
\mathbf{[O]} & \quad \textbf{Open Problem / Conjectured Boundary:} \text{ Phenomenological bridge hypotheses quarantined from proof claims.}
\end{aligned}$$

---

## 🛠️ Reproduction & Verification Pipeline

```bash
# 1. Clone repository
git clone https://github.com/Mega-Therion/Res-Nova.git
cd Res-Nova

# 2. Verify all Lean 4 formal machine proofs
cd 05_lean_formalization
lake env lean CovariantCompletion.lean
lake env lean SkordisZlosnikEmbedding.lean
lake env lean TensorSpeed.lean

# 3. Reproduce SPARC 175-Galaxy Benchmark & 5-Fold Cross-Validation
cd ../02_galaxy_dynamics
python3 sparc_cross_validation.py

# 4. Compile master publication manuscript
cd ..
pdflatex -interaction=nonstopmode final_manuscript.tex
bibtex final_manuscript
pdflatex -interaction=nonstopmode final_manuscript.tex
```

---

## 📂 Repository Topology

```
Res-Nova/
├── 01_foundational_action/       # Variational action derivations & PRD monographs
├── 02_galaxy_dynamics/           # SPARC data, fitting pipelines, & parameter budgets
├── 03_observer_jwst/             # Observer interface & high-z cosmic calibration
├── 04_cosmology/                 # FLRW decoupling & horizon thermodynamics
├── 05_lean_formalization/        # 15 Lean 4 formalization modules (Mathlib verified)
├── visualizer/                   # Interactive Next.js/Vercel Observatory source
├── final_manuscript.pdf          # 12-page peer-review ready master PDF
├── final_manuscript.tex          # REVTeX/LaTeX master source
├── reproducibility_appendix.tex  # Formal theorem & artifact checksum inventory
├── zenodo_metadata.json          # Pre-print archival deposition schema
└── EPISTEMIC_BOUNDARY_v1.4.0.md  # Master claim-by-claim epistemic audit ledger
```

---

<div align="center">

**Res-Nova Observatory & Research Program**  
*AI proposes. Machines verify. Humans audit. Evidence persists.*

</div>
