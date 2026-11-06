/-!
# A2 content audit — self-contained, no Mathlib

`AXIOMS_V2.lean` states Axiom A2 (Entanglement Geometry) in prose as
"spacetime distance is a monotone functional of quantum relative entropy",
but formalizes only

    geometric_emergence : ∃ (dist : M → M → ℝ), ∀ x y : M, dist x y ≥ 0

This file checks what that formalization actually constrains. It is written
against core Lean 4 only (no Mathlib) so it can be re-run without the pinned
dependency, which is exactly why it is kept out of the Mathlib gate targets.

Tag legend follows docs/EPISTEMIC_TIER_LEGEND.md: these are kernel-checked
statements [P] about the *formal text*, not physics results.
-/

namespace A2Audit

/-- The formal content of A2 as written in AXIOMS_V2.lean, over `Bool` as a
two-point carrier standing in for `M`. -/
def A2Shape (dist : Bool → Bool → Rat) : Prop := ∀ x y, dist x y ≥ 0

/-- A two-point divergence that is deliberately asymmetric, modeling the fact
that quantum relative entropy S(ρ‖σ) is not symmetric. -/
def Dtoy : Bool → Bool → Rat
  | true, false => 1
  | _, _ => 0

/-- The zero "distance" satisfies A2 as formalized. -/
theorem a2_admits_zero : A2Shape (fun _ _ => 0) := by
  intro x y
  exact Rat.le_refl

/-- So does every non-negative function, including one that is not a metric:
`Dtoy` is non-negative but asymmetric. -/
theorem a2_admits_nonmetric : ∃ dist : Bool → Bool → Rat,
    A2Shape dist ∧ dist true false ≠ dist false true := by
  refine ⟨Dtoy, ?_, ?_⟩
  · intro x y
    cases x <;> cases y <;> decide
  · decide

/-- The vacuity statement in its sharpest form: A2 as formalized is satisfied
by a function that fails the metric axiom of symmetry, so it does not constrain
the geometry it is supposed to define. -/
theorem a2_does_not_imply_symmetry :
    ¬ (∀ dist : Bool → Bool → Rat, A2Shape dist → dist true false = dist false true) := by
  intro h
  have := h Dtoy (by intro x y; cases x <;> cases y <;> decide)
  exact absurd this (by decide)

/-- Distance built as a monotone functional of an asymmetric divergence
inherits the asymmetry: symmetrization is a separate choice, not a consequence
of A2. `f = id` is monotone, so this is the weakest possible instance. -/
def distFromDiv (f : Rat → Rat) (D : Bool → Bool → Rat) : Bool → Bool → Rat :=
  fun x y => f (D x y)

theorem monotone_of_asymm_is_asymm :
    distFromDiv id Dtoy true false ≠ distFromDiv id Dtoy false true := by
  decide

/-- Consequently a monotone-functional-of-relative-entropy "distance" is a
metric only after an explicit symmetrization step, which A2 does not supply. -/
theorem symmetrization_not_supplied_by_A2 :
    A2Shape (distFromDiv id Dtoy) ∧
      ¬ (distFromDiv id Dtoy true false = distFromDiv id Dtoy false true) := by
  refine ⟨?_, ?_⟩
  · intro x y
    cases x <;> cases y <;> decide
  · decide

end A2Audit

#print axioms A2Audit.a2_admits_zero
#print axioms A2Audit.a2_admits_nonmetric
#print axioms A2Audit.a2_does_not_imply_symmetry
#print axioms A2Audit.monotone_of_asymm_is_asymm
#print axioms A2Audit.symmetrization_not_supplied_by_A2
