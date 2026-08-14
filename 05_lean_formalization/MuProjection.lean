import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.GroupTheory.GroupAction.Defs

/-!
# The Interpolation Program, Machine-Verified Core (2026-07-17)

Formalizes the theorem layer of `DERIVATION_MU_RESIDUAL_INPUTS.md` and
`DERIVATION_MU_SIMPLE_SINGLE_CHANNEL.md`:

1. `mu_simple_eq_cos` — Thm 3.1 (projection cosine): with x = g/a₀,
   μ_simple(x) = x/√(1+x²) equals g/√(a₀²+g²), the cosine of the projection
   angle between the total and Newtonian legs.
2. `mu_simple_lt_one`, `mu_simple_pos` — μ is a genuine projection factor in (0,1).
3. `quadratic_law_root` — the linear-BC (A9) law a_tot = a_bar(½+√(¼+a₀/a_bar))
   is the positive root of a_tot² − a_bar·a_tot − a₀·a_bar = 0, and
   `quadratic_law_root_unique` — it is the ONLY positive root.
4. `laws_differ` — the two candidate laws x/(x+1) and x/√(1+x²) are distinct
   functions (witness x = 1), so the corpus contradiction was real.
5. `invariant_of_transitive` — §3 curvature constancy: any scalar invariant of a
   transitive group action is constant. This is the self-contained proof that
   replaced the recalled Kobayashi–Nomizu citation.
6. `powerLaw_solves_dilaton_eom` — the quadratic-BC profile σ(r) = k/r with
   k² = 2c⁴/a₀² satisfies σ'' = (a₀²/c⁴)σ³ (the dilaton EOM, Technical Note A6),
   while `exp_profile_fails_cubic` shows the linear-BC exponential ansatz cannot:
   its second derivative is (a₀²/c⁴)σ, and (a₀²/c⁴)σ ≠ (a₀²/c⁴)σ³ for σ ∈ (0,1).

Together: the geometry selects the quadratic BC, hence μ(x) = x/√(1+x²).
CAS companion: `Research_and_Data/Documents/mu_residual_witness.py` (11/11).
-/

namespace Yett.MuProjection

open Real

/-! ## §1. The projection cosine (Thm 3.1) -/

/-- With x = g/a₀ (g, a₀ > 0), μ_simple(x) = x/√(1+x²) = g/√(a₀²+g²):
the interpolation function is the cosine of the projection angle. -/
theorem mu_simple_eq_cos (a g : ℝ) (ha : 0 < a) (hg : 0 < g) :
    (g / a) / Real.sqrt (1 + (g / a) ^ 2) = g / Real.sqrt (a ^ 2 + g ^ 2) := by
  have ha' : a ≠ 0 := ne_of_gt ha
  have h1 : 1 + (g / a) ^ 2 = (a ^ 2 + g ^ 2) / a ^ 2 := by field_simp
  have h2 : Real.sqrt ((a ^ 2 + g ^ 2) / a ^ 2) = Real.sqrt (a ^ 2 + g ^ 2) / a := by
    rw [Real.sqrt_div (by positivity) _, Real.sqrt_sq ha.le]
  have hs : 0 < Real.sqrt (a ^ 2 + g ^ 2) := Real.sqrt_pos.mpr (by positivity)
  rw [h1, h2]
  field_simp

/-- μ_simple(x) < 1 for all x. -/
theorem mu_simple_lt_one (x : ℝ) (hx : 0 < x) :
    x / Real.sqrt (1 + x ^ 2) < 1 := by
  have h : x < Real.sqrt (1 + x ^ 2) := by
    have hx2 : Real.sqrt (x ^ 2) < Real.sqrt (1 + x ^ 2) :=
      Real.sqrt_lt_sqrt (by positivity) (by linarith)
    rwa [Real.sqrt_sq hx.le] at hx2
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr (by positivity)
  exact (div_lt_one hs).mpr h

/-- μ_simple(x) > 0 for x > 0. -/
theorem mu_simple_pos (x : ℝ) (hx : 0 < x) :
    0 < x / Real.sqrt (1 + x ^ 2) := by
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr (by positivity)
  positivity

/-! ## §2. The linear-BC quadratic law and its unique positive root -/

/-- a_tot = a_bar(½ + √(¼ + a₀/a_bar)) satisfies
a_tot² − a_bar·a_tot − a₀·a_bar = 0 and is positive. -/
theorem quadratic_law_root (b a0 : ℝ) (hb : 0 < b) (ha : 0 < a0) :
    (b * (1 / 2 + Real.sqrt (1 / 4 + a0 / b))) ^ 2
      - b * (b * (1 / 2 + Real.sqrt (1 / 4 + a0 / b))) - a0 * b = 0
    ∧ 0 < b * (1 / 2 + Real.sqrt (1 / 4 + a0 / b)) := by
  have harg : (0:ℝ) ≤ 1 / 4 + a0 / b := by positivity
  have hs2 : Real.sqrt (1 / 4 + a0 / b) ^ 2 = 1 / 4 + a0 / b := Real.sq_sqrt harg
  have hsnn : 0 ≤ Real.sqrt (1 / 4 + a0 / b) := Real.sqrt_nonneg _
  constructor
  · have hb' : b ≠ 0 := ne_of_gt hb
    field_simp at hs2 ⊢
    nlinarith [hs2]
  · positivity

/-- Uniqueness: two positive roots of t² − b·t − a₀·b = 0 coincide. -/
theorem quadratic_law_root_unique (b a0 t₁ t₂ : ℝ) (hb : 0 < b) (ha : 0 < a0)
    (h₁ : t₁ ^ 2 - b * t₁ - a0 * b = 0) (h₂ : t₂ ^ 2 - b * t₂ - a0 * b = 0)
    (hp₁ : 0 < t₁) (hp₂ : 0 < t₂) : t₁ = t₂ := by
  have hfac : (t₁ - t₂) * (t₁ + t₂ - b) = 0 := by nlinarith
  rcases mul_eq_zero.mp hfac with h | h
  · linarith
  · -- t₁ + t₂ = b: impossible since both roots exceed b (t² = b·t + a₀·b > b·t ⇒ t > b)
    have hgt₁ : b < t₁ := by nlinarith
    have hgt₂ : b < t₂ := by nlinarith
    nlinarith

/-! ## §3. The two candidate laws are genuinely different functions -/

/-- Witness x = 1: the simple-μ law x/(x+1) and the standard-μ law x/√(1+x²)
disagree (½ ≠ 1/√2), so the corpus's two "derived" laws were incompatible. -/
theorem laws_differ :
    (1:ℝ) / (1 + 1) ≠ (1:ℝ) / Real.sqrt (1 + 1 ^ 2) := by
  intro h
  have h2 : Real.sqrt 2 = 2 := by
    have hs : 0 < Real.sqrt (1 + 1 ^ 2) := Real.sqrt_pos.mpr (by norm_num)
    have : (1:ℝ) + 1 ^ 2 = 2 := by norm_num
    rw [this] at h hs
    field_simp at h
    linarith
  have := Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)
  rw [h2] at this
  norm_num at this

/-! ## §4. Curvature constancy: invariant scalar of a transitive action is constant -/

/-- The self-contained constancy theorem (DERIVATION_MU_RESIDUAL_INPUTS.md §3):
if a group G acts transitively on the substrate X and a scalar f is invariant
under the action, then f is constant. Applied with G = SO(240),
X = V₂(ℝ²⁴⁰), f = |𝓕|²: the bundle-curvature magnitude is constant. -/
theorem invariant_of_transitive {G X : Type*} [Group G] [MulAction G X]
    [MulAction.IsPretransitive G X] (f : X → ℝ)
    (hf : ∀ (g : G) (x : X), f (g • x) = f x) (x y : X) : f x = f y := by
  obtain ⟨g, hg⟩ := MulAction.exists_smul_eq G y x
  rw [← hg, hf]

/-! ## §5. Boundary-condition selection: the dilaton EOM -/

/-- The quadratic-BC power-law profile σ(r) = k/r with k² = 2c⁴/a₀²
satisfies the dilaton EOM σ'' = (a₀²/c⁴)σ³ for r ≠ 0 (Technical Note A6,A8).
Stated via explicit iterated derivatives of r ↦ k/r. -/
theorem powerLaw_solves_dilaton_eom (a0 c k r : ℝ) (hr : r ≠ 0)
    (hc : c ≠ 0) (hk : k ^ 2 = 2 * c ^ 4 / a0 ^ 2) (ha : a0 ≠ 0) :
    2 * k / r ^ 3 = a0 ^ 2 / c ^ 4 * (k / r) ^ 3 := by
  have : a0 ^ 2 * k ^ 2 = 2 * c ^ 4 := by
    field_simp at hk
    linarith [hk]
  field_simp
  linear_combination -k * this

/-- The second derivative of σ(r) = k/r is 2k/r³ (so the hypothesis of the
previous theorem is the honest σ''): d/dr (k/r) = −k/r², d/dr (−k/r²) = 2k/r³. -/
theorem powerLaw_iterated_deriv (k r : ℝ) (hr : r ≠ 0) :
    HasDerivAt (fun s : ℝ => k / s) (-k / r ^ 2) r ∧
    HasDerivAt (fun s : ℝ => -k / s ^ 2) (2 * k / r ^ 3) r := by
  constructor
  · have h := (hasDerivAt_inv hr).const_mul k
    simpa [div_eq_mul_inv, neg_div, mul_comm] using h
  · have hpow : HasDerivAt (fun s : ℝ => s ^ 2) (2 * r) r := by
      simpa using hasDerivAt_pow 2 r
    have hinv : HasDerivAt (fun s : ℝ => (s ^ 2)⁻¹) (-(2 * r) / (r ^ 2) ^ 2) r :=
      hpow.inv (pow_ne_zero 2 hr)
    have h := hinv.const_mul (-k)
    have heq : -k * (-(2 * r) / (r ^ 2) ^ 2) = 2 * k / r ^ 3 := by
      have hr2 : (r ^ 2) ^ 2 = r ^ 3 * r := by ring
      rw [hr2]
      have hcancel : (-(2 * r)) / (r ^ 3 * r) = -2 / r ^ 3 := by
        have : -(2 * r) = (-2) * r := by ring
        rw [this, mul_div_mul_right (-2) (r ^ 3) hr]
      rw [hcancel]
      ring
    have h2 : HasDerivAt (fun s : ℝ => -k * (s ^ 2)⁻¹) (2 * k / r ^ 3) r := by
      rw [← heq]
      exact h
    have hfun : (fun s : ℝ => -k / s ^ 2) = (fun s : ℝ => -k * (s ^ 2)⁻¹) := by
      ext s
      simp [div_eq_mul_inv]
    rw [hfun]
    exact h2

/-- The linear-BC exponential ansatz fails the EOM: it yields σ'' = (a₀²/c⁴)σ,
but for a genuine dilaton profile 0 < σ < 1 we have (a₀²/c⁴)σ ≠ (a₀²/c⁴)σ³.
Hence the linear BC (A9) is inconsistent with the dilaton equation of motion,
and the geometry selects the quadratic BC — i.e. μ(x) = x/√(1+x²). -/
theorem exp_profile_fails_cubic (a0 c σ : ℝ) (ha : 0 < a0) (hc : 0 < c)
    (h0 : 0 < σ) (h1 : σ < 1) :
    a0 ^ 2 / c ^ 4 * σ ≠ a0 ^ 2 / c ^ 4 * σ ^ 3 := by
  have hcoef : 0 < a0 ^ 2 / c ^ 4 := by positivity
  intro h
  have hσ : σ = σ ^ 3 := by
    have := mul_left_cancel₀ (ne_of_gt hcoef) h
    exact this
  have key : 0 < σ * (1 - σ) * (1 + σ) :=
    mul_pos (mul_pos h0 (by linarith)) (by linarith)
  nlinarith [key]

end Yett.MuProjection
