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
