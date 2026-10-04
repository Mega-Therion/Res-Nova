# The 2–5 kAU step after matching

**Date:** 2026-10-04

The close-bin baseline is already matched. This step asks whether the rise that starts at 2 kAU is just a change in who is in the sample. Each pair at 2–5 kAU is matched to a pair at 1–2 kAU with a similar mass, a similar distance, and a similar chance-alignment score. Pairs with no close counterpart are dropped.

| cut | matched pairs | median speed ratio, far / near |
| --- | ---: | ---: |
| clean | 1909 | 1.048 |
| loose | 2505 | 1.033 |

The mean ratio is about 1.6 because a few pairs are much faster. The median is the comparison. After the match, the 2–5 kAU pairs are still 5% faster on the strict cut and 3% faster on the loose cut. The step is not a mix of mass, distance, or chance alignment. It is in the velocities.

Script: `wide_binary_step.py`. Numbers: `WIDE_BINARY_STEP.json`.

## Uncertainty (added 2026-10-04, `wide_binary_step_bootstrap.py`)

| cut | matched median | bootstrap SE | unmatched random pairing | near/near null |
| --- | ---: | ---: | ---: | ---: |
| clean | 1.048 | 0.027 | 1.023 | 1.000 ± 0.023 |
| loose | 1.033 | 0.024 | 1.044 | 1.001 ± 0.020 |

- **Against 1:** the matched step is 1.8σ (clean) and 1.4σ (loose).
- **Against the calibrated Newton ratio** for 2–5 vs 1–2 kAU (0.983/0.988 ≈ 0.995 clean, 0.976/0.992 ≈ 0.984 loose, from `WIDE_BINARY_BASELINE.json`), it is about 2σ in both cuts.
- **Effect of the match on the step:** it raised the clean step (1.023 → 1.048) and lowered the loose one (1.044 → 1.033). Both changes are within the noise.
- **Conclusion:** matching on mass, distance and chance alignment does not remove the step, but this matched-pair statistic alone does not establish it. The binned α-fit (1.045 ± 0.011, 1.063 ± 0.009) is the stronger measurement.
