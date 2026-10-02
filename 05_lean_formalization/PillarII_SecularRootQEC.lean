import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

noncomputable section

open Real

namespace PillarII

/-- Pillar 2: The secular polynomial P(l) = l² - 13l - 80 governing the 5-class articulatory phonotactic subshift -/
def secular_poly (l : ℝ) : ℝ := l^2 - 13 * l - 80

/-- Theorem: λ_max = (13 + √489)/2 is an exact zero of the secular polynomial -/
theorem secular_root_exact :
  secular_poly ((13 + sqrt 489) / 2) = 0 := by
  dsimp [secular_poly]
  have h_sqrt_sq : (sqrt 489)^2 = 489 := sq_sqrt (by norm_num)
  have h_sq : ((13 + sqrt 489) / 2)^2 = (169 + 26 * sqrt 489 + 489) / 4 := by
    have h1 : ((13 + sqrt 489) / 2)^2 = (13 + sqrt 489)^2 / 4 := by ring
    rw [h1]
    have h2 : (13 + sqrt 489)^2 = 13^2 + 2 * 13 * sqrt 489 + (sqrt 489)^2 := by ring
    rw [h2, h_sqrt_sq]
    ring
  rw [h_sq]
  ring

/-- CRT Idempotent Decomposition over ℤ₂₂: e₁ = 11, e₂ = 12 -/
theorem crt_idempotents_z22 :
  (11 * 11) % 22 = 11 ∧
  (12 * 12) % 22 = 12 ∧
  (11 + 12) % 22 = 1 ∧
  (11 * 12) % 22 = 0 := by
  decide

end PillarII
