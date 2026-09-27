# Res-Nova Assurance Report

Generated at (UTC): `2026-09-27T23:51:20.284099+00:00`  
Git commit: `a72e947cc3d296de44d96a2d131510e53b1389af`  
Lean targets on disk excluding `lakefile.lean`: **63**  
Registry records: **43**

## Checks

| Check | Status |
|---|---|
| `claim_registry` | **PASS** |
| `claim_consistency` | **PASS** |
| `lean_target_inventory` | **PASS** |
| `manuscript_inventory` | **PASS** |

## Claim states

| State | Count |
|---|---:|
| `computed` | 6 |
| `conditional` | 7 |
| `derived` | 10 |
| `formally-verified` | 8 |
| `proposed` | 2 |
| `retracted` | 10 |

## Lean gate

**STALE** — `05_lean_formalization/` has changed since the last recorded run (tree `f0c6004384451c428a87668ebc327a8939f329b7980c4265e96468abbac37bfd` then, `1db3a4cbb60e3db8abf6b80211ef5d12e80e04f503fbea8ed82594dd9d14763b` now). Rerun the gate; a previous PASS is evidence only for the sources it was run against.

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
