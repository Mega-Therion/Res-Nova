# The galaxy is the anchor

**Status:** [D] for the arithmetic. The high-z galaxy ratios are [C], taken from `A0_HIGHZ_MEASUREMENT_2026-09-16.md`. The 2π divisor is [O].
**Date:** 2026-10-04

The fixed point is the galaxy measurement. Locally that is SPARC T3, \(a_0 = 1.16306\times 10^{-10}\,\mathrm{m\,s^{-2}}\). At higher redshift the galaxies measured in that bin are the anchor for that epoch. The moving scale is \(cH(z)\) in flat Planck 2018 (\(H_0 = 67.36\), \(\Omega_m = 0.3153\)). \(cH(z)/2\pi\) is reported beside it. `HorizonScale.lean` derives \(a = cH\), not the extra \(2\pi\).

| Epoch | Galaxy anchor | \(cH\) / galaxy | \((cH/2\pi)\) / galaxy |
| --- | ---: | ---: | ---: |
| \(z = 0\), SPARC T3 | \(1.163\times 10^{-10}\) | 5.627 | 0.896 |
| RC100, \(z_{\rm eff} = 0.867\) | \(3.021\times 10^{-10}\) | 3.584 | 0.570 |
| RC100, \(z_{\rm eff} = 1.960\) | \(2.659\times 10^{-10}\) | 7.327 | 1.166 |

At \(z = 0\), \(cH\) sits 4.63 times above the galaxy scale. The declared \(2\pi\) form sits 10% below it. Neither is the fixed point.

If the horizon scale were tracking the expansion, \(cH(z)\) would stay in a fixed ratio to the galaxies measured at that \(z\). It does not. The ratio is 5.6 locally, 3.6 near \(z = 0.9\), and 7.3 near \(z = 2\). The \(2\pi\) form swings from 0.90 to 0.57 to 1.17. The high-z audit already found the galaxy scale itself flat from \(z = 0.6\) to \(2.6\), with the step from \(z = 0\) limited by calibration. This table is that fact written with the galaxy held still and the horizon expression as the thing that moves.

Script: `galaxy_anchor_horizon_comparison.py`. Numbers: `GALAXY_ANCHOR_HORIZON.json`.
