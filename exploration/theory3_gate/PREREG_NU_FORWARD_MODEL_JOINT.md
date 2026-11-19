# Pre-registration: Cassini × SPARC joint test for steep interpolating functions under the honest SPARC error model (2026-11-18)

Committed before any number from this test. Exploration, no tier change.

**Why.** Every screening class for the AeST scalar fails (this folder). The surviving lever is the interpolating function. The 2026-10-27 a₀-boundary sweep (`02_galaxy_dynamics/CASSINI_A0_BOUNDARY.json`) left near misses: ν₈,₀.₂₅ (Cassini edge 1.167, SPARC-preferred 1.175×10⁻¹⁰), ν₅, ν₆,₀.₂₅. Its SPARC side used the committed tier-1 fitter: correct √fd scaling, but a common 10% distance prior and no intrinsic scatter. The forward-model audit (#235) shows the data prefer per-galaxy e_D/D and σ_int = 5–7 km/s (Δ(−2 ln L) = −6979).

**Cassini side: unchanged.** Per-(shape, a₀) verdicts are taken from `CASSINI_A0_BOUNDARY.json` (QUMOND axisymmetric EFE, band [−2, 5.2]×10⁻²⁷ s⁻², both g_e). They do not depend on the SPARC pipeline.

**SPARC forward models.**
- **FM-A (regression):** the committed tier-1 fit (`cassini_sparc_joint.fit`, tier 1). It must reproduce the committed tier-1 aggregate for ν₂ at 1.225×10⁻¹⁰ to < 10⁻⁶ relative.
- **FM-B (primary):** tier-1 per galaxy (Υ_d, Υ_b if bulge, fd) with the committed Υ priors, plus:
  - per-galaxy distance prior fd ~ N(1, (e_D/D)²) from `SPARC_Lelli2016c.mrt`, bounds 1 ± 3.5 e_D/D, clipped to [0.3, 3];
  - Gaussian errors σ_V² + σ_int².
  - σ_int is profiled once, for ν₂ at its FM-B best grid a₀, over {0, 2, 4, 5, 6, 7, 8, 10} km/s (full −2 ln L with the log-det term). It is then held fixed for every shape and a₀.
  - All 175 galaxies; no inclination nuisance. The audit flagged edge-on hijack in S3/S4.

**Grid.**
- Shapes: ν₂ (reference), ν₅, ν₆, ν₆,₀ (b,(6,0)), ν₆,₀.₂₅, ν₈,₀.₂₅.
- a₀: the 19 values of `cassini_a0_boundary.A0_GRID`.

**Primary criterion (P1).** Δ(−2 ln L) = Σ_gal min[χ² + priors] − (the same for ν₂ at its FM-B best grid a₀) ≤ 10. With σ_int fixed, the log-det term is common to all models.

**Joint pass.** Cassini PASS at that (shape, a₀) and P1.

**Secondary (reported, not decisive).** The committed four-summary best-ref gate (|Δ| < 1), recomputed under FM-B errors.

**Stop rule.**
- If no (shape, a₀) is a joint pass, the interpolating-function route is closed under FM-B [O].
- If some pass, they are candidates only. Each must then pass, separately:
  - the AeST embedding (a non-folding total-scalar correspondence);
  - the Oort binding test (as `nu6_oort_binding.py`);
  - Mercury;
  - a stability check;
  
  before anything is called open.
