import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# The `ℓⁿ` interpolating family and its duality

`μₙ(x) = x / (1 + xⁿ)^(1/n)`. This is the inverse of Hees et al. 2016's `νₙ` family
(the numerical check is in `02_galaxy_dynamics/mu_n_duality_band.py`). `μ₂` is `μ_std`,
and `μ₁` is the retired `μ_dual`.

## Creation frame — read before citing

**Why this file exists (2026-09-27).** The Cassini external-field quadrupole
(`02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md`) excludes `μ_std = μ₂` at the
derived `a₀` and admits only sharper members of this family. The 2026 bound at 2σ needs
`n ≥ 4.36`. This file asks what structure survives the move from `n = 2` to general `n`.

**What is proved.**
1. `muN_pow`: `μₙ(x)ⁿ = xⁿ / (1 + xⁿ)` for `x ≥ 0`.
2. `muN_dual`: `μₙ(x)ⁿ + μₙ(1/x)ⁿ = 1` for `x > 0`, **every** `n ≥ 1`. `MuStdDuality.lean`'s
   `μ_std(1/x)² + μ_std(x)² = 1` is the `n = 2` member. The `x ↦ 1/x` duality does not
   select `n = 2`.
3. `muN_one_pow`: `μₙ(1)ⁿ = 1/2`, so `μₙ(1) = 2^(-1/n)`. `muN_two_one`: `μ₂(1) = 1/√2`, the
   chiral floor `θ`.

**Inputs NOT derived here.** Nothing selects `n`. That the transition value `μₙ(1)` should
equal a canonical constant (`θ` gives `n = 2`; `κ = 0.9539` gives `n ≈ 14.69`) is a
hypothesis `[conj]`, not a theorem. Cassini excludes the `θ` reading and admits the `κ`
reading; that is an empirical statement made outside this file.

**Non-claims.** No field equation, no empirical content, no selection principle.
-/

noncomputable section

namespace MuNDuality

open Real

/-- The `ℓⁿ` interpolating function `μₙ(x) = x / (1 + xⁿ)^(1/n)`. -/
def muN (n : ℕ) (x : ℝ) : ℝ := x / (1 + x ^ n) ^ ((n : ℝ)⁻¹)

theorem one_add_pow_pos (n : ℕ) {x : ℝ} (hx : 0 ≤ x) : 0 < 1 + x ^ n := by
  have := pow_nonneg hx n
  linarith

/-- `μₙ(x)ⁿ = xⁿ / (1 + xⁿ)`. -/
theorem muN_pow (n : ℕ) (hn : n ≠ 0) {x : ℝ} (hx : 0 ≤ x) :
    muN n x ^ n = x ^ n / (1 + x ^ n) := by
  unfold muN
  rw [div_pow, Real.rpow_inv_natCast_pow (one_add_pow_pos n hx).le hn]

/-- The `x ↦ 1/x` duality holds in `μⁿ` for every `n ≥ 1`. -/
theorem muN_dual (n : ℕ) (hn : n ≠ 0) {x : ℝ} (hx : 0 < x) :
    muN n x ^ n + muN n x⁻¹ ^ n = 1 := by
  rw [muN_pow n hn hx.le, muN_pow n hn (inv_nonneg.mpr hx.le), inv_pow]
  have hxn : 0 < x ^ n := pow_pos hx n
  field_simp
  ring

/-- At the transition point `x = 1`, `μₙ(1)ⁿ = 1/2`. -/
theorem muN_one_pow (n : ℕ) (hn : n ≠ 0) : muN n 1 ^ n = 1 / 2 := by
  rw [muN_pow n hn zero_le_one]
  norm_num

/-- `μ₂` is `μ_std`: `μ₂(x) = x / √(1 + x²)`. -/
theorem muN_two_eq_std (x : ℝ) : muN 2 x = x / Real.sqrt (1 + x ^ 2) := by
  unfold muN
  rw [Real.sqrt_eq_rpow]
  norm_num

/-- `μ₂(1) = 1/√2`, the chiral floor `θ`. -/
theorem muN_two_one : muN 2 1 = 1 / Real.sqrt 2 := by
  rw [muN_two_eq_std]
  norm_num

end MuNDuality
