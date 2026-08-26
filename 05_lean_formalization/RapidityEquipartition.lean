import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Artanh
import Mathlib.Tactic

/-!
# Conditional Rapidity-Equipartition Identities

This module proves exact identities over the real numbers.  It does **not** prove
that a Kerr spin is physically a Lorentz rapidity, nor that an equipartition
condition is selected by a field equation.  Those are external model premises.
-/

namespace RapidityEquipartition

open Real

/-- The algebraic threshold used in the conditional identity gate. -/
noncomputable def theta : ℝ := 1 / Real.sqrt 2

/-- The selected real inverse-hyperbolic value has its exact logarithmic form. -/
theorem arsinh_one_eq_log_one_add_sqrt_two :
    Real.arsinh 1 = Real.log (1 + Real.sqrt 2) := by
  rw [Real.arsinh]
  norm_num

/-- At the chosen `arsinh 1` value, the hyperbolic tangent is `1 / √2`. -/
theorem tanh_arsinh_one_eq_theta :
    Real.tanh (Real.arsinh 1) = theta := by
  unfold theta
  rw [Real.tanh_arsinh]
  norm_num

/-- The inverse-hyperbolic forms agree exactly on the real principal branch. -/
theorem arsinh_one_eq_artanh_theta :
    Real.arsinh 1 = Real.artanh theta := by
  calc
    Real.arsinh 1 = Real.artanh (Real.tanh (Real.arsinh 1)) :=
      (Real.artanh_tanh (Real.arsinh 1)).symm
    _ = Real.artanh theta := by rw [tanh_arsinh_one_eq_theta]

/-- The odds transform of the threshold is the silver ratio. -/
theorem theta_odds_eq_silver_ratio :
    theta / (1 - theta) = 1 + Real.sqrt 2 := by
  unfold theta
  have hsq : (Real.sqrt 2) ^ 2 = (2 : ℝ) := by norm_num
  have hpos : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
  have hne : Real.sqrt 2 ≠ 0 := ne_of_gt hpos
  have hminus : Real.sqrt 2 - 1 ≠ 0 := by
    intro h
    nlinarith
  field_simp [hne, hminus]
  nlinarith

#print axioms arsinh_one_eq_log_one_add_sqrt_two
#print axioms tanh_arsinh_one_eq_theta
#print axioms arsinh_one_eq_artanh_theta
#print axioms theta_odds_eq_silver_ratio

end RapidityEquipartition
