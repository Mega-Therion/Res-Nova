# Res-Nova Assurance Report

Generated at (UTC): `2026-09-28T03:14:59.632919+00:00`  
Git commit: `9468978680a69910e9046c1cac1303109caa9ab6`  
Lean targets on disk excluding `lakefile.lean`: **63**  
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
| `conditional` | 7 |
| `derived` | 12 |
| `empirically-supported` | 1 |
| `formally-verified` | 9 |
| `proposed` | 2 |
| `retracted` | 11 |

## Lean gate

**STALE** — `05_lean_formalization/` has changed since the last recorded run (tree `f0c6004384451c428a87668ebc327a8939f329b7980c4265e96468abbac37bfd` then, `1db3a4cbb60e3db8abf6b80211ef5d12e80e04f503fbea8ed82594dd9d14763b` now). Rerun the gate; a previous PASS is evidence only for the sources it was run against.

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
