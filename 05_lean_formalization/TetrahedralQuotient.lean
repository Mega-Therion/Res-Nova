/-
  TetrahedralQuotient.lean — Pure Lean 4 Core
  Axiom budget: [propext, Classical.choice, Quot.sound] — Zero sorry, Pure Lean 4 Core

  THE SHADOW OF THE SIGN: 2T MODULO THE 2π ROTATION (2026-09-07).
  The composition (PR #29) left one fact hanging: A₄ is 2T's quotient by
  the very sign that is still central. This module constructs the quotient
  in miniature and reads its census.

  The 2π sign is invisible downstairs — the whole corpus says so, and
  PR #27 proved the forward and reverse crack act identically on the
  chiral space. HERE is what that means structurally: mod out by the
  sign, and the crack MERGES WITH ITS REVERSE into a single object.
  The quotient map is the shadow the chiral plane can actually see.

  WHAT IS PROVED [P]:
    - proj: Q8 → V₄ (the Klein four) is a homomorphism; its classes are
      ±1, ±r, ±n (the crack!), ±nr — and multiplying by the 2π sign
      changes NOTHING downstairs (two_pi_invisible).
    - THE SHADOW IS A HOMOMORPHISM: shadow : BT = Q8 ⋊ C₃ → V₄ ⋊ C₃
      respects the multiplication; the quotient's complete group laws
      are INHERITED through the section (the standard descent argument,
      done in miniature — no fresh tables).
    - THE KERNEL IS EXACTLY THE SIGN: the only elements the shadow kills
      are the identity and the 2π rotation. The residue is the WHOLE
      kernel — modding out loses nothing else.
    - THE CRACK MERGES WITH ITS REVERSE: proj n = proj (inv n) —
      downstairs, the mirror and its inverse are ONE object.
    - THE TETRAHEDRAL CENSUS: every element of the quotient has order
      1, 2, or 3 — no element of order 6, 4, or 12 exists; the
      involutions are EXACTLY THREE — the classes of ±r, ±n, ±rn —
      plus the identity: 1 + 3 + 8. This is the conjugacy-class census
      of A₄: the rotation classes of the tetrahedron.
    - THE THREE DIRECTIONS ARE ANONYMOUS: the generation element
      conjugates the three involutions in a single orbit (a → c → b → a).
      No direction is preferred; the choice of crack axis is gauge,
      not structure.

  WHAT IS NOT PROVED, TAGGED [O]:
    - That the 12-element census group IS A₄, or the rotation group of
      the tetrahedron: the identification is interpretation. What is
      proved is the census 1 + 3 + 8 and the conjugacy orbit.
    - Any physics: the reading of the quotient as "what the chiral
      plane sees", the Stiefel-substrate echo, the generation
      identification — all [O], as always.
    - Note for the trunk: DOWNSTAIRS the crack IS an involution — the
      involution-kill WOULD apply there. The escape lives entirely in
      the cover, exactly as the PR #27 census said.

  Cross-references: BinaryTetrahedral.lean (the composition), ChiralResidue.lean
  (the crack, the reverse-loop theorems, the cascade census), BRANCHING_FROM_
  THE_INVARIANT.md (the trunk), FIRST_PRINCIPLES_PHYSICS_MONOGRAPH.md (the
  triality line, honestly relabeled).
-/
import BinaryTetrahedral

namespace TetrahedralQuotient

open ChiralResidue BinaryTetrahedral

/-! ## V₄: the Klein four, Q8 with the sign modded out -/

/-- The quotient Q8/±1, concretely: the four cosets.
    e = ±1, a = ±r, b = ±n (the crack's class), c = ±nr. -/
inductive V4 where
  | e | a | b | c

def mulV4 : V4 → V4 → V4
  | .e, v => v
  | v, .e => v
  | .a, .a => .e | .a, .b => .c | .a, .c => .b
  | .b, .a => .c | .b, .b => .e | .b, .c => .a
  | .c, .a => .b | .c, .b => .a | .c, .c => .e

/-- The coset map: the shadow Q8 casts on V₄. -/
def proj : Q8 → V4
  | ⟨R4.r0, false⟩ => .e
  | ⟨R4.r2, false⟩ => .e
  | ⟨R4.r1, false⟩ => .a
  | ⟨R4.r3, false⟩ => .a
  | ⟨R4.r0, true⟩  => .b
  | ⟨R4.r2, true⟩  => .b
  | ⟨R4.r1, true⟩  => .c
  | ⟨R4.r3, true⟩  => .c

/-- proj is a homomorphism. -/
theorem proj_mul (a b : Q8) :
    proj (mul a b) = mulV4 (proj a) (proj b) := by
  cases a with | mk ka ba =>
    cases b with | mk kb bb =>
      cases ka <;> cases ba <;> cases kb <;> cases bb <;> rfl

/-- Multiplying by the 2π sign changes NOTHING downstairs. THE 2π
    PROBLEM, STATED AS A PROJECTION LAW. -/
theorem two_pi_invisible (q : Q8) :
    proj (mul minusOne q) = proj q := by
  cases q with | mk k b => cases k <;> cases b <;> rfl

/-! ## The cycle's action descends -/

/-- φ̄: the generation cycle's action, induced on the cosets.
    It cycles the three non-identity cosets: a ↦ c ↦ b ↦ a. -/
def phibar : V4 → V4
  | .e => .e
  | .a => .c
  | .c => .b
  | .b => .a

/-- The induced action is a homomorphism of V₄. -/
theorem phibar_mul (v w : V4) :
    phibar (mulV4 v w) = mulV4 (phibar v) (phibar w) := by
  cases v <;> cases w <;> rfl

/-- φ descends: the coset of φ q is φ̄ of the coset of q. -/
theorem proj_phi (q : Q8) : proj (phi q) = phibar (proj q) := by
  cases q with | mk k b => cases k <;> cases b <;> rfl

def phibarPow : C3 → V4 → V4
  | .g0 => fun v => v
  | .g1 => phibar
  | .g2 => fun v => phibar (phibar v)

theorem proj_phiPow (x : C3) (q : Q8) :
    proj (phiPow x q) = phibarPow x (proj q) := by
  cases x with
  | g0 => rfl
  | g1 => cases q with | mk k b => cases k <;> cases b <;> rfl
  | g2 => cases q with | mk k b => cases k <;> cases b <;> rfl

/-! ## The shadow: BT → the quotient -/

def mulAQ : V4 × C3 → V4 × C3 → V4 × C3
  | (v, x), (w, y) => (mulV4 v (phibarPow x w), mulC3 x y)

def oneAQ : V4 × C3 := (V4.e, C3.g0)

/-- The quotient map: the shadow the chiral plane can actually see. -/
def shadow : Q8 × C3 → V4 × C3
  | (q, x) => (proj q, x)

/-- A section: lift each coset to a chosen representative. -/
def rep : V4 → Q8
  | .e => one
  | .a => r
  | .b => n
  | .c => mul n r

def lift : V4 × C3 → Q8 × C3
  | (v, x) => (rep v, x)

theorem proj_rep (v : V4) : proj (rep v) = v := by
  cases v <;> rfl

theorem shadow_lift (p : V4 × C3) : shadow (lift p) = p := by
  obtain ⟨v, x⟩ := p
  simp only [shadow, lift]
  rw [proj_rep]

/-- THE SHADOW IS A HOMOMORPHISM. -/
theorem shadow_hom (s t : Q8 × C3) :
    shadow (mulBT s t) = mulAQ (shadow s) (shadow t) := by
  obtain ⟨q, x⟩ := s
  obtain ⟨q', y⟩ := t
  simp only [shadow, mulBT, mulAQ, Prod.mk.injEq]
  refine ⟨?_, trivial⟩
  rw [proj_mul, proj_phiPow]

def invAQ (p : V4 × C3) : V4 × C3 := shadow (invBT (lift p))

/-! ## The quotient inherits the group laws -/

theorem mulAQ_assoc (p q r : V4 × C3) :
    mulAQ (mulAQ p q) r = mulAQ p (mulAQ q r) := by
  rw [← shadow_lift p, ← shadow_lift q, ← shadow_lift r,
      ← shadow_hom, ← shadow_hom, mulBT_assoc, shadow_hom, shadow_hom]

theorem oneAQ_mul (p : V4 × C3) : mulAQ oneAQ p = p := rfl

theorem mulAQ_one (p : V4 × C3) : mulAQ p oneAQ = p := by
  obtain ⟨v, x⟩ := p
  cases v <;> cases x <;> rfl

theorem mulAQ_left_inv (p : V4 × C3) : mulAQ (invAQ p) p = oneAQ := by
  obtain ⟨v, x⟩ := p
  cases v <;> cases x <;> rfl

/-! ## What the shadow sees -/

/-- THE KERNEL IS EXACTLY THE SIGN: the only elements the shadow kills
    are the identity and the 2π rotation. The residue is the WHOLE
    kernel — modding out loses nothing else. -/
theorem kernel_is_the_sign (s : Q8 × C3) :
    shadow s = oneAQ ↔ s = oneBT ∨ s = (minusOne, C3.g0) := by
  obtain ⟨q, x⟩ := s
  cases x with
  | g0 =>
    cases q with | mk k b =>
      cases k <;> cases b <;> first
        | exact ⟨(fun _ => Or.inl rfl), (fun _ => rfl)⟩
        | exact ⟨(fun _ => Or.inr rfl), (fun _ => rfl)⟩
        | exact ⟨(fun h => nomatch h),
                 (fun h => Or.elim h (fun h' => nomatch h') (fun h' => nomatch h'))⟩
  | g1 =>
    constructor
    · intro h
      simp only [shadow, oneAQ, Prod.mk.injEq] at h
      exact nomatch h.2
    · intro h
      rcases h with h | h <;> exact nomatch h
  | g2 =>
    constructor
    · intro h
      simp only [shadow, oneAQ, Prod.mk.injEq] at h
      exact nomatch h.2
    · intro h
      rcases h with h | h <;> exact nomatch h

/-- THE CRACK MERGES WITH ITS REVERSE: downstairs, the mirror and its
    inverse are ONE object — the involution class b. PR #27 proved they
    ACT identically on the chiral space; here they are literally equal
    in the shadow. -/
theorem crack_merges_with_its_reverse :
    proj (inv n) = proj n := rfl

/-! ## The tetrahedral census -/

/-- THE TETRAHEDRAL CENSUS: every element of the quotient has order
    1, 2, or 3. There is no element of order 6, no order 4, no order
    12 — the order-census of A₄, the rotation classes of the
    tetrahedron: identity, three half-turns, eight vertex-turns. -/
theorem tetrahedral_census (p : V4 × C3) :
    p = oneAQ ∨ mulAQ p p = oneAQ ∨ mulAQ p (mulAQ p p) = oneAQ := by
  obtain ⟨v, x⟩ := p
  cases v <;> cases x <;> first
    | (left; rfl)
    | (right; left; rfl)
    | (right; right; rfl)

/-- The involutions are EXACTLY the identity and the three classes
    ±r, ±n (the crack), ±rn — nothing else squares to the identity. -/
theorem involutions_exhausted (p : V4 × C3) (h : mulAQ p p = oneAQ) :
    p = oneAQ ∨ p = (V4.a, C3.g0) ∨ p = (V4.b, C3.g0) ∨ p = (V4.c, C3.g0) := by
  obtain ⟨v, x⟩ := p
  cases v <;> cases x <;> first
    | (left; rfl)
    | (right; left; rfl)
    | (right; right; left; rfl)
    | (right; right; right; rfl)
    | nomatch h

/-- THE THREE DIRECTIONS ARE ANONYMOUS: the generation element conjugates
    the three involutions in a single orbit (a → c → b → a). No
    direction is preferred; which coset the crack lives in is gauge,
    not structure. -/
theorem directions_anonymous :
    mulAQ (mulAQ (V4.e, C3.g1) (V4.a, C3.g0)) (invAQ (V4.e, C3.g1)) = (V4.c, C3.g0)
    ∧ mulAQ (mulAQ (V4.e, C3.g1) (V4.c, C3.g0)) (invAQ (V4.e, C3.g1)) = (V4.b, C3.g0)
    ∧ mulAQ (mulAQ (V4.e, C3.g1) (V4.b, C3.g0)) (invAQ (V4.e, C3.g1)) = (V4.a, C3.g0) :=
  ⟨rfl, rfl, rfl⟩

end TetrahedralQuotient
