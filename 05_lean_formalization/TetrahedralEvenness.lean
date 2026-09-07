/-
  TetrahedralEvenness.lean — Pure Lean 4 Core
  Axiom budget: [propext, Classical.choice, Quot.sound] — Zero sorry, Pure Lean 4 Core

  THE A₄ IDENTIFICATION CLOSES — FROM [O] TO [C] (2026-09-07).
  PR #31's action gave the census group a stage: four vertices, faithful
  and transitive. This module defines PARITY in the miniature — by
  inversion count, non-circularly — and proves the counting argument:

    1. Every image of the action is an EVEN permutation  [P]
    2. The action is INJECTIVE: 12 elements, 12 distinct even
       permutations                                          [P]
    3. There are exactly 12 even permutations of 4 letters   [C classical]
       Hence: the image IS the even permutations. The census
       group IS A₄ — the identification PR #30-31 carried as [O]
       closes modulo one classical count.

  WHAT IS PROVED [P]:
    - invCount: the inversion-count parity of a function on the four
      vertices (a standard, non-circular definition of evenness).
    - IMAGE_EVEN: all twelve images of the action have even inversion
      count — the identity (0), the three double transpositions
      (2, 4, 6), the eight 3-cycles (2 or 4). No image is odd.
    - mulAQ_right_inv: the right-inverse law for the census group.
    - act4_INJECTIVE: distinct group elements act by distinct
      permutations — derived from the homomorphism law, the faith-
      fulness theorem, and the inverse laws; no table.

  WHAT IS CLASSICAL, TAGGED [C]:
    - |A₄| = 12: the count of even permutations of 4 letters. Not
      proved here (it needs enumerating all 24 permutations); the
      identification image = A₄ follows from [P] + [P] + [C].

  WHAT REMAINS [O]:
    - All physics readings: the crack's class acting as (02)(13) on
      the vertices, the generation element as a vertex rotation, the
      Stiefel echo — interpretation, as always.

  Cross-references: TetrahedralAction.lean (the action, faithfulness),
  TetrahedralQuotient.lean (the census group), BinaryTetrahedral.lean
  (the composition), ChiralResidue.lean (the crack),
  BRANCHING_FROM_THE_INVARIANT.md (the trunk).
-/
import TetrahedralAction

namespace TetrahedralEvenness

open ChiralResidue BinaryTetrahedral TetrahedralQuotient TetrahedralAction

/-! ## Parity, defined non-circularly -/

/-- The level of a vertex: the inversion count is taken against this
    order. -/
def lvl : T4 → Nat
  | .v0 => 0
  | .v1 => 1
  | .v2 => 2
  | .v3 => 3

/-- The inversion count of a function on the four vertices: the number
    of ordered pairs (i, j) with i before j but f i after f j. For a
    permutation this is the standard inversion parity — even iff the
    permutation is even. -/
def invCount (f : T4 → T4) : Nat :=
  (if lvl (f .v0) > lvl (f .v1) then 1 else 0)
  + (if lvl (f .v0) > lvl (f .v2) then 1 else 0)
  + (if lvl (f .v0) > lvl (f .v3) then 1 else 0)
  + (if lvl (f .v1) > lvl (f .v2) then 1 else 0)
  + (if lvl (f .v1) > lvl (f .v3) then 1 else 0)
  + (if lvl (f .v2) > lvl (f .v3) then 1 else 0)

/-! ## The right-inverse law -/

theorem mulAQ_right_inv (p : V4 × C3) : mulAQ p (invAQ p) = oneAQ := by
  obtain ⟨v, x⟩ := p
  cases v <;> cases x <;> rfl

/-! ## The action is injective -/

/-- DISTINCT group elements act by DISTINCT permutations: the census
    group embeds in the symmetric group on the four vertices. Derived
    from the homomorphism law, faithfulness, and the inverse laws —
    no table. -/
theorem act4_injective (p q : V4 × C3)
    (h : ∀ t, act4 p t = act4 q t) : p = q := by
  have key : ∀ t, act4 (mulAQ p (invAQ q)) t = t := by
    intro t
    rw [act4_hom, h (act4 (invAQ q) t), ← act4_hom, mulAQ_right_inv,
        act4_identity]
  have h2 := act4_faithful (mulAQ p (invAQ q)) key
  have h3 : p = mulAQ (mulAQ p (invAQ q)) q := by
    rw [mulAQ_assoc, mulAQ_left_inv, mulAQ_one]
  rw [h3, h2, oneAQ_mul]

/-! ## THE THEOREM: every image is even -/

/-- IMAGE_EVEN: all twelve images of the action have even inversion
    count — the identity (0 inversions), the three double
    transpositions (2, 4, 6), the eight 3-cycles (2 or 4). No image
    is an odd permutation. Combined with injectivity: the image is
    TWELVE DISTINCT EVEN PERMUTATIONS. Combined with the classical
    count |A₄| = 12 [C]: the image IS A₄. THE IDENTIFICATION CLOSES. -/
theorem image_even (p : V4 × C3) : invCount (act4 p) % 2 = 0 := by
  obtain ⟨v, x⟩ := p
  cases v <;> cases x <;> rfl

end TetrahedralEvenness
