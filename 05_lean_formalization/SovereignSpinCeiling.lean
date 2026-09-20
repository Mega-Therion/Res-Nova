/-
Copyright (c) 2026 R.W. Yett / Chyren / Res-Nova. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: R.W. Yett, Antigravity
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# Conditional Sovereign Spin-Ceiling Algebra & Astrophysical Accretion Shift

This module formally proves the exact algebraic value and interval enclosure of the
Sovereign spin ceiling `a* = √2 - 1/2 ∈ (0.914, 0.915)`, as well as the monotonicity theorem
governing apparent Novikov-Thorne spin inference in the presence of inner-edge magnetic torque.

## Main Results

1. `two_theta_sub_theta_sq`:
   The two-channel polynomial at threshold `θ = 1/√2` yields `2θ - θ² = √2 - 1/2`.

2. `sovereign_spin_ceiling_enclosure`:
   Mechanizes numerical interval bounds: `0.914 < √2 - 1/2 < 0.915`.

3. `novikov_thorne_torque_apparent_spin_shift`:
   Proves that when an inner torque reduces the effective radiative emission radius
   `R_in < R_isco(a_intrinsic)`, an observer fitting a standard zero-torque model
   necessarily infers an apparent spin `a_apparent > a_intrinsic`.
-/

namespace SovereignSpinCeiling

open Real

/-- The adopted algebraic threshold in the conditional two-channel expression. -/
noncomputable def theta : ℝ := 1 / Real.sqrt 2

/-- The two-channel polynomial at the adopted threshold has the claimed exact form. -/
theorem two_theta_sub_theta_sq :
    2 * theta - theta ^ 2 = Real.sqrt 2 - 1 / 2 := by
  unfold theta
  have hsq : (Real.sqrt 2) ^ 2 = (2 : ℝ) := by norm_num
  have hpos : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
  have hne : Real.sqrt 2 ≠ 0 := ne_of_gt hpos
  field_simp [hne]
  nlinarith

/-- Applying the real square root preserves the exact algebraic ceiling equality. -/
theorem sovereign_spin_ceiling_eq :
    Real.sqrt (2 * theta - theta ^ 2) = Real.sqrt (Real.sqrt 2 - 1 / 2) := by
  rw [two_theta_sub_theta_sq]

/-- Exact numerical lower bound on the algebraic ceiling:
    0.914 < Real.sqrt 2 - 1 / 2. -/
theorem sovereign_spin_ceiling_lower_bound :
    (914 : ℝ) / 1000 < Real.sqrt 2 - 1 / 2 := by
  have hsq : (1414 / 1000 : ℝ) ^ 2 < 2 := by norm_num
  have hpos : 0 ≤ (1414 / 1000 : ℝ) := by norm_num
  rw [← Real.sqrt_lt_sqrt_iff (by norm_num)] at hsq
  rw [Real.sqrt_sq hpos] at hsq
  linarith

/-- Exact numerical upper bound on the algebraic ceiling:
    Real.sqrt 2 - 1 / 2 < 0.915. -/
theorem sovereign_spin_ceiling_upper_bound :
    Real.sqrt 2 - 1 / 2 < (915 : ℝ) / 1000 := by
  have hsq : (2 : ℝ) < (1415 / 1000 : ℝ) ^ 2 := by norm_num
  have hpos : 0 ≤ (1415 / 1000 : ℝ) := by norm_num
  rw [← Real.sqrt_lt_sqrt_iff (by norm_num)] at hsq
  rw [Real.sqrt_sq hpos] at hsq
  linarith

/-- Enclosure of the algebraic ceiling in the interval (0.914, 0.915). -/
theorem sovereign_spin_ceiling_enclosure :
    (914 : ℝ) / 1000 < Real.sqrt 2 - 1 / 2 ∧ Real.sqrt 2 - 1 / 2 < (915 : ℝ) / 1000 :=
  ⟨sovereign_spin_ceiling_lower_bound, sovereign_spin_ceiling_upper_bound⟩

/-- Novikov-Thorne disk fitting monotonicity:
    If the effective emission radius is reduced by magnetic torque or coronal hardening
    (R_in < R_isco(a_intrinsic)), and the mapping a ↦ R_isco(a) is strictly anti-monotone,
    then any inferred zero-torque spin satisfies a_apparent > a_intrinsic. -/
theorem novikov_thorne_torque_apparent_spin_shift
    (R_isco : ℝ → ℝ) (a_intrinsic a_apparent R_in : ℝ)
    (h_anti : ∀ a1 a2, a1 < a2 → R_isco a2 < R_isco a1)
    (h_torque : R_in < R_isco a_intrinsic)
    (h_fit : R_isco a_apparent = R_in) :
    a_intrinsic < a_apparent := by
  rcases lt_or_ge a_intrinsic a_apparent with h_good | h_le
  · exact h_good
  · rcases eq_or_lt_of_le h_le with h_eq | h_lt
    · have h_t2 := h_torque
      rw [← h_eq] at h_t2
      rw [h_fit] at h_t2
      exact False.elim (lt_irrefl R_in h_t2)
    · have h_r := h_anti a_apparent a_intrinsic h_lt
      have h_r2 : R_isco a_intrinsic < R_in := by
        rw [← h_fit]
        exact h_r
      have h_contra : R_in < R_in := lt_trans h_torque h_r2
      exact False.elim (lt_irrefl R_in h_contra)

#print axioms two_theta_sub_theta_sq
#print axioms sovereign_spin_ceiling_eq
#print axioms sovereign_spin_ceiling_enclosure
#print axioms novikov_thorne_torque_apparent_spin_shift

end SovereignSpinCeiling

