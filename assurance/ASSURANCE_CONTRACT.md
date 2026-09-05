# Res-Nova Assurance Contract

## Purpose

Res-Nova uses one evidence chain for every high-impact statement:

> Natural-language claim → formal proposition or computational definition → source declaration or code artifact → verification environment → evidence → independent witness.

A claim may not be promoted beyond the strongest link in this chain.

## Claim states

| State | Meaning | Minimum evidence |
|---|---|---|
| `proposed` | Research idea or untested statement | Named owner and precise wording |
| `axiomatic` | Assumption supplied to a model or theorem | Explicit assumption record and scope |
| `derived` | Consequence of declared assumptions or definitions | Reproducible derivation or formal proof under those assumptions |
| `computed` | Output of an executable computation | Pinned code, inputs, environment, and captured output |
| `formally-verified` | Kernel-checked formal artifact | Passing target gate, axiom report, and assumption audit |
| `empirically-supported` | Supported by a declared dataset and analysis | Provenance, independent recheck, uncertainty, and sensitivity report |
| `conditional` | Valid only under named conditions | Conditions visible in the claim surface |
| `retracted` | Withdrawn because a prior wording or result is invalid | Retraction reason, affected surfaces, and replacement wording |

## Promotion rules

A passing formal gate cannot promote a physical claim unless the physical assumptions are separately documented. A low residual or parameter comparison cannot promote a causal, universal, or “confirmed” claim. A historical verification log cannot be presented as a current pass without a fresh run at the current commit. A skipped test cannot count as verified. A PDF cannot be the sole witness for a numerical or formal claim.

## Required claim record

Each publication-critical claim must identify:

1. A stable claim ID.
2. Exact current wording and prohibited overclaiming variants.
3. Epistemic state and assurance level.
4. Source data, retrieval date, license, and hashes when applicable.
5. Code, theorem, or declaration paths.
6. Formal hypotheses, physical assumptions, and parameter tier.
7. Exact verification commands and environment identifiers.
8. Independent witness or explicit reason one is unavailable.
9. Affected manuscript, README, HTML, JSON, and PDF surfaces.
10. Last verified commit and status of the next review.

## Failure semantics

Verification scripts must fail closed on missing inputs, stale hashes, target drift, undeclared assumptions, unavailable required backends, skipped critical tests, and contradictory claim surfaces. Warnings may remain warnings only when the report explicitly records why they do not block the declared assurance level.

## Release gates

A release may be called publication-grade only when the formal, empirical, manuscript, and provenance gates all pass for the claims included in that release. Claims outside the release scope must be labeled separately rather than silently included.
