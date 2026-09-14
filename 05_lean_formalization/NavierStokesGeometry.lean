import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.Tactic

/-!
# Elementary geometry for a vorticity-direction formalization

This module establishes only an elementary norm inequality for unit vectors in
three-dimensional Euclidean space. It does not define a Navier–Stokes solution,
vorticity direction, high-vorticity set, angle modulus, or PDE continuation
criterion. It is an L1 geometric prerequisite, not a regularity result.
-/

namespace NavierStokesGeometry

abbrev Vector3 := EuclideanSpace ℝ (Fin 3)

/-- Two unit vectors in `R^3` are at distance at most two.

This is a geometric inequality that can later be applied to normalized
vorticity directions only after those directions and their nonvanishing
hypotheses have been formally defined. -/
theorem norm_sub_le_two_of_norm_eq_one (x y : Vector3)
    (hx : ‖x‖ = 1) (hy : ‖y‖ = 1) : ‖x - y‖ ≤ 2 := by
  calc
    ‖x - y‖ ≤ ‖x‖ + ‖y‖ := norm_sub_le x y
    _ = 2 := by rw [hx, hy]; norm_num

end NavierStokesGeometry
