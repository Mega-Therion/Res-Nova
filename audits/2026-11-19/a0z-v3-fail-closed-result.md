# a0(z) V3: extraction reproduces exactly; the discriminating dataset is withdrawn

**Date:** 2026-11-19. **Runner:** `scripts/a0_z_v3_fail_closed.py` (exit 2).
**Tags:** `[D]` reproduced · `[X]` withdrawn · `[O]` open. **Tier effect: none.**

`CURRENT_STATE_READ_THIS_FIRST.md` recorded that `a0_z_fail_closed_runner.py` "does NOT
exist in this repository". It does now.

## What reproduces

SPARC 175 provenance verified against
`VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256`: 175/175 files match,
0 mismatched, 0 missing. The corpus's own harness `02_galaxy_dynamics/sparc_a0_reextract_std.py`
then reproduces `A0_REEXTRACTION_MU_STD.json` on both μ functions:

| μ | recorded | reproduced | rel diff |
|---|---|---|---|
| μ_std | 1.1562e-10 | 1.1562458e-10 | 3.96e-5 |
| μ_dual | 9.285e-11 | 9.2849503e-11 | 5.35e-6 |

Bootstrap 68% intervals agree to the same order. The guard tolerance is 1e-4 relative
because the record stores only 5 significant figures; the extraction is deterministic
(fixed RNG seed 42), so genuine drift would appear far above that floor. **The +24% μ_std
shift is reproducible**, so the V3 extraction half stands.

## What does not

V3's published `INCONCLUSIVE` verdict (Δχ² = +0.750, 0.87σ; never conclusive anywhere in
the 68% CI) was computed on the 20-point `udf10_*` table. That table was **withdrawn
2026-09-27** in `03_observer_jwst/O4_REAL_DATA_MUSE_DARK_III_2026-09-27.md` §1: Bouche+2021
(A&A 654, A49) is a 9-galaxy angular-momentum pilot, and "Mercier+2022 A&A 667 A75" does not
exist. V3 was frozen and executed 2026-09-12, **fifteen days before the withdrawal**, and
neither `a0_of_z.py` nor `a0_of_z_v2.py` was updated to remove the table.

So the runner refuses to issue a verdict. V3's arithmetic is not in question; its input is
unprovenanced. The number is retained as a record of what was computed, not as evidence.

## What this does and does not change

- Does not change the tier of `O4` / a0(z): it was already `[O]`, and it stays `[O]`.
- Does not resurrect or kill the V1 5.9σ constant-a₀ verdict. That was already unrecoverable.
- Does close a route: **no verdict can ever be re-issued from the V3 table.** Any future
  a0(z) claim must name a traceable dataset.
- The live attempt remains `audits/2026-11-18/a0z_zgt15_manifest.py` (RC100 + RC41, `[U]`
  INCONCLUSIVE), which is provenance-checked against arXiv and is the correct vehicle.

## Fail-closed proof

| input | exit | verdict |
|---|---|---|
| tampered rotmod (one line appended) | 1 | `FAIL_CLOSED`, mismatched file named |
| clean data, no provable discrimination set | 2 | `EXTRACTION_VERIFIED_NO_VERDICT` |
| clean data + a manifest with source/DOI/sha256/n/range | 0 | `VERDICT_PERMITTED` |

The middle row is today's honest state. A guard that cannot fail is not a guard.
