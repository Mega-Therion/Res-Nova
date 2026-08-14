# 🗺️ Corpus Dependency & Inversion Map
**Framework:** Chyren / Res-Nova Epistemic Architecture  
**Author:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Date:** 2026-08-14  
**Primary Dataset:** 138 Master LaTeX Documents ([`corpus_graph.json`](file:///home/mega/grand_monograph/corpus_graph.json))

---

## 1. Classification Topology (The 3 Node Types)

Every document, claim, and equation in the 138-manuscript corpus is categorized into one of three functional node types:

1. **Root Nodes (`[O]` Research Targets):** Foundational hypotheses upon which downstream results depend, but which currently lack first-principles variational proofs (e.g., the $\mu(x)$ closure, the $a_0$ scale normalization, the $\Omega_\Lambda = \ln 2$ cosmology conjecture).
2. **Bridge Nodes (Intermediate Reductions & Fits):** Manifold reductions, AQUAL Euler–Lagrange expansions, and SPARC empirical calibrations that connect root hypotheses to physical observables.
3. **Leaf Nodes (`[P]` Formally Certified Theorems):** Mechanically kernel-verified algebraic propositions in Lean 4 (e.g., Casimir eigenvalues, spectral gaps, polynomial identities) whose mathematical validity is independent of physical ontology.

---

## 2. Global Claim & Dependency Inversion Table

| Node ID / Manuscript | Primary Assertion | Epistemic Tier | Support Type | Upstream Dependencies | Downstream Consumers |
|---|---|---|---|---|---|
| **Root 1: $\mu(x)$ Closure** | Variational action yields rational simple-$\mu$ | `[O]` Open Problem | Variational calculation + Assumed Projection | None (Primitive Hypothesis) | All SPARC fits, Paper 09, Monograph §2 |
| **Root 2: $a_0$ Scale** | $a_0 = c H_0 / (2\pi)$ from horizon thermodynamics | `[O]` Null/Negative Result | KMS temperature matching (cancels $2\pi$) | De Sitter horizon equilibrium | All zero-parameter galactic benchmarks |
| **Root 3: $\Omega_\Lambda = \ln 2$** | Dark energy density matches 1-qubit Shannon limit | `[O]` Conjectural Limit | Entanglement entropy bound ($S_E \le \ln 2$) | Qubit state factorization | Cosmological expansion notes |
| **Bridge 1: Weak-Field AQUAL** | $\nabla\cdot[\mu(|\nabla\Phi|/a_0)\nabla\Phi] = 4\pi G\rho$ | `[C]` Cited Literature | Bekenstein-Milgrom (1984) field theory | Action Principle | SPARC rotation curves |
| **Bridge 2: 5-Fold Cross-Val** | Out-of-sample generalization median $\chi^2/N_g = 14.68$ | `[D]` Empirical Benchmark | 175 SPARC galaxies / 3,391 kinematic points | Fixed population priors | Generalization bounds |
| **Leaf 1: `GODActionKinematics`** | Dual-channel $\tau$-tension polynomial equivalence | `[P]` Kernel Verified | Lean 4 / Mathlib proof (`0 sorry`) | Standard Lean logic | Manuscript Appendix A |
| **Leaf 2: `MuProjection`** | Trigonometric mapping $\mu(x) = \cos(\arctan(1/x))$ | `[P]` Kernel Verified | Lean 4 / Mathlib proof (`0 sorry`) | Standard Lean logic | Manuscript Appendix A |
| **Leaf 3: `SOCasimirGenuine`** | $\mathfrak{so}(n)$ quadratic Casimir scalar eigenvalues | `[P]` Kernel Verified | Lean 4 / Mathlib proof (`0 sorry`) | Standard Lean logic | Manuscript Appendix A |
| **Leaf 4: `DeSitterExtremal`** | Static de Sitter horizon lapse function zero | `[P]` Kernel Verified | Lean 4 / Mathlib proof (`0 sorry`) | Standard Lean logic | Manuscript Appendix A |
| **Leaf 5: `YettParadigm`** | Ramanujan-Yett modular Hamiltonian spectral gap | `[P]` Kernel Verified | Lean 4 / Mathlib proof (`0 sorry`) | Standard Lean logic | Manuscript Appendix A |
| **Leaf 6: `SovereignRegularity`** | Beale-Kato-Majda conditional Sobolev regularity | `[P]` Kernel Verified | Lean 4 / Mathlib proof (`0 sorry`) | Standard Lean logic | Manuscript Appendix A |

---

## 3. The 3 Structural Wiring Faults & Quarantine Rules

```mermaid
graph TD
    subgraph Root Hypotheses [Root Layer: Open Problems [O]]
        R1["Root 1: μ(x) Action Closure"]
        R2["Root 2: a₀ Horizon Scale"]
        R3["Root 3: Ω_Λ = ln 2 Cosmology"]
    end

    subgraph Bridges [Bridge Layer: Field Reductions & Benchmarks [C]/[D]]
        B1["AQUAL Weak-Field Field Equation [C]"]
        B2["SPARC 175-Galaxy Empirical Fits [D]"]
        B3["5-Fold Out-of-Sample CV [D]"]
    end

    subgraph Leaves [Leaf Layer: Lean 4 Kernel Verified [P]]
        L1["GODActionKinematics.lean"]
        L2["ITActionClosure.lean"]
        L3["MuProjection.lean"]
        L4["SOCasimirGenuine.lean"]
        L5["DeSitterExtremal.lean"]
        L6["YettParadigm.lean"]
        L7["SovereignRegularity.lean"]
    end

    R1 --> B1
    R2 --> B2
    B1 --> B2
    B2 --> B3
    L1 -.->|Mathematical Identity| R1
    L3 -.->|Trig Geometry| R1
```

### Quarantine Directives
1. **Quarantine of Unproved Cosmological Attractors:** Narrative claims asserting that $\Omega_\Lambda = \ln 2$ is a "derived prediction" are strictly quarantined to the *Motivational Narrative Annex* until a covariant curved-spacetime Lagrangian derivation is produced.
2. **Quarantine of Silent Constitutive Inversion:** In all technical documentation, $\mu_{\text{simple}}(x)$ must be labeled as an *empirical/algebraic constitutive projection hypothesis $\mathbf{[O]}$*, never as an unconditioned consequence of single-channel variational calculus.
3. **Hard Boundary on Kernel Verification:** `[P]` tags exclusively certify deductive inference within Lean's kernel from stated definitions; they certify zero physical ontology.
