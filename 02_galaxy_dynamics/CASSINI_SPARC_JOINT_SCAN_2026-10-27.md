# Joint Cassini × SPARC scan, 2026-10-27

Pre-registration: `CASSINI_SPARC_JOINT_SCAN_PREREG_2026-10-27.md` (commit `6be3885`, written before any number).
Script: `cassini_sparc_joint_scan.py`. Output: `CASSINI_SPARC_JOINT_SCAN.json` (320 rows; per-row stream in `CASSINI_SPARC_JOINT_SCAN.partial.jsonl`).
Cassini: `qumond_axisym_efe.py` (QUMOND, axisymmetric EFE; PR #194), band [−2, 5.2]×10⁻²⁷ s⁻², pass at both external fields.
SPARC: the frozen Batch-1A gate (`FROZEN_BATCH1A.json`, |Δ reduced χ²| < 1 against the ν₂ baseline, tier 0 and tier 1, median and aggregate). Data, nuisance policy and gate unchanged.
a₀: fitted 1.1607×10⁻¹⁰, derived 1.0422×10⁻¹⁰ m s⁻².

## Result `[D]` within these three families only

**No grid point passes both gates (verdict `NO_JOINT_POINT`).** 320 rows, 0 errors, 22 inadmissible (non-monotone or wrong limits, per the pre-registered admissibility test).

| family | admissible rows | Cassini pass | SPARC pass | joint |
|---|---|---|---|---|
| (a) ν_n, n ∈ [1, 10] step 0.25 | 74 | 42 | 2 | 0 |
| (b) ν_{γ,β} (Milgrom–Sanders / McGaugh union) | 146 | 17 | 0 | 0 |
| (c) tail-cut ν_n (diagnostic) | 78 | 4 | 18 | 0 |

**Family (a), root-found boundaries.** The SPARC window is n ∈ [1.960, 2.041] (fitted a₀) and [1.966, 2.036] (derived): only ν_n ≈ ν₂ passes, since the gate is defined against ν₂. The Cassini edge is n = 5.392 (fitted) and 4.357 (derived). Separation: 3.35 and 2.32 in n. Within (a) the gates are disjoint by a wide margin; the binding SPARC term for every Cassini-passing n is tier-0 aggregate, |Δ| = 28–37.

**Closest approach: family (b) at (γ, β) = (6.0, 0.25), derived a₀.**
- Cassini: Q₂_max = 4.24×10⁻²⁷, **pass**.
- SPARC: tier-0 median 0.824, tier-0 aggregate 0.187, tier-1 median 0.128 (all pass); **tier-1 aggregate 1.298, fail** (gate 1).
- At fitted a₀ the same shape fails Cassini (7.48×10⁻²⁷) and passes all SPARC terms except tier-1 aggregate (1.28).
This is the only Cassini-passing point within a factor ~1.3 of the SPARC gate. The (b) grid is coarse there (γ ∈ {5, 6, 8}, β step 0.25).

**Family (c)** separates the regimes cleanly: the tail-cut keeps SPARC (best Cassini among SPARC passes: Q₂ = 1.71×10⁻²⁶ at (2.0, 10), a fail) or keeps Cassini (best SPARC among Cassini passes: max|Δ| = 10.4 at (1.5, 1.0)), never both.

## What this does and does not say

- It is a statement about these three families on this grid, at QUMOND level. It is not a no-go theorem for all interpolating functions, and says nothing about AeST or λ_s (#187).
- The SPARC gate is relative to ν₂ (|Δχ²_red| < 1). A shape that fits SPARC as well as other MOND functions but differently from ν₂ fails it by construction; the tier-1 aggregate miss at (6.0, 0.25) is 0.30 over that line.
- `[O]` next: a pre-registered refinement of family (b) around (γ, β) = (6, 0.25) with derived a₀, and a check of whether the tier-1 aggregate term is dominated by a few galaxies.

## Fix made during the run

The first two runs crashed: `nu_minus_1` in `qumond_axisym_efe.py` indexed its output as an array, so a scalar call from the tail-cut family raised `TypeError`, and `Pool.map` discarded the whole grid. `nu_minus_1` now accepts scalars (`test_qumond_axisym_efe.py`: 3 groups OK), and the scan streams rows to JSONL and records per-job errors instead of aborting. No pre-registered quantity changed. Runtime 2944 s.
