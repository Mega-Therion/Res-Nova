# What counts as an experiment in this repo

Two numerical jobs are already on disk. They are not samples of a population, and they do not get a new factor grid.

## Inverse screening, already run

Question. On one frozen family, does any grid point keep the SPARC Tier-0 median reduced chi-squared within 1 of bare ν₂ and put Q₂ inside the Hees window.

Unit. One value of the screening parameter s. The integral is deterministic. Running it twice is a verification that the code did not change. It is not a second observation.

The grid was fixed in `INVERSE_SCREENING_WORKSTREAM_SPEC.md` before the run: s in {0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, ∞}. The result was no joint point. A new grid, a new family, or a fit of s after seeing that table is a different experiment and is not licensed by the first one.

Galaxies are not replicates of the Cassini integral. The median over galaxies is one summary of one global setting. Counting 171 galaxies as n = 171 for that Q₂ comparison is pseudoreplication.

## C3, 24 cells, already run as a spherical stand-in

Question. Under the corrected split K = η · η_e, how many of 24 pre-declared cells fall inside Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻².

Factors, crossed in full, no fraction:

- branch: J_D9, J_total
- λ_s: 0.1, 1, 2
- a₀: fitted 1.1607×10⁻¹⁰, derived 1.0422×10⁻¹⁰
- g_e: 1.9×10⁻¹⁰, 2.4×10⁻¹⁰

That is 2 × 3 × 2 × 2 = 24. The run is `CORRECTED_C3_24CELL.json`. Verdict on that solver: none of the 24 inside. J_total did not depend on λ_s in the spherical law, so those three λ_s copies are one calculation written three times. They are not three replicates.

The unpublished collocation solver is a different instrument. Re-running these 24 cells in that solver is a new experiment. It needs the same factor list written down before the run, and a second execution whose outputs match before anyone quotes a cell.

## Ledger list

`MU_STD_DUAL_OR_PADE_66.txt` is an inventory, not a design. Reading those files does not estimate an effect.
