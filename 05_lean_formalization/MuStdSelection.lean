import MuStdUniqueness
import Mathlib.Tactic
import Mathlib.Topology.Order.IntermediateValue

/-!
# Selecting `mu_std` from the A4 disjunction

`AXIOMS_V2.Axiom_A4_VariationalClosure` closes the weak-field constitutive
relation with a *disjunction*:

    mu x = x / (1 + x)   ∨   mu x = x / sqrt (1 + x ^ 2)

The first disjunct is `mu_dual`, falsified 2026-09-12: its approach to the
Newtonian limit is too slow, leaving an anomalous acceleration in the solar
system far above the Cassini and Mercury-precession bounds. The second is
`mu_std`, the live branch.

Leaving the disjunction in an axiom means the axiom still *admits* the dead
branch. This module removes it, not by deleting a disjunct, but by stating the
physical requirement that distinguishes them and proving the disjunction
collapses under it.

The discriminant is the rate at which `mu` approaches 1:

    1 - mu_dual x = 1 / (1 + x)                  -- falls like 1/x
    1 - mu_std  x = 1 / (S (S + x)) ≤ 1 / x ^ 2  -- falls like 1/(2 x^2)

A solar-system screening bound is an inverse-square tail condition. `mu_std`
satisfies it; `mu_dual` cannot, for any constant.

## What this does and does not establish

It does **not** derive `mu_std` from nothing. It shows that *given* the A4
disjunction, one added, independently motivated, falsifiable condition
(`ScreenedTail`) selects `mu_std` and excludes `mu_dual`. The content is the
exclusion: the dead branch is now ruled out inside the formal system rather
than by a note in a markdown file.

`ScreenedTail` is a postulate about the theory's solar-system behaviour, stated
as such. Its physical warrant is the Cassini bound, which is empirical.
-/

namespace ResNova.MuStdSelection

open ResNova.MuStdUniqueness

/-- The falsified branch, named so it can be excluded explicitly. -/
noncomputable def mu_dual (x : ℝ) : ℝ := x / (1 + x)

/-- An inverse-square approach to the Newtonian limit: the formal content of a
solar-system screening bound. -/
def ScreenedTail (mu : ℝ → ℝ) : Prop :=
  ∃ C > 0, ∀ x ≥ (1 : ℝ), 1 - mu x ≤ C / x ^ 2

lemma sqrt_ge_self {x : ℝ} (hx : 0 ≤ x) : x ≤ Real.sqrt (1 + x ^ 2) := by
  have h : x ^ 2 ≤ 1 + x ^ 2 := by nlinarith
  calc x = Real.sqrt (x ^ 2) := by rw [Real.sqrt_sq hx]
    _ ≤ Real.sqrt (1 + x ^ 2) := Real.sqrt_le_sqrt h

/-- `1 - mu_std x` rationalised: `(S - x)(S + x) = S² - x² = 1`. -/
lemma one_sub_mu_std {x : ℝ} (hx : 0 ≤ x) :
    1 - mu_std x = 1 / (Real.sqrt (1 + x ^ 2) * (Real.sqrt (1 + x ^ 2) + x)) := by
  have hS : 0 < Real.sqrt (1 + x ^ 2) := sqrt_one_add_sq_pos x
  have hsum : 0 < Real.sqrt (1 + x ^ 2) + x := by linarith
  have hsq : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 := sq_sqrt_one_add_sq x
  have key : (1 - mu_std x) * (Real.sqrt (1 + x ^ 2) * (Real.sqrt (1 + x ^ 2) + x)) = 1 := by
    unfold mu_std
    field_simp
    nlinarith [hsq, hS, hsum]
  rw [eq_div_iff (by positivity)]
  exact key

/-- **`mu_std` is screened.** Its tail falls like `1 / (2 x ^ 2)`, so `C = 1` works. -/
theorem mu_std_screened : ScreenedTail mu_std := by
  refine ⟨1, one_pos, fun x hx => ?_⟩
  have hx0 : (0 : ℝ) < x := lt_of_lt_of_le zero_lt_one hx
  have hSx : x ≤ Real.sqrt (1 + x ^ 2) := sqrt_ge_self hx0.le
  have hS : 0 < Real.sqrt (1 + x ^ 2) := sqrt_one_add_sq_pos x
  have hx2 : (0 : ℝ) < x ^ 2 := by positivity
  have hprod : x ^ 2 ≤ Real.sqrt (1 + x ^ 2) * (Real.sqrt (1 + x ^ 2) + x) := by
    nlinarith [hSx, hS, hx0]
  rw [one_sub_mu_std hx0.le, one_div, one_div]
  simpa using inv_anti₀ hx2 hprod

/-- **`mu_dual` is not screened.** `1 - mu_dual x = 1/(1+x)` falls only like
`1/x`, so no constant `C` can bound it by `C / x ^ 2`. -/
theorem mu_dual_not_screened : ¬ ScreenedTail mu_dual := by
  rintro ⟨C, hC, h⟩
  obtain ⟨n, hn⟩ := exists_nat_gt (max 1 (4 * C))
  set x : ℝ := (n : ℝ) with hxdef
  have hx1 : (1 : ℝ) ≤ x := le_of_lt (lt_of_le_of_lt (le_max_left _ _) hn)
  have hx0 : (0 : ℝ) < x := lt_of_lt_of_le zero_lt_one hx1
  have hxC : 4 * C < x := lt_of_le_of_lt (le_max_right _ _) hn
  have h1x : (0 : ℝ) < 1 + x := by linarith
  have hval : 1 - mu_dual x = 1 / (1 + x) := by
    unfold mu_dual; field_simp; ring
  have hle := h x hx1
  rw [hval] at hle
  have hx2 : (0 : ℝ) < x ^ 2 := by positivity
  have step : (1 / (1 + x)) * ((1 + x) * x ^ 2) ≤ (C / x ^ 2) * ((1 + x) * x ^ 2) :=
    mul_le_mul_of_nonneg_right hle (by positivity)
  have key : x ^ 2 ≤ C * (1 + x) := by
    field_simp at step; linarith
  nlinarith [key, hx0, hxC, hC, hx1]

/-- **The tail is forced.** Under A4's disjunction plus the screening bound,
`mu` must be `mu_std` for all sufficiently large `x`: the dead branch cannot
survive anywhere past a computable threshold. -/
theorem screening_forces_std_eventually
    (mu : ℝ → ℝ)
    (hA4 : ∀ x > (0 : ℝ), mu x = mu_dual x ∨ mu x = mu_std x)
    (hscr : ScreenedTail mu) :
    ∃ X ≥ (1 : ℝ), ∀ x ≥ X, mu x = mu_std x := by
  obtain ⟨C, hC, hb⟩ := hscr
  obtain ⟨n, hn⟩ := exists_nat_gt (max 1 (4 * C))
  refine ⟨(n : ℝ), le_of_lt (lt_of_le_of_lt (le_max_left _ _) hn), fun x hx => ?_⟩
  have hx1 : (1 : ℝ) ≤ x := le_trans (le_of_lt (lt_of_le_of_lt (le_max_left _ _) hn)) hx
  have hx0 : (0 : ℝ) < x := lt_of_lt_of_le zero_lt_one hx1
  have hxC : 4 * C < x := lt_of_lt_of_le (lt_of_le_of_lt (le_max_right _ _) hn) hx
  rcases hA4 x hx0 with hd | hs
  · exfalso
    have h1x : (0 : ℝ) < 1 + x := by linarith
    have hval : 1 - mu x = 1 / (1 + x) := by rw [hd]; unfold mu_dual; field_simp; ring
    have hle := hb x hx1
    rw [hval] at hle
    have hx2 : (0 : ℝ) < x ^ 2 := by positivity
    have step : (1 / (1 + x)) * ((1 + x) * x ^ 2) ≤ (C / x ^ 2) * ((1 + x) * x ^ 2) :=
      mul_le_mul_of_nonneg_right hle (by positivity)
    have key : x ^ 2 ≤ C * (1 + x) := by
      field_simp at step; linarith
    nlinarith [key, hx0, hxC, hC, hx1]
  · exact hs

/-- **The disjunction collapses, under the uniform reading.** A constitutive
relation is one function, not a patchwork: A4 offers two candidates and the
theory picks one. Read that way, screening selects `mu_std` everywhere. -/
theorem screening_selects_mu_std
    (mu : ℝ → ℝ)
    (huniform : (∀ x > (0 : ℝ), mu x = mu_dual x) ∨ (∀ x > (0 : ℝ), mu x = mu_std x))
    (hscr : ScreenedTail mu) :
    ∀ x > (0 : ℝ), mu x = mu_std x := by
  rcases huniform with hd | hs
  · exfalso
    refine mu_dual_not_screened ?_
    obtain ⟨C, hC, hb⟩ := hscr
    refine ⟨C, hC, fun x hx => ?_⟩
    have hx0 : (0 : ℝ) < x := lt_of_lt_of_le zero_lt_one hx
    rw [← hd x hx0]
    exact hb x hx
  · exact hs

end ResNova.MuStdSelection


-- ---------------------------------------------------------------------------
-- Continuity closes the pointwise branch-switching gap (2026-11-13).
--
-- A4 is pointwise. The older global theorem assumed a separate huniform
-- disjunction. Here continuity plus connectedness of (0,∞) proves that a
-- function which takes only the two distinct branches cannot switch between
-- them. The physical content remains conditional on continuity and on the
-- independent ScreenedTail premise; the action must justify the former and
-- the observational field equations must justify the latter.
-- ---------------------------------------------------------------------------

/-- On x>0, the standard branch is strictly above the dual branch. -/
lemma mu_std_gt_mu_dual {x : ℝ} (hx : 0 < x) :
    mu_std x > mu_dual x := by
  have harg : 1 + x ^ 2 < (1 + x) ^ 2 := by nlinarith
  have hroot : Real.sqrt (1 + x ^ 2) < 1 + x := by
    calc
      Real.sqrt (1 + x ^ 2) < Real.sqrt ((1 + x) ^ 2) :=
        Real.sqrt_lt_sqrt (by positivity) harg
      _ = 1 + x := Real.sqrt_sq (by linarith)
  have hcross' : x * Real.sqrt (1 + x ^ 2) < x * (1 + x) :=
    mul_lt_mul_of_pos_left hroot hx
  have hcross : x / (1 + x) < x / Real.sqrt (1 + x ^ 2) := by
    apply (div_lt_div_iff₀ (by positivity) (sqrt_one_add_sq_pos x)).2
    exact hcross'
  simpa [mu_std, mu_dual] using hcross

/-- Signed separation from the midpoint: the gap is negative on the dual
branch and positive on the standard branch. -/
def branchGap (mu : ℝ → ℝ) (x : ℝ) : ℝ :=
  mu x - (mu_std x + mu_dual x) / 2

lemma branchGap_dual {mu : ℝ → ℝ} {x : ℝ}
    (hx : 0 < x) (hbranch : mu x = mu_dual x) :
    branchGap mu x < 0 := by
  unfold branchGap
  rw [hbranch]
  nlinarith [mu_std_gt_mu_dual hx]

lemma branchGap_std {mu : ℝ → ℝ} {x : ℝ}
    (hx : 0 < x) (hbranch : mu x = mu_std x) :
    0 < branchGap mu x := by
  unfold branchGap
  rw [hbranch]
  nlinarith [mu_std_gt_mu_dual hx]

lemma branchGap_continuousOn (mu : ℝ → ℝ)
    (hmu : ContinuousOn mu (Ioi (0 : ℝ))) :
    ContinuousOn (branchGap mu) (Ioi (0 : ℝ)) := by
  have hsqrt : Continuous (fun x : ℝ => Real.sqrt (1 + x ^ 2)) := by
    fun_prop
  have hstd : ContinuousOn mu_std (Ioi (0 : ℝ)) := by
    have hden : ∀ x : ℝ, Real.sqrt (1 + x ^ 2) ≠ 0 := by
      intro x
      exact (sqrt_one_add_sq_pos x).ne'
    have hcont : Continuous (fun x : ℝ => x / Real.sqrt (1 + x ^ 2)) :=
      continuous_id.div hsqrt hden
    exact hcont.continuousOn
  have hden : ContinuousOn (fun x : ℝ => 1 + x) (Ioi (0 : ℝ)) :=
    continuousOn_const.add continuousOn_id
  have hdual : ContinuousOn mu_dual (Ioi (0 : ℝ)) := by
    change ContinuousOn (fun x : ℝ => x / (1 + x)) (Ioi (0 : ℝ))
    exact continuousOn_id.div hden (by
      intro x hx
      linarith)
  unfold branchGap
  exact hmu.sub ((hstd.add hdual).div_const 2)

/-- A continuous function satisfying the pointwise A4 branch disjunction must
use one branch on all of (0,∞). This eliminates arbitrary pointwise switching
without assuming the global huniform disjunction. -/
theorem continuous_branch_disjunction_is_uniform
    (mu : ℝ → ℝ)
    (hA4 : ∀ x > (0 : ℝ), mu x = mu_dual x ∨ mu x = mu_std x)
    (hcont : ContinuousOn mu (Ioi (0 : ℝ))) :
    (∀ x > (0 : ℝ), mu x = mu_dual x) ∨
      (∀ x > (0 : ℝ), mu x = mu_std x) := by
  by_contra hnot
  have hnotDual : ¬ (∀ x > (0 : ℝ), mu x = mu_dual x) := by
    intro h
    exact hnot (Or.inl h)
  have hnotStd : ¬ (∀ x > (0 : ℝ), mu x = mu_std x) := by
    intro h
    exact hnot (Or.inr h)
  have hstdExists : ∃ x, 0 < x ∧ mu x = mu_std x := by
    by_contra h
    apply hnotDual
    intro x hx
    rcases hA4 x hx with hdual | hstd
    · exact hdual
    · exact False.elim (h ⟨x, hx, hstd⟩)
  have hdualExists : ∃ x, 0 < x ∧ mu x = mu_dual x := by
    by_contra h
    apply hnotStd
    intro x hx
    rcases hA4 x hx with hdual | hstd
    · exact False.elim (h ⟨x, hx, hdual⟩)
    · exact hstd
  obtain ⟨xStd, hxStd, hStd⟩ := hstdExists
  obtain ⟨xDual, hxDual, hDual⟩ := hdualExists
  have hgapCont := branchGap_continuousOn mu hcont
  rcases le_total xDual xStd with hDualStd | hStdDual
  · have hcontIcc : ContinuousOn (branchGap mu) (Set.Icc xDual xStd) :=
      hgapCont.mono (by
        intro x hx
        exact lt_of_lt_of_le hxDual hx.1)
    have hmem : (0 : ℝ) ∈ branchGap mu '' Set.Icc xDual xStd :=
      (intermediate_value_Icc hDualStd hcontIcc)
        ⟨le_of_lt (branchGap_dual hxDual hDual),
          le_of_lt (branchGap_std hxStd hStd)⟩
    rcases hmem with ⟨y, hy, hzero⟩
    have hypos : 0 < y := lt_of_lt_of_le hxDual hy.1
    rcases hA4 y hypos with hdual | hstd
    · have hneg := branchGap_dual hypos hdual
      rw [hzero] at hneg
      norm_num at hneg
    · have hpos := branchGap_std hypos hstd
      rw [hzero] at hpos
      norm_num at hpos
  · have hcontIcc : ContinuousOn (branchGap mu) (Set.Icc xStd xDual) :=
      hgapCont.mono (by
        intro x hx
        exact lt_of_lt_of_le hxStd hx.1)
    have hmem : (0 : ℝ) ∈ branchGap mu '' Set.Icc xStd xDual :=
      (intermediate_value_Icc' hStdDual hcontIcc)
        ⟨le_of_lt (branchGap_dual hxDual hDual),
          le_of_lt (branchGap_std hxStd hStd)⟩
    rcases hmem with ⟨y, hy, hzero⟩
    have hypos : 0 < y := lt_of_lt_of_le hxStd hy.1
    rcases hA4 y hypos with hdual | hstd
    · have hneg := branchGap_dual hypos hdual
      rw [hzero] at hneg
      norm_num at hneg
    · have hpos := branchGap_std hypos hstd
      rw [hzero] at hpos
      norm_num at hpos

/-- The inverse-square screening condition plus continuity now selects the
standard branch globally from A4's pointwise disjunction. The proof no longer
assumes a global branch choice, but continuity is an explicit extra premise;
it must ultimately follow from the differentiable physical action. -/
theorem screening_selects_mu_std_of_continuity
    (mu : ℝ → ℝ)
    (hA4 : ∀ x > (0 : ℝ), mu x = mu_dual x ∨ mu x = mu_std x)
    (hscr : ScreenedTail mu)
    (hcont : ContinuousOn mu (Ioi (0 : ℝ))) :
    ∀ x > (0 : ℝ), mu x = mu_std x := by
  rcases continuous_branch_disjunction_is_uniform mu hA4 hcont with hdual | hstd
  · obtain ⟨C, hC, hbound⟩ := hscr
    have hdualScreened : ScreenedTail mu_dual := by
      refine ⟨C, hC, ?_⟩
      intro x hx
      have hxpos : 0 < x := by linarith
      rw [← hdual x hxpos]
      exact hbound x hx
    exact False.elim (mu_dual_not_screened hdualScreened)
  · exact hstd

#print axioms continuous_branch_disjunction_is_uniform
#print axioms screening_selects_mu_std_of_continuity
