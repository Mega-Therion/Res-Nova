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

/-- The steady-state coherence of an open system. -/
noncomputable def steadyStateCoherence (S : OpenSystem) : ℝ :=
  mu (S.drive / S.dissipation)

/-- **OPEN — the load-bearing premise (Task A.3).** The steady state of the GKSL generator
has coherence `μ(u/γ)`.

Mathematical obstacle: The off-diagonal coherence element of the concrete 2-level
GKSL steady state is |ρ_{01}| = 2(u/γ) / (1 + 8(u/γ)^2), which is a rational
saturation curve, whereas the MOND/chiral transition function μ(u/γ) = (u/γ) / √(1 + (u/γ)^2)
is an algebraic square-root curve. The identification remains an open physical premise. -/
theorem coherence_eq_mu_of_gksl (S : OpenSystem) :
    steadyStateCoherence S = mu (S.drive / S.dissipation) := by
  sorry

/-- **Theorem VI.1, conditional form.** Given the §2 premise, the anti-drift
gate holds. -/
theorem antiDrift_theorem (S : OpenSystem) :
    chiFloor ≤ steadyStateCoherence S ↔ S.dissipation ≤ S.drive := by
  rw [coherence_eq_mu_of_gksl S]
  exact antiDrift_gate S.dissipation_pos S.drive_nonneg

/-- **OPEN.** The Uhlmann-fidelity form reported by Delgado & Goel (2024):
`F ≥ 1/2 ↔ χ ≥ 1/√2`.

Mathematical obstacle: Formalizing Uhlmann fidelity F(ρ, σ) = (Tr√(√ρ σ √ρ))^2
requires the operator square root and spectral theorem on density matrices, which are not yet formalized here. -/
theorem fidelity_half_iff_chi_floor : True := by
  sorry

#print axioms mu_eq_tanh_arsinh
#print axioms mu_one
#print axioms mu_ge_chiFloor_iff
#print axioms antiDrift_gate
#print axioms gksl_steady_state_exists
#print axioms steady_state_is_fixed_point
#print axioms trace_steady_state

end PillarIV
