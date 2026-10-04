# SPARC tier-1: the horizon anchor is not distinguished

**Status:** [D], read off `PARAMETER_LEDGER.json`. No new fit was run.
**Date:** 2026-10-04

Both rows use μ_std. The only difference is the acceleration scale: the horizon anchor `cH0/2π` against the literature value `1.2×10⁻¹⁰ m s⁻²`.

| | Horizon anchor | Literature a₀ |
| --- | ---: | ---: |
| Tier 0 median reduced χ² | 11.077 | 9.935 |
| Tier 0 aggregate χ²/dof | 93.647 | 78.946 |
| Tier 1 median reduced χ² | 3.360 | 3.412 |
| Tier 1 mean reduced χ² | 5.634 | 5.631 |
| Tier 1 aggregate χ²/dof | 6.088 | 6.035 |
| Tier 1 free parameters | 374 | 374 |
| Points | 3375 | 3375 |

At tier 0 the horizon anchor fits worse. At tier 1, with the same distance, inclination, and mass-to-light nuisances free, the two medians differ by about 0.05. That is not a detection of the anchor, and it is not a rejection of it. The anchor stays a declared normalization. NFW, with 716 free parameters, has median 1.921 and is a different model, not a third a₀.
