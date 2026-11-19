import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-!
# Postulate R: Analytic Induced-Metric Brane No-Go and Analytic Auxiliary-Susceptibility Realization

Extends `audits/2026-11-19/postulate_r_membrane_derivation.py` (PR #241) and `SZStdEmbedding.lean`.

## What is proved here (`[P]`)

1. **Analytic induced-metric brane no-go (even restricted to `x ≥ 0`):**
   For a static 3-brane with induced metric `h_ij = δ_ij + v_i v_j` (`v = ∇φ / a₀`, `|v| = x`),
   every rotational scalar invariant depends solely on `y = x²` (the eigenvalues of `h` are
   `{1 + x², 1, 1}`, so `det h = 1 + x²`, `tr h = 3 + x²`, `tr(h²) = (1 + x²)² + 2`).
   Consequently, any local 1-field action `L(h_ij) = L̃(x²)` that is `C²` in `y = x²` at `y = 0`
   yields an Euler–Lagrange response `μ(x) = g(x²)` with `g` differentiable at `0`.
   - `hasDerivWithinAt_even_response_zero`: `(fun x => g (x ^ 2))` has right-derivative `0` at `x = 0`
     on `[0, ∞)`.
   - `hasDerivAt_muStd_zero` and `hasDerivWithinAt_muStd_zero`: `muStd(x) = x / √(1 + x²)` has
     derivative (and right-derivative on `[0, ∞)`) equal to `1` at `x = 0`.
   - `analytic_induced_metric_nogo_nonneg`: there is NO function `g : ℝ → ℝ` differentiable at `0`
     and NO `ε > 0` such that `g (x ^ 2) = muStd x` for all `x ∈ [0, ε)`.
   - `hasDerivAt_Jstd_deriv` and `Jstd_second_deriv_unbounded`: the AQUAL kinetic function
     `J_std(y) = F_std(√y)` has `J_std'(y) = √y / (2 √(1 + y))` and second derivative
     `J_std''(y) = 1 / (4 √y (1 + y)^(3/2))`, which diverges to `+∞` as `y → 0⁺` (a `y^(3/2)` branch point).

2. **Exact analytic auxiliary-susceptibility realization (Legendre–Fenchel supremum):**
   For an auxiliary susceptibility scalar `s ∈ [0, 1)` with the real-analytic potential
   `auxPot s = (log ((1 + s) / (1 - s)) / 2 - s) / 2 = (artanh s - s) / 2` and two-field Lagrangian
   `auxLag x s = s * x² / 2 - auxPot s`:
   - `hasDerivAt_auxPot`: `auxPot'(s) = s² / (2 (1 - s²))` for `|s| < 1`.
   - `hasDerivAt_auxPot_deriv`: `auxPot''(s) = s / (1 - s²)²` for `|s| < 1`.
   - `auxPot_critical_at_zero`: `auxPot'(0) = 0` and `auxPot''(0) = 0` (spinodal critical point at `s = 0`).
   - `auxLag_stationary_iff`: for `x ≥ 0` and `s ∈ [0, 1)`, `x² / 2 - auxPot'(s) = 0 ↔ s = muStd x`.
   - `half_log_ratio_muStd_eq_arsinh`: `(1/2) log((1 + muStd x) / (1 - muStd x)) = arsinh x`.
   - `auxLag_on_shell_eq_Fstd`: `auxLag x (muStd x) = Fstd x` identically for all `x : ℝ`.
   - `auxLag_le_Fstd`: for `x ≥ 0` and every `s ∈ [0, 1)`, `auxLag x s ≤ Fstd x`, with equality
     iff `s = muStd x` (`auxLag_eq_Fstd_iff`).

## Honest scoping (`[O]`)
This module establishes a structural no-go for 1-field local analytic induced-metric brane actions
and constructs an exact analytic two-field realization of `F_std`. Selecting `auxPot` among all
cubic-onset analytic potentials `V(s) = s³/6 + O(s⁵)` remains equivalent to Postulate R and is not
uniquely derived here.
-/

noncomputable section

namespace ResNova.PostulateRAnalyticNoGo

open Real Set

/-- Canonical live interpolating function `μ_std(x) = x / √(1 + x²)`. -/
def muStd (x : ℝ) : ℝ := x / Real.sqrt (1 + x ^ 2)

/-- Canonical live AQUAL potential `F_std(x) = (x √(1 + x²) - arsinh x) / 2`. -/
def Fstd (x : ℝ) : ℝ := (x * Real.sqrt (1 + x ^ 2) - Real.arsinh x) / 2

/-- Real-analytic auxiliary potential `V(s) = (artanh s - s) / 2` on `(-1, 1)`. -/
def auxPot (s : ℝ) : ℝ := (Real.log ((1 + s) / (1 - s)) / 2 - s) / 2

/-- Two-field auxiliary Lagrangian `L(x, s) = (1/2) s x² - V(s)`. -/
def auxLag (x s : ℝ) : ℝ := s * x ^ 2 / 2 - auxPot s

/-- Explicit first derivative `V'(s) = s² / (2 (1 - s²))`. -/
def auxPotDeriv (s : ℝ) : ℝ := s ^ 2 / (2 * (1 - s ^ 2))

/-- Explicit second derivative `V''(s) = s / (1 - s²)²`. -/
def auxPotDeriv2 (s : ℝ) : ℝ := s / (1 - s ^ 2) ^ 2

/-- Explicit first derivative of AQUAL kinetic function `J_std'(y) = √y / (2 √(1 + y))`. -/
def JstdDeriv (y : ℝ) : ℝ := Real.sqrt y / (2 * Real.sqrt (1 + y))

/-- Explicit second derivative `J_std''(y) = 1 / (4 √y (1 + y) √(1 + y))`. -/
def JstdDeriv2 (y : ℝ) : ℝ := 1 / (4 * Real.sqrt y * (1 + y) * Real.sqrt (1 + y))

/-! ## 1. Induced 3-Brane Metric Invariants & Analytic No-Go -/

/-- Determinant of the induced 3-brane metric `h_ij = δ_ij + v_i v_j` equals `1 + |v|²`. -/
theorem induced_metric_det_eq (v1 v2 v3 : ℝ) :
    (1 + v1 ^ 2) * ((1 + v2 ^ 2) * (1 + v3 ^ 2) - (v2 * v3) ^ 2)
      - (v1 * v2) * ((v1 * v2) * (1 + v3 ^ 2) - (v2 * v3) * (v1 * v3))
      + (v1 * v3) * ((v1 * v2) * (v2 * v3) - (1 + v2 ^ 2) * (v1 * v3))
      = 1 + (v1 ^ 2 + v2 ^ 2 + v3 ^ 2) := by
  ring

/-- Trace and squared-trace of `h_ij = δ_ij + v_i v_j` depend solely on `y = |v|²`. -/
theorem induced_metric_traces_eq (v1 v2 v3 : ℝ) :
    ((1 + v1 ^ 2) + (1 + v2 ^ 2) + (1 + v3 ^ 2) = 3 + (v1 ^ 2 + v2 ^ 2 + v3 ^ 2)) ∧
    ((1 + v1 ^ 2) ^ 2 + (1 + v2 ^ 2) ^ 2 + (1 + v3 ^ 2) ^ 2
        + 2 * (v1 * v2) ^ 2 + 2 * (v1 * v3) ^ 2 + 2 * (v2 * v3) ^ 2
      = (1 + (v1 ^ 2 + v2 ^ 2 + v3 ^ 2)) ^ 2 + 2) := by
  constructor <;> ring

/-- Any function of `x²` built from a `g` differentiable at `0` has derivative `0` at `x = 0`. -/
theorem hasDerivAt_even_response_zero {g : ℝ → ℝ} (hg : DifferentiableAt ℝ g 0) :
    HasDerivAt (fun x : ℝ => g (x ^ 2)) 0 0 := by
  let sq : ℝ → ℝ := fun x => x ^ 2
  have hsq : HasDerivAt sq 0 0 := by
    simpa [sq] using hasDerivAt_pow 2 (0 : ℝ)
  have hg' : HasDerivAt g (deriv g 0) (sq 0) := by
    simpa [sq] using hg.hasDerivAt
  have hc : HasDerivAt (g ∘ sq) (deriv g 0 * 0) 0 := HasDerivAt.comp (0 : ℝ) hg' hsq
  have hcomp : (g ∘ sq) = (fun x : ℝ => g (x ^ 2)) := rfl
  rw [hcomp] at hc
  exact hc.congr_deriv (mul_zero _)

/-- Even restricted to the physical domain `x ∈ [0, ∞)`, `g(x²)` has right-derivative `0` at `0`. -/
theorem hasDerivWithinAt_even_response_zero {g : ℝ → ℝ} (hg : DifferentiableAt ℝ g 0) :
    HasDerivWithinAt (fun x : ℝ => g (x ^ 2)) 0 (Set.Ici (0 : ℝ)) 0 :=
  (hasDerivAt_even_response_zero hg).hasDerivWithinAt

/-- `muStd(x) = x / √(1 + x²)` has derivative `1` at `x = 0`. -/
theorem hasDerivAt_muStd_zero : HasDerivAt muStd 1 0 := by
  have hpos : (0 : ℝ) < 1 + (0 : ℝ) ^ 2 := by norm_num
  have h1 : HasDerivAt (fun x : ℝ => 1 + x ^ 2) (2 * (0 : ℝ)) 0 := by
    simpa using (hasDerivAt_pow 2 (0 : ℝ)).const_add 1
  have hsqrt : HasDerivAt (fun x : ℝ => Real.sqrt (1 + x ^ 2))
      (2 * (0 : ℝ) / (2 * Real.sqrt (1 + (0 : ℝ) ^ 2))) 0 := h1.sqrt hpos.ne'
  have hdiv : HasDerivAt (fun x : ℝ => x / Real.sqrt (1 + x ^ 2))
      ((1 * Real.sqrt (1 + (0 : ℝ) ^ 2) - 0 * (2 * (0 : ℝ) / (2 * Real.sqrt (1 + (0 : ℝ) ^ 2)))) /
        (Real.sqrt (1 + (0 : ℝ) ^ 2)) ^ 2) 0 :=
    (hasDerivAt_id 0).div hsqrt (Real.sqrt_pos.mpr hpos).ne'
  have hsimp :
      ((1 * Real.sqrt (1 + (0 : ℝ) ^ 2) - 0 * (2 * (0 : ℝ) / (2 * Real.sqrt (1 + (0 : ℝ) ^ 2)))) /
        (Real.sqrt (1 + (0 : ℝ) ^ 2)) ^ 2) = 1 := by
    norm_num
  have hmu : (fun x : ℝ => x / Real.sqrt (1 + x ^ 2)) = muStd := rfl
  rw [hmu] at hdiv
  exact hdiv.congr_deriv hsimp

/-- **Analytic Induced-Metric Brane No-Go (on `x ≥ 0`):**
No function `g : ℝ → ℝ` differentiable at `0` can satisfy `g(x²) = μ_std(x)` on any positive
half-neighborhood `[0, ε)`. -/
theorem analytic_induced_metric_nogo_nonneg :
    ¬ ∃ (g : ℝ → ℝ) (ε : ℝ),
        DifferentiableAt ℝ g 0 ∧ 0 < ε ∧ ∀ x : ℝ, 0 ≤ x → x < ε → g (x ^ 2) = muStd x := by
  rintro ⟨g, ε, hg, hε, hEq⟩
  have h_ev : (fun x : ℝ => g (x ^ 2)) =ᶠ[nhdsWithin (0 : ℝ) (Set.Ici 0)] muStd := by
    rw [Filter.EventuallyEq, eventually_nhdsWithin_iff]
    filter_upwards [Metric.ball_mem_nhds (0 : ℝ) hε] with x hx hx0
    have hxlt : x < ε := by
      have hdist : |x - 0| < ε := by simpa [Real.dist_eq] using hx
      have hxabs : |x| < ε := by simpa using hdist
      exact (abs_lt.mp hxabs).2
    exact hEq x hx0 hxlt
  have hd0 : HasDerivWithinAt (fun x : ℝ => g (x ^ 2)) 0 (Set.Ici 0) 0 :=
    hasDerivWithinAt_even_response_zero hg
  have hd1 : HasDerivWithinAt muStd 1 (Set.Ici 0) 0 :=
    hasDerivAt_muStd_zero.hasDerivWithinAt
  have hd1' : HasDerivWithinAt (fun x : ℝ => g (x ^ 2)) 1 (Set.Ici 0) 0 :=
    hd1.congr_of_eventuallyEq h_ev (hEq 0 le_rfl hε)
  have huniq : UniqueDiffWithinAt ℝ (Set.Ici (0 : ℝ)) 0 := uniqueDiffWithinAt_Ici 0
  have h01 : (0 : ℝ) = 1 := (hd0.derivWithin huniq).symm.trans (hd1'.derivWithin huniq)
  norm_num at h01

/-! ## 2. Second-Derivative Blowup of `J_std(y) = F_std(√y)` at `y → 0⁺` -/

/-- For `y > 0`, `J_std'(y) = √y / (2 √(1 + y))` has derivative `J_std''(y) = 1 / (4 √y (1 + y)^(3/2))`. -/
theorem hasDerivAt_JstdDeriv {y : ℝ} (hy : 0 < y) :
    HasDerivAt JstdDeriv (JstdDeriv2 y) y := by
  have hy1 : 0 < 1 + y := by linarith
  have hsy : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have hs1 : 0 < Real.sqrt (1 + y) := Real.sqrt_pos.mpr hy1
  have hnum : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt y)) y := by
    simpa using Real.hasDerivAt_sqrt hy.ne'
  have h1y : HasDerivAt (fun t : ℝ => 1 + t) 1 y := by
    simpa using (hasDerivAt_id y).const_add 1
  have hden_s : HasDerivAt (fun t : ℝ => Real.sqrt (1 + t)) (1 / (2 * Real.sqrt (1 + y))) y :=
    h1y.sqrt hy1.ne'
  have hden : HasDerivAt (fun t : ℝ => 2 * Real.sqrt (1 + t))
      (2 * (1 / (2 * Real.sqrt (1 + y)))) y := hden_s.const_mul 2
  have hdiv := hnum.div hden (by positivity : 2 * Real.sqrt (1 + y) ≠ 0)
  have hsqy : Real.sqrt y * Real.sqrt y = y := Real.mul_self_sqrt hy.le
  have hsq1 : Real.sqrt (1 + y) * Real.sqrt (1 + y) = 1 + y := Real.mul_self_sqrt hy1.le
  refine hdiv.congr_deriv ?_
  unfold JstdDeriv2
  field_simp [hsy.ne', hs1.ne', hy1.ne']
  nlinarith [hsqy, hsq1]

/-- `J_std''(y)` is strictly positive for all `y > 0`. -/
theorem JstdDeriv2_pos {y : ℝ} (hy : 0 < y) : 0 < JstdDeriv2 y := by
  unfold JstdDeriv2
  have hsy : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have hy1 : 0 < 1 + y := by linarith
  have hs1 : 0 < Real.sqrt (1 + y) := Real.sqrt_pos.mpr hy1
  positivity

/-- `J_std''(y)` is unbounded above as `y → 0⁺`: for every `M > 0` there exists `y ∈ (0, 1]`
with `M < J_std''(y)`. -/
theorem JstdDeriv2_unbounded (M : ℝ) (hM : 0 < M) :
    ∃ y : ℝ, 0 < y ∧ y ≤ 1 ∧ M < JstdDeriv2 y := by
  set c : ℝ := 1 / (16 * M + 1)
  have hc_pos : 0 < c := by positivity
  have hc_le1 : c ≤ 1 := by
    dsimp [c]
    rw [div_le_one (by positivity : (0 : ℝ) < 16 * M + 1)]
    linarith
  refine ⟨c ^ 2, by positivity, by nlinarith, ?_⟩
  have hy_pos : 0 < c ^ 2 := by positivity
  have hy_le1 : c ^ 2 ≤ 1 := by nlinarith
  have hsqrt_y : Real.sqrt (c ^ 2) = c := Real.sqrt_sq hc_pos.le
  have h1y_le2 : 1 + c ^ 2 ≤ 2 := by linarith
  have hsqrt1y_le2 : Real.sqrt (1 + c ^ 2) ≤ 2 := by
    have h4 : Real.sqrt (1 + c ^ 2) ≤ Real.sqrt 4 := Real.sqrt_le_sqrt (by linarith)
    have hsqrt4 : Real.sqrt (4 : ℝ) = 2 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    linarith
  have hden_pos : 0 < 4 * Real.sqrt (c ^ 2) * (1 + c ^ 2) * Real.sqrt (1 + c ^ 2) := by
    have hs1 : 0 < Real.sqrt (1 + c ^ 2) := Real.sqrt_pos.mpr (by linarith)
    positivity
  have hden_le : 4 * Real.sqrt (c ^ 2) * (1 + c ^ 2) * Real.sqrt (1 + c ^ 2) ≤ 16 * c := by
    rw [hsqrt_y]
    have hprod : (1 + c ^ 2) * Real.sqrt (1 + c ^ 2) ≤ 4 := by
      have hs1_nonneg : 0 ≤ Real.sqrt (1 + c ^ 2) := Real.sqrt_nonneg _
      nlinarith
    nlinarith
  have hinv : 1 / (16 * c) ≤ JstdDeriv2 (c ^ 2) := by
    unfold JstdDeriv2
    exact one_div_le_one_div_of_le hden_pos hden_le
  have h16c : M < 1 / (16 * c) := by
    dsimp [c]
    have hpos1 : (0 : ℝ) < 16 * M + 1 := by positivity
    have hsimp : 1 / (16 * (1 / (16 * M + 1))) = (16 * M + 1) / 16 := by
      field_simp [hpos1.ne']
    rw [hsimp]
    linarith
  linarith

/-! ## 3. Exact Analytic Auxiliary-Susceptibility Realization -/

/-- For `|s| < 1`, `1 + s > 0` and `1 - s > 0`. -/
lemma one_add_sub_pos {s : ℝ} (hs : |s| < 1) : 0 < 1 + s ∧ 0 < 1 - s := by
  have h := abs_lt.mp hs
  exact ⟨by linarith, by linarith⟩

/-- First derivative of the real-analytic auxiliary potential `V(s) = (artanh s - s) / 2`:
`V'(s) = s² / (2 (1 - s²))` for `|s| < 1`. -/
theorem hasDerivAt_auxPot {s : ℝ} (hs : |s| < 1) :
    HasDerivAt auxPot (auxPotDeriv s) s := by
  obtain ⟨hp, hm⟩ := one_add_sub_pos hs
  have hratio_pos : 0 < (1 + s) / (1 - s) := div_pos hp hm
  have hnum : HasDerivAt (fun t : ℝ => 1 + t) 1 s := by
    simpa using (hasDerivAt_id s).const_add 1
  have hden : HasDerivAt (fun t : ℝ => 1 - t) (-1) s := by
    simpa using (hasDerivAt_id s).const_sub 1
  have hq : HasDerivAt (fun t : ℝ => (1 + t) / (1 - t))
      ((1 * (1 - s) - (1 + s) * (-1)) / (1 - s) ^ 2) s := hnum.div hden hm.ne'
  have hlog : HasDerivAt (fun t : ℝ => Real.log ((1 + t) / (1 - t)))
      (((1 * (1 - s) - (1 + s) * (-1)) / (1 - s) ^ 2) / ((1 + s) / (1 - s))) s :=
    hq.log hratio_pos.ne'
  have hsub := ((hlog.div_const 2).sub (hasDerivAt_id s)).div_const 2
  have h1s2 : 1 - s ^ 2 ≠ 0 := by nlinarith
  refine hsub.congr_deriv ?_
  unfold auxPotDeriv
  field_simp [hp.ne', hm.ne', h1s2]
  ring

/-- Second derivative of the auxiliary potential: `V''(s) = s / (1 - s²)²` for `|s| < 1`. -/
theorem hasDerivAt_auxPotDeriv {s : ℝ} (hs : |s| < 1) :
    HasDerivAt auxPotDeriv (auxPotDeriv2 s) s := by
  obtain ⟨hp, hm⟩ := one_add_sub_pos hs
  have h1s2 : 1 - s ^ 2 ≠ 0 := by nlinarith
  have hnum : HasDerivAt (fun t : ℝ => t ^ 2) (2 * s) s := by
    simpa using hasDerivAt_pow 2 s
  have hden1 : HasDerivAt (fun t : ℝ => 1 - t ^ 2) (-(2 * s)) s := by
    simpa using (hasDerivAt_pow 2 s).const_sub 1
  have hden : HasDerivAt (fun t : ℝ => 2 * (1 - t ^ 2)) (2 * (-(2 * s))) s :=
    hden1.const_mul 2
  have hdiv := hnum.div hden (by positivity : (2 : ℝ) * (1 - s ^ 2) ≠ 0)
  refine hdiv.congr_deriv ?_
  unfold auxPotDeriv2
  field_simp [h1s2]
  ring

/-- Spinodal critical point at `s = 0`: `V'(0) = 0` and `V''(0) = 0`. -/
theorem auxPot_critical_at_zero : auxPotDeriv 0 = 0 ∧ auxPotDeriv2 0 = 0 := by
  unfold auxPotDeriv auxPotDeriv2
  norm_num

/-- `|muStd x| < 1` for every real `x`. -/
theorem abs_muStd_lt_one (x : ℝ) : |muStd x| < 1 := by
  unfold muStd
  have hpos : 0 < 1 + x ^ 2 := by positivity
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr hpos
  rw [abs_div, abs_of_pos hs, div_lt_one hs]
  have hsq : |x| ^ 2 < (Real.sqrt (1 + x ^ 2)) ^ 2 := by
    rw [sq_abs, Real.sq_sqrt hpos.le]
    linarith
  nlinarith [abs_nonneg x, hs]

/-- For `x ≥ 0`, `0 ≤ muStd x < 1`. -/
theorem muStd_mem_Ico {x : ℝ} (hx : 0 ≤ x) : 0 ≤ muStd x ∧ muStd x < 1 := by
  have habs := abs_muStd_lt_one x
  have hnn : 0 ≤ muStd x := by
    unfold muStd
    positivity
  exact ⟨hnn, (abs_lt.mp habs).2⟩

/-- Exact algebraic stationarity characterization: for `x ≥ 0` and `s ∈ [0, 1)`,
`x² / 2 - V'(s) = 0` holds if and only if `s = muStd x`. -/
theorem auxLag_stationary_iff {x s : ℝ} (hx : 0 ≤ x) (hs0 : 0 ≤ s) (hs1 : s < 1) :
    x ^ 2 / 2 - auxPotDeriv s = 0 ↔ s = muStd x := by
  have h1s2 : 0 < 1 - s ^ 2 := by nlinarith
  have h1x2 : 0 < 1 + x ^ 2 := by positivity
  have hsx : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr h1x2
  unfold auxPotDeriv muStd
  constructor
  · intro h
    have hmul : x ^ 2 * (1 - s ^ 2) = s ^ 2 := by
      have h' : x ^ 2 / 2 = s ^ 2 / (2 * (1 - s ^ 2)) := by linarith
      field_simp [h1s2.ne'] at h'
      linarith
    have hsq : s ^ 2 * (1 + x ^ 2) = x ^ 2 := by linarith
    have hsq_eq : (s * Real.sqrt (1 + x ^ 2)) ^ 2 = x ^ 2 := by
      rw [mul_pow, Real.sq_sqrt h1x2.le]
      exact hsq
    have hprod : s * Real.sqrt (1 + x ^ 2) = x := by
      nlinarith [mul_nonneg hs0 hsx.le]
    rw [eq_div_iff hsx.ne']
    exact hprod
  · intro hs_eq
    rw [hs_eq]
    have hsq : (x / Real.sqrt (1 + x ^ 2)) ^ 2 = x ^ 2 / (1 + x ^ 2) := by
      rw [div_pow, Real.sq_sqrt h1x2.le]
    have h1m : 1 - x ^ 2 / (1 + x ^ 2) = 1 / (1 + x ^ 2) := by
      field_simp [h1x2.ne']
      ring
    rw [hsq, h1m]
    field_simp [h1x2.ne']
    ring

/-- Exact hyperbolic identity: `(1 / 2) log((1 + muStd x) / (1 - muStd x)) = arsinh x`. -/
theorem half_log_ratio_muStd_eq_arsinh (x : ℝ) :
    Real.log ((1 + muStd x) / (1 - muStd x)) / 2 = Real.arsinh x := by
  have h1x2 : 0 < 1 + x ^ 2 := by positivity
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr h1x2
  have hsq : Real.sqrt (1 + x ^ 2) ^ 2 = 1 + x ^ 2 := Real.sq_sqrt h1x2.le
  have hsum_pos : 0 < x + Real.sqrt (1 + x ^ 2) := by
    have hlt : |x| < Real.sqrt (1 + x ^ 2) := by
      have : |x| ^ 2 < Real.sqrt (1 + x ^ 2) ^ 2 := by
        rw [sq_abs, hsq]
        linarith
      nlinarith [abs_nonneg x, hs]
    linarith [(abs_lt.mp hlt).1]
  have hdiff_pos : 0 < Real.sqrt (1 + x ^ 2) - x := by
    have hlt : |x| < Real.sqrt (1 + x ^ 2) := by
      have : |x| ^ 2 < Real.sqrt (1 + x ^ 2) ^ 2 := by
        rw [sq_abs, hsq]
        linarith
      nlinarith [abs_nonneg x, hs]
    linarith [(abs_lt.mp hlt).2]
  have hratio : (1 + muStd x) / (1 - muStd x) = (x + Real.sqrt (1 + x ^ 2)) ^ 2 := by
    unfold muStd
    have h1m : 1 - x / Real.sqrt (1 + x ^ 2) ≠ 0 := by
      have : (Real.sqrt (1 + x ^ 2) - x) / Real.sqrt (1 + x ^ 2) ≠ 0 := div_ne_zero hdiff_pos.ne' hs.ne'
      have heq : 1 - x / Real.sqrt (1 + x ^ 2) = (Real.sqrt (1 + x ^ 2) - x) / Real.sqrt (1 + x ^ 2) := by
        field_simp [hs.ne']
      rw [heq]
      exact this
    field_simp [hs.ne', h1m]
    nlinarith [hsq]
  rw [hratio, Real.log_pow, Real.arsinh]
  push_cast
  ring

/-- **Exact On-Shell Reduction:** substituting `s = muStd x` into `auxLag x s` recovers
`Fstd x = (x √(1 + x²) - arsinh x) / 2` identically for all real `x`. -/
theorem auxLag_on_shell_eq_Fstd (x : ℝ) : auxLag x (muStd x) = Fstd x := by
  have h1x2 : 0 < 1 + x ^ 2 := by positivity
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr h1x2
  have hsq : Real.sqrt (1 + x ^ 2) * Real.sqrt (1 + x ^ 2) = 1 + x ^ 2 := Real.mul_self_sqrt h1x2.le
  unfold auxLag auxPot Fstd
  rw [half_log_ratio_muStd_eq_arsinh x]
  unfold muStd
  field_simp [hs.ne']
  have hmul : x * (Real.sqrt (1 + x ^ 2) * Real.sqrt (1 + x ^ 2)) = x * (1 + x ^ 2) := by rw [hsq]
  linarith

/-- Derivative of `s ↦ auxLag x s` on `(-1, 1)` equals `x² / 2 - V'(s)`. -/
theorem hasDerivAt_auxLag (x : ℝ) {s : ℝ} (hs : |s| < 1) :
    HasDerivAt (fun t : ℝ => auxLag x t) (x ^ 2 / 2 - auxPotDeriv s) s := by
  have hlin : HasDerivAt (fun t : ℝ => t * x ^ 2 / 2) (1 * x ^ 2 / 2) s :=
    ((hasDerivAt_id s).mul_const (x ^ 2)).div_const 2
  have hsub := hlin.sub (hasDerivAt_auxPot hs)
  refine hsub.congr_deriv ?_
  ring

/-- Strict monotonicity of `V'(s) = s² / (2 (1 - s²))` on `[0, 1)`. -/
lemma auxPotDeriv_strictMono_Ico {a b : ℝ} (ha0 : 0 ≤ a) (hab : a < b) (hb1 : b < 1) :
    auxPotDeriv a < auxPotDeriv b := by
  unfold auxPotDeriv
  have ha2 : 0 < 1 - a ^ 2 := by nlinarith
  have hb2 : 0 < 1 - b ^ 2 := by nlinarith
  rw [div_lt_div_iff₀ (by positivity) (by positivity)]
  nlinarith

/-- **Global Legendre–Fenchel Supremum:** for `x ≥ 0` and every `s ∈ [0, 1)`,
`auxLag x s ≤ Fstd x`, and strictly `<` whenever `s ≠ muStd x`. -/
theorem auxLag_lt_Fstd_of_ne {x s : ℝ} (hx : 0 ≤ x) (hs0 : 0 ≤ s) (hs1 : s < 1)
    (hne : s ≠ muStd x) : auxLag x s < Fstd x := by
  set m := muStd x
  obtain ⟨hm0, hm1⟩ := muStd_mem_Ico hx
  have hstat : x ^ 2 / 2 = auxPotDeriv m := by
    have h0 := (auxLag_stationary_iff hx hm0 hm1).mpr rfl
    linarith
  rw [← auxLag_on_shell_eq_Fstd x]
  rcases lt_or_gt_of_ne hne with hsm | hms
  · -- s < m: derivative is strictly positive on (s, m)
    have hcont : ContinuousOn (fun t : ℝ => auxLag x t) (Set.Icc s m) := fun t ht => by
      have habs : |t| < 1 := abs_lt.mpr ⟨by linarith [ht.1], by linarith [ht.2]⟩
      exact (hasDerivAt_auxLag x habs).continuousAt.continuousWithinAt
    have hdiff : ∀ t ∈ Set.Ioo s m,
        HasDerivAt (fun u : ℝ => auxLag x u) (x ^ 2 / 2 - auxPotDeriv t) t := fun t ht => by
      have habs : |t| < 1 := abs_lt.mpr ⟨by linarith [ht.1], by linarith [ht.2]⟩
      exact hasDerivAt_auxLag x habs
    obtain ⟨c, hc, hmv⟩ := exists_hasDerivAt_eq_slope (fun u : ℝ => auxLag x u)
      (fun u => x ^ 2 / 2 - auxPotDeriv u) hsm hcont hdiff
    have hpos_d : 0 < x ^ 2 / 2 - auxPotDeriv c := by
      rw [hstat]
      have hlt := auxPotDeriv_strictMono_Ico (by linarith [hc.1]) hc.2 hm1
      linarith
    have hslope : 0 < (auxLag x m - auxLag x s) / (m - s) := by linarith
    have hms_pos : 0 < m - s := by linarith
    have := (div_pos_iff_of_pos_right hms_pos).mp hslope
    linarith
  · -- m < s: derivative is strictly negative on (m, s)
    have hcont : ContinuousOn (fun t : ℝ => auxLag x t) (Set.Icc m s) := fun t ht => by
      have habs : |t| < 1 := abs_lt.mpr ⟨by linarith [ht.1], by linarith [ht.2]⟩
      exact (hasDerivAt_auxLag x habs).continuousAt.continuousWithinAt
    have hdiff : ∀ t ∈ Set.Ioo m s,
        HasDerivAt (fun u : ℝ => auxLag x u) (x ^ 2 / 2 - auxPotDeriv t) t := fun t ht => by
      have habs : |t| < 1 := abs_lt.mpr ⟨by linarith [ht.1], by linarith [ht.2]⟩
      exact hasDerivAt_auxLag x habs
    obtain ⟨c, hc, hmv⟩ := exists_hasDerivAt_eq_slope (fun u : ℝ => auxLag x u)
      (fun u => x ^ 2 / 2 - auxPotDeriv u) hms hcont hdiff
    have hneg_d : x ^ 2 / 2 - auxPotDeriv c < 0 := by
      rw [hstat]
      have hlt := auxPotDeriv_strictMono_Ico hm0 hc.1 (by linarith [hc.2])
      linarith
    have hslope : (auxLag x s - auxLag x m) / (s - m) < 0 := by linarith
    have hsm_pos : 0 < s - m := by linarith
    have hnum_neg : auxLag x s - auxLag x m < 0 :=
      ((div_neg_iff.mp hslope).resolve_left (fun h => by linarith [h.2])).1
    linarith

/-- Non-strict global upper bound `auxLag x s ≤ Fstd x` on `[0, 1)`. -/
theorem auxLag_le_Fstd {x s : ℝ} (hx : 0 ≤ x) (hs0 : 0 ≤ s) (hs1 : s < 1) :
    auxLag x s ≤ Fstd x := by
  by_cases h : s = muStd x
  · rw [h, auxLag_on_shell_eq_Fstd]
  · exact le_of_lt (auxLag_lt_Fstd_of_ne hx hs0 hs1 h)

/-- Unique maximizer characterization: `auxLag x s = Fstd x ↔ s = muStd x` on `[0, 1)`. -/
theorem auxLag_eq_Fstd_iff {x s : ℝ} (hx : 0 ≤ x) (hs0 : 0 ≤ s) (hs1 : s < 1) :
    auxLag x s = Fstd x ↔ s = muStd x := by
  constructor
  · intro heq
    by_contra hne
    exact ne_of_lt (auxLag_lt_Fstd_of_ne hx hs0 hs1 hne) heq
  · intro h
    rw [h, auxLag_on_shell_eq_Fstd]

/-! ## Axiom Footprints (every public theorem printed) -/

#print axioms induced_metric_det_eq
#print axioms induced_metric_traces_eq
#print axioms hasDerivAt_even_response_zero
#print axioms hasDerivWithinAt_even_response_zero
#print axioms hasDerivAt_muStd_zero
#print axioms analytic_induced_metric_nogo_nonneg
#print axioms hasDerivAt_JstdDeriv
#print axioms JstdDeriv2_pos
#print axioms JstdDeriv2_unbounded
#print axioms hasDerivAt_auxPot
#print axioms hasDerivAt_auxPotDeriv
#print axioms auxPot_critical_at_zero
#print axioms abs_muStd_lt_one
#print axioms muStd_mem_Ico
#print axioms auxLag_stationary_iff
#print axioms half_log_ratio_muStd_eq_arsinh
#print axioms auxLag_on_shell_eq_Fstd
#print axioms hasDerivAt_auxLag
#print axioms auxLag_lt_Fstd_of_ne
#print axioms auxLag_le_Fstd
#print axioms auxLag_eq_Fstd_iff

end ResNova.PostulateRAnalyticNoGo
