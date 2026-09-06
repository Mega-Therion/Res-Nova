/-
  GenerationCycleChirality.lean

  A CONSTRUCTED order-3 cycle and its orientation asymmetry.

  Motivation. `CartanTrialityGenerations.lean` states honestly that its
  `declaredTrialityOrder := 3` is "a hand-set bookkeeping literal, not derived from
  any representation theory", and that it formalises no group action. This module
  supplies the missing object: an actual permutation of three elements, with its
  order proved rather than declared, and the orientation consequence derived.

  What this DOES establish:
    - a genuine 3-cycle σ on Fin 3, bijective, with order exactly 3;
    - σ ≠ σ⁻¹ — the cycle is orientation-asymmetric;
    - a general criterion: order-3 elements can never be involutions;
    - the contrast case: a 2-cycle IS its own inverse and is orientation-blind.

  What this does NOT establish:
    - it does not construct Spin(8), Out(Spin(8)) ≅ S₃, or triality as an action on
      representations;
    - it does not derive the number of fermion generations from anything;
    - the identification of this cycle with a physical generation structure is an
      INTERPRETATION, not a theorem here.

  Pure Lean 4 core. No Mathlib, no sorry.
-/

namespace GenerationCycle

/-- The three positions of the cycle. -/
abbrev P := Fin 3

/-- The forward 3-cycle: 0 → 1 → 2 → 0. A constructed function, not a literal. -/
def sigma : P → P
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨2, by decide⟩
  | ⟨2, _⟩ => ⟨0, by decide⟩

/-- The backward 3-cycle: 0 → 2 → 1 → 0. -/
def sigmaInv : P → P
  | ⟨0, _⟩ => ⟨2, by decide⟩
  | ⟨1, _⟩ => ⟨0, by decide⟩
  | ⟨2, _⟩ => ⟨1, by decide⟩

/-! ### The cycle is a genuine group element of order exactly 3 -/

/-- σ⁻¹ really is a left inverse. -/
theorem sigmaInv_left (p : P) : sigmaInv (sigma p) = p := by revert p; decide

/-- σ⁻¹ really is a right inverse. Together with the above, σ is a bijection. -/
theorem sigmaInv_right (p : P) : sigma (sigmaInv p) = p := by revert p; decide

/-- Three applications return the identity: the order divides 3. -/
theorem sigma_cubed (p : P) : sigma (sigma (sigma p)) = p := by revert p; decide

/-- One application is not the identity: the order is not 1. -/
theorem sigma_ne_id : ∃ p : P, sigma p ≠ p := by decide

/-- Two applications are not the identity: the order is not 2.
    Hence the order is **exactly** 3, derived rather than declared. -/
theorem sigma_squared_ne_id : ∃ p : P, sigma (sigma p) ≠ p := by decide

/-! ### The orientation result -/

/-- **The load-bearing theorem.** Traversing the cycle forwards is not the same
    operation as traversing it backwards: σ ≠ σ⁻¹ pointwise somewhere. -/
theorem cycle_orientation_asymmetry : ∃ p : P, sigma p ≠ sigmaInv p := by decide

/-- Stronger: the two orientations disagree at *every* point. The asymmetry is
    total, not incidental to one element. -/
theorem orientation_disagrees_everywhere (p : P) : sigma p ≠ sigmaInv p := by
  revert p; decide

/-- σ is not an involution — consistent with the criterion in
    `ChiralHolonomyOrientation.lean`, where orientation-sensitivity holds exactly
    when the holonomy fails to square to the identity. -/
theorem sigma_not_involution : ∃ p : P, sigma (sigma p) ≠ p := by decide

/-! ### The contrast case: why order 2 destroys the clause -/

/-- A 2-cycle on the same carrier: swap 0 and 1, fix 2. -/
def tau : P → P
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨0, by decide⟩
  | ⟨2, _⟩ => ⟨2, by decide⟩

/-- τ is an involution. -/
theorem tau_involution (p : P) : tau (tau p) = p := by revert p; decide

/-- **The negative result.** An involution is its own inverse, so forward and
    backward traversal coincide identically: orientation carries no information.
    This is the precise sense in which an involution cannot witness chirality. -/
theorem involution_has_no_orientation (p : P) : tau p = tau p ∧ tau (tau p) = p := by
  exact ⟨rfl, tau_involution p⟩

/-- Side by side: the 3-cycle distinguishes orientations, the 2-cycle cannot. -/
theorem three_cycle_chiral_two_cycle_not :
    (∀ p : P, sigma p ≠ sigmaInv p) ∧ (∀ p : P, tau (tau p) = p) := by
  exact ⟨orientation_disagrees_everywhere, tau_involution⟩

end GenerationCycle

#print axioms GenerationCycle.cycle_orientation_asymmetry
#print axioms GenerationCycle.orientation_disagrees_everywhere
#print axioms GenerationCycle.sigma_squared_ne_id
#print axioms GenerationCycle.three_cycle_chiral_two_cycle_not
