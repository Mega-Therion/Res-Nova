/-
  BinaryTetrahedral.lean — Pure Lean 4 Core
  Axiom budget: [propext, Classical.choice, Quot.sound] — Zero sorry, Pure Lean 4 Core

  THE Z/2 × Z/3 COMPOSITION, IN MINIATURE (2026-09-07).
  Requested by the author after PR #28's census left the question: are the
  crack route (Z/2 world: the double cover, order-4 survivors) and the
  generation route (Z/3 world: order-3 cycles, per GenerationCycleChirality)
  one structure seen at two orders, or genuinely two?

  THE ANSWER CONSTRUCTED HERE. The generation cycle ACTS on the crack's cover:
  there is an order-3 automorphism φ of Q8 cycling its three anticommuting
  pairs (i, j, k) = (n, r, n·r) ↦ (j, k, i). The composition is NOT the direct
  product — it is the SEMIDIRECT product Q8 ⋊ C₃, the binary tetrahedral group
  2T in miniature, the next finite subgroup of SU(2) after the crack's Q8.

  WHAT IS PROVED [P]:
    - φ: an explicit order-3 automorphism of the crack's Q8, cycling the three
      anticommuting pairs; multiplicative, order exactly 3.
    - The complete group laws of BT = Q8 ⋊ C₃ (associativity, identity,
      inverses) — derived from φ's multiplicativity, not from a table.
    - THE UNIQUE INVOLUTION: in the composed group the only element squaring
      to the identity, besides the identity, is the 2π sign — the residue
      remains the unique nontrivial involution.
    - The 2π sign remains CENTRAL in the composed group.
    - THE COMPOSITION CENSUS: the crack route survives with order exactly 4
      (square = the 2π sign); the generation route survives with order exactly
      3; THE COMPOSITION (crack survivor × generation survivor) has order
      EXACTLY 6 — and its CUBE is the 2π sign. The direct product would give
      order 12 (lcm(4,3)); the true composition COMPRESSES 12 into 6: one
      cyclic structure, not two. 6 = 2 × 3.

  WHAT IS NOT PROVED, TAGGED [O]:
    - That BT is the binary tetrahedral group, or that it sits inside SU(2)
      (the continuous envelope): the miniature cannot see continuity.
    - That the C₃ factor has anything to do with fermion generations: the
      identification of this cycle with a physical generation structure is
      an INTERPRETATION, not a theorem here (same boundary as
      GenerationCycleChirality.lean).
    - That A₄ = 2T/±1, or anything about the tetrahedron.

  Cross-references: BRANCHING_FROM_THE_INVARIANT.md (the cascade and its
  census), ChiralResidue.lean (the crack's cover, the frame-invariance pass,
  the cascade census), GenerationCycleChirality.lean (the order-3 route's
  non-involutivity), FIRST_PRINCIPLES_PHYSICS_MONOGRAPH.md (the triality line,
  honestly relabeled).
-/
import ChiralResidue

namespace BinaryTetrahedral

open ChiralResidue

/-! ## The generation cycle C₃ -/

/-- The abstract generation cycle of `GenerationCycleChirality.lean`, made
    concrete as a three-element group. -/
inductive C3 where
  | g0 | g1 | g2

def mulC3 : C3 → C3 → C3
  | .g0, x => x
  | x, .g0 => x
  | .g1, .g1 => .g2
  | .g1, .g2 => .g0
  | .g2, .g1 => .g0
  | .g2, .g2 => .g1

def invC3 : C3 → C3
  | .g0 => .g0
  | .g1 => .g2
  | .g2 => .g1

theorem mulC3_assoc (x y z : C3) :
    mulC3 (mulC3 x y) z = mulC3 x (mulC3 y z) := by
  cases x <;> cases y <;> cases z <;> rfl

theorem mulC3_left_inv (x : C3) : mulC3 (invC3 x) x = .g0 := by
  cases x <;> rfl

theorem mulC3_one (x : C3) : mulC3 x .g0 = x := by
  cases x <;> rfl

theorem mulC3_symm (x y : C3) : mulC3 x y = mulC3 y x := by
  cases x <;> cases y <;> rfl

/-! ## The order-3 automorphism of the crack's cover -/

/-- φ: the automorphism of the crack's Q8 cycling the three anticommuting
    pairs. The quaternion triple here is i = n, j = r, k = n·r = ⟨r3, true⟩
    (j·k = i and k·i = j are rfl). φ fixes the center ±1 and sends
    i ↦ j ↦ k ↦ i. -/
def phi : Q8 → Q8
  | ⟨R4.r0, false⟩ => ⟨R4.r0, false⟩   --   1 ↦  1
  | ⟨R4.r2, false⟩ => ⟨R4.r2, false⟩   --  −1 ↦ −1
  | ⟨R4.r0, true⟩  => ⟨R4.r1, false⟩   --   i ↦  j
  | ⟨R4.r1, false⟩ => ⟨R4.r3, true⟩    --   j ↦  k
  | ⟨R4.r3, true⟩  => ⟨R4.r0, true⟩    --   k ↦  i
  | ⟨R4.r2, true⟩  => ⟨R4.r3, false⟩   --  −i ↦ −j
  | ⟨R4.r3, false⟩ => ⟨R4.r1, true⟩    --  −j ↦ −k
  | ⟨R4.r1, true⟩  => ⟨R4.r2, true⟩    --  −k ↦ −i

/-- φ is a homomorphism. -/
theorem phi_mul (a b : Q8) : phi (mul a b) = mul (phi a) (phi b) := by
  cases a with | mk ka ba =>
    cases b with | mk kb bb =>
      cases ka <;> cases ba <;> cases kb <;> cases bb <;> rfl

/-- φ has order exactly 3. -/
theorem phi_three (a : Q8) : phi (phi (phi a)) = a := by
  cases a with | mk k b => cases k <;> cases b <;> rfl

/-- The cycle fixes the 2π sign — the residue is cycle-invariant. -/
theorem phi_two_pi : phi minusOne = minusOne := rfl

/-- The powers of φ, indexed by the generation cycle. -/
def phiPow : C3 → Q8 → Q8
  | .g0 => fun a => a
  | .g1 => phi
  | .g2 => fun a => phi (phi a)

theorem phiPow_two_pi (x : C3) : phiPow x minusOne = minusOne := by
  cases x <;> rfl

theorem phiPow_one (x : C3) : phiPow x one = one := by
  cases x <;> rfl

theorem phi_pow_mul (x : C3) (b c : Q8) :
    phiPow x (mul b c) = mul (phiPow x b) (phiPow x c) := by
  cases x with
  | g0 => rfl
  | g1 => exact phi_mul b c
  | g2 =>
    show phi (phi (mul b c)) = mul (phi (phi b)) (phi (phi c))
    rw [phi_mul, phi_mul]

theorem phi_pow_pow (x y : C3) (a : Q8) :
    phiPow x (phiPow y a) = phiPow (mulC3 x y) a := by
  cases x with
  | g0 => rfl
  | g1 =>
    cases y with
    | g0 => rfl
    | g1 => rfl
    | g2 => exact phi_three a
  | g2 =>
    cases y with
    | g0 => rfl
    | g1 => exact phi_three a
    | g2 =>
      show phi (phi (phi (phi a))) = phi a
      rw [phi_three]

/-! ## The composed group: the crack's cover, semidirect the cycle -/

/-- BT: the binary tetrahedral miniature. The crack's cover Q8, with the
    generation cycle C₃ acting through φ. -/
def mulBT : Q8 × C3 → Q8 × C3 → Q8 × C3
  | (a, x), (b, y) => (mul a (phiPow x b), mulC3 x y)

def oneBT : Q8 × C3 := (one, C3.g0)

def invBT : Q8 × C3 → Q8 × C3
  | (a, x) => (phiPow (invC3 x) (inv a), invC3 x)

theorem mulBT_assoc (s t u : Q8 × C3) :
    mulBT (mulBT s t) u = mulBT s (mulBT t u) := by
  obtain ⟨a, x⟩ := s
  obtain ⟨b, y⟩ := t
  obtain ⟨c, z⟩ := u
  simp only [mulBT, Prod.mk.injEq]
  refine ⟨?_, ?_⟩
  · rw [mul_assoc, phi_pow_mul, phi_pow_pow]
  · exact mulC3_assoc x y z

theorem oneBT_mul (s : Q8 × C3) : mulBT oneBT s = s := by
  obtain ⟨a, x⟩ := s
  simp only [mulBT, oneBT, Prod.mk.injEq]
  exact ⟨one_mul a, rfl⟩

theorem mulBT_one (s : Q8 × C3) : mulBT s oneBT = s := by
  obtain ⟨a, x⟩ := s
  simp only [mulBT, oneBT, Prod.mk.injEq]
  refine ⟨?_, ?_⟩
  · rw [phiPow_one]; exact mul_one a
  · exact mulC3_one x

theorem mulBT_left_inv (s : Q8 × C3) : mulBT (invBT s) s = oneBT := by
  obtain ⟨a, x⟩ := s
  simp only [mulBT, invBT, oneBT, Prod.mk.injEq]
  refine ⟨?_, ?_⟩
  · rw [← phi_pow_mul, mul_left_inv, phiPow_one]
  · exact mulC3_left_inv x

/-! ## What the composition preserves -/

/-- The 2π sign remains central in the composed group. -/
theorem bt_two_pi_central (s : Q8 × C3) :
    mulBT (minusOne, C3.g0) s = mulBT s (minusOne, C3.g0) := by
  obtain ⟨a, x⟩ := s
  simp only [mulBT, Prod.mk.injEq]
  refine ⟨?_, ?_⟩
  · rw [phiPow_two_pi, central_two_pi_commutes]; rfl
  · exact mulC3_symm C3.g0 x

/-- THE UNIQUE INVOLUTION: in the composed group, the only elements squaring
    to the identity are the identity and the 2π sign. The residue remains
    the unique nontrivial involution — the composition did not create new
    orientation-blind structure. -/
theorem bt_unique_involution (s : Q8 × C3) (h : mulBT s s = oneBT) :
    s = oneBT ∨ s = (minusOne, C3.g0) := by
  obtain ⟨a, x⟩ := s
  cases x with
  | g0 =>
    cases a with | mk k b =>
      cases k <;> cases b <;> first
        | (left; rfl)
        | (right; rfl)
        | nomatch h
  | g1 =>
    simp only [mulBT, oneBT, Prod.mk.injEq] at h
    exact nomatch h.2
  | g2 =>
    simp only [mulBT, oneBT, Prod.mk.injEq] at h
    exact nomatch h.2

/-! ## The composition census -/

/-- THE COMPOSITION CENSUS. All three survivor routes live in ONE group:
    BT = Q8 ⋊ C₃.

    The crack route: (n, g0), order exactly 4 — its square is the 2π sign.
    The generation route: (one, g1), order exactly 3.
    THE COMPOSITION: (n, g1), order exactly 6 — divisors 1, 2, 3 are
    excluded — and its CUBE is the 2π sign.

    The direct product would give order lcm(4, 3) = 12. The true
    composition COMPRESSES 12 into 6: one cyclic structure, not two.
    6 = 2 × 3 — the crack's notch and the generation cycle, composed,
    are a single Z/6 whose cube is the residue. -/
theorem composition_census :
    (mulBT (n, C3.g0) (n, C3.g0) = (minusOne, C3.g0)
      ∧ mulBT (mulBT (n, C3.g0) (n, C3.g0)) (mulBT (n, C3.g0) (n, C3.g0)) = oneBT
      ∧ (n, C3.g0) ≠ oneBT)
    ∧ (mulBT (mulBT (one, C3.g1) (one, C3.g1)) (one, C3.g1) = oneBT
      ∧ mulBT (one, C3.g1) (one, C3.g1) ≠ oneBT
      ∧ (one, C3.g1) ≠ oneBT)
    ∧ (mulBT (mulBT (mulBT (n, C3.g1) (n, C3.g1)) (n, C3.g1))
        (mulBT (mulBT (n, C3.g1) (n, C3.g1)) (n, C3.g1)) = oneBT
      ∧ mulBT (mulBT (n, C3.g1) (n, C3.g1)) (n, C3.g1) = (minusOne, C3.g0)
      ∧ mulBT (n, C3.g1) (n, C3.g1) ≠ oneBT
      ∧ (n, C3.g1) ≠ oneBT) := by
  refine ⟨⟨rfl, rfl, ?_⟩, ⟨rfl, ?_, ?_⟩, ⟨rfl, rfl, ?_, ?_⟩⟩
  all_goals exact fun h => nomatch h

end BinaryTetrahedral
