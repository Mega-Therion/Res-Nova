# 📜 Pre-Registration Protocol V3: the a₀(z) test with a μ_std-extracted a₀

**Status:** frozen and executed 2026-09-12. Closes the P1 chain opened by `PREREG_A0_OF_Z_V2.md`.

V2 (same night) re-ran the registered test at the FROZEN a₀ = 1.116e-10 under μ_std →
INCONCLUSIVE (2.06σ), and its sensitivity scan showed the verdict is hostage to the a₀
extraction's own μ-dependence. V3 completes the loop: re-extract a₀ from the SPARC
175-galaxy benchmark under μ_std, then re-run the discrimination with that value.

## What was frozen

- Data: SPARC 175 (3391 points), SHA-256 verified against the repo manifest.
- μ_std = x/√(1+x²) for BOTH the a₀ extraction and the a₀(z) discrimination.
- Extraction harness: `02_galaxy_dynamics/sparc_a0_reextract_std.py` — the corpus's own
  documented nuisance-prior grid (Yd, Yb, fd), profile likelihood over a₀, 500× galaxy bootstrap.
- ξ co-scaled by definition: ξ = a₀(0)/(cH₀).

## Executed results [D], recorded as found

| | a₀ (μ_std) | χ²(H_const) | χ²(H_horizon) | Δχ² | verdict |
|---|---|---|---|---|---|
| central | 1.1562×10⁻¹⁰ | 11.366 | 10.615 | +0.75 (0.87σ) | **INCONCLUSIVE** |
| bootstrap-16% | 1.0615×10⁻¹⁰ | | | +8.83 | INCONCLUSIVE |
| bootstrap-84% | 1.2342×10⁻¹⁰ | | | −6.25 | INCONCLUSIVE |

**Neither hypothesis reaches 3σ anywhere in the 68% CI.** The V1 5.9σ constant-a₀ verdict is
unrecoverable under the live closure: V2 at the frozen a₀ is inconclusive, V3 at the
re-extracted a₀ is inconclusive, and the extraction shift (+24% vs μ_dual on the same harness)
moves the test across the inconclusive band in exactly the way the V2 scan predicted.

## Validation honesty [O]

This extraction harness does **not** reproduce `A0_ESTIMATE.json`'s 1.107×10⁻¹⁰ for μ_dual
(it gives 9.29×10⁻¹¹); the original generating script's per-galaxy priors (published distance +
inclination errors) live outside the repo. The μ_dual-vs-μ_std **comparison on this harness**
is internally valid (identical data, priors, method), the +24% shift's direction is provable
(μ_std(x) > μ_dual(x) ∀x>0), and the inconclusive verdict spans the entire bootstrap CI — so
the conclusion is robust to the harness gap. Exact-pipeline reproduction remains open and is
tracked on the Task Board; any future re-claim of a 3σ+ verdict requires it.

## Standing consequence

The a₀(z) question is **OPEN [O]** under the live closure. `.zenodo.json` cites no a₀(z)
verdict. Any new claim requires: exact-pipeline a₀ re-extraction + a JWST-era z>1.5 dataset
(the 20-point MUSE-DARK sample is fully exploited at this precision).
