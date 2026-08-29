# VERIFICATION_RUN_003 — Provenance

**This directory is not a single atomic run.** Its artifacts were produced across
four sessions spanning six days. Recorded here so nobody reads the folder name as
a claim of one simultaneous verification.

| Artifact | Produced |
|---|---|
| `01_lean/RUN_003_RESULT.json` | 2026-08-20 23:10 |
| `01_lean/SHA256SUMS.txt` | 2026-08-20 23:10 |
| `02_sparc/SPARC_DERIVED_CV_REPORT.json` | 2026-08-20 23:10 |
| `01_lean/GATE_TRANSCRIPT.txt` | **2026-08-23 01:31** |
| `figures/*.png` (3) | 2026-08-24 04:40 |
| `02_sparc/SPARC_DERIVED_RUN_MANIFEST.json` | **2026-08-26 15:51** |

## Checksum manifest was stale — corrected 2026-08-29

`01_lean/SHA256SUMS.txt` was frozen on 08-20 but `GATE_TRANSCRIPT.txt` was
legitimately regenerated on 08-23 (commit `b5057f7`, "synchronize 21 Lean 4
modules and update verification transcript"). The manifest was never
regenerated, so it **failed its own check**:

```
GATE_TRANSCRIPT.txt: FAILED
RUN_003_RESULT.json: OK
sha256sum: WARNING: 1 computed checksum did NOT match
```

The transcript is the correct artifact; the manifest was the stale one. The
manifest has been regenerated against the current files. The failure is recorded
here rather than silently overwritten.

## Known staleness (not fixed here)

`GATE_TRANSCRIPT.txt` reports **21 / 21** targets. The Res-Nova lakefile now
declares more roots than that. This transcript is a record of the 08-23 gate, not
of the current one — **do not cite it as current coverage.** A fresh run is
needed before it is used as evidence for anything.
