# SPARC Lelli+2016c catalogue: pinned provenance for the BLK-1017 audit

**Status (2026-11-05):** provenance fix only. No physics claim, tier or number in this
repository changes.

## The gap this closes

Two audit documents compare the E.H.Y.E.H. manuscript's Table II against
`SPARC_Lelli2016c.mrt`:

- the BLK-1009 audit on The Block (item: "Table II: no fit code produced it, and its values
  don't match `SPARC_Lelli2016c.mrt`");
- `EHYEH_AUDIT_AND_SALVAGE_SKETCH_2026-11-05.md` §1 ("For example, DDO 154 is 51.3 ± 1.5
  there and 47.0 ± 1.0 in the catalogue").

Neither was checkable from this repository: the catalogue was not committed anywhere under
`02_galaxy_dynamics/`, and no script reproduced the comparison. Both audits cited a file the
repo did not have. That is the same class of gap as the withdrawn 20-point O4 table
(`PEER_REVIEW_READINESS.md`, 2026-09-27): a number with no traceable source in the tree.

## What was added

| Path | Contents |
|---|---|
| `02_galaxy_dynamics/sparc_catalogue/SPARC_Lelli2016c.mrt` | the catalogue verbatim, fetched from `https://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt` on 2026-11-05 |
| `02_galaxy_dynamics/sparc_catalogue/verify_lelli_catalogue.py` | parser + pinned-value checks, 7 checks, exit 0 |
| this file | the record |

**Catalogue SHA-256:** `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`
(28 259 bytes, 175 galaxies parsed).

## Verified [E]

`python3 02_galaxy_dynamics/sparc_catalogue/verify_lelli_catalogue.py` → 7/7 PASS, exit 0.

- DDO 154: catalogue `V_flat = 47.0 ± 1.0 km/s`; the manuscript's Table II prints `51.3 ± 1.5`.
  The audit's arithmetic is correct: the published value is not the catalogue value.
- NGC 2841: catalogue `V_flat = 284.8 ± 8.6 km/s`.

This confirms the audit's *comparison*. It does **not** confirm the audit's further claim that
NGC 2841's error was "halved" in the manuscript, because Table II itself is not in this
repository and the manuscript lives outside it (`Chyren/3_research/publications/
holographic_obserververse/`). Table II still has no generating code, so it stays `[X]` as
published and the BLK-1017 remedy stands: remove it, or replace it with fits from the repo's
own SPARC pipeline at a₀ = 1.1607.

## Why the catalogue is pinned rather than referenced by URL

The same reason `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256` pins the
rotmod files: a URL is not evidence that a file is unchanged. With the SHA-256 in the tree,
any later reader can tell whether a comparison was made against the same catalogue the audits
used. If the upstream file ever moves, the checksum mismatch makes it visible rather than
silent.

## Scope

Added: one data file, one verification script, one record. No existing file was edited, no
claim was retagged, and nothing here extends or endorses the manuscript.
