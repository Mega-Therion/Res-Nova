import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# The gate as a normalised holonomy, and κ as its susceptibility

Formalises the substrate calculation of `HAMILGRANGIAN_CANONICAL.tex`
§`sec:substrate-holonomy` (2026-09-24).

## Creation frame — read before citing

**The question this answers.** The corpus carried, since 2026-07-22, the
conjecture `θ = ln 2 + α_fs · κ(θ)` ("gate = one-bit floor + EM coupling ×
coherence ceiling"), with an owed calculation: show the `U(1)` fibre contributes
a magnetoelectric coupling with susceptibility *exactly* `κ`. This file proves
the algebraic core of that claim.

**The geometry being encoded (NOT proved here).** The live substrate
`V₂(ℝ³)` is the set of orthonormal 2-frames in `ℝ³`; since `e₃ = e₁ × e₂` is
determined it is `SO(3) ≅ ℝP³`, and `(e₁,e₂) ↦ e₁ ∈ S²` exhibits it as the unit
tangent bundle `UT(S²)`, a `U(1)` bundle of Euler number 2. By Gauss–Bonnet,
Levi-Civita holonomy around a loop bounding area `Ω` is a rotation by `Ω`, and
for a cone of half-angle `φ`, `Ω = 2π(1 − cos φ)`. The gate is then *defined* as
holonomy per full turn, `θ := Ω/2π = 1 − cos φ`.

**Inputs that are NOT derived (this file proves identities, not physics):**

1. **The identification `θ := Ω/2π`** — that the corpus's gate IS this
   normalised holonomy. `[conj]`
2. **Gauss–Bonnet holonomy = enclosed area** — standard, cited, not formalised
   here. `[C]`
3. **That `α_fs` is an angle increment in radians** — the one genuinely physical
   step, and the sharpest remaining gap. NOT used anywhere below. `[O]`
4. **Why the base point is `φ₀ = arccos(1 − ln 2)`** — unexplained. `[O]`

**What IS proved below** is the substitution's consequence: under `θ = 1 − cos φ`
the corpus's independently-defined `κ(θ) = √(θ(2−θ))` equals `sin φ`, equals
`dθ/dφ`, and is the unique function with that property on the relevant range.

**Non-claims.** No bundle theory, no connection, no curvature, no `α_fs`, no
physical ontology. The words "holonomy" and "susceptibility" name the intended
reading; the theorems are real-analysis identities. Do not cite this as a
derivation of `θ`, of `α_fs`, or of the numerical value `0.7`.

**Scope note.** The document this supports also records (`rem:thetaprov`) that
`θ = 7/10` is *adopted*, not forced — its cited dimension-ratio provenance fails
audit. Nothing here selects a numerical `θ`.

## Contents

* `kappa`                  — `κ(θ) = √(θ(2−θ))`, the two-channel union amplitude
* `kappa_sq`               — `κ² = 1 − (1−θ)²` (the union probability)          `[thm]`
* `pythagorean`            — `κ(θ)² + (1−θ)² = 1`                               `[thm]`
* `kappa_gate_eq_sin`      — `κ(1 − cos φ) = sin φ` for `φ ∈ [0,π]`             `[thm]`
* `susceptibility_eq_kappa`— `d/dφ (1 − cos φ) = κ(1 − cos φ)`                  `[thm]`
* `kappa_unique`           — any `f` with `f(1−cos φ) = sin φ` agrees with `κ`  `[thm]`
-/

namespace ResNova.GateHolonomy

open Real

noncomputable section

/-! ## 0. Definitions -/

/-- The two-channel union amplitude `κ(θ) = √(θ(2−θ))`, defined in the corpus by
`κ² = P(at least one of two independent channels aligned)`. -/
def kappa (θ : ℝ) : ℝ := Real.sqrt (θ * (2 - θ))

/-- The gate as normalised holonomy: `θ(φ) = Ω/2π = 1 − cos φ`. -/
def gate (φ : ℝ) : ℝ := 1 - Real.cos φ

/-! ## 1. The union reading -/

/-- `κ² = 1 − (1−θ)²`: the probability that at least one of two independent
channels, each aligning with probability `θ`, aligns. -/
theorem kappa_sq {θ : ℝ} (h0 : 0 ≤ θ) (h2 : θ ≤ 2) :
    kappa θ ^ 2 = 1 - (1 - θ) ^ 2 := by
  have hnn : 0 ≤ θ * (2 - θ) := mul_nonneg h0 (by linarith)
  rw [kappa, Real.sq_sqrt hnn]
  ring

/-- **Pythagorean form.** `κ(θ)² + (1−θ)² = 1`: with `κ = sin φ` the loop radius
and `1−θ = cos φ` its height, this is the unit sphere. -/
theorem pythagorean {θ : ℝ} (h0 : 0 ≤ θ) (h2 : θ ≤ 2) :
    kappa θ ^ 2 + (1 - θ) ^ 2 = 1 := by
  rw [kappa_sq h0 h2]; ring

/-! ## 2. The gate is the solid angle, and κ is the sine -/

/-- The gate lies in `[0,2]`, so `κ ∘ gate` is always defined. -/
theorem gate_mem (φ : ℝ) : 0 ≤ gate φ ∧ gate φ ≤ 2 := by
  constructor
  · have := Real.cos_le_one φ; unfold gate; linarith
  · have := Real.neg_one_le_cos φ; unfold gate; linarith

/-- **`κ(1 − cos φ) = sin φ`** for `φ ∈ [0,π]`, where `sin φ ≥ 0`.

This is the substitution's content: the corpus's `κ`, defined from a union
probability, is the sine of the cone half-angle. -/
theorem kappa_gate_eq_sin {φ : ℝ} (h0 : 0 ≤ φ) (hπ : φ ≤ π) :
    kappa (gate φ) = Real.sin φ := by
  have hs : 0 ≤ Real.sin φ := Real.sin_nonneg_of_nonneg_of_le_pi h0 hπ
  have hpy : Real.sin φ ^ 2 + Real.cos φ ^ 2 = 1 := Real.sin_sq_add_cos_sq φ
  have : gate φ * (2 - gate φ) = Real.sin φ ^ 2 := by
    unfold gate; nlinarith [hpy]
  rw [kappa, this, Real.sqrt_sq hs]

/-! ## 3. The susceptibility -/

/-- **The claim that was owed.** The derivative of the gate with respect to the
cone half-angle is exactly `κ` evaluated at that gate:
`dθ/dφ = κ(θ)`, for every `φ ∈ [0,π]`.

This is an identity in `φ`, not a numerical coincidence at one point. -/
theorem susceptibility_eq_kappa {φ : ℝ} (h0 : 0 ≤ φ) (hπ : φ ≤ π) :
    HasDerivAt gate (kappa (gate φ)) φ := by
  have hc : HasDerivAt gate (- -Real.sin φ) φ :=
    (Real.hasDerivAt_cos φ).const_sub 1
  rw [neg_neg] at hc
  rw [kappa_gate_eq_sin h0 hπ]
  exact hc

/-- Derivative form, for rewriting. -/
theorem deriv_gate {φ : ℝ} (h0 : 0 ≤ φ) (hπ : φ ≤ π) :
    deriv gate φ = kappa (gate φ) :=
  (susceptibility_eq_kappa h0 hπ).deriv

/-- **Uniqueness.** Any `f` satisfying `f (1 − cos φ) = sin φ` on `[0,π]` agrees
with `κ` there. So `κ` is not one choice among many — the geometry forces it. -/
theorem kappa_unique (f : ℝ → ℝ)
    (hf : ∀ φ : ℝ, 0 ≤ φ → φ ≤ π → f (gate φ) = Real.sin φ)
    {φ : ℝ} (h0 : 0 ≤ φ) (hπ : φ ≤ π) :
    f (gate φ) = kappa (gate φ) := by
  rw [hf φ h0 hπ, kappa_gate_eq_sin h0 hπ]

/-- The loop radius/height decomposition: `κ = sin φ` and `1 − θ = cos φ`. -/
theorem height_eq_cos (φ : ℝ) : 1 - gate φ = Real.cos φ := by
  unfold gate; ring

/-! ## 4. Axiom audit -/

#print axioms kappa_sq
#print axioms pythagorean
#print axioms gate_mem
#print axioms kappa_gate_eq_sin
#print axioms susceptibility_eq_kappa
#print axioms deriv_gate
#print axioms kappa_unique
#print axioms height_eq_cos

end

end ResNova.GateHolonomy
