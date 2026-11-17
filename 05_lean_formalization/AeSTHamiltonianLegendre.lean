import Mathlib.Data.Real.Basic
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

end ResNova.AeSTHamiltonianLegendre
