/-
  HillVortexCore.lean
  Zero-Mathlib Lean 4 formalization of Hill's Spherical Vortex polynomial streamfunction,
  formal radial differentiation, Stokes operator identity, inside-out stalk-to-rim
  reversal, unique equatorial vortex-ring core locus (2 r^2 = R^2, i.e. r_core/R = 1/sqrt(2)),
  and 5D AdS5 static Dark Bubble proper-acceleration algebra.

  Epistemic Scope:
  - [P] Exact polynomial calculus and algebraic identities over Int (zero external imports,
        zero unfinished proof terms, 100% axiom-print coverage).
  - [D] Companion symbolic PDE / Real.sqrt verification:
        06_unification_and_spin/unified_spine_v2/mushroom_toroidal_vortex_probe.py.
  - [O] Any cosmological identification between Hill's hydrodynamic vortex ring and
        de Sitter horizon mechanics remains an open physical hypothesis; cross-sector
        theta = 1/sqrt(2) unification remains retired [X] per POSTULATE_LAYER_DIRECTIVE.
-/

namespace HillVortexCore

/-- Quartic univariate polynomial `a0 + a1*r + a2*r^2 + a3*r^3 + a4*r^4` over `Int`
    for formal radial differentiation without real division. -/
structure Poly4 where
  a0 : Int
  a1 : Int
  a2 : Int
  a3 : Int
  a4 : Int
  deriving DecidableEq, Repr

/-- Evaluate `p : Poly4` at radial coordinate `r : Int`. -/
def polyEval (p : Poly4) (r : Int) : Int :=
  p.a0 + p.a1 * r + p.a2 * r * r + p.a3 * r * r * r + p.a4 * r * r * r * r

/-- Formal radial derivative `d/dr` on `Poly4`. -/
def polyDeriv (p : Poly4) : Poly4 :=
  ⟨p.a1, 2 * p.a2, 3 * p.a3, 4 * p.a4, 0⟩

/-- Hill's interior streamfunction scaled by `4 R^2`:
    `psiScaled(u0, R, r, s) = 3 u0 r^2 (R^2 - r^2) s^2`, where `s = sin(theta)`. -/
def psiScaled (u0 R r s : Int) : Int :=
  3 * u0 * r * r * (R * R - r * r) * s * s

/-- Radial polynomial representation of `psiScaled(u0, R, r, s)`. -/
def hillRadialPoly (u0 R s : Int) : Poly4 :=
  ⟨0, 0, 3 * u0 * R * R * s * s, 0, -3 * u0 * s * s⟩

/-- Radial velocity component scaled by `4 R^2`:
    `urScaled(u0, R, r, c) = 6 u0 (R^2 - r^2) c`, where `c = cos(theta)`. -/
def urScaled (u0 R r c : Int) : Int :=
  6 * u0 * (R * R - r * r) * c

/-- Polar velocity component scaled by `4 R^2` (positive toward increasing `theta` from crown to base):
    `uthetaScaled(u0, R, r, s) = -6 u0 (R^2 - 2 r^2) s`. -/
def uthetaScaled (u0 R r s : Int) : Int :=
  -6 * u0 * (R * R - 2 * r * r) * s

/-- Vertical velocity along the equatorial plane (`theta = pi/2, s = 1, c = 0`), scaled by `4 R^2`:
    `u_z(r, pi/2) = -u_theta(r, pi/2) = 6 u0 (R^2 - 2 r^2)`. -/
def uzEquatorScaled (u0 R r : Int) : Int :=
  -uthetaScaled u0 R r 1

/-- Axisymmetric Stokes operator `(d^2/dr^2 - 2/r^2) psi` scaled by `4 R^2`:
    `stokesScaled(u0, r, s) = -30 u0 r^2 s^2` (exact Euler vorticity proportionality). -/
def stokesScaled (u0 r s : Int) : Int :=
  -30 * u0 * r * r * s * s

/-- Helper ring normalization lemma: `a * (b - c) = a * b - a * c`. -/
theorem int_mul_sub_distrib (a b c : Int) : a * (b - c) = a * b - a * c := by
  exact Int.mul_sub a b c

/-- Theorem 1: `hillRadialPoly` evaluates identically to `psiScaled` for all `(u0, R, r, s)`. -/
theorem hill_poly_eval_eq_psi (u0 R r s : Int) :
    polyEval (hillRadialPoly u0 R s) r = psiScaled u0 R r s := by
  dsimp [polyEval, hillRadialPoly, psiScaled]
  grind

/-- Theorem 2: `uthetaScaled` is derived directly from the formal radial derivative `d(psi)/dr`:
    `-(d psi / dr) = r * s * uthetaScaled(u0, R, r, s)`. -/
theorem hill_utheta_from_formal_deriv (u0 R r s : Int) :
    -polyEval (polyDeriv (hillRadialPoly u0 R s)) r = r * s * uthetaScaled u0 R r s := by
  dsimp [polyEval, polyDeriv, hillRadialPoly, uthetaScaled]
  grind

/-- Theorem 3 (Exact Inviscid Euler / Stokes Operator Cancellation):
    `r^2 * (d^2 psi / dr^2) - 2 * psi = r^2 * (-30 u0 r^2 s^2)`.
    The `R^2 r^2` quadratic terms cancel identically, proving `omega_phi / (r sin theta) = const`. -/
theorem hill_stokes_operator_cancellation (u0 R r s : Int) :
    r * r * polyEval (polyDeriv (polyDeriv (hillRadialPoly u0 R s))) r
      - 2 * polyEval (hillRadialPoly u0 R s) r
    = r * r * stokesScaled u0 r s := by
  dsimp [polyEval, polyDeriv, hillRadialPoly, stokesScaled]
  grind

/-- Theorem 4a: The spherical vortex boundary `r = R` is an exact zero-streamline (`psi = 0`). -/
theorem hill_psi_boundary_zero (u0 R s : Int) : psiScaled u0 R R s = 0 := by
  dsimp [psiScaled]
  grind

/-- Theorem 4b: Normal velocity vanishes identically across the spherical boundary `r = R`. -/
theorem hill_ur_boundary_zero (u0 R c : Int) : urScaled u0 R R c = 0 := by
  dsimp [urScaled]
  grind

/-- Theorem 5a (Upward Stalk Jet vs. Downward Outer Drumskin Roll):
    At the vortex center `r = 0`, vertical flow is `+6 u0 R^2` (`+3/2 u0`), whereas on the
    equatorial boundary `r = R` it reverses to `-6 u0 R^2` (`-3/2 u0`), summing to zero. -/
theorem hill_stalk_to_rim_reversal (u0 R : Int) :
    uzEquatorScaled u0 R 0 = 6 * u0 * (R * R)
    ∧ uzEquatorScaled u0 R R = -(6 * u0 * (R * R))
    ∧ uzEquatorScaled u0 R 0 + uzEquatorScaled u0 R R = 0 := by
  dsimp [uzEquatorScaled, uthetaScaled]
  grind

/-- Theorem 5b: Equatorialradial velocity vanishes identically (`cos(pi/2) = 0`). -/
theorem hill_ur_equator_zero (u0 R r : Int) : urScaled u0 R r 0 = 0 := by
  dsimp [urScaled]
  simp

/-- Theorem 6 (Stationary Toroidal Vortex-Ring Core Theorem):
    For any non-trivial Hill vortex (`u0 != 0`) on the equatorial plane (`s = 1`),
    the polar/vertical velocity vanishes (`uthetaScaled u0 R r 1 = 0`) if and only if
    `2 * r^2 = R^2` (i.e. `(r_core / R)^2 = 1/2`, or `r_core / R = 1 / sqrt(2)`). -/
theorem hill_vortex_core_iff_double_sq (u0 R r : Int) (hu : u0 ≠ 0) :
    uthetaScaled u0 R r 1 = 0 ↔ 2 * (r * r) = R * R := by
  dsimp [uthetaScaled]
  have h6u : -6 * u0 ≠ 0 := by omega
  have hassoc : 2 * r * r = 2 * (r * r) := Int.mul_assoc 2 r r
  rw [hassoc, Int.mul_one]
  constructor
  · intro hzero
    cases Int.mul_eq_zero.mp hzero with
    | inl hleft => exact False.elim (h6u hleft)
    | inr hright => omega
  · intro hcore
    have hsub : R * R - 2 * (r * r) = 0 := by omega
    rw [hsub, Int.mul_zero]

/-- Theorem 7: At the stationary core locus `2 * r^2 = R^2`, the scaled streamfunction attains
    its interior extremum `psiScaled = 3 u0 r^4` (`= (3/16) u0 R^2` after dividing by `4 R^2`). -/
theorem hill_streamfunction_at_core (u0 R r : Int) (hcore : R * R = 2 * (r * r)) :
    psiScaled u0 R r 1 = 3 * u0 * r * r * (r * r) := by
  dsimp [psiScaled]
  rw [hcore]
  have hsub : 2 * (r * r) - r * r = r * r := by omega
  rw [hsub]
  simp only [Int.mul_one]

/-- Theorem 8a (5D AdS5 Static Dark Bubble Proper Acceleration Algebra):
    On a static brane at radius `R_b = 1 / H_dS` in 5D AdS5 with bulk curvature `k`,
    `a_5D^2 = H_dS^2 + k^2` yields `a_5D^2 - k^2 = H_dS^2` directly (unit coefficient `1`,
    no `1 / (2 pi)^2` thermal denominator). -/
theorem ads5_static_brane_accel_diff (a5_sq k H_dS : Int)
    (h_brane : a5_sq = H_dS * H_dS + k * k) :
    a5_sq - k * k = H_dS * H_dS := by
  omega

/-- Theorem 8b: Any positive integer proxy `four_pi_sq >= 39` for `(2 pi)^2 ≈ 39.478`
    strictly prevents `four_pi_sq * a_KMS^2 = H_dS^2` from matching `a_eff^2 = H_dS^2`
    whenever `H_dS != 0` (`a_KMS^2 != a_eff^2`). -/
theorem ads5_kms_two_pi_distinct (four_pi_sq a_kms_sq H_dS : Int)
    (h_pi : four_pi_sq ≥ 39) (h_H : H_dS ≠ 0)
    (h_kms : four_pi_sq * a_kms_sq = H_dS * H_dS) :
    a_kms_sq ≠ H_dS * H_dS := by
  intro heq
  rw [heq] at h_kms
  have hpos : H_dS * H_dS > 0 := by
    cases Int.lt_trichotomy H_dS 0 with
    | inl hneg => exact Int.mul_pos_of_neg_of_neg hneg hneg
    | inr hrest =>
      cases hrest with
      | inl hzero => exact False.elim (h_H hzero)
      | inr hpos1 => exact Int.mul_pos hpos1 hpos1
  have hge : four_pi_sq * (H_dS * H_dS) ≥ 39 * (H_dS * H_dS) :=
    Int.mul_le_mul_of_nonneg_right h_pi (Int.le_of_lt hpos)
  omega

-- Complete axiom-print audit across every theorem in this file
#print axioms int_mul_sub_distrib
#print axioms hill_poly_eval_eq_psi
#print axioms hill_utheta_from_formal_deriv
#print axioms hill_stokes_operator_cancellation
#print axioms hill_psi_boundary_zero
#print axioms hill_ur_boundary_zero
#print axioms hill_stalk_to_rim_reversal
#print axioms hill_ur_equator_zero
#print axioms hill_vortex_core_iff_double_sq
#print axioms hill_streamfunction_at_core
#print axioms ads5_static_brane_accel_diff
#print axioms ads5_kms_two_pi_distinct

end HillVortexCore
