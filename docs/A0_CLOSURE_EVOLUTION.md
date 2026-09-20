# a₀ — closure evolution and what the shift actually measures

Measured 2026-09-20 at commit `726820f`. Primary artifacts:
`02_galaxy_dynamics/A0_REEXTRACTION_3MU_2026-09-16.json`,
`02_galaxy_dynamics/A0_MEASUREMENT.json`.

## The headline correction

The shift is often quoted as **a₀ = 1.1163e-10 under μ_dual → 1.1607e-10 under μ_std**,
described as the effect of changing the interpolation closure. **That framing is wrong,
and it understates the closure effect by a factor of about 6.**

Those two numbers differ in *three* ways at once, only one of which is the closure:

| | 1.1163e-10 | 1.1607e-10 |
|---|---|---|
| sample | 171 galaxies, 3,375 points | 175 galaxies, 3,391 points |
| distances | pre-audit | distance-corrected (PRs #59/#60) |
| closure | μ_dual = x/(1+x) | μ_std = x/√(1+x²) |
| status | **SUPERSEDED 2026-09-17**, provenance only | live (T1) |

So 1.1163 → 1.1607 (+4.0%) is a *net* drift across an audit, not a measurement of μ.

## The closure effect, isolated

`sparc_a0_reextract_3mu.py` extracts a₀ for three interpolation functions on **one
frozen harness** — same 175 galaxies, same 3,391 points, same priors. That isolates μ:

| μ | form | closure | a₀ (best) | 68% bootstrap |
|---|---|---|---|---|
| μ_dual `[X]` | x/(1+x) | g = ḡ(½+√(¼+a₀/ḡ)) | **9.2420e-11** | [8.480, 10.026]e-11 |
| **μ_std** `[live]` | x/√(1+x²) | g = √((ḡ²+√(ḡ⁴+4ḡ²a₀²))/2) | **1.16067e-10** | [1.0594, 1.2324]e-10 |
| μ_simple | x/(1+√(1+x²)) | g = √(ḡ²+2a₀ḡ) | **5.4430e-11** | [4.653, 6.070]e-11 |

**The closure effect is 9.2420e-11 → 1.16067e-10, i.e. +25.6%** — 6.4× the +4.0% the
common framing attributes to it. a₀ is not closure-independent, and the three rows are
pairwise disjoint at 68%: the number you extract is a property of the (μ, a₀) *pair*,
never of a₀ alone.

## Consequences that follow from this and are easy to miss

- **Any a₀ quoted without its μ is meaningless.** Always cite the pair.
- μ_simple's low value is not a third opinion — it is the deep-MOND √2 normalization
  defect (μ′(0) = ½, the half-rapidity member), documented in
  `POSTULATE_R_ISOLATION_2026-09-16.md`.
- The a₀ = cH₀/2π comparison is defined **only** against the μ_std row
  (1.1607e-10). Forward: Planck H₀ → 1.0422e-10, −1.37σ. The backward inversion to H₀
  is **ladder-covariant, not independent** — 97 of the 175 SPARC distances assume
  H₀ = 73 — so the 68% window is not a falsifier.
- The O4 redshift test inherits all of this: its verdict flips across the ±30%
  a₀-extraction range, which is why the 5.9σ claim is `[X]`-retracted and the μ_std
  re-run is INCONCLUSIVE at 2.06σ.

## Do not do

Do not "reconcile" 1.1163e-10 with 1.1607e-10 by adjusting either. The first is a
superseded pre-audit object retained for provenance; its own `status` field in
`A0_MEASUREMENT.json` says so. Retiring it means ceasing to quote it, not editing it.
