# RV-sentinel fix and power of the step-tracking tests (2026-10-04)

## The bug `[E]`
- El-Badry+2021 stores a missing DR2 radial velocity, and its error, as 1e20, not NaN.
- `prepare()` and `surviving_mask()` tested `np.isfinite`, which is always true for 1e20. Star 1's "RV" of 1e20 was therefore always used, and its 1e20 error put σ(ṽ) far above every cut.
- **Effect:** every wide-binary result before this fix was computed only on pairs whose *first* star has a DR2 RV. Velocities for those survivors were correct. The sample was a bright-primary subsample, not the pre-registered one, and the 35 km/s unknown-RV term never applied.
- Affected: b939187, 75a3a1a, 90f63fa, 35446ee, 33d6b6d, 35c994f, b117c39, e9e1b15, 20f5c93, d8cd8a1, 5655d3d.
- **Fix:** `_rv()` maps |x| ≥ 1e10 to NaN in both copies (`wide_binary_fish.py`, `wide_binary_step.py`). The distance limit is now a module parameter, `DMAX`, still 0.2 kpc by default.

| sample | strict n before → after | light (< 1 M☉) | heavy (≥ 1.5 M☉) |
|---|---|---|---|
| d < 200 pc | 7,436 → 14,777 | 693 → 5,904 | 2,027 → 2,300 |
| d < 500 pc (after fix) | 38,148 | 7,552 | 13,376 |
| d < 1 kpc (after fix) | 41,690 | 7,553 | 16,836 |

## Power of the step-tracking tests (synthetic ṽ only, no Gaia velocities read)
Fraction of correct calls with a true 5% step, strict cut:

| statistic | sample | test 1 (AU / arcsec) | test 2 (AU / acceleration) |
|---|---|---|---|
| Amendment A crossing | d < 200 pc (fixed) | 2.5% / 0% | 0% / 0% |
| Amendment A crossing | d < 500 pc, split 200 pc | 10% / 0% | 7.5% / 2.5% |
| joint step-model fit (Δχ² ≥ 4) | d < 200 pc | 2.5% / 0% | 0% / 0% |
| joint step-model fit | d < 500 pc | 15% / 10% | 0% / 0% |

Scaling the d < 500 pc sample by replication (joint fit, 5% step):

| pairs | test 1 correct (AU / arcsec) | test 2 correct (AU / acceleration) |
|---:|---|---|
| 190,740 (×5) | 70% / 55% | 10% / 5% |
| 381,480 (×10) | 90% / 95% | 55% / 5% |
| 762,960 (×20) | 100% / 100% | 80% / 30% |

- Test 1 needs about 380k pairs at this velocity precision.
- Test 2 needs more than 760k. Its light slice limits it.
- No existing catalog cut to this precision is that large: El-Badry EDR3 gives 41.7k strict and 71.8k loose out to 1 kpc. **What the step tracks cannot be decided with Gaia EDR3/DR3 wide binaries.**

Scripts: `wide_binary_step_power2.py`, `wide_binary_step_power3.py`, `wide_binary_step_power_scale.py`. Numbers: `WIDE_BINARY_STEP_POWER2.json`, `WIDE_BINARY_STEP_POWER3.json`, `WIDE_BINARY_STEP_POWER_SCALE.json`.
