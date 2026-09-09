/-
  FiniteSU2Envelope.lean — Pure Lean + exact real coordinates

  RUNG 7: the finite binary-tetrahedral miniature receives an explicit
  quaternionic realization. This is deliberately narrower than the full
  continuous SU(2) envelope.

  WHAT THIS FILE PROVES [P]:
    * a concrete quaternion multiplication on R^4;
    * the Q8 cover used by BinaryTetrahedral embeds into unit quaternions;
    * an order-three unit quaternion implements the existing phi action by
      conjugation;
    * the semidirect product Q8 ⋊ C3 maps homomorphically into unit
      quaternions and every image has norm one.

  WHAT THIS FILE DOES NOT PROVE [O]:
    * that the image is the whole binary tetrahedral group by an internal
      cardinality theorem;
    * a 2x2 complex-matrix SU(2) representation;
    * topology, continuity, connectedness, Lie structure, or a gauge field;
    * any physical interpretation of the finite model.

  The correct interpretation of this rung is: an explicit finite subgroup
  realization inside the unit-quaternion model of SU(2), not a proof that a
  finite census is the continuous group SU(2).
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import BinaryTetrahedral

namespace FiniteSU2Envelope

noncomputable section

open ChiralResidue BinaryTetrahedral

structure Quat where
  a : ℝ
  b : ℝ
  c : ℝ
  d : ℝ

instance : Inhabited Quat := ⟨⟨0, 0, 0, 0⟩⟩

def qmul (p q : Quat) : Quat :=
  ⟨p.a*q.a - p.b*q.b - p.c*q.c - p.d*q.d,
   p.a*q.b + p.b*q.a + p.c*q.d - p.d*q.c,
   p.a*q.c - p.b*q.d + p.c*q.a + p.d*q.b,
   p.a*q.d + p.b*q.c - p.c*q.b + p.d*q.a⟩

def qone : Quat := ⟨1, 0, 0, 0⟩

def qnorm (p : Quat) : ℝ := p.a^2 + p.b^2 + p.c^2 + p.d^2

theorem quat_ext {p q : Quat} (ha : p.a = q.a) (hb : p.b = q.b)
    (hc : p.c = q.c) (hd : p.d = q.d) : p = q := by
  cases p; cases q; simp_all

theorem qmul_assoc (p q r : Quat) : qmul (qmul p q) r = qmul p (qmul q r) := by
  cases p; cases q; cases r
  apply quat_ext <;> dsimp [qmul] <;> ring

theorem qone_mul (p : Quat) : qmul qone p = p := by
  cases p <;> simp [qmul, qone]

theorem qmul_one (p : Quat) : qmul p qone = p := by
  cases p <;> simp [qmul, qone]

theorem qnorm_mul (p q : Quat) : qnorm (qmul p q) = qnorm p * qnorm q := by
  cases p; cases q <;> dsimp [qmul, qnorm] <;> ring

/-- The Q8 convention already used by the repository, realized in H. -/
def q8Coord : Q8 → Quat
  | ⟨.r0, false⟩ => ⟨1, 0, 0, 0⟩
  | ⟨.r1, false⟩ => ⟨0, 1, 0, 0⟩
  | ⟨.r2, false⟩ => ⟨-1, 0, 0, 0⟩
  | ⟨.r3, false⟩ => ⟨0, -1, 0, 0⟩
  | ⟨.r0, true⟩ => ⟨0, 0, 1, 0⟩
  | ⟨.r1, true⟩ => ⟨0, 0, 0, 1⟩
  | ⟨.r2, true⟩ => ⟨0, 0, -1, 0⟩
  | ⟨.r3, true⟩ => ⟨0, 0, 0, -1⟩

/-- A unit quaternion whose conjugation implements the existing order-three phi. -/
def qT : Quat := ⟨-1/2, -1/2, -1/2, 1/2⟩

def qTPow : C3 → Quat
  | .g0 => qone
  | .g1 => qT
  | .g2 => qmul qT qT

def btCoord (p : Q8 × C3) : Quat :=
  qmul (q8Coord p.1) (qTPow p.2)

theorem qone_unit : qnorm qone = 1 := by simp [qone, qnorm]

theorem q8Coord_unit (a : Q8) : qnorm (q8Coord a) = 1 := by
  cases a with
  | mk k b => cases k <;> cases b <;> norm_num [q8Coord, qnorm]

theorem qT_unit : qnorm qT = 1 := by
  norm_num [qT, qnorm]

theorem qT_cube : qmul (qmul qT qT) qT = qone := by
  norm_num [qT, qone, qmul]

theorem qTPow_unit (x : C3) : qnorm (qTPow x) = 1 := by
  cases x <;> norm_num [qTPow, qone, qT, qnorm, qmul]

theorem btCoord_unit (p : Q8 × C3) : qnorm (btCoord p) = 1 := by
  rw [btCoord, qnorm_mul, q8Coord_unit, qTPow_unit]
  norm_num

theorem q8Coord_mul (a b : Q8) :
    q8Coord (mul a b) = qmul (q8Coord a) (q8Coord b) := by
  cases a with
  | mk ka ba => cases b with
    | mk kb bb => cases ka <;> cases ba <;> cases kb <;> cases bb <;>
        norm_num [q8Coord, mul, R4.add, R4.neg, qmul]

theorem qT_conj_phi (a : Q8) :
    qmul (qmul qT (q8Coord a)) (qmul qT qT) =
      q8Coord (phi a) := by
  cases a with
  | mk k b => cases k <;> cases b <;>
    norm_num [qT, q8Coord, qmul, phi]

/-- The chosen qT has inverse qT^2 and conjugates Q8 exactly by phi. -/
theorem qTPow_conj_phi (x : C3) (a : Q8) :
    qmul (qmul (qTPow x) (q8Coord a)) (qTPow (invC3 x)) =
      q8Coord (phiPow x a) := by
  cases x with
  | g0 =>
    cases a with | mk k b => cases k <;> cases b <;>
      norm_num [qTPow, qone, q8Coord, qmul, phiPow, phi, invC3]
  | g1 =>
    cases a with | mk k b => cases k <;> cases b <;>
      norm_num [qTPow, qT, qone, q8Coord, qmul, phiPow, phi, invC3]
  | g2 =>
    cases a with | mk k b => cases k <;> cases b <;>
      norm_num [qTPow, qT, qone, q8Coord, qmul, phiPow, phi, invC3]

theorem qTPow_mul (x y : C3) :
    qmul (qTPow x) (qTPow y) = qTPow (mulC3 x y) := by
  cases x <;> cases y <;>
    norm_num [qTPow, qT, qone, qmul, mulC3]

/-- Transporting a Q8 element through the C3 power gives the semidirect action. -/
theorem qTPow_transport (x y : C3) (b : Q8) :
    qmul (qmul (qTPow x) (q8Coord b)) (qTPow y) =
      qmul (q8Coord (phiPow x b)) (qTPow (mulC3 x y)) := by
  cases x with
  | g0 => cases y <;> cases b with | mk k z => cases k <;> cases z <;>
      norm_num [qTPow, qone, qT, q8Coord, qmul, phiPow, phi, mulC3]
  | g1 => cases y <;> cases b with | mk k z => cases k <;> cases z <;>
      norm_num [qTPow, qone, qT, q8Coord, qmul, phiPow, phi, mulC3]
  | g2 => cases y <;> cases b with | mk k z => cases k <;> cases z <;>
      norm_num [qTPow, qone, qT, q8Coord, qmul, phiPow, phi, mulC3]

/-- RUNG 7 CAPSTONE: the finite semidirect product realizes as unit quaternions. -/
theorem btCoord_hom (p q : Q8 × C3) :
    btCoord (mulBT p q) = qmul (btCoord p) (btCoord q) := by
  obtain ⟨a, x⟩ := p
  obtain ⟨b, y⟩ := q
  change qmul (q8Coord (mul a (phiPow x b))) (qTPow (mulC3 x y)) =
    qmul (qmul (q8Coord a) (qTPow x)) (qmul (q8Coord b) (qTPow y))
  calc
    qmul (q8Coord (mul a (phiPow x b))) (qTPow (mulC3 x y)) =
        qmul (qmul (q8Coord a) (q8Coord (phiPow x b))) (qTPow (mulC3 x y)) := by
          rw [q8Coord_mul]
    _ = qmul (q8Coord a) (qmul (q8Coord (phiPow x b)) (qTPow (mulC3 x y))) :=
          qmul_assoc _ _ _
    _ = qmul (q8Coord a) (qmul (qmul (qTPow x) (q8Coord b)) (qTPow y)) := by
          rw [qTPow_transport]
    _ = qmul (q8Coord a) (qmul (qTPow x) (qmul (q8Coord b) (qTPow y))) := by
          rw [qmul_assoc]
    _ = qmul (qmul (q8Coord a) (qTPow x)) (qmul (q8Coord b) (qTPow y)) := by
          rw [qmul_assoc]

end
end FiniteSU2Envelope
