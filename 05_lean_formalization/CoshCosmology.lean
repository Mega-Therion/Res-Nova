import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Tactic

namespace ResNova.CoshCosmology

variable {K₂ Z₀ Q₀ Λ Q Z r : ℝ}

noncomputable def K_cosh (Λ K₂ Z₀ Q₀ Q : ℝ) : ℝ :=
  -2 * Λ + 2 * K₂ * Z₀ ^ 2 * (Real.cosh ((Q - Q₀) / Z₀) - 1)

noncomputable def K_Q (K₂ Z₀ Q₀ Q : ℝ) : ℝ := 2 * K₂ * Z₀ * Real.sinh ((Q - Q₀) / Z₀)

noncomputable def K_QQ (K₂ Z₀ Q₀ Q : ℝ) : ℝ := 2 * K₂ * Real.cosh ((Q - Q₀) / Z₀)

noncomputable def cad_sq (r Z : ℝ) : ℝ := r * Real.tanh Z / (1 + r * Z)

theorem cosh_curvature_independent_of_Z0 (K₂ Z₀ Q₀ : ℝ) :
    K_QQ K₂ Z₀ Q₀ Q₀ = 2 * K₂ := by
  unfold K_QQ
  simp

theorem cad_sq_early_saturation (hr : 0 < r) (hZ : 0 ≤ Z) : cad_sq r Z ≤ r := by
  have htanh : Real.tanh Z ≤ 1 := le_of_lt (Real.tanh_lt_one Z)
  have hrZ : 0 ≤ r * Z := mul_nonneg hr.le hZ
  have hden : (1 : ℝ) ≤ 1 + r * Z := by linarith
  have hden0 : (0 : ℝ) < 1 + r * Z := by linarith
  unfold cad_sq
  rw [div_le_iff₀ hden0]
  have h1 : Real.tanh Z ≤ 1 + r * Z := le_trans htanh hden
  have h2 : r * Real.tanh Z ≤ r * (1 + r * Z) := mul_le_mul_of_nonneg_left h1 hr.le
  exact h2

theorem cad_sq_pos (hr : 0 < r) (hZ : 0 < Z) : 0 < cad_sq r Z := by
  have ht : 0 < Real.tanh Z := by
    rw [Real.tanh_eq]
    have h1 : Real.exp (-Z) < Real.exp Z := Real.exp_lt_exp.mpr (by linarith)
    have hnum : 0 < Real.exp Z - Real.exp (-Z) := sub_pos.mpr h1
    have hden : 0 < Real.exp Z + Real.exp (-Z) := add_pos (Real.exp_pos Z) (Real.exp_pos (-Z))
    exact div_pos hnum hden
  have hrZ : 0 ≤ r * Z := mul_nonneg hr.le hZ.le
  have hden0 : (0 : ℝ) < 1 + r * Z := by linarith
  unfold cad_sq
  exact div_pos (mul_pos hr ht) hden0

theorem late_time_equation_of_state (Λ K₂ Z₀ Q₀ : ℝ) :
    K_cosh Λ K₂ Z₀ Q₀ Q₀ = -2 * Λ := by
  unfold K_cosh
  simp

noncomputable def cad_sq_quadratic (Q₀ Q : ℝ) : ℝ := (Q - Q₀) / Q

theorem quadratic_exceeds_threshold {ε : ℝ} (hQ₀ : 0 < Q₀) (hε : 0 < ε) (hε1 : ε < 1) :
    ∃ Q > Q₀, ε < cad_sq_quadratic Q₀ Q := by
  have h1 : (0 : ℝ) < 1 - ε := by linarith
  have hQpos : (0 : ℝ) < 2 * Q₀ / (1 - ε) := by positivity
  refine ⟨2 * Q₀ / (1 - ε), ?_, ?_⟩
  · rw [gt_iff_lt, lt_div_iff₀ h1]
    have : Q₀ * (1 - ε) = Q₀ - Q₀ * ε := by ring
    rw [this]
    have hQε : 0 < Q₀ * ε := mul_pos hQ₀ hε
    linarith
  · unfold cad_sq_quadratic
    rw [sub_div, div_self (ne_of_gt hQpos)]
    have hinv : Q₀ / (2 * Q₀ / (1 - ε)) = (1 - ε) / 2 := by
      have hQ0_ne : Q₀ ≠ 0 := ne_of_gt hQ₀
      have h1_ne : 1 - ε ≠ 0 := ne_of_gt h1
      field_simp
    rw [hinv]
    linarith

theorem quadratic_bounded_by_one (hQ₀ : 0 < Q₀) (hQ : Q₀ ≤ Q) :
    cad_sq_quadratic Q₀ Q < 1 := by
  have hQpos : 0 < Q := lt_of_lt_of_le hQ₀ hQ
  unfold cad_sq_quadratic
  rw [div_lt_one hQpos]
  linarith

end ResNova.CoshCosmology
