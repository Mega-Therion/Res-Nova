# Where to start

This page is a map. It does not delete the audit notes at the repository root, and it does not change a claim tier.

## The paper and the numbers

- The four blocks and the closed channels: [`FRONT.md`](../FRONT.md). This map does not change a tier.
- Claim status, with dates: [`CURRENT_STATE_READ_THIS_FIRST.md`](../CURRENT_STATE_READ_THIS_FIRST.md).
- Headline numbers: [`RESULTS.md`](../RESULTS.md). `./reproduce_core_results.sh` regenerates them from the SPARC data in an offline copy.
- What was checked or broken from outside: [`CHECKS.md`](../CHECKS.md).
- Claim tags: [`docs/EPISTEMIC_TIER_LEGEND.md`](EPISTEMIC_TIER_LEGEND.md).
- Machine-readable registry: [`assurance/claims.json`](../assurance/claims.json).
- Zenodo concept DOI: [10.5281/zenodo.21539453](https://doi.org/10.5281/zenodo.21539453).

Killed claims stay in the record as `[X]`, with the date on the note that killed them. The README section "What was killed" is the short list. `CURRENT_STATE_READ_THIS_FIRST.md` is the long list.

## The two `06_` directories

Both stay. They are not duplicates of one folder.

- `06_foundations/` holds foundation notes, including external-field screening (`SETA_EXTERNAL_FIELD_SCREENING.md`).
- `06_unification_and_spin/` holds the unification and spin notes, including `e8_algebraic_sweep.py`.

Numbered lanes `01_` through `05_` are the action, galaxy dynamics, high-redshift samples, cosmology, and the Lean tree.
