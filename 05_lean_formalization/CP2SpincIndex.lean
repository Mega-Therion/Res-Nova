/-
Copyright (c) 2026 R.W. Yett / Chyren / Res-Nova. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: R.W. Yett, Muse
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
# Spin^c Dirac Index Polynomial for CP² — Lean 4 Formalization

## Scope (read this first)

This module formalizes the **characteristic-class arithmetic and the index
polynomial** for the Spin^c Dirac operator on CP² twisted by `O(Q)`. It does
NOT formalize:

* the analytic Dirac operator on CP², its domain, or its spectrum;
* the Atiyah–Singer index theorem;
* CP² itself as a manifold, its cohomology ring, or its characteristic
  classes — Mathlib has none of these.

What Lean proves here `[P]` is the polynomial identity: **given** the Â-form
and Chern-character inputs (transcribed below from the geometry, tier
`[ext]`/`[D]`), the characteristic integral evaluates to `(Q+1)(Q+2)/2`.

## The [ext] hypothesis (stated, never proved, never axiomatized)

The Atiyah–Singer index theorem for the Spin^c Dirac operator says

    ind D_Q⁺ = ∫_{CP²} e^{(Q+3/2)H} · Â(CP²),

where `H` generates `H²(CP²; ℤ)` with `∫ H² = 1`. This identification is
**external mathematics** (`[ext]`): it enters this file only as an explicit
hypothesis of `dirac_index_poly`, never as a Lean axiom. The theorem
`index_formula` proves the *integral* equals `(Q+1)(Q+2)/2`; the statement
"this integral is the Dirac index" is the `[ext]` hypothesis, not a Lean
theorem.

## Geometric inputs (tier [ext]/[D] — transcribed, not derived)

With `H` the generator of `H²(CP²; ℤ)`, normalized so `∫ H² = 1`:

* `c₁(T CP²) = 3H`, `c₂(T CP²) = 3H²`, hence `p₁ = c₁² − 2c₂ = 3H²`
  (checked arithmetically in `pontryagin_p1_coeff`);
* Â-genus form `Â = 1 − p₁/24 = 1 − H²/8`
  (checked arithmetically in `aHat_h2_coeff`);
* the canonical Spin^c determinant line is `O(3)`; twisting by `O(Q)` gives
  determinant line `O(2Q+3)`, so the Chern character contributes
  `e^{(Q+3/2)H}` (the exponent is half the determinant degree:
  `det_twist_exponent`).

## The polynomial model

A cohomology class of degree ≤ 4 is represented as a triple `(a₀, a₁, a₂)`
of rationals — the coefficients of `1, H, H²` — with multiplication
truncated at `H³ = 0` (`mulClass`) and integration picking out the `H²`
coefficient (`integral`, since `∫ H² = 1`). The model is honest about what
it is: formal polynomial arithmetic over ℚ, not a cohomology ring.

## Dolan cross-check (notation resolution, 2026-11-17)

The arithmetic identity `(|Y|+2)(|Y|+4)/8 = 3` at `|Y| = 2` is Dolan's own
notation in hep-th/0304037, eq. (B.7): there `d(k,n)` is a ground-level
degeneracy label (`k = n = 0`), and `d(0,0) = 3` at `|Y| = 2`. This `d(0,0)`
must NOT be read as the Dynkin `(0,0)` singlet: in standard Dynkin labels
`d(p,q) = (p+1)(q+1)(p+q+2)/2`, the singlet is `d(0,0) = 1` and the triplet
is `d(1,0) = 3` (both checked in Lean below); in Dolan's hep-th/0307124
notation the triplet is `d_1 = 3`. The substance is the same under every
labelling: three `Q = 1` zero modes forming an SU(3) triplet, agreeing with
the index at `Q = 1` (`index_Q1_eq_dolan`).

## Serre duality note (O15, 2026-11-18)

Because `K_{CP²} = O(-3)`, Serre duality on `CP²` maps `Q ↦ -3 - Q`,
exchanging `h⁰(CP², O(Q))` and `h²(CP², O(-3-Q))`. On the index polynomial
`χ(Q) = (Q+1)(Q+2)/2`, this manifests as the exact reflection symmetry
`indexViaIntegral (-3 - Q) = indexViaIntegral Q` (`index_serre_duality`),
mapping the `Q = 1` triplet (`h⁰ = 3`, `h² = 0`) to the Serre-dual `Q = -4`
triplet (`h⁰ = 0`, `h² = 3`). Note that the algebraic symmetry is `[P]`,
while the cohomology sheaf interpretation (`h⁰` vs `h²`) is external
geometry (`[ext]`).

## Main results

* `index_formula`: `indexViaIntegral Q = (Q+1)(Q+2)/2` for all `Q : ℚ`.
* `index_formula_sq`: the same index as `((2Q+3)² − 1)/8`.
* `index_serre_duality`: `indexViaIntegral (-3 - Q) = indexViaIntegral Q` (O15).
* `index_table`: `Q ∈ {0, 1, −1, −2, −4} ↦ {1, 3, 0, 0, 3}`.
* `dolan_ground_deg_two`: Dolan's (B.7) degeneracy is `3` at `|Y| = 2`.
* `dirac_index_poly`: conditional on the [ext] Atiyah–Singer identification,
  the analytic index is the polynomial.
-/

namespace ResNova.CP2SpincIndex

/-! ### The truncated polynomial model -/

/-- Chern character of a line bundle with first Chern class `t·H`, truncated
at `H³ = 0`: `e^{tH} = 1 + tH + (t²/2)H²`, as coefficients `(a₀, a₁, a₂)`. -/
def chernCharacter (t : ℚ) : ℚ × ℚ × ℚ := (1, t, t ^ 2 / 2)

/-- The Â-genus form of CP²: `Â = 1 − H²/8`. The `−1/8` is the geometric
input `−p₁/24` with `p₁ = 3H²` (see `aHat_h2_coeff`). -/
def aHatForm : ℚ × ℚ × ℚ := (1, 0, -1 / 8)

/-- Product of two truncated classes, with `H³ = 0` imposed. -/
def mulClass (a b : ℚ × ℚ × ℚ) : ℚ × ℚ × ℚ :=
  (a.1 * b.1,
   a.1 * b.2.1 + a.2.1 * b.1,
   a.1 * b.2.2 + a.2.1 * b.2.1 + a.2.2 * b.1)

/-- Integration over CP²: picks out the `H²` coefficient, since `∫ H² = 1`
and `∫ 1 = ∫ H = 0` by degree. -/
def integral (c : ℚ × ℚ × ℚ) : ℚ := c.2.2

/-- The characteristic integral for the Spin^c Dirac operator twisted by
`O(Q)`: `∫ e^{(Q+3/2)H} · Â`. The exponent `Q + 3/2` is half the degree of
the determinant line `O(2Q+3)` (see `det_twist_exponent`). -/
def indexViaIntegral (Q : ℚ) : ℚ :=
  integral (mulClass (chernCharacter (Q + 3 / 2)) aHatForm)

/-- Dolan's ground-level degeneracy, hep-th/0304037 eq. (B.7):
`d(0,0) = (|Y|+2)(|Y|+4)/8`. See the header for the notation resolution. -/
def dolanGroundDeg (Y : ℚ) : ℚ := (|Y| + 2) * (|Y| + 4) / 8

/-- SU(3) dimension in standard Dynkin labels:
`d(p,q) = (p+1)(q+1)(p+q+2)/2`. Included to pin down the notation
distinction: Dynkin `(0,0)` is the singlet, Dynkin `(1,0)` is the triplet. -/
def dynkinDim (p q : ℕ) : ℕ := (p + 1) * (q + 1) * (p + q + 2) / 2

/-! ### Geometric inputs, checked arithmetically -/

/-- `[P]` given the inputs `c₁ = 3H`, `c₂ = 3H²`: the first Pontryagin
class is `p₁ = c₁² − 2c₂ = 3H²`. -/
theorem pontryagin_p1_coeff : (3 : ℚ) ^ 2 - 2 * 3 = 3 := by norm_num

/-- `[P]` given `p₁ = 3H²`: the Â-form's `H²` coefficient is `−p₁/24 = −1/8`. -/
theorem aHat_h2_coeff : -(3 : ℚ) / 24 = -1 / 8 := by norm_num

/-- `[P]` The Chern-character exponent is half the determinant-line degree:
twisting by `O(Q)` on top of the canonical `O(3)` gives determinant line
`O(2Q+3)`, and `(2Q+3)/2 = Q + 3/2`. -/
theorem det_twist_exponent (Q : ℚ) : (2 * Q + 3) / 2 = Q + 3 / 2 := by ring

/-! ### The index polynomial — main theorems -/

/-- `[P]` The characteristic integral is the index polynomial:
`∫ e^{(Q+3/2)H}(1 − H²/8) = (Q+1)(Q+2)/2`. -/
theorem index_formula (Q : ℚ) :
    indexViaIntegral Q = (Q + 1) * (Q + 2) / 2 := by
  simp only [indexViaIntegral, integral, mulClass, chernCharacter, aHatForm]
  ring

/-- `[P]` The same index in the `((2Q+3)² − 1)/8` form: the `H²` coefficient
of the product is `(Q+3/2)²/2 − 1/8`. -/
theorem index_formula_sq (Q : ℚ) :
    indexViaIntegral Q = ((2 * Q + 3) ^ 2 - 1) / 8 := by
  rw [index_formula]
  ring

/-- `[P]` The two closed forms agree. -/
theorem index_poly_eq_sq (Q : ℚ) :
    (Q + 1) * (Q + 2) / 2 = ((2 * Q + 3) ^ 2 - 1) / 8 := by ring

/-- `[P]` Algebraic Serre-duality reflection symmetry `Q ↔ -3 - Q` (O15):
maps `Q = 1` (`h⁰ = 3`) to `Q = -4` (`h² = 3`) with identical index polynomial. -/
theorem index_serre_duality (Q : ℚ) :
    indexViaIntegral (-3 - Q) = indexViaIntegral Q := by
  rw [index_formula, index_formula]
  ring

/-! ### The index table -/

/-- `[P]` `Q = 0`: index 1. -/
theorem index_Q0 : indexViaIntegral 0 = 1 := by
  rw [index_formula]; norm_num

/-- `[P]` `Q = 1`: index 3 — the three generations. -/
theorem index_Q1_three_generations : indexViaIntegral 1 = 3 := by
  rw [index_formula]; norm_num

/-- `[P]` `Q = −1`: index 0. -/
theorem index_Qm1 : indexViaIntegral (-1) = 0 := by
  rw [index_formula]; norm_num

/-- `[P]` `Q = −2`: index 0. -/
theorem index_Qm2 : indexViaIntegral (-2) = 0 := by
  rw [index_formula]; norm_num

/-- `[P]` `Q = −4`: index 3. -/
theorem index_Qm4 : indexViaIntegral (-4) = 3 := by
  rw [index_formula]; norm_num

/-- `[P]` The full table: `Q ∈ {0, 1, −1, −2, −4} ↦ {1, 3, 0, 0, 3}`. -/
theorem index_table :
    indexViaIntegral 0 = 1 ∧ indexViaIntegral 1 = 3 ∧
      indexViaIntegral (-1) = 0 ∧ indexViaIntegral (-2) = 0 ∧
      indexViaIntegral (-4) = 3 :=
  ⟨index_Q0, index_Q1_three_generations, index_Qm1, index_Qm2, index_Qm4⟩

/-! ### Dolan cross-check -/

/-- `[P]` Dolan hep-th/0304037 eq. (B.7): the ground-level degeneracy
`d(0,0) = (|Y|+2)(|Y|+4)/8` is `3` at `|Y| = 2`. -/
theorem dolan_ground_deg_two : dolanGroundDeg 2 = 3 := by
  norm_num [dolanGroundDeg]

/-- `[P]` Same degeneracy at `Y = −2` (the formula depends on `|Y|`). -/
theorem dolan_ground_deg_neg_two : dolanGroundDeg (-2) = 3 := by
  norm_num [dolanGroundDeg]

/-- `[P]` The index at `Q = 1` agrees with Dolan's ground-level degeneracy:
three zero modes, an SU(3) triplet under either labelling. -/
theorem index_Q1_eq_dolan : indexViaIntegral 1 = dolanGroundDeg 2 := by
  rw [index_Q1_three_generations, dolan_ground_deg_two]

/-- `[P]` Dynkin `(0,0)` is the singlet — this is NOT Dolan's `d(0,0)`. -/
theorem dynkin_singlet : dynkinDim 0 0 = 1 := rfl

/-- `[P]` Dynkin `(1,0)` is the triplet — Dolan hep-th/0307124 `d_1 = 3`. -/
theorem dynkin_triplet : dynkinDim 1 0 = 3 := rfl

/-! ### The [ext] bridge — conditional, not proved -/

/-- `[ext] ⇒ [P]` Conditional on the Atiyah–Singer identification (the
hypothesis `hAS`, external mathematics, NOT a Lean axiom and NOT proved
here), the analytic Spin^c Dirac index at twist `Q` is the polynomial
`(Q+1)(Q+2)/2`. What Lean proves is the polynomial evaluation; the
identification of the integral with the analytic index is the hypothesis. -/
theorem dirac_index_poly (Q : ℚ) (analyticIndex : ℚ)
    (hAS : analyticIndex = indexViaIntegral Q) :
    analyticIndex = (Q + 1) * (Q + 2) / 2 := by
  rw [hAS, index_formula]

/-- `[ext] ⇒ [P]` Same conditional statement at `Q = 1`: three generations. -/
theorem dirac_index_Q1_three_generations (analyticIndex : ℚ)
    (hAS : analyticIndex = indexViaIntegral 1) :
    analyticIndex = 3 := by
  rw [hAS, index_Q1_three_generations]

end ResNova.CP2SpincIndex

/-! ### Axiom audit -/

#print axioms ResNova.CP2SpincIndex.index_formula
#print axioms ResNova.CP2SpincIndex.index_formula_sq
#print axioms ResNova.CP2SpincIndex.index_serre_duality
#print axioms ResNova.CP2SpincIndex.index_table
#print axioms ResNova.CP2SpincIndex.dolan_ground_deg_two
#print axioms ResNova.CP2SpincIndex.index_Q1_eq_dolan
#print axioms ResNova.CP2SpincIndex.dirac_index_poly
#print axioms ResNova.CP2SpincIndex.dirac_index_Q1_three_generations
