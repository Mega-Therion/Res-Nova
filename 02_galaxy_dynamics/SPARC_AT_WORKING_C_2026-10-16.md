# SPARC at the working Lagrangian zero

**Pre-registration:** `PREREG_SPARC_WORKING_C_2026-10-16.md`, commit `cb660b6`. Sample check passed: `load` returned 171 galaxies. Thickness `h_z = 0.1` kpc. `C = 0.579124707982253`, `x*` and `a₀` held fixed.

**Tier.** The three totals are `[D]`, in `SPARC_AT_WORKING_C.json`. Centripetal acceleration is `ν_eff g_N − g_W`, with `g_W` the outward spherical identity and `P(y) − C` inside it.

**Verdict.** Not excluded. The screen total is 18123.519. Newton, from the same fitter with `S = 0`, is 293096.718. The difference is −274973.200, which is not greater than +1. `excluded` is false. The outlier list is empty.

The unscreened `μ_std` total computed in this run is 18123.52096145091, the same digits as `TIDAL_ACTION_SPARC.json`. The screen sits 0.00209 below that comparison. `g_W` does not move the galaxy aggregate.
