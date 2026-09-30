# Res-Nova Assurance Report

Generated at (UTC): `2026-09-30T19:57:23.131211+00:00`  
Git commit: `31453101db5acaf64bcb7bd0d5f08f7699a2e0d4`  
Lean targets on disk excluding `lakefile.lean`: **65**  
Registry records: **48**

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
| `conditional` | 8 |
| `derived` | 10 |
| `empirically-supported` | 1 |
| `formally-verified` | 9 |
| `proposed` | 2 |
| `retracted` | 12 |

## Lean gate

**STALE** — `05_lean_formalization/` has changed since the last recorded run (tree `f0c6004384451c428a87668ebc327a8939f329b7980c4265e96468abbac37bfd` then, `27756e02fcc9f6fc37fbf92077f2b89ec691848cfc5d3eb8d890e59b78c116fe` now). Rerun the gate; a previous PASS is evidence only for the sources it was run against.

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
