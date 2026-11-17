(*
  Independent finite-data spot-check for StringTheoryBridge.lean.
  This checks the Cartan matrix under the explicit node permutation and the
  480 + 16 = 496 bookkeeping. It does not formalize the E8 Lie algebra,
  root-space decomposition, or any physical claim.

  The Mathlib E8 Cartan entries correspond to the pinned source:
  https://github.com/leanprover-community/mathlib4/blob/5eec30bc56ed5a23be2e27c544a949ba0bceddeb/Mathlib/LinearAlgebra/Matrix/Cartan.lean
*)
From Coq Require Import List Lia ZArith.
Import ListNotations.
Open Scope Z_scope.

Definition resnova_cartan : list (list Z) :=
  [[2; -1; 0; 0; 0; 0; 0; 0];
   [-1; 2; -1; 0; 0; 0; 0; 0];
   [0; -1; 2; -1; 0; 0; 0; 0];
   [0; 0; -1; 2; -1; 0; 0; 0];
   [0; 0; 0; -1; 2; -1; 0; -1];
   [0; 0; 0; 0; -1; 2; -1; 0];
   [0; 0; 0; 0; 0; -1; 2; 0];
   [0; 0; 0; 0; -1; 0; 0; 2]].

Definition mathlib_e8_cartan : list (list Z) :=
  [[2; 0; -1; 0; 0; 0; 0; 0];
   [0; 2; 0; -1; 0; 0; 0; 0];
   [-1; 0; 2; -1; 0; 0; 0; 0];
   [0; -1; -1; 2; -1; 0; 0; 0];
   [0; 0; 0; -1; 2; -1; 0; 0];
   [0; 0; 0; 0; -1; 2; -1; 0];
   [0; 0; 0; 0; 0; -1; 2; -1];
   [0; 0; 0; 0; 0; 0; -1; 2]].

Definition resnova_to_mathlib : list nat :=
  [7%nat; 6%nat; 5%nat; 4%nat; 3%nat; 2%nat; 0%nat; 1%nat].
Definition indices : list nat :=
  [0%nat; 1%nat; 2%nat; 3%nat; 4%nat; 5%nat; 6%nat; 7%nat].

Definition matrix_entry (m : list (list Z)) (i j : nat) : Z :=
  nth j (nth i m ([] : list Z)) 0%Z.

Definition reindexed_mathlib_cartan : list (list Z) :=
  map
    (fun i =>
      map
        (fun j => matrix_entry mathlib_e8_cartan
          (nth i resnova_to_mathlib 0%nat) (nth j resnova_to_mathlib 0%nat))
        indices)
    indices.

Theorem resnova_to_mathlib_length : length resnova_to_mathlib = 8%nat.
Proof. reflexivity. Qed.

Theorem resnova_to_mathlib_nodup : NoDup resnova_to_mathlib.
Proof.
  repeat (apply NoDup_cons; [simpl; intuition congruence |]).
  apply NoDup_nil.
Qed.

Theorem resnova_to_mathlib_in_range :
  Forall (fun i => Nat.lt i 8%nat) resnova_to_mathlib.
Proof. repeat constructor; simpl; lia. Qed.

Theorem cartan_reindex_matches : reindexed_mathlib_cartan = resnova_cartan.
Proof. vm_compute; reflexivity. Qed.

Theorem root_plus_rank_bookkeeping : (480 + 16 = 496)%nat.
Proof. reflexivity. Qed.
