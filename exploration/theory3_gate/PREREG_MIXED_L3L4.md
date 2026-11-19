# Pre-registration: mixed cubic + quartic Galileon on the AeST scalar (2026-11-18)

Written and committed before any mixed-L₃L₄ number is computed.

**Model.** The live AeST scalar law (total law x μ_std(x) = y, λ_s ∈ {0.5, 1, 3}), plus cubic (κ₃) and quartic (κ₄) Galileon terms on φ. Spherical flux: f(s) + K₃ s²/r + K₄ s³/r² = q, with K₃ = 2κ₃a₀ₘ and K₄ = 2κ₄a₀ₘ². The bookkeeping (screened solar system, a₀ₘ = η a₀,fit) is the same as `door_nested_solution.py`.

**Method.** A spherical background around the Sun, from the isotropic parts of the external-field AQUAL term, the cubic and quartic self terms, and the mixed term 6κ₄ cof(H):T (which acts as an effective cubic κ₄ tr T). On top of it, the first-order ℓ = 2 response with all anisotropic sources:
- the external-field anisotropy L;
- the Galaxy's cubic cofactor 2κ₃(tr T − T) and quartic cofactor 6κ₄ cof(T);
- the mixed source 6κ₄ cof(H₀):T.

T is the Milky Way scalar Hessian at R☉ and is triaxial: radial a₀ₘs′, azimuthal a₀ₘs/R, and vertical from the AQUAL midplane balance with ρ₀ = 0.1 M☉ pc⁻³. Directions: Galactic centre and Galactic north pole in ecliptic coordinates.

**Gates, in order (cheapest first).**
1. R☉ gate:
   - the model's own Milky Way gives g(R☉) ∈ [1.9, 2.4]×10⁻¹⁰ m s⁻²;
   - the linearised principal symbol around the Sun is positive definite at every sampled direction and at radii from R☉ to 10 r_V.
2. Sun gate:
   - Mercury precession ≤ 1.6 mas/cy;
   - Saturn Q₂_eff ∈ [−2, 5.2]×10⁻²⁷ s⁻² at g_e = 1.9 and 2.4×10⁻¹⁰.
   - **Screen:** a point counts as a candidate only if |Q₂_eff| ≤ 2.6×10⁻²⁷, half the upper bound, because the calculation is first order.
3. SPARC gate: Δχ² ≤ 0 against the live μ_std baseline, with Υ refit under a 0.1 dex prior. Run only on candidates that pass gates 1–2.

**Regressions, before the scan.**
- (a) At K₃ = 0 and T = 0, the ℓ = 2 ODE leak against the exact stretched cone, for σ ∈ {1.05, 1.5, 2, 3, 4}. Report the first-order error.
- (b) At K₃ = 0, the SPARC solver reproduces rows of `DOOR_NESTED_SOLUTION.json`.

**Grid.** λ_s ∈ {0.5, 1, 3}; K₄ = 10³⁸…10⁴¹ m² (7 points); K₃/K₄ = 10⁻²²…10⁻¹⁶ m⁻¹ (13 points).

**Side constraints, recorded for every candidate.**
- The GW170817 bound on Q₀ from K₄, via α_T ∝ r_V⁶ from `OPEN_DOOR_GATE.json`.
- Cubic braiding, α_B ≈ κ₃ c Q₀ H₀, at that Q₀.

**Stop rule.**
- If no grid point passes gates 1–3 under the half-bound screen, mixed L₃ + L₄ is recorded as closed [O] at first order, and the work moves to the symmetron route.
- If a candidate survives, it is not called open until a 2D axisymmetric nonlinear solve confirms it.
