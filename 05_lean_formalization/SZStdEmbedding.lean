import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# D9 on the live branch: the Skordis–Złośnik kinetic function for `μ_std`, by calculus

`SkordisZlosnikEmbedding.lean` carries a `μ_std` section, but its `sz_std_aqual_reduction`
*defines* `dJ_dY_std := μ_std/2` and then proves `2·dJ_dY_std = μ_std`. That is true by
definition and fails the corpus's substitutability test. This module supplies the content.
It writes down the kinetic function and **differentiates** it.

## Creation frame — read before citing

With a₀ = 1 and x = √𝒴:
* `F_std x = (x √(1+x²) − arsinh x)/2`. This is the unique antiderivative with `F(0) = 0` of
  D2's constraint 1, `F′(x) = x μ(x)`, at `μ = μ_std`.
* `J_std 𝒴 = F_std (√𝒴)`, the AeST free function in the quasistatic sector (the
  `TARGET_D7` §2.1 normalization pattern, `λ_s` set to the value that makes `μ = 2J′`).

**Proved.**
1. `hasDerivAt_F_std`: `F_std′(x) = x² / √(1+x²) = x · μ_std(x)` (constraint 1, by calculus).
2. `hasDerivAt_J_std`: for `𝒴 > 0`, `J_std′(𝒴) = μ_std(√𝒴)/2`, i.e. `2 J′ = μ_std`. This is the
   AQUAL reduction, derived.
3. `J_std_deriv_pos`: `J_std′(𝒴) > 0` for `𝒴 > 0` (the first ghost condition, on the derived
   derivative).

**Not proved here.** The normalization `λ_s` is an input (`TARGET_D7` §2.1). Nothing selects
`μ_std` (see `MuNDuality.lean`: the duality holds for every n). There is no field equation and no
solar-system claim. The external-field quadrupole is in
`02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md`.
-/

noncomputable section

namespace SZStdEmbedding

open Real

/-- The live interpolating function. -/
def muStd (x : ℝ) : ℝ := x / Real.sqrt (1 + x ^ 2)

/-- `F_std(x) = (x√(1+x²) − arsinh x)/2`, the antiderivative of `x·μ_std(x)` with `F(0)=0`. -/
def Fstd (x : ℝ) : ℝ := (x * Real.sqrt (1 + x ^ 2) - Real.arsinh x) / 2

/-- The AeST free function in the quasistatic sector, `J(𝒴) = F_std(√𝒴)` (a₀ = 1). -/
def Jstd (Y : ℝ) : ℝ := Fstd (Real.sqrt Y)

theorem one_add_sq_pos (x : ℝ) : 0 < 1 + x ^ 2 := by positivity

/-- Constraint 1 of D2 at `μ_std`, by differentiation: `F_std′(x) = x²/√(1+x²)`. -/
theorem hasDerivAt_Fstd (x : ℝ) :
    HasDerivAt Fstd (x ^ 2 / Real.sqrt (1 + x ^ 2)) x := by
  have hpos := one_add_sq_pos x
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr hpos
  have h1 : HasDerivAt (fun x : ℝ => 1 + x ^ 2) (2 * x) x := by
    simpa using ((hasDerivAt_pow 2 x).const_add 1)
  have h2 : HasDerivAt (fun x : ℝ => Real.sqrt (1 + x ^ 2))
      (2 * x / (2 * Real.sqrt (1 + x ^ 2))) x := h1.sqrt hpos.ne'
  have h3 := (hasDerivAt_id x).mul h2
  have h4 := Real.hasDerivAt_arsinh x
  have h5 := (h3.sub h4).div_const 2
  have hsq : Real.sqrt (1 + x ^ 2) * Real.sqrt (1 + x ^ 2) = 1 + x ^ 2 := Real.mul_self_sqrt hpos.le
  refine h5.congr_deriv ?_
  simp only [id, one_mul]
  field_simp
  nlinarith [hsq]

/-- `F_std′(x) = x · μ_std(x)`. -/
theorem Fstd_deriv_eq (x : ℝ) : x ^ 2 / Real.sqrt (1 + x ^ 2) = x * muStd x := by
  unfold muStd
  ring

/-- The AQUAL reduction, derived: for `𝒴 > 0`, `J_std′(𝒴) = μ_std(√𝒴)/2`. -/
theorem hasDerivAt_Jstd {Y : ℝ} (hY : 0 < Y) :
    HasDerivAt Jstd (muStd (Real.sqrt Y) / 2) Y := by
  have hsY : 0 < Real.sqrt Y := Real.sqrt_pos.mpr hY
  have hF := hasDerivAt_Fstd (Real.sqrt Y)
  have hsqrt : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt Y)) Y := by
    simpa using Real.hasDerivAt_sqrt hY.ne'
  have hc := hF.comp Y hsqrt
  have hpos := one_add_sq_pos (Real.sqrt Y)
  have hs1 : 0 < Real.sqrt (1 + Real.sqrt Y ^ 2) := Real.sqrt_pos.mpr hpos
  have hYsq : Real.sqrt Y ^ 2 = Y := Real.sq_sqrt hY.le
  refine hc.congr_deriv ?_
  simp only [muStd]
  rw [hYsq]
  field_simp
  rw [hYsq]

/-- The D7-scaled scalar potential, represented as a rescaling of the proved `Jstd`. -/
def Jscaled (lambdaS aT Y : ℝ) : ℝ :=
  2 * lambdaS * aT ^ 2 * Jstd (Y / aT ^ 2)

/-- For positive scale, `Jscaled` is the stated `Fstd` normalization. -/
theorem Jscaled_eq_scaled_Fstd {lambdaS aT Y : ℝ} (ha : 0 < aT) :
    Jscaled lambdaS aT Y =
      2 * lambdaS * aT ^ 2 * Fstd (Real.sqrt Y / aT) := by
  unfold Jscaled Jstd
  by_cases hY : 0 ≤ Y
  · rw [Real.sqrt_div hY, Real.sqrt_sq_eq_abs, abs_of_pos ha]
  · have hYneg : Y ≤ 0 := le_of_lt (lt_of_not_ge hY)
    have harg : Y / aT ^ 2 ≤ 0 :=
      div_nonpos_of_nonpos_of_nonneg hYneg (sq_nonneg aT)
    rw [Real.sqrt_eq_zero_of_nonpos harg, Real.sqrt_eq_zero_of_nonpos hYneg]
    simp [Fstd]

/-- Derivative of the scaled potential, reusing the established `Jstd` derivative. -/
theorem hasDerivAt_Jscaled {lambdaS aT Y : ℝ} (hY : 0 < Y) (ha : 0 < aT) :
    HasDerivAt (fun y : ℝ => Jscaled lambdaS aT y)
      (lambdaS * muStd (Real.sqrt Y / aT)) Y := by
  have ha2 : 0 < aT ^ 2 := pow_pos ha 2
  have harg : 0 < Y / aT ^ 2 := div_pos hY ha2
  have hJ := hasDerivAt_Jstd harg
  have hscale : HasDerivAt (fun y : ℝ => y / aT ^ 2) (1 / aT ^ 2) Y := by
    simpa using (hasDerivAt_id Y).div_const (aT ^ 2)
  have hcomp := hJ.comp Y hscale
  have hsqrt : Real.sqrt (Y / aT ^ 2) = Real.sqrt Y / aT := by
    rw [Real.sqrt_div hY.le, Real.sqrt_sq_eq_abs, abs_of_pos ha]
  have hderiv :
      (2 * lambdaS * aT ^ 2) *
          ((muStd (Real.sqrt (Y / aT ^ 2)) / 2) * (1 / aT ^ 2)) =
        lambdaS * muStd (Real.sqrt Y / aT) := by
    rw [hsqrt]
    field_simp [ne_of_gt ha]
  have hscaled := (hcomp.const_mul (2 * lambdaS * aT ^ 2)).congr_deriv hderiv
  simpa [Jscaled] using hscaled

/-- The requested D7-scaled derivative. `Y > 0` and `aT > 0` suffice; `lambdaS` is arbitrary. -/
theorem hasDerivAt_scaled_Fstd {lambdaS aT Y : ℝ} (hY : 0 < Y) (ha : 0 < aT) :
    HasDerivAt (fun y : ℝ =>
      2 * lambdaS * aT ^ 2 * Fstd (Real.sqrt y / aT))
      (lambdaS * muStd (Real.sqrt Y / aT)) Y := by
  have hscaled := hasDerivAt_Jscaled (lambdaS := lambdaS) (aT := aT) (Y := Y) hY ha
  have hEq :
      (fun y : ℝ => 2 * lambdaS * aT ^ 2 * Fstd (Real.sqrt y / aT)) =ᶠ[nhds Y]
        (fun y : ℝ => Jscaled lambdaS aT y) :=
    Filter.Eventually.of_forall (fun y =>
      (Jscaled_eq_scaled_Fstd (lambdaS := lambdaS) (aT := aT) (Y := y) ha).symm)
  exact hscaled.congr_of_eventuallyEq hEq

/-- First ghost condition on the derived derivative: `J_std′(𝒴) > 0` for `𝒴 > 0`. -/
theorem Jstd_deriv_pos {Y : ℝ} (hY : 0 < Y) : 0 < muStd (Real.sqrt Y) / 2 := by
  unfold muStd
  have hsY : 0 < Real.sqrt Y := Real.sqrt_pos.mpr hY
  have hs1 : 0 < Real.sqrt (1 + Real.sqrt Y ^ 2) := Real.sqrt_pos.mpr (one_add_sq_pos _)
  positivity

end SZStdEmbedding
