import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Euclidean.Angle.Unoriented.Basic
import NavierStokesSpec

/-!
# The periodic global-regularity target, as a statement (no proof)

This module freezes one target: Fefferman's statement (B), the incompressible Navier–Stokes
problem on `ℝ³/ℤ³` with zero force (C. L. Fefferman, *Existence and smoothness of the
Navier–Stokes equation*, 2000). The source text is quoted in
`NAVIER_STOKES_SOURCE_STATEMENTS.md`.

Everything named below is a definition, except four sanity theorems at the end.
**Nothing here proves `PeriodicGlobalRegularity`, and no declaration assumes it.**

Representation choices:
- **Space.** Fields live on Euclidean `ℝ³` (`NavierStokesSpec.Point3`) and are periodic under
  the unit translations `x ↦ x + e_j`, as in Fefferman's (8) and (10). They are not defined
  on a quotient type.
- **Derivatives.** Fréchet derivatives in Euclidean coordinates.
- **Time.** The equations are imposed for `t > 0`, and smoothness is required on the closed
  half-space `[0, ∞) × ℝ³`. A function on `ℝ` has no meaningful two-sided time derivative at
  the initial time, and by continuity the equations then also hold at `t = 0` from the right.

This module also restates the alignment obligation over genuine solutions
(`AlignmentPersistence`, with vorticity the curl of the velocity).
`NavierStokesSpec.PersistenceObligation` quantifies over *every* field, and
`persistenceObligation_false` below shows it is false as stated.
-/

namespace NavierStokesTarget

open NavierStokesSpec
open scoped ContDiff

/-- The unit basis vector `e_j`. -/
noncomputable def e (j : Fin 3) : Point3 := EuclideanSpace.single j (1 : ℝ)

/-- Invariance under the three unit translations (Fefferman's periodicity conditions). -/
def UnitPeriodic {α : Type*} (f : Point3 → α) : Prop :=
  ∀ j : Fin 3, ∀ x : Point3, f (x + e j) = f x

/-- The partial derivative `∂_j f (x)`. -/
noncomputable def pd (j : Fin 3) (f : Point3 → ℝ) (x : Point3) : ℝ :=
  fderiv ℝ f x (e j)

/-- The `i`-th component of a vector field. -/
def comp (v : Point3 → Vector3) (i : Fin 3) : Point3 → ℝ := fun x => v x i

/-- `div v`. -/
noncomputable def divergence (v : Point3 → Vector3) (x : Point3) : ℝ :=
  ∑ j, pd j (comp v j) x

/-- `Δ f`. -/
noncomputable def laplacian (f : Point3 → ℝ) (x : Point3) : ℝ :=
  ∑ j, pd j (pd j f) x

/-- `curl v`, the vorticity of a velocity field. -/
noncomputable def curl (v : Point3 → Vector3) : VorticityField := fun x =>
  !₂[pd 1 (comp v 2) x - pd 2 (comp v 1) x,
     pd 2 (comp v 0) x - pd 0 (comp v 2) x,
     pd 0 (comp v 1) x - pd 1 (comp v 0) x]

/-- A time-dependent velocity field `u(t, x)`. -/
abbrev Velocity := ℝ → Point3 → Vector3

/-- A time-dependent pressure `p(t, x)`. -/
abbrev Pressure := ℝ → Point3 → ℝ

/-- Zero-force incompressible Navier–Stokes at `(t, x)`, componentwise:
`∂ₜuᵢ + Σⱼ uⱼ ∂ⱼuᵢ = ν Δuᵢ − ∂ᵢp` and `div u = 0`. These are Fefferman's (1) and (2) with
`f = 0`. -/
def NavierStokesAt (ν : ℝ) (u : Velocity) (p : Pressure) (t : ℝ) (x : Point3) : Prop :=
  (∀ i : Fin 3,
      deriv (fun s => u s x i) t + ∑ j, u t x j * pd j (comp (u t) i) x
        = ν * laplacian (comp (u t) i) x - pd i (p t) x) ∧
  divergence (u t) x = 0

/-- Smoothness on `[a, b) × ℝ³`, read as joint smoothness in `(t, x)` on that set. -/
def SmoothOn {β : Type*} [NormedAddCommGroup β] [NormedSpace ℝ β]
    (f : ℝ → Point3 → β) (a b : ℝ) : Prop :=
  ContDiffOn ℝ ∞ (fun z : ℝ × Point3 => f z.1 z.2) (Set.Ico a b ×ˢ Set.univ)

/-- Smoothness on the closed half-space `[0, ∞) × ℝ³` (Fefferman's (11)). -/
def SmoothOnClosedHalfSpace {β : Type*} [NormedAddCommGroup β] [NormedSpace ℝ β]
    (f : ℝ → Point3 → β) : Prop :=
  ContDiffOn ℝ ∞ (fun z : ℝ × Point3 => f z.1 z.2) (Set.Ici 0 ×ˢ Set.univ)

/-- Admissible initial data for statement (B): smooth, divergence-free and unit-periodic. -/
def AdmissibleData (u₀ : Point3 → Vector3) : Prop :=
  ContDiff ℝ ∞ u₀ ∧ UnitPeriodic u₀ ∧ ∀ x, divergence u₀ x = 0

/-- A global smooth periodic solution with data `u₀`. It satisfies the equations for `t > 0`,
is smooth on `[0, ∞) × ℝ³`, is spatially periodic for `t ≥ 0`, and has `u(0) = u₀`. -/
def GlobalSmoothPeriodicSolution (ν : ℝ) (u₀ : Point3 → Vector3) (u : Velocity)
    (p : Pressure) : Prop :=
  SmoothOnClosedHalfSpace u ∧ SmoothOnClosedHalfSpace p ∧
  (∀ t, 0 ≤ t → UnitPeriodic (u t)) ∧ u 0 = u₀ ∧
  ∀ t, 0 < t → ∀ x, NavierStokesAt ν u p t x

/-- **Statement (B), as a proposition.** This module does not prove it, and no declaration
assumes it. -/
def PeriodicGlobalRegularity : Prop :=
  ∀ ν : ℝ, 0 < ν → ∀ u₀ : Point3 → Vector3, AdmissibleData u₀ →
    ∃ (u : Velocity) (p : Pressure), GlobalSmoothPeriodicSolution ν u₀ u p

/-- A smooth periodic solution on `[0, T)`. -/
def SmoothPeriodicSolutionOn (ν : ℝ) (u₀ : Point3 → Vector3) (u : Velocity) (p : Pressure)
    (T : ℝ) : Prop :=
  SmoothOn u 0 T ∧ SmoothOn p 0 T ∧ (∀ t, 0 ≤ t → t < T → UnitPeriodic (u t)) ∧
  u 0 = u₀ ∧ ∀ t, 0 < t → t < T → ∀ x, NavierStokesAt ν u p t x

/-- **The open obligation of the conditional program.** Every smooth periodic solution, from
admissible data, satisfies `AlignmentPredicate K L ρ` for its vorticity `curl (u t)` at every
time it exists. Not proved here. -/
def AlignmentPersistence (K L ρ : ℝ) : Prop :=
  ∀ ν : ℝ, 0 < ν → ∀ (u₀ : Point3 → Vector3) (u : Velocity) (p : Pressure) (T : ℝ),
    AdmissibleData u₀ → SmoothPeriodicSolutionOn ν u₀ u p T →
      ∀ t, 0 ≤ t → t < T → AlignmentPredicate K L ρ (curl (u t))

/-! ## Sanity theorems about the definitions (none of them is about regularity) -/

/-- Helper: a component of a constant field is constant. -/
@[simp] theorem comp_const (c : Vector3) (i : Fin 3) : comp (fun _ => c) i = fun _ => c i := rfl

/-- Helper: a partial derivative of a constant function vanishes. -/
@[simp] theorem pd_const (j : Fin 3) (c : ℝ) : pd j (fun _ => c) = fun _ => 0 := by
  funext x
  simp [pd]

/-- The zero field is admissible data, so `AdmissibleData` is not empty. -/
theorem zero_admissible : AdmissibleData (fun _ => 0) := by
  refine ⟨contDiff_const, fun _ _ => rfl, fun x => ?_⟩
  simp [divergence]

/-- The zero velocity and pressure solve the problem for zero data, so the solution predicate
is satisfiable and statement (B) is not vacuously false. -/
theorem zero_solution (ν : ℝ) :
    GlobalSmoothPeriodicSolution ν (fun _ => 0) (fun _ _ => 0) (fun _ _ => 0) := by
  refine ⟨contDiffOn_const, contDiffOn_const, fun _ _ _ _ => rfl, rfl, fun t _ x => ?_⟩
  refine ⟨fun i => ?_, ?_⟩
  · simp [laplacian]
  · simp [divergence]

/-- The equations have content. A spatially constant field that grows in time, `u(t, x) = t e₀`
with zero pressure, fails them at every point: `∂ₜu₀ = 1`, while every other term is `0`. -/
theorem growing_constant_field_not_a_solution (ν t : ℝ) (x : Point3) :
    ¬ NavierStokesAt ν (fun s _ => s • e 0) (fun _ _ => 0) t x := by
  rintro ⟨h, -⟩
  have h0 := h 0
  simp [laplacian, e] at h0

/-- `NavierStokesSpec.PersistenceObligation` is false as stated. It asks `AlignmentPredicate`
of every field, and a field with two nearby high-vorticity points of opposite direction
violates it. This is why `AlignmentPersistence` quantifies over solutions instead. -/
theorem persistenceObligation_false : ¬ PersistenceObligation 1 1 1 := by
  intro h
  let a : Point3 := 0
  let b : Point3 := EuclideanSpace.single 0 (1 / 2 : ℝ)
  let v : Vector3 := EuclideanSpace.single 0 (1 : ℝ)
  have hab : a ≠ b := by
    intro hab
    have := congrArg (fun z : Point3 => z 0) hab
    simp [a, b] at this
  let w : VorticityField := fun x => if x = a then v else if x = b then -v else 0
  have hv : ‖v‖ = 1 := by simp [v]
  have hωa : w a = v := by simp [w]
  have hωb : w b = -v := by simp [w, hab.symm]
  have hdist : dist a b = 1 / 2 := by
    simp [a, b, dist_eq_norm]
  obtain ⟨hx, hy, hle⟩ := h w a b (by simp [HighVorticity, hωa, hv]) (by simp [HighVorticity, hωb, hv])
    (by rw [hdist]; norm_num) (by rw [hdist]; norm_num)
  have hda : direction w a hx = v := by
    simp [direction, hωa, hv]
  have hdb : direction w b hy = -v := by
    simp [direction, hωb, hv]
  rw [hda, hdb, hdist, sub_neg_eq_add] at hle
  have h2 : ‖v + v‖ = 2 := by
    rw [← two_smul ℝ v, norm_smul, hv]; norm_num
  rw [h2] at hle
  norm_num at hle

/-! ## L3a: on one time slice, alignment gives the sine form of the direction condition -/

/-- For unit vectors, the sine of the angle between them is at most the chord length. -/
theorem sin_angle_le_norm_sub (a b : Vector3) (ha : ‖a‖ = 1) (hb : ‖b‖ = 1) :
    Real.sin (InnerProductGeometry.angle a b) ≤ ‖a - b‖ := by
  have hc : Real.cos (InnerProductGeometry.angle a b) = inner ℝ a b := by
    rw [InnerProductGeometry.cos_angle, ha, hb]; simp
  have hs0 : 0 ≤ Real.sin (InnerProductGeometry.angle a b) := InnerProductGeometry.sin_angle_nonneg a b
  have hsq : ‖a - b‖ ^ 2 = 2 - 2 * inner ℝ a b := by
    rw [@norm_sub_sq_real, ha, hb]; ring
  have hcos_le : inner ℝ a b ≤ 1 := by
    have := real_inner_le_norm a b; rw [ha, hb] at this; linarith
  have hcos_ge : -1 ≤ inner ℝ a b := by
    have := neg_le_of_abs_le (abs_real_inner_le_norm a b); rw [ha, hb] at this; linarith
  have hsin2 : Real.sin (InnerProductGeometry.angle a b) ^ 2 = 1 - inner ℝ a b ^ 2 := by
    rw [← hc]; linarith [Real.sin_sq_add_cos_sq (InnerProductGeometry.angle a b)]
  have key : Real.sin (InnerProductGeometry.angle a b) ^ 2 ≤ ‖a - b‖ ^ 2 := by
    rw [hsin2, hsq]; nlinarith
  nlinarith [key, hs0, norm_nonneg (a - b)]

/-- **L3a: kinematic, one time slice.** Suppose `AlignmentPredicate K L ρ ω` holds. Then for any
two high-vorticity points at distance in `(0, ρ]`, the angle `φ` between the vorticity vectors
satisfies `sin φ ≤ L · |x − y|`. This is the sine form of a vorticity-direction condition, with
`ρ_CF = 1 / L`.

It is only the geometric half of L3. It says nothing about:
- time, or a solution class;
- the torus versus `ℝ³`;
- the source's threshold or `δ` conventions (`exploration/navier_stokes/SOURCE_STATEMENTS.md`). -/
theorem alignment_gives_sine_condition {K L ρ : ℝ} {w : VorticityField}
    (h : AlignmentPredicate K L ρ w) {x y : Point3} (hx : HighVorticity K w x)
    (hy : HighVorticity K w y) (h0 : 0 < dist x y) (hρ : dist x y ≤ ρ) :
    Real.sin (InnerProductGeometry.angle (w x) (w y)) ≤ L * dist x y := by
  obtain ⟨hx0, hy0, hle⟩ := h x y hx hy h0 hρ
  have hrx : 0 < ‖w x‖⁻¹ := inv_pos.mpr (norm_pos_iff.mpr hx0)
  have hry : 0 < ‖w y‖⁻¹ := inv_pos.mpr (norm_pos_iff.mpr hy0)
  have hang : InnerProductGeometry.angle (w x) (w y)
      = InnerProductGeometry.angle (direction w x hx0) (direction w y hy0) := by
    unfold direction
    rw [InnerProductGeometry.angle_smul_left_of_pos _ _ hrx,
      InnerProductGeometry.angle_smul_right_of_pos _ _ hry]
  rw [hang]
  exact (sin_angle_le_norm_sub _ _ (direction_unit w x hx0) (direction_unit w y hy0)).trans hle

end NavierStokesTarget
