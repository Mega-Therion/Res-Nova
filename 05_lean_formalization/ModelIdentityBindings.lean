/-
  ModelIdentityBindings.lean — the Wave/AeST theorems restated on `ModelIdentity.canonical`

  Each theorem below reads a physics literal from the canonical model-identity record
  instead of writing it into the statement: the generation count, the μ function, the
  matter coupling, the aether norm, the spacetime dimension and a₀. Each proof goes
  through the record, so `scripts/sabotage_model_identity.sh` can mutate one field in a
  throwaway copy and require this file to stop compiling.

  Theorems whose proof does NOT depend on a field are marked "field-insensitive" in their
  docstring (for example, the diffeomorphism Noether identity holds in every dimension).
  That is a finding about the theorem, not a gap in the binding.

  Source theorems (unchanged in their own modules):
  * `Wave3BBNAndSpinCCP2Bounds`: `matter_27_three_gen_forces_Q0_and_kpsi`,
    `no_zero_sum_twist_below_nine`, `jtot_bbn_5pct_impossible`;
  * `AeSTParameterizedNormalization`: `deriv_Jparam`, `Jparam_deriv_pos`;
  * `AeSTDiffeomorphismNoether`: `diffeo_invariance_implies_noether_identity`;
  * `AeSTHamiltonianLegendre`: `d2U_dmu2_neg`;
  * `HorizonScale`: `freeman_surface_density_pos`.
-/
import ModelIdentity
import Wave3BBNAndSpinCCP2Bounds
import AeSTParameterizedNormalization
import AeSTDiffeomorphismNoether
import AeSTHamiltonianLegendre
import HorizonScale

namespace ResNova.ModelIdentityBindings

open ResNova.ModelIdentity
open ResNova.Wave3BBNAndSpinCCP2Bounds

/-! ## 1. Generation count (`generationTarget`) -/

/-- **Canonical 3-generation charge lock.** Net chiral `16` count `± generationTarget`
(in `twiceInd` units, `± 2 · generationTarget`) from `(27,3)` under a traceless `SU(3)_f`
twist forces `Q₀ ∈ {-1,-2}` and `k_ψ = ±1`. Sensitive to `generationTarget`. -/
theorem canonical_generation_charge_lock {Q0 k_psi q1 q2 q3 : ℤ}
    (hsum : q1 + q2 + q3 = 0)
    (hnet :
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) =
        2 * generationTargetZ canonical ∨
      (twiceInd (Q0 + (k_psi + q1)) - twiceInd (Q0 - (k_psi + q1))) +
      (twiceInd (Q0 + (k_psi + q2)) - twiceInd (Q0 - (k_psi + q2))) +
      (twiceInd (Q0 + (k_psi + q3)) - twiceInd (Q0 - (k_psi + q3))) =
        -(2 * generationTargetZ canonical)) :
    (Q0 = -1 ∨ Q0 = -2) ∧ (k_psi = 1 ∨ k_psi = -1) := by
  rw [canonical_generationTargetZ] at hnet
  norm_num at hnet
  exact matter_27_three_gen_forces_Q0_and_kpsi hsum hnet

/-- **No zero-sum twist of the trivial bundle reproduces the generation target.**
For traceless `SU(3)_f` twists, `∑ twiceInd(1 + qᵢ) ≥ 18 > 2 · generationTarget`.
Sensitive to `generationTarget` (fails for a target of 9 or more). -/
theorem canonical_zero_sum_twist_overshoots {q1 q2 q3 : ℤ} (hsum : q1 + q2 + q3 = 0) :
    twiceInd (1 + q1) + twiceInd (1 + q2) + twiceInd (1 + q3) ≠
      2 * generationTargetZ canonical := by
  rw [canonical_generationTargetZ]
  have h := no_zero_sum_twist_below_nine hsum
  omega

/-! ## 2. Interpolating function (`interpolation`) -/

open SZStdEmbedding in
/-- **The parameterized AeST scalar function differentiates to the canonical μ.**
`J'(Y) = λ_s · μ(√Y / a)` with `μ` read from the record. Sensitive to `interpolation`. -/
theorem canonical_Jparam_derivative {Y lam a : ℝ} (hY : 0 < Y) (ha : 0 < a) :
    deriv (ResNova.AeSTParameterizedNormalization.Jparam lam a) Y =
      lam * mu canonical (Real.sqrt Y / a) := by
  rw [canonical_mu]
  exact ResNova.AeSTParameterizedNormalization.deriv_Jparam hY ha

/-- **First ghost condition on the canonical μ.** For `λ_s > 0`, `λ_s · μ(√Y/a) > 0` on
`Y > 0`. Sensitive to `interpolation`. -/
theorem canonical_Jparam_derivative_pos {Y lam a : ℝ}
    (hY : 0 < Y) (hlam : 0 < lam) (ha : 0 < a) :
    0 < lam * mu canonical (Real.sqrt Y / a) := by
  rw [canonical_mu]
  exact ResNova.AeSTParameterizedNormalization.Jparam_deriv_pos hY hlam ha

/-- The canonical μ saturates below 1 on the condensate range, which is what makes
`μ_max = (2 - K_B) λ_s` the live upper edge used by `AeSTHamiltonianLegendre`:
`μ(x) < 1` for all `x`. Sensitive to `interpolation` through `canonical_mu`. -/
theorem canonical_mu_lt_one (x : ℝ) : mu canonical x < 1 := by
  rw [canonical_mu]
  unfold SZStdEmbedding.muStd
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.mpr (by positivity)
  rw [div_lt_one hs]
  have hlt : x ^ 2 < 1 + x ^ 2 := by linarith
  calc x ≤ |x| := le_abs_self x
    _ = Real.sqrt (x ^ 2) := (Real.sqrt_sq_eq_abs x).symm
    _ < Real.sqrt (1 + x ^ 2) := Real.sqrt_lt_sqrt (sq_nonneg x) hlt

/-- **Strict concavity of `U_μ` on the live range, at the canonical a₀ scale.**
`∂²U_μ/∂μ² < 0` on `0 < μ < μ_max` for the record's `ã₀ = a₀ > 0`. Sensitive to `a0`
(needs a positive measured value). -/
theorem canonical_d2U_dmu2_neg {muMax m : ℝ}
    (hmMax : 0 < muMax) (hm0 : 0 < m) (hmLt : m < muMax) :
    ResNova.AeSTHamiltonianLegendre.d2U_dmu2_expr (a0SI canonical) muMax m < 0 := by
  have ha : 0 < a0SI canonical := by
    rw [canonical_a0SI]; positivity
  exact ResNova.AeSTHamiltonianLegendre.d2U_dmu2_neg ha hmMax hm0 hmLt

/-! ## 3. Matter coupling (`matterCoupling`) -/

/-- The `G_cosmo / G_N` ratio of `Wave3BBNAndSpinCCP2Bounds.GCosmoRatio` is the pure-AeST
ratio, valid only when matter couples minimally to `g_μν` (`TARGET_D7` §1). This is the
applicability gate. -/
def bbnRatioApplies (M : ModelIdentity) : Prop := M.matterCoupling = MatterCoupling.minimal

theorem canonical_bbnRatioApplies : bbnRatioApplies canonical := rfl

/-- **5% BBN no-go, conditional on the record.** Under the canonical (minimal) coupling,
no `λ_s > 0` with `K_B ≥ 0` satisfies both the 5% BBN bound and the `J_tot` non-folding
threshold. Sensitive to `matterCoupling` through `canonical_bbnRatioApplies`. -/
theorem canonical_bbn_5pct_no_go {lam KB : ℝ}
    (_happ : bbnRatioApplies canonical)
    (hlam : 0 < lam) (hKB : 0 ≤ KB)
    (hBBN : 19 / 20 ≤ GCosmoRatio lam KB)
    (hJ : 32 * (lam / (1 + lam)) ^ 2 < 27) : False :=
  jtot_bbn_5pct_impossible hlam hKB hBBN hJ

/-- The no-go discharged on the canonical record. -/
theorem canonical_bbn_5pct_no_go_closed {lam KB : ℝ}
    (hlam : 0 < lam) (hKB : 0 ≤ KB)
    (hBBN : 19 / 20 ≤ GCosmoRatio lam KB)
    (hJ : 32 * (lam / (1 + lam)) ^ 2 < 27) : False :=
  canonical_bbn_5pct_no_go canonical_bbnRatioApplies hlam hKB hBBN hJ

/-! ## 4. Aether norm (`aetherNorm`) -/

/-- **The projector `q_μν = g_μν + A_μ A_ν` annihilates `A`.** Contracting with `A^ν`
gives `A_μ + A_μ (A^ν A_ν) = A_μ (1 + aetherNorm)`, which vanishes because the record
fixes `A^ν A_ν = -1`. Sensitive to `aetherNorm`. -/
theorem canonical_projector_annihilates_aether (A_mu : ℝ) :
    A_mu + A_mu * (canonical.aetherNorm : ℝ) = 0 := by
  have h : (canonical.aetherNorm : ℝ) = -1 := by
    have : canonical.aetherNorm = -1 := by decide
    exact_mod_cast this
  rw [h]; ring

/-! ## 5. Spacetime dimension (`spacetimeDim`) -/

/-- **Diffeomorphism Noether identity in the canonical dimension.** Field-insensitive: the
identity holds for every `n`, so changing `spacetimeDim` does not break it. Recorded so the
dependence is visible. -/
theorem canonical_diffeo_noether_identity
    (N : Fin canonical.spacetimeDim → ℝ)
    (hinv : ∀ ξ : Fin canonical.spacetimeDim → ℝ, ∑ ν, ξ ν * N ν = 0)
    (ν : Fin canonical.spacetimeDim) : N ν = 0 :=
  ResNova.AeSTDiffeomorphismNoether.diffeo_invariance_implies_noether_identity N hinv ν

/-- The canonical dimension has exactly one timelike and three spacelike directions.
Sensitive to `spacetimeDim` and `signature`. -/
theorem canonical_dim_is_one_plus_three :
    canonical.spacetimeDim = 4 ∧ canonical.signature = (1, 3) := by decide

/-! ## 6. a₀ (`a0`) -/

/-- **Freeman surface density at the canonical a₀ is positive** for any `G > 0`.
Sensitive to `a0` (needs a positive measured value). -/
theorem canonical_freeman_density_pos {G : ℝ} (hG : 0 < G) :
    0 < ResNova.HorizonScale.freeman_surface_density (a0SI canonical) G := by
  have ha : 0 < a0SI canonical := by rw [canonical_a0SI]; positivity
  exact ResNova.HorizonScale.freeman_surface_density_pos _ _ ha hG Real.pi_pos

/-- The canonical a₀ lies inside its own bootstrap 95% interval `[0.972, 1.295] × 10⁻¹⁰`
(`CURRENT_STATE`, a₀ headline). Sensitive to `a0`. -/
theorem canonical_a0_in_bootstrap_interval :
    (972 / 1000 : ℝ) * (10 : ℝ) ^ (-10 : ℤ) ≤ a0SI canonical ∧
      a0SI canonical ≤ (1295 / 1000 : ℝ) * (10 : ℝ) ^ (-10 : ℤ) := by
  rw [canonical_a0SI]
  have hp : (0 : ℝ) < (10 : ℝ) ^ (-10 : ℤ) := by positivity
  constructor <;> nlinarith

#print axioms canonical_generation_charge_lock
#print axioms canonical_zero_sum_twist_overshoots
#print axioms canonical_Jparam_derivative
#print axioms canonical_Jparam_derivative_pos
#print axioms canonical_mu_lt_one
#print axioms canonical_d2U_dmu2_neg
#print axioms canonical_bbnRatioApplies
#print axioms canonical_bbn_5pct_no_go
#print axioms canonical_bbn_5pct_no_go_closed
#print axioms canonical_projector_annihilates_aether
#print axioms canonical_diffeo_noether_identity
#print axioms canonical_dim_is_one_plus_three
#print axioms canonical_freeman_density_pos
#print axioms canonical_a0_in_bootstrap_interval

end ResNova.ModelIdentityBindings
