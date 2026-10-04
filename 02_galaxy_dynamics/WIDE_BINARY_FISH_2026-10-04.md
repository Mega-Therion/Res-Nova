# Wide-binary test of the fish rule: result (2026-10-04)

Pre-registration: `PREREG_WIDE_BINARY_FISH.md` (dcca5d0) + Amendment A (096c8a8), committed before any fit.
Data `[E]`: El-Badry, Rix & Heintz 2021, Gaia EDR3 wide binaries, Zenodo 4435257. 1,817,594 pairs read.
Scripts: `wide_binary_extract.py`, `wide_binary_fish.py`, `wide_binary_fish_sensitivity.py` (exploratory).
Outputs: `WIDE_BINARY_FISH.json`, `WIDE_BINARY_FISH_SENSITIVITY.json`.

## Validation (pre-registered injection recovery)
χ² of the injected model, 4 dof, threshold 18.5:

| cut | N-injection χ²(N) | F-injection χ²(F) | P-injection χ²(P) | F on N-injection |
|---|---|---|---|---|
| clean | 3.7 | 0.9 | 7.1 | 608.5 |
| loose | 9.2 | 4.8 | 6.1 | 1362.7 |

Every injected model was recovered below threshold, and F separates from N by >300 in χ². The run counts as a verdict run.

## Measured R(s) = α(s)/α(0.5–2 kAU)

| bin (kAU) | clean n | clean R | loose n | loose R | F | S | E | P | N |
|---|---|---|---|---|---|---|---|---|---|
| 2–5 | 1943 | 1.045 ± 0.011 | 2558 | 1.063 ± 0.009 | 1.015 | 1.005 | 1.005 | 1.01 | 1.005 |
| 5–10 | 691 | 1.040 ± 0.023 | 1004 | 1.072 ± 0.018 | 1.106 | 1.02 | 1.015 | 1.01 | 1.005 |
| 10–20 | 301 | 1.099 ± 0.035 | 534 | 1.130 ± 0.025 | 1.332 | 1.075 | 1.005 | 1.00 | 1.015 |
| 20–30 | 62 | 1.109 ± 0.057 | 154 | 1.063 ± 0.025 | 1.724 | 1.171 | 1.015 | 1.005 | 1.015 |

Model columns are the clean-cut predictions. The loose-cut predictions differ by ≤0.05.

## Pre-registered χ² (4 dof; excluded if > 18.5)

| cut | N | F | E | S | P |
|---|---|---|---|---|---|
| clean | 23.2 | **174.8** | 23.6 | 14.9 | 22.5 |
| loose | 93.7 | **732.1** | 59.4 | 76.0 | 96.8 |

## Verdict under the pre-registered rule
- **F (pure fish: the binary is its own system, full internal boost) is EXCLUDED under both cuts.** `[E]`
  - Robustness: across the exploratory eccentricity shifts (γ ± 0.3) and both anchorings, χ²(F) ranges 147–1191. The data never rise toward 1.33/1.72.
- **N, E, S and P: no verdict.**
  - None is excluded under both cuts. S passes clean (14.9) and fails loose (76.0).
  - N, E and P fail both, but see the systematic below. Re-running the same pipeline with a different random seed moved these χ² values by up to ~10 (clean N: 23.2 vs 32.8). Near-threshold values are not stable at NMC = 40.

## Unmodelled systematic `[E]`
- R is already 1.045 (clean, 4σ) and 1.063 (loose, 7σ) in the 2–5 kAU bin.
- There g_N ≈ 10 a0, and every model predicts ≤ 1.015.
- No gravity model in this test produces that offset, so it is a sample or forward-model systematic. Candidates are the eccentricity prior γ(s), hidden companions growing with s, and the M_G→mass relation. It dominates the N/E/P/S χ².

## Exploratory, NOT pre-registered: anchor R to the 2–5 kAU bin (3 dof)

| variant | N | F | E | S | P |
|---|---|---|---|---|---|
| clean, γ nominal | 0.8 | 174.3 | 0.4 | 7.6 | 1.3 |
| loose, γ nominal | 7.4 | 683.4 | 5.0 | **51.0** | 6.9 |
| clean, γ − 0.3 | 11.3 | 1116.7 | 7.3 | 35.3 | 20.0 |
| clean, γ + 0.3 | 4.4 | 208.3 | 4.1 | 4.4 | 3.2 |
| loose, γ − 0.3 | 24.9 | 1191.5 | 10.8 | 70.1 | 29.2 |
| loose, γ + 0.3 | 12.7 | 742.8 | 5.8 | 55.9 | 14.6 |

Once the 2–5 kAU offset is removed:
- N, E and P (Newton / EFE / nesting) fit.
- S (Form-2 screen) is disfavoured in the loose cut in every γ variant (51–70).

This is a lean, not a verdict, because the anchoring was chosen after seeing the data.

## What this means for the fish idea `[O]`
- The binary-as-its-own-system reading ("system = gravitationally bound", model F) is dead in Gaia.
- The surviving readings are the ones where a wide binary feels Newtonian inside, with the boost suppressed to the percent level:
  - nesting (P: passenger of the dominant field);
  - EFE;
  - plain Newton.
- Form-2 screening (S ≈ 0.2 at the Sun) predicts a 7–17% rise at 10–30 kAU. Clean data allow it; the loose cut, after re-anchoring, does not.
- Next test to separate P from S cleanly: model the 2–5 kAU systematic (Hwang+2022 γ(s) with its errors, a triple fraction rising with s), raise NMC, and rerun the pre-registered statistic.
