# Five screening checks, 2026-10-16

The action-form value is x*_A = 7.035884281332817×10^11. A draft of this note wrote 10^14. a0 = 1.1607×10^{-10} m/s^2. Sections 1, 2 and 3 were redone on 2026-10-16 under the BLK-400 standard: the screen reads only the Newtonian shadow, S = 1/(1+(x/x*)^2), the action keeps W, and the Galactic field is in the comparison. Gates from `TIDAL_TWO_BODY_GATES.json`: G5 momentum imbalance for the action form is 1.05×10^{-4}; the divergence form reaches 0.94×10^{-2}. G10 free-fall residual is 8.8×10^{-13} of g_Ne, and the mass difference is 1.9×10^{-16}.

## 1. Oort cloud

The field is the action-form orientation average at 1 Msun and g_e = 1.9×10^{-10}, which is the Galactic field used for the Sun. W is inside that table. Two readings of the same Γ. The shell column is 2∫(Γ−1)/s^2 ds from 0.1 kAU out to r: the dip and the peak cancel, and that column is −1.0×10^{-6} at 20 kAU. The binding column is 2∫_r^∞ (Γ−1)/s^2 ds, with the tail past 400 kAU held at the last Γ. That is the shift in 1/a of a Newtonian parabola. Γ is log-interpolated in mass between 0.8 and 1.4 Msun, q1 = 0.5.

| r (kAU) | Γ action | binding Δ(1/a) | shell Δ(1/a) from 0.1 kAU | Γ unscreened | unscreened binding |
|---|---|---|---|---|---|
| 5.1 | 0.981 | 1.7×10^{-5} | 2.2×10^{-6} | 1.032 | 3.3×10^{-5} |
| 10.0 | 0.940 | 2.7×10^{-5} | 1.2×10^{-5} | 1.086 | 1.7×10^{-5} |
| 19.6 | 1.283 | 1.4×10^{-5} | −2.6×10^{-7} | 1.088 | 1.1×10^{-5} |
| 47.8 | 1.091 | 3.9×10^{-6} | −1.0×10^{-5} | 1.088 | 4.5×10^{-6} |

The external-field floor is Γ → 1.088, so 2×0.088/r = 8.8×10^{-6} AU^{-1} at 20 kAU. The binding at 19.6 kAU is 1.4×10^{-5} because the peak has not finished. q1 = 0.8 changes the binding by less than 2×10^{-6}. The long-period-comet spike sits near 10^{-4} AU^{-1} `[C]`. The binding is about 7 times smaller than that spike at 20 kAU, and about 4 times smaller at 10 kAU. The shell column is the wrong quantity for that comparison: it throws away the tail. This is not a rerun of the planet-scattering population, and it is not the lopsided torque on perihelia in Vokrouhlický, Nesvorný & Tremaine 2024. That integration is not done.

**RESULT oort_binding_below_the_spike_torque_open.** The 1.0×10^{-6} shell number is withdrawn as a comparison to the spike. The earlier result that the outer cloud stays as MONDian as the unscreened theory used the divergence form without W and stays withdrawn.

## 2. NGC 2419

Inputs `[C]`: Baumgardt et al. 2009, M = 9.0×10^5 Msun, σ = 4.14 ± 0.48 km/s, projected half-light 19 pc. The Plummer used here has a 3D half-mass radius of 26 pc, the later catalogue scale, so the density is a model, not their King fit.

Central density 27.2 Msun/pc^3. From 0.5 to 80 pc, x/x*_A ≤ 0.012 and S ≥ 0.99986. The spherical W term is 3×10^{-7} of g_N at the half-mass radius. There is no Newtonian core.

The Plummer line-of-sight scale is 4.44 km/s with no boost. At the half-mass radius, g_N = 9.28×10^{-11} m/s^2 and ν(g_N/a0) = 1.359, so the isolated scale is 5.18 km/s. A dispersion averages the whole cluster. Along a line, the internal acceleration is ν(|g_N + g_e μ|)(g_N + g_e μ) − ν(g_e) g_e μ, and μ is uniform on [−1, 1]. That average boost is 1.359 at V_c = 150, 180 and 220 km/s, and the scale stays 5.18 km/s. It sits 2.2 error bars above 4.14 ± 0.48 km/s.

V_c^2/R at R = 90 kpc is an assumed centripetal acceleration, not a measured field. At V_c = 180 km/s it is 1.17×10^{-11} m/s^2, and g_N/g_e = 7.96. Treating that number as the Newtonian field and keeping only the subtracting side gave 4.66, 4.59 and 4.51 km/s. The adding side of the same split is 5.64, 5.70 and 5.76 km/s. If V_c^2/R is the true field, the Newtonian external field solves y ν(y) = g_e/a0 and is 1.17×10^{-12} m/s^2 at 180 km/s. The two sides are then 4.95 and 5.39 km/s at 180 km/s, and 4.86–5.02 against 5.33–5.48 across 150–220 km/s. The orientation average does not move. A Jeans model was not fitted.

**RESULT ngc2419_unscreened_orientation_average_stays_at_5.18.** The one-sided parallel row is withdrawn. W does not move the average.

## 3. NGC 5055 at Chae's fixed e_env

Mass held at Υ = 0.55, fd = 0.9. Chae et al. 2020 give e_env = 0.04, so g_ext = 4.8×10^{-12} m/s^2 `[C]`. The shadow Hessian is the galaxy's own spherical tide, x = c^2 √6 g_N /(a0^2 r). On the outer disk x/x*_A is 4×10^{-6} down to 8×10^{-8}, so S = 1. The spherical W estimate is at most 2×10^{-8} of g_N. A disk solve of W is not done.

The Galactic field enters ν through y = |g_N + g_ext|/a0. Its direction is not in the scalar e_env. Outer disk, 16 points, R ≥ 10 kpc:

The  disk  evaluation of  W  is now  run  (`ngc5055_disk_w.py`,  `NGC5055_DISK_W.json`). Same  Υ = 0.55, fd = 0.9, a0 = 1.1607×10^{-10}, x*_A, and C = 0. The midplane tide is the radial derivative of g_N, the azimuthal piece g_N/R, and a vertical piece that closes the trace. On the 16 outer points, x/x*_A reaches 6.08×10^{-6} and S stays above 1 − 4×10^{-11}. The radial acceleration from W is at most 5.20×10^{-11} of g_N. That is smaller than the spherical estimate of 2×10^{-8}, and it does not move the 25 km/s drop. This is the midplane derivative of the baryonic curve, not a 2D Poisson solve. C = 0 remains the failed pre-registered screen.

| g_ext direction | outer χ² | median residual | model drop 14.3 to 54.6 kpc | V at 54.6 kpc |
|---|---|---|---|---|
| none | 326.1 | −8.3 km/s | 10.3 km/s | 191.5 |
| perpendicular | 82.2 | −4.0 km/s | 25.1 km/s | 176.6 |
| parallel | 269.5 | +8.1 km/s | 36.9 km/s | 162.4 |

The data fall 34.0 km/s and are 172 km/s at 54.6 kpc. With the field perpendicular to the baryonic field, the model drop is 25 km/s and the far point is 4.6 km/s high. Screening and W do not move this galaxy. The external field inside ν does.

**RESULT ngc5055_unscreened_external_field_sets_the_drop.**

## 5. What x*_A is, as a tide

`[D]` conversion, not a derivation. With x*_A = 7.035884281332817×10^11, |H|_F = x*_A a0^2 / c^2 = 1.055×10^{-25} s^{-2}. If that norm is 4πGρ, the density is 1857 Msun/pc^3.

Putting the screening edge on the MOND radius would set x* = X_M = 1.774×10^{15}, which is 2.52×10^3 times x*_A. The Sun's edge at this x*_A is 9.73 kAU and the MOND radius is 7.15 kAU. x*_A stays `[O]`: fixed by the Cassini window.

## 4

The  mass-stratified  test is  the  separate pre-registration  written  with  this note.  No Gaia file was opened for it.
