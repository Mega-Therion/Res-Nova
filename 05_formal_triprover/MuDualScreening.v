(* Screening split from MuStdSelection.lean, in Coq's standard reals.
   mu_dual is not inverse-square screened. mu_std's algebraic tail is 1/(S(S+x)). *)
From Coq Require Import Reals Lra.
Open Scope R_scope.

Definition mu_dual (x : R) : R := x / (1 + x).
Definition mu_std (x : R) : R := x / sqrt (1 + x * x).

Lemma one_sub_mu_dual : forall x : R, 0 < x -> 1 - mu_dual x = 1 / (1 + x).
Proof.
  intros x hx.
  unfold mu_dual.
  field.
  lra.
Qed.

Lemma one_sub_mu_std :
  forall x : R, 0 <= x ->
  1 - mu_std x = 1 / (sqrt (1 + x * x) * (sqrt (1 + x * x) + x)).
Proof.
  intros x hx.
  unfold mu_std.
  set (S := sqrt (1 + x * x)).
  assert (HS : 0 < S).
  { unfold S. apply sqrt_lt_R0. nra. }
  assert (Hsq : S * S = 1 + x * x).
  { unfold S. rewrite sqrt_sqrt by nra. reflexivity. }
  assert (Hsum : S + x <> 0) by lra.
  assert (HS0 : S <> 0) by lra.
  replace (1 - x / S) with ((S - x) / S) by (field; exact HS0).
  replace ((S - x) / S) with ((S - x) * (S + x) / (S * (S + x))).
  2: { field; nra. }
  replace ((S - x) * (S + x)) with (S * S - x * x) by ring.
  rewrite Hsq.
  replace (1 + x * x - x * x) with 1 by ring.
  reflexivity.
Qed.

(* No positive C bounds the dual tail by C/x^2 for every x >= 1.
   Witness: any x > max(1, 4C) gives x^2 > C(1+x). *)
Lemma mu_dual_not_screened :
  ~ (exists C : R, 0 < C /\ forall x : R, 1 <= x -> 1 - mu_dual x <= C / (x * x)).
Proof.
  intros [C [HC H]].
  (* Witness x = 4*C + 2. Then x > 1, x > 4*C, and C(1+x) < x^2. *)
  pose (x := 4 * C + 2).
  assert (Hx1 : 1 <= x) by (unfold x; lra).
  specialize (H x Hx1).
  rewrite one_sub_mu_dual in H by (unfold x; lra).
  assert (Hgt : C * (1 + x) < x * x) by (unfold x; nra).
  assert (Hden : 0 < (1 + x) * (x * x)) by (unfold x; nra).
  apply Rmult_le_compat_r with (r := (1 + x) * (x * x)) in H.
  2: { apply Rlt_le. exact Hden. }
  replace ((1 / (1 + x)) * ((1 + x) * (x * x))) with (x * x) in H.
  2: { unfold x. field. lra. }
  replace ((C / (x * x)) * ((1 + x) * (x * x))) with (C * (1 + x)) in H.
  2: { unfold x. field. lra. }
  lra.
Qed.

Lemma mu_std_tail_bounded :
  forall x : R, 1 <= x ->
  (x * x) * (1 - mu_std x) <= 1.
Proof.
  intros x hx.
  rewrite one_sub_mu_std by lra.
  set (S := sqrt (1 + x * x)).
  assert (Hnn : 0 <= 1 + x * x).
  { assert (0 <= x * x) by apply Rle_0_sqr. lra. }
  assert (Hpos1 : 0 < 1 + x * x).
  { assert (0 <= x * x) by apply Rle_0_sqr. lra. }
  assert (Hsq : S * S = 1 + x * x).
  { unfold S. rewrite sqrt_sqrt by exact Hnn. reflexivity. }
  assert (HSpos : 0 < S).
  { unfold S. apply sqrt_lt_R0. exact Hpos1. }
  assert (Hx0 : 0 <= x) by lra.
  assert (Hsum : 0 < S + x).
  { apply Rplus_lt_le_0_compat; [exact HSpos | exact Hx0]. }
  assert (Hden : 0 < S * (S + x)).
  { apply Rmult_lt_0_compat; assumption. }
  apply Rmult_le_reg_r with (r := S * (S + x)).
  - exact Hden.
  - replace (x * x * (1 / (S * (S + x))) * (S * (S + x))) with (x * x) by (field; lra).
    replace (1 * (S * (S + x))) with (S * (S + x)) by ring.
    assert (Hgap : S * (S + x) - x * x = 1 + x * S).
    { replace (S * (S + x)) with (S * S + S * x) by ring.
      rewrite Hsq. ring. }
    assert (Hge : 0 <= 1 + x * S).
    { assert (0 <= x * S) by (apply Rmult_le_pos; [exact Hx0 | apply Rlt_le; exact HSpos]).
      lra. }
    replace (S * (S + x)) with (x * x + (1 + x * S)).
    2: { rewrite <- Hgap. ring. }
    assert (Hle : x * x + 0 <= x * x + (1 + x * S)).
    { apply Rplus_le_compat_l. exact Hge. }
    assert (Heq : x * x + 0 = x * x) by ring.
    rewrite Heq in Hle.
    exact Hle.
Qed.
