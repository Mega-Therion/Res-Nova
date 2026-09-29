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

**Gate B2** (`gate_wind_linear_fe.py`): the first Newton step from the static solution at 100 and 300 km/s must reproduce
§7's real-space correction δφ = −[1/(4+λ)](4Ψ − 3∇⁻²∂_z²Φ̂) at r = 0.1–0.3 kpc, with the criterion in the script's
docstring. Pending.

## Step C: continuation in the wind speed (`stage_c_continuation.py`), pending

Newton from a secant predictor, 0.5 → 300 km/s, with step bisection on failure. Per speed it records:
- g/g_static at r_h (the observable);
- Y/Y_static and u/stealth tilt (the branch indicators: held keeps Y and has u ≈ 0; dragged drives Y → 0 and u → 1);
- the eigenvalues of the equilibrated Hessian nearest zero (a fold needs one crossing zero; Newton failing is not
  enough);
- the final residual at every speed.

The dragged branch's own acceleration is not yet established. M(<r)/(12πr²) is the Φ̂-channel flux, and nothing yet
shows that the dragged branch's acceleration equals it.
