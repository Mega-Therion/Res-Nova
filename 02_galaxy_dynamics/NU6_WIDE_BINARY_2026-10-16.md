# ν₆ on the Gaia wide-binary energy-integral test

**Pre-registration:** `PREREG_NU6_WIDE_BINARY_2026-10-16.md`, commit `8de0f27`, frozen before this run. Work order BLK-403. The Oort proxy in `b6ad903` had already left ν₆ alive.

**Tier:** the χ² values, κ, and `excluded_C3` below are `[D]`, computed by `nu6_wide_binary.py` into `NU6_WIDE_BINARY.json`. This is the El-Badry+2021 sample under the Amendment C cuts. It is not a new Gaia DR4 pre-registration.

**Verdict, from that JSON.** The Newton control is informative (`newton_control_informative` is true): clean-cut Newton χ² is 7.861, inside the frozen window [7, 12]. The published pipeline value 9.508 is a different seed. ν₆ at g_e = 1.9×10⁻¹⁰ is **not excluded** under C3 (`excluded_C3` is false). The second column at 2.32×10⁻¹⁰ is also not excluded. No constant was added and a₀ was not retuned.

C3 excludes only when both cuts have calibrated χ² above 18.5 and raw χ² above the maximum of 40 injections. Clean ν₆: raw 8.812, calibrated 7.138, injection maximum 18.439, κ = 1.235. That cut does not clear either bar. Loose ν₆: raw 71.415, calibrated 32.458, injection maximum 21.540, κ = 2.200. That cut clears both bars, and so does Newton on the same cut (raw 72.028). The loose failure is shared with the Newtonian control, so it is not a ν₆-specific kill. The decision uses both cuts, and the clean cut does not exclude.

Shape, four-bin model ratios on the clean cut, Newtonian template versus ν₆: 1.002 versus 1.000 (2–5 kau), 1.006 versus 0.997 (5–10), 1.007 versus 0.997 (10–20), 1.010 versus 0.990 (20–30). The curves sit on each other. No dip-then-peak is visible at this precision. The loose cut is the same story (widest bin 0.995 versus 0.998).

Dwarf mass-to-light ratios are not started in this file. The loose cut's Newtonian χ² of 72 is outside the clean-cut control window, and that has to be read before a dwarf campaign is treated as unlocked.
