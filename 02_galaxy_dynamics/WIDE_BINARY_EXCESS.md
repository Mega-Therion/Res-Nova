# The 2–5 kAU excess, modeled as an inner orbit

**Date:** 2026-10-04. This was written after the fish-rule result and after Amendment B. It is a sample model, not a blinded gravity verdict.

Amendment B added a dimensionless 1.5 to ṽ and made the hidden-companion fraction zero at 1 kAU. The control bin then chose a fraction of zero, so nothing happened at 2–5 kAU.

The replacement gives the hidden companion a fixed physical speed. The outer orbit slows down as 1/√s, so the same companion is a larger dimensionless excess farther out. The fraction and the speed are fit on the 500–2000 AU histogram only. The speed grid is 0.2, 0.4, 0.8, and 1.2 km/s. The fraction is capped at 0.50.

| cut | fraction | inner speed |
| --- | ---: | ---: |
| clean | 0.30 | 0.2 km/s |
| loose | 0.30 | 0.2 km/s |

Median speed relative to the 500–1000 AU bin:

| bin (AU) | clean observed | clean model | loose observed | loose model |
| --- | ---: | ---: | ---: | ---: |
| 500–1000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 1000–2000 | 0.987 | 0.992 | 0.983 | 0.985 |
| 2000–5000 | 1.018 | 1.003 | 1.039 | 1.003 |
| 5000–10000 | 1.043 | 1.071 | 1.053 | 1.068 |
| 10000–20000 | 1.086 | 1.167 | 1.107 | 1.202 |
| 20000–30000 | 1.120 | 1.295 | 1.159 | 1.315 |

The close pairs will tolerate a 30% companion rate only if the inner speed is the smallest value on the grid, 0.2 km/s. That choice barely moves the 2–5 kAU bin (model 1.003 against 1.018 clean and 1.039 loose) and then climbs too fast. At 20–30 kAU the model is near 1.30 and the medians are near 1.12 and 1.16.

So an inner orbit with a fixed physical speed does not produce a 4% shift that starts at 2 kAU and then stays modest. The shift in the data is flatter than that mechanism. The 2–5 kAU offset is still not accounted for. No gravity verdict is changed.

Script: `wide_binary_excess.py`. Numbers: `WIDE_BINARY_EXCESS.json`.
