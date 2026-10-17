# Wide-binary shell at the working Lagrangian zero

**Setup.** Action form, \(x^* = 7.035884281332817\times 10^{11}\) held fixed, \(g_e = 1.9\times 10^{-10}\,\mathrm{m\,s^{-2}}\), \(M = 0.8\,M_\odot\), \(q_1 = 0.5\). Orientation average is the published 4-point Gauss rule. \(C = 0\) against `C_oort_peak` \(= 0.579124707982253\). This is one mass, not the Gaia \(\chi^2\).

**Tier.** The curve is `[D]`, from `wide_binary_at_working_c.py` into `WIDE_BINARY_AT_WORKING_C.json`.

**Control.** At \(C = 0\) the solver returns \(\Gamma_r = 0.90080\) at 8.0 kAU and \(1.34325\) at 17.5 kAU. The published action-form row is 0.901 at 8.0 kAU and 1.343 at 17.5 kAU.

**Result.** The working \(C\) pulls the shell toward Newton. The minimum on this grid goes from 0.90080 at 8.0 kAU to 0.98555 at 8.0 kAU. The maximum goes from 1.34727 at 16.9 kAU to 1.13360 at 17.5 kAU. The largest change is \(-0.214\) at 16.9 kAU. At 40 kAU the two curves are 1.09464 and 1.08889. The dip and the peak both shrink. They do not disappear.
