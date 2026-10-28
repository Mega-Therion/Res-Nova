# Cassini a₀ boundary sweep, 2026-10-27

Pre-registration: `CASSINI_A0_BOUNDARY_PREREG_2026-10-27.md` (commit `ec865aa`, before any number).
Script: `cassini_a0_boundary.py`. Output: `CASSINI_A0_BOUNDARY.json` (228 rows, 0 errors, 0 inadmissible; runtime 5798 s).
Cassini scorer, SPARC fitter, data and nuisance policy are the joint scan's, unchanged.

## Verdict `[D]` on this grid: `NO_JOINT_REGION`

No (shape, a₀) passes both Cassini and the best-a₀-relative SPARC gate (ν₂ at its own best grid a₀, 1.225×10⁻¹⁰,
as reference: tier-0 median 9.382, tier-0 aggregate 77.110, tier-1 median 3.347, tier-1 aggregate 6.035).

## Cassini edge in a₀ (where max Q₂ crosses 5.2×10⁻²⁷), per shape

| shape | Cassini edge a₀ (10⁻¹⁰) | position | SPARC-preferred a₀ (tier-1 agg) | min max\|Δ\| over Cassini-passing a₀ |
|---|---|---|---|---|
| ν₂, ν₃, tail-cut (2, 10), (2, 3.16) | none: Cassini fails at every grid a₀ | — | 1.175–1.225 | — |
| ν₄ | 0.989 | below derived | 1.25 | 53.2 |
| ν_{6,0.5} | 1.000 | below derived | 1.30 (grid edge) | 2.27 |
| ν_{5,0.25} | 1.014 | below derived | 1.15 | 20.7 |
| **ν_{6,0.25}** | **1.083** | **between** | 1.1607 | 13.2 |
| **ν₅** | **1.121** | **between** | 1.30 (grid edge) | 39.5 |
| ν_{8,0.25} | 1.167 | above fitted | 1.175 | 6.12 |
| ν₆ | 1.213 | above fitted | 1.25 | 29.9 |
| ν_{6,0} | 1.260 | above fitted | 1.30 (grid edge) | 25.3 |

Every shape has a single crossing: Cassini passes below the edge and fails above it.

## What the numbers say

- **For every shape, SPARC prefers an a₀ at or above that shape's Cassini edge.** The two gates pull a₀ in opposite
  directions within each shape, so freeing a₀ does not open a joint region; it generalises the joint scan's wall.
- **Cassini separates 1.0422 from 1.1607 only for shapes whose edge falls between them** (ν₅ and ν_{6,0.25} here), and in
  both cases it allows the derived value and excludes the fitted one. For the other shapes both values sit on the same side.
  So Cassini does not discriminate the two a₀ values shape-independently.
- **The best-a₀ gate is harsher than the frozen gate.** ν₂'s tier-0 aggregate drops from 93.6 (derived) and 82.1 (fitted)
  to 77.1 at a₀ = 1.225, so shapes measured against it lose margin. ν_{6,0.25} at derived a₀, the joint scan's near miss
  (frozen-gate max |Δ| 1.298), has max |Δ| 13.2 here.
- Frozen-gate check at the named a₀ (reported per pre-registration): Cassini-passing rows within 1.6 of the frozen gate are
  ν_{6,0.25} derived (1.30), ν_{8,0.25} fitted (1.45) and derived (1.57). None passes.

## Limits

QUMOND level, these 12 shapes, a₀ ∈ [0.90, 1.30]. Three shapes prefer a₀ at the grid's upper edge, so their preferred a₀
is a lower bound. The best-a₀-relative gate was chosen in the pre-registration; it is not the frozen Batch-1A gate.
Not a statement about AeST, λ_s (#187) or shapes outside this list.

## External comparison (added 2026-10-28)

The Cassini band here is the 2σ interval of Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻² (Park, Hees, Famaey, Desmond & Durakovic, arXiv:2602.17884 (v2 2026-07-28), Phys. Rev. D (2026), doi:10.1103/r7n8-kw38). Their abstract reports a 3–15σ tension between that bound and external galaxy rotation curves, depending on the mass modelling and the galaxy subset. That agrees with `NO_JOINT_REGION` and with the finding above that, shape by shape, SPARC prefers an a₀ at or above where Cassini fails. Only the galaxy side is an independent check; the Cassini side is their number.
