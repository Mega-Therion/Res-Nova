/-
  SU2CarrierRungs.lean — RUNG 9

  Names the algebraic carrier of 2×2 complex matrices satisfying the
  unitary-left identity and determinant-one condition. This is an algebraic
  carrier and closure theorem, not yet a topological or Lie-group structure.
-/
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Determinant
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Tactic.FinCases
import SU2MatrixEnvelope

namespace SU2CarrierRungs

noncomputable section

open SU2MatrixEnvelope
open FiniteSU2Envelope
open ChiralResidue BinaryTetrahedral
open scoped Matrix

abbrev Mat2 := Matrix (Fin 2) (Fin 2) ℂ

/-- Algebraic SU(2) carrier: unitary on the left and determinant one. -/
def SU2Carrier := {M : Mat2 // Mᴴ * M = (1 : Mat2) ∧ Matrix.det M = 1}

/-- The identity element of the algebraic SU(2) carrier. -/
def carrierOne : SU2Carrier :=
  ⟨1, by simp, by simp⟩

/-- Multiplication closure for the algebraic SU(2) carrier. -/
def carrierMul (A B : SU2Carrier) : SU2Carrier :=
  ⟨A.1 * B.1, by
    rw [Matrix.conjTranspose_mul]
    calc
      B.1ᴴ * A.1ᴴ * (A.1 * B.1) =
          B.1ᴴ * (A.1ᴴ * A.1) * B.1 := by
            simp only [Matrix.mul_assoc]
      _ = B.1ᴴ * (1 : Mat2) * B.1 := by rw [A.property.1]
      _ = (1 : Mat2) := by simpa using B.property.1
   , by
      rw [Matrix.det_mul]
      simp [A.property.2, B.property.2]⟩

/-- Carrier multiplication agrees with ordinary matrix multiplication. -/
theorem carrierMul_val (A B : SU2Carrier) :
    (carrierMul A B).1 = A.1 * B.1 := rfl

/-- The identity carrier has the ordinary identity matrix as value. -/
theorem carrierOne_val : carrierOne.1 = 1 := rfl

/-- Every finite binary-tetrahedral matrix image lands in the named carrier. -/
def btCarrier (p : ChiralResidue.Q8 × BinaryTetrahedral.C3) : SU2Carrier :=
  ⟨qMatrix (FiniteSU2Envelope.btCoord p), btMatrix_unitary p, btMatrix_det_one p⟩

theorem btCarrier_val (p : ChiralResidue.Q8 × BinaryTetrahedral.C3) :
    (btCarrier p).1 = qMatrix (FiniteSU2Envelope.btCoord p) := rfl

/-- The finite homomorphism is a homomorphism into the named carrier. -/
theorem btCarrier_hom (p q : ChiralResidue.Q8 × BinaryTetrahedral.C3) :
    btCarrier (BinaryTetrahedral.mulBT p q) = carrierMul (btCarrier p) (btCarrier q) := by
  apply Subtype.ext
  simp only [carrierMul_val, btCarrier_val]
  exact btMatrix_hom p q

end
end SU2CarrierRungs
