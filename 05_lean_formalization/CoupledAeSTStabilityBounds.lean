import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-!
# Coupled 2×2 AeST FLRW Stability Matrix, Power-Law Bounds, and Running-λ_s(Q) Escape Criterion

Adjacent Lean 4 formalization companion to `audits/2026-11-20/coupled_2x2_flrw_stability.py`
and `audits/2026-11-20/running_lambda_and_cosh_stability.py`. Not cited by the main
manuscript (scoped in `ADJACENT_MODULES.txt`). All theorems compile with zero unfinished
proof terms and standard axioms only.

## Scope & Epistemic Boundary

* **Checked in Lean 4 (`[P]`):**
  1. Exact determinant factorization of the coupled 2×2 Fourier Hermitian matrix
     `coupled2x2Matrix : Matrix (Fin 2) (Fin 2) ℂ` for `(φ, A_x)`:
     `det M / (K2_eff K_B / 2) = ω⁴ - (M_gap² + c_{s,UV}² k²) ω² + M_gap² c_{s,IR}² k²`,
     and reproduction of the Skordis–Złośnik (2022) limit at `K1 = 0, K2_eff = 4 𝒦₂`.
  2. All-`k` instability whenever `M_gap² < 0 ∧ c_{s,IR}² > 0 ∧ k > 0`, and positive real roots
     whenever `M_gap² > 0 ∧ 0 < c_{s,IR}² ≤ c_{s,UV}² ∧ k > 0`.
  3. Exact `Q̄`-independent power-law lower bound `2 ≤ K_B ((p - 1)(1 + λ_s) - λ_s)` for
     `U(Q) = c Q^p` (`p > 1`), together with witness bounds for `p = 3` (`> 0.10`) and
     `p = 4` (`> 0.008` and `< 0.10`) at `λ_s = 11.2787`.
  4. Necessary and sufficient existence theorem for covariant running `λ_s(Q)`:
     `(∃ λ_s, M_gap² ≥ 0 ∧ c_{s,UV}² ≤ 1) ↔ K2_eff - K1/Q̄ ≥ 2(2 - K_B)²/K_B`, yielding
     unconditional exclusion `[X]` of stiff `p = 2`, global Cosh viability when
     `4 𝒦₂(1 - r) ≥ 2(2 - K_B)²/K_B`, and the exact AM–GM dip lower bound
     `864 𝒦₂² c Q₀² ≤ (4 𝒦₂ Q₀ / Q̄ + 8 c Q̄²)³` for `2 𝒦₂(Q - Q₀)² + c Q⁴`.
* **Derived in SymPy/Python (`[D]`):** extraction of `L^(2)` from the curved 4D metric +
  unit-aether action, gauge invariance across 4×4 Newtonian & unitary ADM constraints, and
  numerical FLRW background/horizon-crossing integrations.
-/

noncomputable section

namespace ResNova.CoupledAeSTStabilityBounds

open Real

/-! ## 1. Coupled 2×2 Dispersion Definitions & Matrix Factorization -/

/-- Exact aether mass gap squared `M_gap² = Q̄ (2 (2 - K_B)(1 + λ_s) Q̄ - K1) / (2 K_B)`. -/
def MgapSq (KB lam K1 Qbar : ℝ) : ℝ :=
  Qbar * (2 * (2 - KB) * (1 + lam) * Qbar - K1) / (2 * KB)

/-- Exact UV propagation speed squared `c_{s,UV}² = 4 (2 - K_B)(1 + K_B λ_s / 2) / (K2_eff K_B)`. -/
def csUVSq (KB lam K2e : ℝ) : ℝ :=
  4 * (2 - KB) * (1 + KB * lam / 2) / (K2e * KB)

/-- Exact IR adiabatic sound speed squared `c_{s,IR}² = K1 / (K2_eff Q̄)`. -/
def csIRSq (K1 K2e Qbar : ℝ) : ℝ :=
  K1 / (K2e * Qbar)

/-- Coupled 2×2 Hermitian Fourier matrix for fixed-metric `(φ, A_x)` perturbations
extracted from the quadratic AeST Lagrangian around general `K(Q)`. -/
def coupled2x2Matrix (KB lam K1 K2e Qbar w k : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![((K2e * w ^ 2 / 2 - (2 - KB) * (1 + lam) * k ^ 2 : ℝ) : ℂ),
     ((-(2 - KB) * k * w : ℝ) : ℂ) +
       Complex.I * ((k * ((2 - KB) * (1 + lam) * Qbar - K1 / 2) : ℝ) : ℂ);
     ((-(2 - KB) * k * w : ℝ) : ℂ) -
       Complex.I * ((k * ((2 - KB) * (1 + lam) * Qbar - K1 / 2) : ℝ) : ℂ),
     ((KB * w ^ 2 + K1 * Qbar / 2 - (2 - KB) * (1 + lam) * Qbar ^ 2 : ℝ) : ℂ)]

/-- **Exact Coupled 2×2 Dispersion Factorization:** dividing the determinant of
`coupled2x2Matrix` by `K2_eff K_B / 2` yields identically
`ω⁴ - (M_gap² + c_{s,UV}² k²) ω² + M_gap² c_{s,IR}² k²`. -/
theorem coupled_2x2_det_factorization {KB lam K1 K2e Qbar w k : ℝ}
    (hKB : KB ≠ 0) (hK2 : K2e ≠ 0) (hQ : Qbar ≠ 0) :
    (coupled2x2Matrix KB lam K1 K2e Qbar w k).det / ((K2e * KB / 2 : ℝ) : ℂ) =
      ((w ^ 4 - (MgapSq KB lam K1 Qbar + csUVSq KB lam K2e * k ^ 2) * w ^ 2 +
        MgapSq KB lam K1 Qbar * csIRSq K1 K2e Qbar * k ^ 2 : ℝ) : ℂ) := by
  have hden' : K2e * KB / 2 ≠ 0 := div_ne_zero (mul_ne_zero hK2 hKB) two_ne_zero
  have hden : ((K2e * KB / 2 : ℝ) : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr hden'
  rw [div_eq_iff hden]
  unfold coupled2x2Matrix
  rw [Matrix.det_fin_two]
  simp only [Matrix.of_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
  have hreal :
      (K2e * w ^ 2 / 2 - (2 - KB) * (1 + lam) * k ^ 2) *
          (KB * w ^ 2 + K1 * Qbar / 2 - (2 - KB) * (1 + lam) * Qbar ^ 2) -
        ((-(2 - KB) * k * w) ^ 2 + (k * ((2 - KB) * (1 + lam) * Qbar - K1 / 2)) ^ 2) =
      (w ^ 4 - (MgapSq KB lam K1 Qbar + csUVSq KB lam K2e * k ^ 2) * w ^ 2 +
        MgapSq KB lam K1 Qbar * csIRSq K1 K2e Qbar * k ^ 2) * (K2e * KB / 2) := by
    unfold MgapSq csUVSq csIRSq
    field_simp [hKB, hK2, hQ]
    ring
  have hcomplex :
      ((K2e * w ^ 2 / 2 - (2 - KB) * (1 + lam) * k ^ 2 : ℝ) : ℂ) *
          ((KB * w ^ 2 + K1 * Qbar / 2 - (2 - KB) * (1 + lam) * Qbar ^ 2 : ℝ) : ℂ) -
        ((( -(2 - KB) * k * w : ℝ) : ℂ) +
            Complex.I * ((k * ((2 - KB) * (1 + lam) * Qbar - K1 / 2) : ℝ) : ℂ)) *
          ((( -(2 - KB) * k * w : ℝ) : ℂ) -
            Complex.I * ((k * ((2 - KB) * (1 + lam) * Qbar - K1 / 2) : ℝ) : ℂ)) =
      (((K2e * w ^ 2 / 2 - (2 - KB) * (1 + lam) * k ^ 2) *
          (KB * w ^ 2 + K1 * Qbar / 2 - (2 - KB) * (1 + lam) * Qbar ^ 2) -
        ((-(2 - KB) * k * w) ^ 2 + (k * ((2 - KB) * (1 + lam) * Qbar - K1 / 2)) ^ 2) : ℝ) : ℂ) := by
    push_cast
    ring_nf
    rw [Complex.I_sq]
    ring
  rw [hcomplex, hreal]
  push_cast
  ring

/-- **SZ22 Calibration Limit (`K1 = 0, K2_eff = 4 𝒦₂`):** recovers exact SZ22
`c_s² = (2 - K_B)(1 + K_B λ_s / 2) / (𝒦₂ K_B)`, `c_{s,IR}² = 0`, and
`M_gap² = (2 - K_B)(1 + λ_s) Q̄² / K_B`. -/
theorem sz22_limit_calibration {KB lam K2 Qbar : ℝ} (hKB : KB ≠ 0) (hK2 : K2 ≠ 0) (hQ : Qbar ≠ 0) :
    csUVSq KB lam (4 * K2) = (2 - KB) * (1 + KB * lam / 2) / (K2 * KB) ∧
    csIRSq 0 (4 * K2) Qbar = 0 ∧
    MgapSq KB lam 0 Qbar = (2 - KB) * (1 + lam) * Qbar ^ 2 / KB := by
  unfold csUVSq csIRSq MgapSq
  refine ⟨?_, ?_, ?_⟩
  · field_simp [hKB, hK2]
  · simp
  · field_simp [hKB, hQ]
    ring

/-! ## 2. All-`k` Instability When `M_gap² < 0` vs. Healthy Dispersion Roots -/

/-- Dispersion quadratic in `X = ω²`. -/
def dispPoly (M2 cUV cIR k X : ℝ) : ℝ :=
  X ^ 2 - (M2 + cUV * k ^ 2) * X + M2 * cIR * k ^ 2

/-- **All-`k` Longitudinal Instability (`M_gap² < 0`, `c_{s,IR}² > 0`):** for every wavenumber
`k > 0`, the discriminant is strictly positive and there exists a strictly negative root
`X = ω² < 0` (exponential instability for all `k > 0`). -/
theorem tachyonic_gap_all_k_instability {M2 cUV cIR k : ℝ}
    (hM : M2 < 0) (hc : 0 < cIR) (hk : 0 < k) :
    let Δ := (M2 + cUV * k ^ 2) ^ 2 - 4 * M2 * cIR * k ^ 2
    0 < Δ ∧ ∃ X : ℝ, X < 0 ∧ dispPoly M2 cUV cIR k X = 0 := by
  set b := M2 + cUV * k ^ 2
  set Δ := b ^ 2 - 4 * M2 * cIR * k ^ 2
  have hk2 : 0 < k ^ 2 := sq_pos_of_pos hk
  have hprod_neg : M2 * cIR * k ^ 2 < 0 :=
    mul_neg_of_neg_of_pos (mul_neg_of_neg_of_pos hM hc) hk2
  have hΔ_gt : b ^ 2 < Δ := by
    dsimp [Δ]
    linarith
  have hΔ_pos : 0 < Δ := lt_of_le_of_lt (sq_nonneg b) hΔ_gt
  refine ⟨hΔ_pos, (b - Real.sqrt Δ) / 2, ?_, ?_⟩
  · have hlt : b < Real.sqrt Δ := by
      have hsq : b ^ 2 < (Real.sqrt Δ) ^ 2 := by
        rw [Real.sq_sqrt hΔ_pos.le]
        exact hΔ_gt
      have hspos : 0 < Real.sqrt Δ := Real.sqrt_pos.mpr hΔ_pos
      nlinarith
    linarith
  · unfold dispPoly
    have hsq : Real.sqrt Δ ^ 2 = Δ := Real.sq_sqrt hΔ_pos.le
    dsimp [Δ, b] at hsq ⊢
    nlinarith [hsq]

/-- **Healthy Positive-Root Regime (`M_gap² > 0`, `0 < c_{s,IR}² ≤ c_{s,UV}²`):** both
roots `ω±²` are real (`Δ ≥ 0`) and strictly positive for every `k > 0`. -/
theorem stable_window_real_pos_roots {M2 cUV cIR k : ℝ}
    (hM : 0 < M2) (hc : 0 < cIR) (hle : cIR ≤ cUV) (hk : 0 < k) :
    let Δ := (M2 + cUV * k ^ 2) ^ 2 - 4 * M2 * cIR * k ^ 2
    0 ≤ Δ ∧
    0 < (M2 + cUV * k ^ 2 - Real.sqrt Δ) / 2 ∧
    dispPoly M2 cUV cIR k ((M2 + cUV * k ^ 2 - Real.sqrt Δ) / 2) = 0 := by
  set b := M2 + cUV * k ^ 2
  set Δ := b ^ 2 - 4 * M2 * cIR * k ^ 2
  have hk2 : 0 < k ^ 2 := sq_pos_of_pos hk
  have hΔ_nonneg : 0 ≤ Δ := by
    dsimp [Δ, b]
    have h1 : 4 * M2 * cIR * k ^ 2 ≤ 4 * M2 * cUV * k ^ 2 := by nlinarith [mul_pos hM hk2]
    have h2 : (M2 - cUV * k ^ 2) ^ 2 = (M2 + cUV * k ^ 2) ^ 2 - 4 * M2 * cUV * k ^ 2 := by ring
    nlinarith [sq_nonneg (M2 - cUV * k ^ 2)]
  have hb_pos : 0 < b := by
    dsimp [b]
    nlinarith
  have hprod_pos : 0 < 4 * M2 * cIR * k ^ 2 := by positivity
  have hΔ_lt : Δ < b ^ 2 := by
    dsimp [Δ]
    linarith
  refine ⟨hΔ_nonneg, ?_, ?_⟩
  · have hlt : Real.sqrt Δ < b := by
      have hsq : (Real.sqrt Δ) ^ 2 < b ^ 2 := by
        rw [Real.sq_sqrt hΔ_nonneg]
        exact hΔ_lt
      have hs_nn : 0 ≤ Real.sqrt Δ := Real.sqrt_nonneg Δ
      nlinarith
    linarith
  · unfold dispPoly
    have hsq : Real.sqrt Δ ^ 2 = Δ := Real.sq_sqrt hΔ_nonneg
    dsimp [Δ, b] at hsq ⊢
    nlinarith [hsq]

/-! ## 3. Exact `Q̄`-Independent Power-Law Bound & Witness Bounds -/

/-- Exact `Q̄`-independent power-law minimum `K_{B,min}(p, λ_s) = 2 / ((p - 1)(1 + λ_s) - λ_s)`. -/
def KBmin (p lam : ℝ) : ℝ := 2 / ((p - 1) * (1 + lam) - lam)

/-- For pure power law `U(Q) = c Q^p` (`K1 = p A`, `K2_eff = p (p - 1) A / Q̄`), `c_{s,IR}² = 1 / (p - 1)`. -/
theorem powerlaw_csIRSq {p A Qbar : ℝ} (hp : p ≠ 0) (hp1 : p - 1 ≠ 0) (hA : A ≠ 0) (hQ : Qbar ≠ 0) :
    csIRSq (p * A) (p * (p - 1) * A / Qbar) Qbar = 1 / (p - 1) := by
  unfold csIRSq
  field_simp [hp, hp1, hA, hQ]

/-- **Power-Law `K_B` Lower Bound:** For `U(Q) = c Q^p` (`p > 1`), requiring `M_gap² ≥ 0` and
`c_{s,UV}² ≤ 1` forces `2 ≤ K_B ((p - 1)(1 + λ_s) - λ_s)` identically (independent of `Q̄` and `c`),
and `KBmin p λ_s ≤ K_B` whenever `(p - 1)(1 + λ_s) - λ_s > 0`. -/
theorem powerlaw_KB_lower_bound {KB p A Qbar lam : ℝ}
    (hKB0 : 0 < KB) (hKB2 : KB < 2) (hp : 1 < p) (hA : 0 < A) (hQ : 0 < Qbar)
    (hgap : 0 ≤ MgapSq KB lam (p * A) Qbar)
    (huv : csUVSq KB lam (p * (p - 1) * A / Qbar) ≤ 1) :
    2 ≤ KB * ((p - 1) * (1 + lam) - lam) ∧
    (0 < (p - 1) * (1 + lam) - lam → KBmin p lam ≤ KB) := by
  have h2mKB : 0 < 2 - KB := by linarith
  have hp1 : 0 < p - 1 := by linarith
  have hK2pos : 0 < p * (p - 1) * A / Qbar := by positivity
  unfold MgapSq at hgap
  rw [div_nonneg_iff] at hgap
  have hgap_num : p * A ≤ 2 * (2 - KB) * (1 + lam) * Qbar := by
    rcases hgap with ⟨hnum, _⟩ | ⟨_, hden⟩
    · have h2 : 0 ≤ 2 * (2 - KB) * (1 + lam) * Qbar - p * A := by
        nlinarith [mul_nonneg_iff.mp hnum]
      linarith
    · exfalso; linarith
  unfold csUVSq at huv
  have hden_uv : 0 < (p * (p - 1) * A / Qbar) * KB := mul_pos hK2pos hKB0
  rw [div_le_one hden_uv] at huv
  have huv_mul : 4 * (2 - KB) * (1 + KB * lam / 2) * Qbar ≤ KB * p * (p - 1) * A := by
    have hq_ne : Qbar ≠ 0 := hQ.ne'
    have h1 : 4 * (2 - KB) * (1 + KB * lam / 2) ≤ (p * (p - 1) * A / Qbar) * KB := huv
    have h2 : 4 * (2 - KB) * (1 + KB * lam / 2) * Qbar ≤ ((p * (p - 1) * A / Qbar) * KB) * Qbar :=
      mul_le_mul_of_nonneg_right h1 hQ.le
    calc
      4 * (2 - KB) * (1 + KB * lam / 2) * Qbar ≤ ((p * (p - 1) * A / Qbar) * KB) * Qbar := h2
      _ = KB * p * (p - 1) * A := by field_simp [hq_ne]
  have hchain :
      4 * (2 - KB) * (1 + KB * lam / 2) * Qbar ≤
        2 * (2 - KB) * (1 + lam) * (p - 1) * KB * Qbar := by
    have hmul : KB * (p - 1) * (p * A) ≤ KB * (p - 1) * (2 * (2 - KB) * (1 + lam) * Qbar) :=
      mul_le_mul_of_nonneg_left hgap_num (mul_pos hKB0 hp1).le
    nlinarith
  have hcomb : 2 + KB * lam ≤ KB * (p - 1) * (1 + lam) := by
    have h2Q : 0 < 2 * (2 - KB) * Qbar := by positivity
    nlinarith
  have hmain : 2 ≤ KB * ((p - 1) * (1 + lam) - lam) := by linarith
  refine ⟨hmain, fun hpos => ?_⟩
  unfold KBmin
  exact (div_le_iff₀ hpos).mpr hmain

/-- Quantitative witness inequalities at `λ_s = 11.2787`:
* Pure `Q³` (`p = 3`) requires `K_B > 0.10` (violates PR #226 witness `0.008` and BBN `K_B ≤ 0.10`).
* Pure `Q⁴` (`p = 4`) fails at PR #226 witness (`> 0.008`) while leaving `[K_{B,min}, 0.10]` open. -/
theorem witness_KBmin_bounds :
    let lam : ℝ := 112787 / 10000
    (1 / 10 : ℝ) < KBmin 3 lam ∧
    (8 / 1000 : ℝ) < KBmin 4 lam ∧
    KBmin 4 lam < (1 / 10 : ℝ) := by
  unfold KBmin
  norm_num

/-! ## 4. Universal Running-`λ_s(Q)` Existence Theorem & Sector Verdicts -/

/-- Compatibility LHS `K2_eff - K1 / Q̄ = K2_eff (1 - c_{s,IR}²)`. -/
def compatLHS (K1 K2e Qbar : ℝ) : ℝ := K2e - K1 / Qbar

/-- Compatibility RHS `2 (2 - K_B)² / K_B`. -/
def compatRHS (KB : ℝ) : ℝ := 2 * (2 - KB) ^ 2 / KB

/-- **Universal Running-`λ_s(Q)` Existence Theorem:** For `0 < K_B < 2`, `K2_eff > 0`, `Q̄ > 0`,
there exists a scalar `λ_s ∈ ℝ` satisfying BOTH `M_gap² ≥ 0` and `c_{s,UV}² ≤ 1` if and only if
`K2_eff - K1 / Q̄ ≥ 2 (2 - K_B)² / K_B`. -/
theorem running_lambda_exists_iff {KB K1 K2e Qbar : ℝ}
    (hKB0 : 0 < KB) (hKB2 : KB < 2) (hK2 : 0 < K2e) (hQ : 0 < Qbar) :
    (∃ lam : ℝ, 0 ≤ MgapSq KB lam K1 Qbar ∧ csUVSq KB lam K2e ≤ 1) ↔
      compatRHS KB ≤ compatLHS K1 K2e Qbar := by
  have h2mKB : 0 < 2 - KB := by linarith
  constructor
  · rintro ⟨lam, hgap, huv⟩
    unfold MgapSq at hgap
    rw [div_nonneg_iff] at hgap
    have h1 : K1 / Qbar ≤ 2 * (2 - KB) * (1 + lam) := by
      have hnum : K1 ≤ 2 * (2 - KB) * (1 + lam) * Qbar := by
        rcases hgap with ⟨ha, _⟩ | ⟨_, hb⟩
        · have : 0 ≤ 2 * (2 - KB) * (1 + lam) * Qbar - K1 := by
            nlinarith [mul_nonneg_iff.mp ha]
          linarith
        · exfalso; linarith
      exact (div_le_iff₀ hQ).mpr hnum
    unfold csUVSq at huv
    rw [div_le_iff₀ (mul_pos hK2 hKB0)] at huv
    have h2 : 4 * (2 - KB) / KB + 2 * (2 - KB) * lam ≤ K2e := by
      have hdiv : (4 * (2 - KB) * (1 + KB * lam / 2)) / KB ≤ K2e := (div_le_iff₀ hKB0).mpr (by nlinarith)
      have hsim : (4 * (2 - KB) * (1 + KB * lam / 2)) / KB =
          4 * (2 - KB) / KB + 2 * (2 - KB) * lam := by
        field_simp [hKB0.ne']
        ring
      linarith
    unfold compatRHS compatLHS
    have hid : 2 * (2 - KB) ^ 2 / KB = 4 * (2 - KB) / KB - 2 * (2 - KB) := by
      field_simp [hKB0.ne']
      ring
    linarith
  · intro hcompat
    refine ⟨K1 / (2 * (2 - KB) * Qbar) - 1, ?_, ?_⟩
    · unfold MgapSq
      have hid : 2 * (2 - KB) * (1 + (K1 / (2 * (2 - KB) * Qbar) - 1)) * Qbar - K1 = 0 := by
        field_simp [h2mKB.ne', hQ.ne']
        ring
      rw [hid]
      simp
    · unfold csUVSq
      rw [div_le_iff₀ (mul_pos hK2 hKB0)]
      unfold compatRHS compatLHS at hcompat
      have hmul : 2 * (2 - KB) ^ 2 ≤ (K2e - K1 / Qbar) * KB := (div_le_iff₀ hKB0).mp hcompat
      have hrel :
          4 * (2 - KB) * (1 + KB * (K1 / (2 * (2 - KB) * Qbar) - 1) / 2) =
            2 * (2 - KB) ^ 2 + (K1 / Qbar) * KB := by
        field_simp [h2mKB.ne', hQ.ne']
        ring
      nlinarith

/-- **Unconditional Stiff `p = 2` Exclusion (`[X]`):** Whenever `K1 = K2_eff Q̄` (`c_{s,IR}² = 1`),
`K2_eff - K1 / Q̄ = 0`, so NO choice of running `λ_s(Q)` can keep `M_gap² ≥ 0` and `c_{s,UV}² ≤ 1`. -/
theorem stiff_p2_running_lambda_impossible {KB K1 K2e Qbar : ℝ}
    (hKB0 : 0 < KB) (hKB2 : KB < 2) (hK2 : 0 < K2e) (hQ : 0 < Qbar) (hp2 : K1 = K2e * Qbar) :
    ¬ ∃ lam : ℝ, 0 ≤ MgapSq KB lam K1 Qbar ∧ csUVSq KB lam K2e ≤ 1 := by
  rw [running_lambda_exists_iff hKB0 hKB2 hK2 hQ]
  unfold compatLHS compatRHS
  rw [hp2]
  have hzero : K2e - K2e * Qbar / Qbar = 0 := by
    field_simp [hQ.ne']
    ring
  rw [hzero]
  have h2mKB : 0 < 2 - KB := by linarith
  have hpos : 0 < 2 * (2 - KB) ^ 2 / KB := by positivity
  linarith

/-- Elementary hyperbolic lower bound `1 - r ≤ cosh Z - r sinh Z / (1 + r Z)` for `0 < r < 1`
and `Z ≥ 0` (since `sinh Z ≤ cosh Z` and `1 ≤ 1 + r Z`). -/
theorem cosh_sub_sinh_lower {r Z : ℝ} (hr0 : 0 < r) (hr1 : r < 1) (hZ : 0 ≤ Z) :
    1 - r ≤ Real.cosh Z - r * Real.sinh Z / (1 + r * Z) := by
  have h1c : 1 ≤ Real.cosh Z := by
    have hsq := Real.cosh_sq_sub_sinh_sq Z
    nlinarith [Real.cosh_pos Z, sq_nonneg (Real.sinh Z)]
  have hsh_nonneg : 0 ≤ Real.sinh Z := by
    rw [Real.sinh_eq]
    have h1 : 1 ≤ Real.exp Z := Real.one_le_exp hZ
    have h2 : Real.exp (-Z) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
    linarith
  have hden : 1 ≤ 1 + r * Z := by nlinarith [mul_nonneg hr0.le hZ]
  have hsh_le_ch : Real.sinh Z ≤ Real.cosh Z := by
    rw [Real.sinh_eq, Real.cosh_eq]
    have hexp : 0 < Real.exp (-Z) := Real.exp_pos (-Z)
    linarith
  have hratio : Real.sinh Z / (1 + r * Z) ≤ Real.cosh Z := by
    calc
      Real.sinh Z / (1 + r * Z) ≤ Real.sinh Z / 1 := by
        exact div_le_div_of_nonneg_left hsh_nonneg (by positivity) hden
      _ = Real.sinh Z := div_one _
      _ ≤ Real.cosh Z := hsh_le_ch
  have hmul : r * (Real.sinh Z / (1 + r * Z)) ≤ r * Real.cosh Z :=
    mul_le_mul_of_nonneg_left hratio hr0.le
  have h1mr : 0 < 1 - r := by linarith
  have hlow_ch : 1 - r ≤ (1 - r) * Real.cosh Z := by nlinarith
  have hmul_div : r * Real.sinh Z / (1 + r * Z) = r * (Real.sinh Z / (1 + r * Z)) := by ring
  linarith

/-- **Global Cosh Running-`λ_s(Q)` Viability (`[P]`/`[D]`):** for `𝒦_cosh` with `0 < r < 1`
and `Z ≥ 0`, whenever `2(2 - K_B)² / K_B ≤ 4 𝒦₂ (1 - r)`, the compatibility condition holds
at EVERY `Z ≥ 0`, so `λ_s(Q)` exists with `M_gap² ≥ 0` and `c_{s,UV}² ≤ 1` globally. -/
theorem cosh_running_lambda_global_open {KB K2 r Q0 Z : ℝ}
    (hKB0 : 0 < KB) (hKB2 : KB < 2) (hK2 : 0 < K2) (hQ0 : 0 < Q0)
    (hr0 : 0 < r) (hr1 : r < 1) (hZ : 0 ≤ Z)
    (hfloor : compatRHS KB ≤ 4 * K2 * (1 - r)) :
    let Qbar := Q0 * (1 + r * Z)
    let K1 := 4 * K2 * r * Q0 * Real.sinh Z
    let K2e := 4 * K2 * Real.cosh Z
    ∃ lam : ℝ, 0 ≤ MgapSq KB lam K1 Qbar ∧ csUVSq KB lam K2e ≤ 1 := by
  have hQpos : 0 < Q0 * (1 + r * Z) := mul_pos hQ0 (by nlinarith [mul_nonneg hr0.le hZ])
  have hK2epos : 0 < 4 * K2 * Real.cosh Z := mul_pos (by positivity) (Real.cosh_pos Z)
  rw [running_lambda_exists_iff hKB0 hKB2 hK2epos hQpos]
  have hid :
      compatLHS (4 * K2 * r * Q0 * Real.sinh Z) (4 * K2 * Real.cosh Z) (Q0 * (1 + r * Z)) =
        4 * K2 * (Real.cosh Z - r * Real.sinh Z / (1 + r * Z)) := by
    unfold compatLHS
    have hden_ne : 1 + r * Z ≠ 0 := by nlinarith [mul_nonneg hr0.le hZ]
    field_simp [hQ0.ne', hden_ne]
  rw [hid]
  have hlow := cosh_sub_sinh_lower hr0 hr1 hZ
  have hmul : 4 * K2 * (1 - r) ≤ 4 * K2 * (Real.cosh Z - r * Real.sinh Z / (1 + r * Z)) :=
    mul_le_mul_of_nonneg_left hlow (by positivity)
  exact le_trans hfloor hmul

/-- **Combined Dust + `Q⁴` AM–GM Lower Bound (`2 𝒦₂(Q - Q₀)² + c Q⁴`):** the compatibility
quantity `K2_eff - K1/Q̄ = 4 𝒦₂ Q₀ / Q̄ + 8 c Q̄²` obeys `(4 𝒦₂ Q₀ / Q̄ + 8 c Q̄²)³ ≥ 864 𝒦₂² c Q₀²`
for every `Q̄ > 0`. -/
theorem combined_q2_q4_amgm_lower_bound {K2 c Q0 Qbar : ℝ}
    (hK2 : 0 ≤ K2) (hc : 0 ≤ c) (hQ0 : 0 ≤ Q0) (hQ : 0 < Qbar) :
    864 * K2 ^ 2 * c * Q0 ^ 2 ≤ (4 * K2 * Q0 / Qbar + 8 * c * Qbar ^ 2) ^ 3 := by
  set x : ℝ := 2 * K2 * Q0 / Qbar
  set y : ℝ := 8 * c * Qbar ^ 2
  have hx : 0 ≤ x := by positivity
  have hy : 0 ≤ y := by positivity
  have hsum : 4 * K2 * Q0 / Qbar + 8 * c * Qbar ^ 2 = 2 * x + y := by
    dsimp [x, y]
    ring
  have hcube : 27 * x ^ 2 * y ≤ (2 * x + y) ^ 3 := by
    have hid : (2 * x + y) ^ 3 - 27 * x ^ 2 * y = (x - y) ^ 2 * (8 * x + y) := by ring
    have hnn : 0 ≤ (x - y) ^ 2 * (8 * x + y) := mul_nonneg (sq_nonneg (x - y)) (by linarith)
    linarith
  have hprod : 27 * x ^ 2 * y = 864 * K2 ^ 2 * c * Q0 ^ 2 := by
    dsimp [x, y]
    field_simp [hQ.ne']
    ring
  rw [hsum, ← hprod]
  exact hcube

/-! ## Axiom Footprints (every public theorem printed) -/

#print axioms coupled_2x2_det_factorization
#print axioms sz22_limit_calibration
#print axioms tachyonic_gap_all_k_instability
#print axioms stable_window_real_pos_roots
#print axioms powerlaw_csIRSq
#print axioms powerlaw_KB_lower_bound
#print axioms witness_KBmin_bounds
#print axioms running_lambda_exists_iff
#print axioms stiff_p2_running_lambda_impossible
#print axioms cosh_sub_sinh_lower
#print axioms cosh_running_lambda_global_open
#print axioms combined_q2_q4_amgm_lower_bound

end ResNova.CoupledAeSTStabilityBounds
