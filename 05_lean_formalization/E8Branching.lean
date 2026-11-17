import E8Roots
import Mathlib.Tactic

/-!
# E8Branching: The E8 → SO(10) Branching, Formalized at the Weight Level

Author: R.W. Yett (ORCID: 0009-0001-1303-7190)
Project: Res Nova
Date: 2026-11-15

This file formalizes the E8 → SO(10) branching exhibited in
`anthropic-fellows/e8-to-so10-branching-2026-11-09.md` (Slansky's tables,
Adler hep-ph/0201009, Joglekar–Rosner arXiv:1607.06900), building on the
E8 root system in `E8Roots.lean`.

## What is proved — and at what level

This is a **weight-level** formalization of the branching, not a full
representation-theoretic one. The adjoint representation's weights are the
roots plus the Cartan, so the branching of the 248 is captured exactly by
partitioning the 240 roots and counting Cartan generators. What the file
establishes:

1. **Step 1 — E8 ⊃ E6 × SU(3).** The 240 E8 roots partition into four
   disjoint sets: the E6 roots (72), the SU(3) roots (6), the (3,27)
   weights (81), and the (3̄,27̄) weights (81). With the Cartan
   generators (6 for E6, 2 for SU(3)), this is the adjoint decomposition
   `248 = (8,1) ⊕ (1,78) ⊕ (3,27) ⊕ (3̄,27̄)`, i.e.
   `8 + 78 + 81 + 81 = 248`.
2. **The subgroup is E6 × SU(3).** The 72-root set contains six simple
   roots whose Gram matrix is `4 ×` the E6 Cartan matrix; the 6-root set
   contains two simple roots whose Gram matrix is `4 ×` the A2 Cartan
   matrix; and every E6 root is orthogonal to every SU(3) root, so the
   two subalgebras commute — the subgroup is the direct product.
3. **The (3,27) structure.** Projecting the 81 (3,27) roots onto the E6
   weight space gives exactly 27 weights, each with exactly 3 preimages
   (the SU(3) triplet). Negation swaps the (3,27) and (3̄,27̄) sets.
4. **Step 2 — E6 ⊃ SO(10) × U(1).** The 72 E6 roots split into the D5
   roots (40, with Gram `4 ×` the D5 Cartan matrix) plus two 16-root
   spinor sets; with Cartan generators this is
   `78 = 1(0) ⊕ 45(0) ⊕ 16(3) ⊕ 16̄(-3)`. The 27 weights split into
   16 + 10 + 1 with U(1) charges 1, -2, 4 (Joglekar–Rosner convention).
5. **Step 3 — composition.** The full dimension identity
   `16 + 16 + 48 + 48 + 30 + 30 + 3 + 3 + 8 + 45 + 1 = 248`.

## What is NOT proved here

- The branching is established at the level of **root/weight sets and
  their counts**, with the subgroup factors identified by their simple
  roots and Cartan matrices. The file does not formalize Lie algebra
  representations, highest-weight theory, or characters; the claim that
  these weight sets are the stated representations rests on the standard
  identification (weights + Cartan matrix determine the representation),
  cited from Slansky/Adler/Joglekar–Rosner in the exhibited derivation.
- The Pati-Salam step (Step 4 of the derivation) is out of scope.

## Conventions

Everything is in the **doubled coordinates** of `E8Roots.lean`: roots are
`ℤ⁸` vectors of norm² 8. The E6 × SU(3) embedding puts the SU(3) factor
on the first three coordinates: the E6 roots are those with
`y 0 = y 1 = y 2`, and the SU(3) weight of a root is read off
`s3sum y = y 0 + y 1 + y 2` modulo 3 (the triality). The U(1) charge is
`-(y 0 + y 1 + y 2)` on weights. All counts are obtained by `decide` over
the `TypeAData` / `TypeBData` enumerations from `E8Roots.lean`, transferred
to the root finsets through the injectivity of `typeAVec` / `typeBVec`.

## Axioms

Standard Lean axioms only: `[propext, Classical.choice, Quot.sound]`.
Zero `sorry`. Verified by `#print axioms` at the end of the file.
-/

namespace ResNova.E8Branching

open ResNova.E8Roots

/- The image/dedup `decide` computations recurse deeper than the default
   limit; the filter counts do not need this, but the image cards do. -/
set_option maxRecDepth 10000

-- =========================================================================
-- 1. The SU(3) weight sum and the four branch predicates
-- =========================================================================

/-- The SU(3) weight sum: the sum of the first three coordinates.
    Modulo 3 this is the triality: `0` for SU(3) singlets (E6 roots and
    SU(3) roots), `2` for the `3`, `1` for the `3̄`. -/
def s3sum (y : Vec) : ℤ := y 0 + y 1 + y 2

/-- E6 roots: the first three coordinates agree. These are the roots of
    the E6 factor: they are orthogonal to the SU(3) roots (see
    `e6_su3_orthogonal`) and closed under reflection (see
    `e6_reflect_closed`). -/
def IsE6Root (y : Vec) : Prop := y 0 = y 1 ∧ y 1 = y 2

/-- SU(3) roots: supported on the first three coordinates with zero sum,
    i.e. the six roots `±(eᵢ - eⱼ)` for `i, j ∈ {0, 1, 2}`. -/
def IsSU3Root (y : Vec) : Prop := (∀ i, 3 ≤ i → y i = 0) ∧ s3sum y = 0

/-- The (3,27) weights: triality 2. -/
def IsBranch27 (y : Vec) : Prop := s3sum y % 3 = 2

/-- The (3̄,27̄) weights: triality 1. -/
def IsBranch27bar (y : Vec) : Prop := s3sum y % 3 = 1

instance : DecidablePred IsE6Root :=
  fun y => inferInstanceAs (Decidable (y 0 = y 1 ∧ y 1 = y 2))
instance : DecidablePred IsSU3Root :=
  fun y => inferInstanceAs (Decidable ((∀ i, 3 ≤ i → y i = 0) ∧ s3sum y = 0))
instance : DecidablePred IsBranch27 :=
  fun y => inferInstanceAs (Decidable (s3sum y % 3 = 2))
instance : DecidablePred IsBranch27bar :=
  fun y => inferInstanceAs (Decidable (s3sum y % 3 = 1))

-- =========================================================================
-- 2. The four finsets, and the transfer from data counts to root counts
-- =========================================================================

/-- The E6 roots, as a finset. -/
def e6Finset : Finset Vec := rootFinset.filter IsE6Root

/-- The SU(3) roots, as a finset. -/
def su3Finset : Finset Vec := rootFinset.filter IsSU3Root

/-- The (3,27) weights, as a finset. -/
def branch27Finset : Finset Vec := rootFinset.filter IsBranch27

/-- The (3̄,27̄) weights, as a finset. -/
def branch27barFinset : Finset Vec := rootFinset.filter IsBranch27bar

/-- Image and filter commute (up to the predicate's pullback). -/
theorem image_filter_eq {α β : Type*} [DecidableEq β] {s : Finset α}
    {f : α → β} {p : β → Prop} [DecidablePred p] :
    (s.image f).filter p = (s.filter (fun a => p (f a))).image f := by
  ext y
  simp only [Finset.mem_filter, Finset.mem_image]
  constructor
  · rintro ⟨⟨a, ha, rfl⟩, hp⟩
    exact ⟨a, ⟨ha, hp⟩, rfl⟩
  · rintro ⟨a, ⟨ha, hp⟩, rfl⟩
    exact ⟨⟨a, ha, rfl⟩, hp⟩

/-- Counting a predicate on the Type A roots is counting it on the data. -/
theorem card_filter_typeA (P : Vec → Prop) [DecidablePred P] :
    (typeAFinset.filter P).card =
      (Finset.univ.filter (fun d : TypeAData => P (typeAVec d))).card := by
  rw [typeAFinset, image_filter_eq, Finset.card_image_of_injective _ typeAVec_injective]

/-- Counting a predicate on the Type B roots is counting it on the data. -/
theorem card_filter_typeB (P : Vec → Prop) [DecidablePred P] :
    (typeBFinset.filter P).card =
      (Finset.univ.filter (fun e : TypeBData => P (typeBVec e.1))).card := by
  rw [typeBFinset, image_filter_eq, Finset.card_image_of_injective _ typeBVec_injective]

/-- Counting a predicate on all roots splits over the two types. -/
theorem card_filter_root (P : Vec → Prop) [DecidablePred P] :
    (rootFinset.filter P).card =
      (typeAFinset.filter P).card + (typeBFinset.filter P).card := by
  rw [rootFinset, Finset.filter_union, Finset.card_union_of_disjoint]
  exact Disjoint.mono (Finset.filter_subset P typeAFinset)
    (Finset.filter_subset P typeBFinset) typeA_typeB_disjoint

-- The eight data-level counts, each by `decide` over the enumeration.
theorem count_e6_typeA :
    (Finset.univ.filter (fun d : TypeAData => IsE6Root (typeAVec d))).card = 40 := by
  decide
theorem count_e6_typeB :
    (Finset.univ.filter (fun e : TypeBData => IsE6Root (typeBVec e.1))).card = 32 := by
  decide
theorem count_su3_typeA :
    (Finset.univ.filter (fun d : TypeAData => IsSU3Root (typeAVec d))).card = 6 := by
  decide
theorem count_su3_typeB :
    (Finset.univ.filter (fun e : TypeBData => IsSU3Root (typeBVec e.1))).card = 0 := by
  decide
theorem count_branch27_typeA :
    (Finset.univ.filter (fun d : TypeAData => IsBranch27 (typeAVec d))).card = 33 := by
  decide
theorem count_branch27_typeB :
    (Finset.univ.filter (fun e : TypeBData => IsBranch27 (typeBVec e.1))).card = 48 := by
  decide
theorem count_branch27bar_typeA :
    (Finset.univ.filter (fun d : TypeAData => IsBranch27bar (typeAVec d))).card = 33 := by
  decide
theorem count_branch27bar_typeB :
    (Finset.univ.filter (fun e : TypeBData => IsBranch27bar (typeBVec e.1))).card = 48 := by
  decide

/-- There are 72 E6 roots: 40 of Type A, 32 of Type B. -/
theorem e6Finset_card : e6Finset.card = 72 := by
  rw [e6Finset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_e6_typeA, count_e6_typeB]

/-- There are 6 SU(3) roots, all of Type A. -/
theorem su3Finset_card : su3Finset.card = 6 := by
  rw [su3Finset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_su3_typeA, count_su3_typeB]

/-- There are 81 (3,27) weights: 33 of Type A, 48 of Type B. -/
theorem branch27Finset_card : branch27Finset.card = 81 := by
  rw [branch27Finset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_branch27_typeA, count_branch27_typeB]

/-- There are 81 (3̄,27̄) weights: 33 of Type A, 48 of Type B. -/
theorem branch27barFinset_card : branch27barFinset.card = 81 := by
  rw [branch27barFinset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_branch27bar_typeA, count_branch27bar_typeB]

-- =========================================================================
-- 3. The partition: the four sets are disjoint and exhaust the roots
-- =========================================================================

/-- E6 and SU(3) roots are disjoint: a root in both would have all
    coordinates zero, hence norm 0, not 8. -/
theorem e6_su3_disjoint : Disjoint e6Finset su3Finset := by
  rw [Finset.disjoint_left]
  intro y hyE6 hySU3
  rw [e6Finset, Finset.mem_filter] at hyE6
  rw [su3Finset, Finset.mem_filter] at hySU3
  obtain ⟨hyroot, hyE6⟩ := hyE6
  obtain ⟨-, hySU3⟩ := hySU3
  have hroot : IsE8Root y := mem_rootFinset_iff.mp hyroot
  obtain ⟨h01, h12⟩ := hyE6
  obtain ⟨hzero, hsum⟩ := hySU3
  have hy0 : y 0 = 0 := by
    have hsum' : y 0 + y 1 + y 2 = 0 := hsum
    omega
  have hy1 : y 1 = 0 := by omega
  have hy2 : y 2 = 0 := by omega
  have hall : ∀ i : Fin 8, y i = 0 := by
    intro i
    by_cases hi : i < 3
    · have hcases : i = 0 ∨ i = 1 ∨ i = 2 := by omega
      rcases hcases with rfl | rfl | rfl
      · exact hy0
      · exact hy1
      · exact hy2
    · exact hzero i (by omega)
  have hnorm0 : normSq y = 0 := by
    simp only [normSq, dot]
    apply Finset.sum_eq_zero
    intro i _
    rw [hall i]
    simp
  rw [hroot.2] at hnorm0
  norm_num at hnorm0

/-- E6 and (3,27) are disjoint: an E6 root has triality 0. -/
theorem e6_27_disjoint : Disjoint e6Finset branch27Finset := by
  rw [Finset.disjoint_left]
  intro y hyE6 hy27
  rw [e6Finset, Finset.mem_filter] at hyE6
  rw [branch27Finset, Finset.mem_filter] at hy27
  obtain ⟨-, h01, h12⟩ := hyE6
  obtain ⟨-, h27⟩ := hy27
  have hs3 : s3sum y = 3 * y 0 := by
    show y 0 + y 1 + y 2 = 3 * y 0
    omega
  have h27' : s3sum y % 3 = 2 := h27
  omega

/-- E6 and (3̄,27̄) are disjoint: an E6 root has triality 0. -/
theorem e6_27bar_disjoint : Disjoint e6Finset branch27barFinset := by
  rw [Finset.disjoint_left]
  intro y hyE6 hy27bar
  rw [e6Finset, Finset.mem_filter] at hyE6
  rw [branch27barFinset, Finset.mem_filter] at hy27bar
  obtain ⟨-, h01, h12⟩ := hyE6
  obtain ⟨-, h27bar⟩ := hy27bar
  have hs3 : s3sum y = 3 * y 0 := by
    show y 0 + y 1 + y 2 = 3 * y 0
    omega
  have h27bar' : s3sum y % 3 = 1 := h27bar
  omega

/-- SU(3) and (3,27) are disjoint: an SU(3) root has triality 0. -/
theorem su3_27_disjoint : Disjoint su3Finset branch27Finset := by
  rw [Finset.disjoint_left]
  intro y hySU3 hy27
  rw [su3Finset, Finset.mem_filter] at hySU3
  rw [branch27Finset, Finset.mem_filter] at hy27
  obtain ⟨-, -, hsum⟩ := hySU3
  obtain ⟨-, h27⟩ := hy27
  have h27' : s3sum y % 3 = 2 := h27
  omega

/-- SU(3) and (3̄,27̄) are disjoint: an SU(3) root has triality 0. -/
theorem su3_27bar_disjoint : Disjoint su3Finset branch27barFinset := by
  rw [Finset.disjoint_left]
  intro y hySU3 hy27bar
  rw [su3Finset, Finset.mem_filter] at hySU3
  rw [branch27barFinset, Finset.mem_filter] at hy27bar
  obtain ⟨-, -, hsum⟩ := hySU3
  obtain ⟨-, h27bar⟩ := hy27bar
  have h27bar' : s3sum y % 3 = 1 := h27bar
  omega

/-- (3,27) and (3̄,27̄) are disjoint: triality cannot be both 2 and 1. -/
theorem b27_b27bar_disjoint : Disjoint branch27Finset branch27barFinset := by
  rw [Finset.disjoint_left]
  intro y hy27 hy27bar
  rw [branch27Finset, Finset.mem_filter] at hy27
  rw [branch27barFinset, Finset.mem_filter] at hy27bar
  obtain ⟨-, h27⟩ := hy27
  obtain ⟨-, h27bar⟩ := hy27bar
  have h27' : s3sum y % 3 = 2 := h27
  have h27bar' : s3sum y % 3 = 1 := h27bar
  omega

/-- **The partition.** The four sets are disjoint and their union is the
    full set of 240 roots: `72 + 6 + 81 + 81 = 240`. -/
theorem branch_partition :
    e6Finset ∪ su3Finset ∪ branch27Finset ∪ branch27barFinset = rootFinset := by
  apply Finset.eq_of_subset_of_card_le
  · simp only [Finset.union_subset_iff]
    exact ⟨⟨⟨Finset.filter_subset _ _, Finset.filter_subset _ _⟩,
      Finset.filter_subset _ _⟩, Finset.filter_subset _ _⟩
  · rw [rootFinset_card]
    have h1 : Disjoint (e6Finset ∪ su3Finset) branch27Finset :=
      Finset.disjoint_union_left.mpr ⟨e6_27_disjoint, su3_27_disjoint⟩
    have h2 : Disjoint (e6Finset ∪ su3Finset ∪ branch27Finset) branch27barFinset :=
      Finset.disjoint_union_left.mpr
        ⟨Finset.disjoint_union_left.mpr ⟨e6_27bar_disjoint, su3_27bar_disjoint⟩,
          b27_b27bar_disjoint⟩
    rw [Finset.card_union_of_disjoint h2, Finset.card_union_of_disjoint h1,
      Finset.card_union_of_disjoint e6_su3_disjoint,
      e6Finset_card, su3Finset_card, branch27Finset_card, branch27barFinset_card]

-- =========================================================================
-- 4. Step 1: the adjoint decomposition
--    248 = (8,1) ⊕ (1,78) ⊕ (3,27) ⊕ (3̄,27̄)
-- =========================================================================

/-- The E6 adjoint: 72 roots + 6 Cartan generators. -/
theorem e6_adjoint_dim : e6Finset.card + 6 = 78 := by rw [e6Finset_card]

/-- The SU(3) adjoint: 6 roots + 2 Cartan generators. -/
theorem su3_adjoint_dim : su3Finset.card + 2 = 8 := by rw [su3Finset_card]

/-- **Step 1.** The adjoint 248 decomposes as
    `(8,1) ⊕ (1,78) ⊕ (3,27) ⊕ (3̄,27̄)` under E6 × SU(3):
    `8 + 78 + 81 + 81 = 248`, with each term a proven count. -/
theorem step1_branching :
    (su3Finset.card + 2) + (e6Finset.card + 6) +
      branch27Finset.card + branch27barFinset.card = 248 := by
  rw [e6Finset_card, su3Finset_card, branch27Finset_card, branch27barFinset_card]

-- =========================================================================
-- 5. The 72-root set is E6: simple roots and the Cartan matrix
-- =========================================================================

/-- The six simple roots of the E6 subsystem. The first five are the D5
    simple roots (E8 simple roots α₄–α₇ plus `(0,…,0,2,−2)`); the sixth
    is the all-`−1` root, which extends the α₇ arm. -/
def e6SimpleRoot : Fin 6 → Vec
  | 0 => ![0, 0, 0, 2, -2, 0, 0, 0]
  | 1 => ![0, 0, 0, 0, 2, -2, 0, 0]
  | 2 => ![0, 0, 0, 0, 0, 2, -2, 0]
  | 3 => ![0, 0, 0, 0, 0, 0, 2, -2]
  | 4 => ![0, 0, 0, 0, 0, 0, 2, 2]
  | 5 => ![-1, -1, -1, -1, -1, -1, -1, -1]

theorem e6SimpleRoot_isRoot (i : Fin 6) : IsE8Root (e6SimpleRoot i) := by
  fin_cases i <;> refine ⟨⟨?_, ?_⟩, ?_⟩ <;> decide

theorem e6SimpleRoot_mem (i : Fin 6) : e6SimpleRoot i ∈ e6Finset := by
  rw [e6Finset, Finset.mem_filter]
  constructor
  · exact mem_rootFinset_iff.mpr (e6SimpleRoot_isRoot i)
  · fin_cases i <;> decide

/-- The E6 Cartan matrix (branch at node 2, zero-indexed). -/
def cartanE6 : Matrix (Fin 6) (Fin 6) ℤ :=
  !![2, -1, 0, 0, 0, 0;
     -1, 2, -1, 0, 0, 0;
     0, -1, 2, -1, -1, 0;
     0, 0, -1, 2, 0, 0;
     0, 0, -1, 0, 2, -1;
     0, 0, 0, 0, -1, 2]

/-- The Gram matrix of the E6 simple roots is `4 ×` the E6 Cartan matrix
    (the factor 4 is the doubling). This identifies the 72-root set as
    the E6 root system: 72 roots, rank 6, E6 Dynkin diagram. -/
theorem e6_gram_eq_four_cartan (i j : Fin 6) :
    dot (e6SimpleRoot i) (e6SimpleRoot j) = 4 * cartanE6 i j := by
  fin_cases i <;> fin_cases j <;> decide

/-- The E6 roots are closed under negation. -/
theorem e6_neg_closed {y : Vec} (hy : y ∈ e6Finset) : -y ∈ e6Finset := by
  rw [e6Finset, Finset.mem_filter] at hy ⊢
  obtain ⟨hroot, h6⟩ := hy
  obtain ⟨h01, h12⟩ := h6
  constructor
  · exact mem_rootFinset_iff.mpr (root_neg (mem_rootFinset_iff.mp hroot))
  · show (-y) 0 = (-y) 1 ∧ (-y) 1 = (-y) 2
    simp only [Pi.neg_apply]
    constructor <;> omega

/-- The E6 roots are closed under reflection: the E6 set is a root
    subsystem, not just a subset of the right size. -/
theorem e6_reflect_closed {α β : Vec} (hα : α ∈ e6Finset) (hβ : β ∈ e6Finset) :
    reflect α β ∈ e6Finset := by
  rw [e6Finset, Finset.mem_filter] at hα hβ ⊢
  obtain ⟨hαroot, hα6⟩ := hα
  obtain ⟨hβroot, hβ6⟩ := hβ
  obtain ⟨hα01, hα12⟩ := hα6
  obtain ⟨hβ01, hβ12⟩ := hβ6
  constructor
  · exact mem_rootFinset_iff.mpr
      (root_reflect (mem_rootFinset_iff.mp hαroot) (mem_rootFinset_iff.mp hβroot))
  · refine ⟨?_, ?_⟩ <;> simp only [reflect, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    · rw [hβ01, hα01]
    · rw [hβ12, hα12]

-- =========================================================================
-- 6. The 6-root set is SU(3): simple roots and the Cartan matrix
-- =========================================================================

/-- The two simple roots of the SU(3) (A2) subsystem: E8 simple roots
    α₁ and α₂. -/
def su3SimpleRoot : Fin 2 → Vec
  | 0 => ![2, -2, 0, 0, 0, 0, 0, 0]
  | 1 => ![0, 2, -2, 0, 0, 0, 0, 0]

theorem su3SimpleRoot_isRoot (i : Fin 2) : IsE8Root (su3SimpleRoot i) := by
  fin_cases i <;> refine ⟨⟨?_, ?_⟩, ?_⟩ <;> decide

theorem su3SimpleRoot_mem (i : Fin 2) : su3SimpleRoot i ∈ su3Finset := by
  rw [su3Finset, Finset.mem_filter]
  constructor
  · exact mem_rootFinset_iff.mpr (su3SimpleRoot_isRoot i)
  · fin_cases i <;> decide

/-- The A2 Cartan matrix. -/
def cartanA2 : Matrix (Fin 2) (Fin 2) ℤ := !![2, -1; -1, 2]

/-- The Gram matrix of the SU(3) simple roots is `4 ×` the A2 Cartan
    matrix. This identifies the 6-root set as the A2 (SU(3)) root system. -/
theorem su3_gram_eq_four_cartan (i j : Fin 2) :
    dot (su3SimpleRoot i) (su3SimpleRoot j) = 4 * cartanA2 i j := by
  fin_cases i <;> fin_cases j <;> decide

/-- Every Type A SU(3) root is one of the six `±α₁, ±α₂, ±(α₁+α₂)`. -/
theorem su3_typeA_mem_six : ∀ d : TypeAData, IsSU3Root (typeAVec d) →
    typeAVec d ∈ ({su3SimpleRoot 0, -su3SimpleRoot 0, su3SimpleRoot 1,
      -su3SimpleRoot 1, su3SimpleRoot 0 + su3SimpleRoot 1,
      -(su3SimpleRoot 0 + su3SimpleRoot 1)} : Finset Vec) := by
  decide

/-- No Type B root is an SU(3) root. -/
theorem su3_typeB_none : ∀ e : TypeBData, ¬ IsSU3Root (typeBVec e.1) := by
  decide

/-- The six SU(3) roots are exactly `±α₁`, `±α₂`, `±(α₁+α₂)`. -/
theorem su3Finset_eq :
    su3Finset = {su3SimpleRoot 0, -su3SimpleRoot 0, su3SimpleRoot 1,
      -su3SimpleRoot 1, su3SimpleRoot 0 + su3SimpleRoot 1,
      -(su3SimpleRoot 0 + su3SimpleRoot 1)} := by
  apply Finset.eq_of_subset_of_card_le
  · intro y hy
    rw [su3Finset, Finset.mem_filter] at hy
    obtain ⟨hyroot, hySU3⟩ := hy
    rw [rootFinset, Finset.mem_union, typeAFinset, typeBFinset,
      Finset.mem_image, Finset.mem_image] at hyroot
    rcases hyroot with ⟨d, -, rfl⟩ | ⟨⟨ε, hε⟩, -, rfl⟩
    · exact su3_typeA_mem_six d hySU3
    · exact absurd hySU3 (su3_typeB_none ⟨ε, hε⟩)
  · rw [su3Finset_card]
    have h6 : ({su3SimpleRoot 0, -su3SimpleRoot 0, su3SimpleRoot 1,
      -su3SimpleRoot 1, su3SimpleRoot 0 + su3SimpleRoot 1,
      -(su3SimpleRoot 0 + su3SimpleRoot 1)} : Finset Vec).card = 6 := by
      decide
    omega

-- =========================================================================
-- 7. The two factors commute: E6 ⊥ SU(3)
-- =========================================================================

/-- Every E6 root is orthogonal to every SU(3) root: the two subalgebras
    commute, so the subgroup is the direct product E6 × SU(3).
    Proof: the SU(3) root is supported on the first three coordinates with
    zero sum, and the E6 root is constant there, so the dot product is
    `y 0 · (z 0 + z 1 + z 2) = 0`. -/
theorem e6_su3_orthogonal {y z : Vec} (hy : y ∈ e6Finset) (hz : z ∈ su3Finset) :
    dot y z = 0 := by
  rw [e6Finset, Finset.mem_filter] at hy
  rw [su3Finset, Finset.mem_filter] at hz
  obtain ⟨-, h01, h12⟩ := hy
  obtain ⟨-, hzero, hsum⟩ := hz
  have hsum' : z 0 + z 1 + z 2 = 0 := hsum
  have hdot : dot y z = y 0 * z 0 + y 1 * z 1 + y 2 * z 2 := by
    have hsub : ∑ i, y i * z i =
        ∑ i ∈ ({0, 1, 2} : Finset (Fin 8)), y i * z i := by
      symm
      apply Finset.sum_subset (Finset.subset_univ _)
      intro i _ hi
      have hi3 : 3 ≤ i := by
        simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hi
        omega
      rw [hzero i hi3]
      simp
    have h3 : ∑ i ∈ ({0, 1, 2} : Finset (Fin 8)), y i * z i =
        y 0 * z 0 + y 1 * z 1 + y 2 * z 2 := by
      rw [Finset.sum_insert, Finset.sum_insert, Finset.sum_singleton]
      · ring
      · decide
      · decide
    rw [dot, hsub, h3]
  rw [hdot]
  have hy1 : y 1 = y 0 := h01.symm
  have hy2 : y 2 = y 0 := by omega
  rw [hy1, hy2]
  have hfactor : y 0 * z 0 + y 0 * z 1 + y 0 * z 2 =
      y 0 * (z 0 + z 1 + z 2) := by ring
  rw [hfactor, hsum']
  simp

-- =========================================================================
-- 8. The (3,27) structure: 27 weights, each with 3 preimages
-- =========================================================================

/-- Projection of a root onto the E6 weight space, scaled by 3 so the
    coordinates stay integral: the first three coordinates are replaced by
    their sum, the last five are multiplied by 3. -/
def projE6 (y : Vec) : Vec := fun i => if i < 3 then s3sum y else 3 * y i

/-- The 27-weights coming from Type A (3,27) roots (11 of them). -/
def weights27A : Finset Vec :=
  (Finset.univ.filter (fun d : TypeAData => IsBranch27 (typeAVec d))).image
    (fun d => projE6 (typeAVec d))

/-- The 27-weights coming from Type B (3,27) roots (16 of them). -/
def weights27B : Finset Vec :=
  (Finset.univ.filter (fun e : TypeBData => IsBranch27 (typeBVec e.1))).image
    (fun e => projE6 (typeBVec e.1))

/-- The 27 weights of the E6 27: the projection of the (3,27) roots. -/
def weights27 : Finset Vec := weights27A ∪ weights27B

theorem weights27A_card : weights27A.card = 11 := by decide
theorem weights27B_card : weights27B.card = 16 := by decide

/-- Type A weights have first coordinate 2 or -4. -/
theorem weights27A_first : ∀ w ∈ weights27A, w 0 = 2 ∨ w 0 = -4 := by decide

/-- Type B weights have first coordinate -1. -/
theorem weights27B_first : ∀ w ∈ weights27B, w 0 = -1 := by decide

theorem weights27_disjoint : Disjoint weights27A weights27B := by
  rw [Finset.disjoint_left]
  intro w hwA hwB
  have hA := weights27A_first w hwA
  have hB := weights27B_first w hwB
  omega

/-- There are 27 weights: 11 from Type A roots, 16 from Type B. -/
theorem weights27_card : weights27.card = 27 := by
  rw [weights27, Finset.card_union_of_disjoint weights27_disjoint,
    weights27A_card, weights27B_card]

/-- The projection of the (3,27) roots is exactly the 27 weights. -/
theorem branch27_image : branch27Finset.image projE6 = weights27 := by
  have hA : (typeAFinset.filter IsBranch27).image projE6 = weights27A := by
    rw [typeAFinset, image_filter_eq, Finset.image_image]
    rfl
  have hB : (typeBFinset.filter IsBranch27).image projE6 = weights27B := by
    rw [typeBFinset, image_filter_eq, Finset.image_image]
    rfl
  rw [weights27, branch27Finset, rootFinset, Finset.filter_union, Finset.image_union, hA, hB]

/-- Each Type A weight has exactly 3 preimages among the Type A (3,27)
    data (the three choices of which of the first three coordinates
    carries the SU(3) weight). -/
theorem fiber_typeA : ∀ w ∈ weights27A,
    (Finset.univ.filter (fun d : TypeAData =>
      IsBranch27 (typeAVec d) ∧ projE6 (typeAVec d) = w)).card = 3 := by
  decide

/-- Each Type B weight has exactly 3 preimages among the Type B (3,27)
    data (the three `--+` sign patterns on the first three coordinates). -/
theorem fiber_typeB : ∀ w ∈ weights27B,
    (Finset.univ.filter (fun e : TypeBData =>
      IsBranch27 (typeBVec e.1) ∧ projE6 (typeBVec e.1) = w)).card = 3 := by
  decide

/-- The Type A (3,27) roots are 3-to-1 over the Type A weights: 33 = 3 × 11. -/
theorem count_branch27_typeA_fiber :
    (Finset.univ.filter (fun d : TypeAData => IsBranch27 (typeAVec d))).card =
      3 * weights27A.card := by
  have h := Finset.card_eq_sum_card_image (fun d : TypeAData => projE6 (typeAVec d))
    (Finset.univ.filter (fun d : TypeAData => IsBranch27 (typeAVec d)))
  rw [h]
  have hfib : ∀ b ∈ weights27A,
      ((Finset.univ.filter (fun d : TypeAData => IsBranch27 (typeAVec d))).filter
        (fun d => projE6 (typeAVec d) = b)).card = 3 := by
    intro b hb
    rw [Finset.filter_filter]
    exact fiber_typeA b hb
  have himg : (Finset.univ.filter (fun d : TypeAData => IsBranch27 (typeAVec d))).image
      (fun d => projE6 (typeAVec d)) = weights27A := rfl
  rw [Finset.sum_congr himg hfib]
  simp [Finset.sum_const, weights27A_card]

/-- The Type B (3,27) roots are 3-to-1 over the Type B weights: 48 = 3 × 16. -/
theorem count_branch27_typeB_fiber :
    (Finset.univ.filter (fun e : TypeBData => IsBranch27 (typeBVec e.1))).card =
      3 * weights27B.card := by
  have h := Finset.card_eq_sum_card_image (fun e : TypeBData => projE6 (typeBVec e.1))
    (Finset.univ.filter (fun e : TypeBData => IsBranch27 (typeBVec e.1)))
  rw [h]
  have hfib : ∀ b ∈ weights27B,
      ((Finset.univ.filter (fun e : TypeBData => IsBranch27 (typeBVec e.1))).filter
        (fun e => projE6 (typeBVec e.1) = b)).card = 3 := by
    intro b hb
    rw [Finset.filter_filter]
    exact fiber_typeB b hb
  have himg : (Finset.univ.filter (fun e : TypeBData => IsBranch27 (typeBVec e.1))).image
      (fun e => projE6 (typeBVec e.1)) = weights27B := rfl
  rw [Finset.sum_congr himg hfib]
  simp [Finset.sum_const, weights27B_card]

/-- The (3,27) roots are 3-to-1 over the 27 weights: 81 = 3 × 27.
    The factor 3 is the SU(3) triplet — the `3` in `(3,27)`. -/
theorem branch27_three_to_one : branch27Finset.card = 3 * weights27.card := by
  rw [branch27Finset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_branch27_typeA_fiber, count_branch27_typeB_fiber, weights27,
    Finset.card_union_of_disjoint weights27_disjoint, weights27A_card, weights27B_card]

/-- Negation swaps the (3,27) and (3̄,27̄) sets: they are complex
    conjugates of each other. -/
theorem branch27_neg {y : Vec} : y ∈ branch27Finset ↔ -y ∈ branch27barFinset := by
  rw [branch27Finset, branch27barFinset, Finset.mem_filter, Finset.mem_filter]
  have hs : ∀ z : Vec, s3sum (-z) = -s3sum z := by
    intro z
    simp only [s3sum, Pi.neg_apply]
    ring
  constructor
  · intro ⟨hroot, h27⟩
    constructor
    · exact mem_rootFinset_iff.mpr (root_neg (mem_rootFinset_iff.mp hroot))
    · show s3sum (-y) % 3 = 1
      rw [hs]
      have h27' : s3sum y % 3 = 2 := h27
      omega
  · intro ⟨hroot, h27bar⟩
    constructor
    · exact mem_rootFinset_iff.mpr
        (by simpa using root_neg (mem_rootFinset_iff.mp hroot))
    · show s3sum y % 3 = 2
      have h27bar' : s3sum (-y) % 3 = 1 := h27bar
      rw [hs] at h27bar'
      omega

theorem branch27bar_neg {y : Vec} : y ∈ branch27barFinset ↔ -y ∈ branch27Finset := by
  have h := branch27_neg (y := -y)
  rw [neg_neg] at h
  exact h.symm

-- =========================================================================
-- 9. Step 2: E6 ⊃ SO(10) × U(1)
-- =========================================================================

instance : DecidablePred (fun y : Vec => IsE6Root y ∧ y 0 = 0) :=
  fun y => inferInstanceAs (Decidable ((y 0 = y 1 ∧ y 1 = y 2) ∧ y 0 = 0))
instance : DecidablePred (fun y : Vec => IsE6Root y ∧ y 0 = -1) :=
  fun y => inferInstanceAs (Decidable ((y 0 = y 1 ∧ y 1 = y 2) ∧ y 0 = -1))
instance : DecidablePred (fun y : Vec => IsE6Root y ∧ y 0 = 1) :=
  fun y => inferInstanceAs (Decidable ((y 0 = y 1 ∧ y 1 = y 2) ∧ y 0 = 1))

/-- The D5 (SO(10)) roots inside E6: E6 roots with first coordinate 0.
    These are exactly the Type A E6 roots, supported on coordinates 3–7. -/
def d5Finset : Finset Vec := rootFinset.filter (fun y => IsE6Root y ∧ y 0 = 0)

/-- The 16 spinor roots inside E6: E6 roots with first coordinate -1
    (U(1) charge +3). -/
def spin16Finset : Finset Vec := rootFinset.filter (fun y => IsE6Root y ∧ y 0 = -1)

/-- The 16̄ spinor roots inside E6: E6 roots with first coordinate 1
    (U(1) charge -3). -/
def spin16barFinset : Finset Vec := rootFinset.filter (fun y => IsE6Root y ∧ y 0 = 1)

theorem count_d5_typeA :
    (Finset.univ.filter (fun d : TypeAData =>
      IsE6Root (typeAVec d) ∧ (typeAVec d) 0 = 0)).card = 40 := by
  decide
theorem count_d5_typeB :
    (Finset.univ.filter (fun e : TypeBData =>
      IsE6Root (typeBVec e.1) ∧ (typeBVec e.1) 0 = 0)).card = 0 := by
  decide
theorem count_spin16_typeA :
    (Finset.univ.filter (fun d : TypeAData =>
      IsE6Root (typeAVec d) ∧ (typeAVec d) 0 = -1)).card = 0 := by
  decide
theorem count_spin16_typeB :
    (Finset.univ.filter (fun e : TypeBData =>
      IsE6Root (typeBVec e.1) ∧ (typeBVec e.1) 0 = -1)).card = 16 := by
  decide
theorem count_spin16bar_typeA :
    (Finset.univ.filter (fun d : TypeAData =>
      IsE6Root (typeAVec d) ∧ (typeAVec d) 0 = 1)).card = 0 := by
  decide
theorem count_spin16bar_typeB :
    (Finset.univ.filter (fun e : TypeBData =>
      IsE6Root (typeBVec e.1) ∧ (typeBVec e.1) 0 = 1)).card = 16 := by
  decide

/-- There are 40 D5 roots, all of Type A. -/
theorem d5Finset_card : d5Finset.card = 40 := by
  rw [d5Finset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_d5_typeA, count_d5_typeB]

/-- There are 16 spinor roots with first coordinate -1, all of Type B. -/
theorem spin16Finset_card : spin16Finset.card = 16 := by
  rw [spin16Finset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_spin16_typeA, count_spin16_typeB]

/-- There are 16 spinor roots with first coordinate 1, all of Type B. -/
theorem spin16barFinset_card : spin16barFinset.card = 16 := by
  rw [spin16barFinset, card_filter_root, card_filter_typeA, card_filter_typeB,
    count_spin16bar_typeA, count_spin16bar_typeB]

/-- The E6 roots split into D5 (40) plus two spinor sets (16 + 16):
    `40 + 16 + 16 = 72`. -/
theorem e6_partition : d5Finset ∪ spin16Finset ∪ spin16barFinset = e6Finset := by
  have hsub1 : d5Finset ⊆ e6Finset := by
    intro y hy
    rw [d5Finset, Finset.mem_filter] at hy
    rw [e6Finset, Finset.mem_filter]
    exact ⟨hy.1, hy.2.1⟩
  have hsub2 : spin16Finset ⊆ e6Finset := by
    intro y hy
    rw [spin16Finset, Finset.mem_filter] at hy
    rw [e6Finset, Finset.mem_filter]
    exact ⟨hy.1, hy.2.1⟩
  have hsub3 : spin16barFinset ⊆ e6Finset := by
    intro y hy
    rw [spin16barFinset, Finset.mem_filter] at hy
    rw [e6Finset, Finset.mem_filter]
    exact ⟨hy.1, hy.2.1⟩
  apply Finset.eq_of_subset_of_card_le
  · simp only [Finset.union_subset_iff]
    exact ⟨⟨hsub1, hsub2⟩, hsub3⟩
  · rw [e6Finset_card]
    have hd1 : Disjoint d5Finset spin16Finset := by
      rw [Finset.disjoint_left]
      intro y hy1 hy2
      rw [d5Finset, Finset.mem_filter] at hy1
      rw [spin16Finset, Finset.mem_filter] at hy2
      obtain ⟨-, -, h0⟩ := hy1
      obtain ⟨-, -, h0'⟩ := hy2
      omega
    have hd2 : Disjoint d5Finset spin16barFinset := by
      rw [Finset.disjoint_left]
      intro y hy1 hy2
      rw [d5Finset, Finset.mem_filter] at hy1
      rw [spin16barFinset, Finset.mem_filter] at hy2
      obtain ⟨-, -, h0⟩ := hy1
      obtain ⟨-, -, h0'⟩ := hy2
      omega
    have hd3 : Disjoint spin16Finset spin16barFinset := by
      rw [Finset.disjoint_left]
      intro y hy1 hy2
      rw [spin16Finset, Finset.mem_filter] at hy1
      rw [spin16barFinset, Finset.mem_filter] at hy2
      obtain ⟨-, -, h0⟩ := hy1
      obtain ⟨-, -, h0'⟩ := hy2
      omega
    have hu : Disjoint (d5Finset ∪ spin16Finset) spin16barFinset :=
      Finset.disjoint_union_left.mpr ⟨hd2, hd3⟩
    rw [Finset.card_union_of_disjoint hu, Finset.card_union_of_disjoint hd1,
      d5Finset_card, spin16Finset_card, spin16barFinset_card]

/-- The five simple roots of the D5 (SO(10)) subsystem: the first five E6
    simple roots. -/
def d5SimpleRoot : Fin 5 → Vec
  | 0 => ![0, 0, 0, 2, -2, 0, 0, 0]
  | 1 => ![0, 0, 0, 0, 2, -2, 0, 0]
  | 2 => ![0, 0, 0, 0, 0, 2, -2, 0]
  | 3 => ![0, 0, 0, 0, 0, 0, 2, -2]
  | 4 => ![0, 0, 0, 0, 0, 0, 2, 2]

theorem d5SimpleRoot_isRoot (i : Fin 5) : IsE8Root (d5SimpleRoot i) := by
  fin_cases i <;> refine ⟨⟨?_, ?_⟩, ?_⟩ <;> decide

theorem d5SimpleRoot_mem (i : Fin 5) : d5SimpleRoot i ∈ d5Finset := by
  rw [d5Finset, Finset.mem_filter]
  constructor
  · exact mem_rootFinset_iff.mpr (d5SimpleRoot_isRoot i)
  · fin_cases i <;> decide

/-- The D5 Cartan matrix (fork at node 2, zero-indexed). -/
def cartanD5 : Matrix (Fin 5) (Fin 5) ℤ :=
  !![2, -1, 0, 0, 0;
     -1, 2, -1, 0, 0;
     0, -1, 2, -1, -1;
     0, 0, -1, 2, 0;
     0, 0, -1, 0, 2]

/-- The Gram matrix of the D5 simple roots is `4 ×` the D5 Cartan matrix.
    This identifies the 40-root set as the D5 (SO(10)) root system. -/
theorem d5_gram_eq_four_cartan (i j : Fin 5) :
    dot (d5SimpleRoot i) (d5SimpleRoot j) = 4 * cartanD5 i j := by
  fin_cases i <;> fin_cases j <;> decide

/-- The 16 weights of the 27 (first coordinate -1, U(1) charge 1). -/
def weights16 : Finset Vec := weights27.filter (fun w => w 0 = -1)

/-- The 10 weights of the 27 (first coordinate 2, U(1) charge -2). -/
def weights10 : Finset Vec := weights27.filter (fun w => w 0 = 2)

/-- The singlet weight of the 27 (first coordinate -4, U(1) charge 4). -/
def weights1 : Finset Vec := weights27.filter (fun w => w 0 = -4)

theorem weights16_card : weights16.card = 16 := by decide
theorem weights10_card : weights10.card = 10 := by decide
theorem weights1_card : weights1.card = 1 := by decide

/-- The 27 weights split into 16 + 10 + 1. -/
theorem weights27_partition : weights16 ∪ weights10 ∪ weights1 = weights27 := by
  apply Finset.eq_of_subset_of_card_le
  · simp only [Finset.union_subset_iff]
    exact ⟨⟨Finset.filter_subset _ _, Finset.filter_subset _ _⟩,
      Finset.filter_subset _ _⟩
  · rw [weights27_card]
    have hd1 : Disjoint weights16 weights10 := by
      rw [Finset.disjoint_left]
      intro w hw1 hw2
      rw [weights16, Finset.mem_filter] at hw1
      rw [weights10, Finset.mem_filter] at hw2
      obtain ⟨-, h0⟩ := hw1
      obtain ⟨-, h0'⟩ := hw2
      omega
    have hd2 : Disjoint weights16 weights1 := by
      rw [Finset.disjoint_left]
      intro w hw1 hw2
      rw [weights16, Finset.mem_filter] at hw1
      rw [weights1, Finset.mem_filter] at hw2
      obtain ⟨-, h0⟩ := hw1
      obtain ⟨-, h0'⟩ := hw2
      omega
    have hd3 : Disjoint weights10 weights1 := by
      rw [Finset.disjoint_left]
      intro w hw1 hw2
      rw [weights10, Finset.mem_filter] at hw1
      rw [weights1, Finset.mem_filter] at hw2
      obtain ⟨-, h0⟩ := hw1
      obtain ⟨-, h0'⟩ := hw2
      omega
    have hu : Disjoint (weights16 ∪ weights10) weights1 :=
      Finset.disjoint_union_left.mpr ⟨hd2, hd3⟩
    rw [Finset.card_union_of_disjoint hu, Finset.card_union_of_disjoint hd1,
      weights16_card, weights10_card, weights1_card]

/-- The U(1) charge of a 27-weight: minus its first coordinate. -/
def u1Charge27 (w : Vec) : ℤ := -w 0

/-- The 16 weights carry U(1) charge 1. -/
theorem charge_weights16 (w : Vec) (hw : w ∈ weights16) : u1Charge27 w = 1 := by
  rw [weights16, Finset.mem_filter] at hw
  show -w 0 = 1
  omega

/-- The 10 weights carry U(1) charge -2. -/
theorem charge_weights10 (w : Vec) (hw : w ∈ weights10) : u1Charge27 w = -2 := by
  rw [weights10, Finset.mem_filter] at hw
  show -w 0 = -2
  omega

/-- The singlet weight carries U(1) charge 4. -/
theorem charge_weights1 (w : Vec) (hw : w ∈ weights1) : u1Charge27 w = 4 := by
  rw [weights1, Finset.mem_filter] at hw
  show -w 0 = 4
  omega

/-- The U(1) charge of an E6 root: minus three times its first coordinate.
    This is the same linear functional as `u1Charge27`, on unscaled roots:
    charge = `-(y 0 + y 1 + y 2) = -3 * y 0` for E6 roots. -/
def u1Charge78 (y : Vec) : ℤ := -3 * y 0

/-- The D5 roots carry U(1) charge 0. -/
theorem charge_d5 (y : Vec) (hy : y ∈ d5Finset) : u1Charge78 y = 0 := by
  rw [d5Finset, Finset.mem_filter] at hy
  show -3 * y 0 = 0
  omega

/-- The 16 spinor roots carry U(1) charge 3. -/
theorem charge_spin16 (y : Vec) (hy : y ∈ spin16Finset) : u1Charge78 y = 3 := by
  rw [spin16Finset, Finset.mem_filter] at hy
  show -3 * y 0 = 3
  omega

/-- The 16̄ spinor roots carry U(1) charge -3. -/
theorem charge_spin16bar (y : Vec) (hy : y ∈ spin16barFinset) : u1Charge78 y = -3 := by
  rw [spin16barFinset, Finset.mem_filter] at hy
  show -3 * y 0 = -3
  omega

/-- The SO(10) adjoint: 40 roots + 5 Cartan generators. -/
theorem so10_adjoint_dim : d5Finset.card + 5 = 45 := by rw [d5Finset_card]

/-- **Step 2, the 27.** `27 = 16(1) ⊕ 10(-2) ⊕ 1(4)` under SO(10) × U(1). -/
theorem step2_branching_27 : weights16.card + weights10.card + weights1.card = 27 := by
  rw [weights16_card, weights10_card, weights1_card]

/-- **Step 2, the 78.** `78 = 1(0) ⊕ 45(0) ⊕ 16(3) ⊕ 16̄(-3)` under
    SO(10) × U(1): the singlet is the U(1) Cartan generator. -/
theorem step2_branching_78 :
    1 + (d5Finset.card + 5) + spin16Finset.card + spin16barFinset.card = 78 := by
  rw [d5Finset_card, spin16Finset_card, spin16barFinset_card]

-- =========================================================================
-- 10. Step 3: the composed decomposition
-- =========================================================================

/-- **Step 3.** Substituting Step 2 into Step 1, the 248 decomposes under
    SU(3) × SO(10) × U(1) as
    `(1,16)(3) ⊕ (1,16̄)(-3) ⊕ (3,16)(1) ⊕ (3̄,16̄)(-1) ⊕ (3,10)(-2) ⊕
    (3̄,10)(2) ⊕ (3,1)(4) ⊕ (3̄,1)(-4) ⊕ (8,1)(0) ⊕ (1,45)(0) ⊕ (1,1)(0)`:
    `16 + 16 + 48 + 48 + 30 + 30 + 3 + 3 + 8 + 45 + 1 = 248`.
    Each term is a proven count: the `3 ×` factors are the SU(3) triplets
    (`branch27_three_to_one`), the 8 is the SU(3) adjoint, the 45 is the
    SO(10) adjoint, and the final 1 is the U(1) Cartan generator. -/
theorem step3_branching :
    spin16Finset.card + spin16barFinset.card +
    3 * weights16.card + 3 * weights16.card +
    3 * weights10.card + 3 * weights10.card +
    3 * weights1.card + 3 * weights1.card +
    (su3Finset.card + 2) + (d5Finset.card + 5) + 1 = 248 := by
  rw [spin16Finset_card, spin16barFinset_card, weights16_card, weights10_card,
    weights1_card, su3Finset_card, d5Finset_card]

/-- Step 3 as a bare dimension identity. -/
theorem step3_dimension :
    16 + 16 + 3 * 16 + 3 * 16 + 3 * 10 + 3 * 10 + 3 * 1 + 3 * 1 + 8 + 45 + 1 = 248 := by
  norm_num

-- =========================================================================
-- 11. The main theorem and the axiom audit
-- =========================================================================

/-- **The E8 → SO(10) branching, at the weight level.** The 240 roots
    partition into the E6 roots (72), the SU(3) roots (6), the (3,27)
    weights (81), and the (3̄,27̄) weights (81); the (3,27) roots project
    3-to-1 onto 27 weights; the E6 roots split into D5 (40) plus two
    spinor sets (16 + 16); the 27 weights split into 16 + 10 + 1; and the
    composed dimensions sum to 248. -/
theorem e8_to_so10_branching :
    e6Finset.card = 72 ∧ su3Finset.card = 6 ∧
    branch27Finset.card = 81 ∧ branch27barFinset.card = 81 ∧
    e6Finset ∪ su3Finset ∪ branch27Finset ∪ branch27barFinset = rootFinset ∧
    weights27.card = 27 ∧ branch27Finset.card = 3 * weights27.card ∧
    d5Finset.card = 40 ∧ spin16Finset.card = 16 ∧ spin16barFinset.card = 16 ∧
    weights16.card = 16 ∧ weights10.card = 10 ∧ weights1.card = 1 ∧
    16 + 16 + 3 * 16 + 3 * 16 + 3 * 10 + 3 * 10 + 3 * 1 + 3 * 1 + 8 + 45 + 1 = 248 := by
  exact ⟨e6Finset_card, su3Finset_card, branch27Finset_card, branch27barFinset_card,
    branch_partition, weights27_card, branch27_three_to_one,
    d5Finset_card, spin16Finset_card, spin16barFinset_card,
    weights16_card, weights10_card, weights1_card, step3_dimension⟩

-- The headline theorems depend only on the standard Lean axioms.
#print axioms e8_to_so10_branching
#print axioms e6_gram_eq_four_cartan
#print axioms su3_gram_eq_four_cartan
#print axioms d5_gram_eq_four_cartan
#print axioms branch_partition
#print axioms branch27_three_to_one

end ResNova.E8Branching
