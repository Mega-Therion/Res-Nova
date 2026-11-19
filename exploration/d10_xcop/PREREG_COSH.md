# Pre-registration: X-COP R₂₀₀ with the corpus's own Cosh 𝒦(𝒬) (2026-11-19, before any number)

**Question.** Every D10 solve so far used the quadratic limit 𝒦₂(𝒬−Q₀)² of the dust sector, an n = 1 polytrope whose mass grows 2.1× faster than NFW between R₅₀₀ and R₂₀₀. The corpus's live cosmological function is the SZ Cosh form (`CoshCosmology.lean`, `TARGET_D5`), 𝒦 = 2𝒦₂𝒵₀²[cosh((𝒬−Q₀)/𝒵₀) − 1], with r ≡ 𝒵₀/Q₀ allowed in 2.5×10⁻⁸ ≪ r ≲ 2×10⁻². Does Cosh, with nothing else changed, remove the ~25% R₂₀₀ overshoot?

**Model.** Identical to `xcop_screened_full.py` (Test C: x_H on the full solved field, x_H,low = 154, μ = 1/0.9895 Mpc, Φ(r_v) = 0, cosmic supply cap 5.36 M_b). Only the dust source changes:
- quadratic: −μ²r²Φ  →  Cosh: μ²r² Φ_c sinh(−Φ/Φ_c), Φ_c = c² r. Reduces to quadratic as r → ∞.

**Grid (fixed in advance, no interpolation, no refinement after seeing numbers):** r ∈ {∞ (control), 1e-3, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6}.

**Control.** r = ∞ must reproduce Test C (R₅₀₀ = 0.922, R₂₀₀ = 0.755) to ±0.01, else the run is void.

**Pass rule (per r).** Capped R₅₀₀ AND R₂₀₀ both have median in [0.8, 1.25] with ≥ 9/12 in [0.7, 1.4], every cluster's BVP converges, and r lies in the D5 window.

**Reporting.** All r reported. If a passing r exists it is a cluster-calibrated value of an existing constant, `[O]` until checked against an independent observable (D5 MPS cutoff, groups). If none passes, the Cosh concentration route is `[X]` for R₂₀₀.
