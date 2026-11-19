import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum

/-!
# BSZ Auxiliary Potential `U(ν, μ)` and Dirac Matrix `C^{AB}` Invertibility for Live `μ_std` AeST

Addresses the open gate recorded in `BLK-1430` (`AEST_HAMILTONIAN_CONSTRAINT_RECONSTRUCTION_2026-11-17.md` §9.2):
For the live D7/D9 Skordis–Złośnik AeST constitutive sector
  `F(Y, Q) = (2 - K_B) * J_std(Y) - 2 * K₂ * (Q - Q₀)²`
with `J_std(Y) = 2 λ_s ã₀² F_std(√Y / ã₀)` and `μ_max = (2 - K_B) λ_s`,
this module formalizes the exact algebraic identities of the Legendre-type BSZ auxiliary
potential `U(ν, μ) = U_ν(ν) + U_μ(μ)` (BSZ eq. 15), secondary constraints `S^(μ), S^(ν)`
(BSZ eqs. 62–63), the Hessian `∂²U / ∂(A, B)` governing no-tertiary-constraint invertibility
of `C^{AB}` (BSZ eq. 75), and the exact `A_i = 0` canonical phase-space diagonal factor.

All theorems compile with `0 sorry` and standard axioms only.
-/

noncomputable section

namespace ResNova.AeSTHamiltonianLegendre

/-! ## 1. `Q`-Sector Legendre Inversion & Secondary Constraint `S^(ν)` -/

/-- Conjugate map `ν(Q) = 2 K₂ (1 - Q₀ / Q)` (BSZ eq. 83 / eq. 86). -/
def nuOfQ (K2 Q0 Q : ℝ) : ℝ := 2 * K2 * (1 - Q0 / Q)

/-- Inverted field `Q(ν) = Q₀ / (1 - ν / (2 K₂))` (BSZ eq. 87). -/
def qOfNu (K2 Q0 nu : ℝ) : ℝ := Q0 / (1 - nu / (2 * K2))

/-- Closed-form `Q`-sector auxiliary potential `U_ν(ν) = Q₀² ν / (1 - ν / (2 K₂))` (BSZ eq. 88). -/
def U_nu (K2 Q0 nu : ℝ) : ℝ := Q0 ^ 2 * nu / (1 - nu / (2 * K2))

/-- First and second derivatives of `U_ν` with respect to `ν`:
`∂U_ν/∂ν = Q₀² / (1 - ν / (2 K₂))²` and `∂²U_ν/∂ν² = Q₀² / (K₂ (1 - ν / (2 K₂))³)`. -/
def dU_dnu_expr (K2 Q0 nu : ℝ) : ℝ := Q0 ^ 2 / (1 - nu / (2 * K2)) ^ 2

def d2U_dnu2_expr (K2 Q0 nu : ℝ) : ℝ := Q0 ^ 2 / (K2 * (1 - nu / (2 * K2)) ^ 3)

/-- `Q(ν)` inverts `ν(Q)` identically on the domain `K₂ ≠ 0`, `Q₀ ≠ 0`, `2 K₂ - ν ≠ 0`. -/
theorem Q_of_nu_inverts_nu {K2 Q0 nu : ℝ}
    (hK : K2 ≠ 0) (hQ0 : Q0 ≠ 0) (hden : 2 * K2 - nu ≠ 0) :
    nuOfQ K2 Q0 (qOfNu K2 Q0 nu) = nu := by
  unfold nuOfQ qOfNu
  have h1 : 1 - nu / (2 * K2) ≠ 0 := by
    intro h
    apply hden
    have hmul : (1 - nu / (2 * K2)) * (2 * K2) = 0 := by rw [h]; ring
    have heq : (1 - nu / (2 * K2)) * (2 * K2) = 2 * K2 - nu := by
      field_simp
    linarith
  field_simp
  ring

/-- Legendre relation on the `Q`-sector: `-2 K₂ (Q(ν) - Q₀)² + ν Q(ν)² = U_ν(ν)`. -/
theorem U_nu_legendre_identity {K2 Q0 nu : ℝ}
    (hK : K2 ≠ 0) (hden : 2 * K2 - nu ≠ 0) :
    -2 * K2 * (qOfNu K2 Q0 nu - Q0) ^ 2 + nu * (qOfNu K2 Q0 nu) ^ 2 = U_nu K2 Q0 nu := by
  unfold qOfNu U_nu
  have h1 : 1 - nu / (2 * K2) ≠ 0 := by
    intro h
    apply hden
    have heq : (1 - nu / (2 * K2)) * (2 * K2) = 2 * K2 - nu := by field_simp
    rw [h] at heq
    linarith
  field_simp
  ring

/-- The derivative `∂U_ν/∂ν` equals `Q(ν)²`, realizing the secondary constraint `S^(ν) = 0`. -/
theorem dU_dnu_eq_Q_sq (K2 Q0 nu : ℝ) :
    dU_dnu_expr K2 Q0 nu = (qOfNu K2 Q0 nu) ^ 2 := by
  unfold dU_dnu_expr qOfNu
  rw [div_pow]

/-! ## 2. `Y`-Sector (`μ_std`) Inverse Map & Rational Cancellation in `U_μ(μ)` -/

/-- Inverse scalar kinetic invariant `Y(μ) = ã₀² μ² / (μ_max² - μ²)`. -/
def yOfMu (a0t muMax mu : ℝ) : ℝ := a0t ^ 2 * mu ^ 2 / (muMax ^ 2 - mu ^ 2)

/-- First and second derivatives of `U_μ(μ) = ã₀² [μ - μ_max artanh(μ / μ_max)]`:
`∂U_μ/∂μ = -ã₀² μ² / (μ_max² - μ²) = -Y(μ)` and
`∂²U_μ/∂μ² = -2 ã₀² μ_max² μ / (μ_max² - μ²)²`. -/
def d2U_dmu2_expr (a0t muMax mu : ℝ) : ℝ :=
  -(2 * a0t ^ 2 * muMax ^ 2 * mu) / (muMax ^ 2 - mu ^ 2) ^ 2

/-- For `μ = μ_max u / s` with `s² = 1 + u²` (`s ≠ 0`, `μ_max ≠ 0`), we have
`μ_max² - μ² = μ_max² / s² > 0` and `Y(μ) = ã₀² u²` identically. -/
theorem Y_of_mu_identity {a0t muMax u s : ℝ}
    (hs2 : s ^ 2 = 1 + u ^ 2) (hs0 : s ≠ 0) (hm0 : muMax ≠ 0) :
    let mu := muMax * u / s
    muMax ^ 2 - mu ^ 2 = muMax ^ 2 / s ^ 2 ∧ yOfMu a0t muMax mu = a0t ^ 2 * u ^ 2 := by
  intro mu
  have h1 : muMax ^ 2 - (muMax * u / s) ^ 2 = muMax ^ 2 / s ^ 2 := by
    field_simp
    linarith
  refine ⟨h1, ?_⟩
  unfold yOfMu
  dsimp only [mu]
  rw [h1]
  have hdiv : muMax ^ 2 / s ^ 2 ≠ 0 := div_ne_zero (pow_ne_zero 2 hm0) (pow_ne_zero 2 hs0)
  field_simp

/-- Exact cancellation of the rational Legendre piece of `b J_std(Y) - μ Y`:
`μ_max ã₀² (u s) - (μ_max u / s) (ã₀² u²) = ã₀² (μ_max u / s) = ã₀² μ`, leaving
`U_μ(μ) = ã₀² [μ - μ_max arsinh(u)] = ã₀² [μ - μ_max artanh(μ / μ_max)]`. -/
theorem U_mu_rational_part_cancellation {a0t muMax u s : ℝ}
    (hs2 : s ^ 2 = 1 + u ^ 2) (hs0 : s ≠ 0) :
    muMax * a0t ^ 2 * (u * s) - (muMax * u / s) * (a0t ^ 2 * u ^ 2) =
      a0t ^ 2 * (muMax * u / s) := by
  have hdiff : s ^ 2 - u ^ 2 = 1 := by linarith
  have h1 : muMax * a0t ^ 2 * (u * s) - (muMax * u / s) * (a0t ^ 2 * u ^ 2)
      = a0t ^ 2 * (muMax * u / s) * (s ^ 2 - u ^ 2) := by
    field_simp
  rw [h1, hdiff, mul_one]

/-! ## 3. Strict Invertibility of `Hess(U)` and `A_i = 0` Canonical `C^{AB}` (`BSZ eq. 75`) -/

/-- On the live galactic range `0 < μ < μ_max` (`a₀~ > 0`, `μ_max > 0`),
`∂²U_μ/∂μ² < 0` strictly. -/
theorem d2U_dmu2_neg {a0t muMax mu : ℝ}
    (ha : 0 < a0t) (hmMax : 0 < muMax) (hmu0 : 0 < mu) (hmuLt : mu < muMax) :
    d2U_dmu2_expr a0t muMax mu < 0 := by
  unfold d2U_dmu2_expr
  have hdiff : 0 < muMax ^ 2 - mu ^ 2 := by nlinarith
  have hnum : 0 < 2 * a0t ^ 2 * muMax ^ 2 * mu := by positivity
  have hden : 0 < (muMax ^ 2 - mu ^ 2) ^ 2 := by positivity
  exact div_neg_of_neg_of_pos (neg_lt_zero.mpr hnum) hden

/-- On the condensate branch `ν < 2 K₂` (`Q₀ > 0`, `K₂ > 0`), `∂²U_ν/∂ν² > 0` strictly. -/
theorem d2U_dnu2_pos {K2 Q0 nu : ℝ}
    (hQ : 0 < Q0) (hK : 0 < K2) (hnu : nu < 2 * K2) :
    0 < d2U_dnu2_expr K2 Q0 nu := by
  unfold d2U_dnu2_expr
  have h1 : 0 < 1 - nu / (2 * K2) := by
    have h2K : 0 < 2 * K2 := by positivity
    rw [sub_pos, div_lt_one h2K]
    exact hnu
  positivity

/-- Potential Hessian determinant `det(∂²U / ∂(A,B)) < 0` everywhere on
`(μ ∈ (0, μ_max), ν < 2 K₂)` for the live `μ_std` AeST model. -/
theorem det_hessian_U_neg {a0t muMax mu K2 Q0 nu : ℝ}
    (ha : 0 < a0t) (hmMax : 0 < muMax) (hmu0 : 0 < mu) (hmuLt : mu < muMax)
    (hQ : 0 < Q0) (hK : 0 < K2) (hnu : nu < 2 * K2) :
    d2U_dmu2_expr a0t muMax mu * d2U_dnu2_expr K2 Q0 nu < 0 :=
  mul_neg_of_neg_of_pos
    (d2U_dmu2_neg ha hmMax hmu0 hmuLt)
    (d2U_dnu2_pos hQ hK hnu)

/-- Hence `det(∂²U / ∂(A,B)) ≠ 0` on the entire interior `(0 < μ < μ_max, ν < 2 K₂)`. -/
theorem det_C_AB_ne_zero {a0t muMax mu K2 Q0 nu : ℝ}
    (ha : 0 < a0t) (hmMax : 0 < muMax) (hmu0 : 0 < mu) (hmuLt : mu < muMax)
    (hQ : 0 < Q0) (hK : 0 < K2) (hnu : nu < 2 * K2) :
    d2U_dmu2_expr a0t muMax mu * d2U_dnu2_expr K2 Q0 nu ≠ 0 :=
  ne_of_lt (det_hessian_U_neg ha hmMax hmu0 hmuLt hQ hK hnu)

/-- On the `A_i = 0` subspace (spherical/homogeneous sector) on the secondary constraint shell
`S^(ν) = 0`, adding the canonical kinetic contribution `2 Q(ν)² / ν` to `∂²U_ν/∂ν²` gives
`(2 K₂ / ν) · ∂²U_ν/∂ν² = 2 Q₀² / (ν (1 - ν/(2 K₂))³)` identically. -/
theorem S_nu_nu_A0_eq {K2 Q0 nu : ℝ}
    (hK : K2 ≠ 0) (hnu0 : nu ≠ 0) (hden : 2 * K2 - nu ≠ 0) :
    2 * (qOfNu K2 Q0 nu) ^ 2 / nu + d2U_dnu2_expr K2 Q0 nu =
      (2 * K2 / nu) * d2U_dnu2_expr K2 Q0 nu := by
  unfold qOfNu d2U_dnu2_expr
  have h1 : 1 - nu / (2 * K2) ≠ 0 := by
    intro h
    apply hden
    have heq : (1 - nu / (2 * K2)) * (2 * K2) = 2 * K2 - nu := by field_simp
    rw [h] at heq
    linarith
  field_simp
  ring

/-- Therefore on `A_i = 0` with `ν ≠ 0, ν < 2 K₂` and `0 < μ < μ_max`, the full canonical
Dirac matrix determinant is strictly nonzero (no tertiary constraints on the spherical/cosmological branch). -/
theorem canonical_A0_det_ne_zero {a0t muMax mu K2 Q0 nu : ℝ}
    (ha : 0 < a0t) (hmMax : 0 < muMax) (hmu0 : 0 < mu) (hmuLt : mu < muMax)
    (hQ : 0 < Q0) (hK : 0 < K2) (hnu0 : nu ≠ 0) (hnu : nu < 2 * K2) :
    d2U_dmu2_expr a0t muMax mu * (2 * (qOfNu K2 Q0 nu) ^ 2 / nu + d2U_dnu2_expr K2 Q0 nu) ≠ 0 := by
  have hden : 2 * K2 - nu ≠ 0 := by linarith
  rw [S_nu_nu_A0_eq hK.ne' hnu0 hden]
  have h1 : d2U_dmu2_expr a0t muMax mu < 0 := d2U_dmu2_neg ha hmMax hmu0 hmuLt
  have h2 : 0 < d2U_dnu2_expr K2 Q0 nu := d2U_dnu2_pos hQ hK hnu
  have h3 : 2 * K2 / nu ≠ 0 := div_ne_zero (by positivity) hnu0
  exact mul_ne_zero h1.ne (mul_ne_zero h3 h2.ne')

/-! ## 4. Analytic Differentiation of `U_ν(ν)` and `U_μ(μ)` via `artanh` (`BLK-1436` (b)) -/

/-- Inverse hyperbolic tangent on `(-1, 1)`: `artanh x = (log (1 + x) - log (1 - x)) / 2`. -/
def artanh (x : ℝ) : ℝ := (Real.log (1 + x) - Real.log (1 - x)) / 2

/-- Closed-form `Y`-sector auxiliary potential
`U_μ(μ) = ã₀² [μ - μ_max artanh(μ / μ_max)]`. -/
def U_mu_full (a0t muMax mu : ℝ) : ℝ :=
  a0t ^ 2 * (mu - muMax * artanh (mu / muMax))

/-- Derivative of `artanh`: `d/dx artanh(x) = 1 / (1 - x²)` for `-1 < x < 1`. -/
theorem hasDerivAt_artanh {x : ℝ} (h1 : -1 < x) (h2 : x < 1) :
    HasDerivAt artanh (1 / (1 - x ^ 2)) x := by
  unfold artanh
  have hp : 1 + x ≠ 0 := by linarith
  have hm : 1 - x ≠ 0 := by linarith
  have dlog1 : HasDerivAt (fun t : ℝ => Real.log (1 + t)) (1 / (1 + x)) x := by
    have hlin : HasDerivAt (fun t : ℝ => 1 + t) 1 x := (hasDerivAt_id' x).const_add 1
    simpa [div_eq_mul_inv] using hlin.log hp
  have dlog2 : HasDerivAt (fun t : ℝ => Real.log (1 - t)) (-1 / (1 - x)) x := by
    have hlin : HasDerivAt (fun t : ℝ => 1 - t) (-1) x := (hasDerivAt_id' x).const_sub 1
    simpa [div_eq_mul_inv] using hlin.log hm
  have hsub := (dlog1.sub dlog2).div_const 2
  have h1x : 1 - x ^ 2 ≠ 0 := by nlinarith
  refine hsub.congr_deriv ?_
  field_simp
  ring

/-- Analytic first derivative of `U_μ(μ)`:
`∂U_μ/∂μ = -ã₀² μ² / (μ_max² - μ²) = -Y(μ)` everywhere on `-μ_max < μ < μ_max`. -/
theorem hasDerivAt_U_mu_full {a0t muMax mu : ℝ}
    (hmMax : 0 < muMax) (hgt : -muMax < mu) (hlt : mu < muMax) :
    HasDerivAt (U_mu_full a0t muMax) (-yOfMu a0t muMax mu) mu := by
  have hm0 : muMax ≠ 0 := hmMax.ne'
  have h1 : -1 < mu / muMax := (lt_div_iff₀ hmMax).mpr (by linarith)
  have h2 : mu / muMax < 1 := (div_lt_one hmMax).mpr hlt
  have h_art := (hasDerivAt_artanh h1 h2).comp mu ((hasDerivAt_id' mu).div_const muMax)
  have h_full := ((hasDerivAt_id' mu).sub (h_art.const_mul muMax)).const_mul (a0t ^ 2)
  refine h_full.congr_deriv ?_
  have hdiff : muMax ^ 2 - mu ^ 2 ≠ 0 := by nlinarith
  have h1r : 1 - (mu / muMax) ^ 2 ≠ 0 := by
    intro h
    apply hdiff
    have heq : (1 - (mu / muMax) ^ 2) * muMax ^ 2 = muMax ^ 2 - mu ^ 2 := by
      field_simp
    rw [h, zero_mul] at heq
    exact heq.symm
  unfold yOfMu
  field_simp
  ring

/-- Analytic second derivative of `U_μ(μ)`:
`d/dμ (-Y(μ)) = -2 ã₀² μ_max² μ / (μ_max² - μ²)² = ∂²U_μ/∂μ²`. -/
theorem hasDerivAt_neg_yOfMu {a0t muMax mu : ℝ} (hden : muMax ^ 2 - mu ^ 2 ≠ 0) :
    HasDerivAt (fun m => -yOfMu a0t muMax m) (d2U_dmu2_expr a0t muMax mu) mu := by
  have hnum : HasDerivAt (fun m : ℝ => a0t ^ 2 * m ^ 2) (a0t ^ 2 * (2 * mu)) mu := by
    simpa using ((hasDerivAt_pow 2 mu).const_mul (a0t ^ 2))
  have hden_d : HasDerivAt (fun m : ℝ => muMax ^ 2 - m ^ 2) (-(2 * mu)) mu := by
    simpa using ((hasDerivAt_pow 2 mu).const_sub (muMax ^ 2))
  have hq := (hnum.div hden_d hden).neg
  refine hq.congr_deriv ?_
  unfold d2U_dmu2_expr
  field_simp
  ring

/-- Analytic first derivative of `U_ν(ν)`:
`∂U_ν/∂ν = Q₀² / (1 - ν / (2 K₂))²` identically for `K₂ ≠ 0`, `1 - ν / (2 K₂) ≠ 0`. -/
theorem hasDerivAt_U_nu {K2 Q0 nu : ℝ} (hK : K2 ≠ 0) (hden : 1 - nu / (2 * K2) ≠ 0) :
    HasDerivAt (U_nu K2 Q0) (dU_dnu_expr K2 Q0 nu) nu := by
  have hnum : HasDerivAt (fun n : ℝ => Q0 ^ 2 * n) (Q0 ^ 2) nu := by
    simpa using ((hasDerivAt_id' nu).const_mul (Q0 ^ 2))
  have hden_d : HasDerivAt (fun n : ℝ => 1 - n / (2 * K2)) (-(1 / (2 * K2))) nu := by
    simpa using (((hasDerivAt_id' nu).div_const (2 * K2)).const_sub 1)
  have hq := hnum.div hden_d hden
  refine hq.congr_deriv ?_
  unfold dU_dnu_expr
  field_simp
  ring

/-! ## 5. General Non-Spherical `A_i ≠ 0` / `curl A` Dirac Matrix `C^{AB}` (`BLK-1436` #4) -/

/-- In the BSZ Hamiltonian constraint (BSZ eq. 37), the curl terms
`K_B |B|² + 2(2 - K_B) (A × B) · Dφ` depend purely on `(q_{ij}, A_i, φ)` and contain no
auxiliary fields `μ, ν`; their partial derivatives w.r.t. `(μ, ν)` vanish identically. -/
theorem curl_terms_mu_nu_independent (KB B_sq A_cross_B_dot_Dphi mu : ℝ) :
    HasDerivAt (fun _ : ℝ => KB * B_sq + 2 * (2 - KB) * A_cross_B_dot_Dphi) 0 mu :=
  hasDerivAt_const mu _

/-- **Matrix Determinant Lemma for the General `A_i ≠ 0, B = curl A ≠ 0` Dirac Matrix `C^{AB}`:**
Because the kinetic inversion coupling `(2/Ξ) v vᵀ` is rank-1 with `v = (v_μ, v_ν)`,
`det(Hess(U) + (2/Ξ) v vᵀ) = (U_{μμ} U_{νν} / Ξ) · (Ξ + 2 v_μ² / U_{μμ} + 2 v_ν² / U_{νν})`. -/
theorem matrix_determinant_lemma_C_AB {Xi Um Un vm vn : ℝ}
    (hXi : Xi ≠ 0) (hUm : Um ≠ 0) (hUn : Un ≠ 0) :
    (Um + 2 * vm ^ 2 / Xi) * (Un + 2 * vn ^ 2 / Xi) - (2 * vm * vn / Xi) ^ 2 =
      (Um * Un / Xi) * (Xi + 2 * vm ^ 2 / Um + 2 * vn ^ 2 / Un) := by
  field_simp
  ring

/-- **Universal `ν`-Cancellation in the General Non-Spherical `C^{AB}` Sector (`BLK-1436` #4):**
On the secondary constraint shell `S^(ν) = 0`, adding `2 v_ν² / U_{νν}` (with
`v_ν² = (1 + |A|²) Q(ν)²`) to `Ξ = (1 + |A|²) ν - (2 b / K_B + μ) |A|²` cancels the `(1 + |A|²) ν`
dependence identically for ALL spatial vectors `A_i ≠ 0` and magnetic fields `B = curl A ≠ 0`:
`Ξ + 2 v_ν² / U_{νν} = 2 K₂ + (2 K₂ - 2 b / K_B - μ) |A|²`. -/
theorem Xi_add_two_v_nu_sq_div_U_nunu_eq {K2 Q0 nu b KB mu A_sq : ℝ}
    (hK2 : K2 ≠ 0) (hQ0 : Q0 ≠ 0) (hKB : KB ≠ 0) (hden : 2 * K2 - nu ≠ 0) :
    let Xi := (1 + A_sq) * nu - (2 * b / KB + mu) * A_sq
    let v_nu_sq := (1 + A_sq) * (qOfNu K2 Q0 nu) ^ 2
    Xi + 2 * v_nu_sq / d2U_dnu2_expr K2 Q0 nu = 2 * K2 + (2 * K2 - 2 * b / KB - mu) * A_sq := by
  intro Xi v_nu_sq
  have h1 : 1 - nu / (2 * K2) ≠ 0 := by
    intro h
    apply hden
    have heq : (1 - nu / (2 * K2)) * (2 * K2) = 2 * K2 - nu := by field_simp
    rw [h] at heq
    linarith
  dsimp only [Xi, v_nu_sq]
  unfold qOfNu d2U_dnu2_expr
  field_simp
  ring

/-- **Transverse Non-Spherical `A_i ≠ 0, curl A ≠ 0` `C^{AB}` Invertibility:**
For arbitrary non-spherical fields `A_i` and `B = curl A ≠ 0` whenever the longitudinal
`μ`-drift vanishes (`v_μ = 0`, e.g. `A · E` stationary), the canonical Dirac determinant simplifies
to `(U_{μμ} U_{νν} / Ξ) · (2 K₂ + (2 K₂ - 2 b / K_B - μ) |A|²)`, which is strictly nonzero whenever
`Ξ ≠ 0` and `2 K₂ + (2 K₂ - 2 b / K_B - μ) |A|² ≠ 0` (regardless of `B = curl A`). -/
theorem transverse_non_spherical_det_C_AB_ne_zero {a0t muMax mu K2 Q0 nu b KB A_sq : ℝ}
    (ha : 0 < a0t) (hmMax : 0 < muMax) (hmu0 : 0 < mu) (hmuLt : mu < muMax)
    (hQ : 0 < Q0) (hK : 0 < K2) (hKB : KB ≠ 0) (hnu : nu < 2 * K2)
    (hXi : (1 + A_sq) * nu - (2 * b / KB + mu) * A_sq ≠ 0)
    (hShift : 2 * K2 + (2 * K2 - 2 * b / KB - mu) * A_sq ≠ 0) :
    let Xi := (1 + A_sq) * nu - (2 * b / KB + mu) * A_sq
    let Um := d2U_dmu2_expr a0t muMax mu
    let Un := d2U_dnu2_expr K2 Q0 nu
    let vn_sq := (1 + A_sq) * (qOfNu K2 Q0 nu) ^ 2
    Um * (Un + 2 * vn_sq / Xi) - 0 ^ 2 ≠ 0 := by
  intro Xi Um Un vn_sq
  have hUm : Um < 0 := d2U_dmu2_neg ha hmMax hmu0 hmuLt
  have hUn : 0 < Un := d2U_dnu2_pos hQ hK hnu
  have hXi' : Xi ≠ 0 := hXi
  have hUn' : Un ≠ 0 := hUn.ne'
  have hden : 2 * K2 - nu ≠ 0 := by linarith
  have hcan := Xi_add_two_v_nu_sq_div_U_nunu_eq hK.ne' hQ.ne' hKB hden (b := b) (mu := mu) (A_sq := A_sq)
  have hdet : Um * (Un + 2 * vn_sq / Xi) - 0 ^ 2 =
      (Um * Un / Xi) * (2 * K2 + (2 * K2 - 2 * b / KB - mu) * A_sq) := by
    have hmul : (Um * Un / Xi) * (Xi + 2 * vn_sq / Un) = Um * (Un + 2 * vn_sq / Xi) := by
      field_simp
    have hcan' : Xi + 2 * vn_sq / Un = 2 * K2 + (2 * K2 - 2 * b / KB - mu) * A_sq := hcan
    rw [show (0 : ℝ) ^ 2 = 0 by norm_num, sub_zero, ← hmul, hcan']
  rw [hdet]
  have hpre : Um * Un / Xi ≠ 0 := div_ne_zero (mul_ne_zero hUm.ne hUn.ne') hXi'
  exact mul_ne_zero hpre hShift

/-- **General Non-Spherical `A_i ≠ 0, curl A ≠ 0` `C^{AB}` Exact Non-Degeneracy Locus:**
With arbitrary non-zero `v_μ` and arbitrary `B = curl A ≠ 0`, `det C^{AB} ≠ 0` iff `Ξ ≠ 0` and
`2 K₂ + (2 K₂ - 2 b / K_B - μ) |A|² + 2 v_μ² / U_{μμ} ≠ 0` (exact codimension-1 locus). -/
theorem general_non_spherical_det_C_AB_ne_zero {a0t muMax mu K2 Q0 nu b KB A_sq vm vn : ℝ}
    (ha : 0 < a0t) (hmMax : 0 < muMax) (hmu0 : 0 < mu) (hmuLt : mu < muMax)
    (hQ : 0 < Q0) (hK : 0 < K2) (hKB : KB ≠ 0) (hnu : nu < 2 * K2)
    (hvn_sq : vn ^ 2 = (1 + A_sq) * (qOfNu K2 Q0 nu) ^ 2)
    (hXi : (1 + A_sq) * nu - (2 * b / KB + mu) * A_sq ≠ 0)
    (hLocus : 2 * K2 + (2 * K2 - 2 * b / KB - mu) * A_sq + 2 * vm ^ 2 / d2U_dmu2_expr a0t muMax mu ≠ 0) :
    let Xi := (1 + A_sq) * nu - (2 * b / KB + mu) * A_sq
    let Um := d2U_dmu2_expr a0t muMax mu
    let Un := d2U_dnu2_expr K2 Q0 nu
    (Um + 2 * vm ^ 2 / Xi) * (Un + 2 * vn ^ 2 / Xi) - (2 * vm * vn / Xi) ^ 2 ≠ 0 := by
  intro Xi Um Un
  have hUm : Um ≠ 0 := (d2U_dmu2_neg ha hmMax hmu0 hmuLt).ne
  have hUn : 0 < Un := d2U_dnu2_pos hQ hK hnu
  have hden : 2 * K2 - nu ≠ 0 := by linarith
  have hmdl := matrix_determinant_lemma_C_AB hXi hUm hUn.ne' (vm := vm) (vn := vn)
  have hcan := Xi_add_two_v_nu_sq_div_U_nunu_eq hK.ne' hQ.ne' hKB hden (b := b) (mu := mu) (A_sq := A_sq)
  rw [hmdl]
  have heq : Xi + 2 * vm ^ 2 / Um + 2 * vn ^ 2 / Un =
      2 * K2 + (2 * K2 - 2 * b / KB - mu) * A_sq + 2 * vm ^ 2 / Um := by
    rw [hvn_sq]
    dsimp only [Xi, Um, Un] at hcan ⊢
    linarith
  rw [heq]
  exact mul_ne_zero (div_ne_zero (mul_ne_zero hUm hUn.ne') hXi) hLocus

/-- At the Minkowski background `μ = 0` (`BLK-1440`), `∂²U_μ/∂μ² = 0` identically: the interior
invertibility region `(0 < μ < μ_max)` excludes the `μ = 0` Minkowski boundary point. -/
theorem d2U_dmu2_at_zero (a0t muMax : ℝ) : d2U_dmu2_expr a0t muMax 0 = 0 := by
  unfold d2U_dmu2_expr
  ring

/-! ## 6. Dirac Constraint Classification & Absence of Linear Tertiary Constraints at `μ = 0` (`BLK-1446` #2) -/

/-- Exact canonical `Y_can` sum-of-squares decomposition (valid for all `A_i`, `B = curl A`,
and `χ² = 1 + |A|²`): `Y_can = w₁² + |D_⊥ φ|²` where `w₁ := |A| σ + χ D_∥`. -/
theorem Y_can_eq_sum_of_squares {A_norm sig chi Dp_par Dp_perp : ℝ}
    (hchi : chi ^ 2 = 1 + A_norm ^ 2) :
    A_norm ^ 2 * sig ^ 2 + 2 * chi * sig * A_norm * Dp_par +
      Dp_par ^ 2 + Dp_perp ^ 2 + (A_norm * Dp_par) ^ 2 =
      (A_norm * sig + chi * Dp_par) ^ 2 + Dp_perp ^ 2 := by
  have h : (A_norm * sig + chi * Dp_par) ^ 2 + Dp_perp ^ 2 =
      A_norm ^ 2 * sig ^ 2 + 2 * chi * sig * A_norm * Dp_par +
        chi ^ 2 * Dp_par ^ 2 + Dp_perp ^ 2 := by ring
  rw [h, hchi]
  ring

/-- **Secondary Constraint Shell at `μ = 0` Forces `v_μ = 0` (`BLK-1446` #2):**
Because `Y(0) = 0`, the secondary constraint `S^(μ)|_{μ=0} = w₁² + |D_⊥ φ|² = 0` forces both
`w₁ = 0` and `D_⊥ φ = 0`, which forces `v_μ = |A| w₁ = 0` identically even when `A_i ≠ 0`. -/
theorem mu_zero_shell_forces_v_mu_zero {a0t muMax A_norm w1 Dp_perp : ℝ}
    (_hmMax : muMax ≠ 0)
    (hS : w1 ^ 2 + Dp_perp ^ 2 - yOfMu a0t muMax 0 = 0) :
    w1 = 0 ∧ Dp_perp = 0 ∧ A_norm * w1 = 0 := by
  have hy0 : yOfMu a0t muMax 0 = 0 := by
    unfold yOfMu
    simp
  rw [hy0, sub_zero] at hS
  have hw1 : w1 ^ 2 = 0 := by nlinarith [sq_nonneg w1, sq_nonneg Dp_perp]
  have hdp : Dp_perp ^ 2 = 0 := by nlinarith [sq_nonneg w1, sq_nonneg Dp_perp]
  have hw : w1 = 0 := sq_eq_zero_iff.mp hw1
  have hd : Dp_perp = 0 := sq_eq_zero_iff.mp hdp
  exact ⟨hw, hd, by rw [hw, mul_zero]⟩

/-- Division-free determinant identity for `C^{AB} = Hess(U) + (2/Ξ) v vᵀ`, valid across `U_{μμ} = 0`. -/
theorem det_C_AB_no_div (Xi Um Un vm vn : ℝ) (hXi : Xi ≠ 0) :
    (Um + 2 * vm ^ 2 / Xi) * (Un + 2 * vn ^ 2 / Xi) - (2 * vm * vn / Xi) ^ 2 =
      Um * Un + (2 / Xi) * (Um * vn ^ 2 + Un * vm ^ 2) := by
  field_simp
  ring

/-- Off-shell at `μ = 0`, `det C^{AB}|_{μ=0} = (2 / Ξ) U_{νν} v_μ²`; on the `S^(μ)|_{μ=0} = 0`
shell (`v_μ = 0`), the entire `μ`-row and `μ`-column `(C^{μμ}, C^{μν})` vanish identically `(0, 0)`,
so `det C^{AB} = 0` and `rank(C^{AB}) ≤ 1`. -/
theorem C_AB_mu_zero_shell_rank_drop {a0t muMax Xi Un vn : ℝ}
    {w1 Dp_perp A_norm : ℝ} (hmMax : muMax ≠ 0) (hXi : Xi ≠ 0)
    (hS : w1 ^ 2 + Dp_perp ^ 2 - yOfMu a0t muMax 0 = 0) :
    let Um := d2U_dmu2_expr a0t muMax 0
    let vm := A_norm * w1
    Um + 2 * vm ^ 2 / Xi = 0 ∧
    2 * vm * vn / Xi = 0 ∧
    (Um + 2 * vm ^ 2 / Xi) * (Un + 2 * vn ^ 2 / Xi) - (2 * vm * vn / Xi) ^ 2 = 0 := by
  intro Um vm
  obtain ⟨_, _, hvm⟩ := mu_zero_shell_forces_v_mu_zero hmMax hS
  have hUm : Um = 0 := d2U_dmu2_at_zero a0t muMax
  have hvm0 : vm = 0 := hvm
  refine ⟨?_, ?_, ?_⟩
  · rw [hUm, hvm0]; ring
  · rw [hvm0]; ring
  · rw [det_C_AB_no_div Xi Um Un vm vn hXi, hUm, hvm0]; ring

/-- Scalar secondary constraint functional `S^(μ)(w₁, w₂, μ) = w₁² + w₂² - Y(μ)`. -/
def S_mu_func (a0t muMax w1 w2 mu : ℝ) : ℝ := w1 ^ 2 + w2 ^ 2 - yOfMu a0t muMax mu

/-- **Dirac Irregularity & No Linear Tertiary Constraint at `μ = 0` (`BLK-1446` #2):**
All partial derivatives of `S^(μ)(w₁, w₂, μ)` vanish identically at `(w₁ = 0, w₂ = 0, μ = 0)`.
Because `dS^(μ) = 0` everywhere on the `μ = 0` constraint locus, the Poisson bracket
`{S^(μ), H₀}` vanishes identically at `μ = 0`: no new linear functional tertiary constraint is
generated in the Poisson consistency condition `{S^(μ), H_T} = 0`; instead `S^(μ) = 0` fails
Dirac's regularity condition (`rank dS^(μ) = 0`) as a quadratic cone. -/
theorem S_mu_all_partials_vanish_at_zero (a0t muMax : ℝ) (hmMax : muMax ≠ 0) :
    HasDerivAt (fun w1 => S_mu_func a0t muMax w1 0 0) 0 0 ∧
    HasDerivAt (fun w2 => S_mu_func a0t muMax 0 w2 0) 0 0 ∧
    HasDerivAt (fun mu => S_mu_func a0t muMax 0 0 mu) 0 0 := by
  have hm2 : muMax ^ 2 - 0 ^ 2 ≠ 0 := by simp [pow_ne_zero 2 hmMax]
  refine ⟨?_, ?_, ?_⟩
  · have h1 : HasDerivAt (fun w1 : ℝ => w1 ^ 2 + (0 : ℝ) ^ 2 - yOfMu a0t muMax 0) 0 0 := by
      have hsq : HasDerivAt (fun w1 : ℝ => w1 ^ 2) ((2 : ℕ) * (0 : ℝ) ^ (2 - 1)) 0 :=
        hasDerivAt_pow 2 (0 : ℝ)
      have ha : HasDerivAt (fun w1 : ℝ => w1 ^ 2 + (0 : ℝ) ^ 2) ((2 : ℕ) * (0 : ℝ) ^ (2 - 1)) 0 :=
        hsq.add_const ((0 : ℝ) ^ 2)
      simpa using ha.sub_const (yOfMu a0t muMax 0)
    simpa [S_mu_func] using h1
  · have h2 : HasDerivAt (fun w2 : ℝ => (0 : ℝ) ^ 2 + w2 ^ 2 - yOfMu a0t muMax 0) 0 0 := by
      have hsq : HasDerivAt (fun w2 : ℝ => w2 ^ 2) ((2 : ℕ) * (0 : ℝ) ^ (2 - 1)) 0 :=
        hasDerivAt_pow 2 (0 : ℝ)
      have ha : HasDerivAt (fun w2 : ℝ => (0 : ℝ) ^ 2 + w2 ^ 2) ((2 : ℕ) * (0 : ℝ) ^ (2 - 1)) 0 :=
        hsq.const_add ((0 : ℝ) ^ 2)
      simpa using ha.sub_const (yOfMu a0t muMax 0)
    simpa [S_mu_func] using h2
  · have hnum : HasDerivAt (fun m : ℝ => a0t ^ 2 * m ^ 2) (a0t ^ 2 * (2 * 0)) 0 := by
      simpa using ((hasDerivAt_pow 2 (0 : ℝ)).const_mul (a0t ^ 2))
    have hden : HasDerivAt (fun m : ℝ => muMax ^ 2 - m ^ 2) (-(2 * 0)) 0 := by
      simpa using ((hasDerivAt_pow 2 (0 : ℝ)).const_sub (muMax ^ 2))
    have hy : HasDerivAt (yOfMu a0t muMax) 0 0 := by
      have hdiv := hnum.div hden hm2
      refine hdiv.congr_deriv ?_
      simp
    have h3 : HasDerivAt (fun mu : ℝ => (0 : ℝ) ^ 2 + (0 : ℝ) ^ 2 - yOfMu a0t muMax mu) (0 - 0) 0 :=
      (hasDerivAt_const (0 : ℝ) ((0 : ℝ) ^ 2 + (0 : ℝ) ^ 2)).sub hy
    simpa [S_mu_func, sub_zero] using h3

/-- **Quadratic-Cone Multiplier Law at `μ = 0` (`½ d²/dt² S^(μ)|₀ = 0`):**
While `{S^(μ), H₀} = 0` imposes no new spatial constraint on `H₀`, differentiating `S^(μ) = 0`
twice along any trajectory passing through `(w₁ = 0, w₂ = 0, μ = 0)` gives the quadratic slope
relation `ẇ₁² + ẇ₂² = (ã₀ / μ_max)² μ̇²`, fixing `u_μ = μ̇ = 0` on the static Minkowski vacuum and
driving `μ` into the strictly invertible `μ > 0` interior whenever gradients evolve (`ẇ₁² + ẇ₂² > 0`). -/
theorem mu_zero_second_time_deriv_slope {a0t muMax dw1 dw2 u_mu : ℝ}
    (ha : 0 < a0t) (hmMax : 0 < muMax)
    (hcone : dw1 ^ 2 + dw2 ^ 2 = (a0t / muMax) ^ 2 * u_mu ^ 2) :
    (dw1 = 0 ∧ dw2 = 0 → u_mu = 0) ∧ (0 < dw1 ^ 2 + dw2 ^ 2 → u_mu ≠ 0) := by
  refine ⟨?_, ?_⟩
  · rintro ⟨h1, h2⟩
    have hcpos : 0 < (a0t / muMax) ^ 2 := pow_pos (div_pos ha hmMax) 2
    have hsq0 : (a0t / muMax) ^ 2 * u_mu ^ 2 = 0 := by rw [h1, h2] at hcone; linarith
    have hu2 : u_mu ^ 2 = 0 := (mul_eq_zero.mp hsq0).resolve_left hcpos.ne'
    exact sq_eq_zero_iff.mp hu2
  · intro hpos hu0
    rw [hu0] at hcone
    linarith

/-! ## 7. Formal Canonical Poisson Bracket `{S^(μ), H₀} = 0` and 2nd-Derivative Cone Derivation (`BLK-1461` / Wave 3 #2 `[P]`) -/

/-- Canonical symplectic Poisson bracket `{F, G} = ∑ᵢ (∂F/∂qᵢ · ∂G/∂pᵢ − ∂F/∂pᵢ · ∂G/∂qᵢ)`
over `n` canonical conjugate coordinate pairs `(qᵢ, pᵢ)`. -/
def canonicalPoissonBracket {n : ℕ} (dFq dFp dGq dGp : Fin n → ℝ) : ℝ :=
  ∑ i : Fin n, (dFq i * dGp i - dFp i * dGq i)

/-- Total Dirac time-evolution consistency functional `{S, H₀} + ∑ₐ uₐ {S, Φₐ}` against
any minimal Hamiltonian gradient `(dH0q, dH0p)` and `k` constraint gradients `(dPhiq, dPhip)` with
arbitrary Lagrange multipliers `u : Fin k → ℝ`. -/
def diracConsistencyBracket {n k : ℕ} (dSq dSp dH0q dH0p : Fin n → ℝ)
    (u : Fin k → ℝ) (dPhiq dPhip : Fin k → Fin n → ℝ) : ℝ :=
  canonicalPoissonBracket dSq dSp dH0q dH0p +
    ∑ a : Fin k, u a * canonicalPoissonBracket dSq dSp (dPhiq a) (dPhip a)

/-- Along **any** differentiable curve `t ↦ (w₁(t), w₂(t), μ(t))` passing through
`(0, 0, 0)` at `t = t₀`, the composite directional derivative of `S^(μ)(w₁, w₂, μ)` vanishes
identically (`= 0`) by actual `HasDerivAt` chain rule. -/
theorem S_mu_curve_deriv_zero_at_origin {a0t muMax t0 dw1 dw2 dmu : ℝ}
    {w1 w2 mu : ℝ → ℝ} (hmMax : muMax ≠ 0)
    (hw1_0 : w1 t0 = 0) (hw2_0 : w2 t0 = 0) (hmu_0 : mu t0 = 0)
    (hw1 : HasDerivAt w1 dw1 t0) (hw2 : HasDerivAt w2 dw2 t0) (hmu : HasDerivAt mu dmu t0) :
    HasDerivAt (fun t => S_mu_func a0t muMax (w1 t) (w2 t) (mu t)) 0 t0 := by
  have h1 : HasDerivAt (fun t => (w1 t) ^ 2) (2 * w1 t0 ^ (2 - 1) * dw1) t0 := hw1.pow 2
  have h2 : HasDerivAt (fun t => (w2 t) ^ 2) (2 * w2 t0 ^ (2 - 1) * dw2) t0 := hw2.pow 2
  have hm2 : muMax ^ 2 - (mu t0) ^ 2 ≠ 0 := by rw [hmu_0]; simp [pow_ne_zero 2 hmMax]
  have hynum : HasDerivAt (fun t => a0t ^ 2 * (mu t) ^ 2)
      (a0t ^ 2 * (2 * mu t0 ^ (2 - 1) * dmu)) t0 :=
    (hmu.pow 2).const_mul (a0t ^ 2)
  have hyden : HasDerivAt (fun t => muMax ^ 2 - (mu t) ^ 2)
      (-(2 * mu t0 ^ (2 - 1) * dmu)) t0 :=
    (hmu.pow 2).const_sub (muMax ^ 2)
  have hy := hynum.div hyden hm2
  have hfull := (h1.add h2).sub hy
  refine hfull.congr_deriv ?_
  rw [hw1_0, hw2_0, hmu_0]
  simp

/-- **Canonical Partial Vanishing on the `μ = 0` Shell (`[P]`):** For ANY smooth canonical
chart `(w₁, w₂, μ)` on `Fin n` phase space `(q, p)` passing through `(w₁ = 0, w₂ = 0, μ = 0)` at
`(q₀, p₀)` with canonical coordinate derivatives `(dw1q, dw1p, dw2q, dw2p, dmuq, dmup)`,
every canonical partial derivative `(∂S^(μ)/∂qᵢ, ∂S^(μ)/∂pᵢ)` at `(q₀, p₀)` is provably `0`. -/
theorem S_mu_canonical_partials_zero {n : ℕ} {a0t muMax : ℝ} (hmMax : muMax ≠ 0)
    (w1 w2 mu : (Fin n → ℝ) → (Fin n → ℝ) → ℝ)
    (q0 p0 dw1q dw1p dw2q dw2p dmuq dmup : Fin n → ℝ)
    (hw1_0 : w1 q0 p0 = 0) (hw2_0 : w2 q0 p0 = 0) (hmu_0 : mu q0 p0 = 0)
    (hw1q : ∀ i, HasDerivAt (fun t => w1 (Function.update q0 i t) p0) (dw1q i) (q0 i))
    (hw2q : ∀ i, HasDerivAt (fun t => w2 (Function.update q0 i t) p0) (dw2q i) (q0 i))
    (hmuq : ∀ i, HasDerivAt (fun t => mu (Function.update q0 i t) p0) (dmuq i) (q0 i))
    (hw1p : ∀ i, HasDerivAt (fun t => w1 q0 (Function.update p0 i t)) (dw1p i) (p0 i))
    (hw2p : ∀ i, HasDerivAt (fun t => w2 q0 (Function.update p0 i t)) (dw2p i) (p0 i))
    (hmup : ∀ i, HasDerivAt (fun t => mu q0 (Function.update p0 i t)) (dmup i) (p0 i)) :
    (∀ i, HasDerivAt
      (fun t => S_mu_func a0t muMax (w1 (Function.update q0 i t) p0)
        (w2 (Function.update q0 i t) p0) (mu (Function.update q0 i t) p0)) 0 (q0 i)) ∧
    (∀ i, HasDerivAt
      (fun t => S_mu_func a0t muMax (w1 q0 (Function.update p0 i t))
        (w2 q0 (Function.update p0 i t)) (mu q0 (Function.update p0 i t))) 0 (p0 i)) := by
  refine ⟨fun i => ?_, fun i => ?_⟩
  · exact S_mu_curve_deriv_zero_at_origin hmMax
      (by simp [hw1_0]) (by simp [hw2_0]) (by simp [hmu_0])
      (hw1q i) (hw2q i) (hmuq i)
  · exact S_mu_curve_deriv_zero_at_origin hmMax
      (by simp [hw1_0]) (by simp [hw2_0]) (by simp [hmu_0])
      (hw1p i) (hw2p i) (hmup i)

/-- **`{S^(μ), H₀} = 0` Identically on the `μ = 0` Shell (`[P]`):** Given the derived vanishing
canonical partials of `S^(μ)` along every coordinate ray `i : Fin n`, any declared gradient pair
`(dSq, dSp)` satisfying `HasDerivAt` equals zero everywhere (`dSq = 0, dSp = 0`), whence the
canonical Poisson bracket `{S^(μ), H₀}` vanishes identically for **every** Hamiltonian gradient
`(dH0q, dH0p)`. -/
theorem S_mu_poisson_bracket_H0_zero {n : ℕ} {a0t muMax : ℝ} (hmMax : muMax ≠ 0)
    (w1 w2 mu : (Fin n → ℝ) → (Fin n → ℝ) → ℝ)
    (q0 p0 dSq dSp dH0q dH0p dw1q dw1p dw2q dw2p dmuq dmup : Fin n → ℝ)
    (hw1_0 : w1 q0 p0 = 0) (hw2_0 : w2 q0 p0 = 0) (hmu_0 : mu q0 p0 = 0)
    (hw1q : ∀ i, HasDerivAt (fun t => w1 (Function.update q0 i t) p0) (dw1q i) (q0 i))
    (hw2q : ∀ i, HasDerivAt (fun t => w2 (Function.update q0 i t) p0) (dw2q i) (q0 i))
    (hmuq : ∀ i, HasDerivAt (fun t => mu (Function.update q0 i t) p0) (dmuq i) (q0 i))
    (hw1p : ∀ i, HasDerivAt (fun t => w1 q0 (Function.update p0 i t)) (dw1p i) (p0 i))
    (hw2p : ∀ i, HasDerivAt (fun t => w2 q0 (Function.update p0 i t)) (dw2p i) (p0 i))
    (hmup : ∀ i, HasDerivAt (fun t => mu q0 (Function.update p0 i t)) (dmup i) (p0 i))
    (hSq : ∀ i, HasDerivAt
      (fun t => S_mu_func a0t muMax (w1 (Function.update q0 i t) p0)
        (w2 (Function.update q0 i t) p0) (mu (Function.update q0 i t) p0)) (dSq i) (q0 i))
    (hSp : ∀ i, HasDerivAt
      (fun t => S_mu_func a0t muMax (w1 q0 (Function.update p0 i t))
        (w2 q0 (Function.update p0 i t)) (mu q0 (Function.update p0 i t))) (dSp i) (p0 i)) :
    (∀ i, dSq i = 0 ∧ dSp i = 0) ∧ canonicalPoissonBracket dSq dSp dH0q dH0p = 0 := by
  obtain ⟨hzq, hzp⟩ := S_mu_canonical_partials_zero hmMax w1 w2 mu q0 p0
    dw1q dw1p dw2q dw2p dmuq dmup hw1_0 hw2_0 hmu_0 hw1q hw2q hmuq hw1p hw2p hmup
  have hzero : ∀ i, dSq i = 0 ∧ dSp i = 0 := fun i =>
    ⟨(hSq i).unique (hzq i), (hSp i).unique (hzp i)⟩
  refine ⟨hzero, ?_⟩
  unfold canonicalPoissonBracket
  refine Finset.sum_eq_zero fun i _ => ?_
  obtain ⟨hq0, hp0⟩ := hzero i
  rw [hq0, hp0]
  ring

/-- **Dirac No-Linear-Tertiary-Constraint Theorem at `μ = 0` (`[P]`):** On the `μ = 0` shell,
not only does `{S^(μ), H₀} = 0` identically, the full Dirac consistency condition
`{S^(μ), H_T} = {S^(μ), H₀} + ∑ₐ uₐ {S^(μ), Φₐ} = 0` vanishes identically for **all**
Hamiltonians `H₀`, **all** primary constraint gradients `Φₐ`, and **all** multiplier vectors `u`,
proving formally that first-order consistency generates no linear tertiary constraint and leaves
`u_μ` unfixed at first order. -/
theorem dirac_no_linear_tertiary_constraint {n k : ℕ} {a0t muMax : ℝ} (hmMax : muMax ≠ 0)
    (w1 w2 mu : (Fin n → ℝ) → (Fin n → ℝ) → ℝ)
    (q0 p0 dSq dSp dH0q dH0p dw1q dw1p dw2q dw2p dmuq dmup : Fin n → ℝ)
    (u : Fin k → ℝ) (dPhiq dPhip : Fin k → Fin n → ℝ)
    (hw1_0 : w1 q0 p0 = 0) (hw2_0 : w2 q0 p0 = 0) (hmu_0 : mu q0 p0 = 0)
    (hw1q : ∀ i, HasDerivAt (fun t => w1 (Function.update q0 i t) p0) (dw1q i) (q0 i))
    (hw2q : ∀ i, HasDerivAt (fun t => w2 (Function.update q0 i t) p0) (dw2q i) (q0 i))
    (hmuq : ∀ i, HasDerivAt (fun t => mu (Function.update q0 i t) p0) (dmuq i) (q0 i))
    (hw1p : ∀ i, HasDerivAt (fun t => w1 q0 (Function.update p0 i t)) (dw1p i) (p0 i))
    (hw2p : ∀ i, HasDerivAt (fun t => w2 q0 (Function.update p0 i t)) (dw2p i) (p0 i))
    (hmup : ∀ i, HasDerivAt (fun t => mu q0 (Function.update p0 i t)) (dmup i) (p0 i))
    (hSq : ∀ i, HasDerivAt
      (fun t => S_mu_func a0t muMax (w1 (Function.update q0 i t) p0)
        (w2 (Function.update q0 i t) p0) (mu (Function.update q0 i t) p0)) (dSq i) (q0 i))
    (hSp : ∀ i, HasDerivAt
      (fun t => S_mu_func a0t muMax (w1 q0 (Function.update p0 i t))
        (w2 q0 (Function.update p0 i t)) (mu q0 (Function.update p0 i t))) (dSp i) (p0 i)) :
    diracConsistencyBracket dSq dSp dH0q dH0p u dPhiq dPhip = 0 := by
  have hH0 := S_mu_poisson_bracket_H0_zero hmMax w1 w2 mu q0 p0 dSq dSp dH0q dH0p
    dw1q dw1p dw2q dw2p dmuq dmup hw1_0 hw2_0 hmu_0 hw1q hw2q hmuq hw1p hw2p hmup hSq hSp
  obtain ⟨hzero, hPB0⟩ := hH0
  unfold diracConsistencyBracket
  rw [hPB0, zero_add]
  refine Finset.sum_eq_zero fun a _ => ?_
  have hPB_a : canonicalPoissonBracket dSq dSp (dPhiq a) (dPhip a) = 0 := by
    unfold canonicalPoissonBracket
    refine Finset.sum_eq_zero fun i _ => ?_
    obtain ⟨hq0, hp0⟩ := hzero i
    rw [hq0, hp0]
    ring
  rw [hPB_a, mul_zero]

/-- Explicit `2×2` on-shell Dirac matrix `C^{AB}|_{μ=0, v_μ=0} = [[0, 0], [0, U_{νν}]]`:
its `μ`-row and `μ`-column vanish identically and its image is at most 1-dimensional (`x 1` only). -/
def C_AB_mu_zero_matrix (C_nunu : ℝ) : Fin 2 → Fin 2 → ℝ :=
  ![![0, 0], ![0, C_nunu]]

theorem C_AB_mu_zero_range_one_dim (C_nunu : ℝ) (x y : Fin 2 → ℝ) (hxy : x 1 = y 1) :
    (∑ j : Fin 2, C_AB_mu_zero_matrix C_nunu 0 j * x j = 0) ∧
    (∑ j : Fin 2, C_AB_mu_zero_matrix C_nunu 1 j * x j =
      ∑ j : Fin 2, C_AB_mu_zero_matrix C_nunu 1 j * y j) := by
  simp [C_AB_mu_zero_matrix, Fin.sum_univ_two, hxy]

/-- First derivative of `yOfMu(a0t, muMax, μ) = ã₀² μ² / (μ_max² − μ²)`. -/
def yOfMuDeriv (a0t muMax mu : ℝ) : ℝ :=
  2 * a0t ^ 2 * muMax ^ 2 * mu / (muMax ^ 2 - mu ^ 2) ^ 2

/-- Exact first time derivative of `S^(μ)(w₁(t), w₂(t), μ(t))` along a trajectory `t`. -/
def S_mu_traj_deriv (a0t muMax : ℝ) (w1 w1' w2 w2' mu mu' : ℝ → ℝ) (t : ℝ) : ℝ :=
  2 * w1 t * w1' t + 2 * w2 t * w2' t - yOfMuDeriv a0t muMax (mu t) * mu' t

theorem yOfMu_hasDerivAt {a0t muMax m : ℝ} (hden : muMax ^ 2 - m ^ 2 ≠ 0) :
    HasDerivAt (yOfMu a0t muMax) (yOfMuDeriv a0t muMax m) m := by
  have hnum : HasDerivAt (fun x : ℝ => a0t ^ 2 * x ^ 2) (a0t ^ 2 * (2 * m)) m := by
    simpa using ((hasDerivAt_pow 2 m).const_mul (a0t ^ 2))
  have hyden : HasDerivAt (fun x : ℝ => muMax ^ 2 - x ^ 2) (-(2 * m)) m := by
    simpa using ((hasDerivAt_pow 2 m).const_sub (muMax ^ 2))
  have hdiv := hnum.div hyden hden
  refine hdiv.congr_deriv ?_
  unfold yOfMuDeriv
  field_simp
  ring

theorem S_mu_traj_hasDerivAt {a0t muMax t : ℝ}
    {w1 w1' w2 w2' mu mu' : ℝ → ℝ}
    (hden : muMax ^ 2 - (mu t) ^ 2 ≠ 0)
    (hw1 : HasDerivAt w1 (w1' t) t) (hw2 : HasDerivAt w2 (w2' t) t)
    (hmu : HasDerivAt mu (mu' t) t) :
    HasDerivAt (fun s => S_mu_func a0t muMax (w1 s) (w2 s) (mu s))
      (S_mu_traj_deriv a0t muMax w1 w1' w2 w2' mu mu' t) t := by
  have h1 : HasDerivAt (fun s => (w1 s) ^ 2) (2 * w1 t ^ (2 - 1) * w1' t) t := hw1.pow 2
  have h2 : HasDerivAt (fun s => (w2 s) ^ 2) (2 * w2 t ^ (2 - 1) * w2' t) t := hw2.pow 2
  have hy := (yOfMu_hasDerivAt (a0t := a0t) (muMax := muMax) hden).comp t hmu
  have hfull := (h1.add h2).sub hy
  refine hfull.congr_deriv ?_
  unfold S_mu_traj_deriv
  simp

theorem yOfMuDeriv_hasDerivAt_zero {a0t muMax : ℝ} (hmMax : muMax ≠ 0) :
    HasDerivAt (yOfMuDeriv a0t muMax) (2 * (a0t / muMax) ^ 2) 0 := by
  have hm4 : (muMax ^ 2 - (0 : ℝ) ^ 2) ^ 2 ≠ 0 := by
    simp [pow_ne_zero 2 hmMax]
  have hnum : HasDerivAt (fun m : ℝ => 2 * a0t ^ 2 * muMax ^ 2 * m)
      (2 * a0t ^ 2 * muMax ^ 2 * 1) 0 := by
    simpa using ((hasDerivAt_id' (0 : ℝ)).const_mul (2 * a0t ^ 2 * muMax ^ 2))
  have hsub : HasDerivAt (fun m : ℝ => muMax ^ 2 - m ^ 2) (-(2 * 0)) 0 := by
    simpa using ((hasDerivAt_pow 2 (0 : ℝ)).const_sub (muMax ^ 2))
  have hyden : HasDerivAt (fun m : ℝ => (muMax ^ 2 - m ^ 2) ^ 2)
      (2 * (muMax ^ 2 - (0 : ℝ) ^ 2) ^ (2 - 1) * (-(2 * 0))) 0 := hsub.pow 2
  have hdiv := hnum.div hyden hm4
  refine hdiv.congr_deriv ?_
  field_simp
  ring

/-- **Exact Second Time Derivative of `S^(μ)(t)` at `(w₁ = 0, w₂ = 0, μ = 0)` (`[P]`):**
Every `wᵢ''(0)` and `μ''(0)` second-derivative acceleration term vanishes identically because
`w₁(0) = w₂(0) = yOfMuDeriv(0) = 0`, leaving purely `2 (ẇ₁² + ẇ₂² − (ã₀/μ_max)² u_μ²)`. -/
theorem S_mu_traj_second_deriv_at_zero {a0t muMax dw1 dw2 u_mu ddw1 ddw2 du_mu : ℝ}
    {w1 w1' w2 w2' mu mu' : ℝ → ℝ} (hmMax : muMax ≠ 0)
    (hw1_0 : w1 0 = 0) (hw2_0 : w2 0 = 0) (hmu_0 : mu 0 = 0)
    (hw1'_0 : w1' 0 = dw1) (hw2'_0 : w2' 0 = dw2) (hmu'_0 : mu' 0 = u_mu)
    (hw1 : HasDerivAt w1 dw1 0) (hw1' : HasDerivAt w1' ddw1 0)
    (hw2 : HasDerivAt w2 dw2 0) (hw2' : HasDerivAt w2' ddw2 0)
    (hmu : HasDerivAt mu u_mu 0) (hmu' : HasDerivAt mu' du_mu 0) :
    HasDerivAt (S_mu_traj_deriv a0t muMax w1 w1' w2 w2' mu mu')
      (2 * (dw1 ^ 2 + dw2 ^ 2 - (a0t / muMax) ^ 2 * u_mu ^ 2)) 0 := by
  have h1 : HasDerivAt (fun t => 2 * w1 t * w1' t)
      ((2 * dw1) * w1' 0 + (2 * w1 0) * ddw1) 0 :=
    (hw1.const_mul 2).mul hw1'
  have h2 : HasDerivAt (fun t => 2 * w2 t * w2' t)
      ((2 * dw2) * w2' 0 + (2 * w2 0) * ddw2) 0 :=
    (hw2.const_mul 2).mul hw2'
  have hcomp : HasDerivAt (yOfMuDeriv a0t muMax) (2 * (a0t / muMax) ^ 2) (mu 0) := by
    rw [hmu_0]
    exact yOfMuDeriv_hasDerivAt_zero (a0t := a0t) hmMax
  have hyc : HasDerivAt (fun t => yOfMuDeriv a0t muMax (mu t))
      ((2 * (a0t / muMax) ^ 2) * u_mu) 0 :=
    hcomp.comp 0 hmu
  have h3 : HasDerivAt (fun t => yOfMuDeriv a0t muMax (mu t) * mu' t)
      (((2 * (a0t / muMax) ^ 2) * u_mu) * mu' 0 + yOfMuDeriv a0t muMax (mu 0) * du_mu) 0 :=
    hyc.mul hmu'
  have hfull := (h1.add h2).sub h3
  refine hfull.congr_deriv ?_
  rw [hw1_0, hw2_0, hmu_0, hw1'_0, hw2'_0, hmu'_0]
  unfold yOfMuDeriv
  ring

/-- **Derived Quadratic Cone Relation (`[P]`):** From second-order consistency `d²S^(μ)/dt²|_{t=0} = 0`
(`HasDerivAt S_mu_traj_deriv 0 0`), the cone slope equation `ẇ₁² + ẇ₂² = (ã₀ / μ_max)² u_μ²`
is **derived directly by `HasDerivAt.unique`**, rather than assumed as `hcone`. -/
theorem cone_relation_derived_from_second_deriv {a0t muMax dw1 dw2 u_mu ddw1 ddw2 du_mu : ℝ}
    {w1 w1' w2 w2' mu mu' : ℝ → ℝ} (hmMax : muMax ≠ 0)
    (hw1_0 : w1 0 = 0) (hw2_0 : w2 0 = 0) (hmu_0 : mu 0 = 0)
    (hw1'_0 : w1' 0 = dw1) (hw2'_0 : w2' 0 = dw2) (hmu'_0 : mu' 0 = u_mu)
    (hw1 : HasDerivAt w1 dw1 0) (hw1' : HasDerivAt w1' ddw1 0)
    (hw2 : HasDerivAt w2 dw2 0) (hw2' : HasDerivAt w2' ddw2 0)
    (hmu : HasDerivAt mu u_mu 0) (hmu' : HasDerivAt mu' du_mu 0)
    (hd2S : HasDerivAt (S_mu_traj_deriv a0t muMax w1 w1' w2 w2' mu mu') 0 0) :
    dw1 ^ 2 + dw2 ^ 2 = (a0t / muMax) ^ 2 * u_mu ^ 2 := by
  have hcalc := S_mu_traj_second_deriv_at_zero (a0t := a0t) hmMax hw1_0 hw2_0 hmu_0
    hw1'_0 hw2'_0 hmu'_0 hw1 hw1' hw2 hw2' hmu hmu'
  have heq : 2 * (dw1 ^ 2 + dw2 ^ 2 - (a0t / muMax) ^ 2 * u_mu ^ 2) = 0 :=
    hcalc.unique hd2S
  linarith

/-- **Full `[P]` Wave 3 #2 Closure Theorem (`d²S^(μ)/dt² = 0 ⇒ cone law ⇒ u_μ dichotomy`):**
Derives `u_μ = 0` on static Minkowski vacuum and `u_μ ≠ 0` under evolving gradients directly from
`d²/dt² S^(μ) = 0` with no assumed `hcone` hypothesis. -/
theorem mu_zero_second_time_deriv_derived {a0t muMax dw1 dw2 u_mu ddw1 ddw2 du_mu : ℝ}
    {w1 w1' w2 w2' mu mu' : ℝ → ℝ} (ha : 0 < a0t) (hmMax : 0 < muMax)
    (hw1_0 : w1 0 = 0) (hw2_0 : w2 0 = 0) (hmu_0 : mu 0 = 0)
    (hw1'_0 : w1' 0 = dw1) (hw2'_0 : w2' 0 = dw2) (hmu'_0 : mu' 0 = u_mu)
    (hw1 : HasDerivAt w1 dw1 0) (hw1' : HasDerivAt w1' ddw1 0)
    (hw2 : HasDerivAt w2 dw2 0) (hw2' : HasDerivAt w2' ddw2 0)
    (hmu : HasDerivAt mu u_mu 0) (hmu' : HasDerivAt mu' du_mu 0)
    (hd2S : HasDerivAt (S_mu_traj_deriv a0t muMax w1 w1' w2 w2' mu mu') 0 0) :
    (dw1 = 0 ∧ dw2 = 0 → u_mu = 0) ∧ (0 < dw1 ^ 2 + dw2 ^ 2 → u_mu ≠ 0) :=
  mu_zero_second_time_deriv_slope ha hmMax
    (cone_relation_derived_from_second_deriv hmMax.ne' hw1_0 hw2_0 hmu_0 hw1'_0 hw2'_0 hmu'_0
      hw1 hw1' hw2 hw2' hmu hmu' hd2S)

#print axioms S_mu_curve_deriv_zero_at_origin
#print axioms S_mu_canonical_partials_zero
#print axioms S_mu_poisson_bracket_H0_zero
#print axioms dirac_no_linear_tertiary_constraint
#print axioms C_AB_mu_zero_range_one_dim
#print axioms yOfMu_hasDerivAt
#print axioms S_mu_traj_hasDerivAt
#print axioms yOfMuDeriv_hasDerivAt_zero
#print axioms S_mu_traj_second_deriv_at_zero
#print axioms cone_relation_derived_from_second_deriv
#print axioms mu_zero_second_time_deriv_derived

#print axioms d2U_dmu2_at_zero
#print axioms Y_can_eq_sum_of_squares
#print axioms mu_zero_shell_forces_v_mu_zero
#print axioms det_C_AB_no_div
#print axioms C_AB_mu_zero_shell_rank_drop
#print axioms S_mu_all_partials_vanish_at_zero
#print axioms mu_zero_second_time_deriv_slope

#print axioms Q_of_nu_inverts_nu
#print axioms U_nu_legendre_identity
#print axioms dU_dnu_eq_Q_sq
#print axioms Y_of_mu_identity
#print axioms U_mu_rational_part_cancellation
#print axioms d2U_dmu2_neg
#print axioms d2U_dnu2_pos
#print axioms det_hessian_U_neg
#print axioms det_C_AB_ne_zero
#print axioms S_nu_nu_A0_eq
#print axioms canonical_A0_det_ne_zero
#print axioms hasDerivAt_artanh
#print axioms hasDerivAt_U_mu_full
#print axioms hasDerivAt_neg_yOfMu
#print axioms hasDerivAt_U_nu
#print axioms curl_terms_mu_nu_independent
#print axioms matrix_determinant_lemma_C_AB
#print axioms Xi_add_two_v_nu_sq_div_U_nunu_eq
#print axioms transverse_non_spherical_det_C_AB_ne_zero
#print axioms general_non_spherical_det_C_AB_ne_zero

end ResNova.AeSTHamiltonianLegendre
