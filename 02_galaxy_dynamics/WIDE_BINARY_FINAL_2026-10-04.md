# Wide-binary test, final pass: calibrated threshold, fixed baseline (2026-10-04)

Method: Amendment C of `PREREG_WIDE_BINARY_FISH.md` (b63bb6b), fixed before these numbers were computed. It is post-hoc relative to the corrected-sample run (`WIDE_BINARY_FISH_RVFIX_2026-10-04.md`, 9c986c0) and closes that run's two loose ends.

| | |
|---|---|
| Runner | `wide_binary_final.py` |
| Numbers | `WIDE_BINARY_FINAL.json` |
| Masses | `mamajek_mg_mass.csv` |

## Loose end 1: the close-bin baseline. Closed `[E]`
Close-bin Newton/data median, RV-fixed sample:

| masses | strict | loose |
|---|---|---|
| old approximate table | 1.034 | 1.015 |
| Mamajek (checked) | **0.994** | **0.987** |

- The 7–10% gap reported earlier came from two sources. One was the RV-only subsample, the 1e20 sentinel bug. The other was the approximate mass table, which runs 7–18% high for M dwarfs; the corrected sample has eight times more of them.
- A mass-dependent residual remains inside the close bin: Newton/data is 0.967 (< 1 M☉), 1.024 (1–1.5) and 1.119 (≥ 1.5).
- That residual is removed from the statistic by fitting each mass stratum against its own control.

## Loose end 2: the threshold. Calibrated `[E]`
Forty injected catalogues per model per cut were run, each built under that model and carrying a 5% contaminant, through the identical pipeline.
- The true-model χ² median is 4.0–6.0, against 3.36 for χ²(4). So κ = 1.2–1.8: the raw χ² is inflated about 1.5× by design.
- The tails are heavy. The largest null values reach 15.4–43.0.

| cut | | N | F | E | S | P |
|---|---|---|---|---|---|---|
| strict | raw χ² | 9.5 | 246.8 | 10.2 | 7.1 | 14.3 |
| strict | κ | 1.73 | 1.57 | 1.45 | 1.50 | 1.37 |
| strict | calibrated | **5.5** | **157.5** | **7.0** | **4.7** | **10.5** |
| strict | null max | 24.4 | 16.9 | 43.0 | 21.8 | 15.4 |
| loose | raw χ² | 63.8 | 531.8 | 31.7 | 16.1 | 60.8 |
| loose | κ | 1.79 | 1.19 | 1.56 | 1.50 | 1.33 |
| loose | calibrated | **35.6** | **445.7** | **20.3** | **10.8** | **45.6** |
| loose | null max | 24.5 | 15.7 | 27.5 | 21.7 | 16.9 |

**Verdict under C3** (calibrated > 18.5 AND raw > null max, in both cuts):
- **F (fish, full boost): excluded.**
- **N, E, S, P: not excluded.** All four pass the strict cut. In the loose cut N, E and P fail both criteria, and S passes. (Corrected 2026-10-08: this line said E "fails only the calibrated one", but the table gives E raw 31.7 > null max 27.5 and calibrated 20.3 > 18.5. The verdict is unchanged, since E passes the strict cut.)

This replaces the reading in 9c986c0, where N and P "failed both cuts" against an uncalibrated threshold.

## Measured R(s), mass-stratified

| bin (kAU) | strict R | loose R | F | S | E | N |
|---|---|---|---|---|---|---|
| 2–5 | 0.992 ± 0.007 | 1.003 ± 0.008 | 1.014 | 1.006 | 1.008 | 1.000 |
| 5–10 | 1.003 ± 0.017 | 1.067 ± 0.011 | 1.115 | 1.028 | 1.023 | 1.000 |
| 10–20 | 1.064 ± 0.023 | 1.078 ± 0.017 | 1.342 | 1.082 | 1.020 | 1.002 |
| 20–30 | 1.095 ± 0.086 | 1.097 ± 0.050 | 1.685 | 1.185 | 1.015 | 1.000 |

Model columns are for the strict cut.

**The 2–5 kAU step is gone in both cuts.** It came from the RV-only subsample and the mass table.

## Where the remaining excess lives: diagnostic, not pre-registered
R by stratum, strict cut:

| bin (kAU) | M < 1 | 1 ≤ M < 1.5 | M ≥ 1.5 |
|---|---|---|---|
| 2–5 | 0.972 ± 0.010 | 1.014 ± 0.012 | 1.015 ± 0.025 |
| 5–10 | 0.939 ± 0.028 | 1.052 ± 0.027 | 1.015 ± 0.032 |
| 10–20 | 0.963 ± 0.084 | 0.995 ± 0.029 | **1.230 ± 0.042** |

- **The excess sits in the heavy pairs. Light pairs run at or below Newton.** The loose cut shows the same pattern: ≥ 1.5 M☉ gives 1.20 and 1.25 at 5–20 kAU, while < 1 M☉ gives 0.98–1.02.
- **This is the wrong direction for any acceleration-driven boost.** At fixed separation, a lighter pair has a lower Newtonian acceleration. F, S and E all predict that lighter pairs get the *larger* boost.
- Companion fraction rises with primary mass. The loose cut (RUWE < 1.4, R_chance ≤ 0.1) carries more unresolved companions, and it is also the only cut where N fails.
- Both facts point to hidden companions in massive systems, not to modified gravity. That is an interpretation `[O]`. The measured part is the stratum split `[E]`.

## Bottom line
- **The fish rule is excluded** in every version of this test, under every sample, cut and interpolating function.
- **With the baseline fixed and the threshold calibrated, the strict sample is consistent with Newton** (calibrated χ² 5.5). It cannot exclude S or E either.
- **The residual excess is concentrated in heavy pairs and in the looser quality cut.** That is the signature of companions, opposite to the signature of acceleration.
