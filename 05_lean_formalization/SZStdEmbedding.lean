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

/-- First ghost condition on the derived derivative: `J_std′(𝒴) > 0` for `𝒴 > 0`. -/
theorem Jstd_deriv_pos {Y : ℝ} (hY : 0 < Y) : 0 < muStd (Real.sqrt Y) / 2 := by
  unfold muStd
  have hsY : 0 < Real.sqrt Y := Real.sqrt_pos.mpr hY
  have hs1 : 0 < Real.sqrt (1 + Real.sqrt Y ^ 2) := Real.sqrt_pos.mpr (one_add_sq_pos _)
  positivity

end SZStdEmbedding
