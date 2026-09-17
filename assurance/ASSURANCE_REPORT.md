# Res-Nova Assurance Report

Generated at (UTC): `2026-09-17T08:11:27.396924+00:00`  
Git commit: `934b7eee88ac4f4cb028cc096c63ecf37fbed897`  
Lean targets on disk excluding `lakefile.lean`: **48**  
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

**STALE** — `05_lean_formalization/` has changed since the last recorded run (tree `f0c6004384451c428a87668ebc327a8939f329b7980c4265e96468abbac37bfd` then, `20d32a1b0d21f074027c2b28642f0f6d3e10f0967bf57d0fac15549454320b26` now). Rerun the gate; a previous PASS is evidence only for the sources it was run against.

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
