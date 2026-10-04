# Pre-registration: what the 2 kAU step tracks

**Date:** 2026-10-04. Written before either split is computed.

The close-bin baseline is matched. Mass, distance, and chance alignment, matched pair by pair, do not remove a step that starts at 2–5 kAU. This note fixes two tests and the rule that reads them. No split below is looked at until this file is committed.

The speed in a bin is the median of ṽ for pairs with 0 < ṽ < 5. A step is present in a slice when some bin has at least 30 pairs and its median exceeds the 500–1000 AU median in that same slice by 3% or more. The step location is the log-midpoint of the first such bin, in AU and, for test 1, in arcseconds. Bins with fewer than 30 pairs are skipped.

## Test 1. Angle versus distance

Gaia's errors depend on the angular separation, not on the true separation in AU. The same 2 kAU pair is about 20 arcsec at 100 pc and about 10 arcsec at 200 pc.

Distance split, fixed, not the sample median: nearer than 100 pc, and 100–200 pc.

AU bins: 500–1000, 1000–2000, 2000–5000, 5000–10000, 10000–20000, 20000–30000.

Angle bins, arcseconds: 5–10, 10–20, 20–40, 40–80, 80–160.

Decision, in this order:

- If both distance slices have a step and it falls in the same angle bin, while the AU bins differ: the step tracks arcseconds. It is instrumental. Wide binaries then say Newton in this regime.
- If both slices have a step and it falls in the same AU bin, while the angle bins differ: the step tracks AU. It is not an astrometry artifact.
- Otherwise: inconclusive.

## Test 2. Does the step track acceleration?

Run only the strict cut. Mass split, fixed: total mass below 1 solar mass, and total mass at or above 1.5 solar masses. The middle is not used.

If the step is set by a fixed Newtonian acceleration, the heavier pairs reach it farther out, in proportion to √M. The predicted ratio of step locations is √(median mass of the heavy slice / median mass of the light slice). Those medians are properties of who is in the slice. They are not fit.

Decision:

- If both slices have a step, and the ratio of their AU locations is within 20% of that √M prediction: the step tracks acceleration.
- If both slices have a step in the same AU bin: the step does not track mass. It stays a population effect.
- Otherwise: inconclusive.

## What the outcomes mean

- Tracks arcseconds: instrumental. No gravity claim from this step.
- Tracks AU but not mass: population, still not gravity.
- Moves as √M: acceleration-driven. That would be a gravity signal, and it would still have to face Cassini.

Script to be run after this file is committed: `wide_binary_step_track.py`.

## Amendment A (2026-10-04): committed before any split is computed

`WIDE_BINARY_STEP_TRACK.json` does not exist when this is committed, and no slice has been looked at. The original rules stay recorded above. They are also run and reported, but these amended rules decide.

**A1. Why.**
- Step locations at bin log-midpoints (1414, 3162, 7071 … AU) can only differ by ×1 or ×2.0–2.2. Test 2's √M window (1.13–1.69 for a mass ratio near 2) is therefore unreachable, so the acceleration outcome could never be returned.
- A 3% threshold on a 30-pair median is below its noise, which is about 13%.

**A2. Step bin.**
- A bin is a *step bin* when it has ≥ 100 pairs and its median ṽ (0 < ṽ < 5) exceeds the slice's 500–1000 AU median by ≥ 3%.
- That excess must also be ≥ 2σ, where σ is the bootstrap SE of the ratio of the two medians (1000 resamples, seed 20261004).
- The reference 500–1000 AU bin must itself have ≥ 100 pairs, or the slice is *no step*.

**A3. Continuous crossing.**
- The step location is where R = median/reference crosses 1.03.
- It is found by linear interpolation in log(x) between the last non-step bin before the first step bin and that step bin.
- If the first step bin is the first bin after the reference, interpolation runs from the reference (R = 1 at its log-midpoint).
- x is s (AU) or g_N = G M/s² (units of a0 = 1.042e-10 m/s²).

**A4. Test 1 (angle vs AU), strict cut decides, loose reported.**
- Slices: d < 100 pc and 100–200 pc, as before. Compute s_cross in AU for each slice.
- Predictions for Q = s_cross(far)/s_cross(near):
  - AU-tracking predicts Q = 1.
  - Arcsecond-tracking predicts Q = P₁ = median d(far)/median d(near), computed from slice membership and not fit.
- Decision:
  - **tracks_AU** if |ln Q| < |ln(Q/P₁)| and |ln Q| ≤ ln 1.2.
  - **tracks_arcseconds** if |ln(Q/P₁)| < |ln Q| and |ln(Q/P₁)| ≤ ln 1.2.
  - Otherwise, or if either slice has no step: **inconclusive**.

**A5. Test 2 (acceleration vs AU), strict cut decides, loose reported.**
- Slices: total M < 1 M☉ and M ≥ 1.5 M☉, as before. Compute s_cross for each slice.
- Predictions for Q = s_cross(heavy)/s_cross(light):
  - AU-tracking predicts Q = 1.
  - Acceleration-tracking predicts Q = P₂ = √(median M heavy / median M light).
- Decision uses the same rule as A4, with P₂ in place of P₁ and the outcome names **tracks_acceleration** / **tracks_AU** / **inconclusive**.
- g_N-binned rows (edges at 2^k a0, k = −3 … 9) and the g_N crossing are reported as supporting numbers only.

**A6. Mass caveat.**
- The M-dwarf masses from the script's table run 7–18% high against Mamajek (be768c0).
- P₂ is reported from both the script table and the Mamajek table. The decision uses the script table, because it is the table every earlier result used.

Runner: `wide_binary_step_track_amended.py`. The original runner `wide_binary_step_track.py` is run unchanged for the original rules.
