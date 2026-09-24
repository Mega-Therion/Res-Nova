import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# The `x ↦ 1/x` involution on the interpolating functions

Companion to `MuStdUniqueness.lean`. That file establishes the *celerity* reading
of `μ_std` (`mu_std_sinh : μ_std(sinh ψ) = tanh ψ`, with `x` the proper velocity
and `μ` the coordinate velocity of one boost). This file adds the one structure
that file does not carry: the behaviour of both branches under `x ↦ 1/x`.

## Creation frame — read before citing

**Motivation.** `x = |∇Φ|/a₀`, so `x ↦ 1/x` is the exchange `a ↦ a₀²/a` — the
Newtonian and deep-MOND regimes swapped about the transition scale. The question
is whether that exchange is a symmetry of the constitutive relation. On the
rational branch it is, in `μ` itself. On the surviving branch it is not; it
survives one level down, in `μ²`.

**Status of the two branches.** `μ_dual = x/(1+x)` is **ruled out** physically by
the solar-system screening bound (anomalous Mercury precession ≈ 10³ × INPOP10a);
see `CURRENT_STATE_READ_THIS_FIRST.md`. Its theorem here is recorded for the
structural account only and carries no physical weight. `μ_std = x/√(1+x²)` is
the live branch.

**Inputs that are NOT derived (this file proves identities, not physics):**

1. That `x = |∇Φ|/a₀` may be read as a celerity at all is an external premise,
   `[O]` — it is `MuStdUniqueness.lean`'s Postulate R, not re-derived here. The
   *algebra* below is unconditional; only the `β`/`γ` **names** depend on it.
2. Nothing here selects `a ↦ a₀²/a` as a physical symmetry. The theorems say the
   map is an involution of the formulae, not that the dynamics is invariant. `[O]`

**Non-claims.** No continuity, no field equation, no empirical content. In
particular `livedual_is_lorentz` is an identity about `tanh` and `cosh`; it does
not establish that the field gradient transforms as a proper velocity.

**What would falsify the reading.** Nothing here is empirical. The *interpretation*
dies if the AeST/Skordis–Złośnik embedding forces a `μ` for which
`theorem_livedual` fails, or if the celerity reading of `x` is rejected.

## Contents

* `mu_std_inv`        — `μ_std(1/x) = 1/√(1+x²)`                            `[thm]`
* `theorem_livedual`  — `μ_std(1/x)² + μ_std(x)² = 1`                       `[thm]`
* `mu_std_inv_eq_inv_cosh_arsinh` — `μ_std(1/x) = 1/cosh(arsinh x) = γ⁻¹`   `[thm]`
* `livedual_is_lorentz` — the same statement read as `β² + γ⁻² = 1`         `[thm]`
* `mu_std_fixed_point` — `μ_std(1) = 1/√2`, the fixed point of the exchange `[thm]`
* `odds_one_sub`      — `odds(1−p) = 1/odds(p)`                             `[thm]`
* `mu_dual_inv`       — dead branch: `μ_dual(1/x) = 1 − μ_dual(x)`          `[thm]`
-/

namespace ResNova.MuStdDuality

open Real

noncomputable section

/-! ## 0. Definitions (kept defeq to `MuStdUniqueness.lean`) -/

/-- The standard interpolating function `μ_std(x) = x/√(1+x²)`. -/
def mu_std (x : ℝ) : ℝ := x / Real.sqrt (1 + x ^ 2)

/-- The rational (ruled-out) interpolating function `μ_dual(x) = x/(1+x)`. -/
def mu_dual (x : ℝ) : ℝ := x / (1 + x)

/-- The Bayesian odds map `odds(p) = p/(1−p)`. -/
def odds (p : ℝ) : ℝ := p / (1 - p)

/-! ## 1. Elementary positivity -/

theorem sqrt_one_add_sq_pos (x : ℝ) : 0 < Real.sqrt (1 + x ^ 2) := by
  apply Real.sqrt_pos.mpr
  nlinarith [sq_nonneg x]

theorem sqrt_one_add_sq_ne (x : ℝ) : Real.sqrt (1 + x ^ 2) ≠ 0 :=
  ne_of_gt (sqrt_one_add_sq_pos x)

/-- `√(1+x²)² = 1+x²`. -/
theorem sq_sqrt_one_add_sq (x : ℝ) : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 := by
  rw [Real.sq_sqrt]
  nlinarith [sq_nonneg x]

/-! ## 2. The live branch under `x ↦ 1/x` -/

/-- The radical collapses under the inverse argument: `√(1+x⁻²) · x = √(1+x²)`
for `x > 0`. -/
theorem sqrt_inv_arg_mul {x : ℝ} (hx : 0 < x) :
    Real.sqrt (1 + (1 / x) ^ 2) * x = Real.sqrt (1 + x ^ 2) := by
  have hx' : x ≠ 0 := ne_of_gt hx
  calc Real.sqrt (1 + (1 / x) ^ 2) * x
      = Real.sqrt (1 + (1 / x) ^ 2) * Real.sqrt (x ^ 2) := by
        rw [Real.sqrt_sq hx.le]
    _ = Real.sqrt ((1 + (1 / x) ^ 2) * x ^ 2) := by
        rw [Real.sqrt_mul (by positivity)]
    _ = Real.sqrt (1 + x ^ 2) := by
        congr 1
        field_simp
        ring

/-- **`μ_std(1/x) = 1/√(1+x²)`** for `x > 0`. -/
theorem mu_std_inv {x : ℝ} (hx : 0 < x) :
    mu_std (1 / x) = 1 / Real.sqrt (1 + x ^ 2) := by
  have hx' : x ≠ 0 := ne_of_gt hx
  have hS : Real.sqrt (1 + (1 / x) ^ 2) ≠ 0 := sqrt_one_add_sq_ne (1 / x)
  have hT : Real.sqrt (1 + x ^ 2) ≠ 0 := sqrt_one_add_sq_ne x
  rw [mu_std, ← sqrt_inv_arg_mul hx]
  field_simp

/-- **Main result `[thm]`.** The `a ↦ a₀²/a` exchange is a symmetry of the live
branch at the level of the **squared** interpolation function:
`μ_std(1/x)² + μ_std(x)² = 1`. -/
theorem theorem_livedual {x : ℝ} (hx : 0 < x) :
    mu_std (1 / x) ^ 2 + mu_std x ^ 2 = 1 := by
  have hT : Real.sqrt (1 + x ^ 2) ≠ 0 := sqrt_one_add_sq_ne x
  rw [mu_std_inv hx, mu_std, div_pow, div_pow, sq_sqrt_one_add_sq]
  have h1 : (1 : ℝ) + x ^ 2 ≠ 0 := by nlinarith [sq_nonneg x]
  field_simp

/-- `μ_std(1/x) = 1/cosh(arsinh x)`. With `x = sinh ψ` this reads `γ⁻¹`. -/
theorem mu_std_inv_eq_inv_cosh_arsinh {x : ℝ} (hx : 0 < x) :
    mu_std (1 / x) = 1 / Real.cosh (Real.arsinh x) := by
  rw [mu_std_inv hx, Real.cosh_arsinh]

/-- **The relativistic reading `[thm]`.** With `x = sinh ψ`
(`MuStdUniqueness.mu_std_sinh : μ_std(sinh ψ) = tanh ψ`), `theorem_livedual` is
exactly `β² + γ⁻² = 1` — the defining relation of the Lorentz factor.

The *algebra* is unconditional; reading `tanh ψ` as `β` and `cosh ψ` as `γ`
requires the celerity premise, which is `[O]`. -/
theorem livedual_is_lorentz (ψ : ℝ) :
    Real.tanh ψ ^ 2 + (1 / Real.cosh ψ) ^ 2 = 1 := by
  have hc : Real.cosh ψ ≠ 0 := ne_of_gt (Real.cosh_pos ψ)
  rw [Real.tanh_eq_sinh_div_cosh]
  field_simp
  nlinarith [Real.cosh_sq_sub_sinh_sq ψ]

/-- The exchange `x ↦ 1/x` has the unique positive fixed point `x = 1`, where
`μ_std = 1/√2` — the chiral floor `θ_g`. -/
theorem mu_std_fixed_point : mu_std 1 = 1 / Real.sqrt 2 := by
  rw [mu_std]
  norm_num

/-! ## 3. Why `1/x`: complementation is inversion through the odds map -/

/-- **`odds(1−p) = 1/odds(p)`** for `p ∈ (0,1)`. This is why `x ↦ 1/x` is the
right involution to test: on any branch where `μ` inverts the odds map,
complementation in the probability *is* inversion in `x`. -/
theorem odds_one_sub {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) :
    odds (1 - p) = 1 / odds p := by
  have h1 : (1 : ℝ) - p ≠ 0 := by linarith
  have h2 : p ≠ 0 := ne_of_gt hp0
  rw [odds, odds, sub_sub_cancel]
  field_simp

/-- **Dead branch `[thm]`, recorded for contrast only.** On the ruled-out rational
branch the duality holds in `μ` itself, not merely in `μ²`:
`μ_dual(1/x) = 1 − μ_dual(x)`.

`μ_dual` is physically excluded (see the header); this is the structural statement
that the live branch *demotes* rather than loses. -/
theorem mu_dual_inv {x : ℝ} (hx : 0 < x) :
    mu_dual (1 / x) = 1 - mu_dual x := by
  have hx' : x ≠ 0 := ne_of_gt hx
  have h1 : (1 : ℝ) + x ≠ 0 := by positivity
  rw [mu_dual, mu_dual]
  field_simp
  ring

/-! ## 4. Axiom audit -/

#print axioms sqrt_inv_arg_mul
#print axioms mu_std_inv
#print axioms theorem_livedual
#print axioms mu_std_inv_eq_inv_cosh_arsinh
#print axioms livedual_is_lorentz
#print axioms mu_std_fixed_point
#print axioms odds_one_sub
#print axioms mu_dual_inv

end

end ResNova.MuStdDuality
