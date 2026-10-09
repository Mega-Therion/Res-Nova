# Pre-registration: wide-binary excess vs orientation to the external field (2026-10-08)

**Frozen before any look at orientation in the data.** No orientation-split statistic has been computed on the sample. Tier of everything below: `[O]` protocol.

## Why
After the RV fix and mass stratification (`WIDE_BINARY_FINAL_2026-10-04.md`), two models survive the pre-registered χ² rule:
- **E**: μ_std with the external-field effect;
- **S**: the Form-2 screen.

Both fit R(s). They differ in symmetry: the external-field effect makes the internal field **anisotropic** about the Galactic field direction ĝ_ext, while S predicts a screened but **isotropic** boost. A dependence on orientation is a discriminator that R(s) alone cannot provide.

## Model input (to verify before use)
In the regime where the external field dominates, the point-mass potential takes the Milgrom form
Φ ∝ −GM / (μ_e r √(1 + K_e sin²θ)), with K_e = d ln μ / d ln x at x_e = g_ext/a₀ and θ measured from ĝ_ext.
This is `[C]` as recalled from the wide-binary EFE literature (Banik & Zhao). **Check the exact form against the source before any computation.**
For μ_std at x_e ≈ 1.8: K_e = 1/(1+x_e²) ≈ 0.24. That is an order-of-magnitude input only.

## Observable
For each binary:
- ψ = sky-plane angle between the projected separation vector and the projected direction to the Galactic center, at the binary's position. This uses ra/dec of both stars.
- Split the strict-cut sample by |cos ψ| at its median ("aligned" vs "perpendicular").
- Statistic: ΔR(s) = R_aligned(s) − R_perp(s) per pre-registered s bin, using the same R estimator, bins and mass stratification as `WIDE_BINARY_FINAL`.

## Gate 1: power (must pass before the real split is computed)
1. Inject E with the anisotropic potential above into the existing mock generator, project to the sky, and apply the same cuts.
2. Compute the expected ΔR and its error at the real sample's N.
3. **If the expected combined significance over the 5–30 kAU bins is < 2σ, STOP.** Record "underpowered at current N" and do not compute the real split. Looking anyway would only add a forking path.

## Gate 2: decision rule (only if Gate 1 passes)
- E predicts ΔR > 0 of the injected size; S predicts ΔR = 0.
- One-sided test on the combined 5–30 kAU ΔR:
  - ≥ 3σ above 0 and consistent with E's injection → favors E over S;
  - consistent with 0 and ≥ 2σ below E's prediction → disfavors E;
  - anything else → inconclusive.
- Seeds, cuts and bins are fixed now and not changed afterward.

## Known confounds (to be quantified in Gate 1 mocks, not after the look)
- **Projection dilution:** ψ is a sky angle, not the 3D θ.
- **The relative-velocity direction** also matters, not just the separation.
- **Contamination by flybys / triples.** These could correlate with Galactic-plane direction through stellar density.

## Amendment A (2026-10-08): pre-look red team. Committed before Gate 1 or any orientation statistic
Two independent passes attacked this protocol: a numerical check and a referee panel. Their scripts and the verbatim re-run outputs (12 of 12 exit 0, no data file opened) are in `prereg_orientation_redteam_2026-10-08/`. Every number below points to a line there. Tier `[O]`. Everything above this amendment is unchanged as the frozen record. Where they conflict, this amendment governs.

**A1. "Why" is corrected.**
- Under C3, `WIDE_BINARY_FINAL_2026-10-04.md` leaves **N, E, S and P** all unexcluded, not two models.
- N, S and P all predict ΔR = 0. The test therefore discriminates the anisotropic E against **all isotropic laws**, not E against S.
- A result favouring E cannot rehabilitate unscreened μ_std, whose EFE quadrupole is already excluded by Cassini at ~4.6σ (`CURRENT_STATE_READ_THIS_FIRST.md`).

**A2. Model input.**
- The potential written above is Banik & Zhao's **AQUAL** form (arXiv:1509.08457, Eq. 18). Its K_e is their L0; it is renamed **L_e** here.
- Because the pipeline is QUMOND, the injected model is their **QUMOND** form, Eq. 36: Φ = −(GMν_ext/r)(1 + (K0/2) sin²θ), with K0 = ∂ln ν/∂ln n at the Newtonian external field.
- **The pipeline's `boost('E')` must not be used for injection.** Its anisotropy has the wrong sign: aligned 0.933 vs perpendicular 1.115 at g_N/g_ext = 0.01, while the field solution has aligned > perpendicular (`checks_a.out`, `s3_qumond_fft.out`, `s3c_qumond_converge.out`). Its orientation average equals the field solution's (1.05391, `s6_other_checks.out`), which is why R(s) fits are unaffected.
- The injected model's orientation-averaged R(s) must reproduce the frozen E column. If it does not, it is a new model and needs its own χ² run first.

**A3. Parameters, pinned.** These are the pipeline's constants (`wide_binary_fish.py`):
- A0 = 1.042×10⁻¹⁰ m/s², the primary value;
- GE = 1.9×10⁻¹⁰ m/s², entering ν as the Newtonian external field, as the pipeline does;
- DMAX = 0.2 kpc, μ_std, RNG seed 20261004.

E's prediction is reported as a band over:
- A0 ∈ {1.042×10⁻¹⁰ (primary), 1.2×10⁻¹⁰ (literature)};
- GE taken as the Newtonian field or as the true field.

Other a0 values may be added only by a later amendment committed before Gate 1.

**A4. Regime.**
- The asymptotic (external-field-dominated) form fails at 5–10 kAU, where q = g_N/g_ext = 0.25–2.25 for M = 0.8–1.8 M☉ (`s6_other_checks.out`), and is marginal at 10–20 kAU.
- ΔR_E therefore comes from a numerical QUMOND solve, or from a declared bracket [0, asymptotic]. The bracket's lower edge sets Gate 1 and the "disfavours E" threshold.

**A5. Bins.**
- In the strict cut, 20–30 kAU has a single stratum with n = 32 (NMIN = 30), so each half falls below NMIN. The bin is **dropped**.
- The strict 10–20 kAU M<1 stratum (n = 38) is dropped for the same reason.

**A6. Estimator and combination.**
- ΔR is computed per (bin, stratum) cell, each half against its own orientation-split control, and combined with fixed mock weights ∝ ΔR_E/σ². A cell under NMIN in either half is dropped from both halves.
- Only this combined statistic decides. Per-bin, per-stratum and loose-cut values are descriptive.
- The primary estimator is chosen from three candidates by median mock Z, fixed before the split:
  - a |cos ψ| split at 1/√2;
  - a split on w = sin²λ cos 2ψ at 0 (λ = angle between ĝ_ext and the line of sight);
  - a regression on w.
- In the toy, the regression on w gave 1.217× the z of the |cos ψ| split (`checks_d.out`). The other two estimators are reported.

**A7. Gate 1 is raised.**
- Gate 1 passes only if the median Z of ≥ 200 E mocks is **≥ 4**. At that separation, P(favour E | E) = 0.841 and P(disfavour E | S) = 0.954 (`checks_d.out`); at the old 2σ bar they were 0.159 and 0.477.
- σ comes from ≥ 200 isotropic-null mocks, and "favours E" must also exceed the largest null-mock value.
- **Expected outcome: STOP.** These are two red-team upper bounds, not averaged and not results:
  - z ≤ 0.40–0.62, with ceiling 1.38 for an exact 0°/90° split (`s4b_sigma_floor.out`);
  - Z ≲ 1.1 (referee panel).

**A8. Decision rule, defined.**
- "Consistent with E" means within 2σ (two-sided) of the A3 band, including its A4 bracket.
- "Disfavours E" means ≥ 2σ below the band's lower edge and |Z| < 2.
- A result ≥ 3σ below 0, or above the band, is **"anomalous, no verdict"**.
- Everything else is inconclusive.

**A9. Mocks.**
- λ comes from each binary's real (l, b). Positions only: no separation orientation is used.
- The hidden-companion variant T and the Galactic tide are added to every model. The tide is ≤ 3.2×10⁻³ g_N at 30 kAU (`checks_d.out`).
- Local-force velocities are checked against orbits integrated in Eq. 36. In the toy, 6.2% of orbits drifted in energy at K0 ≠ 0 (`checks_c2.out`).

**A10. Pinned before running.**
- The runner script, output file and commit are named in the Gate-1 commit.
- Velocity direction is kept out of the decision.
- Nulls: ΔR in the 2–5 kAU bin and in the orientation-split control, plus a placebo ψ → ψ − 45°. Any null above 3σ blocks a verdict. A 90° placebo is not a null, because it only flips the sign.

**Considered and not adopted.** "Restrict the test to s ≥ 20 kAU" (numerical pass): not adopted, because A5 drops the strict 20–30 kAU bin. The A4 bracket handles the regime instead.
