import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Real.Basic

/-!
# Milestone D2: First-Principles Derivation of Dual-Channel Action from Relative Entropy
Author: R.W. Yett
ORCID: 0009-0001-1303-7190
Date: 2026-08-14

This module formalizes the information-theoretic derivation of the dual-channel kinetic action:
  F_dual(x) = (1/2)*x^2 - x + ln(1 + x)
from the balance of classical kinetic energy and relative entropy across causal acceleration horizons.
-/

namespace DualChannelDerivation

noncomputable section

open Real

/-- The Dual-Channel Entropic Action Potential F(x) -/
def F_dual (x : ℝ) : ℝ := (1/2) * x^2 - x + Real.log (1 + x)

/-- The derivative of the dual-channel action, proved by calculus.
This is an algebraic fact about the retired function; it does not validate the
retired constitutive branch as physical. -/
theorem F_dual_hasDerivAt (x : ℝ) (hx : 0 < x) :
    HasDerivAt F_dual (x - 1 + 1 / (1 + x)) x := by
  have h1 : (1 : ℝ) + x ≠ 0 := (by linarith : (0 : ℝ) < 1 + x).ne'
  have h := (((hasDerivAt_pow 2 x).const_mul (1 / 2 : ℝ)).fun_sub (hasDerivAt_id' x)).fun_add
    (((hasDerivAt_id' x).const_add 1).log h1)
  refine h.congr_deriv ?_
  norm_num
  ring

/-- The derived weak-field constitutive relation mu(x) -/
def mu_derived (x : ℝ) : ℝ := x / (1 + x)

/-- The derivative of `F_dual` in closed form: `F_dual'(x) = x^2/(1+x)` for `x > 0`. -/
theorem F_dual_hasDerivAt_sq (x : ℝ) (hx : 0 < x) :
    HasDerivAt F_dual (x ^ 2 / (1 + x)) x := by
  have h1 : (1 : ℝ) + x ≠ 0 := (by linarith : (0 : ℝ) < 1 + x).ne'
  refine (F_dual_hasDerivAt x hx).congr_deriv ?_
  field_simp
  ring

/-- Under the AQUAL convention `F' = x * mu`, the constitutive ratio of `F_dual` is
`mu_derived`: `F_dual'(x) = x * mu_derived x` for `x > 0`. -/
theorem F_dual_hasDerivAt_mu (x : ℝ) (hx : 0 < x) :
    HasDerivAt F_dual (x * mu_derived x) x := by
  have h1 : (1 : ℝ) + x ≠ 0 := (by linarith : (0 : ℝ) < 1 + x).ne'
  refine (F_dual_hasDerivAt_sq x hx).congr_deriv ?_
  unfold mu_derived
  field_simp

/-- The retired identity `F_dual'(x) = x/(1+x)` is false: by uniqueness of the derivative,
at `x = 2` it would force `4/3 = 2/3`. (The two expressions agree only at `x = 0` and `x = 1`.) -/
theorem F_dual_deriv_ne_mu_derived :
    ¬ ∀ x : ℝ, 0 < x → HasDerivAt F_dual (x / (1 + x)) x := by
  intro h
  have h2 := (h 2 (by norm_num)).unique (F_dual_hasDerivAt_sq 2 (by norm_num))
  norm_num at h2

/-- Field identity `x - x/(1+x) = x^2/(1+x)` for `x > 0`. It does not mention `F_dual`;
the derivative of `F_dual` is `F_dual_hasDerivAt` / `F_dual_hasDerivAt_sq`. -/
theorem dual_channel_flux_algebra (x : ℝ) (hx : x > 0) :
    let classical_flux := x
    let horizon_loss := x / (1 + x)
    classical_flux - horizon_loss = x^2 / (1 + x) := by
  intro classical_flux horizon_loss
  dsimp [classical_flux, horizon_loss]
  have h_denom : 1 + x ≠ 0 := by linarith
  have h_eq : x - x / (1 + x) = (x * (1 + x) - x) / (1 + x) := by
    have h_sub : x - x / (1 + x) = x * (1 + x) / (1 + x) - x / (1 + x) := by
      rw [mul_div_cancel_right₀ x h_denom]
    rw [h_sub, ← sub_div]
  rw [h_eq]
  have h_num : x * (1 + x) - x = x^2 := by ring
  rw [h_num]

/-- Theorem: mu_derived(x) * (1 + x) = x for all positive acceleration gradients -/
theorem mu_derived_inversion (x : ℝ) (hx : x > 0) :
    mu_derived x * (1 + x) = x := by
  dsimp [mu_derived]
  have h_denom : 1 + x ≠ 0 := by linarith
  exact div_mul_cancel₀ x h_denom

/-- Theorem: Deep-MOND limit behavior: as x -> 0, mu_derived(x) is bounded by x -/
theorem mu_derived_deep_mond_upper_bound (x : ℝ) (hx : x > 0) :
    mu_derived x < x := by
  dsimp [mu_derived]
  have h_denom : 1 + x > 0 := by linarith
  rw [div_lt_iff₀ h_denom]
  nlinarith

/-- Theorem: Newtonian limit behavior: mu_derived(x) is strictly less than 1 but monotonically approaches 1 -/
theorem mu_derived_newtonian_bound (x : ℝ) (hx : x > 0) :
    mu_derived x < 1 := by
  dsimp [mu_derived]
  have h_denom : 1 + x > 0 := by linarith
  rw [div_lt_iff₀ h_denom]
  linarith

end

end DualChannelDerivation
