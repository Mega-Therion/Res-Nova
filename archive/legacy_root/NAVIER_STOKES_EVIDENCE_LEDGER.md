# Navier–Stokes Evidence Ledger

**Status:** initial inventory; created 2026-09-13 local research time.

This ledger preserves provenance for the active conditional-regularity program. It records evidence without converting any source into a stronger mathematical claim than it supports. Add entries rather than overwriting historical ones.

## Claim-status key

| Status | Meaning |
|---|---|
| `FORMAL-CONDITIONAL` | Lean-checked statement with explicit assumptions; not an NSE global-regularity proof |
| `MANUSCRIPT-CONDITIONAL` | Paper-level conditional argument needing source/hypothesis verification |
| `AUDIT` | Assessment or provenance record |
| `SUPERSEDED-PRESERVED` | Historical source retained for provenance; not automatically active support |
| `OPEN` | Unproved obligation or conjecture |

## Primary artifacts

| ID | Artifact | Location / identifier | Version or hash | Status | Supported statement |
|---|---|---|---|---|---|
| NS-L-001 | `SovereignRegularity.lean` | `05_lean_formalization/SovereignRegularity.lean` | blob SHA `3fa592917a99b56098f32aab2cbea4eb175bd056` at baseline commit `aaca4f96978676230239e47a921704fa6353bb0f` | `FORMAL-CONDITIONAL` | `sovereign_regularity_theorem` returns the assumed `h_controlled` bound. It is not a formalization of NSE evolution or global regularity. |
| NS-A-001 | Repository assumption audit | `THEORY_ASSUMPTION_AUDIT.md` | blob SHA `7809961a7da3a1b35ece2fa6d2260c2b277b3d7b` | `AUDIT` | Classifies the flagship theorem as a projection and identifies the present BKM-named quantity as a product rather than a time integral. |
| NS-A-002 | Lean inventory | `AUDIT_LEAN_INVENTORY.md` | blob SHA `1ab6dbe6ffe7e4b889ce7b5fdb6cda0a72f7996f` | `AUDIT` | Classifies the Lean content as conditional BKM boundedness under assumed alignment; global NSE regularity is open. |
| NS-M-001 | Sovereign Regularity manuscript | Google Drive submission copy | SHA-256 `1b1f658a167bbf07e05d9e25ccac827a3e51f6d8d5c2170a841d79c5c64baf5c` | `MANUSCRIPT-CONDITIONAL` | On `T^3`, assumes a Lipschitz vorticity-direction condition `SA(K,L)` and says it does not resolve the Clay problem; invariance of the Sovereign Class is stated as open. |
| NS-Z-001 | Zenodo Sovereign Regularity deposit | DOI `10.5281/zenodo.20652236` | Version history must remain attached to any citation | `SUPERSEDED-PRESERVED` | Notion re-verification retains it as a conditional proof with an honesty disclaimer; it is not evidence of a Millennium solution. |
| NS-N-001 | Zenodo supersession re-verification | Notion page `3d977b95-a965-81eb-8b6b-cafa6c97d3cf` | fetched 2026-09-13 | `AUDIT` | Retains the conditional Sovereign Regularity item; classifies the broader Millennium-solution claims for discard. |
| NS-N-002 | Later Lyapunov manuscript pointer | Notion page `3aa77b95-a965-812f-b662-e98b7f7721f7` | fetched 2026-08-25 | `OPEN` | Points to `Documentation/papers_42/PAPER_17_A_LYAPUNOV_CRITERIA_FOR_NAVIER_STOKES_GLOBAL_SMOOTHNESS.tex`; source content has not yet been recovered or assessed. |

## External theorem dependencies to verify

| ID | Dependency | Present use | Verification required | Status |
|---|---|---|---|---|
| NS-D-001 | Beale–Kato–Majda continuation criterion | Manuscript uses time-integrability of vorticity as a continuation input | Verify the exact PDE, domain, solution class, norm, interval, and theorem statement against the primary source or a standard authoritative reference | `OPEN` |
| NS-D-002 | Constantin–Fefferman vorticity-direction criterion | Manuscript proposes `SA(K,L)` as an implication route to a geometric regularity hypothesis | Verify the exact quantitative hypothesis, domain, high-vorticity-set condition, conclusion, and whether the manuscript's formulation is faithful | `OPEN` |
| NS-D-003 | Local strong-solution theory | Manuscript invokes an `H^s`, `s > 5/2`, maximal strong solution | Fix an exact theorem and show compatibility with the chosen Clay-aligned formal target | `OPEN` |

## Non-negotiable open obligations

| ID | Obligation | Why it matters |
|---|---|---|
| NS-O-001 | Derive or prove persistence of `SA(K,L)` from NSE dynamics for an appropriate initial-data class | The current Lean theorem assumes the bound it returns; without this, there is no global regularity result beyond the conditioned class |
| NS-O-002 | State and formalize a Clay-compatible target | The Clay problem requires a complete official alternative, not an informal conditional theorem |
| NS-O-003 | Replace the BKM-named product with a genuine time integral or rename it | Names must match formal mathematical objects |
| NS-O-004 | Recover and audit the Lyapunov manuscript | It cannot enter the active argument until its content, dependencies, and status are known |
| NS-O-005 | Independent PDE and Lean review | Prevents claims from outrunning proof scope |

## Change control

- Do not delete historical records in response to an audit finding. Add a dated status update and keep stable identifiers.
- Do not cite `SUPERSEDED-PRESERVED` entries as current support unless a separate re-admission decision names the precise version and rationale.
- Do not upgrade a claim status without a source link, exact statement, and reproducible build or derivation evidence.
- Every public technical claim must link to one or more ledger IDs.
