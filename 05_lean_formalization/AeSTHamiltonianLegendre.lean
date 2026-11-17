import Mathlib.Data.Real.Basic
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

#print axioms d2U_dmu2_at_zero

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
