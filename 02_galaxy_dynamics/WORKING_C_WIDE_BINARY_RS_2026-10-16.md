# Gaia C3 score of the working-C shell

**Setup.** Action form at \(C = 0.579124707982253\), \(g_e = 1.9\times 10^{-10}\,\mathrm{m\,s^{-2}}\), \(x^*\) held at \(7.035884281332817\times 10^{11}\). The boost is the full mass, mass-ratio and radius grid in `WORKING_C_GAMMA_TABLE.json` (2,700 solves). Newton and the published unscreened two-body curve are scored on the same sample. The \(2.4\times 10^{-10}\) column was not rerun.

**Tier.** The \(\chi^2\) values are `[D]`, in `WORKING_C_WIDE_BINARY_RS.json`. The reproduction control matches `WIDE_BINARY_FINAL.json` with maximum \(\Delta\chi^2 = 0\): clean \(n = 14542\), Newton \(\chi^2 = 9.508\); loose \(n = 20156\), Newton \(\chi^2 = 63.804\).

**Result.** The working-\(C\) shell is not excluded under C3. `excluded_C3` is false.

| Cut | Raw \(\chi^2\) | Calibrated | Injection maximum | Fails the bar |
|---|---|---|---|---|
| Clean | 4.360 | 2.995 | 20.431 | no |
| Loose | 39.605 | 18.171 | 25.750 | no |

On the clean cut the shell is closer to the data than Newton (9.508) and than the unscreened curve (8.657). On the loose cut the calibrated value 18.171 is under the 18.5 bar, so that cut does not fail either. The unscreened curve is also not excluded (clean calibrated 5.229, loose 11.561).
