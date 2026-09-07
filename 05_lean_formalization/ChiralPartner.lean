/-
  ChiralPartner.lean

  THE CHIRAL PARTNER — first formalization pass at §7 of the book
  manuscript section "The Chiral Crack: The Holonomic Loop and the
  Symmetry-Breaking Moment": the doubled cover whose two factors are
  exchanged by parity. This is the factor-exchange skeleton that the
  SU(2)_L × SU(2)_R chiral structure of the Standard Model instantiates.

  Tag: [O] — open, conjectural, motivational for the physical reading.
  The theorems are structural facts about the doubled cover; they
  certify no physical ontology and upgrade nothing in the manuscript's
  claim registry.

  Setting: the partner cover is TWO COPIES of the pin cover of
  ChiralResidue.lean — Q8 × Q8. The first factor is the LEFT copy, the
  second the RIGHT. Parity is the EXCHANGE automorphism (a, b) ↦ (b, a).

  What is proved:

    (A) The exchange is an involutive automorphism of the partner
        cover: swap∘swap = id, and it respects the product
        componentwise (exchange_hom). [proved]
    (B) Parity carries the pure LEFT embedding wholly into the pure
        RIGHT embedding and back — the exchange is total on the pure
        sectors; no pure-left element stays left. [proved]
    (C) The parity-SYMMETRIC states are exactly the diagonal: the
        ambidextrous mixtures (a, a). [proved]
    (D) ONLY THE VACUUM: the only pure-left state fixed by the exchange
        is the trivial one. A nontrivial pure-handed state is never
        parity-symmetric — purity and exchange-symmetry are mutually
        exclusive except at the vacuum. This is the structural seed of
        maximal violation: a coupling that is purely handed cannot
        preserve parity. [proved]
    (E) The pure sectors meet only in the vacuum: no state is both
        purely left and purely right except doing nothing. [proved]
    (F) THE WEAK SELECTION: the doubled cover acts on the chiral space
        through its LEFT component only (wact) — the formal
        counterpart of the weak interaction gauging the left factor
        only. The binary dichotomy is inherited (weak_dichotomy, from
        ChiralResidue), and which sector a state is in is read off the
        left factor alone (weak_reverses_iff, the exact-converse
        capstone of the grading applied to the doubled setting).
        THE PARTNER THEOREM: a pure-left state of reflection type is
        seen by the weak selection as chiral, while its parity
        partner — carrying the same internal type in the other
        factor — is completely invisible to the weak selection
        (chiral_state_visible_partner_invisible). Maximal violation in
        the doubled setting, derived from the grading. [proved]
    (G) THE SO(4) SEED: the two factors commute inside the doubled
        cover (factors_commute, via the group laws), and the diagonal
        sign ε = (−1, −1) is central of order two
        (diagonal_sign_central, diagonal_sign_order_two, via the
        centrality of the 2π rotation). The quotient by ε — the
        identification (a, b) ~ (−a, −b) — is the miniature of
        SO(4) ≅ (SU(2) × SU(2))/±1, the structure whose chiral
        factorization the Standard Model instantiates. [proved as
        structural facts; the quotient itself is not constructed]

  Honest scope: this formalizes the FACTOR-EXCHANGE skeleton of the
  chiral partner model — the Z/2 that exchanges the left and right
  copies. It does NOT yet derive the SU(2)_L gauge structure: that the
  left factor carries an SU(2) gauge symmetry, the mechanism that
  selects a factor for the weak coupling, and the coupling scale all
  remain open. The physics reading is [O]; the theorems are structural
  facts about the doubled cover.

  Pure Lean 4 core. No Mathlib, no sorry. Companion to ChiralResidue.lean
  (whose cover supplies each factor) and ChiralCrackSketch.lean (the
  underlying chiral space). Verified compiling on the pinned toolchain.
-/

import ChiralResidue

namespace ChiralPartner

open ChiralResidue
open ChiralCrack

/-! ### The partner cover: two copies of the pin cover -/

/-- The product of the partner cover, componentwise. -/
def pmul : (Q8 × Q8) → (Q8 × Q8) → (Q8 × Q8)
  | (a1, b1), (a2, b2) => (mul a1 a2, mul b1 b2)

/-- PARITY: the exchange automorphism, swapping the two copies. -/
def exchange : (Q8 × Q8) → (Q8 × Q8)
  | (a, b) => (b, a)

/-- The pure LEFT embedding: the traveler fully in the left copy. -/
def leftEmb (a : Q8) : Q8 × Q8 := (a, one)

/-- The pure RIGHT embedding: the traveler fully in the right copy. -/
def rightEmb (b : Q8) : Q8 × Q8 := (one, b)

/-! ### (A) The exchange is an involutive automorphism -/

theorem exchange_involutive (p : Q8 × Q8) :
    exchange (exchange p) = p := by
  cases p <;> rfl

/-- The exchange respects the product, componentwise: it is an
    automorphism of the partner cover. -/
theorem exchange_hom (p q : Q8 × Q8) :
    exchange (pmul p q) = pmul (exchange p) (exchange q) := by
  cases p <;> cases q <;> rfl

/-! ### (B) Parity carries each pure sector wholly into the other -/

theorem exchange_left (a : Q8) :
    exchange (leftEmb a) = rightEmb a := rfl

theorem exchange_right (b : Q8) :
    exchange (rightEmb b) = leftEmb b := rfl

/-! ### (C) The parity-symmetric states are exactly the diagonal -/

/-- Every diagonal state is fixed by the exchange: the mixtures are
    the ambidextrous ones. -/
theorem diagonal_symmetric (a : Q8) : exchange (a, a) = (a, a) := rfl

/-- CONVERSE: every exchange-fixed state is diagonal. The
    parity-symmetric states are EXACTLY the ambidextrous mixtures. -/
theorem diagonal_fixed (p : Q8 × Q8) (hp : exchange p = p) :
    p.1 = p.2 := by
  cases p with
  | mk a b => exact congrArg Prod.snd hp

/-! ### (D) Only the vacuum: purity and symmetry are exclusive -/

/-- ONLY THE VACUUM: the only pure-left state fixed by the exchange is
    the trivial one. A nontrivial pure-handed state is never
    parity-symmetric — handedness and exchange-symmetry are mutually
    exclusive except at the vacuum. -/
theorem only_vacuum_symmetric (a : Q8)
    (hp : exchange (leftEmb a) = leftEmb a) : a = one := by
  have h : (one, a) = (a, one) := hp
  exact congrArg Prod.snd h

/-! ### (E) The pure sectors meet only in the vacuum -/

/-- No state is both purely left and purely right, except the vacuum. -/
theorem pure_sectors_meet_in_vacuum (a b : Q8)
    (hp : leftEmb a = rightEmb b) : a = one ∧ b = one := by
  exact ⟨congrArg Prod.fst hp, congrArg Prod.snd hp.symm⟩

/-! ### (F) The weak selection: the left projection -/

/-- THE WEAK SELECTION: the doubled cover acts on the chiral space
    through its LEFT component only. This is the formal counterpart of
    the weak interaction gauging the left factor only. -/
def wact : (Q8 × Q8) → Hand → Hand
  | (a, _), h => act a h

/-- The binary dichotomy is inherited by the doubled setting: every
    state of the partner cover either preserves handedness at every
    point or reverses it at every point. Partial violation remains
    impossible. (Derived from ChiralResidue.parity_violation_is_binary.) -/
theorem weak_dichotomy (p : Q8 × Q8) :
    (∀ h, wact p h = h) ∨ (∀ h, wact p h = ChiralCrack.flip h) := by
  cases p with
  | mk a b => exact parity_violation_is_binary a

/-- WHICH sector a state belongs to is read off the left factor alone:
    the coupling's handedness behavior is exactly its left component's
    sector. (The grading capstone of ChiralResidue, applied.) -/
theorem weak_reverses_iff (p : Q8 × Q8) :
    (∀ h, wact p h = ChiralCrack.flip h) ↔ p.1.ref = true := by
  cases p with
  | mk a b => exact (reflection_iff_reverses a).symm

/-- Parity does not change the internal type: the partner carries the
    original's type in the other factor. -/
theorem partner_carries_the_type (a : Q8) :
    (exchange (leftEmb a)).2 = a := rfl

/-- THE PARTNER THEOREM: a pure-left state of reflection type is seen
    by the weak selection as chiral (it reverses handedness at every
    point), while its parity partner — carrying the same internal type
    in the other factor — is COMPLETELY INVISIBLE to the weak
    selection. The coupling sees the original and cannot see the
    partner: maximal violation in the doubled setting, derived from
    the grading capstone, not inserted. -/
theorem chiral_state_visible_partner_invisible (a : Q8)
    (hr : ∀ h, act a h = ChiralCrack.flip h) :
    (∀ h, wact (exchange (leftEmb a)) h = h) ∧ a.ref = true :=
  ⟨fun _h => rfl, (reflection_iff_reverses a).mpr hr⟩

/-! ### (G) The two factors commute: the SO(4) seed -/

/-- The LEFT and RIGHT factors commute inside the doubled cover (via
    the group laws). This is the structural fact underlying
    SO(4) ≅ (SU(2) × SU(2))/±1: the two copies act independently, which
    is what makes the chiral factorization possible at all. -/
theorem factors_commute (a b : Q8) :
    pmul (leftEmb a) (rightEmb b) = pmul (rightEmb b) (leftEmb a) := by
  show (mul a one, mul one b) = (mul one a, mul b one)
  rw [mul_one a, mul_one b, one_mul a, one_mul b]

/-- The DIAGONAL SIGN ε = (−1, −1) is central in the doubled cover: it
    commutes with everything (via the centrality of the 2π rotation
    in each factor). -/
theorem diagonal_sign_central (p : Q8 × Q8) :
    pmul (minusOne, minusOne) p = pmul p (minusOne, minusOne) := by
  cases p with
  | mk a b =>
    show (mul minusOne a, mul minusOne b) = (mul a minusOne, mul b minusOne)
    rw [central_two_pi_commutes a, central_two_pi_commutes b]

/-- ε has order two: the identification (a, b) ~ (−a, −b) squares to
    the identity — the quotient by the diagonal sign is
    well-founded. -/
theorem diagonal_sign_order_two :
    pmul (minusOne, minusOne) (minusOne, minusOne) = (one, one) := rfl

end ChiralPartner
