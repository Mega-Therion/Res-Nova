# AeST: the scalar-channel function whose total law is μ_std

**Status:** `[D]` (computer algebra and numerics). No tier of any existing row changes. D9's function stays the one in use; replacing it with the function below is `[O]`, under D7.
**Date:** 2026-10-14
**Machine:** `scripts/aest_total_scalar_correspondence.py`, 26 checks, exit 0.
**Scope:** the AeST quasistatic weak-field limit of `TARGET_D7_COVARIANT_COMPLETION.md` §2, in spherical symmetry, with the AeST mass term negligible and the Newtonian and scalar gradients aligned. Outside that (non-spherical and external-field problems, the mass-term regime) the relation below is not exact.

## Setting

Matter feels Φ = Φ̂ + φ, with ∇²Φ̂ = 4πĜρ and ∇·[𝒥′(𝒴)∇φ] = 4πĜρ, 𝒴 = |∇φ|². In spherical symmetry the total acceleration is g = ĝ + g_φ with 𝒥′(𝒴) g_φ = ĝ. In the Newtonian regime G_N = (1 + 1/λ_s)Ĝ, so ĝ = η g_N with η = Ĝ/G_N = λ_s/(1+λ_s).

Write x = g/a₀, y = g_N/a₀ and s = g_φ/a₀, where a₀ is the fitted scale of the total law. The SPARC comparison fits the total law x μ_std(x) = y.

## Result

If the total law is x μ_std(x) = y, the scalar channel must satisfy:

| quantity | value |
|---|---|
| scalar acceleration | s = x [1 − η μ_std(x)] |
| slope of the scalar function | 𝒥′(a₀² s²) = η μ_std(x) / (1 − η μ_std(x)) |
| the scalar function, 𝒥(0) = 0 | 𝒥(𝒴(x)) = a₀² [2η F_std(x) − η² y(x)²], with 𝒴(x) = a₀² s(x)² |
| F_std | (x√(1+x²) − arsinh x)/2, so F_std′(x) = x μ_std(x) |
| deep-MOND end | 𝒥 ≈ (2λ_s / 3ã₀) 𝒴^{3/2}, with ã₀ = (1+λ_s) a₀ |
| Newtonian end | 𝒥′ → λ_s |
| single-valued | if and only if λ_s < (27 + 12√6)/5 = 11.2788 |

The function is given in parametric form, with x as the parameter. The relation dJ/dx = 𝒥′(𝒴(x)) d𝒴/dx holds identically (check A3).

**The bound.** s′(x) = 1 − η y′(x), with y′(x) = x(x²+2)/(1+x²)^{3/2}. With t = x²,

  32(1+t)³ − 27 t (t+2)² = (t − 2)² (5t + 8) ≥ 0,

so y′ ≤ 4√2/(3√3), with equality only at x = √2. Hence s is strictly increasing for every x if and only if η < 3√3/(4√2), which is λ_s < (27 + 12√6)/5. Above that value s(x) folds. Two total accelerations would then need different slopes at the same scalar gradient, so no single-valued 𝒥 exists (check B2).

**Static ghost conditions** (`TARGET_D7` §5), on this function:
- 𝒥′ > 0 everywhere, because 0 < η < 1 and 0 < μ_std < 1.
- 𝒥′ + 2𝒴𝒥″ = η y′(x)/s′(x) (check A10). It is positive exactly where s is invertible, so this condition is the same condition as the bound.
- 𝒥″ > 0 wherever s′ > 0 (check A11).

These are conditions on the static scalar problem. Healthy evolution of the full constrained scalar–vector–metric system is a separate question, and it is open.

## What this closes and what it changes

- **The gap it closes is already published.** With 𝒥′ = λ_s μ_std(√𝒴/ã₀), Paper I §III ([10.5281/zenodo.23101840](https://doi.org/10.5281/zenodo.23101840)) shows that the total law equals ν_std only as λ_s → 0. At g_N = a₀ it gives g/g_N = 1.564 for λ_s = 1, against 1.272 for the total law (check B4). Measured here over g_N/a₀ from 10⁻³ to 10³, the largest values of |g/g_tot − 1| fall near g_N ≈ a₀:

  | λ_s | max \|g/g_tot − 1\| | at g_N/a₀ |
  |---|---|---|
  | 0.5 | 0.145 | 0.71 |
  | 1 | 0.233 | 0.79 |
  | 2.6 | 0.369 | 1.00 |

  The function above returns the total μ_std law at every λ_s below the bound. A numerical inversion at λ_s = 0.5, 1, 2.6 and 10 agrees to 3×10⁻¹⁶ (check B1).
- **It is a different function from λ_s μ_std of the scalar gradient.** The two agree at both ends. Between them, the slopes 𝒥′ differ by up to 6.5% at λ_s = 0.1 and up to 80% at λ_s = 1 (check B7).
- **D9 is unchanged and stays `[P]`.** The calculus in `SZStdEmbedding.lean` is correct. What it embeds is μ_std in the scalar channel. The function whose total law is μ_std is the one above, `[D]`. D9's function stays the one in use. Replacing it with the function above is a model choice, recorded `[O]` under D7.
- **The λ_s ≤ 2.60 heuristic applies to the scalar-channel function only.** `02_galaxy_dynamics/lambda_s_solar_system_check.py` uses the residual (1+λ_s)³ a₀²/(2g_N). That is the scalar-channel function's residual (check C2). The Saturn-precession ceilings in the same script (λ_s ≤ 2.21 and 2.68) use the same (1+λ_s)³ factor.
  - Under the function above, the spherical residual is the total law's a₀²/(2g_N), with no λ_s in it (check C1). The script's λ_s → 0 margins (Mercury 1157×, Saturn 46.7× at the live a₀) then hold at every λ_s.
  - So these ceilings bound λ_s only under the scalar-channel function. Under the total-law function, any bound on λ_s must come from the non-spherical external-field problem. This correspondence is not exact there, and that problem is `[O]`.
- **`TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` §4–§5 uses a₀ where `TARGET_D7` §2.1 and Paper I use ã₀ = (1+λ_s)a₀.** With the fitted a₀ in that slot, the deep-MOND total comes out low by 1/√(1+λ_s): 0.708 at λ_s = 1 (check B6). With ã₀ it is correct (check B5). The ghost-free conclusions of §5 do not depend on the scale. The λ_s-dependent solar-system residual is the one `lambda_s_solar_system_check.py` computes, and that script uses ã₀.

## The stealth configuration

The Painlevé–Gullstrand Schwarzschild configuration, with φ = 𝒬₀T and A_μ = (−1, 0, 0, 0), is the one `TARGET_D3` §34 already records. Checks D1–D5 re-check it as a benchmark, for the action

  ℒ = R − (K_B/2)F² + 2b J^μ∇_μφ − b𝒴 − ℱ(𝒴,𝒬) − λ(A·A + 1), with b = 2 − K_B,

with ℱ(0,𝒬₀) = ℱ_𝒬(0,𝒬₀) = 0 and f_𝒴0 = ℱ_𝒴(0,𝒬₀). Metric variations hold A^μ fixed.
- A·A = −1, F = 0, J^μ = 0, 𝒴 = 0 and 𝒬 = 𝒬₀.
- The expansion is Θ = −(3/2r)√(2m/r).
- The vector equation holds with the multiplier λ(r) = b𝒬₀Θ + (b + f_𝒴0)𝒬₀².
- The extra-field metric source vanishes, and Ricci = 0.

This tests the stated equations on one solution. It is not an independent audit of the general variation. It also does not address which branch a system occupies.

## Reproduce

```bash
python3 scripts/aest_total_scalar_correspondence.py   # 26 checks, exit 0, about 10 s
```
