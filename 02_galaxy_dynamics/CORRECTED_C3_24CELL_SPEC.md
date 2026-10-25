# Corrected C3 24-cell re-run

Written before the run. The original C3 collocation scripts named on BLK-714 are not in this checkout. This file is the contract that is executed instead. It does not claim to be those scripts.

## Split in the header

Defect D-1: the flux split that is run is K = η · η_e with Ĝ = η G_N and η = λ_s / (1 + λ_s). The superseded split K = (1 − η) η_e is not used. At λ_s = 1 the two expressions for K are equal. That identity is not a substitute for the integral.

## What is integrated

Each cell builds a spherical quasistatic ν(y), y = g_N / a₀, and passes it to `Q2` in `efe_quadrupole_q2.py` (Hees et al. 2016 eq. 10 and eq. 12).

- J_D9: J′ = λ_s μ_std(g_φ / ((1+λ_s) a₀)), g = η g_N + g_φ, with μ_std(z) = z / √(1+z²). This is the scalar-channel function in `scripts/aest_total_scalar_correspondence.py`.
- J_total: the correspondence total law x μ_std(x) = g_N / a₀. On that law the spherical ν does not depend on λ_s. The λ_s axis is still filled, three identical copies, so a λ_s-blind total law is visible in the grid rather than dropped.

This is not the unpublished LGL collocation. A match to the Block figure 2.138×10⁻²⁶ s⁻² is not assumed.

## Frozen grid (24 cells)

- branch ∈ {J_D9, J_total}
- λ_s ∈ {0.1, 1, 2} (the three values BLK-685 quotes for the corrected C3 numbers)
- a₀ ∈ {1.1607×10⁻¹⁰, 1.0422×10⁻¹⁰} m s⁻² (fitted, derived), as pinned on BLK-714
- g_e ∈ {1.9×10⁻¹⁰, 2.4×10⁻¹⁰} m s⁻²

2 × 3 × 2 × 2 = 24. No extra λ_s after the numbers print.

## Frozen verdict

Window pinned on BLK-714: Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻².

σ = (Q₂ − 1.6×10⁻²⁷) / 1.8×10⁻²⁷.

A cell is INSIDE if |Q₂ − 1.6×10⁻²⁷| ≤ 1.8×10⁻²⁷, and OUTSIDE otherwise.

Grid verdict, fixed now:

- ALL_INSIDE if all 24 cells are INSIDE
- NONE_INSIDE if none are
- MIXED otherwise

O1–O6 from the missing branch-gate design are not relabeled onto this verdict.

The JSON records every cell. The script and the JSON are hashed after the run. No second grid.
