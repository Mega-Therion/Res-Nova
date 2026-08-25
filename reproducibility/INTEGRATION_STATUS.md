# Res-Nova Integration Status

**Date:** 2026-08-25
**Status:** Phase 0 freeze — partial automation, not full independent verification

## Canonical boundaries

- **Res-Nova** is the public research and reproducibility source of record.
- **MVPC-X** is the independently versioned public verifier.
- **Chyren-AEON** is the private orchestration and operator environment.

AEON may ingest public evidence bundles and invoke MVPC-X locally. AEON must not rewrite Res-Nova claims, elevate claim status, or become a dependency of this repository.

## Current state (do not overstate)

| Capability | Present? | Allowed language |
| --- | --- | --- |
| Claim-hygiene CI (scripts, fixtures, synthetic JWST self-test, Lean inventory) | Yes | Automated smoke and manifest validation |
| `scripts/run_mvpc_adapter.py` hash / `sorry` scan | Yes | Static integrity preflight only |
| Full MVPC-X assurance engine execution in this adapter | No | Must not be called independent verification |
| Full Lean reproduction in CI | No | Not a CI-gated Lean proof |
| `VERIFICATION_RUN_007` clean-worktree Lean run | Yes | `clean_worktree` PASS; promotion blocked for independent replication |
| Direct AEON integration reference | No (this document begins it) | Ingest-only, observe-first |

## Run-mode vocabulary

Do not conflate these:

- `self_test` — pipeline health
- `static_preflight` — hashes, schema, labels
- `local_verified` — declared local machine
- `clean_worktree` — clean repo/worktree
- `cold_environment` — fresh disposable environment
- `independent_replication` — distinct person or organization

`VERIFICATION_RUN_007` is registered as `clean_worktree` with `promotion=blocked_for_independent_replication`. It is not a CI gate and not an independent-reproduction claim.

## Compatibility decision (first bridge)

Until a reviewed upgrade record exists:

- Public Res-Nova profiles may declare a pinned MVPC-X version/commit in the lock file.
- A newer MVPC-X release must not silently change pins.
- Verdict changes require a human review record.

See `reproducibility/LEGACY_RUN_INDEX.json` for historical runs. Do not rewrite those directories.
