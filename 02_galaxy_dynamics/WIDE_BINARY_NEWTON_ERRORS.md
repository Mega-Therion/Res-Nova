# Newton with measurement noise and eccentricity error

**Date:** 2026-10-04. A forward-model check, not a new gravity fit.

The excess scripts compared the pairs to noiseless orbits drawn from one γ(s). Two pieces were missing. Each binary's sky-velocity error is now added to the Newton draw. γ(s) is Hwang's line plus a normal error of 0.3, the width already used in the sensitivity test, clipped to [0, 2].

Median speed relative to the 500–1000 AU bin. "Newton" is the model.

| bin (AU) | clean pairs | clean, both errors | loose pairs | loose, both errors |
| --- | ---: | ---: | ---: | ---: |
| 2000–5000 | 1.018 | 0.964 | 1.039 | 0.972 |
| 5000–10000 | 1.043 | 0.952 | 1.053 | 0.956 |
| 10000–20000 | 1.086 | 0.911 | 1.107 | 0.976 |
| 20000–30000 | 1.120 | 0.960 | 1.159 | 0.938 |

Noise alone and the eccentricity error alone do the same thing: the model stays near 0.93–0.97 while the pairs sit above 1. The γ(s) law already makes wider orbits a little slower in this median. Scattering γ, and adding the measurement noise, does not turn that into a rise. The 2–5 kAU excess is still not in the Newton model.

Script: `wide_binary_newton_errors.py`. Numbers: `WIDE_BINARY_NEWTON_ERRORS.json`.
