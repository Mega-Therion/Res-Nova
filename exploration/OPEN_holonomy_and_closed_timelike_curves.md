# Exploration — holonomy on closed timelike curves

**Status:** `[O]` OPEN. Exploration only. **Not for the manuscript** until we know
whether it is solvable. Nothing here is derived.
**Opened:** 2026-09-06, from RY's question: *"does that mean by extension that backwards
time travel is unholonomic?"*

## The question, stated precisely

A closed timelike curve is a closed loop, so it carries a holonomy `U_γ`. If `U_γ ≠ 1`,
a traveller returns to the **same event** but not to the **same state**.

    return-to-event  ≠  return-to-state       whenever  U_γ ≠ 1

The question is whether that separation is forced, and what it costs.

Note the terminology is apt: *nonholonomic* in classical mechanics means exactly
path-dependent — a constraint that cannot be integrated away, where the outcome depends
on the route and not merely the endpoints. That is what `U_{γ₊} ≠ U_{γ₋}` asserts.

## What is already proved (and what it does NOT say)

`05_lean_formalization/ChiralHolonomyOrientation.lean` and
`GenerationCycleChirality.lean` establish, machine-checked and sabotage-tested:

1. reversal inverts holonomy;
2. orientation matters **iff** the holonomy is not an involution;
3. a constructed order-3 cycle where the two orientations disagree at every point.

**These apply to any closed loop. They say nothing about time.** No metric signature, no
causal structure, no timelike condition appears anywhere in either module. A CTC is a
special case only in the sense that it is a loop.

**Guard against one overreach.** `comp_inv` proves `U_γ · U_γ⁻¹ = e` — out-and-back
*does* compose to the identity. Forward-then-reverse is a genuine undo. What differs is
`U_{γ₊}` versus `U_{γ₋}` as *operations*. Conflating "the two directions are different
operations" with "you cannot get back" yields a false result. Do not publish the second
sentence on the strength of the first.

## Why the involution case is the interesting one

If `U_γ² = 1`, the return trip is indistinguishable from the outbound trip: the loop is
time-symmetric and carries no direction. Order 3 is the smallest structure in which that
fails. Stated as a question:

> **Is the arrow of time a statement about group order rather than about entropy?**
> Not "why does entropy increase", but "why is the holonomy not an involution".

Unlike the thermodynamic version this has a crisp answer once the structure group is
named — which is exactly why it is worth attacking, and exactly why it must not be
asserted before it is computed.

## What would have to be built

The gap is concrete, not philosophical:

1. **A metric with a timelike loop.** Neither module has one. Gödel dust or a Kerr
   interior region are the standard exhibits.
2. **A connection on it.** Levi-Civita is the minimum; the Res-Nova sector would need
   the χ / aether connection, which brings its own preferred frame.
3. **The loop integral actually computed.** `U_γ = P exp(−∮_γ A)` around the CTC —
   a number, not a claim.
4. **Its order determined.** Involution → no arrow. Order > 2 → orientation is physical.

Step 3 is the one that decides it. Steps 1–2 are setup.

## Anticipated obstacles — record these before they surprise us

- **The aether picks a time direction already.** Res-Nova's `u^μ` is unit timelike, so
  the theory may forbid CTCs before the holonomy question is even reachable. If so, the
  result is *"this framework excludes the configuration"*, which is a real finding and
  should be reported as one rather than buried.
- **Chronology protection.** Any CTC construction faces the standard semiclassical
  instability arguments. Not fatal to a formal question, but it must be acknowledged.
- **Spinors vs vectors.** Holonomy order depends on the representation being transported.
  A `2π` rotation is the identity on vectors and `−1` on spinors. **Choose the
  representation before computing, or the order is not well defined.**

## Decision rule, set in advance

- If `U_γ` on a timelike loop is computed and is **not** an involution → orientation is
  physical in this framework, and it goes to the manuscript with the computation attached.
- If it **is** an involution → the arrow does not come from this structure, and that is
  recorded as a closed door, not quietly dropped.
- If CTCs are excluded by the aether constraint → report the exclusion; do not report it
  as if the holonomy question had been answered.

**Kept out of the manuscript deliberately.** Per RY 2026-09-06: explore first, publish
only if it survives.
