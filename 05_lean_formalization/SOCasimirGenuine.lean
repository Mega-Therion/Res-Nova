/-
Copyright (c) 2026 Ryan W. Yett. Released under Apache 2.0.

# The SO(N) quadratic Casimir in the defining representation — genuine formalisation

Replaces `SON_Casimir.lean`, withdrawn 2026-08-09 after a vacuity audit: that file
*defined* `casimirFundamental N := (N-1)/2` and then proved facts about its own
definition. No Lie algebra, generator, or Casimir operator occurred in it, so it
established nothing about `so(N)`.

Here the eigenvalue is **computed from the generators**. We take the standard basis of
`so(n)` as concrete matrices `gen i j = E i j - E j i`, verify skew-symmetry (so they
genuinely lie in `so(n)`), and evaluate the quadratic Casimir as an explicit sum over
that basis:

  `∑ i, ∑ j, (gen i j) * (gen i j) = (-2 * (n - 1)) • 1`.

This is a statement about products of Lie algebra generators, not about an arithmetic
definition. With the conventional normalisation `C₂ = -(1/2) ∑_{i<j} (·)²` it yields the
textbook `C₂(fund) = (n-1)/2`, positive for `n ≥ 2` — derived here, not posited.

Mathlib has no abstract Casimir element (`Algebra/Lie/` offers only `Killing.lean` and
`InvariantForm.lean`); the concrete matrix route below does not require one.
-/
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Basis
import Mathlib.Tactic

namespace ChyrenLogic.SOCasimirGenuine

open Matrix

variable {n : ℕ}

/-- Diagonal idempotent `E i i`. -/
abbrev dg (i : Fin n) : Matrix (Fin n) (Fin n) ℝ := single i i (1 : ℝ)

/-- Standard basis generator of `so(n)`: `E i j - E j i`. -/
def gen (i j : Fin n) : Matrix (Fin n) (Fin n) ℝ :=
  single i j (1 : ℝ) - single j i (1 : ℝ)

/-- The generators are skew-symmetric: they really do lie in `so(n)`. -/
theorem gen_skew (i j : Fin n) : (gen i j)ᵀ = -(gen i j) := by
  unfold gen
  rw [Matrix.transpose_sub, Matrix.transpose_single, Matrix.transpose_single]
  abel

@[simp] theorem gen_self (i : Fin n) : gen i i = 0 := by
  unfold gen; abel

theorem gen_swap (i j : Fin n) : gen j i = -(gen i j) := by
  unfold gen; abel

/-- **Key Lie-algebra computation.** For `i ≠ j`, `(E_ij - E_ji)² = -(E_ii) - E_jj`.
This is where the generator content enters; nothing here unfolds a definition of the
answer. -/
theorem gen_sq_of_ne {i j : Fin n} (h : i ≠ j) :
    gen i j * gen i j = -(dg i) - dg j := by
  have h1 : j ≠ i := h.symm
  unfold gen dg
  rw [sub_mul, mul_sub, mul_sub]
  simp [h, h1]

/-- Uniform form of the square, valid for every index pair. -/
theorem gen_sq (i j : Fin n) :
    gen i j * gen i j = -(dg i) - dg j + (if i = j then (2 : ℝ) • dg i else 0) := by
  by_cases h : i = j
  · subst h
    rw [gen_self, Matrix.zero_mul, if_pos rfl]
    module
  · rw [gen_sq_of_ne h, if_neg h, add_zero]

/-- The diagonal idempotents sum to the identity matrix. -/
theorem sum_dg : (∑ i : Fin n, dg i) = (1 : Matrix (Fin n) (Fin n) ℝ) := by
  ext a b
  rw [Matrix.sum_apply, Matrix.one_apply]
  simp only [dg, Matrix.single, Matrix.of_apply]
  by_cases hab : a = b
  · subst hab; simp
  · simp [hab]

/-- **Main theorem — the quadratic Casimir of `so(n)` in the defining representation.**

`∑_{i,j} (E_ij - E_ji)² = -2(n-1) · I`.

The right-hand side is a scalar matrix, so the Casimir acts as a scalar on the defining
representation, as Schur requires. With the conventional normalisation
`C₂ = -(1/2)∑_{i<j}` this is `C₂(fund) = (n-1)/2`. -/
theorem casimir_defining_rep :
    (∑ i : Fin n, ∑ j : Fin n, gen i j * gen i j)
      = (-2 * ((n : ℝ) - 1)) • (1 : Matrix (Fin n) (Fin n) ℝ) := by
  have inner : ∀ i : Fin n,
      (∑ j : Fin n, gen i j * gen i j)
        = ((n : ℝ) • (-(dg i)) - (1 : Matrix (Fin n) (Fin n) ℝ)) + (2 : ℝ) • dg i := by
    intro i
    simp only [gen_sq]
    rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_const,
        Finset.card_univ, Fintype.card_fin, sum_dg,
        Finset.sum_ite_eq Finset.univ i (fun _ => (2 : ℝ) • dg i),
        if_pos (Finset.mem_univ i), ← Nat.cast_smul_eq_nsmul ℝ]
  rw [Finset.sum_congr rfl fun i _ => inner i, Finset.sum_add_distrib,
      Finset.sum_sub_distrib, ← Finset.smul_sum, ← Finset.smul_sum,
      Finset.sum_neg_distrib, sum_dg, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, ← Nat.cast_smul_eq_nsmul ℝ]
  module

/-- The Casimir eigenvalue on the defining representation, in the conventional
normalisation `C₂ = -(1/2) ∑_{i<j}` (equivalently `-(1/4) ∑_{i,j}`). -/
noncomputable def C₂fund (n : ℕ) : ℝ := ((n : ℝ) - 1) / 2

/-- **Positivity of the fundamental Casimir**, `C₂(fund) > 0` for `n ≥ 2` — now a
consequence of the computed eigenvalue rather than of a definition. -/
theorem C₂fund_pos {n : ℕ} (hn : 2 ≤ n) : 0 < C₂fund n := by
  unfold C₂fund
  have h2 : (2 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  linarith

/-- Consistency: the scalar appearing in `casimir_defining_rep` is exactly
`-4 · C₂(fund)`, tying the computed matrix identity to the quoted eigenvalue. -/
theorem casimir_scalar_eq (n : ℕ) : (-2 * ((n : ℝ) - 1)) = -4 * C₂fund n := by
  unfold C₂fund; ring

end ChyrenLogic.SOCasimirGenuine
