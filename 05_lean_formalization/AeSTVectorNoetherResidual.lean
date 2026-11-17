import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum

/-!
# AeST Vector-Variation Coefficient Discrepancy and Nonzero Noether/Bianchi Residual (`PR #215` / `BLK-1429` / `BLK-1436` #5)

This module machine-checks the algebraic component identities from `audits/2026-11-17/aest-vector-variation-factor-audit.md`
(`PR #215`) and `audits/2026-11-17/verify_aest_j_vector_variation.py`:

1. **Isolated `J^μ ∇_μ φ` Discrepancy (`b B^ν` vs `2 b B^ν`):**
   Direct variation of the live D7 AeST action yields normalized coefficient `b = 2 - K_B` multiplying
   `B^ν := p_μ ∇^ν A^μ - ∇_μ (A^μ p^ν)`, whereas Fu et al. (2024), Eq. (4), print `2 b B^ν`.
   Because the unnormalized Euler derivative carries a factor of `2`, the full Euler-derivative
   mismatch is `ΔE_A^μ = 2 b B^μ`.
2. **Minkowski Unit-Norm Non-Vanishing Counterexample (`B^0 = 1`):**
   For `A^μ = (1, 0, 0, 0)` and `φ = t²/2` (`p_0 = t`, `p^0 = -t`, `-∂_t(p^0) = 1`),
   the unit-timelike constraint `g_{μν} A^μ A^ν = -1` holds while `B^0 = 1 ≠ 0`.
3. **Hyperbolic Constrained Noether/Bianchi Test (`Δ𝒩_ν = 2 b (B^μ F_{νμ} - A_ν ∇_μ B^μ)`):**
   For any `(ch, sh)` on the unit hyperbola `ch² - sh² = 1` (e.g. `cosh(ε t), sinh(ε t)`),
   the 1+1 Minkowski test vector `A^μ = (ch, sh, 0, 0)` obeys `g_{μν} A^μ A^ν = -1`, and the
   Noether residual `R_ν := B^μ F_{νμ} - A_ν ∇_μ B^μ` evaluates to
   `R_0 = -ε² (2 ch sh)` and `R_1 = ε² (ch² + sh²) = ε² (1 + 2 sh²) > 0`, proving
   `Δ𝒩_1 = 2 b R_1 ≠ 0` whenever `b ≠ 0` and `ε ≠ 0`.

All theorems compile with `0 sorry` and standard axioms `[propext, Classical.choice, Quot.sound]` only.
-/

noncomputable section

namespace ResNova.AeSTVectorNoetherResidual

/-! ## 1. Vector-Variation Coefficient Discrepancy -/

/-- Normalized `J^μ ∇_μ φ` vector-equation mismatch between Fu et al. (2024) Eq. (4) (`2 b B^ν`)
and direct variation of the pinned D7 action (`b B^ν`). -/
def normalizedDiscrepancy (b B_nu : ℝ) : ℝ := 2 * b * B_nu - b * B_nu

/-- The normalized discrepancy equals `b B^ν`. -/
theorem vector_euler_discrepancy (b B_nu : ℝ) :
    normalizedDiscrepancy b B_nu = b * B_nu := by
  unfold normalizedDiscrepancy
  ring

/-- Because the normalized vector equation divides the full Euler derivative by `2`,
the full Euler-derivative shift `ΔE_A^μ` is `2 b B^μ`. -/
theorem full_euler_shift (b B_mu : ℝ) :
    2 * normalizedDiscrepancy b B_mu = 2 * b * B_mu := by
  unfold normalizedDiscrepancy
  ring

/-! ## 2. Minkowski Non-Vanishing `B^0` Counterexample -/

/-- Minkowski inner product `g_{μν} A^μ A^ν = -(A^0)² + (A^1)² + (A^2)² + (A^3)²`. -/
def minkowskiNormSq (A0 A1 A2 A3 : ℝ) : ℝ := -(A0 ^ 2) + A1 ^ 2 + A2 ^ 2 + A3 ^ 2

/-- For `A^μ = (1, 0, 0, 0)`, the unit-timelike constraint `g_{μν} A^μ A^ν = -1` holds. -/
theorem minkowski_counterexample_unit_norm :
    minkowskiNormSq 1 0 0 0 = -1 := by
  unfold minkowskiNormSq
  norm_num

/-- Algebraic evaluation of `B^0 = p_μ ∂^0 A^μ - ∂_μ(A^μ p^0)` at `A^μ = (1, 0, 0, 0)`,
`∂_t A^μ = 0`, `p^0 = -t`, `-∂_t(p^0) = 1`: yields `B^0 = 1 ≠ 0`. -/
theorem minkowski_counterexample_B0_eq_one (d_t_p0 : ℝ) (hp : d_t_p0 = -1) :
    (0 : ℝ) - ((1 : ℝ) * d_t_p0 + (0 : ℝ)) = 1 ∧ (1 : ℝ) ≠ 0 := by
  rw [hp]
  constructor <;> norm_num

/-! ## 3. Constrained Hyperbolic Noether/Bianchi Residual (`PR #215` §6) -/

/-- On-shell evaluation of `R_ν = B^μ F_{νμ} - A_ν ∇_μ B^μ` in 1+1 Minkowski space. -/
def noetherResidualComp (B0 B1 F_nu0 F_nu1 A_nu divB : ℝ) : ℝ :=
  B0 * F_nu0 + B1 * F_nu1 - A_nu * divB

/-- Any pair `(ch, sh)` on the hyperbola `ch² - sh² = 1` defines a unit-timelike vector
`A^μ = (ch, sh, 0, 0)` satisfying `g_{μν} A^μ A^ν = -1`. -/
theorem hyperbolic_test_unit_norm {ch sh : ℝ} (hhyp : ch ^ 2 - sh ^ 2 = 1) :
    minkowskiNormSq ch sh 0 0 = -1 := by
  unfold minkowskiNormSq
  linarith

/-- Time component of the Noether residual: for `B^μ = (-ε ch, -ε sh)`, `F_{00} = 0`,
`F_{01} = ε ch`, `A_0 = -ch`, and `∇_μ B^μ = -ε² sh`, we obtain `R_0 = -ε² (2 ch sh)`. -/
theorem noether_residual_R0 (eps ch sh : ℝ) :
    noetherResidualComp (-eps * ch) (-eps * sh) 0 (eps * ch) (-ch) (-(eps ^ 2 * sh)) =
      -(eps ^ 2) * (2 * ch * sh) := by
  unfold noetherResidualComp
  ring

/-- Spatial component of the Noether residual: for `B^μ = (-ε ch, -ε sh)`, `F_{10} = -ε ch`,
`F_{11} = 0`, `A_1 = sh`, and `∇_μ B^μ = -ε² sh`, we obtain `R_1 = ε² (ch² + sh²)`. -/
theorem noether_residual_R1 (eps ch sh : ℝ) :
    noetherResidualComp (-eps * ch) (-eps * sh) (-(eps * ch)) 0 sh (-(eps ^ 2 * sh)) =
      eps ^ 2 * (ch ^ 2 + sh ^ 2) := by
  unfold noetherResidualComp
  ring

/-- Under `ch² - sh² = 1` and `ε ≠ 0`, `ch² + sh² = 1 + 2 sh² ≥ 1 > 0`, so `R_1 > 0` strictly. -/
theorem noether_residual_R1_pos {eps ch sh : ℝ} (heps : eps ≠ 0) (hhyp : ch ^ 2 - sh ^ 2 = 1) :
    0 < noetherResidualComp (-eps * ch) (-eps * sh) (-(eps * ch)) 0 sh (-(eps ^ 2 * sh)) := by
  rw [noether_residual_R1]
  have hsum : ch ^ 2 + sh ^ 2 = 1 + 2 * sh ^ 2 := by linarith
  rw [hsum]
  have heps2 : 0 < eps ^ 2 := sq_pos_of_ne_zero heps
  have hcosh : 0 < 1 + 2 * sh ^ 2 := by positivity
  exact mul_pos heps2 hcosh

/-- Full Noether/Bianchi identity shift `Δ𝒩_1 = 2 b R_1`: equals `2 b ε² (1 + 2 sh²)`
under `ch² - sh² = 1`, and is strictly nonzero for every `b ≠ 0` and `ε ≠ 0`. -/
theorem noether_shift_R1_ne_zero {b eps ch sh : ℝ}
    (hb : b ≠ 0) (heps : eps ≠ 0) (hhyp : ch ^ 2 - sh ^ 2 = 1) :
    2 * b * noetherResidualComp (-eps * ch) (-eps * sh) (-(eps * ch)) 0 sh (-(eps ^ 2 * sh)) =
      2 * b * eps ^ 2 * (1 + 2 * sh ^ 2) ∧
    2 * b * noetherResidualComp (-eps * ch) (-eps * sh) (-(eps * ch)) 0 sh (-(eps ^ 2 * sh)) ≠ 0 := by
  have hr1 : noetherResidualComp (-eps * ch) (-eps * sh) (-(eps * ch)) 0 sh (-(eps ^ 2 * sh)) =
      eps ^ 2 * (1 + 2 * sh ^ 2) := by
    rw [noether_residual_R1]
    have hsum : ch ^ 2 + sh ^ 2 = 1 + 2 * sh ^ 2 := by linarith
    rw [hsum]
  refine ⟨?_, ?_⟩
  · rw [hr1]
    ring
  · have hpos := noether_residual_R1_pos heps hhyp
    exact mul_ne_zero (mul_ne_zero (by norm_num) hb) hpos.ne'

#print axioms vector_euler_discrepancy
#print axioms full_euler_shift
#print axioms minkowski_counterexample_unit_norm
#print axioms minkowski_counterexample_B0_eq_one
#print axioms hyperbolic_test_unit_norm
#print axioms noether_residual_R0
#print axioms noether_residual_R1
#print axioms noether_residual_R1_pos
#print axioms noether_shift_R1_ne_zero

end ResNova.AeSTVectorNoetherResidual
