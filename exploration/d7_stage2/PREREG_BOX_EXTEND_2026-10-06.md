# Pre-registration: box extension of the stripped steady state (exploratory)

Committed before the first solve of `box_extend_c1.py`. Status of D7 is unchanged: **branch selection open `[O]`**.
Nothing here can close D7, and no wording below may be cited as a no-go or as "AeST disfavoured".

## Question
Does the stripped 100 km/s isolated-dwarf state (g_e = 0, K_B = 1/2, 𝒦₂ = 75, fixed resolution near the dwarf) keep a MOND
remnant above GR's Newton channel as the box grows? Or does the remnant go to zero, so that it was held up by the outer clamp?

## Why not an asymptotic (Robin) boundary condition
Imposing a logarithmic (MOND) or 1/r (Newtonian) far field at the box edge assumes the answer, because branch selection is
the question. Box extension assumes nothing about the far field.

## Decision variables (at r_h = 0.3 kpc, from `stage_c_c1.observables`)
- **e = g/Φ̂-flux − 0.75**: the excess over GR's Newton channel (1 − K_B/2 = 0.75; README "stripped state" section).
  e → 0 means the remnant is a box artefact.
- **Y/Y_static**: the MOND-regime measure the README uses for "held remnant".

## Existing data (`BOX_SWEEP_C1_16x32_fixed.json`)
| edge [kpc] | e | Y/Y_static |
|---|---|---|
| 10 | 5.0827 | 3.72e-2 |
| 30 | 2.9411 | 1.26e-2 |
| 100 | 1.5333 | 3.41e-3 |
| 300 | 0.7444 | 7.98e-4 |
| 1000 | 0.2278 | 7.32e-5 |

Local log–log slopes steepen: e: −0.50, −0.54, −0.66, −0.98; Y: −0.99, −1.08, −1.32, −1.98.
Fits of a + b·R^−p give **negative** a for both (e: −0.52; Y: −5.0e-4), so the data show no positive floor.

## Predictions for the 3000 kpc box (B = 30000, grid 34×68)
| hypothesis | e(3000) | Y/Y_static(3000) |
|---|---|---|
| H_pw: a persistent power law (fit to all 5 points: p_e = 0.543, p_Y = 1.011) | 0.232 | 1.2e-4 |
| H_steep: continued steepening (last local slope held) | 0.077 | 8.3e-6 |

The predictions differ by 3× (e) and 14× (Y). Solver residuals in the sweep are ~1e-11, so the test has power.

## Decision rule (fixed now)
- **Converging to GR's channel:** e(3000) ≤ 0.12 **and** Y/Y_static(3000) ≤ 4e-5.
  Report: "on this grid, speed and K_B, the stripped state's MOND remnant decreases toward zero with box size; consistent with a box artefact." `[O]`
- **Persistent remnant:** e(3000) ≥ 0.18 **or** Y/Y_static(3000) ≥ 8e-5.
  Report: "remnant decays no faster than a power law; not box-converged."
- **Otherwise:** inconclusive. Run B = 100000 (10000 kpc, grid 37×74) under the same rule, scaled by the H_steep slope.
- **Overshoot flag:** if e(3000) < −0.02 (g below GR's channel), report it as a separate anomaly. Do not fold it into either verdict.
- **Non-convergence** (Newton residual > 1e-10 after 40 iterations): report as non-convergence, with no verdict.

## Anchor
`box_extend_c1.py anchor` re-evaluates the committed 1000 kpc row from `cache_branch/boxsweep_B10000_30x60_v100.npy`, with
no re-solve. It must reproduce g/g_static = 0.0290, g/Φ̂-flux = 0.978 and Y/Y_static = 7.3e-5 to the printed digits, or the
run does not count.

## Scope limits
One grid family, one speed (100 km/s), one K_B (1/2), g_e = 0, and the clamp kept. Even a "converging" result does not
establish uniqueness, does not pass gate B2 or C (different gates), and does not select a branch.
