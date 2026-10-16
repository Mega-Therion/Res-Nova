# Pre-registration: ν₆ wide binaries with energy-integral speeds (2026-10-16)

**Frozen before any ν₆ wide-binary number in this file's pipeline.** Work order: The Block, BLK-403. Follows the Oort proxy result in `b6ad903`, which did not kill ν₆.

## Frozen parameters

- a₀ = 1.1607×10⁻¹⁰ m s⁻². Not retuned.
- ν₆(y) = (½ (1 + √(1 + 4 y⁻⁶)))^(1/6).
- External field for the decision: g_e = 1.9×10⁻¹⁰ m s⁻². A second column at 2.32×10⁻¹⁰ is reported and is not the decision.
- No screening function and no x*.
- Catalog: the El-Badry+2021 column file `eb21_cols.npz` already used by `wide_binary_final.py`. Cuts, bins, Mamajek masses, and the mass strata are those of `wide_binary_final.py` (Amendment C). The clean cut is the strict cut.
- Force law: the external-field QUMOND form called `E` in `wide_binary_fish.py`, with ν₆ in place of ν_std, including the two-body factor Q. The angle between the separation and g_e is drawn once per orbit and held fixed, as in the energy-integral correction `f5f370e`.
- Speed: the vis-viva factor from Φ = −∫ g dr between the same periapsis and apoapsis. It is not √Γ evaluated at the current radius.
- Seed for the reported run: 20261016. Draws per binary: 320 for the Newtonian template, 80 for each model curve.

## Control, before the ν₆ verdict is read

Newton in this same script is the energy integral of GM/r², which is Kepler. The run is informative only if the clean-cut Newton χ² lands in [7, 12]. The published clean-cut Newton χ² is 9.508 (`WIDE_BINARY_FINAL.json`). A Newton χ² outside [7, 12] means this script's Monte Carlo does not match that pipeline, and no ν₆ exclusion is claimed.

## Decision

χ² is the four-bin sum used by `wide_binary_final.py`. The exclusion threshold 18.5 is the one already frozen for 4 degrees of freedom.

Criterion C3, same wording as `PREREG_TIDAL_WIDE_BINARY_2026-10-15.md`: ν₆ is excluded only if, on both the clean and the loose cut, the calibrated χ² exceeds 18.5 and the raw χ² exceeds the maximum of 40 injected catalogues of ν₆. κ = (median injected χ²) / 3.357.

Otherwise ν₆ is not excluded on this test. The model R(s) in each bin is reported so a dip-then-peak can be seen. No constant is added if the model fails.
