# Dark Bubble wall acceleration → a₀: [X] (2026-11-19)
Pre-registered in `PREREG.md`. Script `wall_a0.py`, results `WALL_A0.json`.

**Geometry [D].** The exact normal acceleration of a wall R(τ) in AdS₅ expands, for H, 1/R ≪ k, to
a₅² − k² = 2R̈/R − (H² + 1/R²) = (8πG/3)(ρ_Λ − 2ρ_m).
- This is independent of k. It matches the exact formula to 0.1% at k = 10⁻¹² s⁻¹.
- Pure Λ gives a_w = cH_dS = 5.42×10⁻¹⁰, the factor-4.7 problem.
- **With the real matter content, a_w = cH₀√(Ω_Λ − 2Ω_m(1+z)³) = 1.54×10⁻¹⁰ today.** Matter, not the 2π, brings the scale down to the MOND range.

**K1 (scale): passes, but only with fine-tuning.**
- Rule R1 (μ = dT/dg = μ_std(g/a_w)) gives a₀ = 1.1607×10⁻¹⁰ at Ω_m = 0.3229, inside Planck's 2σ range.
- Rule R2 (Milgrom 1999, a₀ = a_w/2) needs Ω_m = 0.291, outside it.
- But d ln a_w/d Ω_m = −27. The scale exists only because Ω_Λ ≈ 2Ω_m today.

**K2 (stability across SPARC's volume): fails, decisively.**
- a_w² < 0 for z > 0.028 (ρ_m > ρ_Λ/2). There the wall is below the AdS threshold: no Unruh excess, so no a₀.
- Across SPARC (D = 0.98–128 Mpc, z ≤ 0.029), the predicted a₀ drifts from 1.54×10⁻¹⁰ to 0.
- On the radial acceleration relation (fixed Υ), Δχ² = +6675 against a constant a₀ at Ω_m = 0.315, and +4758 at the best Ω_m (0.320). The pre-registered threshold was 25.
- The data want a constant a₀; this mechanism makes it run steeply with redshift.

**K3 (Cassini).** Unruh-temperature inertia is modified *inertia*, not a field equation. There is no Q₂ term from an external-field effect, and the residual at Saturn is about a₀²/(2g) ≈ 10⁻¹⁶ m s⁻², well under the ~10⁻¹⁴ bound. Moot after K2.

**K4 (WEP).** The derivation uses only the wall's 5D kinematics, with no brane gauge couplings. The a₀ value is independent of Basile–Borys–Masias (arXiv:2507.03748, verified), but the host framework still carries that problem.

**Verdict.** [X]. A wall-acceleration Unruh origin of a₀ inside the Dark Bubble is ruled out by a₀'s redshift constancy over SPARC. The Λ-only version (a_dS) is ruled out by scale.
- **Positive fact [D]:** the matter correction is what lowers the scale. Any horizon mechanism that keys on R̈/R rather than H inherits the same steep z-dependence, so this is a reusable no-go.
- **Assumption:** pure AdS on each side; matter realised as strings would not alter K_ττ at leading order.
