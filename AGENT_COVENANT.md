# Agent Covenant — Res Nova

This file is binding on every coding or research agent that edits this repository.

## Authority

1. Current claim authority is `EPISTEMIC_BOUNDARY_v1.5.0.md` plus the JSON artifacts it cites.
2. Physics-seal authority for formal theorems is release `v1.4.0` (Lean modules under `05_lean_formalization/`).
3. Empirical-seal authority for `a0` and matched-parameter scores is commit `3c90ef3e` and the JSON files it added.
4. If README, a manuscript, a Zenodo title, and a ledger disagree, the ledger plus the JSON win. Narrative loses.

## Tags

- `[P]` — proved inside Lean or by an explicit algebraic identity in-repo. No physical ontology is certified.
- `[D]` — computed from named scripts and frozen JSON/manifests.
- `[C]` — peer-reviewed literature, cited, not re-derived here.
- `[O]` — open, conjectural, or motivational. May be planned and tested. May not be announced as shown.

## Forbidden moves

- Do not upgrade `[O]` to `[P]` or `[D]` by wording.
- Do not restore “zero free parameters” or “zero-parameter geometric alternative” as a current model claim.
- Do not quote `a0 = (9.433 ± 0.050) × 10^{-11}` as the working measurement. That headline is superseded. You may cite it only as a retracted method.
- Do not treat 3,391 radial points as independent when quoting precision on `a0`.
- Do not invent a first-principles derivation of `a0` or of `Ω_Λ = ln 2`.
- Do not change SPARC numeric JSON or Lean proofs unless the user asked for a new computation or a new theorem, and the new artifact is ledgered in the same commit.
- Do not cite `PAPER_01` as current theory. See `01_foundational_action/PAPER_01_NOTICE.md`.

## Required moves

- Every new claim gets an item ID, a tag, a file, and a test or quarantine sentence.
- Every SPARC number in prose must match a JSON field to stated rounding.
- If you cannot point to a file, you do not have a result.
- Prefer downgrade to silence.

## What is actually closed

Closed means present in this repo with a tag and an artifact, not “feels finished.”

- Dual-channel identity `F_dual'(x) = x/(1+x)` is `[P]`.
- Single-channel `arcsinh` inverted limits are `[P]`-falsified.
- RAQUAL superluminality, disformal cone split vs GW170817, and Skordis–Złośnik embedding are `[P]` at the v1.4.0 seal.
- Honest SPARC `a0` with a systematic budget is `[D]`.
- Like-for-like parameter ledger and NFW concentration-prior comparison are `[D]`.

## What is not closed

- Horizon identity `a0 = c H0 / (2π)`.
- Reading `ξ = a0 / (c H0)` as a derived coupling rather than arithmetic.
- `Ω_Λ = ln 2`.
- Any high-`z` confirmation.
- Fresh-clone Lean reproduction via `lake exe cache get` (documented, not walked).
- In-repo SPARC data (not vendored).
