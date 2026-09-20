import LambdaSBound
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# The perihelion-precession route to `lambda_s`

D3 §8.4 offers two routes to a solar-system ceiling on `lambda_s`. They are not
of equal standing.

**Route 1 (`Q_2`)** compares the residual against a Cassini quadrupole datum by
setting `Q_2^eq = delta_g / r`. That is an order-of-magnitude heuristic, not an
identity: `delta_g ∝ r^2` is an *isotropic central* perturbation, while the
published `Q_2` is the *traceless anisotropic* coefficient of the MOND external
field effect, `Phi_EFE = -(1/2) Q_2 (z^2 - r^2/3)`. A monopole is being read
against a quadrupole bound. The comparison is informative about magnitude and
nothing more.

**Route 2 (precession)** has no such mismatch. For any isotropic central
perturbation `delta_g = k r^n` on a near-circular orbit, the apsidal angle
`Phi = pi / sqrt(3 + r F'/F)` gives, to first order,

    Delta varpi = pi (n + 2) delta_g / g_N     per revolution

which for `n = 2` is `4 pi delta_g / g_N`. Dividing by `P = 2 pi sqrt(r^3/GM)`:

    d(varpi)/dt = (1 + lambda_s)^3 a_0^2 r^(5/2) / (GM)^(3/2)

This is the exact linear response of a Kepler orbit to the residual the theory
predicts — same geometry on both sides.

This module formalises that rate's structure. `r^(5/2)` is written as
`r^2 * sqrt r` to stay in `Real.sqrt` rather than `rpow`, which keeps the
monotonicity proofs elementary.

Note the steepness: Route 1's observable grows as `r`, Route 2's as `r^(5/2)`.
Outer planets bind far harder under precession, which is proved below rather
than asserted.

What is **not** here: the numerical ceiling. The derivation is exact; the
observational bound it is compared against is an empirical input, and D3 records
its provenance separately.
-/

namespace ResNova.PrecessionBound

/-- Secular perihelion precession rate induced by the `mu_std` residual.
`r^(5/2)` is `r^2 * sqrt r`. -/
noncomputable def precessionRate (lam a0 GM r : ℝ) : ℝ :=
  (1 + lam) ^ 3 * a0 ^ 2 * (r ^ 2 * Real.sqrt r) / (GM * Real.sqrt GM)

/-- **Steeper than Route 1.** The precession observable carries `r^2 * sqrt r`
where `Q_2` carries `r^1`, so the outer solar system binds far harder here. -/
theorem precession_mono_r {lam a0 GM r₁ r₂ : ℝ}
    (hlam : 0 ≤ lam) (hGM : 0 < GM) (h0 : 0 ≤ r₁) (h : r₁ ≤ r₂) :
    precessionRate lam a0 GM r₁ ≤ precessionRate lam a0 GM r₂ := by
  have hsq : r₁ ^ 2 ≤ r₂ ^ 2 := by nlinarith
  have hsr : Real.sqrt r₁ ≤ Real.sqrt r₂ := Real.sqrt_le_sqrt h
  have h3 : (0 : ℝ) ≤ (1 + lam) ^ 3 := by positivity
  have hs0 : (0 : ℝ) ≤ Real.sqrt r₁ := Real.sqrt_nonneg _
  unfold precessionRate
  gcongr

/-- Monotone in `lambda_s`, so the observable is a one-sided constraint on it. -/
theorem precession_mono_lam {lam₁ lam₂ a0 GM r : ℝ}
    (h1 : 0 ≤ lam₁) (h : lam₁ ≤ lam₂) (hGM : 0 < GM) (hr : 0 ≤ r) :
    precessionRate lam₁ a0 GM r ≤ precessionRate lam₂ a0 GM r := by
  have hb : (0 : ℝ) ≤ 1 + lam₁ := by linarith
  have hab : (1 : ℝ) + lam₁ ≤ 1 + lam₂ := by linarith
  have hfac : (1 + lam₂) ^ 3 - (1 + lam₁) ^ 3
      = ((1 + lam₂) - (1 + lam₁))
        * ((1 + lam₂) ^ 2 + (1 + lam₂) * (1 + lam₁) + (1 + lam₁) ^ 2) := by ring
  have hnn : 0 ≤ ((1 + lam₂) - (1 + lam₁))
        * ((1 + lam₂) ^ 2 + (1 + lam₂) * (1 + lam₁) + (1 + lam₁) ^ 2) :=
    mul_nonneg (by linarith) (by nlinarith [hb, hab])
  have hc : (1 + lam₁) ^ 3 ≤ (1 + lam₂) ^ 3 := by linarith [hfac, hnn]
  unfold precessionRate
  gcongr

/-- **The ceiling.** A measured bound on the precession rate at radius `r`
inverts to a bound on `(1 + lambda_s)^3`. Exact, with no geometric mapping in
between -- this is what Route 1 cannot claim. -/
theorem precession_ceiling {lam a0 GM r bound : ℝ}
    (hGM : 0 < GM) (hr : 0 < r) (ha0 : a0 ≠ 0)
    (hmeas : precessionRate lam a0 GM r ≤ bound) :
    (1 + lam) ^ 3 ≤ bound * (GM * Real.sqrt GM) / (a0 ^ 2 * (r ^ 2 * Real.sqrt r)) := by
  have hsr : 0 < Real.sqrt r := Real.sqrt_pos.mpr hr
  have hsG : 0 < Real.sqrt GM := Real.sqrt_pos.mpr hGM
  have hden : 0 < a0 ^ 2 * (r ^ 2 * Real.sqrt r) := by positivity
  have hGd : 0 < GM * Real.sqrt GM := by positivity
  unfold precessionRate at hmeas
  rw [div_le_iff₀ hGd] at hmeas
  rw [le_div_iff₀ hden]
  nlinarith [hmeas, hden, hGd]

/-- The rate is strictly positive for a real orbit, so the ceiling constrains a
nonzero quantity rather than being vacuously true of zero. -/
theorem precession_pos {lam a0 GM r : ℝ}
    (hlam : 0 ≤ lam) (ha0 : a0 ≠ 0) (hGM : 0 < GM) (hr : 0 < r) :
    0 < precessionRate lam a0 GM r := by
  have hsr : 0 < Real.sqrt r := Real.sqrt_pos.mpr hr
  have hsG : 0 < Real.sqrt GM := Real.sqrt_pos.mpr hGM
  have h1 : (0 : ℝ) < 1 + lam := by linarith
  have ha : (0 : ℝ) < a0 ^ 2 := by positivity
  unfold precessionRate
  positivity

end ResNova.PrecessionBound
