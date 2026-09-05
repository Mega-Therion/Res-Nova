# Res-Nova Assurance Report

Generated at (UTC): `2026-09-05T01:15:48.017449+00:00`  
Git commit: `5808e098ce1cc8762af8bd89e41004d44b41be17`  
Lean targets on disk excluding `lakefile.lean`: **30**  
Registry records: **6**

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
| `computed` | 1 |
| `conditional` | 1 |
| `formally-verified` | 2 |
| `retracted` | 2 |

## Lean gate

`cd 05_lean_formalization && bash verify_all_proofs.sh` exited **0** at `cbb4717239e88b3c1d0e195a52f7864413374116` (2026-09-05T01:12:38Z), 30/30 targets, Lean v4.33.0-rc1, Mathlib 5eec30bc.

Certifies: elaboration, absence of sorry, and a standard axiom footprint {propext, Classical.choice, Quot.sound}.

Does not certify: that assumptions carried as typeclass or structure fields are physically justified (THEORY_ASSUMPTION_AUDIT.md), nor cold-clone reproducibility (O6).

## Limitations

- Lean verification certifies elaboration under encoded hypotheses, not physical truth.
- The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.
- The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.
