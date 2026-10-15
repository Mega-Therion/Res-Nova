# The three "Information Tension" field models, reconciled

**Status:** `[D]` (symbolic, `scripts/ttey_field_models.py`, 7/7, exit 0). No tier change; AeST not falsified.
**Date:** 2026-10-14
**Why:** before any TTEY paper can cohere, "Information Tension" must name one field, or an explicit set of related fields. The corpus uses the phrase for three mathematically distinct models. This maps them.

## The three models

| # | where | field equation | structure |
|---|---|---|---|
| 1 | AQUAL / galaxy sector (`SZStdEmbedding`, `TARGET_D7`) | `∇·[μ_std(\|∇φ\|/a₀) ∇φ] = 4πĜρ` | nonlinear kinetic, **no potential**, `φ` a potential (`[φ] = velocity²`), massless |
| 2 | TTEY warp stress tensor (`…/god_theory/physics_formalization/Tension_Stress_Energy_Tensor.md`) | `□𝒯 = V′(𝒯)`, `V = λ(𝒯² − χ²)²`, `χ = 1/√2` | canonical kinetic, double-well, `𝒯` dimensionless, **massive** |
| 3 | TTEY engineering (`PAPER_27`, `project_ttey_drive`) | `Δ𝒯 = κρ`, `ρ` a Dirac-spinor source | linear Poisson, dipole/steering modes |

## What reconciles, what does not

- **Models 1 and 3 are one field.** The Poisson equation (3) is exactly the Newtonian-regime limit of the AQUAL field (1): as `x = |∇φ|/a₀ → ∞`, `μ_std → 1`, so `∇·[μ_std ∇φ] → ∇²φ = source`. In the deep-MOND regime `x → 0`, `μ_std → x` and the same field goes nonlinear. So the galaxy field and the engineering Poisson field are the one Information-Tension field in two regimes. (`chk 1→3`, `chk 1`.)

- **Model 2 is a separate, postulated field.** The double-well `𝒯` has a symmetry-breaking potential the AQUAL field does not, a non-zero vacuum `𝒯 = χ`, and a **massive** excitation `m² = V″(χ) = 8λχ² > 0`. The AQUAL `φ` is massless and carries different dimensions (`velocity²` vs dimensionless). Nothing in the G.O.D./AeST action derives model 2; it is introduced in the stress-tensor note specifically to source a vacuum-relative (Casimir-type) negative energy for the warp bubble. (`chk 2`, `chk 1 vs 2`.)

## Consequence for TTEY

The warp route does not rest only on an energy-condition or quantum-inequality question. It rests first on an **existence** question: is the double-well `𝒯` a real sector of the theory, or an ansatz chosen to yield negative energy? Until `𝒯` is derived from the same action that gives the galaxy law (or declared, with justification, a new sector), the TTEY negative-energy construction is not grounded in the framework. This is the prior gap; the Ford–Roman quantum-inequality bound on the Casimir-type deficit is the next one, and only becomes meaningful once `𝒯` exists.

Paired with `TTEY_COUPLING_AND_THRUST_ACCOUNTING.md` §5 Q1 (the galaxy sector satisfies the null energy condition by the ghost condition), the honest position is: the galaxy field is grounded and NEC-respecting; the warp field is neither grounded nor shown to evade the energy bounds. Neither "TTEY works" nor "TTEY is dead."

## Reproduce

```bash
python3 scripts/ttey_field_models.py   # 7/7, exit 0
```
