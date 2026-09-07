# Branching from the invariant — a Drake-form cascade

**Status:** `[O]` structural proposal. Nothing here is derived.
**Date:** 2026-09-06

## The form, not the content

Drake's mechanism, borrowed structurally: a chain of conditional factors, each a fraction
of the stage before it.

    N = R* · f_p · n_e · f_l · f_i · f_c · L

Every factor is ≤ 1, so **the product shrinks monotonically with depth**. That is the useful
property. It means "downstream" is not a label — it is a *prediction of rarity*.

## The trunk

The unifying principle is one operator, not six:

    U_γ = P exp(−∮_γ A)        with        U_{γ₊} ≠ U_{γ₋}

Transport around a closed path returns changed, path-dependently, and orientation matters.
Everything below is a branch off this, reached by clearing conditions.

## The cascade

For a domain D to *manifest* the invariant rather than merely resemble it:

    M(D) = f_closure · f_memory · f_orient · f_scale · L

| factor | condition | fails when |
|---|---|---|
| `f_closure` | paths in D actually close | the domain only has open trajectories |
| `f_memory` | the return differs from the start, `U_γ ≠ 1` | transport is trivial; the loop forgets |
| `f_orient` | reversal gives a different result, `U_{γ₊} ≠ U_{γ₋}` | `U² = 1` — **any involution kills this** |
| `f_scale` | the effect survives coarse-graining to something observable | it averages away above the microscale |
| `L` | how long the structure persists once formed | it decoheres or dissipates faster than it can be read |

## Why biology is downstream, and what that costs

Physics sits near the trunk: few factors between the invariant and the observable, so `M`
stays large. Biology sits far out — it inherits every factor above it *and* adds its own
(a metabolism to hold the loop open, a substrate to store the return, a timescale long
enough to matter). A long product of fractions is a small number.

So "biology is emergent, not the underlying principle" is not a modest disclaimer. In this
form it is a **structural consequence**: emergent phenomena are the low-`M` tail of a
monotonically shrinking cascade. That is *why* they are contingent and rare, and why they
cannot be evidence for the trunk — a small product tells you almost nothing about the
factors that produced it.

**Corollary, and it is the operative one:** a downstream branch can never confirm the
invariant. It can only *fail* to contradict it. Confirmation has to come from near the
trunk, where the factor chain is short enough to audit.

## The orientation factor is where this is currently broken

`f_orient` is the load-bearing clause — without it the whole structure reduces to "things go
in circles."

Measured 2026-09-06: `05_lean_formalization/ChiralCellularDuality.lean`, the module named
for the chirality of the cellular branch, proves

    σ (σ x) = x

an **involution**. For an involution `U_{γ₋} = U_γ⁻¹ = U_γ = U_{γ₊}`, so `f_orient = 0`
identically. The module named for the arrow proves the one algebraic property that blunts
it. Sabotage-confirmed vacuous besides: renaming its physical quantities to `BANANA_COUNT`,
`HAT_SIZE`, `SHOE_COUNT` and `PUDDLE_DEPTH` compiles clean with all three theorems closing.

Until `f_orient > 0` is established somewhere other than by assertion, the cascade has a
zero in it and every branch below that point evaluates to zero.

## What to do next, in order

1. Establish `f_orient > 0` near the trunk — an explicit `γ` and `γ⁻¹` in the physics
   sector with a computed, unequal holonomy. Not an involution.
2. Only then ask what survives `f_scale`.
3. Biology stays `[C]` and downstream, and is never cited as support.

## MINIATURE AUDIT (2026-09-06; [P] structure, [O] physics reading)

The orientation factor is no longer merely flagged broken — it has a proved miniature model of
the evasion. In Res-Nova's `ChiralResidue` (PR #27, Lean 4, no Mathlib, no sorry):

- **f_orient is satisfied at the cover level.** The forward and reverse crack transports are
  *different* elements (`inv n ≠ n`, differing by exactly the central sign): U_{γ₊} ≠ U_{γ₋} holds.
- **Yet they act identically on the chiral space.** The orientation-dependence is carried
  *entirely by the sign* — real in the cover, invisible downstairs. The trunk's load-bearing
  clause is a double-cover fact: the 2π problem, promoted to a theorem.
- **The involution-kill is evaded by exactly one notch.** On the chiral space the transport
  squares to the identity (the kill *would* apply), but in the cover the square is the 2π
  rotation, not the identity (`mul n n ≠ one`). The cascade dies when U² = 1; the crack's U²
  is the central sign.

The miniature answers this doc's own question: how can a loop return changed without being an
involution? Because its square is not 1 — it is the 2π rotation. The residue sits one notch of
cover above the involution-kill. Tagging: the three structural theorems are [P] (verified); the
physics reading of them remains [O].
