# D7 directional tidal boundary-value problem (2026-11-21)

> **SCOPE NOTICE (2026-11-21):** The mathematical operator and extragalactic X-COP vs. depth-axis no-go results below stand as recorded; per [`../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`](../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md) and [`../../OUTSIDE_GALAXIES.md`](../../OUTSIDE_GALAXIES.md) (Erratum `E-16`), ordinary GR holds outside galaxies and Cassini $Q_2$ is not a gate on the galaxy law `μ_std`.

Equation solved, with one constant coupling and no fitted function:

```
∇²φ = κ T_∥,    T_∥ = −(2GM/r³) P₂(cos θ),    φ → 0 at infinity.
```

The particular solution is φ = (κ GM /(3r)) P₂. A 4000-point finite-difference
shell solve reproduces it to a maximum relative error 6.355e-07.

Orbit average on a circular ecliptic orbit with the galactic centre at ecliptic
latitude -5.53°: ⟨P₂⟩ = 0.243035. The spherical average of T_∥ is 0.
The orbit average is not.

## Pre-registered gates

| Gate | Threshold | Result at the only coupling Mercury allows |
|---|---|---|
| Mercury perihelion | ≤ 1.6 mas/century (2σ) | cap, by construction |
| Cassini Q₂ at 9.5 AU | ≤ 5.2e-27 s⁻² | 3.980e-40 (PASS) |
| SPARC-sized boost | δa ≥ 10⁻³ a₀ where g_N = a₀ | 3.451e-22 (FAIL) |
| Monotonic depth gate vs X-COP | Ξ on for a galaxy and off for a cluster | impossible (FAIL) |

κ capped by Mercury is 3.670344e-11. The fractional radial correction is 2.973407e-12 at every radius. At a 10¹¹ M_☉, 10 kpc point that is an extra 4.145e-22 m/s² on top of g_N = 1.394e-10 m/s².

Setting κ so the boost is order a₀ (1.234390e+01) produces 5.381e+11 mas/century at Mercury.

## Depth axis (|Φ|/c²), shallow to deep

- saturn_solar: 1.039010e-09
- mercury_solar: 2.549897e-08
- galaxy_200kms_disk: 4.450600e-07
- cluster_1000kms: 1.112650e-05

Any nondecreasing function of this axis that reaches a galactic MOND boost is at least that large on a cluster. Gate 2 already killed that unscreened regime at median R_200 = 0.608–0.621. This run does not replace that hydrostatic solve.

## Verdict

[X] for Xi = 1 and for every monotonic Xi(|Phi|/c^2). The Mercury cap leaves a fractional correction far below a0, so SPARC is untouched. A coupling large enough for an order-unity MOND boost violates the perihelion budget. Cluster |Phi| is deeper than galactic |Phi|, so a nondecreasing depth gate that is on for SPARC is on for X-COP, where Gate 2 already records med R200 = 0.608-0.621. A window between those depths needs two new dimensionful edges and fails the uniqueness line. The 12-cluster hydrostatic system was not refit.

## Not done in this run

- No refit of the 175 SPARC rotation curves. The capped extra acceleration is 2.973e-12 of g_N, below any χ² the ledger can see.
- No refit of the 12 X-COP hydrostatic equilibria.
- No new Cassini Doppler reduction. Q₂ here is the curvature |δa|/r² of this solution, scored against the published 5.2×10⁻²⁷ s⁻² cap.
- No covariant Lagrangian. Contracting S_ij with a fixed external tensor privileges the galactic frame. The 2026-11-18 separability note already recorded that this is not a local scalar.
- No Lean proof. The finite-difference residual is a numerical receipt, tier [D]. The monotonicity obstruction is arithmetic on the four depths, tier [D].
- No commit and no push.
