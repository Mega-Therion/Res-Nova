/-
  Res-Nova — RamanujanGapDerivation.lean

  Closes the `h_gap` assumption of `YettParadigm.RamanujanYettSpectrum`.

  There, `κ² ≤ λ₁ − λ₀` is a STRUCTURE FIELD: handed in, and returned verbatim by
  `ramanujan_yett_gap_bound := sys.h_gap`. Substitutability test (2026-09-04):
  the identical proof closes with the physics replaced by nonsense, so it carries
  no content.

  Here the gap is DERIVED. The only hypotheses are the defining properties of a
  d-regular Ramanujan graph — a class with explicit constructions (Lubotzky–
  Phillips–Sarnak, Margulis) — and a concrete witness is exhibited at the end, so
  the statement is not vacuously true.
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

namespace ResNova.RamanujanGap

/-- A `d`-regular Ramanujan spectrum. `λ₀ = d` is the Perron eigenvalue; `lambda1`
is the largest non-trivial eigenvalue, bounded by the Alon–Boppana-tight
Ramanujan condition `|λ| ≤ 2√(d−1)`. Nothing about the gap is assumed. -/
structure RamanujanSpectrum where
  d       : ℝ
  lambda1 : ℝ
  h_deg   : 3 ≤ d
  h_ram   : |lambda1| ≤ 2 * Real.sqrt (d - 1)

namespace RamanujanSpectrum

variable (S : RamanujanSpectrum)

/-- The spectral gap `λ₀ − λ₁ = d − λ₁`. -/
noncomputable def gap : ℝ := S.d - S.lambda1

private lemma sqrt_sq_eq : Real.sqrt (S.d - 1) ^ 2 = S.d - 1 :=
  Real.sq_sqrt (by have := S.h_deg; linarith)

private lemma sqrt_gt_one : 1 < Real.sqrt (S.d - 1) := by
  have hs : Real.sqrt (S.d - 1) ^ 2 = S.d - 1 := S.sqrt_sq_eq
  have hnn : 0 ≤ Real.sqrt (S.d - 1) := Real.sqrt_nonneg _
  have hd := S.h_deg
  nlinarith [hs, hnn, hd]

/-- **DERIVED.** The Ramanujan bound forces `2√(d−1) < d`. The crux is the perfect
square `(√(d−1) − 1)² > 0`. -/
theorem ramanujan_bound_lt_degree : 2 * Real.sqrt (S.d - 1) < S.d := by
  have hs := S.sqrt_sq_eq
  have h1 := S.sqrt_gt_one
  nlinarith [hs, h1]

/-- **DERIVED.** The spectral gap is bounded below by `d − 2√(d−1)`. -/
theorem gap_ge : S.d - 2 * Real.sqrt (S.d - 1) ≤ S.gap := by
  have h := (abs_le.mp S.h_ram).2
  unfold gap; linarith

/-- **DERIVED, not assumed.** The spectral gap is strictly positive. -/
theorem gap_pos : 0 < S.gap := by
  have h1 := S.ramanujan_bound_lt_degree
  have h2 := S.gap_ge
  linarith

/-- **DERIVED, not assumed.** This is the statement `YettParadigm` takes as the
field `h_gap`. Here it is a consequence of `κ ≤ √(d−1) − 1`, which is a condition
on the coupling against the graph degree, not on the gap. -/
theorem kappa_sq_le_gap (kappa : ℝ) (hk : 0 < kappa)
    (hbound : kappa ≤ Real.sqrt (S.d - 1) - 1) :
    kappa * kappa ≤ S.gap := by
  have hs := S.sqrt_sq_eq
  have h2 := S.gap_ge
  nlinarith [hs, hbound, hk.le, h2]

end RamanujanSpectrum

/-- **WITNESS — the Petersen graph.** 3-regular, non-trivial eigenvalues `1` and
`−2`, both within `2√2 ≈ 2.828`. Exhibiting an inhabitant is what makes every
theorem above non-vacuous. -/
noncomputable def petersen : RamanujanSpectrum where
  d       := 3
  lambda1 := 1
  h_deg   := le_refl 3
  h_ram   := by
    have h : (1:ℝ) ≤ Real.sqrt 2 := by
      nlinarith [Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2), Real.sqrt_nonneg 2]
    rw [abs_of_nonneg (by norm_num : (0:ℝ) ≤ 1)]
    norm_num
    linarith

/-- The witness has gap `3 − 1 = 2`. -/
theorem petersen_gap : petersen.gap = 2 := by
  unfold RamanujanSpectrum.gap petersen; norm_num

#print axioms RamanujanSpectrum.gap_pos
#print axioms RamanujanSpectrum.kappa_sq_le_gap
#print axioms petersen_gap

end ResNova.RamanujanGap
