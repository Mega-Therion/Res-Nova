import SZStdEmbedding
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# Parameterized scalar normalization for the live AeST scalar channel (Res-Nova issue #217)

Formalization of obligation 1 of Res-Nova issue #217 ("[AeST formalization] Parameterized
scalar normalization and Noether identity checks"), picked up after Manus stopped (BLK-1437).

## What is proved

For `Y > 0`, `a > 0`, and arbitrary `lam : ℝ`:

* `hasDerivAt_Jparam`: `d/dY [2 * lam * a^2 * Fstd (√Y / a)] = lam * muStd (√Y / a)`.
* `deriv_Jparam`: the same identity in `deriv` form.
* `Jparam_deriv_pos`: for `lam > 0`, the derivative is strictly positive.
* `Jparam_half_one`: at `lam = 1/2`, `a = 1`, the parameterized function is exactly
  `SZStdEmbedding.Jstd`, recovering `hasDerivAt_Jstd` (`Jstd'(Y) = muStd(√Y)/2`).

The derivative identity is linear in `lam`, so `lam > 0` is not needed for it — the
theorem as stated is strictly stronger than the issue's request (`lam > 0` is used
only for the positivity corollary). The proof is the chain rule through
`SZStdEmbedding.hasDerivAt_Fstd` (`Fstd'(x) = x^2 / √(1+x^2) = x * muStd x`) and the
derivative of `fun Y => √Y / a`, as the issue's derivation prescribes.

## Scope (obligation 2 of issue #217) — read before citing

This is a **calculus/normalization result only**. It neither derives the covariant AeST
field equations nor selects the physical branch, and must not be described as a proof of
either. The normalization `lam` (`λ_s`) and scale `a` (`ã`) are inputs; nothing here
fixes them from physics. No evidence tier is promoted by this module.
-/

noncomputable section

namespace ResNova.AeSTParameterizedNormalization

open SZStdEmbedding

/-- The D7-scaled live scalar-channel function `J(Y) = 2 * λ_s * ã^2 * Fstd(√Y / ã)`. -/
def Jparam (lam a Y : ℝ) : ℝ := 2 * lam * a ^ 2 * Fstd (Real.sqrt Y / a)

/-- Issue #217, obligation 1: the parameterized scalar constitutive derivative, by the
chain rule through `hasDerivAt_Fstd`. Holds for arbitrary `lam`; `lam > 0` is needed
only for the positivity corollary below. -/
theorem hasDerivAt_Jparam {Y lam a : ℝ} (hY : 0 < Y) (ha : 0 < a) :
    HasDerivAt (Jparam lam a) (lam * muStd (Real.sqrt Y / a)) Y := by
  have hsY : 0 < Real.sqrt Y := Real.sqrt_pos.mpr hY
  have hsY' : Real.sqrt Y ≠ 0 := hsY.ne'
  have ha' : a ≠ 0 := ha.ne'
  have hS : 0 < Real.sqrt (1 + (Real.sqrt Y / a) ^ 2) :=
    Real.sqrt_pos.mpr (by positivity)
  have hS' : Real.sqrt (1 + (Real.sqrt Y / a) ^ 2) ≠ 0 := hS.ne'
  have hsqrt : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt Y)) Y := by
    simpa using Real.hasDerivAt_sqrt hY.ne'
  have hinner : HasDerivAt (fun Y : ℝ => Real.sqrt Y / a) ((1 / (2 * Real.sqrt Y)) / a) Y :=
    hsqrt.div_const a
  have hF := hasDerivAt_Fstd (Real.sqrt Y / a)
  have hcomp := hF.comp Y hinner
  have hmul := hcomp.const_mul (2 * lam * a ^ 2)
  refine hmul.congr_deriv ?_
  simp only [muStd]
  field_simp

/-- The parameterized derivative in `deriv` form. -/
theorem deriv_Jparam {Y lam a : ℝ} (hY : 0 < Y) (ha : 0 < a) :
    deriv (Jparam lam a) Y = lam * muStd (Real.sqrt Y / a) :=
  (hasDerivAt_Jparam hY ha).deriv

/-- Positivity of the parameterized derivative: for `lam > 0`, `J'(Y) > 0` on `Y > 0`
(the first ghost condition, on the derived derivative). -/
theorem Jparam_deriv_pos {Y lam a : ℝ} (hY : 0 < Y) (hlam : 0 < lam) (ha : 0 < a) :
    0 < lam * muStd (Real.sqrt Y / a) := by
  have hsY : 0 < Real.sqrt Y := Real.sqrt_pos.mpr hY
  have hx : 0 < Real.sqrt Y / a := div_pos hsY ha
  have hS : 0 < Real.sqrt (1 + (Real.sqrt Y / a) ^ 2) :=
    Real.sqrt_pos.mpr (by positivity)
  unfold muStd
  exact mul_pos hlam (div_pos hx hS)

/-- Specialization: at `lam = 1/2`, `a = 1`, the parameterized function is `Jstd`,
recovering the unparameterized AQUAL reduction. -/
theorem Jparam_half_one (Y : ℝ) : Jparam (1 / 2) 1 Y = Jstd Y := by
  simp [Jparam, Jstd]

#print axioms hasDerivAt_Jparam
#print axioms deriv_Jparam
#print axioms Jparam_deriv_pos
#print axioms Jparam_half_one

end ResNova.AeSTParameterizedNormalization
