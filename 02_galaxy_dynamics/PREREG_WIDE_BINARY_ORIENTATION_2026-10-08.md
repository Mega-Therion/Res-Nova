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
