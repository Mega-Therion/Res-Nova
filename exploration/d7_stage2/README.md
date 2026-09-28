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

## Step B: discrete-action Newton solver (in progress)

**Pieces.**
- `compile_local.py` generates `local_derivs.py`: per-cell gradient and Hessian of Lrest and Y (356 upper-triangle
  Hessian entries).
- `solve_steady.py` holds:
  - a stretched (R, z) grid with axis parity and zero outer data;
  - S = Σ w L(D f + q_bg);
  - Newton with the exact sparse Hessian, row-norm equilibration and a line search;
  - an external-field background;
  - grid interpolation.

**What works.**
- The Hessian matches a finite difference of the gradient to 10⁻¹⁰–10⁻⁹.
- With no external field, the spherical SZ solution plus u = 0 solves the static problem on a 16×32 grid: the
  residual reaches 10⁻⁵ and the tilt stays at 3×10⁻⁹ against the stealth tilt 3.7×10⁻⁵. This is the held branch.

**Open.** Newton stalls on finer grids.
- **Cause.** The aether's curl modes stiffen as K_B/Δ², while its gradient mode is held only by the lift. The ratio
  grows as 1/Δ² and reaches ~10¹⁶ on a 32×64 grid, the limit of double precision. Newton then wanders along the soft
  direction.
- **Mitigation 1.** A 10⁻³ a₀ floor inside 𝒥′ (deep MOND is a degenerate p-Laplacian at zero field) cut the 32×64
  residual from 0.35 to 0.018.
- **Mitigation 2.** Grid continuation from an unconverged coarse solution made the finest grid worse.
- **Next.** Solve for the Helmholtz parts u = ∇Λ + curl ψ, so that the soft and stiff directions are scaled
  separately.

## Remaining steps

- **Step B, gates:**
  - v = 0 must reproduce the static AeST MOND dwarf (`gate_static.py`: flux laws for Φ̂ and 𝒥′∂ϕ, held tilt);
  - small v must reproduce the linear §7 response;
  - two resolutions must agree.
- **Step C:** continuation in v at 50, 150 and 300 km/s, reading off the internal acceleration at the half-light radius
  against MOND and Newton.
