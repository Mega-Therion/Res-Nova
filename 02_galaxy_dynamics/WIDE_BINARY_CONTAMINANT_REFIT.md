# Contaminant refit, 2026-10-04

Amendment B in `PREREG_WIDE_BINARY_FISH.md`. Parameters were fit on the 500–2000 AU control bin only, then frozen. Gaia test-bin α values were not used to set them. Measured R(s) is the published fit in `WIDE_BINARY_FISH.json`.

| cut | f_c | β |
| --- | ---: | ---: |
| clean | 0.00 | 0.00 |
| loose | 0.00 | −0.15 |

The control bin does not want a growing population of hidden companions. f_c is zero in both cuts. The mass slope is zero on the clean cut. On the loose cut it is −0.15, and extrapolating that slope makes Newton-plus-mass-error predict R = 1.085 at 2–5 kAU, above the measured 1.063. On the clean cut the predicted Newtonian R at 2–5 kAU stays 1.00 to 1.005 against a measured 1.045. The 4% excess is not removed.

Under the rule written in Amendment B, that means the excess remains a sample systematic and **no new gravity verdict is claimed**. The χ² values are recorded anyway. A model is over 18.5 on every combination only for N, F, S, and P. E is under 18.5 for the clean cut with the mass slope (12.9) and over it otherwise. Fish stays far over the cut (179 to 2413). That does not reopen the fish rule, and it does not newly exclude Newton, nesting, or the screen, because the frozen contaminant did not account for the 2–5 kAU offset.

Script: `wide_binary_refit.py`. Numbers: `WIDE_BINARY_CONTAMINANT_REFIT.json`.
