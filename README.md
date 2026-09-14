# Res-Nova

Technical manuscript, formal verification, and reproducibility package.

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
