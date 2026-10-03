# D7 Stage 2: a dwarf in an aether wind, non-linear

Goal: find the steady state of a deep-MOND dwarf moving through the AeST aether at satellite speeds, and read off its
internal acceleration relative to the MOND and Newtonian predictions. The linear stage is `../d3_alpha` and
`TARGET_D7_SUPPLEMENT_BRANCH_SELECTION_2026-09-27.md` §§6–8.

## Step A: the steady-state field equations `[D]`

`derive_steady_v2.py` builds the AeST Lagrangian in the dwarf's rest frame. The fields are static and the uniform wind
flows along −z. Output: `steady_lagrangian_v2.json`, derived in about 5 s.

**Power counting.** Potentials count as δ², the aether tilt u ≈ ∂ϕ/Q₀ as δ, and derivatives as Q₀/δ; the leading
Lagrangian is O(δ²). The key fact is that at dwarf scales u ≈ 4×10⁻⁵ but u/r ≈ 0.1 Mpc⁻¹ ≈ Q₀, so each extra factor
of (u·∂) is free. The Lagrangian therefore keeps:
- every flat-space term exactly in the aether perturbation and the scalar;
- terms linear in the metric;
- (∂h)² from Einstein–Hilbert **and from the aether's F²**. At K_B = 1/2 the aether's (∂h₀₀)² cancels Einstein–Hilbert's
  exactly.
- The O(h²) Christoffel piece of J·∂φ. It is O(δ³), and is kept so the check below is exact.

**Gate A2.** Linearized about a uniform MOND gradient with static plane waves, the Lagrangian must reproduce the
validated linear operator `../d3_alpha/wind_bg_matrix_{par,perp}_K275.json`. The comparison weights each column by its
field's typical size and compares each entry with its row's largest entry, at v = 0, 10 and 150 km/s.

| version | result |
|---|---|
| v1 (`derive_steady.py`, `gate_linearization.py`): quadratic in every perturbation | **FAIL**. It is missing the g·u·∂u terms, worth up to 26% of the aether row (perp). This is the power-counting error above. |
| v2 without the aether's (∂h)² | **FAIL** on the metric rows: −k²/4 where the builder has 0.69 |
| v2 without the O(h²) Christoffel piece | fails at 1.8×10⁻⁴ on h₀₀–h₀z (the −(3/2)Q₀ h₀z∂_z h₀₀ term) |
| **v2 as committed** | **PASS**: every entry within 2.5×10⁻⁷ in both geometries (`GATE_A2_V2_PAR.txt`, `GATE_A2_V2_PERP.txt`) |

v1 is kept as the record of the counting error.

## Step A′: axisymmetric reduction `[D]`

`reduce_axisym.py` reduces the Lagrangian to axisymmetry about the wind axis:
- scalars h₀₀ and ϕ;
- vectors h₀ᵢ and u (R and z components);
- a tensor h_ij = Aδ + B nn + C(nẑ + ẑn) + D ẑẑ.

It is evaluated on the plane y = 0 by the chain rule.

**Gate A′.** Random smooth axisymmetric test fields are evaluated at a point off the reduction plane (azimuth
0.7 rad). The Cartesian and reduced densities agree to 8.6×10⁻¹⁷ at v = 0, 5×10⁻⁴ and 0.3
(`GATE_A_PRIME_AXISYM.txt`). This also confirms the Lagrangian's invariance about the wind axis.

**Static content** (`static_reduction.py`, `STATIC_REDUCTION.txt`). With h₀₀ = −2Ψ, h_ij = −2Ψδ_ij, h₀ᵢ = 0 and
u = 0 at v = 0:

    L = −(3/2)|∇(Ψ − ϕ)|² − (3/2)𝒥(|∇ϕ|²) + L_m

This is AeST's SZ reduction, with Newtonian channel Φ̂ = Ψ − ϕ and MOND channel ϕ.
- Matter couples to the metric g (AeST is written in the matter frame), so L_m = −ρΨ.
- The aether equation at u = 0 has source (3/10)(∂Φ̂ − 𝒥′∂ϕ). It vanishes exactly when ∇Φ̂ = 𝒥′∇ϕ, AeST's
  alignment condition, which holds for a spherical dwarf.

## Step B: discrete-action Newton solver

`compile_local.py` generates `local_derivs.py`: per-point gradient and Hessian of Lrest and Y (356 upper-triangle
Hessian entries). The action is S = Σ w L(D f + q_bg), with q_bg the external field along z, solved by Newton with the
exact sparse Hessian, row-norm equilibration and a backtracking line search.

**First attempt: cell-centred central differences (`solve_steady.py`), kept as the record.** Newton stalls on fine grids:
- 32×64 residual 0.35, then 0.018 with a 10⁻³ a₀ floor inside 𝒥′;
- grid continuation made the finest grid worse;
- the Helmholtz split u = ∇Λ + curl ψ (`ProblemH`, `run_helmholtz_test.py`) stalls at 0.024 (24×48) and 0.093 (32×64),
  `HELMHOLTZ_TEST.txt`.

The diagnosis (`diag_stall.py`): the linear solves are accurate (2×10⁻¹²), but the softest Hessian modes flip sign between
neighbouring cells (fraction up to 1.00). These are checkerboard modes that central differences cannot see, so the
linear operator leaves them almost free and the non-linear terms excite them.

**The solver: bilinear finite elements with 2×2 Gauss quadrature (`solve_fe.py`).** Full quadrature has no hourglass
modes. Newton converges quadratically from 10² to about 10⁻⁵ in 7 iterations on 16×32 to 32×64, then stalls at 10⁻⁵
(`FE_TEST.txt`).

**The 10⁻⁵ floor was floating-point cancellation, not physics.** The trail (`diag_fe*.py`, `DIAG_FE*.txt`):
- the Hessian matches finite differences to 5×10⁻⁷;
- the floor sits in the scalar rows, and Y never comes within 57× of the 𝒥′ floor;
- the Newton step is dominated by two soft h₀₀ modes near the outer boundary;
- the Taylor remainder along the step does not depend on the step length (6.5×10⁻⁶ at λ = 10⁻³ and 10⁻²), so it is noise;
- splitting the step by field puts the jump in the metric part;
- Y itself jumps by 3.9×10⁻⁷ (relative) for a change whose linear effect is 8.5×10⁻²⁰.

Cause: `val_Y` builds Y from three O(Q₀²) ≈ 10⁻² pieces that cancel down to Y ~ 10⁻¹². In float64, Y at the solution is
off by 1.9×10⁻⁷ against a 50-digit evaluation of the same formula, and by up to 3.4×10⁻² at small-Y test points.

Fix: `y_accurate` rearranges the cancelling pieces exactly (1 + v²γ² − γ² = 0 and x₁₄ − γ = (x₁₃ − γ²)/(x₁₄ + γ)).
- **Gate Y** (`gate_y_accurate.py`, `GATE_Y_ACCURATE.txt`): **PASS**, with worst error 1.2×10⁻¹³ against 50 digits at
  600 random jets, v = 0, 10⁻⁴ and 10⁻³.
- With it, Newton reaches 2–4×10⁻¹² in 6 iterations (`TEST_FE_LD_*.txt`). Long double (`extended=True`, the default)
  adds nothing at v = 0; it is kept for the milder O(v) cancellations in dY at finite wind.
- At v = 100 and 300 km/s from the static solution (g_e = 0.03 a₀) it also reaches ~2×10⁻¹² (`TEST_FE_WIND_FLOOR.txt`).

**Maintenance.** `y_accurate` is a hand-rearranged copy of generated code. Rerun `gate_y_accurate.py` whenever
`compile_local.py` regenerates `local_derivs.py`.

**Gate B1: the static dwarf** (`gate_static_fe.py`, `gate_b1_verdict.py`). Plummer, v_f = 10 km/s, b = 0.3 kpc, all ten
fields. It checks:
- the Φ̂ flux law (∇²Φ̂ = ρ/3);
- the MOND flux law for the total field (∇·(𝒥′∇ϕ) = ρ/3);
- the aether tilt against the stealth tilt.

Criterion, fixed before the numbers: both channels within 0.02 of 1 at every shell on both grids; no drift away from 1
under refinement; tilt < 10⁻³.

| run | estimator | 0.1 kpc (Φ̂, MOND) | other shells | tilt/stealth | verdict |
|---|---|---|---|---|---|
| g_e = 0.03 a₀, box asinh(100), 32×64 → 48×96 | sharp shell (pre-registered) | 1.0006, 1.0002 → 1.0080, 1.0102 | within 0.5% | 2.7×10⁻¹⁰ | **FAIL** (drift at 0.1 kpc), `GATE_B1_VERDICT.txt` |
| same solutions + 64×128 | smooth weight (after the failure) | 1.0069 → 1.0027 → 1.0015 (Φ̂) | converge at 2nd order | — | diagnosis, `DIAG_B1_FLUX.txt` |
| g_e = 0.003 a₀, box asinh(300), 32×64 → 48×96 | smooth weight | 1.0116, 1.0182 → 1.0039, 1.0060 | within 0.6% | 5.0×10⁻⁹ | **PASS**, `GATE_B1_VERDICT_ge0.003_box300.txt` |

- **Why the pre-registered estimator failed.** Bilinear-element derivatives at the 2×2 Gauss points carry an O(h) error
  that cancels between each ± pair. A sharp |r − r₀| < 0.12 r₀ selection splits pairs, so the shell average carries
  O(h/r) noise that does not shrink monotonically (sharp at 0.1 kpc: 1.0006 → 1.0080 → 1.0032).
- A smooth radial weight keeps pairs together and converges at second order in both channels at every radius. The
  sphere-surface flux integral converges too, but noisily.
- The smooth estimator was introduced after the failure, and the table says so. The sharp one still fails at 32×64 in
  the larger box (1.023, 1.034 at 0.1 kpc), where the core elements are coarser.
- **Setup note.** At g_e = 0.03 a₀ this dwarf's own field is only ~0.03 a₀ from 0.1 to 0.6 kpc (the Plummer core keeps
  it small), so the configuration is external-field dominated everywhere. That is why the MOND channel must use the
  total field, and why the primary runs below use g_e = 0.003 a₀ (internal ≈ 10× external) in a 30 kpc box.

**Locking: the Q1 aether cannot represent the tilt zero mode (2026-09-28). All `solve_fe.py` results at v > 0 are
discretization artefacts.** `diag_aether_block.py`: the continuum Lagrangian's only aether-gradient stiffness is the
curl² term (local Hessian block ±1.000 in (U_R,z − U_z,R); no divergence term). `diag_lift.py` (`DIAG_LIFT.txt`): along
the zero mode δϕ = χ, δu = −∇χ/Q₀ the solver's quadratic form is ~10⁸ × §23's lift. All of it is the discrete curl² of
the interpolated gradient field: that field's rms discrete curl is 13–17% of |∇u|, and the match holds to every printed
digit. The curl coefficient exceeds the lift by ~5×10⁸ for dwarf-scale modes, so nodal elements lock the zero mode. That
suppresses the wind response and biases the solver toward held. Affected: gate B2's first run
(`GATE_B2_WIND_LINEAR_FE_ge0.003_box300.json`, `GATE_B2_Q1_LOCKED_RUN.txt`: FAIL, erratic and grid-dependent) and
stage C to 4 km/s (`STAGE_C_Q1_LOCKED_32x64.txt`: g/g_static − 1 ≤ 2×10⁻⁴ where §7 has 0.3 at 3 km/s). Both are
results on the locked discretization, not physics. Gate B1 (v = 0, u = 0 exactly) is unaffected. The fix is
u = ∇Λ + curl(ψθ̂) with every field in C¹ bicubic Hermite elements (`solve_c1.py`).

**The C¹ solver (`solve_c1.py`), gate L: PASS.** All ten fields are in Bogner–Fox–Schmit bicubic Hermite elements with 4×4
Gauss points.
- The aether and h₀ᵢ come from potentials, u = ∇Λ + curl(ψθ̂) and h₀ᵢ = ∇Ω + curl(ωθ̂). The scalar is carried as
  s = ϕ + Q₀γΛ, so the tilt zero mode is exactly the pure Λ direction.
- h₀ᵢ needs potentials too. At K_B = 1/2 the aether's F² cancels the curl part of the Einstein–Hilbert h₀ᵢ Laplacian
  (local W block = div² only, `diag_w_block.py`). W's curl part is then a multiplier paired with u's curl part. Two free
  W fields against the single potential ψ left spurious null modes (10⁻¹²); the potential form removes them (10⁻⁹).
- The Hessian matches finite differences to 6×10⁻¹⁶.
- **Gate L** (`gate_lift_c1.py`, criterion committed before the run): along the zero mode, with the metric frozen, the
  quadratic form equals −2∫E_lift of §23. R = +1.0000 at r₀ = 0.15, 0.3, 0.6 and 1.2 kpc on both 16×32 and 24×48
  (`GATE_L_LIFT_C1.json`, `GATE_L_LIFT_C1.txt`). The Q1 solver was ~10⁸ off.
- **Static baseline.** Stage 1, with Λ frozen at 0 (the held answer, since the aether's static source is
  divergence-free), converges to ~10⁻¹¹. Freeing Λ stalls at ~10⁻⁵ when g_e ≠ 0. The stall comes from a
  discretization-level forcing of 5×10⁻¹⁹ on the Λ rows acting on a mode the external field leaves almost unlifted
  beyond its radius (∇²ϕ → 0).
- **Exploratory wind runs** (`test_c1_wind.py`, `TEST_C1_WIND.txt`; 16×32, g_e = 0.003 a₀; not gated):
  - The wind forcing on the Λ rows is 6×10⁻¹⁴ × (v / 1 km/s), i.e. 10⁵× the static residual already at 1 km/s.
  - At 1 and 10 km/s, Newton straight from the static state does not converge.
  - At 100 km/s it converges (5×10⁻¹²), with g/g_static = 0.098 and Y/Y_static = 0.019 at r_h, and u/tilt = 3×10⁻³.
    The MOND channel is essentially gone. g is ≈ 1.1 × the Φ̂-channel flux; D3 §34's GR reference is 0.75.
  - Branch, resolution and continuity are open. This is not a stage C result.

**Gate B2** (`gate_wind_linear_fe.py`, ported unchanged to the C¹ solver; criterion committed before the first C¹ run):
the first Newton step from the static solution at 100 and 300 km/s must reproduce §7's real-space correction
δφ = −[1/(4+λ)](4Ψ − 3∇⁻²∂_z²Φ̂) at r = 0.1–0.3 kpc within the script's 10% band. **FAIL on both grids,
resolution-converged** (`GATE_B2_VERDICT_C1.txt`):
- g_e = 0.003 a₀, 100 km/s: dF_r/pred_r = 0.895, 0.877, 0.862, 0.841 at r = 0.1, 0.15, 0.2, 0.3 kpc on 16×32, and
  0.896, 0.878, 0.864, 0.843 on 24×48;
- isolated dwarf, 16×32: 0.852, 0.826, 0.805, 0.775.

The full solver's linear response has §7's structure (a v-independent plateau carried by the scalar, tilt ≪ stealth) but
77–90% of its amplitude, falling with radius. §7's local-WKB formula overstates the linear cancellation of the MOND field
by 10–23% in these configurations.

**The stripped state at satellite speeds (exploratory; `analyse_stripped_c1.py`,
`ANALYSIS_highv_ge0_box300_16x32_v100.txt`).** Isolated dwarf, 30 kpc box, 100 km/s:
- the Newton channel ∂_rΦ̂ is 0.752–0.769 of its static value at r = 0.1–2.4 kpc. That is D3 §34's GR normalization
  1 − K_B/2 = 0.75 (the dragged branch is GR with G̃; the held branch has G̃/(1 − K_B/2));
- the MOND channel ∂_rϕ is 7–24% of its static value over the same radii;
- the state is fore–aft symmetric.

**Box sweep at fixed resolution near the dwarf (exploratory; `box_sweep_c1.py 16 32 fixed`,
`BOX_SWEEP_C1_16x32_fixed.json`, `BOX_SWEEP_C1_fixed.txt`).** 100 km/s, g_e = 0, element size near the dwarf held at
asinh(100)/16 (the first sweep, `BOX_SWEEP_C1_16x32.json`, confounded box size with resolution):

| box edge | grid | residual | g/g_static at r_h | g / Φ̂-flux | 𝒴/𝒴_static | u / stealth tilt |
|---|---|---|---|---|---|---|
| 10 kpc | 16×32 | 9.6e-12 | 0.1732 | 5.833 | 0.0372 | 3.0e-3 |
| 30 kpc | 20×40 | 2.0e-11 | 0.1096 | 3.691 | 0.0126 | 3.3e-3 |
| 100 kpc | 23×46 | 2.7e-11 | 0.0678 | 2.283 | 0.0034 | 3.4e-3 |
| 300 kpc | 27×54 | 7.5e-11 | 0.0444 | 1.494 | 0.0008 | 3.5e-3 |
| 1 Mpc | 30×60 | 5.5e-11 | 0.0290 | 0.978 | 0.0001 | 3.5e-3 |

- The static dwarf has g/Φ̂-flux = 33.68. A purely GR-Newtonian (dragged-normalization) dwarf would have
  g/g_static = 0.75/33.68 = 0.0223. The remnant above that falls with the box and is **not converged in box size**.
- 𝒴 falls by four orders of magnitude while the aether tilt stays at ~3×10⁻³ of the stealth tilt: the state loses its
  MOND field without being dragged.
- Static reference: at edges ≥ 100 kpc it is the Λ-frozen (held) stage-1 state at 2.9–4.1×10⁻¹¹ (its 10⁻¹¹ tolerance
  is not met), because freeing Λ stalls at 1.1–1.8×10⁻³.

**Gate C** (`gate_c_c1.py`, criterion committed in the previous commit before its first run; `GATE_C_C1.json`,
`GATE_C_C1.txt`): **FAIL on criterion (a) only.**

| run | v [km/s] | converged (residual) | Newton channel / static, r = 0.1–0.6 kpc | scalar remnant at r_h | g/g_static at r_h |
|---|---|---|---|---|---|
| 100 kpc, 23×46 | 100 | yes (2.7e-11) | 0.7505–0.7514 | 0.0469 | 0.0678 |
| 100 kpc, 23×46 | 300 | yes (5.2e-11) | 0.7506–0.7515 | 0.0479 | 0.0688 |
| 100 kpc, 30×60 | 100 | yes (4.5e-11) | 0.7505–0.7514 | 0.0466 | 0.0675 |
| 100 kpc, 30×60 | 300 | yes (9.7e-11) | 0.7506–0.7515 | 0.0477 | 0.0685 |
| 1 Mpc, 30×60 | 100 | yes (5.5e-11) | 0.7500–0.7501 | 0.0070 | 0.0290 |
| 1 Mpc, 30×60 | 300 | **no** (5.7e-10 against tol 1e-10) | — | — | — |

- (a) Newton converges in every run: **FAIL**, one of six solves.
- (b) Newton channel within 0.02 of 1 − K_B/2: satisfied by all five converged solves.
- (c) scalar remnant at r_h smaller in the 1 Mpc box: 0.0070 against 0.0466, satisfied.
- (d) plateau, 100 against 300 km/s within 2%: 1.5% in both 100 kpc runs; not evaluable at 1 Mpc.

**Low speeds.** Newton at 7–15 km/s, from the static state or from a stripped state, does not converge
(`LOWV_FROM_STATIC_C1_partial.txt`). No continuation path from the held state to the stripped state is established.

**Deflation search for a second steady state** (`deflation_c1.py`; protocol `PREREG_DEFLATION_C1.md`, committed in
`0c37766` before the first run; `DEFLATION_C1_10kpc_16x32.json`, `DEFLATION_C1_RUN.txt`). 10 kpc box, 16×32, 100 km/s,
g_e = 0. The stripped root x* is deflated (Farrell, Birkisson & Funke 2015), and Newton restarts from six guesses.
- Gate D0, the deflation formula: **PASS** (`DEFLATION_SELFTEST.txt`). The τ-scaled step matches explicit deflated
  Newton to 2.1×10⁻⁹, and on a two-root test system the deflated run finds the second root.
- Gate D1, reproduction: **PASS**. x* converges at 9.6×10⁻¹², with Y/Y_static = 0.0372 and g/g_static = 0.1732. It is
  bit-identical to the cached box-sweep solution (|x* − cached| = 0).
- **None of the six deflated runs converges.** Final residuals are 1.9–4.5 after 17–29 iterations, and each run ends
  0.72–1.17 D0 from x* (D0 = |x_s − x*|), where the line search finds no further descent. Guesses: the static held
  state, the Λ-frozen static state, and x* + a(x_s − x*) for a = 0.5, 0.75, 0.9, 1.25.
- Outcome, worded as pre-registered: **no second steady state found from these six guesses by this deflation** `[O]`.
  This does not exclude a held branch.

## Status (2026-10-03)

Exploratory. Gates A2, A′, Y, L and B1 pass; B2 and C fail as pre-registered. Every converged satellite-speed solve is
stripped: its Newton channel carries GR's normalization 1 − K_B/2 to 0.2%, and its MOND remnant falls with box size.
This holds at K_B = 1/2, 𝒦₂ = 75, Q₀ = 0.1/Mpc only.

Not shown:
- that the stripped state is the unique steady state (a non-linear held branch is not excluded; a pre-registered
  deflation search at one grid, box and speed found no second steady state from six guesses);
- box convergence of the remnant;
- other K_B;
- external-field-dominated outskirts;
- time-dependent capture of a held dwarf.

Do not cite this directory as "AeST is disfavoured by satellites".
