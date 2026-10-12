import NavierStokesSpec

/-!
# Time-dependent bridge for the kinematic alignment predicate

This module does not define the Navier–Stokes equations and does not claim that
`vorticityOf` is the curl of `u`. It only gives a typed interface: a
time-dependent velocity is paired with an explicitly supplied time-dependent
vorticity assignment, and alignment is stated at every nonnegative time.

The missing PDE theorem is the construction of a suitable `vorticityOf` from a
periodic divergence-free velocity solution together with a proof that the
resulting alignment predicate persists. That theorem is not asserted here.
-/

namespace NavierStokesSpacetimeBridge

open NavierStokesSpec

abbrev TimeDependentVelocity := ℝ → Point3 → Vector3
abbrev TimeDependentVorticity := ℝ → VorticityField

/-- An explicit interface for assigning a time-dependent vorticity field to a
velocity field. No curl identity, regularity, periodicity, or PDE is built in. -/
def VorticityAssignment :=
  TimeDependentVelocity → TimeDependentVorticity

/-- Alignment of the assigned vorticity field for every nonnegative time.
This is an assumption/interface, not a dynamical persistence theorem. -/
def AlignmentAlongVelocity
    (K L ρ : ℝ)
    (u : TimeDependentVelocity)
    (vorticityOf : VorticityAssignment) : Prop :=
  ∀ t : ℝ, 0 ≤ t →
    AlignmentPredicate K L ρ ((vorticityOf u) t)

/-- The direct bridge statement: an assumed time-indexed alignment hypothesis
implies the same alignment proposition at each nonnegative time. -/
theorem alignment_at_time_of_alignment_along_velocity
    (K L ρ : ℝ)
    (u : TimeDependentVelocity)
    (vorticityOf : VorticityAssignment)
    (h_alignment : AlignmentAlongVelocity K L ρ u vorticityOf)
    (t : ℝ) (ht : 0 ≤ t) :
    AlignmentPredicate K L ρ ((vorticityOf u) t) :=
  h_alignment t ht

end NavierStokesSpacetimeBridge
