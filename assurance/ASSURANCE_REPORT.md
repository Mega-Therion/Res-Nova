# Res-Nova Assurance Report

Generated at (UTC): `2026-10-14T07:25:39.460354+00:00`  
Git commit: `d4f2b919405df2a6f1d073ae9070da22fc46dde5`  
Lean targets on disk excluding `lakefile.lean`: **69**  
Registry records: **58**

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
| `computed` | 10 |
| `conditional` | 9 |
| `derived` | 12 |
| `empirically-supported` | 1 |
| `formally-verified` | 9 |
| `proposed` | 2 |
| `retracted` | 15 |

## Lean gate

**STALE** — `05_lean_formalization/` has changed since the last recorded run (tree `a9ccc3fddf26c62716c3eef494dca911869e570cc00267f8b604ad45266f3474` then, `b6bcc21533daffb334956a79ee4d38561c3101a2531ef7ee4763b2503c4d8d82` now). Rerun the gate; a previous PASS is evidence only for the sources it was run against.

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
