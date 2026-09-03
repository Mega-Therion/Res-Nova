import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Artanh
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.FinCases

/-!
# Pillar IV — The Chiral Anti-Drift Gate  (WORK IN PROGRESS, SORRIES PRESENT)

Target: FIG Tree Theorem VI.1.

    In a dissipative open quantum system governed by the Lindblad-GKSL master
    equation, the ground-state coherence envelope is preserved if and only if
    the coherent drive `u` equals or exceeds the environmental dissipation `γ`:

        u ≥ γ  ⟺  χ ≥ 1/√2

## Status

Section 1 is closed.
Section 2 constructs the concrete GKSL generator, exhibits its analytical steady state,
and proves `gksl_steady_state_exists` cleanly without `sorry`.
The identification of the physical steady-state coherence with `mu(u/gamma)` remains
an open premise (`coherence_eq_mu_of_gksl`), and Uhlmann fidelity remains open
(`fidelity_half_iff_chi_floor`).

## What is actually being claimed, and where the seam is

The gate has two halves, and only one of them is mathematics:

* **§1 (algebraic).** *If* coherence is the interpolation `μ(x) = x / √(1 + x²)`
  evaluated at the drive-to-dissipation ratio `x = u/γ`, then `χ ≥ 1/√2 ↔ u ≥ γ`
  is an exact real-valued theorem. No approximation, no scaled integers.
  This is proved below.

* **§2 (physical).** That a Lindblad-GKSL generator with drive `u` and
  dissipation `γ` *has* a steady-state coherence equal to `μ(u/γ)` is a claim
  about physics, not about ℝ. It is a premise. Formalizing it requires the
  generator itself, which this module now constructs concretely on `Matrix (Fin 2) (Fin 2) ℂ`.

Conflating the two is exactly the error the earlier `4Leibniz/Harmonia.lean`
made: it took the threshold as a hypothesis over scaled naturals and thereby
proved nothing about `1/√2`. Here the threshold is *derived* in §1 and the
physical identification is *isolated* in §2 where it can be seen.

Note that `μ` here is the same interpolation function the FIG Tree monograph
uses in Pillar I for the MOND transition. Mathlib's `Real.tanh_arsinh` gives
`tanh (arsinh x) = x / √(1 + x²)`, tying this to the rapidity route already
machine-checked in `RapidityEquipartition.lean`.
-/

namespace PillarIV

open Real
open Matrix

/-! ## §1. The algebraic gate — CLOSED -/

/-- The chiral threshold `χ_Y = 1/√2`. -/
noncomputable def chiFloor : ℝ := 1 / Real.sqrt 2

/-- The interpolation function `μ(x) = x / √(1 + x²)`, defined for all reals.
This is the same `μ` used for the MOND transition in Pillar I. -/
noncomputable def mu (x : ℝ) : ℝ := x / Real.sqrt (1 + x ^ 2)

/-- `μ` is the hyperbolic tangent of the rapidity `arsinh x`. This is the bridge
to `RapidityEquipartition.lean`. -/
theorem mu_eq_tanh_arsinh (x : ℝ) : mu x = Real.tanh (Real.arsinh x) := by
  rw [Real.tanh_arsinh, mu]

/-- `1 + x²` is positive, so its square root is too. -/
theorem sqrt_one_add_sq_pos (x : ℝ) : 0 < Real.sqrt (1 + x ^ 2) := by
  apply Real.sqrt_pos.mpr
  nlinarith [sq_nonneg x]

/-- `μ(1) = 1/√2`: the threshold is attained exactly at parity `u = γ`. -/
theorem mu_one : mu 1 = chiFloor := by
  unfold mu chiFloor
  norm_num

-- Name probes: these report the exact signatures available at this Mathlib
-- revision. `div_le_div_iff` does NOT exist here; the ₀-family does.
#check @le_div_iff₀
#check @div_le_iff₀
#check @one_le_div

/-- **The gate, algebraic form.** For a nonnegative ratio `x`, coherence reaches
the chiral floor exactly when the ratio reaches parity. -/
theorem mu_ge_chiFloor_iff {x : ℝ} (hx : 0 ≤ x) : chiFloor ≤ mu x ↔ 1 ≤ x := by
  have hs : 0 < Real.sqrt (1 + x ^ 2) := sqrt_one_add_sq_pos x
  have hsq : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 :=
    Real.sq_sqrt (by nlinarith [sq_nonneg x])
  have hsnn : 0 ≤ Real.sqrt (1 + x ^ 2) := hs.le
  have h2 : (0:ℝ) < Real.sqrt 2 := by
    apply Real.sqrt_pos.mpr; norm_num
  have h2sq : Real.sqrt 2 ^ 2 = (2:ℝ) := Real.sq_sqrt (by norm_num)
  have h2nn : (0:ℝ) ≤ Real.sqrt 2 := h2.le
  unfold chiFloor mu
  -- 1/√2 ≤ x / √(1+x²)  ↔  (1/√2)·√(1+x²) ≤ x
  rw [le_div_iff₀ hs, div_mul_eq_mul_div, one_mul]
  -- √(1+x²)/√2 ≤ x  ↔  √(1+x²) ≤ x·√2
  rw [div_le_iff₀ h2]
  constructor
  · -- √(1+x²) ≤ x·√2  →  1 ≤ x
    intro h
    nlinarith [hsq, h2sq, hsnn, h2nn, hx, sq_nonneg (x - 1), sq_nonneg (x + 1),
               mul_nonneg hx h2nn]
  · -- 1 ≤ x  →  √(1+x²) ≤ x·√2
    intro h
    nlinarith [hsq, h2sq, hsnn, h2nn, hx, sq_nonneg (x - 1),
               sq_nonneg (Real.sqrt (1 + x ^ 2) - x * Real.sqrt 2),
               mul_nonneg hx h2nn]

/-- **The gate, in drive/dissipation variables.** With dissipation `γ > 0` and
nonnegative drive `u`, coherence `μ(u/γ)` reaches `1/√2` exactly when `u ≥ γ`. -/
theorem antiDrift_gate {u gamma : ℝ} (hg : 0 < gamma) (hu : 0 ≤ u) :
    chiFloor ≤ mu (u / gamma) ↔ gamma ≤ u := by
  rw [mu_ge_chiFloor_iff (div_nonneg hu hg.le)]
  rw [le_div_iff₀ hg, one_mul]

/-! ## §2. The Lindblad layer — Concrete GKSL Generator & Steady State

The concrete GKSL (Gorini-Kossakowski-Sudarshan-Lindblad) generator on `Matrix (Fin 2) (Fin 2) ℂ`
describing a driven, damped two-level quantum system:
- Coherent Hamiltonian drive `H(u) = u σ_x = ![![0, u], ![u, 0]]` with `u ≥ 0`
- Environmental dissipation rate `γ > 0`
- Standard lowering operator `L = σ_- = ![![0, 1], ![0, 0]]` as jump operator, with `L† = σ_+`
- Lindblad dissipator `D(ρ) = γ (L ρ L† - (1/2) {L† L, ρ})`
- Master generator `L(ρ) = -i [H(u), ρ] + D(ρ)`
-/

/-- A minimal two-level open-system record: coherent drive and dissipation rate. -/
structure OpenSystem where
  drive : ℝ
  dissipation : ℝ
  drive_nonneg : 0 ≤ drive
  dissipation_pos : 0 < dissipation

/-- The standard lowering operator $\sigma_-$ on $\mathbb{C}^2$. -/
def sigma_minus : Matrix (Fin 2) (Fin 2) ℂ :=
  !![0, 1;
     0, 0]

/-- The standard raising operator $\sigma_+$ on $\mathbb{C}^2$. -/
def sigma_plus : Matrix (Fin 2) (Fin 2) ℂ :=
  !![0, 0;
     1, 0]

/-- The coherent drive Hamiltonian (u) = u \sigma_x$ on $\mathbb{C}^2$. -/
def H (u : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![0, (u : ℂ);
     (u : ℂ), 0]

/-- The Lindblad-GKSL generator $\mathcal{L}_{u,\gamma}(\rho) = -i [H(u), \rho] + \mathcal{D}_\gamma(\rho)$. -/
noncomputable def gksl_generator (u gamma : ℝ) (rho : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  let comm := -Complex.I • (H u * rho - rho * H u)
  let L := sigma_minus
  let L_dag := sigma_plus
  let diss := (gamma : ℂ) • (L * rho * L_dag - (1/2 : ℂ) • (L_dag * L * rho + rho * L_dag * L))
  comm + diss

/-- The exact analytical steady state density matrix $\rho_{\mathrm{ss}}$ of the driven, damped two-level system. -/
noncomputable def steady_state (u gamma : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  let D : ℂ := (gamma : ℂ)^2 + 8 * (u : ℂ)^2
  let r00 := ((gamma : ℂ)^2 + 4 * (u : ℂ)^2) / D
  let r01 := Complex.I * (2 * (gamma : ℂ) * (u : ℂ)) / D
  let r10 := -Complex.I * (2 * (gamma : ℂ) * (u : ℂ)) / D
  let r11 := (4 * (u : ℂ)^2) / D
  !![r00, r01;
     r10, r11]

/-- The algebraic denominator $\gamma^2 + 8 u^2$ is non-zero whenever $\gamma > 0$. -/
theorem denom_ne_zero (u : ℝ) {gamma : ℝ} (hg : 0 < gamma) :
    (gamma : ℂ)^2 + 8 * (u : ℂ)^2 ≠ 0 := by
  have hr : gamma ^ 2 + 8 * u ^ 2 ≠ 0 := by
    have hg2 : 0 < gamma ^ 2 := sq_pos_of_pos hg
    have hu2 : 0 ≤ 8 * u ^ 2 := by nlinarith [sq_nonneg u]
    linarith
  have h_eq : (gamma : ℂ)^2 + 8 * (u : ℂ)^2 = (((gamma ^ 2 + 8 * u ^ 2 : ℝ)) : ℂ) := by
    push_cast; rfl
  rw [h_eq]
  exact Complex.ofReal_ne_zero.mpr hr

/-- The steady state $\rho_{\mathrm{ss}}$ has unit trace $\mathrm{Tr}(\rho_{\mathrm{ss}}) = 1$. -/
theorem trace_steady_state (u gamma : ℝ) (hg : 0 < gamma) :
    Matrix.trace (steady_state u gamma) = 1 := by
  have hD := denom_ne_zero u hg
  dsimp [Matrix.trace, Matrix.diag, steady_state]
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  have h_add : (((gamma : ℂ)^2 + 4 * (u : ℂ)^2) / ((gamma : ℂ)^2 + 8 * (u : ℂ)^2)) +
      ((4 * (u : ℂ)^2) / ((gamma : ℂ)^2 + 8 * (u : ℂ)^2)) =
      (((gamma : ℂ)^2 + 8 * (u : ℂ)^2) / ((gamma : ℂ)^2 + 8 * (u : ℂ)^2)) := by
    rw [← add_div]
    ring
  rw [h_add]
  exact div_self hD

/-- Component (0,0) of the GKSL generator vanishes on $\rho_{\mathrm{ss}}$. -/
theorem steady_state_is_fixed_point_00 (u gamma : ℝ) :
    (gksl_generator u gamma (steady_state u gamma)) 0 0 = 0 := by
  simp [gksl_generator, steady_state, H, sigma_minus, sigma_plus]
  ring_nf
  simp [Complex.I_sq]

/-- Component (1,1) of the GKSL generator vanishes on $\rho_{\mathrm{ss}}$. -/
theorem steady_state_is_fixed_point_11 (u gamma : ℝ) :
    (gksl_generator u gamma (steady_state u gamma)) 1 1 = 0 := by
  simp [gksl_generator, steady_state, H, sigma_minus, sigma_plus]
  ring_nf
  simp [Complex.I_sq]

/-- Component (0,1) of the GKSL generator vanishes on $\rho_{\mathrm{ss}}$. -/
theorem steady_state_is_fixed_point_01 (u gamma : ℝ) :
    (gksl_generator u gamma (steady_state u gamma)) 0 1 = 0 := by
  simp [gksl_generator, steady_state, H, sigma_minus, sigma_plus]
  ring

/-- Component (1,0) of the GKSL generator vanishes on $\rho_{\mathrm{ss}}$. -/
theorem steady_state_is_fixed_point_10 (u gamma : ℝ) :
    (gksl_generator u gamma (steady_state u gamma)) 1 0 = 0 := by
  simp [gksl_generator, steady_state, H, sigma_minus, sigma_plus]
  ring

/-- $\rho_{\mathrm{ss}}$ is an exact fixed point: $\mathcal{L}_{u,\gamma}(\rho_{\mathrm{ss}}) = 0$. -/
theorem steady_state_is_fixed_point (u gamma : ℝ) :
    gksl_generator u gamma (steady_state u gamma) = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  · exact steady_state_is_fixed_point_00 u gamma
  · exact steady_state_is_fixed_point_01 u gamma
  · exact steady_state_is_fixed_point_10 u gamma
  · exact steady_state_is_fixed_point_11 u gamma

/-- A density matrix $\rho$ is a physical steady state if it is annihilated by the GKSL generator and has unit trace. -/
def IsSteadyState (u gamma : ℝ) (rho : Matrix (Fin 2) (Fin 2) ℂ) : Prop :=
  gksl_generator u gamma rho = 0 ∧ Matrix.trace rho = 1

/-- **CLOSED (Task A.1 & A.2).** The GKSL generator for the driven, damped two-level
system possesses an exact physical steady state with unit trace. -/
theorem gksl_steady_state_exists (S : OpenSystem) :
    ∃ rho : Matrix (Fin 2) (Fin 2) ℂ, IsSteadyState S.drive S.dissipation rho := by
  refine ⟨steady_state S.drive S.dissipation, steady_state_is_fixed_point S.drive S.dissipation,
          trace_steady_state S.drive S.dissipation S.dissipation_pos⟩

/-- The Bloch transverse coherence function C(x) = 4x / (1 + 8x^2) for x = u/gamma >= 0. -/
noncomputable def blochCoherence (x : ℝ) : ℝ := 4 * x / (1 + 8 * x ^ 2)

theorem bloch_denom_pos (x : ℝ) : 0 < 1 + 8 * x ^ 2 := by
  have : 0 ≤ 8 * x ^ 2 := by nlinarith [sq_nonneg x]
  linarith

theorem bloch_coherence_le_theta (x : ℝ) (hx : 0 ≤ x) :
    blochCoherence x ≤ chiFloor := by
  have hden : 0 < 1 + 8 * x ^ 2 := bloch_denom_pos x
  have hsq2 : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr zero_lt_two
  have h_sq : (4 * x * Real.sqrt 2) ^ 2 ≤ (1 + 8 * x ^ 2) ^ 2 := by
    have h1 : (4 * x * Real.sqrt 2) ^ 2 = 32 * x ^ 2 := by
      calc (4 * x * Real.sqrt 2) ^ 2 = (4 * x) ^ 2 * (Real.sqrt 2) ^ 2 := mul_pow (4 * x) (Real.sqrt 2) 2
      _ = (16 * x ^ 2) * 2 := by rw [Real.sq_sqrt zero_le_two]; ring
      _ = 32 * x ^ 2 := by ring
    have h2 : (1 + 8 * x ^ 2) ^ 2 - 32 * x ^ 2 = (8 * x ^ 2 - 1) ^ 2 := by ring
    have h3 : 0 ≤ (8 * x ^ 2 - 1) ^ 2 := sq_nonneg (8 * x ^ 2 - 1)
    linarith
  have h_le : 4 * x * Real.sqrt 2 ≤ 1 + 8 * x ^ 2 := by
    have h_lhs_nonneg : 0 ≤ 4 * x * Real.sqrt 2 := by
      have : 0 ≤ 4 * x := by linarith
      exact mul_nonneg this (le_of_lt hsq2)
    have h_rhs_nonneg : 0 ≤ 1 + 8 * x ^ 2 := le_of_lt hden
    have h_abs : |4 * x * Real.sqrt 2| ≤ |1 + 8 * x ^ 2| := (sq_le_sq).mp h_sq
    rw [abs_of_nonneg h_lhs_nonneg, abs_of_nonneg h_rhs_nonneg] at h_abs
    exact h_abs
  have h1 : 4 * x ≤ (1 + 8 * x ^ 2) / Real.sqrt 2 := by
    rw [le_div_iff₀ hsq2]
    linarith [h_le]
  dsimp [blochCoherence, chiFloor]
  rw [div_le_iff₀ hden]
  have h2 : (1 / Real.sqrt 2) * (1 + 8 * x ^ 2) = (1 + 8 * x ^ 2) / Real.sqrt 2 := by ring
  rw [h2]
  exact h1

theorem bloch_coherence_eq_theta_iff (x : ℝ) (hx : 0 ≤ x) :
    blochCoherence x = chiFloor ↔ x = 1 / (2 * Real.sqrt 2) := by
  have hden : 0 < 1 + 8 * x ^ 2 := bloch_denom_pos x
  have hsq2 : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr zero_lt_two
  constructor
  · intro h
    dsimp [blochCoherence, chiFloor] at h
    have h_cross : 4 * x * Real.sqrt 2 = 1 + 8 * x ^ 2 := by
      have h1 : (4 * x / (1 + 8 * x ^ 2)) * (1 + 8 * x ^ 2) = (1 / Real.sqrt 2) * (1 + 8 * x ^ 2) := by rw [h]
      rw [div_mul_cancel₀ (4 * x) (ne_of_gt hden)] at h1
      have h2 : 4 * x * Real.sqrt 2 = ((1 / Real.sqrt 2) * (1 + 8 * x ^ 2)) * Real.sqrt 2 := by rw [h1]
      have h3 : ((1 / Real.sqrt 2) * (1 + 8 * x ^ 2)) * Real.sqrt 2 = 1 + 8 * x ^ 2 := by
        calc ((1 / Real.sqrt 2) * (1 + 8 * x ^ 2)) * Real.sqrt 2 = ((1 + 8 * x ^ 2) / Real.sqrt 2) * Real.sqrt 2 := by ring
        _ = 1 + 8 * x ^ 2 := div_mul_cancel₀ (1 + 8 * x ^ 2) (ne_of_gt hsq2)
      rw [h3] at h2
      exact h2
    have h_sq_diff : (8 * x ^ 2 - 1) ^ 2 = 0 := by
      have h_alg : (8 * x ^ 2 - 1) ^ 2 = (1 + 8 * x ^ 2) ^ 2 - (4 * x * Real.sqrt 2) ^ 2 := by
        calc (8 * x ^ 2 - 1) ^ 2 = (1 + 8 * x ^ 2) ^ 2 - 32 * x ^ 2 := by ring
        _ = (1 + 8 * x ^ 2) ^ 2 - (4 * x) ^ 2 * (Real.sqrt 2) ^ 2 := by rw [Real.sq_sqrt zero_le_two]; ring
        _ = (1 + 8 * x ^ 2) ^ 2 - (4 * x * Real.sqrt 2) ^ 2 := by rw [← mul_pow]
      rw [h_alg, ← h_cross]
      ring
    have h_root : 8 * x ^ 2 - 1 = 0 := sq_eq_zero_iff.mp h_sq_diff
    have h_x2 : x ^ 2 = 1 / 8 := by linarith
    have h_target_sq : (1 / (2 * Real.sqrt 2)) ^ 2 = 1 / 8 := by
      calc (1 / (2 * Real.sqrt 2)) ^ 2 = 1 / (2 * Real.sqrt 2) ^ 2 := by ring
      _ = 1 / (4 * (Real.sqrt 2) ^ 2) := by ring
      _ = 1 / (4 * 2) := by rw [Real.sq_sqrt zero_le_two]
      _ = 1 / 8 := by ring
    have h_sq_eq : x ^ 2 = (1 / (2 * Real.sqrt 2)) ^ 2 := by rw [h_x2, h_target_sq]
    have h_nonneg_target : 0 ≤ 1 / (2 * Real.sqrt 2) := by
      have : 0 < 2 * Real.sqrt 2 := by linarith
      exact le_of_lt (one_div_pos.mpr this)
    have h_abs_eq : |x| = |1 / (2 * Real.sqrt 2)| := (sq_eq_sq_iff_abs_eq_abs x (1 / (2 * Real.sqrt 2))).mp h_sq_eq
    rw [abs_of_nonneg hx, abs_of_nonneg h_nonneg_target] at h_abs_eq
    exact h_abs_eq
  · intro h
    rw [h]
    dsimp [blochCoherence, chiFloor]
    have h_x_sq : (1 / (2 * Real.sqrt 2)) ^ 2 = 1 / 8 := by
      calc (1 / (2 * Real.sqrt 2)) ^ 2 = 1 / (2 * Real.sqrt 2) ^ 2 := by ring
      _ = 1 / (4 * (Real.sqrt 2) ^ 2) := by ring
      _ = 1 / (4 * 2) := by rw [Real.sq_sqrt zero_le_two]
      _ = 1 / 8 := by ring
    have h_den : 1 + 8 * (1 / (2 * Real.sqrt 2)) ^ 2 = 2 := by
      rw [h_x_sq]
      ring
    have h_num : 4 * (1 / (2 * Real.sqrt 2)) = 2 / Real.sqrt 2 := by
      calc 4 * (1 / (2 * Real.sqrt 2)) = (4 * 1) / (2 * Real.sqrt 2) := by ring
      _ = 2 / Real.sqrt 2 := by
        have : (4 : ℝ) = 2 * 2 := by norm_num
        rw [this]
        have h_cancel : (2 * 2 * 1) / (2 * Real.sqrt 2) = 2 / Real.sqrt 2 := by
          have h2ne : (2 : ℝ) ≠ 0 := by norm_num
          have hsqne : Real.sqrt 2 ≠ 0 := ne_of_gt hsq2
          field_simp
        exact h_cancel
    rw [h_den, h_num]
    have h_div2 : (2 / Real.sqrt 2) / 2 = 1 / Real.sqrt 2 := by ring
    exact h_div2

theorem steady_state_coherence_im_eq_bloch (u gamma : ℝ) (hg : 0 < gamma) (_hu : 0 ≤ u) :
    2 * ((steady_state u gamma) 0 1).im = blochCoherence (u / gamma) := by
  dsimp [steady_state, blochCoherence]
  have hg2 : 0 < gamma ^ 2 := sq_pos_of_pos hg
  have hg_ne : gamma ≠ 0 := ne_of_gt hg
  have h_den_r : 0 < gamma ^ 2 + 8 * u ^ 2 := by
    have : 0 ≤ 8 * u ^ 2 := by nlinarith [sq_nonneg u]
    linarith
  have h_den_ne : gamma ^ 2 + 8 * u ^ 2 ≠ 0 := ne_of_gt h_den_r
  have h_im_r01 : (Complex.I * (2 * (gamma : ℂ) * (u : ℂ)) / ((gamma : ℂ)^2 + 8 * (u : ℂ)^2)).im =
      (2 * gamma * u) / (gamma ^ 2 + 8 * u ^ 2) := by
    have h_den_C_eq : (gamma : ℂ) ^ 2 + 8 * (u : ℂ) ^ 2 = ((gamma ^ 2 + 8 * u ^ 2 : ℝ) : ℂ) := by
      push_cast; rfl
    have h_num_C_eq : Complex.I * (2 * (gamma : ℂ) * (u : ℂ)) = ((2 * gamma * u : ℝ) : ℂ) * Complex.I := by
      push_cast; ring
    rw [h_num_C_eq, h_den_C_eq]
    rw [Complex.div_ofReal_im]
    have : (((2 * gamma * u : ℝ) : ℂ) * Complex.I).im = 2 * gamma * u := by
      simp only [Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im]
      ring
    rw [this]
  rw [h_im_r01]
  have h_alg : 2 * ((2 * gamma * u) / (gamma ^ 2 + 8 * u ^ 2)) = (4 * gamma * u) / (gamma ^ 2 + 8 * u ^ 2) := by ring
  rw [h_alg]
  have h_div_scale : 4 * (u / gamma) / (1 + 8 * (u / gamma) ^ 2) =
      (4 * (u / gamma) * gamma ^ 2) / ((1 + 8 * (u / gamma) ^ 2) * gamma ^ 2) := by
    exact (mul_div_mul_right (4 * (u / gamma)) (1 + 8 * (u / gamma) ^ 2) (ne_of_gt hg2)).symm
  rw [h_div_scale]
  have h_num_eq : 4 * (u / gamma) * gamma ^ 2 = 4 * gamma * u := by
    calc 4 * (u / gamma) * gamma ^ 2 = 4 * ((u / gamma) * gamma * gamma) := by ring
    _ = 4 * (u * gamma) := by rw [div_mul_cancel₀ u hg_ne]
    _ = 4 * gamma * u := by ring
  have h_den_eq : (1 + 8 * (u / gamma) ^ 2) * gamma ^ 2 = gamma ^ 2 + 8 * u ^ 2 := by
    have : (u / gamma) ^ 2 = u ^ 2 / gamma ^ 2 := div_pow u gamma 2
    rw [this]
    calc (1 + 8 * (u ^ 2 / gamma ^ 2)) * gamma ^ 2 = gamma ^ 2 + 8 * (u ^ 2 / gamma ^ 2 * gamma ^ 2) := by ring
    _ = gamma ^ 2 + 8 * u ^ 2 := by rw [div_mul_cancel₀ (u ^ 2) (ne_of_gt hg2)]
  rw [h_num_eq, h_den_eq]

/-!
### Task B: Status of the Former Identification `coherence_eq_mu_of_gksl`

The earlier identification `steadyStateCoherence S = mu(u/gamma)` (and the derived
`antiDrift_theorem`) has been retired.

**Mathematical / Physical Reason:**
1. Concrete GKSL Coherence: The transverse coherence of the physical 2-level GKSL steady state
   is given by `C(x) = 2 |rho_{01}| = 4x / (1 + 8x^2)` for `x = u / gamma >= 0`.
   This is non-monotonic: it rises from 0 to a maximum of `1/sqrt(2)` at `x = 1/(2*sqrt(2))`
   and subsequently decays to 0 as `x -> infty`.
2. MOND Transition Function: In contrast, `mu(x) = x / sqrt(1 + x^2)` is strictly monotonically
   increasing from 0 to 1 as `x -> infty`.
3. Conclusion: `C(x)` and `mu(x)` cannot be identified. Furthermore, `theta = 1/sqrt(2)` is a
   **ceiling** for the physical system (`C(x) <= theta` everywhere), rather than a lower bound gate.
   This ceiling is formalized rigorously above in `bloch_coherence_le_theta` and
   `bloch_coherence_eq_theta_iff`.
-/

/-!
### Task C: Status of `fidelity_half_iff_chi_floor`

The placeholder declaration `fidelity_half_iff_chi_floor : True := by sorry` has been retired.

**Formalization Requirements:**
Formalizing the Uhlmann fidelity `F(rho, sigma) = (Tr sqrt(sqrt(rho) sigma sqrt(rho)))^2`
and establishing the equivalence `F >= 1/2 <-> chi >= 1/sqrt(2)` requires operator square roots,
polar decomposition, and spectral theory for positive semi-definite trace-class operators on
finite-dimensional Hilbert spaces. No unproven `: True` placeholders are retained in this library.
-/

#print axioms mu_eq_tanh_arsinh
#print axioms mu_one
#print axioms mu_ge_chiFloor_iff
#print axioms antiDrift_gate
#print axioms gksl_steady_state_exists
#print axioms steady_state_is_fixed_point
#print axioms trace_steady_state
#print axioms bloch_coherence_le_theta
#print axioms bloch_coherence_eq_theta_iff
#print axioms steady_state_coherence_im_eq_bloch

end PillarIV
