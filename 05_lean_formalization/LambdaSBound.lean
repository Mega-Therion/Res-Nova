import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# The `lambda_s` bound: why the outer solar system binds

`TARGET_D3_PPN_AND_SOLAR_SYSTEM.md` §8 derives the residual acceleration left by
`mu_std` beyond Newton,

    delta_g(r) = (1 + lambda_s)^3 a_0^2 r^2 / (2 G_N M)

and observes that because it **grows** as `r^2`, the binding solar-system test
is the outermost body with a datum, not the innermost. That inverts the usual
intuition and it is what turns Cassini-at-Saturn into the corpus's first upper
bound on `lambda_s`.

This module formalises the structural content of that argument — the part the
document tiers `[D]`:

* the residual and the derived quadrupole-scale observable `Q_2 = delta_g / r`
  are increasing in `r` and in `lambda_s`;
* therefore the constraint from an outer body is never weaker than from an
  inner one;
* and a measured ceiling on `Q_2` inverts to a ceiling on `(1 + lambda_s)^3`.

It deliberately does **not** formalise the number. The document is explicit
that the existence of an `O(1)` bound is `[D]` while the specific value is
`[C]`, for two independent reasons: the `Q_2` route maps a monopole residual
onto an anisotropic quadrupole datum, and the precession route uses ephemeris
bounds without provenance in the repository. Both weaknesses live in the
empirical inputs, not in the algebra below.

Nothing here asserts that `lambda_s` is bounded. It says: *given* a ceiling on
the observable at some radius, this is the ceiling on `lambda_s` that follows,
and outer radii give tighter ones.
-/

namespace ResNova.LambdaSBound

/-- Residual acceleration beyond Newton under `mu_std`, as derived in D3 §8. -/
noncomputable def deltaG (lam a0 GM r : ℝ) : ℝ :=
  (1 + lam) ^ 3 * a0 ^ 2 * r ^ 2 / (2 * GM)

/-- The quadrupole-scale observable the Cassini datum is quoted against. -/
noncomputable def Q2 (lam a0 GM r : ℝ) : ℝ := deltaG lam a0 GM r / r

/-- `Q_2` in closed form: one power of `r`, not two. -/
theorem Q2_eq {lam a0 GM r : ℝ} (hr : r ≠ 0) :
    Q2 lam a0 GM r = (1 + lam) ^ 3 * a0 ^ 2 * r / (2 * GM) := by
  unfold Q2 deltaG
  field_simp

/-- **The residual grows with radius.** This is the whole inversion: the
constraint tightens as you move outward. -/
theorem deltaG_mono_r {lam a0 GM r₁ r₂ : ℝ}
    (hlam : 0 ≤ lam) (hGM : 0 < GM) (h0 : 0 ≤ r₁) (h : r₁ ≤ r₂) :
    deltaG lam a0 GM r₁ ≤ deltaG lam a0 GM r₂ := by
  have h3 : (0 : ℝ) ≤ (1 + lam) ^ 3 := by positivity
  have hsq : r₁ ^ 2 ≤ r₂ ^ 2 := by nlinarith
  unfold deltaG
  gcongr

/-- `Q_2` likewise grows with radius, linearly. -/
theorem Q2_mono_r {lam a0 GM r₁ r₂ : ℝ}
    (hlam : 0 ≤ lam) (hGM : 0 < GM) (h0 : 0 < r₁) (h : r₁ ≤ r₂) :
    Q2 lam a0 GM r₁ ≤ Q2 lam a0 GM r₂ := by
  rw [Q2_eq (ne_of_gt h0), Q2_eq (ne_of_gt (lt_of_lt_of_le h0 h))]
  have h3 : (0 : ℝ) ≤ (1 + lam) ^ 3 := by positivity
  gcongr

/-- A larger `lambda_s` means a larger signal, so the observable is a genuine
one-sided constraint on it. -/
theorem Q2_mono_lam {lam₁ lam₂ a0 GM r : ℝ}
    (h1 : 0 ≤ lam₁) (h : lam₁ ≤ lam₂) (hGM : 0 < GM) (hr : 0 < r) :
    Q2 lam₁ a0 GM r ≤ Q2 lam₂ a0 GM r := by
  rw [Q2_eq (ne_of_gt hr), Q2_eq (ne_of_gt hr)]
  have hb : (0 : ℝ) ≤ 1 + lam₁ := by linarith
  have hab : (1 : ℝ) + lam₁ ≤ 1 + lam₂ := by linarith
  have hfactor : (1 + lam₂) ^ 3 - (1 + lam₁) ^ 3
      = ((1 + lam₂) - (1 + lam₁))
        * ((1 + lam₂) ^ 2 + (1 + lam₂) * (1 + lam₁) + (1 + lam₁) ^ 2) := by ring
  have hnn : 0 ≤ ((1 + lam₂) - (1 + lam₁))
        * ((1 + lam₂) ^ 2 + (1 + lam₂) * (1 + lam₁) + (1 + lam₁) ^ 2) :=
    mul_nonneg (by linarith) (by nlinarith [hb, hab])
  have hc : (1 + lam₁) ^ 3 ≤ (1 + lam₂) ^ 3 := by linarith [hfactor, hnn]
  gcongr

/-- **The inversion.** A measured ceiling `Q_2 ≤ Qmax` at radius `r` is a
ceiling on `(1 + lambda_s)^3`. Taking cube roots gives the quoted
`lambda_s ≲ O(1)`; the cube form is stated because it is exact, whereas the
numerical root depends on empirical inputs the document tiers `[C]`. -/
theorem lambda_ceiling {lam a0 GM r Qmax : ℝ}
    (hGM : 0 < GM) (hr : 0 < r) (ha0 : a0 ≠ 0)
    (hmeas : Q2 lam a0 GM r ≤ Qmax) :
    (1 + lam) ^ 3 ≤ 2 * GM * Qmax / (a0 ^ 2 * r) := by
  rw [Q2_eq (ne_of_gt hr)] at hmeas
  rw [le_div_iff₀ (by positivity)]
  rw [div_le_iff₀ (by positivity)] at hmeas
  nlinarith [hmeas, hr, hGM, sq_nonneg a0]

/-- **The outermost datum binds.** The ceiling derived at a larger radius is
never weaker. This is the formal content of "Saturn, not Mercury". -/
theorem outer_ceiling_tighter {a0 GM r₁ r₂ Qmax : ℝ}
    (hGM : 0 < GM) (h0 : 0 < r₁) (h : r₁ ≤ r₂) (ha0 : a0 ≠ 0) (hQ : 0 ≤ Qmax) :
    2 * GM * Qmax / (a0 ^ 2 * r₂) ≤ 2 * GM * Qmax / (a0 ^ 2 * r₁) := by
  have hr₂ : 0 < r₂ := lt_of_lt_of_le h0 h
  have ha : (0 : ℝ) < a0 ^ 2 := by positivity
  gcongr

end ResNova.LambdaSBound
