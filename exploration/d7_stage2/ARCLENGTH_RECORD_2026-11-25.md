# Arclength continuation (prereg `ab5a00ef`): record of a stopped run, 2026-11-25

**Status:** stopped by RY's direction (`03_observer_jwst/OBSERVATION_TIER_DIRECTIVE_2026-11-25.md`). AeST's branch dynamics for satellites moving through the Milky Way is a MOND-completion question at the wrong tier for ITT. **No pre-registered outcome was reached.** D7 stays `[O]` as a statement about AeST.

## What ran

| Gate | Result |
|---|---|
| G1, static held state (Λ frozen) | **PASS**: residual 5.9e-12 |
| G0, bordered corrector reproduces the cached stripped state at 20 km/s | **PASS**: residual 2.8e-11, Y/Y_static = 0.015369 (target 0.0154 ± 1e-4) |
| G2, natural Newton at 0.25 km/s from the static state | **FAIL**: stalls at residual 2.87 |

- **Run A (held branch upward)** was not started, because G2 failed (as pre-stated). This repeats the October C¹ result: `STAGE_C_C1_OLDNEWTON` failed at 0.125 km/s. The likely cause is the Λ zero mode, which is exact at v = 0 and only weakly lifted for v > 0. That makes the static state a singular starting point. This is a diagnosis, not tested here.
- **Run B (stripped branch downward)** accepted one step, to p = 19.966 km/s. The tangent's p-component fell from −0.707 to −0.456 in that step, and the corrector then failed at 19.75–19.94 km/s.
  - This is *consistent with* a lower fold of the stripped branch near 19.9 km/s, which matches where natural continuation was lost before (19.4–20).
  - It is an indication only: the pre-registered FOLD-STRIPPED criterion needs the sign change of ṗ and the eigenvalue trend, and neither was reached.

## Operations note

- The first attempt used a monolithic bordered LU and a cache of 7 problems. It hit the system OOM killer, with 3.0 GB resident on an 11 GB machine already under load, and the OOM event also killed a self-hosted CI runner job.
- The runner restarted on its own, and the killed jobs were re-queued.
- The rerun used block elimination, a cache of 3, and a 2.5 GB `MemoryMax` cap. It stayed under 1.5 GB.

## Artifacts

`arclength_c1.py`, `ARCLENGTH_C1.txt`, `ARCLENGTH_C1_attempt1_oomkilled.txt`, `ARCLENGTH_C1_ge0.003_16x32.json`.
