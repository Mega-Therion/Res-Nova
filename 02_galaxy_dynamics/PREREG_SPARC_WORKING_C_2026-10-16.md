# Pre-registration: SPARC at the working Lagrangian zero (2026-10-16)

**Frozen before any SPARC number at this C.** Work order from Muse on The Block, 2026-10-16, relaying RY: run the galaxies at the working C. No retune.

## Frozen inputs

- C = 0.579124707982253, the stored `C_oort_peak` at g_e = 1.9×10⁻¹⁰. The window around it is not scanned.
- x* = 7.035884281332817×10¹¹. a₀ = 1.1607×10⁻¹⁰ m s⁻².
- Action form, two-field QUMOND:

```
Qs = z + S(x) (Q(z) - z - C)
ν_eff = 1 + S(x) (ν_std(y) - 1)
w̃ = -(c²/2) S'(x) (P(y) - C) |H| / Hn
g_W = (2/√6) r⁻³ d/dr (r³ w̃)
```

ν_eff does not depend on C. g_W does. The predicted acceleration at a SPARC radius is g = ν_eff g_N + g_W, with g_W from the same spherical identity `tidal_screening_action_sparc.py` already uses. A disk solve of W is not part of this run.

## Sample and fit

- Galaxies: `parameter_ledger.load` on `resolve_sparc_dir`. The published tidal run has 171. If this load does not return 171, the sample is not the frozen one, no exclusion is claimed, and the model χ² is not read.
- One thickness, h_z = 0.1 kpc. The in-plane and 0.3 kpc brackets are not rerun.
- Per galaxy, the same L-BFGS-B fit and Gaussian priors as `tidal_screening_sparc_cassini.fit_tidal`: Υ_d, Υ_b when a bulge is present, and the distance factor. Bounds (0.01, 5) on the mass-to-light ratios and (0.5, 2) on the distance factor. a₀, x*, and C stay outside the fit.
- Newton is the same fitter with S = 0, so g = g_N. It is computed in the run. It is not taken from another file.
- The unscreened μ_std total already on record is 18123.52096145091 (`TIDAL_ACTION_SPARC.json`). It is a comparison. It is not the decision.

## Decision

The aggregate is the sum of the per-galaxy χ² values.

The screen is excluded if and only if its aggregate exceeds the Newtonian aggregate by more than 1. The margin of 1 is larger than the 0.0004 numerical shift already measured for this pipeline, and it is the whole of "significant" in this pre-registration.

A galaxy whose own χ² exceeds both its Newtonian χ² and its unscreened χ² by more than 1 is reported as an outlier. Outliers do not exclude the aggregate.

If the load is not 171 galaxies, the verdict is "sample mismatch" and the screen is not excluded.
