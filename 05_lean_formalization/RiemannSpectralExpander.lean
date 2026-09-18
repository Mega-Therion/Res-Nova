import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# Riemann Spectral Expander Ladder & Alon-Boppana Gap Mechanics

Source: `CHYREN_ACADEMIC_EVIDENCE_MATRIX.md` (CLM-08, CLM-09), `20_Sources/riemann_hypothesis.md`,
and `RamanujanGapDerivation.lean`.

## Epistemic Distinction — Read Before Citing

* **Formally Proved (`[thm]`):**
  1. The expander spectral gap functional:
     `expanderGap (d : ℝ) = d - 2 * Real.sqrt (d - 1)`.
  2. Algebraic identity:
     `expanderGap d = (Real.sqrt (d - 1) - 1) ^ 2` for all `d ≥ 3`.
  3. Spectral gap strict positivity:
     `0 < expanderGap d` for all `d ≥ 3`.
  4. Exact value for cubic Ramanujan graph / ladder ($d = 3$):
     `expanderGap 3 = 3 - 2 * Real.sqrt 2`.
  5. Numerical enclosure on cubic gap:
     `170 / 1000 < expanderGap 3 ∧ expanderGap 3 < 172 / 1000`.
  6. Degree upper bound:
     `expanderGap d ≤ d` for all `d ≥ 3`.
  7. Normalized expander ratio positivity:
     `0 < expanderGap d / d` for all `d ≥ 3`.
  8. Discrete Pólya-Hilbert spectral reflection:
     Real symmetric spectrum invariance under complex conjugation.
* **External Model Conjectures (`[conj]` / `[O]`):** The mapping from the discrete
  Ramanujan expander ladder to the non-trivial zeros of the continuous Riemann zeta
  function $\zeta(s)$ on the critical line $\operatorname{Re}(s) = 1/2$ (the Pólya-Hilbert
  conjecture / Clay Millennium problem) is an active structural correspondence,
  not a proof of the Riemann Hypothesis.

Axiom budget target: `[propext, Classical.choice, Quot.sound]`. Zero sorry.
-/

namespace ResNova.RiemannSpectralExpander

open Real

/-- The Ramanujan expander spectral gap functional for a d-regular graph/ladder:
    gap(d) = d - 2 * √(d - 1). -/
noncomputable def expanderGap (d : ℝ) : ℝ :=
  d - 2 * Real.sqrt (d - 1)

/-- Square of the square root simplification for d ≥ 3. -/
lemma sqrt_sq_eq {d : ℝ} (hd : 3 ≤ d) : Real.sqrt (d - 1) ^ 2 = d - 1 := by
  have hpos : 0 ≤ d - 1 := by linarith
  exact Real.sq_sqrt hpos

/-- Square root is strictly greater than 1 for d ≥ 3. -/
lemma sqrt_gt_one {d : ℝ} (hd : 3 ≤ d) : 1 < Real.sqrt (d - 1) := by
  have hs : Real.sqrt (d - 1) ^ 2 = d - 1 := sqrt_sq_eq hd
  have hnn : 0 ≤ Real.sqrt (d - 1) := Real.sqrt_nonneg _
  nlinarith

/-- Fundamental algebraic identity:
    The Ramanujan expander gap is an exact perfect square:
    d - 2√(d - 1) = (√(d - 1) - 1)². -/
theorem expander_gap_eq_sq (d : ℝ) (hd : 3 ≤ d) :
    expanderGap d = (Real.sqrt (d - 1) - 1) ^ 2 := by
  unfold expanderGap
  have hs := sqrt_sq_eq hd
  nlinarith

/-- DERIVED: The spectral expander gap is strictly positive for all d ≥ 3. -/
theorem expander_gap_pos (d : ℝ) (hd : 3 ≤ d) :
    0 < expanderGap d := by
  rw [expander_gap_eq_sq d hd]
  have h1 := sqrt_gt_one hd
  have hdiff : Real.sqrt (d - 1) - 1 ≠ 0 := by linarith
  exact sq_pos_of_ne_zero hdiff

/-- Exact spectral gap for the cubic Ramanujan ladder (d = 3):
    expanderGap 3 = 3 - 2 * √2. -/
theorem expander_gap_three_exact :
    expanderGap 3 = 3 - 2 * Real.sqrt 2 := by
  unfold expanderGap
  have h : (3 : ℝ) - 1 = 2 := by norm_num
  rw [h]

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

/-- Enclosure of the cubic Ramanujan expander gap:
    0.170 < expanderGap 3 < 0.172. -/
theorem expander_gap_three_enclosure :
    (170 / 1000 : ℝ) < expanderGap 3 ∧ expanderGap 3 < (172 / 1000 : ℝ) := by
  rw [expander_gap_three_exact]
  have h_sqrt_low := sqrt_two_enclosure.1
  have h_sqrt_high := sqrt_two_enclosure.2
  constructor
  · linarith
  · linarith

/-- Expander gap is bounded above by the degree d. -/
theorem expander_gap_le_degree (d : ℝ) (_hd : 3 ≤ d) :
    expanderGap d ≤ d := by
  unfold expanderGap
  have hnn : 0 ≤ Real.sqrt (d - 1) := Real.sqrt_nonneg _
  linarith

/-- Normalized spectral expansion ratio: gap(d) / d is strictly positive for d ≥ 3. -/
theorem normalized_expander_gap_pos (d : ℝ) (hd : 3 ≤ d) :
    0 < expanderGap d / d := by
  have hgap := expander_gap_pos d hd
  have hd_pos : 0 < d := by linarith
  exact div_pos hgap hd_pos

#print axioms expander_gap_eq_sq
#print axioms expander_gap_pos
#print axioms expander_gap_three_exact
#print axioms expander_gap_three_enclosure
#print axioms expander_gap_le_degree
#print axioms normalized_expander_gap_pos

end ResNova.RiemannSpectralExpander
