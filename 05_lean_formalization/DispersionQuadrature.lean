/-
  DispersionQuadrature.lean
  Zero-Mathlib Lean 4 formalization of the zero-parameter 3D phase-space dispersion
  quadrature law interpolating smoothly between cold 2D planar disks (`Q_3D = 1` as
  `V / sigma_0 -> infinity`) and isotropic 3D dispersion spheres (`Q_3D = sqrt(2)` as
  `V / sigma_0 -> 0`):

      Q_3D^2(V, sigma_0) = 1 + (3 * sigma_0^2) / (V^2 + 3 * sigma_0^2)
                         = (V^2 + 6 * sigma_0^2) / (V^2 + 3 * sigma_0^2).

  Epistemic Scope:
  - [P] Exact integer-cleared polynomial bounds, endpoint iff characterizations (`sigma_0 = 0`
        iff `Q_3D^2 = 1`; `V = 0` iff `Q_3D^2 = 2`), strict cross-multiplied monotonicity in
        `V^2`, midpoint transition `V^2 = 3 * sigma_0^2` (`Q_3D^2 = 3/2`), and cold-disk
        `< 3%` enclosure for `V >= 10 * sigma_0` (zero unfinished proof terms, complete
        axiom-print coverage).
  - [D] Companion multi-survey evaluation across SPARC, RC100, JWST MSA-3D, ALPINE-CRISTAL,
        and GAMA/KiDS-Legacy: `02_galaxy_dynamics/dispersion_quadrature_audit.py`.
  - [O] Physical identification of `Q_3D(V / sigma_0)` as a covariant Jeans / effective baryon
        coupling factor across disks and ellipticals remains an open theoretical hypothesis;
        cross-sector `theta = 1 / sqrt(2)` unification remains retired `[X]`.
-/

namespace DispersionQuadrature

/-- Total phase-space kinetic denominator `V^2 + 3 * sigma^2` (1 azimuthal + 3 dispersion DoFs). -/
def denPhase (v sig : Int) : Int :=
  v * v + 3 * (sig * sig)

/-- Quadrature-weighted numerator `V^2 + 6 * sigma^2 = (V^2 + 3 * sigma^2) + 3 * sigma^2`. -/
def numPhase (v sig : Int) : Int :=
  v * v + 6 * (sig * sig)

/-- Helper: every integer square is non-negative. -/
theorem sq_nonneg_int (x : Int) : 0 ≤ x * x := by
  cases Int.lt_trichotomy x 0 with
  | inl hneg => exact Int.le_of_lt (Int.mul_pos_of_neg_of_neg hneg hneg)
  | inr hrest =>
    cases hrest with
    | inl hzero => rw [hzero]; omega
    | inr hpos => exact Int.le_of_lt (Int.mul_pos hpos hpos)

/-- Helper: `x * x = 0 ↔ x = 0` over `Int`. -/
theorem sq_eq_zero_iff (x : Int) : x * x = 0 ↔ x = 0 := by
  constructor
  · intro h
    cases Int.mul_eq_zero.mp h with
    | inl h1 => exact h1
    | inr h2 => exact h2
  · intro h
    rw [h]
    rfl

/-- Helper: `x ≠ 0 → 0 < x * x` over `Int`. -/
theorem sq_pos_of_ne_zero (x : Int) (hx : x ≠ 0) : 0 < x * x := by
  cases Int.lt_trichotomy x 0 with
  | inl hneg => exact Int.mul_pos_of_neg_of_neg hneg hneg
  | inr hrest =>
    cases hrest with
    | inl hzero => exact False.elim (hx hzero)
    | inr hpos => exact Int.mul_pos hpos hpos

/-- Theorem 1: `denPhase v sig` is universally non-negative. -/
theorem denPhase_nonneg (v sig : Int) : 0 ≤ denPhase v sig := by
  dsimp [denPhase]
  have hv := sq_nonneg_int v
  have hs := sq_nonneg_int sig
  omega

/-- Theorem 2a: Non-zero rotation `v ≠ 0` implies strictly positive phase-space denominator. -/
theorem denPhase_pos_of_rot (v sig : Int) (hv : v ≠ 0) : 0 < denPhase v sig := by
  dsimp [denPhase]
  have hvp := sq_pos_of_ne_zero v hv
  have hs := sq_nonneg_int sig
  omega

/-- Theorem 2b: Non-zero velocity dispersion `sig ≠ 0` implies strictly positive denominator. -/
theorem denPhase_pos_of_disp (v sig : Int) (hs : sig ≠ 0) : 0 < denPhase v sig := by
  dsimp [denPhase]
  have hv := sq_nonneg_int v
  have hsp := sq_pos_of_ne_zero sig hs
  omega

/-- Theorem 3 (Additive Dispersion Decomposition):
    `numPhase v sig = denPhase v sig + 3 * sig^2`, i.e. `Q_3D^2 = 1 + f_disp`. -/
theorem q3d_additive_decomp (v sig : Int) :
    numPhase v sig = denPhase v sig + 3 * (sig * sig) := by
  dsimp [numPhase, denPhase]
  omega

/-- Theorem 4 (Universal Planar Lower Bound `1 <= Q_3D^2`):
    `denPhase v sig ≤ numPhase v sig` for all `(v, sig)`. -/
theorem q3d_sq_ge_one (v sig : Int) : denPhase v sig ≤ numPhase v sig := by
  dsimp [denPhase, numPhase]
  have hs := sq_nonneg_int sig
  omega

/-- Theorem 5 (Exact Cold Thin-Disk Characterization `Q_3D^2 = 1 ↔ sig = 0`):
    `numPhase v sig = denPhase v sig` holds if and only if velocity dispersion vanishes. -/
theorem q3d_eq_one_iff_cold_disk (v sig : Int) :
    numPhase v sig = denPhase v sig ↔ sig = 0 := by
  dsimp [numPhase, denPhase]
  constructor
  · intro h
    have hsq : sig * sig = 0 := by omega
    exact (sq_eq_zero_iff sig).mp hsq
  · intro hs
    rw [hs]
    omega

/-- Theorem 6 (Universal Isotropic Spherical Upper Bound `Q_3D^2 <= 2`, i.e. `Q_3D <= sqrt(2)`):
    `numPhase v sig ≤ 2 * denPhase v sig` for all `(v, sig)`, with deficit exactly `v^2`. -/
theorem q3d_sq_le_two (v sig : Int) :
    2 * denPhase v sig - numPhase v sig = v * v ∧ numPhase v sig ≤ 2 * denPhase v sig := by
  dsimp [denPhase, numPhase]
  have hv := sq_nonneg_int v
  constructor
  · omega
  · omega

/-- Theorem 7 (Exact Pressure-Supported Sphere Characterization `Q_3D^2 = 2 ↔ v = 0`):
    The upper ceiling `Q_3D = sqrt(2)` (`numPhase = 2 * denPhase`) is attained if and only if
    ordered rotation vanishes (`v = 0`, pure dispersion-supported elliptical limit). -/
theorem q3d_eq_two_iff_zero_rot (v sig : Int) :
    numPhase v sig = 2 * denPhase v sig ↔ v = 0 := by
  dsimp [numPhase, denPhase]
  constructor
  · intro h
    have hv0 : v * v = 0 := by omega
    exact (sq_eq_zero_iff v).mp hv0
  · intro hv
    rw [hv]
    omega

/-- Theorem 8 (Cross-Multiplied Strict Antitonicity in Rotational Support):
    Exact cross-difference identity:
      `numPhase v1 sig * denPhase v2 sig - numPhase v2 sig * denPhase v1 sig`
      `= 3 * sig^2 * (v2^2 - v1^2)`.
    Hence for `sig != 0`, `v1^2 < v2^2` strictly decreases `Q_3D^2(v2, sig) < Q_3D^2(v1, sig)`. -/
theorem q3d_cross_diff_identity (v1 v2 sig : Int) :
    numPhase v1 sig * denPhase v2 sig - numPhase v2 sig * denPhase v1 sig
    = 3 * (sig * sig) * (v2 * v2 - v1 * v1) := by
  dsimp [numPhase, denPhase]
  grind

/-- Theorem 8b: Strict inequality corollary of `q3d_cross_diff_identity` for `sig != 0`. -/
theorem q3d_strict_decreasing_in_rot_sq (v1 v2 sig : Int)
    (hs : sig ≠ 0) (hv : v1 * v1 < v2 * v2) :
    numPhase v2 sig * denPhase v1 sig < numPhase v1 sig * denPhase v2 sig := by
  have hid := q3d_cross_diff_identity v1 v2 sig
  have hsp : 0 < 3 * (sig * sig) := by
    have h1 := sq_pos_of_ne_zero sig hs
    omega
  have hdv : 0 < v2 * v2 - v1 * v1 := by omega
  have hprod : 0 < 3 * (sig * sig) * (v2 * v2 - v1 * v1) := Int.mul_pos hsp hdv
  omega

/-- Theorem 9 (Exact Half-Way Spheroid-Disk Transition `Q_3D^2 = 3/2 ↔ V^2 = 3 * sigma^2`):
    `Q_3D^2` sits exactly halfway between `1` and `2` (`2 * numPhase = 3 * denPhase`)
    if and only if rotational energy equals 3D dispersion energy (`v^2 = 3 * sig^2`, `V/sig = sqrt(3)`). -/
theorem q3d_midpoint_iff_equipartition (v sig : Int) :
    2 * numPhase v sig = 3 * denPhase v sig ↔ v * v = 3 * (sig * sig) := by
  dsimp [numPhase, denPhase]
  omega

/-- Theorem 10 (Cold SPARC Spiral Disk `< 3%` Squared-Boost Enclosure):
    Whenever `V >= 10 * sigma_0` (`v^2 >= 100 * sig^2`), `103 * (numPhase - denPhase) <= 3 * denPhase`,
    i.e. `Q_3D^2 <= 106 / 103` (`Q_3D <= 1.0145`, leaving cold thin disks within `1.45%` of `1`). -/
theorem q3d_cold_spiral_enclosure (v sig : Int) (hcold : 100 * (sig * sig) ≤ v * v) :
    103 * numPhase v sig ≤ 106 * denPhase v sig := by
  dsimp [numPhase, denPhase]
  omega

-- Complete axiom-print verification across all theorems in this module
#print axioms sq_nonneg_int
#print axioms sq_eq_zero_iff
#print axioms sq_pos_of_ne_zero
#print axioms denPhase_nonneg
#print axioms denPhase_pos_of_rot
#print axioms denPhase_pos_of_disp
#print axioms q3d_additive_decomp
#print axioms q3d_sq_ge_one
#print axioms q3d_eq_one_iff_cold_disk
#print axioms q3d_sq_le_two
#print axioms q3d_eq_two_iff_zero_rot
#print axioms q3d_cross_diff_identity
#print axioms q3d_strict_decreasing_in_rot_sq
#print axioms q3d_midpoint_iff_equipartition
#print axioms q3d_cold_spiral_enclosure

end DispersionQuadrature
