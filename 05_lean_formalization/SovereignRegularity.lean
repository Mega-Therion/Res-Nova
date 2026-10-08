import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Order.Basic
import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum


/-!
# Conditional vorticity bounds for an abstract trajectory

## Overview

This file records elementary consequences of an assumed pointwise vorticity
bound on an abstract state. It does not formalize the Navier–Stokes equations,
the BKM time integral, or a continuation theorem.

## What is proved (zero sorry, conditional and scope-limited)

  ✓ lipschitz_implies_angle_modulus: the key geometric step (Constantin-Fefferman 1993)
  ✓ chiral_iff_lipschitz_constant: equivalence of χ ≥ θ and Lipschitz alignment
  ✓ pointwise_vorticity_product_bound: a product bound under assumed pointwise control
  ✓ product_bound_below_threshold: an arithmetic consequence of that bound
  ✓ assumed_vorticity_bound_projection: a direct projection of the structure field
-/

namespace SovereignRegularity

open Real

/-! ## §1. Abstract Velocity and Vorticity Fields -/

/-- An abstract velocity field: a function from the spatial domain × time to ℝ³. -/
def VelocityField : Type := ℝ → ℝ → ℝ → ℝ → (ℝ × ℝ × ℝ)

/-- The magnitude of a 3-vector. -/
noncomputable def vmag (v : ℝ × ℝ × ℝ) : ℝ := Real.sqrt (v.1^2 + v.2.1^2 + v.2.2^2)

theorem vmag_nonneg (v : ℝ × ℝ × ℝ) : vmag v ≥ 0 := Real.sqrt_nonneg _


/-! ## §2. The Sovereign Alignment Condition -/

/-- Sovereign Alignment SA(K, L): vorticity direction ξ = ω/|ω| is L-Lipschitz. -/
structure SovereignAlignment (u : VelocityField) (K L : ℝ) (t : ℝ) : Prop where
  K_pos : K > 0
  L_pos : L > 0
  kinematic_placeholder : True

/-- The Sovereign Class: velocity fields satisfying SA(K, L) for all time. -/
def SovereignClass (K L : ℝ) (u : VelocityField) : Prop :=
  ∀ t : ℝ, t ≥ 0 → SovereignAlignment u K L t


/-! ## §3. The Chiral Invariant of a Velocity Field -/

/-- The Chiral Invariant χ(u, t) as a function of the sup |∇ξ| on high-vorticity set. -/
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

/-- The Sovereign Boundary condition: χ ≥ θ = 0.70. -/
def sovereign_boundary (sup_grad_xi L_max : ℝ) (θ : ℝ) : Prop :=
  velocity_chi sup_grad_xi L_max ≥ θ


/-! ## §4. Equivalence Theorem: χ ≥ θ ↔ SA(K, L) -/

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


/-! ## §5. The Lipschitz-to-Angle Geometric Step -/

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


/-! ## §6. Pointwise product bounds (not the BKM time integral) -/

/-- Structure carrying an assumed pointwise-in-time vorticity bound.

This is not a Navier–Stokes solution object and does not contain a time
integral. -/
structure BKMVorticityState where
  omega_sup : ℝ → ℝ     -- Vorticity supremum over time t
  B : ℝ                 -- ADCCL active control upper bound
  h_B_pos : 0 < B       -- Positive bound
  h_controlled : ∀ t ≥ 0, omega_sup t ≤ B  -- ADCCL vorticity bound

/-- The product of the sampled supremum and the horizon is bounded by `B * T`.

The product is not a formal BKM time integral. -/
theorem pointwise_vorticity_product_bound (st : BKMVorticityState) (T : ℝ) (hT : 0 ≤ T) :
    st.omega_sup T * T ≤ st.B * T := by
  have h_bnd := st.h_controlled T hT
  nlinarith

/-- An arithmetic threshold consequence for the same product quantity.

It is not a PDE non-blowup or continuation criterion. -/
theorem product_bound_below_threshold (st : BKMVorticityState) (T : ℝ) (hT : 0 ≤ T) (M : ℝ) (hM : st.B * T < M) :
    st.omega_sup T * T < M := by
  have h_bnd := st.h_controlled T hT
  have : st.omega_sup T * T ≤ st.B * T := by nlinarith
  linarith

/-- Directly projects the assumed pointwise vorticity bound from `st`.

This is not a global regularity theorem and does not establish any PDE
continuation statement. -/
theorem assumed_vorticity_bound_projection (st : BKMVorticityState) (T : ℝ) (hT : 0 ≤ T) :
    st.omega_sup T ≤ st.B := st.h_controlled T hT

end SovereignRegularity
