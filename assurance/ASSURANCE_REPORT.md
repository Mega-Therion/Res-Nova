# Res-Nova Assurance Report

Generated at (UTC): `2026-10-09T16:30:24.525361+00:00`  
Git commit: `8d729b7252feb3b2ff1f24478696904f275828d8`  
Lean targets on disk excluding `lakefile.lean`: **66**  
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

`cd 05_lean_formalization && bash verify_all_proofs.sh` exited **0** at `5e1fa72af841c1478cab59e85629badf2a496877` (2026-10-09T06:35:55Z), 66/66 targets, Lean v4.33.0-rc1, Mathlib 5eec30bc.

Certifies: elaboration, absence of sorry, and a standard axiom footprint {propext, Classical.choice, Quot.sound}.

Does not certify: that assumptions carried as typeclass or structure fields are physically justified (THEORY_ASSUMPTION_AUDIT.md), nor cold-clone reproducibility (O6).

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
