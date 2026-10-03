# Pre-registration: deflation search for a second steady state at satellite speed

Committed before the first production run of `deflation_c1.py run`. The README's Status lists, as not shown,
"that the stripped state is the unique steady state (a non-linear held branch is not excluded)". This protocol looks
for a second steady state. It cannot show uniqueness.

## Setup

The setup matches the committed box sweep (`box_sweep_c1.py`) at its smallest box. That box keeps the largest remnant
(Y/Y_static = 0.0372), which is where a held state is most likely to survive.

- C¹ solver `solve_c1.py` with K_B = 1/2, 𝒦₂ = 75, Q₀ = 0.1/Mpc.
- Isolated Plummer dwarf (v_f = 10 km/s, b = 0.3 kpc), g_e = 0.
- Box edge 10 kpc (asinh(100)), grid 16×32, wind 100 km/s.
- Static held state x_s: the box sweep's two-stage Newton (Λ frozen, then free).
- Stripped root x*: Newton from x_s at 100 km/s, tol 1e-10, maxit 40.

## Gates

- **D0, the deflation formula** (`deflation_c1.py selftest`, run before this commit):
  - (a) The τ-scaled Newton step matches an explicit Newton step on G = M·F to a relative 1e-6, at 20 random points of a 6-dimensional test system with two deflated points.
  - (b) On a two-root system, undeflated Newton from (0.5, 0.5) finds (1, 1). With (1, 1) deflated, Newton from the same start finds (−1, −1).
- **D1, reproduction.** x* converges and reproduces the committed box-sweep row: Y/Y_static and g/g_static at 0.3 kpc within 1% of 0.0372 and 0.1732, and |x* − cached| / |cached| < 1e-6 against `cache_branch/boxsweep_B100_16x32_v100.npy`. If D1 fails, the run stops.

## Search

- **Deflation:** M(x) = Π_i [(|x − x_i*| / D0)^−2 + 1], with D0 = |x_s − x*|.
- **Newton:** the solver's own method (row-norm equilibration, backtracking), with the step scaled by τ and the line search done on M·|F|.
- **Convergence:** the undeflated equilibrated residual must fall below 1e-10 within 60 iterations.
- **Initial guesses, in this order:**
  - G1: x_s.
  - G2: the Λ-frozen stage-1 static state.
  - G3 to G6: x* + a(x_s − x*) for a = 0.5, 0.75, 0.9, 1.25.
- **Distinct:** a converged state is distinct if it lies more than 0.05·D0 from every known root. Each distinct state is added to the deflated set before the next guess.
- **Classification by Y/Y_static at 0.3 kpc:**
  - held: ≥ 0.25 (the MOND gradient keeps at least half its static value);
  - intermediate: from 3 × 0.0372 up to 0.25;
  - stripped-like: below that.

## How the outcome will be stated

- **A distinct held state found:** "a second steady state that keeps Y/Y_static = … at r_h exists at this grid, box,
  speed and parameter point" `[D]`, numerical, with nothing claimed beyond that point.
- **No distinct state found:** "no second steady state found from these six guesses by this deflation" `[O]`. This
  does **not** exclude a held branch.
- **Distinct states that are not held:** recorded with their numbers.

Output: `DEFLATION_C1_10kpc_16x32.json` and the run log.
