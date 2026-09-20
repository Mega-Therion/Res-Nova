import MuStdSelection
import Mathlib.Tactic

/-!
# Solar-system PPN bounds under `mu_std`

`PPNLimits.lean` computes the solar-system margins from
`mu(x) = x / (1 + x)`. That is `mu_dual`, falsified 2026-09-12. Its own
docstring is explicit that the theorems "depend on the specific dual-channel
mu(x) = x/(1+x) ... Substituting a different interpolation function breaks
them." They do break, and this module replaces them.

The change is not cosmetic. The two branches deviate from the Newtonian limit
at different orders:

    1 - mu_dual x = 1 / (1 + x)              ~ 1/x
    1 - mu_std  x = 1 / (S (S + x))          ~ 1/(2 x^2)

so every margin improves by roughly a factor of `x`, which in the solar system
is eight to nine orders of magnitude.

The observational thresholds are unchanged: Cassini `|gamma - 1| < 2.3e-5`,
MESSENGER `|beta - 1| < 2.3e-4`, and the gradient `x = g / a_0` evaluated at
the orbit the measurement actually probes, with `a_0 = 1.116e-10 m/s^2` from
SPARC.

These theorems are not vacuous: each depends on `one_sub_mu_std` and on its
numeric threshold. They fail for `mu_dual`, which is the point.
-/

namespace ResNova.PPNLimitsStd

open ResNova.MuStdUniqueness ResNova.MuStdSelection

/-- Fractional departure from the Newtonian limit under `mu_std`. -/
noncomputable def deviation (x : ℝ) : ℝ := 1 - mu_std x

/-- **The inverse-square screening bound.** For `x ≥ 1`,
`1 - mu_std x ≤ 1 / (2 x^2)`. This is the quantitative content of the
`ScreenedTail` condition that selects `mu_std` over `mu_dual`. -/
theorem deviation_le_inv_two_sq {x : ℝ} (hx : 1 ≤ x) :
    deviation x ≤ 1 / (2 * x ^ 2) := by
  have hx0 : (0 : ℝ) < x := lt_of_lt_of_le zero_lt_one hx
  have hS : 0 < Real.sqrt (1 + x ^ 2) := sqrt_one_add_sq_pos x
  have hSx : x ≤ Real.sqrt (1 + x ^ 2) := sqrt_ge_self hx0.le
  have h2x2 : (0 : ℝ) < 2 * x ^ 2 := by positivity
  have hprod : 2 * x ^ 2 ≤ Real.sqrt (1 + x ^ 2) * (Real.sqrt (1 + x ^ 2) + x) := by
    nlinarith [hSx, hS, hx0]
  unfold deviation
  rw [one_sub_mu_std hx0.le, one_div, one_div]
  simpa using inv_anti₀ h2x2 hprod

/-- Planetary domain, `x ≥ 10^4`: the deviation is below `5e-9`.
Under `mu_dual` the same threshold gave only `1e-4`. -/
theorem planetary_bound {x : ℝ} (hx : (10 : ℝ) ^ 4 ≤ x) :
    deviation x ≤ 5 / 10 ^ 9 := by
  have hx1 : (1 : ℝ) ≤ x := by nlinarith
  have hx0 : (0 : ℝ) < x := by nlinarith
  refine le_trans (deviation_le_inv_two_sq hx1) ?_
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith [hx, hx0]

/-- Cassini, `x ≥ 6e7`: the deviation is below `2.3e-5` with an enormous
margin — bounded by `1.4e-16`, eleven orders below the threshold. -/
theorem cassini_satisfied {x : ℝ} (hx : (6 : ℝ) * 10 ^ 7 ≤ x) :
    deviation x < 23 / 10 ^ 6 := by
  have hx1 : (1 : ℝ) ≤ x := by nlinarith
  have hx0 : (0 : ℝ) < x := by nlinarith
  have hb := deviation_le_inv_two_sq hx1
  have : 1 / (2 * x ^ 2) < 23 / 10 ^ 6 := by
    rw [div_lt_div_iff₀ (by positivity) (by positivity)]
    nlinarith [hx, hx0]
  linarith

/-- MESSENGER, `x ≥ 3e8` (Mercury's orbital gradient): the deviation is below
the perihelion bound `2.3e-4`, bounded by `5.6e-18`. -/
theorem messenger_satisfied {x : ℝ} (hx : (3 : ℝ) * 10 ^ 8 ≤ x) :
    deviation x < 23 / 10 ^ 5 := by
  have hx1 : (1 : ℝ) ≤ x := by nlinarith
  have hx0 : (0 : ℝ) < x := by nlinarith
  have hb := deviation_le_inv_two_sq hx1
  have : 1 / (2 * x ^ 2) < 23 / 10 ^ 5 := by
    rw [div_lt_div_iff₀ (by positivity) (by positivity)]
    nlinarith [hx, hx0]
  linarith

/-- The quantitative MESSENGER margin: `deviation x ≤ 1 / (1.8e17)`. Under
`mu_dual` the comparable margin was `1 / (3e8)` — nine orders weaker. -/
theorem messenger_margin {x : ℝ} (hx : (3 : ℝ) * 10 ^ 8 ≤ x) :
    deviation x ≤ 1 / (18 * 10 ^ 16) := by
  have hx1 : (1 : ℝ) ≤ x := by nlinarith
  have hx0 : (0 : ℝ) < x := by nlinarith
  refine le_trans (deviation_le_inv_two_sq hx1) ?_
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith [hx, hx0]

/-- The deviation is strictly positive: `mu_std` never reaches 1 at finite `x`,
so these are genuine bounds on a nonzero quantity, not statements about zero. -/
theorem deviation_pos {x : ℝ} (hx : 0 < x) : 0 < deviation x := by
  have hS : 0 < Real.sqrt (1 + x ^ 2) := sqrt_one_add_sq_pos x
  have hsum : 0 < Real.sqrt (1 + x ^ 2) + x := by linarith
  unfold deviation
  rw [one_sub_mu_std hx.le]
  positivity

end ResNova.PPNLimitsStd
