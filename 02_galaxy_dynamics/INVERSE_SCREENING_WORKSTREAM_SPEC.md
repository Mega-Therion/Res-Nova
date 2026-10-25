# Inverse-screening workstream, batch 1

Written 2026-10-24 before the batch 1 run. The Muse draft named in BLK-720 and BLK-721 is not on disk. This file is the contract that run uses. It does not adopt a screening law and it does not change a claim status.

## What is being asked

BLK-720 adopts one workstream: an inverse problem whose output is a target specification. A covariant action, a variation, and a stability check are still required before any status attaches. ν₆ is not reopened as a galaxy law. The collar sector is out of scope.

## Frozen family

Unscreened shape is the standard interpolating function, written as the Hees ν₂ used in `efe_quadrupole_q2.py`:

ν₂(y) = (½ (1 + √(1 + 4/y²)))^(1/2)

One-parameter screening operator, fixed before the run:

ν_s(y) = 1 + (ν₂(y) − 1) / (1 + (y/s)²)

y = g_N / a₀. a₀ is the derived value `A0_DERIVED` in `efe_quadrupole_q2.py` (c H₀ / 2π with the constants already in that file). s → ∞ is bare ν₂. Smaller s cuts the MOND boost off at lower y.

No other family is evaluated in this batch. G-C2 and G-C6 are not ansatz rows in this run.

## Frozen grid

s ∈ {0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, ∞}

∞ is the baseline. The grid is not refined after the numbers are seen.

## Frozen gates

SPARC: Tier 0 only. Stellar mass-to-light and distance are the ledger prior means (`parameter_ledger`: Υ_d, Υ_b, f_d = 1). Per galaxy, reduced χ² uses the same `chi2` as `cassini_sparc_joint.py`. The summary statistic is the median of those reduced χ² values over every galaxy the loader returns.

Δ is (median reduced χ² at s) minus (median reduced χ² at ∞).

Cassini: Q₂ from `Q2(ν, a₀, g_e)` at g_e = 1.9×10⁻¹⁰ m s⁻². The window is the 2σ reading of the Hees et al. interval already stated in `efe_quadrupole_q2.py`, Q₂ = (3 ± 3)×10⁻²⁷ s⁻², so Q₂ ∈ [−3, 9]×10⁻²⁷ s⁻². The (1.6 ± 1.8)×10⁻²⁷ figure quoted on The Block is not in a local spec and is not the pass rule.

A grid point passes only if both hold:

1. |Δ| < 1
2. Q₂ is inside the window above

The inverse result is the smallest finite s on the grid that passes. If none pass, the result is that this family has no joint point. That is the batch outcome. There is no second grid.

## What the JSON may claim

The JSON records counts, medians, Q₂, and pass/fail against the two gates. It is a target-specification probe of this one operator. It is not a covariant action and not a replacement for the SPARC ν₆ failure.
