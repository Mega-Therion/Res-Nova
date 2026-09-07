/-
  TetrahedralAction.lean — Pure Lean 4 Core
  Axiom budget: [propext, Classical.choice, Quot.sound] — Zero sorry, Pure Lean 4 Core

  THE THREE ANONYMOUS INVOLUTIONS MEET THE TETRAHEDRON'S FOUR
  VERTICES (2026-09-07). The shadow census (PR #30) left the three
  involutions — the classes of ±r, ±n (the crack), ±rn — anonymous in
  one conjugacy orbit. This module gives them somewhere to act: the
  census group V₄ ⋊ C₃ acts on FOUR POINTS, and the action is the
  tetrahedral geometry, in miniature.

  WHAT IS PROVED [P]:
    - The action: the three involutions act as the three DOUBLE
      TRANSPOSITIONS of the four vertices — (01)(23), (02)(13),
      (03)(12) — and the generation element acts as the 3-cycle
      (012), fixing one vertex.
    - THE ACTION IS A HOMOMORPHISM: derived from one conjugation
      lemma — the generation's conjugation of the involutions IS
      conjugation of permutations. The semidirect structure and the
      vertex action agree.
    - FAITHFUL: only the identity acts trivially — the 12-element
      census group EMBEDS in the permutations of the four vertices.
      Nothing upstairs is invisible here except what the shadow
      already removed.
    - TRANSITIVE: any vertex can be carried to any vertex. The
      tetrahedron's rotation group moves freely among its vertices.
    - THE GENERATION ELEMENT IS A VERTEX ROTATION: it fixes one
      vertex and cycles the other three — the axis through a vertex
      and the opposite face.
    - THE INVOLUTIONS ARE EDGE HALF-TURNS: each moves EVERY vertex —
      the axis runs through the midpoints of opposite edges, fixing
      no vertex.

  WHAT IS NOT PROVED, TAGGED [O]:
    - That the image is EXACTLY the even permutations (the A₄
      identification): parity is not defined here. What is proved is
      the embedding, the transitivity, and the axis geometry.
    - The identification of the four points with the vertices of a
      tetrahedron in space; all physics readings; the Stiefel echo.

  Cross-references: TetrahedralQuotient.lean (the census group, the
  anonymity orbit), BinaryTetrahedral.lean (the composition),
  ChiralResidue.lean (the crack), GenerationCycleChirality.lean (the
  order-3 route), BRANCHING_FROM_THE_INVARIANT.md (the trunk).
-/
import TetrahedralQuotient

namespace TetrahedralAction

open ChiralResidue BinaryTetrahedral TetrahedralQuotient

/-! ## The four vertices -/

/-- The four points the census group acts on. -/
inductive T4 where
  | v0 | v1 | v2 | v3

/-! ## The three involutions as double transpositions -/

/-- The vertex realization of the Klein four: the identity, and the
    three double transpositions. The crack's class b is (02)(13). -/
def rep4 : V4 → T4 → T4
  | .e, t => t
  | .a, .v0 => .v1 | .a, .v1 => .v0 | .a, .v2 => .v3 | .a, .v3 => .v2   -- (01)(23)
  | .b, .v0 => .v2 | .b, .v1 => .v3 | .b, .v2 => .v0 | .b, .v3 => .v1   -- (02)(13)
  | .c, .v0 => .v3 | .c, .v1 => .v2 | .c, .v2 => .v1 | .c, .v3 => .v0   -- (03)(12)

/-- rep4 is a homomorphism of V₄. -/
theorem rep4_mul (v w : V4) (t : T4) :
    rep4 (mulV4 v w) t = rep4 v (rep4 w t) := by
  cases v <;> cases w <;> cases t <;> rfl

/-! ## The generation element as a vertex rotation -/

/-- The vertex realization of the generation cycle: the 3-cycle
    (012), fixing v3 — a rotation about the vertex-face axis. -/
def sig : C3 → T4 → T4
  | .g0, t => t
  | .g1, .v0 => .v1 | .g1, .v1 => .v2 | .g1, .v2 => .v0 | .g1, .v3 => .v3   -- (012)
  | .g2, .v0 => .v2 | .g2, .v1 => .v0 | .g2, .v2 => .v1 | .g2, .v3 => .v3   -- (021)

theorem sig_mul (x y : C3) (t : T4) :
    sig (mulC3 x y) t = sig x (sig y t) := by
  cases x <;> cases y <;> cases t <;> rfl

/-- THE CONJUGATION LEMMA: the generation cycle's conjugation of the
    involutions (φ̄, the anonymity orbit of PR #30) IS conjugation of
    permutations. The semidirect structure and the vertex action
    agree. -/
theorem conj_rep (x : C3) (w : V4) (t : T4) :
    rep4 (phibarPow x w) t = sig x (rep4 w (sig (invC3 x) t)) := by
  cases x <;> cases w <;> cases t <;> rfl

/-! ## The action -/

/-- The census group acts on the four vertices. -/
def act4 : V4 × C3 → T4 → T4
  | (v, x), t => rep4 v (sig x t)

/-- THE ACTION IS A HOMOMORPHISM — derived from the conjugation lemma,
    not from a table. -/
theorem act4_hom (p q : V4 × C3) (t : T4) :
    act4 (mulAQ p q) t = act4 p (act4 q t) := by
  obtain ⟨v, x⟩ := p
  obtain ⟨w, y⟩ := q
  show rep4 (mulV4 v (phibarPow x w)) (sig (mulC3 x y) t)
       = rep4 v (sig x (rep4 w (sig y t)))
  rw [rep4_mul, conj_rep, ← sig_mul, ← mulC3_assoc, mulC3_left_inv]
  rfl

theorem act4_identity (t : T4) : act4 oneAQ t = t := rfl

/-- FAITHFUL: only the identity acts trivially — the census group
    EMBEDS in the permutations of the four vertices. -/
theorem act4_faithful (p : V4 × C3) (h : ∀ t, act4 p t = t) :
    p = oneAQ := by
  obtain ⟨v, x⟩ := p
  have h0 := h T4.v0
  have h1 := h T4.v1
  cases v with
  | e =>
    cases x with
    | g0 => rfl
    | g1 => exact nomatch h0
    | g2 => exact nomatch h0
  | a =>
    cases x with
    | g0 => exact nomatch h0
    | g1 => exact nomatch h1
    | g2 => exact nomatch h0
  | b =>
    cases x with
    | g0 => exact nomatch h0
    | g1 => exact nomatch h0
    | g2 => exact nomatch h1
  | c =>
    cases x with
    | g0 => exact nomatch h0
    | g1 => exact nomatch h0
    | g2 => exact nomatch h0

/-- TRANSITIVE: any vertex can be carried to any vertex. -/
theorem act4_transitive (u v : T4) :
    ∃ p : V4 × C3, act4 p u = v := by
  cases u with
  | v0 =>
    cases v with
    | v0 => exact ⟨(V4.e, C3.g0), rfl⟩
    | v1 => exact ⟨(V4.a, C3.g0), rfl⟩
    | v2 => exact ⟨(V4.b, C3.g0), rfl⟩
    | v3 => exact ⟨(V4.c, C3.g0), rfl⟩
  | v1 =>
    cases v with
    | v0 => exact ⟨(V4.a, C3.g0), rfl⟩
    | v1 => exact ⟨(V4.e, C3.g0), rfl⟩
    | v2 => exact ⟨(V4.c, C3.g0), rfl⟩
    | v3 => exact ⟨(V4.b, C3.g0), rfl⟩
  | v2 =>
    cases v with
    | v0 => exact ⟨(V4.b, C3.g0), rfl⟩
    | v1 => exact ⟨(V4.c, C3.g0), rfl⟩
    | v2 => exact ⟨(V4.e, C3.g0), rfl⟩
    | v3 => exact ⟨(V4.a, C3.g0), rfl⟩
  | v3 =>
    cases v with
    | v0 => exact ⟨(V4.c, C3.g0), rfl⟩
    | v1 => exact ⟨(V4.b, C3.g0), rfl⟩
    | v2 => exact ⟨(V4.a, C3.g0), rfl⟩
    | v3 => exact ⟨(V4.e, C3.g0), rfl⟩

/-- THE GENERATION ELEMENT IS A VERTEX ROTATION: it fixes v3 and
    cycles v0 → v1 → v2 → v0 — the axis through a vertex and the
    opposite face. -/
theorem generation_vertex_axis :
    act4 (V4.e, C3.g1) T4.v3 = T4.v3
    ∧ act4 (V4.e, C3.g1) T4.v0 = T4.v1
    ∧ act4 (V4.e, C3.g1) T4.v1 = T4.v2
    ∧ act4 (V4.e, C3.g1) T4.v2 = T4.v0 := ⟨rfl, rfl, rfl, rfl⟩

/-- THE INVOLUTIONS ARE EDGE HALF-TURNS: each moves EVERY vertex —
    the axis runs through the midpoints of opposite edges, fixing
    no vertex. -/
theorem involutions_move_every_vertex :
    (∀ t, act4 (V4.a, C3.g0) t ≠ t)
    ∧ (∀ t, act4 (V4.b, C3.g0) t ≠ t)
    ∧ (∀ t, act4 (V4.c, C3.g0) t ≠ t) :=
  ⟨(fun t => by cases t <;> exact fun h => nomatch h),
   (fun t => by cases t <;> exact fun h => nomatch h),
   (fun t => by cases t <;> exact fun h => nomatch h)⟩

end TetrahedralAction
