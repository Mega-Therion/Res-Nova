# What the 2 kAU step tracks: result (2026-10-04)

Pre-registration: `PREREG_WIDE_BINARY_STEP.md`.
- 7216165: the original rules.
- da01fda: Amendment A, continuous crossing with ≥ 100 pairs and ≥ 2σ.
- d4eac60: Amendment B, power check.

All three were committed before any split was computed.

## Verdict
**Both tests are inconclusive, under the original and the amended rules, on both cuts.** This was expected.
- Amendment B showed zero power at these slice sizes: a true 5% step returns "inconclusive" in 40 of 40 trials, whichever way it tracks.
- This catalog, with these cuts, cannot say whether the step tracks arcseconds, AU, or acceleration.

| runner | test 1 strict | test 2 strict |
|---|---|---|
| original (`wide_binary_step_track.py`) | inconclusive | inconclusive |
| amended (`wide_binary_step_track_amended.py`) | inconclusive (no step in either slice) | inconclusive (no step in either slice) |

## Descriptive only: R per slice relative to that slice's 500–1000 AU median (± bootstrap SE; bins with < 100 pairs blank)

| strict slice | n | 1–2 kAU | 2–5 kAU | 5–10 kAU | 10–20 kAU |
|---|---:|---|---|---|---|
| < 100 pc | 1411 | 0.941 ± 0.048 | 1.006 ± 0.055 | 0.997 ± 0.070 | — |
| 100–200 pc | 6025 | 0.990 ± 0.025 | 1.019 ± 0.028 | 1.052 ± 0.039 | 1.063 ± 0.045 |
| M < 1 M☉ | 693 | 0.860 ± 0.052 | 0.870 ± 0.054 | — | — |
| M ≥ 1.5 M☉ | 2027 | 1.041 ± 0.052 | 1.061 ± 0.048 | 1.111 ± 0.085 | 1.057 ± 0.065 |

| loose slice | n | 1–2 kAU | 2–5 kAU | 5–10 kAU | 10–20 kAU |
|---|---:|---|---|---|---|
| < 100 pc | 1888 | 0.950 ± 0.044 | 1.018 ± 0.048 | 1.001 ± 0.066 | — |
| 100–200 pc | 7909 | 0.993 ± 0.023 | 1.039 ± 0.024 | 1.067 ± 0.036 | 1.098 ± 0.029 |
| M < 1 M☉ | 982 | 0.893 ± 0.047 | 0.919 ± 0.054 | — | — |
| M ≥ 1.5 M☉ | 2486 | 1.072 ± 0.045 | 1.061 ± 0.043 | 1.186 ± 0.087 | 1.131 ± 0.063 |

- **P values:**
  - P₁ (distance ratio) = 1.93 strict, 1.99 loose.
  - P₂ (√ mass ratio) = 1.345 strict / 1.341 loose with the script table, and 1.353 / 1.350 with Mamajek masses.
- **Not interpreted.** These patterns were not pre-registered as tests and every row is within about 3σ of 1:
  - The rise is visible only in the 100–200 pc slice.
  - Light pairs run *below* their own close bin; heavy pairs run above.
- The light-vs-heavy split in shape (0.86 vs 1.04 at 1–2 kAU, strict) is the largest contrast in the table. A mass-dependent systematic is one candidate. It is a lead, not a result.

## What would answer the question
- **More pairs.** At ~5% amplitude, each slice needs several thousand pairs per bin.
- **Options:**
  - extend the distance limit past 200 pc, accepting worse velocity precision;
  - use a DR3-based wide-binary catalog.
- **Rule:** re-run the Amendment B power check on any new sample before it is fit.

Numbers: `WIDE_BINARY_STEP_TRACK.json` (original rules), `WIDE_BINARY_STEP_TRACK_AMENDED.json`, `WIDE_BINARY_STEP_POWER.json`.
