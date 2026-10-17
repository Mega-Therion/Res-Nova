# Pre-registration: four dwarfs at the working Lagrangian zero (2026-10-16)

**Frozen before any dwarf mass-to-light number at this C.** Work order from Muse on The Block, 2026-10-16, RY approved. No retune.

## Frozen inputs

- C = 0.579124707982253. x* = 7.035884281332817×10¹¹. a₀ = 1.1607×10⁻¹⁰ m s⁻².
- V = 200 km s⁻¹. g_ext = V² / D_gc, the true external field used by `dwarf_screening_test.py`.
- Data and geometry are `dwarf_screening_test.load` on `dwarf_data/lvdb_dwarf_mw.csv`. Stars only. The half-light radius is the circularized radius that loader returns.
- The four dwarfs are Crater II, Carina, Leo II, and Sculptor. No other satellite enters the verdict.
- ν is `tidal_screening_two_body.nu` (ν_std). P is `tidal_screening_two_body.P`. S and S′ come from `screen(x, x*, "action")`.

## Prediction

One formula at the half-light radius. Newtonian σ_N² = G M / (3 r_h). The screen uses the same Wolf normalization,

```
g_N = G M / r_h²
H_int = √6 G M / r_h³
H_ext = √6 g_ext / D_gc
x = c² hypot(H_int, H_ext) / a₀²
ν_eff = 1 + S(x) (ν(g_N/a₀) - 1)
g_in = ν_eff g_N - g_W
σ² = max(g_in, 0) r_h / 3
```

g_W is the outward spherical identity. On 64 radii spaced logarithmically from 0.2 r_h to 5 r_h,

```
w(r) = -(c²/2) S'(x(r)) (P(g_N(r)/a₀) - C) H_int(r) / hypot(H_int(r), H_ext)
g_W = (2/√6) r⁻³ d/dr (r³ w)
```

and the value kept is the node nearest r_h. There is no second isolated-branch formula and no minimum against it.

## Decision

M/L_V is the stellar mass-to-light whose predicted dispersion equals the measured line-of-sight dispersion. The decision value is that solve at σ − 1σ, using the catalog's minus error. The mass grid is the same geometric grid as `nu6_dwarf_ml.py`, from 0.05 to 400.

The BLK-39 rule, unchanged:

- Pass only if all four decision values are ≤ 3.
- Fail only if all four decision values are ≥ 5.
- Anything else is inconclusive.

Newton is the same solver with S = 0 and g_W = 0. It is not the decision. The run is informative only if the four Newtonian decision values match `BRANCH_RULE_SATELLITES.json` to a relative tolerance of 10⁻³. If that fails, the verdict is "not informative" and the screen is not passed and not failed. No mass-to-light is tuned.
