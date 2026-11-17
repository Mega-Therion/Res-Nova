import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum

/-!
# AeST Off-Shell Metric Variation, Static Spherical First Integral, and Weak-Field Condensate / Helmholtz Reduction

This module machine-checks the algebraic and structural identities derived in Safa's 2026-11-17
Block audit sequence (`BLK-1412`, `BLK-1416`, `BLK-1417`, `BLK-1418`, `BLK-1420`):

1. **Off-shell metric-variation basis conversion (`BLK-1412`, `BLK-1416`):**
   Changing independent field variables from `(g^{μν}, A_α)` to `(g^{μν}, A^α)` shifts the metric
   Euler derivative by `-E_{A(μ} A_{ν)}`, which vanishes identically on the vector shell `E_A = 0`.
2. **Static spherical reduction (`BLK-1417`):**
   For `g_{tt} = -e_Φ²`, `g_{rr} = e_Λ²`, `A_t = -e_Φ`, `A^t = e_Φ⁻¹` (`e_Φ = e^Φ`, `e_Λ = e^Λ`),
   proves the unit-norm constraint `g_{tt}(A^t)² = -1`, projector components `q_{tt} = 0`,
   `q^{rr} = e_Λ⁻²`, Maxwell invariant `F_{μν}F^{μν} = -2 e_Λ⁻² (Φ')²`, and the scalar radial
   flux decomposition.
3. **Weak-field condensate & large-gradient Helmholtz equation (`BLK-1418`):**
   Proves the parameter dictionary `f_G = λ_s/(1+λ_s) = 1/(1+β₀)`, the effective condensate
   density identity `4π Ĝ ρ_b + m² X = 4π G_N f_G (ρ_b + ρ_c)`, the tracking channel relation
   `ΔΦ̂ - λ_s Δφ = 0`, and the exact Helmholtz reduction
   `ΔΦ + (m²/f_G)(Φ - μ_c/Q₀) = 4π G_N ρ_b`.
4. **Reproducible `BLK-1420` Benchmark Point:**
   At `K_B = 1/2`, `Q₀ = 1/10`, `λ_s = 1`, `f_G/m² = 99/100`, proves `f_G = 1/2`, `m² = 50/99`,
   `m²/f_G = 100/99`, `K₂ = 1250/33 = 3750/99`, and the `δ = 1/20` RAR band bounds `(1±δ)²`.

All theorems compile with `0 sorry` and standard axioms only.
-/

noncomputable section

namespace ResNova.AeSTWeakFieldCondensate

/-! ## 1. Off-Shell Metric Variation Basis Conversion (`BLK-1412`, `BLK-1416`) -/

/-- Symmetrized outer product `E_{A(μ} A_{ν)} = (E_{Aμ} A_ν + E_{Aν} A_μ) / 2`. -/
def symVectorTerm (EA_mu EA_nu A_mu A_nu : ℝ) : ℝ :=
  (EA_mu * A_nu + EA_nu * A_mu) / 2

/-- Metric Euler derivative `(1/√-g) δS/δg^{μν}|_{A^α}` expressed in terms of
`(1/√-g) δS/δg^{μν}|_{A_α}` via the chain rule `δA_α|_{A^β} = -g_{αμ} A_ν δg^{μν}`. -/
def metricEulerFixedContra (Eg_fixedCov EA_mu EA_nu A_mu A_nu : ℝ) : ℝ :=
  Eg_fixedCov - symVectorTerm EA_mu EA_nu A_mu A_nu

/-- The conversion term is symmetric under `μ ↔ ν`. -/
theorem symVectorTerm_comm (EA_mu EA_nu A_mu A_nu : ℝ) :
    symVectorTerm EA_mu EA_nu A_mu A_nu = symVectorTerm EA_nu EA_mu A_nu A_mu := by
  unfold symVectorTerm
  ring

/-- On the vector equation of motion (`E_{Aμ} = 0` and `E_{Aν} = 0`), the fixed-`A^α` and
fixed-`A_α` metric Euler derivatives coincide identically. -/
theorem metricEuler_eq_on_vector_shell (Eg_fixedCov A_mu A_nu : ℝ) :
    metricEulerFixedContra Eg_fixedCov 0 0 A_mu A_nu = Eg_fixedCov := by
  unfold metricEulerFixedContra symVectorTerm
  ring

/-- Off-shell difference between the two metric variation conventions equals `-E_{A(μ} A_{ν)}`. -/
theorem metricEuler_off_shell_diff (Eg_fixedCov EA_mu EA_nu A_mu A_nu : ℝ) :
    metricEulerFixedContra Eg_fixedCov EA_mu EA_nu A_mu A_nu - Eg_fixedCov =
      -symVectorTerm EA_mu EA_nu A_mu A_nu := by
  unfold metricEulerFixedContra
  ring

/-! ## 2. Static Spherical Reduction Identities (`BLK-1417`) -/

/-- In static spherical coordinates `ds² = -e^{2Φ} dt² + e^{2Λ} dr² + r² dΩ²`
(with `ePhi = e^Φ ≠ 0`), `g_{tt} = -ePhi²` and `A^t = ePhi⁻¹` satisfy `g_{tt} (A^t)² = -1`. -/
theorem spherical_unit_aether_constraint {ePhi : ℝ} (hPhi : ePhi ≠ 0) :
    (-ePhi ^ 2) * (ePhi⁻¹) ^ 2 = -1 := by
  field_simp

/-- The temporal component of the orthogonal projector `q_{tt} = g_{tt} + A_t²` vanishes
identically for `g_{tt} = -ePhi²` and `A_t = -ePhi`. -/
theorem spherical_projector_tt_zero (ePhi : ℝ) :
    (-ePhi ^ 2) + (-ePhi) ^ 2 = 0 := by
  ring

/-- For `F_{rt} = -ePhi · Φ'`, `g^{rr} = eLam⁻²`, and `g^{tt} = -ePhi⁻²`, the Maxwell scalar
`F_{μν} F^{μν} = 2 g^{rr} g^{tt} F_{rt}²` simplifies to `-2 eLam⁻² (Φ')²`. -/
theorem spherical_maxwell_scalar {ePhi eLam dPhi : ℝ} (hPhi : ePhi ≠ 0) :
    2 * (eLam ^ 2)⁻¹ * (-(ePhi ^ 2)⁻¹) * (-ePhi * dPhi) ^ 2 =
      -2 * (eLam ^ 2)⁻¹ * dPhi ^ 2 := by
  field_simp

/-- The static spherical scalar-sector conserved radial flux (`BLK-1417`):
`J_r^{scalar} = 2(2 - K_B) r² e^{Φ - Λ} (Φ' - (1 + 𝒥') φ')`. -/
def sphericalScalarFlux (K_B r ePhiSubLam dPhi dphi Jp : ℝ) : ℝ :=
  2 * (2 - K_B) * r ^ 2 * ePhiSubLam * (dPhi - (1 + Jp) * dphi)

/-- Decomposition of the radial scalar flux into the `J^μ ∇_μ φ` aether-coupling piece
and the `-(1 + 𝒥') 𝒴` scalar-gradient piece (`C = 2 - K_B`). -/
theorem sphericalScalarFlux_decomp (K_B r ePhiSubLam dPhi dphi Jp : ℝ) :
    sphericalScalarFlux K_B r ePhiSubLam dPhi dphi Jp =
      2 * (2 - K_B) * r ^ 2 * ePhiSubLam * dPhi -
      2 * (2 - K_B) * (1 + Jp) * r ^ 2 * ePhiSubLam * dphi := by
  unfold sphericalScalarFlux
  ring

/-! ## 3. Weak-Field Condensate & Large-Gradient Helmholtz Reduction (`BLK-1418`) -/

/-- Tracking fraction `f_G = Ĝ / G_N = λ_s / (1 + λ_s)`. -/
def fG (lam_s : ℝ) : ℝ := lam_s / (1 + lam_s)

/-- Published parameter `β₀ = 1 / λ_s`. -/
def beta0 (lam_s : ℝ) : ℝ := 1 / lam_s

/-- Condensate mass squared `m² = 2 K₂ Q₀² / (2 - K_B)`. -/
def mSq (K2 Q0 K_B : ℝ) : ℝ := 2 * K2 * Q0 ^ 2 / (2 - K_B)

/-- Effective condensate mass density `ρ_c = m² X / (4π G_N f_G)` where `fourPiG = 4π G_N`. -/
def rhoCondensate (m_sq X fourPiG f_g : ℝ) : ℝ :=
  m_sq * X / (fourPiG * f_g)

/-- `f_G(λ_s) = 1 / (1 + β₀(λ_s))` for `λ_s ≠ 0` and `1 + λ_s ≠ 0`. -/
theorem fG_eq_inv_one_add_beta0 {lam_s : ℝ} (h0 : lam_s ≠ 0) :
    fG lam_s = 1 / (1 + beta0 lam_s) := by
  have hb : 1 + beta0 lam_s = (1 + lam_s) / lam_s := by
    unfold beta0
    field_simp
    ring
  unfold fG
  rw [hb, one_div_div]

/-- `1 / f_G(λ_s) = 1 + 1 / λ_s = 1 + β₀(λ_s)`. -/
theorem inv_fG_eq_one_add_beta0 {lam_s : ℝ} (h0 : lam_s ≠ 0) :
    1 / fG lam_s = 1 + beta0 lam_s := by
  unfold fG beta0
  field_simp
  ring

/-- The shared source `4π Ĝ ρ_b + m² X` on the RHS of both weak-field equations
equals `4π G_N f_G (ρ_b + ρ_c)`. -/
theorem weak_field_condensate_source_eq
    (fourPiG f_g rho_b m_sq X : ℝ) (hG : fourPiG ≠ 0) (hf : f_g ≠ 0) :
    (f_g * fourPiG) * rho_b + m_sq * X =
      fourPiG * f_g * (rho_b + rhoCondensate m_sq X fourPiG f_g) := by
  unfold rhoCondensate
  field_simp

/-- **Large-Gradient Tracking Harmony (`BLK-1418`):**
If `ΔΦ̂ = S` and `λ_s Δφ = S` (where `S = 4π Ĝ ρ_b + m² X`), then `ΔΦ̂ - λ_s Δφ = 0`. -/
theorem tracking_channel_harmony (lap_Phi_hat lap_varphi lam_s S : ℝ)
    (h_hat : lap_Phi_hat = S) (h_phi : lam_s * lap_varphi = S) :
    lap_Phi_hat - lam_s * lap_varphi = 0 := by
  linarith

/-- **Helmholtz Reduction in the Large-Gradient Tracking Regime (`BLK-1418`):**
Given:
- `ΔΦ̂ = f_G · (4π G_N) ρ_b + m² X`,
- `λ_s Δφ = f_G · (4π G_N) ρ_b + m² X`,
- `ΔΦ = ΔΦ̂ + Δφ`, and
- `X = μ_c / Q₀ - Φ`,
the total potential `Φ` satisfies the exact Helmholtz equation:
`ΔΦ + (m² / f_G) (Φ - μ_c / Q₀) = 4π G_N ρ_b`. -/
theorem helmholtz_equation_derived
    (lap_Phi lap_Phi_hat lap_varphi lam_s fourPiG rho_b m_sq Phi mu_c_over_Q0 : ℝ)
    (h0 : lam_s ≠ 0) (h1 : 1 + lam_s ≠ 0)
    (h_sum : lap_Phi = lap_Phi_hat + lap_varphi)
    (h_hat : lap_Phi_hat = (fG lam_s * fourPiG) * rho_b + m_sq * (mu_c_over_Q0 - Phi))
    (h_phi : lam_s * lap_varphi = (fG lam_s * fourPiG) * rho_b + m_sq * (mu_c_over_Q0 - Phi)) :
    lap_Phi + (m_sq / fG lam_s) * (Phi - mu_c_over_Q0) = fourPiG * rho_b := by
  unfold fG at h_hat h_phi ⊢
  have h_phi' : lap_varphi =
      ((lam_s / (1 + lam_s) * fourPiG) * rho_b + m_sq * (mu_c_over_Q0 - Phi)) / lam_s := by
    rw [← h_phi, mul_div_cancel_left₀ _ h0]
  rw [h_sum, h_hat, h_phi']
  field_simp
  ring

/-! ## 4. Exact Benchmark Identities (`BLK-1420`) -/

/-- At `λ_s = 1`, `f_G = 1/2` and `β₀ = 1`. -/
theorem benchmark_fG_and_beta0 : fG 1 = 1 / 2 ∧ beta0 1 = 1 := by
  unfold fG beta0
  constructor <;> norm_num

/-- At `K_B = 1/2`, `Q₀ = 1/10`, `f_G = 1/2`, and `f_G / m² = 99 / 100`,
the condensate mass squared is `m² = 50 / 99`, the Helmholtz wavenumber squared is
`m² / f_G = 100 / 99`, and the required quadratic `k`-essence coefficient is
`K₂ = 1250 / 33 = 3750 / 99 ≈ 37.878788`. -/
theorem benchmark_K2_and_mSq :
    mSq (1250 / 33) (1 / 10) (1 / 2) = 50 / 99 ∧
    (50 / 99 : ℝ) / fG 1 = 100 / 99 ∧
    (1250 / 33 : ℝ) = 3750 / 99 := by
  unfold mSq fG
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- At optimality tolerance `δ = 1/20 = 0.05`, the deep-MOND effective mass band
`M_eff / M_b ∈ [(1 - δ)², (1 + δ)²]` has exact endpoints `0.9025` and `1.1025`. -/
theorem benchmark_delta_band :
    (1 - (5 / 100 : ℝ)) ^ 2 = 9025 / 10000 ∧
    (1 + (5 / 100 : ℝ)) ^ 2 = 11025 / 10000 := by
  constructor <;> norm_num

/-! ## 5. Non-Spherical Weak-Field `curl A` Sector & Helmholtz Decomposition (`BLK-1418` / `BLK-1436` #4) -/

/-- **3D Lagrange Identity for BSZ Eq. (17) `Y`:**
With `χ² = 1 + |A|²`, the kinetic norm-square `|σ A + χ Dφ|²` differs from BSZ Eq. (17)
`Y = |A|² σ² + 2 χ σ (A · Dφ) + |Dφ|² + (A · Dφ)²` by the exact cross-product magnitude
`|A × Dφ|²`, which vanishes in spherical symmetry (`A × Dφ = 0`) and is non-negative for general
non-spherical fields. -/
theorem Y_canonical_lagrange_identity (sigma chi A1 A2 A3 D1 D2 D3 : ℝ)
    (hchi : chi ^ 2 = 1 + A1 ^ 2 + A2 ^ 2 + A3 ^ 2) :
    let Y_bsz := (A1 ^ 2 + A2 ^ 2 + A3 ^ 2) * sigma ^ 2 +
      2 * chi * sigma * (A1 * D1 + A2 * D2 + A3 * D3) +
      (D1 ^ 2 + D2 ^ 2 + D3 ^ 2) + (A1 * D1 + A2 * D2 + A3 * D3) ^ 2
    let kin_sq := (sigma * A1 + chi * D1) ^ 2 + (sigma * A2 + chi * D2) ^ 2 + (sigma * A3 + chi * D3) ^ 2
    kin_sq - Y_bsz =
      (A2 * D3 - A3 * D2) ^ 2 + (A3 * D1 - A1 * D3) ^ 2 + (A1 * D2 - A2 * D1) ^ 2 := by
  intro Y_bsz kin_sq
  dsimp only [Y_bsz, kin_sq]
  have hdiff : chi ^ 2 * (D1 ^ 2 + D2 ^ 2 + D3 ^ 2) =
      (1 + A1 ^ 2 + A2 ^ 2 + A3 ^ 2) * (D1 ^ 2 + D2 ^ 2 + D3 ^ 2) := by
    rw [hchi]
  linarith [hdiff, show
    (sigma * A1 + chi * D1) ^ 2 + (sigma * A2 + chi * D2) ^ 2 + (sigma * A3 + chi * D3) ^ 2 -
    ((A1 ^ 2 + A2 ^ 2 + A3 ^ 2) * sigma ^ 2 +
      2 * chi * sigma * (A1 * D1 + A2 * D2 + A3 * D3) +
      (D1 ^ 2 + D2 ^ 2 + D3 ^ 2) + (A1 * D1 + A2 * D2 + A3 * D3) ^ 2) =
      (chi ^ 2 * (D1 ^ 2 + D2 ^ 2 + D3 ^ 2) -
        (1 + A1 ^ 2 + A2 ^ 2 + A3 ^ 2) * (D1 ^ 2 + D2 ^ 2 + D3 ^ 2)) +
      ((A2 * D3 - A3 * D2) ^ 2 + (A3 * D1 - A1 * D3) ^ 2 + (A1 * D2 - A2 * D1) ^ 2) by ring]

/-- **Helmholtz Longitudinal Absorption & Transverse Curl Residual:**
Under `A = ∇α + A_T` (`curl A_T = curl A`, `div A_T = 0`) and `φ̃ = φ + Q₀ α`, the physical
combination `∇φ + Q₀ A` equals `∇φ̃ + Q₀ A_T`, reducing cleanly to `∇φ̃` whenever `A_T = 0`
(purely longitudinal / `curl A = 0`). -/
theorem helmholtz_longitudinal_absorption (dphi Q0 dalpha AT : ℝ) :
    dphi + Q0 * (dalpha + AT) = (dphi + Q0 * dalpha) + Q0 * AT := by
  ring

theorem helmholtz_pure_longitudinal_reduction (dphi Q0 dalpha : ℝ) :
    dphi + Q0 * (dalpha + 0) = dphi + Q0 * dalpha := by
  ring

/-- **Non-Spherical Curl-Source Obstruction (`BLK-1418` / `BLK-1436` #4):**
The curl source `∇(𝒥'(Y)) × ∇φ̃ = (2 𝒥''(Y)) (∇Y × ∇φ̃)` sourcing `∇ × (∇ × A_T)` in the
non-spherical vector equation vanishes identically in the large-gradient Helmholtz limit (`∇𝒥' = 0`),
and is strictly nonzero whenever `𝒥'' ≠ 0` and `(∇Y × ∇φ̃)₁ ≠ 0`. -/
theorem non_spherical_curl_source_const_Jp (dtp1 dtp2 dtp3 : ℝ) :
    (0 * dtp3 - 0 * dtp2) ^ 2 + (0 * dtp1 - 0 * dtp3) ^ 2 + (0 * dtp2 - 0 * dtp1) ^ 2 = 0 := by
  ring

theorem non_spherical_curl_source_obstructs_zero_AT
    {Jpp _dY1 dY2 dY3 _dtp1 dtp2 dtp3 : ℝ}
    (hJpp : Jpp ≠ 0) (hcross : dY2 * dtp3 - dY3 * dtp2 ≠ 0) :
    (2 * Jpp * dY2) * dtp3 - (2 * Jpp * dY3) * dtp2 ≠ 0 := by
  have hfac : (2 * Jpp * dY2) * dtp3 - (2 * Jpp * dY3) * dtp2 =
      2 * Jpp * (dY2 * dtp3 - dY3 * dtp2) := by ring
  rw [hfac]
  exact mul_ne_zero (mul_ne_zero (by norm_num) hJpp) hcross

#print axioms symVectorTerm_comm
#print axioms metricEuler_eq_on_vector_shell
#print axioms metricEuler_off_shell_diff
#print axioms spherical_unit_aether_constraint
#print axioms spherical_projector_tt_zero
#print axioms spherical_maxwell_scalar
#print axioms sphericalScalarFlux_decomp
#print axioms fG_eq_inv_one_add_beta0
#print axioms inv_fG_eq_one_add_beta0
#print axioms weak_field_condensate_source_eq
#print axioms tracking_channel_harmony
#print axioms helmholtz_equation_derived
#print axioms benchmark_fG_and_beta0
#print axioms benchmark_K2_and_mSq
#print axioms benchmark_delta_band
#print axioms Y_canonical_lagrange_identity
#print axioms helmholtz_longitudinal_absorption
#print axioms helmholtz_pure_longitudinal_reduction
#print axioms non_spherical_curl_source_const_Jp
#print axioms non_spherical_curl_source_obstructs_zero_AT

end ResNova.AeSTWeakFieldCondensate
