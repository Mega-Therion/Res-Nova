# Wide-binary fish test on the corrected sample (2026-10-04)

> **Superseded in part by `WIDE_BINARY_FINAL_2026-10-04.md`.** That run uses checked masses, a mass-stratified ratio and an injection-calibrated threshold (κ ≈ 1.5). With those, N, P, E and S are **not** excluded. Only F is.

**Supersedes the sample in `WIDE_BINARY_FISH_2026-10-04.md`.** That run, and every follow-up up to d8cd8a1, used only pairs whose first star has a DR2 RV. The cause was the 1e20 RV sentinel (`WIDE_BINARY_RV_FIX_AND_POWER.md`, 5014df0). This run uses the pre-registered sample as it was meant to be: 14,777 strict and 20,268 loose pairs.

Statistic, bins, models and threshold are unchanged from `PREREG_WIDE_BINARY_FISH.md` + Amendment A. The only additions:
- the RV fix;
- 8× the Monte Carlo draws (`wide_binary_fish_hiprec.py`);
- two seeds.

## χ², 4 dof, exclusion at 18.5 (seed 1 / seed 2)

| cut | N | F | E (μ_std EFE) | S (Form-2) | P (nesting) |
|---|---|---|---|---|---|
| strict | 23.6 / 29.5 | 267.5 / 318.1 | **13.7 / 15.0** | **7.3 / 4.9** | 21.1 / 24.4 |
| loose | 90.5 / 63.3 | 555.1 / 650.6 | 49.5 / 37.3 | 46.4 / 33.1 | 74.9 / 59.1 |

## Measured R(s) (seed 1; seed 2 within 0.015 except loose 20–30 kAU)

| bin (kAU) | strict n | strict R | loose n | loose R | F | S | E | N |
|---|---:|---|---:|---|---|---|---|---|
| 2–5 | 3222 | 1.010 ± 0.005 | 4757 | 1.024 ± 0.005 | 1.01 | 1.005 | 1.005 | 1.00 |
| 5–10 | 1017 | 1.010 ± 0.015 | 1753 | 1.082 ± 0.012 | 1.11 | 1.03 | 1.02 | 1.005 |
| 10–20 | 375 | 1.107 ± 0.027 | 836 | 1.062 ± 0.015 | 1.345 | 1.095 | 1.025 | 1.00 |
| 20–30 | 65 | 1.093 ± 0.046 | 201 | 1.101 ± 0.070 | 1.65 | 1.19 | 1.01 | 0.995 |

## Reading under the pre-registered rule (excluded only if > 18.5 in BOTH cuts)
- **F (fish, full boost): excluded**, as before, and more strongly.
- **N (Newton): excluded.** **P (nesting): excluded.**
- **E (μ_std EFE) and S (Form-2 screen): not excluded.** Each passes the strict cut in both seeds. S fits best: 7.3 and 4.9.
- **On the strict cut, the 2–5 kAU step is gone (1.010 ± 0.005).** It was a property of the RV-only subsample. The strict excess now starts at 10 kAU, where S predicts it.

## Why this is not yet a claim `[O]`
1. **The loose cut is not calibrated to χ²(4).**
   - Injection recovery there gave true-model χ² up to 18.0 (P) and 18.2 (N), right at the threshold.
   - The loose cut also has a 5–10 kAU excess (1.082) that no model predicts. That points to contamination the flat contaminant cannot absorb.
   - In the loose data N sits at 63–90, well above its injections (6–18), so N's loose failure is not threshold noise. But the loose cut's contaminant model is known to be inadequate.
2. **The close-bin absolute baseline is unexplained.** The Newtonian template runs ~7–10% fast in the closest bin (`WIDE_BINARY_NEWTON_ERRORS.md`). The ratio statistic cancels any constant offset, not one that varies with s.
3. **Bins share the control α** and are treated as independent.
4. **The 20–30 kAU strict bin has 65 pairs.** Its fitted c is 0.0, at the grid edge.
5. **This contradicts the published Newtonian result of Banik et al. 2024 `[C]`** and sits nearer Chae's. A result in that dispute needs the hidden-triple modelling that both papers do and this pipeline does not.

**Status:**
- The fish-rule exclusion stands.
- Newton and nesting fail the pre-registered rule on the corrected sample.
- S (Form-2) is the best fit on the strict cut.
- None of this is a detection until (1)–(2) are fixed: a triple-population contaminant fitted with a free scale, and a close-bin template that matches in absolute terms.

Numbers: `WIDE_BINARY_FISH_RVFIX.json` (1× MC), `WIDE_BINARY_FISH_RVFIX_HP1.json`, `WIDE_BINARY_FISH_RVFIX_HP2.json`.
