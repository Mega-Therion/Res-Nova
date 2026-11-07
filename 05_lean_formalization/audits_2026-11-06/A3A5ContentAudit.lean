/-!
# A3 / A5 content audit — self-contained, no Mathlib

Companion to `A2ContentAudit.lean`. That file showed A2 as formalized in
`AXIOMS_V2.lean` is vacuous. This file applies the same test to A3 and A5, and
finds a different defect in each:

- **A3 is vacuous.** Its single field quantifies over a set and a real, but the
  only constraint is `S_max ≥ 0`, which every carrier satisfies by taking
  `S_max = 0`. The instance below is constructed for an *arbitrary* `Q`.
- **A5 is redundant, not vacuous.** Its `newtonian_limit` field is
  character-for-character the third conjunct of
  `IsInterpolationFunction` in A4's `closure_is_interpolation`. A5 therefore
  adds no content to the axiom set: it is derived, not assumed.

Consequence for the ledger: of the five "core physical axioms", A2 is
vacuous as formalized, A3 is vacuous, and A5 is a theorem of A4. The set that
does independent work is {A1, A4}.

## Fidelity note (read before citing)

`AXIOMS_V2.lean` is written over `ℝ` and `Real.sqrt`, which require Mathlib.
This file is written against core Lean 4 only, replacing `ℝ` by `Rat`, so it
re-runs without the pinned dependency — the same house pattern as the A2 audit.

Two shape differences, both in the conservative direction:

1. A3's carrier field type is unchanged (`Set Q`, `Rat` for `ℝ`).
2. `A4Shape` below omits `weak_field_balance`, because `Real.sqrt` is not in
   core. Omitting a conjunct only *weakens* A4. The derivation `A4 ⇒ A5` is
   therefore established for a strictly weaker hypothesis than the real A4, so
   it holds a fortiori for the full class.

All statements are kernel-checked `[P]` about the *formal text*. None is a
physics result.
-/

namespace A3A5Audit

-- =========================================================================
-- A3 — vacuity
-- =========================================================================

/-- A3 as formalized in `AXIOMS_V2.lean`, with `ℝ` replaced by `Rat`.
The prose says the vacuum extremizes entanglement entropy at fixed boundary
volume; the formal field says only that *some* non-negative number exists. -/
class A3Shape (Q : Type) : Prop where
  maximal_vacuum_entanglement : ∀ (_V : Q → Prop), ∃ (S_max : Rat), S_max ≥ 0

/-- The vacuity statement in its sharpest form: A3 as formalized is satisfied
on *every* carrier, so it excludes nothing and constrains no physics. -/
theorem a3_holds_for_every_carrier (Q : Type) : A3Shape Q :=
  ⟨fun _ => ⟨0, by decide⟩⟩

/-- Consequently A3 cannot distinguish a carrier with a genuine entropy
extremum from one with none: any two carriers both satisfy it. -/
theorem a3_admits_no_extremum : A3Shape Empty := a3_holds_for_every_carrier Empty

-- =========================================================================
-- A5 — redundancy
-- =========================================================================

/-- `IsInterpolationFunction` from `AXIOMS_V2.lean:38`, transcribed to `Rat`.
Its **third** conjunct is exactly A5's `newtonian_limit`. -/
def IsInterpolationFunction (μ : Rat → Rat) : Prop :=
  (∀ x, x > 0 → μ x > 0) ∧
  (∀ ε, ε > 0 → ∃ δ, δ > 0 ∧ ∀ x, 0 < x ∧ x < δ → Rat.abs (μ x - x) < ε) ∧
  (∀ ε, ε > 0 → ∃ K, K > 0 ∧ ∀ x, x > K → Rat.abs (μ x - 1) < ε)

/-- A4 as formalized, minus the `Real.sqrt` conjunct (see fidelity note).
Keeps the field name so the derivation mirrors the file. -/
class A4Shape (μ : Rat → Rat) : Prop where
  closure_is_interpolation : IsInterpolationFunction μ

/-- A5 as formalized in `AXIOMS_V2.lean:66`. -/
class A5Shape (μ : Rat → Rat) : Prop where
  newtonian_limit : ∀ ε, ε > 0 → ∃ K, K > 0 ∧ ∀ x, x > K → Rat.abs (μ x - 1) < ε

/-- **A5 follows from A4.** Given only A4's interpolation conjunct, A5's field
is supplied verbatim by the third conjunct. No physics is added by assuming A5
once A4 is in force, so A5 is not an independent axiom. -/
theorem a5_derived_from_a4 (μ : Rat → Rat) (h : A4Shape μ) : A5Shape μ :=
  ⟨h.closure_is_interpolation.2.2⟩

/-- The redundancy is not an artifact of a trivial A4: any `IsInterpolationFunction`
witnesses A5, so the implication holds on the whole inhabited family. -/
theorem a5_derived_from_interpolation (μ : Rat → Rat)
    (h : IsInterpolationFunction μ) : A5Shape μ :=
  ⟨h.2.2⟩

-- =========================================================================
-- What survives
-- =========================================================================

/- A1 is not audited here: its statement needs the Mathlib normed and
inner-product classes, so it does not compile in a core-only file. Unlike A2 and
A3 it is not satisfiable on every carrier — the zero space admits no unit vector
— so it carries content; that contrast is the point of the A2/A3 results. -/

/-- A4 carries content: the interpolation conjunct is falsifiable in the sense
that specific functions fail it (the constant `0` fails the first conjunct). -/
theorem a4_not_vacuous : ¬ IsInterpolationFunction (fun _ => 0) := by
  intro h
  have h1 := h.1 1 (by decide)
  exact absurd h1 (by decide)

end A3A5Audit

-- Kernel-dependency receipt
#print axioms A3A5Audit.a3_holds_for_every_carrier
#print axioms A3A5Audit.a3_admits_no_extremum
#print axioms A3A5Audit.a5_derived_from_a4
#print axioms A3A5Audit.a5_derived_from_interpolation
#print axioms A3A5Audit.a4_not_vacuous
