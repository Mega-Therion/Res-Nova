theory MuDualScreening
  imports Complex_Main
begin

text \<open>The screening split from \<open>MuStdSelection.lean\<close>.
\<open>mu_dual\<close> is not inverse-square screened. The algebraic tail of \<open>mu_std\<close>
is \<open>1/(S(S+x))\<close>, so \<open>x^2(1-mu_std x) \<le> 1\<close> for \<open>x \<ge> 1\<close>.\<close>

definition mu_dual :: "real \<Rightarrow> real" where
  "mu_dual x = x / (1 + x)"

definition mu_std :: "real \<Rightarrow> real" where
  "mu_std x = x / sqrt (1 + x^2)"

lemma one_sub_mu_dual:
  assumes "x \<noteq> -1"
  shows "1 - mu_dual x = 1 / (1 + x)"
  using assms unfolding mu_dual_def by (simp add: field_simps)

lemma one_sub_mu_std:
  assumes "0 \<le> x"
  shows "1 - mu_std x = 1 / (sqrt (1 + x^2) * (sqrt (1 + x^2) + x))"
proof -
  let ?S = "sqrt (1 + x^2)"
  have Ssq: "?S ^ 2 = 1 + x^2"
    by (simp add: real_sqrt_pow2)
  have Spos: "0 < ?S"
  proof -
    have "0 < 1 + x^2"
      using assms by (simp add: add_pos_nonneg)
    then show ?thesis
      by (simp add: real_sqrt_gt_0_iff)
  qed
  have Sneq: "?S \<noteq> 0"
    using Spos by simp
  have sumneq: "?S + x \<noteq> 0"
  proof
    assume "?S + x = 0"
    then have "?S = - x" by simp
    then have "?S ^ 2 = x ^ 2"
      by (simp add: power2_eq_iff)
    with Ssq have "1 + x^2 = x^2" by simp
    then show False by simp
  qed
  have "1 - mu_std x = 1 - x / ?S"
    by (simp add: mu_std_def)
  also have "... = (?S - x) / ?S"
    using Sneq by (simp add: diff_divide_eq_iff)
  also have "... = ((?S - x) * (?S + x)) / (?S * (?S + x))"
  proof -
    have "(?S + x) / (?S + x) = 1"
      using sumneq by simp
    then have "(?S - x) / ?S = (?S - x) / ?S * ((?S + x) / (?S + x))"
      by simp
    also have "... = ((?S - x) * (?S + x)) / (?S * (?S + x))"
      by (simp add: times_divide_times_eq)
    finally show ?thesis .
  qed
  also have "... = (?S ^ 2 - x ^ 2) / (?S * (?S + x))"
    by (simp add: power2_eq_square algebra_simps)
  also have "... = (1 + x^2 - x^2) / (?S * (?S + x))"
    by (simp add: Ssq)
  also have "... = 1 / (?S * (?S + x))"
    by simp
  finally show ?thesis .
qed

lemma mu_std_tail_bounded:
  assumes "1 \<le> x"
  shows "x^2 * (1 - mu_std x) \<le> 1"
proof -
  let ?S = "sqrt (1 + x^2)"
  have hx: "0 \<le> x"
    using assms by simp
  have Sle: "x \<le> ?S"
  proof -
    have "(abs x) ^ 2 \<le> ?S ^ 2"
      by (simp add: real_sqrt_pow2)
    then have "abs x \<le> ?S"
      by (rule power2_le_imp_le) (simp add: real_sqrt_ge_zero)
    then show ?thesis
      using hx by (simp add: abs_of_nonneg)
  qed
  have denpos: "0 < ?S * (?S + x)"
  proof -
    have Spos: "0 < ?S"
    proof -
      have "0 < 1 + x^2"
        using hx by (simp add: add_pos_nonneg)
      then show ?thesis by (simp add: real_sqrt_gt_0_iff)
    qed
    have "0 < ?S + x"
      using Spos hx by (simp add: add_pos_nonneg)
    with Spos show ?thesis by (simp add: mult_pos_pos)
  qed
  have id: "1 - mu_std x = 1 / (?S * (?S + x))"
    using one_sub_mu_std hx by simp
  have "x^2 * (1 - mu_std x) = x^2 / (?S * (?S + x))"
    using id by simp
  also have "... \<le> 1"
  proof -
    have "x^2 \<le> ?S * (?S + x)"
    proof -
      have Ssq: "?S * ?S = 1 + x^2"
        by (simp add: power2_eq_square real_sqrt_pow2)
      have "?S * (?S + x) = ?S * ?S + ?S * x"
        by (simp add: algebra_simps)
      also have "... = 1 + x^2 + x * ?S"
        using Ssq by (simp add: algebra_simps)
      finally have gap: "?S * (?S + x) - x^2 = 1 + x * ?S"
        by (simp add: algebra_simps)
      have "0 \<le> x * ?S"
        using hx by (simp add: mult_nonneg_nonneg real_sqrt_ge_zero)
      then have "0 < 1 + x * ?S"
        by (simp add: add_pos_nonneg)
      with gap have "0 < ?S * (?S + x) - x^2"
        by simp
      then show ?thesis by simp
    qed
    then show ?thesis
      using denpos by (simp add: pos_divide_le_eq)
  qed
  finally show ?thesis .
qed

lemma mu_dual_not_screened:
  "\<not> (\<exists>C>0. \<forall>x::real. 1 \<le> x \<longrightarrow> 1 - mu_dual x \<le> C / x^2)"
proof
  assume "\<exists>C>0. \<forall>x::real. 1 \<le> x \<longrightarrow> 1 - mu_dual x \<le> C / x^2"
  then obtain C where C: "C > 0" and H: "\<forall>x. 1 \<le> x \<longrightarrow> 1 - mu_dual x \<le> C / x^2"
    by blast
  define x where "x = 4 * C + 2"
  have x1: "1 \<le> x" unfolding x_def using C by simp
  have "1 - mu_dual x = 1 / (1 + x)"
    using one_sub_mu_dual unfolding x_def using C by simp
  have le: "1 / (1 + x) \<le> C / x^2"
  proof -
    have "1 - mu_dual x \<le> C / x^2"
      using H x1 by simp
    then show ?thesis
      using \<open>1 - mu_dual x = 1 / (1 + x)\<close> by simp
  qed
  have "x > 4 * C" unfolding x_def using C by simp
  have "x > 1" unfolding x_def using C by simp
  have "C * (1 + x) < x^2"
  proof -
    have "1 + x < 2 * x" using \<open>x > 1\<close> by simp
    have "C * (1 + x) < C * (2 * x)"
      using C \<open>1 + x < 2 * x\<close> by (simp add: mult_strict_left_mono)
    also have "... = (2 * C) * x" by simp
    also have "... < (x / 2) * x"
      using \<open>x > 4 * C\<close> C by (simp add: mult_strict_right_mono)
    also have "... = x^2 / 2" by (simp add: power2_eq_square)
    also have "... < x^2" using \<open>x > 1\<close> by simp
    finally show ?thesis .
  qed
  have "0 < x" using \<open>x > 1\<close> by simp
  have "x^2 / (1 + x) \<le> C"
  proof -
    have nonneg: "0 \<le> x^2"
      using \<open>0 < x\<close> by simp
    have "x^2 * (1 / (1 + x)) \<le> x^2 * (C / x^2)"
      by (rule mult_left_mono[OF le nonneg])
    moreover have "x^2 * (1 / (1 + x)) = x^2 / (1 + x)"
      by simp
    moreover have "x^2 * (C / x^2) = C"
    proof -
      have "x^2 \<noteq> 0"
        using \<open>0 < x\<close> by simp
      then show ?thesis
        by (simp add: power2_eq_square)
    qed
    ultimately show ?thesis by simp
  qed
  then have "x^2 \<le> C * (1 + x)"
    using \<open>x > 1\<close> by (simp add: pos_divide_le_eq)
  with \<open>C * (1 + x) < x^2\<close> show False by simp
qed

end
