/-
  ChiralResidue.lean

  THE WEAK RESIDUE — first formalization pass at promotion-path item (b) of
  the book manuscript section "The Chiral Crack: The Holonomic Loop and the
  Symmetry-Breaking Moment": derive the structure of maximal parity
  violation from the orientation-reversing holonomy instead of inserting it.

  Tag: [O] — open, conjectural, motivational for the physical reading. The
  theorems are structural facts about the pin double cover; they certify no
  physical ontology and upgrade nothing in the manuscript's claim registry.

  What is actually derived here (and what is NOT):

    (A) THE BRIDGE: in the pin double cover, the square of the reflection IS
        the full 2π rotation (n² = r² = the central element). The chiral
        mirror of ChiralCrackSketch and the spinor's sign flip are two faces
        of one central element. [proved]
    (B) PARITY ACTS AS SENSE-REVERSAL: the reflection conjugates every
        rotation to its inverse (n r n⁻¹ = r⁻¹) — and ANY reflection
        conjugates ANY rotation to its inverse (conj_inverts_general).
        The cover is non-abelian: the mirror ANTICOMMUTES with the
        quarter-turn (n r = (r n)·(−1)), while the central 2π rotation
        commutes with everything. [proved]
    (C) MAXIMALITY AS STRUCTURE: handedness change under the pin group is
        BINARY. Every element either preserves handedness at every point of
        the chiral space or reverses it at every point. No element is
        partially parity-violating: a coupling that sees the reflection
        sector at all, sees it totally. "Maximal rather than partial" is a
        dichotomy of the double cover, not a tuned parameter. The cover is moreover GRADED by parity: the
        rotation sector is a subgroup, the reflection sector is its single
        coset, and the two exhaust the group — the dichotomy is the entire
        group cut into exactly two pieces. [proved — this is the
        qualitative core of item (b); it does NOT yet derive the SU(2)_L
        gauge group itself]
    (D) The reflection sector of the pin group acts on the chiral space
        exactly as the IsReflection holonomies of ChiralCrackSketch.lean.
        [proved]

  What remains open for item (b): the derivation of the SU(2) gauge
  structure (as opposed to the maximality dichotomy) from the cover, the
  chiral partner model of §7, and the coupling scale against the
  Chern–Simons parameter space of §9.

  The witness group is Pin⁻ of the plane, realized as the quaternion group
  Q8 (r = i the quarter-turn, n = j the reflection). Pure Lean 4 core.
  No Mathlib, no sorry. Companion to ChiralCrackSketch.lean (the order-2
  mirror side) and ChiralHolonomyOrientation.lean (the reversal clause).
-/

import ChiralCrackSketch

namespace ChiralResidue

/-! ### The pin double cover of the plane, as Q8 -/

/-- Rotation exponents of the cover: Z/4 on four constructors. -/
inductive R4 where
  | r0 | r1 | r2 | r3
deriving DecidableEq, Repr

/-- Mod-4 addition of rotation exponents. -/
def R4.add : R4 → R4 → R4
  | .r0, x => x
  | x, .r0 => x
  | .r1, .r1 => .r2
  | .r1, .r2 => .r3
  | .r1, .r3 => .r0
  | .r2, .r1 => .r3
  | .r2, .r2 => .r0
  | .r2, .r3 => .r1
  | .r3, .r1 => .r0
  | .r3, .r2 => .r1
  | .r3, .r3 => .r2

/-- Negation of exponents (reversal of rotation sense). -/
def R4.neg : R4 → R4
  | .r0 => .r0
  | .r1 => .r3
  | .r2 => .r2
  | .r3 => .r1

/-- Pin⁻ of the plane, realized as the quaternion group: a rotation
    exponent in Z/4 (the double cover of the rotation sector) and a
    reflection parity. -/
structure Q8 where
  rot : R4
  ref : Bool
deriving DecidableEq, Repr

/-- Group operation of the cover. -/
def mul : Q8 → Q8 → Q8
  | ⟨k1, false⟩, ⟨k2, e2⟩ => ⟨R4.add k1 k2, e2⟩
  | ⟨k1, true⟩, ⟨k2, false⟩ => ⟨R4.add k1 (R4.neg k2), true⟩
  | ⟨k1, true⟩, ⟨k2, true⟩ => ⟨R4.add (R4.add k1 (R4.neg k2)) R4.r2, false⟩

/-- The identity: no rotation, no reflection. -/
def one : Q8 := ⟨.r0, false⟩

/-- The quarter-turn r = i. -/
def r : Q8 := ⟨.r1, false⟩

/-- The central element −1 = i²: the 2π rotation — trivial downstairs,
    sign above. -/
def minusOne : Q8 := ⟨.r2, false⟩

/-- The reflection n = j. -/
def n : Q8 := ⟨.r0, true⟩

/-- Inverses in the cover. -/
def inv : Q8 → Q8
  | ⟨k, false⟩ => ⟨R4.neg k, false⟩
  | ⟨k, true⟩ => ⟨R4.add k R4.r2, true⟩

/-! ### Group facts (exhaustive case analysis; finite witness) -/

theorem mul_assoc (a b c : Q8) : mul (mul a b) c = mul a (mul b c) := by
  cases a with | mk k1 b1 => cases b with | mk k2 b2 => cases c with | mk k3 b3 =>
    cases k1 <;> cases b1 <;> cases k2 <;> cases b2 <;> cases k3 <;> cases b3 <;> rfl

theorem one_mul (a : Q8) : mul one a = a := rfl

theorem mul_one (a : Q8) : mul a one = a := by
  cases a with | mk k b => cases k <;> cases b <;> rfl

theorem mul_left_inv (a : Q8) : mul (inv a) a = one := by
  cases a with | mk k b => cases k <;> cases b <;> rfl

theorem mul_right_inv (a : Q8) : mul a (inv a) = one := by
  cases a with | mk k b => cases k <;> cases b <;> rfl

/-- Taking inverses twice returns the element. -/
theorem inv_involutive (a : Q8) : inv (inv a) = a := by
  cases a with | mk k b => cases k <;> cases b <;> rfl

/-- PARITY IS A HOMOMORPHISM to Z/2: the sector of a product is the XOR
    of the sectors. Two reflections compose to a rotation; a reflection
    composed with a rotation is a reflection. The two sectors partition
    the cover multiplicatively — this is what makes "which sector" a
    well-defined property of a coupling. -/
theorem parity_hom (a b : Q8) : (mul a b).ref = (a.ref != b.ref) := by
  cases a with | mk k1 b1 => cases b with | mk k2 b2 =>
    cases k1 <;> cases b1 <;> cases k2 <;> cases b2 <;> rfl

/-! ### (A) The bridge: the mirror's square is the 2π rotation -/

/-- r² = −1: the 2π rotation is the central element. -/
theorem r_sq : mul r r = minusOne := rfl

/-- n² = −1: the mirror squares to the same central element. -/
theorem n_sq : mul n n = minusOne := rfl

/-- THE BRIDGE: in the pin double cover, squaring the mirror IS the full
    rotation. The chiral reflection of ChiralCrackSketch and the spinor's
    sign flip are two faces of one central element. -/
theorem mirror_square_is_full_rotation : mul n n = mul r r := rfl

/-- In the cover, the 2π rotation does not return the state (−ψ): it
    carries the quarter-turn state to its negative. -/
theorem two_pi_moves_the_state : mul minusOne r = inv r := rfl

/-- The 4π rotation returns the state. -/
theorem four_pi_returns_the_state : mul minusOne (mul minusOne r) = r := rfl

/-! ### (B) Parity acts on the rotation sector by sense-reversal -/

/-- n r n⁻¹ = r⁻¹: the reflection conjugates the quarter-turn to its
    inverse — reflection reverses the sense of rotation. -/
theorem conj_inverts_r : mul (mul n r) (inv n) = inv r := rfl

/-- The reflection conjugates EVERY rotation to its inverse: parity acts
    on the rotation sector as reversal of sense. -/
theorem conj_inverts_rotations (k : R4) :
    mul (mul n ⟨k, false⟩) (inv n) = inv ⟨k, false⟩ := by
  cases k <;> rfl

/-- ANY reflection conjugates ANY rotation to its inverse: parity's
    sense-reversal action does not depend on which mirror, or on which
    rotation it acts on. The maximal-dichotomy reading of (C) is
    representation-independent. -/
theorem conj_inverts_general (t s : Q8) (ht : t.ref = true)
    (hs : s.ref = false) : mul (mul t s) (inv t) = inv s := by
  cases t with
  | mk kt bt =>
    cases s with
    | mk ks bs =>
      cases bt with
      | false => exact nomatch ht
      | true =>
        cases bs with
        | true => exact nomatch hs
        | false => cases kt <;> cases ks <;> rfl

/-- The cover is NON-ABELIAN: the mirror does not commute with the
    quarter-turn. -/
theorem non_abelian : mul n r ≠ mul r n := by
  intro h; nomatch h

/-- More: the mirror ANTICOMMUTES with the quarter-turn — n r = (r n)·(−1).
    The reflection reverses the rotation's sense AND flips the cover's
    sign. This is the double cover's version of "mirror × rotation =
    inverse rotation × mirror." -/
theorem anticommutation : mul n r = mul (mul r n) minusOne := rfl

/-- The central 2π rotation commutes with everything: −1 is in the
    center of the cover. Downstairs it is invisible; upstairs it is the
    sign — which is exactly why the cover sees what the plane cannot. -/
theorem central_two_pi_commutes (a : Q8) :
    mul minusOne a = mul a minusOne := by
  cases a with | mk k b => cases k <;> cases b <;> rfl

/-! ### (C) The residue on the chiral space: handedness change is binary -/

open ChiralCrack

/-- The pin group acts on the chiral space: the rotation sector preserves
    handedness, the reflection sector mirrors it. -/
def act : Q8 → Hand → Hand
  | ⟨_, false⟩, h => h
  | ⟨_, true⟩, h => ChiralCrack.flip h

/-- Rotations preserve handedness at every point. -/
theorem rotations_preserve (g : Q8) (hg : g.ref = false) (h : Hand) :
    act g h = h := by
  cases g with
  | mk k b =>
    cases b with
    | false => rfl
    | true => nomatch hg

/-- Reflections reverse handedness at every point. -/
theorem reflections_reverse (g : Q8) (hg : g.ref = true) (h : Hand) :
    act g h = ChiralCrack.flip h := by
  cases g with
  | mk k b =>
    cases b with
    | false => nomatch hg
    | true => rfl

/-- MAXIMALITY AS STRUCTURE: handedness change under the pin group is
    binary — every element either preserves handedness at every point or
    reverses it at every point. There is no partially parity-violating
    coupling: the dichotomy is total, per element, per sector. -/
theorem parity_violation_is_binary (g : Q8) :
    (∀ h : Hand, act g h = h) ∨ (∀ h : Hand, act g h = ChiralCrack.flip h) := by
  cases g with
  | mk k b =>
    cases b with
    | false => exact Or.inl (fun h => rfl)
    | true => exact Or.inr (fun h => rfl)

/-! ### (D) The reflection sector realizes the ChiralCrack holonomies -/

/-- Every reflection-sector element acts on the chiral space exactly as
    the IsReflection holonomies of ChiralCrackSketch.lean. -/
theorem reflection_sector_is_reflection (g : Q8) (hg : g.ref = true) :
    ChiralCrack.IsReflection (act g) := by
  show ∀ h : Hand, act g h = ChiralCrack.flip h
  cases g with
  | mk k b =>
    cases b with
    | false => nomatch hg
    | true => intro h; rfl

/-! ### The sector grading: the cover is a group graded by parity -/

/-- The rotation sector is closed under composition — derived from the
    parity homomorphism, not from the multiplication table. -/
theorem rotation_sector_closed (a b : Q8) (ha : a.ref = false)
    (hb : b.ref = false) : (mul a b).ref = false := by
  rw [parity_hom a b, ha, hb]; rfl

/-- Two reflections compose to a rotation — again from the homomorphism.
    This is the structural reason a parity-violating coupling cannot be
    "double-counted": the reflection sector is not closed. -/
theorem reflections_compose_to_rotation (a b : Q8) (ha : a.ref = true)
    (hb : b.ref = true) : (mul a b).ref = false := by
  rw [parity_hom a b, ha, hb]; rfl

/-- The rotation sector is closed under inverses: it is a subgroup. -/
theorem rotation_sector_inv_closed (a : Q8) (ha : a.ref = false) :
    (inv a).ref = false := by
  cases a with
  | mk k b =>
    cases b with
    | false => rfl
    | true => nomatch ha

/-- THE COSET FACT: every reflection is a rotation composed with the
    distinguished mirror n. The reflection sector is a SINGLE coset of
    the rotation sector — the group is graded by parity: one subgroup,
    one coset, nothing else. -/
theorem reflection_sector_is_coset (t : Q8) (ht : t.ref = true) :
    t = mul ⟨t.rot, false⟩ n := by
  cases t with
  | mk k b =>
    cases b with
    | false => nomatch ht
    | true => cases k <;> rfl

/-- EXHAUSTIVENESS: every element lies in one of the two sectors. -/
theorem sector_exhaustive (a : Q8) : a.ref = false ∨ a.ref = true := by
  cases a with
  | mk k b =>
    cases b with
    | false => exact Or.inl rfl
    | true => exact Or.inr rfl

end ChiralResidue
