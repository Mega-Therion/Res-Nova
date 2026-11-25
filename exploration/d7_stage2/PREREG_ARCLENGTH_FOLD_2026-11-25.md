# Pre-registration: pseudo-arclength continuation of the held and stripped branches in wind speed (2026-11-25)

**Status:** pre-registered. Committed before `arclength_c1.py` is run. D7 stays `[O]` in every outcome.

## Question

The held (MOND) branch has been followed only with the biased Q1 solver, from 0 to 4 km/s (it fails at 5). The stripped branch was followed with the validated C¹ solver from 100 km/s down to 20 km/s (lost below about 19.4 km/s, `BRANCH_DOWN_C1_V2.txt`). The window from 5 to 19 km/s has never been solved by anything.

Natural-parameter continuation cannot pass a fold (a turning point in v). Pseudo-arclength continuation can. This run asks two things:

1. Does the held branch, started from the static held state with the C¹ solver, **fold** (turn back in v) below satellite speeds?
2. Does it reach 100 km/s while staying held?

## Frozen setup

These are the same as `branch_down_c1_v2.py`:

- Solver: `solve_c1.ProblemC1`, 16×32 grid, box asinh(300).
- External field g_e = 0.003 a₀. Plummer dwarf with v_f = 10 km/s, b = 0.3 kpc.
- K_B = 1/2, 𝒦₂ = 75.
- Static state: Newton with the Λ DOFs frozen. All runs at v > 0 have Λ free.

**Unknowns.** (x, p), with p the wind speed in km/s.

**Equations.**
- The equilibrated gradient: Sd·∇S(x; p) = 0, with Sd from the Hessian row norms at the start of each step.
- The pseudo-arclength condition: θ·ẏ·(y − y_pred) + ṗ·(p − p_pred) = 0, in equilibrated coordinates y = Sd⁻¹x.
- θ = 1/|dy/dp|² at the first step, so that the initial tangent splits evenly between y and p.
- ∂F/∂p by central difference with dp = 0.01 km/s.

**Corrector.** Newton on the full bordered (N+1) system, solved with sparse LU. Convergence: equilibrated residual < 1e-10 within 8 iterations. On failure, ds is halved, down to a minimum Δp-equivalent of 0.002 km/s. If the minimum is reached, the run stops and records the failure.

**Stepping.** The tangent is re-solved at each accepted point and its orientation kept. ds grows ×1.5 after a convergence in ≤ 4 iterations, capped at a Δp of 5 km/s.

## Gates (in order; a failed gate stops the run and is reported as such)

- **G0, reproduction.** The bordered corrector at fixed p = 20 km/s (tangent = ∂/∂p), started from the cached stripped state `cache_branch/stripped_ge0.003_16x32_v20.npy`, reproduces it: residual < 1e-10, and Y/Y_static at r_h within 1e-4 of 0.0154.
- **G1, static.** The static held state converges (residual < 1e-10), with Y/Y_static = 1 by construction.
- **G2, first step.** Natural Newton at p = 0.25 km/s from the static state converges.

## Outcomes (pre-stated)

- **FOLD-HELD.** ṗ changes sign along the held branch at p_fold < 20 km/s. The smallest |eigenvalue| of the equilibrated Hessian falls by ≥ 10× toward the turning point. Reading: the held branch connected to the static state does not reach satellite speeds at this parameter point.
- **HELD-SURVIVES.** The path reaches p ≥ 100 km/s with Y/Y_static at r_h ≥ 0.5 throughout. Reading: escape route 1 (non-linear hysteresis) is alive.
- **CONNECTS.** After a fold the path turns back up in p and continues with Y/Y_static < 0.1. Matching the stripped branch's observables within 1% at a common p establishes an S-curve (bistability window).
- **INCONCLUSIVE.** The corrector fails at minimum ds with no fold signature.

**Also run:** arclength from the cached stripped state at 20 km/s, *downward* in p, to look for the stripped branch's lower fold. The same outcome labels apply mirrored (FOLD-STRIPPED at p_fold > 0).

## Artifacts

`arclength_c1.py` → `ARCLENGTH_C1_ge0.003_16x32.json` and `ARCLENGTH_C1.txt`.
