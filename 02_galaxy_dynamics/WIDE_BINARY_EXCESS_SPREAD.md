# Free-scale refit with a spread of inner speeds

**Date:** 2026-10-04. Descriptive. The free-scale column was fit to every bin, so it is not a blinded test.

Each hidden companion draws an inner speed from a lognormal. The fraction, the median speed, and the log-spread are free. Two fits are reported.

**Control-frozen.** The three parameters are fit on 500–2000 AU only.

| cut | fraction | median speed | log-spread |
| --- | ---: | ---: | ---: |
| clean | 0.50 | 0.1 km/s | 0.3 |
| loose | 0.50 | 0.1 km/s | 0.3 |

Median speed relative to 500–1000 AU:

| bin (AU) | clean obs | clean frozen | loose obs | loose frozen |
| --- | ---: | ---: | ---: | ---: |
| 1000–2000 | 0.987 | 0.972 | 0.983 | 0.990 |
| 2000–5000 | 1.018 | 0.980 | 1.039 | 0.982 |
| 5000–10000 | 1.043 | 0.999 | 1.053 | 0.994 |
| 10000–20000 | 1.086 | 1.050 | 1.107 | 1.060 |
| 20000–30000 | 1.120 | 1.148 | 1.159 | 1.174 |

The close pairs still choose the edge of the grid. The frozen curve sits below the 2–5 kAU step (0.980 against 1.018 clean, 0.982 against 1.039 loose) and only catches the widest bin.

**Free-scale.** The same three parameters are fit to the median trend in every bin.

| cut | fraction | median speed | log-spread | sum of squared residuals |
| --- | ---: | ---: | ---: | ---: |
| clean | 0.20 | 0.2 km/s | 0.3 | 0.00040 |
| loose | 0.50 | 0.1 km/s | 0.6 | 0.00101 |

| bin (AU) | clean obs | clean free | loose obs | loose free |
| --- | ---: | ---: | ---: | ---: |
| 1000–2000 | 0.987 | 0.996 | 0.983 | 0.997 |
| 2000–5000 | 1.018 | 1.013 | 1.039 | 1.021 |
| 5000–10000 | 1.043 | 1.039 | 1.053 | 1.037 |
| 10000–20000 | 1.086 | 1.101 | 1.107 | 1.095 |
| 20000–30000 | 1.120 | 1.129 | 1.159 | 1.149 |

A modest spread of inner speeds can describe the rise, once the outer bins are allowed to choose the parameters. On the strict cut that is a 20% companion rate, a median inner speed of 0.2 km/s, and a narrow log-spread of 0.3. On the loose cut the rate sits on the 50% cap, the median speed is 0.1 km/s, and the spread is wider. The 2–5 kAU bin is matched on the strict cut (1.013 against 1.018) and still a bit low on the loose cut (1.021 against 1.039).

This does not decide gravity. It shows the sample trend can be carried by a spread of slow inner orbits if those parameters are fit to the trend itself. The control-frozen version, which is the one that was not shown the outer bins, still misses the 2–5 kAU step.

Script: `wide_binary_excess_spread.py`. Numbers: `WIDE_BINARY_EXCESS_SPREAD.json`.
