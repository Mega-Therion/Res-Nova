# Pre-registration: ν₆ stellar mass-to-light for four dwarfs (2026-10-16)

**Frozen before any ν₆ dwarf mass-to-light number in this file's pipeline.** Work order: The Block, BLK-403, continued by ry after the wide-binary result in `4a050e5`. Oort proxy `b6ad903` preserves the peak. Wide binaries are not excluded under C3. The loose-cut Newtonian χ² of 72 is recorded there and is not reopened here.

## Frozen parameters

- a₀ = 1.1607×10⁻¹⁰ m s⁻². Not retuned.
- ν₆(y) = (½ (1 + √(1 + 4 y⁻⁶)))^(1/6), y = g_N / a₀.
- No screening function and no x*. No new constant.
- Milky Way speed V = 200 km s⁻¹. External acceleration g_ext = V² / D_gc is the true field used by `dwarf_screening_test.py`.
- Data and geometry are `dwarf_screening_test.load` on `dwarf_data/lvdb_dwarf_mw.csv` (Pace 2025, Local Volume Database). Stars only. Half-light radius is the circularized radius that loader already returns.
- The four dwarfs are Crater II, Carina, Leo II, and Sculptor. No other satellite enters the verdict.

## Prediction

Same skeleton as `dwarf_screening_test.predict`. Newtonian σ_N² = G M / (3 r_h). Isolated deep-MOND σ_iso = (4 G M a₀ / 81)^(1/4). That isolated formula is the shared y⁻¹/² limit of ν₆ and of ν_std, and it is not refitted.

External-field branch: the boost is 1/μ(g_ext/a₀), where μ is the inverse of the interpolating function. For ν₆, y is solved from y ν₆(y) = g_ext/a₀ and the boost is ν₆(y). σ_efe² = σ_N² times that boost. The reported dispersion is the minimum of σ_iso and σ_efe.

## Decision

For each dwarf, M/L_V is the stellar mass-to-light whose predicted dispersion equals the measured line-of-sight dispersion, and the decision value is the same solve at σ − 1σ, using the catalog's minus error. The BLK-39 rule, unchanged:

- Pass only if all four decision values are ≤ 3.
- Fail only if all four decision values are ≥ 5.
- Anything else is inconclusive.

Newton is reported beside ν₆ and is not the decision. Newtonian σ_N does not depend on a₀. The run is informative only if the four Newtonian decision values match `BRANCH_RULE_SATELLITES.json` to a relative tolerance of 10⁻³. No mass-to-light is tuned to force a pass.
