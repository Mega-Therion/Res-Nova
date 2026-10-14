import SZStdEmbedding
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Tactic

/-!
# D9/D7: the scalar-channel function whose total law is `μ_std`, by calculus

`SZStdEmbedding.lean` puts `μ_std` in AeST's scalar channel. In spherical symmetry its total law is
`ν_std` only as `λ_s → 0`. This module proves the calculus of the function that makes the total
law `μ_std` at finite `λ_s` (`AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md`).

## Creation frame — read before citing

Setting (`TARGET_D7` §2, `[D]`, taken as given here): `g = ĝ + g_φ`, `𝒥′(𝒴) g_φ = ĝ`, `ĝ = η g_N`,
`η = λ_s/(1+λ_s)`. Units `a₀ = 1`; the parameter is `x = g/a₀`. If the total law is `x μ_std(x) = y`,
the scalar channel needs `s = x − η y`, slope `𝒥′ = η μ/(1 − η μ)`, and `𝒥 = 2η F_std − η² y²`
along the curve `𝒴 = s²`.

**Proved.**
1. `gauss_law`: `𝒥′ · s = η · y` for `0 ≤ η ≤ 1`. This is the Gauss law `𝒥′ g_φ = ĝ` along the curve.
2. `chain_rule`: `d𝒥/dx = 𝒥′ · d𝒴/dx`, so the closed form integrates the slope (with `hasDerivAt_yT`,
   `hasDerivAt_s`, `hasDerivAt_J`, `hasDerivAt_Ycurve`).
3. `yTd_sq_le`: `y′(x)² ≤ 32/27`, from `32(1+t)³ − 27t(t+2)² = (t−2)²(5t+8) ≥ 0` with `t = x²`.
4. `sprime_pos`, `s_strictMono`: if `32η² < 27` (any sign of `η`), then `s′ > 0` everywhere and `s` is strictly
   increasing, so `𝒥′` is a function of `𝒴`.
5. `sprime_neg_at_sqrt_two`, `s_not_monotone`: if `32η² > 27`, then `s′(√2) < 0` and `s` is not
   monotone. The map folds.
6. `flux_hasDerivAt`: the flux `𝒥′ s` has `x`-derivative `η y′`. With `s′ > 0` the flux therefore
   rises with `s`, which is the second static ghost condition `𝒥′ + 2𝒴𝒥″ > 0` in parametric form.
7. `threshold_iff`: for `λ_s ≥ 0`, `32 (λ_s/(1+λ_s))² < 27 ↔ λ_s < (27 + 12√6)/5`.

**Not proved here.** The two-channel reduction itself and its scope (spherical symmetry, aligned
gradients, negligible mass term). Anything about the constrained scalar–vector–metric evolution.
The equality case `32η² = 27`: there `s′(√2) = 0` and `𝒥″` diverges at `x = √2`. Which scalar
function is live is open (D7).
-/

noncomputable section

namespace AeSTTotalScalarCorrespondence

open Real SZStdEmbedding

/-- The total law in units `a₀ = 1`: `y = x μ_std(x) = x²/√(1+x²)`. -/
def yT (x : ℝ) : ℝ := x ^ 2 / Real.sqrt (1 + x ^ 2)

/-- Its derivative, `y′(x) = x(x²+2)/((1+x²)√(1+x²))`. -/
def yTd (x : ℝ) : ℝ := x * (x ^ 2 + 2) / ((1 + x ^ 2) * Real.sqrt (1 + x ^ 2))

/-- The scalar acceleration along the curve, `s = x − η y`. -/
def s (η x : ℝ) : ℝ := x - η * yT x

/-- The slope of the scalar function along the curve, `𝒥′ = η μ/(1 − η μ)`. -/
def Jp (η x : ℝ) : ℝ := η * muStd x / (1 - η * muStd x)

/-- The scalar function along the curve, `𝒥 = 2η F_std − η² y²`. -/
def J (η x : ℝ) : ℝ := 2 * η * Fstd x - η ^ 2 * yT x ^ 2

/-- `𝒴` along the curve, `𝒴 = s²`. -/
def Ycurve (η x : ℝ) : ℝ := s η x ^ 2

theorem yT_eq (x : ℝ) : yT x = x * muStd x := by
  unfold yT muStd
  ring

theorem muStd_lt_one (x : ℝ) : muStd x < 1 := by
  unfold muStd
  have hpos := one_add_sq_pos x
  have hr : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr hpos
  have hsq : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 := Real.sq_sqrt hpos.le
  have hx : x < Real.sqrt (1 + x ^ 2) := by
    nlinarith [Real.sqrt_nonneg (1 + x ^ 2)]
  rw [div_lt_one hr]
  exact hx

theorem one_sub_pos {η : ℝ} (hη0 : 0 ≤ η) (hη1 : η ≤ 1) (x : ℝ) : 0 < 1 - η * muStd x := by
  have hm := muStd_lt_one x
  rcases le_or_gt (muStd x) 0 with h | h
  · nlinarith
  · nlinarith

/-- The Gauss law along the curve: `𝒥′ · s = η · y`. -/
theorem gauss_law {η : ℝ} (hη0 : 0 ≤ η) (hη1 : η ≤ 1) (x : ℝ) :
    Jp η x * s η x = η * yT x := by
  have h := (one_sub_pos hη0 hη1 x).ne'
  have hs : s η x = x * (1 - η * muStd x) := by
    unfold s
    rw [yT_eq]
    ring
  rw [hs, yT_eq]
  unfold Jp
  field_simp

theorem hasDerivAt_yT (x : ℝ) : HasDerivAt yT (yTd x) x := by
  have hpos := one_add_sq_pos x
  have hr : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr hpos
  have hsq : Real.sqrt (1 + x ^ 2) * Real.sqrt (1 + x ^ 2) = 1 + x ^ 2 :=
    Real.mul_self_sqrt hpos.le
  have h1 : HasDerivAt (fun x : ℝ => 1 + x ^ 2) (2 * x) x := by
    simpa using ((hasDerivAt_pow 2 x).const_add 1)
  have h2 : HasDerivAt (fun x : ℝ => Real.sqrt (1 + x ^ 2))
      (2 * x / (2 * Real.sqrt (1 + x ^ 2))) x := h1.sqrt hpos.ne'
  have h3 : HasDerivAt (fun x : ℝ => x ^ 2) (2 * x) x := by
    simpa using hasDerivAt_pow 2 x
  have hsq2 : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 := Real.sq_sqrt hpos.le
  have h4 := h3.div h2 hr.ne'
  refine h4.congr_deriv ?_
  unfold yTd
  field_simp
  rw [hsq2]
  ring

theorem hasDerivAt_s (η x : ℝ) : HasDerivAt (s η) (1 - η * yTd x) x :=
  (hasDerivAt_id' x).sub ((hasDerivAt_yT x).const_mul η)

theorem hasDerivAt_J (η x : ℝ) :
    HasDerivAt (J η) (2 * η * yT x - η ^ 2 * (2 * yT x * yTd x)) x := by
  have hF : HasDerivAt Fstd (yT x) x := hasDerivAt_Fstd x
  have h := (hF.const_mul (2 * η)).sub (((hasDerivAt_yT x).pow 2).const_mul (η ^ 2))
  exact h.congr_deriv (by norm_num)

theorem hasDerivAt_Ycurve (η x : ℝ) :
    HasDerivAt (Ycurve η) (2 * s η x * (1 - η * yTd x)) x :=
  ((hasDerivAt_s η x).pow 2).congr_deriv (by norm_num)

/-- The closed form integrates the slope: `d𝒥/dx = 𝒥′ · d𝒴/dx`. -/
theorem chain_rule {η : ℝ} (hη0 : 0 ≤ η) (hη1 : η ≤ 1) (x : ℝ) :
    HasDerivAt (J η) (Jp η x * (2 * s η x * (1 - η * yTd x))) x := by
  refine (hasDerivAt_J η x).congr_deriv ?_
  have hg := gauss_law hη0 hη1 x
  calc 2 * η * yT x - η ^ 2 * (2 * yT x * yTd x)
      = 2 * (η * yT x) * (1 - η * yTd x) := by ring
    _ = 2 * (Jp η x * s η x) * (1 - η * yTd x) := by rw [hg]
    _ = Jp η x * (2 * s η x * (1 - η * yTd x)) := by ring

theorem yTd_sq_eq (x : ℝ) : yTd x ^ 2 = x ^ 2 * (x ^ 2 + 2) ^ 2 / (1 + x ^ 2) ^ 3 := by
  have hpos := one_add_sq_pos x
  have hsq : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 := Real.sq_sqrt hpos.le
  unfold yTd
  rw [div_pow, mul_pow, mul_pow, hsq]
  ring

/-- `y′(x)² ≤ 32/27`, with `32(1+t)³ − 27t(t+2)² = (t−2)²(5t+8)`. -/
theorem yTd_sq_le (x : ℝ) : yTd x ^ 2 ≤ 32 / 27 := by
  have hpos := one_add_sq_pos x
  rw [yTd_sq_eq, div_le_iff₀ (by positivity)]
  nlinarith [mul_nonneg (sq_nonneg (x ^ 2 - 2)) (show (0 : ℝ) ≤ 5 * x ^ 2 + 8 by positivity)]

theorem poly_identity (t : ℝ) : 32 * (1 + t) ^ 3 - 27 * t * (t + 2) ^ 2 = (t - 2) ^ 2 * (5 * t + 8) := by
  ring

/-- Below the bound, `s′ > 0` everywhere. -/
theorem sprime_pos {η : ℝ} (hη : 32 * η ^ 2 < 27) (x : ℝ) : 0 < 1 - η * yTd x := by
  have hd := yTd_sq_le x
  nlinarith [mul_nonneg (sq_nonneg η) (sub_nonneg.mpr hd), sq_nonneg (η * yTd x - 1)]

/-- Below the bound, `s` is strictly increasing, so the slope is a function of `𝒴`. -/
theorem s_strictMono {η : ℝ} (hη : 32 * η ^ 2 < 27) : StrictMono (s η) :=
  strictMono_of_deriv_pos (fun x => by
    rw [(hasDerivAt_s η x).deriv]
    exact sprime_pos hη x)

theorem yTd_sqrt_two_sq : yTd (Real.sqrt 2) ^ 2 = 32 / 27 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  rw [yTd_sq_eq, h2]
  norm_num

theorem yTd_sqrt_two_pos : 0 < yTd (Real.sqrt 2) := by
  unfold yTd
  have h2 : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  positivity

/-- Above the bound, `s′(√2) < 0`. -/
theorem sprime_neg_at_sqrt_two {η : ℝ} (hη0 : 0 < η) (hη : 27 < 32 * η ^ 2) :
    1 - η * yTd (Real.sqrt 2) < 0 := by
  have hd := yTd_sqrt_two_sq
  have hp := yTd_sqrt_two_pos
  have hsq : (η * yTd (Real.sqrt 2)) ^ 2 = η ^ 2 * (32 / 27) := by
    rw [mul_pow, hd]
  nlinarith [mul_pos hη0 hp]

/-- Above the bound, `s` is not monotone: the map folds. -/
theorem s_not_monotone {η : ℝ} (hη0 : 0 < η) (hη : 27 < 32 * η ^ 2) : ¬ Monotone (s η) := by
  intro hm
  have h := hm.deriv_nonneg (x := Real.sqrt 2)
  rw [(hasDerivAt_s η (Real.sqrt 2)).deriv] at h
  linarith [sprime_neg_at_sqrt_two hη0 hη]

/-- The flux `𝒥′ s` has `x`-derivative `η y′`. -/
theorem flux_hasDerivAt {η : ℝ} (hη0 : 0 ≤ η) (hη1 : η ≤ 1) (x : ℝ) :
    HasDerivAt (fun x => Jp η x * s η x) (η * yTd x) x := by
  have hfun : (fun x => Jp η x * s η x) = fun x => η * yT x :=
    funext (fun x => gauss_law hη0 hη1 x)
  rw [hfun]
  exact (hasDerivAt_yT x).const_mul η

/-- The bound in terms of `λ_s`: `32 (λ/(1+λ))² < 27 ↔ λ < (27 + 12√6)/5`. -/
theorem threshold_iff {l : ℝ} (hl : 0 ≤ l) :
    32 * (l / (1 + l)) ^ 2 < 27 ↔ l < (27 + 12 * Real.sqrt 6) / 5 := by
  have hr : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  have hr0 : 0 < Real.sqrt 6 := Real.sqrt_pos.mpr (by norm_num)
  have h1 : 0 < 1 + l := by linarith
  have hlm : 0 < l - (27 - 12 * Real.sqrt 6) / 5 := by nlinarith
  rw [div_pow, mul_div_assoc', div_lt_iff₀ (by positivity)]
  constructor
  · intro h
    by_contra hc
    rw [not_lt] at hc
    nlinarith [mul_nonneg (sub_nonneg.mpr hc) hlm.le]
  · intro h
    nlinarith [mul_pos (sub_pos.mpr h) hlm]

end AeSTTotalScalarCorrespondence
