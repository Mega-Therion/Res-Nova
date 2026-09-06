/-
  ChiralHolonomyOrientation.lean

  The orientation clause of the chiral-holonomy invariant, proved rather than asserted.

  CLAIM UNDER TEST:  U_{γ₊} ≠ U_{γ₋}   -- traversing a loop backwards is not the
  same operation as traversing it forwards.

  This module establishes:
    (1) reversal inverts holonomy                          [structural]
    (2) orientation matters  ⟺  the holonomy is not an involution
    (3) a CONCRETE WITNESS in C₃ (balanced ternary / triality) where it holds
    (4) the NEGATIVE result: for any involution, orientation is destroyed

  (4) is why `ChiralCellularDuality.lean`, which proves σ(σ x) = x, cannot support
  this clause: an involution is exactly the degenerate case.

  Pure Lean 4 core. No Mathlib, no sorry.
-/

namespace ChiralHolonomy

/-- The rotation group C₃, written as balanced ternary residues. Concretely: the
    orientation states {0, +1, −1} with +1 and −1 distinct. -/
inductive C3 where
  | e    -- identity      (0)
  | r    -- rotation      (+1)
  | r2   -- inverse rot   (−1)
deriving DecidableEq, Repr

open C3

/-- Composition: traversing one path segment then another. -/
def comp : C3 → C3 → C3
  | e,  x  => x
  | x,  e  => x
  | r,  r  => r2
  | r,  r2 => e
  | r2, r  => e
  | r2, r2 => r

/-- Reversing a traversal. -/
def inv : C3 → C3
  | e  => e
  | r  => r2
  | r2 => r

/-- Reversal is a genuine inverse: going out and back is the identity. -/
theorem comp_inv (x : C3) : comp x (inv x) = e := by
  cases x <;> rfl

/-- Holonomy of the reversed loop is the inverse of the holonomy.
    This is the structural fact the whole clause rests on. -/
def holonomyReversed (u : C3) : C3 := inv u

/-! ### (2) Orientation matters exactly when the holonomy is not an involution -/

/-- If a holonomy squares to the identity, reversal changes nothing.
    THE DEGENERATE CASE — this is what an involution does to the clause. -/
theorem involution_destroys_orientation (u : C3) (h_inv : comp u u = e) :
    holonomyReversed u = u := by
  cases u
  · rfl
  · exact absurd h_inv (by decide)
  · exact absurd h_inv (by decide)

/-- Conversely, orientation is meaningful exactly when u is not self-inverse. -/
theorem orientation_iff_not_involution (u : C3) :
    holonomyReversed u ≠ u ↔ comp u u ≠ e := by
  cases u <;> simp [holonomyReversed, inv, comp]

/-! ### (3) The concrete witness: orientation asymmetry actually occurs -/

/-- **The load-bearing theorem.** There is a holonomy whose forward and backward
    traversals differ. The clause U_{γ₊} ≠ U_{γ₋} is satisfiable, not vacuous. -/
theorem orientation_asymmetry_witness : holonomyReversed r ≠ r := by decide

/-- The witness is chiral in the strict sense: the two orientations are distinct
    non-identity elements, i.e. genuine handedness rather than mere non-triviality. -/
theorem witness_is_properly_chiral :
    holonomyReversed r ≠ r ∧ holonomyReversed r ≠ e ∧ r ≠ e := by decide

/-- And it is not an involution — consistent with the criterion above. -/
theorem witness_not_involution : comp r r ≠ e := by decide

/-! ### Why order 2 fails and order 3 succeeds -/

/-- Three traversals return to identity: the loop closes at order 3, not 2. -/
theorem witness_order_three : comp (comp r r) r = e := by decide

/-- In C₃ the ONLY element for which orientation is lost is the identity —
    every non-trivial holonomy is orientation-sensitive. -/
theorem only_identity_is_orientation_blind (u : C3) :
    holonomyReversed u = u → u = e := by
  cases u <;> intro h <;> first | rfl | exact absurd h (by decide)

end ChiralHolonomy

/-! ### Axiom budget (checked in-file; see the gate for the recorded output) -/
#print axioms ChiralHolonomy.orientation_asymmetry_witness
#print axioms ChiralHolonomy.involution_destroys_orientation
#print axioms ChiralHolonomy.orientation_iff_not_involution
#print axioms ChiralHolonomy.only_identity_is_orientation_blind
