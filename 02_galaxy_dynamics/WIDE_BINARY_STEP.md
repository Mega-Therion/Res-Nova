# The 2–5 kAU step after matching

**Date:** 2026-10-04

The close-bin baseline is already matched. This step asks whether the rise that starts at 2 kAU is just a change in who is in the sample. Each pair at 2–5 kAU is matched to a pair at 1–2 kAU with a similar mass, a similar distance, and a similar chance-alignment score. Pairs with no close counterpart are dropped.

| cut | matched pairs | median speed ratio, far / near |
| --- | ---: | ---: |
| clean | 1909 | 1.048 |
| loose | 2505 | 1.033 |

The mean ratio is about 1.6 because a few pairs are much faster. The median is the comparison. After the match, the 2–5 kAU pairs are still 5% faster on the strict cut and 3% faster on the loose cut. The step is not a mix of mass, distance, or chance alignment. It is in the velocities.

Script: `wide_binary_step.py`. Numbers: `WIDE_BINARY_STEP.json`.
