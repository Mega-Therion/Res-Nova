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

## Next

- **Step A′:** reduce to axisymmetry about the wind axis. The external field is then along z as well.
- **Step B:** discrete-action Newton solver on an (R, z) grid. Gates:
  - v = 0 must reproduce the static AeST MOND dwarf;
  - small v must reproduce the linear §7 response;
  - two resolutions must agree.
- **Step C:** continuation in v at 50, 150 and 300 km/s, reading off the internal acceleration at the half-light radius
  against MOND and Newton.
