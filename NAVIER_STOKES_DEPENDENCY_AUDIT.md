# Navier–Stokes Dependency Audit

**Purpose:** record the exact target and the analytic dependencies that must be verified before any conditional regularity statement is reused or formalized.

**Scope:** this is a source-backed dependency map, not a proof of any open Navier–Stokes statement.

## 1. Official target specification

The Clay/Fefferman problem asks for a proof of one complete alternative. For this project, the cleanest initial specification target is **Alternative B**: for every smooth, divergence-free periodic initial velocity on `R^3/Z^3`, with zero force and positive viscosity, construct a smooth periodic solution for all `t ≥ 0`.

The existing Sovereign Regularity manuscript begins on the torus, so Alternative B is a better first target than moving between `T^3` and `R^3` by an informal localization claim.

A conditional theorem about only solutions satisfying `SA(K,L)` is not Alternative B: the Clay target quantifies over **every** smooth divergence-free initial datum in the specified setting.

## 2. Existing program and exact gap

The current program has the following desired implication chain:

```text
Alignment predicate A(u,t)
  ⇒ geometric vorticity-direction condition G(u,t)
  ⇒ source-verified conditional regularity/continuation theorem
  ⇒ global smoothness for solutions satisfying A for their maximal interval.
```

The missing global implication is:

```text
all Clay-admissible initial data
  ⇒ A(u,t) holds for all times of existence.
```

The current Lean theorem does not prove either chain. It projects an assumed uniform vorticity bound from a structure field.

## 3. Constantin–Fefferman dependency

### What is supported by the available sources

A review source describes the Constantin–Fefferman result as establishing regularity for whole-space 3D Navier–Stokes solutions when the direction of vorticity is spatially Lipschitz in high-vorticity regions; the condition is required for almost all relevant point pairs and almost all times, and it can be localized to pairs with `|x-y| < δ`. Later work cited by that review discusses a `1/2`-Hölder condition.

### What the manuscript must establish

The manuscript's `SA(K,L)` / `χ` route may be usable only after all of the following are explicit:

1. The exact solution class, domain, time interval, forcing convention, and regularity assumptions of the theorem being invoked.
2. The exact high-vorticity threshold condition: both vorticities must satisfy the condition at the compared points.
3. The exact angle/coherence condition, including whether it is required almost everywhere, pointwise, and only for distances below a specified `δ`.
4. A proved equivalence or implication from the project definition of `χ ≥ θ` to that exact condition.
5. A check that constants and dimensions are meaningful: a dimensionless threshold `θ = 0.7` cannot by itself determine a Lipschitz constant without a specified dimensional normalization `L_max`.
6. A domain-specific proof. A theorem stated on `R^3` does not automatically become a theorem on `T^3`; periodic analogues or a direct torus theorem must be cited and checked.

### Current status

`OPEN / IMPORTED-THEOREM`. The geometric idea is a candidate route to a known conditional criterion; it is not yet a self-contained or formally verified reduction.

## 4. Continuation criterion dependency

The active manuscripts use a BKM-style statement involving

```text
∫₀ᵀ ||ω(·,t)||_{L∞} dt
```

as a continuation condition. The original Beale–Kato–Majda article cited in the manuscripts concerns 3D Euler. Fefferman's Clay statement likewise mentions the BKM vorticity-integral fact in its Euler discussion.

A Navier–Stokes continuation criterion may be available in the required strong-solution setting, but it must be separately identified and cited with its exact hypotheses. The project must not cite the Euler theorem alone as if it proves the Navier–Stokes step.

Additionally, an a priori bound on `||ω||_{L²}` does not by itself imply the displayed `L¹_t L∞_x` condition. Any valid route must supply a theorem or derivation of the required stronger spacetime control.

### Current status

`OPEN / IMPORTED-THEOREM`.

## 5. Lyapunov route audit

Paper 17 derives an inequality of the displayed form

```text
dE/dt ≤ -(ν/2)||∇ω||²_{L²} + C₂(1-θ)^4 E^3 + C₁E.
```

This is not a closed global bound for unrestricted data. The right-hand side retains positive superlinear and linear terms. Replacing `(1-θ)^4` with `0.0081` at `θ = 0.7` changes the coefficient but supplies neither a sign condition nor a global barrier.

To rehabilitate any Lyapunov theorem, the project must prove one of the following, with explicit assumptions:

- a coercive negative term that dominates every positive term on the claimed solution class;
- a small-data or small-critical-norm invariant region;
- a quantitatively specified feedback/control mechanism that is part of the PDE and not an assumed property of the desired solution; or
- a different closed a priori estimate.

Absent one of these, the Lyapunov functional is a proposed analytic tool, not a global monotonicity theorem.

## 6. Lean target ladder

The initial Lean work should be divided into statements that can be honest about their scope:

| Level | Formal target | Claim permitted |
|---|---|---|
| L0 | Scalar threshold arithmetic, e.g. `χ ≥ 0.7 → 1-χ ≤ 0.3` | Elementary arithmetic lemma |
| L1 | Unit-vector/angle inequalities | Geometric lemma |
| L2 | Definitions of fields, high-vorticity set, alignment predicate, time interval, and real integrals | Formal specification |
| L3 | `A(u,t) → G(u,t)` with all hypotheses explicit | Conditional geometric reduction |
| L4 | A formalized conditional continuation theorem, or a clearly axiomatized imported theorem with provenance | Conditional PDE theorem |
| L5 | A proof that all data in Clay Alternative B satisfy/preserve `A` | Candidate Clay-level result, subject to independent review |

No theorem below L5 may be described as resolving the Clay problem.

## 7. Immediate technical tickets

1. Choose the definitive domain: begin with periodic `R^3/Z^3` to match Clay Alternative B, or state a separate whole-space program.
2. Write a source-accurate statement of the selected vorticity-direction criterion and its assumptions.
3. Define `χ` with all quantifiers, high-vorticity threshold, scale, measurability, and units explicit.
4. Prove `χ ≥ θ →` the selected geometric criterion, if it is true as defined.
5. Identify a correct Navier–Stokes continuation theorem for the chosen strong-solution framework.
6. Either close the Lyapunov inequality under explicit additional conditions or downgrade it to a heuristic/research lemma.
7. Recover the complete original Lean sources and convert every displayed `True := trivial` claim into an accurately named tautology or remove its stronger interpretation.

## 8. Citation discipline

Every future paper, README, theorem docstring, or release note must distinguish:

- results proved in this repository;
- results imported from the PDE literature;
- assumptions imposed on a solution; and
- open conjectures about NSE dynamics.

A numerical simulation, a scalar Lean inequality, or a theorem that projects an assumption may support only the statement it literally proves.
