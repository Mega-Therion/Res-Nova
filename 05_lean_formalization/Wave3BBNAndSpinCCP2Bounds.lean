/-
  Wave3BBNAndSpinCCP2Bounds.lean

  Formalizes machine-checked structural results [P] from the 2026-11-17
  Advanced Modus dialectic and Safa/Muse Spin^c CP^2 Gate 2 audit:
  (Res-Nova Wave 3 opens `BLK-1446` #1, `BLK-1450`, `BLK-1459`, `BLK-1461` §8 & §9 #2)

  1. AeST BBN × Caustic-Folding Window (`GCosmoRatio`, `jtot_bbn_5pct_impossible`,
     `jtot_bbn_10pct_KB_ceiling`):
     In pure AeST (`TARGET_D7`), Friedmann uses `G_cosmo = G_tilde = (1 - K_B/2) G_hat`
     while local Cavendish gravity uses `G_N = (1 + 1/lam) G_hat`, so
       `G_cosmo / G_N = lam * (2 - K_B) / (2 * (1 + lam)) < lam / (1 + lam)`
     for `K_B > 0`. Under a 5% BBN bound `G_cosmo / G_N >= 19/20`, `lam >= 19` is forced,
     strictly excluding `AeSTTotalScalarCorrespondence`'s non-folding threshold
     `32 * (lam / (1 + lam))^2 < 27` (`lam < 11.28`). Under a 10% BBN bound (`>= 9/10`),
     non-folding forces `K_B < 41/1000` (`< 0.041`).

  2. `E8 × CP^2` `Spin^c` Generation-Index Classification (`twiceInd_triplet_identity`,
     `no_zero_sum_twist_below_nine`, `nontrivial_zero_sum_twist_strictly_above_nine`,
     `symmetric_compensating_bundle_unique`, `singlet_and_sterile_index_counts`):
     Over `ℤ`, `twiceInd Q := (Q+1)*(Q+2) = 2 * ind(D_Q^+)` satisfies duality `Q ↔ -3-Q`,
     non-negativity, the exact triplet sum identity
       `∑_i twiceInd(1 + q_i) = 18 + 5*(q₁+q₂+q₃) + (q₁²+q₂²+q₃²)`,
     a strict lower bound `≥ 9` (`≥ 10` when non-trivial) for ANY zero-sum `SU(3)` twist,
     and uniqueness `q ∈ {-1, -4}` for symmetric compensating bundles yielding `∑ ind = 3`.

  3. Safa `BLK-1450` Gate 2 `E8 → E6 × SU(3)_f → SO(10) × U(1)_ψ` Charge-Locking Proofs
     (extended per `BLK-1477` precision & Gate 2 audit):
     - `spinC_chiral_excess_linear`: `ind(Q₀ + x) - ind(Q₀ - x) = (2*Q₀ + 3)*x` is strictly
       linear in any `U(1)` gauge charge `x`.
     - `e8_248_chiral_excess_formula`, `su5_248_chiral_10_excess_formula`, and
       `e8_248_chiral_excess_zero_iff_traceless`: Across the full self-conjugate `248`
       (`(16,3)_{+1} ⊕ (16,1)_{-3}`, and `SU(5)` `10`-plets), total net chiral index equals
       `2*(2*Q₀ + 3)*(q₁ + q₂ + q₃)` (in `twiceInd`), vanishing **if and only if** the
       `SU(3)_f` twist is traceless (`q₁ + q₂ + q₃ = 0`). Under traceless twists, the
       `(78,1)`-derived `(16,1)_{-3}` cancels the `(27,3)` contribution identically; obtaining
       nonzero net generations then requires decoupling/projecting `(78,1)`, breaking `248`
       self-conjugacy, or adding a traceful external `U(1)` twist (`q₁ + q₂ + q₃ ≠ 0`).
     - `matter_27_chiral_excess_formula`, `matter_27_three_gen_forces_Q0_and_kpsi`,
       `matter_27_three_gen_locus_iff`, and `matter_27_three_gen_retains_exotic_10_values`:
       Restricted to `(27,3)` with traceless `SU(3)_f`, net `±3` chiral `16` generations
       holds iff `(Q₀, k_ψ, Q₀ - 2 k_ψ) ∈ {(-2,-1,0), (-2,1,-4), (-1,-1,1), (-1,1,-3)}`,
       which unconditionally yields `twiceInd (Q₀ - 2 k_ψ) ∈ {2, 6}` (`ind ≥ 1` per color,
       i.e. `≥ 3` colored light `10`-plets in the traceless symmetric `(27,3)` branch).
     - **Traceful & Asymmetric `SU(3)_f` Extension (`BLK-1477` `Q_10` vs `248` check):**
       `traceless_distinct_weights_retain_exotic_10` proves NO traceless `SU(3)_f` twist
       (even with distinct weights `q₁, q₂, q₃`) cancels all three `(10,3)_{-2}` colors at
       `Q₀ ∈ {-1,-2}, k_ψ ∈ {1,-1}` (`∑ twiceInd ≥ 6`). `traceful_Gate2_locus_cancel_10_forces_violation`
       and `traceful_27_three_gen_and_10_cancel_iff` prove that allowing traceful `q₁+q₂+q₃ ≠ 0`
       at `Q₀ ∈ {-1,-2}, k_ψ ∈ {1,-1}` can cancel all three `(10,3)` colors ONLY by forcing
       `|tr| ≥ 3`, `|net_16| ≥ 6` (breaking `±3`), and `|net_248| ≥ 3`; over all `ℤ⁵`,
       simultaneous `(27,3)` `net = ±3` and full `(10,3)` cancellation occurs iff `k_ψ = 0` and
       `(Q₀, q₁, q₂, q₃) ∈ {(-2, 1, 1, 1), (-1, -1, -1, -1)}` (`tr = ±3`, `net_248 = -3 ≠ 0`).
       Moreover `exotic_10_net_chiral_excess_never_zero_when_three_gen` shows the net chiral
       `(10,3)_{-2}` excess never vanishes when `(27,3)` has `net_16 = ±3`.
     - **Single-Multiplet Dolan `Q = 1` vs Gate 2 `Q₀` (`L1/L2` Boundary `[P]`):**
       `twiceInd_shift_expansion`, `single_multiplet_three_gen_iff`,
       `canonical_Q0_zero_triplet_chiral_excess_no_three_gen`, and
       `gate2_locus_disjoint_from_single_multiplet_Q1` prove that `BLK-1450`'s `Q = 1`
       (`ind(1) = 3`) is a single-operator twist (`twiceInd Q = 6 ↔ Q ∈ {1,-4}`, giving `9`
       families in the unshifted `Q₀ = 0` triplet chiral-excess sum), whereas Gate 2's 4-point
       locus forces `Q₀ ∈ {-1,-2}` and individual charges `Q₀ ± k_ψ ∈ {-3,-2,-1,0}`
       (`ind ∈ {0,1}`, disjoint from `{1,-4}`), summing `3 × (±1) = ±3` across `SU(3)_f` colors.

  Epistemic Scope: Pure algebraic / arithmetic invariants over `ℝ` and `ℤ`; BBN compatibility rests
  on the imported `TARGET_D7` `G_cosmo` formula and `AeSTTotalScalarCorrespondence` `11.2788` bound;
  `Spin^c` index values import the Atiyah–Singer polynomial formula `(Q+1)(Q+2)/2` `[ext]`.
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

namespace ResNova.Wave3BBNAndSpinCCP2Bounds

section AeSTBBNWindow

/-- Ratio of cosmological background gravitational constant `G_cosmo = G_tilde = (1 - K_B/2) G_hat`
to local Newtonian constant `G_N = (1 + 1/λ_s) G_hat` in pure AeST (`TARGET_D7` §§1–2). -/
noncomputable def GCosmoRatio (lam KB : ℝ) : ℝ :=
  lam * (2 - KB) / (2 * (1 + lam))

/-- For any positive tracking parameter `λ_s > 0` and positive aether kinetic constant `K_B > 0`,
the cosmological-to-Newtonian gravity ratio is strictly bounded by `λ_s / (1 + λ_s)`. -/
theorem GCosmoRatio_lt_eta {lam KB : ℝ} (hlam : 0 < lam) (hKB : 0 < KB) :
    GCosmoRatio lam KB < lam / (1 + lam) := by
  unfold GCosmoRatio
  have hden1 : 0 < 1 + lam := by linarith
  have hden2 : 0 < 2 * (1 + lam) := by linarith
  rw [div_lt_div_iff₀ hden2 hden1]
  have hpos : 0 < lam * KB * (1 + lam) := by positivity
  linarith

/-- Non-strict version when `0 ≤ K_B`. -/
theorem GCosmoRatio_le_eta {lam KB : ℝ} (hlam : 0 < lam) (hKB : 0 ≤ KB) :
    GCosmoRatio lam KB ≤ lam / (1 + lam) := by
  unfold GCosmoRatio
  have hden1 : 0 < 1 + lam := by linarith
  have hden2 : 0 < 2 * (1 + lam) := by linarith
  rw [div_le_div_iff₀ hden2 hden1]
  have hnn : 0 ≤ lam * KB * (1 + lam) := by positivity
  linarith

/-- Any BBN lower bound `1 - δ ≤ G_cosmo / G_N` with `0 ≤ K_B` and `0 < δ < 1` forces
`λ_s ≥ (1 - δ) / δ`. -/
theorem bbn_lower_bound_forces_lambda_s {lam KB δ : ℝ}
    (hlam : 0 < lam) (hKB : 0 ≤ KB) (hδ0 : 0 < δ) (_hδ1 : δ < 1)
    (hBBN : 1 - δ ≤ GCosmoRatio lam KB) :
    (1 - δ) / δ ≤ lam := by
  have h1 : 1 - δ ≤ lam / (1 + lam) := le_trans hBBN (GCosmoRatio_le_eta hlam hKB)
  have hden : 0 < 1 + lam := by linarith
  rw [le_div_iff₀ hden] at h1
  rw [div_le_iff₀ hδ0]
  linarith

/-- Exact cleared polynomial equivalence for `AeSTTotalScalarCorrespondence`'s non-folding
condition `32 * (λ_s / (1 + λ_s))^2 < 27`: equivalent to `5 λ_s^2 - 54 λ_s - 27 < 0`. -/
theorem jtot_nonfolding_iff_poly {lam : ℝ} (hlam : 0 < lam) :
    32 * (lam / (1 + lam)) ^ 2 < 27 ↔ 5 * lam ^ 2 - 54 * lam - 27 < 0 := by
  have hden : 0 < (1 + lam) ^ 2 := by positivity
  have hdiv : 32 * (lam / (1 + lam)) ^ 2 = (32 * lam ^ 2) / (1 + lam) ^ 2 := by
    rw [div_pow]; ring
  rw [hdiv, div_lt_iff₀ hden]
  constructor <;> intro h <;> linarith

/-- Explicit rational upper bound: any `λ_s > 0` satisfying `32 (λ_s / (1 + λ_s))^2 ≤ 27`
is strictly below `11.3 = 113 / 10` (`(27 + 12√6)/5 ≈ 11.2788`). -/
theorem jtot_nonfolding_lt_eleven_point_three {lam : ℝ} (hlam : 0 < lam)
    (hJ : 32 * (lam / (1 + lam)) ^ 2 ≤ 27) :
    lam < 113 / 10 := by
  have hden : 0 < (1 + lam) ^ 2 := by positivity
  have hdiv : 32 * (lam / (1 + lam)) ^ 2 = (32 * lam ^ 2) / (1 + lam) ^ 2 := by
    rw [div_pow]; ring
  rw [hdiv, div_le_iff₀ hden] at hJ
  have hpoly : 5 * lam ^ 2 - 54 * lam - 27 ≤ 0 := by linarith
  by_contra hge
  push Not at hge
  have hbad : 0 < 5 * lam ^ 2 - 54 * lam - 27 := by nlinarith
  linarith

/-- **No-Go Theorem (`[P]`):** Under a 5% BBN gravity bound (`G_cosmo / G_N ≥ 19/20`) and
non-negative aether kinetic coupling (`K_B ≥ 0`), NO tracking constant `λ_s > 0` lies inside
`AeSTTotalScalarCorrespondence`'s non-folding threshold `32 (λ_s/(1+λ_s))^2 < 27`. -/
theorem jtot_bbn_5pct_impossible {lam KB : ℝ}
    (hlam : 0 < lam) (hKB : 0 ≤ KB)
    (hBBN : 19 / 20 ≤ GCosmoRatio lam KB)
    (hJ : 32 * (lam / (1 + lam)) ^ 2 < 27) :
    False := by
  have hlam19 : (19 : ℝ) ≤ lam := by
    have hb := bbn_lower_bound_forces_lambda_s hlam hKB (by norm_num : (0 : ℝ) < 1 / 20)
      (by norm_num : (1 / 20 : ℝ) < 1) (by linarith)
    linarith
  have hlt := jtot_nonfolding_lt_eleven_point_three hlam hJ.le
  linarith

/-- Under a relaxed 10% BBN bound (`G_cosmo / G_N ≥ 9/10`), staying inside `J_tot`'s non-folding
domain (`λ_s < 113/10`) strictly forces `K_B < 41 / 1000` (`K_B < 0.041`, sharp max `≈ 0.0404`). -/
theorem jtot_bbn_10pct_KB_ceiling {lam KB : ℝ}
    (hlam : 0 < lam)
    (hBBN : 9 / 10 ≤ GCosmoRatio lam KB)
    (hJ : 32 * (lam / (1 + lam)) ^ 2 ≤ 27) :
    KB < 41 / 1000 := by
  have hlt : lam < 113 / 10 := jtot_nonfolding_lt_eleven_point_three hlam hJ
  unfold GCosmoRatio at hBBN
  have hden : 0 < 2 * (1 + lam) := by linarith
  rw [le_div_iff₀ hden] at hBBN
  have hmul : KB * lam ≤ (1 / 5 : ℝ) * lam - 9 / 5 := by linarith
  nlinarith

end AeSTBBNWindow

section SpinCCP2Index

/-- Twice the Atiyah–Singer `Spin^c CP^2` index `2 * ind(D_Q^+) = (Q + 1)(Q + 2)` over `ℤ`. -/
def twiceInd (Q : ℤ) : ℤ := (Q + 1) * (Q + 2)

/-- Twice the index is non-negative for every integer charge `Q : ℤ`. -/
theorem twiceInd_nonneg (Q : ℤ) : 0 ≤ twiceInd Q := by
  unfold twiceInd
  have h : Q + 1 ≤ -1 ∨ 0 ≤ Q + 1 := by omega
  rcases h with hneg | hpos
  · have : Q + 2 ≤ 0 := by omega
    exact mul_nonneg_of_nonpos_of_nonpos (by omega) this
  · exact mul_nonneg hpos (by omega)

/-- Exact charge conjugation / Serre duality symmetry `ind(-3 - Q) = ind(Q)` over `ℤ`. -/
theorem twiceInd_duality (Q : ℤ) : twiceInd (-3 - Q) = twiceInd Q := by
  unfold twiceInd
  ring

/-- Exact quadratic decomposition for ANY rank-3 triplet twist `(1 + q₁, 1 + q₂, 1 + q₃)` on `CP^2`:
`∑ twiceInd(1 + q_i) = 18 + 5 * (q₁ + q₂ + q₃) + (q₁² + q₂² + q₃²)`. -/
theorem twiceInd_triplet_identity (q₁ q₂ q₃ : ℤ) :
    twiceInd (1 + q₁) + twiceInd (1 + q₂) + twiceInd (1 + q₃) =
      18 + 5 * (q₁ + q₂ + q₃) + (q₁ ^ 2 + q₂ ^ 2 + q₃ ^ 2) := by
  unfold twiceInd
  ring

/-- **Zero-Sum `SU(3)` Twist No-Go (`[P]`):** Any traceless `SU(3)` twist `(q₁ + q₂ + q₃ = 0)` on the
`(3, 16)(1)` triplet gives at least `9` zero modes (`twiceInd ≥ 18`), and strictly `≥ 10` (`twiceInd ≥ 20`)
whenever any `q_i ≠ 0`. -/
theorem no_zero_sum_twist_below_nine {q₁ q₂ q₃ : ℤ} (hsum : q₁ + q₂ + q₃ = 0) :
    18 ≤ twiceInd (1 + q₁) + twiceInd (1 + q₂) + twiceInd (1 + q₃) := by
  rw [twiceInd_triplet_identity q₁ q₂ q₃, hsum]
  nlinarith [sq_nonneg q₁, sq_nonneg q₂, sq_nonneg q₃]

theorem nontrivial_zero_sum_twist_strictly_above_nine {q₁ q₂ q₃ : ℤ} (hsum : q₁ + q₂ + q₃ = 0)
    (hne : q₁ ≠ 0 ∨ q₂ ≠ 0 ∨ q₃ ≠ 0) :
    20 ≤ twiceInd (1 + q₁) + twiceInd (1 + q₂) + twiceInd (1 + q₃) := by
  have int_sq_ge_one : ∀ {x : ℤ}, x ≠ 0 → 1 ≤ x ^ 2 := by
    intro x hx
    have h : x ≤ -1 ∨ 1 ≤ x := by omega
    rcases h with hle | hge <;> nlinarith
  rw [twiceInd_triplet_identity q₁ q₂ q₃, hsum]
  have hq12 : q₁ ≠ 0 ∨ q₂ ≠ 0 := by
    rcases hne with h | h | h
    · exact Or.inl h
    · exact Or.inr h
    · by_cases h1 : q₁ = 0 <;> by_cases h2 : q₂ = 0
      · exfalso; apply h; omega
      · exact Or.inr h2
      · exact Or.inl h1
      · exact Or.inl h1
  have _hsum_pos : 1 ≤ q₁ ^ 2 + q₂ ^ 2 := by
    rcases hq12 with h1 | h2
    · have := int_sq_ge_one h1; nlinarith [sq_nonneg q₂]
    · have := int_sq_ge_one h2; nlinarith [sq_nonneg q₁]
  have h_even_form : q₁ ^ 2 + q₂ ^ 2 + q₃ ^ 2 = 2 * (q₁ ^ 2 + q₁ * q₂ + q₂ ^ 2) := by
    have hq3 : q₃ = -(q₁ + q₂) := by omega
    rw [hq3]
    ring
  have h_quad_pos : 1 ≤ q₁ ^ 2 + q₁ * q₂ + q₂ ^ 2 := by
    have h2 : 1 ≤ 2 * (q₁ ^ 2 + q₁ * q₂ + q₂ ^ 2) := by
      have : 2 * (q₁ ^ 2 + q₁ * q₂ + q₂ ^ 2) = q₁ ^ 2 + q₂ ^ 2 + (q₁ + q₂) ^ 2 := by ring
      nlinarith [sq_nonneg (q₁ + q₂)]
    omega
  omega

/-- **Unique Symmetric Compensating Bundle (`[P]`):** Any uniform shift `(1 + q, 1 + q, 1 + q)`
yielding total index `3` (`twiceInd = 6`) must satisfy `q = -1` (Muse's `(B2)` `O(-1)^⊕3`) or its
charge conjugate `q = -4` (`O(-4)^⊕3`). -/
theorem symmetric_compensating_bundle_unique {q : ℤ}
    (h : twiceInd (1 + q) + twiceInd (1 + q) + twiceInd (1 + q) = 6) :
    q = -1 ∨ q = -4 := by
  unfold twiceInd at h
  have h1 : (q + 2) * (q + 3) = 2 := by linarith
  have hsplit : q ≤ -5 ∨ q = -4 ∨ q = -3 ∨ q = -2 ∨ q = -1 ∨ 0 ≤ q := by omega
  rcases hsplit with h5 | rfl | rfl | rfl | rfl | h0
  · exfalso; nlinarith
  · exact Or.inr rfl
  · exfalso; omega
  · exfalso; omega
  · exact Or.inl rfl
  · exfalso; nlinarith

/-- Explicit `248` E8 component values verifying `10` surplus modes for `(1, 16)(3)` and `15` for `(3, 1)(4)`. -/
theorem singlet_and_sterile_index_counts :
    twiceInd 3 = 20 ∧ twiceInd (-3) = 2 ∧ twiceInd 4 = 30 ∧ twiceInd (-2) = 0 := by
  unfold twiceInd
  norm_num

end SpinCCP2Index

section E8SpinCChargeLocking

/-- **Exact Chiral Excess Linearity (`[P]`):** Under any canonical `Spin^c` base shift `Q₀ : ℤ` and
gauge `U(1)` charge `x : ℤ` (where conjugates carry `-x`), twice the net chiral excess satisfies
`2 (ind(Q₀ + x) - ind(Q₀ - x)) = 2 (2 Q₀ + 3) x`. The quadratic `x²` anomaly cancels identically. -/
theorem spinC_chiral_excess_linear (Q0 x : ℤ) :
    twiceInd (Q0 + x) - twiceInd (Q0 - x) = 2 * (2 * Q0 + 3) * x := by
  unfold twiceInd
  ring

/-- **Full `E8` (`248`) Self-Conjugacy Chiral Trace No-Go (`[P]` — Safa `BLK-1450` Gate 2):**
Summing the net chiral `16` excess across ALL `16`-plets in `248` (`(16, 3)_{+1}` and `(16, 1)_{-3}`)
under **any** `Spin^c` base shift `Q₀`, **any** `U(1)_ψ` flux `k_ψ`, and **any** traceless `SU(3)_f`
flux `(q₁ + q₂ + q₃ = 0)` yields **strictly zero net chiral families (`0`)** identically.
Obtaining 3 net chiral generations from `E8` on `CP²` therefore requires decoupling/projecting `(78, 1)`
or breaking `248` self-conjugacy. -/
theorem e8_248_total_chiral_excess_zero (Q0 k_psi q1 q2 q3 : ℤ) (hsum : q1 + q2 + q3 = 0) :
    (twiceInd (Q0 + k_psi + q1) - twiceInd (Q0 - k_psi - q1)) +
    (twiceInd (Q0 + k_psi + q2) - twiceInd (Q0 - k_psi - q2)) +
    (twiceInd (Q0 + k_psi + q3) - twiceInd (Q0 - k_psi - q3)) +
    (twiceInd (Q0 - 3 * k_psi) - twiceInd (Q0 + 3 * k_psi)) = 0 := by
  rw [show Q0 + k_psi + q1 = Q0 + (k_psi + q1) by ring,
      show Q0 - k_psi - q1 = Q0 - (k_psi + q1) by ring,
      show Q0 + k_psi + q2 = Q0 + (k_psi + q2) by ring,
      show Q0 - k_psi - q2 = Q0 - (k_psi + q2) by ring,
      show Q0 + k_psi + q3 = Q0 + (k_psi + q3) by ring,
      show Q0 - k_psi - q3 = Q0 - (k_psi + q3) by ring,
      show Q0 - 3 * k_psi = Q0 + (-3 * k_psi) by ring,
      show Q0 + 3 * k_psi = Q0 - (-3 * k_psi) by ring]
  simp only [spinC_chiral_excess_linear]
  calc
    2 * (2 * Q0 + 3) * (k_psi + q1) +
        2 * (2 * Q0 + 3) * (k_psi + q2) +
        2 * (2 * Q0 + 3) * (k_psi + q3) +
        2 * (2 * Q0 + 3) * (-3 * k_psi)
        = 2 * (2 * Q0 + 3) * (q1 + q2 + q3) := by ring
    _ = 0 := by rw [hsum, mul_zero]

/-- **`SU(5) × U(1)_χ × U(1)_ψ × SU(3)_f` Extension (`[P]`):** Even breaking `SO(10) → SU(5) × U(1)_χ`
across all `10`-plets inside `248` (`(10, 3)_{-1,+1}`, `(10, 1)_{-1,-3}`, `(10, 1)_{+4,0}`), total
net chiral `10` excess over `248` remains strictly `0` identically for all fluxes. -/
theorem su5_248_chiral_10_excess_zero (Q0 k_psi k_chi q1 q2 q3 : ℤ) (hsum : q1 + q2 + q3 = 0) :
    (twiceInd (Q0 + (k_psi - k_chi + q1)) - twiceInd (Q0 - (k_psi - k_chi + q1))) +
    (twiceInd (Q0 + (k_psi - k_chi + q2)) - twiceInd (Q0 - (k_psi - k_chi + q2))) +
    (twiceInd (Q0 + (k_psi - k_chi + q3)) - twiceInd (Q0 - (k_psi - k_chi + q3))) +
    (twiceInd (Q0 + (-3 * k_psi - k_chi)) - twiceInd (Q0 - (-3 * k_psi - k_chi))) +
    (twiceInd (Q0 + 4 * k_chi) - twiceInd (Q0 - 4 * k_chi)) = 0 := by
  simp only [spinC_chiral_excess_linear]
  calc
    2 * (2 * Q0 + 3) * (k_psi - k_chi + q1) +
        2 * (2 * Q0 + 3) * (k_psi - k_chi + q2) +
        2 * (2 * Q0 + 3) * (k_psi - k_chi + q3) +
        2 * (2 * Q0 + 3) * (-3 * k_psi - k_chi) +
        2 * (2 * Q0 + 3) * (4 * k_chi)
        = 2 * (2 * Q0 + 3) * (q1 + q2 + q3) := by ring
    _ = 0 := by rw [hsum, mul_zero]

/-- **Matter-Sector `(27, 3)` Exact Chiral Excess (`[P]`):** When `(78, 1)` decouples and only
`(27, 3) ⊕ (27̄, 3̄)` enters, twice the net chiral `16` excess equals `6 * (2 * Q0 + 3) * k_psi`
independently of any traceless `SU(3)_f` twist `(q₁ + q₂ + q₃ = 0)`. -/
theorem matter_27_chiral_excess_formula (Q0 k_psi q1 q2 q3 : ℤ) (hsum : q1 + q2 + q3 = 0) :
    (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
    (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
    (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) =
      6 * (2 * Q0 + 3) * k_psi := by
  simp only [spinC_chiral_excess_linear]
  calc
    2 * (2 * Q0 + 3) * (k_psi + q1) +
        2 * (2 * Q0 + 3) * (k_psi + q2) +
        2 * (2 * Q0 + 3) * (k_psi + q3)
        = 2 * (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) := by ring
    _ = 6 * (2 * Q0 + 3) * k_psi := by rw [hsum]; ring

/-- **Matter-Sector 3-Generation Charge Lock (`[P]`):** Obtaining exact `±3` net chiral `16` families
from `(27, 3)` under `Spin^c × U(1)_ψ × SU(3)_f` forces `(Q₀ = -1 ∨ Q₀ = -2)` AND `(k_ψ = 1 ∨ k_ψ = -1)`! -/
theorem matter_27_three_gen_forces_Q0_and_kpsi {Q0 k_psi q1 q2 q3 : ℤ}
    (hsum : q1 + q2 + q3 = 0)
    (hnet :
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = 6 ∨
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = -6) :
    (Q0 = -1 ∨ Q0 = -2) ∧ (k_psi = 1 ∨ k_psi = -1) := by
  rw [matter_27_chiral_excess_formula Q0 k_psi q1 q2 q3 hsum] at hnet
  have hprod : (2 * Q0 + 3) * k_psi = 1 ∨ (2 * Q0 + 3) * k_psi = -1 := by
    rcases hnet with h | h
    · left; linarith
    · right; linarith
  have hodd : 2 * Q0 + 3 ≤ -1 ∨ 1 ≤ 2 * Q0 + 3 := by omega
  have hsplit : k_psi ≤ -2 ∨ k_psi = -1 ∨ k_psi = 0 ∨ k_psi = 1 ∨ 2 ≤ k_psi := by omega
  rcases hsplit with hle | rfl | rfl | rfl | hge
  · exfalso
    rcases hprod with hp | hp <;> rcases hodd with hlo | hhi <;> nlinarith
  · refine ⟨by rcases hprod with hp | hp <;> omega, Or.inr rfl⟩
  · exfalso
    rcases hprod with hp | hp <;> nlinarith
  · refine ⟨by rcases hprod with hp | hp <;> omega, Or.inl rfl⟩
  · exfalso
    rcases hprod with hp | hp <;> rcases hodd with hlo | hhi <;> nlinarith

/-- **Exotic `(10, 3)_{-2}` Persistence in the Symmetric `net = ±3` Locus (`[P]`):**
For every solution `(Q₀ ∈ {-1, -2}) ∧ (k_ψ ∈ {1, -1})`, the symmetric `(10, 3)_{-2}` exotic
multiplet carries effective charge `Q_10 = Q₀ - 2 k_ψ ∈ {-4, -3, 0, 1}`, strictly avoiding the
zero-mode-free window `{-1, -2}` (`twiceInd (Q₀ - 2 k_ψ) ≠ 0`, yielding `≥ 3` light `10`-plets). -/
theorem matter_27_unique_solution_retains_symmetric_exotic_10 {Q0 k_psi : ℤ}
    (hQ : Q0 = -1 ∨ Q0 = -2) (hk : k_psi = 1 ∨ k_psi = -1) :
    twiceInd (Q0 - 2 * k_psi) ≠ 0 := by
  unfold twiceInd
  rcases hQ with rfl | rfl <;> rcases hk with rfl | rfl <;> norm_num

/-- **Exact 4-Solution Locus (`[P]` — `BLK-1477` Promotion):** Under any traceless `SU(3)_f` twist
`(q₁ + q₂ + q₃ = 0)`, `(27, 3)` yields exact `±3` net chiral `16` generations (`twiceInd` sum `= ±6`)
**if and only if** `(Q₀, k_ψ, Q₀ - 2 k_ψ)` belongs to `{(-2, -1, 0), (-2, 1, -4), (-1, -1, 1), (-1, 1, -3)}`. -/
theorem matter_27_three_gen_locus_iff (Q0 k_psi q1 q2 q3 : ℤ) (hsum : q1 + q2 + q3 = 0) :
    ((twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
     (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
     (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = 6 ∨
     (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
     (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
     (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = -6) ↔
      ((Q0, k_psi, Q0 - 2 * k_psi) = (-2, -1, 0) ∨
       (Q0, k_psi, Q0 - 2 * k_psi) = (-2, 1, -4) ∨
       (Q0, k_psi, Q0 - 2 * k_psi) = (-1, -1, 1) ∨
       (Q0, k_psi, Q0 - 2 * k_psi) = (-1, 1, -3)) := by
  constructor
  · intro hnet
    have hQk := matter_27_three_gen_forces_Q0_and_kpsi hsum hnet
    rcases hQk with ⟨rfl | rfl, rfl | rfl⟩
    · right; right; right; rfl
    · right; right; left; rfl
    · right; left; rfl
    · left; rfl
  · intro hloc
    rw [matter_27_chiral_excess_formula Q0 k_psi q1 q2 q3 hsum]
    rcases hloc with h | h | h | h <;>
      (simp only [Prod.mk.injEq] at h
       rcases h with ⟨rfl, rfl, _⟩
       norm_num)

/-- **Unconditional `≥ 3` Colored Light `10`-plets in Symmetric `(27, 3)` (`[P]`):** On the entire
traceless `net = ±3` locus, `twiceInd (Q₀ - 2 k_ψ) ∈ {2, 6}` (`ind ≥ 1` per color), so the 3-color
symmetric `(10, 3)_{-2}` multiplet satisfies `6 ≤ 3 * twiceInd (Q₀ - 2 k_ψ)` (`≥ 3` light `10`-plets). -/
theorem matter_27_three_gen_retains_exotic_10_values {Q0 k_psi q1 q2 q3 : ℤ}
    (hsum : q1 + q2 + q3 = 0)
    (hnet :
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = 6 ∨
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = -6) :
    (twiceInd (Q0 - 2 * k_psi) = 2 ∨ twiceInd (Q0 - 2 * k_psi) = 6) ∧
    2 ≤ twiceInd (Q0 - 2 * k_psi) ∧
    6 ≤ 3 * twiceInd (Q0 - 2 * k_psi) := by
  have hloc := (matter_27_three_gen_locus_iff Q0 k_psi q1 q2 q3 hsum).mp hnet
  unfold twiceInd
  rcases hloc with h | h | h | h <;>
    (simp only [Prod.mk.injEq] at h
     rcases h with ⟨rfl, rfl, _⟩
     norm_num)

/-- **General `248` Chiral `16` Formula Without Tracelessness (`[P]` — `BLK-1477` Precision Fix):**
Without imposing `q₁ + q₂ + q₃ = 0`, twice the net `16` excess over the full `248` equals
`2 * (2 Q₀ + 3) * (q₁ + q₂ + q₃)` identically (`k_ψ` cancels identically). -/
theorem e8_248_chiral_excess_formula (Q0 k_psi q1 q2 q3 : ℤ) :
    (twiceInd (Q0 + k_psi + q1) - twiceInd (Q0 - k_psi - q1)) +
    (twiceInd (Q0 + k_psi + q2) - twiceInd (Q0 - k_psi - q2)) +
    (twiceInd (Q0 + k_psi + q3) - twiceInd (Q0 - k_psi - q3)) +
    (twiceInd (Q0 - 3 * k_psi) - twiceInd (Q0 + 3 * k_psi)) =
      2 * (2 * Q0 + 3) * (q1 + q2 + q3) := by
  rw [show Q0 + k_psi + q1 = Q0 + (k_psi + q1) by ring,
      show Q0 - k_psi - q1 = Q0 - (k_psi + q1) by ring,
      show Q0 + k_psi + q2 = Q0 + (k_psi + q2) by ring,
      show Q0 - k_psi - q2 = Q0 - (k_psi + q2) by ring,
      show Q0 + k_psi + q3 = Q0 + (k_psi + q3) by ring,
      show Q0 - k_psi - q3 = Q0 - (k_psi + q3) by ring,
      show Q0 - 3 * k_psi = Q0 + (-3 * k_psi) by ring,
      show Q0 + 3 * k_psi = Q0 - (-3 * k_psi) by ring]
  simp only [spinC_chiral_excess_linear]
  ring

/-- **General `SU(5)` `10`-plet Formula in `248` Without Tracelessness (`[P]`):**
Without imposing `q₁ + q₂ + q₃ = 0`, twice the net `SU(5)` `10` excess over `248` equals
`2 * (2 Q₀ + 3) * (q₁ + q₂ + q₃)` identically (`k_ψ` and `k_χ` cancel identically). -/
theorem su5_248_chiral_10_excess_formula (Q0 k_psi k_chi q1 q2 q3 : ℤ) :
    (twiceInd (Q0 + (k_psi - k_chi + q1)) - twiceInd (Q0 - (k_psi - k_chi + q1))) +
    (twiceInd (Q0 + (k_psi - k_chi + q2)) - twiceInd (Q0 - (k_psi - k_chi + q2))) +
    (twiceInd (Q0 + (k_psi - k_chi + q3)) - twiceInd (Q0 - (k_psi - k_chi + q3))) +
    (twiceInd (Q0 + (-3 * k_psi - k_chi)) - twiceInd (Q0 - (-3 * k_psi - k_chi))) +
    (twiceInd (Q0 + 4 * k_chi) - twiceInd (Q0 - 4 * k_chi)) =
      2 * (2 * Q0 + 3) * (q1 + q2 + q3) := by
  simp only [spinC_chiral_excess_linear]
  ring

/-- **Exact `248` Vanishing Criterion (`[P]`):** Over `ℤ`, `2 Q₀ + 3 ≠ 0` is always odd, so the
full-`248` chiral excess vanishes **if and only if** `q₁ + q₂ + q₃ = 0` (`trace T = 0`). -/
theorem e8_248_chiral_excess_zero_iff_traceless (Q0 k_psi q1 q2 q3 : ℤ) :
    (twiceInd (Q0 + k_psi + q1) - twiceInd (Q0 - k_psi - q1)) +
    (twiceInd (Q0 + k_psi + q2) - twiceInd (Q0 - k_psi - q2)) +
    (twiceInd (Q0 + k_psi + q3) - twiceInd (Q0 - k_psi - q3)) +
    (twiceInd (Q0 - 3 * k_psi) - twiceInd (Q0 + 3 * k_psi)) = 0 ↔
      q1 + q2 + q3 = 0 := by
  rw [e8_248_chiral_excess_formula]
  constructor
  · intro hz
    rcases mul_eq_zero.mp hz with h2 | htr
    · exfalso; omega
    · exact htr
  · intro hsum
    rw [hsum, mul_zero]

/-- **Traceful `248` `±3`-Generation Criterion (`[P]`):** Obtaining `net = ±3` (`twiceInd = ±6`)
from the full `248` requires breaking `SU(3)_f` tracelessness (`q₁ + q₂ + q₃ ≠ 0`): specifically
`(2 Q₀ + 3) * (q₁ + q₂ + q₃) = ±3` (so `|q₁ + q₂ + q₃| ∈ {1, 3}`). -/
theorem e8_248_traceful_three_gen_iff (Q0 k_psi q1 q2 q3 : ℤ) :
    ((twiceInd (Q0 + k_psi + q1) - twiceInd (Q0 - k_psi - q1)) +
     (twiceInd (Q0 + k_psi + q2) - twiceInd (Q0 - k_psi - q2)) +
     (twiceInd (Q0 + k_psi + q3) - twiceInd (Q0 - k_psi - q3)) +
     (twiceInd (Q0 - 3 * k_psi) - twiceInd (Q0 + 3 * k_psi)) = 6 ∨
     (twiceInd (Q0 + k_psi + q1) - twiceInd (Q0 - k_psi - q1)) +
     (twiceInd (Q0 + k_psi + q2) - twiceInd (Q0 - k_psi - q2)) +
     (twiceInd (Q0 + k_psi + q3) - twiceInd (Q0 - k_psi - q3)) +
     (twiceInd (Q0 - 3 * k_psi) - twiceInd (Q0 + 3 * k_psi)) = -6) ↔
      ((2 * Q0 + 3) * (q1 + q2 + q3) = 3 ∨
       (2 * Q0 + 3) * (q1 + q2 + q3) = -3) := by
  rw [e8_248_chiral_excess_formula, mul_assoc]
  constructor <;> intro h <;> rcases h with h | h <;> [left; right; left; right] <;> linarith

/-- **Traceful Matter-Sector `(27, 3)` Exact Chiral Excess (`[P]`):** Without assuming
`q₁ + q₂ + q₃ = 0`, twice the net chiral `16` excess in `(27, 3)` equals
`2 * (2 Q₀ + 3) * (3 k_ψ + q₁ + q₂ + q₃)`. -/
theorem matter_27_traceful_chiral_excess_formula (Q0 k_psi q1 q2 q3 : ℤ) :
    (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
    (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
    (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) =
      2 * (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) := by
  simp only [spinC_chiral_excess_linear]
  ring

/-- **Shifted Triplet Quadratic Identity (`[P]`):** Generalizes `twiceInd_triplet_identity` to any
base charge `Q : ℤ`: `∑ twiceInd (Q + q_i) = 3 * twiceInd Q + (2 Q + 3)(q₁ + q₂ + q₃) + ∑ q_i²`. -/
theorem twiceInd_shifted_triplet_identity (Q q1 q2 q3 : ℤ) :
    twiceInd (Q + q1) + twiceInd (Q + q2) + twiceInd (Q + q3) =
      3 * twiceInd Q + (2 * Q + 3) * (q1 + q2 + q3) + (q1 ^ 2 + q2 ^ 2 + q3 ^ 2) := by
  unfold twiceInd
  ring

/-- **Distinct-Weight Traceless `SU(3)_f` Retention of `(10, 3)_{-2}` (`[P]`):** Even allowing
arbitrary distinct traceless `SU(3)_f` weights (`q₁ + q₂ + q₃ = 0`), any solution on the Gate 2
locus `Q₀ ∈ {-1, -2}, k_ψ ∈ {1, -1}` satisfies `∑_i twiceInd (Q₀ - 2 k_ψ + q_i) ≥ 6`. Hence
NO traceless `SU(3)_f` twist cancels all three `(10, 3)` colors. -/
theorem traceless_distinct_weights_retain_exotic_10 {Q0 k_psi q1 q2 q3 : ℤ}
    (hQ : Q0 = -1 ∨ Q0 = -2) (hk : k_psi = 1 ∨ k_psi = -1) (hsum : q1 + q2 + q3 = 0) :
    6 ≤ twiceInd (Q0 - 2 * k_psi + q1) + twiceInd (Q0 - 2 * k_psi + q2) +
        twiceInd (Q0 - 2 * k_psi + q3) ∧
    ¬ (twiceInd (Q0 - 2 * k_psi + q1) = 0 ∧
       twiceInd (Q0 - 2 * k_psi + q2) = 0 ∧
       twiceInd (Q0 - 2 * k_psi + q3) = 0) := by
  have hbase : 2 ≤ twiceInd (Q0 - 2 * k_psi) := by
    unfold twiceInd
    rcases hQ with rfl | rfl <;> rcases hk with rfl | rfl <;> norm_num
  have hsum_ge :
      6 ≤ twiceInd (Q0 - 2 * k_psi + q1) + twiceInd (Q0 - 2 * k_psi + q2) +
          twiceInd (Q0 - 2 * k_psi + q3) := by
    rw [twiceInd_shifted_triplet_identity (Q0 - 2 * k_psi) q1 q2 q3, hsum]
    nlinarith [sq_nonneg q1, sq_nonneg q2, sq_nonneg q3]
  refine ⟨hsum_ge, ?_⟩
  rintro ⟨h1, h2, h3⟩
  omega

/-- **Traceful Twist Cancellation vs `248` & `net_16 = ±3` Obstruction (`[P]` — `BLK-1477` `Q_10` vs `248`):**
At `Q₀ ∈ {-1, -2}` and `k_ψ ∈ {1, -1}`, if an arbitrary (possibly traceful) twist `(q₁, q₂, q₃)`
cancels ALL three `(10, 3)_{-2}` colors (`twiceInd (Q₀ - 2 k_ψ + q_i) = 0` for `i = 1, 2, 3`), then:
1. `|q₁ + q₂ + q₃| ≥ 3` (necessarily traceful: `trace T ≠ 0`),
2. the full-`248` chiral `16` excess satisfies `|248_excess| ≥ 6` (`|net_248| ≥ 3 ≠ 0`), AND
3. the `(27, 3)` chiral `16` excess satisfies `|net_16_twice| ≥ 12` (`|net_16| ≥ 6`, destroying `±3`). -/
theorem traceful_Gate2_locus_cancel_10_forces_violation {Q0 k_psi q1 q2 q3 : ℤ}
    (hQ : Q0 = -1 ∨ Q0 = -2) (hk : k_psi = 1 ∨ k_psi = -1)
    (h10 : twiceInd (Q0 - 2 * k_psi + q1) = 0 ∧
           twiceInd (Q0 - 2 * k_psi + q2) = 0 ∧
           twiceInd (Q0 - 2 * k_psi + q3) = 0) :
    (3 ≤ q1 + q2 + q3 ∨ q1 + q2 + q3 ≤ -3) ∧
    (6 ≤ 2 * (2 * Q0 + 3) * (q1 + q2 + q3) ∨
         2 * (2 * Q0 + 3) * (q1 + q2 + q3) ≤ -6) ∧
    (12 ≤ 2 * (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) ∨
          2 * (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) ≤ -12) := by
  have zero_root : ∀ x : ℤ, twiceInd x = 0 → -2 ≤ x ∧ x ≤ -1 := by
    intro x hx
    unfold twiceInd at hx
    rcases mul_eq_zero.mp hx with h | h <;> omega
  have hb1 := zero_root _ h10.1
  have hb2 := zero_root _ h10.2.1
  have hb3 := zero_root _ h10.2.2
  rcases hQ with rfl | rfl <;> rcases hk with rfl | rfl <;>
    exact ⟨by omega, by omega, by omega⟩

/-- **Complete `ℤ⁵` Traceful `(27, 3)` `net = ±3` + Full `(10, 3)_{-2}` Cancellation Theorem (`[P]`):**
Over ALL `(Q₀, k_ψ, q₁, q₂, q₃) : ℤ⁵` (without tracelessness or parameter restrictions), `(27, 3)`
yields `net_16 = ±3` (`twiceInd` sum `= ±6`) AND all three `(10, 3)_{-2}` colors vanish
**if and only if** `k_ψ = 0` and `(Q₀, q₁, q₂, q₃) ∈ {(-2, 1, 1, 1), (-1, -1, -1, -1)}` — both
requiring traceful `q₁ + q₂ + q₃ = ±3 ≠ 0` (`net_248 = -3 ≠ 0`) and `k_ψ = 0 ∉ {1, -1}`.
Consequently, NO twist with `k_ψ ∈ {1, -1}` (or any `k_ψ ≠ 0`) achieves both `net_16 = ±3` and
all-color `(10, 3)` cancellation. -/
theorem traceful_27_three_gen_and_10_cancel_iff (Q0 k_psi q1 q2 q3 : ℤ) :
    ((2 * (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) = 6 ∨
      2 * (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) = -6) ∧
     twiceInd (Q0 - 2 * k_psi + q1) = 0 ∧
     twiceInd (Q0 - 2 * k_psi + q2) = 0 ∧
     twiceInd (Q0 - 2 * k_psi + q3) = 0) ↔
      (k_psi = 0 ∧
       ((Q0 = -2 ∧ q1 = 1 ∧ q2 = 1 ∧ q3 = 1) ∨
        (Q0 = -1 ∧ q1 = -1 ∧ q2 = -1 ∧ q3 = -1))) := by
  constructor
  · rintro ⟨hnet, h1, h2, h3⟩
    have zero_root : ∀ x : ℤ, twiceInd x = 0 → -2 ≤ x ∧ x ≤ -1 := by
      intro x hx
      unfold twiceInd at hx
      rcases mul_eq_zero.mp hx with h | h <;> omega
    have hb1 := zero_root _ h1
    have hb2 := zero_root _ h2
    have hb3 := zero_root _ h3
    have hprod : (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) = 3 ∨
        (2 * Q0 + 3) * (3 * k_psi + (q1 + q2 + q3)) = -3 := by
      rw [mul_assoc] at hnet
      rcases hnet with h | h <;> [left; right] <;> linarith
    have hQsplit : Q0 ≤ -4 ∨ Q0 = -3 ∨ Q0 = -2 ∨ Q0 = -1 ∨ Q0 = 0 ∨ 1 ≤ Q0 := by omega
    have hSsplit :
        3 * k_psi + (q1 + q2 + q3) ≤ -1 ∨
        3 * k_psi + (q1 + q2 + q3) = 0 ∨
        1 ≤ 3 * k_psi + (q1 + q2 + q3) := by omega
    rcases hQsplit with hlo | rfl | rfl | rfl | rfl | hhi
    · exfalso
      rcases hSsplit with hs | hs | hs <;> rcases hprod with hp | hp <;> nlinarith
    · exfalso
      have hsum3 : 3 * k_psi + (q1 + q2 + q3) = -1 ∨ 3 * k_psi + (q1 + q2 + q3) = 1 := by
        rcases hprod with hp | hp <;> [left; right] <;> linarith
      omega
    · have hk0 : k_psi = 0 := by
        rcases hprod with hp | hp <;> omega
      subst hk0
      have hq : q1 = 1 ∧ q2 = 1 ∧ q3 = 1 := by
        rcases hprod with hp | hp <;> omega
      exact ⟨rfl, Or.inl ⟨rfl, hq⟩⟩
    · have hk0 : k_psi = 0 := by
        rcases hprod with hp | hp <;> omega
      subst hk0
      have hq : q1 = -1 ∧ q2 = -1 ∧ q3 = -1 := by
        rcases hprod with hp | hp <;> omega
      exact ⟨rfl, Or.inr ⟨rfl, hq⟩⟩
    · exfalso
      have hsum3 : 3 * k_psi + (q1 + q2 + q3) = 1 ∨ 3 * k_psi + (q1 + q2 + q3) = -1 := by
        rcases hprod with hp | hp <;> [left; right] <;> linarith
      omega
    · exfalso
      rcases hSsplit with hs | hs | hs <;> rcases hprod with hp | hp <;> nlinarith
  · rintro ⟨rfl, ⟨rfl, rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl, rfl⟩⟩ <;> norm_num [twiceInd]

/-- **Universal Net Chiral `(10, 3)_{-2}` Persistence Under `(27, 3)` `net_16 = ±3` (`[P]`):**
Even for arbitrary traceful twists `(q₁, q₂, q₃) : ℤ³`, the net chiral `(10, 3)_{-2}` excess
`∑_i (twiceInd (Q₀ - 2 k_ψ + q_i) - twiceInd (Q₀ + 2 k_ψ - q_i))` equals
`2 * (2 Q₀ + 3) * (-6 k_ψ + q₁ + q₂ + q₃)`, and can NEVER vanish whenever `(27, 3)` gives
`net_16 = ±3` (`twiceInd` sum `= ±6`, because vanishing forces `q₁ + q₂ + q₃ = 6 k_ψ`, making
the `16` excess a multiple of `18`). -/
theorem exotic_10_net_chiral_excess_never_zero_when_three_gen (Q0 k_psi q1 q2 q3 : ℤ)
    (hnet :
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = 6 ∨
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = -6) :
    (twiceInd (Q0 - 2 * k_psi + q1) - twiceInd (Q0 + 2 * k_psi - q1)) +
    (twiceInd (Q0 - 2 * k_psi + q2) - twiceInd (Q0 + 2 * k_psi - q2)) +
    (twiceInd (Q0 - 2 * k_psi + q3) - twiceInd (Q0 + 2 * k_psi - q3)) =
      2 * (2 * Q0 + 3) * (-6 * k_psi + (q1 + q2 + q3)) ∧
    (twiceInd (Q0 - 2 * k_psi + q1) - twiceInd (Q0 + 2 * k_psi - q1)) +
    (twiceInd (Q0 - 2 * k_psi + q2) - twiceInd (Q0 + 2 * k_psi - q2)) +
    (twiceInd (Q0 - 2 * k_psi + q3) - twiceInd (Q0 + 2 * k_psi - q3)) ≠ 0 := by
  have h10_eq :
      (twiceInd (Q0 - 2 * k_psi + q1) - twiceInd (Q0 + 2 * k_psi - q1)) +
      (twiceInd (Q0 - 2 * k_psi + q2) - twiceInd (Q0 + 2 * k_psi - q2)) +
      (twiceInd (Q0 - 2 * k_psi + q3) - twiceInd (Q0 + 2 * k_psi - q3)) =
        2 * (2 * Q0 + 3) * (-6 * k_psi + (q1 + q2 + q3)) := by
    rw [show Q0 - 2 * k_psi + q1 = Q0 + (-2 * k_psi + q1) by ring,
        show Q0 + 2 * k_psi - q1 = Q0 - (-2 * k_psi + q1) by ring,
        show Q0 - 2 * k_psi + q2 = Q0 + (-2 * k_psi + q2) by ring,
        show Q0 + 2 * k_psi - q2 = Q0 - (-2 * k_psi + q2) by ring,
        show Q0 - 2 * k_psi + q3 = Q0 + (-2 * k_psi + q3) by ring,
        show Q0 + 2 * k_psi - q3 = Q0 - (-2 * k_psi + q3) by ring]
    simp only [spinC_chiral_excess_linear]
    ring
  refine ⟨h10_eq, ?_⟩
  rw [h10_eq]
  intro hz
  rcases mul_eq_zero.mp hz with h2 | htr
  · omega
  · rw [matter_27_traceful_chiral_excess_formula] at hnet
    have htr_eq : q1 + q2 + q3 = 6 * k_psi := by omega
    rw [htr_eq] at hnet
    have hmul18 : 2 * (2 * Q0 + 3) * (3 * k_psi + 6 * k_psi) = 18 * ((2 * Q0 + 3) * k_psi) := by ring
    rw [hmul18] at hnet
    rcases hnet with h | h <;> omega

/-- **Single-Multiplet Expansion vs Chiral-Excess Linearization (`[P]`):**
A single `Spin^c` operator at shifted charge `Q₀ + x` obeys
`twiceInd (Q₀ + x) = twiceInd Q₀ + (2 Q₀ + 3) * x + x²`, retaining both the base-shift index
`twiceInd Q₀` and quadratic `x²`; subtracting the conjugate `Q₀ - x` in `spinC_chiral_excess_linear`
cancels both terms, leaving `2 * (2 Q₀ + 3) * x`. -/
theorem twiceInd_shift_expansion (Q0 x : ℤ) :
    twiceInd (Q0 + x) = twiceInd Q0 + (2 * Q0 + 3) * x + x ^ 2 := by
  unfold twiceInd
  ring

/-- **Dolan / `BLK-1450` Single-Multiplet `ind(Q) = 3` Classification (`[P]`):**
Over `ℤ`, a single `Spin^c` Dirac operator yields `3` zero modes (`twiceInd Q = 6`) **iff**
`Q = 1 ∨ Q = -4`. At unshifted `Q₀ = 0, k_ψ = 1`, `Q = 1` gives `ind = 3` (`twiceInd = 6`),
`(10, 3)_{-2}` at `Q_10 = -2` has `0` modes, and `(1, 16)_{+3}` has `10` surplus modes (`twiceInd = 20`). -/
theorem single_multiplet_three_gen_iff (Q : ℤ) :
    twiceInd Q = 6 ↔ Q = 1 ∨ Q = -4 := by
  constructor
  · intro h
    unfold twiceInd at h
    have hsplit : Q ≤ -5 ∨ Q = -4 ∨ Q = -3 ∨ Q = -2 ∨ Q = -1 ∨ Q = 0 ∨ Q = 1 ∨ 2 ≤ Q := by omega
    rcases hsplit with hle | rfl | rfl | rfl | rfl | rfl | rfl | hge
    · exfalso; nlinarith
    · exact Or.inr rfl
    · exfalso; omega
    · exfalso; omega
    · exfalso; omega
    · exfalso; omega
    · exact Or.inl rfl
    · exfalso; nlinarith
  · rintro (rfl | rfl) <;> norm_num [twiceInd]

theorem single_multiplet_Q1_sector_counts :
    twiceInd (0 + 1) = 6 ∧ twiceInd (0 - 2 * 1) = 0 ∧ twiceInd (0 + 3 * 1) = 20 := by
  unfold twiceInd
  norm_num

/-- **Unshifted `Q₀ = 0` Triplet Exclusion in Gate 2 (`[P]`):**
At `Q₀ = 0` (where a single `+1` charge matches Dolan's `Q = 1`) and traceless `q₁ + q₂ + q₃ = 0`,
the Gate 2 `(27, 3)` net chiral excess equals `18 * k_ψ` (`9 * k_ψ` net generations — e.g. `9` at
`k_ψ = 1`, NOT `3`!), and can NEVER equal `±6` (`±3` generations). Thus `BLK-1450`'s `Q = 1`
requires `(L1)` (identifying the `3` zero modes with the `3` of `SU(3)_f`) plus `(L2)`. -/
theorem canonical_Q0_zero_triplet_chiral_excess_no_three_gen (k_psi q1 q2 q3 : ℤ)
    (hsum : q1 + q2 + q3 = 0) :
    (twiceInd (0 + (k_psi + q1)) - twiceInd (0 - (k_psi + q1))) +
    (twiceInd (0 + (k_psi + q2)) - twiceInd (0 - (k_psi + q2))) +
    (twiceInd (0 + (k_psi + q3)) - twiceInd (0 - (k_psi + q3))) = 18 * k_psi ∧
    18 * k_psi ≠ 6 ∧ 18 * k_psi ≠ -6 := by
  rw [matter_27_chiral_excess_formula 0 k_psi q1 q2 q3 hsum]
  refine ⟨by ring, ?_, ?_⟩ <;> omega

/-- **`L1/L2` Boundary Separation (`[P]` — `BLK-1477` Synthesis):**
On the entire Gate 2 traceless `(27, 3)` `net = ±3` locus, `Q₀ ≠ 0`, both symmetric `16` charges
`Q₀ ± k_ψ` avoid `{1, -4}` completely, and each color contributes `±1` net family from
`(ind(Q₀+k_ψ), ind(Q₀-k_ψ)) ∈ {(1, 0), (0, 1)}` (`twiceInd ∈ {(2, 0), (0, 2)}`), summing `3 × (±1) = ±3`
across colors — strictly distinct from `BLK-1450`'s single-operator `Q = 1` (`twiceInd 1 = 6`, `ind = 3`). -/
theorem gate2_locus_disjoint_from_single_multiplet_Q1 {Q0 k_psi q1 q2 q3 : ℤ}
    (hsum : q1 + q2 + q3 = 0)
    (hnet :
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = 6 ∨
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) = -6) :
    Q0 ≠ 0 ∧
    Q0 + k_psi ≠ 1 ∧ Q0 + k_psi ≠ -4 ∧
    Q0 - k_psi ≠ 1 ∧ Q0 - k_psi ≠ -4 ∧
    ((twiceInd (Q0 + k_psi) = 2 ∧ twiceInd (Q0 - k_psi) = 0) ∨
     (twiceInd (Q0 + k_psi) = 0 ∧ twiceInd (Q0 - k_psi) = 2)) := by
  have hloc := (matter_27_three_gen_locus_iff Q0 k_psi q1 q2 q3 hsum).mp hnet
  unfold twiceInd
  rcases hloc with h | h | h | h <;>
    (simp only [Prod.mk.injEq] at h
     rcases h with ⟨rfl, rfl, _⟩
     norm_num)

end E8SpinCChargeLocking

#print axioms GCosmoRatio_lt_eta
#print axioms GCosmoRatio_le_eta
#print axioms bbn_lower_bound_forces_lambda_s
#print axioms jtot_nonfolding_iff_poly
#print axioms jtot_nonfolding_lt_eleven_point_three
#print axioms jtot_bbn_5pct_impossible
#print axioms jtot_bbn_10pct_KB_ceiling
#print axioms twiceInd_nonneg
#print axioms twiceInd_duality
#print axioms twiceInd_triplet_identity
#print axioms no_zero_sum_twist_below_nine
#print axioms nontrivial_zero_sum_twist_strictly_above_nine
#print axioms symmetric_compensating_bundle_unique
#print axioms singlet_and_sterile_index_counts
#print axioms spinC_chiral_excess_linear
#print axioms e8_248_total_chiral_excess_zero
#print axioms su5_248_chiral_10_excess_zero
#print axioms matter_27_chiral_excess_formula
#print axioms matter_27_three_gen_forces_Q0_and_kpsi
#print axioms matter_27_unique_solution_retains_symmetric_exotic_10
#print axioms matter_27_three_gen_locus_iff
#print axioms matter_27_three_gen_retains_exotic_10_values
#print axioms e8_248_chiral_excess_formula
#print axioms su5_248_chiral_10_excess_formula
#print axioms e8_248_chiral_excess_zero_iff_traceless
#print axioms e8_248_traceful_three_gen_iff
#print axioms matter_27_traceful_chiral_excess_formula
#print axioms twiceInd_shifted_triplet_identity
#print axioms traceless_distinct_weights_retain_exotic_10
#print axioms traceful_Gate2_locus_cancel_10_forces_violation
#print axioms traceful_27_three_gen_and_10_cancel_iff
#print axioms exotic_10_net_chiral_excess_never_zero_when_three_gen
#print axioms twiceInd_shift_expansion
#print axioms single_multiplet_three_gen_iff
#print axioms single_multiplet_Q1_sector_counts
#print axioms canonical_Q0_zero_triplet_chiral_excess_no_three_gen
#print axioms gate2_locus_disjoint_from_single_multiplet_Q1

end ResNova.Wave3BBNAndSpinCCP2Bounds
