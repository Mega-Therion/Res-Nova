# Pre-registration: Cassini as an a₀ discriminator, 2026-10-27

Written and committed before any number from this run. Follows `CASSINI_SPARC_JOINT_SCAN_2026-10-27.md`
(no joint point at fixed a₀; ν_{6,0.25} passes Cassini at derived a₀ but not fitted a₀).

## Question

The joint scan held a₀ at two values. Here a₀ is free. For each shape, where in a₀ does Cassini
start to fail, and where in a₀ does SPARC fit? If, for the shapes SPARC accepts, the Cassini edge
sits between 1.0422 and 1.1607 ×10⁻¹⁰ m s⁻², Cassini separates the two a₀ values. a₀ stays one of the
two irreducible parameters; this asks which value the data allow, not whether it can be derived.

## Fixed inputs (unchanged from the joint scan)

- Cassini: `qumond_axisym_efe.Q2_richardson`, grid resolution n_r=2000, n_th=100; g_e ∈ {1.9, 2.4}×10⁻¹⁰;
  band [−2, 5.2]×10⁻²⁷ s⁻²; PASS/FAIL/INCONCLUSIVE with the same 3σ-of-Richardson-error rule.
- SPARC: `cassini_sparc_joint.fit/summ`, tiers 0 and 1, same data, nuisance priors, galaxy list.
- Admissibility test: same as the joint scan.

## Grid

- a₀ ∈ {0.90, 0.925, …, 1.30}×10⁻¹⁰ (17 values), plus the two named values 1.0422 and 1.1607 (19 total).
- Shapes (12): ν_n for n ∈ {2, 3, 4, 5, 6}; ν_{γ,β} at (5, 0.25), (6, 0), (6, 0.25), (6, 0.5), (8, 0.25);
  tail-cut ν_n at (2.0, 10) and (2.0, 3.1623).

## Quantities

1. **Cassini edge a₀\*_C(shape):** the a₀ at which max over g_e of Q₂ crosses 5.2×10⁻²⁷, root-found with
   brentq inside each bracketing grid interval. All crossings are reported; none are dropped.
2. **SPARC reference:** ν₂ at its own best a₀ (the grid a₀ minimising ν₂'s tier-1 aggregate). Its four
   summaries (tier-0/1, median/aggregate reduced χ²) are the reference R.
3. **SPARC acceptance, best-a₀-relative:** a (shape, a₀) passes if all four summaries are within 1 of R.
   This is a second gate. It does not replace the frozen Batch-1A gate (ν₂ at fixed a₀). The frozen-gate Δ is
   also reported at 1.0422 and 1.1607.
4. **SPARC preferred a₀:** for each shape, the grid a₀ minimising its tier-1 aggregate.

## Verdicts (decided before the run)

- `A0_DISCRIMINATES`: at least one (shape, a₀) passes both gates, and at every such shape the joint
  a₀ interval contains exactly one of {1.0422, 1.1607}, the same one for all shapes.
- `JOINT_REGION`: points pass both gates, but the two named a₀ are not separated as above.
- `NO_JOINT_REGION`: no (shape, a₀) passes both gates on this grid.

Separately, and whatever the verdict: for every shape, report whether a₀\*_C lies below 1.0422,
between the two values, or above 1.1607.

## Limits stated now

QUMOND level, these 12 shapes, this a₀ grid. Not a statement about AeST, λ_s, or other shapes.
The best-a₀-relative gate is my choice made here; reporting it next to the frozen gate is the guard against
choosing a gate after seeing the numbers.
