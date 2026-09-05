# Res-Nova Assurance Capability Map

This map is the index for the assurance-hardening initiative. Module IDs are stable and the dependency arrows point from provider to consumer.

| Module ID | Responsibility | Depends on |
|---|---|---|
| `assurance-contract` | Define evidence levels, claim states, required witnesses, and forbidden promotions | — |
| `claim-registry` | Give headline scientific and formal claims stable IDs and machine-readable evidence links | `assurance-contract` |
| `formal-gate` | Harden Lean target inventory, assumption reporting, vacuity checks, and reproducible environments | `assurance-contract` |
| `empirical-repro` | Make SPARC inputs, tiers, fits, uncertainty, and independent rechecks reproducible | `assurance-contract`, `claim-registry` |
| `manuscript-drift` | Keep source prose, PDFs, manifests, inventories, and code synchronized | `claim-registry`, `formal-gate`, `empirical-repro` |
| `independent-review` | Run adversarial checks, alternative calculations, and claim-calibration rubrics | All preceding modules |
| `release-bundle` | Produce a versioned publication and reproduction package with an assurance report | All preceding modules |

## Build order

`assurance-contract` → (`claim-registry`, `formal-gate`, `empirical-repro`) → `manuscript-drift` → `independent-review` → `release-bundle`.

## Boundary rule

A repository mechanism may promote a claim only within the evidence class it actually checks. Lean elaboration verifies a formal artifact under its hypotheses; it does not validate physical assumptions. A numerical fit verifies a computation against declared data and code; it does not establish causality or universality. A publication PDF is a release surface, not an independent witness.

## Acceptance

Every module must have a specification, executable verification command, and a reportable failure state before it can be considered complete.
