import Mathlib.Data.Fintype.Card
import Mathlib.Tactic
import E8Roots
import Mathlib.Algebra.Lie.Prod
import Mathlib.Algebra.Lie.SerreConstruction

/-!
# E8 × E8 Root-Data and Serre-Lie Bridge

This adjacent module reuses the finite E8 root subtype proved in `E8Roots.lean`.
It tags two disjoint root-data copies and counts 480 roots. It also names
Mathlib's Serre-presentation E8 Lie algebra, forms the direct product of two
such algebras, and proves that the Res-Nova simple-root Gram matrix matches
Mathlib's E8 Cartan matrix after a node reindexing.

The Cartan-matrix match does not identify the existing vector subtype with the
Lie algebra's root spaces or prove a root-space decomposition, dimension 248,
simplicity, or an isomorphism to a separately constructed Lie algebra. This is
not a construction of a heterotic gauge theory, M-theory compactification, or
derivation of Res-Nova's modified-gravity law, scalar couplings, or a₀. See
`06_unification_and_spin/STRING_M_THEORY_BRIDGE.md` for the boundary between
formal mathematics and physical claims.
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

noncomputable section

/-- Mathlib's Serre-presentation Lie algebra of type E8 over `R`. -/
abbrev E8SerreLieAlgebra (R : Type*) [CommRing R] := LieAlgebra.e₈ R

/-- The direct product of two E8 Serre Lie algebras over `R`. -/
abbrev E8xE8SerreLieAlgebra (R : Type*) [CommRing R] :=
  E8SerreLieAlgebra R × E8SerreLieAlgebra R

/-- The E8 Serre bracket satisfies the Lie-ring Leibniz/Jacobi identity. -/
theorem e8Serre_bracket_leibniz_lie {R : Type*} [CommRing R]
    (x y z : E8SerreLieAlgebra R) :
    ⁅x, ⁅y, z⁆⁆ = ⁅⁅x, y⁆, z⁆ + ⁅y, ⁅x, z⁆⁆ :=
  LieRing.leibniz_lie x y z

/-- The E8×E8 product bracket acts componentwise on both factors. -/
theorem e8xE8Serre_bracket_components {R : Type*} [CommRing R]
    (x y : E8xE8SerreLieAlgebra R) :
    ⁅x, y⁆ = (⁅x.1, y.1⁆, ⁅x.2, y.2⁆) :=
  LieAlgebra.Prod.bracket_apply x y

/-- Distinct factors in the product Lie algebra have zero cross-bracket. -/
theorem e8xE8Serre_cross_bracket {R : Type*} [CommRing R]
    (x y : E8SerreLieAlgebra R) :
    ⁅(x, (0 : E8SerreLieAlgebra R)), ((0 : E8SerreLieAlgebra R), y)⁆ = 0 := by
  rw [e8xE8Serre_bracket_components]
  simp

/-- Reindex the Res-Nova simple roots into Mathlib's E8 Cartan-matrix order. -/
def e8CartanNodeReindex : Fin 8 ≃ Fin 8 :=
  Equiv.ofBijective
    (![7, 6, 5, 4, 3, 2, 0, 1] : Fin 8 → Fin 8)
    (by decide)

/-- The Res-Nova Cartan matrix is Mathlib's E8 matrix under `e8CartanNodeReindex`. -/
theorem e8_cartan_reindex_matches (i j : Fin 8) :
    ResNova.E8Roots.cartanE8 i j =
      CartanMatrix.E₈ (e8CartanNodeReindex i) (e8CartanNodeReindex j) := by
  fin_cases i <;> fin_cases j <;> decide

/-- The doubled-coordinate simple-root Gram matrix is four times Mathlib's E8 Cartan matrix. -/
theorem simpleRoot_gram_eq_reindexed_cartan (i j : Fin 8) :
    ResNova.E8Roots.dot (ResNova.E8Roots.simpleRoot i) (ResNova.E8Roots.simpleRoot j) =
      4 * CartanMatrix.E₈ (e8CartanNodeReindex i) (e8CartanNodeReindex j) := by
  rw [ResNova.E8Roots.gram_eq_four_cartan, e8_cartan_reindex_matches]

end

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
#print axioms e8Serre_bracket_leibniz_lie
#print axioms e8xE8Serre_bracket_components
#print axioms e8xE8Serre_cross_bracket
#print axioms e8_cartan_reindex_matches
#print axioms simpleRoot_gram_eq_reindexed_cartan

end ResNova.StringTheoryBridge
