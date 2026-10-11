# Res-Nova Assurance Report

Generated at (UTC): `2026-10-11T22:03:41.157205+00:00`  
Git commit: `223c385779ee2f43dd83560a8e9ca2e0b1594cb7`  
Lean targets on disk excluding `lakefile.lean`: **67**  
Registry records: **57**

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
| `derived` | 11 |
| `empirically-supported` | 1 |
| `formally-verified` | 9 |
| `proposed` | 2 |
| `retracted` | 15 |

## Lean gate

**STALE** — `05_lean_formalization/` has changed since the last recorded run (tree `a9ccc3fddf26c62716c3eef494dca911869e570cc00267f8b604ad45266f3474` then, `99aafbc658b610679eba99edb402236e6278e115946ab32cfc1c986e21690631` now). Rerun the gate; a previous PASS is evidence only for the sources it was run against.

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
