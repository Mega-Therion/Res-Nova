(*
  Independent finite-data spot-check for StringTheoryBridge.lean.
  This checks the explicit Cartan-node permutation and 480 + 16 = 496 only.
  It does not formalize the E8 Lie algebra, its root-space decomposition,
  or a physical connection.
*)
theory E8CartanBridge
  imports Main
begin

definition resnova_cartan :: "int list list" where
  "resnova_cartan =
    [[2, -1, 0, 0, 0, 0, 0, 0],
     [-1, 2, -1, 0, 0, 0, 0, 0],
     [0, -1, 2, -1, 0, 0, 0, 0],
     [0, 0, -1, 2, -1, 0, 0, 0],
     [0, 0, 0, -1, 2, -1, 0, -1],
     [0, 0, 0, 0, -1, 2, -1, 0],
     [0, 0, 0, 0, 0, -1, 2, 0],
     [0, 0, 0, 0, -1, 0, 0, 2]]"

definition mathlib_e8_cartan :: "int list list" where
  "mathlib_e8_cartan =
    [[2, 0, -1, 0, 0, 0, 0, 0],
     [0, 2, 0, -1, 0, 0, 0, 0],
     [-1, 0, 2, -1, 0, 0, 0, 0],
     [0, -1, -1, 2, -1, 0, 0, 0],
     [0, 0, 0, -1, 2, -1, 0, 0],
     [0, 0, 0, 0, -1, 2, -1, 0],
     [0, 0, 0, 0, 0, -1, 2, -1],
     [0, 0, 0, 0, 0, 0, -1, 2]]"

definition resnova_to_mathlib :: "nat list" where
  "resnova_to_mathlib = [7, 6, 5, 4, 3, 2, 0, 1]"

definition indices :: "nat list" where
  "indices = [0, 1, 2, 3, 4, 5, 6, 7]"

definition matrix_entry :: "int list list \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> int" where
  "matrix_entry m i j = m ! i ! j"

definition reindexed_mathlib_cartan :: "int list list" where
  "reindexed_mathlib_cartan =
    map (\<lambda>i. map (\<lambda>j. matrix_entry mathlib_e8_cartan
      (resnova_to_mathlib ! i) (resnova_to_mathlib ! j)) indices) indices"

lemma reindex_length: "length resnova_to_mathlib = 8"
  by eval

lemma reindex_distinct: "distinct resnova_to_mathlib"
  by eval

lemma reindex_covers_fin8: "set resnova_to_mathlib = {0..<8}"
  by eval

lemma cartan_reindex_matches:
  "reindexed_mathlib_cartan = resnova_cartan"
  by eval

lemma root_plus_rank_bookkeeping: "480 + 16 = (496::nat)"
  by simp

end
