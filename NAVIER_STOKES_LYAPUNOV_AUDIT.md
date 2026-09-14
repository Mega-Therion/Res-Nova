# Audit: Paper 17 Lyapunov Navier–Stokes Manuscript

**Artifact audited:** *A Lyapunov Criteria for Navier–Stokes Global Smoothness Sourced by Vorticity Alignment χ ≥ 0.7* (July 25, 2026).

**Source copy recovered:** Google Drive / research ingestion copy. Content hash recorded by the recovered source: `cf5adbe10008384d2a360e2a2dacc5f2eaec8395dd7759511bdbf08ec6212d33`.

**Audit status:** source-claim review. This document assesses what follows from the manuscript text and embedded Lean listings. It does not independently prove or disprove the cited PDE theorems.

## Executive verdict

Paper 17 does **not** supply a verified proof of three-dimensional Navier–Stokes global smoothness. Its viable research content is a conditional proposal: study whether a quantitatively stated vorticity-direction coherence condition can control vortex stretching. Its claimed Lyapunov monotonicity and its claimed machine verification do not establish that proposal as a global-regularity theorem.

The paper explicitly recognizes a conditional/open boundary, but several headline and conclusion passages overstate what the displayed derivations and Lean code support. It must be classified as `MANUSCRIPT-CONDITIONAL / PARTIALLY-SUPPORTED`, not as a formal proof or a solution to the Clay problem.

## Claims and findings

| Paper claim | Evidence displayed in the paper | Audit finding | Status |
|---|---|---|---|
| `χ(u,t) ≥ 0.7` gives a conditional regularity class | A definition of `χ`, a high-vorticity set, and an alignment estimate are given | Potential research direction; exact equivalence to a cited conditional regularity hypothesis still requires source-level verification | `OPEN` |
| Alignment softens a local vortex-stretching kernel | The manuscript derives a pointwise `|y|^{-2}` local bound after inserting an angle-control estimate | Plausible local heuristic/lemma candidate, but the treatment of the exterior integral, regularity assumptions, and constants is not fully established in the manuscript | `PARTIAL` |
| The Lyapunov functional is globally monotone | The displayed estimate reaches `dE/dt ≤ -(ν/2)||∇ω||² + C₂(1-θ)^4 E^3 + C₁E` | This inequality does **not** imply `dL_NS/dt ≤ 0` as written. The positive `E^3` and `E` terms require additional estimates, a smallness condition, or another argument. Substituting `(1-0.7)^4 = 0.0081` changes a coefficient but does not by itself prove absorption or global boundedness for arbitrary data | `UNSUPPORTED` |
| BKM immediately gives continuation | The manuscript invokes BKM after asserting enstrophy boundedness | A bound on `||ω||_{L²}` does not itself yield the required time-integrability of `||ω||_{L∞}`. The missing estimate must be supplied in the specified solution class. Also, the cited 1984 BKM reference is titled for 3-D Euler, so the exact Navier–Stokes continuation theorem and applicability must be verified | `UNSUPPORTED` |
| Lean verifies Navier–Stokes Lyapunov monotonicity | Embedded `NavierStokes.lean` listing defines a scalar gate and proves `1.0 - chi ≤ 0.3` from `chi ≥ 0.7` | The displayed theorem contains no velocity field, PDE, vorticity, strain tensor, enstrophy, time derivative, integral, or continuation argument. It verifies only a scalar arithmetic consequence of the threshold assumption | `FORMAL-SCALAR-ONLY` |
| Lean verifies tension divergence and holonomy convergence | Embedded `TensionProof.lean` listing includes `theorem tension_divergence : True := trivial` and `theorem sovereign_convergence ... : True := trivial` | These declarations check in Lean but their conclusions are `True`; they do not formalize divergence or convergence | `FORMAL-TAUTOLOGY` |
| `NavierStokes.lean` exists as a recoverable repository artifact | Paper names the file | No `NavierStokes.lean` file was found in the connected Mega-Therion GitHub search at audit time | `UNRECOVERED` |

## Embedded Lean listing

The paper itself displays the central Navier–Stokes Lean theorem in substance as:

```lean
def chiral_gate : Real := 0.7

theorem navier_stokes_threshold_lyapunov
    (chi : Real) (hchi : chi >= chiral_gate) :
    1.0 - chi <= 0.3 := by
  unfold chiral_gate at hchi
  linarith
```

This should be retained as a correct elementary threshold lemma, but renamed and documented accordingly. A suitable honest name would be `alignment_deficit_le_of_chi_ge_gate`. It must not be described as Lyapunov monotonicity.

## Required corrections before reuse

1. Reclassify every Paper 17 assertion as a formal scalar lemma, conditional PDE lemma, imported theorem, numerical/physical proposal, or open conjecture.
2. Remove or correct the claim that the displayed Lean code verifies Navier–Stokes regularity, Lyapunov monotonicity, tension divergence, or holonomy convergence.
3. Repair the mathematical route from the strain estimate to a closed a priori inequality; explicitly state any smallness, coercivity, or conditional assumptions.
4. Verify the exact Constantin–Fefferman and Navier–Stokes continuation results used, rather than relying on abbreviated statements.
5. Recover original `TensionProof.lean` and `NavierStokes.lean` source files with commit/hash provenance before treating the embedded listing as authoritative.
6. Keep the `Sovereign Invariance Conjecture` as an open conjecture, not as an equivalent rephrasing of the full Clay problem unless the equivalence is formally established in both directions.

## Reusable core

The following narrowly framed program may be retained:

> Define a measurable quantitative vorticity-direction coherence predicate on high-vorticity regions; prove exact geometric consequences of that predicate; and determine whether it satisfies the hypotheses of a source-verified conditional continuation theorem for a precisely specified 3D Navier–Stokes solution class.

This is a conditional-regularity research program. It is not currently a proof of global regularity for arbitrary smooth finite-energy data.
