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

end ChiralPartner
