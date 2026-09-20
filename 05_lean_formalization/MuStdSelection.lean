import MuStdUniqueness
import Mathlib.Tactic

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
