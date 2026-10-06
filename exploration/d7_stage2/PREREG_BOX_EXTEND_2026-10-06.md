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

**Operational note (2026-10-06, during attempt 2).** Running the ladder, the n = 34 static reference and the optional
n = 31 from-static check at the same time exhausted memory: about 4.3 GB RSS plus 6.3 GB swap across the three solves
on an 11 GB machine.
- The **ladder continues unchanged.**
- The static reference was stopped and re-queued (`d7-ladder-static34-after`) to start when the ladder exits. Its result is unaffected; it is the same computation.
- The **optional from-static check was stopped and is not run**, so initial-guess independence at n = 31 remains untested.

No threshold, target or rule changed.

**Attempt 2 (Amendment 1, nested-grid continuation): NON-CONVERGENCE at the first rung, so no verdict (stop rule).**
- Rung n = 31 (1391 kpc, 31×62), started from the zero-padded converged 1000 kpc solution.
- Equilibrated |grad|/|src| went 8.47 → 1.27 → 0.228 → 0.110 (step 5) → 0.0333 (step 10), then stalled at 0.0333. At step 13 the backtracking line search found no descent along the Newton direction (λ < 1e-4), and Newton returned unconverged. Total 2894 s.
- The queued n = 34 static reference was stopped at start, since without a ladder solution it cannot enter a verdict.
- Rows in `BOX_LADDER_C1.json`; log in `BOX_LADDER_ladder.txt`.

**What was measured.** Both attempts ended in line-search failure (no descent for λ ≥ 1e-4) at equilibrated residuals 0.136 (attempt 1) and 0.033 (attempt 2). The cause is **not yet diagnosed**:
- Attempts 1 and 2 differ in both box size and initial guess, so they cannot separate the two.
- The one run that could, the optional from-static solve at n = 31, was not run.
- Hypothesis under test, not a finding: a direction softens as the box grows. Next step: the near-zero Hessian spectrum of the five cached converged sweep solutions.

**D7 box convergence remains open `[O]`. Nothing here is a physics result.**

**Diagnostic (2026-10-06, no solve; `diag_box_zero_modes.py`, `BOX_ZERO_MODES_C1.json`).** Six smallest |eigenvalues| of the
equilibrated wind Hessian at the five cached converged sweep solutions.

| box edge | smallest eigenvalue | dominant field |
|---|---|---|
| 10 kpc | 1.665e-8 | Ω (the gradient part of the shift, h₀ᵢ = ∇Ω + curl(ω θ̂)), weight 1.0 |
| 30 kpc | 5.468e-10 | Ω |
| 100 kpc | 1.682e-11 | Ω |
| 300 kpc | 5.661e-13 | Ω |
| 1000 kpc | 1.672e-14 | Ω |

- **Scaling:** local log–log slopes −3.11, −2.89, −3.09, −2.93; fit **λ_min ∝ R^−3.00**.
- **The next modes** are ω (0.667) and ψ (0.667). Some eigenvalues are negative, so the Hessian is indefinite.
- **Extrapolated:** 6.0e-15 at 1391 kpc and 6.0e-16 at 3000 kpc, against float64 ε = 2.2e-16.
- **Stall levels:** ε/λ_min ≈ 0.037 and 0.37 at those boxes, versus the observed stalls 0.033 and 0.136.
- **Counterexample:** the 1000 kpc solve converged (5.5e-11) with ε/λ_min ≈ 0.013. So "ε/λ_min sets the stall" is suggestive, not established.
- **Status:** the hypothesis "a near-null direction softening with box volume blocks Newton beyond 1000 kpc" is supported, not proved. D7 remains `[O]`.

**Soft-subspace check at attempt 2's initial guess (2026-10-06; `diag_soft_subspace.py`, `SOFT_SUBSPACE_C1.json`).**
The point is the zero-padded 1000 kpc solution on 31×62, 75,772 DOFs, measured in Newton's equilibrated coordinates.

- **Spectrum:** the 12 smallest |eigenvalues| run continuously from 6.1e-15 (Ω) through 9.1e-15 (ω) and −1.8e-14 (ψ) up to 1.6e-13. The largest ratio between neighbours is only 2.06, so there is **no clear spectral gap**; the soft band is wider than 3 modes.
- **(a) Residual in the 3 softest modes: 1.9e-9 of the equilibrated residual.** That is at roundoff level.
- **(b) Newton step in those modes: 0.82 of the step in equilibrated (y) coordinates.** In physical (x) coordinates ‖dx‖ and ‖dx_perp‖ differ by 5e-8 relative.
  - The full and projected steps reduce the residual identically: 8.4649 → 1.27076 in both.
- **(c) Moving along the softest mode by the Newton step's own x-norm:**
  - g/flux at 0.3 kpc changes by 4.8e-6 relative, and Y by 4.6e-5;
  - the residual changes by 2.8e-7 relative.
  - The direction is nearly flat, not exactly flat.
- **Reading:** projecting out the soft band is admissible, since the residual has no measurable soft component. At the initial guess it changes nothing, so whether it fixes the stall can only be seen at the stall point, which attempts 1–2 did not save.

**Attempt 3 (projected Newton, `attempt3_projected_newton.py`, `5f52f13`): VALIDATION FAIL, so the ladder did not run and there is no verdict.**
- Validation: the committed 100 kpc row from static. Plain Newton converged there to 2.7e-11 in the original sweep.
- Projected Newton: residual 86.6 → 1.35 → 0.239 → 0.0341 → 1.25e-3 → 9.99e-5, then no descent at step 6.
- λ_min = 1.68e-11 throughout. All 24 computed eigenpairs lie within 1000× of λ_min, so the soft band is ≥ 24 modes wide at 100 kpc.
- **The residual's share in the soft band rose to 1:** 1.1e-6, 7.4e-5, 4.2e-4, 2.9e-3, 0.080, **0.9998**, **1 − 9e-12**.
- **Reading (measured):** the final part of the solve lives entirely in the soft band (Ω/ω/ψ). The band carries real residual, not roundoff, so projecting it out cannot converge. This retracts the inference drawn from (a) at the initial guess: (a) holds only far from the root.
- **Consistent with attempts 1–2:**
  - The band's λ_min falls as R⁻³; plain Newton resolves it up to 1000 kpc.
  - Beyond that, float64 solves along it lose precision (ε/λ_min ≈ 0.04 at 1391 kpc, ≈ 0.4 at 3000 kpc), and Newton stalls at 0.033 / 0.136.
- **Per the third-attempt rule, solo attempts stop here.** D7 box convergence beyond 1000 kpc goes to RY as a joint problem. D7 remains `[O]`. Nothing here is a physics result.

**Option 1 (field rescaling), ruled out (2026-10-06; `diag_scaling_condition.py`, `SCALING_CONDITION_C1.json`).**
κ = |eig|max/|eig|min of sym(D H D):

| point | rowsum (current) | Ruiz | Jacobi |
|---|---|---|---|
| 1000 kpc converged | **5.8e13** | 1.6e14 | 9.3e17 |
| 1391 kpc initial guess | **1.6e14** | 4.4e14 | 2.5e18 |

No diagonal scaling beats the current one, so the near-singularity is intrinsic to the discrete equations, not a scaling artefact.

**Next: option 2 (mixed-precision Newton).** Extended-precision (80-bit long double, ε = 1.08e-19) Hessian and gradient assembly, plus refinement of the float64 LU solve with extended-precision residuals. Feasibility checked: scipy.sparse supports float128 matvec and matmul. Not yet built. **D7 stays `[O]`.**
