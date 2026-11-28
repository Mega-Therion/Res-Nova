/-
  AeSTCurlVortexBalance.lean
  Angle 3 (VORT <-> AeST): Zero-Mathlib Lean 4 formalization of the AeST K_B
  curl-vortex energy balance against Hill's spherical vortex vorticity.

  Epistemic Scope:
  - [P] Exact polynomial and algebraic identities over Int (zero external imports,
        zero sorry, 100% axiom-print coverage).
  - [D] Companion SymPy symbolic verification:
        06_unification_and_spin/unified_spine_v2/aest_curl_vortex_balance_verify.py.
  - [O] Physical identification of the AeST vector curl B_A with galactic/halo
        vorticity remains an open hypothesis; never call AeST falsified.
-/

namespace AeSTCurlVortexBalance

/-- Scaled Hill spherical vortex azimuthal vorticity: `15 * u0 * r * s`
    (representing `2 * R^2 * omega_phi` without real division). -/
def hillVorticityScaled (u0 r s : Int) : Int :=
  15 * u0 * r * s

/-- Scaled AeST vector curl magnitude: `c0 * r * s`. -/
def aestCurlScaled (c0 r s : Int) : Int :=
  c0 * r * s

/-- Scaled AeST `K_B` curl-energy density: `K_B * (aestCurlScaled c0 r s)^2`. -/
def aestCurlEnergy (K_B c0 r s : Int) : Int :=
  K_B * (aestCurlScaled c0 r s) * (aestCurlScaled c0 r s)

/-- Curl-vortex balance residual:
    `2 * K_B * (c0 * r * s)^2 - lam * (15 * u0 * r * s)^2`. -/
def balanceResidual (K_B c0 lam u0 r s : Int) : Int :=
  2 * aestCurlEnergy K_B c0 r s - lam * (hillVorticityScaled u0 r s) * (hillVorticityScaled u0 r s)

/-- [P] Exact factorization of the curl-vortex balance residual. -/
theorem balanceResidual_factor (K_B c0 lam u0 r s : Int) :
    balanceResidual K_B c0 lam u0 r s =
      (2 * K_B * c0 * c0 - lam * 225 * u0 * u0) * (r * r * s * s) := by
  simp only [balanceResidual, aestCurlEnergy, aestCurlScaled, hillVorticityScaled]
  rw [Int.sub_mul]
  congr 1
  · simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  · have h225 : (15 : Int) * 15 = 225 := by decide
    simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
    rw [h225]

/-- [P] If the coupling condition `2 * K_B * c0^2 = 225 * lam * u0^2` holds,
    the curl-vortex balance residual vanishes identically for all `(r, s)`. -/
theorem balanceResidual_zero_of_matched (K_B c0 lam u0 r s : Int)
    (h : 2 * K_B * c0 * c0 = lam * 225 * u0 * u0) :
    balanceResidual K_B c0 lam u0 r s = 0 := by
  rw [balanceResidual_factor, h]
  simp

private theorem int_sq_nonneg (x : Int) : 0 ≤ x * x := by
  rcases Int.le_total 0 x with h | h
  · exact Int.mul_nonneg h h
  · have hneg : 0 ≤ -x := Int.neg_nonneg_of_nonpos h
    have heq : x * x = (-x) * (-x) := (Int.neg_mul_neg x x).symm
    rw [heq]
    exact Int.mul_nonneg hneg hneg

/-- [P] Non-negativity of the AeST `K_B` curl-energy density whenever `K_B >= 0`. -/
theorem aestCurlEnergy_nonneg (K_B c0 r s : Int) (hK : 0 ≤ K_B) :
    0 ≤ aestCurlEnergy K_B c0 r s := by
  simp only [aestCurlEnergy]
  rw [Int.mul_assoc]
  exact Int.mul_nonneg hK (int_sq_nonneg _)

end AeSTCurlVortexBalance

#print axioms AeSTCurlVortexBalance.balanceResidual_factor
#print axioms AeSTCurlVortexBalance.balanceResidual_zero_of_matched
#print axioms AeSTCurlVortexBalance.aestCurlEnergy_nonneg
