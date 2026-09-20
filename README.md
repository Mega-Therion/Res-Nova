# Res-Nova

<p align="left">
  <a href="https://doi.org/10.5281/zenodo.21539453"><img src="https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.21539453-024dad?style=flat-square&logo=doi&logoColor=white" alt="Zenodo concept DOI"></a>
  <a href="https://resnova-hub-f4ucvy3e.manus.space"><img src="https://img.shields.io/badge/Research%20Atlas-resnova--hub-0070f3?style=flat-square&logo=safari&logoColor=white" alt="Res Nova Atlas"></a>
  <a href="https://huggingface.co/datasets/ChyRho/res-nova"><img src="https://img.shields.io/badge/Hugging%20Face-ChyRho%2Fres--nova-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="Hugging Face Dataset"></a>
  <a href="https://orcid.org/0009-0001-1303-7190"><img src="https://img.shields.io/badge/ORCID-0009--0001--1303--7190-A6CE39?style=flat-square&logo=orcid&logoColor=white" alt="ORCID"></a>
  <a href="https://www.linkedin.com/in/r-w-yett-152085293/"><img src="https://img.shields.io/badge/LinkedIn-R.W._Yett-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://x.com/_chyrho_"><img src="https://img.shields.io/badge/X-@__ChyRho__-000000?style=flat-square&logo=x&logoColor=white" alt="X"></a>
</p>

Technical manuscript, formal verification, and reproducibility package.

## Citation

**Canonical citation** — cite the concept DOI when you mean the work. It always
resolves to the newest version.

> Yett, R. W. (2026). *Res Nova: Geometrically Ordered Dynamics and Information
> Tension.* Zenodo. https://doi.org/10.5281/zenodo.21539453

| | |
| :--- | :--- |
| Author | Ryan W. Yett |
| ORCID | [0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190) |
| Repository | [Mega-Therion/Res-Nova](https://github.com/Mega-Therion/Res-Nova) |
| Concept DOI (always latest) | [10.5281/zenodo.21539453](https://doi.org/10.5281/zenodo.21539453) |
| Current version DOI | [10.5281/zenodo.22079177](https://doi.org/10.5281/zenodo.22079177) |
| Current repository tag | `v1.9.0` |

### Version history

Zenodo mints a separate DOI for each published version and links the lineage.
Earlier DOIs remain valid and resolvable; they are the historical record, not
errors. The version family under concept `10.5281/zenodo.21539453` is:

| Version DOI | Version | Date |
| :--- | :--- | :--- |
| [22079177](https://doi.org/10.5281/zenodo.22079177) | current | 2026-08-24 |
| [21660856](https://doi.org/10.5281/zenodo.21660856) | 5.0.0 | 2026-07-28 |
| [21623111](https://doi.org/10.5281/zenodo.21623111) | 4.0.0 | 2026-07-27 |
| [21583646](https://doi.org/10.5281/zenodo.21583646) | earlier | — |
| [21544746](https://doi.org/10.5281/zenodo.21544746) | earlier | — |
| [21539454](https://doi.org/10.5281/zenodo.21539454) | earlier | — |

### Release archives

The GitHub release archives are a **separate** lineage from the manuscript. They
record the state of this repository at a tag, not the text of the paper:

| | |
| :--- | :--- |
| Release concept DOI | [10.5281/zenodo.21969120](https://doi.org/10.5281/zenodo.21969120) |
| Latest archived release | [10.5281/zenodo.21969121](https://doi.org/10.5281/zenodo.21969121) (`v1.6.2`) |

The repository is currently at `v1.9.0`, so the newest tags are not yet archived.
Do not cite a release archive when you mean the paper.

The authoritative list of every DOI in this project is
[`docs/publication_registry.yaml`](docs/publication_registry.yaml), generated
from DataCite and enforced by
[`scripts/audit_publication_metadata.py`](scripts/audit_publication_metadata.py).

![Res-Nova Evidence Atlas Lifecycle](visualizer/evidence-atlas-lifecycle.svg)

## Overview

Res-Nova houses the foundational physics manuscript on Geometrically Ordered Dynamics and Information Tension, accompanied by an explicit claim-evidence ledger, formal Lean inventories, cosmological and galactic sector analyses, and reproducibility harnesses.

## System Role & Boundaries

- **Technical Manuscript & Scientific Corpus**: Primary source repository for theory exposition, derivations, and observational comparisons.
- **Evidence Ledger**: Explicitly documents assumptions, derivation paths, and falsifiability criteria. A claim's presence in the ledger records auditability—it does not substitute for empirical consensus.
- **RYTT Boundary (Issue #48)**: Selected manuscript passages are supplied to RYTT strictly as benchmark corpora. Res-Nova does not fork or embed the RYTT compiler.
- **Auditor Boundary (Issue #50)**: Produces `evidence/v1/claim-ledger.json` for independent verification by MVPC-X. Res-Nova does not maintain the verification engine.

## Active Workstreams

- **Issue #50**: Evidence Atlas v1 — machine-readable versioned claim registry with commit-pinned provenance and fail-closed reproducibility gates (`evidence/v1/claim-ledger.json`).
- **Issue #48**: Supply Res-Nova manuscript text as RYTT benchmark fixtures only.

## Acceleration Scale

The working value, fitted over 171 SPARC galaxies / 3375 points under
`tau(g) = 1/2 + sqrt(1/4 + a0/g)` with per-galaxy published distance and
inclination errors (`02_galaxy_dynamics/A0_MEASUREMENT.json`):

`a0 = (1.116 \pm 0.128_{stat} \pm 0.097_{syst}) \times 10^{-10}\,\mathrm{m\,s^{-2}}` (14.4% total)

`a0` is an **empirical acceleration scale**. It is numerically close to `cH0/2pi`;
that closeness is an observation, **not** a derivation, and must not be quoted as one.

**SUPERSEDED** (do not quote as current): the earlier 176-parameter in-sample
headline `chi^2/N_g = 2.92` with `a0 = (9.433 \pm 0.050) \times 10^{-11}`. That error
bar treated 3391 radial points as independent, and the old 5-fold CV leaked a
single global `a0` into every test fold.

## Epistemic Standards

Claims are strictly classified according to recorded evidence:
- **`derived`**: Supported by explicit mathematical derivation and checked assumptions.
- **`empirically_supported`**: Correlated with identified observational datasets (e.g. SPARC, JWST) within defined scope.
- **`conditional`**: Dependent on unresolved model choices or theoretical assumptions.
- **`proposal` / `open`**: Active hypotheses, open problems, or pending calculations.
- **`refuted`**: Preserved contradiction records; never silently discarded.

## Verification & Reproducibility

```bash
# Run local quality and claim gate
bash scripts/local_gate.sh

# Validate claim registry consistency
python scripts/validate_claim_registry.py
python scripts/check_claim_consistency.py
```
