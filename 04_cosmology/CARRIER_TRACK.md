# Track the carrier

**Date:** 2026-10-04. Arithmetic **[D]**. High-z ratios **[C]** from `A0_HIGHZ_MEASUREMENT_2026-09-16.md`.

Bob McGwier's account of the Vega balloons, Danny Jones, 22 May 2026: the gondola was a pendulum in a high wind, the oscillator was hot and jittery, and a linear receiver could not hold the signal. His nonlinear filter estimated that moving state. Once the carrier was tracked, the modulation stood still, because it had a fixed relationship to the carrier.

The same test, on the numbers we have. Two choices for the carrier.

| Epoch | Galaxies, relative to local | Expansion H/H0 | Galaxies divided by the expansion |
| --- | ---: | ---: | ---: |
| z = 0 | 1.00 | 1.00 | 1.00 |
| z ≈ 0.9 | 2.60 | 1.65 | 1.57 |
| z ≈ 2 | 2.29 | 2.98 | 0.77 |

Across the two high-redshift bins, the galaxy measurements move by 0.31. Divided by the expansion, they move by 0.80. The thing that stands still is the galaxy scale. The expansion is the gondola. Using it as the carrier makes the message wander.

Reversed polarity does not change that. Flipping a ratio, galaxy/H versus H/galaxy, or flipping the galaxy number itself into 1/galaxy, leaves the proportional scatter the same: 0.128 in the log for the galaxy and its reciprocal, 0.715 for either way of dividing by H. Multiplying instead of dividing, the other sign, has log-scatter 0.460. That is better than dividing by the expansion and worse than leaving the galaxy scale alone. The smaller linear spread of the reciprocals is only the numbers being smaller. In proportion it is the same scatter.

The step from the local bin down to 1.00 is the calibration limit already in the high-z audit. It is not the carrier.

Script: `carrier_track.py`.
