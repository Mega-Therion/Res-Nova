# SPARC data provenance

## What is in git

Scripts and frozen JSON under `02_galaxy_dynamics/`. Rotation-curve tables are **not** in this repository.

## What the scripts currently assume

Hardcoded author-machine paths (defect, open O5):

- `/home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data` — `*_rotmod.dat`
- `/tmp/claude-1000/-home-mega/1c65399a-35d8-432b-881b-84d118b9952e/scratchpad/corpus_flat.csv` — published D/`i` errors used by `a0_measure.py`

A referee without those paths cannot regenerate `A0_MEASUREMENT.json` from this clone alone. The JSON remains the citable `[D]` artifact of commit `3c90ef3e`.

## How to obtain SPARC

Primary source: Lelli, McGaugh & Schombert 2016, *AJ* 152, 157. Rotation-curve compilation: SPARC (`*_rotmod.dat`). Use the official distribution; do not scrape mirrors of unknown hash.

Until `SPARC_DATA_DIR` is wired, pass directories only if you edit the scripts locally. Do not commit SPARC binaries unless licensing is checked and SHA-256 sums are listed here.

## Reproduction without data

You can still audit:

- the method, in the Python docstrings
- the frozen numbers, in the JSON
- the claim hygiene, with `python3 scripts/check_claim_consistency.py`
