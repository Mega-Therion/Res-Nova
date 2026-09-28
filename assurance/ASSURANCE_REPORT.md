# Res-Nova Assurance Report

Generated at (UTC): `2026-09-28T00:01:27.938337+00:00`  
Git commit: `4d2b8cf37fd3a9c599733475a8c8a143032f3cf2`  
Lean targets on disk excluding `lakefile.lean`: **63**  
Registry records: **45**

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
| `computed` | 5 |
| `conditional` | 7 |
| `derived` | 11 |
| `formally-verified` | 9 |
| `proposed` | 2 |
| `retracted` | 11 |

## Lean gate

**STALE** — `05_lean_formalization/` has changed since the last recorded run (tree `f0c6004384451c428a87668ebc327a8939f329b7980c4265e96468abbac37bfd` then, `1db3a4cbb60e3db8abf6b80211ef5d12e80e04f503fbea8ed82594dd9d14763b` now). Rerun the gate; a previous PASS is evidence only for the sources it was run against.

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
