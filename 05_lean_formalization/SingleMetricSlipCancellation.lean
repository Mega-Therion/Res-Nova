import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-!
# Single-Metric AeST & Tidal-QUMOND Anisotropic-Stress Cancellation and Gravitational Slip

Adjacent Lean 4 formalization companion to `exploration/tidal_aest/single_metric_slip_audit.py`
and `exploration/tidal_aest/SINGLE_METRIC_SLIP_AUDIT.json`. Not cited by the main manuscript
(scoped in `ADJACENT_MODULES.txt`). All theorems compile with zero unfinished proof terms and
standard axioms only.

## Scope & Epistemic Boundary

* **Checked in Lean 4 (`[P]`):**
  1. Standalone deep-MOND scalar `χ` (`F(y) = (2/3) y^(3/2)`, no `J · ∇φ` mixing) `[X]`:
     equation of state `p_r = 2 ρ_χ`, `p_θ = -ρ_χ`, unique hydrostatic power law
     `ρ_χ ∝ r^(-3)`, exact `HasDerivAt` verification of the three linear Einstein equations
     giving `Φ' - Ψ' = 2 A / r²` and `O(1)` fractional slip `2 / ln(r / r₀)`.
  2. Live AeST AQUAL & Tidal-QUMOND on-shell anisotropic stress equivalence: both weak-field
     expressions reduce on shell to `-K_B (Φ')² - (2 - K_B) Φ' φ'`, and combining with the
     `O(ε²)` Einstein tensor term `2 (Φ')²` cancels `(Φ')²` identically, yielding
     `r d/dr(δ_slip' / r) = (2 - K_B) Φ' g_N` and linear-order `Ψ = Φ`.
  3. Exact `HasDerivAt` verification of the closed-form `O(v⁴/c⁴)` boundary-vanishing slip
     solutions in both the Newtonian (`δ_Newt = (1 - K_B/2) (G_N M)² / (4 r²)`, recovering
     isotropic Schwarzschild at `K_B = 0`) and deep-MOND (`δ_MOND = (2/3)(1 - K_B/2) v_c² G_N M / r`)
     regimes, together with `0 ≤ K_B ≤ 2` prefactor bounds.
* **Verified in SymPy (`single_metric_slip_audit.py`, `[D]`):** full 4D isotropic spherical
  Christoffel/Ricci/Einstein tensor expansion to `O(ε²)` and radial variation of `√(-g) ℒ`
  that produce these algebraic forms, plus empirical evaluation across the 12 X-COP clusters.
-/

noncomputable section

namespace ResNova.SingleMetricSlipCancellation

open Real

/-! ## 1. Standalone Deep-MOND Scalar χ (`[X]`) -/

/-- Effective energy density `8πG ρ_χ = χ₁³ / (3 a₀ B³)` for standalone deep-MOND scalar `χ`. -/
def rhoChi (chi1 a0 B : ℝ) : ℝ := chi1 ^ 3 / (3 * a0 * B ^ 3)

/-- Effective radial pressure `8πG p_r = 2 χ₁³ / (3 a₀ B³)`. -/
def prChi (chi1 a0 B : ℝ) : ℝ := 2 * chi1 ^ 3 / (3 * a0 * B ^ 3)

/-- Effective tangential pressure `8πG p_θ = -χ₁³ / (3 a₀ B³)`. -/
def pthetaChi (chi1 a0 B : ℝ) : ℝ := -chi1 ^ 3 / (3 * a0 * B ^ 3)

/-- Equation of state of standalone deep-MOND `χ`: `p_r = 2 ρ_χ`, `p_θ = -ρ_χ`,
and anisotropic stress `p_r - p_θ = 3 ρ_χ`. -/
theorem standalone_deep_mond_eos (chi1 a0 B : ℝ) :
    prChi chi1 a0 B = 2 * rhoChi chi1 a0 B ∧
    pthetaChi chi1 a0 B = -rhoChi chi1 a0 B ∧
    prChi chi1 a0 B - pthetaChi chi1 a0 B = 3 * rhoChi chi1 a0 B := by
  unfold rhoChi prChi pthetaChi
  refine ⟨?_, ?_, ?_⟩ <;> ring

/-- For a power-law density `ρ(r) = C r^(-α)` (`C ≠ 0`, `r > 0`) obeying `p_r = 2 ρ`,
`p_θ = -ρ`, the hydrostatic TOV equilibrium `p_r' + 2 (p_r - p_θ) / r = 0` holds iff `α = 3`. -/
theorem standalone_hydrostatic_exponent_unique {C α r : ℝ} (hC : C ≠ 0) (hr : 0 < r) :
    HasDerivAt (fun t : ℝ => 2 * C * t ^ (-α)) (-2 * α * C * r ^ (-α - 1)) r ∧
    (-2 * α * C * r ^ (-α - 1) + 2 * (3 * (C * r ^ (-α))) / r = 0 ↔ α = 3) := by
  have hd : HasDerivAt (fun t : ℝ => t ^ (-α)) ((-α) * r ^ (-α - 1)) r :=
    Real.hasDerivAt_rpow_const (Or.inl hr.ne')
  have hd_mul : HasDerivAt (fun t : ℝ => 2 * C * t ^ (-α)) ((2 * C) * ((-α) * r ^ (-α - 1))) r :=
    hd.const_mul (2 * C)
  have hd_clean : HasDerivAt (fun t : ℝ => 2 * C * t ^ (-α)) (-2 * α * C * r ^ (-α - 1)) r := by
    refine hd_mul.congr_deriv ?_
    ring
  refine ⟨hd_clean, ?_⟩
  have hr_rpow : r ^ (-α - 1) = r ^ (-α) / r := by
    rw [Real.rpow_sub hr, Real.rpow_one]
  have hpow_ne : r ^ (-α) ≠ 0 := (Real.rpow_pos_of_pos hr (-α)).ne'
  rw [hr_rpow]
  have hfac :
      -2 * α * C * (r ^ (-α) / r) + 2 * (3 * (C * r ^ (-α))) / r =
        (2 * C * r ^ (-α) / r) * (3 - α) := by
    field_simp [hr.ne']
    ring
  rw [hfac, mul_eq_zero]
  have hnonzero : 2 * C * r ^ (-α) / r ≠ 0 := by
    apply div_ne_zero
    · exact mul_ne_zero (mul_ne_zero (by norm_num) hC) hpow_ne
    · exact hr.ne'
  simp only [hnonzero, false_or]
  constructor
  · intro h; linarith
  · intro h; linarith

/-- Standalone deep-MOND radial gravitational derivative `Ψ'(r) = A ln(r/r₀) / r²`
(where `A = 4π G_N C_χ`). -/
def psiPStandalone (A r0 r : ℝ) : ℝ := A * Real.log (r / r0) / r ^ 2

/-- Standalone deep-MOND temporal gravitational derivative `Φ'(r) = Ψ'(r) + 2 A / r²`. -/
def phiPStandalone (A r0 r : ℝ) : ℝ := psiPStandalone A r0 r + 2 * A / r ^ 2

/-- Exact radial derivatives and linear Einstein equations `G^t_t = -2 A / r³`,
`G^r_r = 4 A / r³`, `G^θ_θ = -2 A / r³` for standalone deep-MOND `χ` (`r, r₀ > 0`). -/
theorem standalone_einstein_linear_solution {A r0 r : ℝ} (hr0 : 0 < r0) (hr : 0 < r) :
    let dpsi := A / r ^ 3 - 2 * A * Real.log (r / r0) / r ^ 3
    let dphi := -3 * A / r ^ 3 - 2 * A * Real.log (r / r0) / r ^ 3
    HasDerivAt (psiPStandalone A r0) dpsi r ∧
    HasDerivAt (phiPStandalone A r0) dphi r ∧
    (-2 * (dpsi + 2 * psiPStandalone A r0 r / r) = -2 * A / r ^ 3) ∧
    (2 * (phiPStandalone A r0 r - psiPStandalone A r0 r) / r = 4 * A / r ^ 3) ∧
    ((dphi - dpsi) + (phiPStandalone A r0 r - psiPStandalone A r0 r) / r = -2 * A / r ^ 3) := by
  have hlog : HasDerivAt (fun t : ℝ => Real.log (t / r0)) (r⁻¹) r := by
    have hdiv : HasDerivAt (fun t : ℝ => t / r0) (1 / r0) r := (hasDerivAt_id r).div_const r0
    have hl := hdiv.log (div_pos hr hr0).ne'
    refine hl.congr_deriv ?_
    field_simp [hr.ne', hr0.ne']
  have hnum : HasDerivAt (fun t : ℝ => A * Real.log (t / r0)) (A * r⁻¹) r := hlog.const_mul A
  have hsq : HasDerivAt (fun t : ℝ => t ^ 2) (2 * r) r := by
    simpa using hasDerivAt_pow 2 r
  have hpsi_raw := hnum.div hsq (by positivity : r ^ 2 ≠ 0)
  have hpsi : HasDerivAt (psiPStandalone A r0)
      (A / r ^ 3 - 2 * A * Real.log (r / r0) / r ^ 3) r := by
    refine hpsi_raw.congr_deriv ?_
    field_simp [hr.ne']
  have hinv2 : HasDerivAt (fun t : ℝ => 2 * A * (t ^ 2)⁻¹) ((2 * A) * (-(2 * r) / (r ^ 2) ^ 2)) r :=
    (hsq.inv (by positivity : r ^ 2 ≠ 0)).const_mul (2 * A)
  have hphi_raw := hpsi.add hinv2
  have hphi : HasDerivAt (phiPStandalone A r0)
      (-3 * A / r ^ 3 - 2 * A * Real.log (r / r0) / r ^ 3) r := by
    have hphi_eq :
        HasDerivAt (fun t : ℝ => psiPStandalone A r0 t + 2 * A * (t ^ 2)⁻¹)
          (A / r ^ 3 - 2 * A * Real.log (r / r0) / r ^ 3 + 2 * A * (-(2 * r) / (r ^ 2) ^ 2)) r :=
      hphi_raw
    have hphi_fun :
        (fun t : ℝ => psiPStandalone A r0 t + 2 * A * (t ^ 2)⁻¹) = phiPStandalone A r0 := by
      ext t
      unfold phiPStandalone
      ring
    rw [hphi_fun] at hphi_eq
    refine hphi_eq.congr_deriv ?_
    field_simp [hr.ne']
    ring
  refine ⟨hpsi, hphi, ?_, ?_, ?_⟩
  · unfold psiPStandalone
    field_simp [hr.ne']
    ring
  · unfold phiPStandalone psiPStandalone
    field_simp [hr.ne']
    ring
  · unfold phiPStandalone psiPStandalone
    field_simp [hr.ne']
    ring

/-- The linear fractional slip of standalone deep-MOND `χ` is `O(1)`:
`(Φ' - Ψ') / Ψ' = 2 / ln(r / r₀)` for `r > r₀ > 0` and `A ≠ 0`. -/
theorem standalone_linear_slip_ratio {A r0 r : ℝ} (hA : A ≠ 0) (hr0 : 0 < r0) (hgt : r0 < r) :
    (phiPStandalone A r0 r - psiPStandalone A r0 r) / psiPStandalone A r0 r =
      2 / Real.log (r / r0) := by
  have hr : 0 < r := lt_trans hr0 hgt
  have hlog_pos : 0 < Real.log (r / r0) := Real.log_pos ((one_lt_div hr0).mpr hgt)
  unfold phiPStandalone psiPStandalone
  field_simp [hA, hr.ne', hlog_pos.ne']
  ring

/-! ## 2. Live AeST AQUAL & Tidal-QUMOND On-Shell Stress & Self-Stress Cancellation -/

/-- Weak-field (`N = B = 1`) anisotropic stress `8πG̃ (T^r_r - T^θ_θ)` in live AeST AQUAL. -/
def anisoAQUAL (KB Phi1 phi1 Jp : ℝ) : ℝ :=
  -KB * Phi1 ^ 2 - 2 * (2 - KB) * Phi1 * phi1 + (2 - KB) * phi1 ^ 2 + (2 - KB) * phi1 ^ 2 * Jp

/-- Weak-field (`N = B = 1`) anisotropic stress `8πG̃ (T^r_r - T^θ_θ)` in live Tidal-QUMOND AeST. -/
def anisoQUMOND (KB Phi1 phi1 psi1 Fp : ℝ) : ℝ :=
  -KB * Phi1 ^ 2 - 2 * (2 - KB) * Phi1 * phi1 + (2 - KB) * phi1 ^ 2
    - 2 * (2 - KB) * phi1 * psi1 - (2 - KB) * psi1 ^ 2 * Fp

/-- Common on-shell anisotropic stress `-K_B (Φ')² - (2 - K_B) Φ' φ'`. -/
def anisoOnShell (KB Phi1 phi1 : ℝ) : ℝ :=
  -KB * Phi1 ^ 2 - (2 - KB) * Phi1 * phi1

/-- On shell (`𝒥' = Φ' / φ' - 1`), live AeST AQUAL anisotropic stress equals `anisoOnShell`. -/
theorem aqual_on_shell_aniso {KB Phi1 phi1 Jp : ℝ}
    (hphi : phi1 ≠ 0) (hJ : Jp = Phi1 / phi1 - 1) :
    anisoAQUAL KB Phi1 phi1 Jp = anisoOnShell KB Phi1 phi1 := by
  rw [hJ]
  unfold anisoAQUAL anisoOnShell
  field_simp [hphi]
  ring

/-- On shell (`ℱ' = φ' / g_N`, `ψ' = -g_N`, `Φ' = g_N + φ'`), live Tidal-QUMOND anisotropic
stress identically equals `anisoOnShell`. -/
theorem qumond_on_shell_aniso {KB Phi1 phi1 psi1 gN Fp : ℝ}
    (_hg : gN ≠ 0) (hF : Fp = phi1 / gN) (hpsi : psi1 = -gN) (hPhi : Phi1 = gN + phi1) :
    anisoQUMOND KB Phi1 phi1 psi1 Fp = anisoOnShell KB Phi1 phi1 := by
  rw [hF, hpsi, hPhi]
  unfold anisoQUMOND anisoOnShell
  field_simp [_hg]
  ring

/-- **Exact `(Φ')²` Self-Stress Cancellation:** Combining the `O(ε²)` Einstein tensor term
`2 (Φ')²` (`Ψ = Φ` at `O(ε)`) with `8πG̃ (T^r_r - T^θ_θ)` and `φ' = Φ' - g_N` cancels `(Φ')²`
identically, leaving `(2 - K_B) Φ' g_N` (vanishing when `K_B = 2` or in vacuum `g_N = 0`). -/
theorem aest_self_stress_cancellation (KB Phi1 gN : ℝ) :
    2 * Phi1 ^ 2 + anisoOnShell KB Phi1 (Phi1 - gN) = (2 - KB) * Phi1 * gN := by
  unfold anisoOnShell
  ring

/-! ## 3. Exact `O(v⁴/c⁴)` Gravitational Slip Solutions (`HasDerivAt`) -/

/-- Closed-form Newtonian-regime `O(v⁴/c⁴)` slip `δ_slip(r) = (1 - K_B/2) G_N² M² / (4 r²)`. -/
def deltaNewt (KB GN M r : ℝ) : ℝ := (1 - KB / 2) * (GN * M) ^ 2 / (4 * r ^ 2)

/-- Closed-form deep-MOND `O(v⁴/c⁴)` slip `δ_slip(r) = (2/3)(1 - K_B/2) v_c² G_N M / r`. -/
def deltaMond (KB vc GN M r : ℝ) : ℝ := (2 / 3) * (1 - KB / 2) * vc ^ 2 * GN * M / r

/-- `deltaNewt` satisfies the exact `O(ε²)` slip ODE `r d/dr(δ' / r) = (2 - K_B) (G_N M / r²)²`
for every `r ≠ 0`, and recovers isotropic Schwarzschild `(G_N M)² / (4 r²)` at `K_B = 0`. -/
theorem deltaNewt_slip_ode {KB GN M r : ℝ} (hr : r ≠ 0) :
    let d1 := -(1 - KB / 2) * (GN * M) ^ 2 / (2 * r ^ 3)
    HasDerivAt (deltaNewt KB GN M) d1 r ∧
    HasDerivAt (fun x : ℝ => (-(1 - KB / 2) * (GN * M) ^ 2 / (2 * x ^ 3)) / x)
      (2 * (1 - KB / 2) * (GN * M) ^ 2 / r ^ 5) r ∧
    r * (2 * (1 - KB / 2) * (GN * M) ^ 2 / r ^ 5) = (2 - KB) * (GN * M / r ^ 2) ^ 2 ∧
    deltaNewt 0 GN M r = (GN * M) ^ 2 / (4 * r ^ 2) := by
  have h1 : HasDerivAt (fun x : ℝ => (4 * x ^ 2)⁻¹) (-(8 * r) / (4 * r ^ 2) ^ 2) r := by
    have hpow : HasDerivAt (fun x : ℝ => x ^ 2) (2 * r) r := by
      simpa using hasDerivAt_pow 2 r
    have hmul : HasDerivAt (fun x : ℝ => 4 * x ^ 2) (4 * (2 * r)) r := hpow.const_mul 4
    have hinv := hmul.inv (by positivity : 4 * r ^ 2 ≠ 0)
    refine hinv.congr_deriv ?_
    ring
  have hd1 : HasDerivAt (deltaNewt KB GN M) (-(1 - KB / 2) * (GN * M) ^ 2 / (2 * r ^ 3)) r := by
    have hfun :
        (fun x : ℝ => ((1 - KB / 2) * (GN * M) ^ 2) * (4 * x ^ 2)⁻¹) = deltaNewt KB GN M := by
      ext x
      unfold deltaNewt
      ring
    have hm := h1.const_mul ((1 - KB / 2) * (GN * M) ^ 2)
    rw [hfun] at hm
    refine hm.congr_deriv ?_
    field_simp [hr]
    ring
  have h2 : HasDerivAt (fun x : ℝ => (2 * x ^ 4)⁻¹) (-(8 * r ^ 3) / (2 * r ^ 4) ^ 2) r := by
    have hpow4 : HasDerivAt (fun x : ℝ => x ^ 4) (4 * r ^ 3) r := by
      simpa using hasDerivAt_pow 4 r
    have hmul4 : HasDerivAt (fun x : ℝ => 2 * x ^ 4) (2 * (4 * r ^ 3)) r := hpow4.const_mul 2
    have hinv4 := hmul4.inv (by positivity : 2 * r ^ 4 ≠ 0)
    refine hinv4.congr_deriv ?_
    ring
  have hd2 : HasDerivAt (fun x : ℝ => (-(1 - KB / 2) * (GN * M) ^ 2 / (2 * x ^ 3)) / x)
      (2 * (1 - KB / 2) * (GN * M) ^ 2 / r ^ 5) r := by
    have hfun2 :
        (fun x : ℝ => (-(1 - KB / 2) * (GN * M) ^ 2) * (2 * x ^ 4)⁻¹) =
          (fun x : ℝ => (-(1 - KB / 2) * (GN * M) ^ 2 / (2 * x ^ 3)) / x) := by
      ext x
      ring
    have hm2 := h2.const_mul (-(1 - KB / 2) * (GN * M) ^ 2)
    rw [hfun2] at hm2
    refine hm2.congr_deriv ?_
    field_simp [hr]
    ring
  refine ⟨hd1, hd2, ?_, ?_⟩
  · field_simp [hr]
  · unfold deltaNewt
    ring

/-- `deltaMond` satisfies the exact `O(ε²)` slip ODE
`r d/dr(δ' / r) = (2 - K_B) (v_c² / r) (G_N M / r²)` for every `r ≠ 0`. -/
theorem deltaMond_slip_ode {KB vc GN M r : ℝ} (hr : r ≠ 0) :
    let C := (2 / 3 : ℝ) * (1 - KB / 2) * vc ^ 2 * GN * M
    HasDerivAt (deltaMond KB vc GN M) (-C / r ^ 2) r ∧
    HasDerivAt (fun x : ℝ => (-C / x ^ 2) / x) (3 * C / r ^ 4) r ∧
    r * (3 * C / r ^ 4) = (2 - KB) * (vc ^ 2 / r) * (GN * M / r ^ 2) := by
  set C : ℝ := (2 / 3 : ℝ) * (1 - KB / 2) * vc ^ 2 * GN * M
  have h1 : HasDerivAt (fun x : ℝ => x⁻¹) (-((1 : ℝ) / r ^ 2)) r := by
    have hi := (hasDerivAt_id r).inv hr
    refine hi.congr_deriv ?_
    dsimp [id]
    ring
  have hd1 : HasDerivAt (deltaMond KB vc GN M) (-C / r ^ 2) r := by
    have hfun : (fun x : ℝ => C * x⁻¹) = deltaMond KB vc GN M := by
      ext x
      unfold deltaMond
      dsimp [C]
      ring
    have hm := h1.const_mul C
    rw [hfun] at hm
    refine hm.congr_deriv ?_
    ring
  have h3 : HasDerivAt (fun x : ℝ => (x ^ 3)⁻¹) (-(3 * r ^ 2) / (r ^ 3) ^ 2) r := by
    have hp3 : HasDerivAt (fun x : ℝ => x ^ 3) (3 * r ^ 2) r := by
      simpa using hasDerivAt_pow 3 r
    exact hp3.inv (pow_ne_zero 3 hr)
  have hd2 : HasDerivAt (fun x : ℝ => (-C / x ^ 2) / x) (3 * C / r ^ 4) r := by
    have hfun3 : (fun x : ℝ => (-C) * (x ^ 3)⁻¹) = (fun x : ℝ => (-C / x ^ 2) / x) := by
      ext x
      ring
    have hm3 := h3.const_mul (-C)
    rw [hfun3] at hm3
    refine hm3.congr_deriv ?_
    field_simp [hr]
  refine ⟨hd1, hd2, ?_⟩
  dsimp [C]
  field_simp [hr]

/-- Prefactor envelope across `0 ≤ K_B ≤ 2`: `0 ≤ (1 - K_B/2)/4 ≤ 1/4` and
`0 ≤ (2/3)(1 - K_B/2) ≤ 2/3`. -/
theorem slip_prefactor_bounds {KB : ℝ} (h0 : 0 ≤ KB) (h2 : KB ≤ 2) :
    0 ≤ (1 - KB / 2) / 4 ∧ (1 - KB / 2) / 4 ≤ 1 / 4 ∧
    0 ≤ (2 / 3 : ℝ) * (1 - KB / 2) ∧ (2 / 3 : ℝ) * (1 - KB / 2) ≤ 2 / 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith

/-! ## Axiom Footprints (every public theorem printed) -/

#print axioms standalone_deep_mond_eos
#print axioms standalone_hydrostatic_exponent_unique
#print axioms standalone_einstein_linear_solution
#print axioms standalone_linear_slip_ratio
#print axioms aqual_on_shell_aniso
#print axioms qumond_on_shell_aniso
#print axioms aest_self_stress_cancellation
#print axioms deltaNewt_slip_ode
#print axioms deltaMond_slip_ode
#print axioms slip_prefactor_bounds

end ResNova.SingleMetricSlipCancellation
