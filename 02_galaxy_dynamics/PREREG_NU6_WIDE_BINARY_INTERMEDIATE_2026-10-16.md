# Pre-registration: ν₆ on one intermediate wide-binary cut (2026-10-16)

**Frozen before any χ² on this cut.** Assigned by Muse on The Block after Fork A (page `3fc77b95-a965-81a8-ac9e-e595bdbe93c1`). ν₆ stays not excluded on the finished gauntlet. This cut is the one computation she assigned. It does not replace `PREREG_NU6_WIDE_BINARY_2026-10-16.md`.

## What is unchanged

- a₀ = 1.1607×10⁻¹⁰ m s⁻². Not retuned. No new constant. No screen and no x*.
- ν₆(y) = (½ (1 + √(1 + 4 y⁻⁶)))^(1/6).
- Decision field g_e = 1.9×10⁻¹⁰ m s⁻². The column at 2.32×10⁻¹⁰ is reported and is not the decision.
- Force law, vis-viva speeds, bins, Mamajek masses, mass strata, draws (320 Newtonian, 80 model), and the four-bin χ² are those of `nu6_wide_binary.py` and `wide_binary_final.py`.
- Injections: 40 catalogues, 5% contaminants. κ = (median injected χ²) / 3.357. The 18.5 bar is the same 4-degree-of-freedom bar.
- Catalog: `eb21_cols.npz`. Every mask in `wide_binary_fish.prepare` other than the three numbers below is unchanged.

## The cut

`wide_binary_fish.CUTS` is

- clean: R_chance_align ≤ 0.01, RUWE < 1.2, σ_t < 0.10
- loose: R_chance_align ≤ 0.1, RUWE < 1.4, σ_t < 0.20

The intermediate cut is the halfway point of those three, and nothing else:

- R_chance_align ≤ √(0.01 × 0.1) = 0.0316227766
- RUWE < (1.2 + 1.4) / 2 = 1.3
- σ_t < √(0.10 × 0.20) = 0.1414213562

RUWE is averaged arithmetically because the published cuts step by 0.2. The two ratio cuts are averaged geometrically.

Before any model χ² is read, the selected pairs must be strictly nested: every clean pair is intermediate, every intermediate pair is loose, and the intermediate count is strictly between the clean count and the loose count. If that fails, the cut is not intermediate, no exclusion is claimed, and ν₆ stays standing.

## Decision

On this one cut, a model fails when its calibrated χ² exceeds 18.5 and its raw χ² exceeds the maximum of its own 40 injections. Newton passes when Newton does not fail. The clean-cut window [7, 12] is not the pass criterion here. That window belonged to the published clean sample.

ν₆ at g_e = 1.9×10⁻¹⁰ is excluded if and only if ν₆ fails and Newton passes. If Newton fails, the cut does not discriminate and ν₆ stays standing. If ν₆ does not fail, ν₆ stays standing. The model R(s) in each bin is reported. No constant is added if the model fails.

Random stream for this cut: seed 20261016 with offset 450000, distinct from the clean offset 0 and the loose offset 900000 in `nu6_wide_binary.py`.
