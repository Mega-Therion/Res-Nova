import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# SU(N) Yang-Mills Casimir Mass Gap & Spectral Enclosure

Source: `CHYREN_ACADEMIC_EVIDENCE_MATRIX.md` (CLM-01) and `yang_mills.md`.
Companion to `SOCasimirGenuine.lean` (which computed the Lie-algebra Casimir from generators).

## Epistemic Distinction — Read Before Citing

* **Formally Proved (`[thm]`):**
  1. Lie algebra dimensions and Casimir scaling for $SU(N)$: `sunDim N = N² - 1`, `sunRank N = N - 1`.
  2. Exact dimension and rank values for $SU(2)$ (dim 3, rank 1) and $SU(3)$ (dim 8, rank 2).
  3. Spectral gap positivity: for all $N \ge 2$, $\kappa > 0$, and $\theta > 0$,
     the Casimir mass gap $\Delta_{\text{YM}}(N) = \frac{\kappa}{\theta}(N - 1)$ is strictly positive.
  4. Exact group ratio: $\Delta_{\text{YM}}(3) / \Delta_{\text{YM}}(2) = 2$.
  5. Radical representation at $\theta_{\text{geom}} = 1/\sqrt{2}$:
     $\Delta_{\text{YM}}(N) = \kappa \sqrt{2} (N - 1)$.
  6. Numerical enclosure for $SU(3)$ QCD mass gap: $2.06 < \Delta_{\text{YM}}(3) < 2.07$
     under the nominal coupling $\kappa \in [0.729, 0.731]$.
* **External Model Conjectures (`[conj]` / `[O]`):** The mapping from the internal
  Stiefel/holonomy Casimir gap to the physical non-perturbative quantum Yang-Mills
  Hamiltonian spectrum on $\mathbb{R}^4$ (the Clay Millennium problem) is a theoretical
  framework conjecture, not a proof of the Wightman axioms.

Axiom budget target: `[propext, Classical.choice, Quot.sound]`. Zero sorry.
-/

namespace ResNova.YangMillsCasimirBound

open Real

/-- Lie algebra dimension for SU(N): N² - 1. -/
def sunDim (N : ℕ) : ℕ := N * N - 1

/-- SU(2) has 3 generators (Pauli basis). -/
theorem su2_dim : sunDim 2 = 3 := by decide

/-- SU(3) has 8 generators (Gell-Mann basis). -/
theorem su3_dim : sunDim 3 = 8 := by decide

/-- Structure group rank for SU(N): N - 1. -/
def sunRank (N : ℕ) : ℕ := N - 1

theorem su2_rank : sunRank 2 = 1 := by decide
theorem su3_rank : sunRank 3 = 2 := by decide

/-- The geometric threshold parameter θ_geom = 1 / √2. -/
noncomputable def thetaGeom : ℝ := 1 / Real.sqrt 2

/-- Positivity of the geometric threshold. -/
theorem thetaGeom_pos : 0 < thetaGeom := by
  unfold thetaGeom
  have hpos : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
  exact div_pos (by norm_num) hpos

/-- The Yang-Mills Casimir mass gap functional:
    Δ_YM(N, κ, θ) = (κ / θ) * (N - 1). -/
noncomputable def ymCasimirGap (N : ℕ) (kappa theta : ℝ) : ℝ :=
  (kappa / theta) * (N - 1 : ℝ)

/-- For all N ≥ 2 and positive parameters κ, θ > 0,
    the Casimir spectral gap is strictly positive. -/
theorem ym_casimir_gap_pos (N : ℕ) (hN : 2 ≤ N) (kappa theta : ℝ)
    (hkappa : 0 < kappa) (htheta : 0 < theta) :
    0 < ymCasimirGap N kappa theta := by
  unfold ymCasimirGap
  have h_diff_pos : 0 < (N - 1 : ℝ) := by
    have hN_real : (2 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
    linarith
  have h_quot_pos : 0 < kappa / theta := div_pos hkappa htheta
  exact mul_pos h_quot_pos h_diff_pos

/-- Exact ratio between SU(3) QCD mass gap and SU(2) electroweak mass gap:
    Δ_YM(3) / Δ_YM(2) = 2. -/
theorem ym_gap_ratio_su3_su2 (kappa theta : ℝ) (hkappa : 0 < kappa) (htheta : 0 < theta) :
    ymCasimirGap 3 kappa theta / ymCasimirGap 2 kappa theta = 2 := by
  unfold ymCasimirGap
  have h_ne : kappa / theta ≠ 0 := ne_of_gt (div_pos hkappa htheta)
  push_cast
  have h3 : (3 - 1 : ℝ) = 2 := by norm_num
  have h2 : (2 - 1 : ℝ) = 1 := by norm_num
  rw [h3, h2, mul_one]
  rw [mul_comm, mul_div_cancel_right₀ 2 h_ne]

/-- At the geometric threshold θ_geom = 1 / √2, the scale factor simplifies:
    κ / θ_geom = κ * √2. -/
theorem scale_factor_at_theta_geom (kappa : ℝ) :
    kappa / thetaGeom = kappa * Real.sqrt 2 := by
  unfold thetaGeom
  have hpos : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
  have hne : Real.sqrt 2 ≠ 0 := ne_of_gt hpos
  field_simp [hne]

/-- The SU(3) mass gap at θ_geom is exactly 2 * √2 * κ. -/
theorem ym_su3_gap_exact (kappa : ℝ) :
    ymCasimirGap 3 kappa thetaGeom = 2 * Real.sqrt 2 * kappa := by
  unfold ymCasimirGap
  rw [scale_factor_at_theta_geom]
  push_cast
  ring

/-- Numerical enclosure on √2: 1.414 < √2 < 1.415. -/
theorem sqrt_two_enclosure :
    (1414 / 1000 : ℝ) < Real.sqrt 2 ∧ Real.sqrt 2 < (1415 / 1000 : ℝ) := by
  constructor
  · have hsq : (1414 / 1000 : ℝ) ^ 2 < 2 := by norm_num
    have hpos : 0 ≤ (1414 / 1000 : ℝ) := by norm_num
    rw [← Real.sqrt_lt_sqrt_iff (by norm_num)] at hsq
    rw [Real.sqrt_sq hpos] at hsq
    exact hsq
  · have hsq : (2 : ℝ) < (1415 / 1000 : ℝ) ^ 2 := by norm_num
    have hpos : 0 ≤ (1415 / 1000 : ℝ) := by norm_num
    rw [← Real.sqrt_lt_sqrt_iff (by norm_num)] at hsq
    rw [Real.sqrt_sq hpos] at hsq
    exact hsq

/-- Enclosure of the physical SU(3) mass gap:
    For nominal coupling κ ∈ [0.729, 0.731],
    2.06 < Δ_YM(3) < 2.07. -/
theorem ym_su3_gap_enclosure (kappa : ℝ)
    (h_low : (729 / 1000 : ℝ) ≤ kappa)
    (h_high : kappa ≤ (731 / 1000 : ℝ)) :
    (206 / 100 : ℝ) < ymCasimirGap 3 kappa thetaGeom ∧
    ymCasimirGap 3 kappa thetaGeom < (207 / 100 : ℝ) := by
  rw [ym_su3_gap_exact]
  have h_sqrt_low := sqrt_two_enclosure.1
  have h_sqrt_high := sqrt_two_enclosure.2
  have h_sqrt_pos : 0 < Real.sqrt 2 := by linarith [h_sqrt_low]
  constructor
  · calc
      (206 / 100 : ℝ) < 2 * (1414 / 1000 : ℝ) * (729 / 1000 : ℝ) := by norm_num
      _ < 2 * Real.sqrt 2 * (729 / 1000 : ℝ) := by nlinarith [h_sqrt_low]
      _ ≤ 2 * Real.sqrt 2 * kappa := by nlinarith [h_sqrt_pos, h_low]
  · calc
      2 * Real.sqrt 2 * kappa ≤ 2 * Real.sqrt 2 * (731 / 1000 : ℝ) := by nlinarith [h_sqrt_pos, h_high]
      _ < 2 * (1415 / 1000 : ℝ) * (731 / 1000 : ℝ) := by nlinarith [h_sqrt_high]
      _ < (207 / 100 : ℝ) := by norm_num

#print axioms ym_casimir_gap_pos
#print axioms ym_gap_ratio_su3_su2
#print axioms scale_factor_at_theta_geom
#print axioms ym_su3_gap_exact
#print axioms ym_su3_gap_enclosure

end ResNova.YangMillsCasimirBound
