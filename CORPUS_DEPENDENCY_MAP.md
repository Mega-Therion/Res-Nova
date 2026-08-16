# 🗺️ Corpus Dependency & Inversion Map
**Framework:** Chyren / Res-Nova Epistemic Architecture  
**Author:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Date:** 2026-08-14 (Aligned to v1.5.0, 2026-08-16)  
**Primary Dataset:** 138 Master LaTeX Documents ([`corpus_graph.json`](corpus_graph.json))

---

## 1. Classification Topology (The 3 Node Types)

Every document, claim, and equation in the 138-manuscript corpus is categorized into one of three functional node types:

1. **Root Nodes (`[O]` Research Targets):** Foundational hypotheses upon which downstream results depend, but which currently lack first-principles variational proofs (e.g., the constitutive uniqueness of $\mu(x)$, the $a_0$ scale normalization, the $\Omega_\Lambda = \ln 2$ cosmology conjecture).
2. **Bridge Nodes (Intermediate Reductions & Fits):** Manifold reductions, AQUAL Euler–Lagrange expansions, and SPARC empirical calibrations that connect root hypotheses to physical observables.
3. **Leaf Nodes (`[P]` Formally Certified Theorems):** Mechanically kernel-verified algebraic propositions in Lean 4 (e.g., Casimir eigenvalues, spectral gaps, polynomial identities, dual-channel variational derivatives) whose mathematical validity is independent of physical ontology.

---

## 2. Global Claim & Dependency Inversion Table

| Node ID / Manuscript | Primary Assertion | Epistemic Tier | Support Type | Upstream Dependencies | Downstream Consumers |
|---|---|---|---|---|---|
| **Root 1: $\mu(x)$ Closure** | Dual-channel $\mathcal{F}_{\text{dual}}'(x) = \frac{x}{1+x}$ is `[P]` algebraic; uniqueness of action in nature | `[P]` (algebra) / `[O]` (closure) | `DualChannelDerivation.lean`, `GODActionKinematics.lean` | None (Constitutive Action) | SPARC fits, Paper 09, Monograph §2 |
| **Root 2: $a_0$ Scale** | $a_0 = c H_0 / (2\pi)$ from horizon thermodynamics | `[O]` Null/Negative Result | KMS temperature matching (cancels $2\pi$) | De Sitter horizon equilibrium | Zero-parameter benchmarks |
| **Root 3: $\Omega_\Lambda = \ln 2$** | Dark energy density matches 1-qubit Shannon limit | `[O]` Conjectural Limit | Entanglement entropy bound ($S_E \le \ln 2$) | Qubit state factorization | Cosmological expansion notes |
| **Bridge 1: Weak-Field AQUAL** | $\nabla\cdot[\mu(|\nabla\Phi|/a_0)\nabla\Phi] = 4\pi G\rho$ | `[C]` Cited Literature | Bekenstein-Milgrom (1984) field theory | Action Principle | SPARC rotation curves |
| **Bridge 2: 5-Fold Cross-Val** | Honest CV retrains $a_0$ per fold (D4.6); working measurement $a_0 = 1.116\times 10^{-10}$ | `[D]` Empirical Benchmark | 171 SPARC galaxies / 3,375 kinematic points | Fixed population priors / bootstrap | Generalization bounds |
| **Leaf: Lean 4 Modules** | 17 modules (`DualChannelDerivation.lean`, `SOCasimirGenuine.lean`, `TensorSpeed.lean`, etc.) | `[P]` Kernel Verified | Lean 4 / Mathlib proofs (`0 sorry`) | Standard Lean logic | Manuscript Appendix A |

---

## 3. Structural Wiring & Quarantine Rules

```mermaid
graph TD
    subgraph Root Hypotheses [Root Layer: Open Problems [O]]
        R1["Root 1: μ(x) Action Closure & Dual-Channel Identity"]
        R2["Root 2: a₀ Horizon Scale"]
        R3["Root 3: Ω_Λ = ln 2 Cosmology"]
    end

    subgraph Bridges [Bridge Layer: Field Reductions & Benchmarks [C]/[D]]
        B1["AQUAL Weak-Field Field Equation [C]"]
        B2["SPARC 171-Galaxy Empirical Fits [D]"]
        B3["Honest Out-of-Sample CV & Bootstrap [D]"]
    end

    subgraph Leaves [Leaf Layer: Lean 4 Kernel Verified [P] (17 Modules)]
        L1["DualChannelDerivation.lean"]
        L2["GODActionKinematics.lean"]
        L3["ITActionClosure.lean"]
        L4["MuProjection.lean"]
        L5["SOCasimirGenuine.lean"]
        L6["DeSitterExtremal.lean"]
        L7["TensorSpeed.lean"]
        L8["CovariantCompletion.lean"]
        L9["SkordisZlosnikEmbedding.lean"]
        L10["Other Tracked Modules (17 total)"]
    end

    R1 --> B1
    R2 --> B2
    B1 --> B2
    B2 --> B3
    L1 -.->|Mathematical Identity| R1
    L2 -.->|Polynomial Kinematics| R1
    L4 -.->|Trig Geometry| R1
```

### Quarantine Directives
1. **Quarantine of Unproved Cosmological Attractors:** Narrative claims asserting that $\Omega_\Lambda = \ln 2$ is a "derived prediction" are strictly quarantined to the *Motivational Narrative Annex* until a covariant curved-spacetime Lagrangian derivation is produced.
2. **Quarantine of Silent Constitutive Inversion:** In all technical documentation, single-channel $\operatorname{arcsinh}$ is quarantined as correspondence-false (`PAPER_01_NOTICE.md`). Dual-channel $\mu(x)=x/(1+x)$ is proved `[P]` as an algebraic derivative identity, with its physical uniqueness in nature tagged `[O]`.
3. **Hard Boundary on Kernel Verification:** `[P]` tags exclusively certify deductive inference within Lean's kernel from stated definitions; they certify zero physical ontology.
