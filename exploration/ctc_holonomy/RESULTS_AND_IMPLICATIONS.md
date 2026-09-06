# CTC holonomy — the experiment, run, and what each outcome means

**Status:** `[O]` exploration. **Held out of the manuscript** per RY 2026-09-06.
**Scripts:** `godel_setup.py`, `holonomy_ctc.py`, `holonomy_eig.py`, `find_transition.py`

## What was computed

Parallel transport of a vector around a closed φ-circle in Gödel spacetime, at fixed
(t, r, z), for radii below, at, and above the CTC threshold. The holonomy is
`U_γ = exp(−2π M)` with `M^l_m = Γ^l_{m φ}`. The question put to it:

> Is `U_γ` an involution?

## Result 1 — it is never an involution

| r | sinh r | causal character | ‖U²−I‖ | involution? |
|---|---|---|---|---|
| 0.4000 | 0.4108 | spacelike circle | 5.47e0 | NO |
| 0.7000 | 0.7586 | spacelike circle | 1.23e5 | NO |
| 0.8814 | 1.0000 | **null (CTC threshold)** | 3.01e9 | NO |
| 1.1000 | 1.3356 | CTC (timelike) | 2.99e16 | NO |
| 1.5000 | 2.1293 | CTC (timelike) | 7.21e38 | NO |
| 2.0000 | 3.6269 | CTC (timelike) | 1.82e106 | NO |

**Orientation is physical here.** Forward and backward traversal are different
operations at every radius tested. The clause `U_{γ₊} ≠ U_{γ₋}` is not an artifact of
the toy group — it holds in an actual solution of Einstein's equations.

**Honest caveat, and it matters:** the answer is the same *below* the CTC threshold. The
CTC does not switch orientation on. Non-involutivity is a property of Gödel's rotating
geometry generally, not of closed timelike curves specifically. Any write-up must say so.

## Result 2 — an unexpected transition in the holonomy's *character*

Eigenvalues of the transport generator:

| r | eigenvalues | character |
|---|---|---|
| 0.4000 | `0 ± 0.7782i` | **pure rotation** (elliptic, compact) |
| 0.7000 | `± 0.9018` | **boost** (hyperbolic, non-compact) |
| 0.8814 | `± 1.7321 = ±√3` | boost |
| 1.5000 | `± 7.0128` | boost |

The holonomy changes type — elliptic → hyperbolic — at

    r* = 0.5731079174 ,   sinh²(r*) = (√3 − 1)/2 = 0.3660254038   (matches to 1e-9)

**This threshold is new and is NOT the CTC threshold.** It sits strictly inside it
(r* = 0.573 < r_c = 0.881). Below r*, transport is a rotation and closes back on itself
periodically. Above r*, it is a boost: rapidity accumulates without bound and the loop
*never* closes, at any winding number. At the CTC threshold itself the boost eigenvalue
is exactly ±√3.

## Result 3 — the CTC threshold is θ

Gödel's φ-circles turn timelike where `g_φφ < 0`, i.e. exactly at `sinh r = 1`. And

    tanh(arcsinh x) = x/√(x²+1)     ⟹     tanh(arcsinh 1) = 1/√2 = 0.7071067811865475

which is **θ**, already machine-proven in `05_lean_formalization/RapidityEquipartition.lean`
as `tanh_arsinh_one_eq_theta`. Verified symbolically here: the difference simplifies to 0.

**Why this is worth something.** `RapidityEquipartition.lean` states explicitly that it
does *not* derive the equipartition premise; CLM-10 is `conditional` precisely because
`sinh ψ = 1` is adopted rather than selected by a covariant argument. In Gödel,
`sinh r = 1` **is** selected — by the causal structure of the metric. That is a candidate
covariant source for the condition CLM-10 has been missing.

**What would have to hold for that to count.** The Gödel `r` is a radial coordinate; the
framework's `ψ` is a spin rapidity. Identifying them is not automatic and is *not* done
here. Until an argument connects them, this is a structural coincidence of the form
`sinh = 1`, which is a natural condition and could arise independently in both places.
**Do not report this as closing CLM-10.**

## What each outcome would have proved — as set in advance

The decision rule was fixed before the computation:

- **Not an involution** → orientation is physical in a real metric. *This is what happened.*
  It promotes `U_{γ₊} ≠ U_{γ₋}` from a statement about a finite group to a statement about
  a spacetime. It does **not** prove anything about time travel.
- **An involution** → the arrow does not come from this structure; recorded as a closed door.
- **CTCs excluded by the aether constraint** → report the exclusion. Not reached: this
  computation used Gödel with Levi-Civita, not the Res-Nova connection.

## What this does NOT prove — guard rails

1. **Nothing about whether time travel is possible.** Gödel is a known exact solution with
   CTCs; that was an input, not a finding.
2. **Nothing about the arrow of time in our universe.** Gödel is not our universe — it is
   rotating, has no global time function, and does not expand.
3. **`comp_inv` still holds**: out-and-back composes to the identity. Forward-then-reverse
   is a genuine undo. "The two directions are different operations" ≠ "you cannot return."
4. **Representation dependence** was fixed by choice: this transports *vectors*. On spinors
   the order can differ (a 2π rotation is `+1` on vectors, `−1` on spinors). Any claim about
   "the" holonomy order must name the representation.
5. **The Res-Nova connection has not been used.** This is Levi-Civita on Gödel. Redoing it
   with the χ/aether connection is a separate computation and may not have CTCs at all.

## Implications, stated plainly

**If the framework keeps the orientation clause:** it now has a spacetime example where the
clause is true and computed, not merely satisfiable in a finite group. That is a real
strengthening of the Bohm delta — Bohm's enfoldment/unfoldment is symmetric; this is not.

**The genuinely interesting object is r\*, not the CTC.** A radius where transport stops
being a rotation and becomes a boost is a physical transition: below it, a transported frame
returns periodically; above it, rapidity grows without bound and nothing ever returns. That
is much closer to an "arrow" than the CTC condition is, and it was not anticipated.

**The θ coincidence is a lead, not a result.** It is the strongest thing here and the easiest
to overclaim. Treat as `[O]` until the coordinate-vs-rapidity identification is argued.

## Next steps

1. Determine whether `sinh²(r*) = (√3−1)/2` is exact (it matches to 1e-9) and where √3 comes from.
2. Redo the transport on spinors and compare orders.
3. Replace Levi-Civita with the χ/aether connection and check whether CTCs survive at all.
4. Only then decide whether any of this belongs in the manuscript.
