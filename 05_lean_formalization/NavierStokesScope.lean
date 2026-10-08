import Mathlib.Tactic

/-!
# Scoped alignment-threshold lemmas

This module intentionally contains only elementary real-number consequences of
an assumed scalar alignment threshold. It does not define the Navier–Stokes
equations, vorticity, a solution class, a Lyapunov functional, a time integral,
or a continuation criterion. Consequently, none of its declarations establishes
Navier–Stokes regularity.

The module is the L0 starting point in `NAVIER_STOKES_DEPENDENCY_AUDIT.md`.
-/

namespace NavierStokesScope

/-- The numerical threshold used in the historical alignment proposal.
This is a scalar parameter choice, not a PDE theorem. -/
noncomputable def alignmentGate : ℝ := 7 / 10

/-- If a scalar `χ` is at least the chosen gate, its deficit from one is at most
`3/10`. This is elementary arithmetic only. -/
theorem alignment_deficit_le_of_ge_gate (χ : ℝ)
    (hχ : alignmentGate ≤ χ) : 1 - χ ≤ 3 / 10 := by
  dsimp [alignmentGate] at hχ ⊢
  linarith

/-- The gate is strictly positive. -/
theorem alignmentGate_pos : 0 < alignmentGate := by
  norm_num [alignmentGate]

/-- The gate is at most one. -/
theorem alignmentGate_le_one : alignmentGate ≤ 1 := by
  norm_num [alignmentGate]

end NavierStokesScope
