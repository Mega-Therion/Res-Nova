import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Tactic

/-!
# Target D2 Supplement: structural uniqueness of μ_std(x) = x/√(1+x²)

Source document: `TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md` (2026-09-12).
Mirrors the proof pattern of `Hamilgrangian.lean` (μ_dual = x/(1+x), Padé/odds route)
and `CovariantCompletion.lean`.

## Creation frame — read before citing

**Motivation.** `TARGET_D2` Theorem 9.1/9.2 derived μ_dual = x/(1+x) from an
odds/Fisher argument in the *presence* coordinate p ∈ (0,1). The supplement asks
whether μ_std = x/√(1+x²) — the interpolating function actually used elsewhere in
the corpus — has a derivation of the same shape rather than being a fitted ansatz.
It does, in the *chirality* coordinate m ∈ (−1,1), where the rectification is
`artanh` (rapidity).

**Inputs that are NOT derived (this file proves implications, not physics):**

1. **Postulate R** (rapidity conjugacy) `dF/dψ = x²`, ψ = artanh μ. An input, of the
   same kind as D2 §9.2's odds postulate. `[O]`
2. **The chiral coordinate** — that μ→0 means *unpolarized*, not *absent*. `[C]`
3. **μ′(0) = 1** — an input here exactly as in D2 Theorem 9.3. `[O]`
4. **D2 constraint 4** (the additive `F = F_Newton − F_correction` split) is
   **dropped**, not satisfied; it is unsatisfiable for `F_std`. `[X]`

**Theorem D of the source document is binding here:** §3 (Postulate R) and §4 (the
chiral Fisher identity) are *the same postulate in two dresses*. `theorem_A_*` and
`theorem_B_*` below are **one result, not two independent corroborations**. Do not
count them twice.

**Convention.** AQUAL normalization `F′(x) = x·μ(x)` throughout (the only one that
yields `∇·[μ∇Φ] = 4πGρ`). The object `√(1+x²) − 1` belongs to the rejected
`F′ = μ` normalization (source §1, `[X]`) and does not appear in this file.

**What would falsify this.** Nothing here is empirical: these are implications. The
*physics* dies if the AeST/Skordis–Złośnik embedding forces a different μ (source
§6 item 4, open), or if rotation-curve data at the a₀ crossover discriminate
against x/√(1+x²) in favour of x/(1+x).

## Contents

* `theorem_A_constitutive`      — F_std′(x) = x·μ_std(x)                      `[thm]`
* `theorem_A_conjugacy`         — d/dψ F_std(sinh ψ) = sinh²ψ  (Postulate R holds) `[thm]`
* `theorem_A_postulate_R_ode`   — Postulate R + constitutive ⟹ X′ sinh = X cosh `[thm]`
* `theorem_A_celerity_forced`   — that ODE ⟹ X(ψ) = C sinh ψ                  `[thm]`
* `theorem_A_uniqueness`        — with the normalization, μ = μ_std           `[conditional]`
* `mu_fam_hasDerivAt_zero`      — μ′(0) = 1/C: the normalization *is* μ′(0)=1 `[thm]`
* `theorem_B_fisher_identity`   — F_std′² · ℐ_±(μ_std) = x⁴                    `[thm]`
* `theorem_B_uniqueness`        — that identity ⟺ μ = μ_std on the branch 0<μ<1 `[thm]`
* `theorem_C_exponent_family`   — F′² ℐ_± = x^{2n+2} ⟺ μ = xⁿ/√(1+x^{2n})      `[thm]`
* `theorem_C_selects_n_one`     — μ′(0) = 1 iff n = 1 (i.e. k = 4)             `[thm]`
* `F_std_deriv2_pos` / `F_std_strictConvexOn` — ghost-free convexity           `[thm]`

## Formalization gap, stated explicitly

Source §4's Theorem C table runs `k = 3,4,5,6`. This file formalizes only the **even**
branch `k = 2n+2`, `n : ℕ` — i.e. `k = 4` and `k = 6` from the table, plus every
higher even `k`. The odd entries `k = 3, 5` need half-integer powers `x^{1/2}`,
`x^{3/2}`, whose `μ′(0)` claims (`∞` and `0`) are limit statements at a point where
the function is not differentiable; they are **not** proved here. The gap is a
scope choice of this file, not a defect in the prose: the doc's selection argument
`only μ′(0)=1 survives` is therefore machine-checked against the even competitors
and left open against `k = 3, 5`.
-/

namespace ResNova.MuStdUniqueness

open Real Set

noncomputable section

/-! ## 0. Definitions -/

/-- The standard interpolating function `μ_std(x) = x/√(1+x²) = tanh(arsinh x)`. -/
def mu_std (x : ℝ) : ℝ := x / Real.sqrt (1 + x ^ 2)

/-- The AQUAL kinetic potential `F_std(x) = ½[x√(1+x²) − arsinh x]`
(`TARGET_D2` §3; convention `F′ = xμ`). -/
def F_std (x : ℝ) : ℝ := (1 / 2) * (x * Real.sqrt (1 + x ^ 2) - Real.arsinh x)

/-- `F_std′(x) = x²/√(1+x²)`. -/
def F_std_deriv (x : ℝ) : ℝ := x ^ 2 / Real.sqrt (1 + x ^ 2)

/-- `F_std″(x) = x(2+x²)/(√(1+x²))³` — the ghost-free/convexity integrand. -/
def F_std_deriv2 (x : ℝ) : ℝ := x * (2 + x ^ 2) / Real.sqrt (1 + x ^ 2) ^ 3

/-- Chiral (magnetization) Fisher information `ℐ_±(m) = 1/(1−m²) = γ²`. -/
def fisherChiral (m : ℝ) : ℝ := 1 / (1 - m ^ 2)

/-- The one-parameter celerity family `μ_C(x) = x/√(C²+x²)` arising from the
integration constant of Postulate R's ODE (`x = C sinh ψ`). -/
def mu_fam (C x : ℝ) : ℝ := x / Real.sqrt (C ^ 2 + x ^ 2)

/-- The exponent family of source §4 Theorem C, even branch `k = 2n+2`. -/
def mu_exp (n : ℕ) (x : ℝ) : ℝ := x ^ n / Real.sqrt (1 + x ^ (2 * n))

/-! ## Arithmetic helpers -/

lemma one_add_sq_pos (x : ℝ) : (0 : ℝ) < 1 + x ^ 2 := by positivity

lemma sqrt_one_add_sq_pos (x : ℝ) : 0 < Real.sqrt (1 + x ^ 2) :=
  Real.sqrt_pos.mpr (one_add_sq_pos x)

lemma sqrt_one_add_sq_ne (x : ℝ) : Real.sqrt (1 + x ^ 2) ≠ 0 :=
  (sqrt_one_add_sq_pos x).ne'

lemma sq_sqrt_one_add_sq (x : ℝ) : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 :=
  Real.sq_sqrt (one_add_sq_pos x).le

/-! ## 1. Theorem A — Postulate R forces μ_std -/

/-- `d/dx √(1+x²) = x/√(1+x²)`. -/
lemma hasDerivAt_sqrt_one_add_sq (x : ℝ) :
    HasDerivAt (fun y : ℝ => Real.sqrt (1 + y ^ 2)) (x / Real.sqrt (1 + x ^ 2)) x := by
  have hpoly : HasDerivAt (fun y : ℝ => 1 + y ^ 2) (2 * x) x := by
    simpa using ((hasDerivAt_pow 2 x).const_add 1)
  have h := hpoly.sqrt (one_add_sq_pos x).ne'
  have : 2 * x / (2 * Real.sqrt (1 + x ^ 2)) = x / Real.sqrt (1 + x ^ 2) := by
    rw [mul_div_mul_left _ _ (two_ne_zero)]
  rwa [this] at h

/-- `x·μ_std(x) = x²/√(1+x²) = F_std′(x)`. -/
lemma x_mul_mu_std (x : ℝ) : x * mu_std x = F_std_deriv x := by
  simp [mu_std, F_std_deriv, mul_div_assoc, sq]

/-- **Theorem A, constitutive half `[thm]`.** `F_std` obeys the AQUAL constitutive
relation `F′(x) = x·μ_std(x)` (D2 constraint 1). -/
theorem theorem_A_constitutive (x : ℝ) :
    HasDerivAt F_std (x * mu_std x) x := by
  have hs := hasDerivAt_sqrt_one_add_sq x
  have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id x
  have hprod : HasDerivAt (fun y : ℝ => y * Real.sqrt (1 + y ^ 2))
      (1 * Real.sqrt (1 + x ^ 2) + x * (x / Real.sqrt (1 + x ^ 2))) x := hid.mul hs
  have hsub := hprod.sub (Real.hasDerivAt_arsinh x)
  have hF := hsub.const_mul (1 / 2 : ℝ)
  have hval : (1 / 2 : ℝ) *
      (1 * Real.sqrt (1 + x ^ 2) + x * (x / Real.sqrt (1 + x ^ 2))
        - (Real.sqrt (1 + x ^ 2))⁻¹) = x * mu_std x := by
    have hne := sqrt_one_add_sq_ne x
    have hsq := sq_sqrt_one_add_sq x
    simp only [mu_std]
    field_simp
    linarith [hsq]
  have hF' : HasDerivAt F_std
      ((1 / 2 : ℝ) * (1 * Real.sqrt (1 + x ^ 2) + x * (x / Real.sqrt (1 + x ^ 2))
        - (Real.sqrt (1 + x ^ 2))⁻¹)) x := hF
  rwa [hval] at hF'

/-- `F_std′` as a closed form. -/
theorem F_std_hasDerivAt (x : ℝ) : HasDerivAt F_std (F_std_deriv x) x := by
  have h := theorem_A_constitutive x
  rwa [x_mul_mu_std] at h

lemma deriv_F_std : deriv F_std = F_std_deriv := funext fun x => (F_std_hasDerivAt x).deriv

/-- `μ_std(sinh ψ) = tanh ψ`: `x` is the celerity, `μ` the velocity of one boost. -/
lemma mu_std_sinh (ψ : ℝ) : mu_std (Real.sinh ψ) = Real.tanh ψ := by
  rw [mu_std, ← Real.cosh_arsinh (Real.sinh ψ), Real.arsinh_sinh, Real.tanh_eq_sinh_div_cosh]

/-- `F_std(sinh ψ) = ½(sinh ψ cosh ψ − ψ)` — the ψ-coordinate antiderivative of `sinh²`. -/
theorem F_std_of_sinh (ψ : ℝ) :
    F_std (Real.sinh ψ) = (1 / 2) * (Real.sinh ψ * Real.cosh ψ - ψ) := by
  rw [F_std, ← Real.cosh_arsinh (Real.sinh ψ), Real.arsinh_sinh]

/-- **Theorem A, Postulate R holds for `F_std` `[thm]`.**
With `x = sinh ψ`, the kinetic potential is conjugate to the rapidity:
`dF/dψ = x² = sinh²ψ`. -/
theorem theorem_A_conjugacy (ψ : ℝ) :
    HasDerivAt (fun t : ℝ => F_std (Real.sinh t)) (Real.sinh ψ ^ 2) ψ := by
  have hsinh : HasDerivAt Real.sinh (Real.cosh ψ) ψ := Real.hasDerivAt_sinh ψ
  have h := (F_std_hasDerivAt (Real.sinh ψ)).comp ψ hsinh
  have hval : F_std_deriv (Real.sinh ψ) * Real.cosh ψ = Real.sinh ψ ^ 2 := by
    rw [F_std_deriv, ← Real.cosh_arsinh (Real.sinh ψ), Real.arsinh_sinh]
    field_simp
  simpa [Function.comp_def, hval] using h

/-- **Theorem A, step 1 `[thm]`.** Postulate R (`dF/dψ = x²`) together with the
constitutive relation `F′(x) = x·μ`, `μ = tanh ψ`, forces the celerity ODE
`X′(ψ) sinh ψ = X(ψ) cosh ψ` — i.e. `X′/X = coth ψ`. -/
theorem theorem_A_postulate_R_ode
    (F X X' : ℝ → ℝ)
    (hXpos : ∀ ψ ∈ Ioi (0 : ℝ), 0 < X ψ)
    (hX : ∀ ψ ∈ Ioi (0 : ℝ), HasDerivAt X (X' ψ) ψ)
    (hcon : ∀ ψ ∈ Ioi (0 : ℝ), HasDerivAt F (X ψ * Real.tanh ψ) (X ψ))
    (hR : ∀ ψ ∈ Ioi (0 : ℝ), HasDerivAt (fun t : ℝ => F (X t)) (X ψ ^ 2) ψ) :
    ∀ ψ ∈ Ioi (0 : ℝ), X' ψ * Real.sinh ψ = X ψ * Real.cosh ψ := by
  intro ψ hψ
  have hchain : HasDerivAt (fun t : ℝ => F (X t)) (X ψ * Real.tanh ψ * X' ψ) ψ :=
    (hcon ψ hψ).comp ψ (hX ψ hψ)
  have heq : X ψ * Real.tanh ψ * X' ψ = X ψ ^ 2 := hchain.unique (hR ψ hψ)
  have hXne : X ψ ≠ 0 := (hXpos ψ hψ).ne'
  have hcosh : Real.cosh ψ ≠ 0 := (Real.cosh_pos ψ).ne'
  have htanh : Real.tanh ψ * X' ψ = X ψ := by
    apply mul_left_cancel₀ hXne
    rw [← mul_assoc, heq]
    ring
  rw [Real.tanh_eq_sinh_div_cosh] at htanh
  field_simp at htanh
  linear_combination htanh

/-- **Theorem A, step 2 `[thm]`.** The celerity ODE `X′ sinh = X cosh` on `(0,∞)`
integrates to `X(ψ) = C sinh ψ`: the ratio `X/sinh` is constant. -/
theorem theorem_A_celerity_forced
    (X X' : ℝ → ℝ)
    (hX : ∀ ψ ∈ Ioi (0 : ℝ), HasDerivAt X (X' ψ) ψ)
    (hode : ∀ ψ ∈ Ioi (0 : ℝ), X' ψ * Real.sinh ψ = X ψ * Real.cosh ψ)
    {ψ₀ ψ : ℝ} (h0 : ψ₀ ∈ Ioi (0 : ℝ)) (h1 : ψ ∈ Ioi (0 : ℝ)) :
    X ψ * Real.sinh ψ₀ = X ψ₀ * Real.sinh ψ := by
  have hsinh_ne : ∀ t ∈ Ioi (0 : ℝ), Real.sinh t ≠ 0 := by
    intro t ht; exact (Real.sinh_pos_iff.mpr ht).ne'
  have hgderiv : ∀ t ∈ Ioi (0 : ℝ),
      HasDerivAt (fun t : ℝ => X t / Real.sinh t) 0 t := by
    intro t ht
    have h := (hX t ht).div (Real.hasDerivAt_sinh t) (hsinh_ne t ht)
    have : (X' t * Real.sinh t - X t * Real.cosh t) / Real.sinh t ^ 2 = 0 := by
      rw [hode t ht]; simp
    rwa [this] at h
  have hdiff : DifferentiableOn ℝ (fun t : ℝ => X t / Real.sinh t) (Ioi (0 : ℝ)) := fun t ht =>
    ((hgderiv t ht).differentiableAt).differentiableWithinAt
  have hzero : EqOn (deriv fun t : ℝ => X t / Real.sinh t) 0 (Ioi (0 : ℝ)) := by
    intro t ht; simpa using (hgderiv t ht).deriv
  have hconst : X ψ / Real.sinh ψ = X ψ₀ / Real.sinh ψ₀ :=
    isOpen_Ioi.is_const_of_deriv_eq_zero (isPreconnected_Ioi) hdiff hzero h1 h0
  have h1' := hsinh_ne ψ h1
  have h0' := hsinh_ne ψ₀ h0
  field_simp at hconst
  linear_combination hconst

/-- `μ_C′(0) = 1/C`: the integration constant of Theorem A is exactly the reciprocal
of the slope at the origin, so `μ′(0)=1 ⟺ C = 1 ⟺ μ = μ_std`. Analogue of
`Hamilgrangian.mu_pade_hasDerivAt_zero`. -/
theorem mu_fam_hasDerivAt_zero (C : ℝ) (hC : 0 < C) :
    HasDerivAt (mu_fam C) (1 / C) 0 := by
  have hpoly : HasDerivAt (fun y : ℝ => C ^ 2 + y ^ 2) (2 * (0 : ℝ)) 0 := by
    simpa using ((hasDerivAt_pow 2 (0 : ℝ)).const_add (C ^ 2))
  have hpos : (0 : ℝ) < C ^ 2 + (0 : ℝ) ^ 2 := by positivity
  have hroot := hpoly.sqrt hpos.ne'
  have hnum : HasDerivAt (fun y : ℝ => y) 1 (0 : ℝ) := hasDerivAt_id 0
  have h := hnum.div hroot (Real.sqrt_ne_zero'.mpr hpos)
  have hsq : Real.sqrt (C ^ 2 + (0 : ℝ) ^ 2) = C := by
    norm_num [Real.sqrt_sq hC.le]
  rw [hsq] at h
  have hval : (1 * C - 0 * (2 * (0 : ℝ) / (2 * C))) / C ^ 2 = 1 / C := by
    field_simp
    ring
  rw [hval] at h
  exact h

/-- `μ′(0) = 1` selects `C = 1` in the celerity family. -/
theorem mu_fam_normalization (C : ℝ) (hC : 0 < C)
    (h : HasDerivAt (mu_fam C) 1 0) : C = 1 := by
  have := (mu_fam_hasDerivAt_zero C hC).unique h
  field_simp at this
  linarith

lemma mu_fam_one (x : ℝ) : mu_fam 1 x = mu_std x := by
  simp [mu_fam, mu_std]

/-- **Theorem A `[conditional]` — on Postulate R, the chiral coordinate, and μ′(0)=1.**
Postulate R plus the constitutive relation plus the normalization `X ψ₀ = sinh ψ₀`
(equivalently `C = 1`, equivalently `μ′(0) = 1` by `mu_fam_normalization`) force the
celerity to be `sinh ψ` and hence the interpolating function to be `μ_std`. -/
theorem theorem_A_uniqueness
    (F X X' : ℝ → ℝ)
    (hXpos : ∀ ψ ∈ Ioi (0 : ℝ), 0 < X ψ)
    (hX : ∀ ψ ∈ Ioi (0 : ℝ), HasDerivAt X (X' ψ) ψ)
    (hcon : ∀ ψ ∈ Ioi (0 : ℝ), HasDerivAt F (X ψ * Real.tanh ψ) (X ψ))
    (hR : ∀ ψ ∈ Ioi (0 : ℝ), HasDerivAt (fun t : ℝ => F (X t)) (X ψ ^ 2) ψ)
    {ψ₀ : ℝ} (h0 : ψ₀ ∈ Ioi (0 : ℝ)) (hnorm : X ψ₀ = Real.sinh ψ₀) :
    ∀ ψ ∈ Ioi (0 : ℝ), X ψ = Real.sinh ψ ∧ mu_std (X ψ) = Real.tanh ψ := by
  intro ψ hψ
  have hode := theorem_A_postulate_R_ode F X X' hXpos hX hcon hR
  have hkey := theorem_A_celerity_forced X X' hX hode h0 hψ
  have hs0 : Real.sinh ψ₀ ≠ 0 := (Real.sinh_pos_iff.mpr h0).ne'
  have hXeq : X ψ = Real.sinh ψ := by
    rw [hnorm] at hkey
    exact mul_right_cancel₀ hs0 (by linarith [hkey])
  exact ⟨hXeq, by rw [hXeq, mu_std_sinh]⟩

/-! ## 2. Theorem B — the chiral Fisher identity -/

/-- **Theorem B, forward `[thm]`.** `F_std′(x)² · ℐ_±(μ_std(x)) = x⁴`. -/
theorem theorem_B_fisher_identity (x : ℝ) :
    F_std_deriv x ^ 2 * fisherChiral (mu_std x) = x ^ 4 := by
  have hne := sqrt_one_add_sq_ne x
  have hsq := sq_sqrt_one_add_sq x
  have hp : (0 : ℝ) < 1 + x ^ 2 := one_add_sq_pos x
  have hmu2 : mu_std x ^ 2 = x ^ 2 / (1 + x ^ 2) := by rw [mu_std, div_pow, hsq]
  have hfis : fisherChiral (mu_std x) = 1 + x ^ 2 := by
    rw [fisherChiral, hmu2,
      show (1 : ℝ) - x ^ 2 / (1 + x ^ 2) = 1 / (1 + x ^ 2) by field_simp; ring,
      one_div_one_div]
  have hFd : F_std_deriv x ^ 2 = (x ^ 2) ^ 2 / (1 + x ^ 2) := by
    rw [F_std_deriv, div_pow, hsq]
  rw [hFd, hfis]
  field_simp

/-- **Theorem B, uniqueness `[thm]`.** On the physical branch `0 < m < 1` (the sign
branch discussed in source §4), the chiral Fisher identity
`(x·m)² · ℐ_±(m) = x⁴` holds **iff** `m = μ_std(x)`. -/
theorem theorem_B_uniqueness {x m : ℝ} (hx : 0 < x) (hm : 0 < m) (hm1 : m < 1) :
    (x * m) ^ 2 * fisherChiral m = x ^ 4 ↔ m = mu_std x := by
  have hden : 1 - m ^ 2 ≠ 0 := by nlinarith
  have hs := sqrt_one_add_sq_pos x
  have hsq := sq_sqrt_one_add_sq x
  constructor
  · intro h
    rw [fisherChiral] at h
    have h' : m ^ 2 = x ^ 2 * (1 - m ^ 2) := by
      field_simp at h; linarith [h]
    have hm2 : m ^ 2 * (1 + x ^ 2) = x ^ 2 := by linear_combination h'
    have hsq2 : (m * Real.sqrt (1 + x ^ 2)) ^ 2 = x ^ 2 := by
      rw [mul_pow, hsq]; linarith [hm2]
    have hfac2 : (m * Real.sqrt (1 + x ^ 2) - x) * (m * Real.sqrt (1 + x ^ 2) + x) = 0 := by
      linear_combination hsq2
    have hgt : 0 < m * Real.sqrt (1 + x ^ 2) + x := by positivity
    have heq : m * Real.sqrt (1 + x ^ 2) = x := by
      rcases mul_eq_zero.mp hfac2 with hz | hz
      · linarith
      · linarith
    rw [mu_std, eq_div_iff (sqrt_one_add_sq_ne x)]
    exact heq
  · intro h
    subst h
    rw [x_mul_mu_std]
    exact theorem_B_fisher_identity x

/-! ## 3. Theorem C — exponent selection -/

lemma one_add_pow_pos (n : ℕ) {x : ℝ} (hx : 0 < x) : (0 : ℝ) < 1 + x ^ (2 * n) := by
  positivity

/-- **Theorem C, family `[thm]`.** For `k = 2n + 2`, the identity
`(x m)² ℐ_±(m) = x^k` on the branch `0 < m < 1` holds iff `m = xⁿ/√(1+x^{2n})`. -/
theorem theorem_C_exponent_family (n : ℕ) {x m : ℝ} (hx : 0 < x) (hm : 0 < m) (hm1 : m < 1) :
    (x * m) ^ 2 * fisherChiral m = x ^ (2 * n + 2) ↔ m = mu_exp n x := by
  have hden : 1 - m ^ 2 ≠ 0 := by nlinarith
  have hp : (0 : ℝ) < 1 + x ^ (2 * n) := one_add_pow_pos n hx
  have hsr : Real.sqrt (1 + x ^ (2 * n)) ^ 2 = 1 + x ^ (2 * n) := Real.sq_sqrt hp.le
  have hsrpos : 0 < Real.sqrt (1 + x ^ (2 * n)) := Real.sqrt_pos.mpr hp
  have hxn : x ^ (2 * n) = (x ^ n) ^ 2 := by rw [← pow_mul, mul_comm]
  have hxk : x ^ (2 * n + 2) = (x ^ n) ^ 2 * x ^ 2 := by
    rw [pow_add, hxn]
  constructor
  · intro h
    rw [fisherChiral] at h
    have h' : x ^ 2 * m ^ 2 = x ^ (2 * n + 2) * (1 - m ^ 2) := by
      field_simp at h; linarith [h]
    rw [hxk] at h'
    have hx2 : (0 : ℝ) < x ^ 2 := by positivity
    have hxnpos : (0 : ℝ) < x ^ n := by positivity
    have hm2 : m ^ 2 * (1 + (x ^ n) ^ 2) = (x ^ n) ^ 2 := by
      have hfac : x ^ 2 * (m ^ 2 * (1 + (x ^ n) ^ 2) - (x ^ n) ^ 2) = 0 := by
        linear_combination h'
      rcases mul_eq_zero.mp hfac with hz | hz
      · exact absurd hz hx2.ne'
      · linarith
    have hsq2 : (m * Real.sqrt (1 + x ^ (2 * n))) ^ 2 = (x ^ n) ^ 2 := by
      rw [mul_pow, hsr, hxn]; linarith [hm2]
    have hfac2 : (m * Real.sqrt (1 + x ^ (2 * n)) - x ^ n)
        * (m * Real.sqrt (1 + x ^ (2 * n)) + x ^ n) = 0 := by
      linear_combination hsq2
    have hgt : 0 < m * Real.sqrt (1 + x ^ (2 * n)) + x ^ n := by positivity
    have heq : m * Real.sqrt (1 + x ^ (2 * n)) = x ^ n := by
      rcases mul_eq_zero.mp hfac2 with hz | hz
      · linarith
      · linarith
    rw [mu_exp, eq_div_iff hsrpos.ne']
    exact heq
  · intro h
    subst h
    have hmu2 : mu_exp n x ^ 2 = (x ^ n) ^ 2 / (1 + x ^ (2 * n)) := by
      rw [mu_exp, div_pow, hsr]
    have hfis : fisherChiral (mu_exp n x) = 1 + x ^ (2 * n) := by
      rw [fisherChiral, hmu2, ← hxn,
        show (1 : ℝ) - x ^ (2 * n) / (1 + x ^ (2 * n)) = 1 / (1 + x ^ (2 * n)) by
          field_simp; ring,
        one_div_one_div]
    calc (x * mu_exp n x) ^ 2 * fisherChiral (mu_exp n x)
        = x ^ 2 * (mu_exp n x) ^ 2 * fisherChiral (mu_exp n x) := by ring
      _ = x ^ 2 * ((x ^ n) ^ 2 / (1 + x ^ (2 * n))) * (1 + x ^ (2 * n)) := by rw [hmu2, hfis]
      _ = x ^ 2 * (x ^ n) ^ 2 := by field_simp
      _ = x ^ (2 * n + 2) := by rw [hxk]; ring

/-- `μ_n′(0) = 1` for `n = 1` (`k = 4`). -/
theorem theorem_C_selects_n_one : HasDerivAt (mu_exp 1) 1 0 := by
  have h : mu_exp 1 = mu_fam 1 := by
    funext x; simp [mu_exp, mu_fam]
  rw [h]
  simpa using mu_fam_hasDerivAt_zero 1 one_pos

/-- `μ_n′(0) = 0` for every `n ≥ 2` (`k ≥ 6`): the slope condition kills them. -/
theorem theorem_C_rejects_n_ge_two (n : ℕ) (hn : 2 ≤ n) :
    HasDerivAt (mu_exp n) 0 0 := by
  have hnum : HasDerivAt (fun y : ℝ => y ^ n) 0 (0 : ℝ) := by
    have := hasDerivAt_pow n (0 : ℝ)
    have hz : ((n : ℝ) * (0 : ℝ) ^ (n - 1)) = 0 := by
      have : (0 : ℝ) ^ (n - 1) = 0 := zero_pow (by omega)
      rw [this]; ring
    rwa [hz] at this
  have hpolyderiv : HasDerivAt (fun y : ℝ => 1 + y ^ (2 * n)) 0 (0 : ℝ) := by
    have := hasDerivAt_pow (2 * n) (0 : ℝ)
    have hz : ((2 * n : ℕ) : ℝ) * (0 : ℝ) ^ (2 * n - 1) = 0 := by
      have : (0 : ℝ) ^ (2 * n - 1) = 0 := zero_pow (by omega)
      rw [this]; ring
    rw [hz] at this
    simpa using this.const_add (1 : ℝ)
  have hpos : (0 : ℝ) < 1 + (0 : ℝ) ^ (2 * n) := by
    rw [zero_pow (by omega : 2 * n ≠ 0)]; norm_num
  have hroot := hpolyderiv.sqrt hpos.ne'
  have hden_ne : Real.sqrt (1 + (0 : ℝ) ^ (2 * n)) ≠ 0 := Real.sqrt_ne_zero'.mpr hpos
  have h := hnum.div hroot hden_ne
  have hs1 : Real.sqrt (1 + (0 : ℝ) ^ (2 * n)) = 1 := by
    rw [zero_pow (by omega : 2 * n ≠ 0)]; norm_num
  have hz0 : (0 : ℝ) ^ n = 0 := zero_pow (by omega)
  rw [hs1] at h
  have hval : (0 * 1 - (0 : ℝ) ^ n * (0 / (2 * 1))) / 1 ^ 2 = 0 := by
    rw [hz0]; norm_num
  rw [hval] at h
  exact h

/-! ## 4. Ghost-free convexity (source §1, corrected normalization) -/

/-- `F_std″(x) = x(2+x²)/(1+x²)^{3/2}`. -/
theorem F_std_hasDerivAt_deriv (x : ℝ) :
    HasDerivAt F_std_deriv (F_std_deriv2 x) x := by
  have hs := hasDerivAt_sqrt_one_add_sq x
  have hnum : HasDerivAt (fun y : ℝ => y ^ 2) (2 * x) x := by
    simpa using hasDerivAt_pow 2 x
  have h := hnum.div hs (sqrt_one_add_sq_ne x)
  have hne := sqrt_one_add_sq_ne x
  have hsq := sq_sqrt_one_add_sq x
  have hval : (2 * x * Real.sqrt (1 + x ^ 2) - x ^ 2 * (x / Real.sqrt (1 + x ^ 2)))
      / Real.sqrt (1 + x ^ 2) ^ 2 = F_std_deriv2 x := by
    rw [F_std_deriv2]
    field_simp
    rw [hsq]
    ring
  rwa [hval] at h

lemma deriv_F_std_deriv : deriv F_std_deriv = F_std_deriv2 :=
  funext fun x => (F_std_hasDerivAt_deriv x).deriv

/-- **Ghost-free condition `[thm]`.** `F_std″(x) > 0` for every `x > 0`: the AQUAL
kinetic potential is strictly convex, so the scalar carries no ghost. -/
theorem F_std_deriv2_pos {x : ℝ} (hx : 0 < x) : 0 < F_std_deriv2 x := by
  rw [F_std_deriv2]
  have h1 : 0 < Real.sqrt (1 + x ^ 2) ^ 3 := by positivity
  have h2 : 0 < x * (2 + x ^ 2) := by positivity
  exact div_pos h2 h1

/-- The convexity statement tied to `F_std` itself, not to a detached inequality. -/
theorem F_std_strictConvexOn : StrictConvexOn ℝ (Ici (0 : ℝ)) F_std := by
  refine strictConvexOn_of_deriv2_pos (convex_Ici 0) ?_ ?_
  · exact (fun x _ => (F_std_hasDerivAt x).differentiableAt.continuousAt.continuousWithinAt)
  · intro x hx
    rw [interior_Ici] at hx
    have : (deriv^[2] F_std) x = F_std_deriv2 x := by
      simp [Function.iterate_succ, deriv_F_std, deriv_F_std_deriv]
    rw [this]
    exact F_std_deriv2_pos hx

/-! ## 5. Axiom footprint -/

#print axioms theorem_A_constitutive
#print axioms theorem_A_conjugacy
#print axioms theorem_A_postulate_R_ode
#print axioms theorem_A_celerity_forced
#print axioms theorem_A_uniqueness
#print axioms mu_fam_hasDerivAt_zero
#print axioms mu_fam_normalization
#print axioms theorem_B_fisher_identity
#print axioms theorem_B_uniqueness
#print axioms theorem_C_exponent_family
#print axioms theorem_C_selects_n_one
#print axioms theorem_C_rejects_n_ge_two
#print axioms F_std_deriv2_pos
#print axioms F_std_strictConvexOn

end

end ResNova.MuStdUniqueness
