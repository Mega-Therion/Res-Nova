import Mathlib.Data.Fintype.Card
import Mathlib.Tactic
import E8Roots

/-!
# E8 × E8 Root-Data Bridge

This adjacent module reuses the finite E8 root subtype proved in `E8Roots.lean`.
It tags two disjoint copies, counts 480 roots, records the rank value 8 per
factor as explicit bookkeeping, and proves the arithmetic sum 480 + 16 = 496.

This is not a construction of the E8 Lie algebra, a heterotic gauge theory,
M-theory, a compactification, or a derivation of Res-Nova's modified-gravity
law, scalar couplings, or a₀. See `06_unification_and_spin/STRING_M_THEORY_BRIDGE.md`
for the boundary between this arithmetic and the physical literature.
-/

namespace ResNova.StringTheoryBridge

/-- The two labels used to distinguish the two E8 root-data copies. -/
inductive E8Factor where
  | left
  | right
  deriving DecidableEq

instance : Fintype E8Factor where
  elems := {E8Factor.left, E8Factor.right}
  complete := by
    intro x
    cases x <;> simp

/-- One copy of the already-formalized finite E8 root subtype. -/
abbrev E8RootSubtype :=
  { y : ResNova.E8Roots.Vec // ResNova.E8Roots.IsE8Root y }

/-- A root tagged by which factor of the E8 × E8 root data it belongs to. -/
abbrev E8xE8RootCopy := E8Factor × E8RootSubtype

/-- The two factor tags are a two-element finite type. -/
theorem e8Factor_card : Fintype.card E8Factor = 2 := by
  decide

/-- Two tagged copies contain 2 × 240 = 480 roots. -/
theorem e8xE8_root_count : Fintype.card E8xE8RootCopy = 480 := by
  simp [E8xE8RootCopy, E8RootSubtype, e8Factor_card,
    ResNova.E8Roots.e8_root_count]

/-- Explicit bookkeeping convention: assign rank 8 to each E8 factor.
This value is not derived from the root subtype in this module. -/
def e8Rank : Nat := 8

theorem e8xE8_rank_count : e8Rank + e8Rank = 16 := by
  norm_num [e8Rank]

/-- Root-count plus rank bookkeeping is 480 + 16 = 496.

This theorem concerns finite root-data cardinalities and natural-number
arithmetic only; it does not prove a Lie-algebra dimension or a physical claim.
-/
theorem e8xE8_root_plus_rank_count :
    Fintype.card E8xE8RootCopy + 16 = 496 := by
  calc
    Fintype.card E8xE8RootCopy + 16 =
        Fintype.card E8xE8RootCopy + (e8Rank + e8Rank) := by
          rw [e8xE8_rank_count]
    _ = 496 := by
      rw [e8xE8_root_count]
      norm_num [e8Rank]

#print axioms e8xE8_root_count
#print axioms e8xE8_rank_count
#print axioms e8xE8_root_plus_rank_count

end ResNova.StringTheoryBridge
