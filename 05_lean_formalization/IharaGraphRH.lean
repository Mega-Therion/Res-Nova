import Mathlib

/-!
# Graph Riemann Hypothesis ⇔ Ramanujan (pole-by-pole core)

For a (q+1)-regular graph, the Ihara–Bass determinant formula (Bass 1992, cited,
*not* formalized here) gives

  ζ_G(u)⁻¹ = (1 - u²)^(|E|-|V|) · ∏_λ (1 - λ u + q u²),

the product over adjacency eigenvalues λ. The trivial eigenvalues ±(q+1) give the
trivial poles. The *graph RH* says every non-trivial pole lies on the circle
|u| = q^(-1/2). This is the analogue of Re s = 1/2 under u = q^(-s).

What is proved here, with no `sorry` and the standard axioms only:

* `pole_on_circle_iff`: for real λ and q > 0, every complex root of
  q u² - λ u + 1 lies on |u|² = 1/q **iff** λ² ≤ 4q.
* `graphRH_iff_ramanujan`: for any finite set of non-trivial eigenvalues, the
  graph RH holds iff every |λ| ≤ 2√q, which is the Ramanujan bound.
* Checks for the Petersen graph (non-trivial spectrum {1, -2}, q = 2) and the
  Heawood graph (non-trivial spectrum {±√2}, q = 2).

Scope: this is RH for graph zetas. It says nothing about the Riemann ζ.
-/

namespace ResNova.IharaGraphRH

open Complex

/-- Every complex root of `q u² - λ u + 1` has `‖u‖² = 1/q` iff `λ² ≤ 4q`. -/
theorem pole_on_circle_iff (q l : ℝ) (hq : 0 < q) :
    (∀ u : ℂ, (q : ℂ) * u ^ 2 - (l : ℂ) * u + 1 = 0 → Complex.normSq u = 1 / q) ↔
      l ^ 2 ≤ 4 * q := by
  constructor
  · intro h
    by_contra hlt
    push Not at hlt
    set D := l ^ 2 - 4 * q with hD
    have hDpos : 0 < D := by linarith
    set s := Real.sqrt D with hs
    have hs2 : s ^ 2 = D := Real.sq_sqrt hDpos.le
    have hspos : 0 < s := Real.sqrt_pos.mpr hDpos
    set u1 : ℝ := (l + s) / (2 * q)
    set u2 : ℝ := (l - s) / (2 * q)
    have hq0 : q ≠ 0 := hq.ne'
    have root : ∀ v : ℝ, q * v ^ 2 - l * v + 1 = 0 →
        (q : ℂ) * (v : ℂ) ^ 2 - (l : ℂ) * (v : ℂ) + 1 = 0 := by
      intro v hv
      have : ((q * v ^ 2 - l * v + 1 : ℝ) : ℂ) = 0 := by rw [hv]; simp
      push_cast at this
      exact this
    have r1 : q * u1 ^ 2 - l * u1 + 1 = 0 := by
      have e : q * ((l + s) / (2 * q)) ^ 2 - l * ((l + s) / (2 * q)) + 1
          = (s ^ 2 - D) / (4 * q) := by rw [hD]; field_simp; ring
      simp only [u1]; rw [e, hs2, sub_self, zero_div]
    have r2 : q * u2 ^ 2 - l * u2 + 1 = 0 := by
      have e : q * ((l - s) / (2 * q)) ^ 2 - l * ((l - s) / (2 * q)) + 1
          = (s ^ 2 - D) / (4 * q) := by rw [hD]; field_simp; ring
      simp only [u2]; rw [e, hs2, sub_self, zero_div]
    have n1 := h _ (root u1 r1)
    have n2 := h _ (root u2 r2)
    rw [Complex.normSq_ofReal] at n1 n2
    -- u1*u1 = 1/q = u2*u2 and u1*u2 = 1/q  ⇒  (u1-u2)^2 = 0 ⇒ s = 0
    have prod : u1 * u2 = 1 / q := by
      have e : (l + s) / (2 * q) * ((l - s) / (2 * q)) = (l ^ 2 - s ^ 2) / (4 * q ^ 2) := by
        field_simp; ring
      simp only [u1, u2]; rw [e, hs2, hD]; field_simp; ring
    have hdiff : (u1 - u2) ^ 2 = 0 := by linear_combination n1 + n2 - 2 * prod
    have : u1 - u2 = 0 := by simpa using hdiff
    have : s / q = 0 := by
      have e : u1 - u2 = s / q := by simp only [u1, u2]; field_simp; ring
      linarith [e]
    have : s = 0 := by
      rcases div_eq_zero_iff.mp this with h0 | h0
      · exact h0
      · exact absurd h0 hq0
    linarith
  · intro hle u hu
    have hre := congrArg Complex.re hu
    have him := congrArg Complex.im hu
    simp [pow_two, Complex.mul_re, Complex.mul_im] at hre him
    set x := u.re
    set y := u.im
    rw [Complex.normSq_apply]
    have hq0 : q ≠ 0 := hq.ne'
    by_cases hy : y = 0
    · -- real root: discriminant forces 2 q x = l
      have hre' : q * (x * x) - l * x + 1 = 0 := by
        rw [hy] at hre; linarith [hre]
      have hsq : (2 * q * x - l) ^ 2 = l ^ 2 - 4 * q := by linear_combination 4 * q * hre'
      have h0 : (2 * q * x - l) ^ 2 = 0 := by
        have := sq_nonneg (2 * q * x - l); rw [hsq] at this ⊢; linarith
      have hx : 2 * q * x = l := by
        have := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp h0; linarith
      show x * x + y * y = 1 / q
      rw [eq_div_iff hq0]
      rw [hy] at hre ⊢
      linear_combination (-1) * hre + x * hx
    · -- complex pair: imaginary part forces x = l/(2q)
      have hx : 2 * q * x = l := by
        have : y * (2 * q * x - l) = 0 := by linarith [him]
        rcases mul_eq_zero.mp this with h0 | h0
        · exact absurd h0 hy
        · linarith
      show x * x + y * y = 1 / q
      rw [eq_div_iff hq0]
      linear_combination (-1) * hre + x * hx

/-- Graph RH for a finite set of non-trivial eigenvalues of a (q+1)-regular graph. -/
def GraphRH (q : ℝ) (S : Finset ℝ) : Prop :=
  ∀ l ∈ S, ∀ u : ℂ, (q : ℂ) * u ^ 2 - (l : ℂ) * u + 1 = 0 → Complex.normSq u = 1 / q

/-- Ramanujan bound on the non-trivial spectrum. -/
def Ramanujan (q : ℝ) (S : Finset ℝ) : Prop := ∀ l ∈ S, |l| ≤ 2 * Real.sqrt q

lemma abs_le_two_sqrt_iff (q l : ℝ) (hq : 0 < q) :
    |l| ≤ 2 * Real.sqrt q ↔ l ^ 2 ≤ 4 * q := by
  have h4 : 2 * Real.sqrt q = Real.sqrt (4 * q) := by
    rw [Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 4)]
    norm_num
  rw [h4, ← Real.sqrt_sq_eq_abs]
  exact Real.sqrt_le_sqrt_iff (by positivity)

/-- **Graph RH ⇔ Ramanujan** (given Ihara–Bass): pole-by-pole. -/
theorem graphRH_iff_ramanujan (q : ℝ) (hq : 0 < q) (S : Finset ℝ) :
    GraphRH q S ↔ Ramanujan q S := by
  unfold GraphRH Ramanujan
  refine forall_congr' fun l => imp_congr_right fun _ => ?_
  rw [pole_on_circle_iff q l hq, abs_le_two_sqrt_iff q l hq]

/-- Petersen graph: q = 2, non-trivial spectrum {1, -2}. Graph RH holds. -/
theorem petersen_graphRH : GraphRH 2 {1, -2} := by
  rw [graphRH_iff_ramanujan 2 (by norm_num)]
  intro l hl
  rw [abs_le_two_sqrt_iff 2 l (by norm_num)]
  simp only [Finset.mem_insert, Finset.mem_singleton] at hl
  rcases hl with rfl | rfl <;> norm_num

/-- Heawood graph: q = 2, non-trivial spectrum {√2, -√2}. Graph RH holds. -/
theorem heawood_graphRH : GraphRH 2 {Real.sqrt 2, -Real.sqrt 2} := by
  rw [graphRH_iff_ramanujan 2 (by norm_num)]
  intro l hl
  rw [abs_le_two_sqrt_iff 2 l (by norm_num)]
  simp only [Finset.mem_insert, Finset.mem_singleton] at hl
  rcases hl with rfl | rfl <;> simp [Real.sq_sqrt]

/-- A non-Ramanujan eigenvalue (λ = 2.9 > 2√2) breaks the graph RH. -/
theorem nonRamanujan_breaks : ¬ GraphRH 2 {29 / 10} := by
  rw [graphRH_iff_ramanujan 2 (by norm_num)]
  intro h
  have := (abs_le_two_sqrt_iff 2 (29/10) (by norm_num)).mp (h _ (by simp))
  norm_num at this

end ResNova.IharaGraphRH
