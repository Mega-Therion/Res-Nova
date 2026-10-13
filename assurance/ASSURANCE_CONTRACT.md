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

## Falsifiability result semantics (audit policy for `falsifiability.result`, issue #136)

`falsifiability.result` records the outcome of the claim's *adversarial* test (sabotage /
mutation / independent re-derivation challenge), which is distinct from the claim's
*verification* (the gate run recorded in `last_verified_commit`). The two must not be conflated.

| `result` | Meaning |
|---|---|
| `supported` | The named falsifiability test was executed at (or after) `last_verified_commit` and did not refute the claim. |
| `not_run` | The falsifiability challenge has not been executed — either never, or not at the current commit. This is **not** support: a claim may be `formally-verified` (kernel-checked at some commit) while its adversarial challenge was never run. The registry must never be read as a uniformly current falsifiability audit trail while `not_run` entries remain. |
| `inconclusive` | The test was executed; the outcome neither supports nor contradicts the claim. |
| `contradicted` | The test was executed and refuted the claim. Fail-closed: the claim state must be `retracted` or `conditional`, never a state asserting current support. |

`last_verified_commit` records the commit at which the *verification* last passed. Per the promotion
rules, a historical verification log cannot be presented as a current pass without a fresh run at the
current commit; the same holds for `supported` falsifiability results.

For `formally-verified` claims, `falsifiability.test` SHOULD name the exact Lean declaration(s)
that prove the wording (e.g. `F_dual_hasDerivAt_sq`), so the registry maps wording to artifact.
The registry validator reports claims missing this mapping as warnings (see
`scripts/validate_claim_registry.py`); warnings do not fail the gate but must be cleared or
justified before a publication-grade release.

## Release gates

A release may be called publication-grade only when the formal, empirical, manuscript, and provenance gates all pass for the claims included in that release. Claims outside the release scope must be labeled separately rather than silently included.
