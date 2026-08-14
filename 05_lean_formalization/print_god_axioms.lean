import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace GODTheory

theorem dual_channel_poly_identity (a_tot a_bary a_0 : ℝ)
    (h : a_tot^2 - a_bary * a_tot - a_bary * a_0 = 0) :
    a_tot^2 = a_bary * (a_tot + a_0) := by
  linarith

theorem aqual_simple_mu_ratio (a_tot a_bary a_0 : ℝ)
    (h_pos : a_tot > 0)
    (h_0 : a_0 > 0)
    (h_eq : a_tot^2 = a_bary * (a_tot + a_0)) :
    a_bary * (a_tot + a_0) = a_tot * a_tot := by
  linarith

theorem btfr_exact_scaling (G M r a_0 v : ℝ)
    (h_v : v^2 = (G * M * a_0 / r^2)^(1/2) * r)
    (h_r : r > 0)
    (h_G : G > 0)
    (h_M : M > 0)
    (h_a0 : a_0 > 0) :
    v^4 = G * M * a_0 := by
  have h_pos : G * M * a_0 / r^2 > 0 := by positivity
  have h4 : v^4 = (v^2)^2 := by ring
  rw [h4, h_v]
  have h_sq : ((G * M * a_0 / r^2)^(1/2) * r)^2 = (G * M * a_0 / r^2) * r^2 := by
    rw [mul_pow]
    have h_sqrt_sq : ((G * M * a_0 / r^2)^(1/2))^2 = G * M * a_0 / r^2 := by
      exact Real.sq_sqrt (by positivity)
    rw [h_sqrt_sq]
  rw [h_sq]
  have hr_ne : r^2 ≠ 0 := by positivity
  exact div_mul_cancel₀ (G * M * a_0) hr_ne

#print axioms dual_channel_poly_identity
#print axioms aqual_simple_mu_ratio
#print axioms btfr_exact_scaling

end GODTheory
