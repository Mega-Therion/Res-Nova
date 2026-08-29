import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases

/-!
# Triality and the G₂ Fixed Subalgebra — the concrete matrix facts

This file formalises the *computational* content behind D49: that the order-3
triality automorphism of `so(8)` is what it is claimed to be, and that it moves
the 8-dimensional representations the way the generation argument requires.

## What is and is not proved here

**Proved:** exact integer identities about the explicit matrix `M = 2T`, where `T`
is the triality map derived from the D4 Dynkin diagram (cycling the outer nodes
α₁ → α₃ → α₄, fixing α₂). Working with `M = 2T` keeps everything over `ℤ`, so
every statement is decidable and none of them can be closed by `rfl` on a
hand-assigned literal.

**NOT proved here:** that `G₂` is the fixed subalgebra, or that
`8ᵥ, 8ₛ, 8_c → 7 ⊕ 1`. Those need Spin(8) representation theory that Mathlib does
not have. They are computed in
`Research_and_Data/05_Scripts_and_Tools/verify_triality_g2_fixed_subalgebra.py`
and recorded as `[D]` in D49 — not `[P]`, and not claimed as such.

**Substitutability.** Every theorem below is a statement about `M`'s actual
entries. Perturb any entry and each one fails. Nothing here is a dimension
identity such as `8 = 7 + 1`, which would be arithmetic wearing a physics name.
-/

namespace Triality

/-- `M = 2T`, twice the triality automorphism, over `ℤ`.
Derived by solving `T·A = B` for the D4 outer-node cycle, then doubled. -/
def M : Matrix (Fin 4) (Fin 4) ℤ :=
  !![ 1,  1,  1,  1;
      1,  1, -1, -1;
      1, -1,  1, -1;
     -1,  1,  1, -1]

/-- `T` is orthogonal: `M Mᵀ = 4·I`, i.e. `T Tᵀ = I`. -/
theorem M_orthogonal : M * M.transpose = (4 : ℤ) • (1 : Matrix (Fin 4) (Fin 4) ℤ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [M, Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four,
          Matrix.one_apply, Matrix.smul_apply]

/-- `T` has order three: `M³ = 8·I`, i.e. `T³ = I`.
This is the property that failed for a first hand-written matrix, which turned
out to have order 2. -/
theorem M_order_three : M * M * M = (8 : ℤ) • (1 : Matrix (Fin 4) (Fin 4) ℤ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [M, Matrix.mul_apply, Fin.sum_univ_four, Matrix.one_apply, Matrix.smul_apply]

/-- Every entry of `M` is a unit, so every entry of `T` is `±1/2`. -/
theorem M_entries_unit (i j : Fin 4) : M i j = 1 ∨ M i j = -1 := by
  fin_cases i <;> fin_cases j <;> simp [M]

/-- **The representation-moving fact.** The `8ᵥ` weights are `±eᵢ`. Column `i` of
`M` is `2·T(eᵢ)`, so `T(eᵢ)` has every coordinate `±1/2` — it is a *spinor*
weight, not a vector weight. Triality genuinely moves `8ᵥ` off itself. -/
theorem T_maps_vector_to_spinor_weights (i j : Fin 4) :
    M j i = 1 ∨ M j i = -1 := by
  fin_cases i <;> fin_cases j <;> simp [M]

/-- **Which spinor.** The product of the coordinates of a doubled spinor weight is
`-1` exactly when it has an odd number of negative entries — the `8_c` parity
class. Every column of `M` satisfies this, so `T` sends `8ᵥ` into `8_c`, not `8ₛ`.
This is the concrete form of the cycle `8ᵥ → 8_c → 8ₛ → 8ᵥ`. -/
theorem T_vector_lands_in_odd_parity_class (i : Fin 4) :
    M 0 i * M 1 i * M 2 i * M 3 i = -1 := by
  fin_cases i <;> simp [M] <;> norm_num

/-- `M` is invertible, so `T` is a genuine automorphism and not a projection.
Derived from orthogonality rather than recomputed: `M Mᵀ = 4I` forces
`(det M)² = det(4I) = 4⁴ = 256`, hence `det M = ±16 ≠ 0`. -/
theorem M_det_sq : M.det * M.det = 256 := by
  have h : M.det * M.det = (M * M.transpose).det := by
    rw [Matrix.det_mul, Matrix.det_transpose]
  rw [h, M_orthogonal, Matrix.det_smul, Matrix.det_one, Fintype.card_fin]
  norm_num

theorem M_det_ne_zero : M.det ≠ 0 := by
  intro h
  have := M_det_sq
  rw [h] at this
  norm_num at this

end Triality
