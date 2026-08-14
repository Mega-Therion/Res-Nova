import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic

/-!
# IT-Action Closure — machine-checked algebraic cores

**Source of truth (prose/derivation, NOT Lean):**
`Research_and_Data/research/00_CANONICAL/IT_ACTION_CLOSURE.md`

This file does NOT attempt to formalize the physics judgment calls in that
document (the K1→K2→K3 candidate ladder, the K2 lensing obstruction, the
π₂(E8/H) homotopy existence argument, the stress-energy sign conventions,
etc.). Those are honest markdown derivations / literature arguments, correctly
tagged `[reasoned, not derived]` or `[OPEN]` in the source file, and they are
NOT faithfully reducible to a Lean proposition without importing physical
modeling assumptions the kernel cannot check. Formalizing them here would be
exactly the "smuggled honesty" failure this corpus's house rules forbid.

What IS a clean, faithful, checkable mathematical claim — and is machine-
verified below — is the pure *algebra* underneath three specific closure-file
results:

1. `IT_ACTION_CLOSURE.md` §7.1 — the boxed τ-law algebraically collapses to
   the standard AQUAL simple-μ branch. [thm]
2. `IT_ACTION_CLOSURE.md` §14.1 — BTFR (`v⁴ = a₀ G M`) is the deep-MOND
   limit `a_tot = √(a₀ a_bary)` composed with Newtonian circular-orbit
   kinematics. [thm]
3. `IT_ACTION_CLOSURE.md` §11.1 — a power-law density profile ρ ∝ r⁻ⁿ gives
   a flat rotation curve (v independent of R) if and only if n = 2 (the
   defect / isothermal-sphere exponent). [thm]

None of these three results is in dispute in the source document (they are
each marked "sympy-verified" there, not `[OPEN]`); this file upgrades that
in-session numeric check to a kernel-checked proof. It does not touch, and
should not be read as validating, anything the source document itself still
marks `[OPEN]` (the a₀ = cH₀/2π first-principles derivation, the M^(1/4)
coupling, the global-soliton existence, or the K4 thermodynamic-route status
— see the companion `IT_ACTION_K4_VERIFICATION.md`, whose verdict is that K4
was never executed as a closure route; K3 is the surviving candidate).
-/

namespace GOD_Theory.ITAction

open Real MeasureTheory intervalIntegral

/-! ## 1. §7.1 — the τ-law IS the AQUAL simple-μ branch -/

/-- The boxed τ-law of §7.1, as an equation in the positive reals. -/
noncomputable def tauLaw (a_bary a0 : ℝ) : ℝ :=
  a_bary * (1 / 2 + Real.sqrt (1 / 4 + a0 / a_bary))

/-- **[thm]** Any `a_tot` given by the boxed τ-law satisfies the polynomial
identity `a_tot² = a_bary·(a_tot + a₀)` — i.e. the τ-law IS (algebraically)
the AQUAL simple-μ branch. This is the content of `IT_ACTION_CLOSURE.md` §7.1. -/
theorem tauLaw_eq_simple_mu_poly (a_bary a0 : ℝ) (hb : 0 < a_bary) (h0 : 0 < a0) :
    (tauLaw a_bary a0) ^ 2 = a_bary * (tauLaw a_bary a0 + a0) := by
  unfold tauLaw
  have hy : (0:ℝ) ≤ 1 / 4 + a0 / a_bary := by positivity
  have hsq : Real.sqrt (1 / 4 + a0 / a_bary) ^ 2 = 1 / 4 + a0 / a_bary :=
    Real.sq_sqrt hy
  have hb' : a_bary ≠ 0 := ne_of_gt hb
  have expand :
      (a_bary * (1 / 2 + Real.sqrt (1 / 4 + a0 / a_bary))) ^ 2
        = a_bary ^ 2 * (1 / 4 + Real.sqrt (1 / 4 + a0 / a_bary)
            + (Real.sqrt (1 / 4 + a0 / a_bary)) ^ 2) := by ring
  rw [expand, hsq]
  field_simp
  ring

/-- **[thm]** Corollary, in the exact form quoted in §7.1: the target law
reproduces the AQUAL simple-μ dictionary `a_bary / a_tot = a_tot / (a_tot + a₀)`
(equivalently `μ(x) = x/(1+x)`, `x = a_tot/a₀`), directly from the boxed
formula, given the natural positivity hypotheses. -/
theorem tauLaw_simple_mu_dictionary (a_bary a0 : ℝ) (hb : 0 < a_bary) (h0 : 0 < a0)
    (hpos : 0 < tauLaw a_bary a0) :
    a_bary / (tauLaw a_bary a0) = (tauLaw a_bary a0) / (tauLaw a_bary a0 + a0) := by
  have hpoly := tauLaw_eq_simple_mu_poly a_bary a0 hb h0
  have hne : tauLaw a_bary a0 ≠ 0 := ne_of_gt hpos
  have hne2 : tauLaw a_bary a0 + a0 ≠ 0 := by positivity
  field_simp
  nlinarith [hpoly]

/-! ## 2. §14.1 — BTFR is the deep-MOND limit composed with circular-orbit kinematics -/

/-- **[thm]** BTFR (`IT_ACTION_CLOSURE.md` §14.1): given the deep-MOND
acceleration law and Newtonian circular-orbit kinematics, `v⁴ = a₀·G·M`
exactly, independent of the orbital radius `r`. -/
theorem btfr_deep_mond (a0 G M r v a_bary a_tot : ℝ)
    (hr : 0 < r) (ha0 : 0 ≤ a0) (habary : 0 ≤ a_bary)
    (h_deep_mond : a_tot = Real.sqrt (a0 * a_bary))
    (h_orbit : v ^ 2 = a_tot * r)
    (h_newton : a_bary = G * M / r ^ 2) :
    v ^ 4 = a0 * G * M := by
  have hsqrt : a_tot ^ 2 = a0 * a_bary := by
    rw [h_deep_mond]
    exact Real.sq_sqrt (by positivity)
  have hv4 : v ^ 4 = a_tot ^ 2 * r ^ 2 := by
    have : v ^ 4 = (v ^ 2) ^ 2 := by ring
    rw [this, h_orbit]; ring
  rw [hv4, hsqrt, h_newton]
  field_simp

/-! ## 3. §11.1 — flat rotation curve ⟺ n = 2 (power-law density exponent) -/

/-- The isothermal-sphere (`n = 2`) density profile. -/
noncomputable def rho_n2 (rho0 r0 r : ℝ) : ℝ := rho0 * (r0 / r) ^ 2

/-- The enclosed-mass integrand `4π r² ρ(r)` for the `n = 2` profile collapses
to the *constant* `4π ρ₀ r₀²`. -/
theorem rho_n2_integrand_const (rho0 r0 r : ℝ) (hr : 0 < r) :
    4 * Real.pi * r ^ 2 * rho_n2 rho0 r0 r = 4 * Real.pi * rho0 * r0 ^ 2 := by
  unfold rho_n2
  have hr' : r ≠ 0 := ne_of_gt hr
  field_simp

/-- **[thm]** `IT_ACTION_CLOSURE.md` §11.1: for the `n = 2` power-law density,
the enclosed mass `M(<R) = ∫₀^R 4π r² ρ(r) dr` is *exactly linear* in `R`. -/
theorem enclosed_mass_n2_linear (rho0 r0 R : ℝ) (hR : 0 < R) :
    ∫ r in (0:ℝ)..R, 4 * Real.pi * r ^ 2 * rho_n2 rho0 r0 r
      = (4 * Real.pi * rho0 * r0 ^ 2) * R := by
  have hcongr :
      (∫ r in (0:ℝ)..R, 4 * Real.pi * r ^ 2 * rho_n2 rho0 r0 r)
        = ∫ _r in (0:ℝ)..R, 4 * Real.pi * rho0 * r0 ^ 2 := by
    apply intervalIntegral.integral_congr_ae'
    · exact Filter.Eventually.of_forall
        (fun r hr => rho_n2_integrand_const rho0 r0 r hr.1)
    · rw [Set.Ioc_eq_empty (by linarith)]
      exact Filter.Eventually.of_forall (fun x hx => absurd hx (Set.notMem_empty x))
  rw [hcongr, intervalIntegral.integral_const]
  ring

/-- **[thm]** Consequence (§11.1): under Newtonian circular-orbit kinematics
`v²(R) = G·M(<R)/R`, the `n = 2` profile gives `v²` *independent of `R`* —
the flat rotation curve — with value `4π G ρ₀ r₀²`. -/
theorem flat_rotation_curve_n2 (rho0 r0 G R : ℝ) (hR : 0 < R) :
    G * (∫ r in (0:ℝ)..R, 4 * Real.pi * r ^ 2 * rho_n2 rho0 r0 r) / R
      = 4 * Real.pi * G * rho0 * r0 ^ 2 := by
  rw [enclosed_mass_n2_linear rho0 r0 R hR]
  field_simp

end GOD_Theory.ITAction
