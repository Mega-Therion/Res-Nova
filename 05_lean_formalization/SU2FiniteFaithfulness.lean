/-
  SU2FiniteFaithfulness.lean — RUNG 10

  Faithfulness of the finite matrix representation is reduced to the exact
  finite quaternion coordinates already used by the rung-seven construction.
-/
import SU2CarrierRungs
import SU2MatrixEnvelope

set_option maxHeartbeats 2000000

namespace SU2FiniteFaithfulness

open FiniteSU2Envelope
open SU2MatrixEnvelope
open SU2CarrierRungs
open ChiralResidue BinaryTetrahedral

/-- The finite binary-tetrahedral coordinate map is injective. -/
theorem btCoord_injective : Function.Injective btCoord := by
  intro p q h
  rcases p with ⟨⟨a, ar⟩, x⟩
  rcases q with ⟨⟨b, br⟩, y⟩
  cases a <;> cases ar <;> cases x <;> cases b <;> cases br <;> cases y
  all_goals
    have ha := congrArg Quat.a h
    have hb := congrArg Quat.b h
    have hc := congrArg Quat.c h
    have hd := congrArg Quat.d h
    norm_num [btCoord, q8Coord, qTPow, qT, qone, qmul] at *

/-- The finite matrix representation is faithful. -/
theorem btMatrix_injective :
    Function.Injective (fun p : Q8 × C3 => qMatrix (btCoord p)) := by
  intro p q h
  apply btCoord_injective
  exact SU2MatrixEnvelope.qMatrix_injective h

/-- The named SU(2) carrier representation is faithful. -/
theorem btCarrier_injective :
    Function.Injective SU2CarrierRungs.btCarrier := by
  intro p q h
  apply btMatrix_injective
  exact congrArg Subtype.val h

end SU2FiniteFaithfulness
