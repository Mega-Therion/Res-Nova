import AeSTVectorNoetherResidual
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.Calculus.FDeriv.Add
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.Comp
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Positivity

/-!
# General Diffeomorphism Noether Identity & Curved-Space Matter Conservation (`Res-Nova #217`, `BLK-1443`)

Addresses obligations 3 and 4 of `Res-Nova` GitHub issue `#217` and closes the remaining Lean
generalization boundary recorded in Muse's `BLK-1443`:

1. **Arbitrary-Dimension (`n : ℕ`, `Fin n`) Tensorial Symmetrization & Vector-Sector Equivalence:**
   - `symmetric_contract_antisym` and `symmetric_contract_eq_symmetrized`: a symmetric
     metric Euler tensor `E^{μν} = E^{νμ}` pairs exclusively against the symmetric part of `∇_μ ξ_ν`,
     transforming `δg^{μν} = -2∇^{(μ}ξ^{ν)}` into `-2 E_g^{μν} ∇_μ ξ_ν` in any spacetime dimension `n`.
   - `vector_noether_sector_equiv`: exact `n`-dimensional Leibniz equivalence
     `∑ μ, E_A^μ ∇_ν A_μ - ∑ μ, ∇_μ(E_A^μ A_ν) = ∑ μ, E_A^μ F_{νμ} - A_ν ∑ μ, ∇_μ E_A^μ`.

2. **General `n`-Dimensional Off-Shell Diffeomorphism Noether Identity (`#217` Obligation 3):**
   With independent fields `(g^{μν}, A_μ, φ, λ)` and declared Euler derivatives `E_A^μ := (√-g)⁻¹ δS/δA_μ`,
   `off_shell_variation_decomposition` and `diffeo_invariance_implies_noether_identity` prove
   in arbitrary dimension `n`:
     `2 ∇^μ E_{g,μν} + ∑ μ, E_A^μ F_{νμ} - A_ν ∇_μ E_A^μ + E_φ ∇_ν φ + E_λ ∇_ν λ = 0`.
   `noether_sign_flip_counterexample` confirms sign/convention sensitivity (preventing silent
   sign drift on `E_A` vs `A_ν`).

3. **Matter Conservation as a Consequence of Matter Equations & Total Identity (`#217` Obligation 4):**
   - `matter_conservation_from_matter_eom`: from the matter diffeomorphism identity
     `-∇^μ T_{μν} + E_matter · ∇_ν ψ = 0`, `E_matter = 0` implies `∇^μ T_{μν} = 0`.
   - `matter_conservation_from_aest_total_noether`: under minimal coupling
     (`E_g^{tot} = E_g^{AeST} - ½ T`), combining total diffeomorphism invariance with the
     gravitational (`2 E_g^{AeST} = T`) and aether (`E_A = E_φ = E_λ = 0`) field equations implies
     `∇^μ T_{μν} = 0` without assuming matter conservation separately.
   - `nonminimal_coupling_obstruction`: explicitly shows nonminimal `(A, φ)` exchange sources violate
     `∇^μ T_{μν} = 0` by `-(E_A^μ F_{νμ} - A_ν ∇_μ E_A^μ + E_φ ∇_ν φ)`.

4. **Arbitrary-Dimension Levi-Civita / Metric-Divergence Identity (`verify_issue217_obligations` C1):**
   `metric_div_gamma_identity` proves for any invertible symmetric metric `g` in dimension `n` and any
   symmetric tensor `T`, `-(∂_μ g_{νλ}) T^{μλ} + g_{νλ} Γ^λ_{μα} T^{μα} + ½(∂_ν g_{μα}) T^{μα} = 0`.

5. **Smooth 1+1D Curved-Spacetime Differential Calculus (`Fin 2 → ℝ`, real `fderiv` & Clairaut symmetry):**
   For arbitrary smooth diagonal Lorentzian metrics `g = diag(-e^{2α(t,x)}, e^{2β(t,x)})` with
   `α, β ∈ C^1`, scalar field `χ ∈ C^2`, and potential `V ∈ C^1`:
   - `density_divergence_identity_2d`: proves `∂_μ(√-g V^μ) = √-g (∂_μ V^μ + Γ^μ_{μλ} V^λ)` by `HasFDerivAt`.
   - `scalar_matter_divergence_eq_euler_2d`: proves `∇^μ T_{μν} = E_χ ∂_ν χ` identically from real
     Fréchet partial derivatives and `ContDiffAt.isSymmSndFDerivAt` (Clairaut's theorem), whence
     `scalar_matter_on_shell_conserved_2d` derives `∇^μ T_{μν} = 0` when `E_χ = □χ - V'(χ) = 0`.

6. **Epistemic Boundary (see `lean4-formalizer` Rule 12):**
   Sections 1–4 verify the exact finite-dimensional algebraic, combinatorial, and IBP reductions
   given declared Euler derivatives and variation/IBP pairings (`[P]` given those structures); Section 5
   verifies the full differential-calculus identity by real Mathlib `fderiv` on `1+1D` curved diagonal
   charts; constructing an infinite-dimensional functional variational derivative `δS_AeST/δg^{μν}`
   from a 4D diffeomorphism-invariant integral functional remains external to the kernel.
   All theorems compile with `0 sorry` and standard axioms `[propext, Classical.choice, Quot.sound]` only.
-/

noncomputable section

namespace ResNova.AeSTDiffeomorphismNoether

open scoped BigOperators

/-! ## 1. Arbitrary-Dimension Metric Symmetrization & Vector-Sector Leibniz Equivalence -/

/-- A symmetric matrix `E` (`E μ ν = E ν μ`) annihilates any antisymmetric matrix `W`
(`W μ ν = -W ν μ`) under full double contraction in arbitrary dimension `n`. -/
theorem symmetric_contract_antisym {n : ℕ} (E W : Fin n → Fin n → ℝ)
    (hE : ∀ μ ν, E μ ν = E ν μ) (hW : ∀ μ ν, W μ ν = -W ν μ) :
    ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * W μ ν = 0 := by
  have hflip :
      ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * W μ ν =
        -(∑ μ : Fin n, ∑ ν : Fin n, E μ ν * W μ ν) := by
    calc
      ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * W μ ν
          = ∑ ν : Fin n, ∑ μ : Fin n, E μ ν * W μ ν := Finset.sum_comm
      _ = ∑ ν : Fin n, ∑ μ : Fin n, -(E ν μ * W ν μ) := by
          refine Finset.sum_congr rfl fun ν _ => Finset.sum_congr rfl fun μ _ => ?_
          rw [hE μ ν, hW μ ν]
          ring
      _ = -(∑ ν : Fin n, ∑ μ : Fin n, E ν μ * W ν μ) := by
          simp only [Finset.sum_neg_distrib]
  linarith

/-- Symmetrization of metric contraction (`#217` §2 B2, arbitrary dimension `n`):
a symmetric Euler tensor `E` pairs identically with the symmetrized gradient `(D + Dᵀ)/2`. -/
theorem symmetric_contract_eq_symmetrized {n : ℕ} (E D : Fin n → Fin n → ℝ)
    (hE : ∀ μ ν, E μ ν = E ν μ) :
    ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * D μ ν =
      ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * ((D μ ν + D ν μ) / 2) := by
  let W : Fin n → Fin n → ℝ := fun μ ν => (D μ ν - D ν μ) / 2
  have hW : ∀ μ ν, W μ ν = -W ν μ := fun μ ν => by
    dsimp [W]
    ring
  have hzero := symmetric_contract_antisym E W hE hW
  have hdecomp :
      ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * D μ ν -
        ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * ((D μ ν + D ν μ) / 2) =
      ∑ μ : Fin n, ∑ ν : Fin n, E μ ν * W μ ν := by
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun μ _ => ?_
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun ν _ => ?_
    dsimp [W]
    ring
  linarith

/-- Contracting symmetric `E_g` against inverse-metric diffeomorphism variation
`δg^{μν} = -(dxi μ ν + dxi ν μ)` equals `-2 ∑ μ ν, E_g μ ν * dxi μ ν` in any dimension `n`. -/
theorem symmetrized_metric_variation_eq {n : ℕ} (E_g dxi : Fin n → Fin n → ℝ)
    (hE : ∀ μ ν, E_g μ ν = E_g ν μ) :
    ∑ μ : Fin n, ∑ ν : Fin n, E_g μ ν * (-(dxi μ ν + dxi ν μ)) =
      -2 * ∑ μ : Fin n, ∑ ν : Fin n, E_g μ ν * dxi μ ν := by
  have hsym := symmetric_contract_eq_symmetrized E_g dxi hE
  calc
    ∑ μ : Fin n, ∑ ν : Fin n, E_g μ ν * (-(dxi μ ν + dxi ν μ))
        = -2 * ∑ μ : Fin n, ∑ ν : Fin n, E_g μ ν * ((dxi μ ν + dxi ν μ) / 2) := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun μ _ => ?_
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun ν _ => ?_
          ring
    _ = -2 * ∑ μ : Fin n, ∑ ν : Fin n, E_g μ ν * dxi μ ν := by rw [← hsym]

/-- Field strength `F_{νμ} = ∇_ν A_μ - ∇_μ A_ν` built from covariant derivatives `dA ν μ := ∇_ν A_μ`. -/
def fieldStrength {n : ℕ} (dA : Fin n → Fin n → ℝ) (ν μ : Fin n) : ℝ :=
  dA ν μ - dA μ ν

/-- **Vector-Sector Equivalence (`#217` §2 B1, arbitrary dimension `n`):**
Given Leibniz divergence `∇_μ(E_A^μ A_ν) = (∇_μ E_A^μ)_part A_ν + E_A^μ ∇_μ A_ν`,
`∑ μ, E_A^μ ∇_ν A_μ - ∑ μ, ∇_μ(E_A^μ A_ν) = ∑ μ, E_A^μ F_{νμ} - A_ν ∑ μ, (∇_μ E_A^μ)_part`. -/
theorem vector_noether_sector_equiv {n : ℕ}
    (E_A A divE_comp : Fin n → ℝ) (dA divEA_flux : Fin n → Fin n → ℝ)
    (hLeib : ∀ ν μ, divEA_flux ν μ = divE_comp μ * A ν + E_A μ * dA μ ν) (ν : Fin n) :
    ∑ μ : Fin n, E_A μ * dA ν μ - ∑ μ : Fin n, divEA_flux ν μ =
      ∑ μ : Fin n, E_A μ * fieldStrength dA ν μ - A ν * ∑ μ : Fin n, divE_comp μ := by
  rw [← Finset.sum_sub_distrib]
  have hrhs :
      ∑ μ : Fin n, E_A μ * fieldStrength dA ν μ - A ν * ∑ μ : Fin n, divE_comp μ =
        ∑ μ : Fin n, (E_A μ * (dA ν μ - dA μ ν) - A ν * divE_comp μ) := by
    rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
    rfl
  rw [hrhs]
  refine Finset.sum_congr rfl fun μ _ => ?_
  rw [hLeib ν μ]
  ring

/-! ## 2. General `n`-Dimensional Off-Shell Diffeomorphism Noether Identity (`#217` Obligation 3) -/

/-- Off-shell Noether operator `𝒩_ν` in dimension `n` for fields `(g^{μν}, A_μ, φ, λ)` with
Euler derivatives defined wrt `g^{μν}` and covariant `A_μ`:
`𝒩_ν := 2 ∇^μ E_{g,μν} + E_A^μ F_{νμ} - A_ν ∇_μ E_A^μ + E_φ ∇_ν φ + E_λ ∇_ν λ`. -/
def noetherOperator {n : ℕ}
    (divE_g E_A A : Fin n → ℝ) (dA : Fin n → Fin n → ℝ)
    (divE_A E_phi : ℝ) (dphi : Fin n → ℝ) (E_lam : ℝ) (dlam : Fin n → ℝ)
    (ν : Fin n) : ℝ :=
  2 * divE_g ν + ∑ μ : Fin n, E_A μ * fieldStrength dA ν μ -
    A ν * divE_A + E_phi * dphi ν + E_lam * dlam ν

/-- **Exact Off-Shell Variational Pairing + Integration-by-Parts Decomposition (`#217` §2):**
Contracts the symmetrized metric variation `δg^{μν} = -2∇^{(μ}ξ^{ν)}`, covariant vector variation
`δA_μ = ξ^ν F_{νμ} + ∇_μ(ξ^ν A_ν)`, scalar variation `δφ = ξ^ν ∇_ν φ`, and multiplier
variation `δλ = ξ^ν ∇_ν λ` against an arbitrary vector field `ξ : Fin n → ℝ`, isolating the
boundary total divergence `divTotal` from `∑ ν, ξ^ν 𝒩_ν`. -/
theorem off_shell_variation_decomposition {n : ℕ}
    (E_g dxi : Fin n → Fin n → ℝ) (hE_symm : ∀ μ ν, E_g μ ν = E_g ν μ)
    (divE_g : Fin n → ℝ)
    (E_A A : Fin n → ℝ) (dA : Fin n → Fin n → ℝ) (divE_A : ℝ)
    (E_phi : ℝ) (dphi : Fin n → ℝ) (E_lam : ℝ) (dlam : Fin n → ℝ)
    (ξ : Fin n → ℝ)
    (div_metric_flux div_vec_flux : ℝ)
    (hIBP_g : -2 * ∑ μ : Fin n, ∑ ν : Fin n, E_g μ ν * dxi μ ν =
        div_metric_flux + ∑ ν : Fin n, ξ ν * (2 * divE_g ν))
    (hIBP_A : ∀ (grad_xiA : Fin n → ℝ),
        ∑ μ : Fin n, E_A μ * grad_xiA μ =
          div_vec_flux + ∑ ν : Fin n, ξ ν * (-(A ν * divE_A)))
    (grad_xiA : Fin n → ℝ) :
    let δS_integrand :=
      (∑ μ : Fin n, ∑ ν : Fin n, E_g μ ν * (-(dxi μ ν + dxi ν μ))) +
      (∑ μ : Fin n, E_A μ * ((∑ ν : Fin n, ξ ν * fieldStrength dA ν μ) + grad_xiA μ)) +
      E_phi * (∑ ν : Fin n, ξ ν * dphi ν) +
      E_lam * (∑ ν : Fin n, ξ ν * dlam ν)
    δS_integrand =
      (div_metric_flux + div_vec_flux) +
        ∑ ν : Fin n, ξ ν * noetherOperator divE_g E_A A dA divE_A E_phi dphi E_lam dlam ν := by
  intro δS_integrand
  have hg := symmetrized_metric_variation_eq E_g dxi hE_symm
  have hA_ibp := hIBP_A grad_xiA
  have hF_swap :
      ∑ μ : Fin n, E_A μ * ∑ ν : Fin n, ξ ν * fieldStrength dA ν μ =
        ∑ ν : Fin n, ξ ν * ∑ μ : Fin n, E_A μ * fieldStrength dA ν μ := by
    calc
      ∑ μ : Fin n, E_A μ * ∑ ν : Fin n, ξ ν * fieldStrength dA ν μ
          = ∑ μ : Fin n, ∑ ν : Fin n, ξ ν * (E_A μ * fieldStrength dA ν μ) := by
            refine Finset.sum_congr rfl fun μ _ => ?_
            rw [Finset.mul_sum]
            refine Finset.sum_congr rfl fun ν _ => ?_
            ring
      _ = ∑ ν : Fin n, ∑ μ : Fin n, ξ ν * (E_A μ * fieldStrength dA ν μ) := Finset.sum_comm
      _ = ∑ ν : Fin n, ξ ν * ∑ μ : Fin n, E_A μ * fieldStrength dA ν μ := by
          refine Finset.sum_congr rfl fun ν _ => by rw [← Finset.mul_sum]
  have hnoeth :
      ∑ ν : Fin n, ξ ν * noetherOperator divE_g E_A A dA divE_A E_phi dphi E_lam dlam ν =
        ∑ ν : Fin n, ξ ν * (2 * divE_g ν) +
        ∑ ν : Fin n, ξ ν * (∑ μ : Fin n, E_A μ * fieldStrength dA ν μ) +
        ∑ ν : Fin n, ξ ν * (-(A ν * divE_A)) +
        ∑ ν : Fin n, ξ ν * (E_phi * dphi ν) +
        ∑ ν : Fin n, ξ ν * (E_lam * dlam ν) := by
    simp only [noetherOperator, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun ν _ => ?_
    ring
  dsimp only [δS_integrand]
  have hAsplit :
      ∑ μ : Fin n, E_A μ * (∑ ν : Fin n, ξ ν * fieldStrength dA ν μ + grad_xiA μ) =
        ∑ μ : Fin n, E_A μ * (∑ ν : Fin n, ξ ν * fieldStrength dA ν μ) +
        ∑ μ : Fin n, E_A μ * grad_xiA μ := by
    simp only [mul_add, Finset.sum_add_distrib]
  rw [hg, hIBP_g, hAsplit, hA_ibp, hF_swap, hnoeth, Finset.mul_sum, Finset.mul_sum]
  have hphi : ∑ x : Fin n, E_phi * (ξ x * dphi x) = ∑ x : Fin n, ξ x * (E_phi * dphi x) := by
    refine Finset.sum_congr rfl fun ν _ => by ring
  have hlam : ∑ x : Fin n, E_lam * (ξ x * dlam x) = ∑ x : Fin n, ξ x * (E_lam * dlam x) := by
    refine Finset.sum_congr rfl fun ν _ => by ring
  rw [hphi, hlam]
  ring

/-- **Arbitrary-`ξ` Fundamental Lemma:** If the covariant Noether pairing `∑ ν, ξ ν * N ν` vanishes
for every coordinate direction `ξ = Pi.single ν 1`, then every component `N ν` vanishes identically. -/
theorem diffeo_invariance_implies_noether_identity {n : ℕ}
    (N : Fin n → ℝ) (hinv : ∀ ξ : Fin n → ℝ, ∑ ν : Fin n, ξ ν * N ν = 0) (ν : Fin n) :
    N ν = 0 := by
  have h := hinv (Pi.single ν (1 : ℝ))
  have hsum : ∑ μ : Fin n, (Pi.single ν (1 : ℝ) : Fin n → ℝ) μ * N μ = N ν := by
    rw [Finset.sum_eq_single ν]
    · simp
    · intro b _ hb
      simp [Pi.single_eq_of_ne hb]
    · simp
  linarith

/-- On the gravitational + scalar/multiplier shell (`E_g = 0, E_φ = 0, E_λ = 0`), the off-shell
diffeomorphism Noether identity collapses cleanly to the constrained vector Bianchi constraint
`∑ μ, E_A^μ F_{νμ} - A_ν ∇_μ E_A^μ = 0`. -/
theorem diffeo_noether_on_vector_subshell {n : ℕ}
    (divE_g E_A A : Fin n → ℝ) (dA : Fin n → Fin n → ℝ)
    (divE_A E_phi : ℝ) (dphi : Fin n → ℝ) (E_lam : ℝ) (dlam : Fin n → ℝ)
    (hNoeth : ∀ ν, noetherOperator divE_g E_A A dA divE_A E_phi dphi E_lam dlam ν = 0)
    (hg : ∀ ν, divE_g ν = 0) (hphi : E_phi = 0) (hlam : E_lam = 0) (ν : Fin n) :
    ∑ μ : Fin n, E_A μ * fieldStrength dA ν μ - A ν * divE_A = 0 := by
  have h := hNoeth ν
  unfold noetherOperator at h
  rw [hg ν, hphi, hlam] at h
  linarith

/-- **Sign-Convention Sensitivity Witness:** Flipping the sign of `- A_ν ∇_μ E_A^μ` (for example
via lowering/raising or mistaking `δA^μ` vs `δA_μ` without transforming the Euler derivative) fails
the off-shell Noether identity by `2 A_ν ∇_μ E_A^μ ≠ 0` whenever `A_ν ≠ 0` and `∇_μ E_A^μ ≠ 0`. -/
theorem noether_sign_flip_counterexample {A_nu divE_A rest : ℝ}
    (hTrue : rest - A_nu * divE_A = 0) (hA : A_nu ≠ 0) (hdiv : divE_A ≠ 0) :
    rest + A_nu * divE_A = 2 * (A_nu * divE_A) ∧ rest + A_nu * divE_A ≠ 0 := by
  have hsum : rest + A_nu * divE_A = 2 * (A_nu * divE_A) := by linarith
  refine ⟨hsum, ?_⟩
  rw [hsum]
  exact mul_ne_zero (by norm_num) (mul_ne_zero hA hdiv)

/-! ## 3. Matter Conservation from Matter Shell & Total Diffeomorphism Identity (`#217` Obligation 4) -/

/-- From the matter-sector diffeomorphism identity `-∇^μ T_{μν} + E_matter · ∇_ν ψ = 0`,
satisfying the matter field equations (`E_matter = 0`) enforces covariant stress conservation
`∇^μ T_{μν} = 0` without imposing conservation as a separate postulate. -/
theorem matter_conservation_from_matter_eom {n : ℕ}
    (divT : Fin n → ℝ) (matterEulerLie : Fin n → ℝ)
    (hMatterDiffeo : ∀ ν, -divT ν + matterEulerLie ν = 0)
    (hMatterEOM : ∀ ν, matterEulerLie ν = 0) (ν : Fin n) :
    divT ν = 0 := by
  have h := hMatterDiffeo ν
  rw [hMatterEOM ν] at h
  linarith

/-- **Total-Action Noether Route (`E_g^{tot} = E_g^{AeST} - ½ T`):**
Under minimal coupling `S_tot = S_AeST[g, A, φ, λ] + S_m[g, ψ]`, if the total fields satisfy the
gravitational (`2 ∇^μ E_{g,AeST,μν} = ∇^μ T_{μν}`) and aether (`E_A = 0, divE_A = 0, E_φ = 0, E_λ = 0`)
field equations, the AeST diffeomorphism Noether identity directly enforces `∇^μ T_{μν} = 0`. -/
theorem matter_conservation_from_aest_total_noether {n : ℕ}
    (divE_g_AeST divT E_A A : Fin n → ℝ) (dA : Fin n → Fin n → ℝ)
    (divE_A E_phi : ℝ) (dphi : Fin n → ℝ) (E_lam : ℝ) (dlam : Fin n → ℝ)
    (hAeSTNoeth : ∀ ν, noetherOperator divE_g_AeST E_A A dA divE_A E_phi dphi E_lam dlam ν = 0)
    (hEin : ∀ ν, 2 * divE_g_AeST ν = divT ν)
    (hEA : ∀ μ, E_A μ = 0) (hdivEA : divE_A = 0) (hphi : E_phi = 0) (hlam : E_lam = 0)
    (ν : Fin n) :
    divT ν = 0 := by
  have h := hAeSTNoeth ν
  unfold noetherOperator at h
  have hvec0 : ∑ μ : Fin n, E_A μ * fieldStrength dA ν μ = 0 := by
    simp [hEA]
  rw [hEin ν, hvec0, hdivEA, hphi, hlam] at h
  linarith

/-- **Nonminimal-Coupling Boundary (`#217` §3):** If matter couples nonminimally to `(A, φ)` so that
total equilibrium fixes `E_A^{AeST} = -J_int`, `∇_μ E_A^{AeST} = -divJ`, `E_φ^{AeST} = -Q_int` while
`2 ∇^μ E_{g,AeST,μν} = ∇^μ T_{μν}`, then `∇^μ T_{μν}` need NOT vanish — it equals the exact
interaction exchange density `∑ μ, J_int^μ F_{νμ} - A_ν divJ + Q_int ∇_ν φ`. -/
theorem nonminimal_coupling_exchange_law {n : ℕ}
    (divE_g_AeST divT E_A A : Fin n → ℝ) (dA : Fin n → Fin n → ℝ)
    (divE_A E_phi : ℝ) (dphi : Fin n → ℝ) (E_lam : ℝ) (dlam : Fin n → ℝ)
    (hAeSTNoeth : ∀ ν, noetherOperator divE_g_AeST E_A A dA divE_A E_phi dphi E_lam dlam ν = 0)
    (hEin : ∀ ν, 2 * divE_g_AeST ν = divT ν) (hlam : E_lam = 0) (ν : Fin n) :
    divT ν = -(∑ μ : Fin n, E_A μ * fieldStrength dA ν μ - A ν * divE_A + E_phi * dphi ν) := by
  have h := hAeSTNoeth ν
  unfold noetherOperator at h
  rw [hEin ν, hlam] at h
  linarith

/-! ## 4. Arbitrary-Dimension Levi-Civita Metric-Divergence Identity (`verify_issue217` C1) -/

/-- General Levi-Civita Christoffel symbol `Γ^λ_{μα}` defined from arbitrary inverse metric `ginv`
and metric partial derivatives `dg μ σ α := ∂_μ g_{σα}` in arbitrary dimension `n`. -/
def christoffelGen {n : ℕ} (ginv : Fin n → Fin n → ℝ) (dg : Fin n → Fin n → Fin n → ℝ)
    (lam μ α : Fin n) : ℝ :=
  (1 / 2 : ℝ) * ∑ σ : Fin n, ginv lam σ * (dg μ σ α + dg α σ μ - dg σ μ α)

/-- **Metric-Compatible Christoffel Identity (`#217` §3 C1, arbitrary dimension `n`):**
For ANY invertible symmetric metric `g`, inverse `ginv`, symmetric derivative `dg`, and ANY
symmetric rank-2 tensor `T`, the connection terms inside `∇^μ T_{μν}` cancel identically:
`-(∂_μ g_{νλ}) T^{μλ} + g_{νλ} Γ^λ_{μα} T^{μα} + ½(∂_ν g_{μα}) T^{μα} = 0`. -/
theorem metric_div_gamma_identity {n : ℕ}
    (g ginv T : Fin n → Fin n → ℝ) (dg : Fin n → Fin n → Fin n → ℝ)
    (hinv : ∀ ν σ : Fin n, ∑ lam : Fin n, g ν lam * ginv lam σ = if ν = σ then 1 else 0)
    (hTsym : ∀ a b : Fin n, T a b = T b a)
    (ν : Fin n) :
    -(∑ μ : Fin n, ∑ lam : Fin n, dg μ ν lam * T μ lam) +
      ∑ lam : Fin n, g ν lam * (∑ μ : Fin n, ∑ alp : Fin n, christoffelGen ginv dg lam μ alp * T μ alp) +
      (1 / 2 : ℝ) * ∑ μ : Fin n, ∑ alp : Fin n, dg ν μ alp * T μ alp = 0 := by
  have hcontract :
      ∑ lam : Fin n, g ν lam *
          (∑ μ : Fin n, ∑ alp : Fin n, christoffelGen ginv dg lam μ alp * T μ alp) =
        (1 / 2 : ℝ) *
          ∑ μ : Fin n, ∑ alp : Fin n, (dg μ ν alp + dg alp ν μ - dg ν μ alp) * T μ alp := by
    calc
      ∑ lam : Fin n, g ν lam *
          (∑ μ : Fin n, ∑ alp : Fin n, christoffelGen ginv dg lam μ alp * T μ alp)
          = ∑ μ : Fin n, ∑ alp : Fin n,
              ((∑ lam : Fin n, g ν lam * christoffelGen ginv dg lam μ alp) * T μ alp) := by
            calc
              ∑ lam : Fin n, g ν lam *
                  (∑ μ : Fin n, ∑ alp : Fin n, christoffelGen ginv dg lam μ alp * T μ alp)
                  = ∑ lam : Fin n, ∑ μ : Fin n, ∑ alp : Fin n,
                      g ν lam * (christoffelGen ginv dg lam μ alp * T μ alp) := by
                    refine Finset.sum_congr rfl fun lam _ => ?_
                    rw [Finset.mul_sum]
                    refine Finset.sum_congr rfl fun μ _ => ?_
                    rw [Finset.mul_sum]
              _ = ∑ μ : Fin n, ∑ lam : Fin n, ∑ alp : Fin n,
                      g ν lam * (christoffelGen ginv dg lam μ alp * T μ alp) := Finset.sum_comm
              _ = ∑ μ : Fin n, ∑ alp : Fin n, ∑ lam : Fin n,
                      g ν lam * (christoffelGen ginv dg lam μ alp * T μ alp) := by
                    refine Finset.sum_congr rfl fun μ _ => Finset.sum_comm
              _ = ∑ μ : Fin n, ∑ alp : Fin n,
                      (∑ lam : Fin n, g ν lam * christoffelGen ginv dg lam μ alp) * T μ alp := by
                    refine Finset.sum_congr rfl fun μ _ => Finset.sum_congr rfl fun alp _ => ?_
                    rw [Finset.sum_mul]
                    refine Finset.sum_congr rfl fun lam _ => by ring
      _ = ∑ μ : Fin n, ∑ alp : Fin n,
              ((1 / 2 : ℝ) * (dg μ ν alp + dg alp ν μ - dg ν μ alp)) * T μ alp := by
          refine Finset.sum_congr rfl fun μ _ => Finset.sum_congr rfl fun alp _ => ?_
          have hgG :
              ∑ lam : Fin n, g ν lam * christoffelGen ginv dg lam μ alp =
                (1 / 2 : ℝ) * (dg μ ν alp + dg alp ν μ - dg ν μ alp) := by
            calc
              ∑ lam : Fin n, g ν lam * christoffelGen ginv dg lam μ alp
                  = (1 / 2 : ℝ) * ∑ lam : Fin n, ∑ σ : Fin n,
                      (g ν lam * ginv lam σ) * (dg μ σ alp + dg alp σ μ - dg σ μ alp) := by
                    rw [Finset.mul_sum]
                    refine Finset.sum_congr rfl fun lam _ => ?_
                    unfold christoffelGen
                    have hin : ∀ σ : Fin n,
                        g ν lam * ((1 / 2 : ℝ) * (ginv lam σ * (dg μ σ alp + dg alp σ μ - dg σ μ alp))) =
                          (1 / 2 : ℝ) * ((g ν lam * ginv lam σ) * (dg μ σ alp + dg alp σ μ - dg σ μ alp)) :=
                      fun σ => by ring
                    rw [← mul_assoc, mul_comm (g ν lam) (1 / 2 : ℝ), mul_assoc, Finset.mul_sum]
                    congr 1
                    refine Finset.sum_congr rfl fun σ _ => by ring
              _ = (1 / 2 : ℝ) * ∑ σ : Fin n,
                      (∑ lam : Fin n, g ν lam * ginv lam σ) *
                        (dg μ σ alp + dg alp σ μ - dg σ μ alp) := by
                    rw [Finset.sum_comm]
                    congr 1
                    refine Finset.sum_congr rfl fun σ _ => ?_
                    rw [Finset.sum_mul]
              _ = (1 / 2 : ℝ) * (dg μ ν alp + dg alp ν μ - dg ν μ alp) := by
                    congr 1
                    have hsub :
                        ∑ σ : Fin n,
                            (∑ lam : Fin n, g ν lam * ginv lam σ) *
                              (dg μ σ alp + dg alp σ μ - dg σ μ alp) =
                          ∑ σ : Fin n,
                            (if ν = σ then (1 : ℝ) else 0) *
                              (dg μ σ alp + dg alp σ μ - dg σ μ alp) := by
                      refine Finset.sum_congr rfl fun σ _ => by rw [hinv ν σ]
                    rw [hsub]
                    simp
          rw [hgG]
      _ = (1 / 2 : ℝ) *
            ∑ μ : Fin n, ∑ alp : Fin n, (dg μ ν alp + dg alp ν μ - dg ν μ alp) * T μ alp := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun μ _ => by
            rw [Finset.mul_sum]
            refine Finset.sum_congr rfl fun alp _ => by ring
  have hswap :
      ∑ μ : Fin n, ∑ alp : Fin n, dg alp ν μ * T μ alp =
        ∑ μ : Fin n, ∑ alp : Fin n, dg μ ν alp * T μ alp := by
    calc
      ∑ μ : Fin n, ∑ alp : Fin n, dg alp ν μ * T μ alp
          = ∑ alp : Fin n, ∑ μ : Fin n, dg alp ν μ * T alp μ := by
            rw [Finset.sum_comm]
            refine Finset.sum_congr rfl fun alp _ => Finset.sum_congr rfl fun μ _ => ?_
            rw [hTsym μ alp]
      _ = ∑ μ : Fin n, ∑ alp : Fin n, dg μ ν alp * T μ alp := rfl
  rw [hcontract]
  have hcomb :
      ∑ μ : Fin n, ∑ alp : Fin n, (dg μ ν alp + dg alp ν μ - dg ν μ alp) * T μ alp =
        2 * ∑ μ : Fin n, ∑ alp : Fin n, dg μ ν alp * T μ alp -
          ∑ μ : Fin n, ∑ alp : Fin n, dg ν μ alp * T μ alp := by
    calc
      ∑ μ : Fin n, ∑ alp : Fin n, (dg μ ν alp + dg alp ν μ - dg ν μ alp) * T μ alp
          = (∑ μ : Fin n, ∑ alp : Fin n, dg μ ν alp * T μ alp) +
            (∑ μ : Fin n, ∑ alp : Fin n, dg alp ν μ * T μ alp) -
            (∑ μ : Fin n, ∑ alp : Fin n, dg ν μ alp * T μ alp) := by
            simp only [add_mul, sub_mul, Finset.sum_add_distrib, Finset.sum_sub_distrib]
      _ = 2 * ∑ μ : Fin n, ∑ alp : Fin n, dg μ ν alp * T μ alp -
            ∑ μ : Fin n, ∑ alp : Fin n, dg ν μ alp * T μ alp := by
            rw [hswap]
            ring
  rw [hcomb]
  ring

/-! ## 5. Smooth 1+1D Curved-Spacetime Differential Calculus (`Fin 2 → ℝ`, Real `fderiv`) -/

/-- Two-dimensional spacetime coordinate chart `ℝ²` modeled as `Fin 2 → ℝ` (`0 = t`, `1 = x`). -/
abbrev Coord2 := Fin 2 → ℝ

/-- Partial derivative `∂_μ f(x)` defined via the genuine Mathlib Fréchet derivative `fderiv ℝ`. -/
def pd (f : Coord2 → ℝ) (x : Coord2) (μ : Fin 2) : ℝ :=
  fderiv ℝ f x (Pi.single μ (1 : ℝ))

private lemma fin2_eq (i : Fin 2) : i = 0 ∨ i = 1 := by fin_cases i <;> simp

private lemma pd_add {f g : Coord2 → ℝ} {x : Coord2}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (μ : Fin 2) :
    pd (fun y => f y + g y) x μ = pd f x μ + pd g x μ := by
  have h : HasFDerivAt (fun y => f y + g y) (fderiv ℝ f x + fderiv ℝ g x) x :=
    hf.hasFDerivAt.add hg.hasFDerivAt
  unfold pd
  rw [h.fderiv]
  simp

private lemma pd_sub {f g : Coord2 → ℝ} {x : Coord2}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (μ : Fin 2) :
    pd (fun y => f y - g y) x μ = pd f x μ - pd g x μ := by
  have h : HasFDerivAt (fun y => f y - g y) (fderiv ℝ f x - fderiv ℝ g x) x :=
    hf.hasFDerivAt.sub hg.hasFDerivAt
  unfold pd
  rw [h.fderiv]
  simp

private lemma pd_neg {f : Coord2 → ℝ} {x : Coord2}
    (hf : DifferentiableAt ℝ f x) (μ : Fin 2) :
    pd (fun y => -f y) x μ = -pd f x μ := by
  have h : HasFDerivAt (fun y => -f y) (-fderiv ℝ f x) x := hf.hasFDerivAt.neg
  unfold pd
  rw [h.fderiv]
  simp

private lemma pd_neg_add {f g : Coord2 → ℝ} {x : Coord2}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (μ : Fin 2) :
    pd (fun y => -f y + g y) x μ = -pd f x μ + pd g x μ := by
  have hf' : DifferentiableAt ℝ (fun y => -f y) x := hf.neg
  rw [pd_add hf' hg μ, pd_neg hf μ]

private lemma pd_mul {f g : Coord2 → ℝ} {x : Coord2}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (μ : Fin 2) :
    pd (fun y => f y * g y) x μ = f x * pd g x μ + g x * pd f x μ := by
  have h : HasFDerivAt (fun y => f y * g y) (f x • fderiv ℝ g x + g x • fderiv ℝ f x) x :=
    hf.hasFDerivAt.mul hg.hasFDerivAt
  unfold pd
  rw [h.fderiv]
  simp [smul_eq_mul]

private lemma pd_const_mul {c : ℝ} {f : Coord2 → ℝ} {x : Coord2}
    (hf : DifferentiableAt ℝ f x) (μ : Fin 2) :
    pd (fun y => c * f y) x μ = c * pd f x μ := by
  have h : HasFDerivAt (fun y => c * f y) (c • fderiv ℝ f x) x := hf.hasFDerivAt.const_mul c
  unfold pd
  rw [h.fderiv]
  simp [smul_eq_mul]

private lemma pd_exp {f : Coord2 → ℝ} {x : Coord2}
    (hf : DifferentiableAt ℝ f x) (μ : Fin 2) :
    pd (fun y => Real.exp (f y)) x μ = Real.exp (f x) * pd f x μ := by
  have h : HasFDerivAt (fun y => Real.exp (f y)) (Real.exp (f x) • fderiv ℝ f x) x :=
    (Real.hasDerivAt_exp (f x)).comp_hasFDerivAt x hf.hasFDerivAt
  unfold pd
  rw [h.fderiv]
  simp [smul_eq_mul]

private lemma pd_comp_real {φ : ℝ → ℝ} {f : Coord2 → ℝ} {x : Coord2}
    (hφ : DifferentiableAt ℝ φ (f x)) (hf : DifferentiableAt ℝ f x) (μ : Fin 2) :
    pd (fun y => φ (f y)) x μ = deriv φ (f x) * pd f x μ := by
  have h : HasFDerivAt (fun y => φ (f y)) (deriv φ (f x) • fderiv ℝ f x) x :=
    hφ.hasDerivAt.comp_hasFDerivAt x hf.hasFDerivAt
  unfold pd
  rw [h.fderiv]
  simp [smul_eq_mul]

/-- **Clairaut / Schwarz Symmetry (`C^2` charts):**
On any twice continuously differentiable scalar field `f : Coord2 → ℝ`, mixed Fréchet partial
derivatives commute identically: `∂_μ ∂_ν f(x) = ∂_ν ∂_μ f(x)`. -/
theorem pd_comm {f : Coord2 → ℝ} (hf : ContDiff ℝ 2 f) (x : Coord2) (μ ν : Fin 2) :
    pd (fun y => pd f y ν) x μ = pd (fun y => pd f y μ) x ν := by
  have hf1 : ContDiff ℝ 1 (fderiv ℝ f) := hf.fderiv_right (m := 1) (by norm_num)
  have hdiff : DifferentiableAt ℝ (fderiv ℝ f) x := (hf1.differentiable one_ne_zero) x
  have hcν : HasFDerivAt (fun y => fderiv ℝ f y (Pi.single ν (1 : ℝ)))
      ((fderiv ℝ f x).comp (0 : Coord2 →L[ℝ] Coord2) +
        (fderiv ℝ (fderiv ℝ f) x).flip (Pi.single ν (1 : ℝ))) x :=
    hdiff.hasFDerivAt.clm_apply (hasFDerivAt_const (Pi.single ν (1 : ℝ) : Coord2) x)
  have hcμ : HasFDerivAt (fun y => fderiv ℝ f y (Pi.single μ (1 : ℝ)))
      ((fderiv ℝ f x).comp (0 : Coord2 →L[ℝ] Coord2) +
        (fderiv ℝ (fderiv ℝ f) x).flip (Pi.single μ (1 : ℝ))) x :=
    hdiff.hasFDerivAt.clm_apply (hasFDerivAt_const (Pi.single μ (1 : ℝ) : Coord2) x)
  have hsymm : fderiv ℝ (fderiv ℝ f) x (Pi.single μ (1 : ℝ)) (Pi.single ν (1 : ℝ)) =
      fderiv ℝ (fderiv ℝ f) x (Pi.single ν (1 : ℝ)) (Pi.single μ (1 : ℝ)) :=
    (hf.contDiffAt.isSymmSndFDerivAt (by simp)).eq (Pi.single μ (1 : ℝ)) (Pi.single ν (1 : ℝ))
  unfold pd
  rw [hcν.fderiv, hcμ.fderiv]
  simp [ContinuousLinearMap.flip_apply]
  exact hsymm

/-- 1+1D curved diagonal Lorentzian metric `g_{μν}(x) = diag(-e^{2α(x)}, e^{2β(x)})`. -/
def gDiag (α β : Coord2 → ℝ) (x : Coord2) : Fin 2 → Fin 2 → ℝ
  | 0, 0 => -Real.exp (2 * α x)
  | 1, 1 => Real.exp (2 * β x)
  | _, _ => 0

/-- Inverse 1+1D curved diagonal metric `g^{μν}(x) = diag(-e^{-2α(x)}, e^{-2β(x)})`. -/
def gInvDiag (α β : Coord2 → ℝ) (x : Coord2) : Fin 2 → Fin 2 → ℝ
  | 0, 0 => -Real.exp (-2 * α x)
  | 1, 1 => Real.exp (-2 * β x)
  | _, _ => 0

/-- Volume density `√(-g) = e^{α(x) + β(x)}`. -/
def sqrtNegG (α β : Coord2 → ℝ) (x : Coord2) : ℝ :=
  Real.exp (α x + β x)

/-- Metric inverse relation `g_{νλ} g^{λσ} = δ_ν^σ` everywhere on `Coord2`. -/
theorem gDiag_mul_gInvDiag (α β : Coord2 → ℝ) (x : Coord2) (ν σ : Fin 2) :
    ∑ lam : Fin 2, gDiag α β x ν lam * gInvDiag α β x lam σ = if ν = σ then 1 else 0 := by
  fin_cases ν <;> fin_cases σ <;>
    simp [Fin.sum_univ_two, gDiag, gInvDiag, ← Real.exp_add]

/-- Partial derivatives of the 2D diagonal metric `dgDiag μ a b = ∂_μ g_{ab}`. -/
def dgDiag (α β : Coord2 → ℝ) (x : Coord2) (μ a b : Fin 2) : ℝ :=
  pd (fun y => gDiag α β y a b) x μ

/-- Closed-form Christoffel symbols `Γ^λ_{μν}` computed from `gDiag`, `gInvDiag`, and `dgDiag`. -/
def gammaDiag (α β : Coord2 → ℝ) (x : Coord2) (lam μ ν : Fin 2) : ℝ :=
  christoffelGen (gInvDiag α β x) (dgDiag α β x) lam μ ν

private lemma pd_differentiableAt {f : Coord2 → ℝ} (hf : ContDiff ℝ 2 f) (x : Coord2) (μ : Fin 2) :
    DifferentiableAt ℝ (fun y => pd f y μ) x := by
  have hf1 : ContDiff ℝ 1 (fderiv ℝ f) := hf.fderiv_right (m := 1) (by norm_num)
  have hdiff : DifferentiableAt ℝ (fderiv ℝ f) x := (hf1.differentiable one_ne_zero) x
  exact (hdiff.hasFDerivAt.clm_apply (hasFDerivAt_const (Pi.single μ (1 : ℝ) : Coord2) x)).differentiableAt

private lemma pd_g00 (α : Coord2 → ℝ) {x : Coord2} (hα : DifferentiableAt ℝ α x) (μ : Fin 2) :
    pd (fun y => -Real.exp (2 * α y)) x μ = -2 * Real.exp (2 * α x) * pd α x μ := by
  have h2α : DifferentiableAt ℝ (fun y => 2 * α y) x := hα.const_mul 2
  rw [pd_neg h2α.exp, pd_exp h2α, pd_const_mul hα]
  ring

private lemma pd_g11 (β : Coord2 → ℝ) {x : Coord2} (hβ : DifferentiableAt ℝ β x) (μ : Fin 2) :
    pd (fun y => Real.exp (2 * β y)) x μ = 2 * Real.exp (2 * β x) * pd β x μ := by
  have h2β : DifferentiableAt ℝ (fun y => 2 * β y) x := hβ.const_mul 2
  rw [pd_exp h2β, pd_const_mul hβ]
  ring

private lemma dgDiag_00 (α β : Coord2 → ℝ) {x : Coord2} (hα : DifferentiableAt ℝ α x) (μ : Fin 2) :
    dgDiag α β x μ 0 0 = -2 * Real.exp (2 * α x) * pd α x μ := by
  unfold dgDiag gDiag
  exact pd_g00 α hα μ

private lemma dgDiag_11 (α β : Coord2 → ℝ) {x : Coord2} (hβ : DifferentiableAt ℝ β x) (μ : Fin 2) :
    dgDiag α β x μ 1 1 = 2 * Real.exp (2 * β x) * pd β x μ := by
  unfold dgDiag gDiag
  exact pd_g11 β hβ μ

private lemma dgDiag_01 (α β : Coord2 → ℝ) (x : Coord2) (μ : Fin 2) :
    dgDiag α β x μ 0 1 = 0 := by
  unfold dgDiag gDiag pd
  simp

private lemma dgDiag_10 (α β : Coord2 → ℝ) (x : Coord2) (μ : Fin 2) :
    dgDiag α β x μ 1 0 = 0 := by
  unfold dgDiag gDiag pd
  simp

private lemma gammaDiag_trace_sum (α β : Coord2 → ℝ) {x : Coord2}
    (hα : DifferentiableAt ℝ α x) (hβ : DifferentiableAt ℝ β x) (lam : Fin 2) :
    ∑ μ : Fin 2, gammaDiag α β x μ μ lam = pd α x lam + pd β x lam := by
  rcases fin2_eq lam with rfl | rfl <;>
    · simp only [Fin.sum_univ_two, gammaDiag, christoffelGen, gInvDiag, Fin.isValue,
        dgDiag_00 α β hα, dgDiag_01 α β x, dgDiag_10 α β x, dgDiag_11 α β hβ,
        zero_mul, zero_add, add_zero]
      ring_nf
      rw [← Real.exp_add, ← Real.exp_add]
      simp

/-- **Curved Density Divergence Identity (`#217` §2 B3, `fderiv` Proof):**
In any 1+1D curved diagonal spacetime `g = diag(-e^{2α(t,x)}, e^{2β(t,x)})` with differentiable
metric functions `(α, β)` and differentiable vector components `V : Fin 2 → Coord2 → ℝ`,
`∑ μ, ∂_μ(√-g V^μ) = √-g ∑ μ, (∂_μ V^μ + ∑ λ, Γ^μ_{μλ} V^λ)`. -/
theorem density_divergence_identity_2d (α β : Coord2 → ℝ) (V : Fin 2 → Coord2 → ℝ)
    (x : Coord2) (hα : DifferentiableAt ℝ α x) (hβ : DifferentiableAt ℝ β x)
    (hV : ∀ μ : Fin 2, DifferentiableAt ℝ (V μ) x) :
    ∑ μ : Fin 2, pd (fun y => sqrtNegG α β y * V μ y) x μ =
      sqrtNegG α β x *
        ∑ μ : Fin 2, (pd (V μ) x μ + ∑ lam : Fin 2, gammaDiag α β x μ μ lam * V lam x) := by
  have hsum : DifferentiableAt ℝ (fun y => α y + β y) x := hα.add hβ
  have hsqrt : DifferentiableAt ℝ (sqrtNegG α β) x := hsum.exp
  have hpd_sqrt : ∀ μ, pd (sqrtNegG α β) x μ = sqrtNegG α β x * (pd α x μ + pd β x μ) := fun μ => by
    unfold sqrtNegG
    rw [pd_exp hsum, pd_add hα hβ]
  have hL :
      ∑ μ : Fin 2, pd (fun y => sqrtNegG α β y * V μ y) x μ =
        sqrtNegG α β x * (∑ μ : Fin 2, pd (V μ) x μ +
          ∑ lam : Fin 2, (pd α x lam + pd β x lam) * V lam x) := by
    calc
      ∑ μ : Fin 2, pd (fun y => sqrtNegG α β y * V μ y) x μ
          = ∑ μ : Fin 2, (sqrtNegG α β x * pd (V μ) x μ + V μ x * pd (sqrtNegG α β) x μ) := by
            refine Finset.sum_congr rfl fun μ _ => pd_mul hsqrt (hV μ) μ
      _ = ∑ μ : Fin 2, sqrtNegG α β x * pd (V μ) x μ +
            ∑ lam : Fin 2, sqrtNegG α β x * ((pd α x lam + pd β x lam) * V lam x) := by
            rw [Finset.sum_add_distrib]
            congr 1
            refine Finset.sum_congr rfl fun lam _ => ?_
            rw [hpd_sqrt lam]
            ring
      _ = sqrtNegG α β x * (∑ μ : Fin 2, pd (V μ) x μ +
            ∑ lam : Fin 2, (pd α x lam + pd β x lam) * V lam x) := by
            simp only [mul_add, Finset.mul_sum]
  have hinner :
      ∑ μ : Fin 2, (pd (V μ) x μ + ∑ lam : Fin 2, gammaDiag α β x μ μ lam * V lam x) =
        ∑ μ : Fin 2, pd (V μ) x μ +
          ∑ lam : Fin 2, (pd α x lam + pd β x lam) * V lam x := by
    calc
      ∑ μ : Fin 2, (pd (V μ) x μ + ∑ lam : Fin 2, gammaDiag α β x μ μ lam * V lam x)
          = ∑ μ : Fin 2, pd (V μ) x μ +
              ∑ μ : Fin 2, ∑ lam : Fin 2, gammaDiag α β x μ μ lam * V lam x :=
            Finset.sum_add_distrib
      _ = ∑ μ : Fin 2, pd (V μ) x μ +
              ∑ lam : Fin 2, (∑ μ : Fin 2, gammaDiag α β x μ μ lam) * V lam x := by
            congr 1
            rw [Finset.sum_comm]
            refine Finset.sum_congr rfl fun lam _ => by rw [Finset.sum_mul]
      _ = ∑ μ : Fin 2, pd (V μ) x μ +
              ∑ lam : Fin 2, (pd α x lam + pd β x lam) * V lam x := by
            congr 1
            refine Finset.sum_congr rfl fun lam _ => ?_
            rw [gammaDiag_trace_sum α β hα hβ lam]
  rw [hL, hinner]

/-- Scalar matter Lagrangian scalar `K = ½ g^{ab} ∂_a χ ∂_b χ + V(χ)` on `Coord2`. -/
def scalarK (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) : ℝ :=
  (1 / 2 : ℝ) * (∑ a : Fin 2, ∑ b : Fin 2, gInvDiag α β y a b * pd χ y a * pd χ y b) + V (χ y)

/-- Covariant stress-energy tensor `T_{μν} = ∂_μ χ ∂_ν χ - g_{μν} K`. -/
def scalarTDown (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) (μ ν : Fin 2) : ℝ :=
  pd χ y μ * pd χ y ν - gDiag α β y μ ν * scalarK α β χ V y

/-- Mixed stress-energy tensor `T^μ_ν = g^{μa} T_{aν}`. -/
def scalarTMixed (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) (μ ν : Fin 2) : ℝ :=
  ∑ a : Fin 2, gInvDiag α β y μ a * scalarTDown α β χ V y a ν

/-- Contravariant stress-energy tensor `T^{ab} = T^a_c g^{cb}`. -/
def scalarTCon (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) (a b : Fin 2) : ℝ :=
  ∑ c : Fin 2, scalarTMixed α β χ V y a c * gInvDiag α β y c b

/-- Curved 2D d'Alembertian `□χ = (√-g)⁻¹ ∂_μ(√-g g^{μσ} ∂_σ χ)`. -/
def scalarBox (α β χ : Coord2 → ℝ) (y : Coord2) : ℝ :=
  (∑ μ : Fin 2, pd (fun z => sqrtNegG α β z * ∑ σ : Fin 2, gInvDiag α β z μ σ * pd χ z σ) y μ) /
    sqrtNegG α β y

/-- Scalar matter Euler derivative `E_χ = □χ - V'(χ)`. -/
def scalarEuler (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) : ℝ :=
  scalarBox α β χ y - deriv V (χ y)

/-- Density form of covariant stress-energy divergence `√-g ∇^μ T_{μν} = ∂_μ(√-g T^μ_ν) - ½ √-g (∂_ν g_{ab}) T^{ab}`. -/
def densityCovDivT (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (x : Coord2) (ν : Fin 2) : ℝ :=
  (∑ μ : Fin 2, pd (fun y => sqrtNegG α β y * scalarTMixed α β χ V y μ ν) x μ) -
    sqrtNegG α β x * (1 / 2 : ℝ) * ∑ a : Fin 2, ∑ b : Fin 2, dgDiag α β x ν a b * scalarTCon α β χ V x a b

private lemma scalarK_eval (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) :
    scalarK α β χ V y =
      -(1 / 2 : ℝ) * Real.exp (-2 * α y) * (pd χ y 0) ^ 2 +
        (1 / 2 : ℝ) * Real.exp (-2 * β y) * (pd χ y 1) ^ 2 + V (χ y) := by
  unfold scalarK gInvDiag
  simp only [Fin.sum_univ_two, Fin.isValue]
  ring

private lemma exp_sub_two_a (α β : Coord2 → ℝ) (y : Coord2) :
    Real.exp (α y + β y) * Real.exp (-2 * α y) = Real.exp (-α y + β y) := by
  rw [← Real.exp_add]; ring_nf

private lemma exp_sub_two_b (α β : Coord2 → ℝ) (y : Coord2) :
    Real.exp (α y + β y) * Real.exp (-2 * β y) = Real.exp (α y - β y) := by
  rw [← Real.exp_add]; ring_nf

private lemma scalarTMixed_00 (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) :
    sqrtNegG α β y * scalarTMixed α β χ V y 0 0 =
      -(1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 -
        (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2 -
        Real.exp (α y + β y) * V (χ y) := by
  unfold scalarTMixed scalarTDown sqrtNegG
  simp only [Fin.sum_univ_two, gInvDiag, gDiag, Fin.isValue]
  rw [scalarK_eval]
  have eα : Real.exp (-2 * α y) * Real.exp (2 * α y) = 1 := by
    rw [← Real.exp_add]; simp
  calc
    Real.exp (α y + β y) *
        (-Real.exp (-2 * α y) *
            (pd χ y 0 * pd χ y 0 -
              -Real.exp (2 * α y) *
                (-(1 / 2 : ℝ) * Real.exp (-2 * α y) * (pd χ y 0) ^ 2 +
                  (1 / 2 : ℝ) * Real.exp (-2 * β y) * (pd χ y 1) ^ 2 + V (χ y))) +
          0 * (pd χ y 1 * pd χ y 0 - 0 * _))
        = -(Real.exp (α y + β y) * Real.exp (-2 * α y)) * (pd χ y 0) ^ 2 -
            Real.exp (α y + β y) * (Real.exp (-2 * α y) * Real.exp (2 * α y)) *
              (-(1 / 2 : ℝ) * Real.exp (-2 * α y) * (pd χ y 0) ^ 2 +
                (1 / 2 : ℝ) * Real.exp (-2 * β y) * (pd χ y 1) ^ 2 + V (χ y)) := by ring
    _ = -(Real.exp (α y + β y) * Real.exp (-2 * α y)) * (pd χ y 0) ^ 2 +
            (1 / 2 : ℝ) * (Real.exp (α y + β y) * Real.exp (-2 * α y)) * (pd χ y 0) ^ 2 -
            (1 / 2 : ℝ) * (Real.exp (α y + β y) * Real.exp (-2 * β y)) * (pd χ y 1) ^ 2 -
            Real.exp (α y + β y) * V (χ y) := by
          rw [eα]; ring
    _ = -(1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 -
          (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2 -
          Real.exp (α y + β y) * V (χ y) := by
          rw [exp_sub_two_a α β y, exp_sub_two_b α β y]; ring

private lemma scalarTMixed_10 (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) :
    sqrtNegG α β y * scalarTMixed α β χ V y 1 0 =
      Real.exp (α y - β y) * (pd χ y 0 * pd χ y 1) := by
  unfold scalarTMixed scalarTDown sqrtNegG
  simp only [Fin.sum_univ_two, gInvDiag, gDiag, Fin.isValue]
  calc
    Real.exp (α y + β y) *
        (0 * (pd χ y 0 * pd χ y 0 - -Real.exp (2 * α y) * scalarK α β χ V y) +
          Real.exp (-2 * β y) * (pd χ y 1 * pd χ y 0 - 0 * scalarK α β χ V y))
        = (Real.exp (α y + β y) * Real.exp (-2 * β y)) * (pd χ y 0 * pd χ y 1) := by ring
    _ = Real.exp (α y - β y) * (pd χ y 0 * pd χ y 1) := by rw [exp_sub_two_b α β y]

private lemma scalarTMixed_01 (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) :
    sqrtNegG α β y * scalarTMixed α β χ V y 0 1 =
      -Real.exp (-α y + β y) * (pd χ y 0 * pd χ y 1) := by
  unfold scalarTMixed scalarTDown sqrtNegG
  simp only [Fin.sum_univ_two, gInvDiag, gDiag, Fin.isValue]
  calc
    Real.exp (α y + β y) *
        (-Real.exp (-2 * α y) * (pd χ y 0 * pd χ y 1 - 0 * scalarK α β χ V y) +
          0 * (pd χ y 1 * pd χ y 1 - Real.exp (2 * β y) * scalarK α β χ V y))
        = -(Real.exp (α y + β y) * Real.exp (-2 * α y)) * (pd χ y 0 * pd χ y 1) := by ring
    _ = -Real.exp (-α y + β y) * (pd χ y 0 * pd χ y 1) := by rw [exp_sub_two_a α β y]

private lemma scalarTMixed_11 (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (y : Coord2) :
    sqrtNegG α β y * scalarTMixed α β χ V y 1 1 =
      (1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 +
        (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2 -
        Real.exp (α y + β y) * V (χ y) := by
  unfold scalarTMixed scalarTDown sqrtNegG
  simp only [Fin.sum_univ_two, gInvDiag, gDiag, Fin.isValue]
  rw [scalarK_eval]
  have eβ : Real.exp (-2 * β y) * Real.exp (2 * β y) = 1 := by
    rw [← Real.exp_add]; simp
  calc
    Real.exp (α y + β y) *
        (0 * (pd χ y 0 * pd χ y 1 - 0 * _) +
          Real.exp (-2 * β y) *
            (pd χ y 1 * pd χ y 1 -
              Real.exp (2 * β y) *
                (-(1 / 2 : ℝ) * Real.exp (-2 * α y) * (pd χ y 0) ^ 2 +
                  (1 / 2 : ℝ) * Real.exp (-2 * β y) * (pd χ y 1) ^ 2 + V (χ y))))
        = (Real.exp (α y + β y) * Real.exp (-2 * β y)) * (pd χ y 1) ^ 2 -
            Real.exp (α y + β y) * (Real.exp (-2 * β y) * Real.exp (2 * β y)) *
              (-(1 / 2 : ℝ) * Real.exp (-2 * α y) * (pd χ y 0) ^ 2 +
                (1 / 2 : ℝ) * Real.exp (-2 * β y) * (pd χ y 1) ^ 2 + V (χ y)) := by ring
    _ = (Real.exp (α y + β y) * Real.exp (-2 * β y)) * (pd χ y 1) ^ 2 +
            (1 / 2 : ℝ) * (Real.exp (α y + β y) * Real.exp (-2 * α y)) * (pd χ y 0) ^ 2 -
            (1 / 2 : ℝ) * (Real.exp (α y + β y) * Real.exp (-2 * β y)) * (pd χ y 1) ^ 2 -
            Real.exp (α y + β y) * V (χ y) := by
          rw [eβ]; ring
    _ = (1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 +
          (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2 -
          Real.exp (α y + β y) * V (χ y) := by
          rw [exp_sub_two_a α β y, exp_sub_two_b α β y]; ring

private lemma dgDiag_dot_scalarTCon (α β χ : Coord2 → ℝ) (V : ℝ → ℝ) (x : Coord2)
    (hα : DifferentiableAt ℝ α x) (hβ : DifferentiableAt ℝ β x) (ν : Fin 2) :
    sqrtNegG α β x * (1 / 2 : ℝ) *
        ∑ a : Fin 2, ∑ b : Fin 2, dgDiag α β x ν a b * scalarTCon α β χ V x a b =
      pd α x ν * (sqrtNegG α β x * scalarTMixed α β χ V x 0 0) +
        pd β x ν * (sqrtNegG α β x * scalarTMixed α β χ V x 1 1) := by
  have eα : Real.exp (2 * α x) * Real.exp (-2 * α x) = 1 := by
    rw [← Real.exp_add]; simp
  have eβ : Real.exp (2 * β x) * Real.exp (-2 * β x) = 1 := by
    rw [← Real.exp_add]; simp
  simp only [Fin.sum_univ_two, Fin.isValue]
  rw [dgDiag_00 α β hα ν, dgDiag_01 α β x ν, dgDiag_10 α β x ν, dgDiag_11 α β hβ ν]
  have hT00 : scalarTCon α β χ V x 0 0 = scalarTMixed α β χ V x 0 0 * (-Real.exp (-2 * α x)) := by
    unfold scalarTCon gInvDiag
    simp only [Fin.sum_univ_two, Fin.isValue]
    ring
  have hT11 : scalarTCon α β χ V x 1 1 = scalarTMixed α β χ V x 1 1 * Real.exp (-2 * β x) := by
    unfold scalarTCon gInvDiag
    simp only [Fin.sum_univ_two, Fin.isValue]
    ring
  rw [hT00, hT11]
  calc
    sqrtNegG α β x * (1 / 2 : ℝ) *
        (-2 * Real.exp (2 * α x) * pd α x ν * (scalarTMixed α β χ V x 0 0 * (-Real.exp (-2 * α x))) +
          0 * scalarTCon α β χ V x 0 1 +
          (0 * scalarTCon α β χ V x 1 0 +
            2 * Real.exp (2 * β x) * pd β x ν * (scalarTMixed α β χ V x 1 1 * Real.exp (-2 * β x))))
        = (Real.exp (2 * α x) * Real.exp (-2 * α x)) * pd α x ν *
            (sqrtNegG α β x * scalarTMixed α β χ V x 0 0) +
          (Real.exp (2 * β x) * Real.exp (-2 * β x)) * pd β x ν *
            (sqrtNegG α β x * scalarTMixed α β χ V x 1 1) := by ring
    _ = pd α x ν * (sqrtNegG α β x * scalarTMixed α β χ V x 0 0) +
          pd β x ν * (sqrtNegG α β x * scalarTMixed α β χ V x 1 1) := by
          rw [eα, eβ]; ring

private lemma pd_half_exp_sq (h : Coord2 → ℝ) (q : Coord2 → ℝ) {x : Coord2}
    (hh : DifferentiableAt ℝ h x) (hq : DifferentiableAt ℝ q x) (μ : Fin 2) :
    pd (fun y => (1 / 2 : ℝ) * Real.exp (h y) * (q y) ^ 2) x μ =
      (1 / 2 : ℝ) * Real.exp (h x) * pd h x μ * (q x) ^ 2 +
        Real.exp (h x) * q x * pd q x μ := by
  have h1 : DifferentiableAt ℝ (fun y => (1 / 2 : ℝ) * Real.exp (h y)) x := hh.exp.const_mul _
  have h2 : DifferentiableAt ℝ (fun y => (q y) ^ 2) x := hq.pow 2
  have hpow : pd (fun y => (q y) ^ 2) x μ = 2 * q x * pd q x μ := by
    have hq2 : (fun y => (q y) ^ 2) = (fun y => q y * q y) := funext fun y => sq (q y)
    rw [hq2, pd_mul hq hq]
    ring
  rw [pd_mul h1 h2, pd_const_mul hh.exp, pd_exp hh, hpow]
  ring

private lemma pd_neg_half_exp_sq (h : Coord2 → ℝ) (q : Coord2 → ℝ) {x : Coord2}
    (hh : DifferentiableAt ℝ h x) (hq : DifferentiableAt ℝ q x) (μ : Fin 2) :
    pd (fun y => -(1 / 2 : ℝ) * Real.exp (h y) * (q y) ^ 2) x μ =
      -(1 / 2 : ℝ) * Real.exp (h x) * pd h x μ * (q x) ^ 2 -
        Real.exp (h x) * q x * pd q x μ := by
  have h1 : (fun y => -(1 / 2 : ℝ) * Real.exp (h y) * (q y) ^ 2) =
      fun y => -((1 / 2 : ℝ) * Real.exp (h y) * (q y) ^ 2) := funext fun y => by ring
  have hdiff : DifferentiableAt ℝ (fun y => (1 / 2 : ℝ) * Real.exp (h y) * (q y) ^ 2) x :=
    (hh.exp.const_mul _).mul (hq.pow 2)
  rw [h1, pd_neg hdiff, pd_half_exp_sq h q hh hq μ]
  ring

private lemma pd_exp_mul_pair (h p q : Coord2 → ℝ) {x : Coord2}
    (hh : DifferentiableAt ℝ h x) (hp : DifferentiableAt ℝ p x) (hq : DifferentiableAt ℝ q x)
    (μ : Fin 2) :
    pd (fun y => Real.exp (h y) * (p y * q y)) x μ =
      Real.exp (h x) * (pd h x μ * p x * q x + pd p x μ * q x + p x * pd q x μ) := by
  have he : DifferentiableAt ℝ (fun y => Real.exp (h y)) x := hh.exp
  have hpq : DifferentiableAt ℝ (fun y => p y * q y) x := hp.mul hq
  rw [pd_mul he hpq, pd_exp hh, pd_mul hp hq]
  ring

private lemma scalarBox_mul_sqrtNegG (α β χ : Coord2 → ℝ) (hα : Differentiable ℝ α)
    (hβ : Differentiable ℝ β) (hχ : ContDiff ℝ 2 χ) (x : Coord2) :
    sqrtNegG α β x * scalarBox α β χ x =
      -Real.exp (-α x + β x) * ((-pd α x 0 + pd β x 0) * pd χ x 0 + pd (fun y => pd χ y 0) x 0) +
        Real.exp (α x - β x) * ((pd α x 1 - pd β x 1) * pd χ x 1 + pd (fun y => pd χ y 1) x 1) := by
  have hpos : sqrtNegG α β x ≠ 0 := (Real.exp_pos _).ne'
  unfold scalarBox
  rw [mul_div_cancel₀ _ hpos, Fin.sum_univ_two]
  have hf0 : (fun z => sqrtNegG α β z * ∑ σ : Fin 2, gInvDiag α β z 0 σ * pd χ z σ) =
      fun z => -Real.exp (-α z + β z) * pd χ z 0 := by
    funext z
    unfold sqrtNegG gInvDiag
    simp only [Fin.sum_univ_two, Fin.isValue]
    rw [← exp_sub_two_a α β z]
    ring
  have hf1 : (fun z => sqrtNegG α β z * ∑ σ : Fin 2, gInvDiag α β z 1 σ * pd χ z σ) =
      fun z => Real.exp (α z - β z) * pd χ z 1 := by
    funext z
    unfold sqrtNegG gInvDiag
    simp only [Fin.sum_univ_two, Fin.isValue]
    rw [← exp_sub_two_b α β z]
    ring
  rw [hf0, hf1]
  have hm : (fun z => -Real.exp (-α z + β z) * pd χ z 0) =
      fun z => -(Real.exp (-α z + β z) * pd χ z 0) := funext fun z => by ring
  have h1ab : DifferentiableAt ℝ (fun y => -α y + β y) x := (hα x).neg.add (hβ x)
  have h2ab : DifferentiableAt ℝ (fun y => α y - β y) x := (hα x).sub (hβ x)
  have hχ0 := pd_differentiableAt hχ x 0
  have hχ1 := pd_differentiableAt hχ x 1
  have he1 : DifferentiableAt ℝ (fun y => Real.exp (-α y + β y)) x := h1ab.exp
  have he2 : DifferentiableAt ℝ (fun y => Real.exp (α y - β y)) x := h2ab.exp
  have he1χ : DifferentiableAt ℝ (fun y => Real.exp (-α y + β y) * pd χ y 0) x := he1.mul hχ0
  rw [hm, pd_neg he1χ, pd_mul he1 hχ0, pd_mul he2 hχ1,
    pd_exp h1ab, pd_exp h2ab, pd_neg_add (hα x) (hβ x), pd_sub (hα x) (hβ x)]
  ring

/-- **Curved-Spacetime Scalar Matter Conservation Identity (`#217` Obligation 4 / C2, `fderiv` Proof):**
For ANY smooth 1+1D curved diagonal metric `g = diag(-e^{2α(x)}, e^{2β(x)})` with differentiable
`α, β`, any `C^2` scalar matter field `χ : Coord2 → ℝ`, and any differentiable potential `V : ℝ → ℝ`,
`√-g ∇^μ T_{μν} = √-g E_χ ∂_ν χ` holds identically for both `ν ∈ {0, 1}`. -/
theorem scalar_matter_divergence_eq_euler_2d (α β χ : Coord2 → ℝ) (V : ℝ → ℝ)
    (hα : Differentiable ℝ α) (hβ : Differentiable ℝ β) (hχ : ContDiff ℝ 2 χ)
    (hV : Differentiable ℝ V) (x : Coord2) (ν : Fin 2) :
    densityCovDivT α β χ V x ν = sqrtNegG α β x * scalarEuler α β χ V x * pd χ x ν := by
  have hχd : Differentiable ℝ χ := hχ.differentiable (by norm_num)
  have hχ0 := fun z => pd_differentiableAt hχ z 0
  have hχ1 := fun z => pd_differentiableAt hχ z 1
  have hm_ab : DifferentiableAt ℝ (fun y => -α y + β y) x := (hα x).neg.add (hβ x)
  have hp_ab : DifferentiableAt ℝ (fun y => α y - β y) x := (hα x).sub (hβ x)
  have h_ab : DifferentiableAt ℝ (fun y => α y + β y) x := (hα x).add (hβ x)
  have hVχ : DifferentiableAt ℝ (fun y => V (χ y)) x := (hV (χ x)).comp x (hχd x)
  have hcomm := pd_comm hχ x 1 0
  have hbox := scalarBox_mul_sqrtNegG α β χ hα hβ hχ x
  unfold densityCovDivT scalarEuler
  rw [Fin.sum_univ_two, dgDiag_dot_scalarTCon α β χ V x (hα x) (hβ x) ν]
  have hrhs :
      sqrtNegG α β x * (scalarBox α β χ x - deriv V (χ x)) * pd χ x ν =
        (sqrtNegG α β x * scalarBox α β χ x - Real.exp (α x + β x) * deriv V (χ x)) * pd χ x ν := by
    unfold sqrtNegG
    ring
  rw [hrhs, hbox]
  rcases fin2_eq ν with rfl | rfl
  · have hm00 : (fun y => sqrtNegG α β y * scalarTMixed α β χ V y 0 0) =
        fun y =>
          -(1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 -
            (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2 -
            Real.exp (α y + β y) * V (χ y) := funext fun y => scalarTMixed_00 α β χ V y
    have hm10 : (fun y => sqrtNegG α β y * scalarTMixed α β χ V y 1 0) =
        fun y => Real.exp (α y - β y) * (pd χ y 0 * pd χ y 1) :=
      funext fun y => scalarTMixed_10 α β χ V y
    rw [hm00, hm10, scalarTMixed_00 α β χ V x, scalarTMixed_11 α β χ V x]
    have ht1 : DifferentiableAt ℝ (fun y => -(1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2) x :=
      ((hm_ab.exp.const_mul _)).mul ((hχ0 x).pow 2)
    have ht2 : DifferentiableAt ℝ (fun y => (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2) x :=
      ((hp_ab.exp.const_mul _)).mul ((hχ1 x).pow 2)
    have ht3 : DifferentiableAt ℝ (fun y => Real.exp (α y + β y) * V (χ y)) x := h_ab.exp.mul hVχ
    have ht12 : DifferentiableAt ℝ
        (fun y => -(1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 -
          (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2) x := ht1.sub ht2
    rw [pd_sub ht12 ht3 0, pd_sub ht1 ht2 0,
      pd_neg_half_exp_sq (fun y => -α y + β y) (fun y => pd χ y 0) hm_ab (hχ0 x) 0,
      pd_half_exp_sq (fun y => α y - β y) (fun y => pd χ y 1) hp_ab (hχ1 x) 0,
      pd_mul h_ab.exp hVχ, pd_exp h_ab, pd_comp_real (hV (χ x)) (hχd x) 0,
      pd_exp_mul_pair (fun y => α y - β y) (fun y => pd χ y 0) (fun y => pd χ y 1) hp_ab (hχ0 x) (hχ1 x) 1,
      pd_neg_add (hα x) (hβ x) 0, pd_sub (hα x) (hβ x) 0,
      pd_add (hα x) (hβ x) 0, pd_sub (hα x) (hβ x) 1]
    rw [← hcomm]
    ring
  · have hm01 : (fun y => sqrtNegG α β y * scalarTMixed α β χ V y 0 1) =
        fun y => -(Real.exp (-α y + β y) * (pd χ y 0 * pd χ y 1)) := by
      funext y
      rw [scalarTMixed_01 α β χ V y]
      ring
    have hm11 : (fun y => sqrtNegG α β y * scalarTMixed α β χ V y 1 1) =
        fun y =>
          (1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 +
            (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2 -
            Real.exp (α y + β y) * V (χ y) := funext fun y => scalarTMixed_11 α β χ V y
    rw [hm01, hm11, scalarTMixed_00 α β χ V x, scalarTMixed_11 α β χ V x]
    have hm01d : DifferentiableAt ℝ (fun y => Real.exp (-α y + β y) * (pd χ y 0 * pd χ y 1)) x :=
      hm_ab.exp.mul ((hχ0 x).mul (hχ1 x))
    have ht1 : DifferentiableAt ℝ (fun y => (1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2) x :=
      ((hm_ab.exp.const_mul _)).mul ((hχ0 x).pow 2)
    have ht2 : DifferentiableAt ℝ (fun y => (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2) x :=
      ((hp_ab.exp.const_mul _)).mul ((hχ1 x).pow 2)
    have ht3 : DifferentiableAt ℝ (fun y => Real.exp (α y + β y) * V (χ y)) x := h_ab.exp.mul hVχ
    have ht12 : DifferentiableAt ℝ
        (fun y => (1 / 2 : ℝ) * Real.exp (-α y + β y) * (pd χ y 0) ^ 2 +
          (1 / 2 : ℝ) * Real.exp (α y - β y) * (pd χ y 1) ^ 2) x := ht1.add ht2
    rw [pd_neg hm01d 0,
      pd_exp_mul_pair (fun y => -α y + β y) (fun y => pd χ y 0) (fun y => pd χ y 1) hm_ab (hχ0 x) (hχ1 x) 0,
      pd_sub ht12 ht3 1, pd_add ht1 ht2 1,
      pd_half_exp_sq (fun y => -α y + β y) (fun y => pd χ y 0) hm_ab (hχ0 x) 1,
      pd_half_exp_sq (fun y => α y - β y) (fun y => pd χ y 1) hp_ab (hχ1 x) 1,
      pd_mul h_ab.exp hVχ, pd_exp h_ab, pd_comp_real (hV (χ x)) (hχd x) 1,
      pd_neg_add (hα x) (hβ x) 0, pd_neg_add (hα x) (hβ x) 1,
      pd_sub (hα x) (hβ x) 1, pd_add (hα x) (hβ x) 1]
    rw [hcomm]
    ring

/-- **On-Shell Matter Stress Conservation (`E_χ = 0 ⟹ ∇^μ T_{μν} = 0`):**
In 1+1D curved spacetime with minimally coupled scalar matter `χ`, whenever the matter field
equation `E_χ = □χ - V'(χ) = 0` holds at `x`, `densityCovDivT = 0` follows automatically. -/
theorem scalar_matter_on_shell_conserved_2d (α β χ : Coord2 → ℝ) (V : ℝ → ℝ)
    (hα : Differentiable ℝ α) (hβ : Differentiable ℝ β) (hχ : ContDiff ℝ 2 χ)
    (hV : Differentiable ℝ V) (x : Coord2) (hEOM : scalarEuler α β χ V x = 0) (ν : Fin 2) :
    densityCovDivT α β χ V x ν = 0 := by
  rw [scalar_matter_divergence_eq_euler_2d α β χ V hα hβ hχ hV x ν, hEOM]
  ring

/-! ## 6. Bridge to `AeSTVectorNoetherResidual` (PR #215 Hyperbolic Sector) -/

/-- The general `n = 2` vector-sector Noether expression `∑ μ, E_A^μ F_{νμ} - A_ν divE_A`
reproduces `ResNova.AeSTVectorNoetherResidual.noetherResidualComp` at any on-shell background,
linking the PR #215 shift `Δ𝒩_1 = 2 b R_1 ≠ 0` directly to the general identity of §2. -/
theorem hyperbolic_sector_connects_to_general_noether (B0 B1 A0 A1 divB : ℝ)
    (dA : Fin 2 → Fin 2 → ℝ) (ν : Fin 2) :
    let E_A : Fin 2 → ℝ := ![B0, B1]
    let A : Fin 2 → ℝ := ![A0, A1]
    ∑ μ : Fin 2, E_A μ * fieldStrength dA ν μ - A ν * divB =
      ResNova.AeSTVectorNoetherResidual.noetherResidualComp
        B0 B1 (fieldStrength dA ν 0) (fieldStrength dA ν 1) (A ν) divB := by
  intro E_A A
  unfold ResNova.AeSTVectorNoetherResidual.noetherResidualComp
  simp only [Fin.sum_univ_two, Fin.isValue, Matrix.cons_val_zero, Matrix.cons_val_one, E_A]

#print axioms symmetric_contract_antisym
#print axioms symmetric_contract_eq_symmetrized
#print axioms symmetrized_metric_variation_eq
#print axioms vector_noether_sector_equiv
#print axioms off_shell_variation_decomposition
#print axioms diffeo_invariance_implies_noether_identity
#print axioms diffeo_noether_on_vector_subshell
#print axioms noether_sign_flip_counterexample
#print axioms matter_conservation_from_matter_eom
#print axioms matter_conservation_from_aest_total_noether
#print axioms nonminimal_coupling_exchange_law
#print axioms metric_div_gamma_identity
#print axioms pd_comm
#print axioms gDiag_mul_gInvDiag
#print axioms density_divergence_identity_2d
#print axioms scalar_matter_divergence_eq_euler_2d
#print axioms scalar_matter_on_shell_conserved_2d
#print axioms hyperbolic_sector_connects_to_general_noether

end ResNova.AeSTDiffeomorphismNoether


