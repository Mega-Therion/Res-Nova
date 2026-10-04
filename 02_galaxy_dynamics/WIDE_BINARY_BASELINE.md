# Close-bin baseline

**Date:** 2026-10-04

In the closest bin the Newton median sat near 0.58 and the pairs near 0.54. A constant scale factor would cancel when both are divided by that bin. The mismatch is removed by one eccentricity offset, fit so the noisy Newton median matches the 500–2000 AU pairs, then frozen at every separation.

| cut | offset in γ |
| --- | ---: |
| clean | +0.70 |
| loose | +0.70 |

Median speed relative to 500–1000 AU after that freeze:

| bin (AU) | clean pairs | clean Newton | gap | loose pairs | loose Newton | gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 500–1000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 |
| 1000–2000 | 0.987 | 0.988 | −0.001 | 0.983 | 0.992 | −0.008 |
| 2000–5000 | 1.018 | 0.983 | +0.035 | 1.039 | 0.976 | +0.063 |
| 5000–10000 | 1.043 | 1.004 | +0.039 | 1.053 | 0.982 | +0.072 |
| 10000–20000 | 1.086 | 0.979 | +0.108 | 1.107 | 0.994 | +0.113 |
| 20000–30000 | 1.120 | 0.951 | +0.169 | 1.159 | 0.981 | +0.178 |

The close baseline is closed. The 1000–2000 AU bin agrees. The step at 2–5 kAU is still there, +0.035 on the strict cut and +0.063 on the loose cut, and it keeps growing outward. Matching the close pairs does not produce that step.

Script: `wide_binary_baseline.py`. Numbers: `WIDE_BINARY_BASELINE.json`.
