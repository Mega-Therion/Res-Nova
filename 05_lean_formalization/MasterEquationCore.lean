import Mathlib
import MuStdUniqueness

/-!
# Master Equation Core — initial typed constitutive slice

This module is deliberately narrower than a covariant master action. It gives a
Lean type to a scalar gradient-magnitude profile and composes the already
canonical `F_std` potential with its positive reference scale. It does not
construct a manifold, metric, volume form, vector bundle, action integral, or
Euler–Lagrange equation; `ℝ` alone does not encode physical units.

Source contract: `MasterEquationSpec.md` (`RN-ME-SPEC-0.1`); equation/term
entries: `MasterEquationTerms.csv`.
-/

namespace ResNova.MasterEquationCore

open ResNova.MuStdUniqueness

/-- Scalar-gradient input data for the AQUAL constitutive slice.
`Point` is only an index type here, not a spacetime manifold. -/
structure ScalarGradientData (Point : Type*) where
  gradientMagnitude : Point → ℝ
  gradientMagnitude_nonneg : ∀ p, 0 ≤ gradientMagnitude p
  referenceScale : ℝ
  referenceScale_pos : 0 < referenceScale

/-- Dimensionless gradient argument. Physical dimensions are documented but
not represented by Lean's real-number type. -/
noncomputable def dimensionlessGradient {Point : Type*} (data : ScalarGradientData Point)
    (p : Point) : ℝ := data.gradientMagnitude p / data.referenceScale

/-- The scalar AQUAL kinetic potential evaluated on the dimensionless gradient.
This is not by itself a spacetime Lagrangian density or action. -/
noncomputable def aqualKineticPotential {Point : Type*}
    (data : ScalarGradientData Point) (p : Point) : ℝ :=
  F_std (dimensionlessGradient data p)

/-- The live convention is `F_std'(x) = x * mu_std(x)`.
This is the existing scalar constitutive identity, not a field equation. -/
theorem canonical_constitutive_identity (x : ℝ) :
  deriv F_std x = x * mu_std x := by
  rw [deriv_F_std]
  exact (x_mul_mu_std x).symm

/-- Every profile point supplies a real-valued argument to the canonical
potential; the explicit non-negativity proof discharges the AQUAL domain
contract at that point. -/
theorem dimensionlessGradient_nonneg {Point : Type*}
    (data : ScalarGradientData Point) (p : Point) :
    0 ≤ dimensionlessGradient data p := by
  unfold dimensionlessGradient
  exact div_nonneg (data.gradientMagnitude_nonneg p) (le_of_lt data.referenceScale_pos)

end ResNova.MasterEquationCore
