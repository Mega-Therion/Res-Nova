# AXIOM LEDGER — universal description

**Status:** draft for RY adoption, 2026-11-05. Companion to the statement-form paper plan.
**Rule:** every axiom carries (i) its condition as formalized, (ii) its kill criterion, (iii) the Lean module that consumes it. An axiom without a kill criterion is a belief.

## A1 — Substrate
**Lean:** `ChyrenAxioms.Axiom_A1_Substrate` (`05_lean_formalization/AXIOMS_V2.lean`)
**Condition:** a complex inner-product space Q contains a unit vector (`substrate_exists`).
**Consumed by:** `QuantumSubstrate`; Pillar II modules.
**Kill criterion:** no physical sector requires Hilbert-space structure, or a constructed sector needs a non-Hilbert primitive.

## A2 — Entanglement geometry
**Lean:** `ChyrenAxioms.Axiom_A2_EntanglementGeometry`
**Condition:** spacetime M carries a non-negative distance functional; in prose, distance is a monotone functional of relative entropy. Note: the formalized content is only `dist x y ≥ 0`, so it proves almost nothing. Strengthen before citing as geometry.
**Kill criterion:** a measured metric that cannot be written as a monotone functional of entanglement entropy at the relevant scale.

## A3 — Equilibrium
**Lean:** `ChyrenAxioms.Axiom_A3_Equilibrium`
**Condition:** the vacuum locally extremizes entanglement entropy at fixed boundary volume.
**Kill criterion:** a vacuum configuration with lower entropy at fixed boundary volume, or evidence the vacuum is not an entropy extremum.

## A4 — Variational closure
**Lean:** `ChyrenAxioms.Axiom_A4_VariationalClosure`
**Condition:** mu is an interpolation function and satisfies one of two branches: x/(1+x) or x/sqrt(1+x^2).
**Status:** the disjunction is collapsed inside the formal system by `MuStdSelection.screening_selects_mu_std` (`ScreenedTail` holds for mu_std via `mu_std_screened`; fails for mu_dual for every constant via `mu_dual_not_screened`). The branch is therefore not free.
**Kill criterion:** an observation showing a non-screening tail, or a proof that no interpolation function in this family follows from the action.

## A5 — Recovery
**Lean:** `ChyrenAxioms.Axiom_A5_Recovery`
**Condition:** mu → 1 at large x (Newtonian limit); GR recovered in the strong field.
**Kill criterion:** a strong-field or PPN measurement inconsistent with gamma = 1 under the stated completion. Live pressure point: the unscreened external-field quadrupole fails Cassini at 9.68 sigma.

## Derived, not axiomatic (named for the record)
- `MasterEquationCore.canonical_constitutive_identity`: F_std'(x) = x mu_std(x).
- `MuStdSelection.mu_std_screened`, `mu_dual_not_screened`, `screening_selects_mu_std`.
- `AXIOMS_V2.derived_simple_mu_bounds`, `deep_mond_baryonic_scaling`.
- `MuStdUniqueness.*`: structural uniqueness under the chiral channel (postulate swap; read its creation frame).

## Effectively axiomatic, not yet formalized
- `a0 = c H0 / (2 pi)` — anchor; the 2 pi is declared, not derived. This is the emblem-level gap.
- Substrate → mu shape (Q3): no derivation exists.
- Standard Model import: gauge group, representations, couplings are `[C]`.

## Addendum — E.H.Y.E.H. manuscript consequences
The manuscript's equations inherit these labels. Items the audit marked [X] are not axioms and must not be presented as theorems: the cH0/2pi "derivation", the Cassini pass, the ghost-free inverse from eqs. 30-32, Table II, and "without free parameters".
