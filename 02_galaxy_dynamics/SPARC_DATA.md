# SPARC data provenance

## What is in git

Scripts and frozen JSON under `02_galaxy_dynamics/`. Rotation-curve tables are **not** committed to git and are ignored via `.gitignore` (`02_galaxy_dynamics/sparc_data/`, `*.zip`).

## Data resolution (`sparc_paths.py`)

All scripts in `02_galaxy_dynamics/` resolve the SPARC data directory dynamically via `sparc_paths.py` in the following priority order:

1. CLI argument `--data-dir <DIR>` if provided
2. Environment variable `SPARC_DATA_DIR` (or `SPARC_DATA`)
3. Repo-local `02_galaxy_dynamics/sparc_data/`
4. Current working directory `./sparc_data/`
5. Legacy fallback `/home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data`

If no directory containing `*_rotmod.dat` is found, a clear `FileNotFoundError` is raised listing all tried paths.

For optional per-galaxy published distance and inclination errors, `a0_measure.py` accepts `--meta <CSV>` or `SPARC_META_CSV`. If absent, it runs with standard default priors (10% distance, 5° inclination; `has_meta=false`).

## How to obtain SPARC

Primary source: Lelli, McGaugh & Schombert 2016, *AJ* 152, 157. Official distribution URL: `https://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip`.

To fetch and verify the official dataset into the repo-local directory:

```bash
# Automated fetch and verification script
bash 02_galaxy_dynamics/fetch_sparc.sh
```

The automated script performs the following operations:
1. Downloads `https://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip` into `02_galaxy_dynamics/sparc_data/`.
2. Extracts all 175 `*_rotmod.dat` rotation curve tables.
3. Automatically verifies each file against the authoritative SHA-256 manifest at `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256`.
4. Fails loudly (`exit 1`) if the file count differs from 175 or if any checksum drifts.

The SHA-256 manifest for all 175 `*_rotmod.dat` files is tracked at
`VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256` (an identical copy sits at
`VERIFICATION_RUN_001/03_sparc_nuisance_175/`). It is the authority for what "the SPARC input
corpus" means here; any file set that does not verify against it is a different corpus.

Total files downloaded: **175 `*_rotmod.dat` rotation curve tables**.

## Citable measurement standard

The data directory is gitignored to avoid vendoring public datasets without license modifications. The frozen `[D]` JSON artifacts on `main` (`02_galaxy_dynamics/A0_MEASUREMENT.json`, `PARAMETER_LEDGER.json`, `NFW_CONSTRAINED.json`, `HALO_CONSPIRACY.json`, `A0_ESTIMATE.json`) remain the citable empirical measurements from commit `3c90ef3e` / v1.5.0 seal until a new run is explicitly ledgered.
