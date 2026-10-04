# K_B scan, one grid, 2026-10-04

Pre-registered in `kb_scan_c1.py` before the run. A held remnant means the Newton solve converges and Y/Y_static at 0.3 kpc is above 0.5. One grid cannot show box convergence. No no-go is adopted.

Grid: 16×32, v = 100 km/s, box edge 10 kpc, g_e = 0. Same setup as the converged row of `BOX_SWEEP_C1_16x32.json`.

| K_B | converged | Y/Y_static | g/g_static | held |
| ---: | --- | ---: | ---: | --- |
| 0.25 | yes | 0.001889 | 0.1419 | no |
| 0.50 | yes | 0.037206 | 0.1732 | no |
| 1.00 | yes | 0.003015 | −0.3254 | no |

K_B = 0.5 reproduces the earlier box-sweep Y/Y_static of 0.03720584543762056. The negative g ratio at K_B = 1 is recorded. It is not given a physical reading from this one grid.
