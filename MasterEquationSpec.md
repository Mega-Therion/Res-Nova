# Master Equation Spec — Res Nova Formalization Spine

- **Spec ID:** `RN-ME-SPEC-0.1`
- **State:** Draft working contract; canonical covariant master action remains **open**
- **Created:** 2026-10-13
**Repository baseline:** `Mega-Therion/Res-Nova`, branch `docs/master-equation-formalization-spine`

**Linked artifacts:** [`MasterEquationTerms.csv`](MasterEquationTerms.csv) is the equation/term ledger; [`05_lean_formalization/MasterEquationCore.lean`](05_lean_formalization/MasterEquationCore.lean) is the initial typed constitutive slice; the module is registered in `05_lean_formalization/lakefile.lean` and `05_lean_formalization/verify_all_proofs.sh`.

## Objective

Create one auditable correspondence spine from the repository's surviving mathematical objects to any eventual covariant master action. The first executable slice is the corrected AQUAL `mu_std` constitutive sector. It is not a claim that the AQUAL sector, the dual-channel construction, the Einstein-aether completion, and the separate Chyren Lindblad equation already arise from one action.

## Scope and working equation identities

There is not yet one frozen full master equation. The following source identities are separated on purpose:

1. **`RN-AQUAL-CONST-001` — constitutive pair (current surviving convention).**
   `mu_std(x) = x / sqrt(1 + x^2)` and `F_std'(x) = x * mu_std(x)`, hence `F_std(x) = 1/2 * (x * sqrt(1+x^2) - asinh(x))`. Domain and variational normalization must be declared per use. The derivative convention is explicitly **not** `F' = mu`.
2. **`RN-AQUAL-FIELD-001` — non-relativistic AQUAL field equation.**
   Candidate divergence-form target: `div(mu_std(|grad Phi|/a0) grad Phi) = 4*pi*G*rho`. This spec records it as a target correspondence, not a newly derived theorem. Sign, normalization, boundary conditions, and exact `F_std` argument convention must be reconciled against the chosen action before it can be promoted to canonical.
3. **`RN-COV-ACTION-001` — covariant completion.**
   The candidate `S = integral sqrt(-g) [M_Pl^2 R/2 + L_T(A, chi)] + S_m[tilde(g), psi]` is an ansatz recorded in `COVARIANT_STRESS_ENERGY_COMPLETION.md`. Its complete variation, matter coupling, dimensions, constraints, and stability/causality status are not thereby established.
4. **`RN-DUAL-CHANNEL-001` — older dual/Pade branch.**
   `F_dual(x) = 1/2*x^2 - x + ln(1+x)` is a distinct branch. Its algebraic Legendre results do not establish equivalence to the live `mu_std` AQUAL branch or a covariant field theory.
5. **`CHY-LINDBLAD-001` — separate source framework.**
   The controlled Lindblad equation in `MASTER_EQUATION.md` describes a density-matrix dynamics. It is not silently identified with the Res Nova gravitational action. Any bridge claim needs a typed map and independently stated assumptions.

## Notation and conventions to freeze before promotion

| Symbol | Provisional meaning | Type/domain | Status / unresolved items |
|---|---|---|---|
| `x` | dimensionless gradient magnitude | `x >= 0`, scalar | Definition; specify which gradient and reference scale in each model |
| `mu_std(x)` | surviving interpolation function | `[0,∞) -> [0,1)` | Definition; phenomenological/constitutive role, not a derivation of the full theory |
| `F_std(x)` | AQUAL kinetic potential under corrected convention | `[0,∞) -> R` | Definition; `F_std' = x mu_std`; verify normalization in each action |
| `a0` | acceleration scale | positive acceleration | Empirical/model input unless a separate derivation is supplied |
| `Phi` | non-relativistic gravitational potential | scalar field on spatial domain | Specify units, regularity, boundary data, source convention |
| `rho` | baryonic mass density | scalar density | Specify measure/units and coupling normalization |
| `g_munu` | spacetime metric | Lorentzian metric | Signature and curvature sign convention not globally frozen |
| `A^mu` | unit-timelike vector/aether field in candidate completion | section of tangent bundle | Constraint, bundle, boundary data, and coefficients need explicit contracts |
| `chi` | alignment/scalar field in candidate completion | real scalar field | Potential, normalization, units and coupling remain model-specific |
| `tilde(g)_munu` | matter/disformal metric | metric-valued map | Exact map and matter-coupling variation must be declared |
| `F_dual` | distinct older dual-channel potential | positive scalar domain | Keep distinct from `F_std`; field-level physical interpretation open |
| `rho_state` | density matrix in Chyren Lindblad source | positive trace-one operator | Separate framework; not a Res Nova action field |

**Global conventions not yet fixed:** spacetime dimension (candidate 4), metric signature, orientation, curvature sign, boundary conditions, field regularity, integration measures, index conventions, and a single unit system for the eventual unified theory. For audit readability only, `MasterEquationTerms.csv` uses SI dimensions for the non-relativistic AQUAL PDE, natural units (`c = ℏ = 1`) for the covariant action candidates, and conventional operator units for the separate Lindblad source. These are per-source bookkeeping conventions, not a claim that the sectors are already normalized to one action; convert and reconcile them before unification.

## Epistemic labels

Use these labels on every row and theorem:

- `definition` — introduced by this spec or code.
- `established mathematics` — standard result with its hypotheses recorded.
- `established framework` — conventional physical formalism; exact model match still needs checking.
- `derived` — follows from an explicit in-scope derivation/proof.
- `model assumption` — selected physical ansatz or constitutive input.
- `empirical input` — measured/calibrated quantity.
- `open` — unresolved or not yet derived/verified.

Do not promote a definition, fitted input, or statement copied from a manuscript to `derived` merely because it is written as an equation or compiles in Lean.

## Capability boundary and build order

1. **Correspondence ledger:** enumerate source equations and record types, dimensions, symmetries, variational status, empirical role, and evidence.
2. **Typed constitutive slice:** formalize the `mu_std`/`F_std` scalar interface and the derivative identity, reusing existing definitions.
3. **Covariant field/action specification:** only after field spaces, units, symmetries, action density, and boundaries are explicit.
4. **Variation gate:** derive Euler–Lagrange equations, including boundary terms, from the declared action.
5. **Constraints and Legendre gate:** derive the field-level Hamiltonian and constraints under stated regularity/convexity hypotheses.
6. **Sector interfaces:** gravity, gauge, geometry, spectrum, cosmology, observations, and any Chyren bridge only through explicit contracts.

## Lean contract for the first slice

`05_lean_formalization/MasterEquationCore.lean` may establish only that the existing scalar constitutive objects are correctly composed and that the corrected derivative identity is available. It must not name that slice a covariant field equation, imply units are machine-checked, or assert that varying it yields the full Res Nova dynamics. The first type-checking boundary is scalar/algebraic; a manifold, bundle, volume form, and variational calculus are not yet encoded.

### Implementation audit against the current Lean core

| Spec question | Current implementation | Review status |
|---|---|---|
| Does the code reuse the live `mu_std` / `F_std` definitions and corrected derivative convention? | Imports `MuStdUniqueness`; `canonical_constitutive_identity` states `deriv F_std x = x * mu_std x`. | Covered in this slice; underlying theorem is reused, not re-derived here. |
| Is the normalized scalar argument typed and constrained? | `ScalarGradientData` stores a nonnegative gradient magnitude and positive reference scale; `dimensionlessGradient_nonneg` proves the quotient is nonnegative. | Covered at the abstract scalar level; no units are encoded by `ℝ`. |
| Is an AQUAL potential composition present? | `aqualKineticPotential` evaluates `F_std` on that quotient. | Covered as a scalar function only; not a spacetime Lagrangian density or action integral. |
| Are `Phi`, `rho`, a spatial metric/operator, boundary data, and the AQUAL PDE implemented? | No such field/PDE objects occur in the module. | Open; the CSV PDE row remains a model target, not a Lean theorem. |
| Are the covariant metric/vector/scalar/matter sectors, symmetries, and units encoded? | No manifold, metric, bundles, action density, or unit types occur. | Open; candidate terms remain specification/ledger entries only. |
| Is variation, the constrained Hamiltonian/Legendre map, or a Chyren/Lindblad bridge implemented? | None of these structures or maps occurs in the module. | Open; no inference is made from the scalar theorem. |

This audit therefore finds the core consistent with its intentionally narrow contract; it does **not** close the open physical derivation questions listed above.

## Acceptance criteria

- [x] Every ledger equation identity has a stable ID and a source.
- [x] The live `mu_std` convention (`F_std' = x * mu_std`) is kept separate from the older `F_dual` convention.
- [x] Each ledger term has a mathematical type and a populated unit field; source-specific bookkeeping conventions and remaining unit reconciliations are explicit.
- [x] The Chyren Lindblad dynamics is explicitly identified as separate unless and until a bridge map is given.
- [x] The Lean core imports existing canonical functions and proves no physical conclusion beyond its type/algebraic boundary.
- [x] Full action, Euler–Lagrange, Hamiltonian, and empirical derivations remain explicitly open pending their own proof/evidence gates.

## Primary sources in repository

- `01_foundational_action/COVARIANT_STRESS_ENERGY_COMPLETION.md`
- `01_foundational_action/PAPER_01_MU_DERIVATION_ACTION.tex`
- `01_foundational_action/PRD_supplementary/lean_proofs/MASTER_EQUATION.md` (separate Chyren/Lindblad source)
- `05_lean_formalization/MuStdUniqueness.lean`
- `05_lean_formalization/MuStdFoundations.lean`
- `05_lean_formalization/Hamilgrangian.lean`

## Explicitly out of scope for v0.1

No global unified-action claim; no assertion that a numerical match is a derivation; no E8/SU(2), Stiefel/holonomy, cosmological or particle-mass identification; no claim of field-level `Hamilgrangian` equivalence; no proof of a spectral gap or cognitive Lindblad correction.
