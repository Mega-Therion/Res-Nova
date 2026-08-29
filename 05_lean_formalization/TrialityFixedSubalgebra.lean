import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import TrialityG2

/-!
# The Triality-Fixed Subalgebra — the finite content

D49 computes that the subalgebra of `so(8)` fixed by the order-3 triality has
rank 2 and dimension 14, i.e. `g₂`. This file machine-checks the parts of that
computation which are finite and decidable.

## What is proved

* the fixed Cartan subspace is characterised **exactly** — not merely bounded —
  by two linear conditions, from which rank 2 follows;
* triality scales norms by exactly 4 (so `T` is an isometry), hence it maps the
  norm-2 root vectors of `D₄` to norm-2 vectors;
* `T` maps the root lattice into itself with the factor of 2 that `M = 2T`
  requires, so roots go to roots.

## What is NOT proved

That the fixed subalgebra **is** `g₂`, or that `dim = 2 + 6 + 6 = 14`. That count
needs the Lie-theoretic decomposition of a fixed subalgebra into a fixed Cartan
plus one invariant vector per root orbit — structure Mathlib does not carry for
`so(8)`. The orbit census (6 fixed roots, 6 orbits of size 3) is computed in
`verify_triality_g2_fixed_subalgebra.py` and is tagged `[D]` in D49, not `[P]`.

**Substitutability.** Each theorem constrains `M`'s actual entries. `TrialityG2`
demonstrates this directly: flipping a single entry breaks orthogonality,
order-3, and the parity claim.
-/

namespace Triality

open Matrix

/-- **The fixed subspace, characterised exactly.**
`T v = v` — equivalently `M v = 2v` — holds precisely when the last coordinate
vanishes and the first is the sum of the middle two. The solution set is
therefore `{(b + c, b, c, 0)}`, spanned by `(1,1,0,0)` and `(1,0,1,0)`: a
**rank-2** space, which is the rank of `g₂`.

This is an `iff`, so it pins the fixed space exactly rather than exhibiting
some fixed vectors and stopping. -/
theorem fixed_subspace_char (v : Fin 4 → ℤ) :
    M.mulVec v = 2 • v ↔ (v 3 = 0 ∧ v 0 = v 1 + v 2) := by
  constructor
  · intro h
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    have h3 := congrFun h 3
    simp [M, Matrix.mulVec, dotProduct, Fin.sum_univ_four] at h0 h1 h3
    constructor <;> linarith
  · rintro ⟨h3, h0⟩
    ext i
    fin_cases i <;>
      simp [M, Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> linarith

/-- The two spanning vectors of the fixed subspace are fixed. -/
theorem fixed_basis_one : M.mulVec ![1, 1, 0, 0] = 2 • ![1, 1, 0, 0] := by
  rw [fixed_subspace_char]; refine ⟨by simp, by simp⟩

theorem fixed_basis_two : M.mulVec ![1, 0, 1, 0] = 2 • ![1, 0, 1, 0] := by
  rw [fixed_subspace_char]; refine ⟨by simp, by simp⟩

/-- They are linearly independent: no scalar multiple of one is the other. -/
theorem fixed_basis_independent (a b : ℤ)
    (h : ∀ i, a * (![1, 1, 0, 0] : Fin 4 → ℤ) i + b * (![1, 0, 1, 0] : Fin 4 → ℤ) i = 0) :
    a = 0 ∧ b = 0 := by
  have h1 := h 1
  have h2 := h 2
  simp at h1 h2
  exact ⟨h1, h2⟩

/-- **Triality is an isometry.** `‖M v‖² = 4‖v‖²`, so `T = M/2` preserves the
quadratic form. Consequently `T` sends the norm-2 roots of `D₄` to norm-2
vectors — a necessary condition for permuting the root system, and the reason
the orbit census is a census of roots rather than of arbitrary vectors.

Expanded directly rather than derived from `M_orthogonal`: the two are
equivalent here, and the direct expansion is the shorter route. -/
theorem norm_scaled_by_four (v : Fin 4 → ℤ) :
    (∑ i, (M.mulVec v i) ^ 2) = 4 * ∑ i, (v i) ^ 2 := by
  simp [M, Matrix.mulVec, dotProduct, Fin.sum_univ_four]
  ring

/-- **Integrality.** Every entry of `M v` has the same parity as `∑ v i`, so on
the root lattice (where the coordinate sum is even) `M v` has all-even entries
and `T v = (M v)/2` is again integral. This is what lets `T` act on the lattice
at all. -/
theorem mulVec_entry_parity (v : Fin 4 → ℤ) (i : Fin 4) :
    ∃ k : ℤ, M.mulVec v i = (∑ j, v j) - 2 * k := by
  fin_cases i <;>
    simp [M, Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;>
    [exact ⟨0, by ring⟩; exact ⟨v 2 + v 3, by ring⟩;
     exact ⟨v 1 + v 3, by ring⟩; exact ⟨v 0 + v 3, by ring⟩]

end Triality
