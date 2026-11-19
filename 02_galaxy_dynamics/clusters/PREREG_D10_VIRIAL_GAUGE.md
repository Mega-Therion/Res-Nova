# Pre-registration: fix the D10 μ²Φ gauge at the x_H virial boundary (2026-11-19, before any number)

**Why.** D10 §10 found the first-order AeST μ²Φ correction to the cluster mass is gauge-dependent: median R is 1.13 under Φ(r₅₀₀) = 0 and 0.66 under Φ(0) = 0. Neither choice is physical.

**The fix (from today's tidal-AeST work).** The x_H ≥ 154 virial cut marks where a collapsed structure detaches from the linear, Hubble-flow background. Linear growth is ΛCDM-identical there, so the AeST perturbation potential is zero outside it.

**Gauge C.** Φ(r_v) = 0, where r_v is the radius at which the mean enclosed lensing density is 154/(√3/2) = 177.8 ρ_c(z).
- r_v is obtained from the weak-lensing M₂₀₀ by r_v = r₂₀₀ (200/177.8)^{1/3}, assuming a flat enclosed-density slope between Δ = 200 and 178 (stated approximation).
- The baryon profile (cored, r_c = 0.1 r₅₀₀) and everything else are as in `d10_gauge_test.py`.

**Decision, fixed in advance.**
- Report the median W/W₀ − 1 (the expansion parameter) and the median R(+μ²) at r₅₀₀.
- **Closes at first order:** median R in [0.8, 1.25] AND expansion parameter < 0.5.
- **Inconclusive:** R in range but expansion parameter ≥ 0.5, so first order is not trustworthy.
- **Fails:** R outside [0.8, 1.25].
