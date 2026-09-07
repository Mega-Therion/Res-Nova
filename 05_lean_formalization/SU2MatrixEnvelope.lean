/-
  SU2MatrixEnvelope.lean — RUNG 8

  The finite unit-quaternion realization is now represented by explicit
  2×2 complex matrices. This file proves the algebraic matrix bridge only.

  It does not prove topology, continuity, connectedness, Lie structure, or
  a physical SU(2)_L gauge field.
-/
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Determinant
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring
import FiniteSU2Envelope

namespace SU2MatrixEnvelope

open FiniteSU2Envelope
open scoped Matrix

/-- Standard complex 2×2 matrix attached to a quaternion
    `a + b i + c j + d k`. -/
def qMatrix (p : Quat) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.ofReal p.a + Complex.I * Complex.ofReal p.b,
      Complex.ofReal p.c + Complex.I * Complex.ofReal p.d;
     -Complex.ofReal p.c + Complex.I * Complex.ofReal p.d,
      Complex.ofReal p.a - Complex.I * Complex.ofReal p.b]

/-- Matrix multiplication preserves quaternion multiplication. -/
theorem qMatrix_mul (p q : Quat) :
    qMatrix (qmul p q) = qMatrix p * qMatrix q := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [qMatrix, qmul, Matrix.mul_apply, Fin.sum_univ_two,
      Complex.ext_iff] <;> constructor <;> ring

/-- The quaternion identity maps to the 2×2 identity matrix. -/
theorem qMatrix_one : qMatrix qone = (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [qMatrix, qone]

/-- The determinant is the quaternion norm. -/
theorem qMatrix_det (p : Quat) :
    Matrix.det (qMatrix p) = (qnorm p : ℂ) := by
  have hsq_re (x : ℝ) : ((x : ℂ)^2).re = x^2 := by
    simp [pow_two, Complex.mul_re]
  have hsq_im (x : ℝ) : ((x : ℂ)^2).im = 0 := by
    simp [pow_two, Complex.mul_im]
  apply Complex.ext <;>
    simp [qMatrix, Matrix.det_fin_two, qnorm, hsq_re, hsq_im] <;> ring

/-- Unit quaternions map to unitary matrices. -/
theorem qMatrix_unitary (p : Quat) (hp : qnorm p = 1) :
    (qMatrix p)ᴴ * qMatrix p = (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  dsimp [qnorm] at hp
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.conjTranspose, qMatrix, Matrix.mul_apply, Fin.sum_univ_two,
      qnorm, Complex.ext_iff] <;>
    constructor <;> nlinarith [hp]

/-- Unit quaternions map to determinant-one matrices. -/
theorem qMatrix_det_one (p : Quat) (hp : qnorm p = 1) :
    Matrix.det (qMatrix p) = 1 := by
  rw [qMatrix_det, hp]
  norm_num

/-- The finite binary-tetrahedral image has determinant one. -/
theorem btMatrix_det_one (p : ChiralResidue.Q8 × BinaryTetrahedral.C3) :
    Matrix.det (qMatrix (btCoord p)) = 1 := by
  apply qMatrix_det_one
  exact btCoord_unit p

/-- The finite image is unitary. -/
theorem btMatrix_unitary (p : ChiralResidue.Q8 × BinaryTetrahedral.C3) :
    (qMatrix (btCoord p))ᴴ * qMatrix (btCoord p) =
      (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  exact qMatrix_unitary _ (btCoord_unit p)

/-- The finite semidirect-product map is a matrix homomorphism. -/
theorem btMatrix_hom (p q : ChiralResidue.Q8 × BinaryTetrahedral.C3) :
    qMatrix (btCoord (BinaryTetrahedral.mulBT p q)) =
      qMatrix (btCoord p) * qMatrix (btCoord q) := by
  rw [FiniteSU2Envelope.btCoord_hom, qMatrix_mul]

end SU2MatrixEnvelope
