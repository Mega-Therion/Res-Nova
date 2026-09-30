import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Tactic
import MuStdUniqueness
import MuStdSelection

/-!
# MuStdFoundations: Formal Foundations of the Standard Interpolating Function

Canonical formalization of the constitutive properties of `μ_std(x) = x / √(1 + x²)`
and its associated AQUAL kinetic potential `F_std(x) = 1/2 [ x √(1+x²) - arsinh(x) ]`.

Author: R.W. Yett (ORCID: 0009-0001-1303-7190)
Project: Res Nova Monograph / Chyren Autonomous Verification Pipeline

## Proven theorems (zero `sorry`, standard axioms `[propext, Classical.choice, Quot.sound]`)
1. **Constitutive derivative & strict convexity**
   - `F_std_deriv_eq`: `F_std′(x) = x · μ_std(x)`.
   - `F_std_deriv2_positivity`: `F_std″(x) > 0` for all `x > 0`.
   - `F_std_strict_convexity`: strict convexity of `F_std` on `[0, ∞)`.
2. **Characteristic speed along the background gradient — SUPERLUMINAL** `[thm]` (math) / `[conj]` (reading)
   - `c_long_sq x := x · F_std″(x) / F_std′(x)`, computed from `deriv F_std`, not typed in.
   - `c_long_sq_eq`: `c_long_sq x = (x² + 2)/(x² + 1)` for `x > 0`.
   - `c_long_sq_superluminal`: `1 < c_long_sq x`; `c_long_sq_le_two`: `c_long_sq x ≤ 2`.

   Physical reading: in the relativistic P(X) (RAQUAL-type) completion `L = f(X)`,
   `X = g^{μν}∂_μφ∂_νφ`, with spacelike background gradient, the quadratic action is
   `f′(−ω² + k_⊥²) + (f′ + 2X f″) k_∥²`, so `c_∥² = 1 + 2X f″/f′ = x F″/F′`, while
   `c_⊥² = 1`. This is the known RAQUAL acausality (Bekenstein 1988).

   **Correction 2026-09-30.** This module previously defined `cs_sq x := (1+x²)/(x²+2)`
   by hand, proved `1/2 ≤ cs_sq < 1`, and labelled it "strict causal subluminality".
   That expression is the ratio of transverse to longitudinal *spatial* stiffness,
   `μ/(xμ)′` = `1/c_∥²`, not a propagation speed: no time-derivative coefficient enters
   it, and pure AQUAL is elliptic and has no sound speed at all. The subluminality claim
   was inverted. The hand-typed definition was also not substitutable: its proofs closed
   for any `μ`. AeST's actual scalar speed is a separate result (D6, `c_s < c` for
   `𝒦₂ ≥ 3.75`) and is not what this module proves.
3. **Screened monopole tail at Saturn**
   - `deviation_le_inv_two_sq`: for all `x ≥ 1`, `1 - μ_std(x) ≤ 1 / (2 x²)`.
   - `saturn_monopole_deviation_le`: for `x ≥ 5·10⁵`, `1 - μ_std(x) ≤ 2·10⁻¹²`.
     (Saturn: `g_N = 6.458·10⁻⁵ m/s²`; at the live `a₀ = 1.1607·10⁻¹⁰`, `x ≈ 5.56·10⁵`.)

   **Scope, corrected 2026-09-30.** This is the isolated-Sun MONOPOLE only. It is *not*
   a Cassini clearance: `1 − μ` is a fractional acceleration shift and is not comparable
   to the Cassini bound on `γ − 1` (a light-propagation parameter), with which it was
   previously compared. The binding Cassini test for MOND is the external-field
   quadrupole `Q₂`, which bare `μ_std` FAILS at ~4.6σ at the derived `a₀`
   (`02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md`); passing requires the
   phenomenological screening of `DWARF_SCREENING_TEST_2026-09-27.md`, which has no
   covariant realization `[O]`.
-/

namespace ResNova.MuStdFoundations

open Real
open ResNova.MuStdUniqueness
open ResNova.MuStdSelection

noncomputable section

/-! ## 1. Constitutive Derivative & Strict Convexity -/

/-- Analytic closed-form first derivative `F_std'(x) = x² / √(1 + x²)`. -/
def F_std_deriv_analytic (x : ℝ) : ℝ := x ^ 2 / Real.sqrt (1 + x ^ 2)

/-- **Theorem 1.1a (Constitutive Identity).**
The analytic derivative of `F_std` satisfies the AQUAL constitutive relation `F'(x) = x · μ_std(x)`. -/
theorem F_std_deriv_eq (x : ℝ) : F_std_deriv_analytic x = x * mu_std x := by
  simp [F_std_deriv_analytic, mu_std, mul_div_assoc, sq]

/-- **Theorem 1.1b (Ghost-Free Strict Convexity).**
The second derivative `F_std″(x) = x (x² + 2) / (1 + x²)^(3/2)` is strictly positive for every `x > 0`. -/
theorem F_std_deriv2_positivity {x : ℝ} (hx : 0 < x) : 0 < F_std_deriv2 x :=
  F_std_deriv2_pos hx

/-- **Theorem 1.1c (Global Strict Convexity on Non-Negative Semi-Axis).**
The potential `F_std` is strictly convex on `[0, ∞)`. -/
theorem F_std_strict_convexity : StrictConvexOn ℝ (Set.Ici (0 : ℝ)) F_std :=
  F_std_strictConvexOn

/-! ## 2. Characteristic Speed Along the Gradient (P(X) completion) -/

/-- Longitudinal characteristic speed squared in the P(X) completion,
`c_∥²(x) = x · F″(x) / F′(x)`, built from the derivatives of `F_std` itself. -/
def c_long_sq (x : ℝ) : ℝ := x * deriv (deriv F_std) x / deriv F_std x

/-- **Theorem 1.2a.** `c_∥²(x) = (x² + 2)/(x² + 1)` for `x > 0`. -/
theorem c_long_sq_eq {x : ℝ} (hx : 0 < x) :
    c_long_sq x = (x ^ 2 + 2) / (x ^ 2 + 1) := by
  have hS : 0 < Real.sqrt (1 + x ^ 2) := sqrt_one_add_sq_pos x
  have hS2 : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 := Real.sq_sqrt (by positivity)
  unfold c_long_sq
  rw [deriv_F_std, deriv_F_std_deriv, F_std_deriv, F_std_deriv2]
  have hx2 : (0 : ℝ) < x ^ 2 + 1 := by positivity
  rw [div_eq_div_iff (by positivity) hx2.ne']
  field_simp
  rw [hS2]
  ring

/-- **Theorem 1.2b (superluminality).** `c_∥²(x) > 1` for every `x > 0`:
the P(X) completion of `μ_std` propagates faster than light along the gradient. -/
theorem c_long_sq_superluminal {x : ℝ} (hx : 0 < x) : 1 < c_long_sq x := by
  rw [c_long_sq_eq hx, one_lt_div (by positivity)]
  linarith

/-- **Theorem 1.2c.** `c_∥²(x) ≤ 2`, with the maximum approached in the deep-MOND limit. -/
theorem c_long_sq_le_two {x : ℝ} (hx : 0 < x) : c_long_sq x ≤ 2 := by
  rw [c_long_sq_eq hx, div_le_iff₀ (by positivity)]
  nlinarith [sq_nonneg x]

/-! ## 3. Screened Monopole Tail -/

/-- **Theorem 1.3 (Inverse-Square Screened Tail).**
For all `x ≥ 1`, `1 - μ_std(x) ≤ 1 / (2 x²)`. -/
theorem deviation_le_inv_two_sq {x : ℝ} (hx : 1 ≤ x) :
    1 - mu_std x ≤ 1 / (2 * x ^ 2) := by
  have hx0 : (0 : ℝ) < x := lt_of_lt_of_le zero_lt_one hx
  have hS : 0 < Real.sqrt (1 + x ^ 2) := sqrt_one_add_sq_pos x
  have hSx : x ≤ Real.sqrt (1 + x ^ 2) := sqrt_ge_self hx0.le
  have h2x2 : (0 : ℝ) < 2 * x ^ 2 := by positivity
  have hprod : 2 * x ^ 2 ≤ Real.sqrt (1 + x ^ 2) * (Real.sqrt (1 + x ^ 2) + x) := by
    nlinarith [hSx, hS, hx0]
  rw [one_sub_mu_std hx0.le, one_div, one_div]
  simpa using inv_anti₀ h2x2 hprod

/-- **Theorem 1.4 (Saturn-orbit monopole deviation).** For `x ≥ 5·10⁵`,
`1 - μ_std(x) ≤ 2·10⁻¹²`. Monopole only; see the module docstring for why this is
not a Cassini clearance (the EFE quadrupole is the binding test and bare `μ_std` fails it). -/
theorem saturn_monopole_deviation_le {x : ℝ} (hx : (500000 : ℝ) ≤ x) :
    1 - mu_std x ≤ 2 / 10 ^ 12 := by
  have hx1 : (1 : ℝ) ≤ x := by linarith
  have hb := deviation_le_inv_two_sq hx1
  have h_bound : 1 / (2 * x ^ 2) ≤ 2 / 10 ^ 12 := by
    rw [div_le_div_iff₀ (by positivity) (by positivity)]
    nlinarith [hx]
  linarith

/-! ## 4. Axiom Footprint Verification -/

#print axioms F_std_deriv_eq
#print axioms F_std_deriv2_positivity
#print axioms F_std_strict_convexity
#print axioms c_long_sq_eq
#print axioms c_long_sq_superluminal
#print axioms c_long_sq_le_two
#print axioms deviation_le_inv_two_sq
#print axioms saturn_monopole_deviation_le

end

end ResNova.MuStdFoundations
