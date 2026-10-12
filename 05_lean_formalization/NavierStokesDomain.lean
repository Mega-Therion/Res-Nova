import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.Topology.Instances.AddCircle.Defs
import Mathlib.Tactic

/-!
# Periodic three-dimensional domain

This module chooses the quotient representation

```text
T³ = (ℝ / ℤ)³ = Fin 3 → AddCircle 1.
```

`TorusPoint3` is therefore not an ordinary Euclidean point. A later spacetime
module must define fields on this type, or define periodic lifts from Euclidean
coordinates and prove the lift is invariant under integer translations.

This file introduces types, elementary quotient facts, and draft operator
signatures. It does not encode a metric, smoothness, the Navier–Stokes
equations, or a solution class. The operator signatures do not yet provide
derivative semantics on the quotient.
-/

namespace NavierStokesDomain

/-- One unit-period additive circle, `ℝ / ℤ`. -/
abbrev UnitAddCircle := AddCircle (1 : ℝ)

/-- The periodic three-dimensional domain `ℝ³ / ℤ³`. -/
abbrev TorusPoint3 := Fin 3 → UnitAddCircle

/-- Scalar fields on the periodic three-dimensional domain. -/
abbrev TorusScalarField := TorusPoint3 → ℝ

/-- Vector fields on the periodic three-dimensional domain. -/
abbrev TorusVectorField := TorusPoint3 → EuclideanSpace ℝ (Fin 3)

/-- Names used by the spacetime refactor for periodic scalar fields. -/
abbrev PeriodicScalarField := TorusScalarField

/-- Names used by the spacetime refactor for periodic vector fields. -/
abbrev PeriodicVectorField := TorusVectorField

/-- A supplied first-partial-derivative interface on the torus. The type is an
interface only: it does not assert that the supplied functions are derivatives.
-/
abbrev PartialDerivativeOperator :=
  Fin 3 → PeriodicScalarField → PeriodicScalarField

/-- Draft signature for a gradient operator on periodic scalar fields. -/
abbrev GradientOperator :=
  PeriodicScalarField → PeriodicVectorField

/-- Draft signature for a divergence operator on periodic vector fields. -/
abbrev DivergenceOperator :=
  PeriodicVectorField → PeriodicScalarField

/-- Draft signature for a curl operator on periodic vector fields. -/
abbrev CurlOperator :=
  PeriodicVectorField → PeriodicVectorField

/-- A draft bundle of differential-operator interfaces. Its fields are
supplied operations; no field records that an operation satisfies a derivative
law. -/
structure DifferentialOperatorDraft where
  partials : PartialDerivativeOperator
  gradient : GradientOperator
  divergence : DivergenceOperator
  curl : CurlOperator

/-- Gradient assembled from a supplied partial-derivative interface. -/
noncomputable def gradientFromPartial
    (partials : PartialDerivativeOperator)
    (f : PeriodicScalarField) : PeriodicVectorField :=
  fun x => (EuclideanSpace.equiv (Fin 3) ℝ).symm (fun i => partials i f x)

/-- Divergence assembled from a supplied partial-derivative interface. -/
def divergenceFromPartial
    (partials : PartialDerivativeOperator)
    (u : PeriodicVectorField) : PeriodicScalarField :=
  fun x => ∑ i : Fin 3, partials i (fun y => u y i) x

/-- The unit translation vanishes in the quotient circle. -/
theorem unit_period_is_zero : ((1 : ℝ) : UnitAddCircle) = 0 := by
  exact AddCircle.coe_period (1 : ℝ)

/-- Integer translation by one unit has the same quotient coordinate. -/
theorem quotient_coordinate_periodic (x : ℝ) :
    ((x + 1 : ℝ) : UnitAddCircle) = (x : UnitAddCircle) := by
  exact AddCircle.coe_add_period (1 : ℝ) x

/-- A Euclidean field descends to the torus only when it is invariant under
integer translations in every coordinate. This is a predicate, not an
automatic property of an arbitrary Euclidean function. -/
def IntegerPeriodic
    {α : Type} (f : (Fin 3 → ℝ) → α) : Prop :=
  ∀ x : Fin 3 → ℝ, ∀ n : Fin 3 → ℤ,
    f (fun i => x i + n i) = f x

/-- A function on the torus produces an integer-periodic Euclidean lift by
composing with the quotient map in each coordinate. -/
def torusLift
    {α : Type} (f : TorusPoint3 → α) : (Fin 3 → ℝ) → α :=
  fun x => f (fun i => (x i : UnitAddCircle))

end NavierStokesDomain
