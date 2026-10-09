import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Order.Basic
import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum


/-!
# Conditional scalar bounds for an abstract trajectory (historical file, renamed 2026-10-08)

## Overview

This file records elementary consequences of an *assumed* bound on an abstract state.
It does **not** formalize the Navier–Stokes equations, a vorticity field, the
Beale–Kato–Majda time integral, a continuation theorem, or any regularity result.

## What is proved (zero sorry; scope-limited)

  ✓ lipschitz_implies_angle_modulus: for two unit triples, a chord bound ≤ L·d gives a
    sine bound |sin φ| ≤ L·d. Elementary geometry; no Navier–Stokes content and not the
    Constantin–Fefferman criterion.
  ✓ chiral_iff_lipschitz_constant: for scalars, χ ≥ θ ↔ s ≤ L_max·(1 − θ).
  ✓ pointwise_vorticity_product_bound: an assumed bound times a horizon (a product, not a
    time integral).
  ✓ product_bound_below_threshold: an arithmetic consequence of that product bound.
  ✓ assumed_vorticity_bound_projection: returns the assumed bound itself (`st.h_controlled`).

## Renamed 2026-10-08 (identifiers and comments only; proof terms unchanged)

  sovereign_regularity_theorem   → assumed_vorticity_bound_projection
  bkm_vorticity_integral_finite  → pointwise_vorticity_product_bound
  bkm_no_blowup                  → product_bound_below_threshold
  BKMVorticityState              → AssumedVorticityBoundState
  SovereignAlignment.lipschitz_xi (a `True` field) → kinematic_placeholder
The old names described global regularity and a BKM integral; the statements are a
projection of an assumed field and scalar arithmetic.
-/

namespace SovereignRegularity

open Real

/-! ## §1. Abstract Velocity and Vorticity Fields -/

/-- Four real arguments returning a triple. Reading them as (x, y, z, t) is a convention only:
no domain, time variable, regularity or divergence condition is encoded. -/
def VelocityField : Type := ℝ → ℝ → ℝ → ℝ → (ℝ × ℝ × ℝ)

/-- The magnitude of a 3-vector. -/
noncomputable def vmag (v : ℝ × ℝ × ℝ) : ℝ := Real.sqrt (v.1^2 + v.2.1^2 + v.2.2^2)

theorem vmag_nonneg (v : ℝ × ℝ × ℝ) : vmag v ≥ 0 := Real.sqrt_nonneg _


/-! ## §2. A placeholder structure (historically called the alignment condition) -/

/-- Carries `K > 0`, `L > 0` and a `True` placeholder only. It contains no vorticity, no
direction field and no Lipschitz inequality, so it is **not** an alignment condition. -/
structure SovereignAlignment (u : VelocityField) (K L : ℝ) (t : ℝ) : Prop where
  K_pos : K > 0
  L_pos : L > 0
  kinematic_placeholder : True

/-- Fields for which `SovereignAlignment` holds at every `t ≥ 0`. Since that structure has no
alignment content, this constrains only `K` and `L`. -/
def SovereignClass (K L : ℝ) (u : VelocityField) : Prop :=
  ∀ t : ℝ, t ≥ 0 → SovereignAlignment u K L t


/-! ## §3. The Chiral Invariant of a Velocity Field -/

/-- A scalar function of two inputs, read as `sup |∇ξ|` and `L_max` by convention only: no
supremum, gradient, velocity or time enters. -/
noncomputable def velocity_chi (sup_grad_xi L_max : ℝ) : ℝ :=
  1 - min 1 (sup_grad_xi / L_max)

theorem velocity_chi_le_one (s L_max : ℝ) (hL : L_max > 0) (hs : 0 ≤ s) :
    velocity_chi s L_max ≤ 1 := by
  unfold velocity_chi
  have h1 : min 1 (s / L_max) ≥ 0 := by
    apply le_min (by norm_num)
    positivity
  linarith

theorem velocity_chi_nonneg (s L_max : ℝ) (hL : L_max > 0) :
    velocity_chi s L_max ≥ 0 := by
  unfold velocity_chi
  have : min 1 (s / L_max) ≤ 1 := min_le_left _ _
  linarith

/-- The scalar predicate `velocity_chi s L_max ≥ θ` for an arbitrary real `θ`; the value 0.70 is
not imposed here. -/
def sovereign_boundary (sup_grad_xi L_max : ℝ) (θ : ℝ) : Prop :=
  velocity_chi sup_grad_xi L_max ≥ θ


/-! ## §4. A scalar threshold equivalence (it does not mention `SovereignAlignment`) -/

theorem chiral_iff_lipschitz_constant (sup_grad_xi L_max θ : ℝ)
    (hL : L_max > 0) (hθ_low : 0 ≤ θ) (hθ_high : θ ≤ 1) (h_sup_nn : 0 ≤ sup_grad_xi)
    (h_sup_bd : sup_grad_xi ≤ L_max) :
    sovereign_boundary sup_grad_xi L_max θ ↔ sup_grad_xi ≤ L_max * (1 - θ) := by
  unfold sovereign_boundary velocity_chi
  have hratio_nn : 0 ≤ sup_grad_xi / L_max := div_nonneg h_sup_nn (le_of_lt hL)
  have hratio_le : sup_grad_xi / L_max ≤ 1 := by
    rw [div_le_one hL]; exact h_sup_bd
  have hmin : min 1 (sup_grad_xi / L_max) = sup_grad_xi / L_max :=
    min_eq_right hratio_le
  rw [hmin]
  constructor
  · intro h
    have : sup_grad_xi / L_max ≤ 1 - θ := by linarith
    have := (div_le_iff₀ hL).mp this
    linarith
  · intro h
    have : sup_grad_xi / L_max ≤ 1 - θ := by
      rw [div_le_iff₀ hL]; linarith
    linarith


/-! ## §5. Chord bound to sine bound for two unit triples (elementary geometry) -/

theorem lipschitz_implies_angle_modulus
    (xi_x xi_y : ℝ × ℝ × ℝ)
    (hx : vmag xi_x = 1) (hy : vmag xi_y = 1)
    (L dist_xy : ℝ) (hL : L ≥ 0) (hd : dist_xy ≥ 0)
    (h_lip : Real.sqrt ((xi_x.1 - xi_y.1)^2 + (xi_x.2.1 - xi_y.2.1)^2 + (xi_x.2.2 - xi_y.2.2)^2)
             ≤ L * dist_xy) :
    ∃ sin_phi : ℝ, |sin_phi| ≤ L * dist_xy ∧
      sin_phi^2 = 1 - ((xi_x.1 * xi_y.1 + xi_x.2.1 * xi_y.2.1 + xi_x.2.2 * xi_y.2.2))^2 := by
  set cos_phi := xi_x.1 * xi_y.1 + xi_x.2.1 * xi_y.2.1 + xi_x.2.2 * xi_y.2.2 with hcos
  refine ⟨Real.sqrt (1 - cos_phi^2), ?_, ?_⟩
  · rw [abs_of_nonneg (Real.sqrt_nonneg _)]
    have h_lip_sq : ((xi_x.1 - xi_y.1)^2 + (xi_x.2.1 - xi_y.2.1)^2 + (xi_x.2.2 - xi_y.2.2)^2)
                    ≤ (L * dist_xy)^2 := by
      have hsq_nn : 0 ≤ ((xi_x.1 - xi_y.1)^2 + (xi_x.2.1 - xi_y.2.1)^2 + (xi_x.2.2 - xi_y.2.2)^2) := by
        positivity
      have hLd_nn : 0 ≤ L * dist_xy := mul_nonneg hL hd
      have := Real.sq_sqrt hsq_nn
      nlinarith [Real.sqrt_nonneg ((xi_x.1 - xi_y.1)^2 + (xi_x.2.1 - xi_y.2.1)^2 + (xi_x.2.2 - xi_y.2.2)^2),
                 Real.sq_sqrt hsq_nn, sq_nonneg (Real.sqrt ((xi_x.1 - xi_y.1)^2 + (xi_x.2.1 - xi_y.2.1)^2 + (xi_x.2.2 - xi_y.2.2)^2) - L * dist_xy)]
    have h_expand : (xi_x.1 - xi_y.1)^2 + (xi_x.2.1 - xi_y.2.1)^2 + (xi_x.2.2 - xi_y.2.2)^2
                  = 2 * (1 - cos_phi) := by
      have hxx : xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2 = 1 := by
        have := hx
        unfold vmag at this
        have h_sq : (Real.sqrt (xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2))^2 = 1^2 := by rw [this]
        have hnn : (0:ℝ) ≤ xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2 := by positivity
        rw [Real.sq_sqrt hnn] at h_sq
        linarith
      have hyy : xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2 = 1 := by
        have := hy
        unfold vmag at this
        have h_sq : (Real.sqrt (xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2))^2 = 1^2 := by rw [this]
        have hnn : (0:ℝ) ≤ xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2 := by positivity
        rw [Real.sq_sqrt hnn] at h_sq
        linarith
      rw [hcos]; ring_nf; nlinarith [hxx, hyy]
    have h_cos_bound : cos_phi^2 ≤ 1 := by
      have hxx : xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2 = 1 := by
        have := hx; unfold vmag at this
        have h_sq : (Real.sqrt (xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2))^2 = 1^2 := by rw [this]
        have hnn : (0:ℝ) ≤ xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2 := by positivity
        rw [Real.sq_sqrt hnn] at h_sq; linarith
      have hyy : xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2 = 1 := by
        have := hy; unfold vmag at this
        have h_sq : (Real.sqrt (xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2))^2 = 1^2 := by rw [this]
        have hnn : (0:ℝ) ≤ xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2 := by positivity
        rw [Real.sq_sqrt hnn] at h_sq; linarith
      nlinarith [sq_nonneg (xi_x.1 * xi_y.2.1 - xi_x.2.1 * xi_y.1),
                 sq_nonneg (xi_x.1 * xi_y.2.2 - xi_x.2.2 * xi_y.1),
                 sq_nonneg (xi_x.2.1 * xi_y.2.2 - xi_x.2.2 * xi_y.2.1)]
    have h_one_minus_cos_sq : 1 - cos_phi^2 ≤ (L * dist_xy)^2 := by
      have h_one_minus_cos_nn : 0 ≤ 1 - cos_phi := by nlinarith
      have h_one_plus_cos_le : 1 + cos_phi ≤ 2 := by nlinarith
      have h_factor : 1 - cos_phi^2 = (1 - cos_phi) * (1 + cos_phi) := by ring
      rw [h_factor]
      calc (1 - cos_phi) * (1 + cos_phi)
          ≤ (1 - cos_phi) * 2 := by nlinarith
        _ = 2 * (1 - cos_phi) := by ring
        _ = (xi_x.1 - xi_y.1)^2 + (xi_x.2.1 - xi_y.2.1)^2 + (xi_x.2.2 - xi_y.2.2)^2 := by linarith [h_expand]
        _ ≤ (L * dist_xy)^2 := h_lip_sq
    have hLd_nn : 0 ≤ L * dist_xy := mul_nonneg hL hd
    have h_target_nn : 0 ≤ 1 - cos_phi^2 := by linarith [sq_nonneg cos_phi, h_cos_bound]
    have := Real.sqrt_le_sqrt h_one_minus_cos_sq
    rw [Real.sqrt_sq hLd_nn] at this
    exact this
  · have h_one_minus_cos_nn : 0 ≤ 1 - cos_phi^2 := by
      have h_cos_bound : cos_phi^2 ≤ 1 := by
        have hxx : xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2 = 1 := by
          have := hx; unfold vmag at this
          have h_sq : (Real.sqrt (xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2))^2 = 1^2 := by rw [this]
          have hnn : (0:ℝ) ≤ xi_x.1^2 + xi_x.2.1^2 + xi_x.2.2^2 := by positivity
          rw [Real.sq_sqrt hnn] at h_sq; linarith
        have hyy : xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2 = 1 := by
          have := hy; unfold vmag at this
          have h_sq : (Real.sqrt (xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2))^2 = 1^2 := by rw [this]
          have hnn : (0:ℝ) ≤ xi_y.1^2 + xi_y.2.1^2 + xi_y.2.2^2 := by positivity
          rw [Real.sq_sqrt hnn] at h_sq; linarith
        nlinarith [sq_nonneg (xi_x.1 * xi_y.2.1 - xi_x.2.1 * xi_y.1),
                   sq_nonneg (xi_x.1 * xi_y.2.2 - xi_x.2.2 * xi_y.1),
                   sq_nonneg (xi_x.2.1 * xi_y.2.2 - xi_x.2.2 * xi_y.2.1)]
      linarith
    exact Real.sq_sqrt h_one_minus_cos_nn


/-! ## §6. Consequences of an assumed bound (not the BKM integral, not a regularity result) -/

/-- Carries an *assumed* bound `omega_sup t ≤ B` for `t ≥ 0`. `omega_sup` is an arbitrary
function `ℝ → ℝ`: no supremum, vorticity field, PDE or time integral is defined. -/
structure AssumedVorticityBoundState where
  omega_sup : ℝ → ℝ     -- an arbitrary function (named for its intended reading)
  B : ℝ                 -- the assumed bound
  h_B_pos : 0 < B       -- Positive bound
  h_controlled : ∀ t ≥ 0, omega_sup t ≤ B  -- the assumption itself

/-- The product `omega_sup T * T` is at most `B * T`. A product, not a time integral. -/
theorem pointwise_vorticity_product_bound (st : AssumedVorticityBoundState) (T : ℝ) (hT : 0 ≤ T) :
    st.omega_sup T * T ≤ st.B * T := by
  have h_bnd := st.h_controlled T hT
  nlinarith

/-- If `B * T < M` then `omega_sup T * T < M`. Arithmetic, not a non-blowup criterion. -/
theorem product_bound_below_threshold (st : AssumedVorticityBoundState) (T : ℝ) (hT : 0 ≤ T) (M : ℝ) (hM : st.B * T < M) :
    st.omega_sup T * T < M := by
  have h_bnd := st.h_controlled T hT
  have : st.omega_sup T * T ≤ st.B * T := by nlinarith
  linarith

/-- Returns the assumed bound itself (`st.h_controlled T hT`). Not a regularity theorem, not a
continuation statement; formerly named `sovereign_regularity_theorem`. -/
theorem assumed_vorticity_bound_projection (st : AssumedVorticityBoundState) (T : ℝ) (hT : 0 ≤ T) :
    st.omega_sup T ≤ st.B := st.h_controlled T hT

end SovereignRegularity
