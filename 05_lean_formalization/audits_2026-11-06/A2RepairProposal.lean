/-!
# A2 repair proposal — self-contained, no Mathlib

The audit above shows A2 as written is satisfied by `dist ≡ 0` and by
asymmetric divergences. This file states the repair and kernel-checks that the
repair excludes those cases, i.e. that it is not vacuous.

All statements are kernel-checked [P] about the formal text.
-/

namespace A2Repair

variable {M : Type}

/-- Proposed A2, three conjuncts, all expressible without Mathlib:

1. `nonneg`      — the original content, kept.
2. `refl_zero`   — identity of indiscernibles at zero distance.
3. `symm`        — symmetry, which the raw relative entropy does not have.

The physics content ("monotone functional of relative entropy") remains a
definition of the intended *construction*, not a constraint; see §Notes. -/
structure A2Strong (dist : M → M → Rat) : Prop where
  nonneg : ∀ x y, dist x y ≥ 0
  refl_zero : ∀ x y, dist x y = 0 → x = y
  symm : ∀ x y, dist x y = dist y x

/-- The zero distance is now excluded: it violates identity of indiscernibles
on any carrier with two distinct points. -/
theorem zero_excluded (a b : M) (hne : a ≠ b) :
    ¬ A2Strong (fun _ _ => (0 : Rat)) := by
  intro hs
  exact hne (hs.refl_zero a b rfl)

/-- An asymmetric divergence is now excluded on the same carrier. -/
def Dtoy : Bool → Bool → Rat
  | true, false => 1
  | _, _ => 0

theorem asymmetric_excluded : ¬ A2Strong Dtoy := by
  intro hs
  have h := hs.symm true false
  exact absurd h (by decide)

/-- A witness: the repaired A2 is satisfiable, so the repair is not itself
vacuous. `Bool` with the discrete metric. -/
def dBool (x y : Bool) : Rat := if x = y then 0 else 1

theorem repair_satisfiable : A2Strong dBool := by
  refine ⟨?_, ?_, ?_⟩
  · intro x y
    unfold dBool
    split <;> decide
  · intro x y h
    unfold dBool at h
    split at h
    · assumption
    · exact absurd h (by decide)
  · intro x y
    unfold dBool
    by_cases h : x = y
    · rw [if_pos h, if_pos h.symm]
    · rw [if_neg h, if_neg (Ne.symm h)]

end A2Repair

#print axioms A2Repair.zero_excluded
#print axioms A2Repair.asymmetric_excluded
#print axioms A2Repair.repair_satisfiable
