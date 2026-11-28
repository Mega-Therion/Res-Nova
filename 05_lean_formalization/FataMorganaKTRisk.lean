/-
  FataMorganaKTRisk.lean
  Angle 2 (KT <-> ST Fata Morgana / CPTP K0-Risk): Zero-Mathlib Lean 4
  formalization of K0-index defect, CPTP trace conservation, and K0-weighted
  statistical excess-risk non-negativity.

  Epistemic Scope:
  - [P] Exact integer algebraic identities (zero external imports, zero sorry,
        100% axiom-print coverage).
  - [D] Companion SymPy symbolic verification:
        06_unification_and_spin/unified_spine_v2/fata_morgana_kt_risk_verify.py.
  - [O] Full operator-algebraic C*-K-theory to minimax statistical risk
        equivalence remains an open research bridge.
-/

namespace FataMorganaKTRisk

/-- K0-class topological defect `p_plus - p_minus` over `Int`. -/
def k0Defect (pPlus pMinus : Int) : Int :=
  pPlus - pMinus

/-- CPTP trace-conservation residual `trOut - trIn`. -/
def cptpTraceResidual (trOut trIn : Int) : Int :=
  trOut - trIn

/-- K0-weighted statistical excess risk: `(k0Defect pPlus pMinus)^2 * excessRisk`. -/
def k0WeightedRisk (pPlus pMinus excessRisk : Int) : Int :=
  (k0Defect pPlus pMinus) * (k0Defect pPlus pMinus) * excessRisk

private theorem int_sq_nonneg (x : Int) : 0 ≤ x * x := by
  rcases Int.le_total 0 x with h | h
  · exact Int.mul_nonneg h h
  · have hneg : 0 ≤ -x := Int.neg_nonneg_of_nonpos h
    have heq : x * x = (-x) * (-x) := (Int.neg_mul_neg x x).symm
    rw [heq]
    exact Int.mul_nonneg hneg hneg

/-- [P] Under CPTP trace preservation (`trOut = trIn`), the trace residual vanishes. -/
theorem cptpTraceResidual_zero (trOut trIn : Int) (h : trOut = trIn) :
    cptpTraceResidual trOut trIn = 0 := by
  simp [cptpTraceResidual, h]

/-- [P] K0-weighted statistical excess risk is non-negative whenever `excessRisk >= 0`. -/
theorem k0WeightedRisk_nonneg (pPlus pMinus excessRisk : Int) (hr : 0 ≤ excessRisk) :
    0 ≤ k0WeightedRisk pPlus pMinus excessRisk := by
  simp only [k0WeightedRisk]
  exact Int.mul_nonneg (int_sq_nonneg _) hr

/-- [P] If the K0 topological defect vanishes (`pPlus = pMinus`), the K0-weighted risk vanishes. -/
theorem k0WeightedRisk_zero_of_balanced (pPlus pMinus excessRisk : Int) (h : pPlus = pMinus) :
    k0WeightedRisk pPlus pMinus excessRisk = 0 := by
  simp [k0WeightedRisk, k0Defect, h]

end FataMorganaKTRisk

#print axioms FataMorganaKTRisk.cptpTraceResidual_zero
#print axioms FataMorganaKTRisk.k0WeightedRisk_nonneg
#print axioms FataMorganaKTRisk.k0WeightedRisk_zero_of_balanced
