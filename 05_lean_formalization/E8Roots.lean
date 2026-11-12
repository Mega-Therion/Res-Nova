import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic

/-!
# E8Roots: The E8 Root System, Formalized

Author: R.W. Yett (ORCID: 0009-0001-1303-7190)
Project: Res Nova / Chyren Autonomous Verification Pipeline
Date: 2026-11-11

The E8 root system: 240 roots, the exceptional lattice, the bottle of the
whole program. This file formalizes it on the **doubled integer lattice**,
which clears the halves and keeps every coordinate an integer.

## The doubled lattice

The standard E8 lattice is `L = {x ∈ ℤ⁸ ∪ (ℤ+½)⁸ : Σxᵢ even}`, with roots
the norm² = 2 vectors. Doubling, `L' = 2L` is the set of `y ∈ ℤ⁸` with all
coordinates of the same parity and `Σyᵢ ≡ 0 [ZMOD 4]`; the roots become the
norm² = 8 vectors. Nothing is lost: `y ↦ y/2` is a bijection `L' → L`, and
every statement here divides through by 2 (norms by 4).

## What is proved

1. **Lattice structure.** `L'` is closed under `0`, `+`, `-`, and `ℤ`-scaling;
   every lattice vector has `8 ∣ ‖y‖²` (the lattice is even).
2. **Classification.** Every root is Type A (exactly two coordinates `±2`,
   rest `0`) or Type B (all coordinates `±1`, even number of `-1`).
3. **The count.** There are exactly 240 roots: 112 of Type A, 128 of Type B.
4. **Root-system axioms.** Negation-closed; reflection-closed
   (`s_α(β) = β - (⟨β,α⟩/4)·α` is a root); Cartan integers are integers.
   The key step is `4 ∣ ⟨α,β⟩` for any two roots, proved by polarization
   from the evenness of the lattice — no case analysis needed.
5. **Simple roots + Cartan matrix.** Eight explicit simple roots; their Gram
   matrix is `4 ×` the E8 Cartan matrix; the Dynkin diagram is E8
   (chain 1–2–3–4–5–6–7 with the branch at 5).

## Status

- Unimodularity (`det(Cartan) = 1`, equivalently the simple roots generate
  the full lattice) is the natural next step; it is NOT in this file yet.
  The determinant is verified numerically (`det = 1`, basis `det = 256`
  in doubled coordinates) but the Lean proof by cofactor recursion is
  deferred to a follow-up.
- The E8 → SO(10) branching (`248 = 120 ⊕ 128`, `248 = (8,1) ⊕ (1,78) ⊕
  (3,27) ⊕ (3̄,27̄)`) is representation theory, not root combinatorics;
  it is a separate, larger formalization. This file is the roots.

## Axioms

Standard Lean axioms only: `[propext, Classical.choice, Quot.sound]`.
Zero `sorry`. Verified by `#print axioms` at the end of the file.
-/

namespace ResNova.E8Roots

/-- A vector in ℤ⁸, as a function on `Fin 8`. -/
abbrev Vec := Fin 8 → ℤ

/-- The standard dot product on ℤ⁸. -/
def dot (x y : Vec) : ℤ := ∑ i, x i * y i

/-- The squared norm. -/
def normSq (x : Vec) : ℤ := dot x x

/-- The doubled E8 lattice `L' = 2L`: all coordinates of the same parity,
    and the coordinate sum divisible by 4. -/
def InE8Lattice (y : Vec) : Prop :=
  ((∀ i, Even (y i)) ∨ (∀ i, Odd (y i))) ∧ 4 ∣ ∑ i, y i

/-- The E8 roots: lattice vectors of squared norm 8
    (norm² 2 in the undoubled lattice). -/
def IsE8Root (y : Vec) : Prop := InE8Lattice y ∧ normSq y = 8

/-- Type A roots: exactly two coordinates `±2`, the rest `0`. -/
def IsTypeA (y : Vec) : Prop :=
  ∃ i j, i ≠ j ∧ (y i = 2 ∨ y i = -2) ∧ (y j = 2 ∨ y j = -2) ∧
    ∀ k, k ≠ i → k ≠ j → y k = 0

/-- Type B roots: every coordinate `±1`, with an even number of `-1`s. -/
def IsTypeB (y : Vec) : Prop :=
  (∀ i, y i = 1 ∨ y i = -1) ∧
    Even (Finset.univ.filter (fun i => y i = -1)).card

-- =========================================================================
-- 1. Dot product algebra
-- =========================================================================

theorem dot_comm (x y : Vec) : dot x y = dot y x := by
  simp [dot, mul_comm]

theorem dot_add (x y z : Vec) : dot x (y + z) = dot x y + dot x z := by
  simp [dot, Pi.add_apply, mul_add, Finset.sum_add_distrib]

theorem dot_sub (x y z : Vec) : dot x (y - z) = dot x y - dot x z := by
  simp [dot, Pi.sub_apply, mul_sub, Finset.sum_sub_distrib]

theorem dot_smul_int (k : ℤ) (x y : Vec) : dot x (k • y) = k * dot x y := by
  simp [dot, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem dot_self_nonneg (x : Vec) : 0 ≤ normSq x := by
  simp only [normSq, dot]
  apply Finset.sum_nonneg
  intro i _
  exact mul_self_nonneg (x i)

theorem normSq_add (x y : Vec) :
    normSq (x + y) = normSq x + 2 * dot x y + normSq y := by
  have h : ∀ i : Fin 8, (x i + y i) * (x i + y i) =
      x i * x i + 2 * (x i * y i) + y i * y i := fun i => by ring
  simp only [normSq, dot, Pi.add_apply]
  rw [Finset.sum_congr rfl (fun i _ => h i)]
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.mul_sum]

theorem normSq_sub (x y : Vec) :
    normSq (x - y) = normSq x - 2 * dot x y + normSq y := by
  have h : ∀ i : Fin 8, (x i - y i) * (x i - y i) =
      x i * x i - 2 * (x i * y i) + y i * y i := fun i => by ring
  simp only [normSq, dot, Pi.sub_apply]
  rw [Finset.sum_congr rfl (fun i _ => h i)]
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum]

-- =========================================================================
-- 2. The lattice is a subgroup of ℤ⁸, and it is even
-- =========================================================================

theorem lattice_zero : InE8Lattice 0 := by
  constructor
  · left
    intro i
    exact ⟨0, by simp⟩
  · simp

theorem lattice_add {x y : Vec} (hx : InE8Lattice x) (hy : InE8Lattice y) :
    InE8Lattice (x + y) := by
  obtain ⟨hxpar, hxsum⟩ := hx
  obtain ⟨hypar, hysum⟩ := hy
  constructor
  · rcases hxpar with hxe | hxo <;> rcases hypar with hye | hyo
    · left
      intro i
      exact (hxe i).add (hye i)
    · -- even + odd = odd, coordinatewise
      right
      intro i
      exact Even.add_odd (hxe i) (hyo i)
    · right
      intro i
      exact Odd.add_even (hxo i) (hye i)
    · left
      intro i
      exact (hxo i).add_odd (hyo i)
  · -- sum (x+y) = sum x + sum y, both divisible by 4
    have hsum : ∑ i, (x + y) i = (∑ i, x i) + ∑ i, y i := by
      simp [Pi.add_apply, Finset.sum_add_distrib]
    rw [hsum]
    exact dvd_add hxsum hysum

theorem lattice_neg {x : Vec} (hx : InE8Lattice x) : InE8Lattice (-x) := by
  obtain ⟨hpar, hsum⟩ := hx
  constructor
  · rcases hpar with h | h
    · left
      intro i
      exact Even.neg (h i)
    · right
      intro i
      exact Odd.neg (h i)
  · have hsum' : ∑ i, (-x) i = -(∑ i, x i) := by
      simp [Pi.neg_apply, Finset.sum_neg_distrib]
    rw [hsum']
    exact dvd_neg.mpr hsum

theorem lattice_smul_int {k : ℤ} {x : Vec} (hx : InE8Lattice x) :
    InE8Lattice (k • x) := by
  obtain ⟨hpar, hsum⟩ := hx
  constructor
  · rcases hpar with h | h
    · left
      intro i
      exact Even.mul_left (h i) k
    · -- k * odd: even if k even, odd if k odd. Split on k's parity.
      by_cases hk : Even k
      · left
        intro i
        obtain ⟨r, hr⟩ := hk
        exact ⟨r * x i, by simp [Pi.smul_apply, smul_eq_mul, hr]; ring⟩
      · right
        intro i
        have hko : Odd k := Int.not_even_iff_odd.mp hk
        exact hko.mul (h i)
  · have hsum' : ∑ i, (k • x) i = k * (∑ i, x i) := by
      simp [Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
    rw [hsum']
    exact Dvd.dvd.mul_left hsum k

/-- An odd square is `1 mod 8`. -/
theorem odd_sq_mod_eight {x : ℤ} (hx : Odd x) : x ^ 2 % 8 = 1 := by
  obtain ⟨k, hk⟩ := hx
  obtain ⟨m, hm⟩ := Int.even_mul_succ_self k
  have hsq : (2 * k + 1) ^ 2 = 8 * m + 1 := by
    have h1 : (2 * k + 1) ^ 2 = 4 * (k * (k + 1)) + 1 := by ring
    rw [h1, hm]
    ring
  rw [hk, hsq]
  omega

/-- Every lattice vector has squared norm divisible by 8.
    This is the evenness of the E8 lattice (in doubled coordinates). -/
theorem lattice_normSq_dvd_eight {y : Vec} (hy : InE8Lattice y) :
    8 ∣ normSq y := by
  obtain ⟨hpar, hsum⟩ := hy
  rcases hpar with heven | hodd
  · -- All coordinates even: y = 2z, ‖y‖² = 4‖z‖², and ‖z‖² is even
    -- because ‖z‖² ≡ Σzᵢ (mod 2) and Σzᵢ is even (from 4 ∣ 2Σzᵢ).
    choose z hz using fun i => heven i
    -- hz : ∀ i, y i = z i + z i
    have hy2 : ∀ i, y i = 2 * z i := fun i => by rw [hz i]; ring
    have hsumz : 2 ∣ ∑ i, z i := by
      have h1 : ∑ i, y i = 2 * (∑ i, z i) := by
        rw [Finset.sum_congr rfl (fun i _ => hy2 i)]
        simp [Finset.mul_sum]
      rw [h1] at hsum
      omega
    -- ‖z‖² ≡ Σzᵢ (mod 2): work in ZMod 2.
    have hzmod : ((normSq z : ℤ) : ZMod 2) = 0 := by
      have hcast : ((normSq z : ℤ) : ZMod 2) = ∑ i, ((z i : ZMod 2) ^ 2) := by
        simp only [normSq, dot, Int.cast_sum, Int.cast_mul, Int.cast_pow, ← pow_two]
      rw [hcast]
      have hsq2 : ∀ a : ZMod 2, a ^ 2 = a := by decide
      simp only [hsq2, ← Int.cast_sum]
      exact (ZMod.intCast_zmod_eq_zero_iff_dvd _ _).mpr hsumz
    have h2z : 2 ∣ normSq z :=
      (ZMod.intCast_zmod_eq_zero_iff_dvd _ _).mp hzmod
    obtain ⟨t, ht⟩ := h2z
    use t
    have hnorm : normSq y = 4 * normSq z := by
      simp only [normSq, dot]
      rw [Finset.sum_congr rfl (fun i _ => by rw [hy2 i]; ring : ∀ i ∈ Finset.univ, (y i) * (y i) = 4 * ((z i) * (z i)))]
      rw [Finset.mul_sum]
    rw [hnorm, ht]
    ring
  · -- All coordinates odd: each square is 1 mod 8, and there are 8 of them.
    have hmod : ((normSq y : ℤ) : ZMod 8) = 0 := by
      have hcast : ((normSq y : ℤ) : ZMod 8) = ∑ i, ((y i : ZMod 8) ^ 2) := by
        simp only [normSq, dot, Int.cast_sum, Int.cast_mul, Int.cast_pow, ← pow_two]
      rw [hcast]
      have h1 : ∀ i : Fin 8, ((y i : ZMod 8) ^ 2) = 1 := by
        intro i
        have h := odd_sq_mod_eight (hodd i)
        have h2 : (((y i) ^ 2 : ℤ) : ZMod 8) = ((1 : ℤ) : ZMod 8) := by
          rw [ZMod.intCast_eq_intCast_iff]
          show (y i) ^ 2 % 8 = 1 % 8
          rw [h]
          norm_num
        have h3 : ((y i : ZMod 8) ^ 2) = (((y i) ^ 2 : ℤ) : ZMod 8) := by
          push_cast
          ring
        rw [h3, h2]
        simp
      simp only [h1]
      decide
    exact (ZMod.intCast_zmod_eq_zero_iff_dvd _ _).mp hmod

-- =========================================================================
-- 3. The key lemma: inner products of roots are divisible by 4
-- =========================================================================

/-- Polarization: `2⟨x,y⟩ = ‖x+y‖² - ‖x‖² - ‖y‖²`. -/
theorem two_dot_eq (x y : Vec) :
    2 * dot x y = normSq (x + y) - normSq x - normSq y := by
  rw [normSq_add]
  ring

/-- The inner product of any two roots is divisible by 4.
    Proof: polarization + evenness of the lattice. No case analysis. -/
theorem root_dot_div_four {α β : Vec} (hα : IsE8Root α) (hβ : IsE8Root β) :
    4 ∣ dot α β := by
  have hlat : InE8Lattice (α + β) := lattice_add hα.1 hβ.1
  have h8 := lattice_normSq_dvd_eight hlat
  have h2 := two_dot_eq α β
  rw [hα.2, hβ.2] at h2
  -- 2⟨α,β⟩ = ‖α+β‖² - 16, and 8 ∣ ‖α+β‖², so 8 ∣ 2⟨α,β⟩, so 4 ∣ ⟨α,β⟩.
  omega

/-- Negation of a root is a root. -/
theorem root_neg {y : Vec} (hy : IsE8Root y) : IsE8Root (-y) := by
  constructor
  · exact lattice_neg hy.1
  · simp only [normSq, dot, Pi.neg_apply, neg_mul_neg]
    exact hy.2

/-- Reflection of a root through another root's hyperplane.
    `s_α(β) = β - (⟨β,α⟩/4)·α`; the division is exact by `root_dot_div_four`. -/
def reflect (α β : Vec) : Vec := β - (dot β α / 4) • α

/-- Reflection of a root is a root. -/
theorem root_reflect {α β : Vec} (hα : IsE8Root α) (hβ : IsE8Root β) :
    IsE8Root (reflect α β) := by
  have hdiv := root_dot_div_four hβ hα
  obtain ⟨k, hk⟩ := hdiv
  -- dot β α = 4k, so dot β α / 4 = k
  have hk4 : dot β α / 4 = k := by rw [hk]; omega
  constructor
  · -- lattice: β - k•α, closed under smul, neg, add
    have h1 : InE8Lattice (k • α) := lattice_smul_int hα.1
    have h2 : InE8Lattice (-(k • α)) := lattice_neg h1
    have h3 : InE8Lattice (β + -(k • α)) := lattice_add hβ.1 h2
    have h4 : reflect α β = β + -(k • α) := by
      simp [reflect, hk4, sub_eq_add_neg]
    rw [h4]
    exact h3
  · -- norm: ‖β - kα‖² = ‖β‖² - 2k⟨β,α⟩ + k²‖α‖² = 8 - 8k² + 8k² = 8
    have hdot : dot β α = 4 * k := hk
    have hnorm : normSq (reflect α β) = 8 := by
      have h4 : reflect α β = β - k • α := by simp [reflect, hk4]
      rw [h4]
      rw [normSq_sub]
      have hd1 : dot β (k • α) = k * dot β α := dot_smul_int k β α
      have hd2 : normSq (k • α) = k ^ 2 * normSq α := by
        have e1 : dot (k • α) (k • α) = k * dot (k • α) α :=
          dot_smul_int k (k • α) α
        have e2 : dot (k • α) α = k * dot α α := by
          rw [dot_comm (k • α) α]
          exact dot_smul_int k α α
        simp only [normSq]
        rw [e1, e2]
        ring
      rw [hd1, hd2, hα.2, hβ.2, hdot]
      ring
    exact hnorm

/-- The Cartan integer `2⟨β,α⟩/⟨α,α⟩` is an integer: it equals `⟨β,α⟩/4`. -/
theorem cartan_int {α β : Vec} (hα : IsE8Root α) (hβ : IsE8Root β) :
    ∃ k : ℤ, 2 * dot β α = k * normSq α := by
  obtain ⟨k, hk⟩ := root_dot_div_four hβ hα
  exact ⟨k, by rw [hα.2, hk]; ring⟩

-- =========================================================================
-- 4. Classification: every root is Type A or Type B
-- =========================================================================

/-- A root's coordinates are bounded by 2 in absolute value. -/
theorem root_coord_bound {y : Vec} (hy : IsE8Root y) (i : Fin 8) : |y i| ≤ 2 := by
  have h2 : ∑ j, (y j) ^ 2 = 8 := by
    have h3 : ∑ j, (y j) ^ 2 = ∑ j, y j * y j :=
      Finset.sum_congr rfl (fun j _ => pow_two (y j))
    rw [h3]
    exact hy.2
  have hle : (y i) ^ 2 ≤ 8 := by
    have h1 : (y i) ^ 2 ≤ ∑ j, (y j) ^ 2 :=
      Finset.single_le_sum (fun j _ => sq_nonneg (y j)) (Finset.mem_univ i)
    omega
  by_contra h
  push_neg at h
  have h3 : (3 : ℤ) ≤ |y i| := by omega
  have h9 : (9 : ℤ) ≤ (y i) ^ 2 := by
    have h4 : |y i| ^ 2 = (y i) ^ 2 := sq_abs (y i)
    rw [← h4]
    nlinarith [h3]
  omega

/-- Each squared coordinate of a root is 0, 1, or 4. -/
theorem root_sq_mem {y : Vec} (hy : IsE8Root y) (i : Fin 8) :
    (y i) ^ 2 = 0 ∨ (y i) ^ 2 = 1 ∨ (y i) ^ 2 = 4 := by
  have hb := root_coord_bound hy i
  obtain ⟨hlo, hhi⟩ := abs_le.mp hb
  interval_cases (y i) <;> simp

/-- The classification theorem: every E8 root is Type A or Type B.
    The norm equation `4a + b = 8` (with `a` = #{sq = 4}, `b` = #{sq = 1})
    leaves `(a,b) ∈ {(2,0), (1,4), (0,8)}`; the lattice parity condition
    kills `(1,4)`, since one `±2` (even) and four `±1` (odd) cannot coexist
    in a vector whose coordinates are all of the same parity. -/
theorem root_classification {y : Vec} (hy : IsE8Root y) : IsTypeA y ∨ IsTypeB y := by
  classical
  -- A := {i | (y i)^2 = 4}, B := {i | (y i)^2 = 1}
  set A := Finset.univ.filter (fun i => (y i) ^ 2 = 4) with hA
  set B := Finset.univ.filter (fun i => (y i) ^ 2 = 1) with hB
  have hmemA : ∀ i, i ∈ A ↔ (y i) ^ 2 = 4 := by
    intro i
    simp only [hA, Finset.mem_filter, Finset.mem_univ, true_and]
  have hmemB : ∀ i, i ∈ B ↔ (y i) ^ 2 = 1 := by
    intro i
    simp only [hB, Finset.mem_filter, Finset.mem_univ, true_and]
  -- The norm equation: 4|A| + |B| = 8
  have hsplit : ∀ i : Fin 8, (y i) ^ 2 =
      4 * (if (y i) ^ 2 = 4 then (1 : ℤ) else 0) +
        (if (y i) ^ 2 = 1 then (1 : ℤ) else 0) := by
    intro i
    rcases root_sq_mem hy i with h | h | h <;> simp [h]
  have hnorm8 : ∑ i, (y i) ^ 2 = 8 := by
    have h3 : ∑ i, (y i) ^ 2 = ∑ i, y i * y i :=
      Finset.sum_congr rfl (fun i _ => pow_two (y i))
    rw [h3]
    exact hy.2
  have hsum : 4 * A.card + B.card = 8 := by
    have h1 : ∑ i, (y i) ^ 2 =
        4 * (∑ i, if (y i) ^ 2 = 4 then (1 : ℤ) else 0) +
          ∑ i, if (y i) ^ 2 = 1 then (1 : ℤ) else 0 := by
      rw [Finset.sum_congr rfl (fun i _ => hsplit i)]
      rw [Finset.sum_add_distrib, ← Finset.mul_sum]
    rw [hnorm8, Finset.sum_boole, Finset.sum_boole] at h1
    -- h1 : 8 = 4 * ↑A.card + ↑B.card (in ℤ); flip and cast to ℕ
    rw [← hA, ← hB] at h1
    exact_mod_cast h1.symm
  -- |A| + |B| ≤ 8 (disjoint subsets of an 8-element set)
  have hdisj : Disjoint A B := by
    rw [Finset.disjoint_left]
    intro i hAi hBi
    rw [hmemA] at hAi
    rw [hmemB] at hBi
    omega
  have hle : A.card + B.card ≤ 8 := by
    have hcard : (A ∪ B).card = A.card + B.card :=
      Finset.card_union_of_disjoint hdisj
    have hsub : (A ∪ B).card ≤ 8 := by
      have h := Finset.card_le_card (Finset.subset_univ (A ∪ B))
      simpa using h
    omega
  have hcases : (A.card = 2 ∧ B.card = 0) ∨ (A.card = 1 ∧ B.card = 4) ∨
      (A.card = 0 ∧ B.card = 8) := by omega
  rcases hcases with ⟨ha, hb⟩ | ⟨ha, hb⟩ | ⟨ha, hb⟩
  · -- (2, 0): Type A
    left
    obtain ⟨i, j, hij, hAij⟩ := Finset.card_eq_two.mp ha
    refine ⟨i, j, hij, ?_, ?_, ?_⟩
    · have hi : (y i) ^ 2 = 4 := by
        have : i ∈ A := by rw [hAij]; exact Finset.mem_insert_self i {j}
        exact (hmemA i).mp this
      have h := (sq_eq_sq_iff_eq_or_eq_neg (a := y i) (b := 2)).mp (by
        calc (y i) ^ 2 = 4 := hi
        _ = (2 : ℤ) ^ 2 := by norm_num)
      rcases h with h | h
      · exact Or.inl h
      · right
        calc y i = -2 := h
        _ = -(2 : ℤ) := by norm_num
    · have hj : (y j) ^ 2 = 4 := by
        have : j ∈ A := by
          rw [hAij]
          exact Finset.mem_insert_of_mem (Finset.mem_singleton_self j)
        exact (hmemA j).mp this
      have h := (sq_eq_sq_iff_eq_or_eq_neg (a := y j) (b := 2)).mp (by
        calc (y j) ^ 2 = 4 := hj
        _ = (2 : ℤ) ^ 2 := by norm_num)
      rcases h with h | h
      · exact Or.inl h
      · right
        calc y j = -2 := h
        _ = -(2 : ℤ) := by norm_num
    · intro k hki hkj
      have hkA : k ∉ A := by
        rw [hAij]
        simp [hki, hkj]
      have hkB : k ∉ B := by
        rw [Finset.card_eq_zero.mp hb]
        exact Finset.notMem_empty k
      have h4 := (hmemA k).not.mp hkA
      have h1 := (hmemB k).not.mp hkB
      rcases root_sq_mem hy k with h | h | h
      · -- (y k)^2 = 0 → y k = 0
        exact sq_eq_zero_iff.mp h
      · exact absurd h h1
      · exact absurd h h4
  · -- (1, 4): impossible by parity
    exfalso
    obtain ⟨i, hi⟩ := Finset.card_eq_one.mp ha
    have hBne : B.Nonempty := Finset.card_pos.mp (by omega : 0 < B.card)
    obtain ⟨j, hjB⟩ := hBne
    have hiA : i ∈ A := by rw [hi]; exact Finset.mem_singleton_self i
    have hsq_i : (y i) ^ 2 = 4 := (hmemA i).mp hiA
    have hsq_j : (y j) ^ 2 = 1 := (hmemB j).mp hjB
    have heven_i : Even (y i) := by
      have h := (sq_eq_sq_iff_eq_or_eq_neg (a := y i) (b := 2)).mp (by
        calc (y i) ^ 2 = 4 := hsq_i
        _ = (2 : ℤ) ^ 2 := by norm_num)
      rcases h with h | h
      · rw [h]
        exact even_two
      · rw [h]
        exact Even.neg even_two
    have hodd_j : Odd (y j) := by
      have h := (sq_eq_sq_iff_eq_or_eq_neg (a := y j) (b := 1)).mp (by
        calc (y j) ^ 2 = 1 := hsq_j
        _ = (1 : ℤ) ^ 2 := by norm_num)
      rcases h with h | h <;> rw [h]
      · exact odd_one
      · exact Odd.neg odd_one
    rcases hy.1.1 with hpar | hpar
    · -- all even, but y j is odd
      exact absurd (hpar j) (Int.not_even_iff_odd.mpr hodd_j)
    · -- all odd, but y i is even
      exact absurd (hpar i) (Int.not_odd_iff_even.mpr heven_i)
  · -- (0, 8): Type B
    right
    have hAempty : A = ∅ := Finset.card_eq_zero.mp ha
    have hBuniv : B = Finset.univ := by
      apply Finset.eq_univ_of_card _ hb
    constructor
    · intro i
      have hiB : i ∈ B := by rw [hBuniv]; exact Finset.mem_univ i
      have hsq : (y i) ^ 2 = 1 := (hmemB i).mp hiB
      have h := (sq_eq_sq_iff_eq_or_eq_neg (a := y i) (b := 1)).mp (by
        calc (y i) ^ 2 = 1 := hsq
        _ = (1 : ℤ) ^ 2 := by norm_num)
      rcases h with h | h
      · exact Or.inl h
      · right
        calc y i = -1 := h
        _ = -(1 : ℤ) := by norm_num
    · -- Even number of -1s: Σyᵢ = 8 - 2·#minus, and 4 ∣ Σyᵢ.
      set M := Finset.univ.filter (fun i => y i = -1) with hM
      have hall : ∀ i : Fin 8, y i = 1 ∨ y i = -1 := by
        intro i
        have hiB : i ∈ B := by rw [hBuniv]; exact Finset.mem_univ i
        have hsq : (y i) ^ 2 = 1 := (hmemB i).mp hiB
        have h := (sq_eq_sq_iff_eq_or_eq_neg (a := y i) (b := 1)).mp (by
          calc (y i) ^ 2 = 1 := hsq
          _ = (1 : ℤ) ^ 2 := by norm_num)
        rcases h with h | h
        · exact Or.inl h
        · right
          calc y i = -1 := h
          _ = -(1 : ℤ) := by norm_num
      have hsum2 : ∑ i, y i = 8 - 2 * (M.card : ℤ) := by
        have h1 : ∀ i : Fin 8, y i = 1 - 2 * (if y i = -1 then (1 : ℤ) else 0) := by
          intro i
          rcases hall i with h | h <;> simp [h]
        rw [Finset.sum_congr rfl (fun i _ => h1 i)]
        rw [Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_boole]
        simp [hM]
      have h4 := hy.1.2
      rw [hsum2] at h4
      -- 4 ∣ 8 - 2|M| → |M| = 4 - 2t, hence even (proved over ℤ, cast back)
      obtain ⟨t, ht⟩ := h4
      have hev : Even ((M.card : ℤ)) := ⟨2 - t, by omega⟩
      exact (Int.even_coe_nat _).mp hev

-- =========================================================================
-- 5. The count: exactly 240 roots
-- =========================================================================

/-- The data of a Type A root: an ordered pair of distinct positions
    (given in increasing order) and a sign for each. -/
abbrev TypeAData := {p : Fin 8 × Fin 8 // p.1 < p.2} × Bool × Bool

/-- The data of a Type B root: a sign pattern (`true` = `+1`, `false` = `-1`)
    with an even number of `-1`s. -/
abbrev TypeBData :=
  {ε : Fin 8 → Bool // Even (Finset.univ.filter (fun i => ε i = false)).card}

/-- There are 112 Type A data: C(8,2) = 28 position pairs × 4 sign choices. -/
theorem card_typeAData : Fintype.card TypeAData = 112 := by
  have h28 : Fintype.card {p : Fin 8 × Fin 8 // p.1 < p.2} = 28 := by
    rw [Fintype.card_subtype]
    decide
  simp [TypeAData, Fintype.card_prod, h28, Fintype.card_bool]

/-- Flipping coordinate 0 twice is the identity. -/
theorem flip_flip (ε : Fin 8 → Bool) :
    Function.update (Function.update ε 0 (!ε 0)) 0
      (!(Function.update ε 0 (!ε 0) 0)) = ε := by
  funext i
  by_cases hi : i = 0
  · subst hi
    simp
  · simp [Function.update, hi]

/-- Flipping coordinate 0 swaps the parity of the `-1` count. -/
theorem flip_parity (ε : Fin 8 → Bool) :
    Even (Finset.univ.filter (fun i => Function.update ε 0 (!ε 0) i = false)).card ↔
      Odd (Finset.univ.filter (fun i => ε i = false)).card := by
  -- Convert both sides to parity of integer sums (via Finset.sum_boole).
  have hsum : ∀ η : Fin 8 → Bool,
      (∑ i, if η i = false then (1 : ℤ) else 0) =
        ((Finset.univ.filter (fun i => η i = false)).card : ℤ) := by
    intro η
    rw [Finset.sum_boole]
  rw [← Int.even_coe_nat, ← Int.odd_coe_nat, ← hsum, ← hsum]
  -- Split both sums at coordinate 0; the tails agree.
  have hsplit : ∀ η : Fin 8 → Bool,
      (∑ i, if η i = false then (1 : ℤ) else 0) =
        (if η 0 = false then (1 : ℤ) else 0) +
          ∑ i ∈ Finset.univ.erase 0, if η i = false then (1 : ℤ) else 0 := by
    intro η
    exact (Finset.add_sum_erase _ _ (Finset.mem_univ 0)).symm
  rw [hsplit, hsplit]
  have htail : (∑ i ∈ Finset.univ.erase 0,
      if Function.update ε 0 (!ε 0) i = false then (1 : ℤ) else 0) =
      ∑ i ∈ Finset.univ.erase 0, if ε i = false then (1 : ℤ) else 0 := by
    apply Finset.sum_congr rfl
    intro i hi
    have hi0 : i ≠ 0 := by
      simpa using hi
    simp [Function.update, hi0]
  rw [htail]
  simp only [Function.update_self]
  by_cases h0 : ε 0 = false
  · simp [h0]
    rw [add_comm (1 : ℤ), ← Int.not_even_iff_odd, Int.even_add_one, not_not,
      Int.even_coe_nat]
  · have h0t : ε 0 = true := by
      cases hε : ε 0 <;> simp_all
    simp [h0, h0t]
    rw [add_comm (1 : ℤ), Int.even_add_one, Int.not_even_iff_odd, Int.odd_coe_nat]

/-- There are 128 Type B data: half of the 2^8 sign patterns have an even
    number of `-1`s, since flipping coordinate 0 swaps even and odd. -/
theorem card_typeBData : Fintype.card TypeBData = 128 := by
  rw [Fintype.card_subtype]
  -- E = even-parity patterns, O = odd-parity patterns; |E| + |O| = 256,
  -- and the flip gives |E| = |O|.
  set S := (Finset.univ : Finset (Fin 8 → Bool)) with hS
  set E := S.filter (fun ε =>
    Even (Finset.univ.filter (fun i => ε i = false)).card) with hE
  set O := S.filter (fun ε =>
    Odd (Finset.univ.filter (fun i => ε i = false)).card) with hO
  have hcardS : S.card = 256 := by
    simp [hS, Fintype.card_fun, Fintype.card_fin, Fintype.card_bool]
  have hEO : E.card + O.card = 256 := by
    have hunion : E ∪ O = S := by
      ext ε
      simp [hE, hO, hS]
      exact Nat.even_or_odd _
    have hdisj : Disjoint E O := by
      rw [Finset.disjoint_left]
      intro ε hEe hOo
      simp [hE, hO] at hEe hOo
      exact absurd hEe.2 (Nat.not_even_iff_odd.mpr hOo.2)
    have := Finset.card_union_of_disjoint hdisj
    rw [hunion, hcardS] at this
    exact this.symm
  have hEqO : E.card = O.card := by
    apply Finset.card_bij (fun ε _ => Function.update ε 0 (!ε 0))
    · intro ε hε
      have hEe : Even (Finset.univ.filter (fun i => ε i = false)).card := by
        simp only [hE, Finset.mem_filter] at hε
        exact hε.2
      have hOo : Odd (Finset.univ.filter
          (fun i => Function.update ε 0 (!ε 0) i = false)).card :=
        (flip_parity (Function.update ε 0 (!ε 0))).mp (by rw [flip_flip]; exact hEe)
      simp only [hO, Finset.mem_filter]
      exact ⟨by simp [hS], hOo⟩
    · intro ε₁ _ ε₂ _ h
      rw [← flip_flip ε₁, ← flip_flip ε₂, h]
    · intro ε hε
      refine ⟨Function.update ε 0 (!ε 0), ?_, flip_flip ε⟩
      have hOo : Odd (Finset.univ.filter (fun i => ε i = false)).card := by
        simp only [hO, Finset.mem_filter] at hε
        exact hε.2
      have hEe : Even (Finset.univ.filter
          (fun i => Function.update ε 0 (!ε 0) i = false)).card :=
        (flip_parity ε).mpr hOo
      simp only [hE, Finset.mem_filter]
      exact ⟨by simp [hS], hEe⟩
  omega

/-- Build a Type A root vector from its data. -/
def typeAVec (d : TypeAData) : Vec :=
  fun k => if k = d.1.1.1 then (if d.2.1 then 2 else -2)
           else if k = d.1.1.2 then (if d.2.2 then 2 else -2)
           else 0

/-- Build a Type B root vector from a sign pattern. -/
def typeBVec (ε : Fin 8 → Bool) : Vec := fun i => if ε i then 1 else -1

/-- Every Type A vector is a root. -/
theorem typeAVec_isRoot (d : TypeAData) : IsE8Root (typeAVec d) := by
  obtain ⟨⟨p, hp⟩, s1, s2⟩ := d
  obtain ⟨i, j⟩ := p
  constructor
  · constructor
    · left
      intro k
      by_cases h1 : k = i
      · subst h1
        simp only [typeAVec, if_true]
        cases s1 <;> simp
      · by_cases h2 : k = j
        · subst h2
          simp only [typeAVec, h1, if_false, if_true]
          cases s2 <;> simp
        · simp only [typeAVec, h1, h2, if_false]
          decide
    · -- sum = ±2 ± 2 ∈ {0, ±4}
      have hsum : ∑ k, typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData) k =
          (if s1 then (2 : ℤ) else -2) + (if s2 then (2 : ℤ) else -2) := by
        have h1 : ∑ k, typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData) k =
            ∑ k ∈ ({i, j} : Finset (Fin 8)),
              typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData) k := by
          symm
          apply Finset.sum_subset (Finset.subset_univ _)
          intro k _ hk
          have hki : k ≠ i := by
            simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hk
            exact hk.1
          have hkj : k ≠ j := by
            simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hk
            exact hk.2
          simp [typeAVec, hki, hkj]
        rw [h1]
        have hij : i ≠ j := ne_of_lt hp
        have hji : j ≠ i := hij.symm
        rw [Finset.sum_insert (by simp [hij]), Finset.sum_singleton]
        simp [typeAVec, hji]
      rw [hsum]
      cases s1 <;> cases s2 <;> decide
  · -- norm² = 4 + 4 = 8
    have hnorm : normSq (typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData)) = 8 := by
      have h1 : ∑ k, (typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData) k) ^ 2 = 8 := by
        have hsub : ∑ k, (typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData) k) ^ 2 =
            ∑ k ∈ ({i, j} : Finset (Fin 8)),
              (typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData) k) ^ 2 := by
          symm
          apply Finset.sum_subset (Finset.subset_univ _)
          intro k _ hk
          have hki : k ≠ i := by
            simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hk
            exact hk.1
          have hkj : k ≠ j := by
            simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hk
            exact hk.2
          simp [typeAVec, hki, hkj]
        rw [hsub]
        have hij : i ≠ j := ne_of_lt hp
        have hji : j ≠ i := hij.symm
        rw [Finset.sum_insert (by simp [hij]), Finset.sum_singleton]
        simp [typeAVec, hji]
      have h3 : normSq (typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData)) =
          ∑ k, (typeAVec (⟨⟨(i, j), hp⟩, s1, s2⟩ : TypeAData) k) ^ 2 := by
        simp [normSq, dot, pow_two]
      rw [h3]
      exact h1
    exact hnorm

/-- Every Type B vector (with even `-1` count) is a root. -/
theorem typeBVec_isRoot {ε : Fin 8 → Bool}
    (hε : Even (Finset.univ.filter (fun i => ε i = false)).card) :
    IsE8Root (typeBVec ε) := by
  constructor
  · constructor
    · right
      intro i
      simp [typeBVec]
      by_cases h : ε i <;> simp [h]
    · -- sum = 8 - 2·#false, divisible by 4 since #false is even
      have hsum : ∑ i, typeBVec ε i =
          8 - 2 * ((Finset.univ.filter (fun i => ε i = false)).card : ℤ) := by
        have h1 : ∀ i : Fin 8, typeBVec ε i =
            1 - 2 * (if ε i = false then (1 : ℤ) else 0) := by
          intro i
          simp [typeBVec]
          by_cases h : ε i <;> simp [h]
        rw [Finset.sum_congr rfl (fun i _ => h1 i)]
        rw [Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_boole]
        simp
      rw [hsum]
      obtain ⟨m, hm⟩ := hε
      use 2 - m
      omega
  · -- norm² = 8 (eight ±1s)
    have hnorm : normSq (typeBVec ε) = 8 := by
      have h1 : ∀ i : Fin 8, (typeBVec ε i) ^ 2 = 1 := by
        intro i
        simp [typeBVec]
      have h3 : normSq (typeBVec ε) = ∑ i, (typeBVec ε i) ^ 2 := by
        simp [normSq, dot, pow_two]
      rw [h3, Finset.sum_congr rfl (fun i _ => h1 i)]
      simp
    exact hnorm

/-- A Type A vector is nonzero exactly at its two positions. -/
theorem typeAVec_ne_zero_iff (d : TypeAData) (k : Fin 8) :
    typeAVec d k ≠ 0 ↔ k = d.1.1.1 ∨ k = d.1.1.2 := by
  obtain ⟨⟨⟨i, j⟩, hij⟩, s1, s2⟩ := d
  simp only [typeAVec]
  by_cases h1 : k = i <;> by_cases h2 : k = j
  · subst h1
    subst h2
    exact absurd (ne_of_lt hij) (by simp)
  · simp [h1]
    cases s1 <;> norm_num
  · subst h2
    simp [h1]
    cases s2 <;> norm_num
  · simp [h1, h2]

/-- `typeAVec` is injective: the two positions and their signs are
    recoverable from the vector. -/
theorem typeAVec_injective : Function.Injective typeAVec := by
  intro d1 d2 h
  obtain ⟨⟨⟨i1, j1⟩, hlt1⟩, s11, s12⟩ := d1
  obtain ⟨⟨⟨i2, j2⟩, hlt2⟩, s21, s22⟩ := d2
  -- The nonzero positions agree.
  have hne : ∀ k : Fin 8,
      (k = i1 ∨ k = j1) ↔ (k = i2 ∨ k = j2) := by
    intro k
    have e1 := (typeAVec_ne_zero_iff (⟨⟨(i1, j1), hlt1⟩, s11, s12⟩ : TypeAData) k)
    have e2 := (typeAVec_ne_zero_iff (⟨⟨(i2, j2), hlt2⟩, s21, s22⟩ : TypeAData) k)
    rw [← e1, ← e2]
    rw [h]
  have hi1 : i1 = i2 ∨ i1 = j2 := (hne i1).mp (Or.inl rfl)
  have hj1 : j1 = i2 ∨ j1 = j2 := (hne j1).mp (Or.inr rfl)
  have hi2 : i2 = i1 ∨ i2 = j1 := (hne i2).mpr (Or.inl rfl)
  have hj2 : j2 = i1 ∨ j2 = j1 := (hne j2).mpr (Or.inr rfl)
  have hlt1' : i1 < j1 := hlt1
  have hlt2' : i2 < j2 := hlt2
  have eij : i1 = i2 ∧ j1 = j2 := by
    rcases hi1 with h | h <;> rcases hj1 with h' | h' <;>
      rcases hi2 with h'' | h'' <;> omega
  obtain ⟨ei, ej⟩ := eij
  subst ei
  subst ej
  -- The signs agree.
  have hs1 : s11 = s21 := by
    have h1 := congrFun h i1
    simp [typeAVec, hlt1.ne] at h1
    cases s11 <;> cases s21 <;> simp_all
  have hs2 : s12 = s22 := by
    have h2 := congrFun h j1
    simp [typeAVec, hlt1.ne, (ne_of_lt hlt1).symm] at h2
    cases s12 <;> cases s22 <;> simp_all
  subst hs1
  subst hs2
  rfl

/-- `typeBVec` is injective on sign patterns. -/
theorem typeBVec_injective :
    Function.Injective (fun e : TypeBData => typeBVec e.1) := by
  intro e1 e2 h
  apply Subtype.ext
  funext i
  have hi := congrFun h i
  simp [typeBVec] at hi
  by_cases h1 : e1.1 i <;> by_cases h2 : e2.1 i <;> simp_all

/-- The finset of all Type A root vectors. -/
def typeAFinset : Finset Vec := Finset.univ.image typeAVec

/-- The finset of all Type B root vectors. -/
def typeBFinset : Finset Vec :=
  Finset.univ.image (fun e : TypeBData => typeBVec e.1)

/-- The finset of all E8 roots. -/
def rootFinset : Finset Vec := typeAFinset ∪ typeBFinset

theorem typeAFinset_card : typeAFinset.card = 112 := by
  rw [typeAFinset, Finset.card_image_of_injective _ typeAVec_injective,
    Finset.card_univ, card_typeAData]

theorem typeBFinset_card : typeBFinset.card = 128 := by
  rw [typeBFinset, Finset.card_image_of_injective _ typeBVec_injective,
    Finset.card_univ, card_typeBData]

/-- Type A and Type B vectors are disjoint: a Type A vector has a zero
    coordinate (any position outside its pair), a Type B vector has none. -/
theorem typeA_typeB_disjoint : Disjoint typeAFinset typeBFinset := by
  rw [Finset.disjoint_left]
  intro y hyA hyB
  rw [typeAFinset, Finset.mem_image] at hyA
  rw [typeBFinset, Finset.mem_image] at hyB
  obtain ⟨d1, _, rfl⟩ := hyA
  obtain ⟨⟨ε, hε⟩, _, hyeq⟩ := hyB
  -- d1's vector has a zero coordinate; ε's vector has none.
  obtain ⟨⟨⟨i, j⟩, hij⟩, s1, s2⟩ := d1
  -- pick k ∉ {i, j}: exists since 8 > 2
  have hex : ∃ k : Fin 8, k ≠ i ∧ k ≠ j := by
    by_contra hcon
    push_neg at hcon
    -- every k equals i or j: the type has ≤ 2 elements, contradiction
    have : Fintype.card (Fin 8) ≤ 2 := by
      have hsurj : Function.Surjective (fun b : Bool => if b then i else j) := by
        intro k
        by_cases hki : k = i
        · exact ⟨true, by simp [hki]⟩
        · exact ⟨false, by simp [hcon k hki]⟩
      exact Fintype.card_le_of_surjective _ hsurj
    simp at this
  obtain ⟨k, hki, hkj⟩ := hex
  have hz : typeAVec (⟨⟨(i, j), hij⟩, s1, s2⟩ : TypeAData) k = 0 := by
    simp [typeAVec, hki, hkj]
  have hne : typeBVec ε k ≠ 0 := by
    simp [typeBVec]
    by_cases h : ε k <;> simp [h]
  rw [← hyeq] at hz
  exact hne hz

theorem rootFinset_card : rootFinset.card = 240 := by
  rw [rootFinset, Finset.card_union_of_disjoint typeA_typeB_disjoint,
    typeAFinset_card, typeBFinset_card]

/-- Every Type A root is a Type A vector. -/
theorem typeA_mem {y : Vec} (h : IsTypeA y) : y ∈ typeAFinset := by
  obtain ⟨i, j, hij, hi, hj, h0⟩ := h
  rcases lt_trichotomy i j with hlt | heq | hgt
  · refine Finset.mem_image.mpr ⟨⟨⟨(i, j), hlt⟩, decide (y i = 2), decide (y j = 2)⟩,
      Finset.mem_univ _, ?_⟩
    funext k
    simp only [typeAVec]
    by_cases h1 : k = i
    · subst h1
      rcases hi with hi | hi <;> simp [hi]
    · by_cases h2 : k = j
      · subst h2
        rcases hj with hj | hj <;> simp [hj, h1]
      · simp [h1, h2]
        exact (h0 k h1 h2).symm
  · exact absurd heq hij
  · refine Finset.mem_image.mpr ⟨⟨⟨(j, i), hgt⟩, decide (y j = 2), decide (y i = 2)⟩,
      Finset.mem_univ _, ?_⟩
    funext k
    simp only [typeAVec]
    by_cases h1 : k = j
    · subst h1
      rcases hj with hj | hj <;> simp [hj]
    · by_cases h2 : k = i
      · subst h2
        rcases hi with hi | hi <;> simp [hi, h1]
      · simp [h1, h2]
        exact (h0 k h2 h1).symm

/-- Every Type B root is a Type B vector. -/
theorem typeB_mem {y : Vec} (h : IsTypeB y) : y ∈ typeBFinset := by
  obtain ⟨hall, heven⟩ := h
  -- sign pattern: ε i = (y i = 1)
  set ε : Fin 8 → Bool := fun i => decide (y i = 1) with hε
  have hpar : Even (Finset.univ.filter (fun i => ε i = false)).card := by
    have hset : Finset.univ.filter (fun i => ε i = false) =
        Finset.univ.filter (fun i => y i = -1) := by
      apply Finset.filter_congr
      intro i _
      simp [hε]
      rcases hall i with hi | hi <;> simp [hi]
    rw [hset]
    exact heven
  refine Finset.mem_image.mpr ⟨⟨ε, hpar⟩, Finset.mem_univ _, ?_⟩
  funext i
  simp [typeBVec, hε]
  rcases hall i with hi | hi <;> simp [hi]

/-- The root finset is exactly the set of roots. -/
theorem mem_rootFinset_iff {y : Vec} : y ∈ rootFinset ↔ IsE8Root y := by
  constructor
  · intro h
    simp [rootFinset] at h
    rcases h with h | h
    · rw [typeAFinset, Finset.mem_image] at h
      obtain ⟨d, _, rfl⟩ := h
      exact typeAVec_isRoot d
    · rw [typeBFinset, Finset.mem_image] at h
      obtain ⟨⟨ε, hε⟩, _, rfl⟩ := h
      exact typeBVec_isRoot hε
  · intro h
    simp [rootFinset]
    rcases root_classification h with hA | hB
    · exact Or.inl (typeA_mem hA)
    · exact Or.inr (typeB_mem hB)

/-- The subtype of roots is a fintype, via the root finset. -/
instance : Fintype {y : Vec // IsE8Root y} :=
  Fintype.ofFinset rootFinset (fun y => mem_rootFinset_iff)

/-- **The count: there are exactly 240 E8 roots.** -/
theorem e8_root_count : Fintype.card {y : Vec // IsE8Root y} = 240 := by
  have h := Fintype.card_ofFinset rootFinset (fun y => mem_rootFinset_iff)
  rw [rootFinset_card] at h
  exact h

-- =========================================================================
-- 6. Simple roots and the Cartan matrix
-- =========================================================================

/-- The eight simple roots of E8 (doubled coordinates).
    The chain α₁–α₇ uses `(2,-2)` steps, except α₇ = `(0,…,0,2,2)`;
    the branch root α₈ attaches at α₅. -/
def simpleRoot : Fin 8 → Vec
  | 0 => ![2, -2, 0, 0, 0, 0, 0, 0]
  | 1 => ![0, 2, -2, 0, 0, 0, 0, 0]
  | 2 => ![0, 0, 2, -2, 0, 0, 0, 0]
  | 3 => ![0, 0, 0, 2, -2, 0, 0, 0]
  | 4 => ![0, 0, 0, 0, 2, -2, 0, 0]
  | 5 => ![0, 0, 0, 0, 0, 2, -2, 0]
  | 6 => ![0, 0, 0, 0, 0, 0, 2, 2]
  | 7 => ![-1, -1, -1, -1, -1, 1, 1, -1]

/-- Each simple root is a root. -/
theorem simpleRoot_isRoot (i : Fin 8) : IsE8Root (simpleRoot i) := by
  fin_cases i <;> refine ⟨⟨?_, ?_⟩, ?_⟩ <;> decide

/-- The E8 Cartan matrix. -/
def cartanE8 : Matrix (Fin 8) (Fin 8) ℤ :=
  !![2, -1, 0, 0, 0, 0, 0, 0;
     -1, 2, -1, 0, 0, 0, 0, 0;
     0, -1, 2, -1, 0, 0, 0, 0;
     0, 0, -1, 2, -1, 0, 0, 0;
     0, 0, 0, -1, 2, -1, 0, -1;
     0, 0, 0, 0, -1, 2, -1, 0;
     0, 0, 0, 0, 0, -1, 2, 0;
     0, 0, 0, 0, -1, 0, 0, 2]

/-- The Gram matrix of the simple roots is `4 ×` the Cartan matrix
    (the factor 4 is the doubling). -/
theorem gram_eq_four_cartan (i j : Fin 8) :
    dot (simpleRoot i) (simpleRoot j) = 4 * cartanE8 i j := by
  fin_cases i <;> fin_cases j <;> decide

/-- The Dynkin diagram is E8: the chain 1–2–3–4–5–6–7 with the branch at 5.
    (Adjacency = Gram entry `-4` off the diagonal.) -/
theorem dynkin_adjacency (i j : Fin 8) (hij : i ≠ j) :
    dot (simpleRoot i) (simpleRoot j) = -4 ↔
      (i = 0 ∧ j = 1) ∨ (i = 1 ∧ j = 0) ∨
      (i = 1 ∧ j = 2) ∨ (i = 2 ∧ j = 1) ∨
      (i = 2 ∧ j = 3) ∨ (i = 3 ∧ j = 2) ∨
      (i = 3 ∧ j = 4) ∨ (i = 4 ∧ j = 3) ∨
      (i = 4 ∧ j = 5) ∨ (i = 5 ∧ j = 4) ∨
      (i = 4 ∧ j = 7) ∨ (i = 7 ∧ j = 4) ∨
      (i = 5 ∧ j = 6) ∨ (i = 6 ∧ j = 5) := by
  fin_cases i <;> fin_cases j <;> simp_all <;> decide

-- =========================================================================
-- 7. Axiom audit
-- =========================================================================

-- The headline theorems depend only on the standard Lean axioms.
#print axioms e8_root_count
#print axioms root_classification
#print axioms root_reflect
#print axioms gram_eq_four_cartan

end ResNova.E8Roots
