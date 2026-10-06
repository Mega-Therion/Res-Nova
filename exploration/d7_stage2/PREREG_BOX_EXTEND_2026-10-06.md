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

## Results

**Anchor (2026-10-06): PASS.**
- `anchor_quick` and the full `anchor`, re-evaluated from `cache_branch/boxsweep_B10000_30x60_v100.npy`, reproduce the committed 1000 kpc row to every printed digit: g/g_static = 0.029036439110345473, g/Φ̂-flux = 0.9778217608849343, Y/Y_static = 7.323625928307524e-05, static g/flux = 33.67567755705084.
- Static reference (stage 1): 4.05e-11, the same as the committed row.

**Attempt 1 (B = 30000, 3000 kpc, 34×68, Newton from the static state): NON-CONVERGENCE, so no verdict, per the rule above.**
- Static reference: stage 1 at 4.86e-11, same pattern as every committed box ≥ 100 kpc.
- Wind solve: equilibrated |grad|/|src| fell 85.9 → 1.37 in one step, then stalled at **0.136 after 26 Newton steps**, with the line search at λ ≈ 1e-4. Total 9114 s.
- Row in `BOX_EXTEND_C1_16x32_fixed.json`; log in `BOX_EXTEND_C1_run.txt`.

## Amendment 1 (2026-10-06, committed after attempt 1 and before attempt 2 runs)

**Why.** Attempt 1 failed in the wind Newton solve started from the static state. Attempt 2 changes only the initial
guess and the target box. The question, decision variables, rule structure and scope limits are unchanged.

**Method: box continuation on exactly nested grids.**
- The fixed-resolution grids share dξ = dη = asinh(10⁴)/30 = 0.3301162518345376.
- Choosing B_n = sinh(n·dξ) makes the n×2n grid contain the committed 1000 kpc 30×60 grid node for node: radial offset 0, η offset n − 30 elements on each side, verified to 1e-12.
- Rungs n = 31, 32, 33, 34 (edges 1390, 1935, 2692, **3745 kpc**). Each rung starts from the previous converged solution, with every nodal DOF (f, f_ξ, f_η, f_ξη) copied unchanged (same dξ, so no rescaling) and new outer DOFs set to 0.
- **This tracks the stripped branch by construction.** That matches the question, which concerns the stripped state's remnant.

**Correctness checks before any solve.**
- (i) Embedding into the same grid (offset 0) reproduces x exactly.
- (ii) dξ equality is asserted in code.
- (iii) `observables` on the padded 1000 kpc solution on the 31×62 grid gives g/Φ̂-flux = 0.9778217608849343 at 0.3 kpc.

**Target, fixed now: n = 34, edge R* = 3745.16 kpc (B = 37451.6251).** Chosen because it nests exactly. Rungs 31–33 are
descriptive only.

**Predictions at R*,** using the same two pre-registered formulas: the 5-point pure power fit for H_pw, and the last local slope for H_steep.
- e: H_pw = 0.2059, H_steep = 0.06218.
- Y/Y_static: H_pw = 9.348e-5, H_steep = 5.337e-6.

**Thresholds at R*,** placed at the same log-space positions between H_steep and H_pw that the original thresholds held at
3000 kpc. Positions: e 0.3996 / 0.7684; Y 0.5947 / 0.8565.
- **Converging:** e(R*) ≤ 0.1003 **and** Y/Y_static(R*) ≤ 2.929e-5.
- **Persistent:** e(R*) ≥ 0.156 **or** Y/Y_static(R*) ≥ 6.198e-5.
- **Otherwise:** inconclusive.
- The overshoot flag (e < −0.02) and the scope limits are unchanged.

**Stop rule.** If any rung does not converge (Newton residual > 1e-10 after 40 iterations), the ladder stops there and there is no verdict.

**Static reference at R*.** Computed in a separate process by the same two-stage path as every committed row.
- If its stage 1 does not reach ≤ 1e-10, "converging" cannot be declared, since it needs Y.
- "Persistent" can still be declared from e alone. Otherwise e is reported descriptively.

**Optional check.** A from-static solve at n = 31, in parallel. If it converges and matches the continuation root, the root is independent of the initial guess there. If it fails, that is consistent with attempt 1.

Whatever the ladder gives is reported as "attempt 2 under Amendment 1 at 3745 kpc", not as the 3000 kpc result.
