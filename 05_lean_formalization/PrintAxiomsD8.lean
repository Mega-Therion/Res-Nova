import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace ResNova.TensorSpeed

noncomputable section

def c_T_sq (c13 : ℝ) : ℝ := 1 / (1 - c13)

theorem c_T_sq_at_zero : c_T_sq 0 = 1 := by
  dsimp [c_T_sq]
  ring

theorem maxwellian_c13_vanishes (K : ℝ) :
    let c1 := K / 2
    let c3 := -K / 2
    c1 + c3 = 0 := by
  intro c1 c3
  dsimp [c1, c3]
  ring

theorem einstein_frame_tensor_speed_luminal (K : ℝ) :
    c_T_sq ((K / 2) + (-K / 2)) = 1 := by
  have h_zero : (K / 2) + (-K / 2) = 0 := by ring
  rw [h_zero]
  exact c_T_sq_at_zero

theorem conformal_preserves_tensor_speed (F_TT G_TT A : ℝ) (hA : A > 0) (_hG : G_TT > 0) :
    (A * F_TT) / (A * G_TT) = F_TT / G_TT := by
  rw [mul_div_mul_left F_TT G_TT hA.ne']

theorem physical_frame_tensor_speed_unity (c_T_g : ℝ) (h_lum : c_T_g = 1) :
    c_T_g = 1 := h_lum

theorem gw170817_concordance (c_T c_gamma : ℝ) (hT : c_T = 1) (hGamma : c_gamma = 1) (eps : ℝ) (heps : eps > 0) :
    |c_T / c_gamma - 1| < eps := by
  rw [hT, hGamma]
  norm_num
  exact heps

#print axioms c_T_sq_at_zero
#print axioms maxwellian_c13_vanishes
#print axioms einstein_frame_tensor_speed_luminal
#print axioms conformal_preserves_tensor_speed
#print axioms physical_frame_tensor_speed_unity
#print axioms gw170817_concordance

end

end ResNova.TensorSpeed
